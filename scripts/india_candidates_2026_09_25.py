#!/usr/bin/env python3
"""India freshness-check candidates (2026-09-25): add PM-JANMAN; record queue outcomes.

Queue transitions were made with scripts/update_catalogue_candidate.py
(queued -> researching -> final status, each with an audit line). This script:
- adds scheme ``in-pm-janman`` (verify:true) to data/ + frontend/data/ schemes.json;
- sets ``scheme_id_if_present`` on cand-in-pm-janman now that the row exists.

Outcomes (details in data/catalogue_candidates.json and docs/DECISIONS.md):
- PM-JANMAN -> verified_add (in-pm-janman)
- PM-KUSUM -> deferred (scheme timeline ended 31.03.2026; PM KUSUM 2.0 in proposal stage)
- SVAMITVA -> deferred (household property card, but no individual application route)
- Jal Jeevan Mission / PM SHRI / PM e-Bus Sewa -> rejected (out of scope: infrastructure)

Official sources only: myscheme.gov.in, pib.gov.in (Ministry of Tribal Affairs),
sansad.in Lok Sabha answers. Never invents eligibility.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
CANDS = ROOT / "data" / "catalogue_candidates.json"
FE_CANDS = ROOT / "frontend" / "data" / "catalogue_candidates.json"
LAST = "2026-09-25"

PVTG_STATES = [
    "Andhra Pradesh", "Bihar", "Chhattisgarh", "Gujarat", "Jharkhand", "Karnataka",
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Odisha", "Rajasthan",
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand",
    "West Bengal", "Andaman and Nicobar Islands",
]
STATE_TAGS = [s.lower().replace(" ", "_") for s in PVTG_STATES if not s.startswith("Andaman")]

ML = "(EN — Malayalam review pending) "


def tri(en: str, hi: str | None = None) -> dict:
    return {"en": en, "hi": hi or en, "ml": ML + en}


DOCS = [
    "Aadhaar",
    "Bank account details",
    "PVTG / Scheduled Tribe community certificate (as required by the State)",
    "Inclusion in the PM-JANMAN habitation/household survey (PM Gati Shakti portal) or Gram Sabha list",
]

PM_JANMAN = {
    "id": "in-pm-janman",
    "scheme_name": tri(
        "PM-JANMAN (Pradhan Mantri Janjati Adivasi Nyaya Maha Abhiyan) — PVTG housing & basic services",
        "पीएम-जनमन (प्रधानमंत्री जनजाति आदिवासी न्याय महा अभियान) — पीवीटीजी आवास एवं मूलभूत सुविधाएँ",
    ),
    "description": tri(
        "Mission of the Ministry of Tribal Affairs with 9 line ministries for Particularly Vulnerable Tribal Group (PVTG) households and habitations: pucca houses, electricity, piped water, roads, health, education, nutrition and livelihood, delivered through convergence of existing schemes.",
        "जनजातीय कार्य मंत्रालय का मिशन: विशेष रूप से कमजोर जनजातीय समूह (PVTG) परिवारों/बस्तियों के लिए पक्का घर, बिजली, नल जल, सड़क, स्वास्थ्य, शिक्षा, पोषण और आजीविका।",
    ),
    "eligibility_rules": {
        "min_age": None,
        "max_age": None,
        "max_annual_income": None,
        "max_monthly_household_income": None,
        "occupations": [],
        "categories": ["ST", "PVTG"],
        "gender": None,
        "marital_status": [],
        "disability_required": False,
        "min_disability_percent": None,
        "land_ownership": None,
        "states": PVTG_STATES,
        "countries": ["India"],
        "nationwide": False,
        "notes": "Only households of the 75 notified Particularly Vulnerable Tribal Groups (PVTGs) in 18 States + Andaman & Nicobar Islands — a general ST household is NOT eligible unless it belongs to a PVTG. Beneficiary households are identified through the PM-JANMAN habitation survey (PM Gati Shakti) and Gram Sabha / Block verification. Housing component (PMAY-G norms): PVTG household living in a kaccha / dilapidated house; after the Feb 2026 relaxation the only exclusions are households that already own a pucca house or have a member in government service (PIB, Ministry of Tribal Affairs). No rupee income ceiling is published — max_annual_income null.",
        "verify": True,
        "verify_notes": "2026-09-25: myscheme.gov.in/schemes/pm-janman (official; geo-fenced from box); PIB releases of the Ministry of Tribal Affairs (11 Feb 2026 and 12 Mar 2026: mission period 2023-24 to 2025-26, Rs 24,104 crore; relaxed PMAY-G exclusions); Lok Sabha unstarred questions 1879 and 2031 answered 30.07.2026 (sansad.in) report the mission as ongoing with progress to 30.06.2026 (about 4.76 lakh of 4.90 lakh houses sanctioned). An extension to March 2027 is reported in the press only — confirm the current mission period and remaining housing targets with the District / Block office. implies_low_income not set: no income test; the PVTG + kaccha-house condition is the gate.",
    },
    "benefits": tri(
        "Pucca house under PMAY-G: Rs 2 lakh per house (about Rs 2.39 lakh including convergence for toilet and MGNREGS labour). Convergence for the same households/habitations: electricity connection (incl. off-grid solar), piped drinking water, LPG connection, Ayushman Bharat and PM-JAY cards, Aadhaar/ration/Jan Dhan saturation, mobile medical units, hostels, Anganwadi and multipurpose centres, and Van Dhan livelihood support.",
        "पीएमएवाई-जी के अंतर्गत पक्का घर: ₹2 लाख प्रति घर (अभिसरण सहित लगभग ₹2.39 लाख)। साथ में बिजली, नल जल, एलपीजी, आयुष्मान कार्ड, मोबाइल मेडिकल यूनिट, छात्रावास, आंगनवाड़ी व वन धन आजीविका सहायता।",
    ),
    "required_documents": {"en": DOCS, "hi": DOCS, "ml": [ML + d for d in DOCS]},
    "how_to_apply": tri(
        "No open online form: PVTG households are enumerated in the PM-JANMAN survey. Contact the Gram Panchayat, Block Development Office, ITDA/ITDP or District Tribal Welfare Office to confirm inclusion and to register for the housing and other components; IEC/Aadhaar saturation camps are also held in PVTG habitations.",
        "कोई खुला ऑनलाइन फ़ॉर्म नहीं: पीवीटीजी परिवारों का सर्वेक्षण से चयन। शामिल होने के लिए ग्राम पंचायत, ब्लॉक कार्यालय, आईटीडीए या ज़िला जनजातीय कल्याण कार्यालय से संपर्क करें।",
    ),
    "apply_url": "https://www.myscheme.gov.in/schemes/pm-janman",
    "office_type": "Ministry of Tribal Affairs (with MoRD / PMAY-G and line ministries); District / Block / ITDA",
    "official_source_url": "https://www.myscheme.gov.in/schemes/pm-janman",
    "tags": ["tribal", "pvtg", "st", "housing", "pm-janman", "rural", "low-income"] + STATE_TAGS,
    "last_verified": LAST,
    "nationwide": False,
}


def main() -> None:
    schemes = json.loads(DATA.read_text(encoding="utf-8"))
    ids = {s["id"]: i for i, s in enumerate(schemes)}
    assert not ({"central", "nationwide"} & set(PM_JANMAN["tags"]))
    if PM_JANMAN["id"] in ids:
        schemes[ids[PM_JANMAN["id"]]] = PM_JANMAN
        print("updated in-pm-janman")
    else:
        schemes.append(PM_JANMAN)
        print("added in-pm-janman")
    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload, encoding="utf-8")
    FE_DATA.write_text(payload, encoding="utf-8")

    cands = json.loads(CANDS.read_text(encoding="utf-8"))
    for c in cands["candidates"]:
        if c["id"] == "cand-in-pm-janman":
            c["scheme_id_if_present"] = "in-pm-janman"
        if c["id"] == "cand-in-svamitva":
            c["reason"] = c["reason"].replace(
                "scheme period ends around FY2025-26 extension",
                "survey phase is close to complete",
            )
    text = json.dumps(cands, indent=2, ensure_ascii=False) + "\n"
    CANDS.write_text(text, encoding="utf-8")
    FE_CANDS.write_text(text, encoding="utf-8")
    print(f"total={len(schemes)}")


if __name__ == "__main__":
    main()
