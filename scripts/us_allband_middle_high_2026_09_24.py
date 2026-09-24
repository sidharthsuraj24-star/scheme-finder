#!/usr/bin/env python3
"""US all-band deepen (2026-09-24): middle-class and high-income-eligible
federal tax benefits missing from catalogue. Official .gov only; never invent
ceilings. Syncs data/ + frontend/data/; updates catalogue_meta.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "schemes.json"
FE_DATA = ROOT / "frontend" / "data" / "schemes.json"
META = ROOT / "data" / "catalogue_meta.json"
FE_META = ROOT / "frontend" / "data" / "catalogue_meta.json"
LAST = "2026-09-24"
ISO = "2026-09-24T07:30:00+05:30"


def L(en: str, hi: str | None = None, ml: str | None = None) -> dict:
    return {"en": en, "ml": ml or en, "hi": hi or en}


def docs(items: list[str]) -> dict:
    return {"en": items, "ml": items, "hi": items}


def us_rules(*, notes: str, verify_notes: str, implies_low_income: bool = False) -> dict:
    return {
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
        "notes": notes,
        "verify": True,
        "verify_notes": verify_notes,
        "implies_low_income": implies_low_income,
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


ADDS: list[dict] = [
    us_scheme(
        "us-mortgage-interest-deduction",
        "Home Mortgage Interest Deduction (Schedule A) – United States",
        "गृह बंधक ब्याज कटौती (अनुसूची A) – संयुक्त राज्य अमेरिका",
        "IRS itemized deduction for qualified mortgage interest and points on a loan secured by your main home or a second home. Claimed on Schedule A (Form 1040) when itemizing. Common for middle- and higher-income homeowners whose itemized deductions exceed the standard deduction.",
        "Deduct qualified home mortgage interest (and certain points) subject to acquisition-debt limits: generally $750,000 of post–Dec 15, 2017 acquisition debt ($375,000 MFS), or $1 million for older qualifying debt ($500,000 MFS). Home equity interest deductible only if used to buy, build, or substantially improve a qualified home. Confirm Pub. 936 for your loans.",
        [
            "Form 1098 (Mortgage Interest Statement) if issued",
            "Form 1040 with Schedule A (itemize)",
            "Records of loan use for buy/build/improve if equity debt",
        ],
        "Itemize on Schedule A when filing Form 1040. See IRS Topic 505 and Publication 936 for limits and second-home rules.",
        "https://www.irs.gov/taxtopics/tc505",
        "https://www.irs.gov/taxtopics/tc505",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "housing",
            "itemized-deduction",
        ],
        us_rules(
            notes=(
                "No federal means test / income ceiling for the deduction itself; "
                "must itemize and meet qualified-residence and acquisition-debt rules. "
                "Debt dollar limits apply (Pub. 936 / Topic 505). Source: "
                "https://www.irs.gov/taxtopics/tc505 (reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Topic 505 + Pub. 936. Confirm acquisition-debt "
                "ceilings and Form 1098 amounts for the tax year before quoting."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-salt-deduction",
        "State and Local Tax (SALT) Deduction – United States",
        "राज्य और स्थानीय कर (SALT) कटौती – संयुक्त राज्य अमेरिका",
        "IRS itemized deduction for state and local income (or general sales) taxes plus state and local real and personal property taxes, subject to an overall SALT cap. Claimed on Schedule A (Form 1040). Often material for middle- and higher-income households in high-tax states who itemize.",
        "Combined SALT deduction generally limited to $40,000 ($20,000 MFS) per IRS Topic 503 / Schedule A instructions; the overall limit is reduced if MAGI exceeds stated thresholds but not below $10,000 ($5,000 MFS). Confirm current Instructions for Schedule A for MAGI phase-down of the cap.",
        [
            "Form W-2 / state return records for income or sales taxes paid",
            "Property tax bills / personal property tax records",
            "Form 1040 with Schedule A (itemize)",
        ],
        "Itemize on Schedule A (lines for state/local income or sales, real property, and personal property taxes). See IRS Topic 503 and Schedule A instructions.",
        "https://www.irs.gov/taxtopics/tc503",
        "https://www.irs.gov/taxtopics/tc503",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "itemized-deduction",
            "salt",
        ],
        us_rules(
            notes=(
                "No poverty means test; benefit requires itemizing. SALT dollar cap "
                "and MAGI-based reduction of the cap (not a full phaseout to zero) "
                "are tax-year specific. Source: https://www.irs.gov/taxtopics/tc503 "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Topic 503 cites $40,000/$20,000 SALT cap with MAGI "
                "limitation not reduced below $10,000/$5,000. Confirm Schedule A "
                "instructions for the filing year."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-charitable-contribution-deduction",
        "Charitable Contribution Deduction – United States",
        "धर्मार्थ योगदान कटौती – संयुक्त राज्य अमेरिका",
        "IRS deduction for gifts to qualified charitable organizations. Generally claimed as an itemized deduction on Schedule A; beginning tax year 2026, non-itemizers may deduct limited cash contributions to certain qualified organizations (per IRS Topic 506). No poverty means test—useful across middle and higher incomes when giving.",
        "Itemizers: deduct qualified cash and noncash gifts subject to AGI percentage limits and substantiation rules (Pub. 526). Non-itemizers (TY 2026+): up to $1,000 ($2,000 MFJ) of cash contributions to certain qualified organizations per Topic 506. Gifts to individuals are not deductible.",
        [
            "Bank records or written acknowledgment from the charity",
            "Contemporaneous written acknowledgment for gifts of $250+",
            "Form 8283 for noncash gifts over $500 (appraisal rules for larger gifts)",
            "Form 1040 (Schedule A if itemizing)",
        ],
        "Claim on Schedule A when itemizing, or use the limited non-itemizer cash path for TY 2026+ if eligible. See IRS Topic 506 and Publication 526.",
        "https://www.irs.gov/taxtopics/tc506",
        "https://www.irs.gov/taxtopics/tc506",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "universal",
            "charitable",
            "itemized-deduction",
        ],
        us_rules(
            notes=(
                "No federal income ceiling for charitable deductions; AGI percentage "
                "limits and substantiation apply. Non-itemizer cash deduction begins "
                "TY 2026 (Topic 506). Source: https://www.irs.gov/taxtopics/tc506 "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Topic 506 + Pub. 526. Confirm AGI limits, "
                "non-itemizer cash amounts, and acknowledgment rules for the tax year."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-student-loan-interest-deduction",
        "Student Loan Interest Deduction – United States",
        "छात्र ऋण ब्याज कटौती – संयुक्त राज्य अमेरिका",
        "IRS above-the-line deduction (adjustment to income) for interest paid on a qualified student loan. You do not need to itemize. Aimed at borrowers with middle incomes; phases out as MAGI rises (limits set annually).",
        "Deduct the lesser of $2,500 or interest actually paid on a qualified student loan, subject to MAGI phaseout for your filing status. Claimed on Schedule 1 (Form 1040). Form 1098-E may be issued if interest paid was $600 or more.",
        [
            "Form 1098-E if issued",
            "Loan records showing interest paid and that the loan is qualified",
            "Form 1040 with Schedule 1",
        ],
        "Claim as an adjustment to income on Schedule 1 when filing Form 1040. See IRS Topic 456 and Publication 970 for MAGI phaseouts and qualified-loan rules.",
        "https://www.irs.gov/taxtopics/tc456",
        "https://www.irs.gov/taxtopics/tc456",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "education",
            "student-loan",
        ],
        us_rules(
            notes=(
                "Not MFS; not claimed as a dependent; must be legally obligated on a "
                "qualified student loan; MAGI below the annual phaseout ceiling "
                "(amounts change yearly—do not hard-code). Source: "
                "https://www.irs.gov/taxtopics/tc456 (reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Topic 456. Confirm current MAGI phaseout bands in "
                "Form 1040 instructions / Pub. 970 before quoting ceilings."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-education-credits-aotc-llc",
        "American Opportunity Tax Credit (AOTC) / Lifetime Learning Credit (LLC) – United States",
        "अमेरिकन अपॉर्च्युनिटी टैक्स क्रेडिट (AOTC) / लाइफटाइम लर्निंग क्रेडिट (LLC)",
        "IRS education tax credits for qualified higher-education expenses paid to an eligible institution. AOTC is partially refundable (first four years of postsecondary); LLC is nonrefundable (unlimited years / job-skills courses). Claimed on Form 8863. Middle-income phaseouts apply.",
        "AOTC: up to $2,500 per eligible student (40% refundable up to $1,000). LLC: up to $2,000 per return (20% of up to $10,000 expenses). Cannot claim both for the same student/expenses. MAGI phaseout generally $80k–$90k single / $160k–$180k MFJ (confirm Form 8863 for the tax year). TY 2026+: work-eligible SSN rules for filer/spouse/student per IRS education-credits page.",
        [
            "Form 1098-T (Tuition Statement) if issued",
            "Form 8863 with Form 1040",
            "Valid work-eligible SSNs as required for the tax year",
            "School EIN for AOTC",
        ],
        "Complete Form 8863 and attach to Form 1040. See IRS Education Credits (AOTC and LLC) page and Publication 970.",
        "https://www.irs.gov/credits-deductions/individuals/education-credits-aotc-and-llc",
        "https://www.irs.gov/credits-deductions/individuals/education-credits-aotc-and-llc",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "education",
            "aotc",
            "llc",
        ],
        us_rules(
            notes=(
                "MAGI phaseouts make these middle-income credits (not high-income). "
                "Leave max_annual_income null; amounts and SSN rules are tax-year "
                "specific. Source: "
                "https://www.irs.gov/credits-deductions/individuals/education-credits-aotc-and-llc "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS AOTC/LLC page + Form 8863 drafts. Confirm MAGI "
                "bands, credit amounts, and SSN identification rules for the filing year."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-hsa",
        "Health Savings Account (HSA) – United States",
        "हेल्थ सेविंग्स अकाउंट (HSA) – संयुक्त राज्य अमेरिका",
        "IRS tax-favored medical savings account for eligible individuals covered by a high-deductible health plan (HDHP). Contributions (other than employer) are deductible above the line; earnings grow tax-free; qualified medical distributions are tax-free. No federal poverty means test—common for middle+ households on HDHPs.",
        "Annual contribution limits set by IRS (e.g., Pub. 969 lists 2026 self-only $4,400 / family $8,750 plus $1,000 catch-up if age 55+). Employer contributions may be excluded from income. Must have HDHP coverage, no disqualifying other coverage, not enrolled in Medicare, and not another’s dependent. Report on Form 8889.",
        [
            "HDHP enrollment proof / plan documents",
            "Form 8889 with Form 1040",
            "Form 5498-SA / Form 1099-SA from trustee as applicable",
            "Records of qualified medical expenses for distributions",
        ],
        "Open an HSA with a qualified trustee; contribute up to the annual limit; claim the deduction on Form 8889 with your return. See IRS Publication 969.",
        "https://www.irs.gov/publications/p969",
        "https://www.irs.gov/publications/p969",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "health",
            "hsa",
            "savings",
        ],
        us_rules(
            notes=(
                "No federal income ceiling for HSA eligibility; HDHP and other "
                "coverage rules apply. Contribution limits and HDHP deductible "
                "floors are inflation-adjusted annually. Source: "
                "https://www.irs.gov/publications/p969 (reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Pub. 969 (2025 edition with 2026 HDHP/contribution "
                "tips). Confirm contribution and HDHP dollar amounts for the year "
                "before quoting."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-qbi-199a",
        "Qualified Business Income Deduction (§199A) – United States",
        "योग्य व्यवसाय आय कटौती (§199A) – संयुक्त राज्य अमेरिका",
        "IRS deduction (Section 199A) allowing eligible owners of sole proprietorships, partnerships, S corporations, and certain trusts/estates to deduct up to 20% of qualified business income (QBI), plus 20% of qualified REIT dividends and PTP income, subject to taxable-income and other limitations. Available whether or not you itemize. Relevant for self-employed and pass-through owners across middle and higher incomes.",
        "Up to 20% of QBI (plus REIT/PTP component), limited by taxable income minus net capital gain; wage/UBIA and specified-service trade or business limits may apply above income thresholds. For tax years beginning after 2025, compare also to the Minimum Deduction for Active Qualified Business Income (MDA-QBI) per IRS QBI page. Claim using Form 8995 or 8995-A.",
        [
            "Business books / Schedule C or K-1 showing QBI",
            "Form 8995 or Form 8995-A",
            "Form 1040",
        ],
        "Figure the deduction on Form 8995 or 8995-A and claim on Form 1040. See IRS Qualified Business Income Deduction page and form instructions.",
        "https://www.irs.gov/newsroom/qualified-business-income-deduction",
        "https://www.irs.gov/newsroom/qualified-business-income-deduction",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "self-employed",
            "qbi",
            "business",
        ],
        us_rules(
            notes=(
                "No poverty means test; wage/property and SSTB limitations phase in "
                "with taxable income (thresholds tax-year specific—do not invent). "
                "C-corp wages and employee wages are not QBI. Source: "
                "https://www.irs.gov/newsroom/qualified-business-income-deduction "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS QBI page (updated Sep 2026) notes post-2025 "
                "MDA-QBI rules. Confirm Form 8995/8995-A instructions for thresholds."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-adoption-credit",
        "Adoption Credit / Employer Adoption Benefits Exclusion – United States",
        "गोद लेने का कर क्रेडिट / नियोक्ता गोद लाभ बहिष्करण – संयुक्त राज्य अमेरिका",
        "IRS credit for qualified adoption expenses and/or income exclusion for employer-provided adoption benefits (Form 8839). Applies to domestic, international, private, and public foster-care adoptions of an eligible child. Phaseout begins at relatively high MAGI—relevant to middle and upper-middle adoptive families.",
        "For 2025 IRS page amounts: qualified expenses / exclusion up to $17,280 per eligible child; beginning TY 2025 a portion of the credit is refundable up to $5,000 per qualifying child; MAGI phaseout begins at $259,190 and credit unavailable at $299,190+ (confirm current Form 8839 instructions for later years). Special-needs adoptions may allow full credit even without paid expenses.",
        [
            "Form 8839 with Form 1040",
            "Adoption documentation / ATIN if needed (Form W-7A)",
            "Employer adoption benefits on Form W-2 Box 12 Code T if applicable",
            "Special-needs determination docs if claiming special-needs rules",
        ],
        "Complete Form 8839 and attach to your return. See IRS Adoption Credit page and Form 8839 instructions for timing (domestic vs foreign) and special-needs rules.",
        "https://www.irs.gov/credits-deductions/individuals/adoption-credit",
        "https://www.irs.gov/credits-deductions/individuals/adoption-credit",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "adoption",
            "children",
            "family",
        ],
        us_rules(
            notes=(
                "MAGI phaseout is high (2025 IRS page: phaseout $259,190–$299,189). "
                "Leave max_annual_income null; amounts inflate—verify Form 8839. "
                "Married generally must file jointly. Source: "
                "https://www.irs.gov/credits-deductions/individuals/adoption-credit "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Adoption Credit page (2025 dollar figures shown). "
                "Confirm Form 8839 instructions for the tax year before quoting ceilings."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-car-loan-interest-deduction",
        "Qualified Passenger Vehicle Loan Interest Deduction – United States",
        "योग्य यात्री वाहन ऋण ब्याज कटौती – संयुक्त राज्य अमेरिका",
        "IRS above-the-line deduction (tax years 2025–2028) of up to $10,000 of interest on a qualified new passenger vehicle loan incurred after Dec 31, 2024, secured by a first lien, with final assembly in the United States. Available to itemizers and non-itemizers, subject to MAGI limitations (Topic 505).",
        "Annual deduction up to $10,000 of qualified passenger vehicle loan interest for TY 2025–2028. Used vehicles do not qualify; vehicle’s original use must start with the taxpayer; U.S. final assembly required. MAGI limits apply—confirm current IRS guidance/Form 1040 instructions.",
        [
            "Loan statements showing interest paid on a qualifying vehicle loan",
            "Evidence vehicle is new, U.S.-assembled, and secured by first lien",
            "Form 1040 (adjustment to income path per current instructions)",
        ],
        "Claim per Form 1040 instructions for the tax year (Topic 505 describes the deduction). Confirm MAGI and vehicle qualification before claiming.",
        "https://www.irs.gov/taxtopics/tc505",
        "https://www.irs.gov/taxtopics/tc505",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "vehicle",
            "obbb",
        ],
        us_rules(
            notes=(
                "Available TY 2025–2028 only per IRS Topic 505. MAGI limitations "
                "apply (amounts tax-year specific—do not invent). Loan must be "
                "incurred after Dec 31, 2024; new vehicle; U.S. final assembly; "
                "first lien. Source: https://www.irs.gov/taxtopics/tc505 "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Topic 505 (updated May 2026). Confirm MAGI "
                "phaseouts and reporting line in Form 1040 instructions for the year."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-ira-contributions",
        "Traditional / Roth IRA Contribution Tax Treatment – United States",
        "पारंपरिक / रोथ IRA योगदान कर उपचार – संयुक्त राज्य अमेरिका",
        "IRS individual retirement arrangement framework: annual contributions to traditional and/or Roth IRAs up to inflation-adjusted limits, with traditional IRA contributions potentially deductible (subject to workplace-plan and MAGI rules) and Roth contributions made with after-tax dollars for generally tax-free qualified distributions. No poverty means test—core middle- and higher-income retirement benefit.",
        "Combined traditional + Roth IRA contributions limited annually (IRS 2026 newsroom: $7,500, or higher with age-50+ catch-up—confirm current limits). Traditional deductibility and Roth contribution eligibility can phase out with MAGI if covered by a workplace plan (traditional) or generally for Roth. See IRS IRA contribution limits page and Pub. 590-A.",
        [
            "IRA trustee statements / Form 5498",
            "Form 1040 (and Form 8606 if nondeductible traditional contributions)",
            "Records of taxable compensation and MAGI",
        ],
        "Contribute to an IRA at a bank, broker, or other trustee by the tax-filing deadline (generally); claim any traditional deduction on Form 1040. See IRS Retirement topics – IRA contribution limits.",
        "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-ira-contribution-limits",
        "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-ira-contribution-limits",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "retirement",
            "ira",
            "universal",
        ],
        us_rules(
            notes=(
                "Anyone with taxable compensation (and under age limits for "
                "traditional deductible contributions per current law) may contribute "
                "up to the annual limit; Roth eligibility and traditional deductibility "
                "have MAGI phaseouts—leave max_annual_income null. Source: "
                "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-ira-contribution-limits "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS IRA contribution limits + 2026 newsroom limit "
                "announcement. Confirm contribution, catch-up, and MAGI phaseout "
                "tables for the tax year in Pub. 590-A."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-401k-elective-deferrals",
        "401(k) / Workplace Elective Deferral Tax Treatment – United States",
        "401(k) / कार्यस्थल वैकल्पिक आस्थगन कर उपचार – संयुक्त राज्य अमेरिका",
        "IRS tax treatment of elective deferrals to employer-sponsored retirement plans (e.g., 401(k), 403(b), most governmental 457(b)): contributions are generally pre-tax (traditional) or designated Roth, reducing current taxable wages for traditional deferrals, with tax-deferred (or Roth tax-free qualified) growth. No federal poverty means test—primary middle- and higher-income retirement vehicle when an employer offers a plan.",
        "Elective deferral dollar limits set annually by IRS (2026 newsroom: $24,500 elective deferrals, with catch-up contributions if eligible—confirm current limits). Employer matching may apply per plan. Subject to plan eligibility and IRC annual additions limits. Not available unless your employer sponsors a qualifying plan.",
        [
            "Plan enrollment / salary deferral election with employer",
            "Form W-2 showing deferrals (Box 12 codes)",
            "Plan summary / SPD from employer",
        ],
        "Enroll through your employer’s plan administrator and elect deferrals from pay. Limits and catch-up rules: IRS Retirement topics – Contributions / annual limit newsroom releases.",
        "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-contributions",
        "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-contributions",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "retirement",
            "401k",
            "employer",
        ],
        us_rules(
            notes=(
                "No federal income ceiling for elective deferrals themselves (highly "
                "compensated employee nondiscrimination testing may limit plan "
                "operations). Requires employer plan participation. Contribution "
                "limits are annual—do not invent. Source: "
                "https://www.irs.gov/retirement-plans/plan-participant-employee/retirement-topics-contributions "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS retirement contribution topics + 2026 limit "
                "newsroom. Confirm elective deferral and catch-up amounts for the year."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-capital-gains-preferential-rates",
        "Long-Term Capital Gains Preferential Tax Rates – United States",
        "दीर्घकालिक पूंजीगत लाभ अधिमानी कर दरें – संयुक्त राज्य अमेरिका",
        "IRS preferential tax rates on net long-term capital gain (assets held more than one year) versus ordinary income rates. Educational catalogue entry summarizing Topic 409: 0%, 15%, or 20% brackets depending on taxable income, with special higher rates for collectibles, certain small-business stock, and unrecaptured §1250 gain. Relevant to middle- and higher-income investors and homeowners with taxable investment gains.",
        "Most net long-term capital gain taxed at 0%, 15%, or 20% based on taxable income thresholds that change annually (Topic 409 lists 2025 bracket cutoffs). Short-term gains taxed as ordinary income. Capital losses offset gains then up to $3,000 ($1,500 MFS) of ordinary income, with carryover. NIIT may also apply (Topic 559) for higher investment income.",
        [
            "Form 1099-B / brokerage statements",
            "Form 8949 and Schedule D (Form 1040)",
            "Basis records (Pub. 551)",
        ],
        "Report sales on Form 8949 and summarize on Schedule D with Form 1040. See IRS Topic 409 and Publications 550/544. Not a separate application—rates apply automatically when you report qualifying gains.",
        "https://www.irs.gov/taxtopics/tc409",
        "https://www.irs.gov/taxtopics/tc409",
        "Internal Revenue Service (IRS)",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "middle-class",
            "high-income-eligible",
            "investment",
            "capital-gains",
            "universal",
        ],
        us_rules(
            notes=(
                "No means test to 'apply'—preferential rates apply to net long-term "
                "capital gain by statute. Bracket cutoffs are tax-year specific "
                "(Topic 409). Source: https://www.irs.gov/taxtopics/tc409 "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS Topic 409 (reviewed Feb 2026; shows 2025 income "
                "cutoffs). Confirm Publication 550 / Form 1040 instructions for the "
                "filing year’s 0/15/20% thresholds."
            ),
            implies_low_income=False,
        ),
    ),
    us_scheme(
        "us-opportunity-zones",
        "Opportunity Zones / Qualified Opportunity Fund Deferral – United States",
        "अवसर क्षेत्र / योग्य अवसर निधि आस्थगन – संयुक्त राज्य अमेरिका",
        "IRS program allowing taxpayers to temporarily defer tax on eligible capital (and certain §1231) gains invested in a Qualified Opportunity Fund (QOF) that holds Qualified Opportunity Zone property. Clear retail-investor IRS page; primarily useful to investors with capital gains (often middle-high / high income). Confirm current inclusion deadlines—many deferred gains must be included by Dec 31, 2026.",
        "Deferral of tax on eligible gains invested in a QOF within 180 days for equity (not debt) interest; basis adjustments may apply for longer holds; possible exclusion of post-investment QOF gain after 10 years if rules met. Annual Form 8997 reporting required. Dec 31, 2026 inclusion deadline applies to deferrals under current IRS investor page—verify before investing.",
        [
            "Records of eligible gain realization date and amount",
            "QOF equity investment documentation within 180 days",
            "Form 8949 election and annual Form 8997",
            "Form 1040 / Schedule D as applicable",
        ],
        "Invest eligible gain in a QOF for equity within 180 days; elect deferral on Form 8949; file Form 8997 annually. See IRS “Invest in a Qualified Opportunity Fund” and Opportunity Zones pages. Confirm Treasury/CDFI zone maps and post-2026 rule changes.",
        "https://www.irs.gov/credits-deductions/businesses/invest-in-a-qualified-opportunity-fund",
        "https://www.irs.gov/credits-deductions/businesses/invest-in-a-qualified-opportunity-fund",
        "Internal Revenue Service (IRS) / U.S. Department of the Treasury",
        [
            "united_states",
            "tax",
            "federal",
            "irs",
            "high-income-eligible",
            "investment",
            "opportunity-zones",
        ],
        us_rules(
            notes=(
                "No poverty means test; requires eligible gain and timely QOF "
                "equity investment. Current IRS page: deferral until inclusion event "
                "or Dec 31, 2026, whichever earlier; eligible gains recognized "
                "before Jan 1, 2027. Transition/new designation rules may apply—"
                "verify. Source: "
                "https://www.irs.gov/credits-deductions/businesses/invest-in-a-qualified-opportunity-fund "
                "(reviewed 2026-09-24)."
            ),
            verify_notes=(
                "2026-09-24: IRS QOF investor page (updated Dec 2025). Confirm "
                "Dec 31, 2026 inclusion, Form 8997, and any OBBB/new-cycle changes "
                "before describing benefits to users."
            ),
            implies_low_income=False,
        ),
    ),
]


META_APPEND = (
    " US all-band middle/high federal pack (2026-09-24): Mortgage Interest Deduction, "
    "SALT deduction, Charitable Contribution Deduction, Student Loan Interest Deduction, "
    "AOTC/LLC education credits, HSA, QBI §199A, Adoption Credit, Car Loan Interest "
    "Deduction (TY 2025–2028), Traditional/Roth IRA contribution tax treatment, "
    "401(k) elective deferral tax treatment, long-term capital gains preferential rates, "
    "Opportunity Zones/QOF deferral. Official .gov only; max_annual_income null / "
    "implies_low_income false; tags middle-class / high-income-eligible / universal / tax "
    "where accurate. Honest SKIP: Residential Clean Energy §25D (expenditures after "
    "2025-12-31), Clean Vehicle §30D/§25E (acquired after 2025-09-30), Energy Efficient "
    "Home Improvement §25C (placed in service after 2025-12-31) per IRS OBBB FAQs."
)


def main() -> None:
    schemes: list[dict] = json.loads(DATA.read_text())
    by_id = {s["id"]: i for i, s in enumerate(schemes)}
    added, updated = [], []
    for s in ADDS:
        sid = s["id"]
        if sid in by_id:
            schemes[by_id[sid]] = s
            updated.append(sid)
        else:
            schemes.append(s)
            added.append(sid)

    payload = json.dumps(schemes, indent=2, ensure_ascii=False) + "\n"
    DATA.write_text(payload)
    FE_DATA.write_text(payload)

    meta = json.loads(META.read_text())
    meta["updated_as_of"] = LAST
    meta["updated_as_of_iso"] = ISO
    meta["scheme_count"] = len(schemes)
    scope = meta.get("scope", "")
    if "US all-band middle/high federal pack" not in scope:
        meta["scope"] = scope.rstrip() + META_APPEND
    meta_payload = json.dumps(meta, indent=2, ensure_ascii=False) + "\n"
    META.write_text(meta_payload)
    FE_META.write_text(meta_payload)

    print(f"total={len(schemes)} added={len(added)} updated={len(updated)}")
    print("ADDED:", ", ".join(added) or "(none)")
    print("UPDATED:", ", ".join(updated) or "(none)")


if __name__ == "__main__":
    main()
