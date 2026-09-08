# Scheme Finder — Deployment

Date: 2026-09-08 (Asia/Calcutta)
Repo: https://github.com/sidharthsuraj24-star/scheme-finder

## What was added

| File | Purpose |
|------|--------|
| backend/Dockerfile | Production API image (copies backend/ + data/) |
| .dockerignore | Slimmer build context |
| render.yaml | Render Blueprint free web service |
| backend/Procfile | Railway/Heroku-style start |
| backend/railway.toml | Railway Nixpacks start + healthcheck |
| fly.toml | fly.io app config (region bom) |
| frontend/vercel.json | Vercel Next.js hints |

Backend start command (all hosts):
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

CORS: backend reads CORS_ORIGINS (default `*` for demo; credentials disabled when `*`).

## CLI status on build box (2026-09-08)

| Tool | Present | Auth |
|------|---------|------|
| npx vercel (59.x) | yes | Logged out — no VERCEL_TOKEN |
| flyctl (~0.4) | installed to ~/.fly/bin | no access token |
| render CLI | not installed | no RENDER_API_KEY |
| railway CLI | not installed | no RAILWAY_TOKEN |
| docker | not installed | n/a |
| gh | yes | logged in as sidharthsuraj24-star |

## Blockers (need human once)

### Backend (pick one free-ish host)

**Option A — Render free (recommended, no card for free web service)**
1. Sign in at https://dashboard.render.com
2. New + > Blueprint > connect sidharthsuraj24-star/scheme-finder
3. Apply render.yaml → creates scheme-finder-api
4. After deploy, note URL like https://scheme-finder-api.onrender.com
5. Optional env: CORS_ORIGINS=https://YOUR-FRONTEND.vercel.app

**Option B — Railway**
1. railway login; railway init from repo; set root to backend or use Procfile
2. Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
3. May require card depending on plan/region

**Option C — fly.io**
1. export PATH="$HOME/.fly/bin:$PATH"
2. fly auth login
3. From repo root: fly launch --no-deploy && fly deploy
4. Trial often asks for payment method

### Frontend — Vercel

1. vercel login   # or set VERCEL_TOKEN
2. From frontend/: npx vercel --yes
   Or link monorepo Root Directory = frontend in Vercel project settings
3. Project env: NEXT_PUBLIC_API_URL=https://YOUR-API-HOST
4. Redeploy after setting the env var

Temporary claimable deploy (no login) was attempted; see FINAL_REPORT for outcome.

## Env vars checklist

Frontend: NEXT_PUBLIC_API_URL
Backend: PORT (auto), CORS_ORIGINS, DATABASE_URL (optional), LLM_API_KEY (optional), SCHEMES_PATH (optional)

## End-to-end verification

1. curl -s https://API/health
2. Open Vercel URL, complete wizard, confirm match results load
3. Browser network: POST /api/v1/match → 200

## Live URLs (as of Phase 5 attempt)

- Backend: **NOT DEPLOYED** — needs Render/Fly/Railway login (see blockers). No free public API URL without account.
- Frontend (anonymous temporary Vercel, ~1h TTL unless claimed):
  - URL: https://temporary-fast-gold-jvm9d74.vercel.app
  - Claim (keep it): https://vercel.com/claim-deployment?code=fafd1aab-6559-43fd-9b8c-73e99fd054da
  - Note: build baked NEXT_PUBLIC_API_URL from local .env.local (http://127.0.0.1:8000), so browser match calls will fail until redeployed with a live API URL after backend is up.
