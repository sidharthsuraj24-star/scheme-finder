"""Row data for scripts/uk_starter_pack_2026_09_25.py (United Kingdom starter pack).

Every figure comes from the official page in official_source_url, checked 2026-09-25.
"""
from __future__ import annotations

LAST = "2026-09-25"

E, S, W, NI = "England", "Scotland", "Wales", "Northern Ireland"
NATION_TAG = {E: "england", S: "scotland", W: "wales", NI: "northern_ireland"}

DWP = "Department for Work and Pensions (DWP)"
HMRC = "HM Revenue & Customs (HMRC)"
SSS = "Social Security Scotland (Scottish Government)"
WG = "Welsh Government"
LA = "Local council"
DFE = "Department for Education (DfE)"

NI_NOTE = "Northern Ireland: claim through nidirect.gov.uk (Department for Communities)."
ID_DOCS = ["National Insurance number", "Proof of identity", "Bank or building society details"]


def L(en: str) -> dict:
    return {"en": en, "ml": en, "hi": en}


def docs(items: list[str]) -> dict:
    return {"en": items, "ml": items, "hi": items}


def rules(
    *,
    nations: list[str] | None,
    notes: str,
    verify_notes: str,
    implies_low_income: bool = False,
    min_age: int | None = None,
    max_age: int | None = None,
    max_annual_income: float | None = None,
    disability_required: bool = False,
    maternity_required: bool = False,
    verify: bool = True,
) -> dict:
    uk_wide = not nations
    r = {
        "min_age": min_age,
        "max_age": max_age,
        "max_annual_income": max_annual_income,
        "max_monthly_household_income": None,
        "occupations": [],
        "categories": [],
        "gender": None,
        "marital_status": [],
        "disability_required": disability_required,
        "min_disability_percent": None,
        "land_ownership": None,
        "states": [] if uk_wide else list(nations or []),
        "countries": ["United Kingdom"],
        "nationwide": uk_wide,
        "notes": notes,
        "verify": verify,
        "verify_notes": verify_notes,
        "implies_low_income": implies_low_income,
    }
    if maternity_required:
        r["maternity_required"] = True
    return r


def scheme(id, name, desc, benefits, documents, how, apply_url, official, office, tags, erules) -> dict:
    tag_list = ["united_kingdom"] + [NATION_TAG[n] for n in erules["states"]]
    for t in tags:
        if t not in tag_list:
            tag_list.append(t)
    assert not ({"central", "nationwide", "federal"} & set(tag_list)), id
    return {
        "id": id,
        "scheme_name": L(name),
        "description": L(desc),
        "eligibility_rules": erules,
        "benefits": L(benefits),
        "required_documents": docs(documents),
        "how_to_apply": L(how),
        "apply_url": apply_url,
        "official_source_url": official,
        "last_verified": LAST,
        "office_type": office,
        "tags": tag_list,
    }


ADDS: list[dict] = []
A = ADDS.append

