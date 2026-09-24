"""Security middleware: rate limiting, headers, request size caps.

Rate limit strategy (Phase 1 scale):
- If REDIS_URL is set: Redis fixed-window counter (INCR + EXPIRE) per IP for
  POST match paths. Shared across API instances.
- Else: in-memory sliding-window deque (single-process / demo).
- If Redis is briefly unavailable: fail-to-memory so the demo never hard-dies
  (see docs/SCALE.md).
"""

from __future__ import annotations

import logging
import os
import time
from collections import defaultdict, deque
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .redis_client import get_redis, rate_limit_backend

logger = logging.getLogger(__name__)

# Default: 30 match requests / 60s / IP (in-memory; fine for single-process demo).
RATE_LIMIT_WINDOW_SEC = float(os.environ.get("RATE_LIMIT_WINDOW_SEC", "60"))
RATE_LIMIT_MAX = int(os.environ.get("RATE_LIMIT_MAX", "30"))
MAX_BODY_BYTES = int(os.environ.get("MAX_BODY_BYTES", str(64 * 1024)))  # 64 KiB

_REDIS_KEY_PREFIX = "sf:rl:"


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip() or "unknown"
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _is_match_path(path: str) -> bool:
    p = path.rstrip("/")
    return p.endswith("/match") or p.endswith("/analytics/event")


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        # API JSON only — restrictive CSP still useful against MIME confusion.
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'none'; frame-ancestors 'none'; base-uri 'none'",
        )
        response.headers.setdefault("X-XSS-Protection", "0")
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        limit = int(os.environ.get("MAX_BODY_BYTES", str(MAX_BODY_BYTES)))
        cl = request.headers.get("content-length")
        if cl is not None:
            try:
                if int(cl) > limit:
                    return JSONResponse(
                        status_code=413,
                        content={
                            "error": {
                                "code": "payload_too_large",
                                "message": f"Request body exceeds {limit} bytes",
                            }
                        },
                    )
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": {
                            "code": "bad_content_length",
                            "message": "Invalid Content-Length header",
                        }
                    },
                )
        return await call_next(request)


class MatchRateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding/fixed-window rate limit for POST /match (and /api/v1/match).

    Uses Redis when REDIS_URL is set; otherwise in-memory deque.
    On Redis errors, falls back to in-memory so demos keep working.
    """

    def __init__(self, app, *, max_requests: int | None = None, window_sec: float | None = None):
        super().__init__(app)
        self._max_override = max_requests
        self._window_override = window_sec
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def _limits(self) -> tuple[int, float]:
        max_req = self._max_override if self._max_override is not None else int(
            os.environ.get("RATE_LIMIT_MAX", str(RATE_LIMIT_MAX))
        )
        window = self._window_override if self._window_override is not None else float(
            os.environ.get("RATE_LIMIT_WINDOW_SEC", str(RATE_LIMIT_WINDOW_SEC))
        )
        return max_req, window

    def _allow_memory(self, ip: str) -> bool:
        max_req, window = self._limits()
        now = time.monotonic()
        q = self._hits[ip]
        cutoff = now - window
        while q and q[0] < cutoff:
            q.popleft()
        if len(q) >= max_req:
            return False
        q.append(now)
        return True

    def _allow_redis(self, ip: str) -> bool | None:
        """Return True/False if Redis handled it, or None to signal fallback to memory."""
        client = get_redis()
        if client is None:
            return None
        max_req, window = self._limits()
        # Fixed window keyed by IP + window bucket (shared across instances).
        bucket = int(time.time() // max(1, int(window)))
        key = f"{_REDIS_KEY_PREFIX}{ip}:{bucket}"
        try:
            count = client.incr(key)
            if count == 1:
                client.expire(key, int(window) + 1)
            return int(count) <= max_req
        except Exception as exc:  # noqa: BLE001
            logger.warning("Redis rate-limit error (%s); falling back to memory", exc)
            return None

    def _allow(self, ip: str) -> bool:
        if rate_limit_backend() == "redis":
            result = self._allow_redis(ip)
            if result is not None:
                return result
            # Fail-to-memory when Redis briefly unavailable.
        return self._allow_memory(ip)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method == "POST" and _is_match_path(request.url.path):
            ip = _client_ip(request)
            if not self._allow(ip):
                _, window = self._limits()
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "rate_limited",
                            "message": "Too many match requests; try again shortly.",
                        }
                    },
                    headers={"Retry-After": str(int(window))},
                )
        return await call_next(request)


def ops_authorized(request: Request) -> bool:
    """Allow ops when token matches, or open demo when NEXT_PUBLIC_SHOW_OPS=1 and no token set.

    If OPS_DASHBOARD_TOKEN is set, require Authorization: Bearer <token>.
    If unset: allow when NEXT_PUBLIC_SHOW_OPS is 1/true/yes (demo), else deny.
    """
    token = os.environ.get("OPS_DASHBOARD_TOKEN", "").strip()
    if token:
        auth = (request.headers.get("authorization") or "").strip()
        if auth.lower().startswith("bearer "):
            got = auth[7:].strip()
            return got == token and bool(got)
        # Also accept X-Ops-Token for simple demos
        alt = (request.headers.get("x-ops-token") or "").strip()
        return alt == token
    show = os.environ.get("NEXT_PUBLIC_SHOW_OPS", "").strip().lower()
    return show in ("1", "true", "yes")
