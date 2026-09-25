#!/usr/bin/env python3
"""Resolve an open URL ticket (data/url_tickets.jsonl) after a catalogue URL fix.

Appends a `fixed` row keyed on (scheme_id, ticket url) via url_tickets.resolve_ok,
then syncs frontend/data/url_tickets.jsonl so both trees stay byte-identical.

Examples:
  python3 scripts/resolve_url_ticket.py --scheme-id nsap-nfbs \\
      --url https://nsap.nic.in/ --new-url https://nsap.dord.gov.in/ \\
      --http-or-error "GET 200 (India check-host)" --notes "Host moved"
  python3 scripts/resolve_url_ticket.py --scheme-id X --url U --probe

--probe re-probes (--new-url or --url) with the same HEAD→GET probe used by
write_url_health_snapshot.py; the ticket is only resolved if the probe is OK,
unless --force is given (e.g. geo-fenced hosts verified from another network —
say so in --notes).
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import url_tickets as ut  # noqa: E402

FE_TICKETS = REPO_ROOT / "frontend" / "data" / "url_tickets.jsonl"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--scheme-id", required=True)
    ap.add_argument("--url", required=True, help="URL recorded on the open ticket")
    ap.add_argument("--new-url", default=None, help="Replacement official URL (if changed)")
    ap.add_argument("--http-or-error", default=None, help="Evidence, e.g. 'GET 200'")
    ap.add_argument("--notes", default="Resolved after catalogue URL fix")
    ap.add_argument("--probe", action="store_true", help="Live re-probe before resolving")
    ap.add_argument("--force", action="store_true", help="Resolve even if --probe fails")
    ap.add_argument("--path", type=Path, default=ut.TICKETS_PATH)
    ap.add_argument("--no-sync", action="store_true", help="Do not copy to frontend/data")
    args = ap.parse_args()

    target = args.new_url or args.url
    evidence = args.http_or_error or "OK"
    if args.probe:
        from write_url_health_snapshot import _ok, probe  # noqa: WPS433

        status = probe(target, timeout=10.0)
        print(f"probe {target}: {status}")
        if not _ok(status) and not args.force:
            print("Probe not OK — ticket left open (use --force with a note if verified elsewhere).")
            return 2
        evidence = f"{status}" + (f"; {args.http_or_error}" if args.http_or_error else "")

    notes = args.notes
    if args.new_url and args.new_url != args.url:
        notes = f"URL replaced with {args.new_url}. {notes}"
    row = ut.resolve_ok(
        scheme_id=args.scheme_id,
        url=args.url,
        http_or_error=evidence,
        notes=notes,
        path=args.path,
    )
    if row is None:
        print("No open/investigating ticket for that scheme_id + url.")
        return 1
    print(f"resolved {row['ticket_id']} -> fixed")
    if not args.no_sync and args.path.resolve() == ut.TICKETS_PATH.resolve():
        shutil.copyfile(args.path, FE_TICKETS)
        print(f"synced {FE_TICKETS.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
