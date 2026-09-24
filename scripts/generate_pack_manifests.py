#!/usr/bin/env python3
"""Generate versioned state/country pack manifests from schemes.json.

Packs list scheme_id membership only — they do not duplicate scheme bodies.
Ids look like india-kerala@1.0.0, us-federal@1.0.0. Never invents eligibility.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMES = REPO_ROOT / "data" / "schemes.json"
OUT_DIR = REPO_ROOT / "data" / "packs"
FE_OUT_DIR = REPO_ROOT / "frontend" / "data" / "packs"
INDEX = OUT_DIR / "index.json"

IST = ZoneInfo("Asia/Kolkata")
DEFAULT_VERSION = "1.0.0"

# tag slug -> (pack_slug, country, display)
INDIA_STATE_TAGS: dict[str, tuple[str, str]] = {
    "kerala": ("india-kerala", "Kerala"),
    "karnataka": ("india-karnataka", "Karnataka"),
    "tamil_nadu": ("india-tamil-nadu", "Tamil Nadu"),
    "tamil-nadu": ("india-tamil-nadu", "Tamil Nadu"),
    "maharashtra": ("india-maharashtra", "Maharashtra"),
    "gujarat": ("india-gujarat", "Gujarat"),
    "rajasthan": ("india-rajasthan", "Rajasthan"),
    "delhi": ("india-delhi", "Delhi"),
    "andhra_pradesh": ("india-andhra-pradesh", "Andhra Pradesh"),
    "andhra-pradesh": ("india-andhra-pradesh", "Andhra Pradesh"),
    "telangana": ("india-telangana", "Telangana"),
    "west_bengal": ("india-west-bengal", "West Bengal"),
    "uttar_pradesh": ("india-uttar-pradesh", "Uttar Pradesh"),
    "madhya_pradesh": ("india-madhya-pradesh", "Madhya Pradesh"),
    "bihar": ("india-bihar", "Bihar"),
    "odisha": ("india-odisha", "Odisha"),
    "punjab": ("india-punjab", "Punjab"),
    "haryana": ("india-haryana", "Haryana"),
    "assam": ("india-assam", "Assam"),
    "jharkhand": ("india-jharkhand", "Jharkhand"),
    "chhattisgarh": ("india-chhattisgarh", "Chhattisgarh"),
    "himachal_pradesh": ("india-himachal-pradesh", "Himachal Pradesh"),
    "uttarakhand": ("india-uttarakhand", "Uttarakhand"),
    "goa": ("india-goa", "Goa"),
    "manipur": ("india-manipur", "Manipur"),
    "meghalaya": ("india-meghalaya", "Meghalaya"),
    "mizoram": ("india-mizoram", "Mizoram"),
    "nagaland": ("india-nagaland", "Nagaland"),
    "tripura": ("india-tripura", "Tripura"),
    "sikkim": ("india-sikkim", "Sikkim"),
    "arunachal_pradesh": ("india-arunachal-pradesh", "Arunachal Pradesh"),
    "jammu_kashmir": ("india-jammu-kashmir", "Jammu and Kashmir"),
    "ladakh": ("india-ladakh", "Ladakh"),
    "puducherry": ("india-puducherry", "Puducherry"),
    "chandigarh": ("india-chandigarh", "Chandigarh"),
    "lakshadweep": ("india-lakshadweep", "Lakshadweep"),
}

US_STATE_TAGS: dict[str, tuple[str, str]] = {
    "california": ("us-california", "California"),
    "texas": ("us-texas", "Texas"),
    "new_york": ("us-new-york", "New York"),
    "florida": ("us-florida", "Florida"),
    "illinois": ("us-illinois", "Illinois"),
    "pennsylvania": ("us-pennsylvania", "Pennsylvania"),
    "ohio": ("us-ohio", "Ohio"),
    "georgia": ("us-georgia", "Georgia"),
    "north_carolina": ("us-north-carolina", "North Carolina"),
    "michigan": ("us-michigan", "Michigan"),
    "massachusetts": ("us-massachusetts", "Massachusetts"),
    "washington": ("us-washington", "Washington"),
    "arizona": ("us-arizona", "Arizona"),
    "colorado": ("us-colorado", "Colorado"),
    "virginia": ("us-virginia", "Virginia"),
    "new_jersey": ("us-new-jersey", "New Jersey"),
}


def slugify_file(pack_id: str, version: str) -> str:
    return f"{pack_id}@{version}.json"


def is_us(scheme: dict) -> bool:
    tags = [str(t).lower() for t in (scheme.get("tags") or [])]
    sid = str(scheme.get("id") or "")
    return "united_states" in tags or "united-states" in tags or sid.startswith("us-")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--schemes", type=Path, default=SCHEMES)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--version", default=DEFAULT_VERSION)
    ap.add_argument(
        "--min-size",
        type=int,
        default=1,
        help="Skip packs with fewer than N schemes (default 1)",
    )
    args = ap.parse_args()

    schemes = json.loads(args.schemes.read_text(encoding="utf-8"))
    if not isinstance(schemes, list):
        print("schemes.json must be a list", file=sys.stderr)
        return 1

    membership: dict[str, set[str]] = defaultdict(set)
    meta: dict[str, dict] = {}

    def ensure(pack_id: str, *, country: str, region: str, kind: str) -> None:
        if pack_id not in meta:
            meta[pack_id] = {
                "pack_id": pack_id,
                "version": args.version,
                "country": country,
                "region": region,
                "kind": kind,
            }

    for s in schemes:
        if not isinstance(s, dict) or "id" not in s:
            continue
        sid = s["id"]
        tags = [str(t).lower() for t in (s.get("tags") or [])]
        us = is_us(s)

        if us:
            if "federal" in tags or (sid.startswith("us-") and not any(t in US_STATE_TAGS for t in tags)):
                # federal pack: federal tag OR us-* without a known state tag
                if "federal" in tags or not any(t in US_STATE_TAGS for t in tags):
                    ensure("us-federal", country="United States", region="Federal", kind="country_federal")
                    if "federal" in tags:
                        membership["us-federal"].add(sid)
            for t in tags:
                if t in US_STATE_TAGS:
                    pid, label = US_STATE_TAGS[t]
                    ensure(pid, country="United States", region=label, kind="state")
                    membership[pid].add(sid)
            # Also put pure federal-tagged into us-federal
            if "federal" in tags:
                ensure("us-federal", country="United States", region="Federal", kind="country_federal")
                membership["us-federal"].add(sid)
        else:
            # India / other
            if "central" in tags or "nationwide" in tags:
                ensure("india-central", country="India", region="Central / nationwide", kind="country_central")
                membership["india-central"].add(sid)
            for t in tags:
                if t in INDIA_STATE_TAGS:
                    pid, label = INDIA_STATE_TAGS[t]
                    ensure(pid, country="India", region=label, kind="state")
                    membership[pid].add(sid)

    args.out.mkdir(parents=True, exist_ok=True)
    if FE_OUT_DIR.parent.is_dir():
        FE_OUT_DIR.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(IST).isoformat(timespec="seconds")
    index_packs: list[dict] = []

    for pack_id, ids in sorted(membership.items()):
        if len(ids) < args.min_size:
            continue
        m = meta[pack_id]
        ordered = sorted(ids)
        manifest = {
            "pack_id": pack_id,
            "version": args.version,
            "full_id": f"{pack_id}@{args.version}",
            "country": m["country"],
            "region": m["region"],
            "kind": m["kind"],
            "scheme_ids": ordered,
            "scheme_count": len(ordered),
            "generated_at": generated_at,
            "timezone": "Asia/Kolkata",
            "source": "derived from data/schemes.json tags — membership only, no scheme bodies",
            "note": "Bump version when membership rules change; regenerate via scripts/generate_pack_manifests.py",
        }
        fname = slugify_file(pack_id, args.version)
        path = args.out / fname
        text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
        path.write_text(text, encoding="utf-8")
        if FE_OUT_DIR.parent.is_dir():
            (FE_OUT_DIR / fname).write_text(text, encoding="utf-8")
        index_packs.append(
            {
                "pack_id": pack_id,
                "version": args.version,
                "full_id": manifest["full_id"],
                "file": fname,
                "country": m["country"],
                "region": m["region"],
                "kind": m["kind"],
                "scheme_count": len(ordered),
            }
        )

    index = {
        "schema_version": 1,
        "generated_at": generated_at,
        "timezone": "Asia/Kolkata",
        "default_version": args.version,
        "pack_count": len(index_packs),
        "packs": index_packs,
        "note": "Versioned catalogue packs (membership manifests). See docs/CATALOGUE_OPS.md.",
    }
    index_text = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    INDEX.write_text(index_text, encoding="utf-8")
    if FE_OUT_DIR.parent.is_dir():
        (FE_OUT_DIR / "index.json").write_text(index_text, encoding="utf-8")

    print(f"Wrote {len(index_packs)} packs to {args.out} (version {args.version})")
    for p in index_packs[:8]:
        print(f"  {p['full_id']} ({p['scheme_count']})")
    if len(index_packs) > 8:
        print(f"  ... +{len(index_packs) - 8} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
