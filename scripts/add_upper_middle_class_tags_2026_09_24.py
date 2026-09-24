#!/usr/bin/env python3
"""Add upper-middle-class tag alongside middle-class on clear India tax/savings/universal rows.

Idempotent. Does NOT invent new schemes or eligibility ceilings.
Only tags schemes that already have middle-class and are India tax/savings/universal
targets called out in the income-band PR (PPF, NSC, 80C, 24b, 80D, KVP, MIS, TD, RD, etc.).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"

# Explicit India scheme ids that already carry middle-class and are tax/savings/universal.
TARGET_IDS = {
    "in-ppf",
    "in-nsc",
    "in-scss",
    "in-section-80c-deductions",
    "in-section-24b-home-loan-interest",
    "in-section-80d",
    "in-section-80e",
    "in-section-80g",
    "in-section-80eea",
    "in-kvp",
    "in-post-office-mis",
    "in-post-office-time-deposit",
    "in-post-office-recurring-deposit",
    "in-nps-all-citizen",
    "in-nps-tier-ii",
    "in-sukanya-samriddhi",
    "in-mahila-samman-savings-certificate",
}

TAG = "upper-middle-class"


def main() -> None:
    schemes = json.loads(DATA.read_text())
    by_id = {s["id"]: s for s in schemes}
    touched = []
    for sid in sorted(TARGET_IDS):
        s = by_id.get(sid)
        if not s:
            print(f"SKIP missing {sid}")
            continue
        tags = list(s.get("tags") or [])
        if "middle-class" not in tags:
            print(f"SKIP no middle-class: {sid}")
            continue
        if TAG in tags:
            print(f"OK already: {sid}")
            continue
        # Insert after middle-class for readability
        idx = tags.index("middle-class") + 1
        tags.insert(idx, TAG)
        s["tags"] = tags
        touched.append(sid)
        print(f"TAGGED {sid}")

    if not touched:
        print("No changes.")
        return

    DATA.write_text(json.dumps(schemes, ensure_ascii=False, indent=2) + "\n")
    FE_DATA.write_text(DATA.read_text())

    # Bump catalogue_meta note
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    iso = now.strftime("%Y-%m-%dT%H:%M:%S+05:30")
    day = now.strftime("%Y-%m-%d")
    note = (
        f" Catalogue tag pass {day}: add `{TAG}` alongside existing `middle-class` on "
        f"India tax/savings/universal rows ({', '.join(touched)}) for PRICE ICE 360° "
        f"seeker/striver soft ranking. No new schemes; no invented max_annual_income."
    )
    for meta_path in (META, FE_META):
        meta = json.loads(meta_path.read_text())
        meta["updated_as_of"] = day
        meta["updated_as_of_iso"] = iso
        meta["scheme_count"] = len(schemes)
        scope = meta.get("scope") or ""
        if TAG not in scope:
            meta["scope"] = scope.rstrip() + note
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

    print(f"Tagged {len(touched)} schemes; meta bumped to {iso}")


if __name__ == "__main__":
    main()
