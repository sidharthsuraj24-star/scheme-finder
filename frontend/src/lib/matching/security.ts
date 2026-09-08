/** In-memory sliding-window rate limit + body size helpers for Next.js API routes. */

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

export function allowMatchRequest(ip: string): boolean {
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
