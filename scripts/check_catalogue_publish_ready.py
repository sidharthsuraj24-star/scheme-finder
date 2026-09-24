#!/usr/bin/env python3
"""Lightweight publish gate (curator/reviewer/publisher scaffold — not full CMS).

Fails (exit 1) when:
  - data/ and frontend/data/ schemes.json diverge
  - catalogue_release.json missing or checksum stale vs schemes bytes
  - scheme_count in release/meta disagrees with schemes.json
  - verify:true count is undocumented in catalogue_meta (optional soft check)

Does not invent eligibility. Full CMS roles come later — see docs/TRUST.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_SCHEMES = REPO_ROOT / "data" / "schemes.json"
FE_SCHEMES = REPO_ROOT / "frontend" / "data" / "schemes.json"
DATA_META = REPO_ROOT / "data" / "catalogue_meta.json"
RELEASE_PATH = REPO_ROOT / "data" / "catalogue_release.json"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-missing-verify-doc",
        action="store_true",
        help="Skip soft check that meta mentions verify schemes",
    )
    args = parser.parse_args()
    errors: list[str] = []

    if not DATA_SCHEMES.is_file() or not FE_SCHEMES.is_file():
        errors.append("Both data/schemes.json and frontend/data/schemes.json required")
    else:
        dh = sha256_file(DATA_SCHEMES)
        fh = sha256_file(FE_SCHEMES)
        if dh != fh:
            errors.append(f"schemes.json trees diverge ({dh[:16]}… vs {fh[:16]}…)")

        schemes = json.loads(DATA_SCHEMES.read_text(encoding="utf-8"))
        if not isinstance(schemes, list):
            errors.append("schemes.json must be a JSON array")
            schemes = []
        n = len(schemes)
        verify_n = sum(
            1
            for s in schemes
            if isinstance(s, dict)
            and bool((s.get("eligibility_rules") or s.get("eligibility_rules") or {}).get("verify"))
        )

        if not RELEASE_PATH.is_file():
            errors.append(
                "data/catalogue_release.json missing — run scripts/sign_catalogue_release.py"
            )
        else:
            release = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
            if not isinstance(release, dict):
                errors.append("catalogue_release.json invalid")
            else:
                expected = release.get("schemes_sha256")
                if expected != dh:
                    errors.append(
                        "catalogue_release schemes_sha256 stale — re-run sign_catalogue_release.py"
                    )
                if release.get("scheme_count") != n:
                    errors.append(
                        f"release.scheme_count={release.get('scheme_count')} != {n}"
                    )

        if DATA_META.is_file():
            meta = json.loads(DATA_META.read_text(encoding="utf-8"))
            if isinstance(meta, dict):
                mc = meta.get("scheme_count", meta.get("scheme_count"))
                if mc not in (None, n) and int(mc) != n:
                    errors.append(
                        f"catalogue_meta.scheme_count={mc} != {n}"
                    )
                if not args.allow_missing_verify_doc and verify_n > 0:
                    # Soft documentation: scope/disclaimer should acknowledge curated/verify nature
                    blob = json.dumps(meta, ensure_ascii=False).lower()
                    if "verify" not in blob and "confirm" not in blob:
                        errors.append(
                            f"{verify_n} schemes have verify:true but catalogue_meta "
                            "does not mention verify/confirm — document in meta or TRUST.md"
                        )
        else:
            errors.append("data/catalogue_meta.json missing")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        print(
            "Publish not ready. See docs/TRUST.md (publisher checklist).",
            file=sys.stderr,
        )
        return 1

    print(
        f"OK publish-ready: schemes={sha256_file(DATA_SCHEMES)[:16]}… "
        f"count={len(json.loads(DATA_SCHEMES.read_text(encoding='utf-8')))} "
        f"verify_true={sum(1 for s in json.loads(DATA_SCHEMES.read_text(encoding='utf-8')) if bool((s.get('eligibility_rules') or {}).get('verify')))}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
