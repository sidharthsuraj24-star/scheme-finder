#!/usr/bin/env python3
"""List human-verify catalogue candidates (data/catalogue_candidates.json)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT = REPO_ROOT / "data" / "catalogue_candidates.json"
SCHEMES = REPO_ROOT / "data" / "schemes.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=DEFAULT)
    ap.add_argument(
        "--status",
        default="",
        help="Filter by status (queued|researching|verified_add|rejected|deferred)",
    )
    ap.add_argument("--json", action="store_true", help="Print raw JSON array")
    args = ap.parse_args()

    if not args.path.is_file():
        print(f"No candidates file at {args.path}", file=sys.stderr)
        return 1
    data = json.loads(args.path.read_text(encoding="utf-8"))
    cands = data.get("candidates") if isinstance(data, dict) else data
    if not isinstance(cands, list):
        print("Invalid candidates payload", file=sys.stderr)
        return 1

    scheme_ids: set[str] = set()
    if SCHEMES.is_file():
        schemes = json.loads(SCHEMES.read_text(encoding="utf-8"))
        scheme_ids = {s["id"] for s in schemes if isinstance(s, dict) and "id" in s}

    status_filter = args.status.strip().lower()
    rows = []
    for c in cands:
        if not isinstance(c, dict):
            continue
        st = str(c.get("status") or "")
        if status_filter and st.lower() != status_filter:
            continue
        already = c.get("scheme_id_if_present") in scheme_ids if c.get("scheme_id_if_present") else False
        rows.append({**c, "_already_in_catalogue": already})

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        counts = Counter(str(r.get("status")) for r in rows)
        print(f"candidates={len(rows)} by_status={dict(counts)}")
        for r in rows:
            flag = " [IN_CATALOGUE]" if r.get("_already_in_catalogue") else ""
            print(
                f"- {r.get('id')} | {r.get('status')} | {r.get('name')} | "
                f"{r.get('official_source_url')}{flag}"
            )
            if r.get("reason"):
                print(f"  reason: {r['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
