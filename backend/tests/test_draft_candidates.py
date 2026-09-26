"""Phase 4 automation: auto-draft candidates from official sources.

Fixture-driven only — every test runs with the network disabled.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import urllib.request
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = Path(__file__).parent / "fixtures" / "candidate_sources"
SCRIPT = ROOT / "scripts" / "draft_candidates_from_sources.py"
SCHEMES = ROOT / "data" / "schemes.json"


def _load():
    spec = importlib.util.spec_from_file_location("draft_candidates_from_sources", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


dc = _load()


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def boom(*_a, **_k):
        raise AssertionError("tests must not touch the network")

    monkeypatch.setattr(urllib.request, "urlopen", boom)


@pytest.fixture()
def queue(tmp_path: Path) -> dict[str, Path]:
    cands = tmp_path / "catalogue_candidates.json"
    fe = tmp_path / "fe" / "catalogue_candidates.json"
    fe.parent.mkdir()
    data = json.loads((ROOT / "data" / "catalogue_candidates.json").read_text(encoding="utf-8"))
    # Pre-existing queue row whose URL a fixture item reuses (URL dedupe).
    data["candidates"].append(
        {
            "id": "cand-in-existing-queue-row",
            "name": "Some earlier lead",
            "country": "India",
            "official_source_url": "https://pib.gov.in/PressReleasePage.aspx?PRID=9990004",
            "status": "queued",
            "reason": "fixture",
            "noted_at": "2026-09-20T10:00:00+05:30",
            "actor": "test",
            "notes": "",
        }
    )
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    cands.write_text(text, encoding="utf-8")
    fe.write_text(text, encoding="utf-8")
    return {"cands": cands, "fe": fe, "tmp": tmp_path}


ALL = "pib-en,pib-hi,gov-uk,canada-news,us-federal-register"


def _argv(q, *extra):
    return [
        "--offline-dir",
        str(FIXTURES),
        "--candidates",
        str(q["cands"]),
        "--frontend-candidates",
        str(q["fe"]),
        "--today",
        "2026-09-25",
        "--sources",
        ALL,
        "--myscheme-json",
        str(FIXTURES / "myscheme.json"),
        *extra,
    ]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_dry_run_writes_nothing_and_reports(queue, capsys):
    before = _sha(queue["cands"])
    schemes_before = _sha(SCHEMES)
    out_json = queue["tmp"] / "summary.json"
    assert dc.main(_argv(queue, "--dry-run", "--digest", "--summary-json", str(out_json))) == 0
    assert _sha(queue["cands"]) == before
    assert _sha(SCHEMES) == schemes_before
    md = capsys.readouterr().out
    assert "DRY RUN" in md and "| Source | Status |" in md
    s = json.loads(out_json.read_text())
    assert s["dry_run"] is True and s["queue_written"] is False
    names = [c["name"] for src in s["sources"] for c in src["new"]]
    assert names == [
        "Cabinet approves new Pradhan Mantri Example Artisan Yojana for traditional artisans",
        "प्रधानमंत्री ने उदाहरण कौशल योजना का शुभारंभ किया",
        "New Example Carers Grant scheme opens for applications",
        "Government of Canada launches the Example Youth Apprenticeship Grant",
        "Establishment of the Example Rural Broadband Grant Program",
        "Example State Weavers Assistance Scheme",
    ]


def test_filters_dedupes_and_known_mentions(queue):
    cat = dc.Catalogue(
        json.loads(SCHEMES.read_text(encoding="utf-8")),
        json.loads(queue["cands"].read_text(encoding="utf-8"))["candidates"],
    )
    res = {
        r.id: r
        for r in dc.run(
            ALL.split(",") + ["myscheme"],
            cat,
            today=date(2026, 9, 25),
            since_days=3,
            max_items=50,
            max_new=20,
            fetcher=None,
            offline_dir=FIXTURES,
            myscheme_json=FIXTURES / "myscheme.json",
        )
    }
    pib = res["pib-en"]
    assert pib.items_seen == 6
    assert pib.skipped_old == 1  # June item outside --since-days
    # PM-KISAN headline = update to an existing scheme, not a new candidate.
    assert [k["scheme_id"] for k in pib.known_mentions] == ["pm-kisan"]
    # Same PIB URL as an existing queue row (www-insensitive) → duplicate.
    assert any(d["by"] == "url" and d["matched"] == "cand-in-existing-queue-row" for d in pib.duplicates)
    # "Statement by", convocation → filtered out.
    assert all("Statement" not in c["name"] and "convocation" not in c["name"] for c in pib.new)
    # Canada media advisory filtered by category; FR correction filtered.
    assert len(res["canada-news"].new) == 1
    assert [c["name"] for c in res["us-federal-register"].new] == [
        "Establishment of the Example Rural Broadband Grant Program"
    ]
    # myScheme: PM-KISAN name fuzzy-matches the catalogue; nameless row ignored.
    ms = res["myscheme"]
    assert ms.items_seen == 2
    assert [d["matched"] for d in ms.duplicates] == ["pm-kisan"]
    assert ms.duplicates[0]["by"].startswith("name~")
    assert [c["name"] for c in ms.new] == ["Example State Weavers Assistance Scheme"]


def test_write_appends_needs_review_rows_verbatim_unverified(queue):
    schemes_before = _sha(SCHEMES)
    n_before = len(json.loads(queue["cands"].read_text())["candidates"])
    # Point the audit log at tmp so the repo audit trail is untouched.
    assert dc.main(_argv(queue, "--summary-json", str(queue["tmp"] / "s.json"))) == 0
    data = json.loads(queue["cands"].read_text(encoding="utf-8"))
    assert queue["cands"].read_bytes() == queue["fe"].read_bytes(), "dual-tree copies must stay identical"
    # Only rows appended by this offline run (found_at pinned to --today), so a
    # live auto-draft already in the repo queue does not inflate the count.
    new = [
        c
        for c in data["candidates"]
        if c.get("auto_drafted") and c.get("found_at") == "2026-09-25"
    ]
    assert len(data["candidates"]) == n_before + len(new) == n_before + 6
    for c in new:
        assert c["status"] == "needs_review"
        assert c["verified"] is False
        assert c["id"].startswith("cand-auto-")
        assert c["source_url"] == c["official_source_url"]
        assert c["source_url"].startswith("https://")
        assert c["found_at"] == "2026-09-25"
        assert c["actor"] == "draft_candidates_from_sources"
        assert "unverified" in c["notes"].lower()
        # Never invent eligibility: no rule-like keys anywhere in the draft.
        blob = json.dumps(c).lower()
        for banned in ("eligibility_rules", "income_max", "age_min", "age_max", "benefits"):
            assert banned not in blob
        assert c["extracted"], "at least the title is extracted"
        for key, f in c["extracted"].items():
            assert f["verified"] is False
            assert f["source_field"]
            assert isinstance(f["value"], str) and f["value"]
        assert c["extracted"]["title"]["value"] == c["name"]
    ms = next(c for c in new if c["source"]["id"] == "myscheme")
    assert ms["extracted"]["ministry"]["value"] == "Department of Handlooms (fixture)"
    assert ms["extracted"]["beneficiary_state"]["value"] == "Kerala"
    assert ms["official_source_url"] == "https://www.myscheme.gov.in/schemes/eswas"
    # schemes.json is never touched.
    assert _sha(SCHEMES) == schemes_before


def test_second_run_is_idempotent(queue):
    assert dc.main(_argv(queue, "--summary-json", str(queue["tmp"] / "a.json"))) == 0
    first = queue["cands"].read_bytes()
    assert dc.main(_argv(queue, "--summary-json", str(queue["tmp"] / "b.json"))) == 0
    s = json.loads((queue["tmp"] / "b.json").read_text())
    assert s["new_candidates"] == 0
    assert s["duplicates_skipped"] >= 6
    assert json.loads(queue["cands"].read_bytes())["candidates"] == json.loads(first)["candidates"]


def test_max_new_caps_queue_growth(queue):
    assert dc.main(_argv(queue, "--dry-run", "--max-new", "2", "--summary-json", str(queue["tmp"] / "c.json"))) == 0
    assert json.loads((queue["tmp"] / "c.json").read_text())["new_candidates"] == 2


class _FakeFetcher:
    def __init__(self, responses):
        self.responses = responses
        self.urls: list[str] = []

    def get(self, url, headers=None):
        self.urls.append(url)
        for key, resp in self.responses.items():
            if key in url:
                return resp
        return 404, b""


def test_blocked_source_does_not_stop_run():
    cat = dc.Catalogue([], [])
    fetcher = _FakeFetcher(
        {
            "pib.gov.in": (403, b""),
            "gov.uk": (200, (FIXTURES / "gov-uk.xml").read_bytes()),
            "canada.ca": (-1, b""),
        }
    )
    res = dc.run(
        ["pib-en", "gov-uk", "canada-news", "myscheme"],
        cat,
        today=date(2026, 9, 25),
        since_days=3,
        max_items=50,
        max_new=20,
        fetcher=fetcher,
    )
    by = {r.id: r for r in res}
    assert by["pib-en"].status == "blocked" and "403" in by["pib-en"].detail
    assert by["canada-news"].status == "blocked" and "robots" in by["canada-news"].detail
    assert by["gov-uk"].status == "ok" and len(by["gov-uk"].new) == 1
    # myScheme API is opt-in: skipped without a key, never called.
    assert by["myscheme"].status == "skipped"
    assert not any("myscheme" in u for u in fetcher.urls)
    md = dc.digest_markdown(dc.summary_dict(res, dry_run=True, today=date(2026, 9, 25), written=False))
    assert "blocked" in md and "gov-uk" in md


def test_polite_fetcher_rate_limits_per_host(monkeypatch):
    clock = {"t": 100.0}
    sleeps: list[float] = []
    monkeypatch.setattr(dc.time, "monotonic", lambda: clock["t"])
    monkeypatch.setattr(dc.time, "sleep", lambda s: sleeps.append(s))
    f = dc.PoliteFetcher(delay_sec=2.0)
    f._wait("example.gov")
    clock["t"] += 0.5
    f._wait("example.gov")
    f._wait("other.gov")
    assert sleeps == [pytest.approx(1.5)]
    assert dc.TIMEOUT_SEC <= 20 and dc.MAX_BYTES <= 10 * 1024 * 1024
    assert "scheme-finder" in dc.USER_AGENT


def test_url_and_name_normalisation():
    assert dc.norm_url("https://WWW.pib.gov.in/PressReleasePage.aspx?PRID=1&utm_source=x") == dc.norm_url(
        "http://pib.gov.in/pressreleasepage.aspx?PRID=1"
    )
    assert dc.norm_url("https://example.gov/path/") == dc.norm_url("https://example.gov/path/index.html")
    assert dc.name_key("Pradhan Mantri Awas Yojana") == dc.name_key("PM Awas Yojana")
    assert dc.acronyms("Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)") == {"pmkisan"}


def test_existing_queue_schema_accepts_needs_review():
    raw = json.loads((ROOT / "data" / "catalogue_candidates.json").read_text(encoding="utf-8"))
    for c in raw["candidates"]:
        if c.get("auto_drafted"):
            assert c["status"] in {"needs_review", "queued", "researching", "verified_add", "rejected", "deferred"}
            assert c["verified"] is False or c["status"] != "needs_review"


def test_cli_offline_subprocess(tmp_path):
    """The documented command line runs end-to-end offline."""
    import subprocess

    cands = tmp_path / "c.json"
    shutil.copy(ROOT / "data" / "catalogue_candidates.json", cands)
    out = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--dry-run",
            "--digest",
            "--offline-dir",
            str(FIXTURES),
            "--candidates",
            str(cands),
            "--frontend-candidates",
            str(tmp_path / "nofe" / "c.json"),
            "--today",
            "2026-09-25",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    assert "Candidate auto-draft — 2026-09-25" in out.stdout
    assert "New `needs_review` candidates: **6**" in out.stdout