# ------------------------------------------------------------------ UK-wide
A(scheme(
    "gb-universal-credit",
    "Universal Credit",
    "Monthly means-tested payment to help with living costs for people on a low income, out of work, or unable to work, including help with housing and childcare costs.",
    "2026-27 standard allowance per month: single under 25 £338.58; single 25 or over £424.90; joint claimants both under 25 £528.34; joint claimants one or both 25 or over £666.97. Extra amounts may be added for children, disability or health conditions, caring, housing and childcare costs.",
    ID_DOCS + ["Address and housing costs (rent agreement)", "Income, savings and childcare cost details"],
    "Apply online on GOV.UK (England, Scotland, Wales). In Northern Ireland apply through nidirect.",
    "https://www.gov.uk/universal-credit/how-to-claim",
    "https://www.gov.uk/universal-credit",
    DWP,
    ["income_support", "cash_assistance", "housing", "children", "low-income", "dwp"],
    rules(
        nations=None, min_age=18, max_age=65, implies_low_income=True,
        notes="Means-tested. Usually 18 or over (some 16-17 year olds can claim), under State Pension age (currently 66), living in the UK, and you (and your partner) have £16,000 or less in money, savings and investments. Amount depends on income and circumstances (earnings taper). " + NI_NOTE,
        verify_notes="No single annual income ceiling on GOV.UK — award tapers with earnings; £16,000 capital limit is official. implies_low_income soft gate (UK £60,000 heuristic) applies because no numeric max is encoded. 16-17 exceptions and mixed-age couples: confirm on GOV.UK.",
    ),
))
A(scheme(
    "gb-child-benefit",
    "Child Benefit",
    "Weekly payment for anyone responsible for a child under 16 (or under 20 if they stay in approved education or training). Not means-tested; there is no income limit to claim.",
    "2026-27: £27.05 a week for the eldest or only child; £17.90 a week for each additional child. Claiming also protects National Insurance credits towards State Pension for a non-working parent.",
    ["Child's birth or adoption certificate", "National Insurance number", "Bank details"],
    "Claim online or by form on GOV.UK (HMRC). Claim within 3 months of the birth to avoid losing backdated payments.",
    "https://www.gov.uk/child-benefit/how-to-claim",
    "https://www.gov.uk/child-benefit",
    HMRC,
    ["children", "universal", "middle-class", "upper-middle-class", "high-income-eligible", "hmrc"],
    rules(
        nations=None,
        notes="No income limit to claim. High Income Child Benefit Charge: if your (or your partner's) individual adjusted net income is over £60,000 you repay 1% of the Child Benefit for every £200 over £60,000; fully repaid at £80,000 or more. You can still claim (for NI credits) and opt out of payments.",
        verify_notes="Non-means-tested: max_annual_income null and implies_low_income false by design. HICBC thresholds (£60k/£80k individual adjusted net income) from gov.uk/child-benefit-tax-charge.",
    ),
))
A(scheme(
    "gb-tax-free-childcare",
    "Tax-Free Childcare",
    "Government top-up on money paid into a childcare account for approved childcare, for working parents across the UK.",
    "For every £8 you pay in, the government adds £2 — up to £2,000 a year per child (£4,000 if the child is disabled), in quarterly amounts of up to £500 (£1,000 if disabled).",
    ["National Insurance number", "Unique Taxpayer Reference (if self-employed)", "Child's details"],
    "Apply online on GOV.UK for a childcare account; reconfirm eligibility every 3 months.",
    "https://www.gov.uk/tax-free-childcare/apply-for-tax-free-childcare",
    "https://www.gov.uk/tax-free-childcare",
    HMRC,
    ["children", "child_care", "middle-class", "upper-middle-class", "high-income-eligible", "hmrc"],
    rules(
        nations=None,
        notes="Child aged 11 or under (16 or under if disabled). You (and your partner) must be working and expect to earn at least the minimum threshold (about 16 hours a week at National Minimum/Living Wage) over the next 3 months, and each of you must have adjusted net income of £100,000 or less. Cannot be used at the same time as Universal Credit childcare costs or childcare vouchers.",
        verify_notes="£100,000 is a per-parent adjusted-net-income limit, not a household cap — left in notes (max_annual_income null). Middle- and higher-income working families qualify.",
    ),
))
A(scheme(
    "gb-new-state-pension",
    "New State Pension",
    "Regular payment from the government once you reach State Pension age, based on your National Insurance record. Not means-tested.",
    "2026-27 full new State Pension: £241.30 a week. You usually need 10 qualifying years on your National Insurance record to get any, and 35 qualifying years for the full amount.",
    ["National Insurance number", "Bank details", "State Pension invitation letter / code (if sent)"],
    "Claim online on GOV.UK (you should get a letter about 2 months before State Pension age), by phone or by post. Northern Ireland: Northern Ireland Pension Centre via nidirect.",
    "https://www.gov.uk/get-state-pension",
    "https://www.gov.uk/new-state-pension",
    DWP,
    ["pension", "elderly", "universal", "middle-class", "upper-middle-class", "high-income-eligible", "dwp"],
    rules(
        nations=None, min_age=66,
        notes="Men born on or after 6 April 1951 and women born on or after 6 April 1953. State Pension age is currently 66 and rising to 67 (check your date on GOV.UK). Amount depends on your National Insurance record; income and savings do not matter. State Pension is taxable income.",
        verify_notes="Not means-tested. min_age 66 reflects current State Pension age; the phased rise to 67 means the exact date depends on birth date — confirm on gov.uk/state-pension-age.",
    ),
))
A(scheme(
    "gb-pension-credit",
    "Pension Credit",
    "Means-tested top-up for people over State Pension age on a low income. It also unlocks other help such as Winter Fuel Payment, Cold Weather Payments, Housing Benefit and a free TV licence for over-75s.",
    "2026-27 Guarantee Credit tops weekly income up to £238.00 (single) or £363.25 (couple). Extra amounts: severe disability £86.05/week, carer £48.15/week, children £69.98 per child (£81.07 for a first child born before 6 April 2017). Savings Credit may apply if you reached State Pension age before 6 April 2016.",
    ID_DOCS + ["Details of income, savings and investments", "Housing costs"],
    "Apply online, by phone or by post on GOV.UK from up to 4 months before State Pension age; can be backdated up to 3 months. Northern Ireland: apply through nidirect.",
    "https://www.gov.uk/pension-credit/how-to-claim",
    "https://www.gov.uk/pension-credit",
    DWP,
    ["pension", "elderly", "income_support", "low-income", "dwp"],
    rules(
        nations=None, min_age=66, implies_low_income=True,
        notes="You (and any partner) must have reached State Pension age and live in the UK; weekly income below the Guarantee Credit amounts (£238 single / £363.25 couple) before extra amounts. " + NI_NOTE,
        verify_notes="Official weekly income thresholds kept in notes rather than a hard annual cap because disregards and extra amounts change the figure; implies_low_income soft gate (UK £60,000 heuristic) applies. Northern Ireland page: nidirect.gov.uk/articles/understanding-pension-credit.",
    ),
))
A(scheme(
    "gb-help-to-save",
    "Help to Save",
    "Government savings account with a 50% bonus for people on Universal Credit who are working.",
    "Save £1 to £50 a month. After 2 years you get a bonus of 50% of your highest balance, and another 50% bonus after 4 years on the increase — up to £1,200 in bonuses over 4 years.",
    ["Government Gateway login", "Bank account details for deposits"],
    "Apply online on GOV.UK (HMRC) with your Government Gateway account.",
    "https://www.gov.uk/get-help-savings-low-income/how-to-apply",
    "https://www.gov.uk/get-help-savings-low-income",
    HMRC,
    ["savings", "low-income", "hmrc"],
    rules(
        nations=None, implies_low_income=True,
        notes="You must be receiving Universal Credit and you (with your partner if a joint claim) had take-home pay of £1 or more in your last monthly assessment period, and live in the UK.",
        verify_notes="Eligibility is linked to receiving Universal Credit (itself means-tested); no separate income figure. implies_low_income soft gate applies.",
    ),
))
A(scheme(
    "gb-lifetime-isa",
    "Lifetime ISA (25% government bonus)",
    "Tax-free savings account for a first home (up to £450,000) or later life, with a 25% government bonus. Open to any income level.",
    "Save up to £4,000 each tax year until age 50; the government adds a 25% bonus (up to £1,000 a year). Counts towards the £20,000 annual ISA allowance. Withdrawals for other reasons (before 60, not terminally ill) have a 25% charge.",
    ["National Insurance number", "Proof of identity (provider requirement)"],
    "Open through a bank, building society or investment provider that offers Lifetime ISAs (see GOV.UK).",
    "https://www.gov.uk/lifetime-isa",
    "https://www.gov.uk/lifetime-isa",
    HMRC,
    ["savings", "housing", "first_home", "universal", "middle-class", "upper-middle-class", "high-income-eligible", "hmrc"],
    rules(
        nations=None, min_age=18, max_age=39,
        notes="Must be 18 or over but under 40 to open; UK resident. No income limit. First-home use: property £450,000 or less, first-time buyer, buying with a mortgage, account open at least 12 months.",
        verify_notes="Not means-tested (max_annual_income null). Age 18-39 applies to opening the account; contributions allowed until 50.",
    ),
))
A(scheme(
    "gb-junior-isa",
    "Junior ISA",
    "Long-term tax-free savings account for children, opened by a parent or guardian. No income limit.",
    "2026-27 limit: up to £9,000 a year can be paid in, free of tax on interest, dividends and gains. The child can take control at 16 and withdraw at 18.",
    ["Child's details", "Parent/guardian identity (provider requirement)"],
    "Open through a Junior ISA provider (bank, building society or investment platform) — see GOV.UK.",
    "https://www.gov.uk/junior-individual-savings-accounts",
    "https://www.gov.uk/junior-individual-savings-accounts",
    HMRC,
    ["children", "savings", "universal", "middle-class", "upper-middle-class", "high-income-eligible", "hmrc"],
    rules(
        nations=None,
        notes="Child must be under 18 and living in the UK (Crown servant exceptions). Only parents/guardians with parental responsibility can open it. Cannot hold alongside a Child Trust Fund (transfer instead).",
        verify_notes="Not means-tested; profile income not used.",
    ),
))
A(scheme(
    "gb-isa-allowance",
    "Individual Savings Account (ISA) tax-free allowance",
    "Save or invest up to the annual ISA allowance with no tax on interest, dividends or capital gains. Available to all UK residents aged 18 or over.",
    "2026-27: up to £20,000 across cash, stocks and shares, innovative finance and Lifetime ISAs. No tax on ISA interest, income or gains, and nothing to declare on a tax return.",
    ["National Insurance number", "Proof of identity (provider requirement)"],
    "Open an ISA with a bank, building society or investment provider (see GOV.UK).",
    "https://www.gov.uk/individual-savings-accounts",
    "https://www.gov.uk/individual-savings-accounts",
    HMRC,
    ["tax", "savings", "universal", "middle-class", "upper-middle-class", "high-income-eligible", "hmrc"],
    rules(
        nations=None, min_age=18,
        notes="Must be 18 or over and UK resident (or Crown servant / armed forces abroad). No income limit.",
        verify_notes="Universal tax relief — max_annual_income null, implies_low_income false.",
    ),
))
A(scheme(
    "gb-marriage-allowance",
    "Marriage Allowance",
    "Lets a lower-earning spouse or civil partner transfer £1,260 of their Personal Allowance to a basic-rate taxpayer partner.",
    "Reduces the partner's tax by up to £252 a year; can be backdated to 6 April 2022.",
    ["Both partners' National Insurance numbers", "Proof of identity (Government Gateway)"],
    "Apply online on GOV.UK; the lower earner applies.",
    "https://www.gov.uk/apply-marriage-allowance",
    "https://www.gov.uk/marriage-allowance",
    HMRC,
    ["tax", "marriage", "middle-class", "hmrc"],
    rules(
        nations=None,
        notes="Married or in a civil partnership; the lower earner has income under the £12,570 Personal Allowance; the other partner pays Income Tax at the basic rate (income £12,571-£50,270; in Scotland starter/basic/intermediate rate, usually up to £43,662). Not available with Married Couple's Allowance.",
        verify_notes="Income bands are per-partner tax-band conditions, not a household cap — kept in notes, max_annual_income null.",
    ),
))
A(scheme(
    "gb-maternity-allowance",
    "Maternity Allowance",
    "Weekly payment for pregnant people and new parents who cannot get Statutory Maternity Pay, for example because they are self-employed or recently changed jobs.",
    "Up to 39 weeks of payments (standard rate or 90% of average weekly earnings, whichever is lower); up to 14 weeks in some unpaid family-business cases.",
    ["MATB1 maternity certificate", "Proof of earnings (payslips / SMP1 form)", "National Insurance number"],
    "Claim with form MA1 on GOV.UK once you have been pregnant for 26 weeks. Northern Ireland: claim through nidirect.",
    "https://www.gov.uk/maternity-allowance/how-to-claim",
    "https://www.gov.uk/maternity-allowance",
    DWP,
    ["maternity", "women", "employment", "dwp"],
    rules(
        nations=None, maternity_required=True,
        notes="Employed or registered self-employed for at least 26 of the 66 weeks before the baby is due; if employed, earning (or classed as earning) £30 a week or more in at least 13 of those weeks. " + NI_NOTE,
        verify_notes="Work and earnings test, not means-tested. Weekly standard rate for 2026-27 not restated here — confirm on GOV.UK.",
    ),
))
A(scheme(
    "gb-pension-tax-relief",
    "Pension tax relief (private and workplace pensions)",
    "Income Tax relief on contributions to registered private and workplace pensions, at your highest rate of Income Tax.",
    "Tax relief on contributions up to 100% of earnings, subject to the £60,000 annual allowance (tapered for very high incomes). Basic-rate relief is added automatically in relief-at-source schemes; higher and additional-rate taxpayers can claim the extra through Self Assessment or HMRC.",
    ["Pension provider statements", "Self Assessment return (for higher-rate relief)"],
    "Relief is given through your employer or pension scheme; claim extra higher-rate relief via Self Assessment or by contacting HMRC (see GOV.UK).",
    "https://www.gov.uk/tax-on-your-private-pension/pension-tax-relief",
    "https://www.gov.uk/tax-on-your-private-pension",
    HMRC,
    ["tax", "pension", "savings", "universal", "middle-class", "upper-middle-class", "high-income-eligible", "hmrc"],
    rules(
        nations=None,
        notes="UK taxpayers under 75 contributing to a registered pension scheme. Annual allowance £60,000 or 100% of earnings; tapered annual allowance for high adjusted incomes (see GOV.UK).",
        verify_notes="Universal tax relief; value rises with income — max_annual_income null by design.",
    ),
))

