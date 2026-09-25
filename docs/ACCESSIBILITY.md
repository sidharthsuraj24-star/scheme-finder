# Accessibility — WCAG 2.2 AA audit

**Date:** 2026-09-25 (IST)
**Target:** WCAG 2.2 Level AA (A + AA success criteria) for the public web UI
(`/` wizard → results, saved profiles, share) and the internal `/ops` dashboard.
**Status:** Automated + scripted-manual audit done and all issues found were fixed.
This is **not** a formal conformance certification or VPAT — see
[Known remaining gaps](#known-remaining-gaps). Manual screen-reader testing by a
human (NVDA / JAWS on Windows, VoiceOver on iOS/macOS, TalkBack on Android) is
still recommended before claiming full conformance.

## What was tested and how

| Layer | Tool | Scope |
|-------|------|-------|
| Automated rules | `@axe-core/playwright` 4.x (tags `wcag2a/aa`, `wcag21a/aa`, `wcag22a/aa` + `best-practice`) in Chromium headless | **22 UI states × 3 languages (EN / HI / ML) × 2 viewports (1280×800 desktop, 375×812 mobile)** + `/ops` (open + token-required) + 404 = **132 scans** |
| Contrast over gradients | Second axe `color-contrast` pass with the decorative body gradient flattened to its darkest stop (`#dcfce7`) | Same 132 states (axe otherwise reports text over gradients as "needs review" and never fails it) |
| Scripted manual checks | Playwright keyboard / DOM scripts (`frontend/e2e/a11y-keyboard.spec.ts`) | 17 checks × 2 viewports = 34 tests |
| Lighthouse | Lighthouse 13.5 accessibility category, mobile + desktop presets | `/` and `/ops` initial load |
| Code review | Manual review of every component in `frontend/src/components` + `app/` | Semantics, ARIA, focus management, language of parts, motion |

**UI states covered by axe:** welcome; wizard steps 1–9 on the India/Kerala path
(step 3 with the age life-stage widget, step 8 with the disability % field, step 9
with maternity question); US path step 2 (region select + free text) and step 9
(free-text district); validation error (step 3); parent-for-child mode (step 3);
loading; results; results with an expanded scheme card; results after saving a
profile; home with saved profiles listed; zero results; server error; `/ops`
open; `/ops` token-required; 404.

**Scripted manual checks (`a11y-keyboard.spec.ts`):**

1. Skip link is the first Tab stop, visible on focus, moves focus to `<main>` and bypasses the header / language switcher (2.4.1, 2.4.7).
2. The whole wizard can be completed **keyboard-only** (Tab / Space / Enter / select typeahead) through to results, and a scheme card can be expanded; every Tab stop is checked for a visible focus indicator (≥2px outline with ≥3:1 contrast against white and the page background) and for being in view and not covered by other content (2.1.1, 2.4.3, 2.4.7, 2.4.11, 1.4.11). Focus must not drop to `<body>` between steps, and lands on the results heading.
3. No keyboard trap: 80 Tab presses on the busiest step cycle through >12 distinct controls with no element holding focus (2.1.2).
4. Text/number inputs reference their hint via `aria-describedby`; on error they get `aria-invalid="true"`, `aria-describedby` includes the error id, focus moves to the field, and the message states the valid range (1.3.1, 3.3.1, 3.3.3, 4.1.2).
5. Choice groups (fieldsets) expose the error via `aria-describedby` and the error clears once answered.
6. Every visible `input`/`select` has a real `<label>` (not placeholder-only) — home, US region step, `/ops` (3.3.2, 2.5.3).
7. `<html lang>` switches to `hi` / `ml` / `en` with the UI language, including on load from a stored preference; language buttons carry their own `lang` (3.1.1, 3.1.2).
8. Viewport meta allows pinch-zoom (1.4.4).
9. A persistent polite live region (`#sr-status`) exists before results and announces the result count (4.1.3).
10. `prefers-reduced-motion: reduce` disables entrance animations and the spinner (2.3.3 best effort / vestibular safety).
11–12. Reflow at **320px** and **640px** CSS width (≈ 400% / 200% zoom of a 1280px window): no horizontal scrolling on home (EN/HI/ML), steps 1–9, results, `/ops` (1.4.10, 1.4.4).
13. Text-spacing override (line-height 1.5, letter 0.12em, word 0.16em, paragraph 2em) causes no horizontal overflow (1.4.12).
14. Every visible interactive target is ≥24×24 CSS px (2.5.8) — home, results, saved-profiles.
15. Form-control boundaries and the unselected choice indicator meet 3:1 non-text contrast (1.4.11).
16. `/ops` token field: labelled, `autocomplete="current-password"`, paste not blocked, Enter submits (3.3.8).

Run it yourself:

```bash
cd frontend
npm ci && npx playwright install chromium   # once
npm run build
npm run test:a11y          # axe + keyboard suites, desktop + 375px (starts next on :3100)
npm run test:a11y:report   # axe only, writes a11y-report/*.json + summary table
```

The suite **fails on any serious/critical WCAG-tagged axe violation** (all
violations are still written to the JSON report). CI config lives in
`docs/workflows/a11y.yml` (copy to `.github/workflows/` with a `workflow`-scope
token, same arrangement as the freshness workflow).

## Results — before vs after

### axe-core (132 scans each)

| Severity | Before (instances) | After |
|----------|-------------------:|------:|
| Critical | 0 | 0 |
| Serious | **270** | 0 |
| Moderate | **142** | 0 |
| Minor | 0 | 0 |
| **Total** | **412** | **0** |

Distinct rules before (7): 3 serious, 4 moderate; 16 unique rule+element pairs.

| Rule | Impact | WCAG | Instances before | Where |
|------|--------|------|-----------------:|-------|
| `color-contrast` | serious | 1.4.3 | 186 | Footer `text-slate-400` 11px (2.33:1); results meta lines `text-slate-500` (4.33:1 on the page gradient) |
| `aria-progressbar-name` | serious | 4.1.2 | 78 | Wizard progress bar had no accessible name |
| `scrollable-region-focusable` | serious | 2.1.1 | 6 | Error-details `<pre>` scrolled horizontally, not keyboard reachable |
| `meta-viewport` | moderate | 1.4.4 | 132 | `maximum-scale=1` blocked pinch-zoom on every page |
| `region` | moderate (BP) | — | 6 | 404 page content outside landmarks |
| `landmark-one-main` | moderate (BP) | — | 2 | 404 page had no `<main>` |
| `skip-link` | moderate (BP) | — | 2 | 404 page skip-link target missing |

axe "needs review" items: before 78 `aria-prohibited-attr` (aria-label on a plain
`div` around the progress bar) → 0 after. Remaining "needs review" items are
contrast over gradients; those were covered by the flattened-background pass and by
manual calculation (welcome card `brand-900` on `brand-100` ≈ 8.3:1; age widget
`brand-800` on `brand-50` ≈ 6.9:1).

### Scripted manual checks (per viewport)

| | Before | After |
|--|--|--|
| Checks passing | 4 / 17 (no keyboard trap, text spacing, reflow 320, reflow 640) | **17 / 17** |
| Tests (×2 viewports) | 8 pass / 26 fail | **34 / 34 pass** |

### Lighthouse accessibility

| Page | Before | After |
|------|-------:|------:|
| `/` mobile | 94 (meta-viewport) | 100 |
| `/` desktop | 94 | 100 |
| `/ops` mobile | 94 | 100 |
| `/ops` desktop | 94 | 100 |

## Fixes (by success criterion)

**Perceivable**
- 1.4.4 / 1.4.10 — removed `maximum-scale=1` from the viewport; error-details `<pre>` now wraps; `/ops` URL-health list no longer a nested scroll box.
- 1.4.3 — all low-contrast text (`slate-400`/`slate-500`, 11px footer / meta lines) moved to `slate-700` (≥ 8:1) and ≥12px.
- 1.4.11 / 1.4.1 — inputs, selects and choice buttons use a `slate-500` 2px boundary (≈ 4.8:1). Selected answers show a **filled ✓ indicator** (radio-style circle for single choice, square for multi-choice), not just a pale green tint. Invalid fields get a red border + tint in addition to the text message.
- 1.3.1 — each question is now an `<h2>` (wrapping the `<label>` / inside the `<legend>`); hints are tied to controls with `aria-describedby`; the welcome "for myself / for my child" buttons are a labelled group; scheme names are real `<h3>` headings (previously inside a button, so invisible to heading navigation).
- 1.3.5 — `autocomplete` on country (`country-name`), state/region (`address-level1`), district (`address-level2`).
- 3.1.1 / 3.1.2 — `<html lang>` follows EN/HI/ML (and resets to `en` on `/ops`); language buttons carry `lang="hi"`/`lang="ml"`; English fallback scheme text, verify notes and API messages inside a Hindi/Malayalam page are marked `lang="en"`; skip link is localised and marked with its language.
- AgeLifeStage: removed the `aria-live` region on the animated 0→age counter (it re-announced every frame); a static visually-hidden "Life stage: …" line replaces it.

**Operable**
- 2.4.1 — landmark structure is now `header` (banner: title + language) → `main#main-content` → `footer` (contentinfo); the skip link actually bypasses the header (before, it pointed at a `<main>` that wrapped the header, so it skipped nothing).
- 2.4.3 / 2.4.11 — focus management: Next/Back/Start move focus to the new question heading (which includes a visually-hidden "Step N of 9"); submit → loading panel → results heading (or error heading); Start over / Change answers / Load saved → welcome heading; deleting / clearing saved profiles → saved-profiles heading. Previously focus fell to `<body>` on every step change.
- 2.4.2 — document title reflects language + phase (e.g. "Schemes that may fit you · Scheme Finder", localised in HI/ML); `/ops` has its own title; 404 page added.
- 2.4.7 — focus ring kept (3px `#15803d`, ≥4.5:1 on white and on the page gradient); skip link has a dark ring + white halo.
- 2.5.8 — "Clear all" saved profiles link grown to ≥44px tall; all other targets already ≥48px.
- 2.3.3 (AAA, best effort) — global `prefers-reduced-motion` rule now also stops the loading spinner, transitions and hover/active scaling.

**Understandable**
- 3.3.1 / 3.3.3 — the single generic "Please answer this to continue" is replaced by **specific, translated messages with suggestions** (e.g. "Enter an age in whole years between 0 and 120.", "Enter an amount of 0 or more, using numbers only (for example 90000).", "Choose at least one category, or choose “None”.", step 9 lists exactly which questions are unanswered). Out-of-range disability % is now caught client-side.
- 3.3.2 / 4.1.2 — errors: `role="alert"` message with an id, `aria-invalid="true"` on the invalid input or fieldset, `aria-describedby` → error, focus moved to the first invalid control, error clears when fixed.
- 3.3.2 — visible labels added for the saved-profile name field, the free-text region field (US etc.) and the `/ops` token field (previously placeholder-only).
- 3.3.7 Redundant Entry — new **"Change my answers"** button on results and on the error screen reopens the wizard with every previous answer prefilled (previously only "Start over", which cleared everything even though the zero-results copy says "change your answers and try again"). Back already preserved answers; saved profiles + share links remain.
- 3.3.8 Accessible Authentication — `/ops` has no cognitive test: token field is a labelled `type=password` with `autocomplete="current-password"`, paste allowed, inside a `<form>` so Enter submits.
- 3.2.6 Consistent Help — the help content (disclaimer pointing to the local body / official portal, footer data-freshness line) stays in the same relative position in every phase; the footer is now a real `contentinfo` landmark rendered identically in all phases.
- Zero-results heading no longer says "Schemes that may fit your child" when nothing matched.

**Robust**
- 4.1.2 — progress bar has `aria-label` / `aria-valuetext` ("Step 3 of 9"); removed the prohibited `aria-label` on a plain `div`; scheme-card disclosure button uses `aria-expanded` + `aria-controls` and its name no longer hides the badge/reason text (the old `aria-label` overrode everything inside the button).
- 4.1.3 — a persistent `role="status"` live region announces "Searching schemes…", the result count / "No matching schemes", server errors, "Profile saved / deleted / cleared", "Link copied" and copy failures (inline message instead of a blocking `alert()`). The catalogue freshness banner is no longer a `role="status"` (it is static content).
- Links that open a new tab (official portal, apply, WhatsApp) announce "(opens in a new tab)" and include the scheme name for context.

## Criteria with nothing to fix / not applicable

- 1.2.x media — no audio/video. 1.4.13 — no hover/focus pop-ups. 2.2.x — no time limits (status messages fade but are also announced). 2.5.1 / 2.5.7 — no path-based or dragging gestures. 1.3.4 — no orientation lock. 3.2.1 / 3.2.2 — changing country only resets dependent fields, no context change.

## Known remaining gaps

- **No human screen-reader pass yet.** Behaviour was verified via DOM/ARIA assertions and axe, not by listening. Recommended: NVDA + Firefox/Chrome and JAWS on Windows, VoiceOver on iOS Safari and macOS, TalkBack on Android Chrome — especially for the focus-to-heading pattern between steps, the live-region announcements, and Hindi/Malayalam voices.
- **Hindi / Malayalam copy for the new error / status strings** (`frontend/src/lib/i18nA11y.ts`) needs native-speaker review (same caveat as the rest of the ML/HI UI).
- **Scheme body content** often falls back to English in HI/ML mode. It is now correctly marked `lang="en"` (so 3.1.2 is met), but for many users it is still not in their language.
- Country / state / district names are English-only in all languages (proper nouns; acceptable, but could be localised).
- `/ops` is English-only (internal tool).
- Choice questions use toggle buttons with `aria-pressed` inside `fieldset`/`legend`, not native radio / checkbox inputs. This is valid and fully keyboard operable, but some screen-reader users expect radio semantics; consider native inputs in a later pass.
- Contrast was checked against the **darkest** stop of the decorative gradient; forced-colors / Windows High Contrast mode and dark-mode user styles were **not** tested.
- Zoom/reflow was simulated with 320px / 640px CSS viewports; real browser zoom, text-only zoom and OS font scaling on mobile were not separately tested.
- Lighthouse only audits the initial state of `/` and `/ops`; deeper states rely on the axe sweep.
- External government portals linked from results are outside this app's control.
- The CI workflow is committed under `docs/workflows/a11y.yml`; it only runs once someone with a `workflow`-scope token copies it to `.github/workflows/`.
