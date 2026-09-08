# Scheme Finder

Bilingual (EN/ML) mobile-first Kerala/India welfare scheme wizard. Deterministic rules only.

Repo: https://github.com/sidharthsuraj24-star/scheme-finder

## Stack

- Frontend: Next.js 15, React 19, Tailwind
- Backend: FastAPI, Pydantic v2, Uvicorn
- Data: data/schemes.json (18 schemes, in-memory; optional SQLite)
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

- NEXT_PUBLIC_API_URL (frontend): API base URL, no trailing slash (default http://127.0.0.1:8000)
- DATABASE_URL (backend optional): empty = in-memory JSON
- LLM_API_KEY (backend optional): empty = template explanations
- CORS_ORIGINS (backend): default * for demo; set to Vercel origin in prod
- SCHEMES_PATH (backend optional): path to schemes.json
- PORT (hosting): Render/Railway/Fly inject this

## Matching notes

- Hard filters only from structured eligibility_rules (18 schemes).
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
- Malayalam may need native review.
- Not legal advice; confirm with implementing office.
- Substitutions: SQLite/in-memory not Supabase; template not LLM; local build not Cloud Agent.
- See docs/TEST_LOG.md for Phase 4 results.

## Docs

- docs/API_CONTRACT.md, docs/SCHEMES.md, docs/SOURCES.md, docs/DECISIONS.md
- docs/TEST_LOG.md, docs/DEPLOY.md, docs/FINAL_REPORT.md

## Suggested next features

- Shareable results link; district/LSG deep links; more WCD FAQ rules; native ML review; PWA shell; lock CORS to Vercel origin once live
