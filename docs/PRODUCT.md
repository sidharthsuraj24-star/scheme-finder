# Product — Phase 3 foundation

**Date:** 2026-09-24 (IST)  
**Status:** Foundation slice shipped — **not** Phase 3 complete; **not** enterprise product-complete.

## What shipped (this slice)

1. **Saved profiles (device-only)**  
   Local `localStorage` profiles (cap 5): optional name, ProfileAnswers + lang + `saved_at`.  
   Save / Load / Delete / Clear UI on Home. Never uploaded by default. Share links remain the only intentional export.

2. **Parent-for-child UX**  
   Welcome chooses *for myself* vs *for my child / dependent*. Age / disability copy switches; results banner clarifies matches may be for the dependent.  
   Profile `age` is the **beneficiary** age (required for US Trump Accounts, Coverdell ESA, 529 QTP age-free, ABLE with disability). Matcher audit: no new income ceilings invented; existing `max_age` / disability rules already surface those schemes when child age (and disability for ABLE) are set.

3. **Ops dashboard (read-only)**  
   Route `/ops` + `GET /api/ops/summary` (Next) and `GET /ops/summary` (FastAPI).  
   Gate: `NEXT_PUBLIC_SHOW_OPS=1` for open demo, or `OPS_DASHBOARD_TOKEN` + Bearer / `X-Ops-Token`.  
   Shows scheme_count, updated_as_of, schemes_sha256, stale, verify counts, coarse coverage, URL health snapshot, aggregate analytics. Link to `docs/TRUST.md` publish checklist. **No auth CMS / publisher UI.**

4. **Privacy-preserving analytics**  
   `POST /analytics/event` (and Next `/api/analytics/event`): aggregates only (`match_ok`, country, result_count bucket, optional scheme_id hits). Redis when available, else memory; fail open.  
   **Analytics never feed matcher eligibility** — see `docs/ANALYTICS.md`.

5. **URL health snapshot**  
   `data/url_health_snapshot.json` + `scripts/write_url_health_snapshot.py` (default empty; optional `--probe-sample` short allowlist). Do not hammer live .gov from CI in this pass.

## Later Phase 3 (not in this slice)

| Item | Notes |
|------|--------|
| OTP / DigiLocker auth | Real identity linking |
| Encrypted cloud saved profiles | Server PII with consent |
| Full CMS publisher UI + login | Curator/reviewer/publisher beyond git+audit |
| Org tenants / white-label | Multi-tenant branding |
| Drop-off funnels with PII | Out of scope; aggregates only |
| Claiming product-complete | Explicitly not claimed |

## Deploy note

Fly/Vercel credential deploy may still be blocked (see `docs/DEPLOY.md`). Local + `gh` ship is the release path for this foundation.

## Related

- `docs/PRIVACY.md` — device saves + analytics aggregates  
- `docs/ANALYTICS.md` — never invent eligibility from analytics  
- `docs/TRUST.md` — publish checklist  
- `docs/DECISIONS.md` — Phase 3 decision log

## Phase 4 ops data plane (foundation)

Catalogue ops foundation (candidates, URL tickets, versioned packs, ops hooks)
lives in **`docs/CATALOGUE_OPS.md`**. That slice is **not** Phase 4 complete and
does not replace this Phase 3 product surface doc.

Related: `docs/DATA_REFRESH.md`, `docs/DECISIONS.md`.

