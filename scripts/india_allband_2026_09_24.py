#!/usr/bin/env python3
"""India all-band deepen 2026-09-24: middle-class / high-income-eligible / universal.

Authoritative research: /workspace/india-allband-report.md
Official .gov.in / Income Tax / NSI-India Post / PFRDA / MoE / MoLE / MoSJE / MHI only.
Never invent eligibility. verify=true where amounts/windows vary.
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
LAST = "2026-09-24"
ISO = "2026-09-24T07:30:00+05:30"
ML_PREFIX = "(EN — Malayalam review pending) "

EXPECTED_IDS = [
    "in-ppf",
    "in-nsc",
    "in-scss",
    "in-section-80c-deductions",
    "in-section-24b-home-loan-interest",
    "in-section-80eea",
    "in-nps-tier-ii",
    "in-pm-e-drive",
    "in-startup-india",
    "in-pm-usp-csss",
    "in-nmms",
    "in-pm-usp-csis",
    "in-pm-kmy",
    "in-pm-sym",
    "in-namaste",
]


def L(en: str, hi: str | None = None, ml: str | None = None, *, india_ml: bool = True) -> dict:
    return {"en": en, "hi": hi or en, "ml": ml if ml is not None else ML_PREFIX + en}


def docs(items: list[str], *, india_ml: bool = True) -> dict:
    return {
        "en": items,
        "hi": items,
        "ml": [ML_PREFIX + i if not i.startswith("(EN") else i for i in items],
    }


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
        "scheme_name": L(name_en, hi=name_hi),
        "description": L(desc_en, hi=desc_hi),
        "eligibility_rules": erules,
        "benefits": L(benefits_en, hi=benefits_hi),
        "required_documents": docs(docs_en),
        "how_to_apply": L(how_en, hi=how_hi),
        "apply_url": apply_url,
        "office_type": office,
        "official_source_url": official,
        "tags": tags,
        "last_verified": LAST,
        "nationwide": nationwide_top,
    }


NEW: list[dict] = []

# ---------------------------------------------------------------------------
# 1 PPF
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-ppf",
        "Public Provident Fund (PPF)",
        "पब्लिक प्रोविडेंट फंड (पीपीएफ)",
        "Government small-savings account under the Public Provident Fund Scheme, 2019, available at India Post and authorised banks; long-horizon retirement/savings vehicle with no personal income ceiling.",
        "सार्वजनिक भविष्य निधि योजना, 2019 के तहत डाकघर/अधिकृत बैंकों में दीर्घकालिक बचत खाता; व्यक्तिगत आय सीमा नहीं।",
        "Deposits ₹500–₹1.5 lakh per financial year (multiples of ₹50); one account per adult plus guardian accounts for minors within the combined ₹1.5 lakh annual ceiling; interest notified by MoF; deposits commonly qualify under Income-tax Act section 80C when claimed under the applicable tax regime — confirm live IT/NSI rules. Benefits middle-class and higher-income savers equally (no income gate).",
        "वित्तीय वर्ष में ₹500–₹1.5 लाख जमा; वयस्क एक खाता + अभिभावक खाते संयुक्त सीमा के भीतर; ब्याज वित्त मंत्रालय द्वारा अधिसूचित; सामान्यतः धारा 80C — लागू कर व्यवस्था की पुष्टि करें।",
        [
            "KYC identity and address proof of account holder / guardian",
            "PAN as required by accounts office",
            "Birth proof for minor accounts",
            "Account-opening Form-1 as per scheme",
        ],
        "Open at India Post or authorised bank branches under POSB/NSI PPF rules.",
        "भारत डाक या अधिकृत बैंक शाखा में पीपीएफ खाता खोलें।",
        "https://www.indiapost.gov.in/",
        "https://www.indiapost.gov.in/",
        "Department of Posts / National Savings Institute / authorised banks",
        ["savings", "ppf", "tax", "middle-class", "universal", "central", "nationwide", "post_office"],
        base_rules(
            min_age=None,
            notes=(
                "Resident Indian adult may open a single PPF account; guardian may open one account per minor/person of unsound mind "
                "(combined annual deposit ceiling ₹1.5 lakh across own + minor accounts). Joint accounts not permitted. "
                "NRIs cannot open new PPF accounts under scheme rules. No personal max_annual_income ceiling — do not set implies_low_income. "
                "Benefits middle-class and higher-income resident savers who can deposit within the ₹1.5 lakh/FY cap. "
                "Tax treatment (EEE / 80C) depends on the tax regime chosen for the year — confirm Income Tax Department guidance."
            ),
            verify_notes=(
                "2026-09-24: India Post Post Office Saving Schemes + PPF Scheme 2019 (G.S.R. 915(E)). "
                "Confirm current MoF interest notification and live IT regime interaction before advising."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 2 NSC
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-nsc",
        "National Savings Certificate (NSC) — VIII Issue",
        "राष्ट्रीय बचत प्रमाणपत्र (एनएससी) — VIII अंक",
        "Five-year National Savings Certificate (VIII Issue) sold through India Post / authorised channels; popular tax-saving small-savings instrument with no maximum deposit and no personal income ceiling.",
        "पाँच वर्षीय राष्ट्रीय बचत प्रमाणपत्र (VIII); अधिकतम जमा सीमा नहीं; व्यक्तिगत आय सीमा नहीं।",
        "Minimum deposit commonly ₹1,000 in multiples of ₹100; no maximum; 5-year maturity; interest notified periodically; deposits commonly qualify under section 80C (applicable tax regime). Accrued interest treatment per IT rules. Useful for middle-class and higher-income savers.",
        "न्यूनतम सामान्यतः ₹1,000; अधिकतम सीमा नहीं; 5 वर्ष परिपक्वता; सामान्यतः धारा 80C।",
        [
            "KYC identity and address proof",
            "PAN as required",
            "Application Form as prescribed by Post Office / bank",
        ],
        "Purchase at India Post or authorised outlets under NSC VIII Issue rules.",
        "भारत डाक / अधिकृत केंद्र पर एनएससी खरीदें।",
        "https://www.indiapost.gov.in/",
        "https://www.indiapost.gov.in/",
        "Department of Posts / National Savings Institute",
        ["savings", "nsc", "tax", "middle-class", "universal", "central", "nationwide", "post_office"],
        base_rules(
            notes=(
                "Eligible: resident individuals (single adult; joint up to three adults; guardian for minor/unsound mind; minor ≥10 in own name) per India Post / NSI scheme features. "
                "NRIs / HUF / trusts generally cannot open new NSC per scheme notes. No personal income ceiling — leave max_annual_income null; do not set implies_low_income. "
                "Benefits middle-class and higher-income resident investors; no deposit maximum."
            ),
            verify_notes=(
                "2026-09-24: India Post NSC features + NSI NSC VIII materials. Confirm live interest rate and 80C interaction under chosen tax regime."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 3 SCSS
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-scss",
        "Senior Citizens Savings Scheme (SCSS)",
        "वरिष्ठ नागरिक बचत योजना (एससीएसएस)",
        "Five-year (extendable) small-savings deposit for senior citizens at Post Offices and authorised banks under the Senior Citizens’ Savings Scheme, 2019 (as amended); no personal income ceiling.",
        "वरिष्ठ नागरिकों के लिए पाँच वर्षीय (विस्तार योग्य) बचत जमा; व्यक्तिगत आय सीमा नहीं।",
        "Quarterly interest at MoF-notified SCSS rate (interest is taxable). Deposit commonly qualifies under section 80C when claimed under the applicable regime. Maximum deposit ₹30 lakh per individual across accounts (G.S.R. 240(E) 31.03.2023). Benefits middle- and higher-income seniors who meet age/retirement gates.",
        "त्रैमासिक ब्याज (कर योग्य); अधिकतम जमा ₹30 लाख; सामान्यतः धारा 80C — लागू व्यवस्था की पुष्टि करें।",
        [
            "Age / retirement proof as applicable (60+, or retired 55–59 / defence rules)",
            "KYC identity and address proof",
            "PAN",
            "Deposit funds (min ₹1,000 multiples) within scheme ceiling",
        ],
        "Open at India Post or authorised bank under SCSS 2019 rules.",
        "भारत डाक या अधिकृत बैंक में एससीएसएस खाता खोलें।",
        "https://www.indiapost.gov.in/",
        "https://www.indiapost.gov.in/",
        "Department of Posts / National Savings Institute / authorised banks",
        ["savings", "scss", "tax", "middle-class", "senior", "central", "nationwide", "post_office"],
        base_rules(
            min_age=60,
            notes=(
                "Primary gate: attained age 60 on opening date. Also: age 55–59 who retired on superannuation/otherwise and open within the scheme’s stated window after receipt of retirement benefits with employer certificate "
                "(confirm live rule text — historically one month in 2019 notification; verify current amendment). "
                "Retired Defence Services personnel (excluding civilian defence employees) may open from age 50 subject to specified conditions. "
                "Individual or joint with spouse (first holder must meet age). Deposit min ₹1,000 multiples; maximum ₹30 lakh. HUF/NRI not eligible per scheme history/PIB. "
                "No personal income ceiling — leave max_annual_income null; do not set implies_low_income. Higher-income seniors meeting age rules are eligible."
            ),
            verify_notes=(
                "2026-09-24: SCSS 2019 + ₹30 lakh amendment G.S.R. 240(E); India Post scheme pages. Confirm live interest rate, retirement-window timing, and tax regime interaction."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 4 Section 80C umbrella
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-section-80c-deductions",
        "Income-tax Section 80C deductions (savings & specified payments)",
        "आयकर धारा 80C कटौतियाँ (बचत और निर्दिष्ट भुगतान)",
        "Citizen-facing Income Tax Department framework for deduction under section 80C of the Income-tax Act for specified investments and payments (e.g. life insurance premium, PPF, NSC, SCSS, ELSS, tuition fees, principal repayment of housing loan) subject to the overall Chapter VIA ceiling and the tax regime chosen.",
        "आयकर अधिनियम धारा 80C के तहत निर्दिष्ट निवेश/भुगतान पर कटौती — लागू कर व्यवस्था और समग्र सीमा के अधीन।",
        "Combined deduction under sections 80C, 80CCC and 80CCD(1) commonly capped at ₹1.5 lakh per year when claimed under the old/optional regime that allows Chapter VIA deductions. New/default tax regime generally does not allow most 80C-type deductions — confirm live ITR help for the assessment year. Benefits middle-class and higher-income taxpayers who have eligible outflows and choose a regime that permits the deduction.",
        "सामान्यतः 80C/80CCC/80CCD(1) संयुक्त सीमा ₹1.5 लाख (पुरानी/वैकल्पिक व्यवस्था); नई व्यवस्था में प्रायः अनुपलब्ध — जीवंत आईटीआर सहायता देखें।",
        [
            "PAN and ITR as applicable",
            "Proof of eligible investments/payments (PPF passbook, NSC, insurance premium receipts, housing-loan principal certificate, etc.)",
        ],
        "Claim while filing Income Tax Return on the Income Tax e-Filing portal; invest via Post Office/banks/AMCs as applicable.",
        "आयकर ई-फाइलिंग पोर्टल पर आईटीआर दाखिल करते समय दावा करें।",
        "https://www.incometax.gov.in/iec/foportal/",
        "https://www.incometax.gov.in/iec/foportal/",
        "Income Tax Department / CBDT",
        ["tax", "80c", "middle-class", "savings", "central", "nationwide"],
        base_rules(
            notes=(
                "Not a welfare cash transfer — a statutory tax deduction. No income ceiling to ‘qualify’ for 80C itself; usefulness rises with taxable income under a regime that allows Chapter VIA. "
                "Leave max_annual_income null; do not set implies_low_income. Concrete products PPF/NSC/SCSS/Sukanya/NPS also catalogued separately. "
                "ELSS and other market products are SEBI-regulated — catalogue points to IT Act deduction framing only."
            ),
            verify_notes=(
                "2026-09-24: Income Tax e-Filing portal + ITD tutorials referencing section 80C. Confirm AY-specific regime rules and ₹1.5 lakh combined ceiling before advising."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 5 Section 24(b)
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-section-24b-home-loan-interest",
        "Home-loan interest deduction — Income-tax Section 24(b)",
        "गृह ऋण ब्याज कटौती — आयकर धारा 24(b)",
        "Deduction of interest on capital borrowed for acquisition/construction/repair of house property under section 24(b) of the Income-tax Act, as explained by the Income Tax Department house-property guidance.",
        "गृह संपत्ति हेतु उधार पूंजी पर ब्याज की धारा 24(b) कटौती।",
        "Self-occupied residential property: interest on capital borrowed for acquisition/construction commonly deductible up to ₹2 lakh (conditions include loan on/after 01-04-1999 and completion within 5 years per ITD guidance). Let-out property: actual interest generally allowable. Pre-construction interest in five equal instalments after completion. Benefits middle-class and higher-income homeowners with housing loans — no scheme income ceiling.",
        "स्व-अध्यसित संपत्ति पर सामान्यतः अधिकतम ₹2 लाख ब्याज कटौती (शर्तों सहित); किराए पर दी संपत्ति पर वास्तविक ब्याज — आयकर विभाग मार्गदर्शन देखें।",
        [
            "Housing loan interest certificate from lender",
            "Property and loan documents",
            "PAN / ITR filing credentials",
        ],
        "Claim in the Income Tax Return under Income from House Property on the e-Filing portal.",
        "ई-फाइलिंग पोर्टल पर गृह संपत्ति आय के अंतर्गत आईटीआर में दावा करें।",
        "https://www.incometax.gov.in/iec/foportal/",
        "https://incometaxindia.gov.in/Documents/Left%20Menu/income-from-house-property.htm",
        "Income Tax Department / CBDT",
        ["tax", "housing", "home_loan", "middle-class", "central", "nationwide"],
        base_rules(
            notes=(
                "Statutory tax deduction, not a subsidy payout. No max_annual_income ceiling on claiming 24(b) itself — leave null; do not set implies_low_income. "
                "Higher-income homeowners with eligible interest can benefit. Interaction with new vs old tax regime and with sections 80EE/80EEA — confirm live ITD guidance for the assessment year."
            ),
            verify_notes=(
                "2026-09-24: ITD ‘Income from house property’ page (§24(b) limits). Confirm AY regime rules and exact monetary caps before advising."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 6 Section 80EEA
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-section-80eea",
        "Additional affordable home-loan interest deduction — Section 80EEA",
        "किफायती गृह ऋण अतिरिक्त ब्याज कटौती — धारा 80EEA",
        "Additional deduction (over section 24(b)) of up to ₹1.5 lakh for interest on loan taken for affordable residential house property under section 80EEA, for individuals meeting stamp-duty, first-home, and loan-sanction window conditions.",
        "धारा 80EEA के तहत किफायती आवास ऋण ब्याज पर अतिरिक्त कटौती (अधिकतम ₹1.5 लाख) — स्वीकृति खिड़की और शर्तों सहित।",
        "Deduction up to ₹1,50,000 for interest, typically after exhausting section 24(b), when conditions are met. Loan must have been sanctioned by a financial institution between 01-04-2019 and 31-03-2022; stamp duty value ≤ ₹45 lakh; assessee owned no residential house on sanction date; not eligible to claim section 80EE. New tax regime generally disallows this Chapter VIA deduction — confirm live ITR help. Still relevant for middle-income buyers who took qualifying loans in the window.",
        "अधिकतम ₹1.5 लाख; ऋण स्वीकृति 01-04-2019 से 31-03-2022; स्टांप ≤₹45 लाख; प्रथम आवास; 80EE नहीं — जीवंत नियम देखें।",
        [
            "Loan sanction letter showing date within 01-04-2019 to 31-03-2022",
            "Stamp duty value evidence ≤ ₹45 lakh",
            "Interest certificate; declaration of no other residential house on sanction date",
            "ITR / PAN",
        ],
        "Claim in ITR Schedule VIA on the Income Tax e-Filing portal if conditions met (old/optional regime).",
        "शर्तें पूर्ण होने पर ई-फाइलिंग पोर्टल पर आईटीआर में दावा करें।",
        "https://www.incometax.gov.in/iec/foportal/",
        "https://www.incometaxindia.gov.in/w/section-80eea-2",
        "Income Tax Department / CBDT",
        ["tax", "housing", "home_loan", "middle-class", "80eea", "central", "nationwide"],
        base_rules(
            notes=(
                "Sanction window closed 31-03-2022 — no new loans after that date qualify; existing eligible borrowers may continue claiming while interest is paid and conditions hold. "
                "Not for high-value homes above stamp ₹45 lakh. Leave max_annual_income null (no separate income ceiling in section text beyond property value); do not set implies_low_income. "
                "Tag middle-class: targets affordable first homes."
            ),
            verify_notes=(
                "2026-09-24: ITD section 80EEA page + e-Filing AY help (sanction 1 Apr 2019–31 Mar 2022). Confirm regime availability each AY."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 7 NPS Tier II
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-nps-tier-ii",
        "National Pension System — Tier II (voluntary)",
        "राष्ट्रीय पेंशन प्रणाली — टियर II (स्वैच्छिक)",
        "Optional NPS Tier II investment account available to subscribers who already hold an active NPS Tier I account; flexible withdrawals; distinct from Tier I tax-advantaged retirement account and from Atal Pension Yojana.",
        "सक्रिय टियर I वाले अभिदाताओं के लिए वैकल्पिक टियर II खाता; लचीली निकासी; टियर I कर लाभ से भिन्न।",
        "Market-linked voluntary investments with unrestricted withdrawals per PFRDA rules. Per PFRDA All Citizen Model FAQs, Tier II contributions generally do not get the special tax deductions available to Tier I (80CCD / 80CCD(1B)) — confirm live PFRDA/IT guidance. Useful liquidity sleeve for middle-class and higher-income NPS subscribers; no income ceiling.",
        "लचीली निकासी; सामान्यतः टियर II पर 80CCD-प्रकार कटौती नहीं (टियर I से भिन्न) — पीएफआरडीए/आयकर पुष्टि करें।",
        [
            "Active NPS Tier I PRAN",
            "KYC as required by eNPS / PoP",
            "Bank account for contributions",
        ],
        "Activate via eNPS / Point of Presence after Tier I is active (resident citizens per PFRDA; NRI/OCI Tier II limits — confirm live FAQ).",
        "सक्रिय टियर I के बाद ईएनपीएस / पीओपी के माध्यम से सक्रिय करें।",
        "https://pfrda.org.in/schemes/national-pension-system/nps-for-all-citizen-models",
        "https://pfrda.org.in/schemes/national-pension-system/nps-for-all-citizen-models",
        "PFRDA / NPS Trust / Points of Presence",
        ["pension", "nps", "tier-ii", "middle-class", "savings", "central", "nationwide", "pfrda"],
        base_rules(
            min_age=18,
            max_age=70,
            notes=(
                "Requires active Tier I. Age band commonly aligned with All Citizen Model (often 18–70 on eNPS — confirm live). "
                "PFRDA materials: NRI/OCI generally cannot activate Tier II even with Tier I — verify current FAQ. "
                "No personal income ceiling — leave max_annual_income null; do not set implies_low_income. "
                "Tax clarity: Tier II is NOT a substitute for Tier I section 80CCD benefits for most subscribers."
            ),
            verify_notes=(
                "2026-09-24: PFRDA All Citizen Model pages/FAQs. Confirm live Tier II eligibility for NRI/OCI and tax treatment before advising."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 8 PM E-DRIVE
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-pm-e-drive",
        "PM E-DRIVE — electric two-wheeler demand incentive",
        "पीएम ई-ड्राइव — इलेक्ट्रिक दोपहिया मांग प्रोत्साहन",
        "Ministry of Heavy Industries demand incentive under PM Electric Drive Revolution in Innovative Vehicle Enhancement (PM E-DRIVE) for eligible advanced-battery electric two-wheelers; e-voucher via Aadhaar face authentication at purchase.",
        "भारी उद्योग मंत्रालय की पीएम ई-ड्राइव योजना के तहत पात्र ई-दोपहिया पर मांग प्रोत्साहन; खरीद पर ई-वाउचर।",
        "Upfront reduction in vehicle price via dealer e-voucher for eligible e-2Ws fitted with advanced batteries. Privately or corporately owned registered e-2Ws are eligible (as well as commercial). Exact incentive formula/caps per operational guidelines — verify live portal. No personal income ceiling stated for the retail e-2W path — middle-class and higher-income buyers can benefit while stock/quota lasts.",
        "पात्र उन्नत-बैटरी ई-2W पर डीलर ई-वाउचर से अग्रिम छूट; निजी/कॉर्पोरेट पंजीकृत ई-2W पात्र; व्यक्तिगत आय सीमा नहीं बताई गई।",
        [
            "Aadhaar for face-authenticated e-voucher",
            "Eligible OEM/model with advanced battery as per scheme",
            "Vehicle registration as required",
        ],
        "Generate e-voucher on the PM E-DRIVE portal at time of purchase; incentive deducted by dealer per guidelines.",
        "खरीद के समय पीएम ई-ड्राइव पोर्टल पर ई-वाउचर बनाएँ; डीलर छूट लागू करता है।",
        "https://pmedrive.heavyindustries.gov.in/",
        "https://pmedrive.heavyindustries.gov.in/",
        "Ministry of Heavy Industries",
        ["ev", "subsidy", "electric_vehicle", "universal", "middle-class", "central", "nationwide", "transport"],
        base_rules(
            notes=(
                "Citizen retail path focuses on e-2W: both commercial and privately/corporately owned registered e-2Ws with advanced batteries. "
                "e-3W incentives are for commercial use only — not private passenger cars. e-ambulances/trucks/buses are institutional. "
                "Portal notice (fetched 2026-09-24): terminal date for e-2Ws extended till 31.03.2028 (amendment notification 10.08.2026 referenced on portal). "
                "One beneficiary per category rules per FAQs — confirm live. No personal max_annual_income — leave null; do not set implies_low_income. "
                "Higher-income private e-2W buyers are not excluded by an income gate."
            ),
            verify_notes=(
                "2026-09-24: pmedrive.heavyindustries.gov.in home + operational guidelines. Confirm live e-2W end date, incentive ₹/kWh caps, and e-voucher steps before advising."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 9 Startup India
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-startup-india",
        "Startup India — DPIIT recognition & founder benefits",
        "स्टार्टअप इंडिया — डीपीआईआईटी मान्यता एवं लाभ",
        "DPIIT recognition under the Startup India initiative for eligible private limited companies, LLPs, registered partnerships, or cooperative societies meeting age, turnover, originality, and innovation/scalability criteria — gateway to compliance relief, IPR facilitation, public procurement easing, and possible section 80-IAC tax exemption pathway.",
        "पात्र संस्थाओं के लिए डीपीआईआईटी स्टार्टअप मान्यता — अनुपालन राहत, आईपीआर सुविधा, खरीद सरलीकरण, और संभावित 80-IAC मार्ग।",
        "Recognition benefits may include labour/environment self-certification windows, patent/trademark facilitation support, GeM/procurement relaxations, and—for separately approved eligible Pvt Ltd/LLP incorporated on/after 01-04-2016—section 80-IAC income-tax deduction for 3 consecutive years within first 10 years (subject to Inter-Ministerial Board approval). Founders may be middle- or high-income; entity turnover ceilings apply (commonly ≤₹200 crore any FY for normal recognition; deeptech track differs) — confirm live portal.",
        "मान्यता लाभ: स्व-प्रमाणन, आईपीआर सहायता, खरीद छूट; अलग स्वीकृति पर 80-IAC संभव। संस्था टर्नओवर सीमाएँ — पोर्टल देखें।",
        [
            "Certificate of incorporation / LLP deed / partnership registration",
            "Details proving innovation/scalability and that entity was not formed by splitting/reconstructing an existing business",
            "Financials/ITR as required for recognition or 80-IAC application",
        ],
        "Apply for DPIIT recognition on startupindia.gov.in (or NSWS); optionally apply for section 80-IAC after recognition via the portal form.",
        "startupindia.gov.in पर डीपीआईआईटी मान्यता हेतु आवेदन करें; तत्पश्चात वैकल्पिक 80-IAC।",
        "https://www.startupindia.gov.in/content/sih/en/startup-scheme.html",
        "https://www.startupindia.gov.in/content/sih/en/startup-scheme.html",
        "DPIIT / Startup India",
        ["startup", "tax", "middle-class", "entrepreneur", "dpiit", "central", "nationwide"],
        base_rules(
            occupations=["entrepreneur", "startup_founder"],
            categories=["startup"],
            notes=(
                "Entity-level scheme: existence ≤10 years (≤20 deeptech track per portal), turnover ≤₹200 crore (≤₹300 crore deeptech) in any FY since incorporation, not formed by splitting/reconstructing existing business, innovative/scalable. "
                "No personal founder income ceiling — leave max_annual_income null; do not set implies_low_income. "
                "Notes must reflect that higher-income founders of eligible startups can benefit. 80-IAC is a separate approval, not automatic with recognition."
            ),
            verify_notes=(
                "2026-09-24: startupindia.gov.in Startup Scheme / recognition page. Confirm live turnover/age tracks and 80-IAC conditions before advising."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 10 PM-USP CSSS
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-pm-usp-csss",
        "PM-USP Central Sector Scheme of Scholarship for College and University Students",
        "पीएम-यूएसपी केंद्रीय क्षेत्र छात्रवृत्ति (कॉलेज/विश्वविद्यालय)",
        "Merit-cum-means scholarship under Pradhan Mantri Uchchatar Shiksha Protsahan (PM-USP) for Class XII board pass-outs above the 80th percentile in their stream who pursue regular degree courses, with gross parental/family income up to ₹4.5 lakh per annum.",
        "कक्षा 12 में संबंधित स्ट्रीम में 80वें प्रतिशतक से ऊपर; नियमित डिग्री; पारिवारिक आय अधिकतम ₹4.5 लाख।",
        "₹12,000 per annum for first three years of graduation-level study; ₹20,000 per annum at postgraduate level (professional/integrated rules per guidelines — e.g. B.Tech up to graduation year 4 amounts as specified). DBT to student bank account. About 82,000 fresh scholarships per year; 50% for girls. Not a BPL-only scheme — covers lower-middle / middle-income families up to ₹4.5 lakh.",
        "स्नातक प्रथम तीन वर्ष ₹12,000/वर्ष; स्नातकोत्तर ₹20,000/वर्ष (दिशानिर्देशानुसार)।",
        [
            "Class XII marksheet / board percentile evidence",
            "Family income certificate (fresh applicants; ≤ ₹4.5 lakh)",
            "Admission proof in eligible regular course / AISHE-coded institution",
            "Aadhaar / bank account for DBT; NSP application",
        ],
        "Apply on National Scholarships Portal (scholarships.gov.in) within NSP timelines; institute and state verification required.",
        "राष्ट्रीय छात्रवृत्ति पोर्टल (scholarships.gov.in) पर आवेदन करें।",
        "https://scholarships.gov.in/",
        "https://scholarships.gov.in/public/schemeGuidelines/CSSS_GUIDLINES_07022024_updated.pdf",
        "Department of Higher Education / National Scholarship Portal",
        ["scholarship", "education", "middle-class", "pm-usp", "central", "nationwide", "nsp"],
        base_rules(
            max_annual_income=450000,
            implies_low_income=True,
            categories=["student", "merit"],
            notes=(
                "Above 80th percentile of successful candidates in relevant Class XII stream; regular degree (not correspondence/distance/diploma); AICTE/regulatory-recognised institution; "
                "not already availing another specified merit/state fee-waiver scheme; gross parental/family income ≤ ₹4.5 lakh (income certificate for fresh). "
                "Renewal: ≥50% marks and ≥75% attendance typical gates. max_annual_income encodes the ₹4.5 lakh family-income ceiling."
            ),
            verify_notes=(
                "2026-09-24: PM-USP CSSS guidelines PDF on scholarships.gov.in (AY 2022-23 onwards rates). Confirm NSP open/close dates each year."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 11 NMMS
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-nmms",
        "National Means-cum-Merit Scholarship Scheme (NMMSS)",
        "राष्ट्रीय मीन्स-कम-मेरिट छात्रवृत्ति योजना (एनएमएमएसएस)",
        "Central sector scholarship to reduce dropout after Class VIII for meritorious students from economically weaker families, with parental income not more than ₹3.5 lakh per annum, studying in government / government-aided / local-body schools.",
        "कक्षा 8 के बाद ड्रॉपआउट रोकने हेतु मेधावी विद्यार्थियों के लिए; पैतृक आय अधिकतम ₹3.5 लाख; सरकारी/सहायता प्राप्त/स्थानीय निकाय विद्यालय।",
        "₹12,000 per annum (₹1,000/month) for Classes IX–XII (maximum four years) via DBT after State selection test (MAT+SAT) and NSP processing. 1,00,000 fresh scholarships per year with State/UT quotas. Covers families above extreme poverty up to ₹3.5 lakh — middle/lower-middle band, not BPL-only.",
        "कक्षा 9–12 के लिए ₹12,000 प्रति वर्ष; राज्य चयन परीक्षा + एनएसपी।",
        [
            "Parental income proof ≤ ₹3.5 lakh",
            "Class VII/VIII mark criteria for appearing/selection as per guidelines",
            "Enrolment in eligible government/aided/local-body school (not KV/JNV/central-state residential with full boarding, not private schools)",
            "Bank account; NSP application after selection",
        ],
        "Appear in State/UT NMMSS selection test at Class VIII stage; then apply/renew on scholarships.gov.in (NSP) as directed.",
        "राज्य/केंद्रशासित प्रदेश की एनएमएमएसएस परीक्षा दें; फिर एनएसपी पर आवेदन/नवीकरण।",
        "https://scholarships.gov.in/",
        "https://scholarships.gov.in/public/schemeGuidelines/NMMSSGuidelines.pdf",
        "Department of School Education & Literacy / National Scholarship Portal",
        ["scholarship", "education", "middle-class", "nmms", "central", "nationwide", "nsp"],
        base_rules(
            max_annual_income=350000,
            implies_low_income=True,
            categories=["student", "merit"],
            notes=(
                "Parental income ≤ ₹3.5 lakh from all sources at selection. Regular student entering Class IX in Government, Government-aided, or local-body school. "
                "Not entitled: Kendriya Vidyalayas, Jawahar Navodaya Vidyalayas, residential schools with boarding/lodging provided, private schools. "
                "Selection via State MAT+SAT; pass aggregates and Class VIII marks per guidelines (relaxations for SC/ST). "
                "max_annual_income encodes ₹3.5 lakh parental ceiling. NSP timelines referenced into AY 2026-27 in PIB/NSP notices — confirm live each year."
            ),
            verify_notes=(
                "2026-09-24: NMMSS revised guidelines PDF on scholarships.gov.in; PIB/NSP activity into 2026-27. Confirm continuation circulars and State exam schedule."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 12 PM-USP CSIS
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-pm-usp-csis",
        "PM-USP Central Sector Interest Subsidy (CSIS) on education loans",
        "पीएम-यूएसपी शिक्षा ऋण ब्याज सब्सिडी (सीएसआईएस)",
        "Interest subsidy during the moratorium period on eligible education loans for students from families with income up to ₹4.5 lakh per annum, under the PM-USP CSIS component administered with banks (portal: PM Vidyalaxmi / MoE pages).",
        "पारिवारिक आय अधिकतम ₹4.5 लाख वाले पात्र शिक्षा ऋणों पर अधिस्थगन अवधि में ब्याज सब्सिडी।",
        "Full simple interest subsidy during moratorium (course period + one year, per MoE scheme framing) on eligible IBA-model education loans for approved professional/technical courses in India, commonly up to the loan limit stated in current guidelines (often cited up to ₹10 lakh — confirm live MoE/bank page). Benefit generally once. Supports non-poor middle-income students below the ₹4.5 lakh family-income gate.",
        "अधिस्थगन में साधारण ब्याज सब्सिडी; पात्र व्यावसायिक/तकनीकी पाठ्यक्रम; आय ≤₹4.5 लाख — बैंक/एमओई से पुष्टि करें।",
        [
            "Family income certificate ≤ ₹4.5 lakh",
            "Sanctioned education loan from eligible bank under IBA model scheme",
            "Admission/course documents for approved professional/technical programme in India",
            "Aadhaar / bank details; claim via bank / PM Vidyalaxmi as directed",
        ],
        "Take an eligible education loan; subsidy is claimed/processed through the lending bank and MoE/PM Vidyalaxmi channels (pmvidyalaxmi.co.in).",
        "पात्र शिक्षा ऋण लें; बैंक और पीएम विद्यालक्ष्मी / शिक्षा मंत्रालय प्रक्रिया से सब्सिडी।",
        "https://pmvidyalaxmi.co.in/",
        "https://www.education.gov.in/central-scheme-provide-interest-subsidy-csis-educational-loans",
        "Department of Higher Education / member banks",
        ["education", "loan", "interest_subsidy", "middle-class", "pm-usp", "csis", "central", "nationwide"],
        base_rules(
            max_annual_income=450000,
            implies_low_income=True,
            categories=["student"],
            occupations=["student"],
            notes=(
                "Family income up to ₹4.5 lakh per annum (MoE CSIS framing). Eligible professional/technical courses and IBA model education loan from participating bank. "
                "Subsidy during moratorium; typically available only once. max_annual_income encodes the ₹4.5 lakh ceiling. "
                "Not limited to BPL — covers middle-income households under the cap. Exact loan ceiling and course list — verify live MoE guidelines / bank circulars (do not invent)."
            ),
            verify_notes=(
                "2026-09-24: education.gov.in CSIS page + pmvidyalaxmi.co.in. Confirm current loan ceiling, course eligibility, and claim workflow with lending bank."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 13 PM-KMY
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-pm-kmy",
        "Pradhan Mantri Kisan Maandhan Yojana (PM-KMY)",
        "प्रधानमंत्री किसान मानधन योजना (पीएम-केएमवाई)",
        "Voluntary contributory old-age pension for landholding small and marginal farmers (cultivable land up to 2 hectares) aged 18–40, administered with LIC, providing assured monthly pension on attaining age 60 subject to exclusions.",
        "2 हेक्टेयर तक भूमि वाले लघु/सीमांत किसान (प्रवेश आयु 18–40) के लिए अंशदायी पेंशन; 60 वर्ष पर सुनिश्चित मासिक पेंशन।",
        "Assured ₹3,000 per month pension at age 60; equal matching contribution by Central Government; monthly subscriber contribution ₹55–₹200 by entry age. Family pension 50% to spouse after vesting as per guidelines. Option to auto-debit from PM-KISAN benefit.",
        "60 वर्ष पर ₹3,000/माह; केंद्र का समतुल्य योगदान; प्रवेश आयु अनुसार ₹55–₹200/माह।",
        [
            "Aadhaar",
            "Bank passbook / account details (PM-KISAN account if using that mandate)",
            "Landholding evidence as small/marginal farmer (≤2 ha) per State land records",
            "Enrolment-cum-auto-debit mandate at CSC / SNO",
        ],
        "Enrol at Common Service Centre (CSC) or via State Nodal Officer / designated online links with Aadhaar and bank details.",
        "सीएससी या राज्य नोडल अधिकारी / निर्दिष्ट ऑनलाइन लिंक से नामांकन।",
        "https://www.myscheme.gov.in/schemes/pmkmy",
        "https://www.pmkisan.gov.in/Documents/PM-KMY%20-%20Operational%20Guidelines.pdf",
        "Department of Agriculture & Farmers Welfare / LIC / CSC",
        ["pension", "farmer", "pm-kmy", "maandhan", "central", "nationwide", "agriculture"],
        base_rules(
            min_age=18,
            max_age=40,
            occupations=["farmer", "small_marginal_farmer"],
            land_ownership="cultivable_landholding_upto_2_ha",
            categories=["smf"],
            notes=(
                "Small/Marginal Farmer owning cultivable land up to 2 hectare as per State/UT land records; entry age 18–40. "
                "Exclusions include: covered under NPS/ESIC/EPFO etc.; opted PM-SYM or PM-LVM; institutional landholders; constitutional post holders; ministers/MPs/MLAs etc.; "
                "serving/retired govt/PSE/local-body officers (excl. MTS/Class IV/Group D); persons who paid income tax in last assessment year; "
                "registered professionals (doctors, engineers, lawyers, CAs, architects) in practice. "
                "Not a high-income scheme — income-tax payers excluded. Leave max_annual_income null (no rupee ceiling stated beyond exclusions); do not set implies_low_income true solely from farmer status — exclusions already bar IT payers."
            ),
            verify_notes=(
                "2026-09-24: PM-KMY Operational Guidelines PDF on pmkisan.gov.in; myscheme.gov.in/schemes/pmkmy. Confirm live enrolment portal URL (maandhan.in intermittent from box)."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 14 PM-SYM
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-pm-sym",
        "Pradhan Mantri Shram Yogi Maandhan (PM-SYM)",
        "प्रधानमंत्री श्रम योगी मानधन (पीएम-एसवाईएम)",
        "Voluntary contributory pension for unorganised workers aged 18–40 with monthly income ≤ ₹15,000 who are not income-tax payers and not covered under NPS, ESIC, or EPFO.",
        "असंगठित कर्मकारों (मासिक आय ≤₹15,000; आयु 18–40) के लिए अंशदायी पेंशन; आयकरदाता/एनपीएस/ईएसआईसी/ईपीएफओ नहीं।",
        "Minimum assured pension ₹3,000 per month after age 60; 50:50 matching contribution by Central Government; subscriber monthly contribution ₹55–₹200 by entry age. Family pension 50% to spouse during receipt as per scheme.",
        "60 वर्ष के बाद ₹3,000/माह सुनिश्चित पेंशन; केंद्र का 50:50 योगदान।",
        [
            "Aadhaar",
            "Savings / Jan Dhan bank account",
            "Mobile phone",
            "Self-certification of unorganised-worker eligibility at CSC",
        ],
        "Enrol at nearest CSC with Aadhaar and bank account (self-certification); facilitation via LIC/ESIC/EPFO/Labour offices directing to CSC.",
        "आधार और बैंक खाते के साथ निकटतम सीएससी पर नामांकन।",
        "https://www.labour.gov.in/offerings/schemes-and-services/details/pm-sym-QTOzATMtQWa",
        "https://www.labour.gov.in/offerings/schemes-and-services/details/pm-sym-QTOzATMtQWa",
        "Ministry of Labour & Employment / LIC / CSC",
        ["pension", "unorganised_worker", "pm-sym", "maandhan", "central", "nationwide", "labour"],
        base_rules(
            min_age=18,
            max_age=40,
            max_monthly_household_income=15000,
            occupations=["unorganised_worker", "self_employed"],
            categories=["unorganised_worker"],
            notes=(
                "Unorganised workers (home-based, street vendors, construction, agri workers, etc.) with monthly income ₹15,000 or less; entry age 18–40. "
                "Must not be covered under NPS, ESIC, or EPFO; must not be an income-tax payer. "
                "max_monthly_household_income encodes the ₹15,000 monthly income gate (scheme text: monthly income). "
                "Not for wealthy / IT-paying professionals."
            ),
            verify_notes=(
                "2026-09-24: labour.gov.in PM-SYM page (contribution chart and exclusions). Confirm live CSC enrolment and any portal URL changes."
            ),
        ),
    )
)

# ---------------------------------------------------------------------------
# 15 NAMASTE
# ---------------------------------------------------------------------------
NEW.append(
    india_scheme(
        "in-namaste",
        "NAMASTE — National Action for Mechanised Sanitation Ecosystem",
        "नमस्ते — यांत्रिक स्वच्छता पारिस्थितिकी तंत्र हेतु राष्ट्रीय कार्रवाई",
        "Joint MoSJE–MoHUA programme for sewer and septic tank workers (SSWs) and related sanitation workers (waste pickers included per revised guidelines), delivering profiling, occupational safety, health cover, skilling, and livelihood/PPE support via Urban Local Bodies — not a general middle-class cash scheme.",
        "सीवर/सेप्टिक टैंक कर्मियों हेतु प्रोफाइलिंग, सुरक्षा, स्वास्थ्य कवर, कौशल और आजीविका सहायता — सामान्य मध्यमवर्गीय योजना नहीं।",
        "Intended outcomes include zero fatalities in sanitation work, formalisation and skilling, PPE and safety training, Ayushman Bharat-PMJAY health coverage pathway for identified workers, SHG/entrepreneurship and alternate livelihood support, and capital subsidy / concessional loans for mechanisation as per guidelines. Access is typically through ULB identification/profiling camps rather than open self-registration alone.",
        "पहचाने गए कर्मियों के लिए सुरक्षा प्रशिक्षण, पीपीई, स्वास्थ्य कवर, आजीविका/मशीनीकरण सहायता — यूएलबी प्रोफाइलिंग।",
        [
            "Identification as SSW / eligible sanitation worker via ULB profiling",
            "Aadhaar and bank details as required by ULB / NAMASTE BMS",
            "Documents sought in profiling camp / guidelines",
        ],
        "Contact Urban Local Body / State NAMASTE nodal officer for profiling; see MoSJE scheme page and NAMASTE BMS portal.",
        "शहरी स्थानीय निकाय / राज्य नमास्ते नोडल से प्रोफाइलिंग हेतु संपर्क करें।",
        "https://bmsnamaste.dosje.gov.in/home",
        "https://socialjustice.gov.in/schemes/37",
        "Department of Social Justice & Empowerment / MoHUA / ULBs",
        ["sanitation", "livelihood", "namaste", "occupational_safety", "central", "nationwide", "urban"],
        base_rules(
            occupations=["sanitation_worker", "sewer_septic_worker", "waste_picker"],
            categories=["sanitation_worker"],
            notes=(
                "Citizen path exists via ULB profiling of sewer/septic tank workers (and waste pickers per revised guidelines) — independent, ULB/parastatal, or private-organisation workers as defined. "
                "Not an open universal middle-class benefit and not for high-income general public. Leave max_annual_income null (no general income ceiling published as a simple rupee gate); do not mis-tag as middle-class/wealthy. "
                "verify=true for exact benefit packages which vary by component/guidelines edition."
            ),
            verify_notes=(
                "2026-09-24: socialjustice.gov.in/schemes/37 + bmsnamaste.dosje.gov.in. Confirm live profiling process and waste-picker inclusion details in latest guidelines."
            ),
        ),
    )
)


def patch_existing(schemes: list[dict]) -> list[str]:
    """Light tag/note updates on existing India rows."""
    touched: list[str] = []
    by_id = {s["id"]: s for s in schemes}

    nps = by_id.get("in-nps-all-citizen")
    if nps:
        tags = list(nps.get("tags") or [])
        for t in ("tax", "middle-class", "universal"):
            if t not in tags:
                tags.append(t)
        nps["tags"] = tags
        er = nps.setdefault("eligibility_rules", {})
        notes = er.get("notes") or ""
        extra = (
            " Tax: Tier I contributions may attract deductions under sections 80CCD(1)/80CCD(1B) when claimed under a tax regime that allows them "
            "(confirm live IT/PFRDA rules). Tier II is a separate voluntary account without the same general tax deduction — see catalogue id in-nps-tier-ii. "
            "No income ceiling — middle-class and higher-income citizens may join All Citizen Model."
        )
        if "80CCD" not in notes:
            er["notes"] = (notes + extra).strip()
        er["verify_notes"] = (
            (er.get("verify_notes") or "")
            + " 2026-09-24 all-band: tax regime / Tier II clarity cross-check."
        ).strip()
        nps["last_verified"] = LAST
        touched.append("in-nps-all-citizen")

    suk = by_id.get("in-sukanya-samriddhi")
    if suk:
        tags = list(suk.get("tags") or [])
        for t in ("tax", "middle-class"):
            if t not in tags:
                tags.append(t)
        suk["tags"] = tags
        er = suk.setdefault("eligibility_rules", {})
        notes = er.get("notes") or ""
        if "80C" not in notes and "higher-income" not in notes:
            er["notes"] = (
                notes
                + " Deposits commonly qualify under section 80C under applicable tax regime. No personal income ceiling — middle-class and higher-income families with an eligible girl child may open (subject to two-girl rule)."
            ).strip()
        suk["last_verified"] = LAST
        touched.append("in-sukanya-samriddhi")

    pmay = by_id.get("in-pmay-u-2")
    if pmay:
        er = pmay.setdefault("eligibility_rules", {})
        notes = er.get("notes") or ""
        if "MIG" in notes and "middle-class" not in (pmay.get("tags") or []):
            tags = list(pmay.get("tags") or [])
            tags.append("middle-class")
            pmay["tags"] = tags
        if "do not duplicate CLSS" not in notes:
            er["notes"] = (
                notes
                + " MIG (₹6–9 lakh household income FAQ band) is included in this single PMAY-U 2.0 row via ISS/other verticals — do not add a separate historical CLSS duplicate."
            ).strip()
        pmay["last_verified"] = LAST
        touched.append("in-pmay-u-2")

    return touched


def main() -> None:
    assert [s["id"] for s in NEW] == EXPECTED_IDS, (
        f"NEW order/ids mismatch:\n expected={EXPECTED_IDS}\n got={[s['id'] for s in NEW]}"
    )
    assert len(NEW) == 15

    schemes: list[dict] = json.loads(DATA.read_text())
    before = len(schemes)
    existing = {s["id"] for s in schemes}

    clash = [i for i in EXPECTED_IDS if i in existing]
    if clash:
        print(f"ERROR: IDs already present (refusing overwrite): {clash}", file=sys.stderr)
        sys.exit(1)

    # Encoding sanity: no-income-ceiling rows must not set implies_low_income true
    for s in NEW:
        er = s["eligibility_rules"]
        if er.get("max_annual_income") is None and er.get("implies_low_income") is True:
            # allow only if explicitly monthly-gated poverty schemes? PM-SYM has monthly not annual —
            # user rule: NO income ceiling → do not set ili true. PM-SYM has monthly ceiling encoded separately.
            if s["id"] not in {"in-pm-sym"}:  # still should not set ili true
                print(f"ERROR encoding: {s['id']} has ili true with null max_annual_income", file=sys.stderr)
                sys.exit(1)
        if er.get("implies_low_income") is True and er.get("max_annual_income") is None:
            if s["id"] in {
                "in-ppf",
                "in-nsc",
                "in-scss",
                "in-section-80c-deductions",
                "in-section-24b-home-loan-interest",
                "in-section-80eea",
                "in-nps-tier-ii",
                "in-pm-e-drive",
                "in-startup-india",
            }:
                print(f"ERROR: middle/high row {s['id']} must not set implies_low_income true", file=sys.stderr)
                sys.exit(1)

    touched = patch_existing(schemes)

    for s in NEW:
        schemes.append(s)

    ids = [s["id"] for s in schemes]
    assert len(ids) == len(set(ids)), "Duplicate ids after append"

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    after = len(schemes)
    assert after == before + 15

    scope_addendum = (
        " Catalogue refresh 2026-09-24 India all-band: middle/high/universal deepen — PPF, NSC, SCSS, "
        "Section 80C umbrella, Section 24(b) home-loan interest, Section 80EEA, NPS Tier II clarity, "
        "PM E-DRIVE e-2W, Startup India DPIIT, PM-USP CSSS, NMMS, PM-USP CSIS; freshness PM-KMY, PM-SYM, NAMASTE; "
        "light tag/note updates on NPS Tier I, Sukanya, PMAY-U 2.0 MIG. Official .gov.in / IT / NSI-Post / PFRDA / MoE / MoLE / MoSJE / MHI only; "
        "last_verified 2026-09-24; no invented eligibility; no-income-ceiling rows leave max_annual_income null without implies_low_income true."
    )

    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = after
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = ISO
        scope = meta.get("scope", "")
        if "Catalogue refresh 2026-09-24 India all-band" not in scope:
            meta["scope"] = scope.rstrip() + scope_addendum
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    assert DATA.read_text() == FE_DATA.read_text()
    assert META.read_text() == FE_META.read_text()
    assert json.loads(META.read_text())["scheme_count"] == after
    assert json.loads(META.read_text())["updated_as_of"] == LAST

    present = {s["id"] for s in json.loads(DATA.read_text())}
    for i in EXPECTED_IDS:
        assert i in present, f"missing after write: {i}"

    print(f"BEFORE: {before}")
    print(f"AFTER:  {after}")
    print(f"DELTA:  {after - before}")
    print("ADDED:", EXPECTED_IDS)
    print("PATCHED:", touched)
    print(
        "SKIPPED: APY/PMJJBY/PMSBY/NPS-T1/Sukanya/Surya/PMAY-U2 duplicate, LTC employer-only, "
        "PLI industry, FAME-as-primary (use PM E-DRIVE), CLSS duplicate, patent niche, Ayushman-as-wealthy"
    )


if __name__ == "__main__":
    main()
