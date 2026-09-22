/** Deterministic eligibility matcher — port of backend/app/matcher.py */

import { cataloguePayload, resolveLastVerified } from "./catalogue";
import { buildExplanation } from "./explanations";
import type {
  ExcludedScheme,
  MatchOptions,
  MatchProfile,
  MatchResponse,
  MatchedScheme,
  NeedsVerificationItem,
  SchemeRecord,
  StatusLiteral,
} from "./types";

const SECC_STYLE_CATEGORIES = new Set([
  "secc_deprivation",
  "rsby_chis_2018_19",
  "pmjay",
  "eshram",
  "pmkisan",
  "mgnrega",
  "nfsa_ration",
  "aww_awh_asha",
]);

/** LIFE / housing beneficiary types — require explicit housing_status or category. */
const HOUSING_STYLE_CATEGORIES = new Set([
  "homeless",
  "landless",
  "incomplete_house",
  "temporary_shelter",
  "landed_homeless",
  "landless_homeless",
]);

const LAND_REQUIRED_TOKENS = new Set([
  "cultivable_landholding_required",
  "landholding_required",
  "requires_land",
  "cultivable_own",
]);

const LAND_POSITIVE = new Set([
  "true",
  "yes",
  "1",
  "cultivable_own",
  "owns_house_and_land",
  "owned",
  "owner",
  "landholding",
  "has_land",
  "own",
  "cultivable",
]);

const LAND_NEGATIVE = new Set(["false", "no", "0", "none", "landless", "nil", "n/a", "na"]);

function norm(value: string | null | undefined): string {
  if (value == null) return "";
  return String(value).trim().toLowerCase().replace(/-/g, "_").replace(/ /g, "_");
}

function normSet(values: string[] | null | undefined): Set<string> {
  const out = new Set<string>();
  for (const v of values || []) {
    const n = norm(v);
    if (n) out.add(n);
  }
  return out;
}

export function profileHasLand(landOwnership: boolean | string | null | undefined): boolean | null {
  if (landOwnership == null) return null;
  if (typeof landOwnership === "boolean") return landOwnership;
  const token = norm(String(landOwnership));
  if (LAND_POSITIVE.has(token)) return true;
  if (LAND_NEGATIVE.has(token)) return false;
  return null;
}

export function schemeRequiresLand(ruleLand: unknown): boolean {
  if (ruleLand == null || ruleLand === false) return false;
  if (ruleLand === true) return true;
  const token = norm(String(ruleLand));
  if (!token) return false;
  if (LAND_REQUIRED_TOKENS.has(token)) return true;
  if (token.includes("landholding_required") || token.includes("cultivable_landholding")) return true;
  return false;
}

export function schemeLandIsHomelessStyle(ruleLand: unknown): boolean {
  if (ruleLand == null) return false;
  const token = norm(String(ruleLand));
  return token.includes("landless") || token.includes("homeless");
}

export class RuleResult {
  matched: string[] = [];
  unmatched: string[] = [];
  missing: string[] = [];
  hard_fail = false;
  uncertain = false;

  fail(rule: string): void {
    this.unmatched.push(rule);
    this.hard_fail = true;
  }
  ok(rule: string): void {
    this.matched.push(rule);
  }
  miss(fieldName: string, makeUncertain = true): void {
    this.missing.push(fieldName);
    if (makeUncertain) this.uncertain = true;
  }
}

function unique(arr: string[]): string[] {
  return [...new Set(arr)];
}

