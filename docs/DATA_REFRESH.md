# Scheme catalogue data refresh

**Stamp:** `updated_as_of` = **2026-09-08** (see `data/catalogue_meta.json`).  
**Stale after:** `stale_after_days` = **30** (UI shows an amber warning when today − updated_as_of > 30).  
**Scope:** Curated **central + Kerala** schemes only — **not** a complete all-India catalogue (currently 18 schemes).  
**Disclaimer (also in meta):** Confirm with the official source before applying.

## Why we do not fully auto-scrape “all India”

Fully automatic scraping of every Indian welfare scheme (MyScheme, state portals, Sevana, ministry sites) is **unreliable and dangerous** for eligibility matching:

1. **Hallucinated eligibility** — LLM or brittle scrapers invent income caps, age rules, or category lists that look plausible but are wrong.
2. **Page structure drift** — portals change HTML/PDF layouts; silent parse failures produce stale or empty rules.
3. **Legal/compliance risk** — quoting wrong benefit amounts or eligibility can mislead applicants.
4. **Verify flags** — many official pages are ambiguous (additive vs replacement amounts, district GOs). Those must stay `verify: true` until a human reads the source.

Therefore this repo **never** treats scraped text as authoritative eligibility without a human merge. The weekly Actions job only opens an issue — it does **not** auto-edit `eligibility_rules`.

---

## Weekly human steps (every Monday, or when the Actions issue opens)

1. Open the GitHub Issue titled **Scheme catalogue freshness check** (created/updated by `.github/workflows/scheme-freshness.yml`).
2. Locally (optional):  
   `python3 scripts/scheme_freshness_check.py`  
   or with URL probes:  
   `python3 scripts/scheme_freshness_check.py --check-urls`
3. For each scheme checkbox:
   - Open `official_source_url`.
   - Confirm age / income / category / benefit text still matches `data/schemes.json`.
   - Note broken URLs (from the script’s `url_check` line) and fix `apply_url` / `official_source_url` only when the official page clearly moved.
4. If nothing changed: tick the boxes, comment “reviewed YYYY-MM-DD — no rule changes”, and close or leave the issue for next week.
5. If something changed: open a **PR** (never push eligibility straight to main without review). See monthly steps below for the PR checklist.
6. Do **not** invent numbers to clear `verify: true`. Prefer keeping `verify` + `verify_notes`.

---

## Monthly human steps (recommended full pass)

1. **Fetch changelogs / listings** (read-only):
   - [MyScheme](https://www.myscheme.gov.in/) search / scheme pages relevant to Kerala + central schemes already in the seed.
   - Kerala Sevana / LSGD welfare pension FAQs: https://welfarepension.lsgkerala.gov.in/FAQsEng.aspx
   - Scheme-specific official URLs already stored in `data/schemes.json` → `official_source_url`.
2. **Diff** against `data/schemes.json` (benefit text, age/income caps, apply URLs only when the official page clearly states them).
3. **Open a PR** with:
   - JSON diff for `data/schemes.json` **and** the copy at `frontend/data/schemes.json`
   - Short notes citing the official URL and date checked
   - Per-scheme `last_verified` bumped to the ISO date you checked (e.g. `2026-09-08`)
4. **Human verify** every changed `eligibility_rules` field and benefit amount before merge.
5. Bump `data/catalogue_meta.json` → `updated_as_of` / `updated_as_of_iso` (and keep `stale_after_days`, `disclaimer`) and copy to `frontend/data/catalogue_meta.json`.
6. Keep `verify: true` + `verify_notes` when the official source is ambiguous — do **not** invent numbers to “refresh” the catalogue.
7. After merge: confirm production `GET /api/health` shows the new `catalogue.updated_as_of` and `is_stale: false`.

---

## Weekly reminder (GitHub Actions)

`.github/workflows/scheme-freshness.yml` runs weekly (**Monday 09:00 UTC**) and on `workflow_dispatch`. It:

1. Runs `scripts/scheme_freshness_check.py --check-urls`
2. Opens (or comments on) an issue titled **Scheme catalogue freshness check**
3. Reminds: **do not auto-edit eligibility**; human must verify then PR

It does **not** auto-merge scheme data.

### If the workflow file could not be pushed

Pushing `.github/workflows/*` requires a GitHub credential with the **`workflow` scope**. The default `gh` OAuth token (`gist`, `read:org`, `repo` only) is rejected with:

> refusing to allow an OAuth App to create or update workflow … without `workflow` scope

**Fallback already in-repo:**

- Copy of the workflow: `docs/workflows/scheme-freshness.yml`
- To install manually: add a PAT with `workflow` + `repo`, then either:
  - `cp docs/workflows/scheme-freshness.yml .github/workflows/` and push, or
  - paste the file in the GitHub UI under Actions → New workflow

All other freshness files (meta, script, UI, docs) can ship without the `workflow` scope.

---

## Honesty in the UI

- **Fresh** (within `stale_after_days`): green banner with updated-as-of date + “Confirm eligibility on the official source before you apply.”
- **Stale**: amber warning — “Scheme data may be outdated (last updated …). Always confirm on the official site before applying.”
- Each **SchemeCard** shows `last_verified` when present and a prominent **Official source — confirm here** link.
- Results footer: strengthened disclaimer — no guaranteed eligibility; verify=true matches stay uncertain.

Do not inflate `scheme_count` with invented schemes. Add schemes only with citable official sources documented in `docs/SOURCES.md` / the PR.

## Data fields

| Field | Where | Notes |
|-------|--------|--------|
| `updated_as_of` / `updated_as_of_iso` | `catalogue_meta.json` | Catalogue stamp |
| `stale_after_days` | `catalogue_meta.json` | Default 30 |
| `disclaimer` | `catalogue_meta.json` | Confirm official source |
| `last_verified` | each scheme in `schemes.json` | ISO date; defaults to catalogue stamp if missing |
| `official_source_url` | each scheme | **Required** |
| `is_stale` | `/api/health` + match responses | `today - updated_as_of > stale_after_days` |
