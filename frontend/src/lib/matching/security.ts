/** Rate limit + body size helpers for Next.js API routes.
 *
 * Backend: in-memory sliding window by default.
 * When UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN are set, uses Upstash
 * REST (INCR + EXPIRE) so limits work across Vercel instances. On Upstash
 * failure, falls back to memory so the demo never hard-dies.
 */

import { createHash, timingSafeEqual } from "node:crypto";
import { MAX_BODY_BYTES, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_SEC } from "./types";
import { API_CSP, STATIC_SECURITY_HEADERS } from "../securityHeaders.mjs";

type HitBucket = number[];

const globalStore = globalThis as typeof globalThis & {
  __schemeFinderRateHits?: Map<string, HitBucket>;
};

/** Hard cap on tracked keys so unique-IP floods cannot grow memory unbounded. */
const MAX_TRACKED_KEYS = 10_000;

function hitsMap(): Map<string, HitBucket> {
  if (!globalStore.__schemeFinderRateHits) {
    globalStore.__schemeFinderRateHits = new Map();
  }
  return globalStore.__schemeFinderRateHits;
}

function pruneHits(map: Map<string, HitBucket>, cutoff: number): void {
  if (map.size < MAX_TRACKED_KEYS) return;
  for (const [k, q] of map) {
    if (!q.length || q[q.length - 1] < cutoff) map.delete(k);
  }
  // Still too big (active flood): drop oldest insertion-order entries.
  while (map.size >= MAX_TRACKED_KEYS) {
    const first = map.keys().next().value;
    if (first === undefined) break;
    map.delete(first);
  }
}

/**
 * Client IP for rate limiting. On Vercel, x-forwarded-for / x-real-ip are set
 * by the platform edge (client-supplied values are overwritten), so the first
 * hop is trustworthy there. Self-hosted deployments must sit behind a proxy
 * that does the same, otherwise the header is spoofable.
 */
export function clientIp(request: Request): string {
  const vercel = request.headers.get("x-vercel-forwarded-for");
  const forwarded = vercel || request.headers.get("x-forwarded-for");
  if (forwarded) {
    return forwarded.split(",")[0]?.trim().slice(0, 64) || "unknown";
  }
  const real = request.headers.get("x-real-ip");
  if (real) return real.trim().slice(0, 64) || "unknown";
  return "unknown";
}

function upstashConfigured(): boolean {
  return Boolean(
    process.env.UPSTASH_REDIS_REST_URL?.trim() &&
      process.env.UPSTASH_REDIS_REST_TOKEN?.trim(),
  );
}

function allowMatchRequestMemory(
  ip: string,
  maxReq = Number(process.env.RATE_LIMIT_MAX || RATE_LIMIT_MAX),
  windowSec = Number(process.env.RATE_LIMIT_WINDOW_SEC || RATE_LIMIT_WINDOW_SEC),
): boolean {
  const now = Date.now() / 1000;
  const map = hitsMap();
  pruneHits(map, now - windowSec);
  const q = (map.get(ip) || []).filter((t) => t >= now - windowSec);
  if (q.length >= maxReq) {
    map.set(ip, q);
    return false;
  }
  q.push(now);
  map.set(ip, q);
  return true;
}

async function allowMatchRequestUpstash(ip: string): Promise<boolean | null> {
  const base = process.env.UPSTASH_REDIS_REST_URL!.trim().replace(/\/$/, "");
  const token = process.env.UPSTASH_REDIS_REST_TOKEN!.trim();
  const maxReq = Number(process.env.RATE_LIMIT_MAX || RATE_LIMIT_MAX);
  const windowSec = Number(process.env.RATE_LIMIT_WINDOW_SEC || RATE_LIMIT_WINDOW_SEC);
  const bucket = Math.floor(Date.now() / 1000 / Math.max(1, Math.floor(windowSec)));
  const key = `sf:rl:${ip}:${bucket}`;

  try {
    // Pipeline: INCR then EXPIRE (only meaningful on first hit; harmless otherwise)
    const res = await fetch(`${base}/pipeline`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify([
        ["INCR", key],
        ["EXPIRE", key, String(Math.floor(windowSec) + 1)],
      ]),
      cache: "no-store",
    });
    if (!res.ok) return null;
    const data = (await res.json()) as Array<{ result?: number | string }>;
    const count = Number(data?.[0]?.result ?? NaN);
    if (!Number.isFinite(count)) return null;
    return count <= maxReq;
  } catch {
    return null;
  }
}

/** Sync memory path kept for callers that do not await (tests / legacy). */
export function allowMatchRequestSync(ip: string): boolean {
  return allowMatchRequestMemory(ip);
}