export function evaluateScheme(scheme: SchemeRecord, profile: MatchProfile): RuleResult {
  const rules = (scheme.eligibility_rules || {}) as Record<string, unknown>;
  const result = new RuleResult();

  // --- countries (default India for backward compat) ---
  let schemeCountries = (rules.countries as string[] | undefined) || [];
  if (!schemeCountries.length) {
    schemeCountries = ["India"];
  }
  const allowedCountries = new Set(schemeCountries.map(norm));
  const profileCountry = (profile.country || "India").trim() || "India";
  if (!allowedCountries.has(norm(profileCountry))) {
    result.fail("countries");
  } else {
    result.ok("countries");
  }

  // --- states / nationwide (within matched country) ---
  // Nationwide if: nationwide flag, empty states, or states include India / All India.
  // Profile state/region is required for a clean match; missing → uncertain (miss).
  const schemeStates = (rules.states as string[] | undefined) || [];
  const nationwideFlag =
    Boolean(rules.nationwide) || Boolean((scheme as { nationwide?: boolean }).nationwide);
  const allowed = new Set(schemeStates.map(norm));
  const isNationwide =
    nationwideFlag ||
    schemeStates.length === 0 ||
    allowed.has("india") ||
    allowed.has("all_india");
  const profileState = (profile.state || "").trim();
  if (result.hard_fail && result.unmatched.includes("countries")) {
    // country mismatch already excludes
  } else if (!profileState) {
    result.miss("state");
  } else if (isNationwide) {
    result.ok("states");
  } else if (allowed.has(norm(profileState))) {
    result.ok("states");
  } else {
    result.fail("states");
  }

  // --- age ---
  const minAge = rules.min_age as number | undefined | null;
  const maxAge = rules.max_age as number | undefined | null;
  if (minAge != null || maxAge != null) {
    if (profile.age == null) {
      result.miss("age");
    } else {
      let ageOk = true;
      if (minAge != null && profile.age < Number(minAge)) {
        ageOk = false;
        result.fail("min_age");
      } else if (minAge != null) {
        result.ok("min_age");
      }
      if (maxAge != null && profile.age > Number(maxAge)) {
        ageOk = false;
        result.fail("max_age");
      } else if (maxAge != null && ageOk) {
        result.ok("max_age");
      }
    }
  }

  // --- income ---
  // Hard ceiling ALWAYS excludes when exceeded — including verify=true schemes.
  // Derive annual↔monthly here so a missing derived field cannot soft-pass the gate.
  const maxAnnual = rules.max_annual_income as number | undefined | null;
  const maxMonthly = rules.max_monthly_household_income as number | undefined | null;
  if (maxAnnual != null) {
    let annual = profile.annual_income;
    if (annual == null && profile.monthly_household_income != null) {
      annual = Number(profile.monthly_household_income) * 12;
    }
    if (annual == null) result.miss("annual_income");
    else if (Number(annual) > Number(maxAnnual)) result.fail("max_annual_income");
    else result.ok("max_annual_income");
  }
  if (maxMonthly != null) {
    let monthly = profile.monthly_household_income;
    if (monthly == null && profile.annual_income != null) {
      monthly = Number(profile.annual_income) / 12;
    }
    if (monthly == null) result.miss("monthly_household_income");
    else if (Number(monthly) > Number(maxMonthly)) result.fail("max_monthly_household_income");
    else result.ok("max_monthly_household_income");
  }

  // Soft gate for BPL/destitute schemes with no numeric ceiling encoded.
  // Prefer real max_annual_income / max_monthly when known; this only applies when both are null.
  // Documented threshold: annual >= ₹5,00,000 → hard exclude (implies_low_income).
  const IMPLIES_LOW_INCOME_ANNUAL_GATE = 500_000;
  const impliesLow = Boolean(rules.implies_low_income);
  if (impliesLow && maxAnnual == null && maxMonthly == null) {
    let annual = profile.annual_income;
    if (annual == null && profile.monthly_household_income != null) {
      annual = Number(profile.monthly_household_income) * 12;
    }
    if (annual == null) result.miss("annual_income");
    else if (Number(annual) >= IMPLIES_LOW_INCOME_ANNUAL_GATE) result.fail("implies_low_income");
    else result.ok("implies_low_income");
  }

  // --- disability ---
  const disabilityRequired = Boolean(rules.disability_required);
  const minDisability = rules.min_disability_percent as number | undefined | null;
  if (disabilityRequired || minDisability != null) {
    let hasDisability = profile.disability;
    if (hasDisability == null && profile.disability_percent != null) {
      hasDisability = Number(profile.disability_percent) > 0;
    }
    if (disabilityRequired) {
      if (hasDisability == null && profile.disability_percent == null) {
        result.miss("disability");
      } else if (
        hasDisability === false ||
        (profile.disability_percent != null && Number(profile.disability_percent) <= 0)
      ) {
        result.fail("disability_required");
      } else {
        result.ok("disability_required");
      }
    }
    if (minDisability != null) {
      if (profile.disability_percent == null) result.miss("disability_percent");
      else if (Number(profile.disability_percent) < Number(minDisability))
        result.fail("min_disability_percent");
      else result.ok("min_disability_percent");
    }
  }

  // --- gender ---
  const genderRule = rules.gender as string | undefined | null;
  if (genderRule) {
    if (!profile.gender) result.miss("gender");
    else if (norm(profile.gender) !== norm(genderRule)) result.fail("gender");
    else result.ok("gender");
  }

  // --- marital_status ---
  const maritalAllowed = (rules.marital_status as string[] | undefined) || [];
  if (maritalAllowed.length) {
    if (!profile.marital_status) {
      result.miss("marital_status");
    } else {
      const profileMs = norm(profile.marital_status);
      const allowedNorm = maritalAllowed.map(norm);
      let matchedToken: string | null = null;
      for (const token of allowedNorm) {
        if (profileMs === token) {
          matchedToken = token;
          break;
        }
        if (profileMs === "deserted" && token.startsWith("deserted")) {
          matchedToken = token;
          break;
        }
        if (
          (profileMs === "missing_husband" || profileMs === "husband_missing") &&
          token.includes("husband_missing")
        ) {
          matchedToken = token;
          break;
        }
      }
      if (matchedToken == null) {
        result.fail("marital_status");
      } else if (matchedToken === "deserted_7_years_over_50") {
        if (profile.age == null) result.miss("age");
        else if (profile.age < 50) result.fail("deserted_7_years_over_50");
        else {
          result.ok("marital_status");
          result.ok("deserted_7_years_over_50");
        }
      } else {
        result.ok("marital_status");
      }
    }
  }

  // --- occupations ---
  // Real intersection only. Empty / missing profile occupations must NEVER
  // satisfy a non-empty scheme occupation allowlist (not a wildcard).
  const schemeOccs = (rules.occupations as string[] | undefined) || [];
  if (schemeOccs.length) {
    const profileOccs = normSet(profile.occupations);
    const schemeOccsN = normSet(schemeOccs);
    if (!profileOccs.size) {
      result.fail("occupations");
    } else {
      let hit = false;
      for (const o of profileOccs) {
        if (schemeOccsN.has(o)) {
          hit = true;
          break;
        }
      }
      if (hit) result.ok("occupations");
      else result.fail("occupations");
    }
  }

  // --- categories ---
  const schemeCats = (rules.categories as string[] | undefined) || [];
  if (schemeCats.length) {
    const schemeCatsN = normSet(schemeCats);
    const profileCats = normSet(profile.categories);
    const flags = profile.flags || {};
    if (flags.secc_eligible || flags.secc_deprivation) profileCats.add("secc_deprivation");
    if (flags.rsby_chis_2018_19) profileCats.add("rsby_chis_2018_19");
    if (profile.housing_status) profileCats.add(norm(profile.housing_status));
    if (profile.residence_type) {
      const rt = norm(profile.residence_type);
      profileCats.add(rt);
      if (rt === "urban") profileCats.add("urban_household");
    }

    const seccOnly =
      [...schemeCatsN].every((c) => SECC_STYLE_CATEGORIES.has(c) || c.startsWith("secc"));
    // PMJAY / KASP-style list schemes often mix SECC tokens with BPL.
    // Require a positive intersecting flag/category — never soft-list for random users.
    const listEvidenceRequired =
      schemeCatsN.size > 0 &&
      [...schemeCatsN].every(
        (c) => SECC_STYLE_CATEGORIES.has(c) || c === "bpl" || c.startsWith("secc"),
      ) &&
      [...schemeCatsN].some((c) => SECC_STYLE_CATEGORIES.has(c) || c.startsWith("secc"));
    const housingOnly =
      schemeCatsN.size > 0 && [...schemeCatsN].every((c) => HOUSING_STYLE_CATEGORIES.has(c));

    const intersectionSet = new Set<string>();
    for (const c of profileCats) {
      if (schemeCatsN.has(c)) intersectionSet.add(c);
    }
    const intersection = intersectionSet.size > 0;

    const rawProfileCats = normSet(profile.categories);
    let hasHousingSignal = false;
    if (profile.housing_status && HOUSING_STYLE_CATEGORIES.has(norm(profile.housing_status))) {
      hasHousingSignal = true;
    }
    for (const c of rawProfileCats) {
      if (HOUSING_STYLE_CATEGORIES.has(c)) hasHousingSignal = true;
    }
    for (const c of intersectionSet) {
      if (HOUSING_STYLE_CATEGORIES.has(c)) hasHousingSignal = true;
    }

    if (intersection) {
      result.ok("categories");
    } else if (housingOnly && !hasHousingSignal) {
      // Missing housing_status / housing category → uncertain; never likely via blank profile.
      result.miss("housing_status");
      result.uncertain = true;
    } else if (seccOnly || listEvidenceRequired) {
      // No matching SECC/list evidence → hard exclude (verify_notes stay in catalogue).
      result.fail("categories");
    } else if (!profileCats.size) {
      result.miss("categories");
    } else {
      result.fail("categories");
    }
  }

  // --- land_ownership ---
  const ruleLand = rules.land_ownership;
  if (schemeRequiresLand(ruleLand)) {
    const hasLand = profileHasLand(profile.land_ownership);
    if (hasLand == null) result.miss("land_ownership");
    else if (hasLand === false) result.fail("land_ownership_required");
    else result.ok("land_ownership");
  } else if (schemeLandIsHomelessStyle(ruleLand)) {
    const hasLand = profileHasLand(profile.land_ownership);
    if (hasLand === false) result.ok("land_ownership_landless");
  }

  // --- maternity ---
  // Hard fail unless positive pregnant/lactating/recent-child signal.
  // false / null / absent must NOT soft-match as uncertain.
  if (rules.maternity_required) {
    const pregnant = profile.is_pregnant;
    const lactating = profile.is_lactating;
    const childMonths = profile.child_age_months;
    const positive =
      pregnant === true ||
      lactating === true ||
      (childMonths != null && Number(childMonths) >= 0 && Number(childMonths) <= 6);
    if (positive) result.ok("maternity_required");
    else result.fail("maternity_required");
  }

  // --- NFBS breadwinner ---
  if (rules.primary_breadwinner_deceased_required) {
    const flag = profile.primary_breadwinner_deceased;
    if (flag === true) result.ok("primary_breadwinner_deceased_required");
    else if (flag === false) result.fail("primary_breadwinner_deceased_required");
    else result.miss("primary_breadwinner_deceased");
  }

  // --- KAWWF / agri labour tenure ---
  if (rules.kawwf_member_required) {
    const flag = profile.kawwf_member;
    if (flag === true) result.ok("kawwf_member_required");
    else if (flag === false) result.fail("kawwf_member_required");
    else result.miss("kawwf_member");
  }

  const minAgriYears = rules.min_agri_labour_years as number | undefined | null;
  if (minAgriYears != null) {
    const years = profile.agri_labour_years;
    if (years == null) result.miss("agri_labour_years");
    else if (Number(years) < Number(minAgriYears)) result.fail("min_agri_labour_years");
    else result.ok("min_agri_labour_years");
  }

  // --- districts (optional hard filter only when scheme lists districts) ---
  const schemeDistricts = (rules.districts as string[] | undefined) || [];
  if (schemeDistricts.length) {
    if (!profile.district) result.miss("district");
    else if (normSet(schemeDistricts).has(norm(profile.district))) result.ok("districts");
    else result.fail("districts");
  }

  return result;
}


