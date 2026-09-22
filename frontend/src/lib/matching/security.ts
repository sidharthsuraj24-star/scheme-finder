/** Rate limit + body size helpers for Next.js API routes.
 *
 * Backend: in-memory sliding window by default.
 * When UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN are set, uses Upstash
 * REST (INCR + EXPIRE) so limits work across Vercel instances. On Upstash
 * failure, falls back to memory so the demo never hard-dies.
 */

import { MAX_BODY_BYTES, RATE_LIMIT_MAX, RATE_LIMIT_WINDOW_SEC } from "./types";

type HitBucket = number[];

const globalStore = globalThis as typeof globalThis & {
  __schemeFinderRateHits?: Map<string, HitBucket>;
};

function hitsMap(): Map<string, HitBucket> {
  if (!globalStore.__schemeFinderRateHits) {
    globalStore.__schemeFinderRateHits = new Map();
  }
  return globalStore.__schemeFinderRateHits;
}

export function clientIp(request: Request): string {
  const forwarded = request.headers.get("x-forwarded-for");
  if (forwarded) {
    return forwarded.split(",")[0]?.trim() || "unknown";
  }
  const real = request.headers.get("x-real-ip");
  if (real) return real.trim() || "unknown";
  return "unknown";
}

function upstashConfigured(): boolean {
  return Boolean(
    process.env.UPSTASH_REDIS_REST_URL?.trim() &&
      process.env.UPSTASH_REDIS_REST_TOKEN?.trim(),
  );
}

function allowMatchRequestMemory(ip: string): boolean {
  const maxReq = Number(process.env.RATE_LIMIT_MAX || RATE_LIMIT_MAX);
  const windowSec = Number(process.env.RATE_LIMIT_WINDOW_SEC || RATE_LIMIT_WINDOW_SEC);
  const now = Date.now() / 1000;
  const map = hitsMap();
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

export function securityHeaders(init?: ResponseInit): Headers {
  const h = new Headers(init?.headers);
  h.set("X-Content-Type-Options", "nosniff");
  h.set("X-Frame-Options", "DENY");
  h.set("Referrer-Policy", "no-referrer");
  h.set("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'; base-uri 'none'");
  h.set("X-XSS-Protection", "0");
  return h;
}

export function jsonWithSecurity(data: unknown, init?: ResponseInit): Response {
  const headers = securityHeaders(init);
  headers.set("Content-Type", "application/json");
  return new Response(JSON.stringify(data), {
    ...init,
    headers,
  });
}
