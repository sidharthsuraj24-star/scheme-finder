# Scheme Finder — Scale architecture (Phase 1 foundation)

Date: 2026-09-22 (Asia/Calcutta)

This document describes the **enterprise-scale foundation** landed in Phase 1.
It does **not** claim that free Vercel / a single free Redis instance can serve
500k–1M concurrent users. That target needs paid capacity and load-test evidence.

## Target architecture

```
CDN / static frontend (Vercel or similar)
        │  NEXT_PUBLIC_API_URL → dedicated API
        ▼
FastAPI match API  (multi-instance: Fly / Render / Cloud Run / Railway)
        │
        ├── Catalogue loaded once per process (in-memory SchemeStore)
        ├── Redis: shared rate limits (required for horizontal scale)
        └── Redis: optional match-response cache (MATCH_CACHE_TTL_SEC > 0)
```

| Layer | Role |
|-------|------|
| CDN / Vercel frontend | Serve UI + optional same-origin `/api/*` for small demos |
| Dedicated FastAPI | Stateless match workers; scale out with more machines |
| Redis / Upstash | Cross-instance rate limits; optional response cache |
| Catalogue | Loaded once per process from `data/schemes.json` — no per-request disk I/O |

## SLOs (aspirational for dedicated API)

| Metric | Target |
|--------|--------|
| Match latency p95 (warm process, cold Redis cache miss) | **&lt; 200 ms** |
| Match latency p95 (warm Redis match cache hit) | **&lt; 50 ms** |
| Error rate (5xx / total) | **&lt; 0.1%** |
| Rate-limit correctness | Shared Redis counter across instances |

Measure with `scripts/loadtest_match.py` against a staging URL — not against
wishful thinking.

## Rate limiting

| Environment | Backend |
|-------------|---------|
| FastAPI without `REDIS_URL` | In-memory sliding window (`deque`) — **single process only** |
| FastAPI with `REDIS_URL` | Redis fixed window (`INCR` + `EXPIRE`) per IP |
| Redis briefly down | **Fail-to-memory** — demo never hard-dies; limits become per-instance until Redis returns |
| Next.js `/api/match` | In-memory, or Upstash REST when `UPSTASH_REDIS_REST_URL` + `UPSTASH_REDIS_REST_TOKEN` are set |

Fail-to-memory is an intentional availability choice for demos. For strict
global caps under Redis outage, switch to fail-closed (reject) in a later phase.

## Optional match cache

- Env: `MATCH_CACHE_TTL_SEC` (default **0** = off).
- When TTL &gt; 0 and Redis is up: cache full JSON response keyed by SHA-256 of
  normalized `profile` + `options`.
- Never invents eligibility; only stores what `match_schemes` already returned.
- Cache is Redis-only (no in-process cache for multi-instance consistency).

## Hosting options

| Component | Options |
|-----------|---------|
| API | Fly.io, Render, Google Cloud Run, Railway |
| Redis | Upstash (serverless), Redis Cloud, Fly Redis, Memorystore |
| Frontend | Vercel (static + optional edge), Cloudflare Pages + CDN |

### Local scale stack

```bash
docker compose -f docker-compose.scale.yml up --build
# API: http://localhost:8000
# Redis: localhost:6379
# Env inside api: REDIS_URL=redis://redis:6379/0
```

### Fly / Render placeholders

- `fly.toml`: set secrets `REDIS_URL`, prefer `min_machines_running ≥ 1` for prod,
  **512mb** VM memory recommended for catalogue + uvicorn.
- `render.yaml`: add `REDIS_URL` (sync: false) and optional `MATCH_CACHE_TTL_SEC`.

## Honest note: 500k–1M concurrent

Reaching **500k–1M concurrent** users requires:

1. **Paid** multi-region API capacity (not free Vercel serverless alone).
2. **Paid** Redis / Upstash with enough ops/sec and connections.
3. CDN for static assets; dedicated match API behind a load balancer.
4. Connection limits, keep-alive, and horizontal autoscaling tuned under load.
5. **Load-test evidence** on production-like hardware (`scripts/loadtest_match.py`
   or k6/Locust) showing p95 and error-rate SLOs hold.

Phase 1 only lands the **foundation**: shared Redis limits, readiness, optional
cache, compose stack, and migration path. Capacity is a billing + ops problem.

## Migration: same-origin Vercel → split deploy

1. Deploy FastAPI with `REDIS_URL` (compose / Fly / Render).
2. Confirm `GET /ready` → `schemes_loaded: true`, `rate_limit_backend: "redis"`.
3. Set frontend `NEXT_PUBLIC_API_URL=https://YOUR-API-HOST`.
4. Set CORS on API: `CORS_ORIGINS=https://YOUR-VERCEL-HOST`.
5. (Optional) Keep Vercel `/api/match` as fallback; add Upstash REST env vars for
   multi-instance Vercel rate limits if you still use same-origin routes.
6. Run loadtest against the FastAPI URL; tune `RATE_LIMIT_*` and machine count.
7. Gradually shift traffic; monitor `/ready` and error rates.

## Env vars (Phase 1)

| Var | Default | Purpose |
|-----|---------|---------|
| `REDIS_URL` | unset | Enable Redis rate limit (+ cache when TTL &gt; 0) |
| `MATCH_CACHE_TTL_SEC` | `0` | Match response cache TTL; `0` disables |
| `RATE_LIMIT_MAX` | `30` | Max match POSTs per window per IP |
| `RATE_LIMIT_WINDOW_SEC` | `60` | Window length |
| `UPSTASH_REDIS_REST_URL` | unset | Frontend Upstash REST (with token) |
| `UPSTASH_REDIS_REST_TOKEN` | unset | Frontend Upstash REST token |
| `CORS_ORIGINS` | `*` (dev) / empty (prod) | Browser origins for dedicated API |
| `NEXT_PUBLIC_API_URL` | empty | Frontend → dedicated API base |

## Related

- `docs/DEPLOY.md` — deploy paths and Phase 1 pointer
- `docker-compose.scale.yml` — local redis + api
- `scripts/loadtest_match.py` — concurrency smoke tool
