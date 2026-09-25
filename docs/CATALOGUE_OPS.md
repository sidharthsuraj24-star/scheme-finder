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
| Auto-draft candidates (2026-09-25) | `scripts/draft_candidates_from_sources.py` | Official feeds → `needs_review` leads + daily digest |
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
- `status`: `needs_review` \| `queued` \| `researching` \| `verified_add` \| `rejected` \| `deferred`
  (`needs_review` = auto-drafted lead, nobody has looked at it yet)
- `reason`, `noted_at`, `actor`, `notes`
- optional `scheme_id_if_present` when already curated
- auto-drafted rows add: `auto_drafted: true`, `verified: false`, `candidate_kind`
  (`scheme_listing` \| `press_release_lead` \| `notice_lead`), `source`
  (`id`, `label`, `feed_url`, `lang`), `source_url`, `found_at` (YYYY-MM-DD IST) and
  `extracted` — each field `{ "value", "verified": false, "source_field" }`, copied
  verbatim from the feed/listing. **No eligibility is ever extracted or inferred.**

**Honesty:** Historical India leftovers (PM-KMY, PM-SYM, NAMASTE) are already in
`schemes.json` (`in-pm-kmy`, `in-pm-sym`, `in-namaste`). Phase 4 seeds **deferred**
documentation rows only — open queue may be empty. That is intentional.

### Daily freshness → candidates (automated drafting, 2026-09-25)

`scripts/draft_candidates_from_sources.py` turns the "paste a candidate" step into
an automatic **draft** step. It never touches `schemes.json` and never invents
eligibility; everything it writes is `status: "needs_review"` and unverified.

Sources (official only; polite: robots.txt honoured, ≥2 s between requests per
host, 15 s timeout, 5 MB cap, ≤50 items per source, ≤20 new rows per run):

| id | Source | Notes |
|----|--------|-------|
| `pib-en`, `pib-hi` | PIB press-release RSS (English, Hindi) | Leads only (press releases, not scheme pages). **Akamai returns 403 to the box/CI network** — reported as `blocked`; works from Indian networks |
| `myscheme` | myScheme listing | The listing is client-rendered behind a keyed search API, so it is **opt-in**: pass `--myscheme-json FILE` (a saved search-API JSON response) or set `MYSCHEME_API_KEY` only if you are authorised to use a key. Skipped otherwise |
| `gov-uk` | GOV.UK news Atom (keyword "scheme") | Leads |
| `canada-news` | Canada News Centre Atom (news releases only) | Leads |
| `us-federal-register` | Federal Register API (final rules, term "program") | Leads |

Filtering and dedupe:

- Feed items need a scheme/programme term **and** a launch/new/opens signal in the
  title (Hindi: योजना/मिशन/अभियान… + शुभारंभ/शुरू/घोषणा…); routine items
  (corrections, statements, media advisories, seizures…) are dropped; items older
  than `--since-days` (default 3) are ignored.
- A row is a duplicate if its id, normalised URL (scheme/`www`/trailing slash/
  `utm_*`-insensitive) or fuzzy name (difflib ≥ 0.88 after `Pradhan Mantri→PM`
  aliasing and stop-words, EN/HI/ML names, or the same explicit acronym such as
  `PM-KISAN`) matches a scheme in `schemes.json` **or** any row already in the queue.
  Re-runs are idempotent (ids are derived from the source URL).
- Headlines naming a scheme we already carry (e.g. "…PM-KISAN instalment…") are
  **not** drafted; they are listed under "Existing schemes in the news" in the
  digest as a re-verification prompt.

#### Daily routine (run after the 6:09 AM IST freshness check)

```bash
cd <repo> && git pull --ff-only
python3 scripts/draft_candidates_from_sources.py \
  --digest-md /tmp/candidate-digest.md \
  --summary-json /tmp/candidate-digest.json
# optional: --myscheme-json /path/to/myscheme-search.json
python3 scripts/list_catalogue_candidates.py --status needs_review
```

Report in the daily digest (paste `/tmp/candidate-digest.md` as-is). It contains:

1. The count of new `needs_review` candidates, each with name, source and URL.
2. Duplicates skipped, plus "existing schemes in the news" (re-verify those).
3. The per-source status table. Call out any `blocked`/`error` source (PIB 403
   from non-Indian networks is expected) so a human can check it by hand.
4. If new rows were written, commit **only** `data/catalogue_candidates.json`,
   `frontend/data/catalogue_candidates.json` and `data/catalogue_audit.jsonl`
   (message: `catalogue: auto-draft N needs_review candidates (YYYY-MM-DD)`).
   Never commit a `schemes.json` change from this step.

Preview without writing anything: add `--dry-run --digest`. Offline/test mode:
`--offline-dir backend/tests/fixtures/candidate_sources --today 2026-09-25`.
Tests: `backend/tests/test_draft_candidates.py` (fixtures only, network disabled).

Human triage of a `needs_review` row: open `source_url`, find the official scheme
page, then `update_catalogue_candidate.py --id <id> --status researching|rejected
--reason "..."`. Only after human verification does anything go to a
`schemes.json` PR.

### Manual path (still supported)

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
- ~~Automated candidate extraction~~ → drafting shipped 2026-09-25 (`draft_candidates_from_sources.py`);
  still open: myScheme without a key/export, PIB from non-Indian networks, and
  extracting fields beyond feed metadata (deliberately not attempted: no eligibility parsing)
- Claiming Phase 4 complete or enterprise “500k” catalogue scale
- Fly/Vercel deploy without credentials

## Related

- `docs/DATA_REFRESH.md` — weekly/monthly human refresh
- `docs/TRUST.md` — signed releases + audit
- `docs/PRODUCT.md` — Phase 3 product surface; links here for ops data plane
- `docs/DECISIONS.md` — Phase 4 decision entry
- `docs/COUNTRY_UK.md` — United Kingdom conventions (gb-* ids, nations, £ soft gate)
