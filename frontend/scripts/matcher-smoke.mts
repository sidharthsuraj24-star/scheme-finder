/**
 * Small smoke checks mirroring backend accuracy tests.
 * Run: npx --yes tsx scripts/matcher-smoke.mts
 */
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { matchSchemes } from "../src/lib/matching/matcher";
import type { MatchProfile, SchemeRecord } from "../src/lib/matching/types";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const schemes = JSON.parse(
  readFileSync(join(root, "data/schemes.json"), "utf8"),
) as SchemeRecord[];

function base(partial: Partial<MatchProfile>): MatchProfile {
  return {
    age: null,
    gender: null,
    state: "Kerala",
    district: null,
    marital_status: null,
    annual_income: null,
    monthly_household_income: null,
    occupations: [],
    categories: [],
    disability: null,
    disability_percent: null,
    land_ownership: null,
    language: null,
    is_student: null,
    is_pregnant: null,
    pregnancy_order: null,
    is_lactating: null,
    child_age_months: null,
    housing_status: null,
    residence_type: null,
    income_tax_payer: null,
    kawwf_member: null,
    agri_labour_years: null,
    primary_breadwinner_deceased: null,
    deceased_breadwinner_age: null,
    flags: {},
    ...partial,
  };
}

function ids(resp: { matched: { scheme_id: string }[] }) {
  return new Set(resp.matched.map((m) => m.scheme_id));
}

let failed = 0;
function check(name: string, ok: boolean, detail = "") {
  if (ok) console.log(`PASS ${name}`);
  else {
    failed += 1;
    console.error(`FAIL ${name} ${detail}`);
  }
}

// other occupation → NOT agri labour
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 65,
      gender: "male",
      district: "Ernakulam",
      annual_income: 45000,
      occupations: ["other"],
      land_ownership: "none",
    }),
  );
  check("other_not_agri", !ids(resp).has("kerala-agri-labour-pension"));
  check(
    "empty_occ_not_agri",
    !ids(
      matchSchemes(
        schemes,
        base({ age: 65, annual_income: 45000, occupations: [], land_ownership: "none" }),
      ),
    ).has("kerala-agri-labour-pension"),
  );
  check("district_echo", resp.district === "Ernakulam");
}

// farmer+land → pm-kisan uncertain
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 45,
      occupations: ["farmer", "landholding_farmer"],
      land_ownership: "cultivable_own",
      annual_income: 180000,
    }),
  );
  const hit = resp.matched.find((m) => m.scheme_id === "pm-kisan");
  check("pm_kisan_uncertain", !!hit && hit.status === "uncertain");
  check("farmer_not_agri", !ids(resp).has("kerala-agri-labour-pension"));
}

// senior low income → old age likely
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 68,
      gender: "male",
      annual_income: 45000,
      occupations: ["other"],
      land_ownership: "none",
      district: "Ernakulam",
    }),
  );
  const hit = resp.matched.find((m) => m.scheme_id === "kerala-old-age-pension");
  check("old_age_likely", !!hit && hit.status === "likely_eligible");
  check(
    "district_in_explanation",
    !!hit && hit.explanation.en.includes("District on profile: Ernakulam"),
  );
}

// no housing → LIFE not likely
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 40,
      annual_income: 80000,
      occupations: ["other"],
      land_ownership: "none",
    }),
  );
  const life = resp.matched.find((m) => m.scheme_id === "kerala-life-mission");
  check("life_not_likely", !life || life.status !== "likely_eligible");
}

// deserted under 50 → not widow
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 45,
      gender: "female",
      marital_status: "deserted",
      annual_income: 50000,
    }),
  );
  check("deserted_under_50", !ids(resp).has("kerala-widow-pension"));
}

// agri without kawwf → uncertain
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 63,
      annual_income: 70000,
      occupations: ["agricultural_labour"],
      land_ownership: "none",
    }),
  );
  const hit = resp.matched.find((m) => m.scheme_id === "kerala-agri-labour-pension");
  check("agri_uncertain_no_kawwf", !!hit && hit.status === "uncertain");
}


