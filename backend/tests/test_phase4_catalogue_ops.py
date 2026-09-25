"""Phase 4 foundation: candidates, URL tickets, pack manifests, ops hooks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data"
FE_DATA = REPO_ROOT / "frontend" / "data"
SCRIPTS = REPO_ROOT / "scripts"
PACKS = DATA / "packs"

REQUIRED_SCHEME_FIELDS = (
    "id",
    "scheme_name",
    "official_source_url",
    "eligibility_rules",
    "tags",
)

# Representative packs for regression (India states + US federal + 2 US states)
REPR_PACKS = (
    "india-kerala@1.0.0",
    "india-central@1.0.0",
    "india-sikkim@1.0.0",
    "us-federal@1.0.0",
    "us-california@1.0.0",
    "us-texas@1.0.0",
)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("NEXT_PUBLIC_SHOW_OPS", "1")
    monkeypatch.delenv("OPS_DASHBOARD_TOKEN", raising=False)
    from app.analytics import reset_memory_for_tests

    reset_memory_for_tests()
    from app import main as main_mod

    with TestClient(main_mod.app) as c:
        yield c


def test_dual_tree_schemes_still_identical():
    assert (DATA / "schemes.json").read_bytes() == (FE_DATA / "schemes.json").read_bytes()


def test_catalogue_candidates_schema():
    path = DATA / "catalogue_candidates.json"
    assert path.is_file()
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(raw, dict)
    cands = raw["candidates"]
    assert isinstance(cands, list)
    schemes = json.loads((DATA / "schemes.json").read_text(encoding="utf-8"))
    ids = {s["id"] for s in schemes}
    valid = {"needs_review", "queued", "researching", "verified_add", "rejected", "deferred"}
    for c in cands:
        assert c["id"] and c["name"] and c["official_source_url"]
        assert c["status"] in valid
        assert str(c["official_source_url"]).startswith("http")
        # If historical mapped id present, it must exist in catalogue
        mapped = c.get("scheme_id_if_present")
        if mapped:
            assert mapped in ids
        # Never invent queued duplicates of catalogue ids without research
        if c["status"] == "queued" and mapped:
            assert mapped not in ids


def test_url_tickets_jsonl_and_open_count():
    path = DATA / "url_tickets.jsonl"
    assert path.is_file()
    sys.path.insert(0, str(SCRIPTS))
    import url_tickets as ut  # noqa: WPS433

    rows = ut.read_tickets(path)
    assert len(rows) >= 1
    for r in rows:
        assert r.get("ticket_id")
        assert r.get("url", "").startswith("http")
        assert r.get("status") in {"open", "investigating", "fixed", "wontfix"}
    summary = ut.summarize(path)
    # Pre-seeded known-flaky tickets were all resolved 2026-09-25 (URL fixes);
    # open_count is data-dependent, so only check it is consistent.
    assert summary["open_count"] >= 0
    assert sum(summary["by_status"].values()) == summary["unique_keys"]


def test_url_tickets_dual_tree_identical():
    assert (DATA / "url_tickets.jsonl").read_bytes() == (FE_DATA / "url_tickets.jsonl").read_bytes()


def test_url_ticket_fixes_2026_09_25_resolved_in_catalogue():
    sys.path.insert(0, str(SCRIPTS))
    import url_tickets as ut  # noqa: WPS433

    latest = ut.latest_by_key(ut.read_tickets(DATA / "url_tickets.jsonl"))
    for key in (
        ("nsap-nfbs", "https://nsap.nic.in/"),
        ("ap-ntr-bharosa-oap", "https://sspensions.ap.gov.in/SSP/Home"),
        ("sk-unmarried-women-pension", "https://pensionscheme.sikkim.gov.in/"),
    ):
        assert latest[key]["status"] == "fixed"
    by_id = {s["id"]: s for s in json.loads((DATA / "schemes.json").read_text(encoding="utf-8"))}
    nfbs = by_id["nsap-nfbs"]
    assert nfbs["official_source_url"] == "https://nsap.dord.gov.in/"
    assert nfbs["apply_url"] == "https://nsap.dord.gov.in/"
    assert "nsap.nic.in/" not in (nfbs["apply_url"] + nfbs["official_source_url"])
    for sid in ("nsap-nfbs", "ap-ntr-bharosa-oap", "sk-unmarried-women-pension"):
        assert by_id[sid]["last_verified"] >= "2026-09-25"
        assert by_id[sid]["eligibility_rules"]["verify"] is True


def test_url_probe_retries_get_after_head_404(monkeypatch: pytest.MonkeyPatch):
    sys.path.insert(0, str(SCRIPTS))
    import urllib.error
    import write_url_health_snapshot as w  # noqa: WPS433

    class _Resp:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def fake_urlopen(req, timeout=0):
        if req.get_method() == "HEAD":
            raise urllib.error.HTTPError(req.full_url, 404, "nf", {}, None)
        return _Resp()

    monkeypatch.setattr(w.urllib.request, "urlopen", fake_urlopen)
    status = w.probe("https://pensionscheme.sikkim.gov.in/")
    assert status == "GET 200 (HEAD 404)"
    assert w._ok(status)


def test_url_ticket_upsert_and_resolve(tmp_path: Path):
    sys.path.insert(0, str(SCRIPTS))
    import url_tickets as ut  # noqa: WPS433

    path = tmp_path / "url_tickets.jsonl"
    a = ut.upsert_failure(
        scheme_id="demo-scheme",
        url="https://example.gov/demo",
        http_or_error="FAIL HTTP 404",
        path=path,
        now="2026-09-24T10:00:00+05:30",
    )
    assert a["status"] == "open"
    b = ut.upsert_failure(
        scheme_id="demo-scheme",
        url="https://example.gov/demo",
        http_or_error="FAIL HTTP 500",
        path=path,
        now="2026-09-24T11:00:00+05:30",
    )
    assert b["ticket_id"] == a["ticket_id"]
    assert b["last_seen"] == "2026-09-24T11:00:00+05:30"
    fixed = ut.resolve_ok(
        scheme_id="demo-scheme",
        url="https://example.gov/demo",
        http_or_error="HEAD 200",
        path=path,
        now="2026-09-24T12:00:00+05:30",
    )
    assert fixed is not None
    assert fixed["status"] == "fixed"
    assert ut.open_ticket_count(path) == 0


def test_pack_manifests_representative():
    schemes = json.loads((DATA / "schemes.json").read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in schemes}
    index = json.loads((PACKS / "index.json").read_text(encoding="utf-8"))
    assert index["pack_count"] >= 6
    assert (FE_DATA / "packs" / "index.json").is_file()

    for full_id in REPR_PACKS:
        path = PACKS / f"{full_id}.json"
        assert path.is_file(), f"missing pack {full_id}"
        # frontend mirror
        assert (FE_DATA / "packs" / f"{full_id}.json").is_file()
        manifest = json.loads(path.read_text(encoding="utf-8"))
        assert manifest["full_id"] == full_id
        assert manifest["scheme_count"] == len(manifest["scheme_ids"])
        assert manifest["scheme_count"] >= 1
        for sid in manifest["scheme_ids"]:
            assert sid in by_id, f"{sid} listed in {full_id} but missing from schemes.json"
            s = by_id[sid]
            for field in REQUIRED_SCHEME_FIELDS:
                assert field in s and s[field] is not None, f"{sid} missing {field}"
            url = s["official_source_url"]
            assert isinstance(url, str) and url.startswith(("http://", "https://"))


def test_ops_summary_exposes_phase4_counts(client: TestClient):
    r = client.get("/ops/summary")
    assert r.status_code == 200
    body = r.json()
    assert "url_tickets" in body
    assert body["url_tickets"]["open_count"] >= 0
    assert "candidates" in body
    assert body["candidates"]["total"] >= 1
    assert "deferred" in (body["candidates"].get("by_status") or {})
    assert "packs" in body
    assert body["packs"]["pack_count"] >= 6
    assert body.get("catalogue_ops_doc") == "docs/CATALOGUE_OPS.md"
    # open tickets also mirrored under url_health
    assert (body.get("url_health") or {}).get("open_url_tickets") == body["url_tickets"]["open_count"]
