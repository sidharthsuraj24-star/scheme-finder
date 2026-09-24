# Analytics — privacy-preserving aggregates

**Date:** 2026-09-24 (IST)

## Hard rule

**Analytics never feed matcher eligibility.**  
Do not invent `max_annual_income`, age cut-offs, or category rules from hit counts, drop-off, or “top schemes.” Catalogue rules come only from official sources (`docs/SOURCES.md`, curator process in `docs/TRUST.md`).

## What we record

Allowed events (examples): `match_ok`, `match_error`, `share_copy`, `ops_view`.

Per event, optional:

- `country` (coarse)
- `result_count_bucket` (`0`, `1-3`, `4-10`, `11-30`, `31+`)
- `scheme_ids` (max 10 ids) for hit tallies

**Never:** profile bodies, income values, names, ages, districts, disability percents, share-link payloads, or raw IPs (optional salted IP hash remains access-log only — see `docs/PRIVACY.md`).

## Storage

- FastAPI: in-memory counters and/or Redis (`REDIS_URL`) with TTL (~48h). Fail open if Redis is down.
- Next.js same-origin demo: in-process memory on `POST /api/analytics/event`, optional forward to FastAPI.

Ops: `GET /ops/summary` includes `analytics.match_volume` / `match_volume_24h` style fields when available.

## Endpoint

`POST /analytics/event` / `POST /api/v1/analytics/event`  
Body: `{ "event": "match_ok", "country": "India", "scheme_ids": ["…"], "result_count": 12 }`  
Rate-limited with match paths.
