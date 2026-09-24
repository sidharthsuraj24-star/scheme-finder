"""Privacy-preserving aggregate analytics (never feeds matcher eligibility).

Records counts only: event type, country, result_count bucket, optional scheme_id
hits. No profile bodies, income, names, ages, or districts.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from collections import defaultdict
from typing import Any

from .redis_client import get_redis

logger = logging.getLogger(__name__)

_LOCK = threading.Lock()
# In-memory: windowed counters keyed by day bucket (UTC day) then metric.
_MEMORY: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
_MEMORY_SCHEME: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

_ALLOWED_EVENTS = frozenset({"match_ok", "match_error", "share_copy", "ops_view"})
_MAX_SCHEME_IDS = 10
_SCHEME_ID_MAX_LEN = 64
_TTL_SEC = int(os.environ.get("ANALYTICS_TTL_SEC", str(48 * 3600)))
_REDIS_PREFIX = "sf:an:"


def _day_bucket(now: float | None = None) -> str:
    ts = int(now if now is not None else time.time())
    return time.strftime("%Y-%m-%d", time.gmtime(ts))


def _bucket_result_count(n: int | None) -> str | None:
    if n is None:
        return None
    try:
        v = int(n)
    except (TypeError, ValueError):
        return None
    if v < 0:
        return None
    if v == 0:
        return "0"
    if v <= 3:
        return "1-3"
    if v <= 10:
        return "4-10"
    if v <= 30:
        return "11-30"
    return "31+"


def record_event(
    event: str,
    *,
    country: str | None = None,
    scheme_ids: list[str] | None = None,
    result_count: int | None = None,
    result_count_bucket: str | None = None,
) -> dict[str, Any]:
    """Increment aggregate counters. Fail-open: never raises to callers."""
    if event not in _ALLOWED_EVENTS:
        return {"ok": False, "error": "invalid_event"}
    day = _day_bucket()
    country_key = (country or "unknown").strip()[:64] or "unknown"
    bucket = result_count_bucket or _bucket_result_count(result_count)
    ids: list[str] = []
    if scheme_ids:
        for sid in scheme_ids[:_MAX_SCHEME_IDS]:
            if isinstance(sid, str) and sid.strip() and len(sid) <= _SCHEME_ID_MAX_LEN:
                ids.append(sid.strip())

    metrics = [
        f"event:{event}",
        f"event:{event}:country:{country_key}",
    ]
    if bucket:
        metrics.append(f"event:{event}:bucket:{bucket}")

    try:
        client = get_redis()
        if client is not None:
            pipe = client.pipeline(transaction=False)
            for m in metrics:
                key = f"{_REDIS_PREFIX}{day}:{m}"
                pipe.incr(key)
                pipe.expire(key, _TTL_SEC)
            for sid in ids:
                skey = f"{_REDIS_PREFIX}{day}:scheme:{sid}"
                pipe.incr(skey)
                pipe.expire(skey, _TTL_SEC)
            pipe.execute()
            return {"ok": True, "backend": "redis", "day": day}
    except Exception as exc:  # noqa: BLE001 — fail open to memory
        logger.warning("analytics redis write failed (%s); using memory", exc)

    with _LOCK:
        store = _MEMORY[day]
        for m in metrics:
            store[m] += 1
        sstore = _MEMORY_SCHEME[day]
        for sid in ids:
            sstore[sid] += 1
    return {"ok": True, "backend": "memory", "day": day}


def _sum_prefix(store: dict[str, int], prefix: str) -> int:
    return sum(v for k, v in store.items() if k.startswith(prefix))


def snapshot(days: int = 1) -> dict[str, Any]:
    """Aggregate snapshot for ops dashboard. No PII."""
    days = max(1, min(7, int(days)))
    now = time.time()
    day_keys = [_day_bucket(now - i * 86400) for i in range(days)]
    match_ok = 0
    by_country: dict[str, int] = defaultdict(int)
    by_bucket: dict[str, int] = defaultdict(int)
    top_schemes: dict[str, int] = defaultdict(int)
    backend = "memory"

    client = get_redis()
    if client is not None:
        try:
            for day in day_keys:
                # Scan is ok for small demo keyspace; keys are TTL'd.
                for key in client.scan_iter(match=f"{_REDIS_PREFIX}{day}:*", count=200):
                    try:
                        val = int(client.get(key) or 0)
                    except Exception:  # noqa: BLE001
                        continue
                    suffix = key[len(f"{_REDIS_PREFIX}{day}:") :]
                    if suffix == "event:match_ok":
                        match_ok += val
                    elif suffix.startswith("event:match_ok:country:"):
                        by_country[suffix.split(":", 3)[-1]] += val
                    elif suffix.startswith("event:match_ok:bucket:"):
                        by_bucket[suffix.split(":", 3)[-1]] += val
                    elif suffix.startswith("scheme:"):
                        top_schemes[suffix[7:]] += val
            backend = "redis"
        except Exception as exc:  # noqa: BLE001
            logger.warning("analytics redis read failed (%s); using memory", exc)
            backend = "memory"

    if backend == "memory" or match_ok == 0:
        with _LOCK:
            for day in day_keys:
                store = _MEMORY.get(day) or {}
                match_ok += int(store.get("event:match_ok", 0))
                for k, v in store.items():
                    if k.startswith("event:match_ok:country:"):
                        by_country[k.split(":", 3)[-1]] += v
                    elif k.startswith("event:match_ok:bucket:"):
                        by_bucket[k.split(":", 3)[-1]] += v
                for sid, v in (_MEMORY_SCHEME.get(day) or {}).items():
                    top_schemes[sid] += v
            if any(_MEMORY.values()) or any(_MEMORY_SCHEME.values()):
                backend = "memory" if client is None else backend

    top = sorted(top_schemes.items(), key=lambda x: (-x[1], x[0]))[:15]
    return {
        "match_volume": match_ok,
        "match_volume_window_days": days,
        "match_volume_24h": match_ok if days == 1 else None,
        "by_country": dict(sorted(by_country.items(), key=lambda x: (-x[1], x[0]))[:20]),
        "by_result_bucket": dict(sorted(by_bucket.items())),
        "top_scheme_ids": [{"scheme_id": s, "hits": h} for s, h in top],
        "analytics_backend": backend if (client is not None or any(_MEMORY.values())) else "none",
        "note": "Aggregates only — never used for eligibility matching.",
    }


def reset_memory_for_tests() -> None:
    with _LOCK:
        _MEMORY.clear()
        _MEMORY_SCHEME.clear()
