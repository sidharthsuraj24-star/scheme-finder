# Decisions — Scheme Finder Phase 1

## Data curation

1. **No invented eligibility.** Only fields supported by official pages were populated; unclear items set `verify=true` with `verify_notes`.
2. **Kerala Sevana over bare NSAP for Kerala pensions.** Central NSAP age/BPL frames differ from Sevana FAQ (e.g., widow age). Matcher for Kerala residents should prefer Sevana rules; NSAP cited for NFBS/central context.
3. **Mentally vs physically challenged.** Kept as separate scheme ids because KSSP/LSGD publish distinct pages; Sevana forms group them. Marked verify for operational distinctness and age conflict on imcp page.
4. **LIFE Mission.** Included with verify=true; hard `max_annual_income=300000` (₹3 lakh/year) from LIFE eligibility summaries / LSGI materials (2026-09-16). Exceeding income excludes even when verify=true. Category details still portal-confirm.
5. **PM-KISAN land size.** Homepage says all landholding families (with exclusions); older FAQ said ≤2 ha → verify flag.
6. **Benefits amounts.** Sevana tables show Rs.2000 — recorded as listed on FAQ criteria tables; advise re-check against latest GO before user-facing benefit quotes.

## Malayalam copy

- UI chrome (welcome, questions, buttons, errors, freshness banners, disclaimers, share) has natural Malayalam strings in `frontend/src/lib/i18n.ts`.
- Scheme `scheme_name` / `description` / `benefits` / `how_to_apply` ML for the main Sevana pensions and other catalogue entries were kept or improved where confident.
- `required_documents.ml` pending suffixes (`[ML copy pending native review]`) were replaced with natural Malayalam for common document labels; if unsure we keep English rather than invent wrong ML.
- **ML was improved for shipping but still welcome native speaker review** (tone, honorifics, and LSGD terminology).


## UI languages EN / ML / HI (2026-09-16)

- UI languages: **English (en)**, **Malayalam (ml)**, **Hindi (hi)**.
- Hindi UI chrome is complete in `frontend/src/lib/i18n.ts` (welcome, questions, buttons, errors, freshness banners, income labels, share, disclaimers, age life-stage labels, zero-match, filtered-using-income, etc.).
- Scheme body fields (`scheme_name` / `description` / `benefits` / `how_to_apply` / `required_documents`) support an optional `hi` key; **where missing, the UI falls back to English** — do not invent unofficial Hindi legal names. A sample of major schemes has official-style Hindi names; full catalogue Hindi pending native review.

## Planned stack fallbacks (Phase 2+)

| Concern | Preferred | Fallback |
|---------|-----------|----------|
| Database | Supabase (Postgres) | **SQLite** local file (`scheme_finder.db`) if no Supabase credentials |
| Explanations | LLM (API key) | **Template explanations** from matched/unmatched rule lists if no LLM key |
| Auth | Supabase Auth / optional API key | None for local demo |
| Hosting | Container / serverless | Local Uvicorn |

Env example:
```
DATABASE_URL=          # empty → SQLite
SUPABASE_URL=
SUPABASE_KEY=
LLM_API_KEY=           # empty → templates only
```

## Sample profiles

`data/sample_profiles.json` has 15 synthetic profiles for matcher tests (senior, widow, PwD, farmer, student, pregnant, high-income control, etc.). Not real persons.

## Out of scope for Phase 1

- Live matching engine / FastAPI implementation
- Scrapers or automatic GO sync
- Storing user PII

## Income matching (2026-09-16)

