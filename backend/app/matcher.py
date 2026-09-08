"""Deterministic eligibility matcher.

Hard filters ONLY from structured eligibility_rules — never invent thresholds.
LLM must never decide eligibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .catalogue import catalogue_payload, resolve_last_verified
from .explanations import build_explanation
from .models import (
    ExcludedScheme,
    MatchedScheme,
    MatchOptions,
    MatchProfile,
    MatchResponse,
    NeedsVerificationItem,
)

# Categories that cannot be inferred from typical UI fields alone.
SECC_STYLE_CATEGORIES = {
    "secc_deprivation",
    "rsby_chis_2018_19",
    "pmjay",
    "eshram",
    "pmkisan",
    "mgnrega",
    "nfsa_ration",
    "aww_awh_asha",
}

# LIFE / housing beneficiary types — require explicit housing_status or category.
HOUSING_STYLE_CATEGORIES = {
    "homeless",
    "landless",
    "incomplete_house",
    "temporary_shelter",
    "landed_homeless",
    "landless_homeless",
}

# land_ownership scheme values that REQUIRE the profile to own cultivable land
LAND_REQUIRED_TOKENS = {
    "cultivable_landholding_required",
    "landholding_required",
    "requires_land",
    "cultivable_own",
}

# Profile land values meaning "has land / ownership"
LAND_POSITIVE = {
    "true",
    "yes",
    "1",
    "cultivable_own",
    "owns_house_and_land",
    "owned",
    "owner",
    "landholding",
    "has_land",
    "own",
    "cultivable",
}

# Profile land values meaning "no land"
LAND_NEGATIVE = {
    "false",
    "no",
    "0",
    "none",
    "landless",
    "nil",
    "n/a",
    "na",
}


def _norm(value: str | None) -> str:
    if value is None:
        return ""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _norm_set(values: list[str] | None) -> set[str]:
    return {_norm(v) for v in (values or []) if _norm(v)}


def profile_has_land(land_ownership: bool | str | None) -> bool | None:
    """Return True/False if known, None if unknown."""
    if land_ownership is None:
        return None
    if isinstance(land_ownership, bool):
        return land_ownership
    token = _norm(str(land_ownership))
    if token in LAND_POSITIVE:
        return True
    if token in LAND_NEGATIVE:
        return False
    # Unknown string — treat as uncertain
    return None


def scheme_requires_land(rule_land: Any) -> bool:
    if rule_land is None or rule_land is False:
        return False
    if rule_land is True:
        return True
    token = _norm(str(rule_land))
    if not token:
        return False
    if token in LAND_REQUIRED_TOKENS:
        return True
    if "landholding_required" in token or "cultivable_landholding" in token:
        return True
    # Max-land caps like family_land_not_more_than_2_acres are NOT requirements.
    return False


def scheme_land_is_homeless_style(rule_land: Any) -> bool:
    if rule_land is None:
        return False
    token = _norm(str(rule_land))
    return "landless" in token or "homeless" in token


@dataclass
class RuleResult:
    matched: list[str] = field(default_factory=list)
    unmatched: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    hard_fail: bool = False
    uncertain: bool = False

    def fail(self, rule: str) -> None:
        self.unmatched.append(rule)
        self.hard_fail = True

    def ok(self, rule: str) -> None:
        self.matched.append(rule)

    def miss(self, field_name: str, *, make_uncertain: bool = True) -> None:
        self.missing.append(field_name)
        if make_uncertain:
            self.uncertain = True


def evaluate_scheme(scheme: dict[str, Any], profile: MatchProfile) -> RuleResult:
    rules = scheme.get("eligibility_rules") or {}
    result = RuleResult()

    # --- states ---
    scheme_states = rules.get("states") or []
    if scheme_states:
        profile_state = (profile.state or "Kerala").strip()
        # "India" means national scheme open to all states in seed data.
        allowed = {_norm(s) for s in scheme_states}
        if _norm(profile_state) in allowed or "india" in allowed:
            result.ok("states")
        else:
            result.fail("states")

    # --- age ---
    min_age = rules.get("min_age")
    max_age = rules.get("max_age")
    if min_age is not None or max_age is not None:
        if profile.age is None:
            result.miss("age")
        else:
            age_ok = True
            if min_age is not None and profile.age < int(min_age):
                age_ok = False
                result.fail("min_age")
            elif min_age is not None:
                result.ok("min_age")
            if max_age is not None and profile.age > int(max_age):
                age_ok = False
                result.fail("max_age")
            elif max_age is not None and age_ok:
                result.ok("max_age")

    # --- income ---
    max_annual = rules.get("max_annual_income")
    max_monthly = rules.get("max_monthly_household_income")
    if max_annual is not None:
        if profile.annual_income is None:
            result.miss("annual_income")
        elif float(profile.annual_income) > float(max_annual):
            result.fail("max_annual_income")
        else:
            result.ok("max_annual_income")
    if max_monthly is not None:
        if profile.monthly_household_income is None:
            result.miss("monthly_household_income")
        elif float(profile.monthly_household_income) > float(max_monthly):
            result.fail("max_monthly_household_income")
        else:
            result.ok("max_monthly_household_income")

    # --- disability ---
    disability_required = bool(rules.get("disability_required"))
    min_disability = rules.get("min_disability_percent")
    if disability_required or min_disability is not None:
        has_disability = profile.disability
        if has_disability is None and profile.disability_percent is not None:
            has_disability = float(profile.disability_percent) > 0

        if disability_required:
            if has_disability is None and profile.disability_percent is None:
                result.miss("disability")
            elif has_disability is False or (
                profile.disability_percent is not None and float(profile.disability_percent) <= 0
            ):
                result.fail("disability_required")
            else:
                result.ok("disability_required")

        if min_disability is not None:
            if profile.disability_percent is None:
                result.miss("disability_percent")
            elif float(profile.disability_percent) < float(min_disability):
                result.fail("min_disability_percent")
            else:
                result.ok("min_disability_percent")

    # --- gender ---
    gender_rule = rules.get("gender")
    if gender_rule:
        if not profile.gender:
            result.miss("gender")
        elif _norm(profile.gender) != _norm(gender_rule):
            result.fail("gender")
        else:
            result.ok("gender")

    # --- marital_status ---
    marital_allowed = rules.get("marital_status") or []
    if marital_allowed:
        if not profile.marital_status:
            result.miss("marital_status")
        else:
            profile_ms = _norm(profile.marital_status)
            allowed_norm = [_norm(m) for m in marital_allowed]
            matched_token = None
            for token in allowed_norm:
                if profile_ms == token:
                    matched_token = token
                    break
                # Allow profile "widow" to match token widow; also deserted aliases
                if profile_ms == "deserted" and token.startswith("deserted"):
                    matched_token = token
                    break
                if profile_ms in {"missing_husband", "husband_missing"} and "husband_missing" in token:
                    matched_token = token
                    break

            if matched_token is None:
                result.fail("marital_status")
            elif matched_token == "deserted_7_years_over_50":
                if profile.age is None:
                    result.miss("age")
                elif profile.age < 50:
                    result.fail("deserted_7_years_over_50")
                else:
                    result.ok("marital_status")
                    result.ok("deserted_7_years_over_50")
            else:
                result.ok("marital_status")

    # --- occupations ---
    # Real intersection only. Empty / missing profile occupations must NEVER
    # satisfy a non-empty scheme occupation allowlist (not a wildcard).
    scheme_occs = rules.get("occupations") or []
    if scheme_occs:
        profile_occs = _norm_set(profile.occupations)
        scheme_occs_n = _norm_set(scheme_occs)
        if not profile_occs:
            result.fail("occupations")
        elif profile_occs & scheme_occs_n:
            result.ok("occupations")
        else:
            result.fail("occupations")

    # --- categories ---
    scheme_cats = rules.get("categories") or []
    if scheme_cats:
        scheme_cats_n = _norm_set(scheme_cats)
        profile_cats = _norm_set(profile.categories)
        # Also pull flag-based SECC-style signals into profile categories
        flags = profile.flags or {}
        if flags.get("secc_eligible") or flags.get("secc_deprivation"):
            profile_cats.add("secc_deprivation")
        if flags.get("rsby_chis_2018_19"):
            profile_cats.add("rsby_chis_2018_19")
        if profile.housing_status:
            profile_cats.add(_norm(profile.housing_status))
        if profile.residence_type:
            # urban → urban_household soft alias
            rt = _norm(profile.residence_type)
            profile_cats.add(rt)
            if rt == "urban":
                profile_cats.add("urban_household")

        secc_only = scheme_cats_n <= SECC_STYLE_CATEGORIES or all(
            c in SECC_STYLE_CATEGORIES or c.startswith("secc") for c in scheme_cats_n
        )
        housing_only = bool(scheme_cats_n) and scheme_cats_n <= HOUSING_STYLE_CATEGORIES
        intersection = profile_cats & scheme_cats_n

        # Explicit housing signal for LIFE-style schemes (not land_ownership alone).
        has_housing_signal = bool(
            (profile.housing_status and _norm(profile.housing_status) in HOUSING_STYLE_CATEGORIES)
            or bool(_norm_set(profile.categories) & HOUSING_STYLE_CATEGORIES)
            or bool(intersection & HOUSING_STYLE_CATEGORIES)
        )

        if intersection:
            result.ok("categories")
        elif housing_only and not has_housing_signal:
            # Missing housing_status / housing category → uncertain or soft exclude path;
            # never likely_eligible. Do not treat blank profile as homeless.
            result.miss("housing_status")
            result.uncertain = True
        elif not profile_cats:
            if secc_only:
                # Missing SECC-style categories → uncertain, not auto-match / not hard fail
                result.miss("categories")
                result.uncertain = True
            else:
                result.miss("categories")
        else:
            # Profile has categories but none intersect
            if secc_only:
                result.miss("categories")
                result.uncertain = True
                # Do not hard-fail SECC-only schemes solely on missing SECC flags;
                # mark uncertain instead of not_eligible when no intersection.
            else:
                result.fail("categories")

    # --- land_ownership ---
    rule_land = rules.get("land_ownership")
    if scheme_requires_land(rule_land):
        has_land = profile_has_land(profile.land_ownership)
        if has_land is None:
            result.miss("land_ownership")
        elif has_land is False:
            result.fail("land_ownership_required")
        else:
            result.ok("land_ownership")
    elif scheme_land_is_homeless_style(rule_land):
        # Soft signal — categories usually carry homeless/landless; don't hard fail.
        has_land = profile_has_land(profile.land_ownership)
        if has_land is False:
            result.ok("land_ownership_landless")
        elif has_land is True:
            # Landed but may still be homeless (incomplete house) — leave to categories
            pass

    # --- maternity (from structured eligibility_rules only; seed notes/tags) ---
    if rules.get("maternity_required"):
        pregnant = profile.is_pregnant
        lactating = profile.is_lactating
        child_months = profile.child_age_months
        positive = (
            pregnant is True
            or lactating is True
            or (child_months is not None and int(child_months) >= 0 and int(child_months) <= 6)
        )
        explicit_negative = (
            pregnant is False
            and lactating is not True
            and child_months is None
        )
        all_unknown = pregnant is None and lactating is None and child_months is None
        if positive:
            result.ok("maternity_required")
        elif explicit_negative:
            result.fail("maternity_required")
        elif all_unknown:
            result.miss("is_pregnant")
        else:
            # Partial negatives / unknowns without a positive maternity signal
            if pregnant is False and lactating is False and (
                child_months is None or int(child_months) > 6
            ):
                result.fail("maternity_required")
            else:
                result.miss("is_pregnant")

    # --- NFBS-style breadwinner death (structured flag only) ---
    if rules.get("primary_breadwinner_deceased_required"):
        flag = profile.primary_breadwinner_deceased
        if flag is True:
            result.ok("primary_breadwinner_deceased_required")
        elif flag is False:
            result.fail("primary_breadwinner_deceased_required")
        else:
            result.miss("primary_breadwinner_deceased")

    # --- KAWWF / agri labour tenure (Sevana agricultural labour pension) ---
    if rules.get("kawwf_member_required"):
        flag = profile.kawwf_member
        if flag is True:
            result.ok("kawwf_member_required")
        elif flag is False:
            result.fail("kawwf_member_required")
        else:
            # Notes require KAWWF membership — missing → uncertain, not likely
            result.miss("kawwf_member")

    min_agri_years = rules.get("min_agri_labour_years")
    if min_agri_years is not None:
        years = profile.agri_labour_years
        if years is None:
            result.miss("agri_labour_years")
        elif int(years) < int(min_agri_years):
            result.fail("min_agri_labour_years")
        else:
            result.ok("min_agri_labour_years")

    # --- districts (optional hard filter only when scheme lists districts) ---
    scheme_districts = rules.get("districts") or []
    if scheme_districts:
        if not profile.district:
            result.miss("district")
        else:
            allowed = _norm_set(scheme_districts)
            if _norm(profile.district) in allowed:
                result.ok("districts")
            else:
                result.fail("districts")

    return result


def _score(result: RuleResult) -> float:
    if result.hard_fail:
        return 0.0
    total = len(result.matched) + len(result.unmatched) + len(result.missing)
    if total == 0:
        return 0.5  # no hard rules — weak match / open scheme
    return len(result.matched) / total


def match_schemes(
    schemes: list[dict[str, Any]],
    profile: MatchProfile,
    options: MatchOptions | None = None,
) -> MatchResponse:
    options = options or MatchOptions()
    matched: list[MatchedScheme] = []
    excluded: list[ExcludedScheme] = []
    needs_verification: list[NeedsVerificationItem] = []

    for scheme in schemes:
        rules = scheme.get("eligibility_rules") or {}
        verify = bool(rules.get("verify"))
        verify_notes = rules.get("verify_notes") or ""
        result = evaluate_scheme(scheme, profile)

        if result.hard_fail:
            excluded.append(
                ExcludedScheme(
                    scheme_id=scheme["id"],
                    status="not_eligible",
                    reasons=list(dict.fromkeys(result.unmatched)),
                )
            )
            continue

        # Status determination
        if verify or result.uncertain or result.missing:
            status = "uncertain"
        else:
            status = "likely_eligible"

        if status == "uncertain" and not options.include_verify_uncertain:
            needs_verification.append(
                NeedsVerificationItem(
                    scheme_id=scheme["id"],
                    status="uncertain",
                    verify_notes=verify_notes,
                )
            )
            continue

        explanation = build_explanation(
            scheme=scheme,
            profile=profile,
            matched_rules=result.matched,
            unmatched_rules=result.unmatched,
            missing_fields=result.missing,
            status=status,
        )

        item = MatchedScheme(
            scheme_id=scheme["id"],
            score=round(_score(result), 4),
            status=status,
            matched_rules=list(dict.fromkeys(result.matched)),
            unmatched_rules=list(dict.fromkeys(result.unmatched)),
            missing_profile_fields=list(dict.fromkeys(result.missing)),
            verify=verify,
            verify_notes=verify_notes if verify else "",
            explanation=explanation,
            scheme_name=scheme.get("scheme_name") or {},
            description=scheme.get("description"),
            benefits=scheme.get("benefits"),
            documents=scheme.get("required_documents"),
            how_to_apply=scheme.get("how_to_apply"),
            apply_url=scheme.get("apply_url"),
            official_source_url=scheme.get("official_source_url"),
            last_verified=resolve_last_verified(scheme),
            tags=scheme.get("tags") or [],
        )
        matched.append(item)
        if status == "uncertain" and verify:
            needs_verification.append(
                NeedsVerificationItem(
                    scheme_id=scheme["id"],
                    status="uncertain",
                    verify_notes=verify_notes,
                )
            )

    # Prefer likely_eligible over uncertain when scores tie (better mobile UX).
    matched.sort(
        key=lambda m: (
            0 if m.status == "likely_eligible" else 1,
            -m.score,
            m.scheme_id,
        )
    )
    if options.max_results and len(matched) > options.max_results:
        matched = matched[: options.max_results]

    message = None
    if not matched:
        message = (
            "No schemes matched this profile based on published eligibility rules. "
            "Try adjusting income, occupation, category, or disability fields, "
            "or browse GET /schemes for the full catalogue. Always verify with the "
            "implementing office before applying."
        )

    freshness = catalogue_payload()
    return MatchResponse(
        matched=matched,
        excluded=excluded,
        needs_verification=needs_verification,
        message=message,
        count=len(matched),
        district=profile.district,
        catalogue=freshness["catalogue"],
        is_stale=freshness["is_stale"],
    )
