#!/usr/bin/env bash
# Run Scheme Finder FastAPI with multiple uvicorn workers.
#
# Suitable for local scale tests AND Docker/Fly (no .venv required in image).
#
# CPU / worker formula (CPU-bound /match evaluation):
#   WEB_CONCURRENCY = max(1, min(8, nproc))
#   On Fly shared-cpu-1x (1 vCPU, 512mb): prefer 2 workers.
#   On a 4-vCPU box: 4 workers is a good default for local load tests.
#   Do NOT set workers >> CPUs — GIL + catalogue RAM (~tens of MB each) waste memory.
#
# Usage:
#   ./scripts/run_api_workers.sh              # default WORKERS=nproc (capped), :8000
#   WORKERS=2 PORT=8000 ./scripts/run_api_workers.sh
#   # Docker/Fly CMD:
#   WEB_CONCURRENCY=2 ./scripts/run_api_workers.sh
#
# Shared rate limits / match cache across workers require REDIS_URL.
# In-memory rate limits are per-process when Redis is unset.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/backend"

NPROC="$(getconf _NPROCESSORS_ONLN 2>/dev/null || nproc 2>/dev/null || echo 2)"
DEFAULT_WORKERS="$NPROC"
if [ "$DEFAULT_WORKERS" -gt 8 ]; then DEFAULT_WORKERS=8; fi
if [ "$DEFAULT_WORKERS" -lt 1 ]; then DEFAULT_WORKERS=1; fi

WORKERS="${WORKERS:-${WEB_CONCURRENCY:-$DEFAULT_WORKERS}}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"

# Throughput tests often raise the limit; production should set explicitly.
export RATE_LIMIT_MAX="${RATE_LIMIT_MAX:-100000}"
export RATE_LIMIT_WINDOW_SEC="${RATE_LIMIT_WINDOW_SEC:-60}"
export MATCH_CACHE_TTL_SEC="${MATCH_CACHE_TTL_SEC:-0}"

if [ -x "$ROOT/backend/.venv/bin/uvicorn" ]; then
  UVICORN="$ROOT/backend/.venv/bin/uvicorn"
elif command -v uvicorn >/dev/null 2>&1; then
  UVICORN="$(command -v uvicorn)"
else
  echo "uvicorn not found (install backend requirements or activate .venv)" >&2
  exit 1
fi

echo "Starting uvicorn workers=$WORKERS host=$HOST port=$PORT redis=${REDIS_URL:+set}" >&2
exec "$UVICORN" app.main:app \
  --host "$HOST" \
  --port "$PORT" \
  --workers "$WORKERS"
