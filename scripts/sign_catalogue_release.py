#!/usr/bin/env python3
"""Sign a catalogue release: SHA-256 of dual-tree schemes.json + release metadata.

Writes data/catalogue_release.json and syncs a copy under frontend/data/.
Appends an immutable audit line (action=release).

Run before commit when catalogue (schemes.json) changes:
  python3 scripts/sign_catalogue_release.py --changelog "Describe the change"
  # or omit --changelog to use git shortlog since last release tag/commit note
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_SCHEMES = REPO_ROOT / "data" / "schemes.json"
FE_SCHEMES = REPO_ROOT / "frontend" / "data" / "schemes.json"
DATA_META = REPO_ROOT / "data" / "catalogue_meta.json"
RELEASE_PATH = REPO_ROOT / "data" / "catalogue_release.json"
FE_RELEASE_PATH = REPO_ROOT / "frontend" / "data" / "catalogue_release.json"
IST = ZoneInfo("Asia/Kolkata")

# Import sibling helper without packaging
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from append_catalogue_audit import append_audit  # noqa: E402


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def git_shortlog_since_release(prev: dict | None) -> str:
    """Best-effort changelog from git log since previous generated_at or last release."""
    try:
        if prev and prev.get("commit_sha"):
            rng = f"{prev['commit_sha']}..HEAD"
        else:
            rng = "-20"
        out = subprocess.check_output(
            ["git", "log", "--oneline", rng],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if out:
            lines = out.splitlines()[:15]
            return "; ".join(lines)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return "Catalogue release (no git shortlog available)"


def resolve_commit_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def build_release(*, changelog: str | None, dry_run: bool = False) -> dict:
    if not DATA_SCHEMES.is_file():
        raise SystemExit(f"Missing {DATA_SCHEMES}")
    if not FE_SCHEMES.is_file():
        raise SystemExit(f"Missing {FE_SCHEMES}")

    data_hash = sha256_file(DATA_SCHEMES)
    fe_hash = sha256_file(FE_SCHEMES)
    if data_hash != fe_hash:
        raise SystemExit(
            "data/schemes.json and frontend/data/schemes.json differ "
            f"(sha256 {data_hash[:12]}… vs {fe_hash[:12]}…). Sync before signing."
        )

    schemes = load_json(DATA_SCHEMES)
    if not isinstance(schemes, list):
        raise SystemExit("schemes.json must be a JSON array")
    scheme_count = len(schemes)

    meta: dict = {}
    if DATA_META.is_file():
        raw = load_json(DATA_META)
        if isinstance(raw, dict):
            meta = raw

    updated_as_of = str(meta.get("updated_as_of") or datetime.now(IST).date().isoformat())
    prev: dict | None = None
    if RELEASE_PATH.is_file():
        raw_prev = load_json(RELEASE_PATH)
        if isinstance(raw_prev, dict):
            prev = raw_prev

    entry_text = changelog if changelog is not None else git_shortlog_since_release(prev)
    generated_at = datetime.now(IST).isoformat(timespec="seconds")
    commit_sha = resolve_commit_sha()

    changelog_history: list[dict] = []
    if prev and isinstance(prev.get("changelog"), list):
        changelog_history = list(prev["changelog"])
    elif prev and isinstance(prev.get("changelog"), str):
        changelog_history = [
            {
                "at": prev.get("generated_at"),
                "text": prev["changelog"],
                "schemes_sha256": prev.get("schemes_sha256"),
            }
        ]

    new_entry = {
        "at": generated_at,
        "text": entry_text,
        "schemes_sha256": data_hash,
        "scheme_count": scheme_count,
        "updated_as_of": updated_as_of,
    }
    if commit_sha:
        new_entry["commit_sha"] = commit_sha
    changelog_history.append(new_entry)
    # Keep last 50 entries
    changelog_history = changelog_history[-50:]

    release = {
        "updated_as_of": updated_as_of,
        "scheme_count": scheme_count,
        "schemes_sha256": data_hash,
        "generated_at": generated_at,
        "timezone": "Asia/Kolkata",
        "changelog": changelog_history,
        "latest_changelog": entry_text,
    }
    if commit_sha:
        release["commit_sha"] = commit_sha
    if meta.get("disclaimer"):
        release["disclaimer"] = meta["disclaimer"]

    if dry_run:
        return release

    text = json.dumps(release, ensure_ascii=False, indent=2) + "\n"
    RELEASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    RELEASE_PATH.write_text(text, encoding="utf-8")
    FE_RELEASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FE_RELEASE_PATH.write_text(text, encoding="utf-8")

    append_audit(
        action="release",
        scheme_ids=[],
        notes=entry_text[:500],
        release_checksum=data_hash,
        commit_sha=commit_sha,
        extra={"scheme_count": scheme_count, "updated_as_of": updated_as_of},
    )
    return release


def verify_release(*, release_path: Path = RELEASE_PATH) -> int:
    """Exit 0 if release checksum matches both schemes trees; else 1."""
    if not release_path.is_file():
        print("FAIL: catalogue_release.json missing", file=sys.stderr)
        return 1
    release = load_json(release_path)
    if not isinstance(release, dict):
        print("FAIL: catalogue_release.json not an object", file=sys.stderr)
        return 1
    expected = release.get("schemes_sha256")
    if not expected or not isinstance(expected, str):
        print("FAIL: schemes_sha256 missing", file=sys.stderr)
        return 1
    data_hash = sha256_file(DATA_SCHEMES)
    fe_hash = sha256_file(FE_SCHEMES)
    ok = True
    if data_hash != fe_hash:
        print(
            f"FAIL: dual-tree schemes.json diverge "
            f"({data_hash[:16]}… vs {fe_hash[:16]}…)",
            file=sys.stderr,
        )
        ok = False
    if data_hash != expected:
        print(
            f"FAIL: checksum mismatch file={data_hash} release={expected}",
            file=sys.stderr,
        )
        ok = False
    else:
        print(f"OK schemes_sha256={data_hash} scheme_count={release.get('scheme_count')}")
    count = release.get("scheme_count")
    schemes = load_json(DATA_SCHEMES)
    if isinstance(schemes, list) and count is not None and int(count) != len(schemes):
        print(
            f"FAIL: scheme_count {count} != len(schemes) {len(schemes)}",
            file=sys.stderr,
        )
        ok = False
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changelog",
        default=None,
        help="Changelog text for this release (default: git shortlog)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print release JSON without writing files or audit",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify existing release checksum against schemes.json trees",
    )
    args = parser.parse_args()
    if args.verify:
        return verify_release()
    release = build_release(changelog=args.changelog, dry_run=args.dry_run)
    print(json.dumps(release, ensure_ascii=False, indent=2))
    if not args.dry_run:
        print(f"Wrote {RELEASE_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
        print(f"Wrote {FE_RELEASE_PATH.relative_to(REPO_ROOT)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
