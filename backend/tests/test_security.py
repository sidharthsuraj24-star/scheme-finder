"""Security-focused tests: validation, path confinement, headers, rate limit, docs."""

from __future__ import annotations

import importlib
from pathlib import Path

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
    from app import main as main_mod

    monkeypatch.setenv("RATE_LIMIT_MAX", "3")
    _clear_rate_limits(main_mod.app)
    body = {"age": 68, "monthly_household_income": 4000, "state": "Kerala"}
    statuses = [client.post("/match", json=body).status_code for _ in range(6)]
    assert 429 in statuses, statuses
    assert any(s == 200 for s in statuses)


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