# ------------------------------------------------------ multi-nation (GB / E+W+NI)
A(scheme(
    "gb-personal-independence-payment",
    "Personal Independence Payment (PIP)",
    "Extra money for people aged 16 to State Pension age with a long-term physical or mental health condition or disability that affects daily living or mobility. Not means-tested.",
    "2026-27 weekly: daily living £76.70 (standard) or £114.60 (enhanced); mobility £30.30 (standard) or £80.00 (enhanced).",
    ["National Insurance number", "Details of GP and health professionals", "Medication and treatment details", "Bank details"],
    "Start a claim by phone with DWP (or by post), then complete the 'How your disability affects you' form. Northern Ireland: claim through nidirect.",
    "https://www.gov.uk/pip/how-to-claim",
    "https://www.gov.uk/pip",
    DWP,
    ["disability", "health", "universal", "middle-class", "dwp"],
    rules(
        nations=[E, W, NI], min_age=16, max_age=65, disability_required=True,
        notes="Aged 16 or over and under State Pension age; long-term condition expected to last 12 months or more; difficulty with daily living or mobility. Not affected by income or savings; you can work. Scotland: apply for Adult Disability Payment instead. " + NI_NOTE,
        verify_notes="Not means-tested (no income cap). Northern Ireland route: nidirect.gov.uk/articles/personal-independence-payment-pip.",
    ),
))
A(scheme(
    "gb-dla-children",
    "Disability Living Allowance (DLA) for children",
    "Tax-free payment for children under 16 who need extra care or have walking difficulties because of a disability or health condition. Not means-tested.",
    "2026-27 weekly: care component £30.30, £76.70 or £114.60; mobility component £30.30 or £80.00 — between £30.30 and £194.60 a week in total.",
    ["Child's details and medical information", "Parent/guardian National Insurance number", "Bank details"],
    "Claim with form DLA1A from GOV.UK. Northern Ireland: claim through nidirect.",
    "https://www.gov.uk/disability-living-allowance-children/how-to-claim",
    "https://www.gov.uk/disability-living-allowance-children",
    DWP,
    ["disability", "children", "health", "universal", "dwp"],
    rules(
        nations=[E, W, NI], disability_required=True,
        notes="Child under 16 whose care or mobility needs are substantially greater than other children of the same age, for at least 3 months and expected to last at least 6 months. A parent or guardian claims for the child. Scotland: Child Disability Payment instead. " + NI_NOTE,
        verify_notes="The profile 'disability' flag is used as the household disability signal (a parent claims for the child). Not means-tested.",
    ),
))
A(scheme(
    "gb-carers-allowance",
    "Carer's Allowance",
    "Weekly payment for people who care for someone at least 35 hours a week, where the person cared for gets a qualifying disability benefit.",
    "2026-27: £86.45 a week. Also gives National Insurance credits.",
    ["Your National Insurance number", "Cared-for person's National Insurance number and benefit details", "Earnings details", "Bank details"],
    "Apply online on GOV.UK. Northern Ireland: claim through nidirect.",
    "https://www.gov.uk/carers-allowance/how-to-claim",
    "https://www.gov.uk/carers-allowance",
    DWP,
    ["carer", "disability", "dwp"],
    rules(
        nations=[E, W, NI], min_age=16,
        notes="Aged 16 or over; caring 35+ hours a week; not in full-time education; earnings of £204 a week or less after deductions. The person you care for must get a qualifying benefit (e.g. PIP daily living, Attendance Allowance, DLA middle/highest care). Scotland: Carer Support Payment instead. " + NI_NOTE,
        verify_notes="The £204/week earnings limit is an earnings condition, not a household means test — kept in notes. Savings do not count.",
    ),
))
A(scheme(
    "gb-attendance-allowance",
    "Attendance Allowance",
    "Extra money for people over State Pension age with a disability or illness who need help with personal care or supervision. Not means-tested.",
    "2026-27 weekly: lower rate £76.70; higher rate £114.60 (for example, care needed day and night, or terminal illness).",
    ["National Insurance number", "GP / health professional details", "Bank details"],
    "Claim by form or online on GOV.UK. Northern Ireland: claim through nidirect.",
    "https://www.gov.uk/attendance-allowance/how-to-claim",
    "https://www.gov.uk/attendance-allowance",
    DWP,
    ["disability", "elderly", "health", "universal", "middle-class", "dwp"],
    rules(
        nations=[E, W, NI], min_age=66, disability_required=True,
        notes="State Pension age or over; needed help for at least 6 months (unless terminally ill). Income and savings do not matter. Scotland: Pension Age Disability Payment instead. " + NI_NOTE,
        verify_notes="Not means-tested. min_age tracks current State Pension age (66).",
    ),
))
A(scheme(
    "gb-winter-fuel-payment",
    "Winter Fuel Payment",
    "Annual tax-free payment to help older people with heating costs for winter 2026 to 2027.",
    "£200 or £300 per household (£100 or £150 each if shared with another eligible person), usually paid automatically in November or December 2026.",
    ["Usually none — paid automatically if you get State Pension or another qualifying benefit"],
    "Usually automatic. If you do not get it automatically, claim on GOV.UK (England and Wales) or nidirect (Northern Ireland).",
    "https://www.gov.uk/winter-fuel-payment/how-to-claim",
    "https://www.gov.uk/winter-fuel-payment",
    DWP,
    ["energy", "elderly", "universal", "middle-class", "dwp"],
    rules(
        nations=[E, W, NI], min_age=66,
        notes="Born on or before 27 June 1960 and living in England, Wales or Northern Ireland in the qualifying week of 21-27 September 2026. If your individual taxable income is over £35,000, HMRC recovers the payment through the tax system (you can opt out). Scotland: Pension Age Winter Heating Payment instead.",
        verify_notes="Not means-tested at award; the £35,000 individual-income recovery is a tax clawback, not an eligibility cap — kept in notes (max_annual_income null).",
    ),
))
A(scheme(
    "gb-cold-weather-payment",
    "Cold Weather Payment",
    "Automatic £25 payment for each 7-day period of very cold weather for people on certain low-income benefits.",
    "£25 for each 7-day period when the average temperature is 0°C or below, between 1 November 2026 and 31 March 2027.",
    ["None — paid automatically"],
    "Paid automatically into the account your benefit is paid into — no claim needed.",
    "https://www.gov.uk/cold-weather-payment",
    "https://www.gov.uk/cold-weather-payment",
    DWP,
    ["energy", "low-income", "dwp"],
    rules(
        nations=[E, W], implies_low_income=True,
        notes="Getting Pension Credit, income-related ESA (work-related activity or support group, or with certain premiums), Universal Credit (you and any partner not employed or gainfully self-employed, plus other conditions), or Support for Mortgage Interest. Not available in Scotland (Winter Heating Payment instead). Northern Ireland runs its own arrangements via nidirect (not encoded here).",
        verify_notes="Benefit-linked (means-tested). NI version not verified this pass, so nations are limited to England and Wales.",
    ),
))
A(scheme(
    "gb-sure-start-maternity-grant",
    "Sure Start Maternity Grant",
    "One-off £500 payment towards the costs of a first baby for families on certain benefits.",
    "£500 one-off payment (usually for the first child, or for multiple births); does not need to be repaid.",
    ["Form SF100", "Proof of pregnancy or birth (health professional signature)", "Benefit details"],
    "Claim with form SF100 from 11 weeks before the due date up to 6 months after the birth (GOV.UK).",
    "https://www.gov.uk/sure-start-maternity-grant/how-to-claim",
    "https://www.gov.uk/sure-start-maternity-grant",
    DWP,
    ["maternity", "children", "low-income", "dwp"],
    rules(
        nations=[E, W], maternity_required=True, implies_low_income=True,
        notes="You or your partner get income-related ESA, Pension Credit or Universal Credit (or a Support for Mortgage Interest loan); usually no other children under 16 (exceptions for multiple births and some other cases). Scotland: Best Start Grant Pregnancy and Baby Payment instead. Northern Ireland has its own grant via nidirect (not encoded here).",
        verify_notes="Benefit-linked (means-tested).",
    ),
))
A(scheme(
    "gb-healthy-start",
    "Healthy Start",
    "Prepaid card to buy milk, fruit, vegetables, pulses and infant formula, plus free vitamins, for pregnant people and families with young children on low incomes.",
    "Money loaded every 4 weeks onto a Healthy Start card for healthy food and milk, plus free Healthy Start vitamins (amounts on the NHS Healthy Start website).",
    ["National Insurance number", "Benefit details", "Due date or child's date of birth"],
    "Apply online through the NHS Healthy Start service linked from GOV.UK.",
    "https://www.healthystart.nhs.uk/",
    "https://www.gov.uk/healthy-start",
    "NHS Business Services Authority (Department of Health and Social Care)",
    ["food", "children", "maternity", "health", "low-income"],
    rules(
        nations=[E, W, NI], implies_low_income=True,
        notes="More than 10 weeks pregnant or have a child under 4, and claiming a qualifying benefit (for example Universal Credit with family take-home pay of £408 or less a month). Under-18s who are more than 10 weeks pregnant qualify without benefits. Scotland: Best Start Foods instead.",
        verify_notes="The £408/month take-home figure applies to the UC route; not encoded as a hard cap. Apply URL is the NHS BSA Healthy Start service (official NHS).",
    ),
))
A(scheme(
    "gb-warm-home-discount",
    "Warm Home Discount",
    "One-off £150 discount off the electricity bill for households on certain means-tested benefits (winter 2026 to 2027).",
    "£150 off your electricity bill (or sometimes gas), applied by your supplier — the money is not paid to you.",
    ["Usually none — applied automatically in England and Wales"],
    "England and Wales: usually automatic. Scotland: automatic for the 'core group', otherwise apply to your energy supplier. The scheme reopens in October 2026.",
    "https://www.gov.uk/the-warm-home-discount-scheme",
    "https://www.gov.uk/the-warm-home-discount-scheme",
    "Department for Energy Security and Net Zero (DESNZ)",
    ["energy", "utility", "low-income"],
    rules(
        nations=[E, W, S], implies_low_income=True,
        notes="Conditions on 23 August 2026: your supplier is in the scheme; your name (or your partner's) is on the electricity bill; England and Wales — you or your partner get Universal Credit, Housing Benefit, income-related ESA or Pension Credit. Scotland — core group (e.g. Pension Credit, some UC/ESA cases) or your supplier's broader group. Not available in Northern Ireland.",
        verify_notes="Scheme closed at time of check and reopens October 2026 for winter 2026-27 (eligibility date 23 August 2026 per GOV.UK). Benefit-linked.",
    ),
))
A(scheme(
    "gb-disabled-facilities-grant",
    "Disabled Facilities Grant",
    "Council grant for changes to a disabled person's home, such as ramps, stairlifts, level-access showers or extensions.",
    "Up to £30,000 in England, £36,000 in Wales and £25,000 in Northern Ireland (some councils give more). Amount depends on household income and savings over £6,000; disabled children under 18 are assessed without parents' income.",
    ["Proof of disability / occupational therapist assessment", "Proof of ownership or tenancy", "Income and savings details"],
    "Apply to your local council (England and Wales) or through the Housing Executive (Northern Ireland) — see GOV.UK.",
    "https://www.gov.uk/disabled-facilities-grants/how-to-claim",
    "https://www.gov.uk/disabled-facilities-grants",
    LA,
    ["disability", "housing", "home_adaptation", "grant"],
    rules(
        nations=[E, W, NI], disability_required=True,
        notes="Owner-occupiers, tenants and landlords with a disabled occupant who intends to live there for the grant period (usually 5 years). Means-tested for adults (household income; savings over £6,000); not for disabled children under 18. Not available in Scotland.",
        verify_notes="Means test is council-run with no single national figure, so implies_low_income is NOT set (children's grants are not means-tested).",
    ),
))
A(scheme(
    "gb-access-to-work",
    "Access to Work",
    "Grant to pay for practical support at work if you have a disability or a physical or mental health condition — equipment, support workers, travel to work, communication support.",
    "Grant amount depends on your needs (for example specialist equipment, a BSL interpreter, or taxi fares if you cannot use public transport); it does not need to be repaid and does not affect other benefits.",
    ["National Insurance number", "Workplace and employer contact details", "Details of your condition and the support needed"],
    "Check eligibility and apply online on GOV.UK.",
    "https://www.gov.uk/access-to-work/apply",
    "https://www.gov.uk/access-to-work",
    DWP,
    ["disability", "employment", "grant", "universal", "dwp"],
    rules(
        nations=[E, W, S], min_age=16, disability_required=True,
        notes="Aged 16 or over, in or about to start paid work (including self-employment), living in England, Scotland or Wales. Not means-tested. Northern Ireland has a separate Access to Work scheme (not encoded here).",
        verify_notes="Not means-tested.",
    ),
))
A(scheme(
    "gb-blue-badge",
    "Blue Badge (disabled parking)",
    "Parking permit that lets disabled people park closer to where they need to go.",
    "Park on streets with parking restrictions and in disabled bays. Costs up to £10 in England, up to £20 in Scotland, and is free in Wales.",
    ["Proof of identity and address", "Recent photo", "Proof of benefit or medical evidence", "National Insurance number"],
    "Apply online through the GOV.UK Blue Badge service (your council decides).",
    "https://www.gov.uk/apply-blue-badge",
    "https://www.gov.uk/apply-blue-badge",
    LA,
    ["disability", "transport", "universal"],
    rules(
        nations=[E, S, W], disability_required=True,
        notes="Automatic eligibility with certain benefits (e.g. PIP mobility, higher-rate DLA mobility); otherwise assessed by the council. Northern Ireland runs a separate Blue Badge service via nidirect.",
        verify_notes="Not means-tested.",
    ),
))
A(scheme(
    "gb-council-tax-reduction",
    "Council Tax Reduction",
    "Council scheme that reduces Council Tax bills — by up to 100% — for people on a low income or claiming certain benefits.",
    "Reduction of up to 100% of your Council Tax bill depending on your council's scheme, your income and circumstances.",
    ["Proof of income and savings", "Council Tax account number", "Benefit details"],
    "Apply to your local council (GOV.UK postcode lookup).",
    "https://www.gov.uk/apply-council-tax-reduction",
    "https://www.gov.uk/apply-council-tax-reduction",
    LA,
    ["housing", "tax", "low-income", "council_tax"],
    rules(
        nations=[E, S, W], implies_low_income=True,
        notes="Means-tested; each council sets its own scheme for working-age people in England (Scotland and Wales have national schemes run by councils; pensioners have a national scheme). Northern Ireland uses domestic rates, not Council Tax.",
        verify_notes="No national income ceiling — implies_low_income soft gate applies.",
    ),
))
A(scheme(
    "gb-council-tax-single-person-discount",
    "Council Tax single person discount (25%)",
    "25% off the Council Tax bill if you live on your own or everyone else in the home is 'disregarded' (for example full-time students). Not means-tested.",
    "25% reduction in Council Tax (50% if everyone in the home is disregarded).",
    ["Council Tax account number", "Proof of who lives at the address (if asked)"],
    "Apply to your local council (GOV.UK).",
    "https://www.gov.uk/council-tax/who-has-to-pay",
    "https://www.gov.uk/council-tax",
    LA,
    ["housing", "tax", "council_tax", "universal", "middle-class", "upper-middle-class", "high-income-eligible"],
    rules(
        nations=[E, W], min_age=18,
        notes="You pay Council Tax and live alone, or everyone else in your home is disregarded (under 18, full-time students, certain apprentices, severely mentally impaired, live-in carers and others). Any income level. Scotland has its own single person discount rules.",
        verify_notes="Universal discount — income not relevant.",
    ),
))
A(scheme(
    "gb-budgeting-loan",
    "Budgeting Loan",
    "Interest-free loan for essentials such as furniture, clothes, rent in advance or moving costs, for people who have been on certain benefits for 6 months.",
    "Borrow from £100 up to £348 (single), £464 (with a partner) or £812 (if you or your partner get Child Benefit); repaid from your benefits with no interest.",
    ["National Insurance number", "Benefit details"],
    "Apply online or with form SF500 on GOV.UK. Universal Credit claimants apply for a Budgeting Advance instead.",
    "https://www.gov.uk/budgeting-help-benefits/how-to-apply",
    "https://www.gov.uk/budgeting-help-benefits",
    DWP,
    ["loan", "low-income", "dwp"],
    rules(
        nations=[E, S, W], implies_low_income=True,
        notes="Getting Income Support, income-based JSA, income-related ESA or Pension Credit for the past 6 months. Not available if you currently get Universal Credit (use a Budgeting Advance). Savings over £1,000 (£2,000 if 63 or over) reduce the amount. Northern Ireland has a different scheme.",
        verify_notes="Benefit-linked (means-tested).",
    ),
))
A(scheme(
    "gb-sdlt-first-time-buyer-relief",
    "Stamp Duty Land Tax first-time buyer relief",
    "Reduced Stamp Duty for first-time buyers purchasing a home worth £500,000 or less in England or Northern Ireland. Not means-tested.",
    "No SDLT on the first £300,000; 5% on the portion from £300,001 to £500,000. No relief if the price is over £500,000.",
    ["Your solicitor or conveyancer handles the SDLT return"],
    "Claimed on the SDLT return, usually by your solicitor or conveyancer (GOV.UK).",
    "https://www.gov.uk/stamp-duty-land-tax/residential-property-rates",
    "https://www.gov.uk/stamp-duty-land-tax",
    HMRC,
    ["tax", "housing", "first_home", "universal", "middle-class", "upper-middle-class", "hmrc"],
    rules(
        nations=[E, NI],
        notes="You and anyone you buy with are first-time buyers (never owned a home anywhere) and will live in the property; purchase price £500,000 or less. Scotland uses LBTT and Wales uses LTT (different taxes).",
        verify_notes="Property-price condition, not income — max_annual_income null.",
    ),
))
A(scheme(
    "gb-boiler-upgrade-scheme",
    "Boiler Upgrade Scheme",
    "Grant towards replacing fossil-fuel heating with a heat pump or biomass boiler. Not means-tested.",
    "£7,500 off an air source or ground source heat pump; £5,000 off a biomass boiler; £2,500 off an air-to-air heat pump (with an extra £1,500 until March 2027 for homes switching from oil or LPG, per GOV.UK). The installer applies and deducts the grant.",
    ["Valid Energy Performance Certificate (EPC)", "Installer quote"],
    "Find an MCS-certified installer, who applies for the grant on your behalf (GOV.UK).",
    "https://www.gov.uk/apply-boiler-upgrade-scheme",
    "https://www.gov.uk/apply-boiler-upgrade-scheme",
    "Ofgem / Department for Energy Security and Net Zero",
    ["energy", "housing", "green", "grant", "universal", "middle-class", "upper-middle-class", "high-income-eligible"],
    rules(
        nations=[E, W],
        notes="Property owners (homeowners, landlords, small businesses) in England or Wales replacing fossil-fuel heating; valid EPC; installation by an MCS-certified installer. No income test.",
        verify_notes="Not means-tested. Air-to-air and oil/LPG top-up details: confirm on GOV.UK at application.",
    ),
))

