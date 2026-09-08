# scheme-finder

Bilingual (EN/ML) chat-style matcher for Kerala/India government welfare schemes — Next.js + FastAPI.

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
