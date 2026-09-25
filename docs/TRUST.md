# Trust & compliance — Phase 2 foundation

**Date:** 2026-09-24 (IST)  
**Status:** Foundation slice shipped — **not** enterprise-certified; **not** full Phase 2 complete.

This document defines curator / reviewer / publisher responsibilities for the
JSON-in-git catalogue. A full Scheme CMS UI + auth is **out of scope** for this
slice; git history + `data/catalogue_audit.jsonl` + signed releases are the
trust trail until CMS lands.

## Roles (scaffold)

| Role | Responsibility |
|------|----------------|
| **Curator** | Propose catalogue edits (add/update/tag) from official sources only. Never invent eligibility. Dual-write `data/schemes.json` and `frontend/data/schemes.json`. |
| **Reviewer** | Verify official URLs, `verify`/`verify_notes`, and that rule fields match cited pages. Approve PRs; may append audit `verify` entries. |
| **Publisher** | Run signed release + publish gate, append audit `release`, merge/push to `main`. |

Publish = **signed release** + **audit entry** + **main push**.

## Signed catalogue releases

```bash
# After schemes.json changes (both trees identical):
python3 scripts/sign_catalogue_release.py --changelog "Short human summary"

# Verify checksum vs file bytes:
python3 scripts/sign_catalogue_release.py --verify

# Before claiming publish-ready:
python3 scripts/check_catalogue_publish_ready.py
```

Outputs:

- `data/catalogue_release.json` (+ sync copy under `frontend/data/`)
  - `updated_as_of`, `scheme_count`, `schemes_sha256`, `generated_at` (IST),
    `changelog` history, `latest_changelog`
- Append-only line in `data/catalogue_audit.jsonl` (`action=release`)

Public API (read-only metadata; checksum is **not** a secret):

- `GET /catalogue/meta` (and `/api/v1/catalogue/meta`)
- `GET /ready` includes `schemes_sha256` when a release file exists
- Match/health `catalogue` object may include `schemes_sha256` + `release_generated_at`

## Immutable audit log

`data/catalogue_audit.jsonl` — one JSON object per line:

- `timestamp` (IST offset), `actor` (`CATALOGUE_ACTOR` or git), `action`
  (`add` / `update` / `tag` / `verify` / `release` / …), `scheme_ids[]`,
  `notes`, optional `commit_sha`, optional `release_checksum`

```bash
CATALOGUE_ACTOR="suraj" python3 scripts/append_catalogue_audit.py \
  --action verify --scheme-ids in-ppf --notes "Checked NSI page 2026-09-24"
```

**Never rewrite past lines.** Deepen scripts may call the helper; do not truncate
the file to “clean up” history.

## Privacy (see also `docs/PRIVACY.md`)

- No account PII stored by default.
- Match path logs **status, latency, country, optional IP hash** — not full profiles.
- Profiles are processed ephemerally for matching.

## Accessibility & security (honest partial)

**This slice:** skip-to-content link, `main` landmark, existing button labels /
`aria-expanded` on scheme cards, security headers (prior hardening).

**2026-09-25:** WCAG 2.2 AA audit (automated axe sweep over every route / step /
language / viewport + scripted keyboard checks + Lighthouse) done and fixes shipped —
see **`docs/ACCESSIBILITY.md`**. Not a formal certification; human screen-reader
testing still recommended.

**Later Phase 2 milestones (not claimed done here):**

- External **pentest**
- **SOC2-ready** logging/retention program
- Encrypted saved profiles / DigiLocker
- Full CMS UI with role-based auth

## Disclaimer UX

Every results view must tell users to **confirm eligibility on the official
portal** before applying (banner + per-scheme official link + footer). Copy must
not invent new legal guarantees.

## Residual

Fly deploy credentials remain blocked (Phase 1). Catalogue edits stay human-curated
in git — no eligibility invention.
