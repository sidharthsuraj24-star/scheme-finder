#!/usr/bin/env python3
"""Canada starter pack (2026-09-25): federal + provincial/territorial schemes.

Official sources only: canada.ca (Canada Revenue Agency, Employment and Social
Development Canada / Service Canada) and official provincial/territorial government
sites (alberta.ca, gov.bc.ca, gov.mb.ca, gnb.ca, novascotia.ca, gov.nt.ca,
ontario.ca, quebec.ca, retraitequebec.gouv.qc.ca, revenuquebec.ca, saskatchewan.ca,
yukon.ca). Rates are the July 2026 – June 2027 benefit-year (or 2026) figures shown
on those pages when checked on 2026-09-25. All amounts are Canadian dollars (C$ / CAD).

Conventions (see docs/COUNTRY_CANADA.md):
- IDs use the ``can-`` prefix (``ca-`` is already used by US/California rows).
  Provincial rows are ``can-<province code>-…`` (e.g. can-on-…, can-qc-…).
- eligibility_rules.countries = ["Canada"]; all-Canada federal rows have states [] and
  nationwide true; provincial/territorial rows list their province with nationwide
  false. Federal rows that exclude a province (CPP and EI maternity/parental outside
  Quebec; Canada Student Grants outside QC/NT/NU) list the other provinces explicitly.
- Tags: ``canada`` (+ ``canada_federal`` for federal rows, + province tags for
  provincial rows). Never ``central`` / ``nationwide`` / ``federal`` (India/US buckets).
- India PRICE ICE 360 bands never apply; the US $60k gate never applies. Canada soft
  gate (matcher) is C$58,523 — the 2026 top of the lowest federal tax bracket, also the
  ESDC CLB / additional-CESG low-income line — used ONLY for implies_low_income rows
  with no numeric max. Official ceilings are encoded as max_annual_income (highest
  published cut-off where it varies by household; smaller-household figures in notes).
  Phase-outs that reach middle incomes (CCB, BC Family Benefit, OTB, OCB, ACFB) keep
  implies_low_income false and max_annual_income null.

Syncs data/ + frontend/data/ (byte-identical) and updates catalogue_meta.
Rows live in canada_starter_pack_2026_09_25_{rows,federal,provincial}.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from canada_starter_pack_2026_09_25_rows import ADDS, LAST  # noqa: E402

DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
ISO = "2026-09-25T17:00:00+05:30"

META_APPEND = (
    "; Canada starter pack (2026-09-25): Canada added as a catalogue country (ids can-*; "
    "ca-* is California; currency C$ / CAD; 13 provinces and territories as regions; packs "
    "canada-federal + canada-<province>). All-income coverage — means-tested (GIS, "
    "Allowance, Canada Workers Benefit, Canada Disability Benefit, CGEB, CLB, provincial "
    "child benefits, AISH, ODSP, SAID) plus universal / middle / high-income-eligible "
    "(CCB, OAS with recovery-tax note, CPP/QPP, EI regular / maternity / parental, QPIP, "
    "DTC, RDSP, RESP + CESG, TFSA, RRSP, FHSA, Home Buyers' Plan, Quebec Family "
    "Allowance). Official canada.ca (CRA / ESDC) and provincial/territorial government "
    "sites only; July 2026 – June 2027 rates; last_verified 2026-09-25; India PRICE bands "
    "and the US $60k gate never applied; Canada soft gate C$58,523 (2026 lowest federal "
    "bracket / ESDC CLB line; catalogue heuristic) only for implies_low_income rows "
    "without numeric max. Honest SKIPs: Canada Carbon Rebate (ended April 2025), GST/HST "
    "credit (renamed CGEB July 2026 — added as CGEB), BC Climate Action Tax Credit (ended "
    "with BC consumer carbon tax), Nunavut Senior Fuel Subsidy (official page not "
    "reachable), Nova Scotia HARP (2026-27 terms not yet published). India candidates "
    "2026-09-25: PM-JANMAN added (in-pm-janman, verify); PM-KUSUM + SVAMITVA deferred; "
    "Jal Jeevan Mission, PM SHRI, PM e-Bus Sewa rejected as infrastructure."
)


def main() -> None:
    schemes: list[dict] = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {s["id"]: i for i, s in enumerate(schemes)}
    added, updated = [], []
    for s in ADDS:
        sid = s["id"]
        assert sid.startswith("can-"), sid
        if sid in by_id:
            schemes[by_id[sid]] = s
            updated.append(sid)
        else:
            schemes.append(s)
            added.append(sid)

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload, encoding="utf-8")
    FE_DATA.write_text(payload, encoding="utf-8")

    meta = json.loads(META.read_text(encoding="utf-8"))
    meta["updated_as_of"] = LAST
    meta["updated_as_of_iso"] = ISO
    meta["scheme_count"] = len(schemes)
    scope = meta.get("scope", "")
    scope = scope.replace(
        "incl. United States and United Kingdom (curated; not worldwide).",
        "incl. United States, United Kingdom and Canada (curated; not worldwide).",
    )
    if "Canada starter pack (2026-09-25)" not in scope:
        scope = scope.rstrip().rstrip(".") + META_APPEND
    meta["scope"] = scope
    meta_payload = json.dumps(meta, indent=2, ensure_ascii=False) + "\n"
    META.write_text(meta_payload, encoding="utf-8")
    FE_META.write_text(meta_payload, encoding="utf-8")

    print(f"total={len(schemes)} added={len(added)} updated={len(updated)}")
    print("ADDED:", ", ".join(added) or "(none)")
    print("UPDATED:", ", ".join(updated) or "(none)")


if __name__ == "__main__":
    main()
