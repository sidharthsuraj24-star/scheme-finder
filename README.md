# scheme-finder

Bilingual (EN/ML) step-wizard matcher for Kerala/India government welfare schemes — Next.js + FastAPI.

## Phase 1
Curated seed data in `data/` and docs in `docs/`.

## Phase 2 — Backend
Deterministic FastAPI matcher in `backend/`.

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest -q
```

See `backend/README.md` and `docs/API_CONTRACT.md`.

## Phase 3 — Frontend
Mobile-first Next.js (App Router) + Tailwind UI in `frontend/`.

Terminal 1 — API:

```bash
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Terminal 2 — UI:

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Production check: `npm run build` inside `frontend/`.

Open http://localhost:3000

Match endpoint: backend serves both `POST /match` and `POST /api/v1/match` (see `backend/app/main.py`). The UI prefers `/api/v1/match` and falls back to `/match`.