# ------------------------------------------------------------------ England
A(scheme(
    "gb-eng-free-childcare-working-parents",
    "Free childcare for working parents (England, up to 30 hours)",
    "Up to 30 hours a week of funded childcare for working parents of children aged 9 months to 4 years in England.",
    "Up to 30 hours of free childcare a week for 38 weeks a year (can be spread over more weeks with fewer hours) at an approved provider.",
    ["National Insurance number", "Unique Taxpayer Reference (if self-employed)", "Child's details"],
    "Apply online through the childcare service on GOV.UK (from when your child is 23 weeks old); reconfirm every 3 months and give the code to your provider.",
    "https://www.gov.uk/free-childcare-if-working/apply-for-free-childcare-if-youre-working",
    "https://www.gov.uk/free-childcare-if-working",
    DFE,
    ["children", "child_care", "middle-class", "upper-middle-class"],
    rules(
        nations=[E],
        notes="Child aged 9 months to 4 years (until school). You (and your partner) usually work and each expect to earn at least the minimum threshold (about 16 hours a week at National Minimum/Living Wage) over the next 3 months, and each has adjusted net income of £100,000 or less.",
        verify_notes="£100,000 is per parent, not a household cap — max_annual_income null.",
    ),
))
A(scheme(
    "gb-eng-15-hours-3-4-year-olds",
    "15 hours free early education for all 3 and 4 year olds (England)",
    "Universal free early education for every 3 and 4 year old in England, regardless of income or work.",
    "570 hours a year (usually 15 hours a week for 38 weeks) at an approved nursery, pre-school or childminder.",
    ["Child's birth certificate or proof of age (provider may ask)"],
    "Contact an approved childcare provider or your local council; it starts the term after your child turns 3.",
    "https://www.gov.uk/help-with-childcare-costs/free-childcare-and-education-for-3-to-4-year-olds",
    "https://www.gov.uk/help-with-childcare-costs/free-childcare-and-education-for-3-to-4-year-olds",
    DFE,
    ["children", "child_care", "education", "universal"],
    rules(
        nations=[E],
        notes="All 3 and 4 year olds in England from the term after their 3rd birthday. Some 2 year olds also qualify if the family gets certain support. No income test for 3-4 year olds.",
        verify_notes="Universal entitlement.",
    ),
))
A(scheme(
    "gb-eng-free-school-meals",
    "Free school meals (England)",
    "Free school lunches for children in England from families on Universal Credit and other qualifying support, plus universal infant free school meals.",
    "Free lunch every school day. All children in reception, year 1 and year 2 at state schools get free meals regardless of income.",
    ["National Insurance number", "Benefit details", "Child's school details"],
    "Apply through your local council (GOV.UK postcode lookup).",
    "https://www.gov.uk/apply-free-school-meals",
    "https://www.gov.uk/apply-free-school-meals",
    LA,
    ["children", "education", "food", "low-income"],
    rules(
        nations=[E], implies_low_income=True,
        notes="From the 2026 to 2027 school year, children in all Universal Credit households in England can get free school meals regardless of earnings; other qualifying support includes income-related ESA, income-based JSA, Income Support and the Pension Credit guarantee element. Infant (reception to year 2) meals are universal.",
        verify_notes="Benefit-linked (means-tested) for older pupils; infant meals universal. implies_low_income soft gate applies to the means-tested route.",
    ),
))
A(scheme(
    "gb-eng-shared-ownership",
    "Shared Ownership (England)",
    "Buy a share of a home (usually 10% to 75%) and pay rent on the rest; aimed at households who cannot afford to buy outright.",
    "Buy a share with a smaller deposit and mortgage; pay reduced rent on the rest; option to buy more shares later ('staircasing'). Older People's Shared Ownership for those aged 55 or over.",
    ["Proof of income and savings", "Mortgage in principle", "Identity documents"],
    "Apply through a shared ownership provider or housing association; find homes via GOV.UK links.",
    "https://www.gov.uk/shared-ownership-scheme",
    "https://www.gov.uk/shared-ownership-scheme",
    "Ministry of Housing, Communities and Local Government / housing associations",
    ["housing", "first_home", "middle-class"],
    rules(
        nations=[E], min_age=18, max_annual_income=90000,
        notes="Household income £80,000 or less outside London, or £90,000 or less in London; first-time buyer, previously owned a home but cannot afford one now, or an existing shared owner moving. Older People's Shared Ownership: 55 or over.",
        verify_notes="max_annual_income encodes the official London household cap (£90,000); outside London the official cap is £80,000 — confirm by location. Scotland, Wales and Northern Ireland run separate schemes.",
    ),
))
A(scheme(
    "gb-eng-first-homes",
    "First Homes (England)",
    "New homes sold to local first-time buyers at a discount of at least 30% of market value.",
    "Discount of 30% to 50% off market value (price after discount no more than £250,000, or £420,000 in London).",
    ["Proof of first-time buyer status", "Proof of income", "Mortgage for at least 50% of the price"],
    "Buy through a developer or local council offering First Homes (GOV.UK).",
    "https://www.gov.uk/first-homes-scheme",
    "https://www.gov.uk/first-homes-scheme",
    "Ministry of Housing, Communities and Local Government / local councils",
    ["housing", "first_home", "middle-class"],
    rules(
        nations=[E], min_age=18, max_annual_income=90000,
        notes="18 or over, first-time buyer, buying with a mortgage for at least 50% of the price; household income £80,000 or less (£90,000 in London). Councils may add local criteria (e.g. key workers, local connection).",
        verify_notes="max_annual_income encodes the official London household cap (£90,000); £80,000 outside London. Availability depends on local developments delivering First Homes — confirm with the council.",
    ),
))
A(scheme(
    "gb-eng-right-to-buy",
    "Right to Buy (England)",
    "Lets most council tenants buy their council home at a discount.",
    "Discount of 35% (houses) or 50% (flats) after 3 to 5 years as a public-sector tenant, rising with tenancy length up to the maximum for your area (and no more than 70% of the value). The discount may have to be repaid if you sell within 5 years.",
    ["Right to Buy application form (RTB1)", "Tenancy details", "Identity documents"],
    "Send the Right to Buy application form to your landlord (GOV.UK).",
    "https://www.gov.uk/right-to-buy-buying-your-council-home",
    "https://www.gov.uk/right-to-buy-buying-your-council-home",
    LA,
    ["housing", "tenant", "first_home"],
    rules(
        nations=[E],
        notes="Secure tenant; the home is your only or main home and self-contained; public-sector landlord for at least 3 years (not necessarily in a row). Different rules in Wales, Scotland and Northern Ireland.",
        verify_notes="Right to Buy in England is under reform — confirm the current qualifying period and maximum discounts on GOV.UK before relying on figures.",
    ),
))
A(scheme(
    "gb-eng-student-finance",
    "Student finance for higher education (England)",
    "Tuition Fee Loan and Maintenance Loan for students from England at university or college, plus extra help for disabled students, parents and carers.",
    "Tuition Fee Loan paid to the university; Maintenance Loan for living costs (amount depends on household income and where you live and study). Repayments depend on earnings, not the amount owed.",
    ["National Insurance number", "Passport or identity", "Household income details (for means-tested support)"],
    "Apply online through Student Finance England (GOV.UK).",
    "https://www.gov.uk/apply-online-for-student-finance",
    "https://www.gov.uk/student-finance",
    "Student Finance England (Department for Education)",
    ["education", "college", "student", "loan", "universal", "middle-class", "upper-middle-class"],
    rules(
        nations=[E],
        notes="UK nationals or people with settled or other eligible status, normally resident in England, on an eligible course at a recognised provider. Tuition Fee Loan is not means-tested; the Maintenance Loan amount is means-tested (a minimum loan is available at any household income). Student finance is changing for courses starting on or after 1 January 2027.",
        verify_notes="All-income entitlement (non-means-tested minimum). Scotland (SAAS), Wales (Student Finance Wales) and NI (Student Finance NI) have separate systems.",
    ),
))
A(scheme(
    "gb-eng-older-persons-bus-pass",
    "Older person's bus pass (England)",
    "Free off-peak travel on local buses anywhere in England once you reach State Pension age.",
    "Free local bus travel (off-peak; some councils extend the times). In London, free travel on buses, tube and other transport from age 60 (within London).",
    ["Proof of age", "Proof of address", "Photo"],
    "Apply to your local council (GOV.UK postcode lookup).",
    "https://www.gov.uk/apply-for-elderly-person-bus-pass",
    "https://www.gov.uk/apply-for-elderly-person-bus-pass",
    LA,
    ["transport", "elderly", "universal"],
    rules(
        nations=[E], min_age=66,
        notes="England: from State Pension age (currently 66). London: free travel within London from 60. Wales, Scotland and Northern Ireland give a bus pass from 60 through their own schemes. Not means-tested.",
        verify_notes="Universal; min_age tracks State Pension age.",
    ),
))

