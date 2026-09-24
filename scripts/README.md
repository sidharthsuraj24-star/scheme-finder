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


## Catalogue trust (Phase 2 foundation)

```bash
# Sign release after schemes.json changes (both trees must match)
python3 scripts/sign_catalogue_release.py --changelog "Describe catalogue change"
python3 scripts/sign_catalogue_release.py --verify

# Append audit line (also done automatically by sign script on release)
CATALOGUE_ACTOR="suraj" python3 scripts/append_catalogue_audit.py \
  --action update --scheme-ids id1,id2 --notes "Why"

# Publisher gate before main push
python3 scripts/check_catalogue_publish_ready.py
```

See `docs/TRUST.md`. Does **not** edit eligibility rules.


## Catalogue ops (Phase 4 foundation)

```bash
# Candidates
python3 scripts/list_catalogue_candidates.py
python3 scripts/update_catalogue_candidate.py --id cand-in-example --status researching \
  --reason "Checking official portal"

# URL tickets + health snapshot
python3 scripts/write_url_health_snapshot.py --probe-known-flaky   # short allowlist only
python3 scripts/list_url_tickets.py

# Versioned pack manifests (membership only)
python3 scripts/generate_pack_manifests.py --version 1.0.0
```

See `docs/CATALOGUE_OPS.md`. Does **not** invent eligibility or auto-edit schemes.
