"""Template explanations from matched rules. Optional LLM stub (never decides eligibility)."""

from __future__ import annotations

import os
from typing import Any

from .models import LocalizedText, MatchProfile


DISCLAIMER_EN = (
    "Based on published eligibility rules only; confirm with the implementing office. "
    "Not legal advice."
)
DISCLAIMER_ML = (
    "പ്രസിദ്ധീകരിച്ച യോഗ്യതാ നിബന്ധനകളെ അടിസ്ഥാനമാക്കി മാത്രം; "
    "നടപ്പാക്കുന്ന ഓഫീസുമായി സ്ഥിരീകരിക്കുക. നിയമ ഉപദേശമല്ല."
)


def _fmt_income(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"Rs.{int(value):,}"


def _rule_phrase_en(
    rule: str,
    scheme: dict[str, Any],
    profile: MatchProfile,
) -> str:
    rules = scheme.get("eligibility_rules") or {}
    if rule == "min_age":
        return f"age {profile.age} meets minimum age {rules.get('min_age')}"
    if rule == "max_age":
        return f"age {profile.age} within maximum age {rules.get('max_age')}"
    if rule == "max_annual_income":
        return (
            f"annual income {_fmt_income(profile.annual_income)} "
            f"within cap {_fmt_income(rules.get('max_annual_income'))}"
        )
    if rule == "max_monthly_household_income":
        return (
            f"monthly household income {_fmt_income(profile.monthly_household_income)} "
            f"within cap {_fmt_income(rules.get('max_monthly_household_income'))}"
        )
    if rule == "gender":
        return f"gender '{profile.gender}' matches required '{rules.get('gender')}'"
    if rule == "marital_status":
        return f"marital status '{profile.marital_status}' is in allowed list"
    if rule == "deserted_7_years_over_50":
        return f"deserted case with age {profile.age} (≥50 required)"
    if rule == "disability_required":
        return "disability requirement satisfied"
    if rule == "min_disability_percent":
        return (
            f"disability {profile.disability_percent}% meets minimum "
            f"{rules.get('min_disability_percent')}%"
        )
    if rule == "occupations":
        return "occupation intersects scheme occupation list"
    if rule == "categories":
        return "category intersects scheme category list"
    if rule == "states":
        return f"state '{profile.state or 'Kerala'}' is in scheme states"
    if rule == "land_ownership":
        return "land ownership requirement satisfied"
    if rule == "land_ownership_landless":
        return "profile indicates landless / no ownership"
    return rule.replace("_", " ")


def _rule_phrase_ml(
    rule: str,
    scheme: dict[str, Any],
    profile: MatchProfile,
) -> str:
    # Concise ML mirrors; native review pending for production.
    rules = scheme.get("eligibility_rules") or {}
    if rule == "min_age":
        return f"പ്രായം {profile.age} ഏറ്റവും കുറഞ്ഞ പ്രായം {rules.get('min_age')} നിറവേറ്റുന്നു"
    if rule == "max_annual_income":
        return (
            f"വാർഷിക വരുമാനം {_fmt_income(profile.annual_income)} "
            f"പരിധി {_fmt_income(rules.get('max_annual_income'))} യിൽ ഉൾപ്പെടുന്നു"
        )
    if rule == "max_monthly_household_income":
        return (
            f"മാസ വരുമാനം {_fmt_income(profile.monthly_household_income)} "
            f"പരിധിക്കുള്ളിൽ"
        )
    if rule == "gender":
        return f"ലിംഗം '{profile.gender}' യോജിക്കുന്നു"
    if rule == "marital_status":
        return f"വൈവാഹിക നില '{profile.marital_status}' അനുവദനീയമാണ്"
    if rule == "disability_required":
        return "ഭിന്നശേഷി നിബന്ധന നിറവേറ്റുന്നു"
    if rule == "min_disability_percent":
        return (
            f"ഭിന്നശേഷി {profile.disability_percent}% "
            f"കുറഞ്ഞത് {rules.get('min_disability_percent')}% നിറവേറ്റുന്നു"
        )
    if rule == "occupations":
        return "തൊഴിൽ പട്ടികയുമായി യോജിക്കുന്നു"
    if rule == "categories":
        return "വിഭാഗം പട്ടികയുമായി യോജിക്കുന്നു"
    if rule == "states":
        return f"സംസ്ഥാനം '{profile.state or 'Kerala'}' യോജിക്കുന്നു"
    if rule == "land_ownership":
        return "ഭൂമി ഉടമസ്ഥത നിബന്ധന നിറവേറ്റുന്നു"
    return rule.replace("_", " ") + " [ML]"


def template_explanation(
    *,
    scheme: dict[str, Any],
    profile: MatchProfile,
    matched_rules: list[str],
    unmatched_rules: list[str],
    missing_fields: list[str],
    status: str,
) -> LocalizedText:
    name_en = (scheme.get("scheme_name") or {}).get("en") or scheme.get("id", "scheme")
    name_ml = (scheme.get("scheme_name") or {}).get("ml") or name_en

    if matched_rules:
        parts_en = [_rule_phrase_en(r, scheme, profile) for r in matched_rules]
        parts_ml = [_rule_phrase_ml(r, scheme, profile) for r in matched_rules]
        body_en = "; ".join(parts_en) + "."
        body_ml = "; ".join(parts_ml) + "."
    else:
        body_en = "No structured hard-filter fields constrained this match."
        body_ml = "ഘടനാപരമായ കഠിന ഫിൽട്ടറുകൾ ഈ പൊരുത്തത്തെ നിയന്ത്രിച്ചില്ല."

    if status == "uncertain":
        prefix_en = f"Possibly relevant for {name_en} (needs verification). "
        prefix_ml = f"{name_ml} — സ്ഥിരീകരണം ആവശ്യം. "
    else:
        prefix_en = f"Likely eligible for {name_en}: "
        prefix_ml = f"{name_ml} യ്ക്ക് യോഗ്യതയുണ്ടാകാം: "

    extra_en = ""
    extra_ml = ""
    if missing_fields:
        extra_en += f" Missing profile fields: {', '.join(missing_fields)}."
        extra_ml += f" കുറവുള്ള ഫീൽഡുകൾ: {', '.join(missing_fields)}."
    if unmatched_rules:
        extra_en += f" Unmatched: {', '.join(unmatched_rules)}."
    verify = bool((scheme.get("eligibility_rules") or {}).get("verify"))
    if verify:
        notes = (scheme.get("eligibility_rules") or {}).get("verify_notes") or ""
        extra_en += " Official rules marked verify=true"
        if notes:
            extra_en += f" ({notes[:180]}{'…' if len(notes) > 180 else ''})"
        extra_en += "."
        extra_ml += " ഔദ്യോഗിക നിബന്ധനകൾ verify=true ആയി അടയാളപ്പെടുത്തിയിരിക്കുന്നു."

    en = prefix_en + body_en + extra_en + " " + DISCLAIMER_EN
    ml = prefix_ml + body_ml + extra_ml + " " + DISCLAIMER_ML
    return LocalizedText(en=en.strip(), ml=ml.strip())


def llm_explanation_stub(
    *,
    scheme: dict[str, Any],
    profile: MatchProfile,
    matched_rules: list[str],
    status: str,
) -> LocalizedText | None:
    """Optional LLM polish. Never called for eligibility decisions.

    Returns None when LLM_API_KEY is unset or call is unavailable — caller
    falls back to templates.
    """
    api_key = os.environ.get("LLM_API_KEY", "").strip()
    if not api_key:
        return None
    # Stub: do not invent thresholds; only rephrase matched_rules.
    # Real provider wiring is deferred; keep deterministic templates as source of truth.
    base = template_explanation(
        scheme=scheme,
        profile=profile,
        matched_rules=matched_rules,
        unmatched_rules=[],
        missing_fields=[],
        status=status,
    )
    base.en = "[LLM stub] " + base.en
    base.ml = "[LLM stub] " + base.ml
    return base


def build_explanation(
    *,
    scheme: dict[str, Any],
    profile: MatchProfile,
    matched_rules: list[str],
    unmatched_rules: list[str],
    missing_fields: list[str],
    status: str,
) -> LocalizedText:
    llm = llm_explanation_stub(
        scheme=scheme,
        profile=profile,
        matched_rules=matched_rules,
        status=status,
    )
    if llm is not None:
        return llm
    return template_explanation(
        scheme=scheme,
        profile=profile,
        matched_rules=matched_rules,
        unmatched_rules=unmatched_rules,
        missing_fields=missing_fields,
        status=status,
    )


def generator_mode() -> str:
    return "llm" if os.environ.get("LLM_API_KEY", "").strip() else "template"
