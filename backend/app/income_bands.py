"""India household income-band classification (PRICE ICE 360°).

Source of truth (NOT a Government of India statutory definition):
PRICE ICE 360° / "The Rise of India's Middle Class" — 2020–21 prices.
Primary PDF: https://www.price360.in/Executive_Summary_Middle_Class.pdf

₹15 lakh is the Seekers → Strivers cut (Strivers are ₹15–30 lakh annual).
These bands are for UX labels and soft ranking only — NEVER invent scheme
eligibility ceilings (max_annual_income) from PRICE bands.
"""

from __future__ import annotations

from typing import Any, TypedDict

# Short citation for API / UI.
INCOME_BAND_SOURCE = "PRICE ICE 360° (2020–21 prices; not official GoI)"

INCOME_BAND_NOTE = (
    "Household income bands from PRICE ICE 360° / The Rise of India's Middle Class "
    "(2020–21 prices). Not a Government of India statutory classification. "
    "Used for UX labels and soft ranking only — does not change scheme eligibility rules. "
    "₹15 lakh is the Seekers→Strivers boundary (Strivers: ₹15–30 lakh)."
)

# (min_inclusive, max_inclusive_or_None, band_id, band_label)
# Upper bound None means open-ended (≥).
_BANDS: list[tuple[float, float | None, str, str]] = [
    (0, 124_999, "destitute", "Destitute"),
    (125_000, 499_999, "aspirer", "Aspirer"),
    (500_000, 1_499_999, "seeker", "Middle class (Seekers)"),
    (1_500_000, 2_999_999, "striver", "Upper middle class (Strivers)"),
    (3_000_000, 4_999_999, "near_rich", "Near rich"),
    (5_000_000, 9_999_999, "clear_rich", "Clear rich"),
    (10_000_000, 19_999_999, "sheer_rich", "Sheer rich"),
    (20_000_000, None, "super_rich", "Super rich"),
]

# Coarser income_class: destitute | aspirer | middle_class (seeker+striver) | rich (≥30L)
_BAND_TO_CLASS: dict[str, str] = {
    "destitute": "destitute",
    "aspirer": "aspirer",
    "seeker": "middle_class",
    "striver": "middle_class",
    "near_rich": "rich",
    "clear_rich": "rich",
    "sheer_rich": "rich",
    "super_rich": "rich",
}

# Human-readable range hints for UI (lakh-style).
BAND_RANGE_HINT: dict[str, str] = {
    "destitute": "under ₹1.25 lakh",
    "aspirer": "₹1.25–5 lakh",
    "seeker": "₹5–15 lakh",
    "striver": "₹15–30 lakh",
    "near_rich": "₹30–50 lakh",
    "clear_rich": "₹50 lakh–1 crore",
    "sheer_rich": "₹1–2 crore",
    "super_rich": "₹2 crore+",
}


class IncomeBandResult(TypedDict):
    band_id: str | None
    band_label: str | None
    income_class: str | None
    source: str | None
    note: str | None


def _norm_country(country: str | None) -> str:
    if not country:
        return "india"
    return str(country).strip().lower().replace("-", "_").replace(" ", "_")


def is_india_country(country: str | None) -> bool:
    return _norm_country(country or "India") in {"india"}


def classify_india_annual_income(
    annual: float | None,
    *,
    country: str | None = "India",
) -> IncomeBandResult:
    """Classify annual household income into PRICE ICE 360° bands.

    Returns null band fields when annual is None, or when country is not India
    (US / other stubs deferred — skip non-India bands this PR).
    """
    empty: IncomeBandResult = {
        "band_id": None,
        "band_label": None,
        "income_class": None,
        "source": None,
        "note": None,
    }
    if not is_india_country(country):
        return empty
    if annual is None:
        return empty
    try:
        value = float(annual)
    except (TypeError, ValueError):
        return empty
    if value < 0:
        return empty

    for lo, hi, band_id, band_label in _BANDS:
        if value < lo:
            continue
        if hi is None or value <= hi:
            return {
                "band_id": band_id,
                "band_label": band_label,
                "income_class": _BAND_TO_CLASS[band_id],
                "source": INCOME_BAND_SOURCE,
                "note": INCOME_BAND_NOTE,
            }
    # Fallback (should not hit — super_rich is open-ended)
    return {
        "band_id": "super_rich",
        "band_label": "Super rich",
        "income_class": "rich",
        "source": INCOME_BAND_SOURCE,
        "note": INCOME_BAND_NOTE,
    }


def format_band_sentence(band: IncomeBandResult | dict[str, Any]) -> str | None:
    """One plain UX sentence; None if band unknown."""
    band_id = band.get("band_id")
    band_label = band.get("band_label")
    if not band_id or not band_label:
        return None
    hint = BAND_RANGE_HINT.get(str(band_id), "")
    range_part = f" ({hint})" if hint else ""
    return (
        f"Based on PRICE ICE 360 household bands (2020–21 prices): "
        f"{band_label}{range_part}. "
        f"Not an official government classification — does not change scheme rules; "
        f"only helps sort and explain results."
    )


# ---------------------------------------------------------------------------
# Soft ranking boosts (deterministic; secondary to hard eligibility)
# ---------------------------------------------------------------------------

# For seeker / striver / *_rich India profiles: modest bump for middle/tax/savings tags.
# Take the MAX of matching tag boosts, then cap at MIDDLE_HIGH_BOOST_CAP.
MIDDLE_HIGH_BOOST_TAGS: dict[str, float] = {
    "upper-middle-class": 0.10,
    "high-income-eligible": 0.10,
    "middle-class": 0.08,
    "tax": 0.06,
    "savings": 0.06,
    "universal": 0.05,
}
MIDDLE_HIGH_BOOST_CAP = 0.12
MIDDLE_HIGH_BANDS = frozenset(
    {"seeker", "striver", "near_rich", "clear_rich", "sheer_rich", "super_rich"}
)

# For destitute / aspirer: tiny optional boost for welfare / implies_low schemes.
LOW_INCOME_BOOST_TAGS: dict[str, float] = {
    "welfare": 0.04,
    "bpl": 0.04,
    "pension": 0.03,
}
LOW_INCOME_IMPLIES_BOOST = 0.04
LOW_INCOME_BOOST_CAP = 0.05
LOW_INCOME_BANDS = frozenset({"destitute", "aspirer"})


def income_band_score_boost(
    band_id: str | None,
    tags: list[str] | None,
    *,
    implies_low_income: bool = False,
) -> float:
    """Return a small deterministic score bump for ranking (0 if none).

    Does NOT change hard gates (max_annual_income, implies_low_income exclude).
    Applied after base eligibility score; sort still prefers likely_eligible first.
    """
    if not band_id:
        return 0.0
    tag_set = {str(t).strip().lower() for t in (tags or []) if t}

    if band_id in MIDDLE_HIGH_BANDS:
        bump = 0.0
        for tag, amount in MIDDLE_HIGH_BOOST_TAGS.items():
            if tag in tag_set:
                bump = max(bump, amount)
        return min(bump, MIDDLE_HIGH_BOOST_CAP)

    if band_id in LOW_INCOME_BANDS:
        bump = 0.0
        for tag, amount in LOW_INCOME_BOOST_TAGS.items():
            if tag in tag_set:
                bump = max(bump, amount)
        if implies_low_income:
            bump = max(bump, LOW_INCOME_IMPLIES_BOOST)
        return min(bump, LOW_INCOME_BOOST_CAP)

    return 0.0
