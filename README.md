# Scheme Finder

Trilingual (EN/ML/HI) mobile-first welfare scheme wizard — India + selected other countries incl. United States, United Kingdom and Canada (curated; not worldwide; see docs/COUNTRY_UK.md, docs/COUNTRY_CANADA.md). Deterministic rules only. Hindi UI complete; scheme body Hindi may fall back to English pending native review.

Repo: https://github.com/sidharthsuraj24-star/scheme-finder

## Stack

- Frontend: Next.js 15, React 19, Tailwind
- Backend: FastAPI, Pydantic v2, Uvicorn
- Data: data/schemes.json (curated schemes — India multi-state/central + BD/NP/LK/MV starters + US federal/state waves incl. Wave 5 CO/MN/SC/AL/LA, Wave 6 KY/OR/OK/CT/UT, Wave 7 IA/NV/AR/MS/KS, Wave 8 NM/NE/ID/HI/ME, and Wave 9 NH/RI/MT/DE/SD; in-memory; optional SQLite)
- Tests: pytest

## Run locally

### Backend (port 8000)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pytest -q
```

Endpoints: GET /health, GET /schemes, POST /api/v1/match (alias POST /match), POST /explain, GET /sources. Docs: http://127.0.0.1:8000/docs

### Frontend (port 3000)

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
npm run build
```

## Env vars

- NEXT_PUBLIC_API_URL (frontend): empty = same-origin `/api`; set to FastAPI base (no trailing slash) for dedicated API mode
- DATABASE_URL (backend optional): empty = in-memory JSON
- LLM_API_KEY (backend optional): empty = template explanations
- CORS_ORIGINS (backend): default * for demo; set to Vercel origin in prod (e.g. `https://YOUR-APP.vercel.app` when using dedicated API)
- REDIS_URL (backend): enable shared rate limits + optional match cache
- MATCH_CACHE_TTL_SEC (backend): 0=off; 60 for warm-cache demos
- WEB_CONCURRENCY (backend/Docker/Fly): uvicorn workers (default 2 in image)
- SCHEMES_PATH (backend optional): path to schemes.json
- PORT (hosting): Render/Railway/Fly inject this

## Catalogue trust (Phase 2 foundation)

- Signed releases: `python3 scripts/sign_catalogue_release.py` → `data/catalogue_release.json`
- Publish gate: `python3 scripts/check_catalogue_publish_ready.py`
- Audit log: `data/catalogue_audit.jsonl` (append-only)
- See docs/TRUST.md

## Product surface (Phase 3 foundation)

- Device-only saved profiles, parent-for-child wizard mode, `/ops` read-only dashboard
- Aggregate analytics (`POST /analytics/event`) — never invents eligibility
- See docs/PRODUCT.md, docs/ANALYTICS.md, docs/PRIVACY.md

## Matching notes

- Hard filters only from structured eligibility_rules (structured catalogue; see docs/SCHEMES.md).
- verify=true never returns likely_eligible.
- Maternity uses maternity_required; NFBS uses primary_breadwinner_deceased_required.
- Zero matches return HTTP 200 with a helpful message.
- Sort likely_eligible before uncertain, then by score.

## Deploy

See docs/DEPLOY.md for steps and blockers.

- Backend: backend/Dockerfile, render.yaml, backend/Procfile, backend/railway.toml, fly.toml
- Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
- Frontend: deploy frontend/ on Vercel (frontend/vercel.json); set NEXT_PUBLIC_API_URL to live API
- CORS defaults to * for demo

## Known limitations

- District collected in UI but unused in matcher.
- Several schemes verify=true; see verify_notes / docs/SCHEMES.md.
- Malayalam and Hindi scheme-body copy may need native review (UI chrome for both is shipped; missing `hi` scheme fields fall back to English).
- Not legal advice; confirm with implementing office.
- Substitutions: SQLite/in-memory not Supabase; template not LLM; local build not Cloud Agent.
- See docs/TEST_LOG.md for Phase 4 results.

## Docs

- docs/TRUST.md — Phase 2 trust foundation (roles, signed releases, audit)
- docs/ACCESSIBILITY.md — WCAG 2.2 AA audit, a11y regression suite (`cd frontend && npm run test:a11y`)
- docs/SECURITY.md — free security pass (ZAP, npm audit, pip-audit, gitleaks), headers/CSP, threat model, disclosure (`bash scripts/security_audit.sh`, `cd frontend && npm run test:security`)
- docs/CATALOGUE_OPS.md — Phase 4 catalogue ops foundation (candidates, URL tickets, packs)
- docs/PRODUCT.md — Phase 3 product surface + ops dashboard
- docs/PRIVACY.md — no account PII by default; ephemeral match profiles

- docs/SCALE.md — Phase 1 dedicated API + Redis + load evidence
- docs/API_CONTRACT.md, docs/SCHEMES.md, docs/SOURCES.md, docs/DECISIONS.md
- docs/TEST_LOG.md, docs/DEPLOY.md, docs/FINAL_REPORT.md

## Suggested next features

- Shareable results link; district/LSG deep links; more WCD FAQ rules; native ML review; PWA shell; lock CORS to Vercel origin once live