// LIFE high monthly income (wizard 12.5L/mo → annual 1.5Cr) must NOT match
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 53,
      gender: "female",
      state: "Kerala",
      district: "Palakkad",
      marital_status: "married",
      monthly_household_income: 1_250_000,
      annual_income: null,
      disability: false,
      disability_percent: 0,
      primary_breadwinner_deceased: false,
      land_ownership: "none",
      occupations: ["other"],
      categories: [],
      housing_status: null,
    }),
  );
  check("life_high_income_excluded", !ids(resp).has("kerala-life-mission"));
  check(
    "life_high_income_hard_fail",
    resp.excluded.some(
      (e) => e.scheme_id === "kerala-life-mission" && e.reasons.includes("max_annual_income"),
    ),
  );
}

// LIFE low income + homeless/landless → uncertain (verify)
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 53,
      gender: "female",
      state: "Kerala",
      district: "Palakkad",
      marital_status: "married",
      monthly_household_income: 20_000,
      annual_income: null,
      land_ownership: "none",
      occupations: ["other"],
      categories: ["landless", "homeless"],
      housing_status: "homeless",
    }),
  );
  const life = resp.matched.find((m) => m.scheme_id === "kerala-life-mission");
  check("life_low_income_uncertain", !!life && life.status === "uncertain");
  check(
    "life_low_income_ceiling_ok",
    !!life && life.matched_rules.includes("max_annual_income"),
  );
}


// High earner Kerala female — no JSY / PMJAY / LIFE soft matches
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 53,
      gender: "female",
      state: "Kerala",
      marital_status: "married",
      annual_income: 1_850_000,
      land_ownership: "none",
      occupations: ["other"],
      categories: [],
      is_pregnant: false,
      is_lactating: false,
      disability: false,
      primary_breadwinner_deceased: false,
    }),
  );
  const banned = [
    "janani-suraksha-yojana-kerala",
    "ab-pmjay-national",
    "kerala-kasp-pmjay",
    "kerala-life-mission",
    "kerala-old-age-pension",
  ];
  for (const id of banned) {
    check(`high_earner_excludes_${id}`, !ids(resp).has(id));
  }
}

// Maternity absent → JSY hard fail
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 28,
      gender: "female",
      state: "Kerala",
      annual_income: 50_000,
      categories: ["BPL", "SC"],
      occupations: ["other"],
      land_ownership: "none",
      // is_pregnant / is_lactating left null
    }),
  );
  check("maternity_absent_excludes_jsy", !ids(resp).has("janani-suraksha-yojana-kerala"));
  check(
    "maternity_absent_hard_fail",
    resp.excluded.some(
      (e) => e.scheme_id === "janani-suraksha-yojana-kerala" && e.reasons.includes("maternity_required"),
    ),
  );
}

// SECC flag still matches KASP
{
  const resp = matchSchemes(
    schemes,
    base({
      age: 40,
      state: "Kerala",
      annual_income: 80_000,
      occupations: ["other"],
      categories: ["secc_deprivation"],
      flags: { secc_eligible: true },
      land_ownership: "none",
    }),
  );
  check("secc_flag_matches_kasp", ids(resp).has("kerala-kasp-pmjay"));
}

// Income ladder numeric ceilings
{
  for (const [annual, expectLife] of [
    [1_850_000, false],
    [1_250_000, false],
    [250_000, true],
    [80_000, true],
    [36_000, true],
  ] as const) {
    const resp = matchSchemes(
      schemes,
      base({
        age: 40,
        gender: "female",
        state: "Kerala",
        annual_income: annual,
        land_ownership: "none",
        occupations: ["other"],
        categories: ["homeless", "landless"],
        housing_status: "homeless",
      }),
    );
    check(
      `life_income_${annual}`,
      expectLife ? ids(resp).has("kerala-life-mission") : !ids(resp).has("kerala-life-mission"),
    );
  }
}



