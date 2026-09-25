"""Explanation wording: readable country rule, India-only BPL/destitute, right currency."""

from __future__ import annotations

import pytest

from app.db import reset_store
from app.explanations import _country_display, template_explanation
from app.matcher import match_schemes
from app.models import MatchOptions, MatchProfile
from app.schemes_loader import load_schemes

OPTS = MatchOptions(max_results=100, include_verify_uncertain=True)


@pytest.fixture(scope="module")
def schemes():
    return load_schemes()


@pytest.fixture(autouse=True)
def _store(schemes):
    reset_store(schemes)
    yield
    reset_store(schemes)


def _profile(country: str, state: str, income: int, **kw) -> MatchProfile:
    base = dict(
        country=country,
        state=state,
        age=35,
        gender="female",
        annual_income=income,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
    )
    base.update(kw)
    return MatchProfile(**base)


def _low_income_hits(resp):
    return [m for m in resp.matched if "implies_low_income" in m.matched_rules]


def test_country_display_aliases():
    assert _country_display("united_kingdom") == "United Kingdom"
    assert _country_display("UK") == "United Kingdom"
    assert _country_display("usa") == "United States"
    assert _country_display(None) == "India"
    assert _country_display("Nepal") == "Nepal"


@pytest.mark.parametrize(
    "country,state,income,display",
    [
        ("United Kingdom", "England", 18_000, "United Kingdom"),
        ("United States", "California", 20_000, "United States"),
        ("India", "Kerala", 45_000, "India"),
    ],
)
def test_countries_rule_is_readable(schemes, country, state, income, display):
    resp = match_schemes(schemes, _profile(country, state, income), OPTS)
    hits = [m for m in resp.matched if "countries" in m.matched_rules]
    assert hits
    for m in hits:
        assert f"available in {display}" in m.explanation.en
        assert f"{display} ൽ ലഭ്യമാണ്" in m.explanation.ml
        assert " countries;" not in m.explanation.en
        assert "countries [ML]" not in m.explanation.ml


def test_uk_low_income_wording_neutral_and_gbp(schemes):
    resp = match_schemes(schemes, _profile("United Kingdom", "England", 18_000), OPTS)
    hits = _low_income_hits(resp)
    assert any(m.scheme_id == "gb-universal-credit" for m in hits)
    for m in hits:
        assert "BPL" not in m.explanation.en and "destitute" not in m.explanation.en
        assert "BPL" not in m.explanation.ml
        assert "low-income / means-tested" in m.explanation.en
        assert "£18,000" in m.explanation.en and "£60,000" in m.explanation.en
        assert "Rs." not in m.explanation.en and "$" not in m.explanation.en


def test_us_low_income_wording_neutral_and_usd(schemes):
    resp = match_schemes(
        schemes, _profile("United States", "California", 20_000, occupations=["unemployed"]), OPTS
    )
    hits = _low_income_hits(resp)
    assert hits
    for m in hits:
        assert "BPL" not in m.explanation.en and "destitute" not in m.explanation.en
        assert "low-income / means-tested" in m.explanation.en
        assert "$20,000" in m.explanation.en and "£" not in m.explanation.en


def test_india_low_income_keeps_bpl_wording(schemes):
    resp = match_schemes(
        schemes,
        _profile("India", "Kerala", 45_000, age=68, gender="male", categories=["BPL"]),
        OPTS,
    )
    hits = _low_income_hits(resp)
    assert hits
    for m in hits:
        assert "BPL/destitute" in m.explanation.en
        assert "BPL/destitute" in m.explanation.ml
        assert "Rs.45,000" in m.explanation.en
        assert "means-tested" not in m.explanation.en


def test_template_other_country_without_gate_is_neutral():
    scheme = {"id": "np-x", "scheme_name": {"en": "X"}, "eligibility_rules": {}}
    text = template_explanation(
        scheme=scheme,
        profile=_profile("Nepal", "Bagmati", 1000),
        matched_rules=["countries", "implies_low_income"],
        unmatched_rules=[],
        missing_fields=[],
        status="likely_eligible",
    )
    assert "available in Nepal" in text.en
    assert "BPL" not in text.en and "low-income / means-tested" in text.en
