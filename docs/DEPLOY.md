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

