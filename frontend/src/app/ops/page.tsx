"use client";

import { useEffect, useState } from "react";

type OpsSummary = {
  scheme_count?: number;
  updated_as_of?: string;
  schemes_sha256?: string;
  is_stale?: boolean;
  verify_true_count?: number;
  verify_false_count?: number;
  coverage?: { by_country?: Record<string, number> };
  url_health?: {
    generated_at?: string;
    note?: string;
    flaky_hosts?: { host?: string; status?: string; scheme_id?: string }[];
    checked_count?: number;
    ok_count?: number;
    open_url_tickets?: number;
  };
  url_tickets?: {
    open_count?: number;
    by_status?: Record<string, number>;
  };
  candidates?: {
    total?: number;
    by_status?: Record<string, number>;
    queued?: number;
    deferred?: number;
  };
  packs?: {
    pack_count?: number;
    default_version?: string;
  };
  analytics?: {
    match_volume?: number;
    match_volume_24h?: number | null;
    by_country?: Record<string, number>;
    top_scheme_ids?: { scheme_id: string; hits: number }[];
    note?: string;
  };
  trust_checklist_doc?: string;
  catalogue_ops_doc?: string;
  error?: { code?: string; message?: string };
};

export default function OpsPage() {
  const [data, setData] = useState<OpsSummary | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [token, setToken] = useState("");

  const load = async (bearer?: string) => {
    setErr(null);
    try {
      const headers: Record<string, string> = { Accept: "application/json" };
      const t = (bearer ?? token).trim();
      if (t) headers.Authorization = `Bearer ${t}`;
      const r = await fetch("/api/ops/summary", { headers, cache: "no-store" });
      const body = (await r.json()) as OpsSummary;
      if (!r.ok) {
        setErr(body?.error?.message || `HTTP ${r.status}`);
        setData(null);
        return;
      }
      setData(body);
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
      setData(null);
    }
  };

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main id="main-content" className="mx-auto max-w-2xl space-y-4 px-1 py-4" tabIndex={-1}>
      <header>
        <h1 className="text-2xl font-extrabold text-slate-900">Ops dashboard</h1>
        <p className="mt-1 text-sm text-slate-600">
          Read-only catalogue / URL tickets / candidates / packs / analytics. No CMS publisher UI. No
          PII. Phase 4 foundation — not Phase 4 complete.
        </p>
      </header>

      <div className="flex flex-col gap-2 rounded-xl border border-slate-200 bg-white p-3 sm:flex-row">
        <input
          type="password"
          className="min-h-tap flex-1 rounded-lg border border-slate-300 px-3 text-sm"
          placeholder="OPS_DASHBOARD_TOKEN (if required)"
          value={token}
          onChange={(e) => setToken(e.target.value)}
        />
        <button
          type="button"
          className="min-h-tap rounded-lg bg-slate-800 px-4 text-sm font-bold text-white"
          onClick={() => void load()}
        >
          Refresh
        </button>
      </div>

      {err ? (
        <p className="rounded-xl border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-950" role="alert">
          {err}
          <span className="mt-1 block text-xs">
            Demo: set <code>NEXT_PUBLIC_SHOW_OPS=1</code>. Locked: set{" "}
            <code>OPS_DASHBOARD_TOKEN</code> and paste it above.
          </span>
        </p>
      ) : null}

      {data ? (
        <div className="space-y-3 text-sm">
          <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-bold text-slate-900">Catalogue</h2>
            <ul className="mt-2 space-y-1 text-slate-700">
              <li>
                <strong>scheme_count:</strong> {data.scheme_count ?? "—"}
              </li>
              <li>
                <strong>updated_as_of:</strong> {data.updated_as_of ?? "—"}
              </li>
              <li>
                <strong>schemes_sha256:</strong>{" "}
                <code className="break-all text-xs">{data.schemes_sha256 ?? "—"}</code>
              </li>
              <li>
                <strong>stale:</strong> {data.is_stale ? "yes" : "no"}
              </li>
              <li>
                <strong>verify:true:</strong> {data.verify_true_count ?? "—"} ·{" "}
                <strong>verify:false:</strong> {data.verify_false_count ?? "—"}
              </li>
            </ul>
            {data.coverage?.by_country ? (
              <div className="mt-2">
                <p className="font-semibold">Coverage</p>
                <ul className="list-inside list-disc">
                  {Object.entries(data.coverage.by_country).map(([k, v]) => (
                    <li key={k}>
                      {k}: {v}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
            <p className="mt-3 text-xs text-slate-500">
              Publish checklist: <code>{data.trust_checklist_doc || "docs/TRUST.md"}</code>
              {" · "}
              Ops: <code>{data.catalogue_ops_doc || "docs/CATALOGUE_OPS.md"}</code>
            </p>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-bold text-slate-900">URL tickets</h2>
            <p className="mt-1 text-slate-700">
              <strong>open:</strong>{" "}
              {data.url_tickets?.open_count ?? data.url_health?.open_url_tickets ?? "—"}
            </p>
            {data.url_tickets?.by_status ? (
              <ul className="mt-1 list-inside list-disc text-xs">
                {Object.entries(data.url_tickets.by_status).map(([k, v]) => (
                  <li key={k}>
                    {k}: {v}
                  </li>
                ))}
              </ul>
            ) : null}
            <p className="mt-2 text-xs text-slate-500">
              Append-only <code>data/url_tickets.jsonl</code> — list via{" "}
              <code>scripts/list_url_tickets.py</code>
            </p>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-bold text-slate-900">Candidate queue</h2>
            <p className="mt-1 text-slate-700">
              total {data.candidates?.total ?? "—"} · queued {data.candidates?.queued ?? "—"} ·
              deferred {data.candidates?.deferred ?? "—"}
            </p>
            {data.candidates?.by_status ? (
              <ul className="mt-1 list-inside list-disc text-xs">
                {Object.entries(data.candidates.by_status).map(([k, v]) => (
                  <li key={k}>
                    {k}: {v}
                  </li>
                ))}
              </ul>
            ) : null}
            <p className="mt-2 text-xs text-slate-500">
              Never invent eligibility. Feed from daily freshness / human paste — see{" "}
              <code>docs/CATALOGUE_OPS.md</code>
            </p>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-bold text-slate-900">Packs</h2>
            <p className="mt-1 text-slate-700">
              <strong>pack_count:</strong> {data.packs?.pack_count ?? "—"}
              {data.packs?.default_version ? ` · version ${data.packs.default_version}` : ""}
            </p>
            <p className="mt-2 text-xs text-slate-500">
              Membership manifests in <code>data/packs/</code> — regenerate with{" "}
              <code>scripts/generate_pack_manifests.py</code>
            </p>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-bold text-slate-900">URL health</h2>
            <p className="mt-1 text-xs text-slate-500">{data.url_health?.note}</p>
            <p className="mt-1 text-slate-700">
              Generated: {String(data.url_health?.generated_at || "—")} · checked{" "}
              {String(data.url_health?.checked_count ?? "—")} · ok{" "}
              {String(data.url_health?.ok_count ?? "—")}
            </p>
            {(data.url_health?.flaky_hosts || []).length === 0 ? (
              <p className="mt-2 text-slate-500">No flaky hosts in snapshot.</p>
            ) : (
              <ul className="mt-2 max-h-48 space-y-1 overflow-y-auto text-xs">
                {(data.url_health?.flaky_hosts || []).map((h, i) => (
                  <li key={`${h.host}-${i}`} className="rounded bg-slate-50 px-2 py-1">
                    <strong>{h.host || "host"}</strong> — {h.status}{" "}
                    {h.scheme_id ? `(${h.scheme_id})` : ""}
                  </li>
                ))}
              </ul>
            )}
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h2 className="font-bold text-slate-900">Analytics (aggregates)</h2>
            <p className="mt-1 text-xs text-slate-500">{data.analytics?.note}</p>
            <p className="mt-2">
              match_volume_24h:{" "}
              {data.analytics?.match_volume_24h ?? data.analytics?.match_volume ?? "—"}
            </p>
            {data.analytics?.by_country ? (
              <ul className="mt-1 list-inside list-disc">
                {Object.entries(data.analytics.by_country).map(([k, v]) => (
                  <li key={k}>
                    {k}: {v}
                  </li>
                ))}
              </ul>
            ) : null}
            {(data.analytics?.top_scheme_ids || []).length ? (
              <ul className="mt-2 text-xs">
                {data.analytics!.top_scheme_ids!.map((s) => (
                  <li key={s.scheme_id}>
                    {s.scheme_id}: {s.hits}
                  </li>
                ))}
              </ul>
            ) : null}
          </section>
        </div>
      ) : null}
    </main>
  );
}
