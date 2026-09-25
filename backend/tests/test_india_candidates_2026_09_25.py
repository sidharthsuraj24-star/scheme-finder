"""India freshness-check candidates (2026-09-25): PM-JANMAN added; queue outcomes recorded."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.db import reset_store
from app.matcher import evaluate_scheme, match_schemes
from app.models import MatchOptions, MatchProfile
from app.schemes_loader import load_schemes

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FE_DATA = ROOT / "frontend" / "data"
OPTS = MatchOptions(max_results=100)
EXPECTED = {
    "cand-in-pm-janman": "verified_add",
    "cand-in-pm-kusum": "deferred",
    "cand-in-svamitva": "deferred",
    "cand-in-jal-jeevan-mission": "rejected",
    "cand-in-pm-shri": "rejected",
    "cand-in-pm-ebus-sewa": "rejected",
}


@pytest.fixture(scope="module")
def schemes():
    return load_schemes()


@pytest.fixture(autouse=True)
def _store(schemes):
    reset_store(schemes)
    yield
    reset_store(schemes)


def _janman(schemes):
    return next(s for s in schemes if s["id"] == "in-pm-janman")


def test_candidate_queue_outcomes_recorded():
    raw = (DATA / "catalogue_candidates.json").read_bytes()
    assert raw == (FE_DATA / "catalogue_candidates.json").read_bytes()
    cands = {c["id"]: c for c in json.loads(raw)["candidates"]}
    for cid, status in EXPECTED.items():
        c = cands[cid]
        assert c["status"] == status, cid
        assert c["previous_status"] == "researching", cid  # moved through the queue
        assert c["country"] == "India"
        assert c["official_source_url"].startswith("https://"), cid
        assert len(c["reason"]) > 60, cid
    for cid in ("cand-in-jal-jeevan-mission", "cand-in-pm-shri", "cand-in-pm-ebus-sewa"):
        assert cands[cid]["reason"].startswith("Out of scope: infrastructure"), cid
    assert cands["cand-in-pm-janman"]["scheme_id_if_present"] == "in-pm-janman"
    assert "31.03.2026" in cands["cand-in-pm-kusum"]["reason"]
    assert "property card" in cands["cand-in-svamitva"]["reason"]


def test_candidate_audit_trail_present():
    lines = [json.loads(x) for x in (DATA / "catalogue_audit.jsonl").read_text().splitlines() if x.strip()]
    for cid, status in EXPECTED.items():
        statuses = [e.get("candidate_status") for e in lines if e.get("candidate_id") == cid]
        assert statuses[:3] == ["queued", "researching", status] or statuses[-3:] == ["queued", "researching", status], (cid, statuses)


def test_only_pm_janman_added_to_catalogue(schemes):
    ids = {s["id"] for s in schemes}
    assert "in-pm-janman" in ids
    for bad in ("in-pm-kusum", "pm-kusum", "in-svamitva", "in-jal-jeevan-mission", "in-pm-shri", "in-pm-ebus-sewa"):
        assert bad not in ids


def test_pm_janman_shape(schemes):
    s = _janman(schemes)
    er = s["eligibility_rules"]
    assert er["countries"] == ["India"]
    assert er["verify"] is True
    assert er["max_annual_income"] is None
    assert er["nationwide"] is False
    assert set(er["categories"]) == {"ST", "PVTG"}
    assert len(er["states"]) == 19 and "Andaman and Nicobar Islands" in er["states"]
    assert not ({"central", "nationwide"} & set(s["tags"]))
    assert "PVTG" in er["notes"]


def test_pm_janman_matching(schemes):
    s = _janman(schemes)
    st_mp = MatchProfile(country="India", state="Madhya Pradesh", age=40, annual_income=60_000,
                         occupations=["farmer"], categories=["ST"])
    assert not evaluate_scheme(s, st_mp).hard_fail
    assert "in-pm-janman" in {m.scheme_id for m in match_schemes(schemes, st_mp, OPTS).matched}
    # Not a PVTG state (e.g. Punjab) -> excluded
    assert evaluate_scheme(s, st_mp.model_copy(update={"state": "Punjab"})).hard_fail
    # General category household -> excluded
    assert evaluate_scheme(s, st_mp.model_copy(update={"categories": ["General"]})).hard_fail
    # Other countries never see it
    ca = MatchProfile(country="Canada", state="Ontario", age=40, annual_income=20_000, categories=["ST"])
    assert evaluate_scheme(s, ca).hard_fail
