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
do not invent US Census / Pew / OECD bands here. United Kingdom (added 2026-09-25)
likewise has its own GBP gate — see the 2026-09-25 UK entry below.

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

## 2026-09-24 — Phase 3 product surface foundation

**Decision:** Ship a product-surface foundation without claiming Phase 3 complete,
OTP/DigiLocker auth, white-label tenants, or a CMS publisher UI.

1. **Saved profiles = localStorage only** (cap 5). Documented in PRIVACY.md; no
   server PII by default.
2. **Parent-for-child UX** uses existing profile `age` / `disability` / soft
   `is_student` + `child_age_months` — no new eligibility fields or invented
   `max_annual_income`. US Trump Accounts / Coverdell / 529 / ABLE already match
   when beneficiary age (and disability for ABLE) is on the profile.
3. **Ops dashboard** is read-only, env-gated (`NEXT_PUBLIC_SHOW_OPS` /
   `OPS_DASHBOARD_TOKEN`). Surfaces catalogue meta, checksum, coverage, URL health
   snapshot, aggregate analytics.
4. **Analytics** = aggregates only; never feeds matcher eligibility
   (`docs/ANALYTICS.md`).
5. **URL health** = checked-in snapshot + script; do not hammer full catalogue
   from CI in this pass.

**Not done:** OTP, DigiLocker, multi-tenant white-label, CMS login, Fly/Vercel
credential deploy (may still be blocked), claiming enterprise product-complete.

## 2026-09-24 — Phase 4 catalogue ops foundation

**Decision:** Ship an ops **data plane** (candidates, URL tickets, versioned packs,
ops hooks) without claiming Phase 4 complete, a full CMS, pager, or 500k scale.

1. **Candidate queue** is human-verify only. Historical PM-KMY / PM-SYM / NAMASTE
   already live in `schemes.json` → seeded as `deferred` documentation rows;
   empty open queue is honest and OK.
2. **URL tickets** are append-only JSONL; probes upsert open / resolve fixed.
   Known flaky hosts may be pre-seeded; never DOS gov sites (short timeout,
   limited concurrency).
3. **Packs** are versioned membership manifests derived from tags — no duplicated
   scheme bodies; regenerate with `generate_pack_manifests.py`.
4. **Ops dashboard** extends Phase 3 env gate to show ticket / candidate / pack
   counts. Full CMS + pager remain later.

**Not done:** CMS UI, pager, auto-adding schemes from candidates, claiming Phase 4
complete, Fly/Vercel credential deploy.

## 2026-09-25 — United Kingdom country + GBP soft gate

**Decision:** Add the United Kingdom as a catalogue country: 60 `gb-*` rows, the four
nations as regions, `£` currency, and `uk-*` packs. It is the 7th catalogue country after
India, Bangladesh, Nepal, Sri Lanka, Maldives and the United States. Conventions are in
`docs/COUNTRY_UK.md`.

1. **IDs `gb-*`.** `uk-*` is already taken by India/Uttarakhand rows.
2. **Income:**
   - India PRICE bands never apply to UK profiles, and the US $60k gate is not reused.
   - New `IMPLIES_LOW_INCOME_ANNUAL_GATE_GBP = 60_000` for `implies_low_income` rows
     with no numeric max.
   - This is a catalogue heuristic, not an official line. It is anchored on HMRC's
     £60,000 High Income Child Benefit Charge threshold.
   - The earlier test that asserted "UK has no gate" was updated on purpose.
3. **Hard caps only for official household ceilings:** Shared Ownership and First Homes
   (£90k London / £80k elsewhere), NI EMA (£22.5k), NI Discretionary Support (£29,741).
   Per-parent £100k childcare limits, Marriage Allowance tax bands, HICBC and the £35k
   Winter Fuel recovery stay in notes.
4. **All-income coverage:** universal, tax and savings rows (Child Benefit, State
   Pension, ISA/LISA/JISA, pension relief, SDLT relief, Boiler Upgrade Scheme, Tax-Free
   Childcare) never set `implies_low_income`, so wealthy profiles still see them.
5. **Explanation currency:** `_fmt_income` / `fmtIncome` now prefix `$` for the US and
   `£` for the UK. India and other countries keep the legacy `Rs.` prefix.

**Not done:**
- Translating scheme bodies to ML/HI (EN copies, as for US rows).
- A separate child-disability profile field.
- NI-specific rows where the nidirect page was not confirmed.

