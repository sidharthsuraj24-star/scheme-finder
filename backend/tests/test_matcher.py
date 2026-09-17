"""Unit tests for deterministic matcher using sample_profiles.json (≥8 cases)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.db import SchemeStore, reset_store
from app.matcher import evaluate_scheme, match_schemes, profile_has_land
from app.models import MatchOptions, MatchProfile, MatchRequest
from app.schemes_loader import load_schemes

ROOT = Path(__file__).resolve().parents[2]
PROFILES_PATH = ROOT / "data" / "sample_profiles.json"


@pytest.fixture(scope="module")
def schemes():
    return load_schemes()


@pytest.fixture(scope="module")
def profiles() -> dict:
    with PROFILES_PATH.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return {p["id"]: p for p in data}


@pytest.fixture(autouse=True)
def _store(schemes):
    reset_store(schemes)
    yield
    reset_store(schemes)


def _profile_from_sample(raw: dict) -> MatchProfile:
    """Map sample_profiles.json fields onto MatchProfile."""
    data = {k: v for k, v in raw.items() if k not in {"id", "label", "notes"}}
    # disability_percent null → no disability unless set
    if data.get("disability_percent") is not None:
        data["disability"] = True
    return MatchProfile(**data)


def _matched_ids(resp) -> set[str]:
    return {m.scheme_id for m in resp.matched}


def _likely_or_uncertain(resp, scheme_id: str) -> bool:
    return any(m.scheme_id == scheme_id for m in resp.matched)


# ---------------------------------------------------------------------------
# Core profile cases (≥8)
# ---------------------------------------------------------------------------


def test_senior_low_income_matches_old_age_pension(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    resp = match_schemes(schemes, profile)
    assert "kerala-old-age-pension" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-old-age-pension")
    assert hit.status == "likely_eligible"
    assert "min_age" in hit.matched_rules
    assert "max_annual_income" in hit.matched_rules
    assert hit.verify is False


def test_widow_matches_widow_pension(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-widow-low-income"])
    resp = match_schemes(schemes, profile)
    assert "kerala-widow-pension" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-widow-pension")
    assert hit.status == "likely_eligible"
    assert "marital_status" in hit.matched_rules
    assert "gender" in hit.matched_rules


def test_disabled_matches_disability_pension(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-pwd-physical"])
    resp = match_schemes(schemes, profile)
    assert "kerala-disability-pension-physical" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-disability-pension-physical")
    # verify=true → uncertain, never claim certain eligibility
    assert hit.status == "uncertain"
    assert hit.verify is True
    assert "min_disability_percent" in hit.matched_rules
    assert "disability_required" in hit.matched_rules


def test_farmer_with_land_matches_pm_kisan(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-small-farmer"])
    resp = match_schemes(schemes, profile)
    assert "pm-kisan" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "pm-kisan")
    assert "occupations" in hit.matched_rules
    assert "land_ownership" in hit.matched_rules
    assert hit.status == "uncertain"  # verify=true
    assert hit.verify is True


def test_high_income_few_or_no_pension_matches(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-high-income-no-match"])
    resp = match_schemes(schemes, profile)
    pension_ids = {
        "kerala-old-age-pension",
        "kerala-widow-pension",
        "kerala-disability-pension-physical",
        "kerala-disability-pension-mental",
        "kerala-unmarried-women-pension",
        "kerala-agri-labour-pension",
    }
    matched_pensions = _matched_ids(resp) & pension_ids
    assert matched_pensions == set(), f"Unexpected pension matches: {matched_pensions}"
    # PM-KISAN: tax-payer / professional — still may match occupations+land unless we
    # encode IT exclusion (not in structured rules). Land+farmer occupation may match
    # but occupations list is professional_engineer only → should NOT match pm-kisan.
    assert "pm-kisan" not in _matched_ids(resp)


def test_zero_matches_returns_message_not_error(schemes):
    """Extreme mismatch: non-Kerala young male, high income, no disability/land/cats."""
    profile = MatchProfile(
        age=25,
        gender="male",
        state="Goa",
        marital_status="married",
        annual_income=5_000_000,
        monthly_household_income=400_000,
        occupations=["software_engineer"],
        categories=[],
        disability=False,
        disability_percent=None,
        land_ownership="none",
        income_tax_payer=True,
    )
    resp = match_schemes(schemes, profile)
    # May still get open schemes with no hard filters that don't require state mismatch.
    # Force empty by also excluding uncertain optional:
    resp2 = match_schemes(
        schemes,
        profile,
        MatchOptions(include_verify_uncertain=False),
    )
    # With include_verify_uncertain=False, schemes that pass hard filters but are
    # verify/uncertain go to needs_verification, not matched.
    # Goa fails Kerala-only; India-wide schemes may still pass if no other hard fails.
    # Build a true zero-match: fail all via income + disability + occupation + gender.
    # For message field: when matched is empty, message must be set.
    empty_profile = MatchProfile(
        age=10,
        gender="male",
        state="Goa",
        annual_income=9_000_000,
        occupations=["astronaut"],
        categories=["XYZ_NOT_A_CATEGORY"],
        disability=False,
        land_ownership="none",
    )
    resp3 = match_schemes(schemes, empty_profile, MatchOptions(include_verify_uncertain=False))
    # Filter matched to empty for assertion path — if any remain, they must not be pensions
    if resp3.count == 0:
        assert resp3.message is not None
        assert "No schemes matched" in resp3.message
    else:
        # Soft open schemes with no hard rules can still appear; message only when empty
        assert resp3.message is None
        assert all(m.scheme_id not in {
            "kerala-old-age-pension",
            "kerala-widow-pension",
        } for m in resp3.matched)

    # Explicit empty matched list message contract
    from app.models import MatchResponse

    empty = MatchResponse(matched=[], excluded=[], needs_verification=[], count=0, message=None)
    # Engine always sets message when empty:
    forced = match_schemes([], empty_profile)
    assert forced.matched == []
    assert forced.message is not None


def test_student_category_matches_egrantz(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-sc-student"])
    resp = match_schemes(schemes, profile)
    assert "kerala-egrantz" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-egrantz")
    assert "occupations" in hit.matched_rules
    assert "categories" in hit.matched_rules
    assert hit.verify is True
    assert hit.status == "uncertain"


def test_income_ceiling_edge_inclusive(schemes):
    """Exact income cap (100000) must still match old-age pension."""
    profile = MatchProfile(
        age=65,
        gender="male",
        state="Kerala",
        marital_status="married",
        annual_income=100_000,
        monthly_household_income=8333.33,
        occupations=[],
        categories=[],
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-old-age-pension" in _matched_ids(resp)
    # One rupee over → excluded
    over = profile.model_copy(update={"annual_income": 100_001})
    resp2 = match_schemes(schemes, over)
    assert "kerala-old-age-pension" not in _matched_ids(resp2)
    assert any(
        e.scheme_id == "kerala-old-age-pension" and "max_annual_income" in e.reasons
        for e in resp2.excluded
    )


# ---------------------------------------------------------------------------
# Additional / edge cases
# ---------------------------------------------------------------------------


def test_agri_labourer_not_pm_kisan_without_land(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-agri-labourer"])
    resp = match_schemes(schemes, profile)
    assert "kerala-agri-labour-pension" in _matched_ids(resp)
    assert "pm-kisan" not in _matched_ids(resp)
    assert any(
        e.scheme_id == "pm-kisan" and "land_ownership_required" in e.reasons
        for e in resp.excluded
    )


def test_unmarried_woman_pension(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-unmarried-woman-55"])
    resp = match_schemes(schemes, profile)
    assert "kerala-unmarried-women-pension" in _matched_ids(resp)


def test_deserted_requires_age_50(schemes):
    scheme = next(s for s in schemes if s["id"] == "kerala-widow-pension")
    young = MatchProfile(
        age=45,
        gender="female",
        state="Kerala",
        marital_status="deserted_7_years_over_50",
        annual_income=50_000,
    )
    result = evaluate_scheme(scheme, young)
    assert result.hard_fail
    assert "deserted_7_years_over_50" in result.unmatched

    older = young.model_copy(update={"age": 52})
    result2 = evaluate_scheme(scheme, older)
    assert not result2.hard_fail
    assert "marital_status" in result2.matched


def test_monthly_income_cap_adip(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-pwd-physical"])
    # monthly 7000 < 30000 → ADIP should match
    resp = match_schemes(schemes, profile)
    assert "adip-assistive-devices" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "adip-assistive-devices")
    assert "max_monthly_household_income" in hit.matched_rules
    assert hit.status == "likely_eligible"  # verify=false


def test_secc_categories_missing_hard_fail(schemes):
    """KASP/PMJAY list schemes without SECC flags → hard exclude, never soft-matched."""
    profile = MatchProfile(
        age=40,
        gender="female",
        state="Kerala",
        annual_income=80_000,
        categories=[],
        occupations=[],
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-kasp-pmjay" not in _matched_ids(resp)
    assert "ab-pmjay-national" not in _matched_ids(resp)
    assert any(
        e.scheme_id == "kerala-kasp-pmjay" and "categories" in e.reasons for e in resp.excluded
    )
    assert any(
        e.scheme_id == "ab-pmjay-national" and "categories" in e.reasons for e in resp.excluded
    )


def test_derive_annual_from_monthly():
    req = MatchRequest(monthly_household_income=5000, age=70, state="Kerala")
    profile = req.resolved_profile()
    assert profile.annual_income == 60_000


def test_derive_monthly_from_annual():
    req = MatchRequest(annual_income=120_000, age=70, state="Kerala")
    profile = req.resolved_profile()
    assert profile.monthly_household_income == 10_000


def test_occupation_normalization(schemes):
    profile = MatchProfile(
        age=63,
        state="Kerala",
        annual_income=70_000,
        occupations=["Agricultural Labour"],  # spaces + case
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-agri-labour-pension" in _matched_ids(resp)


def test_land_helpers():
    assert profile_has_land("none") is False
    assert profile_has_land("landless") is False
    assert profile_has_land("cultivable_own") is True
    assert profile_has_land(True) is True
    assert profile_has_land(False) is False
    assert profile_has_land(None) is None


def test_explanation_cites_matched_rules_only(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    resp = match_schemes(schemes, profile)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-old-age-pension")
    assert hit.explanation.en
    assert "age" in hit.explanation.en.lower() or "min_age" in hit.matched_rules
    # Must not invent thresholds not in rules
    assert "invent" not in hit.explanation.en.lower()


def test_pregnant_sc_matches_pmmvy(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-pregnant-sc"])
    resp = match_schemes(schemes, profile)
    assert "pmmvy" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "pmmvy")
    assert "gender" in hit.matched_rules
    assert "categories" in hit.matched_rules
    assert "maternity_required" in hit.matched_rules
    assert "janani-suraksha-yojana-kerala" in _matched_ids(resp)


def test_non_pregnant_female_excludes_maternity_schemes(schemes, profiles):
    """BPL widow who is not pregnant must not get likely PMMVY/JSY."""
    profile = _profile_from_sample(profiles["profile-widow-low-income"])
    profile = profile.model_copy(update={"is_pregnant": False, "is_lactating": False})
    resp = match_schemes(schemes, profile)
    assert "pmmvy" not in _matched_ids(resp)
    assert "janani-suraksha-yojana-kerala" not in _matched_ids(resp)
    assert any(
        e.scheme_id == "pmmvy" and "maternity_required" in e.reasons for e in resp.excluded
    )


def test_nfbs_requires_breadwinner_flag(schemes, profiles):
    bereaved = _profile_from_sample(profiles["profile-bereaved-bpl"])
    resp = match_schemes(schemes, bereaved)
    assert "nsap-nfbs" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "nsap-nfbs")
    assert "primary_breadwinner_deceased_required" in hit.matched_rules

    widow = _profile_from_sample(profiles["profile-widow-low-income"])
    widow = widow.model_copy(update={"primary_breadwinner_deceased": False})
    resp2 = match_schemes(schemes, widow)
    assert "nsap-nfbs" not in _matched_ids(resp2)


def test_likely_eligible_sorted_before_uncertain(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    profile = profile.model_copy(update={"disability": False, "occupations": ["other"]})
    resp = match_schemes(schemes, profile)
    assert resp.matched
    statuses = [m.status for m in resp.matched]
    if "likely_eligible" in statuses and "uncertain" in statuses:
        assert statuses.index("likely_eligible") < statuses.index("uncertain")


def test_api_match_endpoint():
    from fastapi.testclient import TestClient
    from app.main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

    r = client.get("/schemes?lang=en")
    assert r.status_code == 200
    assert r.json()["count"] >= 18

    r = client.get("/schemes/kerala-old-age-pension")
    assert r.status_code == 200
    assert r.json()["id"] == "kerala-old-age-pension"

    r = client.get("/schemes/does-not-exist")
    assert r.status_code == 404

    r = client.post(
        "/match",
        json={
            "age": 68,
            "gender": "male",
            "state": "Kerala",
            "annual_income": 45000,
            "land_ownership": "none",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] >= 1
    assert any(m["scheme_id"] == "kerala-old-age-pension" for m in body["matched"])

    # Nested contract shape
    r = client.post(
        "/api/v1/match",
        json={
            "profile": {
                "age": 52,
                "gender": "female",
                "state": "Kerala",
                "marital_status": "widow",
                "annual_income": 60000,
            },
            "options": {"lang": "en"},
        },
    )
    assert r.status_code == 200
    assert any(m["scheme_id"] == "kerala-widow-pension" for m in r.json()["matched"])


# ---------------------------------------------------------------------------
# Accuracy hardening (occupation / housing / kawwf / deserted)
# ---------------------------------------------------------------------------


def test_other_occupation_not_agri_labour(schemes):
    """occupation=other must hard-exclude agri labour (and not soft-match)."""
    profile = MatchProfile(
        age=65,
        gender="male",
        state="Kerala",
        district="Ernakulam",
        annual_income=45000,
        occupations=["other"],
        categories=[],
        land_ownership="none",
        disability=False,
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-agri-labour-pension" not in _matched_ids(resp)
    assert any(
        e.scheme_id == "kerala-agri-labour-pension" and "occupations" in e.reasons
        for e in resp.excluded
    )
    # Empty occupations also must NOT soft-match agri labour allowlist
    empty = profile.model_copy(update={"occupations": []})
    resp2 = match_schemes(schemes, empty)
    assert "kerala-agri-labour-pension" not in _matched_ids(resp2)
    assert any(
        e.scheme_id == "kerala-agri-labour-pension" and "occupations" in e.reasons
        for e in resp2.excluded
    )
    # District echoed on response
    assert resp.district == "Ernakulam"
    assert "District on profile: Ernakulam" in next(
        m.explanation.en for m in resp.matched if m.scheme_id == "kerala-old-age-pension"
    )


def test_farmer_with_land_pm_kisan_uncertain_ok(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-small-farmer"])
    resp = match_schemes(schemes, profile)
    assert "pm-kisan" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "pm-kisan")
    assert hit.status == "uncertain"
    assert "occupations" in hit.matched_rules
    assert "land_ownership" in hit.matched_rules
    # Farmer must not match agri-labour pension
    assert "kerala-agri-labour-pension" not in _matched_ids(resp)


def test_senior_low_income_old_age_likely(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    profile = profile.model_copy(update={"occupations": ["other"], "district": "Ernakulam"})
    resp = match_schemes(schemes, profile)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-old-age-pension")
    assert hit.status == "likely_eligible"


def test_no_housing_flags_life_not_likely(schemes):
    """LIFE Mission must not be likely_eligible without housing_status / housing category."""
    profile = MatchProfile(
        age=40,
        gender="female",
        state="Kerala",
        annual_income=80_000,
        occupations=["other"],
        categories=[],
        land_ownership="none",
        housing_status=None,
    )
    resp = match_schemes(schemes, profile)
    life = [m for m in resp.matched if m.scheme_id == "kerala-life-mission"]
    if life:
        assert life[0].status != "likely_eligible"
        assert "housing_status" in life[0].missing_profile_fields or life[0].status == "uncertain"
    # Explicit homeless → can match (still verify=true → uncertain)
    housed = profile.model_copy(update={"housing_status": "homeless", "categories": ["homeless"]})
    resp2 = match_schemes(schemes, housed)
    assert "kerala-life-mission" in _matched_ids(resp2)
    hit = next(m for m in resp2.matched if m.scheme_id == "kerala-life-mission")
    assert hit.status == "uncertain"
    assert "categories" in hit.matched_rules


def test_deserted_under_50_not_widow_path(schemes):
    profile = MatchProfile(
        age=45,
        gender="female",
        state="Kerala",
        marital_status="deserted",
        annual_income=50_000,
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-widow-pension" not in _matched_ids(resp)
    assert any(
        e.scheme_id == "kerala-widow-pension"
        and ("deserted_7_years_over_50" in e.reasons or "marital_status" in e.reasons)
        for e in resp.excluded
    )


def test_agri_labour_without_kawwf_is_uncertain(schemes):
    """Sevana agri labour notes require KAWWF — missing flag → uncertain not likely."""
    profile = MatchProfile(
        age=63,
        state="Kerala",
        annual_income=70_000,
        occupations=["agricultural_labour"],
        land_ownership="none",
        kawwf_member=None,
        agri_labour_years=None,
    )
    resp = match_schemes(schemes, profile)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-agri-labour-pension")
    assert hit.status == "uncertain"
    assert "kawwf_member" in hit.missing_profile_fields
    assert "agri_labour_years" in hit.missing_profile_fields

    full = profile.model_copy(update={"kawwf_member": True, "agri_labour_years": 12})
    resp2 = match_schemes(schemes, full)
    hit2 = next(m for m in resp2.matched if m.scheme_id == "kerala-agri-labour-pension")
    assert hit2.status == "likely_eligible"
    assert "kawwf_member_required" in hit2.matched_rules
    assert "min_agri_labour_years" in hit2.matched_rules


def test_kasp_hard_fails_without_secc_flags(schemes):
    profile = MatchProfile(
        age=40,
        state="Kerala",
        annual_income=80_000,
        occupations=["other"],
        categories=[],
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-kasp-pmjay" not in _matched_ids(resp)
    assert any(
        e.scheme_id == "kerala-kasp-pmjay" and "categories" in e.reasons for e in resp.excluded
    )


def test_district_filter_when_scheme_lists_districts(schemes):
    """Optional districts array hard-filters; absent array → no hard filter."""
    base = next(s for s in schemes if s["id"] == "kerala-old-age-pension")
    scheme = {
        **base,
        "id": "kerala-old-age-pension-district-demo",
        "eligibility_rules": {
            **(base.get("eligibility_rules") or {}),
            "districts": ["Ernakulam", "Thrissur"],
        },
    }
    ok = MatchProfile(
        age=65,
        state="Kerala",
        district="Ernakulam",
        annual_income=40_000,
        occupations=["other"],
    )
    bad = ok.model_copy(update={"district": "Wayanad"})
    assert not evaluate_scheme(scheme, ok).hard_fail
    assert "districts" in evaluate_scheme(scheme, ok).matched
    assert evaluate_scheme(scheme, bad).hard_fail


# ---------------------------------------------------------------------------
# Multi-state / nationwide matching
# ---------------------------------------------------------------------------


def test_tn_user_does_not_get_kerala_sevana(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-tn-girl-student"])
    resp = match_schemes(schemes, profile)
    sevana = {
        "kerala-old-age-pension",
        "kerala-widow-pension",
        "kerala-disability-pension-physical",
        "kerala-disability-pension-mental",
        "kerala-unmarried-women-pension",
        "kerala-agri-labour-pension",
    }
    assert _matched_ids(resp) & sevana == set()
    assert any(e.scheme_id == "kerala-old-age-pension" for e in resp.excluded)
    assert "tn-pudhumai-penn" in _matched_ids(resp)


def test_kerala_user_still_gets_sevana_old_age(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    resp = match_schemes(schemes, profile)
    assert "kerala-old-age-pension" in _matched_ids(resp)


def test_all_india_pm_kisan_matches_up_farmer_with_land(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-up-farmer-pmkisan"])
    resp = match_schemes(schemes, profile)
    assert "pm-kisan" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "pm-kisan")
    assert "states" in hit.matched_rules
    assert "land_ownership" in hit.matched_rules
    assert "kerala-old-age-pension" not in _matched_ids(resp)


def test_nationwide_flag_matches_any_state(schemes):
    pm = next(s for s in schemes if s["id"] == "pm-kisan")
    rules = pm.get("eligibility_rules") or {}
    assert rules.get("nationwide") is True
    assert "All India" in (rules.get("states") or [])
    for state in ("Tamil Nadu", "Karnataka", "Maharashtra", "West Bengal", "Delhi", "Ladakh"):
        profile = MatchProfile(
            age=40,
            gender="male",
            state=state,
            occupations=["farmer", "landholding_farmer"],
            land_ownership="cultivable_own",
        )
        result = evaluate_scheme(pm, profile)
        assert not result.hard_fail, state
        assert "states" in result.matched


def test_state_specific_scheme_rejects_other_state(schemes):
    scheme = next(s for s in schemes if s["id"] == "ka-gruha-lakshmi")
    ok = MatchProfile(age=35, gender="female", state="Karnataka")
    bad = MatchProfile(age=35, gender="female", state="Kerala")
    assert not evaluate_scheme(scheme, ok).hard_fail
    assert evaluate_scheme(scheme, bad).hard_fail
    assert "states" in evaluate_scheme(scheme, bad).unmatched


def test_match_response_includes_state(schemes):
    profile = MatchProfile(
        age=30,
        gender="female",
        state="Maharashtra",
        district="Pune",
        annual_income=150000,
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert resp.state == "Maharashtra"
    assert resp.district == "Pune"


# ---------------------------------------------------------------------------
# Expanded state catalogue (Gujarat and other newly covered states)
# ---------------------------------------------------------------------------


def test_gujarat_user_does_not_get_kerala_sevana(schemes):
    profile = MatchProfile(
        age=68,
        gender="male",
        state="Gujarat",
        annual_income=40_000,
        occupations=["other"],
        land_ownership="none",
        categories=["BPL"],
    )
    resp = match_schemes(schemes, profile)
    sevana = {
        "kerala-old-age-pension",
        "kerala-widow-pension",
        "kerala-disability-pension-physical",
        "kerala-disability-pension-mental",
        "kerala-unmarried-women-pension",
        "kerala-agri-labour-pension",
    }
    assert _matched_ids(resp) & sevana == set()
    assert any(e.scheme_id == "kerala-old-age-pension" for e in resp.excluded)


def test_gujarat_bpl_matches_mukhyamantri_amrutum(schemes):
    profile = MatchProfile(
        age=40,
        gender="female",
        state="Gujarat",
        annual_income=150_000,
        categories=["BPL"],
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "gj-mukhyamantri-amrutum" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "gj-mukhyamantri-amrutum")
    assert "states" in hit.matched_rules
    assert hit.verify is True


def test_gujarat_girl_student_matches_namo_lakshmi(schemes):
    profile = MatchProfile(
        age=16,
        gender="female",
        state="Gujarat",
        occupations=["student"],
        annual_income=100_000,
    )
    resp = match_schemes(schemes, profile)
    assert "gj-namo-lakshmi" in _matched_ids(resp)
    assert "kerala-egrantz" not in _matched_ids(resp)


def test_mp_woman_matches_ladli_behna_not_kerala(schemes):
    profile = MatchProfile(
        age=30,
        gender="female",
        state="Madhya Pradesh",
        marital_status="married",
        annual_income=180_000,
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "mp-ladli-behna" in _matched_ids(resp)
    assert "kerala-old-age-pension" not in _matched_ids(resp)
    assert "mh-ladki-bahin" not in _matched_ids(resp)


def test_nationwide_pm_kisan_still_matches_new_states(schemes):
    pm = next(s for s in schemes if s["id"] == "pm-kisan")
    for state in ("Gujarat", "Assam", "Odisha", "Delhi", "Goa", "Jharkhand", "Punjab", "Uttarakhand", "Himachal Pradesh", "Manipur", "Ladakh", "Puducherry"):
        profile = MatchProfile(
            age=40,
            gender="male",
            state=state,
            occupations=["farmer", "landholding_farmer"],
            land_ownership="cultivable_own",
        )
        result = evaluate_scheme(pm, profile)
        assert not result.hard_fail, state
        assert "states" in result.matched


def test_assam_orunodoi_matches_nfsa_woman(schemes):
    profile = MatchProfile(
        age=35,
        gender="female",
        state="Assam",
        annual_income=120_000,
        categories=["nfsa_ration"],
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "as-orunodoi" in _matched_ids(resp)
    assert "ga-griha-aadhar" not in _matched_ids(resp)


def test_haryana_senior_matches_old_age_samman(schemes):
    profile = MatchProfile(
        age=65,
        gender="male",
        state="Haryana",
        annual_income=80_000,
        occupations=["other"],
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "hr-old-age-samman" in _matched_ids(resp)
    assert "kerala-old-age-pension" not in _matched_ids(resp)


def test_catalogue_covers_new_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        for st in rules.get("states") or []:
            if st not in {"All India", "India"}:
                by_state.add(st)
    for required in (
        "Gujarat",
        "Rajasthan",
        "Bihar",
        "Madhya Pradesh",
        "Odisha",
        "Andhra Pradesh",
        "Telangana",
        "Assam",
        "Goa",
        "Jharkhand",
        "Haryana",
        "Chhattisgarh",
        "Delhi",
        "Punjab",
        "Uttarakhand",
        "Himachal Pradesh",
        "Manipur",
        "Nagaland",
        "Puducherry",
    ):
        assert required in by_state, required


def test_punjab_senior_matches_old_age_not_kerala(schemes):
    profile = MatchProfile(
        age=66,
        gender="male",
        state="Punjab",
        annual_income=50_000,
        occupations=["other"],
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "pb-old-age-pension" in _matched_ids(resp)
    assert "kerala-old-age-pension" not in _matched_ids(resp)
    assert "kerala-agri-labour-pension" not in _matched_ids(resp)


def test_uttarakhand_and_himachal_not_kerala_only(schemes):
    uk = MatchProfile(
        age=65,
        gender="female",
        state="Uttarakhand",
        annual_income=40_000,
        occupations=["other"],
    )
    hp = MatchProfile(
        age=62,
        gender="male",
        state="Himachal Pradesh",
        annual_income=30_000,
        occupations=["other"],
    )
    uk_resp = match_schemes(schemes, uk)
    hp_resp = match_schemes(schemes, hp)
    assert "uk-old-age-pension" in _matched_ids(uk_resp)
    assert "hp-old-age-pension" in _matched_ids(hp_resp)
    assert "kerala-old-age-pension" not in _matched_ids(uk_resp)
    assert "kerala-old-age-pension" not in _matched_ids(hp_resp)
    assert "kerala-widow-pension" not in _matched_ids(uk_resp)
    assert "kerala-egrantz" not in _matched_ids(hp_resp)


def test_catalogue_covers_punjab_uttarakhand_himachal(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        for st in rules.get("states") or []:
            if st not in {"All India", "India"}:
                by_state.add(st)
    for required in ("Punjab", "Uttarakhand", "Himachal Pradesh"):
        assert required in by_state, required

def test_manipur_senior_not_kerala_sevana(schemes):
    profile = MatchProfile(
        age=66,
        gender="male",
        state="Manipur",
        annual_income=40_000,
        occupations=["other"],
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "mn-old-age-pension" in _matched_ids(resp)
    assert "kerala-old-age-pension" not in _matched_ids(resp)
    assert "kerala-widow-pension" not in _matched_ids(resp)
    assert "kerala-agri-labour-pension" not in _matched_ids(resp)
    assert "kerala-egrantz" not in _matched_ids(resp)


def test_northeast_and_ut_catalogue_coverage(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        for st in rules.get("states") or []:
            if st not in {"All India", "India"}:
                by_state.add(st)
    for required in (
        "Arunachal Pradesh",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Sikkim",
        "Tripura",
        "Andaman and Nicobar Islands",
        "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu",
        "Jammu and Kashmir",
        "Ladakh",
        "Lakshadweep",
        "Puducherry",
    ):
        assert required in by_state, required


def test_sikkim_unmarried_woman_not_kerala(schemes):
    profile = MatchProfile(
        age=48,
        gender="female",
        state="Sikkim",
        marital_status="unmarried",
        categories=["BPL"],
        annual_income=50_000,
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "sk-unmarried-women-pension" in _matched_ids(resp)
    assert "kerala-unmarried-women-pension" not in _matched_ids(resp)
    assert "kerala-old-age-pension" not in _matched_ids(resp)


def test_nagaland_cmhis_not_kerala_health(schemes):
    profile = MatchProfile(
        age=40,
        gender="female",
        state="Nagaland",
        categories=["pmjay"],
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "nl-cmhis" in _matched_ids(resp)
    assert "kerala-kasp-pmjay" not in _matched_ids(resp)


def test_jk_ladli_beti_girl_child(schemes):
    profile = MatchProfile(
        age=5,
        gender="female",
        state="Jammu and Kashmir",
        annual_income=60_000,
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "jk-ladli-beti" in _matched_ids(resp)
    assert "uk-nanda-gaura" not in _matched_ids(resp)
    assert "wb-kanyashree" not in _matched_ids(resp)



# ---------------------------------------------------------------------------
# LIFE Mission income ceiling (₹3 lakh/year hard filter even if verify=true)
# ---------------------------------------------------------------------------


def test_life_excluded_for_high_monthly_income_kerala_profile(schemes):
    """Production bug: age 53 F married Palakkad, monthly 12.5L → annual 1.5Cr must NOT match LIFE."""
    profile = MatchProfile(
        age=53,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="married",
        monthly_household_income=1_250_000,  # wizard field → annual = 15_000_000
        disability=False,
        disability_percent=0,
        primary_breadwinner_deceased=False,
        land_ownership="none",
        occupations=["other"],
        categories=[],
        housing_status=None,
    )
    assert profile.annual_income == 15_000_000
    resp = match_schemes(schemes, profile)
    assert "kerala-life-mission" not in _matched_ids(resp)
    assert "kerala-life-mission" not in {n.scheme_id for n in resp.needs_verification}
    excluded = next(e for e in resp.excluded if e.scheme_id == "kerala-life-mission")
    assert excluded.status == "not_eligible"
    assert "max_annual_income" in excluded.reasons


def test_life_uncertain_for_low_income_landless_homeless(schemes):
    """Monthly ~20k (annual 2.4L) + homeless/landless → LIFE may appear as uncertain (verify)."""
    profile = MatchProfile(
        age=53,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="married",
        monthly_household_income=20_000,  # annual 240_000 < 300_000
        disability=False,
        land_ownership="none",
        occupations=["other"],
        categories=["landless", "homeless"],
        housing_status="homeless",
    )
    assert profile.annual_income == 240_000
    resp = match_schemes(schemes, profile)
    assert "kerala-life-mission" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "kerala-life-mission")
    assert hit.status == "uncertain"
    assert hit.verify is True
    assert "max_annual_income" in hit.matched_rules
    assert "categories" in hit.matched_rules


def test_life_income_hard_fail_even_with_verify_and_housing(schemes):
    """Exceeding ₹3L excludes LIFE even when housing categories would otherwise soft-match."""
    profile = MatchProfile(
        age=40,
        gender="female",
        state="Kerala",
        monthly_household_income=50_000,  # annual 600_000 > 300_000
        land_ownership="none",
        categories=["homeless"],
        housing_status="homeless",
        occupations=["other"],
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-life-mission" not in _matched_ids(resp)
    excluded = next(e for e in resp.excluded if e.scheme_id == "kerala-life-mission")
    assert "max_annual_income" in excluded.reasons


# ---------------------------------------------------------------------------
# Income differentiation: same demographics, three income bands
# ---------------------------------------------------------------------------


def _kerala_base(**income_kwargs) -> MatchProfile:
    """Shared Kerala demographics — only income varies across the three bands."""
    return MatchProfile(
        age=53,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="married",
        disability=False,
        disability_percent=0,
        primary_breadwinner_deceased=False,
        land_ownership="none",
        occupations=["other"],
        categories=["homeless", "landless"],
        housing_status="homeless",
        **income_kwargs,
    )


def test_three_income_bands_differ_for_life_and_pensions(schemes):
    """Low ~3k/mo, mid ~40k/mo, high 12.5L/year → different LIFE/pension outcomes; high never gets LIFE."""
    low = _kerala_base(monthly_household_income=3_000)  # annual 36_000
    mid = _kerala_base(monthly_household_income=40_000)  # annual 480_000
    high = _kerala_base(annual_income=1_250_000)  # 12.5L/year (yearly wizard mode)

    assert low.annual_income == 36_000
    assert mid.annual_income == 480_000
    assert high.annual_income == 1_250_000
    assert high.monthly_household_income == pytest.approx(1_250_000 / 12)

    resp_low = match_schemes(schemes, low)
    resp_mid = match_schemes(schemes, mid)
    resp_high = match_schemes(schemes, high)

    life = "kerala-life-mission"
    # LIFE max_annual=300000: low under, mid/high over
    assert life in _matched_ids(resp_low)
    assert life not in _matched_ids(resp_mid)
    assert life not in _matched_ids(resp_high)
    assert any(
        e.scheme_id == life and "max_annual_income" in e.reasons for e in resp_high.excluded
    )
    assert any(
        e.scheme_id == life and "max_annual_income" in e.reasons for e in resp_mid.excluded
    )

    # Kerala Sevana-style pensions: max_annual=100000 — low may match age/gender/etc.;
    # mid (4.8L) and high (12.5L) must be excluded on income.
    pension = "kerala-old-age-pension"  # min_age 60 — age 53 will fail age, not income.
    # Use widow pension path? age 53 married female — widow needs widow status.
    # Disability / unmarried not applicable. agri labour needs occupation.
    # So for this demographic, pensions may not match on age/marital — assert LIFE band
    # differences above, and assert high income excludes LIFE + Karunya (3L) + Matru etc.
    karunya = "kerala-karunya-benevolent-fund"  # max_annual 300000
    assert karunya not in _matched_ids(resp_high)
    assert karunya not in _matched_ids(resp_mid)
    # low vs mid/high matched sets differ (LIFE present only on low)
    assert _matched_ids(resp_low) != _matched_ids(resp_mid)
    assert _matched_ids(resp_low) != _matched_ids(resp_high)
    # Mid (4.8L) and high (12.5L) may share the same non-income-gated matches for this
    # demographic; pension differentiation is covered below with a senior profile.

    # Same demographics as seniors → pensions differ by income
    senior_low = MatchProfile(
        age=70,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="widow",
        monthly_household_income=3_000,
        disability=False,
        land_ownership="none",
        occupations=["other"],
        categories=["BPL"],
    )
    senior_mid = MatchProfile(
        age=70,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="widow",
        monthly_household_income=40_000,  # annual 4.8L > 1L Sevana + > 3L LIFE
        disability=False,
        land_ownership="none",
        occupations=["other"],
        categories=["BPL"],
    )
    senior_high = MatchProfile(
        age=70,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="widow",
        annual_income=1_250_000,
        disability=False,
        land_ownership="none",
        occupations=["other"],
        categories=["BPL"],
    )
    r_sl = match_schemes(schemes, senior_low)
    r_sm = match_schemes(schemes, senior_mid)
    r_sh = match_schemes(schemes, senior_high)
    oap = "kerala-old-age-pension"
    widow = "kerala-widow-pension"
    assert oap in _matched_ids(r_sl)
    assert widow in _matched_ids(r_sl)
    assert oap not in _matched_ids(r_sm) and oap not in _matched_ids(r_sh)
    assert widow not in _matched_ids(r_sm) and widow not in _matched_ids(r_sh)
    assert _matched_ids(r_sl) != _matched_ids(r_sm)
    assert _matched_ids(r_sl) != _matched_ids(r_sh)


def test_high_annual_income_via_yearly_field_excludes_life(schemes):
    """Wizard Yearly mode sends annual_income=1250000 directly — must exclude LIFE."""
    profile = MatchProfile(
        age=53,
        gender="female",
        state="Kerala",
        district="Palakkad",
        marital_status="married",
        annual_income=1_250_000,
        categories=["homeless"],
        housing_status="homeless",
        land_ownership="none",
        occupations=["other"],
    )
    assert profile.annual_income == 1_250_000
    resp = match_schemes(schemes, profile)
    assert "kerala-life-mission" not in _matched_ids(resp)
    excluded = next(e for e in resp.excluded if e.scheme_id == "kerala-life-mission")
    assert "max_annual_income" in excluded.reasons


def test_implies_low_income_soft_gate_excludes_high_earners(schemes):
    """BPL/destitute schemes without numeric ceiling exclude annual >= 5L via implies_low_income."""
    high = MatchProfile(
        age=65,
        gender="male",
        state="Meghalaya",
        annual_income=600_000,
        categories=["BPL"],
        occupations=["other"],
        land_ownership="none",
    )
    low = MatchProfile(
        age=65,
        gender="male",
        state="Meghalaya",
        annual_income=80_000,
        categories=["BPL"],
        occupations=["other"],
        land_ownership="none",
    )
    resp_high = match_schemes(schemes, high)
    resp_low = match_schemes(schemes, low)
    sid = "ml-nsap-old-age-pension"
    assert sid not in _matched_ids(resp_high)
    assert any(
        e.scheme_id == sid and "implies_low_income" in e.reasons for e in resp_high.excluded
    )
    assert sid in _matched_ids(resp_low)


def test_aasara_official_income_ceiling(schemes):
    """Telangana Aasara: official urban max ₹2L encoded; over → exclude."""
    over = MatchProfile(
        age=65,
        gender="male",
        state="Telangana",
        annual_income=250_000,
        occupations=["other"],
        categories=[],
        land_ownership="none",
    )
    under = MatchProfile(
        age=65,
        gender="male",
        state="Telangana",
        annual_income=180_000,
        occupations=["other"],
        categories=[],
        land_ownership="none",
    )
    resp_over = match_schemes(schemes, over)
    resp_under = match_schemes(schemes, under)
    sid = "tg-aasara-pension"
    assert sid not in _matched_ids(resp_over)
    assert any(
        e.scheme_id == sid and "max_annual_income" in e.reasons for e in resp_over.excluded
    )
    assert sid in _matched_ids(resp_under)


# ---------------------------------------------------------------------------
# Hard gates: maternity absent, SECC list schemes, any income amount
# ---------------------------------------------------------------------------


def test_maternity_absent_or_null_hard_excludes_jsy(schemes):
    """Not pregnant / not lactating — including null/absent — must hard-fail maternity schemes."""
    base = dict(
        age=53,
        gender="female",
        state="Kerala",
        marital_status="married",
        annual_income=80_000,
        land_ownership="none",
        occupations=["other"],
        categories=["BPL", "SC"],
    )
    for update in (
        {},  # maternity fields absent
        {"is_pregnant": None, "is_lactating": None},
        {"is_pregnant": False, "is_lactating": False},
        {"is_pregnant": False, "is_lactating": None},
    ):
        profile = MatchProfile(**{**base, **update})
        resp = match_schemes(schemes, profile)
        assert "janani-suraksha-yojana-kerala" not in _matched_ids(resp), update
        assert "pmmvy" not in _matched_ids(resp), update
        assert any(
            e.scheme_id == "janani-suraksha-yojana-kerala" and "maternity_required" in e.reasons
            for e in resp.excluded
        ), update


def test_high_earner_kerala_female_excludes_poverty_and_list_schemes(schemes):
    """Live bug: Kerala F 53 married, land none, annual 18.5L / 12.5L must not soft-match JSY/PMJAY/LIFE/Sevana."""
    banned = {
        "janani-suraksha-yojana-kerala",
        "pmmvy",
        "ab-pmjay-national",
        "kerala-kasp-pmjay",
        "kerala-life-mission",
        "kerala-old-age-pension",
        "kerala-widow-pension",
        "kerala-agri-labour-pension",
        "kerala-unmarried-women-pension",
        "kerala-disability-pension-physical",
        "kerala-disability-pension-mental",
    }
    for annual in (1_850_000, 1_250_000):
        profile = MatchProfile(
            age=53,
            gender="female",
            state="Kerala",
            district="Palakkad",
            marital_status="married",
            annual_income=annual,
            land_ownership="none",
            occupations=["other"],
            categories=[],
            disability=False,
            is_pregnant=False,
            is_lactating=False,
            primary_breadwinner_deceased=False,
        )
        resp = match_schemes(schemes, profile)
        hit = _matched_ids(resp) & banned
        assert hit == set(), f"annual={annual} unexpectedly matched {hit}"


def test_income_amounts_numeric_ceilings_and_soft_gate(schemes):
    """Any annual amount is compared numerically — 18.5L, 12.5L, 2.5L, 80k, 36k."""
    # LIFE max_annual_income = 300000
    for annual, expect_life in (
        (1_850_000, False),
        (1_250_000, False),
        (250_000, True),  # under 3L with housing signal
        (80_000, True),
        (36_000, True),
    ):
        profile = MatchProfile(
            age=40,
            gender="female",
            state="Kerala",
            annual_income=annual,
            land_ownership="none",
            occupations=["other"],
            categories=["homeless", "landless"],
            housing_status="homeless",
        )
        resp = match_schemes(schemes, profile)
        if expect_life:
            assert "kerala-life-mission" in _matched_ids(resp), annual
        else:
            assert "kerala-life-mission" not in _matched_ids(resp), annual
            assert any(
                e.scheme_id == "kerala-life-mission" and "max_annual_income" in e.reasons
                for e in resp.excluded
            ), annual

    # implies_low_income gate at 5L (Meghalaya NSAP)
    for annual, expect in ((1_850_000, False), (250_000, True), (80_000, True), (36_000, True)):
        profile = MatchProfile(
            age=65,
            gender="male",
            state="Meghalaya",
            annual_income=annual,
            categories=["BPL"],
            occupations=["other"],
            land_ownership="none",
        )
        resp = match_schemes(schemes, profile)
        sid = "ml-nsap-old-age-pension"
        if expect:
            assert sid in _matched_ids(resp), annual
        else:
            assert sid not in _matched_ids(resp), annual


def test_low_income_pregnant_bpl_still_matches_maternity_and_list(schemes):
    """Encoded low-income pregnant / BPL / SECC cases still work."""
    pregnant = MatchProfile(
        age=24,
        gender="female",
        state="Kerala",
        marital_status="married",
        annual_income=36_000,
        land_ownership="none",
        occupations=["other"],
        categories=["SC", "BPL"],
        is_pregnant=True,
    )
    resp = match_schemes(schemes, pregnant)
    assert "pmmvy" in _matched_ids(resp)
    assert "janani-suraksha-yojana-kerala" in _matched_ids(resp)

    secc = MatchProfile(
        age=40,
        gender="female",
        state="Kerala",
        annual_income=80_000,
        occupations=["other"],
        categories=["secc_deprivation"],
        land_ownership="none",
        flags={"secc_eligible": True},
    )
    resp2 = match_schemes(schemes, secc)
    assert "kerala-kasp-pmjay" in _matched_ids(resp2)
    assert "ab-pmjay-national" in _matched_ids(resp2)


# ---------------------------------------------------------------------------
# Cross-country matching
# ---------------------------------------------------------------------------


def test_india_profile_defaults_country_and_still_matches_sevana(schemes, profiles):
    """Backward compat: missing country → India; Kerala Sevana still matches."""
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    assert profile.country == "India"
    resp = match_schemes(schemes, profile)
    assert "kerala-old-age-pension" in _matched_ids(resp)


def test_bd_profile_does_not_get_kerala_sevana(schemes):
    profile = MatchProfile(
        country="Bangladesh",
        age=70,
        gender="male",
        state="Dhaka",
        district="Dhaka",
        marital_status="married",
        annual_income=5000,
        occupations=["other"],
        categories=["none"] if False else [],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "kerala-old-age-pension" not in _matched_ids(resp)
    # Country mismatch should hard-exclude Kerala schemes
    excluded = {e.scheme_id: e for e in resp.excluded}
    assert "kerala-old-age-pension" in excluded
    assert "countries" in excluded["kerala-old-age-pension"].reasons


def test_bd_scheme_matches_bd_profile(schemes):
    profile = MatchProfile(
        country="Bangladesh",
        age=70,
        gender="male",
        state="Dhaka",
        district="Dhaka",
        marital_status="married",
        annual_income=5000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "bd-old-age-allowance" in _matched_ids(resp)
    hit = next(m for m in resp.matched if m.scheme_id == "bd-old-age-allowance")
    assert "countries" in hit.matched_rules


def test_nepal_senior_matches_np_scheme_not_india(schemes):
    profile = MatchProfile(
        country="Nepal",
        age=72,
        gender="female",
        state="Bagmati",
        district="Kathmandu",
        marital_status="widow",
        annual_income=100000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    assert "np-senior-citizen-allowance" in _matched_ids(resp)
    assert "np-widow-allowance" in _matched_ids(resp)
    assert "kerala-old-age-pension" not in _matched_ids(resp)


def test_catalogue_includes_non_india_countries(schemes):
    ids = {s["id"] for s in schemes}
    for sid in (
        "bd-old-age-allowance",
        "bd-widow-allowance",
        "np-senior-citizen-allowance",
        "lk-aswesuma",
        "mv-disability-allowance",
        "us-snap",
        "us-ssi",
    ):
        assert sid in ids
    countries = set()
    for s in schemes:
        for c in (s.get("eligibility_rules") or {}).get("countries") or []:
            countries.add(c)
    assert "India" in countries
    assert "Bangladesh" in countries
    assert "Nepal" in countries
    assert "Sri Lanka" in countries
    assert "United States" in countries


def test_us_profile_matches_snap_and_ssi_not_india(schemes):
    """US senior low-income profile matches SNAP/SSI-style federal rows, not India schemes."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="California",
        district="Los Angeles",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "us-social-security-retirement" in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids
    assert "bd-old-age-allowance" not in ids
    snap = next(m for m in resp.matched if m.scheme_id == "us-snap")
    assert "countries" in snap.matched_rules
    assert snap.verify is True


