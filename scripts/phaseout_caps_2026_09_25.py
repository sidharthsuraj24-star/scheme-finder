#!/usr/bin/env python3
"""Encode official zero-points for gradual phase-out benefits (2026-09-25).

Production smoke found a C$250k Ontario family still seeing the Ontario Child Benefit
(uncapped). This sets ``max_annual_income`` on phase-out benefits to the income at which
the benefit reaches zero for a generous but realistic family (4 children, or the largest
size the official page tabulates), using only official formulas (CRA, provincial pages and
statutes, GOV.UK / gov.wales). The basis is appended to notes; verify stays true.
Rows without a determinable official zero-point stay ungated (see LEFT_UNGATED).

Idempotent: re-running does not duplicate the basis sentence.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phaseout_caps_2026_09_25_rows import CAPS  # noqa: E402

TREES = [ROOT / "data" / "schemes.json", ROOT / "frontend" / "data" / "schemes.json"]
LAST = "2026-09-25"


def apply(rows: list[dict]) -> list[str]:
    by_id = {r["id"]: r for r in rows}
    changed = []
    for sid, spec in CAPS.items():
        row = by_id[sid]  # KeyError = catalogue drift; fail loudly
        er = row["eligibility_rules"]
        er["max_annual_income"] = spec["cap"]
        if spec["basis"] not in er["notes"]:
            er["notes"] = er["notes"].rstrip() + " " + spec["basis"]
        er["verify"] = True
        er["verify_notes"] = spec["verify_notes"]
        for t in spec.get("remove_tags", []):
            if t in row["tags"]:
                row["tags"].remove(t)
        row["last_verified"] = LAST
        changed.append(sid)
    return changed


def main() -> int:
    raw = json.loads(TREES[0].read_text(encoding="utf-8"))
    rows = raw if isinstance(raw, list) else raw["schemes"]
    changed = apply(rows)
    text = json.dumps(raw, ensure_ascii=False, indent=2) + "\n"
    for p in TREES:
        p.write_text(text, encoding="utf-8")
    print(f"capped {len(changed)} rows: {', '.join(changed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
