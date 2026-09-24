"""Phase 3 foundation: ops summary, analytics aggregates, parent-child matcher audit."""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from app.analytics import record_event, reset_memory_for_tests, snapshot
from app.db import get_store
from app.matcher import match_schemes
from app.models import MatchOptions, MatchProfile


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NEXT_PUBLIC_SHOW_OPS", "1")
    monkeypatch.delenv("OPS_DASHBOARD_TOKEN", raising=False)
    reset_memory_for_tests()
    from app import main as main_mod

    with TestClient(main_mod.app) as c:
        yield c


def test_analytics_event_rejects_unknown(client: TestClient):
    r = client.post("/analytics/event", json={"event": "steal_profile", "country": "India"})
    # Pydantic validation → 422; defensive handler → 400
    assert r.status_code in (400, 422)


def test_analytics_event_and_ops_summary(client: TestClient):
    r = client.post(
        "/api/v1/analytics/event",
        json={
            "event": "match_ok",
            "country": "United States",
            "scheme_ids": ["us-trump-accounts", "us-529-qtp"],
            "result_count": 5,
        },
    )
    assert r.status_code == 200
    assert r.json().get("ok") is True

    ops = client.get("/ops/summary")
    assert ops.status_code == 200
    body = ops.json()
    assert body["scheme_count"] >= 800
    assert body.get("schemes_sha256")
    assert "coverage" in body
    assert "url_health" in body
    assert body["analytics"]["match_volume"] >= 1
    assert "United States" in (body["analytics"].get("by_country") or {})
    # No PII keys
    blob = str(body)
    assert "annual_income" not in blob
    assert "disability_percent" not in blob


def test_ops_requires_token_when_configured(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OPS_DASHBOARD_TOKEN", "secret-ops-token")
    monkeypatch.delenv("NEXT_PUBLIC_SHOW_OPS", raising=False)
    reset_memory_for_tests()
    from app import main as main_mod

    with TestClient(main_mod.app) as c:
        denied = c.get("/ops/summary")
        assert denied.status_code == 401
        ok = c.get("/ops/summary", headers={"Authorization": "Bearer secret-ops-token"})
        assert ok.status_code == 200


def test_parent_child_us_savings_matcher_audit():
    """Beneficiary age on profile surfaces Trump/Coverdell; ABLE needs disability.

    No new eligibility fields invented in Phase 3 — UI wires existing age/disability.
    """
    store = get_store()
    opts = MatchOptions(max_results=80, include_verify_uncertain=True)

    adult = MatchProfile(
        age=42,
        country="United States",
        state="California",
        annual_income=90000,
        occupations=["other"],
        categories=["none"],
        disability=False,
        land_ownership="none",
    )
    adult_ids = {m.scheme_id for m in match_schemes(store.schemes, adult, opts).matched}
    assert "us-trump-accounts" not in adult_ids
    assert "us-coverdell-esa" not in adult_ids
    assert "us-529-qtp" in adult_ids  # no federal max_age

    child = MatchProfile(
        age=10,
        country="United States",
        state="California",
        annual_income=90000,
        occupations=["student"],
        categories=["none"],
        disability=False,
        land_ownership="none",
        is_student=True,
    )
    child_ids = {m.scheme_id for m in match_schemes(store.schemes, child, opts).matched}
    assert "us-trump-accounts" in child_ids
    assert "us-coverdell-esa" in child_ids
    assert "us-529-qtp" in child_ids
    assert "us-able-accounts" not in child_ids  # needs disability

    child_pwd = MatchProfile(
        age=12,
        country="United States",
        state="California",
        annual_income=90000,
        occupations=["student"],
        categories=["none"],
        disability=True,
        disability_percent=50,
        land_ownership="none",
        is_student=True,
    )
    pwd_ids = {m.scheme_id for m in match_schemes(store.schemes, child_pwd, opts).matched}
    assert "us-able-accounts" in pwd_ids
    assert "us-trump-accounts" in pwd_ids


def test_analytics_memory_snapshot_no_profile_fields():
    reset_memory_for_tests()
    record_event("match_ok", country="India", scheme_ids=["demo"], result_count=0)
    snap = snapshot(days=1)
    assert snap["match_volume"] >= 1
    assert "note" in snap
    assert "profile" not in snap
