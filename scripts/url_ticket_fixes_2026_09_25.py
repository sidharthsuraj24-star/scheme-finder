#!/usr/bin/env python3
"""URL ticket fixes (2026-09-25) for the three open Phase 4 URL tickets.

- nsap-nfbs: nsap.nic.in is NXDOMAIN at NIC's authoritative DNS (host retired).
  Current official NSAP portal (Ministry of Rural Development, NSAP-PPS) is
  https://nsap.dord.gov.in/ — resolves via NIC DNS; HTTP 200 from India
  (check-host.net Mumbai/Rajpura nodes) but geo-restricted from non-Indian networks.
- ap-ntr-bharosa-oap: sspensions.ap.gov.in back up (GET 200 on /SSP/Home and
  /ssp/home/about, HEAD 302); ticket's 5xx was intermittent. Official source now the
  About page (same as sibling ap-ntr-bharosa-* rows); apply URL unchanged.
- sk-unmarried-women-pension: pensionscheme.sikkim.gov.in GET 200 (IIS returns 404
  to HEAD only — false positive from the HEAD-only probe). URL unchanged.

Official government URLs only; eligibility text unchanged except provenance notes.
Syncs data/ + frontend/data/ (byte-identical).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
LAST = "2026-09-25"

NSAP = "https://nsap.dord.gov.in/"
NSAP_GEO = (
    " URL ticket 2026-09-25: legacy host nsap.nic.in retired (NXDOMAIN); official NSAP "
    "portal is now nsap.dord.gov.in (Ministry of Rural Development). The portal "
    "geo-restricts non-Indian networks — verified HTTP 200 from India on 2026-09-25."
)
AP_NOTE = (
    " URL ticket 2026-09-25: sspensions.ap.gov.in is intermittently unavailable (HTTP 5xx "
    "seen 2026-09-24; HTTP 200 on 2026-09-25). If the portal is down, use Village/Ward "
    "Secretariat or the NTR Bharosa mirror at abdg.aptonline.in/SSP."
)
SK_NOTE = (
    " URL ticket 2026-09-25: portal verified live (HTTP 200 on GET; the server answers "
    "HEAD with 404, which caused a false 'broken link' ticket)."
)


def patch(s: dict) -> bool:
    sid = s.get("id")
    r = s.setdefault("eligibility_rules", {})
    if sid == "nsap-nfbs":
        s["apply_url"] = NSAP
        s["official_source_url"] = NSAP
        s["how_to_apply"]["en"] = (
            "Apply through State/UT NSAP implementing agency / local body as notified; "
            "see the NSAP portal (nsap.dord.gov.in, Ministry of Rural Development) for "
            "scheme status."
        )
        vn = r.get("verify_notes") or ""
        vn = vn.replace(
            "some nsap.nic.in FAQ text", "some legacy nsap.nic.in FAQ text"
        )
        if "URL ticket 2026-09-25" not in vn:
            vn = vn.rstrip() + NSAP_GEO
        r["verify_notes"] = vn
        r["verify"] = True
    elif sid == "ap-ntr-bharosa-oap":
        s["official_source_url"] = "https://sspensions.ap.gov.in/ssp/home/about"
        s["apply_url"] = "https://sspensions.ap.gov.in/SSP/Home"
        vn = r.get("verify_notes") or ""
        if "URL ticket 2026-09-25" not in vn:
            r["verify_notes"] = vn.rstrip() + AP_NOTE
        r["verify"] = True
    elif sid == "sk-unmarried-women-pension":
        vn = r.get("verify_notes") or ""
        if "URL ticket 2026-09-25" not in vn:
            r["verify_notes"] = vn.rstrip() + SK_NOTE
        r["verify"] = True
    else:
        return False
    s["last_verified"] = LAST
    return True


def main() -> None:
    schemes = json.loads(DATA.read_text(encoding="utf-8"))
    changed = [s["id"] for s in schemes if patch(s)]
    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload, encoding="utf-8")
    FE_DATA.write_text(payload, encoding="utf-8")
    print("PATCHED:", ", ".join(changed))


if __name__ == "__main__":
    main()
