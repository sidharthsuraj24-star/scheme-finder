#!/usr/bin/env python3
"""US tax + college gap deepen (2026-09-24). Idempotent.

Fill remaining US state gaps: state EITC / homestead / property-tax credit and
state college grant/scholarship where a clear official .gov source exists.
Official .gov only for official_source_url; apply_url may be a state portal.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
PACK = Path(__file__).resolve().parent / "data_packs" / "wave_2026_09_24_us_tax_college_gaps.json"
LAST = "2026-09-24"
ISO = "2026-09-24T14:15:00+05:30"

SKIPS = [
    {
        "id_or_topic": "us-ar-eitc / Arkansas state EITC",
        "reason": "dfa.arkansas.gov EITC page documents federal EITC only; Arkansas has no separate state EITC on IRS state-EITC lists. Added us-ar-homestead-credit instead.",
    },
    {
        "id_or_topic": "nv-* statewide EITC / homestead property-tax credit",
        "reason": "Nevada has no income tax / no state EITC; no clear active statewide senior homestead rebate on tax.nv.gov beyond local exemptions and the automatic primary-residence tax-cap abatement. Honest SKIP.",
    },
    {
        "id_or_topic": "de-seed college",
        "reason": "Delaware SEED already catalogued (de-seed); no duplicate.",
    },
    {
        "id_or_topic": "sd-homestead-exemption deferral",
        "reason": "SD already has sd-tax-refund; added sd-assessment-freeze (distinct). Homestead Exemption deferral exists on dor.sd.gov but overlaps senior relief set — skipped to avoid near-duplicate clutter.",
    },
    {
        "id_or_topic": "co-cof duplicate",
        "reason": "College Opportunity Fund stipend already present (co-cof); added co-student-grant as the clear need-based grant beyond COF.",
    },
]


def _ok_official(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host.endswith(".gov") or host.endswith(".gov.in") or host.endswith(".nic.in"):
        return True
    if ".state." in host and host.endswith(".us"):
        return True
    return False


def main() -> None:
    NEW = json.loads(PACK.read_text())
    assert isinstance(NEW, list) and len(NEW) >= 12, len(NEW)

    for s in NEW:
        assert _ok_official(s["official_source_url"]), (s["id"], s["official_source_url"])
        assert s["last_verified"] == LAST
        assert s["eligibility_rules"]["verify"] is True
        assert s["eligibility_rules"]["max_annual_income"] is None
        assert s["eligibility_rules"]["max_monthly_household_income"] is None
        assert s["eligibility_rules"]["countries"] == ["United States"]
        assert s["eligibility_rules"]["nationwide"] is False
        assert len(s["eligibility_rules"]["states"]) == 1
        sid = s["id"]
        # collision guard vs India AR/LA/GA/IN/MN etc.
        if sid.startswith(("ar-", "la-", "ga-", "in-", "mn-", "tn-")) and not sid.startswith(
            ("us-ar-", "us-la-", "us-ga-", "us-in-", "us-mn-", "us-tn-")
        ):
            raise AssertionError(f"US id collision risk: {sid}")
        for lang in ("en", "hi", "ml"):
            assert s["scheme_name"].get(lang)
            assert s["description"].get(lang)
            assert s["benefits"].get(lang)
            assert s["how_to_apply"].get(lang)
            assert isinstance(s["required_documents"].get(lang), list)

    schemes = json.loads(DATA.read_text())
    existing = {x["id"] for x in schemes}
    before = len(schemes)
    dups = [s["id"] for s in NEW if s["id"] in existing]
    to_add = [s for s in NEW if s["id"] not in existing]
    if dups:
        print(f"skip already-present ids ({len(dups)}): {dups}")

    schemes.extend(to_add)
    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    count = len(schemes)
    wave_note = (
        "Catalogue deepen 2026-09-24 US tax/college gaps: state EITC / homestead / property-tax "
        "relief and need-based or broad merit college grants for remaining thin states — "
        "DC EITC; HI EITC; AR homestead credit; AK senior property exemption; WY property tax refund; "
        "NH LMI homeowners property tax relief; NM Working Families Tax Credit; SD assessment freeze; "
        "AL ASAP; FL Bright Futures (.gov); CO Student Grant (beyond COF); CT Roberta B. Willis; "
        "KS Comprehensive Grant; NE Opportunity Grant; NJ TAG; PA State Grant; ME State Grant; "
        "OK Promise; RI Promise; VT Incentive Grant. Official .gov for official_source_url; "
        "last_verified 2026-09-24; verify:true; no invented eligibility; honest SKIP AR state EITC "
        "(federal-only page), NV statewide EITC/homestead rebate, DE SEED duplicate."
    )
    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = count
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        if "US tax/college gaps" not in scope:
            meta["scope"] = scope.rstrip(".") + "; " + wave_note
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    print(f"before={before} added={len(to_add)} after={count}")
    print("US adds:", [s["id"] for s in to_add])
    print("SKIPS:")
    for sk in SKIPS:
        print(f"  - {sk['id_or_topic']}: {sk['reason']}")


if __name__ == "__main__":
    main()
