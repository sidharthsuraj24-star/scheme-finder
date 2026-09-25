#!/usr/bin/env python3
"""United Kingdom starter pack (2026-09-25): UK-wide + nation-specific schemes.

Official sources only: gov.uk (UK Government / DWP / HMRC / DfE / DESNZ / MHCLG),
mygov.scot + transport.gov.scot + gov.scot (Scottish Government / Social Security
Scotland / Transport Scotland), gov.wales (Welsh Government), nidirect.gov.uk
(Northern Ireland Executive). Rates are the 2026-27 figures shown on those pages
when checked on 2026-09-25.

Conventions (see docs/COUNTRY_UK.md):
- IDs use the ``gb-`` prefix (``uk-`` is already used by India/Uttarakhand rows).
- eligibility_rules.countries = ["United Kingdom"]; UK-wide rows have states [] and
  nationwide true; nation rows list nations ("England", "Scotland", "Wales",
  "Northern Ireland") with nationwide false.
- Tags: ``united_kingdom`` + nation tags (england/scotland/wales/northern_ireland).
  Never ``central`` / ``nationwide`` / ``federal`` (India/US pack buckets).
- India PRICE ICE 360 bands never apply. UK soft gate (matcher) is £60,000, only for
  implies_low_income rows with no numeric max. implies_low_income is set ONLY for
  genuinely means-tested schemes; non-means-tested rows keep max_annual_income null.
- max_annual_income is encoded only where the official page states a household
  income ceiling (Shared Ownership / First Homes £90k London cap, NI EMA £22.5k,
  NI Discretionary Support £29,741). Per-parent limits (e.g. £100k for childcare
  offers) are NOT household caps and stay in notes.

Syncs data/ + frontend/data/ (byte-identical) and updates catalogue_meta.
Data rows live in uk_starter_pack_2026_09_25_rows.py.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from uk_starter_pack_2026_09_25_rows import ADDS, LAST  # noqa: E402

DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
ISO = "2026-09-25T13:00:00+05:30"

META_APPEND = (
    "; United Kingdom starter pack (2026-09-25): UK added as a catalogue country "
    "(ids gb-*; currency £; nations England/Scotland/Wales/Northern Ireland as regions; "
    "packs uk-wide + uk-england/uk-scotland/uk-wales/uk-northern-ireland). All-income "
    "coverage — means-tested (Universal Credit, Pension Credit, Help to Save, Healthy "
    "Start, Scottish Child Payment, Best Start, Council Tax Reduction, Warm Home Discount) "
    "plus universal / middle / high-income-eligible (Child Benefit with HICBC note, "
    "Tax-Free Childcare, 30 hours, State Pension, ISA / Lifetime ISA / Junior ISA, "
    "Marriage Allowance, pension tax relief, SDLT first-time buyer relief, Boiler Upgrade "
    "Scheme, disability benefits PIP/ADP/AA/PADP). Official gov.uk / mygov.scot / "
    "transport.gov.scot / gov.scot / gov.wales / nidirect.gov.uk only; 2026-27 rates; "
    "last_verified 2026-09-25; India PRICE bands never applied; UK soft gate £60,000 "
    "(catalogue heuristic, HICBC anchor) only for implies_low_income rows without numeric "
    "max. Honest SKIPs: Help to Buy Equity Loan (closed 2023), Help to Buy ISA (closed to "
    "new savers 2019), tax credits (ended April 2025), Child Trust Fund (closed), Nest "
    "Wales / NI rate relief / NI free school meals / NI Affordable Warmth / Scottish free "
    "prescriptions (official page not confirmed this pass). URL tickets 2026-09-25: "
    "nsap-nfbs moved to nsap.dord.gov.in; ap-ntr-bharosa-oap and "
    "sk-unmarried-women-pension re-verified."
)


def main() -> None:
    schemes: list[dict] = json.loads(DATA.read_text(encoding="utf-8"))
    by_id = {s["id"]: i for i, s in enumerate(schemes)}
    ids = [s["id"] for s in ADDS]
    assert len(ids) == len(set(ids)), "duplicate ids in ADDS"
    added, updated = [], []
    for s in ADDS:
        sid = s["id"]
        assert sid.startswith("gb-"), sid
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
        "India + selected other countries (curated; not worldwide).",
        "India + selected other countries incl. United States and United Kingdom (curated; not worldwide).",
    )
    if "United Kingdom starter pack (2026-09-25)" not in scope:
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
