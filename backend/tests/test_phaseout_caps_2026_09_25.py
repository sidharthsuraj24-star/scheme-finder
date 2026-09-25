"""Official phase-out zero-points (2026-09-25).

A C$250k Ontario family must not see the Ontario Child Benefit; a C$45k one-child family
still does; the CCB still reaches middle and upper-middle incomes per CRA's formula.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from app.db import reset_store
from app.matcher import evaluate_scheme, match_schemes
from app.models import MatchOptions, MatchProfile
from app.schemes_loader import load_schemes

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from phaseout_caps_2026_09_25_rows import CAPS, LEFT_UNGATED  # noqa: E402

OPTS = MatchOptions(max_results=100)


@pytest.fixture(scope="module")
def schemes():
    return load_schemes()


@pytest.fixture(autouse=True)
def _store(schemes):
    reset_store(schemes)
    yield
    reset_store(schemes)


def _by_id(schemes):
    return {s["id"]: s for s in schemes}


def _ca(**kw) -> MatchProfile:
    base = dict(country="Canada", age=38, gender="female", state="Ontario", marital_status="married",
                annual_income=45_000, occupations=["other"], categories=[], disability=False,
                disability_percent=0)
    base.update(kw)
    return MatchProfile(**base)


def _ids(resp):
    return {m.scheme_id for m in resp.matched}


# ------------------------------------------------------------------ data


def test_caps_encoded_with_basis_and_verify(schemes):
    by_id = _by_id(schemes)
    for sid, spec in CAPS.items():
        er = by_id[sid]["eligibility_rules"]
        assert er["max_annual_income"] == spec["cap"], sid
        assert er["verify"] is True, sid
        assert spec["basis"] in er["notes"], sid
        assert er["notes"].count(spec["basis"]) == 1, sid  # idempotent
        assert er["verify_notes"] == spec["verify_notes"], sid


def test_reviewed_rows_without_official_zero_point_stay_ungated(schemes):
    by_id = _by_id(schemes)
    for sid in LEFT_UNGATED:
        assert by_id[sid]["eligibility_rules"]["max_annual_income"] is None, sid


def test_official_formula_values():
    # CCB: 4 children under 6 (CRA July 2026 – June 2027)
    assert CAPS["can-canada-child-benefit"]["cap"] == round(82_847 + (4 * 8_157 - 10_260) / 0.095 + 0.5)
    # OCB: 4 × C$1,759.92 at 8% over C$26,865
    assert CAPS["can-on-child-benefit"]["cap"] == 26_865 + round(4 * 1_759.92 / 0.08)
    # BCFB: minimums for 4 children at 4% over C$96,562
    assert CAPS["can-bc-family-benefit"]["cap"] == 96_562 + (775 + 750 + 725 + 725) * 25
    # OTB: senior-couple OEPTC (C$1,488 at 2% over C$43,571)
    assert CAPS["can-on-trillium-benefit"]["cap"] == 43_571 + 1_488 * 50


def test_trees_identical():
    a = (ROOT / "data" / "schemes.json").read_bytes()
    b = (ROOT / "frontend" / "data" / "schemes.json").read_bytes()
    assert a == b


# --------------------------------------------------------------- matching


def test_250k_ontario_family_does_not_get_ocb(schemes):
    ocb = _by_id(schemes)["can-on-child-benefit"]
    r = evaluate_scheme(ocb, _ca(annual_income=250_000))
    assert r.hard_fail and "max_annual_income" in r.unmatched
    ids = _ids(match_schemes(schemes, _ca(annual_income=250_000), OPTS))
    assert "can-on-child-benefit" not in ids
    assert "can-on-trillium-benefit" not in ids


def test_45k_one_child_family_still_gets_ocb(schemes):
    # 1-child zero-point is about C$48,864 — well above C$45k
    ocb = _by_id(schemes)["can-on-child-benefit"]
    assert not evaluate_scheme(ocb, _ca(annual_income=45_000)).hard_fail
    assert "can-on-child-benefit" in _ids(match_schemes(schemes, _ca(annual_income=45_000), OPTS))


@pytest.mark.parametrize("income", [60_000, 95_000, 150_000, 250_000, 318_000])
def test_ccb_still_reaches_middle_and_upper_middle_incomes(schemes, income):
    ccb = _by_id(schemes)["can-canada-child-benefit"]
    assert not evaluate_scheme(ccb, _ca(annual_income=income)).hard_fail, income


def test_ccb_capped_above_official_zero_point(schemes):
    ccb = _by_id(schemes)["can-canada-child-benefit"]
    assert evaluate_scheme(ccb, _ca(annual_income=330_000)).hard_fail


def test_provincial_child_benefits_respect_zero_points(schemes):
    by_id = _by_id(schemes)
    bc = by_id["can-bc-family-benefit"]
    assert not evaluate_scheme(bc, _ca(state="British Columbia", annual_income=150_000)).hard_fail
    assert evaluate_scheme(bc, _ca(state="British Columbia", annual_income=250_000)).hard_fail
    ab = by_id["can-ab-child-family-benefit"]
    assert not evaluate_scheme(ab, _ca(state="Alberta", annual_income=65_000)).hard_fail
    assert evaluate_scheme(ab, _ca(state="Alberta", annual_income=75_000)).hard_fail
    nb = by_id["can-nb-hst-credit"]  # official C$85k replaces the C$58,523 soft gate
    assert not evaluate_scheme(nb, _ca(state="New Brunswick", annual_income=70_000)).hard_fail
    assert evaluate_scheme(nb, _ca(state="New Brunswick", annual_income=90_000)).hard_fail


def test_quebec_family_allowance_stays_open_at_high_income(schemes):
    fa = _by_id(schemes)["can-qc-family-allowance"]  # minimum amount paid at all incomes
    assert not evaluate_scheme(fa, _ca(state="Quebec", annual_income=250_000)).hard_fail


def test_uk_childcare_household_cap(schemes):
    tfc = _by_id(schemes)["gb-tax-free-childcare"]
    uk = dict(country="United Kingdom", state="England", age=35, gender="female", marital_status="married",
              occupations=["other"], categories=[], disability=False, disability_percent=0)
    assert not evaluate_scheme(tfc, MatchProfile(annual_income=150_000, **uk)).hard_fail
    assert evaluate_scheme(tfc, MatchProfile(annual_income=250_000, **uk)).hard_fail
    cb = _by_id(schemes)["gb-child-benefit"]  # universal with HICBC — never capped
    assert not evaluate_scheme(cb, MatchProfile(annual_income=250_000, **uk)).hard_fail
