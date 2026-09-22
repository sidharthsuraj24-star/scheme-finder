"""Optional Redis cache for POST /match JSON responses.

Controlled by MATCH_CACHE_TTL_SEC (default 0 = off).
Only caches when TTL > 0 and Redis is available. Never caches eligibility
rules themselves — only the full JSON response for an identical request.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from typing import Any

from .redis_client import get_redis

logger = logging.getLogger(__name__)

_CACHE_PREFIX = "sf:match:"


def match_cache_ttl_sec() -> int:
    try:
        return max(0, int(os.environ.get("MATCH_CACHE_TTL_SEC", "0")))
    except ValueError:
        return 0


def cache_key_for(profile: dict[str, Any], options: dict[str, Any]) -> str:
    """Stable hash of normalized profile + options."""
    payload = {"profile": profile, "options": options}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{_CACHE_PREFIX}{digest}"


def get_cached_match(profile: dict[str, Any], options: dict[str, Any]) -> dict[str, Any] | None:
    ttl = match_cache_ttl_sec()
    if ttl <= 0:
        return None
    client = get_redis()
    if client is None:
        return None
    key = cache_key_for(profile, options)
    try:
        raw = client.get(key)
        if not raw:
            return None
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception as exc:  # noqa: BLE001
        logger.warning("match cache get failed: %s", exc)
    return None


def set_cached_match(
    profile: dict[str, Any],
    options: dict[str, Any],
    response: dict[str, Any],
) -> None:
    ttl = match_cache_ttl_sec()
    if ttl <= 0:
        return
    client = get_redis()
    if client is None:
        return
    key = cache_key_for(profile, options)
    try:
        client.setex(key, ttl, json.dumps(response, default=str))
    except Exception as exc:  # noqa: BLE001
        logger.warning("match cache set failed: %s", exc)
