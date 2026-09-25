# Catalogue ops — Phase 4 foundation

**Date:** 2026-09-24 (IST)  
**Status:** Ops **data plane** foundation shipped — **not** Phase 4 complete.  
No full human CMS, no pager, no claim of 500k scale.

Never invent scheme eligibility. Official sources only. Dual-tree
`data/schemes.json` ↔ `frontend/data/schemes.json` must stay identical.

## What this slice adds

| Piece | Path / script | Purpose |
|-------|----------------|---------|
| Human-verify candidate queue | `data/catalogue_candidates.json` | Statused queue before catalogue add |
| List / update candidates | `scripts/list_catalogue_candidates.py`, `scripts/update_catalogue_candidate.py` | Transitions + audit via `append_catalogue_audit.py` |
| URL ticket queue | `data/url_tickets.jsonl` | Append-only tickets for DNS/404/5xx/SSL |
| Ticket list | `scripts/list_url_tickets.py` | Latest open/investigating/fixed view |
| Health → tickets | `scripts/write_url_health_snapshot.py` | Upserts failures; fixes on recovery |
| Versioned packs | `data/packs/*@1.0.0.json` + `index.json` | Membership manifests by state/country |
| Pack generator | `scripts/generate_pack_manifests.py` | Derive ids from scheme tags |
| Resolve ticket | `scripts/resolve_url_ticket.py` | Mark a ticket fixed after a URL fix (+ frontend sync) |
| Ops dashboard | `/ops`, `/ops/summary` | Open tickets, candidate counts, pack count |

## 1. Human-verify candidate queue

Schema (each row in `candidates[]`):

- `id`, `name`, `country`, `official_source_url`
- `status`: `queued` \| `researching` \| `verified_add` \| `rejected` \| `deferred`
- `reason`, `noted_at`, `actor`, `notes`
- optional `scheme_id_if_present` when already curated

**Honesty:** Historical India leftovers (PM-KMY, PM-SYM, NAMASTE) are already in
`schemes.json` (`in-pm-kmy`, `in-pm-sym`, `in-namaste`). Phase 4 seeds **deferred**
documentation rows only — open queue may be empty. That is intentional.

### Daily freshness → candidates

External daily freshness (~**6:09 AM IST**) already runs outside this slice.
Enhance the human loop as:

1. Run / read freshness report (`scripts/scheme_freshness_check.py`, optional URL probes).
2. For a **new** programme name found on an official portal that is **not** in
   `schemes.json`, paste a candidate:
   ```bash
   python3 scripts/update_catalogue_candidate.py --add \
     --id cand-in-example --name "Official name" --country India \
     --official-source-url "https://example.gov.in/..." \
     --status queued --reason "Seen on MyScheme listing YYYY-MM-DD"
   ```
3. Research → `researching`; after human verify against the official page,
   either open a PR to add the scheme (`verified_add` is a **queue signal only** —
   this script never writes eligibility into `schemes.json`) or `rejected` /
   `deferred`.
4. Never invent income caps, ages, or category lists to clear the queue.

## 2. URL probe → ticket queue

Append-only JSONL fields: `ticket_id`, `scheme_id`, `url`, `status`
(`open` \| `investigating` \| `fixed` \| `wontfix`), `http_or_error`,
`first_seen`, `last_seen`, `notes`.

```bash
# Default: empty snapshot (no live probes)
python3 scripts/write_url_health_snapshot.py

# Short known-flaky probe (max ~3 hosts, timeout 6s, concurrency 2)
python3 scripts/write_url_health_snapshot.py --probe-known-flaky

# Or feed machine JSON after a freshness run
python3 scripts/write_url_health_snapshot.py --from-freshness-json path/to/results.json

python3 scripts/list_url_tickets.py
```

Resolve a ticket after fixing the catalogue URL (appends a `fixed` row and syncs
`frontend/data/url_tickets.jsonl`, which must stay byte-identical):

```bash
python3 scripts/resolve_url_ticket.py --scheme-id <id> --url <ticket url> \
    [--new-url <replacement>] --probe [--force] --notes "evidence"
```