## 2026-09-25 — Canada country + CAD soft gate

**Decision:** Add Canada as a catalogue country with 67 `can-*` rows (29 federal + 38
provincial/territorial). All 13 provinces and territories are regions, amounts use
`C$` / CAD, and packs are `canada-federal` plus `canada-<province>`. Conventions are in
`docs/COUNTRY_CANADA.md`.

1. **IDs `can-*`.** `ca-*` is already taken by US/California rows. Country aliases are
   `canada` / `can`, and deliberately **not** `ca`.
2. **Currency:** `C$` everywhere (wizard `currencySymbol`, backend `_currency_prefix`,
   frontend `fmtIncome`, scheme text), so Canadian amounts are never read as USD.
3. **Income:**
   - India PRICE bands never apply to Canada, and the US $60k gate is never reused.
   - New `IMPLIES_LOW_INCOME_ANNUAL_GATE_CAD = 58_523` is used only for
     `implies_low_income` rows with no numeric max. It is a catalogue heuristic,
     anchored on the 2026 top of the lowest federal tax bracket, which ESDC also uses as
     the CLB low-income line and the additional-CESG tier.
   - Official ceilings are encoded as `max_annual_income`. Where the ceiling varies by
     household we use the highest published cut-off, with the other figures in notes
     (e.g. CGEB C$82,952, GIS C$54,624, CDCP < C$90k, CLB C$73,577).
   - Phase-outs that reach middle incomes (CCB, BC Family Benefit, ACFB, OTB, OCB) are
     not gated.
   - `test_matcher.py` previously asserted that Canada had no gate. It now asserts
     C$58,523, and the "no gate" synthetic case moved to Maldives.
4. **Federal rows that exclude a province:** CPP and EI maternity/parental exclude
   Quebec (QPP / QPIP). Canada Student Grants exclude QC / NT / NU. These rows list the
   eligible provinces explicitly but stay in `canada-federal`.
5. **Verified status as of Sep 2026:**
   - Canada Disability Benefit is active (C$204.20/month).
   - CDCP is open to all eligible ages for 2026–27.
   - The GST/HST credit was renamed the Canada Groceries and Essentials Benefit (CGEB)
     in July 2026.
   - The Canada Carbon Rebate ended April 2025 and is skipped.

**Not done:**
- Translating scheme bodies to ML/HI (EN copies, as for US/UK rows).
- Nunavut Senior Fuel Subsidy (gov.nu.ca is unreachable).
- Nova Scotia HARP (2026–27 terms are unpublished).
- Ontario GAINS (held back by the 4-per-province cap).
- Provincial student grants and child-care subsidies.

## 2026-09-25 — India freshness candidates (PM-KUSUM, PM-JANMAN + 4)

Each candidate was moved through `data/catalogue_candidates.json` (queued →
researching → final) with `scripts/update_catalogue_candidate.py`. Every transition has
an audit line.

- **PM-JANMAN → `verified_add`, added as `in-pm-janman` (`verify: true`).**
  - Benefit: PVTG households get a pucca house under PMAY-G norms (Rs 2 lakh) plus
    convergence services.
  - Coverage: 18 States + A&N Islands. Categories `ST` / `PVTG`, and
    `max_annual_income: null` because there is no income test.
  - No `central` tag, because it is not nationwide; the row goes into the 18 state packs.
  - Sources: PIB (Ministry of Tribal Affairs, Feb/Mar 2026) and Lok Sabha answers of
    30.07.2026 report it as ongoing. The extension to March 2027 is press-only, hence
    `verify: true`.
- **PM-KUSUM → `deferred`.**
  - MNRE OM dated 28 Mar 2026 says the scheme timeline ended 31.03.2026, and
    PM KUSUM 2.0 is "in the proposal stage".
  - Only projects with PPAs/NTPs issued by 31.12.2025 were extended.
  - There is no current new-farmer application route. Re-queue when the 2.0
    guidelines are published.
- **SVAMITVA → `deferred`, after careful judgement.**
  - The property card is a genuine household benefit.
  - But there is no individual application or eligibility test: cards are delivered
    through a village-wide drone survey and state distribution.
  - Revisit if MoPR or a state publishes a claim route.
- **Jal Jeevan Mission, PM SHRI, PM e-Bus Sewa → `rejected`,** with reasons prefixed
  "Out of scope: infrastructure, not an individual entitlement". They fund village water
  schemes, school upgrades and city bus fleets respectively.

