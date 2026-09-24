#!/usr/bin/env python3
"""India mid-band fill for thin-tag states/UTs (2026-09-24).

Idempotent. Adds middle-class / universal citizen programmes (EV road-tax,
municipal property-tax interest waiver) for priority states/UTs that still had
~0 mid-band tags despite 5–11 total rows. Official .gov.in / .nic.in / BEE only.
Never invent eligibility ceilings — verify=true + notes. Syncs data/ +
frontend/data/ schemes and catalogue_meta. Optional light tag patches on
existing Assam middle-ish rows.
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
PACK = Path(__file__).resolve().parent / "data_packs" / "wave_2026_09_24_india_midband_thin_states.json"
LAST = "2026-09-24"
ISO = "2026-09-24T16:45:00+05:30"

SKIPS = [
    {
        "id_or_topic": "hr-hwdcl-education-loan-interest-subsidy",
        "reason": "Prior SKIP retained — HWDCL host is not .gov.in.",
    },
    {
        "id_or_topic": "hp-medha-protsahan",
        "reason": "Family-income cap around ₹2.5 lakh / BPL-adjacent coaching aid — not middle/universal distinctive this wave.",
    },
    {
        "id_or_topic": "jk-mission-youth-super-75",
        "reason": "Mission Youth Super 75 framed for underprivileged/meritorious segments — not clearly middle/universal; skipped.",
    },
    {
        "id_or_topic": "mz-*/nl-*/sk-*/an-*/ld-* distinctive middle EV or property-tax",
        "reason": "No high-confidence statewide/UT .gov.in middle/universal programme verified beyond existing welfare rows; quality over forced count.",
    },
    {
        "id_or_topic": "py-* distinctive UT middle property-tax / EV",
        "reason": "Puducherry EV policy remains draft-class in public materials; no clear UT-wide early property-tax rebate verified on .gov.in this wave.",
    },
    {
        "id_or_topic": "farm-pump / BPL pension clones / category-only duplicates",
        "reason": "Out of scope for mid-band fill.",
    },
]

TAG_PATCHES = [
    {
        "id": "as-nijut-moina",
        "add_tags": ["middle-class", "universal", "scholarship"],
        "reason": "Official Higher Education guideline: girl students domiciled in Assam irrespective of economic status — mid/universal tags were missing.",
    },
    {
        "id": "as-atal-amrit-abhiyan",
        "add_tags": ["middle-class", "health"],
        "reason": "APL enrolment path up to ₹5 lakh family income — middle-band health cover; tag was missing.",
    },
]


def _ok_host(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False
    if host.endswith(".gov") or host.endswith(".gov.in") or host.endswith(".nic.in"):
        return True
    allow = ("beeindia.gov.in",)  # covered by .gov.in
    return any(host == e or host.endswith("." + e) for e in allow)


def main() -> None:
    NEW = json.loads(PACK.read_text())
    assert isinstance(NEW, list) and len(NEW) >= 10, len(NEW)

    for s in NEW:
        assert _ok_host(s["official_source_url"]), (s["id"], s["official_source_url"])
        assert _ok_host(s["apply_url"]), (s["id"], s["apply_url"])
        assert s["last_verified"] == LAST
        er = s["eligibility_rules"]
        assert er["verify"] is True
        assert er["max_monthly_household_income"] is None
        assert er["max_annual_income"] is None
        assert er.get("implies_low_income") is not True
        assert er["countries"] == ["India"]
        assert er["nationwide"] is False
        assert len(er["states"]) == 1
        assert s["id"].startswith(
            ("hr-", "uk-", "hp-", "jh-", "mn-", "tr-", "as-", "ch-", "la-")
        ), s["id"]
        # collision guards
        if s["id"].startswith("uk-"):
            assert er["states"] == ["Uttarakhand"], s["id"]
        if s["id"].startswith("la-"):
            assert er["states"] == ["Ladakh"], s["id"]
        if s["id"].startswith("ch-"):
            assert er["states"] == ["Chandigarh"], s["id"]
        if s["id"].startswith("mn-"):
            assert er["states"] == ["Manipur"], s["id"]

    schemes = json.loads(DATA.read_text())
    by_id = {x["id"]: x for x in schemes}
    before = len(schemes)

    dups = [s["id"] for s in NEW if s["id"] in by_id]
    to_add = [s for s in NEW if s["id"] not in by_id]
    if dups:
        print(f"skip already-present ids ({len(dups)}): {dups}")

    schemes.extend(to_add)

    patched = []
    for patch in TAG_PATCHES:
        row = next((x for x in schemes if x["id"] == patch["id"]), None)
        if not row:
            print(f"tag-patch skip missing id: {patch['id']}")
            continue
        tags = list(row.get("tags") or [])
        added = []
        for t in patch["add_tags"]:
            if t not in tags:
                tags.append(t)
                added.append(t)
        if added:
            row["tags"] = tags
            row["last_verified"] = LAST
            patched.append((patch["id"], added, patch["reason"]))

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    count = len(schemes)
    wave_note = (
        "Catalogue deepen 2026-09-24 India mid-band fill for thin-tag states/UTs: "
        "Haryana EV MV-tax exemption + ULB property-tax interest waiver; Assam/Jharkhand/"
        "Chandigarh/Ladakh/Tripura/Manipur/Uttarakhand/Himachal Pradesh EV road-tax or "
        "registration/token-tax pathways; light tag patches on Assam Nijut Moina + Atal Amrit. "
        f"Official .gov.in/.nic.in (BEE Haryana.pdf); last_verified {LAST}; no invented "
        "eligibility; honest SKIPs for HWDCL, HP Medha Protsahan, JK Super 75, thin "
        "MZ/NL/SK/AN/LD/PY extras, BPL/farm-pump clones."
    )
    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = count
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        marker = "India mid-band fill for thin-tag states/UTs"
        if marker not in scope:
            meta["scope"] = scope.rstrip(".") + "; " + wave_note
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    print(f"before={before} added={len(to_add)} after={count}")
    print("India adds:", [s["id"] for s in to_add])
    print("Tag patches:")
    for pid, added, reason in patched:
        print(f"  - {pid}: +{added} ({reason})")
    print("SKIPS:")
    for sk in SKIPS:
        print(f"  - {sk['id_or_topic']}: {sk['reason']}")


if __name__ == "__main__":
    main()
