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
    "Neighbours (BD/NP/LK/MV)": 0,
  };
  for (const s of schemes) {
    const tags = (s.tags || []).map((x) => String(x).toLowerCase());
    const er = (s.eligibility_rules || {}) as { verify?: boolean };
    if (er.verify) verifyTrue += 1;
    if (tags.includes("united_states") || tags.includes("united-states")) {
      byCountry["United States"] += 1;
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
    },
    analytics: {
      note: "Aggregates only — never used for eligibility. Use FastAPI /ops/summary for live counters when API is deployed.",
      match_volume_24h: null,
    },
    trust_checklist_doc: "docs/TRUST.md",
    product_doc: "docs/PRODUCT.md",
    catalogue: freshness.catalogue,
  });
}