/** Geo meta matching evaluateScheme country/state hard-fail rules. */
function schemeGeoMeta(scheme: SchemeRecord): {
  countries: Set<string>;
  states: Set<string>;
  isNationwide: boolean;
} {
  const rules = (scheme.eligibility_rules || {}) as Record<string, unknown>;
  let rawCountries = (rules.countries as string[] | undefined) || [];
  if (!rawCountries.length) rawCountries = ["India"];
  const countries = new Set(rawCountries.map(norm).filter(Boolean));
  const schemeStates = (rules.states as string[] | undefined) || [];
  const states = new Set(schemeStates.map(norm).filter(Boolean));
  const nationwideFlag =
    Boolean(rules.nationwide) || Boolean((scheme as { nationwide?: boolean }).nationwide);
  const isNationwide =
    nationwideFlag ||
    schemeStates.length === 0 ||
    states.has("india") ||
    states.has("all_india");
  return { countries, states, isNationwide };
}

/** Precomputed country / (country, state) indexes including nationwide schemes. */
export class SchemeGeoIndex {
  readonly schemes: SchemeRecord[];
  private countries: Set<string>[];
  private byCountry: Map<string, number[]> = new Map();
  private nationwideByCountry: Map<string, number[]> = new Map();
  private byCountryState: Map<string, number[]> = new Map();

