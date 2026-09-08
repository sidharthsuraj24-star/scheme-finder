# Scheme catalogue data refresh

**Stamp:** `updated_as_of` = **2026-09-08** (see `data/catalogue_meta.json`).  
**Scope:** Curated **central + Kerala** schemes only — **not** a complete all-India catalogue (currently 18 schemes).

## Why we do not fully auto-scrape “all India”

Fully automatic scraping of every Indian welfare scheme (MyScheme, state portals, Sevana, ministry sites) is **unreliable and dangerous** for eligibility matching:

1. **Hallucinated eligibility** — LLM or brittle scrapers invent income caps, age rules, or category lists that look plausible but are wrong.
2. **Page structure drift** — portals change HTML/PDF layouts; silent parse failures produce stale or empty rules.
3. **Legal/compliance risk** — quoting wrong benefit amounts or eligibility can mislead applicants.
4. **Verify flags** — many official pages are ambiguous (additive vs replacement amounts, district GOs). Those must stay `verify: true` until a human reads the source.

Therefore this repo **never** treats scraped text as authoritative eligibility without a human merge.

## Recommended: monthly semi-automatic pipeline

1. **Fetch changelogs / listings** (read-only):
   - [MyScheme](https://www.myscheme.gov.in/) search / scheme pages relevant to Kerala + central schemes already in the seed.
   - Kerala Sevana / LSGD welfare pension FAQs: https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx
   - Scheme-specific official URLs already stored in `data/schemes.json` → `official_source_url`.
2. **Diff** against `data/schemes.json` (benefit text, age/income caps, apply URLs only when the official page clearly states them).
3. **Open a PR** with the JSON diff + short notes citing the official URL and date checked.
4. **Human verify** every changed `eligibility_rules` field and benefit amount before merge.
5. Bump `data/catalogue_meta.json` → `updated_as_of` / `updated_as_of_iso` and copy to `frontend/data/`.
6. Keep `verify: true` + `verify_notes` when the official source is ambiguous — do **not** invent numbers to “refresh” the catalogue.

## Weekly reminder (GitHub Actions)

`.github/workflows/scheme-freshness.yml` runs weekly (Monday 09:00 UTC) and opens (or comments on) an issue titled **Scheme catalogue freshness check** with a checklist. It does **not** auto-merge scheme data.

## Honesty in the UI

The frontend shows: *Scheme data updated as of 8 Sep 2026 · Curated central + Kerala set (not every scheme in India)*.

Do not inflate `scheme_count` with invented schemes. Add schemes only with citable official sources documented in `docs/SOURCES.md` / the PR.
