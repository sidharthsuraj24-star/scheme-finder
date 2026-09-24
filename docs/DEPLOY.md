# Scheme Finder — Deployment

Date: 2026-09-08 (Asia/Calcutta)  
Repo: https://github.com/sidharthsuraj24-star/scheme-finder

## Preferred demo path: single-host Vercel (Next.js + `/api`)

As of Phase 6 the **matcher runs inside the Next.js app** (`frontend/src/lib/matching/` + App Router routes under `frontend/src/app/api/`).

- `GET /api/health`
- `GET /api/schemes` · `GET /api/schemes/[id]`
- `POST /api/match`

Frontend `NEXT_PUBLIC_API_URL` defaults to **empty** (same-origin `/api/match`). No separate Render/Fly backend is required for the public demo. You can still set `NEXT_PUBLIC_API_URL` to a FastAPI base if you want the Python API.

### Deploy frontend (E2E)

```bash
cd frontend
npx vercel@latest deploy --prod --yes
# or anonymous / preview:
npx vercel deploy --yes
```

Requires `vercel login` or `VERCEL_TOKEN`. If CLI is logged out, that is the blocker (see below).

## Auth / CLI blockers (build box)

| Tool | Auth | Notes |
|------|------|-------|
| npx vercel | Needs login or `VERCEL_TOKEN` | Without it: prod deploy blocked |
| Anonymous `vercel deploy --yes` | May create temporary claimable URL | TTL short unless claimed |
| Render / Fly / Railway | Separate tokens | Optional now — FastAPI still available via Docker/render.yaml |

### Exact Vercel auth blocker (if deploy fails)

```
Error: No existing credentials found. Please run `vercel login` or supply `VERCEL_TOKEN`.
```

Human fix once:

1. `cd frontend && npx vercel login` **or** export `VERCEL_TOKEN=...`
2. `npx vercel@latest deploy --prod --yes`
3. Leave `NEXT_PUBLIC_API_URL` unset (same-origin API).

Same-origin API routes remain ready in the repo regardless of deploy auth.

## Optional separate FastAPI backend

Still supported: `backend/` + `render.yaml` / `fly.toml` / Dockerfile. Set frontend env:

```
NEXT_PUBLIC_API_URL=https://YOUR-API-HOST
```

## Catalogue freshness

See `docs/DATA_REFRESH.md` and `data/catalogue_meta.json` (`updated_as_of: 2026-09-08`).

## End-to-end verification (same-origin)

1. Open the Vercel URL
2. `curl -s https://YOUR-VERCEL-URL/api/health`
3. Complete wizard → browser network: `POST /api/match` → 200


## Live E2E URL (Phase 6 — same-origin API)

- **Temporary anonymous deploy (claim to keep):** https://temporary-fast-gold-jvm9d74.vercel.app
- Claim: https://vercel.com/claim-deployment?code=fafd1aab-6559-43fd-9b8c-73e99fd054da
- Verified 2026-09-08: `GET /api/health` → ok · `POST /api/match` → matches (same-origin, empty `NEXT_PUBLIC_API_URL`)
- **Prod auth blocker:** `Error: No existing credentials found. Run vercel deploy --temporary ... or vercel login`. Plain `npx vercel deploy --yes` and `--prod` fail without `VERCEL_TOKEN` / login. Anonymous path that works: `npx vercel@latest deploy --yes --temporary`.



## Dedicated API + Redis deploy checklist (Phase 1 — 2026-09-24)

One-command path after secrets exist (Fly preferred, region `bom`):

```bash
# 0) Auth (blocker if missing)
fly auth login
# optional: fly auth whoami

# 1) Upstash (or Fly Redis) — copy REDIS_URL (rediss://...)
#    https://console.upstash.com → Create Redis → region near bom/Singapore/Mumbai

# 2) App + secrets
fly apps create scheme-finder-api --org personal   # skip if exists
fly secrets set REDIS_URL='rediss://default:TOKEN@HOST:6379'
fly secrets set ENV=production
fly secrets set CORS_ORIGINS='https://YOUR-APP.vercel.app'
# optional warm cache:
fly secrets set MATCH_CACHE_TTL_SEC=60
# production warm machines (edit fly.toml or):
#   fly scale count 1   # and set min_machines_running=1 in fly.toml

# 3) Deploy
fly deploy
fly status
curl -sS https://scheme-finder-api.fly.dev/ready
# expect: "rate_limit_backend":"redis", "schemes_loaded":true

# 4) Load evidence
RATE_LIMIT_MAX=100000  # already on server via secret if set
python scripts/loadtest_match.py --url https://scheme-finder-api.fly.dev \
  --concurrency 20 --requests 200 --profile india

# 5) Point Vercel frontend at dedicated API
#    Vercel project → Settings → Environment Variables:
#      NEXT_PUBLIC_API_URL=https://scheme-finder-api.fly.dev
#    Redeploy frontend.
```

**Build-box status (2026-09-24):** `fly auth whoami` → no access token;
`REDIS_URL` / `FLY_API_TOKEN` / `VERCEL_TOKEN` unset; `docker` not installed.
Local evidence uses `redis-server` + `scripts/run_api_workers.sh` (same env as compose).
Suraj must run `fly auth login` (and create Upstash) on a machine with a browser.

Render alternative: Blueprint `render.yaml`, attach Redis, set `REDIS_URL` + `CORS_ORIGINS`,
health path `/ready`.


## Phase 1 scale foundation

For horizontal scale (Redis rate limits, readiness, optional match cache, split
frontend/API deploy), see **`docs/SCALE.md`**.

Quick local stack:

```bash
docker compose -f docker-compose.scale.yml up --build
curl -s http://127.0.0.1:8000/ready
python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 20 --requests 200
```

Env highlights: `REDIS_URL`, `MATCH_CACHE_TTL_SEC`, frontend `UPSTASH_REDIS_REST_URL` +
`UPSTASH_REDIS_REST_TOKEN` for Vercel multi-instance rate limits.
