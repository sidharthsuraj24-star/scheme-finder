#!/usr/bin/env python3
"""Write data/url_health_snapshot.json from freshness probe results.

Default: sample/empty-safe snapshot (no live gov probes) for UI wiring.
Optional --probe-sample: HEAD a short allowlisted .gov set (max ~8 URLs).
Never invents eligibility. Feed daily routine by piping freshness failures
or regenerating after scripts/scheme_freshness_check.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "data" / "url_health_snapshot.json"
SCHEMES = REPO_ROOT / "data" / "schemes.json"

# Short safe allowlist for optional demo probes (official .gov only).
_PROBE_SAMPLE_IDS = (
    "us-trump-accounts",
    "us-coverdell-esa",
    "us-529-qtp",
    "us-able-accounts",
    "in-pm-kisan",
    "sevana-old-age-pension",
)


def ist_now() -> str:
    return datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds")


def probe(url: str, timeout: float = 8.0) -> str:
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "scheme-finder-url-health/0.1"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return f"HEAD {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 405, 501):
            try:
                get_req = urllib.request.Request(
                    url,
                    method="GET",
                    headers={"User-Agent": "scheme-finder-url-health/0.1"},
                )
                with urllib.request.urlopen(get_req, timeout=timeout) as resp:
                    return f"GET {resp.status} (HEAD {e.code})"
            except Exception as e2:  # noqa: BLE001
                return f"FAIL HEAD {e.code}; GET {e2}"
        return f"FAIL HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return f"FAIL {e}"


def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower() or url
    except Exception:  # noqa: BLE001
        return url


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--probe-sample",
        action="store_true",
        help="HEAD a short allowlisted sample (do not use as full catalogue hammer)",
    )
    ap.add_argument(
        "--from-freshness-json",
        type=Path,
        default=None,
        help="Optional JSON list of {host,status,scheme_id,url} from a freshness run",
    )
    args = ap.parse_args()

    flaky: list[dict] = []
    checked = 0
    ok = 0

    if args.from_freshness_json and args.from_freshness_json.is_file():
        raw = json.loads(args.from_freshness_json.read_text(encoding="utf-8"))
        items = raw if isinstance(raw, list) else raw.get("results") or []
        for item in items:
            if not isinstance(item, dict):
                continue
            checked += 1
            status = str(item.get("status") or item.get("result") or "")
            if status.upper().startswith("OK") or " 200" in status:
                ok += 1
            else:
                flaky.append(
                    {
                        "host": item.get("host") or host_of(str(item.get("url") or "")),
                        "status": status[:200],
                        "scheme_id": item.get("scheme_id"),
                        "url": item.get("url"),
                    }
                )
    elif args.probe_sample and SCHEMES.is_file():
        schemes = json.loads(SCHEMES.read_text(encoding="utf-8"))
        by_id = {s["id"]: s for s in schemes if isinstance(s, dict) and "id" in s}
        for sid in _PROBE_SAMPLE_IDS:
            s = by_id.get(sid)
            if not s:
                continue
            url = s.get("official_source_url")
            if not isinstance(url, str) or not url.startswith("http"):
                continue
            checked += 1
            status = probe(url)
            if status.startswith("HEAD 2") or status.startswith("GET 2"):
                ok += 1
            else:
                flaky.append(
                    {
                        "host": host_of(url),
                        "status": status[:200],
                        "scheme_id": sid,
                        "url": url,
                    }
                )
    else:
        # Empty/sample snapshot for UI — document how daily routine fills it.
        flaky = []
        checked = 0
        ok = 0

    payload = {
        "generated_at": ist_now(),
        "timezone": "Asia/Kolkata",
        "checked_count": checked,
        "ok_count": ok,
        "flaky_hosts": flaky[:50],
        "note": (
            "Sample/ops snapshot. Default run writes empty flaky list (no live probes). "
            "Use --probe-sample for a short allowlist, or --from-freshness-json after "
            "scripts/scheme_freshness_check.py. Never hammers full catalogue from CI."
        ),
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} checked={checked} ok={ok} flaky={len(flaky)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