// United Kingdom (2026-09-25): GBP soft gate, nation filtering, no India bands / US gate
{
  const ukBase = (partial: Partial<MatchProfile>) =>
    base({
      country: "United Kingdom",
      state: "England",
      age: 35,
      gender: "female",
      occupations: ["other"],
      annual_income: 30_000,
      disability: false,
      disability_percent: 0,
      ...partial,
    } as Partial<MatchProfile>);
  const opts = { max_results: 100 };

  const low = matchSchemes(schemes, ukBase({ annual_income: 18_000 }), opts);
  check("uk_low_income_uc", ids(low).has("gb-universal-credit"));
  check("uk_no_india_band", low.income_band == null);
  const uc = low.matched.find((m) => m.scheme_id === "gb-universal-credit");
  const ucText = JSON.stringify(uc ?? {});
  check("uk_explanation_pounds", ucText.includes("£60,000") && !ucText.includes("$60,000"), ucText.slice(0, 200));

  const rich = matchSchemes(schemes, ukBase({ age: 30, annual_income: 250_000 }), opts);
  check("uk_rich_excludes_uc", !ids(rich).has("gb-universal-credit"));
  for (const id of ["gb-lifetime-isa", "gb-child-benefit", "gb-isa-allowance"]) {
    check(`uk_rich_keeps_${id}`, ids(rich).has(id));
  }
  // Per-parent £100k childcare limits imply a £200k household maximum
  check("uk_rich_excludes_tfc", !ids(rich).has("gb-tax-free-childcare"));
  const ukUpper = matchSchemes(schemes, ukBase({ age: 30, annual_income: 150_000 }), opts);
  check("uk_upper_keeps_tfc", ids(ukUpper).has("gb-tax-free-childcare"));
  check("uk_rich_excludes_shared_ownership", !ids(rich).has("gb-eng-shared-ownership"));

  const scot = matchSchemes(schemes, ukBase({ state: "Scotland", annual_income: 15_000 }), opts);
  check("uk_scotland_scp", ids(scot).has("gb-sct-scottish-child-payment"));
  check("uk_scotland_no_eng_childcare", !ids(scot).has("gb-eng-free-childcare-working-parents"));
  const eng = matchSchemes(schemes, ukBase({ state: "England", annual_income: 15_000 }), opts);
  check("uk_england_no_scp", !ids(eng).has("gb-sct-scottish-child-payment"));
  check(
    "uk_no_india_or_us_rows",
    ![...ids(eng)].some((i) => i.startsWith("us-") || i.startsWith("kerala-") || i.startsWith("uk-")),
  );
}

// Explanation text: readable countries rule; BPL/destitute wording India-only; right currency
{
  const opts = { max_results: 100 };
  const lowHits = (resp: ReturnType<typeof matchSchemes>) =>
    resp.matched.filter((m) => m.matched_rules.includes("implies_low_income"));
  const cases: [string, Partial<MatchProfile>, string][] = [
    ["uk", { country: "United Kingdom", state: "England", age: 35, annual_income: 18_000 }, "United Kingdom"],
    ["us", { country: "United States", state: "California", age: 35, annual_income: 20_000, occupations: ["unemployed"] }, "United States"],
    ["in", { age: 68, gender: "male", annual_income: 45_000, categories: ["BPL"] }, "India"],
  ];
  for (const [tag, partial, display] of cases) {
    const resp = matchSchemes(schemes, base(partial), opts);
    const withCountry = resp.matched.filter((m) => m.matched_rules.includes("countries"));
    check(
      `expl_countries_readable_${tag}`,
      withCountry.length > 0 &&
        withCountry.every(
          (m) =>
            m.explanation.en.includes(`available in ${display}`) &&
            !m.explanation.en.includes(" countries;") &&
            m.explanation.ml.includes(`${display} ൽ ലഭ്യമാണ്`),
        ),
    );
    const low = lowHits(resp);
    if (tag === "in") {
      check(
        "expl_india_keeps_bpl",
        low.length > 0 && low.every((m) => m.explanation.en.includes("BPL/destitute") && m.explanation.en.includes("Rs.45,000")),
      );
    } else {
      const cur = tag === "uk" ? "£18,000" : "$20,000";
      check(
        `expl_${tag}_neutral_low_income`,
        low.length > 0 &&
          low.every(
            (m) =>
              !m.explanation.en.includes("BPL") &&
              !m.explanation.en.includes("destitute") &&
              !m.explanation.ml.includes("BPL") &&
              m.explanation.en.includes("low-income / means-tested") &&
              m.explanation.en.includes(cur) &&
              !m.explanation.en.includes("Rs."),
          ),
      );
    }
  }
}

