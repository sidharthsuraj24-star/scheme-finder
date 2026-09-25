"""Canada catalogue (2026-09-25): provinces/territories, CAD soft gate, all-income coverage."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.db import reset_store
from app.explanations import _currency_prefix, _fmt_income, _implies_low_gate_label
from app.income_bands import classify_india_annual_income
from app.matcher import (
    IMPLIES_LOW_INCOME_ANNUAL_GATE_CAD,
    IMPLIES_LOW_INCOME_ANNUAL_GATE_USD,
    evaluate_scheme,
    implies_low_income_annual_gate,
    match_schemes,
)
from app.models import MatchOptions, MatchProfile
from app.schemes_loader import load_schemes

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
FE_DATA = ROOT / "frontend" / "data"
PACKS = DATA / "packs"
PROVINCES = {
    "Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador",
    "Northwest Territories", "Nova Scotia", "Nunavut", "Ontario", "Prince Edward Island",
    "Quebec", "Saskatchewan", "Yukon",
}
PROV_CODE = {
    "Alberta": "ab", "British Columbia": "bc", "Manitoba": "mb", "New Brunswick": "nb",
    "Newfoundland and Labrador": "nl", "Northwest Territories": "nt", "Nova Scotia": "ns",
    "Nunavut": "nu", "Ontario": "on", "Prince Edward Island": "pe", "Quebec": "qc",
    "Saskatchewan": "sk", "Yukon": "yt",
}
OFFICIAL_HOSTS = (
    "www.canada.ca",
    "www.alberta.ca",
    "www2.gov.bc.ca",
    "www.gov.mb.ca",
    "www2.gnb.ca",
    "novascotia.ca",
    "www.ece.gov.nt.ca",
    "www.ontario.ca",
    "www.quebec.ca",
    "www.retraitequebec.gouv.qc.ca",
    "www.revenuquebec.ca",
    "www.saskatchewan.ca",
    "yukon.ca",
)
OPTS = MatchOptions(max_results=100)


@pytest.fixture(scope="module")
def schemes():
    return load_schemes()


@pytest.fixture(autouse=True)
def _store(schemes):
    reset_store(schemes)
    yield
    reset_store(schemes)


@pytest.fixture(scope="module")
def ca_rows(schemes):
    return [s for s in schemes if "Canada" in (s["eligibility_rules"].get("countries") or [])]


def _ca(**kw) -> MatchProfile:
    base = dict(
        country="Canada",
        age=35,
        gender="female",
        state="Ontario",
        marital_status="married",
        annual_income=45_000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
    )
    base.update(kw)
    return MatchProfile(**base)


def _ids(resp) -> set[str]:
    return {m.scheme_id for m in resp.matched}


def _by_id(schemes) -> dict:
    return {s["id"]: s for s in schemes}


# --------------------------------------------------------------- data shape


def test_canada_rows_present_and_well_formed(ca_rows):
    assert 50 <= len(ca_rows) <= 80
    for s in ca_rows:
        er = s["eligibility_rules"]
        assert s["id"].startswith("can-"), s["id"]  # ca-* is California
        assert er["countries"] == ["Canada"]
        assert "canada" in s["tags"]
        assert not ({"central", "nationwide", "federal", "united_states"} & set(s["tags"])), s["id"]
        assert s["last_verified"] >= "2026-09-25"
        assert er["verify"] is True
        for url in (s["official_source_url"], s["apply_url"]):
            host = url.split("/")[2]
            assert host in OFFICIAL_HOSTS, (s["id"], url)
        federal = "canada_federal" in s["tags"]
        if er["states"]:
            assert set(er["states"]) <= PROVINCES, s["id"]
            assert er["nationwide"] is False
            if not federal:
                assert len(er["states"]) == 1, s["id"]
                prov = er["states"][0]
                assert s["id"].startswith(f"can-{PROV_CODE[prov]}-"), s["id"]
                assert prov.lower().replace(" ", "_") in s["tags"]
        else:
            assert federal and er["nationwide"] is True, s["id"]
        # Non-means-tested rows must not carry implies_low_income or an income cap
        if {"universal", "high-income-eligible"} & set(s["tags"]):
            assert er["implies_low_income"] is False, s["id"]
            assert er["max_annual_income"] is None, s["id"]
        # Canada amounts are C$ — never bare "$"
        assert "C$" in s["benefits"]["en"] or "$" not in s["benefits"]["en"], s["id"]


def test_canada_ids_do_not_collide_with_california(schemes, ca_rows):
    ids = [s["id"] for s in schemes]
    assert len(ids) == len(set(ids))
    california = [s for s in schemes if s["id"].startswith("ca-")]
    assert california, "California ca-* rows expected"
    for s in california:
        assert "Canada" not in (s["eligibility_rules"].get("countries") or [])
    assert all(not s["id"].startswith("ca-") for s in ca_rows)


def test_every_province_and_territory_has_at_least_one_row(ca_rows):
    provincial = [s for s in ca_rows if "canada_federal" not in s["tags"]]
    covered = {st for s in provincial for st in s["eligibility_rules"]["states"]}
    assert covered == PROVINCES
    for prov in PROVINCES:
        n = sum(1 for s in provincial if s["eligibility_rules"]["states"] == [prov])
        assert 1 <= n <= 4, (prov, n)


def test_federal_core_programs_present(ca_rows):
    ids = {s["id"] for s in ca_rows}
    for sid in (
        "can-canada-child-benefit", "can-groceries-essentials-benefit", "can-canada-workers-benefit",
        "can-old-age-security", "can-guaranteed-income-supplement", "can-cpp-retirement",
        "can-ei-regular", "can-ei-maternity-parental", "can-canada-disability-benefit",
        "can-disability-tax-credit", "can-rdsp", "can-resp-cesg", "can-canada-learning-bond",
        "can-tfsa", "can-rrsp", "can-fhsa", "can-home-buyers-plan", "can-canada-dental-care-plan",
        "can-canada-student-grant-full-time", "can-canada-caregiver-credit",
    ):
        assert sid in ids, sid
    # Closed / renamed programmes are not listed
    blob = json.dumps([s["scheme_name"]["en"] for s in ca_rows])
    assert "Carbon Rebate" not in blob
    assert not any("gst-hst-credit" in s["id"] for s in ca_rows)


def test_catalogue_meta_count_and_scope(schemes):
    meta = json.loads((DATA / "catalogue_meta.json").read_text(encoding="utf-8"))
    assert meta["scheme_count"] == len(schemes)
    assert "Canada" in meta["scope"]
    assert (DATA / "catalogue_meta.json").read_bytes() == (FE_DATA / "catalogue_meta.json").read_bytes()
    assert (DATA / "schemes.json").read_bytes() == (FE_DATA / "schemes.json").read_bytes()


def test_canada_packs_generated(ca_rows):
    index = json.loads((PACKS / "index.json").read_text(encoding="utf-8"))
    packs = {p["pack_id"]: p for p in index["packs"] if p["country"] == "Canada"}
    assert len(packs) == 14
    assert "canada-federal" in packs and packs["canada-federal"]["kind"] == "country_federal"
    for prov in PROVINCES:
        assert "canada-" + prov.lower().replace(" ", "-") in packs, prov
    by_id = {s["id"]: s for s in ca_rows}
    seen: set[str] = set()
    for p in packs.values():
        manifest = json.loads((PACKS / p["file"]).read_text(encoding="utf-8"))
        assert manifest["scheme_count"] == len(manifest["scheme_ids"]) > 0
        assert (FE_DATA / "packs" / p["file"]).read_bytes() == (PACKS / p["file"]).read_bytes()
        for sid in manifest["scheme_ids"]:
            assert sid in by_id, sid
        seen |= set(manifest["scheme_ids"])
    assert seen == set(by_id)
    fed = set(json.loads((PACKS / "canada-federal@1.0.0.json").read_text())["scheme_ids"])
    qc = set(json.loads((PACKS / "canada-quebec@1.0.0.json").read_text())["scheme_ids"])
    assert {"can-canada-child-benefit", "can-cpp-retirement", "can-ei-maternity-parental"} <= fed
    assert {"can-qc-qpip", "can-qc-family-allowance"} <= qc
    # Canada rows never leak into India / US packs
    for other in ("india-central@1.0.0.json", "us-federal@1.0.0.json", "us-california@1.0.0.json"):
        ids = set(json.loads((PACKS / other).read_text())["scheme_ids"])
        assert not any(sid.startswith("can-") for sid in ids), other


# ------------------------------------------------------------ income handling


def test_canada_gets_cad_gate_not_us_gate_or_india_bands():
    assert implies_low_income_annual_gate("Canada") == IMPLIES_LOW_INCOME_ANNUAL_GATE_CAD == 58_523
    assert IMPLIES_LOW_INCOME_ANNUAL_GATE_CAD != IMPLIES_LOW_INCOME_ANNUAL_GATE_USD
    assert implies_low_income_annual_gate("ca") is None  # never alias California's prefix
    assert _implies_low_gate_label("Canada") == "C$58,523"
    assert _currency_prefix("Canada") == "C$"
    assert _fmt_income(45_000, "Canada") == "C$45,000"
    assert _fmt_income(45_000, "United States") == "$45,000"
    band = classify_india_annual_income(1_500_000, country="Canada")
    assert band["band_id"] is None and band["band_label"] is None and band["income_class"] is None


def test_canada_profile_response_has_no_india_band(schemes):
    resp = match_schemes(schemes, _ca(annual_income=1_500_000), OPTS)
    assert resp.country == "Canada"
    assert resp.income_band is None
    assert resp.income_band_label is None


def test_canada_soft_gate_boundary(schemes):
    cdb = _by_id(schemes)["can-canada-disability-benefit"]
    assert cdb["eligibility_rules"]["implies_low_income"] is True
    assert cdb["eligibility_rules"]["max_annual_income"] is None
    kw = dict(disability=True, disability_percent=60)
    low = evaluate_scheme(cdb, _ca(annual_income=20_000, **kw))
    assert not low.hard_fail and "implies_low_income" in low.matched
    # C$59,000 is under the US $60k gate but over the Canada gate — proves the USD gate is not reused
    mid = evaluate_scheme(cdb, _ca(annual_income=59_000, **kw))
    assert mid.hard_fail and "implies_low_income" in mid.unmatched
    assert not evaluate_scheme(cdb, _ca(annual_income=58_000, **kw)).hard_fail


def test_canada_official_caps_enforced(schemes):
    by_id = _by_id(schemes)
    cdcp = by_id["can-canada-dental-care-plan"]
    assert not evaluate_scheme(cdcp, _ca(annual_income=85_000)).hard_fail
    assert evaluate_scheme(cdcp, _ca(annual_income=95_000)).hard_fail
    gis = by_id["can-guaranteed-income-supplement"]
    assert not evaluate_scheme(gis, _ca(age=70, annual_income=18_000)).hard_fail
    assert evaluate_scheme(gis, _ca(age=70, annual_income=80_000)).hard_fail
    assert evaluate_scheme(gis, _ca(age=50, annual_income=18_000)).hard_fail  # under 65


# ---------------------------------------------------------- province filter


def test_ontario_profile_gets_ontario_rows_not_other_provinces(schemes):
    ids = _ids(match_schemes(schemes, _ca(state="Ontario", annual_income=30_000), OPTS))
    assert {"can-on-trillium-benefit", "can-on-child-benefit", "can-canada-child-benefit"} <= ids
    provincial = {i for i in ids if i.startswith("can-") and i[4:7].rstrip("-") in PROV_CODE.values() and i[6] == "-"}
    assert all(i.startswith("can-on-") for i in provincial), provincial
    assert "can-cpp-retirement" not in ids  # age 35
    assert not any(i.startswith(("us-", "gb-", "kerala-", "ca-")) for i in ids)


def test_quebec_excluded_from_cpp_and_ei_parental_but_gets_qpip(schemes):
    qc = _ids(match_schemes(schemes, _ca(state="Quebec", age=30, annual_income=60_000), OPTS))
    assert "can-qc-qpip" in qc and "can-qc-family-allowance" in qc
    assert "can-ei-maternity-parental" not in qc
    assert "can-ei-regular" in qc  # EI regular applies in Quebec
    assert "can-canada-student-grant-full-time" not in qc
    on = _ids(match_schemes(schemes, _ca(state="Ontario", age=30, annual_income=60_000), OPTS))
    assert "can-ei-maternity-parental" in on and "can-qc-qpip" not in on
    old_qc = _ids(match_schemes(schemes, _ca(state="Quebec", age=67, annual_income=40_000), OPTS))
    assert "can-qc-qpp-retirement" in old_qc and "can-cpp-retirement" not in old_qc
    assert "can-old-age-security" in old_qc


def test_bc_and_territory_filtering(schemes):
    bc = _ids(match_schemes(schemes, _ca(state="British Columbia", annual_income=40_000), OPTS))
    assert "can-bc-family-benefit" in bc and "can-bc-renters-tax-credit" in bc
    assert "can-ab-child-family-benefit" not in bc
    nu = _ids(match_schemes(schemes, _ca(state="Nunavut", annual_income=20_000), OPTS))
    assert "can-nu-child-benefit" in nu
    assert "can-canada-student-grant-full-time" not in nu  # not offered in NU
    assert not any(i.startswith(("can-on-", "can-bc-", "can-qc-")) for i in nu)


def test_canada_rows_not_shown_to_india_us_or_uk_profiles(schemes):
    profiles = (
        MatchProfile(country="India", state="Kerala", age=35, annual_income=300_000, occupations=["other"]),
        MatchProfile(country="United States", state="California", age=35, annual_income=30_000, occupations=["other"]),
        MatchProfile(country="United Kingdom", state="England", age=35, annual_income=30_000, occupations=["other"]),
    )
    for p in profiles:
        ids = _ids(match_schemes(schemes, p, OPTS))
        assert not any(i.startswith("can-") for i in ids), p.country


# --------------------------------------------------------- all-income coverage


def test_wealthy_canada_profile_still_sees_registered_plans_and_universal(schemes):
    """C$250k profile: excluded from means-tested rows, still sees TFSA/RRSP/FHSA etc."""
    by_id = _by_id(schemes)
    rich = _ca(state="Alberta", age=32, annual_income=250_000)
    for sid in (
        "can-tfsa", "can-rrsp", "can-fhsa", "can-home-buyers-plan", "can-canada-child-benefit",
        "can-resp-cesg", "can-ei-maternity-parental", "can-home-buyers-amount",
    ):
        r = evaluate_scheme(by_id[sid], rich)
        assert not r.hard_fail, (sid, r.unmatched)
    for sid in (
        "can-groceries-essentials-benefit", "can-canada-dental-care-plan", "can-canada-workers-benefit",
        "can-canada-learning-bond", "can-ab-aish",
    ):
        assert evaluate_scheme(by_id[sid], rich).hard_fail, sid
    ids = _ids(match_schemes(schemes, rich, OPTS))
    assert {"can-tfsa", "can-rrsp", "can-fhsa"} <= ids
    assert "can-groceries-essentials-benefit" not in ids
    old_rich = _ids(match_schemes(schemes, _ca(state="Ontario", age=70, annual_income=120_000), OPTS))
    assert "can-old-age-security" in old_rich  # clawback is a tax note, not a cap
    assert "can-guaranteed-income-supplement" not in old_rich
    assert "can-rrsp" in old_rich  # 70 <= 71


def test_low_income_family_sees_federal_and_provincial_support(schemes):
    ids = _ids(match_schemes(schemes, _ca(state="Nova Scotia", age=30, annual_income=25_000), OPTS))
    assert {
        "can-canada-child-benefit", "can-groceries-essentials-benefit", "can-canada-workers-benefit",
        "can-canada-dental-care-plan", "can-ns-child-benefit", "can-ns-affordable-living-tax-credit",
    } <= ids


def test_canada_explanation_uses_cad(schemes):
    resp = match_schemes(schemes, _ca(state="Ontario", annual_income=20_000, disability=True, disability_percent=60), OPTS)
    hit = next(m for m in resp.matched if m.scheme_id == "can-canada-disability-benefit")
    text = hit.explanation.en
    assert "C$58,523" in text and "C$20,000" in text
    assert "$60,000" not in text and "Rs." not in text
    assert "available in Canada" in text
