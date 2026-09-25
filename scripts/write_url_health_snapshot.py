#!/usr/bin/env python3
"""Write data/url_health_snapshot.json from freshness probe results.

Default: sample/empty-safe snapshot (no live gov probes) for UI wiring.
Optional --probe-sample: HEAD a short allowlisted .gov set (max ~8 URLs).
Optional --probe-known-flaky: short probe of historically flaky hosts only
(nsap.dord.gov.in, sspensions.ap.gov.in, pensionscheme.sikkim.gov.in) — small
timeout, low concurrency, User-Agent set. Never invents eligibility.

HEAD is tried first; on HEAD 400/403/404/405/5xx/501 the probe retries with GET,
because some official IIS portals (e.g. pensionscheme.sikkim.gov.in) answer HEAD
with 404 while GET returns 200.

Hosts in _GEOFENCED_INDIA_HOSTS block non-Indian networks (TLS EOF / timeout from
US CI/box). A failed probe there is reported as "GEO-FENCED …" and does NOT open a
ticket; verify from an Indian network (e.g. check-host.net India nodes) instead.

On failure statuses, upserts open tickets in data/url_tickets.jsonl; on OK,
resolves matching open tickets to fixed.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "data" / "url_health_snapshot.json"
FE_OUT = REPO_ROOT / "frontend" / "data" / "url_health_snapshot.json"
SCHEMES = REPO_ROOT / "data" / "schemes.json"
TICKETS = REPO_ROOT / "data" / "url_tickets.jsonl"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import url_tickets as tickets  # noqa: E402

# Short safe allowlist for optional demo probes (official .gov only).
_PROBE_SAMPLE_IDS = (
    "us-trump-accounts",
    "us-coverdell-esa",
    "us-529-qtp",
    "us-able-accounts",
    "in-pm-kisan",
    "sevana-old-age-pension",
)

# Known historically flaky hosts — probe at most one URL per host.
_KNOWN_FLAKY_HOST_MARKERS = (
    # nsap.nic.in retired (NXDOMAIN) — NSAP portal moved to nsap.dord.gov.in (2026-09-25)
    "nsap.dord.gov.in",
    "sspensions.ap.gov.in",
    "pensionscheme.sikkim.gov.in",
)

# Official hosts that geo-restrict non-Indian networks (verified 2026-09-25 via
# check-host.net: HTTP 200 from India nodes, timeout/TLS EOF elsewhere).
_GEOFENCED_INDIA_HOSTS = frozenset({"nsap.dord.gov.in"})

# HEAD statuses that warrant a GET retry before declaring failure.
_HEAD_RETRY_WITH_GET = frozenset({400, 403, 404, 405, 500, 501, 502, 503, 504})


def ist_now() -> str:
    return datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds")


def probe(url: str, timeout: float = 6.0) -> str:
    headers = {"User-Agent": "scheme-finder-url-health/0.1"}
    req = urllib.request.Request(url, method="HEAD", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return f"HEAD {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in _HEAD_RETRY_WITH_GET:
            try:
                get_req = urllib.request.Request(url, method="GET", headers=headers)
                with urllib.request.urlopen(get_req, timeout=timeout) as resp:
                    return f"GET {resp.status} (HEAD {e.code})"
            except urllib.error.HTTPError as e2:
                return f"FAIL HEAD {e.code}; GET HTTP {e2.code}"
            except Exception as e2:  # noqa: BLE001
                return f"FAIL HEAD {e.code}; GET {e2}"
        return f"FAIL HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        status = f"FAIL {e}"
        if host_of(url) in _GEOFENCED_INDIA_HOSTS:
            return f"GEO-FENCED (India-only host; verify from India) — {status}"
        return status


def host_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower() or url
    except Exception:  # noqa: BLE001
        return url


def _ok(status: str) -> bool:
    return (not tickets.is_failure_status(status)) and (
        status.startswith("HEAD 2")
        or status.startswith("GET 2")
        or status.upper().startswith("OK")
        or (" 200" in status and "FAIL" not in status.upper())
    )


def apply_ticket_updates(results: list[dict]) -> dict:
    opened = 0
    fixed = 0
    for item in results:
        url = str(item.get("url") or "")
        if not url.startswith("http"):
            continue
        status = str(item.get("status") or "")
        sid = item.get("scheme_id")
        if status.startswith("GEO-FENCED"):
            # Cannot judge from a non-Indian network — never open/resolve tickets.
            continue
        if tickets.is_failure_status(status) or not _ok(status):
            if tickets.is_failure_status(status):
                tickets.upsert_failure(
                    scheme_id=str(sid) if sid else None,
                    url=url,
                    http_or_error=status,
                    notes="From write_url_health_snapshot",
                    path=TICKETS,
                )
                opened += 1
        else:
            if tickets.resolve_ok(
                scheme_id=str(sid) if sid else None,
                url=url,
                http_or_error=status,
                path=TICKETS,
            ):
                fixed += 1
    return {"upserted_failures": opened, "resolved_fixed": fixed}


def collect_known_flaky_targets(schemes: list[dict]) -> list[dict]:
    """One representative scheme URL per known-flaky host."""
    found: dict[str, dict] = {}
    for s in schemes:
        if not isinstance(s, dict):
            continue
        url = s.get("official_source_url")
        if not isinstance(url, str) or not url.startswith("http"):
            continue
        h = host_of(url)
        for marker in _KNOWN_FLAKY_HOST_MARKERS:
            if marker in h and marker not in found:
                found[marker] = {"scheme_id": s.get("id"), "url": url, "host": h}
    return list(found.values())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--probe-sample",
        action="store_true",
        help="HEAD a short allowlisted sample (do not use as full catalogue hammer)",
    )
    ap.add_argument(
        "--probe-known-flaky",
        action="store_true",
        help="Short probe of historically flaky hosts only (max ~3, timeout 6s)",
    )
    ap.add_argument(
        "--from-freshness-json",
        type=Path,
        default=None,
        help="Optional JSON list of {host,status,scheme_id,url} from a freshness run",
    )
    ap.add_argument(
        "--no-tickets",
        action="store_true",
        help="Do not upsert/resolve url_tickets.jsonl",
    )
    ap.add_argument(
        "--seed-known-flaky-tickets",
        action="store_true",
        help="Pre-seed open tickets for known flaky hosts without probing "
        "(uses last known failure notes)",
    )
    args = ap.parse_args()

    flaky: list[dict] = []
    checked = 0
    ok = 0
    results_for_tickets: list[dict] = []

    if args.from_freshness_json and args.from_freshness_json.is_file():
        raw = json.loads(args.from_freshness_json.read_text(encoding="utf-8"))
        items = raw if isinstance(raw, list) else raw.get("results") or []
        for item in items:
            if not isinstance(item, dict):
                continue
            checked += 1
            status = str(item.get("status") or item.get("result") or "")
            row = {
                "host": item.get("host") or host_of(str(item.get("url") or "")),
                "status": status[:200],
                "scheme_id": item.get("scheme_id"),
                "url": item.get("url"),
            }
            results_for_tickets.append(row)
            if _ok(status):
                ok += 1
            else:
                flaky.append(row)
    elif (args.probe_sample or args.probe_known_flaky) and SCHEMES.is_file():
        schemes = json.loads(SCHEMES.read_text(encoding="utf-8"))
        by_id = {s["id"]: s for s in schemes if isinstance(s, dict) and "id" in s}
        targets: list[tuple[str | None, str]] = []
        if args.probe_sample:
            for sid in _PROBE_SAMPLE_IDS:
                s = by_id.get(sid)
                if not s:
                    continue
                url = s.get("official_source_url")
                if isinstance(url, str) and url.startswith("http"):
                    targets.append((sid, url))
        if args.probe_known_flaky:
            for t in collect_known_flaky_targets(schemes):
                targets.append((t.get("scheme_id"), t["url"]))

        # Dedupe by URL; limit concurrency
        seen_urls: set[str] = set()
        unique: list[tuple[str | None, str]] = []
        for sid, url in targets:
            if url in seen_urls:
                continue
            seen_urls.add(url)
            unique.append((sid, url))

        def _one(pair: tuple[str | None, str]) -> dict:
            sid, url = pair
            status = probe(url, timeout=6.0)
            return {
                "host": host_of(url),
                "status": status[:200],
                "scheme_id": sid,
                "url": url,
            }

        with ThreadPoolExecutor(max_workers=2) as pool:
            futs = [pool.submit(_one, p) for p in unique]
            for fut in as_completed(futs):
                row = fut.result()
                checked += 1
                results_for_tickets.append(row)
                if _ok(row["status"]):
                    ok += 1
                else:
                    flaky.append(row)
    elif args.seed_known_flaky_tickets and SCHEMES.is_file():
        schemes = json.loads(SCHEMES.read_text(encoding="utf-8"))
        for t in collect_known_flaky_targets(schemes):
            # Seed without live probe — historical notes only
            tickets.upsert_failure(
                scheme_id=str(t.get("scheme_id") or "") or None,
                url=t["url"],
                http_or_error="SEED historically flaky (DNS/404/5xx) — confirm with --probe-known-flaky",
                notes="Phase 4 foundation pre-seed; do not DOS. Re-probe before closing.",
                path=TICKETS,
            )
            flaky.append(
                {
                    "host": t["host"],
                    "status": "SEED historically flaky",
                    "scheme_id": t.get("scheme_id"),
                    "url": t["url"],
                }
            )
        checked = len(flaky)
        ok = 0
    else:
        flaky = []
        checked = 0
        ok = 0

    ticket_stats = {"upserted_failures": 0, "resolved_fixed": 0}
    if not args.no_tickets and results_for_tickets:
        ticket_stats = apply_ticket_updates(results_for_tickets)

    open_count = tickets.open_ticket_count(TICKETS)
    payload = {
        "generated_at": ist_now(),
        "timezone": "Asia/Kolkata",
        "checked_count": checked,
        "ok_count": ok,
        "flaky_hosts": flaky[:50],
        "open_url_tickets": open_count,
        "ticket_updates": ticket_stats,
        "note": (
            "Ops snapshot. Default run writes empty flaky list (no live probes). "
            "Use --probe-sample / --probe-known-flaky (short allowlist) or "
            "--from-freshness-json after scripts/scheme_freshness_check.py. "
            "Failures upsert data/url_tickets.jsonl; recoveries set status fixed. "
            "Never hammers full catalogue from CI."
        ),
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    OUT.write_text(text, encoding="utf-8")
    if FE_OUT.parent.is_dir():
        FE_OUT.write_text(text, encoding="utf-8")
    print(
        f"Wrote {OUT} checked={checked} ok={ok} flaky={len(flaky)} "
        f"open_tickets={open_count} ticket_updates={ticket_stats}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
