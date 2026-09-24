"""Phase 2 trust foundation: signed release checksum + immutable audit log."""

from __future__ import annotations

import hashlib
import json
import logging
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / "scripts"
DATA_SCHEMES = REPO_ROOT / "data" / "schemes.json"
FE_SCHEMES = REPO_ROOT / "frontend" / "data" / "schemes.json"
RELEASE_PATH = REPO_ROOT / "data" / "catalogue_release.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_dual_tree_schemes_identical():
    assert DATA_SCHEMES.is_file() and FE_SCHEMES.is_file()
    assert DATA_SCHEMES.read_bytes() == FE_SCHEMES.read_bytes()


def test_release_checksum_matches_schemes_bytes():
    assert RELEASE_PATH.is_file(), "run scripts/sign_catalogue_release.py first"
    release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    expected = release["schemes_sha256"]
    assert _sha256(DATA_SCHEMES) == expected
    assert _sha256(FE_SCHEMES) == expected
    schemes = json.loads(DATA_SCHEMES.read_text(encoding="utf-8"))
    assert release["scheme_count"] == len(schemes)


def test_sign_script_verify_exits_zero():
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / "sign_catalogue_release.py"), "--verify"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_append_audit_append_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    sys.path.insert(0, str(SCRIPTS))
    import append_catalogue_audit as audit  # noqa: WPS433

    path = tmp_path / "catalogue_audit.jsonl"
    monkeypatch.setenv("CATALOGUE_ACTOR", "test-curator")
    e1 = audit.append_audit(
        action="update",
        scheme_ids=["demo-1"],
        notes="first",
        path=path,
        commit_sha="abc",
    )
    e2 = audit.append_audit(
        action="release",
        scheme_ids=[],
        notes="second",
        release_checksum="deadbeef",
        path=path,
        commit_sha="def",
    )
    raw = path.read_text(encoding="utf-8")
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    assert len(lines) == 2
    parsed = audit.read_audit_entries(path)
    assert len(parsed) == 2
    assert parsed[0]["action"] == "update"
    assert parsed[0]["scheme_ids"] == ["demo-1"]
    assert parsed[0]["actor"] == "test-curator"
    assert parsed[1]["action"] == "release"
    assert parsed[1]["release_checksum"] == "deadbeef"
    assert raw.startswith(json.dumps(e1, ensure_ascii=False, separators=(",", ":")) + "\n")
    assert e2["notes"] == "second"


@pytest.fixture()
def client():
    from app import main as main_mod

    with TestClient(main_mod.app) as c:
        yield c


def test_catalogue_meta_endpoint_exposes_checksum(client: TestClient):
    r = client.get("/catalogue/meta")
    assert r.status_code == 200
    body = r.json()
    assert "catalogue" in body
    release = body.get("release")
    assert release is not None
    assert release.get("schemes_sha256")
    assert len(release["schemes_sha256"]) == 64
    ready = client.get("/ready")
    assert ready.status_code == 200
    assert ready.json().get("schemes_sha256") == release["schemes_sha256"]


def test_match_access_log_omits_profile_pii(client: TestClient, caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.INFO, logger="scheme_finder.access"):
        r = client.post(
            "/match",
            json={
                "profile": {
                    "country": "India",
                    "state": "Kerala",
                    "age": 70,
                    "annual_income": 120000,
                }
            },
        )
        assert r.status_code == 200
    joined = " ".join(
        rec.getMessage() for rec in caplog.records if rec.name == "scheme_finder.access"
    )
    assert "match_access" in joined
    assert "country=India" in joined or "country=India" in joined
    assert "annual_income" not in joined
    assert "120000" not in joined
