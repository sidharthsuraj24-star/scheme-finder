"""Security-focused tests: validation, path confinement, headers, rate limit, docs."""

from __future__ import annotations

import importlib
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.models import MatchProfile, MatchRequest
from app.schemes_loader import confine_schemes_path
from app.security import MatchRateLimitMiddleware


def _clear_rate_limits(app) -> None:
    seen: set[int] = set()

    def walk(obj: object) -> None:
        if obj is None or id(obj) in seen:
            return
        seen.add(id(obj))
        if isinstance(obj, MatchRateLimitMiddleware):
            obj._hits.clear()
            obj._ops_hits.clear()
        for attr in ("app", "application"):
            walk(getattr(obj, attr, None))

    # Force stack build
    _ = getattr(app, "middleware_stack", None)
    walk(app.middleware_stack)


@pytest.fixture()
def client():
    from app import main as main_mod

    with TestClient(main_mod.app) as c:
        _clear_rate_limits(main_mod.app)
        yield c
        _clear_rate_limits(main_mod.app)


def test_reject_absurd_age():
    with pytest.raises(ValidationError):
        MatchProfile(age=999)
    with pytest.raises(ValidationError):
        MatchProfile(age=-1)


def test_reject_absurd_income():
    with pytest.raises(ValidationError):
        MatchProfile(annual_income=1e12)
    with pytest.raises(ValidationError):
        MatchProfile(monthly_household_income=-5)


def test_reject_huge_occupation_list():
    with pytest.raises(ValidationError):
        MatchProfile(occupations=[f"job{i}" for i in range(100)])


def test_reject_nested_flags():
    with pytest.raises(ValidationError):
        MatchProfile(flags={"a": {"nested": True}})


def test_max_results_capped():
    with pytest.raises(ValidationError):
        MatchRequest(options={"max_results": 10_000})


def test_schemes_path_cannot_escape_repo():
    with pytest.raises(ValueError, match="escapes"):
        confine_schemes_path(Path("/etc/passwd"))
    with pytest.raises(ValueError, match="escapes|\\.json"):
        confine_schemes_path(Path("/tmp/evil.json"))


def test_schemes_path_allows_repo_data():
    repo_data = Path(__file__).resolve().parents[2] / "data" / "schemes.json"
    confined = confine_schemes_path(repo_data)
    assert confined.is_file()
    assert confined.name == "schemes.json"


def test_security_headers_on_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert r.headers.get("x-frame-options") == "DENY"
    assert "no-referrer" in (r.headers.get("referrer-policy") or "")
    assert "default-src" in (r.headers.get("content-security-policy") or "")


def test_match_rejects_invalid_profile(client):
    r = client.post("/api/v1/match", json={"age": 500, "state": "Kerala"})
    assert r.status_code == 422


def test_match_rate_limit(client, monkeypatch):
    """In-memory rate limit still works when REDIS_URL is unset."""
    from app import main as main_mod

    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.setenv("RATE_LIMIT_MAX", "3")
    _clear_rate_limits(main_mod.app)
    body = {"age": 68, "monthly_household_income": 4000, "state": "Kerala"}
    statuses = [client.post("/match", json=body).status_code for _ in range(6)]
    assert 429 in statuses, statuses
    assert any(s == 200 for s in statuses)


def test_match_rate_limit_redis_mock(client, monkeypatch):
    """When REDIS_URL is set, middleware uses Redis INCR; mock enforces limit."""
    from app import main as main_mod
    from app import redis_client as rc

    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("RATE_LIMIT_MAX", "3")
    monkeypatch.setenv("RATE_LIMIT_WINDOW_SEC", "60")
    rc.reset_redis_client()

    counters: dict[str, int] = {}

    mock = MagicMock()

    def incr(key: str) -> int:
        counters[key] = counters.get(key, 0) + 1
        return counters[key]

    mock.incr.side_effect = incr
    mock.expire.return_value = True
    mock.ping.return_value = True

    monkeypatch.setattr("app.security.get_redis", lambda: mock)
    monkeypatch.setattr("app.security.rate_limit_backend", lambda: "redis")
    _clear_rate_limits(main_mod.app)

    body = {"age": 68, "monthly_household_income": 4000, "state": "Kerala"}
    statuses = [client.post("/match", json=body).status_code for _ in range(6)]
    assert 429 in statuses, statuses
    assert any(s == 200 for s in statuses)
    assert mock.incr.called

    monkeypatch.delenv("REDIS_URL", raising=False)
    rc.reset_redis_client()


def test_match_rate_limit_redis_fail_to_memory(client, monkeypatch):
    """If Redis raises, middleware falls back to in-memory and still rate-limits."""
    from app import main as main_mod
    from app import redis_client as rc

    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("RATE_LIMIT_MAX", "3")
    rc.reset_redis_client()

    mock = MagicMock()
    mock.incr.side_effect = ConnectionError("redis down")
    monkeypatch.setattr("app.security.get_redis", lambda: mock)
    monkeypatch.setattr("app.security.rate_limit_backend", lambda: "redis")
    _clear_rate_limits(main_mod.app)

    body = {"age": 68, "monthly_household_income": 4000, "state": "Kerala"}
    statuses = [client.post("/match", json=body).status_code for _ in range(6)]
    assert 429 in statuses, statuses
    assert any(s == 200 for s in statuses)

    monkeypatch.delenv("REDIS_URL", raising=False)
    rc.reset_redis_client()


def test_ready_endpoint(client, monkeypatch):
    monkeypatch.delenv("REDIS_URL", raising=False)
    for path in ("/ready", "/api/v1/ready"):
        r = client.get(path)
        assert r.status_code == 200, path
        data = r.json()
        assert data["status"] == "ready"
        assert data["schemes_loaded"] is True
        assert data["scheme_count"] > 0
        assert data["rate_limit_backend"] == "memory"
        assert data["redis"]["configured"] is False


