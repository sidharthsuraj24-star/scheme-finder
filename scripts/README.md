# Scripts

## Scheme freshness checklist

```bash
# Local checklist (no network)
python3 scripts/scheme_freshness_check.py

# Also HEAD/GET official_source_url values
python3 scripts/scheme_freshness_check.py --check-urls
```

Exits `0` even when URLs fail (report-only). Exit `1` only on script crash.
Does **not** edit eligibility rules.


## API workers + load test (Phase 1 scale)

```bash
# Local Redis + multi-worker API (compose alternative)
redis-server --daemonize yes
REDIS_URL=redis://127.0.0.1:6379/0 MATCH_CACHE_TTL_SEC=0 WEB_CONCURRENCY=2 \
  ./scripts/run_api_workers.sh

# Or Docker Compose
docker compose -f docker-compose.scale.yml up --build
# Warm cache override:
docker compose -f docker-compose.scale.yml -f docker-compose.scale.cache.yml up --build

python scripts/loadtest_match.py --url http://127.0.0.1:8000 --concurrency 20 --requests 200
```

Worker formula: `WEB_CONCURRENCY = max(1, min(8, nproc))`; Fly 1 shared CPU → 2.
See `docs/SCALE.md`.
