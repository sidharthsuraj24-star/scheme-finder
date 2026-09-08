#!/usr/bin/env python3
"""Scheme catalogue freshness checklist (semi-automatic; no eligibility edits).

Prints scheme ids + official_source_url + last_verified age.
Optionally HEAD/GET official URLs and notes failures.
Exits 0 always for Actions (report in output); exit 1 only on script crash.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMES_PATH = REPO_ROOT / "data" / "schemes.json"
META_PATH = REPO_ROOT / "data" / "catalogue_meta.json"


def days_since(iso_date: str, today: date | None = None) -> int | None:
    today = today or datetime.now(timezone.utc).date()
    try:
        d = date.fromisoformat(iso_date[:10])
    except ValueError:
        return None
    return (today - d).days


def check_url(url: str, timeout: float = 12.0) -> str:
    """Return OK / status / error note. Never invents eligibility."""
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "scheme-finder-freshness-check/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return f"HEAD {resp.status}"
    except urllib.error.HTTPError as e:
        # Some portals reject HEAD — fall back to GET
        if e.code in (403, 405, 501):
            try:
                get_req = urllib.request.Request(
                    url,
                    method="GET",
                    headers={"User-Agent": "scheme-finder-freshness-check/1.0"},
                )
                with urllib.request.urlopen(get_req, timeout=timeout) as resp:
                    return f"GET {resp.status} (HEAD {e.code})"
            except Exception as e2:  # noqa: BLE001
                return f"FAIL HEAD {e.code}; GET {e2}"
        return f"FAIL HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        # Try GET once more for network/method oddities
        try:
            get_req = urllib.request.Request(
                url,
                method="GET",
                headers={"User-Agent": "scheme-finder-freshness-check/1.0"},
            )
            with urllib.request.urlopen(get_req, timeout=timeout) as resp:
                return f"GET {resp.status} (HEAD error: {e})"
        except Exception as e2:  # noqa: BLE001
            return f"FAIL {e2}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-urls",
        action="store_true",
        help="Optionally HEAD/GET official_source_url and note failures",
    )
    parser.add_argument(
        "--schemes",
        type=Path,
        default=SCHEMES_PATH,
        help="Path to schemes.json",
    )
    parser.add_argument(
        "--meta",
        type=Path,
        default=META_PATH,
        help="Path to catalogue_meta.json",
    )
    args = parser.parse_args()

    try:
        schemes = json.loads(args.schemes.read_text(encoding="utf-8"))
        meta = json.loads(args.meta.read_text(encoding="utf-8")) if args.meta.is_file() else {}
    except Exception as e:  # noqa: BLE001
        print(f"CRASH reading inputs: {e}", file=sys.stderr)
        return 1

    if not isinstance(schemes, list):
        print("CRASH: schemes.json must be a JSON array", file=sys.stderr)
        return 1

    updated_as_of = str(meta.get("updated_as_of") or "unknown")
    stale_after = int(meta.get("stale_after_days") or 30)
    cat_age = days_since(updated_as_of) if updated_as_of != "unknown" else None
    is_stale = cat_age is not None and cat_age > stale_after

    lines: list[str] = []
    lines.append("# Scheme catalogue freshness checklist")
    lines.append("")
    lines.append(f"- Catalogue `updated_as_of`: **{updated_as_of}** ({cat_age} days ago)" if cat_age is not None else f"- Catalogue `updated_as_of`: **{updated_as_of}**")
    lines.append(f"- `stale_after_days`: {stale_after}")
    lines.append(f"- `is_stale`: **{is_stale}**")
    lines.append(f"- Scheme count: {len(schemes)}")
    lines.append("")
    lines.append("## Human steps (do NOT auto-edit eligibility)")
    lines.append("")
    lines.append("1. Open each official URL below and verify age/income/benefit text.")
    lines.append("2. If rules changed, open a PR updating `data/schemes.json` + `frontend/data/` copy.")
    lines.append("3. Keep `verify: true` when the official page is ambiguous — never invent caps.")
    lines.append("4. Bump `last_verified` (ISO date) per scheme you checked.")
    lines.append("5. Bump `catalogue_meta.json` `updated_as_of` / `updated_as_of_iso` after the PR is ready.")
    lines.append("")
    lines.append("## Schemes")
    lines.append("")

    for s in schemes:
        sid = s.get("id", "?")
        url = s.get("official_source_url") or "(MISSING official_source_url)"
        last = s.get("last_verified") or updated_as_of
        age = days_since(str(last))
        age_s = f"{age}d" if age is not None else "?"
        lines.append(f"- [ ] `{sid}`")
        lines.append(f"  - official_source_url: {url}")
        lines.append(f"  - last_verified: {last} (age: {age_s})")
        if args.check_urls and isinstance(url, str) and url.startswith("http"):
            note = check_url(url)
            lines.append(f"  - url_check: {note}")
        lines.append("")

    report = "\n".join(lines)
    print(report)

    # Also write a machine-friendly path for Actions to attach
    out = REPO_ROOT / "scripts" / ".freshness-report.md"
    try:
        out.write_text(report + "\n", encoding="utf-8")
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"CRASH: {e}", file=sys.stderr)
        raise SystemExit(1) from e