1. **Hard ceilings first.** Always hard-exclude when `max_annual_income` / `max_monthly_household_income` is exceeded (including verify=true schemes). Prefer filling official ceilings over soft gates.
2. **Telangana Aasara.** CAG Audit Report No.1 of 2023: exclude if annual household income > ₹1.50L rural / > ₹2.00L urban. Encoded `max_annual_income=200000` (urban absolute max); rural 1.5L nuance stays in verify_notes.
3. **`implies_low_income` soft gate.** For BPL/destitute/welfare-pension schemes where no official rupee ceiling was found: set `eligibility_rules.implies_low_income=true` and hard-exclude when annual income ≥ **₹5,00,000**. Do not invent numeric ceilings.
4. **Wizard income mode.** Default **Yearly**; toggle Monthly|Yearly. Yearly sends `annual_income`; Monthly sends `monthly_household_income` (API derives the other). Live conversion shown. Fixes users typing annual figures into a monthly-only field.

## 2026-09-24 — India PRICE ICE 360° household income bands (UX / ranking only)

**Decision:** Classify **India-only** annual household income into PRICE ICE 360°
bands (Seekers ₹5–15L, Strivers ₹15–30L, etc.) for MatchResponse labels and a
small deterministic ranking boost on `middle-class` / `upper-middle-class` /
`tax` / `savings` / `universal` / `high-income-eligible` tags.

**Country scope (hard rule):** PRICE bands, `income_band` / `income_band_label` /
`income_class` / `income_band_source` on MatchResponse, Results UI Seekers/Strivers
sentence, and seeker/striver/*_rich soft ranking boosts apply **only when
`country` is India**. United States, Bangladesh, Nepal, Sri Lanka, Maldives, and
any future country must **not** map local currency onto PRICE INR thresholds.
US keeps its own currency-aware soft gate (`implies_low_income` at USD $60k) —
do not invent US Census / Pew / OECD bands here.

**Not done:** Inventing `max_annual_income` from PRICE bands; replacing the
₹5L `implies_low_income` BPL soft gate with ₹15L; claiming PRICE bands are
official GoI policy; applying India bands to non-India profiles.

**Source:** PRICE ICE 360° / “The Rise of India's Middle Class” (2020–21 prices).
PDF: https://www.price360.in/Executive_Summary_Middle_Class.pdf

**Code:** `backend/app/income_bands.py`, `frontend/src/lib/matching/incomeBands.ts`.


## 2026-09-24 — Phase 2 trust & compliance foundation

**Decision:** Ship a concrete trust foundation without claiming Phase 2 complete
or enterprise certification.

1. **Signed catalogue releases.** `scripts/sign_catalogue_release.py` hashes
   dual-tree `schemes.json` (SHA-256), writes `data/catalogue_release.json`
   (+ frontend sync) with `updated_as_of`, `scheme_count`, `schemes_sha256`,
   `generated_at` (IST), and changelog. Public metadata via `/catalogue/meta`
   and `/ready` — checksum is integrity metadata, not a secret.
2. **Immutable audit log.** Append-only `data/catalogue_audit.jsonl` via
   `scripts/append_catalogue_audit.py`. Actor from `CATALOGUE_ACTOR` or git.
   Never rewrite past lines. Full CMS roles come later; git + audit is the trail.
3. **Roles scaffold.** Curator / reviewer / publisher defined in `docs/TRUST.md`.
   Publisher checklist = signed release + audit + `check_catalogue_publish_ready.py`
   + main push. No admin CMS UI in this slice.
4. **Privacy.** Match path must not log full profiles; structured access logs
   only (status, latency, country, optional IP hash). See `docs/PRIVACY.md`.
5. **Disclaimer UX.** Strengthen results copy (EN/ML/HI) so every results view
   requires confirm-on-official-portal; per-scheme official link labels emphasize
   official site. No new legal claims.
6. **A11y partial.** Skip-to-content + main landmark now; full WCAG 2.2 AA +
   pentest + SOC2 logging = later Phase 2 milestones (documented in TRUST.md).

**Not done:** CMS auth UI, encrypted profiles, DigiLocker, SOC2/pentest engagement,
claiming enterprise-ready, Phase 1 Fly deploy (still credential-blocked).
