"""United Kingdom catalogue (2026-09-25): nations, GBP soft gate, all-income coverage."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.db import reset_store
from app.explanations import _fmt_income, _implies_low_gate_label
from app.income_bands import classify_india_annual_income
from app.matcher import (
    IMPLIES_LOW_INCOME_ANNUAL_GATE_GBP,
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
NATIONS = {"England", "Scotland", "Wales", "Northern Ireland"}
OFFICIAL_HOSTS = (
    "www.gov.uk",
    "www.mygov.scot",
    "www.gov.scot",
    "www.transport.gov.scot",
    "www.gov.wales",
    "www.nidirect.gov.uk",
    "www.healthystart.nhs.uk",  # NHS BSA service linked from gov.uk/healthy-start
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
def uk_rows(schemes):
    return [s for s in schemes if "United Kingdom" in (s["eligibility_rules"].get("countries") or [])]


def _uk(**kw) -> MatchProfile:
    base = dict(
        country="United Kingdom",
        age=35,
        gender="female",
        state="England",
        marital_status="married",
        annual_income=30_000,
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


def test_uk_rows_present_and_well_formed(uk_rows):
    assert 30 <= len(uk_rows) <= 80
    for s in uk_rows:
        er = s["eligibility_rules"]
        assert s["id"].startswith("gb-"), s["id"]  # uk-* is India/Uttarakhand
        assert er["countries"] == ["United Kingdom"]
        assert "united_kingdom" in s["tags"]
        assert not ({"central", "nationwide", "federal"} & set(s["tags"])), s["id"]
        assert s["last_verified"] >= "2026-09-25"
        for url in (s["official_source_url"], s["apply_url"]):
            host = url.split("/")[2]
            assert host in OFFICIAL_HOSTS, (s["id"], url)
        if er["states"]:
            assert set(er["states"]) <= NATIONS, s["id"]
            assert er["nationwide"] is False
            for nation in er["states"]:
                assert nation.lower().replace(" ", "_") in s["tags"]
        else:
            assert er["nationwide"] is True
        # Non-means-tested rows must not carry implies_low_income
        if {"universal", "high-income-eligible"} & set(s["tags"]):
            assert er["implies_low_income"] is False, s["id"]
            assert er["max_annual_income"] is None, s["id"]


def test_uk_ids_do_not_collide_with_uttarakhand(schemes):
    ids = [s["id"] for s in schemes]
    assert len(ids) == len(set(ids))
    uttarakhand = [s for s in schemes if s["id"].startswith("uk-")]
    assert uttarakhand, "Uttarakhand uk-* rows expected"
    for s in uttarakhand:
        assert "United Kingdom" not in (s["eligibility_rules"].get("countries") or [])


def test_catalogue_meta_count_matches(schemes):
    meta = json.loads((DATA / "catalogue_meta.json").read_text(encoding="utf-8"))
    assert meta["scheme_count"] == len(schemes)
    assert "United Kingdom" in meta["scope"]
    assert (DATA / "catalogue_meta.json").read_bytes() == (FE_DATA / "catalogue_meta.json").read_bytes()


def test_uk_packs_generated(uk_rows):
    index = json.loads((PACKS / "index.json").read_text(encoding="utf-8"))
    uk_packs = {p["pack_id"]: p for p in index["packs"] if p["country"] == "United Kingdom"}
    assert set(uk_packs) == {"uk-wide", "uk-england", "uk-scotland", "uk-wales", "uk-northern-ireland"}
    assert uk_packs["uk-wide"]["kind"] == "country_national"
    by_id = {s["id"]: s for s in uk_rows}
    for pid, p in uk_packs.items():
        manifest = json.loads((PACKS / p["file"]).read_text(encoding="utf-8"))
        assert manifest["scheme_count"] == len(manifest["scheme_ids"]) > 0
        assert (FE_DATA / "packs" / p["file"]).read_bytes() == (PACKS / p["file"]).read_bytes()
        for sid in manifest["scheme_ids"]:
            assert sid in by_id, sid
    wide = set(json.loads((PACKS / "uk-wide@1.0.0.json").read_text())["scheme_ids"])
    scot = set(json.loads((PACKS / "uk-scotland@1.0.0.json").read_text())["scheme_ids"])
    assert "gb-universal-credit" in wide and "gb-child-benefit" in wide
    assert "gb-sct-scottish-child-payment" in scot
    assert "gb-personal-independence-payment" not in scot
    # UK rows never leak into India/US packs
    central = set(json.loads((PACKS / "india-central@1.0.0.json").read_text())["scheme_ids"])
    assert not any(sid.startswith("gb-") for sid in central)


# ------------------------------------------------------------ income handling


def test_uk_gets_gbp_gate_not_india_bands_or_us_gate():
    assert implies_low_income_annual_gate("United Kingdom") == IMPLIES_LOW_INCOME_ANNUAL_GATE_GBP == 60_000
    assert _implies_low_gate_label("United Kingdom") == "£60,000"
    assert _implies_low_gate_label("United States") == "$60,000"
    assert _fmt_income(45_000, "United Kingdom") == "£45,000"
    assert _fmt_income(45_000, "India").startswith("Rs.")
    # India PRICE bands are India-only
    band = classify_india_annual_income(1_500_000, country="United Kingdom")
    assert band["band_id"] is None and band["band_label"] is None and band["income_class"] is None


def test_uk_profile_response_has_no_india_band(schemes):
    resp = match_schemes(schemes, _uk(annual_income=1_500_000), OPTS)
    assert resp.country == "United Kingdom"
    assert resp.income_band is None
    assert resp.income_band_label is None


def test_uk_soft_gate_excludes_high_income_from_means_tested(schemes):
    by_id = _by_id(schemes)
    uc = by_id["gb-universal-credit"]
    low = evaluate_scheme(uc, _uk(annual_income=18_000))
    assert not low.hard_fail
    assert "implies_low_income" in low.matched
    high = evaluate_scheme(uc, _uk(annual_income=60_000))
    assert high.hard_fail
    assert "implies_low_income" in high.unmatched
    # USD gate is NOT reused: £59,000 is under the UK gate (would also be under $60k,
    # so check the label/explanation path uses £)
    mid = evaluate_scheme(uc, _uk(annual_income=59_000))
    assert not mid.hard_fail


def test_uk_official_household_caps_enforced(schemes):
    by_id = _by_id(schemes)
    so = by_id["gb-eng-shared-ownership"]
    assert so["eligibility_rules"]["max_annual_income"] == 90_000
    assert not evaluate_scheme(so, _uk(annual_income=75_000)).hard_fail
    assert evaluate_scheme(so, _uk(annual_income=120_000)).hard_fail


# ------------------------------------------------------------- nation filter


def test_scotland_profile_gets_scottish_benefits_not_dwp_replacements(schemes):
    resp = match_schemes(
        schemes,
        _uk(state="Scotland", age=40, annual_income=15_000, disability=True, disability_percent=50),
        OPTS,
    )
    ids = _ids(resp)
    assert "gb-sct-scottish-child-payment" in ids
    assert "gb-sct-adult-disability-payment" in ids
    assert "gb-universal-credit" in ids  # UK-wide
    assert "gb-personal-independence-payment" not in ids  # E/W/NI only
    assert "gb-winter-fuel-payment" not in ids
    assert "gb-eng-free-childcare-working-parents" not in ids
    assert not any(i.startswith(("us-", "kerala-", "uk-")) for i in ids)


def test_england_profile_does_not_get_scottish_or_welsh_rows(schemes):
    resp = match_schemes(schemes, _uk(state="England", annual_income=20_000), OPTS)
    ids = _ids(resp)
    assert "gb-eng-free-childcare-working-parents" in ids
    assert "gb-universal-credit" in ids
    assert not any(i.startswith(("gb-sct-", "gb-wls-", "gb-ni-")) for i in ids)


def test_wales_and_ni_nation_filtering(schemes):
    wales = _ids(match_schemes(schemes, _uk(state="Wales", annual_income=20_000), OPTS))
    assert "gb-wls-childcare-offer" in wales
    assert "gb-wls-free-prescriptions" in wales
    assert "gb-eng-shared-ownership" not in wales
    ni = _ids(match_schemes(schemes, _uk(state="Northern Ireland", age=72, annual_income=20_000), OPTS))
    assert "gb-ni-lone-pensioner-allowance" in ni
    assert "gb-winter-fuel-payment" in ni
    assert "gb-warm-home-discount" not in ni  # not available in NI
    assert "gb-council-tax-reduction" not in ni  # NI uses rates


def test_uk_rows_not_shown_to_india_or_us_profiles(schemes):
    india = MatchProfile(country="India", state="Kerala", age=35, annual_income=300_000, occupations=["other"])
    us = MatchProfile(country="United States", state="California", age=35, annual_income=30_000, occupations=["other"])
    for p in (india, us):
        ids = _ids(match_schemes(schemes, p, OPTS))
        assert not any(i.startswith("gb-") for i in ids)


# --------------------------------------------------------- all-income coverage


def test_wealthy_uk_profile_still_sees_non_means_tested_schemes(schemes):
    """£250k profile: excluded from means-tested rows, still sees universal/tax/savings rows."""
    by_id = _by_id(schemes)
    rich = _uk(state="England", age=30, annual_income=250_000)
    for sid in (
        "gb-lifetime-isa",
        "gb-isa-allowance",
        "gb-junior-isa",
        "gb-child-benefit",
        "gb-tax-free-childcare",
        "gb-pension-tax-relief",
        "gb-sdlt-first-time-buyer-relief",
        "gb-boiler-upgrade-scheme",
    ):
        r = evaluate_scheme(by_id[sid], rich)
        assert not r.hard_fail, (sid, r.unmatched)
    for sid in ("gb-universal-credit", "gb-help-to-save", "gb-eng-shared-ownership", "gb-eng-first-homes"):
        assert evaluate_scheme(by_id[sid], rich).hard_fail, sid
    ids = _ids(match_schemes(schemes, rich, OPTS))
    assert {"gb-lifetime-isa", "gb-child-benefit", "gb-tax-free-childcare"} <= ids
    assert "gb-universal-credit" not in ids


def test_lifetime_isa_age_limit_respected(schemes):
    lisa = _by_id(schemes)["gb-lifetime-isa"]
    assert not evaluate_scheme(lisa, _uk(age=39, annual_income=250_000)).hard_fail
    assert evaluate_scheme(lisa, _uk(age=45, annual_income=250_000)).hard_fail


def test_uk_pensioner_sees_state_pension_and_pension_credit_when_low_income(schemes):
    ids = _ids(match_schemes(schemes, _uk(state="England", age=70, annual_income=9_000), OPTS))
    assert {"gb-new-state-pension", "gb-pension-credit", "gb-winter-fuel-payment"} <= ids
    rich = _ids(match_schemes(schemes, _uk(state="England", age=70, annual_income=90_000), OPTS))
    assert "gb-new-state-pension" in rich
    assert "gb-pension-credit" not in rich


def test_uk_explanation_uses_pounds(schemes):
    resp = match_schemes(schemes, _uk(state="England", annual_income=18_000), OPTS)
    uc = next(m for m in resp.matched if m.scheme_id == "gb-universal-credit")
    text = json.dumps(uc.model_dump(), ensure_ascii=False)
    assert "£60,000" in text
    assert "Rs.5,00,000" not in text and "$60,000" not in text
