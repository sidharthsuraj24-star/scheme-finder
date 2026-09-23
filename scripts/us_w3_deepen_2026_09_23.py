#!/usr/bin/env python3
"""US Wave W3 deepen (2026-09-23): remaining states + nationwide core gap-fills.

Region (W3 remaining): CT, DE, RI, VT, NH, ME, WV, MS, AR, IA, KS, NE, ND, SD, MT, WY, ID.
Also fill missing cores for EVERY state (SNAP/Medicaid/TANF/LIHEAP/CHIP kids health).
Rules: .gov only; no invented eligibility ceilings; last_verified 2026-09-23.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
LAST = "2026-09-23"


def L(en: str, hi: str | None = None, ml: str | None = None) -> dict:
    return {"en": en, "ml": ml or en, "hi": hi or en}


def docs(items: list[str]) -> dict:
    return {"en": items, "ml": items, "hi": items}


def rules(
    state: str,
    *,
    notes: str,
    verify_notes: str,
    implies_low_income: bool = True,
    min_age: int | None = None,
    max_age: int | None = None,
    max_annual_income: int | None = None,
    disability_required: bool = False,
    categories: list | None = None,
    gender: str | None = None,
) -> dict:
    return {
        "min_age": min_age,
        "max_age": max_age,
        "max_annual_income": max_annual_income,
        "max_monthly_household_income": None,
        "occupations": [],
        "categories": categories or [],
        "gender": gender,
        "marital_status": [],
        "disability_required": disability_required,
        "min_disability_percent": None,
        "land_ownership": None,
        "states": [state],
        "countries": ["United States"],
        "nationwide": False,
        "notes": notes,
        "verify": True,
        "verify_notes": verify_notes,
        "implies_low_income": implies_low_income,
    }


def scheme(
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

# ---------------------------------------------------------------------------
# NATIONWIDE CORE GAP-FILLS (true missing cores)
# ---------------------------------------------------------------------------

NEW.append(
    scheme(
        "fl-liheap",
        "LIHEAP (Low-Income Home Energy Assistance) – FloridaCommerce",
        "LIHEAP – फ्लोरिडा",
        "FloridaCommerce administers LIHEAP through a network of local community action agencies. The program helps income-qualified Florida residents with home heating and cooling costs; payments go to the utility on the household’s behalf.",
        "Help paying eligible home heating and/or cooling bills for qualifying Florida households (amounts and availability vary by county and funding).",
        [
            "Most recent home energy bill",
            "Proof of income for household members",
            "Photo ID of applicant",
            "Social Security numbers for household members",
            "Proof of U.S. citizenship or permanent residence",
            "Florida residency",
        ],
        "Contact your local LIHEAP / community action agency listed via FloridaCommerce, or use the Florida LIHEAP application path linked from floridajobs.org. Benefits and crisis help vary by local agency funding.",
        "https://liheapch.acf.gov/profiles/Florida.htm",
        "https://liheapch.acf.gov/profiles/Florida.htm",
        "Florida Department of Commerce (FloridaCommerce) / local Community Action Agencies",
        ["united_states", "florida", "liheap", "energy", "utility", "heat", "cooling"],
        rules(
            "Florida",
            notes="FL LIHEAP (FloridaCommerce): income generally at or below 60% Florida SMI or 150% FPL (charts published on floridajobs.org); responsible for heating/cooling bills; Florida resident; U.S. citizen/qualified alien/permanent resident. No single annual ceiling encoded — household-size charts and local agency rules apply.",
            verify_notes="Income charts, benefit ranges, and local agency application windows change — verify=true via floridajobs.org LIHEAP.",
        ),
    )
)

NEW.append(
    scheme(
        "ak-denali-kidcare",
        "Denali KidCare (CHIP / children’s Medicaid) – Alaska",
        "Denali KidCare – अलास्का",
        "Denali KidCare is Alaska’s CHIP/children’s Medicaid coverage for eligible children from birth through age 18 and eligible pregnant people who meet income and other program rules. Administered by the Alaska Department of Health.",
        "Free or low-cost health coverage for eligible Alaska children and pregnant people under Denali KidCare / Medicaid CHIP pathways.",
        [
            "Identity and Alaska residency",
            "Income documentation",
            "Child / pregnancy information",
            "Citizenship or immigration documentation as required",
        ],
        "Apply through Alaska Medicaid / Denali KidCare pathways on health.alaska.gov (Alaska Connect or Healthcare.gov as directed on the official page).",
        "https://health.alaska.gov/en/services/denali-kidcare/",
        "https://health.alaska.gov/en/services/denali-kidcare/",
        "Alaska Department of Health / Denali KidCare",
        ["united_states", "alaska", "chip", "kids", "children", "medicaid", "denali_kidcare", "health"],
        rules(
            "Alaska",
            notes="Denali KidCare: Alaska children (birth–18) and eligible pregnant people; income and citizenship/immigration rules; CHIP/Medicaid pathways. No single annual ceiling encoded.",
            verify_notes="Income % FPL and pregnancy/child rules — verify=true via health.alaska.gov Denali KidCare.",
            max_age=18,
        ),
    )
)

NEW.append(
    scheme(
        "hi-chip-children",
        "Med-QUEST Children’s Coverage (Medicaid / CHIP) – Hawaii",
        "Med-QUEST बच्चों का कवरेज – हवाई",
        "Hawaii Med-QUEST covers eligible children under age 19 through Medicaid and CHIP pathways. Apply via Med-QUEST / myBenefits Hawaii for free or low-cost children’s health coverage.",
        "Medicaid/CHIP health coverage for eligible Hawaii children under 19.",
        [
            "Identity and Hawaii residency",
            "Income documentation",
            "Child information / birth records as required",
        ],
        "Apply online through Med-QUEST myBenefits Hawaii or use the DHS health coverage application linked from medquest.hawaii.gov.",
        "https://medquest.hawaii.gov/en/members-applicants/get-started/how-to-apply.html",
        "https://medquest.hawaii.gov/content/medquest/en/about/what-is-medicaid.html",
        "Hawaii Department of Human Services / Med-QUEST Division",
        ["united_states", "hawaii", "chip", "kids", "children", "medicaid", "medquest", "health"],
        rules(
            "Hawaii",
            notes="Med-QUEST children’s Medicaid/CHIP: Hawaii children under 19; household income and other Med-QUEST rules. No single annual ceiling encoded.",
            verify_notes="Age, income, and immigration pathways — verify=true via medquest.hawaii.gov.",
            max_age=18,
        ),
    )
)

NEW.append(
    scheme(
        "nm-chip",
        "New Mexico CHIP (Children’s Health Insurance) – HCA",
        "न्यू मेक्सिको CHIP – बच्चों का स्वास्थ्य",
        "New Mexico CHIP provides Medicaid-comparable health coverage for eligible uninsured children under 19 whose household income is above Medicaid limits but within CHIP category limits. Administered by the Health Care Authority.",
        "Children’s health insurance (CHIP categories) for eligible New Mexico children under 19.",
        [
            "Identity and New Mexico residency",
            "Income documentation",
            "Child information",
            "Proof child is uninsured (CHIP rules)",
        ],
        "Apply for Medicaid/CHIP through YES.NM.gov / HCA assistance application (HCA-100) as directed on hca.nm.gov.",
        "https://www.hca.nm.gov/",
        "https://www.hca.nm.gov/",
        "New Mexico Health Care Authority / Medical Assistance Division",
        ["united_states", "new_mexico", "chip", "kids", "children", "medicaid", "health", "hca"],
        rules(
            "New Mexico",
            notes="NM CHIP (categories for children under 19 above Medicaid income bands, within published FPL ranges; no resource test; generally no other insurance). Exact % FPL bands change — not encoded as a single ceiling.",
            verify_notes="CHIP vs Medicaid category income bands and insurance rules — verify=true via hca.nm.gov / YES NM.",
            max_age=18,
        ),
    )
)

NEW.append(
    scheme(
        "ok-chip",
        "SoonerCare Children / CHIP – Oklahoma Health Care Authority",
        "SoonerCare बच्चों / CHIP – ओक्लाहोमा",
        "Oklahoma SoonerCare covers eligible children through Medicaid and CHIP pathways administered by the Oklahoma Health Care Authority. Children’s SoonerCare provides comprehensive health coverage for qualifying Oklahoma kids.",
        "Medicaid/CHIP health coverage for eligible Oklahoma children via SoonerCare.",
        [
            "Identity and Oklahoma residency",
            "Income documentation",
            "Child information",
        ],
        "Apply online via MySoonerCare / OKDHSLive pathways linked from oklahoma.gov OHCA, or follow Children’s Health Insurance Program updates on ohca pages.",
        "https://oklahoma.gov/ohca/individuals/mysoonercare.html",
        "https://oklahoma.gov/ohca/about/about-us/children-s-health-insurance-program--chip--updates.html",
        "Oklahoma Health Care Authority (OHCA)",
        ["united_states", "oklahoma", "chip", "kids", "children", "medicaid", "soonercare", "health"],
        rules(
            "Oklahoma",
            notes="SoonerCare children/CHIP: Oklahoma children meeting age, income, and residency rules under OHCA. No single annual ceiling encoded.",
            verify_notes="Income charts and CHIP updates — verify=true via oklahoma.gov/ohca.",
            max_age=18,
        ),
    )
)

NEW.append(
    scheme(
        "wa-apple-health-kids",
        "Apple Health for Kids (CHIP / children’s Medicaid) – Washington HCA",
        "Apple Health for Kids – वाशिंगटन",
        "Washington Apple Health for Kids provides free or low-cost health coverage for eligible children under 19. Coverage is free at lower income levels; premium tiers may apply at higher CHIP income bands.",
        "Free or low-cost Apple Health coverage for eligible Washington children under 19.",
        [
            "Identity and Washington residency",
            "Income documentation",
            "Child information",
        ],
        "Apply or renew through Washington Healthplanfinder / HCA Apple Health pathways linked from hca.wa.gov children’s health pages.",
        "https://www.hca.wa.gov/free-or-low-cost-health-care/i-help-others-apply-and-access-apple-health/health-care-children",
        "https://www.hca.wa.gov/free-or-low-cost-health-care/i-help-others-apply-and-access-apple-health/health-care-children",
        "Washington Health Care Authority (HCA)",
        ["united_states", "washington", "chip", "kids", "children", "medicaid", "apple_health", "health"],
        rules(
            "Washington",
            notes="Apple Health for Kids: children under 19; free coverage generally at or below published FPL (HCA cites ~215% FPL free; premiums up to higher CHIP band ~317% FPL). No single annual ceiling encoded.",
            verify_notes="FPL bands and premium tiers — verify=true via hca.wa.gov Apple Health for Kids.",
            max_age=18,
        ),
    )
)

# ---------------------------------------------------------------------------
# W3 STATE DEEPEN — cores clarifying CHIP + 1–2 distinctive each
# ---------------------------------------------------------------------------

# Connecticut
NEW.append(
    scheme(
        "ct-eitc",
        "Connecticut Earned Income Tax Credit (CT EITC) – DRS",
        "CT EITC – कनेक्टिकट",
        "Refundable Connecticut state earned income tax credit for full-year CT residents who qualify for the federal EITC. For recent tax years the state credit is 40% of the allowed federal EITC, plus an additional $250 if the filer has at least one qualifying child.",
        "Refundable state tax credit (percentage of federal EITC; plus $250 with qualifying child under current law) claimed on Form CT-1040 with Schedule CT-EITC.",
        [
            "Federal return claiming federal EITC",
            "Form CT-1040 / Schedule CT-EITC",
            "Valid SSN for filer, spouse, and qualifying children",
            "Full-year Connecticut residency documentation as needed",
        ],
        "File Form CT-1040 with Schedule CT-EITC through myConneCT / DRS. See portal.ct.gov DRS CT EITC information page.",
        "https://portal.ct.gov/drs/ct---eitc/ct-eitc-information/ct-earned-income-tax-credit/",
        "https://portal.ct.gov/drs/ct---eitc/ct-eitc-information/ct-earned-income-tax-credit/",
        "Connecticut Department of Revenue Services (DRS)",
        ["united_states", "connecticut", "eitc", "tax_credit", "refundable", "drs"],
        rules(
            "Connecticut",
            notes="CT EITC: must qualify for federal EITC; full-year CT resident; valid SSNs; investment income within published limit; state credit = 40% of federal EITC for TY commencing on/after 2023, plus $250 with ≥1 qualifying child (current statute). AGI/earned-income federal limits apply — not encoded as one ceiling.",
            verify_notes="Federal EITC limits, investment-income cap, and CT rate/% — verify=true via portal.ct.gov/DRS CT EITC.",
            implies_low_income=True,
        ),
    )
)
NEW.append(
    scheme(
        "ct-rap",
        "Connecticut Rental Assistance Program (RAP) – DOH",
        "CT RAP किराया सहायता – कनेक्टिकट",
        "Connecticut’s state-funded Rental Assistance Program (RAP) helps eligible low-income households afford rent through the Department of Housing. Waiting lists open and close periodically.",
        "Monthly rental assistance subsidy for eligible Connecticut households when the waiting list is open and a voucher is issued.",
        [
            "Identity and Connecticut residency",
            "Income documentation",
            "Housing / landlord information when selected",
        ],
        "Monitor portal.ct.gov/DOH Rental Assistance Program for waiting-list status and application instructions (list may be closed).",
        "https://portal.ct.gov/doh/doh/programs/rental-assistance-program",
        "https://portal.ct.gov/doh/doh/programs/rental-assistance-program",
        "Connecticut Department of Housing (DOH)",
        ["united_states", "connecticut", "housing", "rental_assistance", "rap", "doh"],
        rules(
            "Connecticut",
            notes="CT RAP: low-income CT households; waiting list frequently closed; income and household rules apply when applications are accepted. No single annual ceiling encoded.",
            verify_notes="Waiting-list status and income limits — verify=true via portal.ct.gov/DOH RAP.",
        ),
    )
)

# Delaware
NEW.append(
    scheme(
        "de-eitc",
        "Delaware Earned Income Tax Credit (EITC) – Division of Revenue",
        "Delaware EITC – डेलावेयर",
        "Delaware allows taxpayers who qualify for the federal EITC to claim a state EITC: either a refundable credit equal to a published percentage of the federal credit or a larger nonrefundable percentage, per Division of Revenue schedules.",
        "State EITC reducing Delaware income tax (refundable or nonrefundable option per current PIT schedules).",
        [
            "Federal return with federal EITC",
            "Delaware PIT-RES / PIT-RSS schedules",
            "SSN / residency documentation as required",
        ],
        "Claim on Delaware personal income tax return schedules (PIT-RSS) available from revenue.delaware.gov; follow current-year instructions.",
        "https://revenue.delaware.gov/personal-income-tax-forms/",
        "https://revenue.delaware.gov/personal-income-tax-forms/",
        "Delaware Division of Revenue",
        ["united_states", "delaware", "eitc", "tax_credit", "revenue"],
        rules(
            "Delaware",
            notes="DE EITC: must qualify for federal EITC; Delaware resident return; choose refundable (~4.5% of federal) or nonrefundable (~20% of federal) per current PIT-RSS instructions. Percentages and options can change by tax year — verify.",
            verify_notes="Refundable vs nonrefundable percentages and federal EITC linkage — verify=true via revenue.delaware.gov PIT forms/instructions.",
        ),
    )
)

# Rhode Island
NEW.append(
    scheme(
        "ri-eitc",
        "Rhode Island Earned Income Tax Credit (EITC) – Division of Taxation",
        "Rhode Island EITC – रोड आइलैंड",
        "Rhode Island provides a refundable earned income tax credit equal to a percentage of the federal EITC for qualifying filers. For tax years beginning on or after January 1, 2024, the RI EITC is 16% of the federal credit and is fully refundable.",
        "Refundable Rhode Island tax credit equal to 16% of the federal EITC (current law for TY2024+).",
        [
            "Federal return claiming federal EITC",
            "RI-1040 with RI Schedule EIC",
            "Rhode Island residency / filing documentation",
        ],
        "File RI-1040 with Schedule EIC via tax.ri.gov forms and instructions.",
        "https://tax.ri.gov/forms/individual-tax-forms/personal-income-tax-forms",
        "https://tax.ri.gov/forms/individual-tax-forms/personal-income-tax-forms",
        "Rhode Island Division of Taxation",
        ["united_states", "rhode_island", "eitc", "tax_credit", "refundable"],
        rules(
            "Rhode Island",
            notes="RI EITC: qualify for federal EITC; RI credit = 16% of federal for TY beginning 2024+; fully refundable. Federal income limits apply — not encoded as one RI ceiling.",
            verify_notes="Percentage and federal linkage — verify=true via tax.ri.gov RI-1040 / Schedule EIC instructions.",
        ),
    )
)

# Vermont
NEW.append(
    scheme(
        "vt-dr-dynasaur",
        "Dr. Dynasaur (CHIP / children’s Medicaid) – Vermont DVHA",
        "Dr. Dynasaur – वर्मांट",
        "Dr. Dynasaur is Vermont’s low-cost or free health coverage for children and teenagers under age 19 (and eligible pregnant people). It is Vermont’s CHIP/children’s Medicaid pathway administered with Vermont Health Connect / DVHA.",
        "Free or low-cost health coverage for eligible Vermont children under 19 and eligible pregnant people.",
        [
            "Identity and Vermont residency",
            "Income documentation",
            "Child / pregnancy information",
        ],
        "Apply through Vermont Health Connect (VermontHealthConnect.gov) or DVHA apply pathways linked from dvha.vermont.gov Dr. Dynasaur pages.",
        "https://dvha.vermont.gov/members/dr-dynasaur",
        "https://dvha.vermont.gov/members/dr-dynasaur",
        "Vermont Department of Vermont Health Access (DVHA) / Vermont Health Connect",
        ["united_states", "vermont", "chip", "kids", "children", "medicaid", "dr_dynasaur", "health"],
        rules(
            "Vermont",
            notes="Dr. Dynasaur: children under 19 (official pages cite household income below ~312% FPL for children) and pregnant people (lower FPL band). Premiums for children may be suspended. No single annual ceiling encoded.",
            verify_notes="FPL bands, pregnancy postpartum coverage, and premiums — verify=true via dvha.vermont.gov / Vermont Health Connect.",
            max_age=18,
        ),
    )
)
NEW.append(
    scheme(
        "vt-eitc",
        "Vermont Earned Income Tax Credit (EITC) – Department of Taxes",
        "Vermont EITC – वर्मांट",
        "Vermont offers a state earned income tax credit based on a percentage of the federal EITC for qualifying Vermont residents. Vermont also publishes guidance for claiming the credit (and Vermont CTC) in certain SSN/ITIN situations.",
        "State EITC claimed on Vermont personal income tax return (Schedule IN-112 / related schedules).",
        [
            "Federal EITC calculation / Schedule EIC as applicable",
            "Vermont income tax return and credit schedules",
            "Residency documentation",
        ],
        "File Vermont personal income tax forms and credit schedules available at tax.vermont.gov; see Department of Taxes credit guidance.",
        "https://tax.vermont.gov/individuals/personal-income-tax/tax-credits/no-ssn-itin",
        "https://tax.vermont.gov/individuals/personal-income-tax/tax-credits/no-ssn-itin",
        "Vermont Department of Taxes",
        ["united_states", "vermont", "eitc", "tax_credit", "refundable"],
        rules(
            "Vermont",
            notes="VT EITC: percentage of federal EITC for qualifying Vermont residents (rate on current IN-112 instructions). Special SSN/ITIN filing paths exist per tax.vermont.gov. No single AGI ceiling encoded beyond federal EITC linkage.",
            verify_notes="State percentage of federal EITC and filing rules — verify=true via tax.vermont.gov IN-112 instructions.",
        ),
    )
)

# New Hampshire
NEW.append(
    scheme(
        "nh-childrens-medicaid",
        "Children’s Medicaid / Expanded Children’s Medicaid (CHIP) – New Hampshire DHHS",
        "Children’s Medicaid – न्यू हैम्पशायर",
        "New Hampshire Children’s Medicaid (Expanded Children’s Medicaid) provides health coverage for eligible children under 19, including CHIP expansion pathways administered by DHHS. Apply through NH EASY.",
        "Medicaid/CHIP health coverage for eligible New Hampshire children under 19.",
        [
            "Identity and New Hampshire residency",
            "Income documentation",
            "Child information",
        ],
        "Apply online at nheasy.nh.gov or follow DHHS Medicaid program pages.",
        "https://nheasy.nh.gov/",
        "https://www.dhhs.nh.gov/programs-services/medicaid",
        "New Hampshire Department of Health and Human Services (DHHS)",
        ["united_states", "new_hampshire", "chip", "kids", "children", "medicaid", "dhhs", "nh_easy"],
        rules(
            "New Hampshire",
            notes="NH Children’s Medicaid / Expanded Children’s Medicaid: children under 19; income up to published FPL (DHHS materials cite expansion around ~323% FPL with disregard — verify current chart). No single annual ceiling encoded.",
            verify_notes="Current FPL charts and continuous eligibility — verify=true via dhhs.nh.gov / NH EASY.",
            max_age=18,
        ),
    )
)
NEW.append(
    scheme(
        "nh-child-care-scholarship",
        "New Hampshire Child Care Scholarship – DHHS",
        "NH Child Care Scholarship – न्यू हैम्पशायर",
        "New Hampshire Child Care Scholarship helps eligible low-income working families pay for child care while parents work, attend school, or participate in approved activities. Funded through federal CCDF partnership administered by DHHS.",
        "Child care subsidy / scholarship payments for eligible New Hampshire families.",
        [
            "Identity and residency",
            "Income and work/school activity documentation",
            "Child information / provider information",
        ],
        "Apply through NH EASY / DHHS child care scholarship pathways linked from dhhs.nh.gov.",
        "https://nheasy.nh.gov/",
        "https://www.dhhs.nh.gov/programs-services/childcare",
        "New Hampshire Department of Health and Human Services (DHHS)",
        ["united_states", "new_hampshire", "child_care", "scholarship", "ccdf", "dhhs"],
        rules(
            "New Hampshire",
            notes="NH Child Care Scholarship: low-income families with work/school/approved activities; income and provider rules. No single annual ceiling encoded.",
            verify_notes="Income tiers and activity requirements — verify=true via dhhs.nh.gov child care / NH EASY.",
        ),
    )
)

# Maine
NEW.append(
    scheme(
        "me-chip-children",
        "MaineCare / CHIP for Children (Cub Care pathway) – Maine DHHS",
        "MaineCare / CHIP बच्चे – मेन",
        "Maine provides free MaineCare or CHIP coverage for eligible children under 19 (historically branded Cub Care). Household income is generally up to published FPL percentages with no asset test for children’s coverage pathways.",
        "Free or low-cost health coverage for eligible Maine children under 19.",
        [
            "Identity and Maine residency",
            "Income documentation",
            "Child information",
        ],
        "Apply online at MyMaineConnection.gov or follow maine.gov/dhhs OMS children MaineCare options pages.",
        "https://www.mymaineconnection.gov/",
        "https://www.maine.gov/dhhs/oms/mainecare-options/children",
        "Maine Department of Health and Human Services / Office of MaineCare Services",
        ["united_states", "maine", "chip", "kids", "children", "medicaid", "mainecare", "cub_care"],
        rules(
            "Maine",
            notes="MaineCare/CHIP children: under 19; income generally up to ~300% FPL per OMS children pages; no asset test for children’s pathways. No single annual ceiling encoded.",
            verify_notes="Income standards and CHIP rule updates — verify=true via maine.gov/dhhs OMS children.",
            max_age=18,
        ),
    )
)
NEW.append(
    scheme(
        "me-eitc",
        "Maine Earned Income Credit (EIC) – Maine Revenue Services",
        "Maine EIC – मेन",
        "Maine’s Earned Income Credit equals 25% of the federal EITC for taxpayers with qualifying children (50% for taxpayers with no qualifying children) for tax years beginning on or after January 1, 2022. Refundable for Maine residents and part-year residents.",
        "Refundable Maine income tax credit based on a percentage of the federal EITC.",
        [
            "Federal EITC information",
            "Form 1040ME, Schedule A, and Maine EITC worksheet",
        ],
        "Claim on Form 1040ME with Schedule A and the Earned Income Tax Credit Worksheet from maine.gov/revenue.",
        "https://www.maine.gov/revenue/taxes/tax-relief-credits-programs/income-tax-credits/earned-income-credit",
        "https://www.maine.gov/revenue/taxes/tax-relief-credits-programs/income-tax-credits/earned-income-credit",
        "Maine Revenue Services",
        ["united_states", "maine", "eitc", "tax_credit", "refundable", "revenue"],
        rules(
            "Maine",
            notes="Maine EIC: 25% of federal EITC with qualifying children / 50% with no qualifying children (TY2022+); refundable for residents and part-year residents; ITIN and age pathways described on MRS page. Federal EITC income limits apply.",
            verify_notes="Percentages and Form 1040ME worksheet — verify=true via maine.gov/revenue EIC page.",
        ),
    )
)

# West Virginia
NEW.append(
    scheme(
        "wv-family-tax-credit",
        "West Virginia Family Tax Credit (Low-Income Family Tax Credit) – Tax Division",
        "WV Family Tax Credit – वेस्ट वर्जीनिया",
        "West Virginia’s Family Tax Credit (Schedule FTC-1) can reduce or eliminate West Virginia personal income tax for eligible low-income individuals and families based on modified federal AGI and family size. Zero-exemption filers and federal AMT payers do not qualify.",
        "Nonrefundable reduction or elimination of WV personal income tax for eligible low-income filers.",
        [
            "West Virginia IT-140 return",
            "Schedule FTC-1",
            "Income and exemption information",
        ],
        "Claim Schedule FTC-1 with Form IT-140 using forms/instructions from tax.wv.gov.",
        "https://tax.wv.gov/Documents/PIT/2025/it140.PersonalIncomeTaxFormsAndInstructions.2025.pdf",
        "https://tax.wv.gov/Documents/TSD/tsd110.pdf",
        "West Virginia Tax Division",
        ["united_states", "west_virginia", "tax_credit", "family_tax_credit", "low_income"],
        rules(
            "West Virginia",
            notes="WV Family Tax Credit (W. Va. Code §11-21-22): income and family-size tables on Schedule FTC-1; not available to zero-exemption filers or federal AMT payers. Tables change by tax year — not encoded as one ceiling.",
            verify_notes="FTC-1 income tables and exclusions — verify=true via tax.wv.gov PIT instructions / TSD 110.",
        ),
    )
)

# Mississippi
NEW.append(
    scheme(
        "ms-homestead-exemption",
        "Mississippi Homestead Exemption – Department of Revenue",
        "मिसिसिपी Homestead Exemption",
        "Mississippi Homestead Exemption provides property tax relief for eligible owner-occupied primary residences. Additional age/disability tiers may increase relief. Applications are handled through the county tax assessor with DOR program rules.",
        "Property tax exemption / credit on an eligible Mississippi homestead (amount depends on tier).",
        [
            "Proof of ownership and occupancy of primary residence",
            "Mississippi residency",
            "Age or disability documentation if claiming enhanced tiers",
            "County assessor homestead application",
        ],
        "Apply through your county tax assessor following Mississippi Department of Revenue homestead exemption guidance at dor.ms.gov.",
        "https://www.dor.ms.gov/county-services/homestead-exemption",
        "https://www.dor.ms.gov/county-services/homestead-exemption",
        "Mississippi Department of Revenue / County Tax Assessors",
        ["united_states", "mississippi", "homestead", "property_tax", "housing", "dor"],
        rules(
            "Mississippi",
            notes="MS Homestead Exemption: owner-occupied primary residence; standard and age/disability tiers per DOR. Not an income-tested cash benefit; some tiers have additional rules. Confirm current credit amounts with DOR/county.",
            verify_notes="Exemption amounts and age/disability tiers — verify=true via dor.ms.gov homestead exemption.",
            implies_low_income=False,
        ),
    )
)

# Arkansas
NEW.append(
    scheme(
        "us-ar-tea-work-supports",
        "Arkansas TEA Work Supports / Transitional Employment Assistance supports – DHS",
        "Arkansas TEA work supports – आर्कान्सा",
        "Beyond basic TEA cash, Arkansas DHS Transitional Employment Assistance provides related work supports for eligible families moving toward employment (child care, transportation, and case management as authorized). Apply via Access Arkansas / DHS.",
        "Employment-related supports for eligible TEA / TANF families in Arkansas (services vary by case plan).",
        [
            "Identity and Arkansas residency",
            "Income and household documentation",
            "Proof of children / work activities as required",
        ],
        "Apply through Access Arkansas or county DHS offices; see humanservices.arkansas.gov TEA / TANF pages.",
        "https://access.arkansas.gov/Learn/Home",
        "https://humanservices.arkansas.gov/divisions-shared-services/county-operations/temporary-assistance-for-needy-families/transitional-employment-assistance/",
        "Arkansas Department of Human Services / County Operations",
        ["united_states", "arkansas", "tanf", "tea", "work_supports", "employment", "dhs"],
        rules(
            "Arkansas",
            notes="Arkansas TEA work supports: low-income families with dependent children meeting TEA/TANF rules; specific supports depend on approved employment plan. No single annual ceiling encoded.",
            verify_notes="TEA eligibility, time limits, and support types — verify=true via humanservices.arkansas.gov TEA.",
        ),
    )
)

# Iowa
NEW.append(
    scheme(
        "ia-eitc",
        "Iowa Earned Income Tax Credit – Department of Revenue",
        "Iowa EITC – आयोवा",
        "Iowa’s refundable Earned Income Tax Credit equals 15% of the federal EITC for qualifying filers. Claimed on the Iowa individual income tax return.",
        "Refundable Iowa tax credit equal to 15% of the federal EITC.",
        [
            "Federal return claiming federal EITC",
            "Iowa individual income tax return",
        ],
        "Claim on the Iowa income tax return using forms/guidance from revenue.iowa.gov.",
        "https://revenue.iowa.gov/taxes/tax-guidance/individual-income-tax/1040-expanded-instructions/other-nonrefundable-iowa-credits",
        "https://revenue.iowa.gov/taxes/tax-guidance/individual-income-tax/1040-expanded-instructions/other-nonrefundable-iowa-credits",
        "Iowa Department of Revenue",
        ["united_states", "iowa", "eitc", "tax_credit", "refundable"],
        rules(
            "Iowa",
            notes="Iowa EITC: 15% of federal EITC for qualifying filers (Iowa Administrative Code / Revenue guidance). Federal EITC income limits apply — not a separate Iowa AGI ceiling in catalogue.",
            verify_notes="Confirm current percentage and claim lines — verify=true via revenue.iowa.gov.",
        ),
    )
)
NEW.append(
    scheme(
        "ia-rent-reimbursement",
        "Iowa Rent Reimbursement – Iowa HHS",
        "Iowa Rent Reimbursement – आयोवा",
        "Iowa Rent Reimbursement helps eligible Iowa renters age 65+ or adults 18+ who are totally disabled with a refund based on rent paid, subject to income limits and property-taxable housing rules.",
        "Annual rent reimbursement payment for eligible Iowa senior or totally disabled renters (subject to income cap and formula).",
        [
            "Proof of rent paid",
            "Age 65+ or total disability documentation",
            "Income documentation",
            "Iowa residency",
        ],
        "Apply via Iowa.gov Rent Reimbursement / Iowa HHS instructions for the claim year.",
        "https://www.iowa.gov/how-do-i-apply-rent-reimbursement",
        "https://www.iowa.gov/how-do-i-apply-rent-reimbursement",
        "Iowa Department of Health and Human Services (HHS)",
        ["united_states", "iowa", "rent_reimbursement", "housing", "senior", "disability"],
        rules(
            "Iowa",
            notes="Iowa Rent Reimbursement: age 65+ or totally disabled age 18+; income within published annual limit for claim year (HHS publishes yearly; e.g. prior guidance cited mid-$20k range — verify current); reimbursement based on percentage of rent with caps. No single permanent ceiling encoded.",
            verify_notes="Annual income limit, disability definition, and reimbursement formula — verify=true via iowa.gov / HHS rent reimbursement.",
            min_age=18,
        ),
    )
)

# Kansas
NEW.append(
    scheme(
        "ks-chip",
        "Kansas CHIP (Children’s Health Insurance under KanCare) – KDHE / DCF",
        "Kansas CHIP – कान्सास",
        "Kansas CHIP covers uninsured children under 19 whose household income exceeds Medicaid limits but falls within CHIP bands. Coverage is delivered through KanCare; premiums may apply above certain FPL levels.",
        "CHIP health coverage for eligible Kansas children under 19 (KanCare).",
        [
            "Identity and Kansas residency",
            "Income documentation",
            "Child information",
            "Proof of being uninsured as required",
        ],
        "Apply through Medical KEES / KanCare eligibility pathways (cssp.kees.ks.gov) or DCF/KDHE guidance.",
        "https://cssp.kees.ks.gov/apspssp/",
        "https://www.kdhe.ks.gov/185/KanCare-Eligibility-Guidelines",
        "Kansas Department of Health and Environment / DCF (KanCare)",
        ["united_states", "kansas", "chip", "kids", "children", "kancare", "medicaid", "health"],
        rules(
            "Kansas",
            notes="KS CHIP: uninsured children under 19; income above Medicaid but within CHIP FPL bands; family premiums may apply above ~167% FPL per KDHE guidelines. No single annual ceiling encoded.",
            verify_notes="CHIP premiums and FPL bands — verify=true via kdhe.ks.gov KanCare Eligibility Guidelines.",
            max_age=18,
        ),
    )
)
NEW.append(
    scheme(
        "ks-homestead",
        "Kansas Homestead Property Tax Refund – Department of Revenue",
        "Kansas Homestead Refund – कान्सास",
        "Kansas Homestead Property Tax Refund (Form K-40H) provides a refund to eligible homeowners who owned and occupied a qualifying Kansas homestead all year, meet income limits, and meet age, disability, or dependent-child requirements.",
        "Property tax refund for eligible Kansas homesteaders (amount per Form K-40H tables; subject to annual income limit).",
        [
            "Form K-40H",
            "Proof of homestead ownership/occupancy",
            "Income documentation",
            "Age, disability, or dependent-child documentation as applicable",
        ],
        "File Form K-40H with Kansas Department of Revenue using current instruction booklet at ksrevenue.gov.",
        "https://www.ksrevenue.gov/pdf/k-40hbook25.pdf",
        "https://www.ksrevenue.gov/pdf/k-40hbook25.pdf",
        "Kansas Department of Revenue",
        ["united_states", "kansas", "homestead", "property_tax", "refund", "housing"],
        rules(
            "Kansas",
            notes="KS Homestead (K-40H): full-year Kansas homeowner-occupant; household income within published annual limit (instruction booklet cites limit near low-$40k for recent year — verify current); age 55+/disability/dependent-child pathways; refund capped per tables.",
            verify_notes="Income limit, age/disability pathways, and refund caps — verify=true via ksrevenue.gov K-40H booklet.",
        ),
    )
)

# Nebraska
NEW.append(
    scheme(
        "ne-kids-connection",
        "Kids Connection (CHIP) – Nebraska DHHS",
        "Kids Connection CHIP – नेब्रास्का",
        "Nebraska Kids Connection is the state’s CHIP program providing Medicaid-covered services to eligible uninsured children age 18 and younger who do not qualify for regular Medicaid. Apply through iServe Nebraska.",
        "CHIP health coverage for eligible Nebraska children 18 and under.",
        [
            "Identity and Nebraska residency",
            "Income documentation",
            "Child information",
            "Uninsured status as required",
        ],
        "Apply online at iserve.nebraska.gov or follow dhhs.ne.gov Medicaid eligibility pages.",
        "https://iserve.nebraska.gov/",
        "https://dhhs.ne.gov/pages/Medicaid-Eligibility.aspx",
        "Nebraska Department of Health and Human Services (DHHS)",
        ["united_states", "nebraska", "chip", "kids", "children", "kids_connection", "medicaid", "health"],
        rules(
            "Nebraska",
            notes="Kids Connection (CHIP): uninsured children ≤18 not eligible for regular Medicaid; income and residency rules. No single annual ceiling encoded.",
            verify_notes="CHIP vs Medicaid income bands — verify=true via dhhs.ne.gov Medicaid Eligibility / iServe.",
            max_age=18,
        ),
    )
)
NEW.append(
    scheme(
        "ne-eitc",
        "Nebraska Earned Income Tax Credit – Department of Revenue",
        "Nebraska EITC – नेब्रास्का",
        "Nebraska offers a refundable state earned income tax credit equal to a percentage of the federal EITC for qualifying Nebraska filers. Claimed on the Nebraska individual income tax return.",
        "Refundable Nebraska tax credit based on a percentage of the federal EITC.",
        [
            "Federal return claiming federal EITC",
            "Nebraska individual income tax return",
        ],
        "Claim on the Nebraska income tax return using forms from revenue.nebraska.gov.",
        "https://revenue.nebraska.gov/sites/default/files/doc/tax-forms/2025/f_Individual_Income_Tax_Booklet.pdf",
        "https://revenue.nebraska.gov/sites/default/files/doc/tax-forms/2025/f_Individual_Income_Tax_Booklet.pdf",
        "Nebraska Department of Revenue",
        ["united_states", "nebraska", "eitc", "tax_credit", "refundable"],
        rules(
            "Nebraska",
            notes="NE EITC: refundable credit equal to 10% of federal EITC for Nebraska residents (and eligible partial-year residents with income ratio); nonresidents generally ineligible. Federal EITC limits apply.",
            verify_notes="Confirm current 10% rate and Schedule I lines — verify=true via revenue.nebraska.gov Individual Income Tax Booklet.",
        ),
    )
)

# North Dakota
NEW.append(
    scheme(
        "nd-homestead-credit",
        "North Dakota Homestead Property Tax Credit & Renter’s Refund – Tax Commissioner",
        "ND Homestead Credit – नॉर्थ डकोटा",
        "North Dakota Homestead Property Tax Credit helps eligible senior or permanently disabled homeowners reduce property taxes; eligible renters may qualify for a renter’s refund. Apply through the local assessor / Tax Commissioner program.",
        "Property tax credit for eligible ND homeowners and/or renter’s refund for eligible renters (subject to income and age/disability rules).",
        [
            "Age 65+ or permanent disability documentation",
            "Income documentation",
            "Proof of homestead ownership or rent paid",
            "North Dakota residency",
        ],
        "Homeowners apply through the local assessor by the published deadline; see tax.nd.gov Homestead Property Tax Credit and Renter’s Refund.",
        "https://www.tax.nd.gov/homestead-property-tax-credit-and-renters-refund",
        "https://www.tax.nd.gov/homestead-property-tax-credit-and-renters-refund",
        "North Dakota Office of State Tax Commissioner / Local Assessors",
        ["united_states", "north_dakota", "homestead", "property_tax", "renters_refund", "housing", "senior"],
        rules(
            "North Dakota",
            notes="ND Homestead Credit: homeowners 65+ or permanently disabled; household income within published limit (program materials cite up to $70,000 — verify current); renters may receive refunds up to published cap. Apply by local deadlines.",
            verify_notes="Income limits, disability definition, renter caps, deadlines — verify=true via tax.nd.gov homestead page.",
            min_age=65,
        ),
    )
)

# South Dakota
NEW.append(
    scheme(
        "sd-tax-refund",
        "South Dakota Sales or Property Tax Refund (Senior/Disabled) – DOR",
        "SD Tax Refund – साउथ डकोटा",
        "South Dakota Department of Revenue administers an annual refund program for eligible senior citizens and citizens with disabilities that refunds part of prior-year sales tax paid, or property tax, whichever is greater (cannot receive both).",
        "Annual sales-tax or property-tax refund for eligible SD seniors/disabled residents meeting income limits.",
        [
            "Age or disability documentation",
            "Income documentation for prior year",
            "South Dakota residency",
            "DOR refund application for the claim year",
        ],
        "Submit the DOR Sales or Property Tax Refund application by the published deadline (dor.sd.gov).",
        "https://dor.sd.gov/newsroom/tax-refund-program-open-to-senior-citizens-and-citizens-with-disabilities/",
        "https://dor.sd.gov/newsroom/tax-refund-program-open-to-senior-citizens-and-citizens-with-disabilities/",
        "South Dakota Department of Revenue (DOR)",
        ["united_states", "south_dakota", "tax_refund", "senior", "disability", "property_tax", "sales_tax"],
        rules(
            "South Dakota",
            notes="SD senior/disabled tax refund: residency, age/disability, and income limits published annually (single vs household differ). Refund is sales tax or property tax component, not both. No permanent ceiling encoded.",
            verify_notes="Annual income limits, deadlines, and application form year — verify=true via dor.sd.gov.",
        ),
    )
)

# Montana
NEW.append(
    scheme(
        "mt-eitc",
        "Montana Earned Income Tax Credit – Department of Revenue",
        "Montana EITC – मोंटाना",
        "Montana’s refundable Earned Income Tax Credit is generally 10% of the federal EITC for eligible Montana residents who claim the federal credit. File Montana Form 2; nonresidents do not qualify.",
        "Refundable Montana tax credit equal to 10% of the federal EITC for qualifying residents.",
        [
            "Federal return claiming federal EITC",
            "Montana Form 2",
            "Montana residency",
        ],
        "Claim on Montana Form 2 using revenue.mt.gov EITC guidance and Form 2 instructions.",
        "https://revenue.mt.gov/taxes/tax-credits/mt-earned-income-tax-credit",
        "https://revenue.mt.gov/taxes/tax-credits/mt-earned-income-tax-credit",
        "Montana Department of Revenue",
        ["united_states", "montana", "eitc", "tax_credit", "refundable"],
        rules(
            "Montana",
            notes="MT EITC: generally 10% of federal EITC; Montana residents; nonresidents ineligible; part-year residents may receive proportional credit. Federal EITC limits apply.",
            verify_notes="Rate and residency proration — verify=true via revenue.mt.gov MT EITC / Form 2 instructions.",
        ),
    )
)

# Wyoming
NEW.append(
    scheme(
        "wy-child-care",
        "Wyoming Child Care Subsidy / ECARES – DFS",
        "Wyoming Child Care Subsidy – वायोमिंग",
        "Wyoming Department of Family Services Child Care Subsidy helps eligible low-income families pay for child care while parents work, attend school, or participate in approved training. Provider and family enrollment runs through ECARES.",
        "Child care subsidy payments for eligible Wyoming families.",
        [
            "Identity and Wyoming residency",
            "Income and work/school activity documentation",
            "Child and provider information",
        ],
        "Apply / check eligibility through DFS Child Care Assistance and ECARES pathways on dfs.wyo.gov.",
        "https://dfs.wyo.gov/services/family-services/child-care/",
        "https://dfs.wyo.gov/services/family-services/child-care/",
        "Wyoming Department of Family Services (DFS)",
        ["united_states", "wyoming", "child_care", "subsidy", "ccdf", "dfs"],
        rules(
            "Wyoming",
            notes="WY Child Care Subsidy: low-income families with approved work/school/training activities; income and provider rules via DFS/ECARES. No single annual ceiling encoded.",
            verify_notes="Income tiers and ECARES enrollment — verify=true via dfs.wyo.gov child care.",
        ),
    )
)

# Idaho
NEW.append(
    scheme(
        "id-property-tax-reduction",
        "Idaho Property Tax Reduction (Circuit Breaker) – State Tax Commission",
        "Idaho Property Tax Reduction – आइडाहो",
        "Idaho’s Property Tax Reduction (Circuit Breaker) program may reduce property taxes for eligible homeowners (age 65+, disabled, blind, widowed, and other listed statuses) with income at or below the published annual bracket.",
        "Property tax reduction credit for eligible Idaho homeowners meeting status and income rules.",
        [
            "Proof of homeownership and occupancy",
            "Age/disability/widow/other qualifying status documentation",
            "Income documentation for prior year",
            "Property Tax Reduction application by deadline",
        ],
        "Apply with the county / State Tax Commission Property Tax Reduction program by the published deadline (tax.idaho.gov).",
        "https://tax.idaho.gov/taxes/property/homeowners/reduction/",
        "https://tax.idaho.gov/taxes/property/homeowners/reduction/",
        "Idaho State Tax Commission / County Assessors",
        ["united_states", "idaho", "property_tax", "circuit_breaker", "housing", "senior"],
        rules(
            "Idaho",
            notes="Idaho Property Tax Reduction: eligible status categories (65+, disabled, blind, widowed, etc.); income at or below published bracket for claim year; reduction amount within published min/max. No permanent ceiling encoded.",
            verify_notes="Income brackets, status categories, deadlines, reduction range — verify=true via tax.idaho.gov Property Tax Reduction.",
        ),
    )
)


def _host_is_gov(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host.endswith(".gov")


def _retag_chip(schemes: list[dict]) -> int:
    """Ensure BadgerCare and similar kids-health packs carry chip tags."""
    n = 0
    for s in schemes:
        if s["id"] == "wi-badgercare":
            tags = s.setdefault("tags", [])
            for t in ("chip", "kids", "children"):
                if t not in tags:
                    tags.append(t)
                    n += 1
            s["last_verified"] = LAST
        if s["id"] == "vt-medicaid":
            tags = s.setdefault("tags", [])
            for t in ("chip", "kids", "children"):
                if t not in tags:
                    tags.append(t)
                    n += 1
            s["last_verified"] = LAST
        if s["id"] == "ct-husky":
            tags = s.setdefault("tags", [])
            for t in ("chip", "kids", "children"):
                if t not in tags:
                    tags.append(t)
                    n += 1
            s["last_verified"] = LAST
        if s["id"] == "ri-rite-care":
            tags = s.setdefault("tags", [])
            for t in ("chip", "kids", "children"):
                if t not in tags:
                    tags.append(t)
                    n += 1
            s["last_verified"] = LAST
    return n


def main() -> None:
    assert len(NEW) >= 20
    for s in NEW:
        assert _host_is_gov(s["official_source_url"]), (s["id"], s["official_source_url"])
        assert _host_is_gov(s["apply_url"]), (s["id"], s["apply_url"])
        assert s["eligibility_rules"]["countries"] == ["United States"]
        assert s["eligibility_rules"]["nationwide"] is False
        assert len(s["eligibility_rules"]["states"]) == 1
        assert s["eligibility_rules"]["max_annual_income"] is None
        assert s["eligibility_rules"]["max_monthly_household_income"] is None
        assert s["last_verified"] == LAST
        assert s["eligibility_rules"]["verify"] is True

    schemes = json.loads(DATA.read_text())
    existing = {x["id"] for x in schemes}

    dups = [s["id"] for s in NEW if s["id"] in existing]
    if dups:
        print(f"skip already-present ids ({len(dups)}): {dups}")
        NEW[:] = [s for s in NEW if s["id"] not in existing]

    retag_n = _retag_chip(schemes)

    if NEW:
        schemes.extend(NEW)

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    count = len(schemes)
    wave_note = (
        "US Wave W3 deepen (2026-09-23): remaining states CT/DE/RI/VT/NH/ME/WV/MS/AR/IA/KS/NE/ND/SD/MT/WY/ID "
        "plus nationwide core gap-fills (FL LIHEAP; AK Denali KidCare; HI/NM/OK/WA/NH/ME/KS/NE children’s CHIP pathways; "
        "VT Dr. Dynasaur explicit; state EITC/housing/homestead distinctive adds). All .gov; last_verified 2026-09-23; "
        "nationwide:false for state rows; quality over forced count."
    )
    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = count
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = "2026-09-23T10:21:00+05:30"
        scope = meta.get("scope", "")
        if "US Wave W3 deepen (2026-09-23)" not in scope:
            meta["scope"] = scope.rstrip(".") + "; " + wave_note
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    print(f"Added {len(NEW)} schemes; retag ops={retag_n}; total {count}")
    by: dict[str, list[str]] = {}
    for s in NEW:
        st = s["eligibility_rules"]["states"][0]
        by.setdefault(st, []).append(s["id"])
    for st, ids in sorted(by.items()):
        print(f"  {st}: {ids}")


if __name__ == "__main__":
    main()
