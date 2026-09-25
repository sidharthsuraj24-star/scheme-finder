import {
  allowRequest,
  checkContentLength,
  clientIp,
  jsonWithSecurity,
  readBodyLimited,
} from "@/lib/matching";

export const runtime = "nodejs";

const ALLOWED = new Set(["match_ok", "match_error", "share_copy", "ops_view"]);

/** Analytics payloads are tiny; anything bigger is abuse. */
const MAX_ANALYTICS_BYTES = 4 * 1024;
const MAX_MEMORY_KEYS = 5_000;
const COUNTRY_RE = /^[A-Za-z][A-Za-z .()/-]{0,63}$/;
const SCHEME_ID_RE = /^[a-z0-9][a-z0-9_-]{0,63}$/;

/** In-process demo counters when FastAPI is not the host (Vercel same-origin). */
const memory: Record<string, number> = Object.create(null);
let memoryKeys = 0;

function bump(key: string): void {
  if (!(key in memory)) {
    if (memoryKeys >= MAX_MEMORY_KEYS) return; // bounded: drop new keys once full
    memoryKeys += 1;
  }
  memory[key] = (memory[key] || 0) + 1;
}

function day(): string {
  return new Date().toISOString().slice(0, 10);
}

export async function POST(request: Request) {
  const sizeErr = checkContentLength(request);
  if (sizeErr) {
    return jsonWithSecurity(
      { error: { code: "payload_too_large", message: "Request body too large" } },
      { status: 413 },
    );
  }
  if (!allowRequest("analytics", clientIp(request), Number(process.env.ANALYTICS_RATE_LIMIT_MAX || 60), 60)) {
    return jsonWithSecurity(
      { error: { code: "rate_limited", message: "Too many requests; try again shortly." } },
      { status: 429, headers: { "Retry-After": "60" } },
    );
  }
  let body: unknown;
  try {
    const raw = await readBodyLimited(request, MAX_ANALYTICS_BYTES);
    if (raw === null) {
      return jsonWithSecurity(
        { error: { code: "payload_too_large", message: "Request body too large" } },
        { status: 413 },
      );
    }
    body = JSON.parse(raw);
  } catch {
    return jsonWithSecurity(
      { error: { code: "invalid_json", message: "Expected JSON body" } },
      { status: 400 },
    );
  }
  if (body == null || typeof body !== "object" || Array.isArray(body)) {
    return jsonWithSecurity(
      { error: { code: "invalid_body", message: "Expected object" } },
      { status: 400 },
    );
  }
  const o = body as Record<string, unknown>;
  const event = typeof o.event === "string" ? o.event : "";
  if (!ALLOWED.has(event)) {
    return jsonWithSecurity(
      { error: { code: "invalid_event", message: "Unknown analytics event" } },
      { status: 400 },
    );
  }
  const countryRaw = typeof o.country === "string" ? o.country.trim() : "";
  const country = COUNTRY_RE.test(countryRaw) ? countryRaw : "unknown";
  const key = `${day()}:event:${event}:country:${country}`;
  bump(key);
  let resultCount: number | undefined;
  if (typeof o.result_count === "number" && Number.isFinite(o.result_count)) {
    const n = Math.min(100_000, Math.max(0, Math.floor(o.result_count)));
    resultCount = n;
    let bucket = "31+";
    if (n === 0) bucket = "0";
    else if (n <= 3) bucket = "1-3";
    else if (n <= 10) bucket = "4-10";
    else if (n <= 30) bucket = "11-30";
    bump(`${day()}:event:${event}:bucket:${bucket}`);
  }
  const schemeIds: string[] = [];
  if (Array.isArray(o.scheme_ids)) {
    for (const sid of o.scheme_ids.slice(0, 10)) {
      if (typeof sid !== "string" || !SCHEME_ID_RE.test(sid)) continue;
      schemeIds.push(sid);
      bump(`${day()}:scheme:${sid}`);
    }
  }
  // Optional forward to dedicated FastAPI when configured.
  const api = (process.env.NEXT_PUBLIC_API_URL || "").trim().replace(/\/$/, "");
  if (api) {
    try {
      await fetch(`${api}/api/v1/analytics/event`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        // Forward only the validated fields, never the raw client payload.
        body: JSON.stringify({
          event,
          country,
          ...(resultCount !== undefined ? { result_count: resultCount } : {}),
          scheme_ids: schemeIds,
        }),
        signal: AbortSignal.timeout(3000),
      });
    } catch {
      /* fail open — local memory already updated */
    }
  }
  return jsonWithSecurity({ ok: true, backend: api ? "forward+memory" : "memory" });
}
