import {
  catalogueMeta,
  cataloguePayload,
  getAllSchemes,
  isCatalogueStale,
  jsonWithSecurity,
  schemeCount,
} from "@/lib/matching";
import { readFileSync, existsSync } from "fs";
import { join } from "path";

export const runtime = "nodejs";

function opsAllowed(request: Request): boolean {
  const token = (process.env.OPS_DASHBOARD_TOKEN || "").trim();
  if (token) {
    const auth = (request.headers.get("authorization") || "").trim();
    if (auth.toLowerCase().startsWith("bearer ") && auth.slice(7).trim() === token) {
      return true;
    }
    const alt = (request.headers.get("x-ops-token") || "").trim();
    return alt === token;
  }
  const show = (process.env.NEXT_PUBLIC_SHOW_OPS || "").trim().toLowerCase();
  return show === "1" || show === "true" || show === "yes";
}

function loadJson(candidates: string[]): Record<string, unknown> | null {
  for (const path of candidates) {
    try {
      if (!existsSync(path)) continue;
      return JSON.parse(readFileSync(path, "utf8")) as Record<string, unknown>;
    } catch {
      /* try next */
    }
  }
  return null;
}

function dataCandidates(name: string): string[] {
  const cwd = process.cwd();
  return [
    join(cwd, "data", name),
    join(cwd, "..", "data", name),
    join(cwd, "frontend", "data", name),
  ];
}


function loadUrlTicketsSummary(): {
  open_count: number;
  by_status: Record<string, number>;
  unique_tickets: number;
  rows_total: number;
} {
  const cwd = process.cwd();
  const candidates = [
    join(cwd, "data", "url_tickets.jsonl"),
    join(cwd, "..", "data", "url_tickets.jsonl"),
    join(cwd, "frontend", "data", "url_tickets.jsonl"),
  ];
  let raw = "";
  for (const p of candidates) {
    try {
      if (existsSync(p)) {
        raw = readFileSync(p, "utf8");
        break;
      }
    } catch {
      /* next */
    }
  }
  const byKey = new Map<string, Record<string, unknown>>();
  for (const line of raw.split("\n")) {
    const t = line.trim();
    if (!t) continue;
    try {
      const row = JSON.parse(t) as Record<string, unknown>;
      const key = `${row.scheme_id || ""}|${row.url || ""}`;
      byKey.set(key, row);
    } catch {
      /* skip */
    }
  }
  const by_status: Record<string, number> = {};
  for (const row of byKey.values()) {
    const st = String(row.status || "unknown");
    by_status[st] = (by_status[st] || 0) + 1;
  }
  const open_count = (by_status.open || 0) + (by_status.investigating || 0);
  return { open_count, by_status, unique_tickets: byKey.size, rows_total: raw ? raw.split("\n").filter(Boolean).length : 0 };
}

function loadCandidatesSummary(): {
  total: number;
  by_status: Record<string, number>;
  queued: number;
  researching: number;
  deferred: number;
  verified_add: number;
  rejected: number;
} {
  const raw = loadJson(dataCandidates("catalogue_candidates.json"));
  const list = Array.isArray(raw?.candidates)
    ? (raw!.candidates as Record<string, unknown>[])
    : Array.isArray(raw)
      ? (raw as Record<string, unknown>[])
      : [];
  const by_status: Record<string, number> = {};
  for (const c of list) {
    if (!c || typeof c !== "object") continue;
    const st = String((c as { status?: string }).status || "unknown");
    by_status[st] = (by_status[st] || 0) + 1;
  }
  return {
    total: list.length,
    by_status,
    queued: by_status.queued || 0,
    researching: by_status.researching || 0,
    deferred: by_status.deferred || 0,
    verified_add: by_status.verified_add || 0,
    rejected: by_status.rejected || 0,
  };
}