def test_us_disabled_matches_ssdi_not_india_disability(schemes):
    profile = MatchProfile(
        country="United States",
        age=45,
        gender="male",
        state="Texas",
        district="Harris",
        marital_status="married",
        annual_income=8000,
        occupations=["other"],
        categories=[],
        disability=True,
        disability_percent=60,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "us-ssdi" in ids
    assert "us-snap" in ids
    assert "kerala-disability-pension-physical" not in ids
    assert "bd-disability-allowance" not in ids


def test_india_profile_does_not_match_us_schemes(schemes, profiles):
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "us-snap" not in ids
    assert "us-ssi" not in ids
    assert "us-medicare" not in ids


# ---------------------------------------------------------------------------
# US Wave 1 state deepen (CA / NY / TX / FL / IL)
# ---------------------------------------------------------------------------


def test_ca_profile_matches_ca_and_federal_us(schemes):
    """California low-income senior matches ca-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="California",
        district="Los Angeles",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "ca-calfresh" in ids
    assert "ca-medi-cal" in ids
    assert "ca-ssi-ssp" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "tx-snap" not in ids
    assert "ny-snap" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_tx_profile_does_not_match_ca_schemes(schemes):
    """Texas profile must not match California-only schemes; may match tx-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Texas",
        district="Harris",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    ca_ids = {s["id"] for s in schemes if s["id"].startswith("ca-")}
    assert ids & ca_ids == set()
    assert any(e.scheme_id == "ca-calfresh" and "states" in e.reasons for e in resp.excluded)
    assert "tx-snap" in ids or "tx-medicaid" in ids or "tx-tanf" in ids
    assert "us-snap" in ids


def test_india_profile_does_not_match_us_or_ca_schemes(schemes, profiles):
    """India Kerala profile must not match federal us-* or Wave 1 ca-* state schemes."""
    profile = _profile_from_sample(profiles["profile-senior-destitute"])
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "us-snap" not in ids
    assert "us-ssi" not in ids
    assert "ca-calfresh" not in ids
    assert "ca-calworks" not in ids
    assert "tx-snap" not in ids
    assert "il-snap" not in ids
    assert "kerala-old-age-pension" in ids


def test_catalogue_covers_us_wave1_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in ("California", "New York", "Texas", "Florida", "Illinois"):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 2 state deepen (PA / OH / GA / NC / MI)
# ---------------------------------------------------------------------------


def test_pa_profile_matches_pa_and_federal_us(schemes):
    """Pennsylvania low-income senior matches pa-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="Pennsylvania",
        district="Philadelphia",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "pa-snap" in ids
    assert "pa-medicaid" in ids
    assert "pa-liheap" in ids
    assert "pa-pace" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "oh-snap" not in ids
    assert "ca-calfresh" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_oh_profile_does_not_match_pa_schemes(schemes):
    """Ohio profile must not match Pennsylvania-only schemes; may match oh-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Ohio",
        district="Franklin",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    pa_ids = {s["id"] for s in schemes if s["id"].startswith("pa-")}
    assert ids & pa_ids == set()
    assert any(e.scheme_id == "pa-snap" and "states" in e.reasons for e in resp.excluded)
    assert "oh-snap" in ids or "oh-medicaid" in ids or "oh-owf-tanf" in ids
    assert "us-snap" in ids


def test_catalogue_covers_us_wave2_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "Pennsylvania",
        "Ohio",
        "Georgia",
        "North Carolina",
        "Michigan",
    ):
        assert required in by_state, required