  constructor(schemes: SchemeRecord[]) {
    this.schemes = schemes;
    this.countries = new Array(schemes.length);
    for (let i = 0; i < schemes.length; i++) {
      const { countries, states, isNationwide } = schemeGeoMeta(schemes[i]);
      this.countries[i] = countries;
      for (const c of countries) {
        let list = this.byCountry.get(c);
        if (!list) {
          list = [];
          this.byCountry.set(c, list);
        }
        list.push(i);
        if (isNationwide) {
          let nw = this.nationwideByCountry.get(c);
          if (!nw) {
            nw = [];
            this.nationwideByCountry.set(c, nw);
          }
          nw.push(i);
        } else {
          for (const st of states) {
            const key = `${c}\0${st}`;
            let bucket = this.byCountryState.get(key);
            if (!bucket) {
              bucket = [];
              this.byCountryState.set(key, bucket);
            }
            bucket.push(i);
          }
        }
      }
    }
  }

  partition(profile: MatchProfile): {
    candidates: SchemeRecord[];
    geoExcluded: ExcludedScheme[];
  } {
    const profileCountry = norm((profile.country || "India").trim() || "India");
    const profileState = (profile.state || "").trim();
    const profileStateN = profileState ? norm(profileState) : "";

    let idxList: number[];
    if (profileStateN) {
      const nw = this.nationwideByCountry.get(profileCountry) || [];
      const st = this.byCountryState.get(`${profileCountry}\0${profileStateN}`) || [];
      idxList = Array.from(new Set([...nw, ...st])).sort((a, b) => a - b);
    } else {
      idxList = [...(this.byCountry.get(profileCountry) || [])];
    }

    const candSet = new Set(idxList);
    const candidates = idxList.map((i) => this.schemes[i]);
    const geoExcluded: ExcludedScheme[] = [];
    for (let i = 0; i < this.schemes.length; i++) {
      if (candSet.has(i)) continue;
      const reason = this.countries[i].has(profileCountry) ? "states" : "countries";
      geoExcluded.push({
        scheme_id: this.schemes[i].id,
        status: "not_eligible",
        reasons: [reason],
      });
    }
    return { candidates, geoExcluded };
  }
}