`--probe` re-checks with the same HEAD→GET probe; `--force` is only for hosts verified
from another network (say so in `--notes`).

**Probe behaviour (2026-09-25):** HEAD first. On HEAD 400/403/404/405/5xx/501 the probe
retries with GET. Some official portals answer HEAD wrongly: pensionscheme.sikkim.gov.in
(IIS) gives HEAD 404 and sspensions.ap.gov.in gives HEAD 500, while GET returns 200 on
both. Those HEAD answers caused the original false "broken" tickets.

**Geo-fenced hosts:** `_GEOFENCED_INDIA_HOSTS` in `write_url_health_snapshot.py`
(currently `nsap.dord.gov.in`) block non-Indian networks with a TLS EOF or timeout. A
failed probe from CI or the box is reported as `GEO-FENCED …` and never opens or resolves
a ticket. Verify from India instead, e.g. the public check-host.net India nodes.

Known historically flaky hosts (probed by `--probe-known-flaky`):

- `nsap.dord.gov.in`: the NSAP portal. Legacy `nsap.nic.in` is NXDOMAIN and was
  replaced 2026-09-25. The new host is geo-fenced to India.
- `sspensions.ap.gov.in`: intermittent 5xx; HEAD returns 500.
- `pensionscheme.sikkim.gov.in`: HEAD returns 404, GET returns 200.

All three 2026-09-24 pre-seeded tickets were resolved `fixed` on 2026-09-25.

Do **not** hammer the full catalogue from CI. Prefer the daily routine + small
allowlists. User-Agent is set; keep timeouts short.

## 3. Versioned state / country packs

Manifests under `data/packs/` (mirrored to `frontend/data/packs/`):

- Example ids: `india-kerala@1.0.0`, `india-central@1.0.0`, `us-federal@1.0.0`,
  `us-california@1.0.0`, `uk-wide@1.0.0`, `uk-scotland@1.0.0`
- United Kingdom (2026-09-25):
  - UK rows are detected by the `united_kingdom` tag, a `gb-` id, or
    `countries: ["United Kingdom"]`. They are handled before the India fallback.
  - `uk-wide` (kind `country_national`) holds rows with no nations listed.
  - `uk-england` / `uk-scotland` / `uk-wales` / `uk-northern-ireland` (kind `nation`)
    come from `eligibility_rules.states`.
  - See `docs/COUNTRY_UK.md`.
- Contents: `scheme_ids[]` membership only — **no** duplicated scheme bodies
- Regenerated from tags in `schemes.json`:

```bash
python3 scripts/generate_pack_manifests.py --version 1.0.0
```

**Versioning:** bump `--version` when membership rules change (not on every
scheme add that merely expands an existing tag set — regenerating `1.0.0` is OK
while the rule is stable; document breaking rule changes with a new version).

Pytest covers representative packs (India states + US federal + sample US
states): all listed ids exist; required fields present; `official_source_url`
is http(s); dual-tree `schemes.json` identical.

## 4. Ops dashboard hooks

Env gate unchanged: `NEXT_PUBLIC_SHOW_OPS=1` **or** `OPS_DASHBOARD_TOKEN`.

`/ops` and `/ops/summary` show:

- open URL ticket count (+ by_status)
- candidate queue counts by status
- pack count

## Still open (later Phase 4)

- Full human CMS + reviewer/publisher UI
- Pager / on-call for ticket SLA
- Automated candidate extraction from freshness Markdown (still human paste OK)
- Claiming Phase 4 complete or enterprise “500k” catalogue scale
- Fly/Vercel deploy without credentials

## Related

- `docs/DATA_REFRESH.md` — weekly/monthly human refresh
- `docs/TRUST.md` — signed releases + audit
- `docs/PRODUCT.md` — Phase 3 product surface; links here for ops data plane
- `docs/DECISIONS.md` — Phase 4 decision entry
- `docs/COUNTRY_UK.md` — United Kingdom conventions (gb-* ids, nations, £ soft gate)