# ----------------------------------------------------------------- Scotland
# mygov.scot is the Scottish Government's official citizen portal; Social Security
# Scotland (socialsecurity.gov.scot) links to it for eligibility and applications.
A(scheme(
    "gb-sct-scottish-child-payment",
    "Scottish Child Payment",
    "Weekly payment for each child under 16 for families in Scotland who get certain low-income benefits.",
    "£28.20 a week for each child under 16, paid every 4 weeks. No limit on the number of children.",
    ["National Insurance number", "Benefit details", "Child's details"],
    "Apply online, by phone or by post to Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/scottish-child-payment/how-to-apply",
    "https://www.mygov.scot/scottish-child-payment",
    SSS,
    ["children", "cash_assistance", "low-income"],
    rules(
        nations=[S], implies_low_income=True,
        notes="Live in Scotland; responsible for a child under 16; you or your partner get Universal Credit, income-based JSA, income-related ESA, Income Support or Pension Credit.",
        verify_notes="Benefit-linked (means-tested). mygov.scot is the Scottish Government's official citizen portal used by Social Security Scotland.",
    ),
))
A(scheme(
    "gb-sct-best-start-grant",
    "Best Start Grant (Scotland)",
    "Three one-off payments for families on certain benefits: Pregnancy and Baby Payment, Early Learning Payment and School Age Payment.",
    "Pregnancy and Baby Payment £796.65 for a first child (£398.35 for later children); Early Learning Payment when the child is 2 to 3 and a half; School Age Payment when the child is old enough to start school (amounts on mygov.scot).",
    ["National Insurance number", "Benefit details", "Due date or child's date of birth"],
    "Apply online, by phone or by post to Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/best-start-grant-best-start-foods/how-to-apply",
    "https://www.mygov.scot/best-start-grant-best-start-foods",
    SSS,
    ["children", "maternity", "education", "low-income"],
    rules(
        nations=[S], implies_low_income=True,
        notes="Live in Scotland and you or your partner get a qualifying benefit (e.g. Universal Credit, Pension Credit, income-based JSA, income-related ESA, Income Support, Housing Benefit). Pregnancy and Baby Payment: from 24 weeks pregnant until the baby is 6 months old. Under-18s, and under-20s who depend on their parents, may qualify without benefits.",
        verify_notes="Benefit-linked. Early Learning and School Age Payment amounts not restated — confirm on mygov.scot.",
    ),
))
A(scheme(
    "gb-sct-best-start-foods",
    "Best Start Foods (Scotland)",
    "Prepaid card to buy healthy food for pregnant people and children under 3 in low-income families in Scotland (replaces Healthy Start).",
    "Money loaded onto a Best Start Foods card every 4 weeks for healthy foods such as milk, fruit, vegetables, eggs and pulses (amounts on mygov.scot).",
    ["National Insurance number", "Benefit details", "Due date or child's date of birth"],
    "Apply together with Best Start Grant through Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/best-start-grant-best-start-foods/how-to-apply",
    "https://www.mygov.scot/best-start-grant-best-start-foods",
    SSS,
    ["food", "children", "maternity", "low-income"],
    rules(
        nations=[S], implies_low_income=True,
        notes="Pregnant or have a child under 3, live in Scotland and get a qualifying benefit (income limits apply for some benefits such as Universal Credit). Pregnant under-18s qualify without benefits.",
        verify_notes="Benefit-linked; earnings limits for the UC route not encoded as a hard cap.",
    ),
))
A(scheme(
    "gb-sct-adult-disability-payment",
    "Adult Disability Payment (Scotland)",
    "Scotland's replacement for PIP: extra money for people aged 16 to State Pension age with a long-term disability or health condition. Not means-tested.",
    "2026-27 weekly: daily living £76.70 (standard) or £114.60 (enhanced); mobility £30.30 (standard) or £80.00 (enhanced).",
    ["National Insurance number", "Supporting information about your condition", "Bank details"],
    "Apply online, by phone, by post or face to face with Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/adult-disability-payment/how-to-apply",
    "https://www.mygov.scot/adult-disability-payment",
    SSS,
    ["disability", "health", "universal", "middle-class"],
    rules(
        nations=[S], min_age=16, max_age=65, disability_required=True,
        notes="Live in Scotland; 16 or over and under State Pension age; long-term condition affecting daily living or mobility. Income and savings do not matter.",
        verify_notes="Not means-tested.",
    ),
))
A(scheme(
    "gb-sct-child-disability-payment",
    "Child Disability Payment (Scotland)",
    "Scotland's replacement for DLA for children: extra money for disabled children under 16. Not means-tested.",
    "2026-27 weekly care component £30.30, £76.70 or £114.60, plus a mobility component of £30.30 or £80.00 where eligible.",
    ["Child's details and supporting information", "Parent/guardian National Insurance number", "Bank details"],
    "Apply online, by phone or by post to Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/child-disability-payment/how-to-apply",
    "https://www.mygov.scot/child-disability-payment",
    SSS,
    ["disability", "children", "health", "universal"],
    rules(
        nations=[S], disability_required=True,
        notes="Child under 16 living in Scotland with care or mobility needs because of a disability or long-term condition. A parent or guardian applies. Not means-tested.",
        verify_notes="The profile 'disability' flag is used as the household disability signal (a parent claims for the child).",
    ),
))
A(scheme(
    "gb-sct-carer-support-payment",
    "Carer Support Payment (Scotland)",
    "Scotland's replacement for Carer's Allowance, for people caring for someone 35 or more hours a week.",
    "Up to £86.45 a week. Carers may also get the Scottish Carer Supplement (paid twice a year) and Carer Additional Person Payment where eligible (see mygov.scot).",
    ["Your and the cared-for person's National Insurance numbers", "Earnings details", "Bank details"],
    "Apply online, by phone or by post to Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/carer-support-payment/how-to-apply",
    "https://www.mygov.scot/carer-support-payment",
    SSS,
    ["carer", "disability"],
    rules(
        nations=[S], min_age=16,
        notes="Live in Scotland; 16 or over; caring 35+ hours a week for someone who gets a qualifying disability benefit; take-home pay of £204 a week or less. Some full-time students can apply.",
        verify_notes="Earnings condition only; savings do not count.",
    ),
))
A(scheme(
    "gb-sct-pension-age-disability-payment",
    "Pension Age Disability Payment (Scotland)",
    "Scotland's replacement for Attendance Allowance: extra money for people over State Pension age who need help because of a disability or long-term condition. Not means-tested.",
    "2026-27 weekly: lower rate £76.70; higher rate £114.60.",
    ["National Insurance number", "Supporting information", "Bank details"],
    "Apply online, by phone or by post to Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/pension-age-disability-payment/how-to-apply",
    "https://www.mygov.scot/pension-age-disability-payment",
    SSS,
    ["disability", "elderly", "health", "universal", "middle-class"],
    rules(
        nations=[S], min_age=66, disability_required=True,
        notes="Live in Scotland; State Pension age or over; care or supervision needs for at least 6 months (unless terminally ill). Income and savings do not matter.",
        verify_notes="Not means-tested.",
    ),
))
A(scheme(
    "gb-sct-pension-age-winter-heating-payment",
    "Pension Age Winter Heating Payment (Scotland)",
    "Scotland's replacement for Winter Fuel Payment: annual payment to help older people with heating costs.",
    "£105.55 to £316.70 depending on age and whether you get certain benefits; letters from November 2026, usually paid automatically.",
    ["Usually none — paid automatically"],
    "Usually automatic via Social Security Scotland (mygov.scot); contact them if you think you qualify but are not paid.",
    "https://www.mygov.scot/pension-age-winter-heating-payment",
    "https://www.mygov.scot/pension-age-winter-heating-payment",
    SSS,
    ["energy", "elderly", "universal", "middle-class"],
    rules(
        nations=[S], min_age=66,
        notes="Live in Scotland and have reached State Pension age by the qualifying week for winter 2026-27. If your individual taxable income is over £35,000, HMRC recovers the payment through tax.",
        verify_notes="Not means-tested at award; the £35,000 recovery is a tax clawback, not an eligibility cap.",
    ),
))
A(scheme(
    "gb-sct-winter-heating-payment",
    "Winter Heating Payment (Scotland)",
    "Annual £62 payment for people in Scotland on certain low-income benefits (replaces Cold Weather Payment).",
    "£62 once a year, paid automatically — whatever the weather.",
    ["None — paid automatically"],
    "Paid automatically by Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/winter-heating-payment",
    "https://www.mygov.scot/winter-heating-payment",
    SSS,
    ["energy", "low-income"],
    rules(
        nations=[S], implies_low_income=True,
        notes="Live in Scotland and get a qualifying benefit (e.g. Pension Credit, Universal Credit with conditions, income-related ESA, income-based JSA, Income Support, Support for Mortgage Interest) in the qualifying week of 2-8 November 2026.",
        verify_notes="Benefit-linked.",
    ),
))
A(scheme(
    "gb-sct-young-carer-grant",
    "Young Carer Grant (Scotland)",
    "Annual payment for young carers aged 16 to 18 in Scotland who care for someone for an average of 16 hours a week.",
    "£405.10 a year (you can apply once each year).",
    ["Your National Insurance number", "Details of the person you care for and their benefit"],
    "Apply online, by phone or by post to Social Security Scotland (mygov.scot).",
    "https://www.mygov.scot/young-carer-grant",
    "https://www.mygov.scot/young-carer-grant",
    SSS,
    ["carer", "youth"],
    rules(
        nations=[S], min_age=16, max_age=18,
        notes="Aged 16, 17 or 18; live in Scotland; care on average 16+ hours a week (over the last 3 months) for someone who gets a qualifying disability benefit; not getting Carer's Allowance or Carer Support Payment.",
        verify_notes="Not means-tested.",
    ),
))
A(scheme(
    "gb-sct-job-start-payment",
    "Job Start Payment (Scotland)",
    "One-off payment to help young people on low-income benefits with the costs of starting a job.",
    "£331.95, or £531.10 if you have children.",
    ["Job offer details", "Benefit details", "National Insurance number"],
    "Apply to Social Security Scotland within 3 months of the job offer (mygov.scot).",
    "https://www.mygov.scot/job-start-payment",
    "https://www.mygov.scot/job-start-payment",
    SSS,
    ["employment", "youth", "low-income"],
    rules(
        nations=[S], min_age=16, max_age=24, implies_low_income=True,
        notes="Aged 16-24 (up to 25 for care leavers), live in Scotland, have a job offer, and have been on a qualifying benefit (e.g. Universal Credit, income-based JSA) for 6 months before the offer.",
        verify_notes="Benefit-linked. max_age 24; care leavers up to 25 — confirm on mygov.scot.",
    ),
))
A(scheme(
    "gb-sct-funded-elc-1140",
    "Funded early learning and childcare — 1,140 hours (Scotland)",
    "1,140 hours a year of funded early learning and childcare for all 3 and 4 year olds (and eligible 2 year olds) in Scotland, regardless of parents' work status.",
    "Up to 1,140 hours a year (about 30 hours a week in term time) at a funded provider.",
    ["Child's birth certificate", "Proof of address"],
    "Apply through your local council.",
    "https://www.gov.scot/policies/early-education-and-care/early-learning-and-childcare/",
    "https://www.gov.scot/policies/early-education-and-care/early-learning-and-childcare/",
    "Scottish Government / local councils",
    ["children", "child_care", "education", "universal"],
    rules(
        nations=[S],
        notes="All 3 and 4 year olds; eligible 2 year olds (e.g. family on certain benefits, care-experienced). No income or work test for 3-4 year olds.",
        verify_notes="Universal for 3-4 year olds (gov.scot policy page).",
    ),
))
A(scheme(
    "gb-sct-free-school-lunches-p1-p5",
    "Free school lunches for P1 to P5 (Scotland)",
    "All children in primary 1 to 5 at council or Scottish Government-funded schools get free school lunches during term-time.",
    "Free school lunch every school day in P1-P5; older pupils can get free meals if the family gets certain benefits (apply to the council).",
    ["None for P1-P5; benefit proof for older pupils"],
    "Automatic for P1-P5; contact your local council for older pupils (mygov.scot).",
    "https://www.mygov.scot/primary-school-meals",
    "https://www.mygov.scot/primary-school-meals",
    "Scottish Government / local councils",
    ["children", "education", "food", "universal"],
    rules(
        nations=[S],
        notes="All P1-P5 pupils at local-authority or Scottish Government-funded schools; financial circumstances do not matter. Independent schools and home-educated children are excluded.",
        verify_notes="Universal.",
    ),
))
A(scheme(
    "gb-sct-under-22-free-bus",
    "Under 22s free bus travel (Scotland)",
    "Free bus travel across Scotland for everyone aged 5 to 21 living in Scotland.",
    "Unlimited free travel on registered local and long-distance bus services in Scotland with a National Entitlement Card.",
    ["Proof of age and address", "Photo", "Parent/guardian consent if under 16"],
    "Apply for a National Entitlement Card or Young Scot card online or via your council or school (Transport Scotland).",
    "https://www.transport.gov.scot/concessionary-travel/under-22s-free-bus-travel/",
    "https://www.transport.gov.scot/concessionary-travel/under-22s-free-bus-travel/",
    "Transport Scotland",
    ["transport", "youth", "children", "universal"],
    rules(
        nations=[S], min_age=5, max_age=21,
        notes="Aged 5-21 and living in Scotland (under-5s already travel free). Includes people seeking asylum and refugees. No income test.",
        verify_notes="Universal.",
    ),
))
A(scheme(
    "gb-sct-60-plus-disabled-free-bus",
    "Free bus travel for people 60+ or disabled (Scotland)",
    "Free bus travel throughout Scotland for people aged 60 or over, or disabled people of any age, with a National Entitlement Card.",
    "Free travel on registered local and long-distance buses in Scotland at any time; companion travel for eligible disabled people.",
    ["Proof of age or disability", "Proof of address", "Photo"],
    "Apply for a National Entitlement Card through your local council or online (Transport Scotland).",
    "https://www.transport.gov.scot/concessionary-travel/60plus-or-disabled-free-bus-travel/",
    "https://www.transport.gov.scot/concessionary-travel/60plus-or-disabled-free-bus-travel/",
    "Transport Scotland",
    ["transport", "elderly", "disability", "universal"],
    rules(
        nations=[S], min_age=60,
        notes="Aged 60 or over and living in Scotland, or disabled and meeting the scheme's disability criteria (any age). No income test.",
        verify_notes="min_age 60 covers the age route; disabled people under 60 also qualify — confirm disability criteria on Transport Scotland.",
    ),
))