// Canada (2026-09-25): CAD soft gate, province filtering, no India bands / US gate
{
  const caBase = (partial: Partial<MatchProfile>) =>
    base({
      country: "Canada",
      state: "Ontario",
      age: 35,
      gender: "female",
      occupations: ["other"],
      annual_income: 45_000,
      disability: false,
      disability_percent: 0,
      ...partial,
    } as Partial<MatchProfile>);
  const opts = { max_results: 100 };

  const lowDis = matchSchemes(schemes, caBase({ annual_income: 20_000, disability: true, disability_percent: 60 }), opts);
  check("ca_low_income_cdb", ids(lowDis).has("can-canada-disability-benefit"));
  check("ca_no_india_band", lowDis.income_band == null);
  const cdb = lowDis.matched.find((m) => m.scheme_id === "can-canada-disability-benefit");
  const cdbText = cdb?.explanation.en ?? "";
  check(
    "ca_explanation_cad",
    cdbText.includes("C$58,523") && cdbText.includes("C$20,000") && !/(^|[^C])\$/.test(cdbText) && !cdbText.includes("Rs."),
    cdbText.slice(0, 200),
  );
  // C$59,000 is under the US $60k gate but over the Canada gate: USD gate must not be reused
  const mid = matchSchemes(schemes, caBase({ annual_income: 59_000, disability: true, disability_percent: 60 }), opts);
  check("ca_gate_not_usd", !ids(mid).has("can-canada-disability-benefit"));

  const rich = matchSchemes(schemes, caBase({ state: "Alberta", age: 32, annual_income: 250_000 }), opts);
  for (const id of ["can-tfsa", "can-rrsp", "can-fhsa"]) {
    check(`ca_rich_keeps_${id}`, ids(rich).has(id));
  }
  check("ca_rich_excludes_cgeb", !ids(rich).has("can-groceries-essentials-benefit"));
  check("ca_rich_excludes_cdcp", !ids(rich).has("can-canada-dental-care-plan"));
  // Official phase-out zero-points (2026-09-25): C$250k Ontario family no longer sees OCB
  const onRich = matchSchemes(schemes, caBase({ state: "Ontario", age: 38, annual_income: 250_000 }), opts);
  check("ca_on_rich_no_ocb", !ids(onRich).has("can-on-child-benefit"));
  check("ca_on_rich_no_otb", !ids(onRich).has("can-on-trillium-benefit"));
  check("ca_on_rich_keeps_ccb", ids(onRich).has("can-canada-child-benefit"));
  const onLow = matchSchemes(schemes, caBase({ state: "Ontario", age: 30, annual_income: 45_000 }), opts);
  check("ca_on_45k_keeps_ocb", ids(onLow).has("can-on-child-benefit"));
  const onTop = matchSchemes(schemes, caBase({ state: "Ontario", age: 38, annual_income: 330_000 }), opts);
  check("ca_330k_no_ccb", !ids(onTop).has("can-canada-child-benefit"));

  const qc = matchSchemes(schemes, caBase({ state: "Quebec", age: 30, annual_income: 60_000 }), opts);
  check("ca_quebec_qpip", ids(qc).has("can-qc-qpip"));
  check("ca_quebec_no_ei_parental", !ids(qc).has("can-ei-maternity-parental"));
  const on = matchSchemes(schemes, caBase({ state: "Ontario", annual_income: 30_000 }), opts);
  check("ca_ontario_otb", ids(on).has("can-on-trillium-benefit"));
  check("ca_ontario_no_bc_rows", ![...ids(on)].some((i) => i.startsWith("can-bc-") || i.startsWith("can-qc-")));
  check(
    "ca_no_india_us_uk_rows",
    ![...ids(on)].some((i) => i.startsWith("us-") || i.startsWith("ca-") || i.startsWith("gb-") || i.startsWith("kerala-")),
  );
  const us = matchSchemes(schemes, base({ country: "United States", state: "California", age: 35, annual_income: 30_000 } as Partial<MatchProfile>), opts);
  check("us_no_canada_rows", ![...ids(us)].some((i) => i.startsWith("can-")));
}

if (failed) {
  console.error(`\n${failed} failed`);
  process.exit(1);
}
console.log("\nAll TS smoke checks passed");
