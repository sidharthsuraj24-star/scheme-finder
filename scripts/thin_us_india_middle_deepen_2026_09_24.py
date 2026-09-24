#!/usr/bin/env python3
"""Apply thin-US + India middle-band deepen packs (2026-09-24). Idempotent."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
PACK_DIR = Path(__file__).resolve().parent / "data_packs"
LAST = "2026-09-24"
ISO = "2026-09-24T13:45:00+05:30"

SKIPS = [
    {
        "id_or_topic": "nc-eitc / NC S211 Earned Income Tax Credit",
        "reason": "ncleg.gov BillLookUp/2025/S211 last action 2025-03-03 Ref To Com On Rules — not enacted.",
    },
    {
        "id_or_topic": "in-section-54 / in-section-54f capital-gains housing relief",
        "reason": "Official IT pages exist but ceilings/conditions are complex and regime-dependent; SKIP rather than invent numeric limits.",
    },
    {
        "id_or_topic": "mt-* additional distinctive beyond mt-eitc",
        "reason": "No clear statewide Promise/college-grant .gov path verified this wave beyond existing EITC; quality over forced count.",
    },
    {
        "id_or_topic": "ka-/mh- extra middle-band beyond existing packs",
        "reason": "mh-mahadbt-scholarships already listed; additional KA/MH middle paths not cleanly verified without duplicate risk.",
    },
]

PACK_FILES = [
    "wave_2026_09_24_part_us_a.json",
    "wave_2026_09_24_part_us_b.json",
    "wave_2026_09_24_part_us_c.json",
    "wave_2026_09_24_part_india.json",
]


def _ok_host(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host.endswith(".gov") or host.endswith(".gov.in") or host.endswith(".nic.in"):
        return True
    # State government portals on .state.*.us (e.g. revenue.state.mn.us)
    if ".state." in host and host.endswith(".us"):
        return True
    allow = (
        "schev.edu",
        "ushe.edu",
        "hawaii.edu",
        "nshe.nevada.edu",
        "communitycolleges.wy.edu",
        "wvhepc.edu",
        "cfnc.org",
        "ohe.mn.gov",  # also covered by .gov
    )
    return any(host == e or host.endswith("." + e) for e in allow)


def load_new() -> list[dict]:
    out: list[dict] = []
    for name in PACK_FILES:
        path = PACK_DIR / name
        chunk = json.loads(path.read_text())
        assert isinstance(chunk, list), name
        out.extend(chunk)
    return out


def main() -> None:
    NEW = load_new()
    assert len(NEW) >= 20, len(NEW)
    for s in NEW:
        assert _ok_host(s["official_source_url"]), (s["id"], s["official_source_url"])
        assert _ok_host(s["apply_url"]), (s["id"], s["apply_url"])
        assert s["last_verified"] == LAST
        assert s["eligibility_rules"]["verify"] is True
        assert s["eligibility_rules"]["max_monthly_household_income"] is None
        country = s["eligibility_rules"]["countries"][0]
        if country == "United States":
            assert s["eligibility_rules"]["nationwide"] is False
            assert len(s["eligibility_rules"]["states"]) == 1
            assert s["eligibility_rules"]["max_annual_income"] is None
            # collision guard: US rows must not use bare la-/mn-/ar- that collide with India
            sid = s["id"]
            if sid.startswith(("la-", "mn-", "ar-")) and not sid.startswith(("us-la-", "us-mn-", "us-ar-")):
                raise AssertionError(f"US id collision risk: {sid}")
        else:
            if s["id"] != "gj-education-loan-interest-subsidy":
                assert s["eligibility_rules"]["max_annual_income"] is None
            if s["id"].startswith(("in-", "dl-")) and s["eligibility_rules"].get("implies_low_income"):
                raise AssertionError(f"implies_low_income unexpected on {s['id']}")

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
        "Catalogue deepen 2026-09-24 thin-US + India middle-band: "
        "Minnesota (Working Family Credit, Homestead Credit Refund, State Grant) and Louisiana "
        "(state EITC, TOPS, Homestead Exemption) distinctive packs (us-mn-*/us-la-*); thin-state "
        "college/tax/universal adds for NC/VA/AZ/MO/WI/KY/UT/NV/AR/MS/NM/ID/HI/DE/ND/AK/WY/WV; "
        "India middle/universal — KVP, Post Office MIS, §§80D/80E/80G, Mahila Samman Savings Certificate, "
        "Delhi MCD property-tax rebate, Gujarat education-loan interest subsidy. "
        "Official .gov/.gov.in/.nic.in (and state HE .edu / CFNC apply host where that is the program page); "
        "last_verified 2026-09-24; no invented eligibility; honest SKIP NC EITC (S211 not enacted), "
        "IT §§54/54F, thin MT extra, some KA/MH duplicates."
    )
    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = count
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        if "thin-US + India middle-band" not in scope:
            meta["scope"] = scope.rstrip(".") + "; " + wave_note
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    us_ids = [s["id"] for s in to_add if s["eligibility_rules"]["countries"] == ["United States"]]
    in_ids = [s["id"] for s in to_add if s["eligibility_rules"]["countries"] == ["India"]]
    print(f"before={before} added={len(to_add)} after={count}")
    print("US adds:", us_ids)
    print("India adds:", in_ids)
    print("SKIPS:")
    for sk in SKIPS:
        print(f"  - {sk['id_or_topic']}: {sk['reason']}")


if __name__ == "__main__":
    main()
