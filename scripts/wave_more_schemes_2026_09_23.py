#!/usr/bin/env python3
"""Catalogue update 2026-09-23 wave 2: Ujjwala, PMAY, Mudra, SVANidhi, NFSA,
social security (PMSBY/PMJJBY/APY/Sukanya/NPS/Stand-Up/eShram), PMFBY/KCC/JSY,
PM RAHAT; US Summer EBT, VA disability, SSA survivors, FEMA IA, Free File/VITA.

Authoritative research: /workspace/more-schemes-verify-report.md
Official sources only; verify=true where amounts/limits vary. Never invent eligibility.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
LAST = "2026-09-23"
ISO = "2026-09-23T10:00:00+05:30"
ML_PREFIX = "(EN — Malayalam review pending) "

EXPECTED_IDS = [
    "in-pm-ujjwala",
    "in-pmay-u-2",
    "in-pmay-g",
    "in-pm-svanidhi",
    "in-mudra",
    "in-nfsa-onorc",
    "in-pmsby",
    "in-pmjjby",
    "in-apy",
    "in-sukanya-samriddhi",
    "in-nps-all-citizen",
    "in-standup-india",
    "in-eshram",
    "in-pmfby",
    "in-kisan-credit-card",
    "in-janani-suraksha",
    "in-pm-rahat",
    "us-summer-ebt",
    "us-va-disability",
    "us-ssa-survivors",
    "us-fema-ia",
    "us-free-file-vita",
]


def L(en: str, hi: str | None = None, ml: str | None = None, *, india_ml: bool = False) -> dict:
    if india_ml:
        return {"en": en, "hi": hi or en, "ml": ml if ml is not None else ML_PREFIX + en}
    return {"en": en, "ml": ml or en, "hi": hi or en}


def docs(items: list[str], *, india_ml: bool = False) -> dict:
    if india_ml:
        return {
            "en": items,
            "hi": items,
            "ml": [ML_PREFIX + i if not i.startswith("(EN") else i for i in items],
        }
    return {"en": items, "ml": items, "hi": items}


def base_rules(**kwargs) -> dict:
    r = {
        "min_age": None,
        "max_age": None,
        "max_annual_income": None,
        "max_monthly_household_income": None,
        "occupations": [],
        "categories": [],
        "gender": None,
        "marital_status": [],
        "disability_required": False,
        "min_disability_percent": None,
        "land_ownership": None,
        "states": ["All India"],
        "countries": ["India"],
        "nationwide": True,
        "notes": "",
        "verify": True,
        "verify_notes": "",
    }
    r.update(kwargs)
    return r


def us_rules(**kwargs) -> dict:
    r = {
        "min_age": None,
        "max_age": None,
        "max_annual_income": None,
        "max_monthly_household_income": None,
        "occupations": [],
        "categories": [],
        "gender": None,
        "marital_status": [],
        "disability_required": False,
        "min_disability_percent": None,
        "land_ownership": None,
        "states": [],
        "countries": ["United States"],
        "nationwide": True,
        "notes": "",
        "verify": True,
        "verify_notes": "",
    }
    r.update(kwargs)
    return r


def india_scheme(
    id: str,
    name_en: str,
    name_hi: str,
    desc_en: str,
    desc_hi: str,
    benefits_en: str,
    benefits_hi: str,
    docs_en: list[str],
    how_en: str,
    how_hi: str,
    apply_url: str,
    official: str,
    office: str,
    tags: list[str],
    erules: dict,
    *,
    nationwide_top: bool = True,
) -> dict:
    return {
        "id": id,
        "scheme_name": L(name_en, hi=name_hi, india_ml=True),
        "description": L(desc_en, hi=desc_hi, india_ml=True),
        "eligibility_rules": erules,
        "benefits": L(benefits_en, hi=benefits_hi, india_ml=True),
        "required_documents": docs(docs_en, india_ml=True),
        "how_to_apply": L(how_en, hi=how_hi, india_ml=True),
        "apply_url": apply_url,
        "office_type": office,
        "official_source_url": official,
        "tags": tags,
        "last_verified": LAST,
        "nationwide": nationwide_top,
    }


def us_scheme(
    id: str,
    name_en: str,
    name_hi: str,
    desc_en: str,
    benefits_en: str,
    docs_en: list[str],
    how_en: str,
    apply_url: str,
    official: str,
    office: str,
    tags: list[str],
    erules: dict,
) -> dict:
    return {
        "id": id,
        "scheme_name": L(name_en, hi=name_hi),
        "description": L(desc_en),
        "eligibility_rules": erules,
        "benefits": L(benefits_en),
        "required_documents": docs(docs_en),
        "how_to_apply": L(how_en),
        "apply_url": apply_url,
        "official_source_url": official,
        "last_verified": LAST,
        "office_type": office,
        "tags": tags,
    }


NEW: list[dict] = []

# --- Wave A ---
NEW.append(
    india_scheme(
        "in-pm-ujjwala",
        "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "प्रधानमंत्री उज्ज्वला योजना (पीएमयूवाई)",
        "Central scheme providing LPG connections to adult women from poor households who have no existing LPG connection in the household from any Oil Marketing Company (OMC).",
        "गरीब परिवारों की वयस्क महिलाओं को एलपीजी कनेक्शन; परिवार में किसी भी ओएमसी से मौजूदा कनेक्शन नहीं होना चाहिए।",
        "Free/subsidized LPG connection package (security deposit of cylinder, regulator, hose, installation/admin; first refill and hot plate per OMC/KYC scheme text). Exact inclusions can vary by OMC/release — confirm on pmuy.gov.in.",
        "मुफ्त/सब्सिडीयुक्त एलपीजी कनेक्शन पैकेज (सिलेंडर जमा, रेगुलेटर, होज़, इंस्टॉलेशन; पहली रिफिल व हॉट प्लेट ओएमसी/केवाईसी पाठानुसार)। सटीक समावेशन सत्यापित करें।",
        [
            "KYC documents",
            "Aadhaar (applicant and adult family members as required on composition document)",
            "Ration card / state family-composition document (or Annexure I self-declaration for migrants)",
            "Bank account details",
            "Signed deprivation declaration in prescribed format",
            "Proof of address if Aadhaar address differs (PoA)",
        ],
        "Apply online at https://pmuy.gov.in/ (ujjwala2) or via LPG distributor; CSC may charge ₹20 (FAQ).",
        "pmuy.gov.in पर ऑनलाइन या एलपीजी वितरक के माध्यम से आवेदन; सीएससी शुल्क FAQ अनुसार।",
        "https://pmuy.gov.in/ujjwala2.html",
        "https://pmuy.gov.in/",
        "Ministry of Petroleum and Natural Gas / OMCs / LPG distributors",
        ["lpg", "ujjwala", "women", "energy", "central", "nationwide", "subsidy"],
        base_rules(
            min_age=18,
            gender="female",
            categories=["poor_household", "no_lpg_connection"],
            notes=(
                "Adult woman ≥18; no other LPG connection in the household from any OMC; belongs to a poor household based on signed deprivation declaration (prescribed format). "
                "Documents per portal FAQ: KYC, Aadhaar, ration/family composition (or migrant Annexure I), bank details, deprivation declaration, PoA if needed."
            ),
            verify_notes="2026-09-23: pmuy.gov.in / ujjwala2 FAQs. Connection package inclusions and any CSC fee can vary — verify on live portal.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-pmay-u-2",
        "Pradhan Mantri Awas Yojana – Urban 2.0 (PMAY-U 2.0)",
        "प्रधानमंत्री आवास योजना – शहरी 2.0 (पीएमएवाई-यू 2.0)",
        "Urban housing assistance (2024–2029) for EWS/LIG/MIG families that do not own a pucca house anywhere in India, via BLC, AHP, ARH, and Interest Subsidy Scheme (ISS) verticals.",
        "शहरी ईडब्ल्यूएस/एलआईजी/एमआईजी परिवारों हेतु आवास सहायता (2024–2029); भारत में कहीं भी पक्का मकान नहीं होना चाहिए।",
        "Central assistance for construct/purchase/rent varies by vertical and State/UT (e.g. BLC/AHP central share cited in FAQ tables around ₹1.50–2.50 lakh per unit); ISS interest subsidy up to ₹1.80 lakh. Confirm current FAQ/guidelines.",
        "ऊर्ध्वाधर व राज्य/यूटी के अनुसार केंद्रीय सहायता; आईएसएस ब्याज सब्सिडी अधिकतम ₹1.80 लाख तक (FAQ)। सटीक राशि सत्यापित करें।",
        [
            "Identity and residence proof",
            "Income documents for EWS/LIG/MIG band",
            "Self-declaration of no pucca house in India in applicant/family name",
            "Bank details",
            "Other documents as per Unified Web Portal / ULB",
        ],
        "Apply via Unified Web Portal / CSC / Urban Local Body (ULB). See pmay-urban.gov.in and PMAY MIS FAQ.",
        "एकीकृत वेब पोर्टल / सीएससी / नगर निकाय के माध्यम से आवेदन।",
        "https://pmay-urban.gov.in/",
        "https://pmay-urban.gov.in/pmay-u-2.0-guidelines",
        "Ministry of Housing and Urban Affairs / ULBs",
        ["housing", "urban", "pmay", "ews", "lig", "mig", "central", "nationwide"],
        base_rules(
            categories=["ews", "lig", "mig", "urban"],
            max_annual_income=900000,
            notes=(
                "Urban EWS / LIG / MIG families with no pucca house in applicant’s or any family member’s name anywhere in India. "
                "Income bands (scheme FAQ): EWS up to ₹3 lakh; LIG ₹3–6 lakh; MIG ₹6–9 lakh annual household income. "
                "Not eligible if availed Central/State/ULB housing benefit in last 20 years. Implementation 2024–2029. "
                "Preference groups in guidelines (widows, PwD, SC/ST, street vendors under SVANidhi, Vishwakarma artisans, etc.). "
                "max_annual_income encodes MIG upper FAQ band only as a soft ceiling; actual band is category-specific — verify=true."
            ),
            verify_notes="2026-09-23: pmay-urban.gov.in + pmaymis FAQ. Central assistance amounts and preference lists vary by vertical/State — confirm live FAQ/guidelines.",
            implies_low_income=True,
        ),
    )
)

NEW.append(
    india_scheme(
        "in-pmay-g",
        "Pradhan Mantri Awaas Yojana – Gramin (PMAY-G)",
        "प्रधानमंत्री आवास योजना – ग्रामीण (पीएमएवाई-जी)",
        "Rural housing assistance for houseless households or those living in kutcha/dilapidated dwellings, identified via SECC/Awaas+ deprivation criteria with Gram Sabha verification and exclusion filters.",
        "ग्रामीण बेघर या कच्चे/जीर्ण आवास वाले परिवारों हेतु सहायता; एसईसीसी/आवास+ व ग्राम सभा सत्यापन।",
        "Unit assistance commonly cited in official materials as about ₹1.20 lakh (plains) / ₹1.30 lakh (hilly/difficult/NER) — confirm exact current figures from live DoRD guidelines before advising.",
        "इकाई सहायता अक्सर मैदानी क्षेत्रों में लगभग ₹1.20 लाख / पहाड़ी-कठिन/पूर्वोत्तर में ₹1.30 लाख बताई जाती है — वर्तमान दिशानिर्देश से सत्यापित करें।",
        [
            "Identity proof (Aadhaar as required by State)",
            "SECC / Awaas+ survey recognition / Gram Sabha verification trail",
            "Bank account for DBT",
            "Land / house site details as required by State RD",
        ],
        "Through Gram Panchayat / Awaas+ survey / State rural development channels (not the urban PMAYMIS portal).",
        "ग्राम पंचायत / आवास+ सर्वे / राज्य ग्रामीण विकास चैनलों के माध्यम से।",
        "https://pmayg.dord.gov.in/",
        "https://pmayg.dord.gov.in/",
        "Ministry of Rural Development / State RD / Gram Panchayat",
        ["housing", "rural", "pmay", "central", "nationwide", "dbt"],
        base_rules(
            categories=["rural", "houseless", "kutcha_dwelling"],
            notes=(
                "Rural households that are houseless or live in kutcha/dilapidated dwellings, identified via SECC / Awaas+ deprivation criteria with Gram Sabha verification. "
                "Exclusion filters apply (e.g. government employment, income-tax payer, high KCC limit, specified assets — encode only from current DoRD framework). "
                "Distinct from PMAY-U; urban/rural jurisdiction decides."
            ),
            verify_notes="2026-09-23: pmayg.dord.gov.in. Exact unit assistance ₹ amounts and exclusion list must be confirmed from current DoRD framework PDF/guidelines.",
            implies_low_income=True,
        ),
    )
)

NEW.append(
    india_scheme(
        "in-pm-svanidhi",
        "PM SVANidhi (Street Vendors’ AtmaNirbhar Nidhi)",
        "पीएम स्वनिधि (स्ट्रीट वेंडर्स आत्मनिर्भर निधि)",
        "Collateral-free working-capital loans for street vendors in ULBs / census towns / peri-urban areas, with UPI-linked incentives and lending extended through 31 Mar 2030 (Cabinet).",
        "शहरी/पेरी-अर्बन स्ट्रीट वेंडर्स हेतु बिना जमानत कार्यशील पूंजी ऋण; यूपीआई प्रोत्साहन; ऋण अवधि 31 मार्च 2030 तक विस्तार।",
        "Collateral-free working-capital tranches (restructured bands commonly up to ₹15,000 / ₹25,000 / ₹50,000 per MoHUA/app guidance); UPI-linked RuPay credit card after 2nd repayment; digital cashback incentives (Cabinet note has cited up to ₹1,600). Confirm live portal bands.",
        "बिना जमानत कार्यशील पूंजी किश्तें (समान्यतः ₹15k/₹25k/₹50k बैंड); दूसरी चुकौती के बाद यूपीआई-रुपे कार्ड; डिजिटल कैशबैक — पोर्टल पर सत्यापित करें।",
        [
            "Certificate of Vending (CoV) / vendor ID card / digital Letter of Recommendation (LoR via PMS Portal only; manual LoR invalid)",
            "Bank account with mandatory unique UPI ID linked to vendor account",
            "Identity / KYC as required by lending institution",
        ],
        "Apply on PMS Portal / app / ULB / Block / CSC: https://pmsvanidhi.mohua.gov.in/",
        "पीएमएस पोर्टल / ऐप / यूएलबी / ब्लॉक / सीएससी के माध्यम से आवेदन।",
        "https://pmsvanidhi.mohua.gov.in/",
        "https://pmsvanidhi.mohua.gov.in/",
        "Ministry of Housing and Urban Affairs / ULBs / lending institutions",
        ["street_vendor", "loan", "urban", "svanidhi", "central", "nationwide", "upi"],
        base_rules(
            occupations=["street_vendor"],
            categories=["street_vendor"],
            notes=(
                "Street vendors in ULBs / census towns / peri-urban areas with valid CoV / ID card / digital LoR (LoR only via PMS Portal). "
                "LoR-cum-loan path for those without CoV/ID. Mandatory unique UPI ID linked to vendor bank account. "
                "Lending period extended through 31 Mar 2030 per Cabinet note. Lender assessment applies."
            ),
            verify_notes="2026-09-23: pmsvanidhi.mohua.gov.in + MoHUA/Cabinet extension notes. Tranche amounts and cashback caps — confirm on live portal.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-mudra",
        "Pradhan Mantri MUDRA Yojana (PMMY)",
        "प्रधानमंत्री मुद्रा योजना (पीएमएमवाई)",
        "Collateral-free institutional credit for micro enterprises for non-agricultural purposes (including agri-allied such as poultry, dairy, beekeeping), via banks/NBFCs/MFIs under Shishu/Kishore/Tarun/Tarun Plus categories.",
        "सूक्ष्म उद्यमों हेतु बिना जमानत संस्थागत ऋण (गैर-कृषि व कृषि-संबद्ध); शिशु/किशोर/तरुण/तरुण प्लस श्रेणियाँ।",
        "Category loan bands (DFS/MUDRA): Shishu ≤₹50,000; Kishore >₹50,000–₹5 lakh; Tarun >₹5–₹10 lakh; Tarun Plus >₹10–₹20 lakh after successful Tarun repayment (w.e.f. 24.10.2024). Amount subject to lender credit assessment.",
        "शिशु ≤₹50,000; किशोर >₹50k–₹5 लाख; तरुण >₹5–₹10 लाख; तरुण प्लस >₹10–₹20 लाख (सफल तरुण चुकौती के बाद)। ऋणदाता मूल्यांकन लागू।",
        [
            "Identity and address KYC",
            "Business/purpose details for micro enterprise",
            "Bank account",
            "Documents as required by member lending institution / Jan Samarth / common MUDRA form",
        ],
        "Apply through member lending institutions, Jan Samarth, or mudra.org.in common form.",
        "सदस्य ऋणदाता संस्था / जन समर्थ / mudra.org.in सामान्य फॉर्म के माध्यम से।",
        "https://www.mudra.org.in/",
        "https://financialservices.gov.in/pradhan-mantri-mudra-yojana-pmmy",
        "Department of Financial Services / MUDRA / member banks-NBFCs-MFIs",
        ["mudra", "loan", "micro_enterprise", "central", "nationwide", "credit"],
        base_rules(
            occupations=["micro_enterprise", "self_employed", "agri_allied"],
            categories=["micro_enterprise"],
            notes=(
                "Access to institutional collateral-free credit for micro enterprises; purposes non-agricultural including agri-allied (poultry, dairy, beekeeping, etc.); term loan + working capital. "
                "Lender credit assessment applies — do not invent personal eligibility beyond scheme purpose."
            ),
            verify_notes="2026-09-23: financialservices.gov.in PMMY + mudra.org.in. Category ceilings and Tarun Plus rules — confirm current DFS/MUDRA pages.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-nfsa-onorc",
        "National Food Security Act / TPDS + One Nation One Ration Card (ONORC)",
        "राष्ट्रीय खाद्य सुरक्षा अधिनियम / टीपीडीएस + वन नेशन वन राशन कार्ड (ओएनओआरसी)",
        "National food-security entitlement under NFSA (Priority / Antyodaya Anna Yojana households as identified by States/UTs) plus ONORC portability to draw entitled foodgrain at any ePoS Fair Price Shop nationwide.",
        "एनएफएसए के अंतर्गत प्राथमिकता/अंत्योदय परिवारों हेतु खाद्यान्न पात्रता; ओएनओआरसी से देशभर किसी भी ईपीओएस एफपीएस पर पोर्टेबिलिटी।",
        "Subsidised foodgrain entitlements under NFSA (AAY vs priority issue prices/kg as per DoFPD/NFSA). ONORC allows drawing entitled grain at any ePoS FPS with ration card / Aadhaar authentication. Exact kg rates vary — verify.",
        "एनएफएसए के अंतर्गत सब्सिडीयुक्त खाद्यान्न; ओएनओआरसी से किसी भी ईपीओएस एफपीएस पर आहरण। किग्रा/दर राज्य-केंद्र नियमों से सत्यापित करें।",
        [
            "Valid NFSA ration card (issued by State/UT)",
            "Aadhaar authentication at ePoS (as required)",
            "Mera Ration app / IMPDS tools for portability as applicable",
        ],
        "New ration cards are issued by State/UT food departments (not a single national application form). For ONORC portability and grievances see nfsa.gov.in, impds.nic.in, helpline 14445, and Mera Ration app.",
        "नए राशन कार्ड राज्य/यूटी खाद्य विभाग जारी करते हैं। ओएनओआरसी/शिकायत: nfsa.gov.in, impds.nic.in, हेल्पलाइन 14445, मेरा राशन ऐप।",
        "https://nfsa.gov.in/",
        "https://nfsa.gov.in/",
        "Department of Food and Public Distribution / State Food Departments / FPS",
        ["food", "ration", "nfsa", "onorc", "tpds", "central", "nationwide"],
        base_rules(
            categories=["priority_household", "aay", "nfsa"],
            notes=(
                "Priority / AAY households under NFSA as identified by States/UTs (state ration-card rules). "
                "ONORC: NFSA beneficiaries can draw entitled foodgrain at any ePoS FPS nationwide with ration card / Aadhaar authentication. "
                "Application for new ration cards is state-run; this national entry covers entitlement + ONORC portability + grievance channels."
            ),
            verify_notes="2026-09-23: nfsa.gov.in + impds.nic.in. Issue prices/kg entitlements and state identification rules vary — verify with DoFPD/State food department.",
            implies_low_income=True,
        ),
    )
)

# --- Wave B ---
NEW.append(
    india_scheme(
        "in-pmsby",
        "Pradhan Mantri Suraksha Bima Yojana (PMSBY)",
        "प्रधानमंत्री सुरक्षा बीमा योजना (पीएमएसबीवाई)",
        "Government-backed accidental death and disability insurance for bank/Post Office account holders aged 18–70, with annual auto-debit premium.",
        "बैंक/डाकघर खाताधारकों (18–70 वर्ष) हेतु दुर्घटना मृत्यु/विकलांगता बीमा; वार्षिक ऑटो-डेबिट प्रीमियम।",
        "Accidental death/disability cover commonly ₹2 lakh (death/total disability) / ₹1 lakh (partial) per FAQ; premium commonly ₹20/year (or as revised). Confirm current FAQ on jansuraksha.gov.in.",
        "दुर्घटना कवर सामान्यतः ₹2 लाख / आंशिक ₹1 लाख; प्रीमियम सामान्यतः ₹20/वर्ष — जानसुरक्षा FAQ से सत्यापित करें।",
        [
            "Individual bank or Post Office savings account",
            "Consent for auto-debit of premium",
            "KYC / nomination as required by bank/PO",
        ],
        "Enrol at bank branch / Business Correspondent / Post Office or via bank website. One enrolment despite multiple accounts.",
        "बैंक शाखा / बीसी / डाकघर या बैंक वेबसाइट से नामांकन।",
        "https://jansuraksha.gov.in/",
        "https://financialservices.gov.in/pmsby",
        "Department of Financial Services / banks / Post Offices",
        ["insurance", "accident", "pmsby", "jansuraksha", "central", "nationwide"],
        base_rules(
            min_age=18,
            max_age=70,
            notes=(
                "Individual bank/Post Office account holders age 18–70; one enrolment despite multiple accounts; consent to auto-debit. "
                "Premium and sum assured per current Jan Suraksha / DFS FAQ."
            ),
            verify_notes="2026-09-23: jansuraksha.gov.in + DFS PMSBY. Premium ₹20 and cover amounts — confirm current FAQ PDF.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-pmjjby",
        "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
        "प्रधानमंत्री जीवन ज्योति बीमा योजना (पीएमजेजेबीवाई)",
        "Government-backed life insurance for bank/Post Office account holders who join between ages 18–50; risk cover can continue to 55 with premiums if joined before 50.",
        "बैंक/डाकघर खाताधारकों हेतु जीवन बीमा; प्रवेश आयु 18–50; प्रीमियम के साथ कवर 55 तक जारी रह सकता है।",
        "Life cover commonly ₹2 lakh; annual premium cited in FAQ (e.g. ₹436) — confirm current premium on jansuraksha / DFS FAQ before advising.",
        "जीवन कवर सामान्यतः ₹2 लाख; वार्षिक प्रीमियम FAQ अनुसार (उदा. ₹436) — वर्तमान दर सत्यापित करें।",
        [
            "Individual bank or Post Office savings account",
            "Consent for auto-debit",
            "KYC / nomination as required",
            "Age proof showing join age 18–50",
        ],
        "Enrol at bank / BC / Post Office. One account only for cover.",
        "बैंक / बीसी / डाकघर से नामांकन।",
        "https://jansuraksha.gov.in/",
        "https://jansuraksha.gov.in/",
        "Department of Financial Services / banks / Post Offices / life insurers",
        ["insurance", "life", "pmjjby", "jansuraksha", "central", "nationwide"],
        base_rules(
            min_age=18,
            max_age=50,
            notes=(
                "Individual bank/PO account holders age 18–50 at join; risk cover can continue to 55 with premiums if joined before 50; "
                "one account only; auto-debit. Life cover and premium per current FAQ."
            ),
            verify_notes="2026-09-23: jansuraksha.gov.in PMJJBY FAQ. Confirm current annual premium (FAQ has cited ₹436) and cover terms.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-apy",
        "Atal Pension Yojana (APY)",
        "अटल पेंशन योजना (एपीवाई)",
        "Guaranteed pension scheme for bank account holders aged 18–40 who are not income-tax payers; contribution varies by chosen pension amount; pension starts at age 60.",
        "18–40 वर्ष के बैंक खाताधारक जो आयकरदाता नहीं; चुनी पेंशन राशि के अनुसार अंशदान; 60 वर्ष पर गारंटीकृत पेंशन।",
        "Guaranteed pension at age 60 per chosen contribution slab (PFRDA/DFS tables). Exact monthly contribution and pension amounts — verify on PFRDA/Jan Suraksha.",
        "60 वर्ष पर गारंटीकृत पेंशन (अंशदान स्लैब अनुसार)। सटीक राशि पीएफआरडीए/जानसुरक्षा से सत्यापित करें।",
        [
            "Bank savings account",
            "Aadhaar / KYC",
            "Self-declaration of not being an income-tax payer (as required)",
            "Nomination details",
        ],
        "Enrol through bank / Jan Suraksha channels; see jansuraksha.gov.in and pfrda.org.in.",
        "बैंक / जानसुरक्षा चैनलों से नामांकन।",
        "https://jansuraksha.gov.in/",
        "https://www.pfrda.org.in/",
        "PFRDA / Department of Financial Services / banks",
        ["pension", "apy", "retirement", "central", "nationwide", "jansuraksha"],
        base_rules(
            min_age=18,
            max_age=40,
            categories=["non_income_tax_payer"],
            notes=(
                "Bank account holders age 18–40 who are not income-tax payers; contribution varies by chosen pension amount. "
                "Distinct from NPS All Citizen Model."
            ),
            verify_notes="2026-09-23: PIB/PFRDA/Jan Suraksha APY. Contribution and pension slabs — verify current PFRDA/DFS tables.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-sukanya-samriddhi",
        "Sukanya Samriddhi Account (Sukanya Samriddhi Yojana)",
        "सुकन्या समृद्धि खाता (सुकन्या समृद्धि योजना)",
        "Small-savings account for a girl child below 10 years, opened by natural/legal guardian at Post Office or authorised bank; deposits ₹250–₹1.5 lakh per financial year under scheme rules.",
        "10 वर्ष से कम आयु की बालिका हेतु लघु बचत खाता; अभिभावक द्वारा डाकघर/अधिकृत बैंक में; वार्षिक जमा ₹250–₹1.5 लाख।",
        "Tax-favoured small-savings account: deposit period commonly 15 years; maturity commonly 21 years from opening (per scheme rules). Interest rate notified periodically by MoF — verify current rate.",
        "कर-लाभयुक्त लघु बचत; जमा अवधि सामान्यतः 15 वर्ष; परिपक्वता सामान्यतः खोलने से 21 वर्ष। ब्याज दर अधिसूचना से सत्यापित करें।",
        [
            "Girl child’s birth certificate",
            "Guardian KYC / identity and address proof",
            "Photos and account-opening form as required by Post Office / bank",
        ],
        "Open at India Post or authorised bank branches under POSB/NSI scheme rules.",
        "भारत डाक या अधिकृत बैंक शाखा में खाता खोलें।",
        "https://www.indiapost.gov.in/",
        "https://www.nsiindia.gov.in/",
        "Department of Posts / National Savings Institute / authorised banks",
        ["savings", "girl_child", "sukanya", "post_office", "central", "nationwide"],
        base_rules(
            max_age=10,
            gender="female",
            categories=["girl_child"],
            notes=(
                "Account for girl child below 10; opened by natural/legal guardian; generally max two girls per family (twins/triplets exceptions per rules). "
                "Deposits ₹250–₹1.5 lakh per FY; deposit period 15 years; maturity 21 years from opening (per scheme rules)."
            ),
            verify_notes="2026-09-23: nsiindia.gov.in / India Post scheme rules. Interest rate and any rule amendments — confirm current MoF/NSI notification.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-nps-all-citizen",
        "National Pension System — All Citizen Model (Tier I)",
        "राष्ट्रीय पेंशन प्रणाली — ऑल सिटीजन मॉडल (टियर I)",
        "Voluntary Tier I NPS for Indian citizens / NRI / OCI meeting KYC (not HUF/PIO), distinct from Atal Pension Yojana; age band per current PFRDA/eNPS (commonly 18–70 on eNPS — confirm live page).",
        "भारतीय नागरिक / एनआरआई / ओसीआई हेतु स्वैच्छिक टियर I एनपीएस (एपीवाई से अलग); आयु बैंड वर्तमान पीएफआरडीए/ईएनपीएस अनुसार।",
        "Market-linked retirement corpus under PFRDA-regulated NPS; contribution and exit rules per PFRDA/eNPS. Not a fixed guaranteed pension like APY.",
        "पीएफआरडीए-विनियमित एनपीएस के अंतर्गत बाजार-संबद्ध सेवानिवृत्ति कोष; अंशदान/निकासी नियम ईएनपीएस अनुसार।",
        [
            "KYC as required by eNPS / Point of Presence",
            "Bank account for contributions",
            "PAN / Aadhaar as applicable",
        ],
        "Enrol via eNPS (NSDL CRA) or authorised Points of Presence; see PFRDA All Citizen Model page.",
        "ईएनपीएस (एनएसडीएल सीआरए) या अधिकृत पीओपी के माध्यम से नामांकन।",
        "https://enps.nsdl.com/",
        "https://www.pfrda.org.in/schemes/national-pension-system/nps-for-all-citizen-models",
        "PFRDA / NSDL CRA / Points of Presence",
        ["pension", "nps", "retirement", "central", "nationwide", "pfrda"],
        base_rules(
            min_age=18,
            max_age=70,
            notes=(
                "Indian citizens / NRI / OCI meeting KYC; age band per current PFRDA/eNPS (commonly 18–70 on eNPS — confirm live page); voluntary Tier I. "
                "Not HUF/PIO. Distinct from APY."
            ),
            verify_notes="2026-09-23: pfrda.org.in All Citizen Model + eNPS. Confirm live age band, contribution minima, and exit rules before advising.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-standup-india",
        "Stand-Up India",
        "स्टैंड-अप इंडिया",
        "Bank loans for SC/ST or woman entrepreneurs (age >18) for greenfield enterprises in manufacturing, services, trading, or agri-allied; composite loan commonly ₹10 lakh–₹1 crore.",
        "एससी/एसटी या महिला उद्यमियों (>18) हेतु ग्रीनफील्ड उद्यम ऋण; संयोजन ऋण सामान्यतः ₹10 लाख–₹1 करोड़।",
        "Composite loan typically ₹10 lakh to ₹1 crore; ~15% margin money; CGFSIL cover per scheme. Exact terms subject to bank appraisal.",
        "संयोजन ऋण सामान्यतः ₹10 लाख से ₹1 करोड़; लगभग 15% मार्जिन; सीजीएफएसआईएल कवर। बैंक मूल्यांकन लागू।",
        [
            "Identity proving SC/ST or woman entrepreneur status as applicable",
            "Project / business plan for greenfield enterprise",
            "KYC and bank documents",
            "For non-individual entities: evidence of ≥51% SC/ST/woman shareholding and control",
        ],
        "Apply at standupmitra.in / bank branch / Lead District Manager (LDM).",
        "standupmitra.in / बैंक शाखा / एलडीएम के माध्यम से आवेदन।",
        "https://www.standupmitra.in/",
        "https://www.standupmitra.in/",
        "Department of Financial Services / banks / LDM",
        ["loan", "sc", "st", "women", "entrepreneur", "standup_india", "central", "nationwide"],
        base_rules(
            min_age=18,
            categories=["sc", "st", "woman_entrepreneur"],
            occupations=["entrepreneur", "greenfield_enterprise"],
            notes=(
                "SC/ST or woman entrepreneur >18; loan for greenfield enterprise in manufacturing / services / trading / agri-allied; "
                "non-individual: ≥51% SC/ST/woman shareholding & control; composite loan ₹10 lakh–₹1 crore; ~15% margin; CGFSIL cover. "
                "Not a bank defaulter (standard lender rules)."
            ),
            verify_notes="2026-09-23: standupmitra.in + PIB scheme notes. Loan ceiling/margin/CGFSIL — confirm current portal terms.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-eshram",
        "e-Shram (National Database of Unorganised Workers)",
        "ई-श्रम (असंगठित श्रमिक राष्ट्रीय डेटाबेस)",
        "Free national registration for unorganised workers (age 16+) who are not ESIC/EPFO members and not income-tax payees; issues a permanent Universal Account Number (UAN). FAQ states registration facilitates social-security delivery; currently registration-focused (not automatic cash).",
        "असंगठित श्रमिकों (16+) का निःशुल्क पंजीकरण जो ईएसआईसी/ईपीएफओ सदस्य व आयकरदाता नहीं; स्थायी यूएएन। वर्तमान में मुख्यतः पंजीकरण।",
        "Free registration and permanent UAN. Does not by itself guarantee cash transfers; FAQ notes registration facilitates future social-security delivery.",
        "निःशुल्क पंजीकरण व स्थायी यूएएन। स्वतः नकद लाभ की गारंटी नहीं; भविष्य की सामाजिक सुरक्षा हेतु सुविधा।",
        [
            "Aadhaar",
            "Aadhaar-linked mobile preferred (else CSC biometric)",
            "Occupation / unorganised worker category details as on portal",
        ],
        "Register free on https://eshram.gov.in/ (self or via CSC biometric if mobile not linked).",
        "eshram.gov.in पर निःशुल्क पंजीकरण (या सीएससी बायोमेट्रिक)।",
        "https://eshram.gov.in/",
        "https://eshram.gov.in/faqs",
        "Ministry of Labour and Employment / CSC",
        ["unorganised_worker", "eshram", "uan", "registration", "central", "nationwide", "labour"],
        base_rules(
            min_age=16,
            occupations=["unorganised_worker", "home_based", "self_employed", "wage_worker"],
            categories=["unorganised_worker", "non_income_tax_payer"],
            notes=(
                "Unorganised worker (home-based / self-employed / wage; not ESIC/EPFO member); age 16+; not income-tax payee; "
                "Aadhaar (+ linked mobile preferred; else CSC biometric). Free registration; UAN permanent. "
                "FAQ: right now only registration is being done for direct cash — still catalogue-worthy as apply-facing national ID."
            ),
            verify_notes="2026-09-23: eshram.gov.in FAQs. Any future linked benefits — confirm official FAQ; do not invent cash entitlements.",
        ),
    )
)

# --- Wave C ---
NEW.append(
    india_scheme(
        "in-pmfby",
        "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "प्रधानमंत्री फसल बीमा योजना (पीएमएफबीवाई)",
        "Crop insurance for farmers cultivating a notified crop in a notified area with insurable interest (owners, tenants, sharecroppers). Loanee/KCC and non-loanee paths per state operational rules.",
        "अधिसूचित फसल/क्षेत्र में बीमायोग्य हित वाले किसानों हेतु फसल बीमा; ऋणकर्ता/गैर-ऋणकर्ता मार्ग राज्य नियमों अनुसार।",
        "Yield/weather-related claim settlement per operational guidelines. Farmer premium caps commonly cited as 2% Kharif / 1.5% Rabi for foodgrain-oilseed and 5% for commercial-horticulture (PIB/guidelines) — verify season and state.",
        "दावा निपटान दिशानिर्देश अनुसार। किसान प्रीमियम सीमा सामान्यतः खरीफ 2% / रबी 1.5% / वाणिज्यिक-बागवानी 5% — मौसम व राज्य सत्यापित करें।",
        [
            "Land / tenancy / sowing documents as required for non-loanee",
            "KCC / loan details if loanee path",
            "Bank account for premium/claims",
            "Aadhaar / KYC as required by State / insurer",
        ],
        "Enrol via pmfby.gov.in / bank / PACS / CSC / insurer before seasonal cut-off.",
        "pmfby.gov.in / बैंक / पैक्स / सीएससी / बीमाकर्ता के माध्यम से मौसमी कट-ऑफ से पहले।",
        "https://pmfby.gov.in/",
        "https://pmfby.gov.in/",
        "Ministry of Agriculture / State agriculture / banks / insurers",
        ["crop_insurance", "farmer", "pmfby", "agriculture", "central", "nationwide"],
        base_rules(
            occupations=["farmer", "tenant_farmer", "sharecropper"],
            categories=["farmer"],
            land_ownership="insurable_interest_notified_crop",
            notes=(
                "Farmers cultivating notified crop in notified area with insurable interest (owners, tenants, sharecroppers). "
                "Loanee/KCC farmers may be covered per state rules; non-loanee voluntary with land/tenancy/sowing docs. "
                "Farmer premium caps commonly 2% Kharif / 1.5% Rabi foodgrain-oilseed / 5% commercial-horticulture — verify season."
            ),
            verify_notes="2026-09-23: pmfby.gov.in operational guidelines. Notified crops/areas, premium caps, and cut-offs vary by State/season — verify=true.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-kisan-credit-card",
        "Kisan Credit Card (KCC)",
        "किसान क्रेडिट कार्ड (केसीसी)",
        "Short-term agricultural credit facility for farmers including owner-cultivators, tenant farmers, oral lessees, sharecroppers, and SHGs/JLGs; expanded KCC also covers allied activities (animal husbandry, fisheries) per RBI/GoI circulars.",
        "किसानों (मालिक/किरायेदार/मौखिक पट्टेदार/बटाईदार/एसएचजी-जेएलजी) हेतु अल्पकालिक कृषि ऋण; विस्तारित केसीसी में पशुपालन/मत्स्य भी।",
        "Revolving credit limit and interest subvention as per current RBI/GoI circulars — amounts and rates vary; verify with lending bank. Do not invent a single national ceiling.",
        "परिसंचारी ऋण सीमा व ब्याज अनुदान वर्तमान आरबीआई/भारत सरकार परिपत्र अनुसार — बैंक से सत्यापित करें।",
        [
            "Identity and land / tenancy / cultivation proof as required by bank",
            "KYC and bank account",
            "For allied activities: activity proof per bank checklist",
        ],
        "Apply at participating commercial / cooperative / RRB / Small Finance banks.",
        "वाणिज्यिक / सहकारी / आरआरबी / एसएफबी बैंकों में आवेदन।",
        "https://www.rbi.org.in/",
        "https://www.rbi.org.in/",
        "RBI / commercial-cooperative-RRB-SFB banks",
        ["kcc", "farmer", "credit", "agriculture", "central", "nationwide", "loan"],
        base_rules(
            occupations=["farmer", "tenant_farmer", "sharecropper", "animal_husbandry", "fisheries"],
            categories=["farmer", "shg", "jlg"],
            notes=(
                "Farmers including owner-cultivators, tenant farmers, oral lessees, sharecroppers, SHGs/JLGs; "
                "also allied activities (animal husbandry, fisheries) under expanded KCC. "
                "Credit limit/interest subvention per RBI/GoI circulars — verify=true for numbers."
            ),
            verify_notes="2026-09-23: RBI Master Directions/circulars on KCC. Limit and interest subvention figures change — confirm current circular and bank product page.",
        ),
    )
)

NEW.append(
    india_scheme(
        "in-janani-suraksha",
        "Janani Suraksha Yojana (JSY) – National",
        "जननी सुरक्षा योजना (जेएसवाई) – राष्ट्रीय",
        "National NHM cash-assistance scheme to promote institutional delivery. Low-performing vs high-performing state (LPS/HPS) rules differ; state-specific variants (e.g. Kerala, Rajasthan) also exist in this catalogue.",
        "संस्थागत प्रसव प्रोत्साहन हेतु राष्ट्रीय नकद सहायता; एलपीएस/एचपीएस राज्य नियम भिन्न; राज्य-विशिष्ट प्रविष्टियाँ भी कैटलॉग में हैं।",
        "Cash assistance for institutional delivery; amounts and beneficiary categories differ for LPS vs HPS states per MoHFW/NHM guidelines — do not invent rupee amounts; confirm current MoHFW guideline.",
        "संस्थागत प्रसव हेतु नकद सहायता; एलपीएस/एचपीएस में राशि व पात्रता भिन्न — वर्तमान मोएचएफडब्ल्यू दिशानिर्देश से सत्यापित करें।",
        [
            "Pregnancy / ANC records as required by State NHM",
            "Identity / BPL or category proof where HPS rules require",
            "Bank account for DBT where applicable",
            "Institutional delivery documentation",
        ],
        "Through government health facilities / ASHA / State NHM channels under JSY. See nhm.gov.in scheme materials; confirm LPS/HPS status of your State.",
        "सरकारी स्वास्थ्य संस्थान / आशा / राज्य एनएचएम जेएसवाई चैनलों के माध्यम से।",
        "https://nhm.gov.in/",
        "https://nhm.gov.in/",
        "Ministry of Health and Family Welfare / NHM / State Health Departments",
        ["maternity", "jsy", "institutional_delivery", "nhm", "central", "nationwide", "women"],
        base_rules(
            gender="female",
            categories=["pregnant_woman", "institutional_delivery"],
            marital_status=[],
            notes=(
                "Cash assistance to promote institutional delivery. LPS vs HPS state rules differ (broader in low-performing states; "
                "BPL/SC/ST conditions often apply in HPS). Must pull current MoHFW guidelines — do not invent rupee amounts. "
                "Catalogue also has Kerala and Rajasthan state variants."
            ),
            verify_notes="2026-09-23: NHM/MoHFW JSY materials. National amounts and LPS/HPS eligibility need MoHFW guideline lock before quoting rupees.",
        ),
    )
)

# --- Optional Wave E ---
NEW.append(
    india_scheme(
        "in-pm-rahat",
        "PM RAHAT (cashless treatment for road accident victims)",
        "पीएम राहत (सड़क दुर्घटना पीड़ितों हेतु कैशलेस उपचार)",
        "Cashless trauma care for victims of motor-vehicle road accidents at designated hospitals (including compliant AB-PM-JAY hospitals), with police authentication. Hospital-mediated pathway (not a citizen DBT application portal).",
        "मोटर वाहन सड़क दुर्घटना पीड़ितों हेतु नामित अस्पतालों में कैशलेस ट्रॉमा केयर; पुलिस प्रमाणीकरण। अस्पताल-माध्यम मार्ग।",
        "Cashless treatment commonly up to ₹1.5 lakh for up to 7 days; hospitalization generally within 24 hours of accident per scheme text. Implementation can be uneven by state — verify.",
        "कैशलेस उपचार सामान्यतः अधिकतम ₹1.5 लाख / 7 दिन तक; सामान्यतः दुर्घटना के 24 घंटे के भीतर अस्पताल प्रवेश। राज्य कार्यान्वयन भिन्न हो सकता है।",
        [
            "Police authentication / accident documentation as required by hospital protocol",
            "Identity of victim as required",
            "Treatment at designated / compliant hospital",
        ],
        "Hospital-mediated: seek care at designated hospitals under the scheme; police authentication supports cashless processing. Not a self-serve DBT portal application.",
        "नामित अस्पताल में उपचार; पुलिस प्रमाणीकरण से कैशलेस प्रक्रिया। स्वयं-सेवा डीबीटी पोर्टल नहीं।",
        "https://pib.gov.in/",
        "https://pib.gov.in/",
        "Ministry of Road Transport and Highways / designated hospitals / police",
        ["road_safety", "trauma", "cashless", "emergency", "central", "nationwide", "health"],
        base_rules(
            categories=["road_accident_victim"],
            notes=(
                "Victims of motor-vehicle road accidents needing trauma care; cashless treatment up to ₹1.5 lakh for up to 7 days; "
                "hospitalization generally within 24 hours; police authentication; designated hospitals (incl. compliant AB-PM-JAY hospitals). "
                "Applies regardless of nationality per scheme text. Hospital-mediated — not a DBT apply portal."
            ),
            verify_notes="2026-09-23: PIB nationwide launch messaging (e.g. Feb 2026) + MoRTH scheme materials. State rollout uneven — verify=true; confirm designated hospital list locally.",
        ),
    )
)

# --- US ---
NEW.append(
    us_scheme(
        "us-summer-ebt",
        "Summer EBT / SUN Bucks – United States",
        "समर ईबीटी / सन बक्स – संयुक्त राज्य अमेरिका",
        "USDA grocery benefit for eligible school-age children during summer in participating states, Tribes, and territories. Often called SUN Bucks. Availability is not universal in all jurisdictions.",
        "About $120 grocery benefit per eligible school-age child for the summer in participating jurisdictions (confirm current FNS amount). Delivered via EBT or similar state mechanism.",
        [
            "Child school-age eligibility and residency in a participating state/Tribe/territory",
            "Auto path via SNAP/TANF/FDPIR/Medicaid/foster/homeless/migrant/free-reduced meals where applicable; otherwise state/Tribe application",
        ],
        "Check FNS Summer EBT page for participating jurisdictions and your state/Tribe application or automatic enrolment path: https://www.fns.usda.gov/sebt",
        "https://www.fns.usda.gov/sebt",
        "https://www.fns.usda.gov/sebt",
        "USDA Food and Nutrition Service / state or Tribal Summer EBT agency",
        ["united_states", "food", "children", "summer", "ebt", "usda", "federal"],
        us_rules(
            implies_low_income=True,
            categories=["school_age_child"],
            notes=(
                "$120 grocery benefit per eligible school-age child for summer in participating states/Tribes/territories. "
                "Auto paths via SNAP/TANF/FDPIR/Medicaid/foster/homeless/migrant/free-reduced meals; others apply via state/Tribe. "
                "Not available in all jurisdictions — check FNS map."
            ),
            verify_notes="2026-09-23: fns.usda.gov/sebt. Confirm current per-child amount, participating jurisdictions, and state application windows.",
        ),
    )
)

NEW.append(
    us_scheme(
        "us-va-disability",
        "VA Disability Compensation – United States",
        "वीए डिसेबिलिटी कंपंसेशन – संयुक्त राज्य अमेरिका",
        "Tax-free monthly VA compensation for Veterans with a current illness or injury connected to active duty, active duty for training, or inactive duty training (or presumptive/PACT Act pathways). Discharge generally other than dishonorable.",
        "Tax-free monthly disability compensation based on VA disability rating and dependents. Amounts published in VA compensation rate tables — verify current rates.",
        [
            "DD214 or equivalent service records",
            "Medical evidence of current disability and nexus to service (or presumptive basis)",
            "VA claim forms / online claim submission materials",
        ],
        "File a claim online or with help from an accredited representative: https://www.va.gov/disability/how-to-file-claim/ — review eligibility at https://www.va.gov/disability/eligibility/",
        "https://www.va.gov/disability/how-to-file-claim/",
        "https://www.va.gov/disability/eligibility/",
        "U.S. Department of Veterans Affairs (VA)",
        ["united_states", "veteran", "disability", "va", "federal", "compensation"],
        us_rules(
            disability_required=True,
            categories=["veteran", "service_connected"],
            occupations=["veteran"],
            notes=(
                "Current illness/injury AND service on active duty / ADT / IADT; plus in-service / aggravation / post-service service-connected claim (or presumptive). "
                "Discharge generally other than dishonorable. PACT Act expands toxic-exposure pathways."
            ),
            verify_notes="2026-09-23: va.gov disability eligibility + how-to-file. Rating percentages and monthly rates change — confirm current VA rate tables.",
        ),
    )
)

NEW.append(
    us_scheme(
        "us-ssa-survivors",
        "Social Security Survivors Benefits – United States",
        "सोशल सिक्योरिटी सर्वाइवर्स बेनिफिट्स – संयुक्त राज्य अमेरिका",
        "Monthly Social Security benefits for eligible spouses, ex-spouses, children, and dependent parents of a deceased worker who paid Social Security taxes.",
        "Monthly survivors benefits based on the deceased worker’s earnings record. Exact amounts from SSA — verify.",
        [
            "Proof of death and relationship to the deceased worker",
            "SSN of deceased and claimant",
            "Birth/marriage/divorce records as applicable",
            "Citizenship/immigration documents as required by SSA",
        ],
        "Apply with SSA (online where available, phone, or field office). Review https://www.ssa.gov/survivor/eligibility",
        "https://www.ssa.gov/survivor/eligibility",
        "https://www.ssa.gov/survivor/eligibility",
        "Social Security Administration (SSA)",
        ["united_states", "social_security", "survivors", "ssa", "federal"],
        us_rules(
            categories=["surviving_spouse", "surviving_child", "dependent_parent"],
            notes=(
                "Spouse/ex-spouse/child/dependent parent of deceased worker who paid SS taxes. "
                "Spouses: typically 60+ (or 50–59 if disabled), marriage duration rules, remarriage limits; or any age caring for child. "
                "Children: unmarried, ≤17, or 18–19 in K–12 full-time, or disabled before 22. "
                "Dependent parents 62+ with financial support rules."
            ),
            verify_notes="2026-09-23: ssa.gov/survivor/eligibility. Age/marriage/disability rules have nuance — verify with SSA before advising.",
        ),
    )
)

NEW.append(
    us_scheme(
        "us-fema-ia",
        "FEMA Individual Assistance – United States",
        "फेमा इंडिविजुअल असिस्टेंस – संयुक्त राज्य अमेरिका",
        "Federal disaster assistance for individuals and households in a presidentially declared disaster area with damage to a primary residence or other serious unmet disaster-caused needs, when uninsured or underinsured.",
        "Grants and other Individual Assistance help for temporary housing, home repairs, and other serious disaster-caused needs per FEMA program rules — not a substitute for insurance. Amounts case-specific.",
        [
            "Proof of identity, occupancy, and ownership/tenancy as required",
            "Insurance information (or lack thereof)",
            "Damage documentation",
            "SSN and qualifying citizenship/immigration status per FEMA rules",
        ],
        "Apply at DisasterAssistance.gov, FEMA app, phone, or Disaster Recovery Center after a declaration covering your area: https://www.disasterassistance.gov/",
        "https://www.disasterassistance.gov/",
        "https://www.fema.gov/assistance/individual/program/eligibility",
        "FEMA / DisasterAssistance.gov",
        ["united_states", "disaster", "fema", "housing", "federal", "emergency"],
        us_rules(
            categories=["disaster_survivor"],
            notes=(
                "Declared disaster area; damaged primary residence or serious unmet disaster need; uninsured/underinsured; "
                "qualifying citizenship/immigration + SSN rules per FEMA. Apply online / app / phone / DRC."
            ),
            verify_notes="2026-09-23: disasterassistance.gov + fema.gov IA eligibility. Only available after a qualifying declaration — confirm your county is included.",
        ),
    )
)

NEW.append(
    us_scheme(
        "us-free-file-vita",
        "IRS Free File + VITA/TCE – United States",
        "आईआरएस फ्री फाइल + वीआईटीए/टीसीई – संयुक्त राज्य अमेरिका",
        "Free federal tax-return pathways: IRS Free File guided software (AGI limit), Free File Fillable Forms (any income), Volunteer Income Tax Assistance (VITA), and Tax Counseling for the Elderly (TCE).",
        "Free preparation and e-file of federal returns (and often state, where offered) via Free File partners or IRS-certified VITA/TCE volunteers. Complements EITC/CTC claiming.",
        [
            "Income documents (W-2, 1099, etc.)",
            "Identity / SSN or ITIN for filers and dependents",
            "Bank account for direct deposit if desired",
            "For VITA/TCE: appointment and intake forms as required by site",
        ],
        "Free File: https://www.irs.gov/e-file-do-your-taxes-for-free — VITA/TCE locator: https://www.irs.gov/individuals/free-tax-return-preparation-for-qualifying-taxpayers",
        "https://www.irs.gov/e-file-do-your-taxes-for-free",
        "https://www.irs.gov/individuals/free-tax-return-preparation-for-qualifying-taxpayers",
        "Internal Revenue Service (IRS) / VITA-TCE partner sites",
        ["united_states", "tax", "irs", "free_file", "vita", "tce", "federal"],
        us_rules(
            implies_low_income=True,
            max_annual_income=89000,
            notes=(
                "Free File guided software: AGI ≤ $89,000 (TY2025 / filing season 2026 per IRS newsroom); Fillable Forms any income. "
                "VITA: generally ≤ $69,000, disability, limited English. TCE: age 60+ focus. "
                "max_annual_income encodes Free File guided AGI ceiling only; VITA/TCE have different gates — verify=true."
            ),
            verify_notes="2026-09-23: IRS Free File + VITA pages / newsroom AGI $89,000 for FS2026. Confirm each filing season’s Free File AGI limit and local VITA eligibility.",
        ),
    )
)


def main() -> None:
    assert [s["id"] for s in NEW] == EXPECTED_IDS, (
        f"NEW order/ids mismatch:\n expected={EXPECTED_IDS}\n got={[s['id'] for s in NEW]}"
    )
    assert len(NEW) == 22

    # Brief wait if another writer might be active
    import time

    time.sleep(0.5)

    schemes: list[dict] = json.loads(DATA.read_text())
    before = len(schemes)
    existing = {s["id"] for s in schemes}

    missing_check = [i for i in EXPECTED_IDS if i in existing]
    if missing_check:
        print(f"ERROR: IDs already present (refusing overwrite): {missing_check}", file=sys.stderr)
        sys.exit(1)

    for s in NEW:
        schemes.append(s)

    ids = [s["id"] for s in schemes]
    assert len(ids) == len(set(ids)), "Duplicate ids after append"

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    after = len(schemes)
    assert after == before + 22

    scope_addendum = (
        " Catalogue refresh 2026-09-23 wave 2: India Ujjwala, PMAY-U 2.0, PMAY-G, PM SVANidhi, MUDRA, "
        "NFSA/ONORC, PMSBY, PMJJBY, APY, Sukanya Samriddhi, NPS All Citizen, Stand-Up India, e-Shram, "
        "PMFBY, KCC, JSY national, PM RAHAT; US Summer EBT, VA Disability, SSA Survivors, FEMA IA, Free File/VITA."
    )

    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = after
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        if "Catalogue refresh 2026-09-23 wave 2" not in scope:
            meta["scope"] = scope.rstrip() + scope_addendum
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    assert DATA.read_text() == FE_DATA.read_text()
    assert json.loads(META.read_text())["scheme_count"] == after
    assert json.loads(FE_META.read_text())["scheme_count"] == after
    assert json.loads(META.read_text())["updated_as_of"] == LAST

    present = {s["id"] for s in json.loads(DATA.read_text())}
    for i in EXPECTED_IDS:
        assert i in present, f"missing after write: {i}"

    print(f"BEFORE: {before}")
    print(f"AFTER:  {after}")
    print(f"DELTA:  {after - before}")
    print("ADDED:", EXPECTED_IDS)
    print("SKIPPED per report: Jal Jeevan, POSHAN/ICDS, Soil Health, eNAM, PM CARES closed cohort, Ticket to Work, ended COBRA/ERA")


if __name__ == "__main__":
    main()