def test_ready_reports_redis_when_configured(client, monkeypatch):
    from app import redis_client as rc

    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    rc.reset_redis_client()
    monkeypatch.setattr(
        "app.main.ping_redis",
        lambda: {"configured": True, "ok": True, "optional": True},
    )
    monkeypatch.setattr("app.main.rate_limit_backend", lambda: "redis")

    r = client.get("/ready")
    assert r.status_code == 200
    data = r.json()
    assert data["rate_limit_backend"] == "redis"
    assert data["redis"]["configured"] is True

    monkeypatch.delenv("REDIS_URL", raising=False)
    rc.reset_redis_client()


def test_match_cache_off_by_default(client, monkeypatch):
    monkeypatch.setenv("MATCH_CACHE_TTL_SEC", "0")
    monkeypatch.delenv("REDIS_URL", raising=False)
    body = {"age": 68, "monthly_household_income": 4000, "state": "Kerala"}
    r = client.post("/match", json=body)
    assert r.status_code == 200


def test_match_cache_uses_redis_when_ttl_set(client, monkeypatch):
    from app import match_cache as mc
    from app import redis_client as rc

    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/0")
    monkeypatch.setenv("MATCH_CACHE_TTL_SEC", "60")
    rc.reset_redis_client()

    store: dict[str, str] = {}
    mock = MagicMock()

    def get(key: str):
        return store.get(key)

    def setex(key: str, ttl: int, value: str):
        store[key] = value
        return True

    mock.get.side_effect = get
    mock.setex.side_effect = setex
    mock.ping.return_value = True
    monkeypatch.setattr("app.match_cache.get_redis", lambda: mock)

    body = {"age": 68, "monthly_household_income": 4000, "state": "Kerala"}
    r1 = client.post("/match", json=body)
    assert r1.status_code == 200
    assert store, "expected cache write"
    r2 = client.post("/match", json=body)
    assert r2.status_code == 200
    assert r1.json() == r2.json()

    monkeypatch.setenv("MATCH_CACHE_TTL_SEC", "0")
    monkeypatch.delenv("REDIS_URL", raising=False)
    rc.reset_redis_client()


def test_payload_too_large(client):
    huge = b"x" * (70 * 1024)
    r = client.post(
        "/match",
        content=huge,
        headers={"Content-Type": "application/json", "Content-Length": str(len(huge))},
    )
    assert r.status_code == 413


def test_docs_disabled_in_production(monkeypatch):
    monkeypatch.setenv("ENV", "production")
    monkeypatch.setenv("CORS_ORIGINS", "https://example.com")
    import app.main as main_mod

    importlib.reload(main_mod)
    try:
        with TestClient(main_mod.app) as c:
            assert c.get("/docs").status_code == 404
            assert c.get("/openapi.json").status_code == 404
            assert c.get("/health").status_code == 200
    finally:
        monkeypatch.setenv("ENV", "development")
        importlib.reload(main_mod)


# --- Phase 2 security pass (2026-09-25) -----------------------------------


def test_hardening_headers_on_api(client):
    r = client.get("/health")
    assert r.headers["strict-transport-security"].startswith("max-age=63072000")
    assert r.headers["cache-control"] == "no-store"
    assert r.headers["cross-origin-opener-policy"] == "same-origin"
    assert "camera=()" in r.headers["permissions-policy"]


def test_ops_401_is_generic_and_constant_time(monkeypatch):
    monkeypatch.setenv("OPS_DASHBOARD_TOKEN", "phase2-secret-token")
    monkeypatch.delenv("NEXT_PUBLIC_SHOW_OPS", raising=False)
    from app import main as main_mod
    from app import security as sec

    with TestClient(main_mod.app) as c:
        _clear_rate_limits(main_mod.app)
        r = c.get("/ops/summary", headers={"Authorization": "Bearer wrong"})
        assert r.status_code == 401
        body = r.text
        # No env-var names / auth-mode hints and never the configured token.
        assert "OPS_DASHBOARD_TOKEN" not in body
        assert "NEXT_PUBLIC_SHOW_OPS" not in body
        assert "phase2-secret-token" not in body
        assert r.json()["detail"]["error"]["message"] == "Unauthorized"
        # Token in the query string is never accepted.
        assert c.get("/ops/summary?token=phase2-secret-token").status_code == 401
        assert c.get("/ops/summary", headers={"X-Ops-Token": "phase2-secret-token"}).status_code == 200
        # Prefix of the token must not pass.
        assert c.get("/ops/summary", headers={"Authorization": "Bearer phase2-secret"}).status_code == 401
    import inspect

    assert "compare_digest" in inspect.getsource(sec.ops_authorized)


def test_ops_auth_is_rate_limited(monkeypatch):
    monkeypatch.setenv("OPS_DASHBOARD_TOKEN", "phase2-secret-token")
    monkeypatch.setenv("OPS_RATE_LIMIT_MAX", "3")
    from app import main as main_mod

    with TestClient(main_mod.app) as c:
        _clear_rate_limits(main_mod.app)
        codes = [c.get("/ops/summary", headers={"Authorization": "Bearer nope"}).status_code for _ in range(5)]
        assert codes[:3] == [401, 401, 401]
        assert codes[3:] == [429, 429]
        _clear_rate_limits(main_mod.app)


def test_chunked_post_without_length_rejected(client):
    def gen():
        yield b'{"age": 30}'

    r = client.post("/match", content=gen(), headers={"Content-Type": "application/json"})
    assert r.status_code == 411


def test_cors_never_allows_credentials(client):
    r = client.options(
        "/match",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"},
    )
    assert r.headers.get("access-control-allow-credentials") != "true"