/**
 * Async-capable rate limit: Upstash REST when configured, else memory.
 * Prefer awaiting this from route handlers.
 */
export async function allowMatchRequest(ip: string): Promise<boolean> {
  if (upstashConfigured()) {
    const result = await allowMatchRequestUpstash(ip);
    if (result !== null) return result;
    // Fail-to-memory when Upstash briefly unavailable.
  }
  return allowMatchRequestMemory(ip);
}

/**
 * Generic per-IP limiter for other routes (analytics, ops auth). Memory only:
 * per-instance on serverless, which is enough to blunt casual abuse / token
 * guessing; use Upstash-backed match limits for cross-instance guarantees.
 */
export function allowRequest(bucket: string, ip: string, max: number, windowSec = 60): boolean {
  return allowMatchRequestMemory(`${bucket}:${ip}`, max, windowSec);
}

export function rateLimitWindowSec(): number {
  return Number(process.env.RATE_LIMIT_WINDOW_SEC || RATE_LIMIT_WINDOW_SEC);
}

export function maxBodyBytes(): number {
  return Number(process.env.MAX_BODY_BYTES || MAX_BODY_BYTES);
}

export function checkContentLength(request: Request): Response | null {
  const limit = maxBodyBytes();
  const cl = request.headers.get("content-length");
  if (cl != null) {
    const n = Number(cl);
    if (!Number.isFinite(n)) {
      return Response.json(
        { error: { code: "bad_content_length", message: "Invalid Content-Length header" } },
        { status: 400 },
      );
    }
    if (n > limit) {
      return Response.json(
        {
          error: {
            code: "payload_too_large",
            message: `Request body exceeds ${limit} bytes`,
          },
        },
        { status: 413 },
      );
    }
  }
  return null;
}

/**
 * Read a request body as text with a hard byte cap, even when the client uses
 * chunked transfer encoding / omits or lies about Content-Length.
 * Returns null when the cap is exceeded.
 */
export async function readBodyLimited(request: Request, limit = maxBodyBytes()): Promise<string | null> {
  if (!request.body) return "";
  const reader = request.body.getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > limit) {
      try {
        await reader.cancel();
      } catch {
        /* ignore */
      }
      return null;
    }
    chunks.push(value);
  }
  const buf = new Uint8Array(total);
  let off = 0;
  for (const c of chunks) {
    buf.set(c, off);
    off += c.byteLength;
  }
  return new TextDecoder("utf-8", { fatal: false }).decode(buf);
}

/** Constant-time string comparison (hash both sides so lengths never leak). */
export function safeEqual(a: string, b: string): boolean {
  const ha = createHash("sha256").update(a, "utf8").digest();
  const hb = createHash("sha256").update(b, "utf8").digest();
  return timingSafeEqual(ha, hb) && a.length === b.length;
}

/**
 * /ops gate. With OPS_DASHBOARD_TOKEN set, require it via
 * `Authorization: Bearer` or `X-Ops-Token` (headers only — never the URL, and
 * never logged). Without a token, allow only when NEXT_PUBLIC_SHOW_OPS is on.
 */
export function opsAuthorized(request: Request): boolean {
  const token = (process.env.OPS_DASHBOARD_TOKEN || "").trim();
  if (token) {
    const auth = (request.headers.get("authorization") || "").trim();
    let presented = "";
    if (auth.toLowerCase().startsWith("bearer ")) presented = auth.slice(7).trim();
    else presented = (request.headers.get("x-ops-token") || "").trim();
    if (!presented) return false;
    return safeEqual(presented, token);
  }
  const show = (process.env.NEXT_PUBLIC_SHOW_OPS || "").trim().toLowerCase();
  return show === "1" || show === "true" || show === "yes";
}

export function securityHeaders(init?: ResponseInit): Headers {
  const h = new Headers(init?.headers);
  for (const { key, value } of STATIC_SECURITY_HEADERS as { key: string; value: string }[]) {
    if (!h.has(key)) h.set(key, value);
  }
  h.set("Content-Security-Policy", API_CSP);
  h.set("X-XSS-Protection", "0");
  // API responses may contain profile-derived data or ops metrics: never cache.
  if (!h.has("Cache-Control")) h.set("Cache-Control", "no-store");
  return h;
}

export function jsonWithSecurity(data: unknown, init?: ResponseInit): Response {
  const headers = securityHeaders(init);
  headers.set("Content-Type", "application/json; charset=utf-8");
  return new Response(JSON.stringify(data), {
    ...init,
    headers,
  });
}
