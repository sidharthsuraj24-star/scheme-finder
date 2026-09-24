#!/usr/bin/env python3
"""US big-states distinctive deepen (2026-09-24).

Finish FAILED W1/W2 deepen for large/high-priority states after W3 (d18a766, 661 schemes).
Official .gov ONLY; never invent eligibility ceilings; verify:true; last_verified 2026-09-24.
Ambiguous ID collisions: us-ga-*, us-tn-*, us-in-* for new Georgia/Tennessee/Indiana rows.
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
LAST = "2026-09-24"


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
    disability_required: bool = False,
    categories: list | None = None,
    gender: str | None = None,
) -> dict:
    return {
        "min_age": min_age,
        "max_age": max_age,
        "max_annual_income": None,
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
# CALIFORNIA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "ca-cal-grant",
        "Cal Grant – California Student Aid Commission",
        "Cal Grant – कैलिफ़ोर्निया",
        "California’s primary need-based college grant that does not need to be repaid. Students attending Cal Grant–eligible institutions are considered after timely FAFSA or California Dream Act Application (CADAA) submission plus a verified GPA.",
        "Need-based tuition and education grant aid at eligible California colleges (award type and amount depend on Cal Grant path and school).",
        [
            "FAFSA or California Dream Act Application (CADAA)",
            "Verified Cal Grant GPA or test score via school",
            "California residency / Dream Act eligibility documentation as required",
            "WebGrants 4 Students account to track awards",
        ],
        "Submit FAFSA (studentaid.gov) or CADAA (dream.csac.ca.gov) by the CSAC priority deadline; confirm GPA on WebGrants 4 Students (mygrantinfo.csac.ca.gov).",
        "https://csac.ca.gov/how-apply",
        "https://csac.ca.gov/cal-grant",
        "California Student Aid Commission (CSAC)",
        ["united_states", "california", "cal_grant", "college", "education", "grant", "need_based"],
        rules(
            "California",
            notes="Cal Grant: California students at Cal Grant–eligible schools; financial need/income-asset screens, GPA, and FAFSA/CADAA timing apply. No single annual ceiling encoded — CSAC tables and award types (A/B/C etc.) vary.",
            verify_notes="Deadlines, income/asset ceilings, and award amounts change by academic year — verify=true via csac.ca.gov Cal Grant.",
        ),
    )
)
NEW.append(
    scheme(
        "ca-yctc",
        "California Young Child Tax Credit (YCTC)",
        "YCTC – कैलिफ़ोर्निया युवा बाल कर क्रेडिट",
        "Refundable California Young Child Tax Credit for eligible families with a qualifying child under age 6. Claimed with FTB Form 3514 alongside CalEITC pathways; tables publish annually on ftb.ca.gov.",
        "Refundable state tax credit (up to the published YCTC maximum for the tax year) for qualifying California returns with a young child.",
        [
            "California income tax return",
            "FTB 3514",
            "SSN or ITIN for filer and qualifying child",
            "Proof of qualifying child under age 6",
        ],
        "File a California return claiming YCTC on FTB 3514 (CalFile, VITA, or preparer). See ftb.ca.gov Young Child Tax Credit.",
        "https://www.ftb.ca.gov/file/personal/credits/young-child-tax-credit.html",
        "https://www.ftb.ca.gov/file/personal/credits/young-child-tax-credit.html",
        "California Franchise Tax Board (FTB)",
        ["united_states", "california", "yctc", "tax_credit", "child", "income_support"],
        rules(
            "California",
            notes="YCTC (FTB): generally CalEITC-related path with qualifying child under 6 at year-end; income/AGI within published CalEITC/YCTC table (TY2025 table cites max credit and phaseouts). Zero-earned-income path has separate net-loss/wage caps — verify annually.",
            verify_notes="Tax-year credit max, phaseouts, and zero-income path caps change — verify=true via ftb.ca.gov YCTC. No permanent ceiling encoded.",
        ),
    )
)
NEW.append(
    scheme(
        "ca-care-fera",
        "CARE / FERA Utility Discount – California CPUC",
        "CARE/FERA – कैलिफ़ोर्निया उपयोगिता छूट",
        "California Alternate Rates for Energy (CARE) and Family Electric Rate Assistance (FERA) provide income-qualified discounts on electric and/or gas bills from CPUC-regulated utilities. Apply through your utility.",
        "Ongoing percentage discount on eligible electric and/or gas bills (CARE roughly 30–35% electric / 20% gas; FERA roughly 18% electric for households above CARE limits — utility-specific).",
        [
            "Utility account information",
            "Income documentation or categorical program enrollment proof",
            "Household size information",
            "CARE/FERA application via utility",
        ],
        "Contact your electric/gas utility CARE/FERA program (links on cpuc.ca.gov CARE/FERA page) and submit the utility’s application.",
        "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/electric-costs/care-fera-program",
        "https://www.cpuc.ca.gov/industries-and-topics/electrical-energy/electric-costs/care-fera-program",
        "California Public Utilities Commission (CPUC) / regulated utilities",
        ["united_states", "california", "care", "fera", "energy", "utility", "discount"],
        rules(
            "California",
            notes="CARE/FERA: income at or below published household-size guidelines (CPUC tables, e.g. June 2026–May 2027 CARE/FERA charts) or categorical public-assistance enrollment; served by participating utility. No single annual ceiling encoded.",
            verify_notes="Income charts and discount percentages update periodically — verify=true via cpuc.ca.gov CARE/FERA and your utility.",
        ),
    )
)

# ---------------------------------------------------------------------------
# TEXAS
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "tx-texas-grant",
        "TEXAS Grant – Toward EXcellence, Access & Success",
        "TEXAS Grant – टेक्सास",
        "Need-based Texas Higher Education Coordinating Board grant for eligible Texas residents pursuing a bachelor’s degree at participating public universities/health-related institutions. Awarded through the college financial-aid office after FAFSA or TASFA.",
        "Need-based grant aid toward tuition and related costs at eligible Texas public universities (funding limited; amounts set annually).",
        [
            "FAFSA or Texas Application for State Financial Aid (TASFA)",
            "Texas residency documentation as required by institution",
            "Enrollment at eligible Texas public university / HRI",
            "Satisfactory academic progress for renewal",
        ],
        "Complete FAFSA or TASFA (highered.texas.gov TASFA) by your school’s and statewide priority deadlines; your financial-aid office awards TEXAS Grant if funds and eligibility allow.",
        "https://www.highered.texas.gov/students-families/tasfa/",
        "https://www.highered.texas.gov/student-financial-aid-programs/grant-loan-programs/",
        "Texas Higher Education Coordinating Board (THECB)",
        ["united_states", "texas", "texas_grant", "college", "education", "grant", "need_based"],
        rules(
            "Texas",
            notes="TEXAS Grant: Texas resident; financial need; at least 3/4-time enrollment in bachelor’s program at eligible GATI/HRI; Selective Service and conviction rules; funding limited. No single annual ceiling encoded.",
            verify_notes="Need thresholds, award amounts, and pathways change by FY — verify=true via highered.texas.gov TEXAS Grant guidelines.",
        ),
    )
)
NEW.append(
    scheme(
        "tx-teog",
        "Texas Educational Opportunity Grant (TEOG)",
        "TEOG – टेक्सास सामुदायिक कॉलेज अनुदान",
        "Need-based THECB grant for eligible Texas residents attending public community colleges, state colleges, or technical institutes. Awarded after FAFSA or TASFA through the campus financial-aid office.",
        "Need-based grant aid at eligible Texas two-year / technical public institutions (semester maxima published annually).",
        [
            "FAFSA or TASFA",
            "Texas residency documentation",
            "Enrollment at eligible community/state college or technical institute",
            "Satisfactory academic progress for renewal",
        ],
        "Submit FAFSA or TASFA and contact your college financial-aid office; TEOG is awarded from limited THECB allocations.",
        "https://www.highered.texas.gov/students-families/tasfa/",
        "https://www.highered.texas.gov/student-financial-aid-programs/grant-loan-programs/",
        "Texas Higher Education Coordinating Board (THECB)",
        ["united_states", "texas", "teog", "college", "community_college", "grant", "need_based"],
        rules(
            "Texas",
            notes="TEOG: Texas resident with financial need at eligible public two-year/technical schools; initial/renewal credit-hour and SAP rules; funding limited. No single annual ceiling encoded.",
            verify_notes="Award maxima and eligibility pathways change by FY — verify=true via highered.texas.gov TEOG guidelines.",
        ),
    )
)
NEW.append(
    scheme(
        "tx-homestead-exemption",
        "Texas Residence Homestead Exemption",
        "टेक्सास होमस्टेड छूट",
        "Texas property-tax homestead exemption reduces taxable value of a qualifying principal residence. School districts must provide a large mandatory exemption; counties and other units may offer additional local-option exemptions. Apply with the county appraisal district (Form 50-114).",
        "Reduction in taxable homestead value (mandatory school-district exemption plus any local-option exemptions); may lower annual property taxes.",
        [
            "Form 50-114 Residence Homestead Exemption application",
            "Texas driver’s license or state ID with matching homestead address",
            "Proof of ownership and principal residence",
            "Additional affidavits if heir property / special categories",
        ],
        "File Form 50-114 with the appraisal district in the county where the property is located (general deadline before May 1; late filing rules may apply). Forms: comptroller.texas.gov property-tax forms.",
        "https://comptroller.texas.gov/taxes/property-tax/forms/",
        "https://comptroller.texas.gov/taxes/property-tax/exemptions/",
        "Texas Comptroller of Public Accounts / County Appraisal Districts",
        ["united_states", "texas", "homestead", "property_tax", "housing", "exemption"],
        rules(
            "Texas",
            notes="TX Homestead: own and occupy as principal residence; school-district mandatory exemption amount set in Tax Code (e.g. $140,000 cited on Comptroller page); local-option and age 65+/disabled add-ons may apply. No single income ceiling for the general homestead.",
            verify_notes="Exemption dollar amounts and local options change by statute/local action — verify=true via comptroller.texas.gov exemptions and your CAD.",
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# FLORIDA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "fl-healthy-start",
        "Healthy Start – Florida Department of Health",
        "Healthy Start – फ़्लोरिडा",
        "Florida Healthy Start provides free care coordination and support services for pregnant people and families with infants/young children to improve healthy pregnancy and early childhood outcomes. Local Healthy Start coalitions and county health departments deliver services.",
        "Free prenatal/infant care coordination, education, and referrals (services vary by local coalition).",
        [
            "Pregnancy or infant information",
            "Florida residency / contact information",
            "Prenatal screening form or local referral",
            "Insurance/income information if requested locally",
        ],
        "Contact your local Healthy Start coalition or county Florida Department of Health office via floridahealth.gov Healthy Start pages; complete prenatal screening/referral as directed.",
        "https://www.floridahealth.gov/individual-family-health/child-infant-youth/healthy-start/",
        "https://www.floridahealth.gov/individual-family-health/child-infant-youth/healthy-start/",
        "Florida Department of Health / Healthy Start Coalitions",
        ["united_states", "florida", "healthy_start", "maternal", "infant", "health"],
        rules(
            "Florida",
            notes="Healthy Start: pregnant people and families with young children in Florida; local coalition intake. Generally free; no statewide income ceiling encoded.",
            verify_notes="Local service menus and referral paths vary — verify=true via floridahealth.gov Healthy Start.",
            implies_low_income=False,
        ),
    )
)
NEW.append(
    scheme(
        "fl-homestead-exemption",
        "Florida Homestead Exemption (Property Tax)",
        "फ़्लोरिडा होमस्टेड छूट",
        "Florida homestead exemption can reduce the taxable value of a permanent primary residence (commonly described as up to $50,000 with school/non-school split; inflation adjustments may apply). Apply with your county property appraiser by the published deadline (often March 1). Miami-Dade Property Appraiser .gov portal documented as an official county apply path.",
        "Lower taxable value on a qualifying Florida homestead, reducing annual property taxes; Save Our Homes assessment limits may also apply once homestead is granted.",
        [
            "Homestead application (DR-501 or county online portal)",
            "Proof of ownership as of January 1",
            "Proof of permanent Florida residence (ID, voter registration, etc.)",
            "U.S. citizenship or permanent residency documentation as required",
        ],
        "Apply online or by form with your county property appraiser by the deadline (example .gov path: Miami-Dade Property Appraiser homestead portal). Other counties have their own .gov portals.",
        "https://wwwx.miamidade.gov/pa/exemption/homestead.page",
        "https://wwwx.miamidade.gov/pa/exemption/homestead.page",
        "Florida County Property Appraisers (homestead)",
        ["united_states", "florida", "homestead", "property_tax", "housing", "exemption"],
        rules(
            "Florida",
            notes="FL Homestead: own and occupy as permanent residence on January 1; file by county deadline (commonly March 1). Exemption structure includes base and additional non-school portions; amounts subject to statute/CPI updates. Statewide DOR materials are often on floridarevenue.com (not .gov); county .gov PA portals are the citizen apply path used here.",
            verify_notes="Exemption amounts, CPI adjustments, and county portals — verify=true via your county property appraiser .gov site.",
            implies_low_income=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# NEW YORK
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "ny-empire-state-child-credit",
        "Empire State Child Credit – New York",
        "Empire State Child Credit – न्यूयॉर्क",
        "Refundable New York State Empire State Child Credit for full-year residents with qualifying children under 17. Claimed on Form IT-213 with the NYS income tax return; credit amounts and income phaseouts are published by the Tax Department.",
        "Refundable credit per qualifying child (tax-year amounts published on tax.ny.gov; higher for children under 4).",
        [
            "New York State income tax return",
            "Form IT-213 Claim for Empire State Child Credit",
            "SSN or ITIN for filer and each qualifying child",
            "Proof of full-year NYS residency",
        ],
        "File a full-year NYS return with Form IT-213. See tax.ny.gov Empire State child credit.",
        "https://www.tax.ny.gov/pit/credits/empire_state_child_credit.htm",
        "https://www.tax.ny.gov/pit/credits/empire_state_child_credit.htm",
        "New York State Department of Taxation and Finance",
        ["united_states", "new_york", "empire_state_child_credit", "tax_credit", "child", "income_support"],
        rules(
            "New York",
            notes="ESCC: full-year NYS resident; qualifying child under 17; SSN/ITIN; credit reduced above published AGI thresholds by filing status. Amounts differ for under-4 vs ages 4–16. No single max_annual_income encoded.",
            verify_notes="Credit amounts and phaseouts change by tax year — verify=true via tax.ny.gov Empire State child credit.",
        ),
    )
)
NEW.append(
    scheme(
        "ny-eitc",
        "New York State Earned Income Credit",
        "NYS EITC – न्यूयॉर्क",
        "New York State earned income credit for filers who qualify for the federal EITC (with NYS-specific rules). Generally equals a percentage of the federal credit and is refundable for full-year residents.",
        "Refundable state earned income credit (generally a percentage of federal EITC, reduced by any household credit per Tax Department rules).",
        [
            "New York State income tax return",
            "Form IT-215 Claim for Earned Income Credit",
            "Valid SSN for filer and qualifying children by return due date",
            "Federal EITC qualification documentation",
        ],
        "File a NYS return claiming the earned income credit on Form IT-215 after determining federal EITC eligibility.",
        "https://www.tax.ny.gov/pit/credits/earned_income_credit.htm",
        "https://www.tax.ny.gov/pit/credits/earned_income_credit.htm",
        "New York State Department of Taxation and Finance",
        ["united_states", "new_york", "eitc", "tax_credit", "income_support"],
        rules(
            "New York",
            notes="NYS EITC: generally must qualify for federal EITC; valid SSN rules; refundability differs for full-year vs part-year/nonresident. Credit amount is a published percentage of federal EITC. No standalone ceiling encoded.",
            verify_notes="Percentage of federal EITC and related rules — verify=true via tax.ny.gov earned income credit.",
        ),
    )
)
NEW.append(
    scheme(
        "ny-tap",
        "NYS Tuition Assistance Program (TAP)",
        "TAP – न्यूयॉर्क ट्यूशन सहायता",
        "New York’s Tuition Assistance Program provides need-based tuition grants for eligible residents attending approved NYS colleges. Apply each year via FAFSA/TAP or NYS DREAM Act pathways through HESC.",
        "Annual tuition grant (published range, e.g. about $1,000–$5,665 for recent award years) that does not need to be repaid.",
        [
            "FAFSA and NYS TAP application (or DREAM Act path)",
            "NYS residency documentation (12 continuous months) or DREAM Act eligibility",
            "Enrollment at approved NYS college",
            "Income / dependency status information",
        ],
        "Complete FAFSA then the NYS TAP application at tap.hesc.ny.gov (or DREAM Act path). Deadline published on hesc.ny.gov TAP page.",
        "https://www.tap.hesc.ny.gov/totw/",
        "https://hesc.ny.gov/find-aid/nys-grants-scholarships/tuition-assistance-program-tap",
        "Higher Education Services Corporation (HESC) – New York",
        ["united_states", "new_york", "tap", "college", "education", "grant", "need_based"],
        rules(
            "New York",
            notes="TAP: NYS resident (or DREAM Act); approved NYS college; NTI limits differ by dependency/filing situation (HESC publishes multiple caps); academic standing and enrollment rules. No single ceiling encoded.",
            verify_notes="Award amounts, NTI caps, and deadlines change by academic year — verify=true via hesc.ny.gov TAP.",
        ),
    )
)

# ---------------------------------------------------------------------------
# WASHINGTON
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "wa-working-families-tax-credit",
        "Washington Working Families Tax Credit (WFTC)",
        "WFTC – वाशिंगटन",
        "Refundable Working Families Tax Credit administered by the Washington Department of Revenue for eligible low-to-moderate-income workers who meet federal EITC-related and Washington residency rules. Apply through My DOR / workingfamiliescredit.wa.gov.",
        "Refundable tax credit (maximum published annually; e.g. up to about $1,330 cited for recent tax years) paid to eligible Washington applicants.",
        [
            "Federal tax return / EITC-related information",
            "Washington residency proof (at least 183 days)",
            "SSN or ITIN as required",
            "WFTC application via My DOR or paper form",
        ],
        "Apply at workingfamiliescredit.wa.gov (My DOR, approved software, or paper) during the published application window.",
        "https://workingfamiliescredit.wa.gov/apply",
        "https://workingfamiliescredit.wa.gov/eligibility",
        "Washington State Department of Revenue",
        ["united_states", "washington", "wftc", "tax_credit", "income_support", "eitc"],
        rules(
            "Washington",
            notes="WFTC: generally meet federal EITC requirements, WA residency ≥183 days, file federal return, and meet income/other DOR rules. Credit max and income limits published annually. No permanent ceiling encoded.",
            verify_notes="Eligibility and award tables change by tax year — verify=true via workingfamiliescredit.wa.gov.",
        ),
    )
)
NEW.append(
    scheme(
        "wa-college-bound",
        "Washington College Bound Scholarship",
        "College Bound – वाशिंगटन",
        "Early-commitment Washington College Bound Scholarship for income-eligible students who enroll in middle school, meet pledge/graduation requirements, and complete FAFSA or WASFA annually. Administered by the Washington Student Achievement Council (WSAC).",
        "State aid that helps cover tuition at public rates, eligible fees, and a small book allowance when combined with other aid (details on wsac.wa.gov).",
        [
            "College Bound enrollment / pledge completion",
            "FAFSA or WASFA each year",
            "Washington high school graduation or WA GED",
            "Income / foster-care eligibility documentation as required",
        ],
        "Eligible students enroll via College Bound timelines on wsac.wa.gov; renew by filing FAFSA/WASFA and meeting pledge requirements.",
        "https://wsac.wa.gov/college-bound",
        "https://wsac.wa.gov/college-bound",
        "Washington Student Achievement Council (WSAC)",
        ["united_states", "washington", "college_bound", "college", "scholarship", "education"],
        rules(
            "Washington",
            notes="College Bound: early enrollment by income/foster status; graduate from WA school/GED; enroll in college within one year; income at or below published MFI percentage (e.g. 65% MFI cited in WSAC FAQs); FAFSA/WASFA annually. No single ceiling encoded.",
            verify_notes="Income MFI thresholds and award coordination change — verify=true via wsac.wa.gov College Bound.",
        ),
    )
)
NEW.append(
    scheme(
        "wa-college-grant",
        "Washington College Grant (WA Grant)",
        "Washington College Grant – वाशिंगटन",
        "Washington’s primary need-based college grant for eligible residents attending participating Washington institutions. Students are considered after FAFSA or WASFA; awards coordinate with College Bound and other aid.",
        "Need-based grant aid toward tuition and related costs at participating Washington colleges (award charts published by WSAC).",
        [
            "FAFSA or WASFA",
            "Washington residency documentation",
            "Enrollment at participating institution",
            "Satisfactory academic progress",
        ],
        "Complete FAFSA or WASFA; WSAC and your financial-aid office determine Washington College Grant eligibility from published award charts.",
        "https://wsac.wa.gov/wcg",
        "https://wsac.wa.gov/wcg",
        "Washington Student Achievement Council (WSAC)",
        ["united_states", "washington", "college_grant", "college", "grant", "need_based", "education"],
        rules(
            "Washington",
            notes="WA College Grant: Washington resident; financial need per WSAC MFI/award charts; attending participating school. No single annual ceiling encoded.",
            verify_notes="Award charts and MFI bands change by academic year — verify=true via wsac.wa.gov WCG.",
        ),
    )
)

# ---------------------------------------------------------------------------
# ILLINOIS
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "il-eitc",
        "Illinois Earned Income Tax Credit (EITC)",
        "Illinois EITC – इलिनॉय",
        "Illinois state earned income tax credit claimed on the Illinois income tax return. Eligibility and credit computation follow Illinois Department of Revenue rules aligned with federal EITC concepts (including expanded age paths published for recent years).",
        "Refundable or partially refundable state EITC per IDOR tables for the tax year (amount depends on income and qualifying children).",
        [
            "Illinois income tax return",
            "Federal EITC / income documentation",
            "SSN or ITIN as required by IDOR",
            "Qualifying child information if claiming with children",
        ],
        "File an Illinois return claiming the state EITC per tax.illinois.gov EITC instructions for the tax year.",
        "https://tax.illinois.gov/programs/eitc.html",
        "https://tax.illinois.gov/programs/eitc.html",
        "Illinois Department of Revenue",
        ["united_states", "illinois", "eitc", "tax_credit", "income_support"],
        rules(
            "Illinois",
            notes="IL EITC: meet IDOR eligibility for the tax year (often tied to federal EITC concepts; Illinois may allow additional age paths). Credit rate/amount published annually. No permanent ceiling encoded.",
            verify_notes="Credit percentage, income limits, and age rules change — verify=true via tax.illinois.gov EITC.",
        ),
    )
)
NEW.append(
    scheme(
        "il-map",
        "Illinois Monetary Award Program (MAP)",
        "MAP Grant – इलिनॉय",
        "Illinois MAP is a need-based undergraduate grant paid to eligible Illinois colleges for eligible Illinois residents. Students are considered after FAFSA or the Alternative Application for Illinois Financial Aid; ISAC administers awards (student portal is isac.org — official program listing on illinois.gov GATA/CSFA).",
        "Need-based grant for tuition and mandatory fees at approved Illinois institutions (award depends on need and funding).",
        [
            "FAFSA or Alternative Application for Illinois Financial Aid",
            "Illinois residency documentation",
            "Enrollment at MAP-approved Illinois institution",
            "Satisfactory academic progress",
        ],
        "Submit FAFSA (studentaid.gov) or the Illinois Alternative Application as directed; your college and ISAC determine MAP eligibility.",
        "https://studentaid.gov/h/apply-for-aid/fafsa",
        "https://omb.illinois.gov/PUBLIC/GATA/CSFA/Program.aspx?csfa=1381",
        "Illinois Student Assistance Commission (ISAC) / Illinois GATA CSFA",
        ["united_states", "illinois", "map", "college", "grant", "need_based", "education"],
        rules(
            "Illinois",
            notes="MAP: Illinois resident undergraduate at approved Illinois school; financial need; FAFSA/Alternative Application; funding limited. No single annual ceiling encoded.",
            verify_notes="Award formula and deadlines change — verify=true via illinois.gov CSFA MAP listing and ISAC guidance.",
        ),
    )
)

# ---------------------------------------------------------------------------
# PENNSYLVANIA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "pa-property-tax-rent-rebate",
        "Pennsylvania Property Tax / Rent Rebate (PTRR)",
        "PTRR – पेंसिल्वेनिया संपत्ति कर/किराया रिबेट",
        "Pennsylvania Property Tax/Rent Rebate helps eligible older adults, widows/widowers, and adults with disabilities with a rebate on property taxes or rent. Administered by the Department of Revenue via myPATH / Form PA-1000.",
        "Annual rebate on eligible property taxes or rent (maximum rebate published by Revenue for the claim year).",
        [
            "Form PA-1000 Property Tax/Rent Rebate claim",
            "Proof of age, widow/widower status, or disability as applicable",
            "Property tax or rent payment proof",
            "Income documentation for eligibility income",
        ],
        "Apply via myPATH or Form PA-1000 on pa.gov PTRR pages by the published claim deadline.",
        "https://www.pa.gov/services/revenue/apply-for-property-tax-or-rent-rebate",
        "https://www.pa.gov/agencies/revenue/ptrr",
        "Pennsylvania Department of Revenue",
        ["united_states", "pennsylvania", "ptrr", "property_tax", "rent_rebate", "senior", "housing"],
        rules(
            "Pennsylvania",
            notes="PTRR: age 65+, widow/widower 50+, or 18+ with disability; PA residency; eligibility income within published tiers; property tax or rent paid. Rebate maxima differ for owners vs renters. No single ceiling encoded.",
            verify_notes="Income tiers, rebate maxima, and deadlines change — verify=true via pa.gov PTRR.",
            min_age=18,
        ),
    )
)
NEW.append(
    scheme(
        "pa-tax-forgiveness",
        "Pennsylvania Tax Forgiveness (Schedule SP)",
        "PA Tax Forgiveness – पेंसिल्वेनिया",
        "Pennsylvania Tax Forgiveness can reduce or eliminate PA personal income tax for eligible low- and moderate-income filers. Claimed on PA-40 Schedule SP with the PA-40 return.",
        "Forgiveness of all or part of PA income tax liability based on eligibility income, filing status, and dependents (percentage from Schedule SP).",
        [
            "PA-40 Personal Income Tax return",
            "Schedule SP Tax Forgiveness",
            "Eligibility income documentation (may include nontaxable income)",
            "Dependent information if applicable",
        ],
        "File PA-40 with Schedule SP per Department of Revenue Tax Forgiveness instructions on pa.gov.",
        "https://www.pa.gov/agencies/revenue/resources/tax-types-and-information/personal-income-tax/tax-forgiveness",
        "https://www.pa.gov/agencies/revenue/resources/tax-types-and-information/personal-income-tax/tax-forgiveness",
        "Pennsylvania Department of Revenue",
        ["united_states", "pennsylvania", "tax_forgiveness", "tax_credit", "income_support"],
        rules(
            "Pennsylvania",
            notes="Tax Forgiveness: PA filers whose eligibility income is within Schedule SP tables by filing status and dependents. Eligibility income can include items beyond taxable income. No single ceiling encoded.",
            verify_notes="Schedule SP tables change by tax year — verify=true via pa.gov Tax Forgiveness.",
        ),
    )
)
NEW.append(
    scheme(
        "pa-whole-home-repairs",
        "Pennsylvania Whole-Home Repairs Program",
        "Whole-Home Repairs – पेंसिल्वेनिया",
        "Pennsylvania Whole-Home Repairs Program helps eligible homeowners with safety, habitability, accessibility, and efficiency repairs (grants administered locally; funding limited). Apply through the county/agency on DCED’s agency list.",
        "Locally administered repair grants (guidelines cite up to about $50,000 per unit when funds allow) for eligible owner-occupied homes.",
        [
            "Proof of homeownership and occupancy",
            "Income documentation (commonly ≤80% AMI locally)",
            "Scope of needed repairs",
            "Application via county administering agency",
        ],
        "Find your county agency on dced.pa.gov Whole-Home Repairs agency list and apply locally while funding remains.",
        "https://dced.pa.gov/whole-home-repairs-program-agency-list/",
        "https://dced.pa.gov/programs/covid-19-arpa-whole-home-repairs-program/",
        "Pennsylvania Department of Community & Economic Development (DCED)",
        ["united_states", "pennsylvania", "whole_home_repairs", "housing", "home_repair", "grant"],
        rules(
            "Pennsylvania",
            notes="Whole-Home Repairs: owner-occupied; income generally at or below ~80% AMI per program guidelines; local agency intake; funding limited/ARPA-era. No single statewide ceiling encoded.",
            verify_notes="Local funding status and income rules — verify=true via dced.pa.gov Whole-Home Repairs pages.",
        ),
    )
)

# ---------------------------------------------------------------------------
# OHIO
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "oh-ocog",
        "Ohio College Opportunity Grant (OCOG)",
        "OCOG – ओहायो",
        "Need-based Ohio College Opportunity Grant for eligible Ohio residents pursuing an associate, first bachelor’s, or nurse diploma at eligible institutions. No separate OCOG application — complete the FAFSA.",
        "Need-based grant toward remaining tuition/fees after Pell at eligible Ohio schools (maxima vary by school type; published by ODHE).",
        [
            "FAFSA",
            "Ohio residency documentation",
            "Enrollment in eligible undergraduate/nursing diploma program",
            "Satisfactory academic progress",
        ],
        "Submit FAFSA by the ODHE-published deadline (commonly October 1); your financial-aid office awards OCOG if eligible and funded.",
        "https://studentaid.gov/h/apply-for-aid/fafsa",
        "https://highered.ohio.gov/students/pay-for-college/ohio-grants-scholarships/ocog",
        "Ohio Department of Higher Education",
        ["united_states", "ohio", "ocog", "college", "grant", "need_based", "education"],
        rules(
            "Ohio",
            notes="OCOG: Ohio resident; SAI and household income within published caps (ODHE cites SAI ≤ $3,750 and household income ≤ $96,000 on program page); eligible program/school types; SAP. Community-college path limited to listed exceptions. No single ceiling encoded as permanent field.",
            verify_notes="SAI/income caps and award charts change — verify=true via highered.ohio.gov OCOG.",
        ),
    )
)
NEW.append(
    scheme(
        "oh-homestead-exemption",
        "Ohio Homestead Exemption (Property Tax)",
        "ओहायो होमस्टेड छूट",
        "Ohio homestead exemption reduces property taxes for eligible low-income seniors, permanently and totally disabled homeowners, certain surviving spouses, and enhanced categories for disabled veterans / public-service surviving spouses. Apply with the county auditor (DTE forms).",
        "Property tax credit shielding a published amount of home market value from taxation (inflation-adjusted reduction amounts on tax.ohio.gov).",
        [
            "DTE 105A (or 105I/105K for special categories)",
            "Proof of age 65+, disability certification, or surviving-spouse status",
            "Ownership and principal-residence proof",
            "MAGI / income documentation when means-tested",
        ],
        "File the applicable DTE homestead form with your county auditor by December 31 of the tax year (manufactured-home timing differs). See tax.ohio.gov homestead FAQ.",
        "https://tax.ohio.gov/help-center/faqs/real-property-tax-homestead-means-testing/real-property-tax--homestead-means-testing",
        "https://tax.ohio.gov/help-center/faqs/real-property-tax-homestead-means-testing/real-property-tax--homestead-means-testing",
        "Ohio Department of Taxation / County Auditors",
        ["united_states", "ohio", "homestead", "property_tax", "senior", "disability", "housing"],
        rules(
            "Ohio",
            notes="OH Homestead: age 65+ or permanently/totally disabled (or listed surviving-spouse/veteran paths); own & occupy as principal residence; means-tested MAGI threshold for most applicants (enhanced veteran/public-service paths may have no income test). Reduction amounts inflation-adjusted. No permanent ceiling encoded.",
            verify_notes="MAGI thresholds and reduction amounts update — verify=true via tax.ohio.gov homestead FAQ.",
            min_age=65,
        ),
    )
)

# ---------------------------------------------------------------------------
# MICHIGAN
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "mi-homestead-property-tax-credit",
        "Michigan Homestead Property Tax Credit",
        "Michigan Homestead Credit – मिशिगन",
        "Michigan Homestead Property Tax Credit helps eligible homeowners and renters with a credit related to property taxes or rent. Claimed on the Michigan income tax return when household resources are within the published annual limit.",
        "Refundable or tax-reducing credit based on property taxes/rent and household resources (tables on michigan.gov).",
        [
            "Michigan income tax return with homestead credit claim",
            "Property tax bill or rent documentation",
            "Household resources / income documentation",
            "Michigan residency / homestead information",
        ],
        "Claim the Homestead Property Tax Credit on your Michigan return per michigan.gov HPTC guidance for the tax year.",
        "https://www.michigan.gov/taxes/iit/tax-guidance/credits-exemptions/hptc",
        "https://www.michigan.gov/taxes/iit/tax-guidance/credits-exemptions/hptc",
        "Michigan Department of Treasury",
        ["united_states", "michigan", "homestead", "property_tax", "rent", "tax_credit"],
        rules(
            "Michigan",
            notes="MI HPTC: Michigan homeowner or renter; household resources within published annual limit (Treasury cites limits such as ~$71,500 for recent years); taxable-value caps may apply for homeowners. No permanent ceiling encoded.",
            verify_notes="Household resource limits and taxable-value caps change — verify=true via michigan.gov HPTC.",
        ),
    )
)
NEW.append(
    scheme(
        "mi-tuition-incentive-program",
        "Michigan Tuition Incentive Program (TIP)",
        "TIP – मिशिगन ट्यूशन प्रोत्साहन",
        "Michigan TIP provides college tuition assistance for eligible students identified through Medicaid coverage history who complete the FAFSA and meet enrollment/academic rules. Phase I supports certificate/associate pathways; Phase II can help toward a bachelor’s.",
        "Tuition incentive aid for eligible Medicaid-linked students at participating Michigan colleges (Phase I/II benefits per MI Student Aid).",
        [
            "FAFSA",
            "TIP eligibility tied to Medicaid coverage history",
            "Enrollment at eligible Michigan institution",
            "Academic progress / Phase requirements",
        ],
        "Eligible students apply via FAFSA and follow MI Student Aid TIP checklists on michigan.gov/mistudentaid.",
        "https://www.michigan.gov/mistudentaid/programs/tuition-incentive-program",
        "https://www.michigan.gov/mistudentaid/programs/tuition-incentive-program",
        "Michigan Student Aid / Treasury",
        ["united_states", "michigan", "tip", "college", "tuition", "education", "medicaid_linked"],
        rules(
            "Michigan",
            notes="TIP: Medicaid coverage for required months within a lookback window; Michigan resident; FAFSA; Phase I/II academic and enrollment rules. No separate income ceiling encoded beyond Medicaid-linked eligibility.",
            verify_notes="Medicaid month requirements and Phase benefits — verify=true via michigan.gov TIP.",
        ),
    )
)

# ---------------------------------------------------------------------------
# MASSACHUSETTS
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "ma-eitc",
        "Massachusetts Earned Income Tax Credit (EITC)",
        "Massachusetts EITC – मैसाचुसेट्स",
        "Massachusetts refundable EITC equal to a published percentage of the federal EITC (mass.gov cites 40% for tax years beginning 2023). Claimed on the Massachusetts personal income tax return by eligible residents.",
        "Refundable state EITC equal to the published percentage of federal EITC for qualifying Massachusetts filers.",
        [
            "Massachusetts income tax return",
            "Federal EITC qualification",
            "SSN/ITIN documentation as required",
            "Residency information (part-year rules apply)",
        ],
        "File a Massachusetts return claiming the state EITC per mass.gov EITC instructions.",
        "https://www.mass.gov/info-details/massachusetts-earned-income-tax-credit-eitc",
        "https://www.mass.gov/info-details/massachusetts-earned-income-tax-credit-eitc",
        "Massachusetts Department of Revenue",
        ["united_states", "massachusetts", "eitc", "tax_credit", "income_support"],
        rules(
            "Massachusetts",
            notes="MA EITC: generally qualify for federal EITC; Massachusetts resident for at least part of the year (full-year nonresidents ineligible). Credit = published % of federal EITC. No separate ceiling encoded.",
            verify_notes="Percentage of federal EITC and residency rules — verify=true via mass.gov EITC.",
        ),
    )
)
NEW.append(
    scheme(
        "ma-massgrant",
        "MASSGrant / MASSGrant Plus – Massachusetts",
        "MASSGrant – मैसाचुसेट्स",
        "Need-based MASSGrant and MASSGrant Plus help eligible Massachusetts undergraduates pay for college. Students generally complete FAFSA or MASFA by published deadlines; OSFA/DHE administers awards.",
        "Need-based grant aid for eligible Massachusetts undergraduates (Pell-linked and Plus pathways per mass.gov guidelines).",
        [
            "FAFSA or Massachusetts Application for State Financial Aid (MASFA)",
            "Massachusetts residency documentation",
            "Enrollment at eligible institution",
            "Satisfactory academic progress",
        ],
        "Submit FAFSA or MASFA by the OSFA deadline; your financial-aid office and OSFA determine MASSGrant eligibility.",
        "https://studentaid.gov/h/apply-for-aid/fafsa",
        "https://www.mass.gov/info-details/massgrant-massgrant-plus",
        "Massachusetts Office of Student Financial Assistance / DHE",
        ["united_states", "massachusetts", "massgrant", "college", "grant", "need_based", "education"],
        rules(
            "Massachusetts",
            notes="MASSGrant: Massachusetts resident undergraduate; financial need (often Pell-linked; MASFA SAI caps for alternative path); eligible school; funding limited. No single ceiling encoded.",
            verify_notes="Deadlines, Pell/Plus rules, and award amounts — verify=true via mass.gov MASSGrant.",
        ),
    )
)
NEW.append(
    scheme(
        "ma-mrvp",
        "Massachusetts Rental Voucher Program (MRVP)",
        "MRVP – मैसाचुसेट्स किराया वाउचर",
        "MRVP provides mobile or project-based rental vouchers for eligible low-income Massachusetts households. Apply through CHAMP (Common Housing Application for Massachusetts Programs).",
        "Rental subsidy so eligible households generally pay about 30% of income toward rent (subject to program rules and unit availability).",
        [
            "CHAMP housing application",
            "Income documentation (commonly ≤80% AMI)",
            "Household composition / identity",
            "Massachusetts residency / local preference documents as required",
        ],
        "Apply via CHAMP following mass.gov MRVP how-to instructions; waitlists and local housing authority rules apply.",
        "https://www.mass.gov/how-to/apply-for-the-massachusetts-rental-voucher-program-mrvp",
        "https://www.mass.gov/how-to/apply-for-the-massachusetts-rental-voucher-program-mrvp",
        "Massachusetts Executive Office of Housing and Livable Communities / local housing agencies",
        ["united_states", "massachusetts", "mrvp", "housing", "rental", "voucher"],
        rules(
            "Massachusetts",
            notes="MRVP: low-income household (commonly ≤80% AMI); Massachusetts; CHAMP application; voucher availability limited. No single statewide income dollar ceiling encoded.",
            verify_notes="AMI limits, waitlists, and mobile vs project-based rules — verify=true via mass.gov MRVP.",
        ),
    )
)

# ---------------------------------------------------------------------------
# NEW JERSEY
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "nj-eitc",
        "New Jersey Earned Income Tax Credit (NJEITC)",
        "NJEITC – न्यू जर्सी",
        "Refundable New Jersey EITC for eligible low-to-moderate-income residents, calculated as a published percentage of the federal EITC (Taxation cites 40% for recent years). Claimed on the NJ-1040.",
        "Refundable state EITC equal to the published percentage of federal EITC for qualifying NJ residents (including certain childless adults age 18+ per NJ rules).",
        [
            "NJ-1040 Resident Income Tax Return",
            "Federal return / EITC computation",
            "SSN/ITIN as required",
            "Residency documentation",
        ],
        "File NJ-1040 claiming NJEITC per nj.gov Taxation EITC pages.",
        "https://nj.gov/treasury/taxation/eitc/eitcinfo.shtml",
        "https://nj.gov/treasury/taxation/eitc/eitcinfo.shtml",
        "New Jersey Division of Taxation",
        ["united_states", "new_jersey", "eitc", "njeitc", "tax_credit", "income_support"],
        rules(
            "New Jersey",
            notes="NJEITC: generally based on federal EITC; NJ allows certain expansions (e.g. age 18+ without dependents per Taxation guidance); claim on NJ-1040. Percentage published annually. No permanent ceiling encoded.",
            verify_notes="Percentage of federal EITC and age rules — verify=true via nj.gov Taxation EITC.",
        ),
    )
)
NEW.append(
    scheme(
        "nj-srap",
        "New Jersey State Rental Assistance Program (SRAP)",
        "SRAP – न्यू जर्सी किराया सहायता",
        "NJ DCA State Rental Assistance Program provides rental subsidies for eligible very-low-income New Jersey households. Applications open periodically through lottery/waitlist announcements on the DCA SRAP page.",
        "Monthly rental subsidy for selected eligible households (subject to waitlist openings and funding).",
        [
            "SRAP waitlist / lottery application when open",
            "Income documentation (very low income)",
            "Household composition and NJ residency",
            "Citizenship/eligible immigration status as required",
        ],
        "Monitor nj.gov DCA SRAP page for waitlist openings and apply during announced lottery periods.",
        "https://www.nj.gov/dca/dhcr/offices/srap.shtml",
        "https://www.nj.gov/dca/dhcr/offices/srap.shtml",
        "New Jersey Department of Community Affairs (DCA)",
        ["united_states", "new_jersey", "srap", "housing", "rental", "assistance"],
        rules(
            "New Jersey",
            notes="SRAP: very-low-income NJ households; waitlist/lottery when DCA opens intake; preference categories may apply. No permanent income ceiling encoded.",
            verify_notes="Waitlist status and income limits — verify=true via nj.gov DCA SRAP.",
        ),
    )
)

# ---------------------------------------------------------------------------
# VIRGINIA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "va-low-income-credit",
        "Virginia EITC / Credit for Low-Income Individuals",
        "Virginia Low-Income Credit – वर्जीनिया",
        "Virginia offers a Credit for Low-Income Individuals and a Virginia Earned Income Tax Credit option for eligible lower-income taxpayers. Claimed on the Virginia income tax return per Virginia Tax instructions (refundability rules published by tax year).",
        "State income tax credit for eligible low-income Virginians (either low-income credit amount per exemption or Virginia EITC equal to a published % of federal EITC — taxpayer chooses per instructions).",
        [
            "Virginia income tax return",
            "Federal EITC / income documentation",
            "Exemption / dependent information",
            "Residency documentation",
        ],
        "File a Virginia return claiming the low-income credit or Virginia EITC per tax.virginia.gov instructions for the tax year.",
        "https://www.tax.virginia.gov/low-income-individuals-credit",
        "https://www.tax.virginia.gov/low-income-individuals-credit",
        "Virginia Tax",
        ["united_states", "virginia", "eitc", "low_income_credit", "tax_credit", "income_support"],
        rules(
            "Virginia",
            notes="VA low-income credit / EITC: eligibility and refundability follow Virginia Tax published rules for the tax year (EITC % of federal; alternate per-exemption credit). No permanent ceiling encoded.",
            verify_notes="Credit amounts, EITC %, and refundability — verify=true via tax.virginia.gov low-income credit.",
        ),
    )
)

# ---------------------------------------------------------------------------
# NORTH CAROLINA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "nc-homestead-property-tax-relief",
        "North Carolina Homestead / Property Tax Relief (AV-9)",
        "NC Homestead Tax Relief – नॉर्थ कैरोलिना",
        "North Carolina property tax relief programs for qualifying elderly, disabled, or disabled-veteran homeowners (homestead exclusion, disability exclusion, circuit breaker, etc.). File Form AV-9 with the county assessor by the published deadline.",
        "Property tax exclusion or deferral reducing the tax burden on a qualifying primary residence (program type depends on age/disability/income path).",
        [
            "Form AV-9 Application for Property Tax Relief",
            "Proof of age, disability, or disabled-veteran status as applicable",
            "Income documentation for means-tested paths",
            "Ownership and occupancy proof",
        ],
        "File AV-9 with your county assessor by the deadline (commonly June 1). Form and instructions: ncdor.gov AV-9 pages.",
        "https://www.ncdor.gov/av-9-2026-application-property-tax-relief",
        "https://www.ncdor.gov/av-9-2026-application-property-tax-relief",
        "North Carolina Department of Revenue / County Assessors",
        ["united_states", "north_carolina", "homestead", "property_tax", "senior", "disability"],
        rules(
            "North Carolina",
            notes="NC AV-9 relief: qualifying elderly/disabled/disabled-veteran homeowners; income and assessment rules differ by exclusion vs circuit-breaker path; file with county assessor. No single ceiling encoded.",
            verify_notes="Income limits, exclusion amounts, and deadlines — verify=true via ncdor.gov AV-9 and county assessor.",
            min_age=65,
        ),
    )
)

# ---------------------------------------------------------------------------
# MARYLAND
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "md-eitc",
        "Maryland Earned Income Tax Credit",
        "Maryland EITC – मैरीलैंड",
        "Maryland Earned Income Tax Credit for eligible filers, including pathways for federal EITC recipients and certain ITIN / young-adult expansions published by the Comptroller. Claimed on the Maryland return; use the Comptroller EITC screener tools.",
        "State EITC benefit per Comptroller tables for the tax year (may include refundable components).",
        [
            "Maryland income tax return",
            "Federal EITC / income information",
            "SSN or ITIN as allowed",
            "Residency documentation",
        ],
        "File a Maryland return claiming EITC; optionally use interactive2.marylandtaxes.gov EITC screener first.",
        "https://interactive2.marylandtaxes.gov/EITCScreener",
        "https://marylandcomptroller.gov/individuals/eitc.html",
        "Maryland Comptroller",
        ["united_states", "maryland", "eitc", "tax_credit", "income_support"],
        rules(
            "Maryland",
            notes="MD EITC: eligibility per Comptroller guidance for the tax year (federal EITC link plus Maryland expansions). No permanent ceiling encoded.",
            verify_notes="Credit amounts and expansion rules change — verify=true via marylandcomptroller.gov EITC.",
        ),
    )
)
NEW.append(
    scheme(
        "md-guaranteed-access-grant",
        "Maryland Guaranteed Access (GA) Grant – Howard P. Rawlings",
        "Maryland GA Grant – मैरीलैंड",
        "Need-based Howard P. Rawlings Guaranteed Access Grant for eligible Maryland undergraduates with significant financial need. Administered by MHEC; students complete FAFSA or MHEC One-App and create an MDCAPS account.",
        "Need-based grant toward college costs at eligible Maryland institutions (award maxima published by MHEC for the aid year).",
        [
            "FAFSA or MHEC One-App by published deadline",
            "MDCAPS account and requested documents",
            "Maryland residency documentation",
            "Enrollment at eligible Maryland institution",
        ],
        "Submit FAFSA/One-App by MHEC deadline, create MDCAPS account, and submit documents as requested on mhec.maryland.gov GA Grant pages.",
        "https://mhec.maryland.gov/preparing/pages/financialaid/programdescriptions/prog_gagrant.aspx",
        "https://mhec.maryland.gov/preparing/pages/financialaid/programdescriptions/prog_gagrant.aspx",
        "Maryland Higher Education Commission (MHEC)",
        ["united_states", "maryland", "guaranteed_access_grant", "college", "grant", "need_based"],
        rules(
            "Maryland",
            notes="GA Grant: Maryland resident with significant financial need; FAFSA/One-App + MDCAPS; eligible undergraduate enrollment; funding/document deadlines apply. No single ceiling encoded.",
            verify_notes="Award maxima and deadlines change — verify=true via mhec.maryland.gov GA Grant.",
        ),
    )
)

# ---------------------------------------------------------------------------
# WISCONSIN
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "wi-homestead-credit",
        "Wisconsin Homestead Credit",
        "Wisconsin Homestead Credit – विस्कॉन्सिन",
        "Wisconsin Homestead Credit helps eligible renters and homeowners with a property-tax/rent-related credit claimed on Schedule H or H-EZ with the Wisconsin income tax return (or standalone claim when applicable).",
        "Refundable credit reducing property-tax/rent burden for qualifying households (maximum credit published annually by DOR).",
        [
            "Schedule H or H-EZ Homestead Credit",
            "Rent certificate or property tax bill",
            "Household income documentation",
            "Wisconsin residency / homestead information",
        ],
        "Claim Homestead Credit on your Wisconsin return (or per DOR standalone instructions) using Schedule H/H-EZ. See revenue.wi.gov Homestead Credit FAQs.",
        "https://www.revenue.wi.gov/Pages/FAQS/ise-homestead.aspx",
        "https://www.revenue.wi.gov/Pages/FAQS/ise-homestead.aspx",
        "Wisconsin Department of Revenue",
        ["united_states", "wisconsin", "homestead", "property_tax", "rent", "tax_credit"],
        rules(
            "Wisconsin",
            notes="WI Homestead Credit: household income below published annual limit; age/disability or other qualifying status per Schedule H instructions; rent or property taxes paid. No permanent ceiling encoded.",
            verify_notes="Income limits and max credit change annually — verify=true via revenue.wi.gov Homestead Credit.",
        ),
    )
)

# ---------------------------------------------------------------------------
# MISSOURI
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "mo-property-tax-credit",
        "Missouri Property Tax Credit (Circuit Breaker)",
        "Missouri Property Tax Credit – मिसौरी",
        "Missouri Property Tax Credit helps eligible seniors and 100% disabled residents with a credit for property taxes or rent (Form MO-PTC). Administered by the Department of Revenue.",
        "Annual credit/rebate on property taxes or rent (DOR publishes separate maxima for homeowners vs renters).",
        [
            "Form MO-PTC (or combined return path if filing income tax)",
            "Proof of age 65+ or 100% disability",
            "Property tax receipt or rent documentation",
            "Income documentation",
        ],
        "File Form MO-PTC with required receipts by the published deadline on dor.mo.gov Property Tax Credit pages.",
        "https://dor.mo.gov/taxation/individual/tax-types/property-tax-credit/",
        "https://dor.mo.gov/taxation/individual/tax-types/property-tax-credit/",
        "Missouri Department of Revenue",
        ["united_states", "missouri", "property_tax_credit", "circuit_breaker", "senior", "disability"],
        rules(
            "Missouri",
            notes="MO PTC: age 65+ or 100% disabled; income within published limits; owned/rented Missouri home. Homeowner vs renter maxima differ. No permanent ceiling encoded.",
            verify_notes="Income limits and rebate maxima change — verify=true via dor.mo.gov Property Tax Credit.",
            min_age=65,
        ),
    )
)

# ---------------------------------------------------------------------------
# COLORADO
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "co-eitc",
        "Colorado Earned Income Tax Credit",
        "Colorado EITC – कोलोराडो",
        "Colorado refundable EITC claimed on DR 0104 with Individual Credit Schedule DR 0104CR. Rate is a published percentage of federal EITC (DOR cites higher transitional rates for recent years).",
        "Refundable state EITC equal to the published percentage of federal EITC for eligible Colorado residents (including ITIN pathways per DOR).",
        [
            "Colorado Form DR 0104",
            "DR 0104CR credit schedule (and DR 0104TN if applicable)",
            "Federal EITC computation",
            "Residency documentation",
        ],
        "File Colorado return with DR 0104CR claiming EITC per tax.colorado.gov instructions.",
        "https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit",
        "https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit",
        "Colorado Department of Revenue – Taxation",
        ["united_states", "colorado", "eitc", "tax_credit", "income_support"],
        rules(
            "Colorado",
            notes="CO EITC: generally federal EITC-eligible (plus CO ITIN paths); full- or part-year Colorado resident; credit = published % of federal EITC. No permanent ceiling encoded.",
            verify_notes="Credit percentage by tax year — verify=true via tax.colorado.gov EITC topics.",
        ),
    )
)
NEW.append(
    scheme(
        "co-cof",
        "Colorado College Opportunity Fund (COF) Stipend",
        "COF – कोलोराडो कॉलेज अवसर निधि",
        "College Opportunity Fund provides a per-credit stipend that reduces tuition for eligible undergraduate students at participating Colorado public colleges. Students must create a COF account and authorize their institution.",
        "Per-credit tuition stipend applied by the college after COF authorization (lifetime credit-hour limits apply).",
        [
            "COF account at cdhe.colorado.gov",
            "SSN or student ID as required",
            "Enrollment at participating Colorado public institution",
            "Authorization for the college to apply COF",
        ],
        "Create/authorize a COF account via cdhe.colorado.gov College Opportunity Fund pages before term census.",
        "https://cdhe.colorado.gov/college-opportunity-fund-cof-stipend",
        "https://cdhe.colorado.gov/college-opportunity-fund-cof-stipend",
        "Colorado Department of Higher Education",
        ["united_states", "colorado", "cof", "college", "tuition_stipend", "education"],
        rules(
            "Colorado",
            notes="COF: eligible undergraduate at participating Colorado public college; create COF account and authorize credits; lifetime credit-hour cap. Not a classic need-tested grant — residency/eligibility rules apply.",
            verify_notes="Stipend per credit and lifetime caps — verify=true via cdhe.colorado.gov COF.",
            implies_low_income=False,
        ),
    )
)
NEW.append(
    scheme(
        "co-cera",
        "Colorado Emergency Rental Assistance (CERA)",
        "CERA – कोलोराडो आपातकालीन किराया सहायता",
        "Colorado Emergency Rental Assistance helps income-qualified renters facing housing instability/eviction risk. Administered through the Division of Housing / CARE Center pathways on doh.colorado.gov.",
        "Short-term rental assistance (program materials cite potential aid up to published caps when funds allow) for eligible renter households.",
        [
            "Proof of tenancy / lease",
            "Income documentation",
            "Evidence of housing instability or past-due rent as required",
            "Colorado residency / household information",
        ],
        "Apply through Colorado Division of Housing CERA / CARE Center pathways listed on doh.colorado.gov emergency rental assistance (funding windows vary).",
        "https://doh.colorado.gov/emergency-rental-assistance",
        "https://doh.colorado.gov/emergency-rental-assistance",
        "Colorado Division of Housing",
        ["united_states", "colorado", "cera", "housing", "rental", "emergency"],
        rules(
            "Colorado",
            notes="CERA: income-qualified Colorado renters with housing instability; funding limited and may pause. No permanent statewide ceiling encoded.",
            verify_notes="Funding status and income limits — verify=true via doh.colorado.gov emergency rental assistance.",
        ),
    )
)

# ---------------------------------------------------------------------------
# OREGON
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "or-eitc",
        "Oregon Earned Income Credit",
        "Oregon EIC – ऑरेगन",
        "Oregon refundable earned income credit for eligible workers who qualify for the federal EITC (with a higher percentage if a dependent is under age 3). ITIN filers may use Schedule OR-EIC-ITIN per DOR.",
        "Refundable credit equal to a published percentage of federal EITC (higher rate with a young dependent per DOR).",
        [
            "Oregon income tax return",
            "Federal EITC computation or OR-EIC-ITIN schedule",
            "Dependent age information if claiming enhanced rate",
            "Residency documentation",
        ],
        "File an Oregon return claiming the earned income credit per oregon.gov DOR tax benefits for families.",
        "https://www.oregon.gov/dor/programs/individuals/pages/credits.aspx",
        "https://www.oregon.gov/dor/programs/individuals/pages/credits.aspx",
        "Oregon Department of Revenue",
        ["united_states", "oregon", "eitc", "tax_credit", "income_support"],
        rules(
            "Oregon",
            notes="OR EIC: generally federal EITC-eligible (ITIN path available); credit = published % of federal (enhanced with dependent under 3). No permanent ceiling encoded.",
            verify_notes="Percentages and ITIN schedule rules — verify=true via oregon.gov DOR credits.",
        ),
    )
)
NEW.append(
    scheme(
        "or-opportunity-grant",
        "Oregon Opportunity Grant",
        "Oregon Opportunity Grant – ऑरेगन",
        "Oregon’s primary need-based college grant for eligible residents pursuing a first associate or bachelor’s degree. Students apply through FAFSA or ORSAA; Oregon Student Aid administers awards.",
        "Need-based grant aid at eligible Oregon colleges (award ranges published by Oregon Student Aid for the aid year).",
        [
            "FAFSA or Oregon Student Aid Application (ORSAA)",
            "Oregon residency documentation",
            "Enrollment toward first associate/bachelor’s",
            "Satisfactory academic progress",
        ],
        "Submit FAFSA or ORSAA; check award status via Oregon Student Aid (oregonstudentaid.gov Opportunity Grant).",
        "https://oregonstudentaid.gov/oregon-opportunity-grant.aspx",
        "https://oregonstudentaid.gov/oregon-opportunity-grant.aspx",
        "Office of Student Access and Completion / Oregon Student Aid",
        ["united_states", "oregon", "opportunity_grant", "college", "grant", "need_based"],
        rules(
            "Oregon",
            notes="Oregon Opportunity Grant: Oregon resident; financial need; first associate/bachelor’s; eligible school; funding limited. No single ceiling encoded.",
            verify_notes="Award ranges and deadlines — verify=true via oregonstudentaid.gov Opportunity Grant.",
        ),
    )
)

# ---------------------------------------------------------------------------
# ARIZONA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "az-property-tax-credit",
        "Arizona Property Tax Refund Credit (Form 140PTC)",
        "Arizona Property Tax Credit – एरिज़ोना",
        "Arizona income-tax credit/refund for eligible full-year residents age 65+ or receiving Title 16 SSI who paid property tax or rent and meet low-income limits. Claim Form 140PTC with the Arizona return.",
        "Refundable property-tax/rent credit for qualifying seniors/SSI recipients (amount depends on income and taxes/rent paid per ADOR tables).",
        [
            "Form 140PTC Property Tax Refund Credit claim",
            "Proof of age 65+ or SSI Title 16",
            "Property tax or rent payment proof",
            "Income documentation",
        ],
        "File Form 140PTC with your Arizona return (or per ADOR instructions) by the published deadline.",
        "https://azdor.gov/forms/tax-credits-forms/property-tax-refund-credit-claim-form-fillable",
        "https://azdor.gov/individuals/income-tax-filing-assistance/tax-credits",
        "Arizona Department of Revenue",
        ["united_states", "arizona", "property_tax_credit", "senior", "ssi", "tax_credit"],
        rules(
            "Arizona",
            notes="AZ 140PTC: full-year resident; age 65+ or SSI Title 16; paid AZ property tax or rent; income within published low-income limits. No permanent ceiling encoded.",
            verify_notes="Income limits and credit computation — verify=true via azdor.gov tax credits / 140PTC.",
            min_age=65,
        ),
    )
)

# ---------------------------------------------------------------------------
# NEVADA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "nv-millennium-scholarship",
        "Governor Guinn Millennium Scholarship – Nevada",
        "Millennium Scholarship – नेवादा",
        "Nevada Governor Guinn Millennium Scholarship helps eligible Nevada high-school graduates with per-credit tuition support at eligible Nevada colleges, up to a lifetime maximum published by the State Treasurer / NVigate.",
        "Per-credit tuition payments toward eligible Nevada institutions (lifetime maximum published, commonly cited around $10,000).",
        [
            "Nevada high school graduation / eligibility certification",
            "Enrollment at eligible Nevada institution",
            "GPA and credit-load requirements for continued eligibility",
            "NVigate / Treasurer program acknowledgment as required",
        ],
        "Eligible graduates are notified/certified through Nevada processes; activate and maintain eligibility via NVigate / institution steps on nvigate.gov Millennium Scholarship pages.",
        "https://nvigate.gov/programs/governor-guinn-millennium-scholarship/",
        "https://nvigate.gov/programs/governor-guinn-millennium-scholarship/",
        "Nevada State Treasurer / NVigate",
        ["united_states", "nevada", "millennium_scholarship", "college", "scholarship", "education"],
        rules(
            "Nevada",
            notes="Millennium Scholarship: eligible Nevada graduate; GPA/curriculum and enrollment rules; per-credit payments with lifetime cap. Merit-based with residency — not classic need-tested. No income ceiling encoded.",
            verify_notes="Per-credit rates, GPA, and lifetime max — verify=true via nvigate.gov / Treasurer GGMS.",
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# GEORGIA (us-ga-*)
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "us-ga-hope",
        "Georgia HOPE Scholarship / HOPE Grant",
        "Georgia HOPE – जॉर्जिया",
        "Georgia HOPE Scholarship and HOPE Grant programs help eligible Georgia students pay for college or certificate/diploma programs at eligible institutions. Administered by the Georgia Student Finance Commission (gsfc.georgia.gov).",
        "Tuition assistance at eligible Georgia postsecondary institutions for HOPE Scholarship (degree) or HOPE Grant (certificate/diploma) pathways meeting academic rules.",
        [
            "FAFSA or Georgia state aid application path as directed by GSFC",
            "Georgia residency / citizenship documentation",
            "GPA / academic eligibility records",
            "Enrollment at eligible Georgia institution",
        ],
        "Create/manage aid via GSFC HOPE pages on gsfc.georgia.gov; complete FAFSA if required by your pathway and institution.",
        "https://gsfc.georgia.gov/hope",
        "https://gsfc.georgia.gov/hope",
        "Georgia Student Finance Commission (GSFC)",
        ["united_states", "georgia", "hope", "college", "scholarship", "grant", "education"],
        rules(
            "Georgia",
            notes="HOPE Scholarship/Grant: Georgia resident; academic GPA and program rules differ for Scholarship vs Grant; eligible institutions; funding/Zell Miller variants exist. No single income ceiling for classic HOPE Scholarship.",
            verify_notes="GPA, award amounts, and Zell Miller rules — verify=true via gsfc.georgia.gov HOPE.",
            implies_low_income=False,
        ),
    )
)
NEW.append(
    scheme(
        "us-ga-homestead",
        "Georgia Homestead Exemption",
        "Georgia Homestead – जॉर्जिया",
        "Georgia homestead exemption reduces the assessed value of a qualifying primary residence for property tax. Apply with the local county tax official by the published deadline (georgia.gov how-to).",
        "Lower assessed value for a qualifying Georgia homestead, reducing property taxes (local option exemptions may add senior/disabled benefits).",
        [
            "County homestead exemption application",
            "Proof of ownership and occupancy as of January 1",
            "Georgia residency / ID",
            "Age or disability documentation for enhanced local exemptions",
        ],
        "Apply with your county tax commissioner/assessor by the local deadline (commonly April 1) following georgia.gov homestead how-to.",
        "https://georgia.gov/apply-homestead-exemption",
        "https://georgia.gov/apply-homestead-exemption",
        "Georgia county tax officials / Georgia.gov",
        ["united_states", "georgia", "homestead", "property_tax", "housing", "exemption"],
        rules(
            "Georgia",
            notes="GA Homestead: own and occupy as primary residence on January 1; file with county by deadline. Base and local-option senior/disabled exemptions vary by county. No statewide income ceiling for the standard homestead.",
            verify_notes="Local exemption amounts and deadlines — verify=true via georgia.gov and your county tax office.",
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# TENNESSEE (us-tn-*)
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "us-tn-property-tax-relief",
        "Tennessee Property Tax Relief",
        "Tennessee Property Tax Relief – टेनेसी",
        "Tennessee Property Tax Relief assists qualifying low-income elderly or disabled homeowners and disabled veterans with property tax relief. Apply through the county trustee or city collecting official per Comptroller guidance.",
        "Property tax relief payment/credit for qualifying homeowners (income and category rules published by the Comptroller).",
        [
            "Local property tax relief application",
            "Proof of age, disability, or disabled-veteran status",
            "Income documentation",
            "Ownership and homestead proof",
        ],
        "Apply with your county trustee or city collecting official by the local deadline (Comptroller notes applications often due shortly after the delinquency date). See comptroller.tn.gov tax relief.",
        "https://comptroller.tn.gov/office-functions/pa/property-taxes/property-tax-programs/tax-relief.html",
        "https://comptroller.tn.gov/office-functions/pa/property-taxes/property-tax-programs/tax-relief.html",
        "Tennessee Comptroller of the Treasury / County Trustees",
        ["united_states", "tennessee", "property_tax_relief", "senior", "disability", "veteran", "housing"],
        rules(
            "Tennessee",
            notes="TN Property Tax Relief: low-income elderly or disabled homeowners and disabled veterans; income ceilings published by Comptroller; apply locally. No permanent ceiling encoded.",
            verify_notes="Income limits and deadlines — verify=true via comptroller.tn.gov property tax relief.",
            min_age=65,
        ),
    )
)
NEW.append(
    scheme(
        "us-tn-hope-scholarship",
        "Tennessee HOPE Scholarship (Education Lottery Scholarship)",
        "Tennessee HOPE – टेनेसी",
        "Tennessee HOPE / Education Lottery Scholarship helps eligible Tennessee students attend approved in-state postsecondary institutions. Students generally complete the FAFSA and meet academic criteria; THEC/TSAC administer pathways described on tn.gov.",
        "Lottery-funded scholarship toward tuition at eligible Tennessee institutions (award amounts and renewal GPA rules published by THEC/TSAC).",
        [
            "FAFSA",
            "Tennessee residency / high school academic records",
            "ACT/SAT or GPA documentation as required",
            "Enrollment at eligible Tennessee institution",
        ],
        "Complete FAFSA and follow THEC/TSAC financial-aid steps on tn.gov THEC students & families financial aid pages; monitor the TSAC student portal as directed.",
        "https://www.tn.gov/thec/students-families/financial-aid.html",
        "https://www.tn.gov/thec/students-families/financial-aid.html",
        "Tennessee Higher Education Commission / TSAC",
        ["united_states", "tennessee", "hope", "lottery_scholarship", "college", "scholarship", "education"],
        rules(
            "Tennessee",
            notes="TN HOPE: Tennessee resident; academic eligibility (GPA and/or test scores); FAFSA; renewal GPA checkpoints; time limits after initial enrollment. Merit/lottery-based — no classic need ceiling encoded.",
            verify_notes="Award amounts and academic rules — verify=true via tn.gov THEC/TSAC financial aid.",
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# INDIANA (us-in-*)
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "us-in-21st-century-scholars",
        "Indiana 21st Century Scholars",
        "21st Century Scholars – इंडियाना",
        "Indiana 21st Century Scholars provides up to four years of tuition support at eligible Indiana colleges for students who enroll in 7th/8th grade (or are auto-enrolled via free/reduced lunch) and complete Scholar Success requirements. Apply/confirm via ScholarTrack.",
        "Tuition and regularly assessed fees at eligible Indiana colleges for scholars who meet high-school pledge, FAFSA, and college continuation rules.",
        [
            "ScholarTrack parent/student accounts",
            "7th/8th-grade enrollment or auto-enrollment confirmation",
            "Income documentation if applying outside auto-enrollment",
            "Annual FAFSA beginning senior year / college",
        ],
        "Parents apply or confirm auto-enrollment in ScholarTrack (scholartrack.che.in.gov) by June 30 of 8th grade when required; students complete Scholar Success Program activities.",
        "https://scholartrack.che.in.gov/",
        "https://scholars.in.gov/parents/enroll/",
        "Indiana Commission for Higher Education / 21st Century Scholars",
        ["united_states", "indiana", "21st_century_scholars", "college", "scholarship", "education"],
        rules(
            "Indiana",
            notes="21st Century Scholars: Indiana 7th/8th graders; income guidelines aligned to free/reduced lunch (or foster/guardianship exceptions); complete pledge & Scholar Success; FAFSA; college SAP. Enrollment window is middle school. No permanent dollar ceiling encoded.",
            verify_notes="Income chart and Scholar Success requirements — verify=true via scholars.in.gov / ScholarTrack.",
        ),
    )
)
NEW.append(
    scheme(
        "us-in-eitc",
        "Indiana Earned Income Credit",
        "Indiana EIC – इंडियाना",
        "Indiana earned income credit for eligible taxpayers, generally those who qualify for the federal EITC. Claimed on the Indiana individual income tax return with Schedule IN-EIC.",
        "State earned income credit computed from federal EITC per Indiana DOR Publication EIC / Schedule IN-EIC for the tax year.",
        [
            "Indiana income tax return",
            "Schedule IN-EIC",
            "Federal EITC computation",
            "SSN documentation as required",
        ],
        "File an Indiana return claiming the earned income credit per in.gov DOR tax credits guidance.",
        "https://www.in.gov/dor/i-am-a/individual/tax-credits/",
        "https://www.in.gov/dor/i-am-a/individual/tax-credits/",
        "Indiana Department of Revenue",
        ["united_states", "indiana", "eitc", "tax_credit", "income_support"],
        rules(
            "Indiana",
            notes="IN EIC: generally federal EITC-qualified; claim on Indiana return with Schedule IN-EIC. Credit computation published annually. No permanent ceiling encoded.",
            verify_notes="Schedule IN-EIC and Publication EIC — verify=true via in.gov DOR.",
        ),
    )
)

# ---------------------------------------------------------------------------
# KENTUCKY
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "ky-homestead-exemption",
        "Kentucky Homestead Exemption",
        "Kentucky Homestead – केंटकी",
        "Kentucky homestead exemption reduces the taxable assessed value of a qualifying primary residence for homeowners age 65+ or totally disabled and receiving disability payments. Apply with the local Property Valuation Administrator (form 62A350).",
        "Reduction in taxable assessed value by the published homestead exemption amount for the tax period (DOR announces the amount periodically).",
        [
            "Homestead/Disability exemption application (62A350)",
            "Proof of age 65+ or total disability with disability payments",
            "Ownership and occupancy as of January 1",
            "File with county PVA",
        ],
        "Submit the homestead application to your county PVA by December 31 per revenue.ky.gov Homestead Exemption guidance.",
        "https://revenue.ky.gov/Property/Residential-Farm-Commercial-Property/Pages/Homestead-Exemption.aspx",
        "https://revenue.ky.gov/Property/Residential-Farm-Commercial-Property/Pages/Homestead-Exemption.aspx",
        "Kentucky Department of Revenue / County PVAs",
        ["united_states", "kentucky", "homestead", "property_tax", "senior", "disability"],
        rules(
            "Kentucky",
            notes="KY Homestead: age 65+ or totally disabled receiving disability payments; own & occupy as personal residence on January 1; one exemption per household. Exemption dollar amount set periodically by DOR. No income ceiling for the standard homestead.",
            verify_notes="Exemption amount and disability documentation — verify=true via revenue.ky.gov Homestead Exemption.",
            min_age=65,
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# SOUTH CAROLINA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "sc-need-based-grant",
        "South Carolina Need-based Grant",
        "SC Need-based Grant – साउथ कैरोलिना",
        "South Carolina Need-based Grant provides additional aid for eligible SC residents with the greatest financial need at eligible public institutions. Students complete the FAFSA; campus financial-aid offices award limited funds.",
        "Need-based grant (CHE cites up to about $3,500 full-time / $1,750 part-time annually when funds allow) toward cost of attendance after other gift aid.",
        [
            "FAFSA",
            "South Carolina residency documentation",
            "Enrollment at eligible public SC institution",
            "Satisfactory academic progress",
        ],
        "Submit FAFSA; contact your public college financial-aid office. Program overview: che.sc.gov scholarships and grants for SC residents.",
        "https://studentaid.gov/h/apply-for-aid/fafsa",
        "https://www.che.sc.gov/index.php/students-families-and-military/scholarships-and-grants-sc-residents",
        "South Carolina Commission on Higher Education / campus aid offices",
        ["united_states", "south_carolina", "need_based_grant", "college", "grant", "education"],
        rules(
            "South Carolina",
            notes="SC Need-based Grant: SC resident; financial need; eligible public institution; FAFSA; term limits. Award amounts subject to funding. No single ceiling encoded.",
            verify_notes="Award maxima and residency rules — verify=true via che.sc.gov scholarships/grants page.",
        ),
    )
)
NEW.append(
    scheme(
        "sc-homestead-exemption",
        "South Carolina Homestead Exemption",
        "SC Homestead – साउथ कैरोलिना",
        "South Carolina homestead exemption provides property-tax relief for qualifying homeowners age 65+, totally and permanently disabled, or legally blind. Apply through the county auditor.",
        "Property tax exemption/relief on a qualifying primary residence for eligible seniors, disabled, or legally blind homeowners.",
        [
            "County homestead exemption application",
            "Proof of age 65+, total permanent disability, or legal blindness",
            "Ownership and occupancy documentation",
            "File with county auditor",
        ],
        "Apply with your county auditor. See dor.sc.gov property tax resources / homestead materials.",
        "https://dor.sc.gov/tax/property",
        "https://dor.sc.gov/tax/property",
        "South Carolina Department of Revenue / County Auditors",
        ["united_states", "south_carolina", "homestead", "property_tax", "senior", "disability"],
        rules(
            "South Carolina",
            notes="SC Homestead: age 65+, totally and permanently disabled, or legally blind; primary residence; apply via county auditor. No general income ceiling for the basic homestead path.",
            verify_notes="Local application timing and documentation — verify=true via dor.sc.gov property tax and county auditor.",
            min_age=65,
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# ALABAMA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "al-homestead-exemption",
        "Alabama Homestead Exemptions",
        "Alabama Homestead – अलाबामा",
        "Alabama homestead exemptions reduce state and/or local property taxes on a qualifying primary residence. Age 65+ and other categories may receive expanded exemptions; apply through the county tax assessing official.",
        "Property tax exemption on a qualifying Alabama homestead (state and local components differ by age/income/disability category).",
        [
            "County homestead exemption application",
            "Proof of ownership and principal residence",
            "Age 65+ or other qualifying category documentation",
            "Income documentation when required for local full exemption",
        ],
        "Apply with your county tax assessor/collecting official per revenue.alabama.gov homestead exemption guidance.",
        "https://www.revenue.alabama.gov/property-tax/homestead-exemptions/",
        "https://www.revenue.alabama.gov/property-tax/homestead-exemptions/",
        "Alabama Department of Revenue / County assessing officials",
        ["united_states", "alabama", "homestead", "property_tax", "senior", "housing"],
        rules(
            "Alabama",
            notes="AL Homestead: principal residence; categories include under-65 limited exemption and age 65+/disabled expanded paths; some local full exemptions are income-conditioned. No single statewide ceiling encoded.",
            verify_notes="Category rules and local income tests — verify=true via revenue.alabama.gov homestead exemptions.",
            implies_low_income=False,
        ),
    )
)
NEW.append(
    scheme(
        "al-weatherization",
        "Alabama Weatherization Assistance Program",
        "Alabama Weatherization – अलाबामा",
        "Alabama Weatherization Assistance Program improves energy efficiency and home health/safety for income-eligible households. ADECA contracts local community action agencies; applicants contact the agency serving their county.",
        "No-cost or low-cost weatherization measures (insulation, air sealing, health/safety fixes) based on an energy audit for eligible homes.",
        [
            "Income documentation (at or below published % of poverty)",
            "Proof of ownership or landlord permission if renter",
            "Utility / energy information",
            "Application via local Community Action Agency",
        ],
        "Contact the weatherization agency for your county listed on adeca.alabama.gov Weatherization Assistance Program (ADECA does not process applications directly).",
        "https://adeca.alabama.gov/weatherization/",
        "https://adeca.alabama.gov/weatherization/",
        "Alabama Department of Economic and Community Affairs (ADECA)",
        ["united_states", "alabama", "weatherization", "energy", "housing", "wap"],
        rules(
            "Alabama",
            notes="AL WAP: household income at or below published poverty percentage (ADECA cites 200% FPL); priority for elderly, disabled, families with children; local CAA intake. No single dollar ceiling encoded.",
            verify_notes="Income % FPL and local agency contacts — verify=true via adeca.alabama.gov weatherization.",
        ),
    )
)

# ---------------------------------------------------------------------------
# OKLAHOMA
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "ok-homestead-exemption",
        "Oklahoma Homestead / Property Tax Exemptions",
        "Oklahoma Homestead – ओक्लाहोमा",
        "Oklahoma homestead exemption and related property-tax exemptions reduce taxable assessed value for qualifying owner-occupied homes. Additional low-income and disabled-veteran exemptions may apply. File OTC forms with the county assessor.",
        "Reduction in assessed value / property tax for a qualifying Oklahoma homestead (standard plus any additional exemptions).",
        [
            "OTC homestead exemption application (e.g. Form 921 / related forms)",
            "Proof of ownership and occupancy on January 1",
            "Income documentation for additional low-income exemption if claimed",
            "Disabled-veteran documentation if applicable",
        ],
        "File with your county assessor by the published deadline (often March 15) using forms linked from oklahoma.gov Tax exemptions pages.",
        "https://oklahoma.gov/tax/individuals/exemptions.html",
        "https://oklahoma.gov/tax/individuals/exemptions.html",
        "Oklahoma Tax Commission / County Assessors",
        ["united_states", "oklahoma", "homestead", "property_tax", "housing", "exemption"],
        rules(
            "Oklahoma",
            notes="OK Homestead: own & occupy on January 1; standard homestead plus optional additional exemption when household income is at or below published limit; separate disabled-veteran paths. No permanent single ceiling encoded.",
            verify_notes="Form numbers, income add-on limits, and deadlines — verify=true via oklahoma.gov tax exemptions and county assessor.",
            implies_low_income=False,
        ),
    )
)

# ---------------------------------------------------------------------------
# UTAH
# ---------------------------------------------------------------------------
NEW.append(
    scheme(
        "ut-homeowner-renter-relief",
        "Utah Homeowner’s or Renter’s Relief (Circuit Breaker)",
        "Utah Circuit Breaker – यूटा",
        "Utah circuit-breaker relief helps qualifying seniors, widows/widowers, and certain disabled or hardship applicants with property-tax or renter credit relief. Homeowners apply via county (TC-90H); renters apply to the Tax Commission (TC-90CB).",
        "Property tax credit or renter relief for qualifying households (income limits and credit amounts published annually).",
        [
            "TC-90H (homeowner) or TC-90CB (renter) application",
            "Proof of age, widow/widower, disability, or hardship status",
            "Income documentation for household",
            "Ownership/occupancy or rent proof",
        ],
        "Homeowners: file TC-90H with the county by the published deadline. Renters: file TC-90CB with the Tax Commission. See tax.utah.gov homeowner/renter relief.",
        "https://tax.utah.gov/relief/homeowner-renter-relief/",
        "https://tax.utah.gov/relief/homeowner-renter-relief/",
        "Utah State Tax Commission / Counties",
        ["united_states", "utah", "circuit_breaker", "property_tax", "renter_relief", "senior"],
        rules(
            "Utah",
            notes="UT circuit breaker: qualifying status categories; household income below published annual limit; homeowner vs renter forms and deadlines differ. No permanent ceiling encoded.",
            verify_notes="Income limits, deadlines, and form versions — verify=true via tax.utah.gov homeowner/renter relief.",
            min_age=65,
        ),
    )
)


def _host_is_gov(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return host.endswith(".gov")


def main() -> None:
    assert len(NEW) >= 20, len(NEW)
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

    # Collision guard: never overwrite India-looking short prefixes accidentally
    india_collide = [s["id"] for s in NEW if s["id"].startswith(("tn-", "in-", "ga-", "ar-", "la-", "mn-")) and not s["id"].startswith(("us-tn-", "us-in-", "us-ga-", "us-ar-", "us-la-", "us-mn-"))]
    assert not india_collide, india_collide

    dups = [s["id"] for s in NEW if s["id"] in existing]
    if dups:
        print(f"skip already-present ids ({len(dups)}): {dups}")
        NEW[:] = [s for s in NEW if s["id"] not in existing]

    if NEW:
        schemes.extend(NEW)

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    count = len(schemes)
    wave_note = (
        "US big-states distinctive deepen (2026-09-24): Tier A/B large-state packs — state EITC/child credits, "
        "need-based college grants, homestead/property-tax relief, housing/energy distinctive programs for "
        "CA/TX/FL/NY/WA/IL/PA/OH/MI/MA/NJ/VA/NC/MD/WI/MO/CO/OR/AZ/NV/GA/TN/IN/KY/SC/AL/OK/UT "
        "(GA/TN/IN new ids use us-ga-*/us-tn-*/us-in-*). Official .gov only; last_verified 2026-09-24; "
        "nationwide:false; quality over forced count; honest SKIP where no clear .gov distinctive path."
    )
    for mp in (META, FE_META):
        meta = json.loads(mp.read_text())
        meta["scheme_count"] = count
        meta["updated_as_of"] = LAST
        meta["updated_as_of_iso"] = "2026-09-24T06:45:00+05:30"
        scope = meta.get("scope", "")
        if "US big-states distinctive deepen (2026-09-24)" not in scope:
            meta["scope"] = scope.rstrip(".") + "; " + wave_note
        mp.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")

    print(f"Added {len(NEW)} schemes; total {count}")
    by: dict[str, list[str]] = {}
    for s in NEW:
        st = s["eligibility_rules"]["states"][0]
        by.setdefault(st, []).append(s["id"])
    for st, ids in sorted(by.items()):
        print(f"  {st}: {ids}")


if __name__ == "__main__":
    main()