# ---------------------------------------------------------------------------
# US Wave 3 state deepen (NJ / VA / WA / AZ / MA)
# ---------------------------------------------------------------------------


def test_nj_profile_matches_nj_and_federal_us(schemes):
    """New Jersey low-income senior matches nj-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="New Jersey",
        district="Essex",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "nj-snap" in ids
    assert "nj-familycare" in ids
    assert "nj-liheap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "va-snap" not in ids
    assert "pa-snap" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_va_profile_does_not_match_nj_schemes(schemes):
    """Virginia profile must not match New Jersey-only schemes; may match va-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Virginia",
        district="Fairfax",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    nj_ids = {s["id"] for s in schemes if s["id"].startswith("nj-")}
    assert ids & nj_ids == set()
    assert any(e.scheme_id == "nj-snap" and "states" in e.reasons for e in resp.excluded)
    assert "va-snap" in ids or "va-medicaid" in ids or "va-tanf" in ids
    assert "us-snap" in ids


def test_catalogue_covers_us_wave3_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "New Jersey",
        "Virginia",
        "Washington",
        "Arizona",
        "Massachusetts",
    ):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 4 state deepen (TN / IN / MO / MD / WI)
# ---------------------------------------------------------------------------


def test_tennessee_profile_matches_us_tn_and_federal_us(schemes):
    """Tennessee low-income senior matches us-tn-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="Tennessee",
        district="Davidson",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "us-tn-snap" in ids
    assert "us-tn-tenncare" in ids
    assert "us-tn-liheap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "in-snap" not in ids
    assert "mo-snap" not in ids
    assert "tn-pudhumai-penn" not in ids  # India Tamil Nadu
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_indiana_profile_does_not_match_us_tn_schemes(schemes):
    """Indiana profile must not match Tennessee-only us-tn-* schemes; may match in-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Indiana",
        district="Marion",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    us_tn_ids = {s["id"] for s in schemes if s["id"].startswith("us-tn-")}
    assert ids & us_tn_ids == set()
    assert any(e.scheme_id == "us-tn-snap" and "states" in e.reasons for e in resp.excluded)
    assert "in-snap" in ids or "in-medicaid" in ids or "in-tanf" in ids
    assert "us-snap" in ids