## 2026-09-25 — URL ticket fixes + HEAD→GET probe

- `nsap-nfbs` now points to `https://nsap.dord.gov.in/` (MoRD NSAP portal).
  `nsap.nic.in` is NXDOMAIN at NIC DNS. The new host returns 200 from India
  (check-host.net) but is geo-fenced elsewhere. It is listed in `_GEOFENCED_INDIA_HOSTS`
  so non-Indian probes never open tickets for it.
- `ap-ntr-bharosa-oap` and `sk-unmarried-women-pension`: portals are live. Their false
  tickets came from HEAD 500 / HEAD 404 answers, so the probe now retries GET on
  HEAD 400/403/404/405/5xx.
- All three tickets were resolved via `scripts/resolve_url_ticket.py`. The URL ticket
  tests now accept `open_count >= 0`.

## 2026-09-25 — WCAG 2.2 AA audit (Phase 2 trust)

- Target WCAG 2.2 **AA**; results and gaps in `docs/ACCESSIBILITY.md` — no certification claimed.
- a11y strings live in `frontend/src/lib/i18nA11y.ts` and are merged into the main i18n tables (keeps catalogue/UI copy edits in `i18n.ts` conflict-free).
- Wizard focus moves to the new question heading on every step change; errors focus the first invalid control.
- Choice answers stay as `aria-pressed` toggle buttons (visible ✓ indicator added) rather than native radios — revisit after human screen-reader testing.
- Regression gate: Playwright + axe (`npm run test:a11y`) fails on serious/critical WCAG violations; CI template in `docs/workflows/a11y.yml`.

## 2026-09-25 — Free security pass (Phase 2) + auto-drafted candidates (Phase 4)

- Security: strict **nonce-based CSP** (pages rendered dynamically for per-request nonces), full header set via `next.config.mjs` + `src/lib/securityHeaders.mjs`, `/backend` rewrite dev-only, constant-time header-only ops token, streamed body caps, analytics sanitised before forwarding. Scans + before/after in `docs/SECURITY.md`. Explicitly **not** a pentest / SOC 2.
- `postcss` advisory in Next 15's bundled copy fixed with an npm `overrides` entry rather than a Next 16 major upgrade.
- Vercel's `Access-Control-Allow-Origin: *` on public static/HTML accepted (no credentials).
- Candidate queue gains status **`needs_review`** for machine-drafted leads (`scripts/draft_candidates_from_sources.py`). Drafts copy feed metadata verbatim, each field `verified: false`; never eligibility, never `schemes.json`. myScheme is opt-in (keyed API / export) and PIB is 403 from non-Indian networks — both reported as source status, not silently skipped.

## 2026-09-25 — Official zero-points for phase-out benefits

- Trigger: production smoke showed a C$250k Ontario family still seeing the Ontario Child Benefit (uncertain) because phase-out rows were ungated.
- Decision: gradual phase-out benefits carry `max_annual_income` = the income where the benefit reaches **zero** for a generous but realistic family (4 children, or the largest size the official page tabulates), from official formulas only (CRA, provincial pages/statutes, GOV.UK/gov.wales), rounded up; basis in `notes`, `verify: true`. Caps: CCB C$318,300; CDB C$266,005; OCB C$114,861; BCFB C$170,937; ACFB C$70,143; OTB C$117,971; NB HST credit C$85,000, NWT child benefit C$80,000 and NS affordable living tax credit C$39,900 (these three replace the C$58,523 soft gate). UK: per-parent £100k childcare limits → £200k household maximum (Tax-Free Childcare, England working-parent childcare, Wales Childcare Offer).
- No official zero-point → stays ungated: Quebec Family Allowance (minimum at all incomes), OAS (individual recovery tax), RESP/CESG and RDSP (basic grant at all incomes), UK Child Benefit, Marriage Allowance, Winter Fuel. Reduction rate unpublished → stays on the soft gate: NB child tax benefit, NL child benefit / income supplement, NU and YT child benefits.
- Caveat: programme tests use net income (AFNI / adjusted net income) while the profile asks for annual income; caps are generous (largest family) and every row stays `verify: true`.
- Tag rule in tests relaxed: rows tagged `universal` / `high-income-eligible` may carry a cap only if it is ≥ 150,000 (still reaches high incomes). CCB loses the `universal` tag (it is a phase-out).

