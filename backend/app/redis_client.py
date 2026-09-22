"""Optional Redis helpers for rate limiting and match-response cache.

When REDIS_URL is unset, callers use in-memory fallbacks.
When Redis is briefly unavailable, prefer fail-to-memory so the demo
never hard-dies (documented in docs/SCALE.md).
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

_client: Any | None = None
_client_failed = False


def redis_url() -> str:
    return os.environ.get("REDIS_URL", "").strip()


def rate_limit_backend() -> str:
    """Report configured backend: redis if URL set (even if temporarily down), else memory."""
    return "redis" if redis_url() else "memory"


def get_redis() -> Any | None:
    """Return a sync Redis client or None if unavailable / not configured.

    On connection/import failure, returns None (caller should fall back to memory).
    """
    global _client, _client_failed
    url = redis_url()
    if not url:
        return None
    if _client is not None:
        return _client
    if _client_failed:
        # Allow retry after previous failure by clearing on next successful URL check
        # Soft reset: try once more if we previously failed
        pass
    try:
        import redis  # type: ignore[import-untyped]

        client = redis.Redis.from_url(
            url,
            decode_responses=True,
            socket_connect_timeout=0.5,
            socket_timeout=0.5,
        )
        client.ping()
        _client = client
        _client_failed = False
        return _client
    except Exception as exc:  # noqa: BLE001 — fail open to memory
        logger.warning("Redis unavailable (%s); falling back to memory", exc)
        _client = None
        _client_failed = True
        return None


def reset_redis_client() -> None:
    """Test helper: drop cached client so next get_redis() reconnects."""
    global _client, _client_failed
    _client = None
    _client_failed = False


def ping_redis() -> dict[str, Any]:
    """Readiness probe. Returns status dict; does not raise."""
    url = redis_url()
    if not url:
        return {"configured": False, "ok": True, "optional": True}
    client = get_redis()
    if client is None:
        return {"configured": True, "ok": False, "optional": True, "error": "unreachable"}
    try:
        client.ping()
        return {"configured": True, "ok": True, "optional": True}
    except Exception as exc:  # noqa: BLE001
        return {"configured": True, "ok": False, "optional": True, "error": str(exc)}
