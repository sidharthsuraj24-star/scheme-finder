"""Canonical States + Union Territories of India (as of 2026).

28 States + 8 UTs. English names are canonical for matching.
Mirrors frontend/src/lib/indiaRegions.ts
"""

from __future__ import annotations

from typing import Literal, TypedDict

RegionKind = Literal["state", "ut"]


class IndiaRegion(TypedDict, total=False):
    name: str
    kind: RegionKind
    short: str
    code: str


INDIA_REGIONS: list[IndiaRegion] = [
    # --- States (28) ---
    {"name": "Andhra Pradesh", "kind": "state", "code": "IN-AP"},
    {"name": "Arunachal Pradesh", "kind": "state", "code": "IN-AR"},
    {"name": "Assam", "kind": "state", "code": "IN-AS"},
    {"name": "Bihar", "kind": "state", "code": "IN-BR"},
    {"name": "Chhattisgarh", "kind": "state", "code": "IN-CT"},
    {"name": "Goa", "kind": "state", "code": "IN-GA"},
    {"name": "Gujarat", "kind": "state", "code": "IN-GJ"},
    {"name": "Haryana", "kind": "state", "code": "IN-HR"},
    {"name": "Himachal Pradesh", "kind": "state", "code": "IN-HP"},
    {"name": "Jharkhand", "kind": "state", "code": "IN-JH"},
    {"name": "Karnataka", "kind": "state", "code": "IN-KA"},
    {"name": "Kerala", "kind": "state", "short": "കേരളം", "code": "IN-KL"},
    {"name": "Madhya Pradesh", "kind": "state", "code": "IN-MP"},
    {"name": "Maharashtra", "kind": "state", "code": "IN-MH"},
    {"name": "Manipur", "kind": "state", "code": "IN-MN"},
    {"name": "Meghalaya", "kind": "state", "code": "IN-ML"},
    {"name": "Mizoram", "kind": "state", "code": "IN-MZ"},
    {"name": "Nagaland", "kind": "state", "code": "IN-NL"},
    {"name": "Odisha", "kind": "state", "code": "IN-OR"},
    {"name": "Punjab", "kind": "state", "code": "IN-PB"},
    {"name": "Rajasthan", "kind": "state", "code": "IN-RJ"},
    {"name": "Sikkim", "kind": "state", "code": "IN-SK"},
    {"name": "Tamil Nadu", "kind": "state", "code": "IN-TN"},
    {"name": "Telangana", "kind": "state", "code": "IN-TG"},
    {"name": "Tripura", "kind": "state", "code": "IN-TR"},
    {"name": "Uttar Pradesh", "kind": "state", "code": "IN-UP"},
    {"name": "Uttarakhand", "kind": "state", "code": "IN-UT"},
    {"name": "West Bengal", "kind": "state", "code": "IN-WB"},
    # --- Union Territories (8) ---
    {"name": "Andaman and Nicobar Islands", "kind": "ut", "short": "A & N Islands", "code": "IN-AN"},
    {"name": "Chandigarh", "kind": "ut", "code": "IN-CH"},
    {"name": "Dadra and Nagar Haveli and Daman and Diu", "kind": "ut", "short": "DNH & DD", "code": "IN-DH"},
    {"name": "Delhi", "kind": "ut", "short": "NCT of Delhi", "code": "IN-DL"},
    {"name": "Jammu and Kashmir", "kind": "ut", "short": "J&K", "code": "IN-JK"},
    {"name": "Ladakh", "kind": "ut", "code": "IN-LA"},
    {"name": "Lakshadweep", "kind": "ut", "code": "IN-LD"},
    {"name": "Puducherry", "kind": "ut", "code": "IN-PY"},
]

DEFAULT_STATE = "Kerala"

INDIA_REGION_NAMES: list[str] = [r["name"] for r in INDIA_REGIONS]

_NAME_SET = {n.lower() for n in INDIA_REGION_NAMES}


def is_known_india_region(name: str | None) -> bool:
    if not name:
        return False
    return name.strip().lower() in _NAME_SET


def normalize_region_name(name: str | None) -> str | None:
    if not name:
        return None
    trimmed = name.strip()
    for r in INDIA_REGIONS:
        if r["name"].lower() == trimmed.lower():
            return r["name"]
    return None
