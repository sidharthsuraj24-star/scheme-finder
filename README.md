# Scheme Finder

Bilingual (English / Malayalam) mobile-first step wizard for Kerala/India welfare schemes. Deterministic rules only.

## Stack

- Frontend: Next.js 15, React 19, Tailwind
- Backend: FastAPI, Pydantic, Uvicorn
- Data: data/schemes.json (18 schemes)
- Tests: pytest

## Run locally

### Backend (port 8000)

cd backend; python3 -m venv .venv; source .venv/bin/activate; pip install -r requirements.txt; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; pytest -q

Match: POST /api/v1/match (alias POST /match). Health: GET /health.

### Frontend (port 3000)

cd frontend; cp .env.example .env.local; install deps; start Next.js on port 3000; run production build check.

## Env vars

- NEXT_PUBLIC_API_URL (frontend): API base URL
- DATABASE_URL (backend optional): empty = in-memory JSON
- LLM_API_KEY (backend optional): empty = template explanations

## Matching notes

- Hard filters only from structured eligibility_rules (18 schemes).
- verify=true never returns likely_eligible.
- Maternity uses maternity_required; NFBS uses primary_breadwinner_deceased_required.
- Zero matches return HTTP 200 with a helpful message.
- Sort likely_eligible before uncertain, then by score.

## Known limitations

- District collected in UI but unused in matcher.
- Several schemes verify=true; see verify_notes.
- Malayalam may need native review.
- Not legal advice; confirm with implementing office.
- See docs/TEST_LOG.md for Phase 4 results.

## Docs

- docs/API_CONTRACT.md, docs/SCHEMES.md, docs/SOURCES.md, docs/DECISIONS.md
- docs/TEST_LOG.md

## Suggested next features

- Shareable results link; district/LSG deep links; more WCD FAQ rules; native ML review; PWA shell
