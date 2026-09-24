#!/usr/bin/env python3
"""India large-state middle/universal deepen + US Montana/Vermont cleanup (2026-09-24).

Idempotent. Official .gov.in / .gov / PIB / state portals only (plus allowlisted
MUS .edu and India Post). Never invent permanent eligibility ceilings — prefer
verify=true + notes. Syncs data/ + frontend/data/ schemes and catalogue_meta.
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
PACK_DIR = Path(__file__).resolve().parent / "data_packs"
LAST = "2026-09-24"
ISO = "2026-09-24T14:30:00+05:30"

PACK_FILES = [
    "wave_2026_09_24_india_state_middle.json",
    "wave_2026_09_24_us_montana_vt.json",
]

SKIPS = [
    {
        "id_or_topic": "hr-hwdcl-education-loan-interest-subsidy",
        "reason": "HWDCL page is on hwdcl.org (not .gov.in); skipped under official-domain rule this wave.",
    },
    {
        "id_or_topic": "pb-* distinctive middle-class property-tax / education-loan state top-up",
        "reason": "No high-confidence statewide .gov.in middle/universal programme verified beyond existing pb-* rows; Chandigarh MC rebate is UT-scoped.",
    },
    {
        "id_or_topic": "in-section-54 / in-section-54f",
        "reason": "Prior wave SKIP retained — complex regime-dependent capital-gains housing relief; do not invent numeric limits.",
    },
    {
        "id_or_topic": "farm-pump / pure BPL pension clones / infrastructure-only",
        "reason": "Out of scope for middle/universal deepen.",
    },
    {
        "id_or_topic": "ka-udyogini / hr-medhavi-chhattar",
        "reason": "Udyogini / Medhavi Chhattar are EWS/SC-BC gated; not middle/universal distinctive adds.",
    },
]


def _ok_host(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host.endswith(".gov") or host.endswith(".gov.in") or host.endswith(".nic.in"):
        return True
    if ".state." in host and host.endswith(".us"):
        return True
    allow = (
        "mus.edu",
        "scholarships.mus.edu",
        "indiapost.gov.in",  # covered by .gov.in
        "upneda.org.in",
        "mahadiscom.in",
        "schev.edu",
        "ushe.edu",
        "hawaii.edu",
        "nshe.nevada.edu",
        "communitycolleges.wy.edu",
        "wvhepc.edu",
        "cfnc.org",
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
    assert len(NEW) >= 15, len(NEW)
    for s in NEW:
        assert _ok_host(s["official_source_url"]), (s["id"], s["official_source_url"])
        assert _ok_host(s["apply_url"]), (s["id"], s["apply_url"])
        assert s["last_verified"] == LAST
        er = s["eligibility_rules"]
        assert er["verify"] is True
        assert er["max_monthly_household_income"] is None
        country = er["countries"][0]
        if country == "United States":
            assert er["nationwide"] is False
            assert len(er["states"]) == 1
            # collision guard
            sid = s["id"]
            if sid.startswith(("ga-", "tn-")) and not sid.startswith(("us-ga-", "us-tn-", "mt-", "vt-")):
                # India ga-/tn- are fine; US Georgia/Tennessee must stay us-ga-/us-tn-
                pass
            if sid.startswith(("la-", "mn-", "ar-")) and not sid.startswith(("us-la-", "us-mn-", "us-ar-")):
                raise AssertionError(f"US id collision risk: {sid}")
            if er.get("implies_low_income") is True and sid.startswith("mt-homestead"):
                raise AssertionError("homestead must not imply low income")
        else:
            if er.get("implies_low_income") is True:
                # only allowed for clearly income-capped student aid
                assert s["id"] in {"od-kalinga-sikhya-sathi"}, s["id"]
            if s["id"].startswith(("in-", "dl-", "ka-", "tn-", "mh-", "up-", "tg-", "ap-")) and er.get(
                "implies_low_income"
            ):
                if s["id"] != "od-kalinga-sikhya-sathi" and er.get("implies_low_income") is True:
                    # middle/universal rows must not imply low income
                    if s["id"].startswith(("in-", "dl-", "ka-", "tn-", "mh-", "up-", "tg-", "ap-")):
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
        "Catalogue deepen 2026-09-24 India large-state middle/universal + US Montana/Vermont cleanup: "
        "Bihar & West Bengal Student Credit Cards; Odisha Kalinga Sikhya Sathi; BBMP/GCC/GHMC/AP municipal "
        "property-tax early rebates; Maharashtra EV Policy 2025 incentives; UP rooftop-solar state top-up; "
        "MP MMVY merit support; Delhi EV road-tax exemption; Rajasthan Rajiv Gandhi Scholarship for Academic "
        "Excellence; India Post Time Deposit & Recurring Deposit; Montana Homestead Reduced Rate + MUS Honor "
        "Scholarship; Vermont Property Tax Credit. Official .gov/.gov.in/.nic.in (MUS .edu for Honor Scholarship); "
        f"last_verified {LAST}; no invented eligibility; honest SKIPs for HWDCL non-.gov.in, thin Punjab extras, "
        "IT §§54/54F, BPL/farm-pump clones."
    )
    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = count
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        marker = "India large-state middle/universal + US Montana/Vermont"
        if marker not in scope:
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
