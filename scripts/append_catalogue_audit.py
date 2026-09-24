#!/usr/bin/env python3
"""Append one immutable line to data/catalogue_audit.jsonl.

Never rewrites past lines. Used by sign_catalogue_release.py and deepen scripts.
Actor: CATALOGUE_ACTOR env, else git user.name / "git", else "unknown".
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = REPO_ROOT / "data" / "catalogue_audit.jsonl"
IST = ZoneInfo("Asia/Kolkata")

VALID_ACTIONS = frozenset(
    {"add", "update", "tag", "verify", "release", "publish_check", "note"}
)


def resolve_actor() -> str:
    env = os.environ.get("CATALOGUE_ACTOR", "").strip()
    if env:
        return env
    try:
        out = subprocess.check_output(
            ["git", "config", "user.name"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if out:
            return out
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return "git"


def resolve_commit_sha() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def now_ist_iso() -> str:
    return datetime.now(IST).isoformat(timespec="seconds")


def read_audit_entries(path: Path = AUDIT_PATH) -> list[dict[str, Any]]:
    """Parse JSONL; skip blank lines. Does not rewrite the file."""
    if not path.is_file():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        entries.append(json.loads(line))
    return entries


def append_audit(
    *,
    action: str,
    scheme_ids: list[str] | None = None,
    notes: str = "",
    release_checksum: str | None = None,
    commit_sha: str | None = None,
    actor: str | None = None,
    extra: dict[str, Any] | None = None,
    path: Path = AUDIT_PATH,
) -> dict[str, Any]:
    if action not in VALID_ACTIONS:
        raise ValueError(f"action must be one of {sorted(VALID_ACTIONS)}, got {action!r}")
    entry: dict[str, Any] = {
        "timestamp": now_ist_iso(),
        "actor": actor or resolve_actor(),
        "action": action,
        "scheme_ids": list(scheme_ids or []),
        "notes": notes or "",
    }
    sha = commit_sha if commit_sha is not None else resolve_commit_sha()
    if sha:
        entry["commit_sha"] = sha
    if release_checksum:
        entry["release_checksum"] = release_checksum
    if extra:
        for k, v in extra.items():
            if k not in entry:
                entry[k] = v
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--action",
        required=True,
        choices=sorted(VALID_ACTIONS),
        help="Catalogue action type",
    )
    parser.add_argument(
        "--scheme-ids",
        default="",
        help="Comma-separated scheme ids (optional)",
    )
    parser.add_argument("--notes", default="", help="Free-text notes")
    parser.add_argument(
        "--release-checksum",
        default="",
        help="SHA-256 of schemes.json for release/verify entries",
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=AUDIT_PATH,
        help="Audit JSONL path",
    )
    args = parser.parse_args()
    ids = [s.strip() for s in args.scheme_ids.split(",") if s.strip()]
    entry = append_audit(
        action=args.action,
        scheme_ids=ids,
        notes=args.notes,
        release_checksum=args.release_checksum or None,
        path=args.path,
    )
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
