# Scheme Finder — Backend (Phase 2)

Deterministic FastAPI matcher for Kerala / India welfare schemes.

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Schemes load from `../data/schemes.json` into memory (SQLite dump optional via `db.maybe_init_sqlite`).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Liveness `{status, version}` |
| GET | `/schemes?lang=en\|ml` | Scheme summaries (`state`, `tag`, `verify` filters) |
| GET | `/schemes/{id}` | Full scheme record |
| POST | `/match` | Deterministic eligibility match |
| POST | `/explain` | Template (or LLM-stub) explanation |
| GET | `/sources` | Curated official URLs |

`/api/v1/...` aliases are also registered.

### POST /match body

Flat fields **or** nested `{ "profile": {...}, "options": {...} }`:

- `age`, `gender`, `state` (default `Kerala`), `district`
- `marital_status`, `occupations` (list or comma-string), `categories`
- `annual_income` **or** `monthly_household_income` (derive the other)
- `disability` / `disability_percent`, `land_ownership`, `language`

Zero matches → HTTP 200 with `matched: []` and a helpful `message`.

## Matcher rules

Hard filters come **only** from structured `eligibility_rules`.  
If `verify=true`, matches are marked `uncertain` (never `likely_eligible`).  
Explanations are templates from `matched_rules`; `LLM_API_KEY` enables an optional stub that still does not decide eligibility.

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## Env

```
DATABASE_URL=     # empty → in-memory + optional SQLite file
LLM_API_KEY=      # empty → template explanations only
```
