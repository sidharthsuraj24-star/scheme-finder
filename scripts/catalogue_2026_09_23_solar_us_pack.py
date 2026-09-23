#!/usr/bin/env python3
"""Catalogue update 2026-09-23: India solar + Lakhpati Bitiya + VB-G RAM G + Vishwakarma;
US household tax/energy/aid pack. Official sources only; verify=true where limits vary.
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
LAST = "2026-09-23"
ISO = "2026-09-23T09:45:00+05:30"
ML_PREFIX = "(EN — Malayalam review pending) "


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
        "states": [],
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
    nationwide_top: bool | None = None,
) -> dict:
    obj = {
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
    }
    if nationwide_top is not None:
        obj["nationwide"] = nationwide_top
    return obj


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


# ---------------------------------------------------------------------------
# India REPLACE: dl-ladli-scheme → dl-lakhpati-bitiya
# ---------------------------------------------------------------------------
LAKHPATI = india_scheme(
    "dl-lakhpati-bitiya",
    "Delhi Lakhpati Bitiya Scheme",
    "दिल्ली लखपति बिटिया योजना",
    "GNCTD girl-child milestone savings scheme superseding Delhi Ladli Scheme 2008 from 1 Apr 2026; phased deposits redeemable at 18/21 with education conditions (gazette 30 Mar 2026).",
    "1 अप्रैल 2026 से दिल्ली लाड़ली योजना 2008 के स्थान पर GNCTD बालिका बचत योजना; 18/21 वर्ष पर शिक्षा शर्तों सहित चरणबद्ध जमा।",
    "Phased payments redeemable at 18/21 (as applicable): Birth ₹11,000; Class 1 ₹5,000; Class 6 ₹5,000; Class 9 ₹5,000; Class 11 or Polytechnic/ITI after Class 10 ₹5,000; Class 12 ₹5,000; then diploma/graduation path amounts (1-yr diploma ₹10,000; 2-yr ₹20,000; 3-yr diploma or 3-yr graduation ₹20,000 structured; 4-yr graduation ₹25,000 structured). Encashable only after Class XII (or polytechnic/ITI) + age 18, or after graduation/diploma + age 21, as applicable. Non-transferable; no loan against deposit; marriage before 18 disqualifies maturity. Do not treat marketing 'matures to ₹1.20 lakh' as a fixed gazette lump sum.",
    "18/21 वर्ष पर भुनाई योग्य चरणबद्ध राशि (राजपत्र अनुसार): जन्म ₹11,000; कक्षा 1/6/9/11 या पॉली/ITI/12 पर ₹5,000 इत्यादि; डिप्लोमा/स्नातक पथ अलग। 18 से पहले विवाह पर परिपक्वता अयोग्य। विपणन '₹1.20 लाख' को निश्चित राजपत्र राशि न मानें।",
    [
        "Residence proof (≥3 years in NCT Delhi)",
        "Birth certificate (Registrar of Births & Deaths, Delhi)",
        "Joint photograph of parent and child",
        "Self-declaration of income and marital status",
        "Admission / bonafide school certificate (where applicable)",
        "Immunization certificate (new beneficiaries from 01.04.2026)",
        "Private-school cases: DEO verification as required",
    ],
    "Apply online via the dedicated portal to the District Women & Child Development Officer (per gazette). Confirm current e-District / WCD service name after rename from Ladli. https://edistrict.delhigovt.nic.in/",
    "राजपत्र अनुसार जिला महिला एवं बाल विकास अधिकारी को समर्पित पोर्टल पर ऑनलाइन आवेदन; लाड़ली नाम परिवर्तन के बाद ई-डिस्ट्रिक्ट/WCD सेवा नाम पुष्टि करें।",
    "https://edistrict.delhigovt.nic.in/",
    "https://wcd.delhi.gov.in/wcd/delhi-ladli-scheme-2008",
    "Department of Women and Child Development, Government of NCT of Delhi",
    ["girl-child", "women", "education", "delhi", "dbt", "savings"],
    base_rules(
        min_age=0,
        max_age=21,
        max_annual_income=120000,
        gender="female",
        nationwide=False,
        states=["Delhi"],
        notes=(
            "English gazette (30 Mar 2026; in force 1 Apr 2026): girl born in Delhi (birth certificate from Registrar Births & Deaths); "
            "applicant bonafide NCT Delhi resident ≥3 years before application; annual family income ≤ ₹1,20,000; benefit limited to two girls per family; "
            "studying in Govt/MCD/NDMC or Govt-recognised Delhi school (school-going path); not married before age 18; immunization as per norms for new beneficiaries from 01.04.2026; "
            "existing Ladli beneficiaries eligible for further higher-education milestones if unmarried till 18; CCI exemptions for residence/income/birth place (State as guardian). "
            "Supersedes Delhi Ladli Scheme 2008 (former catalogue id dl-ladli-scheme)."
        ),
        verify_notes=(
            "2026-09-23: Gazette PDF (District North CDN) + WCD notification dated 01-04-2026. "
            "dmnorth scheme card metadata looked stale — treat gazette + WCD as authoritative. "
            "Confirm live apply service name on e-District/WCD."
        ),
    ),
    nationwide_top=False,
)

# ---------------------------------------------------------------------------
# India ADDs
# ---------------------------------------------------------------------------
INDIA_NEW: list[dict] = []

INDIA_NEW.append(
    india_scheme(
        "in-pm-surya-ghar",
        "PM Surya Ghar: Muft Bijli Yojana",
        "पीएम सूर्य घर: मुफ्त बिजली योजना",
        "Central CFA for grid-connected residential rooftop solar via the National Portal; target 1 crore households through FY 2026-27 (implementation till 31 Mar 2027).",
        "राष्ट्रीय पोर्टल के माध्यम से ग्रिड-कनेक्टेड आवासीय रूफटॉप सोलर हेतु केंद्रीय CFA; FY 2026-27 तक लगभग 1 करोड़ परिवार (31 मार्च 2027 तक)।",
        "CFA: ₹30,000/kWp for first 2 kWp; ₹18,000/kWp for additional 1 kWp; no additional CFA beyond 3 kWp (max ₹78,000 for ≥3 kW). Special-category States/UTs: ₹33,000/kWp and ₹19,800/kWp. GHS/RWA common facilities: ₹18,000/kWp (special ₹19,800) up to 500 kWp @3 kWp/house. Collateral-free low-interest loan products (~7% / repo+50 bps band per guidelines) for systems up to 3 kW via National Portal / Jan Samarth. Scheme messaging includes free/low-cost electricity framing up to ~300 units/month via RTS generation (outcome framing, not a separate tariff entitlement).",
        "CFA: प्रथम 2 kWp पर ₹30,000/kWp; अतिरिक्त 1 kWp पर ₹18,000/kWp; 3 kWp से अधिक CFA नहीं (अधिकतम ₹78,000)। विशेष श्रेणी राज्य/UT उच्च दरें। 3 kW तक कम ब्याज ऋण विकल्प।",
        [
            "DISCOM Consumer Account Number / residential connection ID",
            "Bank account proof (cancelled cheque / e-statement / passbook)",
            "Identity as required by National Portal",
            "Geo-tagged installation photos; DISCOM inspection & net-metering agreement",
            "Portal-registered vendor selection",
        ],
        "Apply only on the National Portal https://pmsuryaghar.gov.in/ ; choose a portal-registered vendor; complete DISCOM net-metering; CFA via e-token to bank/loan account.",
        "केवल राष्ट्रीय पोर्टल pmsuryaghar.gov.in पर आवेदन; पोर्टल-पंजीकृत विक्रेता चुनें; DISCOM नेट-मीटरिंग; CFA बैंक/ऋण खाते में।",
        "https://pmsuryaghar.gov.in/",
        "https://mnre.gov.in/en/notice/guidelines-for-pm-surya-ghar-muft-bijli-yojana/",
        "MNRE / Local DISCOM / National Portal",
        ["solar", "rooftop", "renewable", "energy", "subsidy", "central", "nationwide", "housing"],
        base_rules(
            states=["All India"],
            nationwide=True,
            notes=(
                "Residential consumer with valid DISCOM Consumer Account Number / equivalent; grid-connected RTS on roof/terrace/balcony/elevated structure (BiPV also eligible). "
                "Not for non-residential (commercial/industrial/govt) CFA under this component. DCR (domestically manufactured modules/cells) required; off-grid not eligible. "
                "No income gate stated for residential CFA. GHS/RWA common facilities covered under separate CFA row."
            ),
            verify_notes=(
                "2026-09-23: MNRE Capex CFA guidelines + PIB Cabinet; CFA disbursement confirmed in PIB (e.g. as of 19.03.2026). "
                "Exact portal document field list may vary — verify on pmsuryaghar.gov.in."
            ),
        ),
        nationwide_top=True,
    )
)

INDIA_NEW.append(
    india_scheme(
        "dl-rooftop-solar-subsidy",
        "Delhi Rooftop Solar Capital Subsidy (Delhi Solar Energy Policy / PM Surya Ghar ULA)",
        "दिल्ली रूफटॉप सोलर पूंजी सब्सिडी (दिल्ली सोलर ऊर्जा नीति / पीएम सूर्य घर ULA)",
        "GNCTD additional capital subsidy for residential rooftop solar, combined with PM Surya Ghar CFA; Utility Led Aggregation (ULA) free-install path for eligible low-consumption households.",
        "आवासीय रूफटॉप सोलर हेतु GNCTD अतिरिक्त पूंजी सब्सिडी (पीएम सूर्य घर CFA के साथ); पात्र कम-खपत परिवारों हेतु ULA निःशुल्क स्थापना मार्ग।",
        "Delhi enhanced capital subsidy up to ₹78,000 for residential installations. GHS: @₹11,000/kW. Under ULA (IPGCL), eligible consumers averaging up to 400 units/month can get free rooftop solar up to 3 kW (subject to technical feasibility, programme availability, first-come-first-serve; initial phase target cited up to 1.10 lakh ULA installs to 28 Feb 2027). Consumer pays net cost after PM Surya Ghar CFA (up to ₹78,000) + Delhi state capital subsidy (up to ₹78,000).",
        "आवासीय प्रतिष्ठानों हेतु दिल्ली पूंजी सब्सिडी अधिकतम ₹78,000; GHS @₹11,000/kW; ULA में ≤400 यूनिट/माह औसत पर 3 kW तक निःशुल्क (तकनीकी व्यवहार्यता/उपलब्धता अधीन)।",
        [
            "Delhi residential DISCOM connection / consumer ID",
            "Consent / capacity request via DISCOM online or barcode as directed",
            "PM Surya Ghar National Portal application for central CFA",
            "Identity and bank details as required by Delhi Solar Portal / DISCOM",
        ],
        "Central CFA via https://pmsuryaghar.gov.in/ ; Delhi state processing via Delhi Solar Portal / DISCOM consent flow. See https://solar.delhi.gov.in/",
        "केंद्रीय CFA pmsuryaghar.gov.in पर; दिल्ली राज्य प्रसंस्करण सोलर पोर्टल/DISCOM सहमति से।",
        "https://solar.delhi.gov.in/page/state-subsidy",
        "https://solar.delhi.gov.in/page/central-subsidy",
        "Power Department / EEREM / DISCOM / IPGCL (ULA), GNCTD",
        ["solar", "rooftop", "delhi", "subsidy", "energy", "state"],
        base_rules(
            nationwide=False,
            states=["Delhi"],
            notes=(
                "Residential consumer in Delhi under amended Solar Energy Policy. ULA free path: average monthly consumption ≤400 units (priority). "
                "No separate income ceiling stated in the Power Department PDF for the capital subsidy. Complements PM Surya Ghar CFA."
            ),
            verify_notes=(
                "2026-09-23: Amounts from official Power Department GNCTD PDF (solar.delhi.gov.in). "
                "ULA availability and unit-band incentives: confirm on live portal/PDF before advising a household."
            ),
        ),
        nationwide_top=False,
    )
)

INDIA_NEW.append(
    india_scheme(
        "in-vb-g-ram-g",
        "Viksit Bharat – Guarantee for Rozgar and Ajeevika Mission (Gramin) (VB-G RAM G Act, 2025)",
        "विकसित भारत – गारंटी फॉर रोजगार एंड आजीविका मिशन (ग्रामीण) (वीबी-जी राम जी अधिनियम, 2025)",
        "Statutory rural employment guarantee succeeding MGNREGA from 1 Jul 2026: up to 125 days unskilled wage work per eligible rural household per financial year.",
        "1 जुलाई 2026 से मनरेगा के स्थान पर वैधानिक ग्रामीण रोजगार गारंटी: पात्र ग्रामीण परिवार को प्रति वित्त वर्ष अधिकतम 125 दिन अकुशल मजदूरी कार्य।",
        "Guarantee of 125 days wage employment per FY (was 100 under MGNREGA). Wages weekly/fortnightly via DBT; delay compensation 0.05%/day if unpaid >15 days after muster close. Until new rates notified, existing MGNREGA wage rates continue (state pages may cite notified minima — confirm all-India notification before treating any single rupee wage as universal). Peak agri season: States may notify up to 60-day pause; 125 days still apply in the remaining period.",
        "प्रति वित्त वर्ष 125 दिन मजदूरी रोजगार की गारंटी; DBT से साप्ताहिक/पाक्षिक मजदूरी; विलंब मुआवजा नियम लागू। अखिल भारतीय मजदूरी दर एक संख्या के रूप में न मानें — अधिसूचना पुष्टि करें।",
        [
            "Household member names, ages, and address for registration",
            "Aadhaar / e-KYC as typically required in practice",
            "Gram Panchayat registration / job card (e-KYC cards remain valid until Gramin Rozgar Guarantee Cards issued)",
        ],
        "Register / demand work at Gram Panchayat or Programme Officer (oral/writing/digital). Employment within 15 days or unemployment allowance. Citizen MIS: vbgramg.dord.gov.in (access may vary); legacy nrega.dord.gov.in for older records.",
        "ग्राम पंचायत / कार्यक्रम अधिकारी के पास पंजीकरण व कार्य मांग; 15 दिनों में रोजगार या बेरोजगारी भत्ता।",
        "https://www.pib.gov.in/PressReleasePage.aspx?lang=1&PRID=2279446&reg=3",
        "https://www.pib.gov.in/FaqDetails.aspx?ModuleId=4&NoteId=158511&lang=1&reg=3",
        "Ministry of Rural Development / Gram Panchayat / Programme Officer",
        ["employment", "rural", "wage", "central", "nationwide", "dbt", "livelihood"],
        base_rules(
            states=["All India"],
            nationwide=True,
            categories=["rural_household"],
            notes=(
                "Every rural household whose adult members volunteer for unskilled manual work. "
                "Live for citizens from 1 Jul 2026 (PIB 30 Jun 2026); MGNREGA repealed same day. "
                "Do not hard-code a single nationwide daily wage — rates are notified and may vary by state/date."
            ),
            verify_notes=(
                "2026-09-23: PIB rollout + FAQ; Haryana RD summary updated 01 Jul 2026. "
                "Haryana RD cited MoRD minimum ₹409/manday w.e.f. 30 Jun 2026 — confirm all-India notification before encoding as universal."
            ),
        ),
        nationwide_top=True,
    )
)

INDIA_NEW.append(
    india_scheme(
        "in-pm-vishwakarma",
        "PM Vishwakarma",
        "पीएम विश्वकर्मा",
        "Central holistic support for traditional artisans and craftspeople in 18 notified trades: toolkit incentive, training stipend, and collateral-free credit with interest subvention.",
        "18 अधिसूचित व्यवसायों में पारंपरिक कारीगरों हेतु केंद्रीय सहायता: टूलकिट प्रोत्साहन, प्रशिक्षण वृत्ति, और ब्याज अनुदान सहित बिना गिरवी ऋण।",
        "Toolkit incentive ₹15,000; training stipend ₹500/day; collateral-free loans up to ₹3 lakh (₹1L + ₹2L tranches) at 5% with GoI interest subvention up to 8%.",
        "टूलकिट प्रोत्साहन ₹15,000; प्रशिक्षण वृत्ति ₹500/दिन; बिना गिरवी ऋण अधिकतम ₹3 लाख (₹1 लाख + ₹2 लाख किस्तें) 5% पर, सरकार ब्याज अनुदान अधिकतम 8% तक।",
        [
            "Aadhaar (biometric enrolment at CSC)",
            "Proof of trade / artisan activity as required by portal",
            "Bank account details",
            "Family / eligibility declarations per guidelines",
        ],
        "Free CSC enrolment with Aadhaar biometric on https://pmvishwakarma.gov.in/ ; GP/ULB → District → Screening Committee. Helpline 18002677777.",
        "निःशुल्क CSC नामांकन (आधार बायोमेट्रिक) pmvishwakarma.gov.in पर; ग्राम पंचायत/ULB → जिला → स्क्रीनिंग समिति। हेल्पलाइन 18002677777।",
        "https://pmvishwakarma.gov.in/",
        "https://pmvishwakarma.gov.in/",
        "Ministry of Micro, Small and Medium Enterprises / CSC / District Administration",
        ["artisan", "skill", "credit", "msme", "central", "nationwide", "livelihood"],
        base_rules(
            min_age=18,
            states=["All India"],
            nationwide=True,
            occupations=["artisan", "craftsperson", "self_employed_unorganised"],
            notes=(
                "Age ≥18; self-employed unorganised sector in one of 18 notified trades; one member per family; not a government employee/family. "
                "Generally no similar credit-scheme loan in past 5 years (MUDRA/PM SVANidhi fully repaid may be eligible per Sep 2026 PIB note — confirm on portal guidelines)."
            ),
            verify_notes=(
                "2026-09-23: pmvishwakarma.gov.in + PIB. Confirm current trade list, credit look-back, and exclusion rules on live portal guidelines."
            ),
        ),
        nationwide_top=True,
    )
)

# ---------------------------------------------------------------------------
# US ADDs
# ---------------------------------------------------------------------------
US_NEW: list[dict] = []

US_NEW.append(
    us_scheme(
        "us-eitc",
        "Earned Income Tax Credit (EITC) – United States",
        "अर्जित आय कर क्रेडिट (EITC) – संयुक्त राज्य अमेरिका",
        "Refundable IRS tax credit for eligible workers with earned income. Often the largest refundable credit for low- and moderate-income workers; claim on Form 1040 (Free File / VITA available).",
        "Refundable credit; amount depends on filing status, earned income, and number of qualifying children. TY2026 maximums and income phaseouts are set annually by the IRS — do not treat any single figure as permanent.",
        [
            "Valid SSN by return due date (filer/spouse/qualifying child as required)",
            "Earned income records (W-2, self-employment)",
            "Form 1040 (and Schedule EIC if applicable)",
        ],
        "Claim on your federal income tax return (Form 1040). Free File, VITA, or a tax preparer. See IRS EITC pages for current-year limits.",
        "https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit-eitc",
        "https://www.irs.gov/credits-deductions/individuals/earned-income-tax-credit/who-qualifies-for-the-earned-income-tax-credit-eitc",
        "Internal Revenue Service (IRS)",
        ["united_states", "tax", "refundable", "irs", "federal", "eitc"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Must have earned income; investment income below the annual limit; valid SSN by return due date (incl. extensions) for filer/spouse/qualifying child; "
                "U.S. citizen or resident alien all year; not Form 2555; filing-status rules apply (incl. MFS exceptions). "
                "Without a qualifying child: live in U.S. more than half the year; not another’s dependent/qualifying child; age at least 25 and under 65 (one spouse on a joint return). "
                "Amounts and income thresholds change each tax year."
            ),
            verify_notes=(
                "2026-09-23: IRS who-qualifies + EITC overview. Encode year-specific max credit/income tables with verify=true; IRS newsroom has cited TY2026 maxima (e.g. for 3+ children) — confirm on current IRS pages before advising a dollar amount."
            ),
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-child-tax-credit",
        "Child Tax Credit (CTC) / Additional Child Tax Credit (ACTC) – United States",
        "चाइल्ड टैक्स क्रेडिट (CTC) / अतिरिक्त CTC – संयुक्त राज्य अमेरिका",
        "IRS family tax credit for qualifying children under 17; ACTC may be refundable. Claim on Form 1040 with Schedule 8812. Other Dependent Credit (ODC) may apply for other dependents.",
        "CTC up to $2,200 per qualifying child; ACTC up to $1,700 refundable with earned income ≥ $2,500 (amounts per IRS; confirm tax year). Full CTC generally if income ≤ $200,000 ($400,000 MFJ); phaseout above. ODC up to $500 for other dependents (separate rules).",
        [
            "SSN valid for employment for filer (or spouse if MFJ) and each qualifying child, issued before return due date",
            "Form 1040 + Schedule 8812",
            "Proof of relationship / residency / support as required",
        ],
        "Claim on Form 1040 with Schedule 8812 when you file your federal return. See IRS Child Tax Credit page for current-year rules.",
        "https://www.irs.gov/credits-deductions/individuals/child-tax-credit",
        "https://www.irs.gov/credits-deductions/individuals/child-tax-credit",
        "Internal Revenue Service (IRS)",
        ["united_states", "tax", "children", "irs", "federal", "ctc"],
        us_rules(
            notes=(
                "Qualifying child generally under 17 at year-end; relationship, residency, support, dependent, joint-return, and citizenship tests apply. "
                "Dollar amounts and phaseouts are tax-year specific."
            ),
            verify_notes="2026-09-23: IRS Child Tax Credit page. Confirm TY amounts on current IRS instructions before quoting ceilings.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-child-dependent-care-credit",
        "Child and Dependent Care Credit (CDCC) – United States",
        "बाल एवं आश्रित देखभाल क्रेडिट (CDCC) – संयुक्त राज्य अमेरिका",
        "IRS credit for child/dependent care expenses so the taxpayer (and spouse if filing jointly) can work or look for work. Notably expanded beginning tax year 2026. Claim on Form 2441.",
        "Percentage of eligible work-related care expenses (Form 2441 / Pub. 503). Beginning 2026: max percentage 50% (was 35%), floors at 20%; 20% floor applies only after AGI exceeds $206,000 MFJ / $103,000 other filers (vs $43,000 previously). Employer dependent-care exclusion max raised to $7,500 (2026). Exact expense caps: follow Form 2441.",
        [
            "Form 2441",
            "Care provider information (TIN/SSN as required)",
            "Records of qualifying care expenses",
        ],
        "File Form 2441 with your Form 1040. Review IRS 2026 Instructions for Form 2441 and Publication 503.",
        "https://www.irs.gov/forms-pubs/about-form-2441",
        "https://www.irs.gov/pub/irs-dft/i2441--dft.pdf",
        "Internal Revenue Service (IRS)",
        ["united_states", "tax", "childcare", "irs", "federal", "cdcc"],
        us_rules(
            notes=(
                "Credit for care expenses enabling work or job search; qualifying person and earned-income rules apply. "
                "2026 expansion confirmed on IRS draft 2026 Form 2441 instructions — confirm final instructions at filing time."
            ),
            verify_notes="2026-09-23: IRS draft 2026 Form 2441 instructions. Expense caps and edge cases: verify on final Form 2441 / Pub. 503.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-premium-tax-credit",
        "Premium Tax Credit (PTC) – ACA Marketplace (United States)",
        "प्रीमियम टैक्स क्रेडिट (PTC) – ACA मार्केटप्लेस",
        "IRS / Healthcare.gov credit that lowers monthly Marketplace health insurance premiums. Advance PTC is reconciled on Form 8962. Cost-sharing reductions (CSR) may further lower out-of-pocket costs on Silver plans when income qualifies — see Healthcare.gov.",
        "Monthly premium subsidy (advance) and/or year-end credit. Exact savings depend on household income, location, and plan. CSR (related): additional deductible/copay savings generally require a Silver plan when Marketplace results show CSR eligibility.",
        [
            "Marketplace application / eligibility determination",
            "Form 1095-A (if advance PTC)",
            "Form 8962 with Form 1040 to reconcile",
        ],
        "Apply for coverage and savings at HealthCare.gov (or your state Marketplace) during Open Enrollment or a Special Enrollment Period. Reconcile advance PTC on Form 8962 when you file taxes.",
        "https://www.healthcare.gov/lower-costs/save-on-monthly-premiums/",
        "https://www.irs.gov/individuals-and-families/eligibility-for-the-premium-tax-credit",
        "Centers for Medicare & Medicaid Services (CMS) / IRS / HealthCare.gov",
        ["united_states", "health", "aca", "marketplace", "tax", "federal", "ptc"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Marketplace enrollment; not eligible for affordable employer coverage providing minimum value or other government coverage (Medicare/Medicaid/TRICARE etc.) for the month; "
                "premiums paid by return due date; generally household income at least 100% FPL and (for years other than temporary ARPA expansions) no more than 400% FPL; "
                "generally cannot file MFS (limited exceptions); cannot be another’s dependent. Enhanced PTC expansions were temporary — confirm TY2026 Form 8962 / Healthcare.gov materials."
            ),
            verify_notes=(
                "2026-09-23: Healthcare.gov + IRS PTC eligibility. Confirm current-year FPL band and any temporary expansions on Form 8962 TY2026 instructions before encoding hard caps. "
                "CSR income bands: confirm on Healthcare.gov Open Enrollment materials (not separately invented here)."
            ),
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-medicare-savings-programs",
        "Medicare Savings Programs (QMB / SLMB / QI / QDWI) – United States",
        "मेडिकेयर बचत कार्यक्रम (QMB / SLMB / QI / QDWI)",
        "State Medicaid programs that help pay Medicare Part A/B premiums and, for QMB, deductibles/coinsurance/copays. Apply through your state Medicaid office.",
        "QMB: Part A/B premiums + deductibles/coinsurance/copays. SLMB/QI: Part B premiums (QI is first-come, annual apply). QDWI: Part A premiums for certain working disabled who lost premium-free Part A. 2026 federal monthly income/resource limits published on Medicare.gov (states may be more generous; AK/HI slightly higher).",
        [
            "Medicare information",
            "Income and resource documentation",
            "State Medicaid / MSP application",
        ],
        "Apply through your state Medicaid agency (Medicare Savings Programs). See medicare.gov for federal limits and state contacts.",
        "https://www.medicare.gov/basics/costs/help/medicare-savings-programs",
        "https://www.medicare.gov/basics/costs/help/medicare-savings-programs",
        "State Medicaid agencies / CMS Medicare",
        ["united_states", "medicare", "medicaid", "health", "federal", "msp"],
        us_rules(
            implies_low_income=True,
            notes=(
                "2026 federal limits (Medicare.gov; states may be more generous): "
                "QMB individual/couple monthly income $1,350 / $1,824; SLMB $1,616 / $2,184; QI $1,816 / $2,455; resources $9,950 / $14,910 (indiv/couple) for QMB/SLMB/QI; "
                "QDWI $5,405 / $7,299 income and $4,000 / $6,000 resources. Alaska/Hawaii slightly higher."
            ),
            verify_notes="2026-09-23: medicare.gov MSP page. Confirm current-year limits and state expansions at application time.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-extra-help",
        "Extra Help (Medicare Part D Low-Income Subsidy) – United States",
        "एक्स्ट्रा हेल्प (मेडिकेयर पार्ट D लो-इनकम सब्सिडी)",
        "SSA / Medicare program that lowers Part D prescription drug premiums, deductibles, and copays for people with limited income and resources. Automatic if full Medicaid, certain MSPs, or SSI.",
        "Lower or $0 Part D premiums/deductibles and reduced drug copays. Exact copay amounts change by year — see medicare.gov. Not available in Puerto Rico / some territories (local alternatives).",
        [
            "Social Security / Medicare information",
            "Income and resource documentation (unless automatic eligibility)",
            "SSA Extra Help application (Form SSA-1020) if not automatic",
        ],
        "Apply anytime with Social Security (ssa.gov/medicare/part-d-extra-help) or see medicare.gov drug-cost help. Automatic enrollment if you have full Medicaid, MSP paying Part B, or SSI.",
        "https://www.ssa.gov/medicare/part-d-extra-help",
        "https://www.medicare.gov/basics/costs/help/drug-costs",
        "Social Security Administration / CMS Medicare",
        ["united_states", "medicare", "prescriptions", "ssa", "federal", "extra-help"],
        us_rules(
            implies_low_income=True,
            max_annual_income=23940,
            notes=(
                "2026 income ≤ $23,940 individual / $32,460 couple; resources ≤ $18,090 / $36,100 (medicare.gov / SSA). "
                "Automatic if full Medicaid, MSP (state pays Part B), or SSI. Couple figures and exclusions (burial funds etc.) follow official rules."
            ),
            verify_notes="2026-09-23: medicare.gov drug-costs + SSA Extra Help. Copays and exact resource exclusions: verify on live pages annually.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-pell-grant",
        "Federal Pell Grant – United States",
        "संघीय पेल ग्रांट – संयुक्त राज्य अमेरिका",
        "Need-based federal grant for eligible undergraduates who demonstrate financial need via the FAFSA. Primary free college aid for many low- and moderate-income students.",
        "Grant amount depends on Student Aid Index, cost of attendance, and enrollment intensity. Maximum award is set by award year (confirm current maximum on StudentAid.gov; recent announcements have cited ~$7,395 — verify before quoting).",
        [
            "FAFSA (Free Application for Federal Student Aid)",
            "Citizenship / eligible noncitizen documentation as required",
            "School enrollment in an eligible program; Satisfactory Academic Progress",
        ],
        "Complete the FAFSA at studentaid.gov. Your school packages Pell if you qualify. Check FAFSA deadlines on StudentAid.gov.",
        "https://studentaid.gov/apply-for-aid/fafsa/fafsa-deadlines/",
        "https://studentaid.gov/understand-aid/types/grants/pell",
        "U.S. Department of Education / Federal Student Aid",
        ["united_states", "education", "grant", "pell", "fafsa", "federal"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Generally for undergraduates without a bachelor’s/graduate/professional degree who show need via FAFSA; "
                "citizenship/eligible noncitizen, eligible program enrollment, and SAP rules apply. Award varies — do not invent a single household income ceiling."
            ),
            verify_notes="2026-09-23: studentaid.gov Pell + award-year announcements. Confirm current award-year maximum before quoting a dollar figure.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-weatherization-assistance",
        "Weatherization Assistance Program (WAP) – United States",
        "वेदरराइजेशन असिस्टेंस प्रोग्राम (WAP)",
        "DOE program that funds free or low-cost home energy efficiency upgrades (insulation, air sealing, etc.) for income-eligible households — distinct from LIHEAP bill payment. Apply via local WAP agency.",
        "No-cost or low-cost weatherization measures that permanently reduce energy use/bills. Local waitlists common. Homeowners and renters (with landlord permission) may qualify.",
        [
            "Proof of income or categorical eligibility (e.g. SSI / LIHEAP criteria where used)",
            "Proof of residence / ownership or landlord permission for renters",
            "Local WAP agency application",
        ],
        "Contact your local Weatherization Assistance agency (see energy.gov how-to-apply). Priority often given to elderly, disability, children, and high energy burden households.",
        "https://www.energy.gov/cmei/scep/wap/how-apply-weatherization-assistance",
        "https://www.energy.gov/cmei/scep/wap/how-apply-weatherization-assistance",
        "U.S. Department of Energy / state & local WAP grantees",
        ["united_states", "energy", "weatherization", "doe", "federal", "housing"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Households at or below 200% of poverty guidelines, or receiving SSI; states may use LIHEAP criteria (up to 60% state median income). "
                "Categorical expansions exist for certain HUD/USDA means-tested participants (WPN guidance). Priority: elderly, disability, children, high energy use/burden."
            ),
            verify_notes="2026-09-23: energy.gov WAP how-to-apply. Local agency income rules and waitlists vary — verify with the local provider.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-home-energy-rebates",
        "Home Energy Rebates (HOMES + HEEHR / HEEHRA) – United States",
        "होम एनर्जी रिबेट्स (HOMES + HEEHR) – संयुक्त राज्य अमेरिका",
        "IRA federal home energy rebate programs administered by states/Tribes: HOMES whole-home upgrades and High-Efficiency Electric Home Rebates (point-of-sale appliances/envelope/wiring/HVAC). Availability and rules are state-dependent.",
        "HOMES: whole-home upgrades (modeled savings path, minimum ~20% savings); rebates up to $8,000 (grantees may increase for <80% AMI). HEEHR: point-of-sale rebates up to $14,000 for eligible measures. Funding authority through Sept 30, 2031. Exact products and income rules set by state/Tribal energy office.",
        [
            "State/Tribal energy office rebate application",
            "Income documentation if required by the state program",
            "Contractor / project documentation as required",
        ],
        "Check your state or Tribal energy office and energy.gov/save / Home Energy Rebates program pages for launch status and how to apply. Not all states have opened applications yet.",
        "https://www.energy.gov/cmei/scep/home-energy-rebates-program",
        "https://www.energy.gov/cmei/scep/home-energy-rebates-program",
        "U.S. Department of Energy / state & Tribal energy offices",
        ["united_states", "ira", "energy", "rebate", "doe", "federal"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Available in select states; state/Tribal energy office sets products, income rules, and launch status. "
                "Do not assume nationwide open enrollment. IRA §50121 HOMES and §50122 HEEHR."
            ),
            verify_notes="2026-09-23: energy.gov Home Energy Rebates. Confirm state launch status and income tiers with the state energy office before advising a household.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-lifeline",
        "Lifeline (phone/internet discount) – United States",
        "लाइफलाइन (फोन/इंटरनेट छूट) – संयुक्त राज्य अमेरिका",
        "FCC affordability program providing a monthly discount on phone or internet service for qualifying low-income households. The Affordable Connectivity Program (ACP) ended June 1, 2024 — Lifeline is the remaining national FCC program.",
        "Discount up to $9.25/month ($34.25 on Tribal lands) per FCC. One benefit per household.",
        [
            "Proof of income ≤ 135% FPL or proof of qualifying program participation (Medicaid, SNAP, SSI, Federal Public Housing Assistance, Veterans Pension/Survivors Benefit, Tribal pathways, etc.)",
            "Lifeline application via company or National Verifier",
        ],
        "Apply through a participating Lifeline provider or the National Verifier. See fcc.gov/lifeline-consumers and lifelinesupport.org.",
        "https://www.lifelinesupport.org/how-to-apply/",
        "https://www.fcc.gov/lifeline-consumers",
        "Federal Communications Commission (FCC) / Universal Service Administrative Company",
        ["united_states", "broadband", "phone", "fcc", "federal", "lifeline"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Income ≤ 135% FPL (see current LifelineSupport.org table), OR household participates in Medicaid, SNAP, SSI, Federal Public Housing Assistance "
                "(incl. HCV, PBRA, Public Housing), Veterans Pension/Survivors Benefit; Tribal and survivor pathways exist. One benefit per household. ACP is ended — do not present ACP as live."
            ),
            verify_notes="2026-09-23: FCC Lifeline + LifelineSupport.org. Confirm current FPL table and provider list at application time.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-public-housing",
        "HUD Public Housing – United States",
        "HUD सार्वजनिक आवास – संयुक्त राज्य अमेरिका",
        "HUD program in which local Public Housing Agencies (PHAs) own/operate affordable rental housing for low-income families, elderly, and persons with disabilities. Distinct from Housing Choice Vouchers (Section 8).",
        "Affordable rent typically based on Total Tenant Payment (~30% of adjusted income under HUD formula). Waitlists often long or closed — contact your local PHA.",
        [
            "PHA application",
            "Income documentation",
            "Citizenship or eligible immigration status documentation",
            "Screening / references as required by the PHA",
        ],
        "Apply through your local Public Housing Agency. Find PHA contacts via HUD. Waitlist status varies by locality.",
        "https://www.hud.gov/helping-americans/public-housing",
        "https://www.hud.gov/helping-americans/public-housing",
        "U.S. Department of Housing and Urban Development / local PHAs",
        ["united_states", "housing", "hud", "public-housing", "federal"],
        us_rules(
            implies_low_income=True,
            notes=(
                "PHA determines eligibility based on (1) annual gross income, (2) elderly/disability/family qualification, (3) U.S. citizenship or eligible immigration status; references/screening apply. "
                "HUD income limits: low-income 80% AMI, very low-income 50% AMI (vary by area). Do not encode a single national dollar ceiling."
            ),
            verify_notes="2026-09-23: hud.gov public housing. Confirm local PHA income limits and waitlist status.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-head-start",
        "Head Start / Early Head Start – United States",
        "हेड स्टार्ट / अर्ली हेड स्टार्ट – संयुक्त राज्य अमेरिका",
        "Free early learning and family support for eligible children ages birth to 5 (Early Head Start may include prenatal services). Apply via local Head Start programs.",
        "Free early childhood education and related family services. Waitlists possible.",
        [
            "Local Head Start / Early Head Start application",
            "Proof of income or categorical eligibility (TANF, SSI, SNAP, foster care, homelessness)",
            "Child age / birth documentation as required",
        ],
        "Find and apply to a local program via headstart.gov how-to-apply / program locator.",
        "https://headstart.gov/how-apply",
        "https://headstart.gov/how-apply",
        "U.S. Department of Health and Human Services / local Head Start grantees",
        ["united_states", "education", "children", "head-start", "federal"],
        us_rules(
            implies_low_income=True,
            max_age=5,
            notes=(
                "Household income at or below poverty guidelines; OR family receives TANF, SSI, or SNAP; OR child in foster care / experiencing homelessness — qualify regardless of income. "
                "Ages birth to 5; some Early Head Start prenatal services."
            ),
            verify_notes="2026-09-23: headstart.gov how-apply. Confirm local program slots and any additional eligibility priorities.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-school-meals",
        "Free and Reduced-Price School Meals (NSLP / SBP) – United States",
        "निःशुल्क व रियायती स्कूल भोजन (NSLP / SBP)",
        "USDA National School Lunch Program and School Breakfast Program: free or reduced-price meals for eligible schoolchildren. Many children are directly certified via SNAP (and often TANF).",
        "Daily free or reduced-price breakfast and/or lunch at participating schools during the school year (and sometimes summer options via related programs).",
        [
            "School / district meal application (unless directly certified)",
            "Income information or case number for SNAP/TANF if applicable",
        ],
        "Apply through your local school or school district anytime. Households receiving SNAP are often directly certified for free meals. See FNS NSLP household page.",
        "https://www.fns.usda.gov/nslp/household",
        "https://www.fns.usda.gov/nslp/household",
        "USDA Food and Nutrition Service / local school food authorities",
        ["united_states", "food", "children", "school", "usda", "federal"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Eligibility via current Income Eligibility Guidelines on the school application; automatic free meals if household receives SNAP (and often TANF). "
                "WIC/unemployment may indicate possible eligibility — contact the school. Do not invent a single national annual income ceiling (IEGs vary by household size and year)."
            ),
            verify_notes="2026-09-23: fns.usda.gov NSLP household + Income Eligibility Guidelines FR notice. Confirm current IEG table for the school year.",
        ),
    )
)

US_NEW.append(
    us_scheme(
        "us-savers-credit",
        "Retirement Savings Contributions Credit (Saver’s Credit) – United States",
        "रिटायरमेंट सेविंग्स कंट्रीब्यूशन क्रेडिट (सेवर्स क्रेडिट)",
        "IRS nonrefundable credit for eligible contributions to an IRA, workplace retirement plan, or ABLE account (rules on IRS pages). Form 8880. Note: Saver’s Match is scheduled to replace the credit for retirement contributions starting with 2027 contributions (claimed on the 2027 return filed 2028); ABLE contributions may still use a credit path per IRS notices.",
        "Credit for a percentage of eligible contributions; commonly described as up to $1,000 ($2,000 joint) — confirm on current Form 8880. Income, age, dependency, student, and tax-liability limits apply.",
        [
            "Form 8880 with Form 1040",
            "Records of eligible retirement / ABLE contributions",
        ],
        "Claim on Form 8880 when you file your federal return. Review IRS Saver’s Credit and Tax Topic 610. Watch for Saver’s Match transition starting with 2027 contributions.",
        "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-savings-contributions-credit-savers-credit",
        "https://www.irs.gov/taxtopics/tc610",
        "Internal Revenue Service (IRS)",
        ["united_states", "tax", "retirement", "irs", "federal", "savers-credit"],
        us_rules(
            implies_low_income=True,
            notes=(
                "Eligible contributions to IRA/workplace plan/ABLE subject to IRS rules; income/age/dependency/student/tax-liability limits apply. "
                "Saver’s Match scheduled to replace the credit for retirement contributions starting with 2027 contributions — encode carefully until regulations finalize."
            ),
            verify_notes=(
                "2026-09-23: IRS Saver’s Credit + Topic 610 + Saver’s Match page. Confirm Form 8880 current-year income bands and Match implementation details before advising."
            ),
        ),
    )
)


def main() -> None:
    schemes: list[dict] = json.loads(DATA.read_text())
    before = len(schemes)
    by_id = {s["id"]: i for i, s in enumerate(schemes)}

    replaced = []
    added = []

    # REPLACE ladli → lakhpati (rename id in place)
    if "dl-ladli-scheme" in by_id:
        idx = by_id["dl-ladli-scheme"]
        schemes[idx] = LAKHPATI
        replaced.append("dl-ladli-scheme -> dl-lakhpati-bitiya")
        by_id.pop("dl-ladli-scheme")
        by_id["dl-lakhpati-bitiya"] = idx
    elif "dl-lakhpati-bitiya" in by_id:
        schemes[by_id["dl-lakhpati-bitiya"]] = LAKHPATI
        replaced.append("dl-lakhpati-bitiya (refresh)")
    else:
        schemes.append(LAKHPATI)
        added.append("dl-lakhpati-bitiya")
        by_id["dl-lakhpati-bitiya"] = len(schemes) - 1

    # Optional freshness bump for hr-ddlly
    if "hr-ddlly" in by_id:
        schemes[by_id["hr-ddlly"]]["last_verified"] = LAST

    for s in INDIA_NEW + US_NEW:
        sid = s["id"]
        if sid in by_id:
            schemes[by_id[sid]] = s
            replaced.append(f"{sid} (overwrite)")
        else:
            schemes.append(s)
            added.append(sid)
            by_id[sid] = len(schemes) - 1

    # Uniqueness check
    ids = [s["id"] for s in schemes]
    assert len(ids) == len(set(ids)), f"Duplicate ids: {[i for i in ids if ids.count(i) > 1]}"

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    after = len(schemes)
    scope_addendum = (
        " Catalogue refresh 2026-09-23: India PM Surya Ghar + Delhi rooftop solar subsidy; "
        "Delhi Lakhpati Bitiya (replaces Ladli); VB-G RAM G Act rural employment; PM Vishwakarma; "
        "US federal household pack (EITC, CTC, CDCC, PTC, MSP, Extra Help, Pell, WAP, Home Energy Rebates, "
        "Lifeline, Public Housing, Head Start, school meals, Saver’s Credit)."
    )

    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = after
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        if "Catalogue refresh 2026-09-23" not in scope:
            meta["scope"] = scope.rstrip() + scope_addendum
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    # Sync check
    assert DATA.read_text() == FE_DATA.read_text()
    assert json.loads(META.read_text())["scheme_count"] == after
    assert json.loads(FE_META.read_text())["updated_as_of"] == LAST

    print(f"BEFORE: {before}")
    print(f"AFTER:  {after}")
    print(f"DELTA:  {after - before}")
    print("REPLACED:", replaced)
    print("ADDED:", added)
    print("SKIPPED (as planned): PM-KUSUM, DEPwD UDID funding, ASIC, 25C/25D, ACP, LIHWAP")
    print("hr-ddlly last_verified bumped:", "hr-ddlly" in by_id)


if __name__ == "__main__":
    main()
