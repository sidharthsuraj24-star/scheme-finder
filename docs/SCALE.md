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



## Local multi-worker uvicorn (single machine)

A single uvicorn worker is CPU-bound on `/match` (process holds the catalogue in
memory; geo indexes prune candidates, but one event-loop still serializes
CPU-heavy evaluation under high concurrency — p95 rises sharply around c=100).

For **local scale** on one host, run multiple workers (each loads its own
catalogue + geo index):

```bash
cd backend
RATE_LIMIT_MAX=100000 MATCH_CACHE_TTL_SEC=0 \
  .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
```

Notes:

- `--workers N` = N processes. In-memory rate limits are **per worker**; set
  `REDIS_URL` for a shared limiter when using more than one worker.
- Match cache (`MATCH_CACHE_TTL_SEC`) is Redis-only; leave at `0` for cold-path
  load tests.
- Tip: compare single-worker vs multi-worker with the same harness:

```bash
# Single worker baseline / regression
RATE_LIMIT_MAX=100000 MATCH_CACHE_TTL_SEC=0 \
  backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000

python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 20 --requests 200 --profile india
python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 50 --requests 500 --profile india
python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 100 --requests 1000 --profile india
```

Horizontal scale across machines still needs Redis + a load balancer (see
compose / Fly / Render above). Geo candidate pruning (country / state indexes)
cuts per-request scheme evaluations when `profile.country` / `state` are set;
it does **not** invent or alter eligibility rules.

## Related

- `docs/DEPLOY.md` — deploy paths and Phase 1 pointer
- `docker-compose.scale.yml` — local redis + api
- `scripts/loadtest_match.py` — concurrency smoke tool


## Measured local load tests (2026-09-22)

Hardware: shared box (~8 vCPU). Catalogue: 589 schemes with geo pruning.
Rate limit raised (`RATE_LIMIT_MAX=100000`); `MATCH_CACHE_TTL_SEC=0`; no Redis.

### Single worker (after geo prune)

| Concurrency | Requests | RPS | p50 / p95 (ms) |
| ---: | ---: | ---: | --- |
| 20 | 200 | ~250 | 66 / 176 |
| 50 | 500 | ~219 | 177 / 558 |
| 100 | 1000 | ~146 | 396 / 2109 |

### Four workers (`uvicorn --workers 4` / `scripts/run_api_workers.sh`)

| Concurrency | Requests | RPS | p50 / p95 (ms) | Errors |
| ---: | ---: | ---: | --- | --- |
| 20 | 200 | **488** | 22 / 170 | 0 |
| 50 | 500 | **272** | 129 / 483 | 0 |
| 100 | 1000 | **162** | 328 / 2032 | 0 |
| 200 | 2000 | **194** | 512 / 4512 | 0 |

Takeaway: multi-worker roughly **doubles** RPS at moderate concurrency (c=20: 250→488). At high concurrency (c≥100) p95 still climbs — need more CPU/replicas + Redis shared rate limits, not more local workers alone on a contended box.

Local run:

```bash
./scripts/run_api_workers.sh          # WORKERS=4 PORT=8000
python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 20 --requests 200
```


## Load test results (2026-09-24)

Hardware: shared box (~8 vCPU, ~16 GiB). Catalogue: **822** schemes. Stack:
`redis-server` on `127.0.0.1:6379` + `scripts/run_api_workers.sh` with
`WEB_CONCURRENCY=2`, `REDIS_URL=redis://127.0.0.1:6379/0`,
`RATE_LIMIT_MAX=100000`. (`docker compose` / `docker.io` **not installed** on
the build box — same env as `docker-compose.scale.yml`; compose files still
shipped for Suraj's machine.)

`GET /ready` confirmed: `rate_limit_backend: "redis"`, `redis.ok: true`,
`schemes_loaded: true`.

Harness: `scripts/loadtest_match.py` (India sample profile). Match JSON body
≈ **227 KB** — transfer dominates under high concurrency even on cache hits.

### A) Redis on, `MATCH_CACHE_TTL_SEC=0` (cache-miss / compute path)

| Concurrency | Requests | RPS | p50 / p95 / p99 (ms) | Error rate | vs SLO p95 &lt;200ms (miss) |
| ---: | ---: | ---: | --- | ---: | --- |
| 20 | 200 | **268.4** | 70.0 / **109.4** / 121.2 | 0.000% | **PASS** |
| 50 | 500 | 186.7 | 197.5 / 661.4 / 940.6 | 0.000% | FAIL (saturated) |
| 100 | 1000 | 129.1 | 420.4 / 2494.8 / 4450.7 | 0.000% | FAIL (saturated) |

### B) Redis on, `MATCH_CACHE_TTL_SEC=60` (warm match cache)

| Concurrency | Requests | RPS | p50 / p95 / p99 (ms) | Error rate | vs SLO p95 &lt;50ms (hit) |
| ---: | ---: | ---: | --- | ---: | --- |
| 5 | 100 | **323.8** | 14.1 / **20.3** / 39.8 | 0.000% | **PASS** |
| 10 | 200 | 325.9 | 26.8 / 51.6 / 67.5 | 0.000% | FAIL (borderline) |
| 20 | 200 | 306.4 | 52.3 / 119.8 / 125.3 | 0.000% | FAIL (payload×c) |
| 50 | 500 | 194.4 | 181.1 / 684.7 / 980.7 | 0.000% | FAIL (saturated) |
| 100 | 1000 | 118.7 | 495.1 / 2385.8 / 3868.3 | 0.000% | FAIL (saturated) |

### Error-rate SLO (&lt; 0.1%)

**PASS** on all runs above (0 transport / 0 5xx).

### C) Two API replicas

**Skipped on this box** — no Docker Engine for
`docker-compose.scale.replicas.yml --scale api=2`. Override file +
`scripts/nginx-scale.conf` are ready for Suraj's Docker host. Local substitute
was `WEB_CONCURRENCY=2` (two uvicorn processes, shared Redis).

### Verdict (honest)

| SLO | Result |
|-----|--------|
| p95 miss &lt;200ms | **PASS** at c=20 on this box; fails when concurrency saturates CPU |
| p95 hit &lt;50ms | **PASS** at c≤5; large ~227KB responses push p95 over 50ms by c=10–20 |
| Error rate &lt;0.1% | **PASS** |
| 500k–1M concurrent | **Not claimed** — needs paid multi-region API + Redis capacity |

### Deploy path status (2026-09-24)

| Check | Result |
|-------|--------|
| `fly auth whoami` | **Blocked** — no access token (`fly auth login` required) |
| `REDIS_URL` / Upstash in env | **Unset** (no secret values present) |
| `FLY_API_TOKEN` / `VERCEL_TOKEN` | **Unset** |
| `docker` / compose | **Not installed** on build box |
| Live dedicated API URL | **None yet** — see deploy checklist in `docs/DEPLOY.md` |

