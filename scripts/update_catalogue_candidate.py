#!/usr/bin/env python3
"""Update a catalogue candidate status and append audit trail.

Status transitions: needs_review|queued|researching|verified_add|rejected|deferred
(`needs_review` = auto-drafted by scripts/draft_candidates_from_sources.py; a
human moves it to queued/researching/rejected after checking the source).
Never invents eligibility. Prefer queue plumbing over adding schemes here.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT = REPO_ROOT / "data" / "catalogue_candidates.json"
FE_DEFAULT = REPO_ROOT / "frontend" / "data" / "catalogue_candidates.json"
SCHEMES = REPO_ROOT / "data" / "schemes.json"
IST = ZoneInfo("Asia/Kolkata")

VALID = frozenset({"needs_review", "queued", "researching", "verified_add", "rejected", "deferred"})

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from append_catalogue_audit import append_audit, resolve_actor  # noqa: E402


def ist_now() -> str:
    return datetime.now(IST).isoformat(timespec="seconds")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--id", required=True, help="Candidate id")
    ap.add_argument("--status", required=True, choices=sorted(VALID))
    ap.add_argument("--reason", default="", help="Why status changed")
    ap.add_argument("--notes", default="", help="Free-text notes")
    ap.add_argument("--official-source-url", default="", help="Update official URL")
    ap.add_argument("--name", default="", help="Update display name")
    ap.add_argument("--country", default="", help="Update country")
    ap.add_argument(
        "--add",
        action="store_true",
        help="Create candidate if missing (requires --name and --official-source-url)",
    )
    ap.add_argument("--path", type=Path, default=DEFAULT)
    args = ap.parse_args()

    if args.path.is_file():
        data = json.loads(args.path.read_text(encoding="utf-8"))
    else:
        data = {
            "schema_version": 1,
            "updated_at": ist_now(),
            "timezone": "Asia/Kolkata",
            "note": "Human-verify candidate queue.",
            "candidates": [],
        }

    cands = data.setdefault("candidates", [])
    if not isinstance(cands, list):
        print("Invalid candidates list", file=sys.stderr)
        return 1

    # Guard: refuse verified_add if already in schemes under a known id note
    scheme_ids: set[str] = set()
    if SCHEMES.is_file():
        schemes = json.loads(SCHEMES.read_text(encoding="utf-8"))
        scheme_ids = {s["id"] for s in schemes if isinstance(s, dict) and "id" in s}

    target = None
    for c in cands:
        if isinstance(c, dict) and c.get("id") == args.id:
            target = c
            break

    actor = resolve_actor()
    if target is None:
        if not args.add:
            print(f"Candidate {args.id!r} not found (pass --add to create)", file=sys.stderr)
            return 1
        if not args.name or not args.official_source_url:
            print("--add requires --name and --official-source-url", file=sys.stderr)
            return 1
        target = {
            "id": args.id,
            "name": args.name,
            "country": args.country or "India",
            "official_source_url": args.official_source_url,
            "status": args.status,
            "reason": args.reason or "Created via update_catalogue_candidate.py",
            "noted_at": ist_now(),
            "actor": actor,
            "notes": args.notes,
        }
        cands.append(target)
    else:
        prev = target.get("status")
        target["status"] = args.status
        if args.reason:
            target["reason"] = args.reason
        if args.notes:
            target["notes"] = args.notes
        if args.official_source_url:
            target["official_source_url"] = args.official_source_url
        if args.name:
            target["name"] = args.name
        if args.country:
            target["country"] = args.country
        target["noted_at"] = ist_now()
        target["actor"] = actor
        target["previous_status"] = prev

    # Honesty: if marking verified_add, remind human must PR schemes.json separately
    if args.status == "verified_add":
        present = target.get("scheme_id_if_present")
        if present and present in scheme_ids:
            print(
                f"WARNING: {present} already in schemes.json — prefer status=deferred",
                file=sys.stderr,
            )
        target["notes"] = (
            (target.get("notes") or "")
            + " | verified_add means human approved adding via PR — this script does not mutate schemes.json"
        ).strip(" |")

    data["updated_at"] = ist_now()
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    args.path.parent.mkdir(parents=True, exist_ok=True)
    args.path.write_text(text, encoding="utf-8")
    if FE_DEFAULT.parent.is_dir():
        FE_DEFAULT.write_text(text, encoding="utf-8")

    append_audit(
        action="note",
        scheme_ids=[args.id],
        notes=f"candidate status -> {args.status}: {args.reason or args.notes}",
        extra={"candidate_id": args.id, "candidate_status": args.status},
    )
    print(json.dumps(target, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
