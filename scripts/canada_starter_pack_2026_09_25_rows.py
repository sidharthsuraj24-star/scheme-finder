"""Row data for scripts/canada_starter_pack_2026_09_25.py (Canada starter pack).

Every figure comes from the official page in official_source_url (canada.ca — CRA /
ESDC / Service Canada — or an official provincial / territorial government site),
checked 2026-09-25. Amounts are Canadian dollars (C$ / CAD), never USD.
"""
from __future__ import annotations

LAST = "2026-09-25"

AB, BC, MB, NB = "Alberta", "British Columbia", "Manitoba", "New Brunswick"
NL, NT, NS, NU = "Newfoundland and Labrador", "Northwest Territories", "Nova Scotia", "Nunavut"
ON, PE, QC, SK, YT = "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon"
PROVINCES = [AB, BC, MB, NB, NL, NT, NS, NU, ON, PE, QC, SK, YT]
PROV_TAG = {p: p.lower().replace(" ", "_") for p in PROVINCES}
ALL_BUT_QC = [p for p in PROVINCES if p != QC]
ALL_BUT_QC_NT_NU = [p for p in PROVINCES if p not in (QC, NT, NU)]

CRA = "Canada Revenue Agency (CRA)"
ESDC = "Employment and Social Development Canada (ESDC) / Service Canada"
CRA_PROV = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/provincial-territorial-programs/"
CCB_URL = "https://www.canada.ca/en/revenue-agency/services/child-family-benefits/canada-child-benefit-overview.html"

SIN_DOCS = ["Social Insurance Number (SIN)", "Filed income tax and benefit return (both spouses/partners)", "Direct deposit details"]
QC_NOTE_CPP = "Quebec residents are covered by the Québec Pension Plan (Retraite Québec) instead — see can-qc-qpp-retirement."
FILE_TAX = "File your income tax and benefit return every year (both you and your spouse or common-law partner) — CRA then calculates the benefit automatically."


def L(en: str) -> dict:
    return {"en": en, "ml": en, "hi": en}


def docs(items: list[str]) -> dict:
    return {"en": items, "ml": items, "hi": items}


def rules(
    *,
    provinces: list[str] | None,
    notes: str,
    verify_notes: str,
    implies_low_income: bool = False,
    min_age: int | None = None,
    max_age: int | None = None,
    max_annual_income: float | None = None,
    disability_required: bool = False,
    marital_status: list[str] | None = None,
    verify: bool = True,
) -> dict:
    all_canada = not provinces
    for p in provinces or []:
        assert p in PROVINCES, p
    return {
        "min_age": min_age,
        "max_age": max_age,
        "max_annual_income": max_annual_income,
        "max_monthly_household_income": None,
        "occupations": [],
        "categories": [],
        "gender": None,
        "marital_status": list(marital_status or []),
        "disability_required": disability_required,
        "min_disability_percent": None,
        "land_ownership": None,
        "states": [] if all_canada else list(provinces or []),
        "countries": ["Canada"],
        "nationwide": all_canada,
        "notes": notes,
        "verify": verify,
        "verify_notes": verify_notes,
        "implies_low_income": implies_low_income,
    }


def scheme(id, name, desc, benefits, documents, how, apply_url, official, office, tags, erules, *, federal: bool) -> dict:
    assert id.startswith("can-"), id
    tag_list = ["canada"]
    if federal:
        tag_list.append("canada_federal")
    # Province tags only for provincial / territorial rows (federal rows with a
    # province list, e.g. CPP outside Quebec, stay in the canada-federal pack).
    if not federal:
        tag_list += [PROV_TAG[p] for p in erules["states"]]
    for t in tags:
        if t not in tag_list:
            tag_list.append(t)
    assert not ({"central", "nationwide", "federal", "united_states", "california"} & set(tag_list)), id
    return {
        "id": id,
        "scheme_name": L(name),
        "description": L(desc),
        "eligibility_rules": erules,
        "benefits": L(benefits),
        "required_documents": docs(documents),
        "how_to_apply": L(how),
        "apply_url": apply_url,
        "official_source_url": official,
        "last_verified": LAST,
        "office_type": office,
        "tags": tag_list,
    }


ADDS: list[dict] = []


def F(*a, **k):
    ADDS.append(scheme(*a, **k, federal=True))


def P(*a, **k):
    ADDS.append(scheme(*a, **k, federal=False))


ALL_INCOMES = ["universal", "middle-class", "upper-middle-class", "high-income-eligible"]

from canada_starter_pack_2026_09_25_federal import add_federal  # noqa: E402
from canada_starter_pack_2026_09_25_provincial import add_provincial  # noqa: E402

add_federal()
add_provincial()

_ids = [r["id"] for r in ADDS]
assert len(_ids) == len(set(_ids)), "duplicate can- ids"
