# Scheme Finder — Final Report (draft)

Date: 2026-09-08 (Asia/Calcutta)

## Repo

https://github.com/sidharthsuraj24-star/scheme-finder

## Scheme summary pointers

- Seed catalogue: data/schemes.json (18 schemes)
- Human index: docs/SCHEMES.md
- Sources: docs/SOURCES.md
- API contract: docs/API_CONTRACT.md
- Design decisions: docs/DECISIONS.md

## Test summary (Phase 4 + Phase 5 recheck)

| Suite | Result |
|-------|--------|
| Live API sample profiles | 14/14 PASS (see docs/TEST_LOG.md) |
| Backend pytest | 23/23 PASS (re-run after CORS/SCHEMES_PATH changes) |
| Frontend next build | OK (also succeeded inside Vercel temporary deploy) |

### Verify flags

- Schemes with eligibility_rules.verify=true never emit likely_eligible (forced uncertain).
- Maternity / NFBS rule keys fixed in Phase 4; covered in TEST_LOG cases.

## Substitutions vs original plan

| Planned | Actual |
|---------|--------|
| Supabase / Postgres | In-memory JSON + optional local SQLite dump (DATABASE_URL reserved) |
| LLM explanations | Template explanations (LLM_API_KEY stub only; never decides eligibility) |
| Cloud Agent build | Local box build |
| Always-on free prod hosts | Deploy configs committed; auth missing for persistent hosts |

## Deploy status

### Added for deploy

- backend/Dockerfile, .dockerignore
- render.yaml (Render free Blueprint)
- backend/Procfile, backend/railway.toml
- fly.toml
- frontend/vercel.json
- CORS via CORS_ORIGINS (default * for demo)
- SCHEMES_PATH optional override in loader
- docs/DEPLOY.md

### Live URLs

| Service | Status |
|---------|--------|
| Frontend | Temporary anonymous Vercel: https://temporary-fast-gold-jvm9d74.vercel.app (claim: https://vercel.com/claim-deployment?code=fafd1aab-6559-43fd-9b8c-73e99fd054da) |
| Backend | Not live — blocker: no Render/Railway/Fly auth on box; Docker unavailable |
| End-to-end | No — frontend temporary build points at localhost:8000; no public API |

### Exact blockers for persistent deploy

1. Backend: Sign in to Render (preferred free) and apply render.yaml, OR fly auth login + fly deploy, OR Railway login. Then set CORS_ORIGINS to the Vercel origin.
2. Frontend: vercel login (or claim temporary deployment) and set NEXT_PUBLIC_API_URL to the live API, then redeploy frontend/.

## Suggested next features

- Claim/persist Vercel frontend; deploy Render API; wire NEXT_PUBLIC_API_URL + CORS_ORIGINS
- Shareable results link (encoded profile query)
- District / LSG deep links once seed rules use geography
- More WCD / Sevana FAQ structured rules
- Native Malayalam copy review
- PWA shell / offline wizard shell
- Optional real LLM explanations behind feature flag (still not for eligibility)

## Commit note

Phase 5 deploy files + docs committed with one-shot git identity (no git config mutation).
