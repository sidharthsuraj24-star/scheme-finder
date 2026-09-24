#!/usr/bin/env python3
"""List URL probe tickets from data/url_tickets.jsonl (latest per scheme_id+url)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import url_tickets as tickets  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--path", type=Path, default=tickets.TICKETS_PATH)
    ap.add_argument(
        "--status",
        default="open",
        help="Filter latest status (default open; use 'all' for every latest row)",
    )
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    latest = tickets.latest_by_key(tickets.read_tickets(args.path))
    rows = list(latest.values())
    st = args.status.strip().lower()
    if st != "all":
        if st == "open":
            rows = [r for r in rows if str(r.get("status")) in tickets.OPENISH]
        else:
            rows = [r for r in rows if str(r.get("status") or "").lower() == st]

    summary = tickets.summarize(args.path)
    if args.json:
        print(json.dumps({"summary": summary, "tickets": rows}, indent=2, ensure_ascii=False))
    else:
        print(f"summary={summary}")
        print(f"showing={len(rows)} (filter={args.status})")
        for r in sorted(rows, key=lambda x: str(x.get("last_seen") or ""), reverse=True):
            print(
                f"- {r.get('ticket_id')} | {r.get('status')} | {r.get('scheme_id')} | "
                f"{r.get('host')} | {r.get('http_or_error')}"
            )
            print(f"  url: {r.get('url')}")
            print(f"  first={r.get('first_seen')} last={r.get('last_seen')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
