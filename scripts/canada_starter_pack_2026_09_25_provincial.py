"""Provincial / territorial rows for the Canada starter pack — part 2 of 2.

Sources: CRA provincial-territorial program pages (canada.ca) for programs CRA
administers, plus official provincial/territorial government sites.
"""
from __future__ import annotations


def add_provincial() -> None:
    add_west()
    add_prairies_atlantic()
    add_north_central()


def add_west() -> None:
    from canada_starter_pack_2026_09_25_rows import (  # noqa: PLC0415
        AB, ALL_INCOMES, BC, CRA_PROV, SIN_DOCS, P, rules,
    )

    P(
        "can-ab-child-family-benefit",
        "Alberta Child and Family Benefit (ACFB)",
        "Tax-free quarterly payment for lower- and middle-income Alberta families with children under 18, with an extra working component.",
        "July 2026 – June 2027 base component: C$1,529 for the first child and C$764 each for the 2nd–4th child; working component (family working income over C$2,760): C$782 / C$712 / C$426 / C$141 for 1–4 children. Paid in August, November, February and May.",
        SIN_DOCS,
        "No separate application: apply for the Canada Child Benefit and file tax returns — CRA pays the ACFB for Alberta.",
        "https://www.alberta.ca/alberta-child-and-family-benefit",
        CRA_PROV + "province-alberta.html",
        "Government of Alberta (administered by CRA)",
        ["children", "cash", "low-income", "middle-class"],
        rules(
            provinces=[AB],
            notes="Alberta resident eligible for the CCB with children under 18. Base component reduced when AFNI exceeds C$28,116 (partial between C$28,116 and C$47,115); working component reduced above C$47,115.",
            verify_notes="Zero-out depends on number of children — max_annual_income null; phase-out reaches middle incomes so implies_low_income false.",
        ),
    )
    P(
        "can-ab-seniors-benefit",
        "Alberta Seniors Benefit",
        "Monthly income-tested payment for low-income Alberta seniors receiving OAS.",
        "Monthly amount depends on income, marital status and housing; guideline income limits from July 1, 2026: C$32,690 single, C$53,800 couple (combined).",
        ["Social Insurance Number (SIN)", "Proof of Alberta residence", "Tax returns (you and spouse)"],
        "Apply online or by mail (Seniors Financial Assistance application); you may be enrolled automatically when you turn 65.",
        "https://www.alberta.ca/alberta-seniors-benefit",
        "https://www.alberta.ca/alberta-seniors-benefit",
        "Government of Alberta (Seniors, Community and Social Services)",
        ["elderly", "pension", "income_support", "low-income"],
        rules(
            provinces=[AB], min_age=65, max_annual_income=53800,
            notes="65 or older; lived in Alberta at least 3 months immediately before applying; Canadian citizen or permanent resident; receiving OAS (if eligible); annual income within guidelines (C$32,690 single / C$53,800 couple).",
            verify_notes="max_annual_income encodes the couple guideline (C$53,800); single C$32,690 in notes.",
        ),
    )
    P(
        "can-ab-aish",
        "Assured Income for the Severely Handicapped (AISH)",
        "Alberta monthly living allowance plus health benefits for adults with a severe, permanent disability that prevents them from earning a living.",
        "Monthly living allowance, health benefits (prescriptions, dental, optical) and possible personal benefits; amounts set by Alberta regulations.",
        ["Medical report on the disability", "Proof of income and assets", "Social Insurance Number (SIN)", "Proof of Alberta residence and status in Canada"],
        "Apply online or on paper through Alberta Supports (AISH), with the medical report completed by a health professional.",
        "https://www.alberta.ca/aish",
        "https://www.alberta.ca/aish",
        "Government of Alberta (Assisted Living and Social Services)",
        ["disability", "income_support", "health", "low-income"],
        rules(
            provinces=[AB], min_age=18, disability_required=True, implies_low_income=True,
            notes="18 or older and not eligible for OAS; severe and permanent disability that is the main factor limiting your ability to earn a living; Alberta resident; Canadian citizen or permanent resident; meet AISH income and asset limits.",
            verify_notes="Income and asset limits not encoded — catalogue Canada soft gate (C$58,523, heuristic) via implies_low_income. Confirm current living allowance and asset limit on alberta.ca.",
        ),
    )
    P(
        "can-bc-family-benefit",
        "BC Family Benefit",
        "Tax-free monthly payment for low- and middle-income BC families with children under 18.",
        "July 2026 – June 2027 maximum per month: C$145.83 for the first child (plus C$41.66 single-parent supplement), C$91.66 for the second child, C$75 for each additional child; floor amounts (C$64.58 / C$62.50 / C$60.41) apply for AFNI between C$30,176 and C$96,562.",
        SIN_DOCS,
        "No separate application: apply for the Canada Child Benefit and file tax returns — CRA pays it for BC.",
        "https://www2.gov.bc.ca/gov/content/family-social-supports/affordability/family-benefit",
        CRA_PROV + "province-british-columbia.html",
        "Government of British Columbia (administered by CRA)",
        ["children", "cash", "low-income", "middle-class"],
        rules(
            provinces=[BC],
            notes="BC resident eligible for the CCB. Reduced by 4% of AFNI over C$30,176 down to the floor amounts; reduced by a further 4% of AFNI over C$96,562.",
            verify_notes="Phase-out reaches middle/upper-middle incomes and depends on children — max_annual_income null, implies_low_income false.",
        ),
    )
    P(
        "can-bc-renters-tax-credit",
        "BC renter's tax credit",
        "Refundable BC income tax credit for low- and moderate-income renters.",
        "Up to C$400 a year (claimed on your BC tax return).",
        ["Rental details (address, landlord, months rented)", "Social Insurance Number (SIN)"],
        "Claim on Form BC479 with your tax return.",
        "https://www2.gov.bc.ca/gov/content/taxes/income-taxes/personal/credits/renters-tax-credit",
        "https://www2.gov.bc.ca/gov/content/taxes/income-taxes/personal/credits/renters-tax-credit",
        "Government of British Columbia (Ministry of Finance; claimed through CRA)",
        ["housing", "tax_credit", "low-income", "middle-class"],
        rules(
            provinces=[BC], min_age=19, max_annual_income=86189,
            notes="BC resident on December 31; 19 or older (or have a spouse/partner or are a parent living with your child); rented an eligible home in BC for at least 6 months of the year. 2026 tax year: reduced when adjusted income exceeds C$66,189; no credit at C$86,189 or more.",
            verify_notes="Official 2026 zero-out C$86,189 encoded. gov.bc.ca banner notes pages are not updated during an election period — reconfirm afterwards.",
        ),
    )
    P(
        "can-bc-seniors-supplement",
        "BC Senior's Supplement",
        "Automatic monthly BC top-up for low-income seniors receiving OAS and the Guaranteed Income Supplement (or the federal Allowance).",
        "Up to C$99.30 per month for a single senior, up to C$220.50 for a senior couple, up to C$99.83 for a spouse receiving the federal Allowance.",
        ["None — paid automatically based on OAS/GIS"],
        "No application: payment starts automatically one month after your first OAS/GIS payment if you qualify.",
        "https://www2.gov.bc.ca/gov/content/family-social-supports/seniors/financial-legal-matters/income-security-programs/seniors-supplement",
        "https://www2.gov.bc.ca/gov/content/family-social-supports/seniors/financial-legal-matters/income-security-programs/seniors-supplement",
        "Government of British Columbia (Ministry of Social Development and Poverty Reduction)",
        ["elderly", "pension", "income_support", "low-income"],
        rules(
            provinces=[BC], min_age=60, implies_low_income=True,
            notes="Permanent BC resident receiving OAS and GIS (65+) with no other significant taxable income, or aged 60–64 receiving the federal Allowance. Automatic.",
            verify_notes="Tied to GIS/Allowance (income-tested) — no separate income figure; catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-bc-training-education-savings-grant",
        "BC Training and Education Savings Grant (BCTESG)",
        "One-time C$1,200 BC grant deposited into a child's RESP — no contribution required.",
        "C$1,200 per eligible child, paid into an RESP.",
        ["Child's SIN", "Parent/guardian's SIN", "RESP with a participating provider"],
        "Ask a participating RESP provider to apply between the child's 6th birthday and the day before their 9th birthday.",
        "https://www2.gov.bc.ca/gov/content/education-training/k-12/support/scholarships/bc-training-and-education-savings-grant",
        "https://www2.gov.bc.ca/gov/content/education-training/k-12/support/scholarships/bc-training-and-education-savings-grant",
        "Government of British Columbia (Ministry of Education and Child Care)",
        ["children", "education", "savings", "grant"] + ALL_INCOMES,
        rules(
            provinces=[BC],
            notes="Child born in 2006 or later; child and parent/guardian are BC residents with valid SINs at the time of application; apply between the child's 6th birthday and the day before the 9th birthday. Not income-tested.",
            verify_notes="Universal: max_annual_income null. Age window refers to the child (not encoded as applicant age). The canada.ca RESP page (2026) also lists the BCTESG.",
        ),
    )


def add_prairies_atlantic() -> None:
    from canada_starter_pack_2026_09_25_rows import (  # noqa: PLC0415
        CRA_PROV, MB, NB, NL, NS, PE, SIN_DOCS, SK, P, rules,
    )

    P(
        "can-mb-55-plus",
        "55 PLUS — A Manitoba Income Supplement",
        "Quarterly income supplement for lower-income Manitobans aged 55 and older.",
        "Up to C$161.80 per quarter for a single person and up to C$173.90 per eligible person in a couple.",
        ["Manitoba Health registration number", "Income information (tax return / notice of assessment)", "Social Insurance Number (SIN)"],
        "People receiving GIS or the federal Allowance are assessed automatically; others (junior component) apply to Manitoba Families by form.",
        "https://www.gov.mb.ca/fs/eia/55plus.html",
        "https://www.gov.mb.ca/fs/eia/55plus.html",
        "Government of Manitoba (Manitoba Families)",
        ["elderly", "income_support", "low-income"],
        rules(
            provinces=[MB], min_age=55, implies_low_income=True,
            notes="55 or older; Manitoba resident with a Manitoba Health number; low income. Senior component: GIS / Allowance recipients. Junior component (55–64): income up to about C$9,746.40 single or C$16,255.20 couple.",
            verify_notes="Income limits vary by component — catalogue Canada soft gate (C$58,523) via implies_low_income; junior limits in notes.",
        ),
    )
    P(
        "can-mb-rent-assist",
        "Manitoba Rent Assist (non-EIA)",
        "Monthly shelter benefit for low-income Manitoba renters in private, unsubsidized housing who are not on Employment and Income Assistance.",
        "Monthly amount depends on household income, size and rent (calculated by Manitoba Families).",
        ["Rental agreement / proof of rent", "Income information for all household members", "Manitoba Health number"],
        "Apply online or by form to Manitoba Families (Rent Assist).",
        "https://www.gov.mb.ca/fs/eia/rent_assist.html",
        "https://www.gov.mb.ca/fs/eia/non_rentassist_facts.html",
        "Government of Manitoba (Manitoba Families)",
        ["housing", "rent", "low-income"],
        rules(
            provinces=[MB], min_age=18, max_annual_income=60768,
            notes="18 or older; Canadian citizen or permanent resident; renting in the private market without other rent subsidy; not receiving EIA. Net household income under the limit: single C$29,120 (C$33,920 if 55+ or with DTC/CPP-D); 2 people C$38,720; 3–4 people C$50,240; 5+ C$60,768.",
            verify_notes="max_annual_income encodes the highest official limit (5+ people, C$60,768).",
        ),
    )
    P(
        "can-mb-child-benefit",
        "Manitoba Child Benefit",
        "Monthly help for low-income Manitoba families with children who are not on Employment and Income Assistance.",
        "Up to C$35 a month (C$420 a year) per child.",
        ["Proof of CCB eligibility", "Income information (notice of assessment)", "Manitoba Health number"],
        "Apply by mail to Manitoba Families using the Manitoba Child Benefit application.",
        "https://www.gov.mb.ca/fs/eia/mcb.html",
        "https://www.gov.mb.ca/fs/eia/mcb.html",
        "Government of Manitoba (Manitoba Families)",
        ["children", "cash", "low-income"],
        rules(
            provinces=[MB], implies_low_income=True,
            notes="Manitoba resident receiving the Canada Child Benefit and not receiving EIA; low family income (Manitoba's example: full benefit at about C$15,000, partial up to about C$20,000 — limits rise with family size).",
            verify_notes="Official page gives examples rather than a table — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-nb-child-tax-benefit",
        "New Brunswick Child Tax Benefit (with Working Income Supplement and School Supplement)",
        "Monthly payment for low-income New Brunswick families with children, plus a working income supplement and a yearly school supplement.",
        "Basic benefit C$20.83/month per child; Working Income Supplement up to C$20.83/month per family (phased in above C$3,750 of family earned income); School Supplement C$100 per child (paid in July) if AFNI is C$20,000 or less.",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for New Brunswick.",
        CRA_PROV + "province-new-brunswick.html",
        CRA_PROV + "province-new-brunswick.html",
        "Government of New Brunswick (administered by CRA)",
        ["children", "cash", "low-income"],
        rules(
            provinces=[NB], implies_low_income=True,
            notes="New Brunswick resident eligible for the CCB. Basic benefit reduced when AFNI exceeds C$20,000; WIS partial between AFNI C$20,921 and C$25,921.",
            verify_notes="Zero-out depends on number of children — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-nb-hst-credit",
        "New Brunswick Harmonized Sales Tax Credit",
        "Tax-free quarterly credit (paid with the CGEB) for low-income New Brunswick individuals and families.",
        "Up to C$300 for an individual, C$300 for a spouse/partner and C$100 per child under 19 (C$300 for the first child in a single-parent family).",
        SIN_DOCS,
        "No separate application: file your tax return — CRA pays it with the Canada Groceries and Essentials Benefit.",
        CRA_PROV + "province-new-brunswick.html",
        CRA_PROV + "province-new-brunswick.html",
        "Government of New Brunswick (administered by CRA)",
        ["cash", "tax_credit", "low-income"],
        rules(
            provinces=[NB], implies_low_income=True,
            notes="New Brunswick resident eligible for the CGEB. Reduced by 2% of AFNI over C$35,000.",
            verify_notes="Zero-out depends on family size — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-nb-low-income-seniors-benefit",
        "New Brunswick Low-Income Seniors' Benefit",
        "Annual payment for low-income New Brunswick seniors receiving GIS or the federal Allowance.",
        "C$629 for 2026 (one benefit per couple living together).",
        ["Proof of GIS / Allowance / Allowance for the Survivor received in 2025", "Social Insurance Number (SIN)"],
        "Apply to the Government of New Brunswick online or by form by December 31, 2026.",
        "https://www2.gnb.ca/content/gnb/en/corporate/promo/new-brunswick-low-income-seniors-benefit.html",
        "https://www2.gnb.ca/content/gnb/en/corporate/promo/new-brunswick-low-income-seniors-benefit.html",
        "Government of New Brunswick (Department of Finance and Treasury Board)",
        ["elderly", "cash", "low-income"],
        rules(
            provinces=[NB], min_age=60, implies_low_income=True,
            notes="New Brunswick resident on December 31, 2025 who received GIS (65+) or the Allowance / Allowance for the Survivor (60–64) in 2025. Apply by December 31, 2026.",
            verify_notes="Tied to GIS/Allowance (income-tested) — catalogue Canada soft gate via implies_low_income.",
        ),
    )
    P(
        "can-nl-child-benefit",
        "Newfoundland and Labrador Child Benefit (with Early Childhood Nutrition Supplement)",
        "Monthly payment for low-income NL families with children, plus a nutrition supplement for children under 5.",
        "Per month: C$157.33 (first child), C$166.83 (second), C$179.16 (third), C$192.50 (each additional). Early Childhood Nutrition Supplement: up to C$150/month per child under 5, depending on income.",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for Newfoundland and Labrador.",
        CRA_PROV + "province-newfoundland-labrador.html",
        CRA_PROV + "province-newfoundland-labrador.html",
        "Government of Newfoundland and Labrador (administered by CRA)",
        ["children", "cash", "nutrition", "low-income"],
        rules(
            provinces=[NL], implies_low_income=True,
            notes="NL resident eligible for the CCB; partial benefit when AFNI is above C$20,397.",
            verify_notes="Zero-out depends on number of children — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-nl-income-supplement",
        "Newfoundland and Labrador Income Supplement",
        "Tax-free quarterly payment for low-income NL individuals, families and persons with disabilities.",
        "Up to C$520 for an individual, C$589 for a couple, plus C$231 per child; disability amount C$231 for each DTC-eligible family member.",
        SIN_DOCS,
        "No separate application: file your tax return — CRA pays it with the CGEB.",
        CRA_PROV + "province-newfoundland-labrador.html",
        CRA_PROV + "province-newfoundland-labrador.html",
        "Government of Newfoundland and Labrador (administered by CRA)",
        ["cash", "income_support", "low-income", "disability"],
        rules(
            provinces=[NL], implies_low_income=True,
            notes="NL resident eligible for the CGEB; amount based on family situation and AFNI.",
            verify_notes="Income thresholds not encoded — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-nl-seniors-benefit",
        "Newfoundland and Labrador Seniors' Benefit",
        "Tax-free annual benefit (paid quarterly) for low-income NL seniors.",
        "Up to C$1,882 per year (July 2026 – June 2027).",
        SIN_DOCS,
        "No separate application: file your tax return — CRA pays it with the CGEB.",
        CRA_PROV + "province-newfoundland-labrador.html",
        CRA_PROV + "province-newfoundland-labrador.html",
        "Government of Newfoundland and Labrador (administered by CRA)",
        ["elderly", "cash", "low-income"],
        rules(
            provinces=[NL], min_age=64, max_annual_income=46549,
            notes="NL resident aged 64 or older on December 31, 2025 (or spouse/partner is). Full amount at AFNI C$30,409 or less; partial between C$30,409 and C$46,549.",
            verify_notes="Official upper income C$46,549 encoded.",
        ),
    )
    P(
        "can-nl-disability-benefit",
        "Newfoundland and Labrador Disability Benefit",
        "Monthly provincial payment for working-age NL residents approved for the disability tax credit.",
        "Up to C$400 per month.",
        ["Approved disability tax credit", "Filed tax returns"],
        "Automatic for eligible people who file tax returns and have an approved DTC.",
        CRA_PROV + "province-newfoundland-labrador.html",
        CRA_PROV + "province-newfoundland-labrador.html",
        "Government of Newfoundland and Labrador (administered by CRA)",
        ["disability", "cash", "low-income"],
        rules(
            provinces=[NL], min_age=18, max_age=64, disability_required=True, max_annual_income=55404,
            notes="NL resident aged 18–64 with a valid disability tax credit; full benefit at AFNI below C$29,402; no benefit at C$42,404 or more for an individual (C$55,404 when both spouses qualify).",
            verify_notes="max_annual_income encodes the higher official limit (both spouses eligible); individual limit C$42,404 in notes.",
        ),
    )
    P(
        "can-ns-child-benefit",
        "Nova Scotia Child Benefit",
        "Monthly payment for low-income Nova Scotia families with children under 18.",
        "Up to C$127.08 per month per child (July 2026 – June 2027).",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for Nova Scotia.",
        CRA_PROV + "province-nova-scotia.html",
        CRA_PROV + "province-nova-scotia.html",
        "Government of Nova Scotia (administered by CRA)",
        ["children", "cash", "low-income"],
        rules(
            provinces=[NS], max_annual_income=34000,
            notes="Nova Scotia resident eligible for the CCB; full amount below AFNI C$26,000; partial between C$26,000 and C$34,000.",
            verify_notes="Official upper income C$34,000 encoded.",
        ),
    )
    P(
        "can-ns-affordable-living-tax-credit",
        "Nova Scotia Affordable Living Tax Credit",
        "Tax-free quarterly credit (paid with the CGEB) for low-income Nova Scotia individuals and families.",
        "Up to C$255 per individual or couple plus C$60 per child (July 2026 – June 2027).",
        SIN_DOCS,
        "No separate application: file your tax return — CRA pays it with the CGEB.",
        CRA_PROV + "province-nova-scotia.html",
        CRA_PROV + "province-nova-scotia.html",
        "Government of Nova Scotia (administered by CRA)",
        ["cash", "tax_credit", "low-income"],
        rules(
            provinces=[NS], implies_low_income=True,
            notes="Nova Scotia resident eligible for the CGEB; reduced by 5% of AFNI over C$30,000.",
            verify_notes="Zero-out depends on family size — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-ns-poverty-reduction-credit",
        "Nova Scotia Poverty Reduction Credit",
        "Annual payment for Nova Scotia Income Assistance recipients without children who have very low income.",
        "C$500 a year, paid C$125 each quarter.",
        ["Filed tax return"],
        "Automatic — no application; you must file a tax return.",
        "https://novascotia.ca/coms/PovertyReductionCredit.html",
        "https://novascotia.ca/coms/PovertyReductionCredit.html",
        "Government of Nova Scotia (Department of Opportunities and Social Development)",
        ["cash", "income_support", "low-income"],
        rules(
            provinces=[NS], max_annual_income=16000,
            notes="Received Nova Scotia Income Assistance for the whole previous year (January–December), filed a tax return, adjusted income under C$16,000, and no dependent children.",
            verify_notes="Official income limit C$16,000 encoded.",
        ),
    )
    P(
        "can-pe-child-benefit",
        "Prince Edward Island Child Benefit",
        "Monthly payment for PEI families with children under 18 (low and middle income).",
        "C$34.16 per month per child if AFNI is under C$45,000; C$24.16 per month per child if AFNI is C$45,000–C$80,000.",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for PEI.",
        CRA_PROV + "province-prince-edward-island.html",
        CRA_PROV + "province-prince-edward-island.html",
        "Government of Prince Edward Island (administered by CRA)",
        ["children", "cash", "low-income", "middle-class"],
        rules(
            provinces=[PE], max_annual_income=80000,
            notes="PEI resident eligible for the CCB; no benefit when AFNI is over C$80,000.",
            verify_notes="Official ceiling C$80,000 encoded.",
        ),
    )
    P(
        "can-pe-sales-tax-credit",
        "Prince Edward Island Sales Tax Credit (PEI Essentials Benefit from November 2026)",
        "Tax-free quarterly credit (paid with the CGEB) for lower-income PEI residents.",
        "Up to C$310 for an individual and C$365 for a couple or single parent (July 2026 – June 2027). Renamed the PEI Essentials Benefit from November 2026 with a C$175 minimum.",
        SIN_DOCS,
        "No separate application: file your tax return — CRA pays it with the CGEB.",
        CRA_PROV + "province-prince-edward-island.html",
        CRA_PROV + "province-prince-edward-island.html",
        "Government of Prince Edward Island (administered by CRA)",
        ["cash", "tax_credit", "low-income"],
        rules(
            provinces=[PE], implies_low_income=True,
            notes="PEI resident eligible for the CGEB; amount depends on AFNI and family situation.",
            verify_notes="Thresholds not encoded — catalogue Canada soft gate (C$58,523) via implies_low_income. Confirm November 2026 Essentials Benefit terms.",
        ),
    )
    P(
        "can-sk-low-income-tax-credit",
        "Saskatchewan Low-Income Tax Credit",
        "Tax-free quarterly credit (paid with the CGEB) for low- and modest-income Saskatchewan residents.",
        "Up to C$460 for an individual, C$460 for a spouse/partner (or eligible dependant) and C$181 per child (maximum two children) — up to C$1,282 per family (July 2026 – June 2027).",
        SIN_DOCS,
        "No separate application: file your tax return — CRA pays it with the CGEB.",
        CRA_PROV + "province-saskatchewan.html",
        CRA_PROV + "province-saskatchewan.html",
        "Government of Saskatchewan (administered by CRA)",
        ["cash", "tax_credit", "low-income", "middle-class"],
        rules(
            provinces=[SK], max_annual_income=81668,
            notes="Saskatchewan resident eligible for the CGEB; reduced when AFNI exceeds C$39,345; families with AFNI between C$39,345 and C$81,668 may get part of the credit.",
            verify_notes="Official upper income C$81,668 encoded (families at the top get only a partial credit).",
        ),
    )
    P(
        "can-sk-seniors-income-plan",
        "Saskatchewan Seniors Income Plan (SIP)",
        "Monthly top-up for low-income Saskatchewan seniors who receive OAS and GIS.",
        "Up to C$360 per month for a single senior living at home (different amounts for couples and special-care homes).",
        ["None — assessed automatically from OAS/GIS"],
        "Automatic for eligible OAS/GIS recipients; contact the Seniors Income Plan office if you think you qualify.",
        "https://www.saskatchewan.ca/residents/family-and-social-support/seniors-services/seniors-income-plan",
        "https://www.saskatchewan.ca/residents/family-and-social-support/seniors-services/seniors-income-plan",
        "Government of Saskatchewan (Ministry of Social Services)",
        ["elderly", "income_support", "low-income"],
        rules(
            provinces=[SK], min_age=65, implies_low_income=True,
            notes="65 or older; Saskatchewan resident receiving OAS and GIS; very low other income (SIP reaches zero at about C$4,560 of taxable income excluding OAS/GIS for a single senior).",
            verify_notes="Income measured excluding OAS/GIS — catalogue Canada soft gate via implies_low_income; threshold in notes.",
        ),
    )
    P(
        "can-sk-said",
        "Saskatchewan Assured Income for Disability (SAID)",
        "Long-term income support for Saskatchewan adults with significant and enduring disabilities.",
        "Living Income Benefit (restructured and expanded from September 1, 2026) plus Exceptional Needs benefits; earned income exemptions C$7,500 single / C$8,700 couple / C$9,500 family per year.",
        ["Disability Impact Assessment", "Proof of identity and status", "Income and asset information"],
        "Apply online or by phone (1-800-667-7155) to Saskatchewan Social Services.",
        "https://www.saskatchewan.ca/said",
        "https://www.saskatchewan.ca/said",
        "Government of Saskatchewan (Ministry of Social Services)",
        ["disability", "income_support", "low-income"],
        rules(
            provinces=[SK], min_age=18, disability_required=True, implies_low_income=True,
            notes="18 or older; living in Saskatchewan; Canadian citizen, permanent resident, refugee (or CUAET); lack financial resources for basic needs; significant and enduring disability of a permanent nature (Disability Impact Assessment).",
            verify_notes="Financial need not encoded numerically — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )


def add_north_central() -> None:
    from canada_starter_pack_2026_09_25_rows import (  # noqa: PLC0415
        ALL_INCOMES, CRA_PROV, NT, NU, ON, QC, SIN_DOCS, YT, P, rules,
    )

    P(
        "can-nt-child-benefit",
        "Northwest Territories Child Benefit",
        "Monthly payment for low- and modest-income NWT families with children under 18.",
        "Per month for children under 6: C$67.91 (1 child), C$122.25 (2), C$166.41 (3), C$203.75 (4), plus C$30.58 each additional; for children 6–17: C$54.33 / C$97.83 / C$133.08 / C$163.00, plus C$24.41 each additional.",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for the NWT.",
        CRA_PROV + "northwest-territories.html",
        CRA_PROV + "northwest-territories.html",
        "Government of the Northwest Territories (administered by CRA)",
        ["children", "cash", "low-income"],
        rules(
            provinces=[NT], implies_low_income=True,
            notes="NWT resident eligible for the CCB; partial benefit when AFNI is above C$30,000.",
            verify_notes="Zero-out depends on number of children — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-nt-senior-home-heating-subsidy",
        "NWT Senior Home Heating Subsidy",
        "Monthly help with home heating costs from September to April for NWT seniors with low-to-moderate household income.",
        "2026–2027 season: C$460, C$560 or C$750 per month depending on your community zone (C$3,680 / C$4,480 / C$6,000 for the season).",
        ["Proof of age", "Total household income", "Proof of homeownership or rental"],
        "Apply at your local Education, Culture and Employment (ECE) Service Centre; deadline March 15, 2027.",
        "https://www.ece.gov.nt.ca/en/services/income-security-programs/senior-home-heating-subsidy",
        "https://www.ece.gov.nt.ca/en/services/income-security-programs/senior-home-heating-subsidy",
        "Government of the Northwest Territories (Education, Culture and Employment)",
        ["elderly", "energy", "utility", "low-income", "middle-class"],
        rules(
            provinces=[NT], min_age=60, max_annual_income=87000,
            notes="NWT resident aged 60 or older; household income up to C$66,000 (Zone 1), C$75,000 (Zone 2) or C$87,000 (Zone 3) depending on community; not receiving Income Assistance.",
            verify_notes="max_annual_income encodes the highest zone threshold (Zone 3, C$87,000); lower zones in notes. Income Assistance exclusion per ECE program page.",
        ),
    )
    P(
        "can-nu-child-benefit",
        "Nunavut Child Benefit",
        "Monthly payment for low-income Nunavut families with children under 18.",
        "C$58 per month per child (July 2026 – June 2027).",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for Nunavut.",
        CRA_PROV + "nunavut.html",
        CRA_PROV + "nunavut.html",
        "Government of Nunavut (administered by CRA)",
        ["children", "cash", "low-income"],
        rules(
            provinces=[NU], implies_low_income=True,
            notes="Nunavut resident eligible for the CCB; partial benefit when AFNI is above C$22,065.",
            verify_notes="Zero-out depends on number of children — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-on-trillium-benefit",
        "Ontario Trillium Benefit (OTB: sales tax credit, energy and property tax credit, northern energy credit)",
        "Monthly Ontario payment combining the Ontario sales tax credit, the Ontario energy and property tax credit and the Northern Ontario energy credit.",
        "July 2026 – June 2027 Ontario sales tax credit: up to C$378 per adult and per child. Energy and property tax credit and Northern Ontario energy credit amounts depend on rent/property tax, age and income. Paid monthly on the 10th.",
        SIN_DOCS + ["Rent or property tax amounts (Form ON-BEN)"],
        "Complete Form ON-BEN with your tax return; CRA pays the OTB.",
        CRA_PROV + "province-ontario.html",
        CRA_PROV + "province-ontario.html",
        "Government of Ontario (administered by CRA)",
        ["cash", "tax_credit", "housing", "energy", "low-income", "middle-class"],
        rules(
            provinces=[ON],
            notes="Ontario resident on December 31, 2025 who applied on Form ON-BEN. Sales tax credit reduced by 4% of adjusted net income over C$29,047 (single, no children) or of AFNI over C$36,309 (families).",
            verify_notes="Components and thresholds vary by household — max_annual_income null; phase-out reaches middle-income families (implies_low_income false).",
        ),
    )
    P(
        "can-on-child-benefit",
        "Ontario Child Benefit",
        "Monthly payment for low- to moderate-income Ontario families with children under 18.",
        "Up to C$146.66 per month per child (July 2026 – June 2027), paid with the CCB.",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for Ontario.",
        CRA_PROV + "province-ontario.html",
        CRA_PROV + "province-ontario.html",
        "Government of Ontario (administered by CRA)",
        ["children", "cash", "low-income", "middle-class"],
        rules(
            provinces=[ON],
            notes="Ontario resident eligible for the CCB; partial benefit when AFNI is above C$26,865 (zero-out rises with the number of children).",
            verify_notes="Phase-out reaches middle incomes for larger families — max_annual_income null, implies_low_income false.",
        ),
    )
    P(
        "can-on-seniors-dental-care",
        "Ontario Seniors Dental Care Program (OSDCP)",
        "Free routine dental care for low-income Ontario seniors aged 65 or older.",
        "Free check-ups, cleaning, fillings, x-rays, extractions, root canals and gum treatment; dentures partially covered. Coverage runs to July 31 each year.",
        ["Social Insurance Number (SIN) (to verify income)", "Ontario health card", "Proof of Ontario residence"],
        "Apply online or by paper form (ontario.ca); then book with a participating provider.",
        "https://www.ontario.ca/page/dental-care-seniors",
        "https://www.ontario.ca/page/dental-care-seniors",
        "Government of Ontario (Ministry of Health)",
        ["elderly", "health", "dental", "low-income"],
        rules(
            provinces=[ON], min_age=65, max_annual_income=42290,
            notes="65 or older; Ontario resident; annual net income C$25,480 or less (single) or combined C$42,290 or less (couple); no other dental benefits except the Canadian Dental Care Plan (not Ontario Works / ODSP / NIHB / private insurance).",
            verify_notes="max_annual_income encodes the couple limit (C$42,290); single C$25,480 in notes.",
        ),
    )
    P(
        "can-on-odsp",
        "Ontario Disability Support Program (ODSP)",
        "Ontario income support and health benefits for adults with disabilities in financial need.",
        "Up to C$1,436 a month for basic needs and shelter for a single person (July 2026 rates, +1.9%), more for families and special needs; drug, dental and vision benefits. The Canada Disability Benefit is exempt as income.",
        ["Proof of identity and status in Canada", "Financial information (income, assets, rent)", "Disability Determination Package completed by a health professional"],
        "Apply online or by phone/at a local ODSP office; the financial eligibility check comes first, then the disability determination.",
        "https://www.ontario.ca/page/ontario-disability-support-program",
        "https://www.ontario.ca/page/ontario-disability-support-program",
        "Government of Ontario (Ministry of Children, Community and Social Services)",
        ["disability", "income_support", "health", "low-income"],
        rules(
            provinces=[ON], min_age=18, disability_required=True, implies_low_income=True,
            notes="18 or older; Ontario resident; in financial need (income and assets below ODSP limits); a substantial physical or mental impairment expected to last a year or more that restricts work, self-care or community life (or a prescribed class, e.g. CPP-D recipients).",
            verify_notes="Income/asset limits not encoded — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-qc-family-allowance",
        "Quebec Family Allowance (Allocation famille)",
        "Retraite Québec's regular payment for Quebec families with children under 18; every eligible family gets at least the minimum amount.",
        "2026: C$1,221 to C$3,068 per child per year (single-parent supplement C$430 to C$1,077), plus a C$127 school-supplies supplement; Supplement for Handicapped Children C$2,892 a year (exceptional-care tiers C$14,580 / C$9,696).",
        ["Birth registration (Déclaration de naissance)", "Québec tax returns for both parents"],
        "Usually automatic when you register the birth in Québec; otherwise apply to Retraite Québec. File Québec tax returns every year.",
        "https://www.retraitequebec.gouv.qc.ca/en/citizens/children/family-allowance",
        "https://www.retraitequebec.gouv.qc.ca/en/benefits-amounts-key-data",
        "Retraite Québec (Government of Québec)",
        ["children", "cash"] + ALL_INCOMES,
        rules(
            provinces=[QC],
            notes="Quebec resident with a dependent child under 18 living with you; you or your spouse is a Canadian citizen, permanent resident or protected person (some temporary residents qualify). Amount depends on family income (line 275), number of children and custody — the minimum is paid at all incomes.",
            verify_notes="Minimum paid at all incomes: max_annual_income null.",
        ),
    )
    P(
        "can-qc-qpip",
        "Québec Parental Insurance Plan (QPIP / RQAP)",
        "Quebec's parental insurance: maternity, paternity, parental and adoption benefits for insured workers and self-employed people in Quebec (replaces EI maternity/parental).",
        "Basic plan: maternity 18 weeks at 70% of average weekly earnings; paternity 5 weeks at 70%; plus shareable parental weeks. Special plan: maternity 15 weeks at 75%, paternity 3 weeks at 75%. Maximum insurable earnings C$103,000 (2026).",
        ["Social Insurance Number (SIN)", "Records of Employment (wage earners) or Schedule L income (self-employed)", "Child's birth or adoption details"],
        "Apply online to the QPIP (Centre de service à la clientèle) once your benefit period can begin.",
        "https://www.quebec.ca/en/family-and-support-for-individuals/pregnancy-parenthood/financial-support-pregnant-women-families/quebec-parental-insurance-plan",
        "https://www.quebec.ca/en/family-and-support-for-individuals/pregnancy-parenthood/financial-support-pregnant-women-families/quebec-parental-insurance-plan/pregnancy-childbirth/choice-plan",
        "Government of Québec (Ministère de l'Emploi et de la Solidarité sociale)",
        ["maternity", "children", "employment", "insurance", "middle-class", "upper-middle-class", "high-income-eligible"],
        rules(
            provinces=[QC],
            notes="Quebec resident at the start of the benefit period; at least C$2,000 of insurable earnings in the qualifying period; paid or owe QPIP (or EI) contributions; stopped work or weekly earnings/time reduced by at least 40%. Not income-tested.",
            verify_notes="Earnings-replacement: max_annual_income null.",
        ),
    )
    P(
        "can-qc-solidarity-tax-credit",
        "Quebec Solidarity Tax Credit (Crédit d'impôt pour solidarité)",
        "Refundable Revenu Québec credit for low- and middle-income households, with QST, housing and northern-village components.",
        "July 2026 – June 2027 amounts calculated from your situation on December 31, 2025 (QST, housing and northern-village components), reduced as family income rises; paid monthly, quarterly or yearly.",
        ["Schedule D of the Québec income tax return", "Dwelling / RL-31 information", "Direct deposit with Revenu Québec"],
        "Claim on Schedule D of your Québec tax return and register for direct deposit.",
        "https://www.revenuquebec.ca/en/citizens/tax-credits/solidarity-tax-credit/",
        "https://www.revenuquebec.ca/en/citizens/tax-credits/solidarity-tax-credit/",
        "Revenu Québec (Government of Québec)",
        ["cash", "tax_credit", "housing", "low-income", "middle-class"],
        rules(
            provinces=[QC], implies_low_income=True,
            notes="Quebec resident on December 31, 2025 who filed a Québec tax return (Schedule D). Reduced as family income rises; the maximum family income depends on family situation (Revenu Québec table).",
            verify_notes="Family-income maximums by situation not encoded — catalogue Canada soft gate (C$58,523) via implies_low_income; confirm with the Revenu Québec estimator.",
        ),
    )
    P(
        "can-qc-qpp-retirement",
        "Québec Pension Plan (QPP) retirement pension",
        "Retraite Québec's contributory retirement pension for people who worked in Quebec (instead of CPP).",
        "2026 maximum monthly retirement pension: C$1,507.65 at 65 (C$964.90 at 60; C$2,394.15 at 72). Disability and survivor pensions also available.",
        ["Social Insurance Number (SIN)", "Bank details"],
        "Apply to Retraite Québec online (My Account) or by form.",
        "https://www.retraitequebec.gouv.qc.ca/en/",
        "https://www.retraitequebec.gouv.qc.ca/en/benefits-amounts-key-data",
        "Retraite Québec (Government of Québec)",
        ["pension", "elderly", "employment"] + ALL_INCOMES,
        rules(
            provinces=[QC], min_age=60,
            notes="Aged 60 or older and contributed to the QPP (work in Quebec). The pension can start between 60 and 72. Not income-tested.",
            verify_notes="Contributory: max_annual_income null.",
        ),
    )
    P(
        "can-yt-child-benefit",
        "Yukon Child Benefit",
        "Monthly payment for low- and modest-income Yukon families with children under 18.",
        "Up to C$80.50 per month per child (July 2026 – June 2027).",
        SIN_DOCS,
        "No separate application: apply for the CCB and file tax returns — CRA pays it for Yukon.",
        CRA_PROV + "yukon.html",
        CRA_PROV + "yukon.html",
        "Government of Yukon (administered by CRA)",
        ["children", "cash", "low-income"],
        rules(
            provinces=[YT], implies_low_income=True,
            notes="Yukon resident eligible for the CCB; partial benefit when AFNI is above C$35,000.",
            verify_notes="Zero-out depends on number of children — catalogue Canada soft gate (C$58,523) via implies_low_income.",
        ),
    )
    P(
        "can-yt-pioneer-utility-grant",
        "Yukon Pioneer Utility Grant (PUG)",
        "Annual grant to help Yukon seniors (owners or renters) with home heating costs.",
        "2026 maximum before income testing: C$1,382.58 inside Whitehorse city limits; C$1,466.50 outside Whitehorse.",
        ["CRA notice of assessment (line 23600)", "Proof of housing costs", "Proof of age and status"],
        "Apply every year between July 1 and December 31, 2026 — online portal, in person or by mail.",
        "https://yukon.ca/en/pioneer-utility-grant",
        "https://yukon.ca/en/pioneer-utility-grant",
        "Government of Yukon (Yukon Housing Corporation)",
        ["elderly", "energy", "utility", "low-income", "middle-class", "upper-middle-class"],
        rules(
            provinces=[YT], min_age=65, max_annual_income=217470,
            notes="65 or older in 2026; Canadian citizen or permanent resident; lived in Yukon at least 12 months (183 days of the year in Yukon, including 3 months of October–March). Not eligible if net income is above C$154,206 (single) or C$217,470 (couple).",
            verify_notes="max_annual_income encodes the couple limit (C$217,470); single C$154,206 in notes. Grant is income-tested below these limits.",
        ),
    )