# -------------------------------------------------------------------- Wales
A(scheme(
    "gb-wls-childcare-offer",
    "Childcare Offer for Wales (up to 30 hours)",
    "Up to 30 hours a week of early education and childcare for working or studying parents of 3 and 4 year olds in Wales, for up to 48 weeks a year.",
    "Up to 30 hours a week of combined early education and funded childcare for up to 48 weeks a year.",
    ["Proof of identity and address", "Proof of earnings or course enrolment", "Child's birth certificate"],
    "Apply online through the Childcare Offer for Wales digital service (GOV.WALES).",
    "https://www.gov.wales/get-30-hours-childcare-3-and-4-year-olds",
    "https://www.gov.wales/get-30-hours-childcare-3-and-4-year-olds/eligibility",
    WG,
    ["children", "child_care", "middle-class", "upper-middle-class"],
    rules(
        nations=[W],
        notes="Live in Wales; each parent's gross income £100,000 or less; each parent employed and earning at least the equivalent of 16 hours a week at National Minimum/Living Wage, on statutory leave, or enrolled on a further or higher education course of at least 10 weeks. Child aged 3-4 (from the term after turning 3, per local admissions).",
        verify_notes="£100,000 per-parent gross limit — not a household cap (max_annual_income null).",
    ),
))
A(scheme(
    "gb-wls-universal-primary-free-school-meals",
    "Universal Primary Free School Meals (Wales)",
    "Free school meals for all primary school children in Wales, regardless of income.",
    "Free school lunch every school day for all primary pupils at maintained schools.",
    ["Registration with the school if asked"],
    "Your child's school or local authority arranges it; register if asked (GOV.WALES).",
    "https://www.gov.wales/universal-primary-free-school-meals-upfsm",
    "https://www.gov.wales/universal-primary-free-school-meals-upfsm",
    WG,
    ["children", "education", "food", "universal"],
    rules(
        nations=[W],
        notes="All primary school children in Wales. Families on qualifying benefits should still apply for means-tested free school meals (eFSM) to unlock other help such as the School Essentials Grant.",
        verify_notes="Universal.",
    ),
))
A(scheme(
    "gb-wls-school-essentials-grant",
    "School Essentials Grant (Wales)",
    "Grant towards school uniform, sports kit, equipment and trips for children in low-income families in Wales.",
    "£125 per learner per school year (£200 for learners entering year 7). Applications open 1 July 2026 to 31 May 2027.",
    ["Proof of eligibility for means-tested free school meals", "Child's school details"],
    "Apply through your local council (GOV.WALES).",
    "https://www.gov.wales/school-essentials-grant-help-school-costs",
    "https://www.gov.wales/school-essentials-grant-help-school-costs",
    WG,
    ["children", "education", "grant", "low-income"],
    rules(
        nations=[W], implies_low_income=True,
        notes="Children in reception to year 11 who are eligible for means-tested free school meals (eFSM); all looked-after children qualify. Universal primary free school meals alone do not qualify.",
        verify_notes="Linked to eFSM (means-tested).",
    ),
))
A(scheme(
    "gb-wls-discretionary-assistance-fund",
    "Discretionary Assistance Fund (Wales)",
    "Grants that do not need to be repaid for people in Wales facing extreme financial hardship or needing help to live independently.",
    "Emergency Assistance Payment for essentials (food, gas, electricity, heating oil, emergency travel); Individual Assistance Payment for white goods and furniture to live independently.",
    ["Proof of identity and address", "Income and benefit details"],
    "Apply online or by phone to the Discretionary Assistance Fund (GOV.WALES).",
    "https://www.gov.wales/discretionary-assistance-fund-daf",
    "https://www.gov.wales/discretionary-assistance-fund-daf",
    WG,
    ["emergency", "cash_assistance", "low-income"],
    rules(
        nations=[W], implies_low_income=True,
        notes="Live in Wales; extreme financial hardship (e.g. lost your job, waiting for a first benefit payment) or need help to live independently. Cannot be used for ongoing bills.",
        verify_notes="Hardship-based; no published income figure — implies_low_income soft gate. Minimum age not restated on the summary page.",
    ),
))
A(scheme(
    "gb-wls-free-prescriptions",
    "Free NHS prescriptions (Wales)",
    "Everyone registered with a GP in Wales gets free prescriptions from a pharmacy in Wales.",
    "No prescription charges in Wales. Wales residents with a GP in England can get an entitlement card.",
    ["None if registered with a GP in Wales; entitlement card if your GP is in England"],
    "Automatic at the pharmacy (GOV.WALES).",
    "https://www.gov.wales/free-prescriptions",
    "https://www.gov.wales/free-prescriptions",
    WG,
    ["health", "universal"],
    rules(
        nations=[W],
        notes="Registered with a GP in Wales (or a Wales resident with a GP in England using an entitlement card). No income test.",
        verify_notes="Universal.",
    ),
))

