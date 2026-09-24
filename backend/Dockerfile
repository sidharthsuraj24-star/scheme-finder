# Scheme Finder API — production image
# Build from repo root: docker build -f backend/Dockerfile -t scheme-finder-api .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    # Default 2 workers: fits Fly shared-cpu-1x / 512mb; override via WEB_CONCURRENCY.
    WEB_CONCURRENCY=2

WORKDIR /app

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend/ /app/backend/
COPY data/ /app/data/
COPY scripts/run_api_workers.sh /app/scripts/run_api_workers.sh
RUN chmod +x /app/scripts/run_api_workers.sh

WORKDIR /app/backend
EXPOSE 8000

# Multi-worker uvicorn (see scripts/run_api_workers.sh for CPU formula).
# WEB_CONCURRENCY / WORKERS / PORT / REDIS_URL / MATCH_CACHE_TTL_SEC honored.
CMD ["sh", "-c", "HOST=0.0.0.0 /app/scripts/run_api_workers.sh"]
