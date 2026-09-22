#!/usr/bin/env bash
# Run Scheme Finder FastAPI with multiple uvicorn workers (local scale testing).
# Usage:
#   ./scripts/run_api_workers.sh              # default 4 workers on :8000
#   WORKERS=2 PORT=8000 ./scripts/run_api_workers.sh
#
# Rate limit is raised for throughput measurement. For shared limits across
# workers in production, set REDIS_URL (in-memory limits are per-process).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"
WORKERS="${WORKERS:-4}"
PORT="${PORT:-8000}"
HOST="${HOST:-127.0.0.1}"
export RATE_LIMIT_MAX="${RATE_LIMIT_MAX:-100000}"
export RATE_LIMIT_WINDOW_SEC="${RATE_LIMIT_WINDOW_SEC:-60}"
export MATCH_CACHE_TTL_SEC="${MATCH_CACHE_TTL_SEC:-0}"

exec .venv/bin/uvicorn app.main:app \
  --host "$HOST" \
  --port "$PORT" \
  --workers "$WORKERS"