# --------------------------------------------------------- Northern Ireland
A(scheme(
    "gb-ni-education-maintenance-allowance",
    "Education Maintenance Allowance (Northern Ireland)",
    "Means-tested weekly allowance for 16-19 year olds staying on at school or further education college in Northern Ireland.",
    "£30 a week (paid fortnightly) plus up to two £100 bonus payments for meeting learning goals (academic year 2026-27).",
    ["Household income evidence", "Proof of identity", "Bank details"],
    "Apply through the EMA process described on nidirect.",
    "https://www.nidirect.gov.uk/articles/education-maintenance-allowance-explained",
    "https://www.nidirect.gov.uk/articles/education-maintenance-allowance-explained",
    "Department for the Economy (Northern Ireland)",
    ["education", "student", "youth", "low-income"],
    rules(
        nations=[NI], min_age=16, max_age=19, max_annual_income=22500,
        notes="Aged 16-19 in the qualifying window; household income £20,500 or less (one dependent child) or £22,500 or less (more than one dependent child); full-time at school or 15+ guided hours a week at college on an eligible course up to Level 3.",
        verify_notes="max_annual_income encodes the official higher household threshold (£22,500); £20,500 for single-child households — confirm on nidirect.",
    ),
))
A(scheme(
    "gb-ni-discretionary-support",
    "Discretionary Support (Northern Ireland)",
    "Interest-free loans or grants for short-term living expenses or household items for people in Northern Ireland in a crisis.",
    "Up to three interest-free loans in 12 months, or grants that do not need repaying, for living expenses, household items, limited travel or rent in advance.",
    ["National Insurance number", "Rent or mortgage details", "Income and savings details", "Bank details"],
    "Apply to the Finance Support Service (Department for Communities) — see nidirect.",
    "https://www.nidirect.gov.uk/articles/discretionary-support",
    "https://www.nidirect.gov.uk/articles/discretionary-support",
    "Department for Communities (Northern Ireland)",
    ["emergency", "loan", "cash_assistance", "low-income"],
    rules(
        nations=[NI], min_age=16, max_annual_income=29741,
        notes="Live in Northern Ireland; extreme or exceptional situation or crisis arising in NI; 18 or over (16 without parental support); you and your partner's total annual income after deductions not more than £29,741.40.",
        verify_notes="max_annual_income encodes the official figure (£29,741.40 after deductions; some income is disregarded).",
    ),
))
A(scheme(
    "gb-ni-lone-pensioner-allowance",
    "Lone Pensioner Allowance (Northern Ireland)",
    "20% discount on domestic rates for people aged 70 or over who live alone. Not means-tested.",
    "20% off your rates bill.",
    ["National Insurance number", "LPS or NIHE application form"],
    "Homeowners apply to Land & Property Services; tenants apply through the Northern Ireland Housing Executive (see nidirect).",
    "https://www.nidirect.gov.uk/articles/lone-pensioner-allowance",
    "https://www.nidirect.gov.uk/articles/lone-pensioner-allowance",
    "Land & Property Services (Department of Finance, Northern Ireland)",
    ["housing", "tax", "elderly", "universal", "middle-class"],
    rules(
        nations=[NI], min_age=70,
        notes="Aged 70 or over and living alone (exceptions for live-in carers, under-18s, or someone with a severe mental impairment). Not means-tested; does not affect benefits.",
        verify_notes="Universal.",
    ),
))
