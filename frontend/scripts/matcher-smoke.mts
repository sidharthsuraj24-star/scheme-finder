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


if (failed) {
  console.error(`\n${failed} failed`);
  process.exit(1);
}
console.log("\nAll TS smoke checks passed");