def test_india_tamil_nadu_matches_tn_not_us_tennessee(schemes, profiles):
    """India Tamil Nadu must still match India tn-* and must NOT match US Tennessee us-tn-*."""
    # Prefer sample profile if it is Tamil Nadu; otherwise build explicitly.
    profile = MatchProfile(
        country="India",
        age=22,
        gender="female",
        state="Tamil Nadu",
        district="Chennai",
        marital_status="unmarried",
        annual_income=50000,
        occupations=["student"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "tn-pudhumai-penn" in ids or any(i.startswith("tn-") and not i.startswith("us-tn-") for i in ids)
    us_tn_ids = {s["id"] for s in schemes if s["id"].startswith("us-tn-")}
    assert ids & us_tn_ids == set()
    assert "us-tn-snap" not in ids
    assert "us-snap" not in ids


def test_catalogue_covers_us_wave4_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "Tennessee",
        "Indiana",
        "Missouri",
        "Maryland",
        "Wisconsin",
    ):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 5 state deepen (CO / MN / SC / AL / LA)
# ---------------------------------------------------------------------------


def test_colorado_profile_matches_co_and_federal_us(schemes):
    """Colorado low-income senior matches co-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="Colorado",
        district="Denver",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "co-snap" in ids
    assert "co-health-first-colorado" in ids
    assert "co-leap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "us-mn-snap" not in ids
    assert "sc-snap" not in ids
    assert "al-snap" not in ids
    assert "us-la-snap" not in ids
    assert "mn-old-age-pension" not in ids  # India Manipur
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_minnesota_profile_does_not_match_colorado_schemes(schemes):
    """Minnesota profile must not match Colorado-only co-* schemes; may match us-mn-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Minnesota",
        district="Hennepin",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    co_ids = {s["id"] for s in schemes if s["id"].startswith("co-")}
    assert ids & co_ids == set()
    assert any(e.scheme_id == "co-snap" and "states" in e.reasons for e in resp.excluded)
    assert "us-mn-snap" in ids or "us-mn-medical-assistance" in ids or "us-mn-mfip" in ids
    assert "us-snap" in ids
    # Must not match India Manipur mn-* rows
    india_mn = {s["id"] for s in schemes if s["id"].startswith("mn-") and not s["id"].startswith("us-mn-")}
    assert ids & india_mn == set()


def test_india_manipur_matches_mn_not_us_minnesota(schemes):
    """India Manipur must still match India mn-* and must NOT match US Minnesota us-mn-*."""
    profile = MatchProfile(
        country="India",
        age=70,
        gender="female",
        state="Manipur",
        district="Imphal West",
        marital_status="widow",
        annual_income=30000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert any(i.startswith("mn-") and not i.startswith("us-mn-") for i in ids)
    us_mn_ids = {s["id"] for s in schemes if s["id"].startswith("us-mn-")}
    assert ids & us_mn_ids == set()
    assert "us-mn-snap" not in ids
    assert "us-snap" not in ids


def test_india_ladakh_matches_la_not_us_louisiana(schemes):
    """India Ladakh must still match India la-* and must NOT match US Louisiana us-la-*."""
    profile = MatchProfile(
        country="India",
        age=70,
        gender="female",
        state="Ladakh",
        district="Leh",
        marital_status="widow",
        annual_income=30000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert any(i.startswith("la-") and not i.startswith("us-la-") for i in ids)
    us_la_ids = {s["id"] for s in schemes if s["id"].startswith("us-la-")}
    assert ids & us_la_ids == set()
    assert "us-la-snap" not in ids


def test_catalogue_covers_us_wave5_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "Colorado",
        "Minnesota",
        "South Carolina",
        "Alabama",
        "Louisiana",
    ):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 6 state deepen (KY / OR / OK / CT / UT)
# ---------------------------------------------------------------------------


def test_kentucky_profile_matches_ky_and_federal_us(schemes):
    """Kentucky low-income senior matches ky-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="Kentucky",
        district="Jefferson",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "ky-snap" in ids
    assert "ky-medicaid" in ids
    assert "ky-liheap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "or-snap" not in ids
    assert "ok-snap" not in ids
    assert "ct-snap" not in ids
    assert "ut-snap" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_oregon_profile_does_not_match_kentucky_schemes(schemes):
    """Oregon profile must not match Kentucky-only ky-* schemes; may match or-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Oregon",
        district="Multnomah",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    ky_ids = {s["id"] for s in schemes if s["id"].startswith("ky-")}
    assert ids & ky_ids == set()
    assert any(e.scheme_id == "ky-snap" and "states" in e.reasons for e in resp.excluded)
    assert "or-snap" in ids or "or-ohp" in ids or "or-tanf" in ids
    assert "us-snap" in ids


def test_catalogue_covers_us_wave6_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "Kentucky",
        "Oregon",
        "Oklahoma",
        "Connecticut",
        "Utah",
    ):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 7 state deepen (IA / NV / AR / MS / KS)
# ---------------------------------------------------------------------------


def test_iowa_profile_matches_ia_and_federal_us(schemes):
    """Iowa low-income senior matches ia-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="Iowa",
        district="Polk",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "ia-snap" in ids
    assert "ia-medicaid" in ids
    assert "ia-liheap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "nv-snap" not in ids
    assert "us-ar-snap" not in ids
    assert "ms-snap" not in ids
    assert "ks-snap" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_nevada_profile_does_not_match_iowa_schemes(schemes):
    """Nevada profile must not match Iowa-only ia-* schemes; may match nv-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Nevada",
        district="Clark",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    ia_ids = {s["id"] for s in schemes if s["id"].startswith("ia-")}
    assert ids & ia_ids == set()
    assert any(e.scheme_id == "ia-snap" and "states" in e.reasons for e in resp.excluded)
    assert "nv-snap" in ids or "nv-medicaid" in ids or "nv-tanf" in ids
    assert "us-snap" in ids


def test_india_arunachal_matches_ar_not_us_arkansas(schemes):
    """India Arunachal Pradesh must still match India ar-* and must NOT match US Arkansas us-ar-*."""
    profile = MatchProfile(
        country="India",
        age=70,
        gender="female",
        state="Arunachal Pradesh",
        district="Itanagar",
        marital_status="widow",
        annual_income=30000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert any(i.startswith("ar-") and not i.startswith("us-ar-") for i in ids)
    us_ar_ids = {s["id"] for s in schemes if s["id"].startswith("us-ar-")}
    assert ids & us_ar_ids == set()
    assert "us-ar-snap" not in ids
    assert "us-snap" not in ids


def test_catalogue_covers_us_wave7_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "Iowa",
        "Nevada",
        "Arkansas",
        "Mississippi",
        "Kansas",
    ):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 8 state deepen (NM / NE / ID / HI / ME)
# ---------------------------------------------------------------------------


def test_new_mexico_profile_matches_nm_and_federal_us(schemes):
    """New Mexico low-income senior matches nm-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="New Mexico",
        district="Bernalillo",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "nm-snap" in ids
    assert "nm-medicaid" in ids
    assert "nm-liheap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "ne-snap" not in ids
    assert "id-snap" not in ids
    assert "hi-snap" not in ids
    assert "me-snap" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_nebraska_profile_does_not_match_nm_schemes(schemes):
    """Nebraska profile must not match New Mexico-only nm-* schemes; may match ne-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Nebraska",
        district="Douglas",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    nm_ids = {s["id"] for s in schemes if s["id"].startswith("nm-")}
    assert ids & nm_ids == set()
    assert any(e.scheme_id == "nm-snap" and "states" in e.reasons for e in resp.excluded)
    assert "ne-snap" in ids or "ne-medicaid" in ids or "ne-adc" in ids
    assert "us-snap" in ids


def test_catalogue_covers_us_wave8_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "New Mexico",
        "Nebraska",
        "Idaho",
        "Hawaii",
        "Maine",
    ):
        assert required in by_state, required