function loadPacksSummary(): {
  pack_count: number;
  default_version?: string;
  index_generated_at?: string;
} {
  const cwd = process.cwd();
  const candidates = [
    join(cwd, "data", "packs", "index.json"),
    join(cwd, "..", "data", "packs", "index.json"),
    join(cwd, "frontend", "data", "packs", "index.json"),
  ];
  const idx = loadJson(candidates);
  if (!idx) return { pack_count: 0 };
  return {
    pack_count: Number(idx.pack_count || (Array.isArray(idx.packs) ? idx.packs.length : 0)),
    default_version: typeof idx.default_version === "string" ? idx.default_version : undefined,
    index_generated_at: typeof idx.generated_at === "string" ? idx.generated_at : undefined,
  };
}


export async function GET(request: Request) {
  if (!opsAllowed(request)) {
    return jsonWithSecurity(
      {
        error: {
          code: "ops_unauthorized",
          message:
            "Set NEXT_PUBLIC_SHOW_OPS=1 for demo, or send Authorization: Bearer <OPS_DASHBOARD_TOKEN>.",
        },
      },
      { status: 401 },
    );
  }

  const schemes = getAllSchemes();
  let verifyTrue = 0;
  const byCountry: Record<string, number> = {
    "India / other": 0,
    "United States": 0,
    "United Kingdom": 0,
    "Neighbours (BD/NP/LK/MV)": 0,
  };
  for (const s of schemes) {
    const tags = (s.tags || []).map((x) => String(x).toLowerCase());
    const er = (s.eligibility_rules || {}) as { verify?: boolean };
    if (er.verify) verifyTrue += 1;
    if (tags.includes("united_states") || tags.includes("united-states")) {
      byCountry["United States"] += 1;
    } else if (tags.includes("united_kingdom") || /^gb-/.test(String(s.id || ""))) {
      byCountry["United Kingdom"] += 1;
    } else if (
      tags.some((t) => ["bangladesh", "nepal", "sri-lanka", "maldives"].includes(t)) ||
      /^(bd|np|lk|mv)-/.test(String(s.id || ""))
    ) {
      byCountry["Neighbours (BD/NP/LK/MV)"] += 1;
    } else {
      byCountry["India / other"] += 1;
    }
  }

  const freshness = cataloguePayload();
  const release = loadJson(dataCandidates("catalogue_release.json")) || {};
  const urlHealth = loadJson(dataCandidates("url_health_snapshot.json"));

  const api = (process.env.NEXT_PUBLIC_API_URL || "").trim().replace(/\/$/, "");
  if (api) {
    try {
      const headers: Record<string, string> = { Accept: "application/json" };
      const token = (process.env.OPS_DASHBOARD_TOKEN || "").trim();
      if (token) headers.Authorization = `Bearer ${token}`;
      const r = await fetch(`${api}/api/v1/ops/summary`, { headers, cache: "no-store" });
      if (r.ok) {
        return jsonWithSecurity(await r.json());
      }
    } catch {
      /* fall through to local summary */
    }
  }

  const urlTickets = loadUrlTicketsSummary();
  const candidates = loadCandidatesSummary();
  const packs = loadPacksSummary();

  return jsonWithSecurity({
    scheme_count: schemeCount(),
    updated_as_of: catalogueMeta.updated_as_of || release.updated_as_of,
    schemes_sha256: release.schemes_sha256,
    is_stale: isCatalogueStale(),
    stale_after_days: catalogueMeta.stale_after_days ?? 30,
    release_generated_at: release.generated_at,
    verify_true_count: verifyTrue,
    verify_false_count: Math.max(0, schemes.length - verifyTrue),
    coverage: { by_country: byCountry },
    url_health: {
      generated_at: urlHealth?.generated_at,
      note: urlHealth?.note,
      flaky_hosts: Array.isArray(urlHealth?.flaky_hosts) ? urlHealth.flaky_hosts : [],
      checked_count: urlHealth?.checked_count,
      ok_count: urlHealth?.ok_count,
      open_url_tickets: urlTickets.open_count,
    },
    url_tickets: urlTickets,
    candidates,
    packs,
    analytics: {
      note: "Aggregates only — never used for eligibility. Use FastAPI /ops/summary for live counters when API is deployed.",
      match_volume_24h: null,
    },
    trust_checklist_doc: "docs/TRUST.md",
    product_doc: "docs/PRODUCT.md",
    catalogue_ops_doc: "docs/CATALOGUE_OPS.md",
    catalogue: freshness.catalogue,
  });
}