const _geoIndexCache = new WeakMap<SchemeRecord[], SchemeGeoIndex>();

function geoIndexFor(schemes: SchemeRecord[]): SchemeGeoIndex {
  let idx = _geoIndexCache.get(schemes);
  if (!idx) {
    idx = new SchemeGeoIndex(schemes);
    _geoIndexCache.set(schemes, idx);
  }
  return idx;
}

function score(result: RuleResult): number {
  if (result.hard_fail) return 0;
  const total = result.matched.length + result.unmatched.length + result.missing.length;
  if (total === 0) return 0.5;
  return result.matched.length / total;
}

export function matchSchemes(
  schemes: SchemeRecord[],
  profile: MatchProfile,
  options?: Partial<MatchOptions> | null,
): MatchResponse {
  const opts: MatchOptions = {
    include_verify_uncertain: options?.include_verify_uncertain ?? true,
    lang: options?.lang ?? "en",
    max_results: options?.max_results ?? 50,
  };

  const matched: MatchedScheme[] = [];
  const excluded: ExcludedScheme[] = [];
  const needs_verification: NeedsVerificationItem[] = [];

  const { candidates, geoExcluded } = geoIndexFor(schemes).partition(profile);
  excluded.push(...geoExcluded);

  for (const scheme of candidates) {
    const rules = (scheme.eligibility_rules || {}) as Record<string, unknown>;
    const verify = Boolean(rules.verify);
    const verify_notes = String(rules.verify_notes || "");
    const result = evaluateScheme(scheme, profile);

    if (result.hard_fail) {
      excluded.push({
        scheme_id: scheme.id,
        status: "not_eligible",
        reasons: unique(result.unmatched),
      });
      continue;
    }

    let status: StatusLiteral =
      verify || result.uncertain || result.missing.length > 0 ? "uncertain" : "likely_eligible";

    if (status === "uncertain" && !opts.include_verify_uncertain) {
      needs_verification.push({
        scheme_id: scheme.id,
        status: "uncertain",
        verify_notes,
      });
      continue;
    }

    const explanation = buildExplanation({
      scheme,
      profile,
      matched_rules: result.matched,
      unmatched_rules: result.unmatched,
      missing_fields: result.missing,
      status,
    });

    matched.push({
      scheme_id: scheme.id,
      score: Math.round(score(result) * 10000) / 10000,
      status,
      matched_rules: unique(result.matched),
      unmatched_rules: unique(result.unmatched),
      missing_profile_fields: unique(result.missing),
      verify,
      verify_notes: verify ? verify_notes : "",
      explanation,
      scheme_name: scheme.scheme_name || {},
      description: scheme.description ?? null,
      benefits: scheme.benefits ?? null,
      documents: scheme.required_documents ?? null,
      how_to_apply: scheme.how_to_apply ?? null,
      apply_url: scheme.apply_url ?? null,
      official_source_url: scheme.official_source_url ?? null,
      last_verified: resolveLastVerified(scheme),
      tags: scheme.tags || [],
    });

    if (status === "uncertain" && verify) {
      needs_verification.push({
        scheme_id: scheme.id,
        status: "uncertain",
        verify_notes,
      });
    }
  }

  matched.sort((a, b) => {
    const sa = a.status === "likely_eligible" ? 0 : 1;
    const sb = b.status === "likely_eligible" ? 0 : 1;
    if (sa !== sb) return sa - sb;
    if (b.score !== a.score) return b.score - a.score;
    return a.scheme_id.localeCompare(b.scheme_id);
  });

  const truncated =
    opts.max_results && matched.length > opts.max_results
      ? matched.slice(0, opts.max_results)
      : matched;

  const message =
    truncated.length === 0
      ? "No schemes matched this profile based on published eligibility rules. Try adjusting income, occupation, category, or disability fields, or browse GET /schemes for the full catalogue. Always verify with the implementing office before applying."
      : null;

  const freshness = cataloguePayload();
  return {
    matched: truncated,
    excluded,
    needs_verification,
    message,
    count: truncated.length,
    district: profile.district ?? null,
    state: profile.state || null,
    country: profile.country || "India",
    catalogue: freshness.catalogue,
    is_stale: freshness.is_stale,
  };
}