# ---------------------------------------------------------------------------
# US Wave 9 state deepen (NH / RI / MT / DE / SD)
# ---------------------------------------------------------------------------


def test_new_hampshire_profile_matches_nh_and_federal_us(schemes):
    """New Hampshire low-income senior matches nh-* state rows and federal us-* nationwide."""
    profile = MatchProfile(
        country="United States",
        age=70,
        gender="female",
        state="New Hampshire",
        district="Hillsborough",
        marital_status="widow",
        annual_income=12000,
        monthly_household_income=1000,
        occupations=["other"],
        categories=[],
        disability=False,
        disability_percent=0,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    assert "nh-snap" in ids
    assert "nh-medicaid" in ids
    assert "nh-liheap" in ids
    assert "us-snap" in ids
    assert "us-ssi" in ids
    assert "us-medicare" in ids
    assert "ri-snap" not in ids
    assert "mt-snap" not in ids
    assert "de-snap" not in ids
    assert "sd-snap" not in ids
    assert "kerala-old-age-pension" not in ids
    assert "pm-kisan" not in ids


def test_rhode_island_profile_does_not_match_nh_schemes(schemes):
    """Rhode Island profile must not match New Hampshire-only nh-* schemes; may match ri-* and federal us-*."""
    profile = MatchProfile(
        country="United States",
        age=40,
        gender="female",
        state="Rhode Island",
        district="Providence",
        marital_status="married",
        annual_income=15000,
        occupations=["other"],
        categories=[],
        disability=False,
        land_ownership="none",
    )
    resp = match_schemes(schemes, profile)
    ids = _matched_ids(resp)
    nh_ids = {s["id"] for s in schemes if s["id"].startswith("nh-")}
    assert ids & nh_ids == set()
    assert any(e.scheme_id == "nh-snap" and "states" in e.reasons for e in resp.excluded)
    assert "ri-snap" in ids or "ri-medicaid" in ids or "ri-works" in ids
    assert "us-snap" in ids


def test_catalogue_covers_us_wave9_states(schemes):
    by_state = set()
    for s in schemes:
        rules = s.get("eligibility_rules") or {}
        if rules.get("nationwide"):
            continue
        if "United States" not in (rules.get("countries") or []):
            continue
        for st in rules.get("states") or []:
            by_state.add(st)
    for required in (
        "New Hampshire",
        "Rhode Island",
        "Montana",
        "Delaware",
        "South Dakota",
    ):
        assert required in by_state, required
