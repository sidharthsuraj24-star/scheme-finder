import { jsonWithSecurity } from "@/lib/matching";

export const runtime = "nodejs";

const ALLOWED = new Set(["match_ok", "match_error", "share_copy", "ops_view"]);

/** In-process demo counters when FastAPI is not the host (Vercel same-origin). */
const memory: Record<string, number> = Object.create(null);

function day(): string {
  return new Date().toISOString().slice(0, 10);
}

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
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
  const country =
    typeof o.country === "string" && o.country.trim()
      ? o.country.trim().slice(0, 64)
      : "unknown";
  const key = `${day()}:event:${event}:country:${country}`;
  memory[key] = (memory[key] || 0) + 1;
  if (typeof o.result_count === "number" && Number.isFinite(o.result_count)) {
    const n = Math.max(0, Math.floor(o.result_count));
    let bucket = "31+";
    if (n === 0) bucket = "0";
    else if (n <= 3) bucket = "1-3";
    else if (n <= 10) bucket = "4-10";
    else if (n <= 30) bucket = "11-30";
    const bk = `${day()}:event:${event}:bucket:${bucket}`;
    memory[bk] = (memory[bk] || 0) + 1;
  }
  if (Array.isArray(o.scheme_ids)) {
    for (const sid of o.scheme_ids.slice(0, 10)) {
      if (typeof sid !== "string" || !sid.trim() || sid.length > 64) continue;
      const sk = `${day()}:scheme:${sid.trim()}`;
      memory[sk] = (memory[sk] || 0) + 1;
    }
  }
  // Optional forward to dedicated FastAPI when configured.
  const api = (process.env.NEXT_PUBLIC_API_URL || "").trim().replace(/\/$/, "");
  if (api) {
    try {
      await fetch(`${api}/api/v1/analytics/event`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(o),
      });
    } catch {
      /* fail open — local memory already updated */
    }
  }
  return jsonWithSecurity({ ok: true, backend: api ? "forward+memory" : "memory" });
}

/** Test/ops helper — not public docs; returns aggregates only. */
export function __memorySnapshotForTests(): Record<string, number> {
  return { ...memory };
}
