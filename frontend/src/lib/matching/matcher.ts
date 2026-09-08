/** Deterministic eligibility matcher — port of backend/app/matcher.py */

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

  // --- states ---
  const schemeStates = (rules.states as string[] | undefined) || [];
  if (schemeStates.length) {
    const profileState = (profile.state || "Kerala").trim();
    const allowed = new Set(schemeStates.map(norm));
    if (allowed.has(norm(profileState)) || allowed.has("india")) {
      result.ok("states");
    } else {
      result.fail("states");
    }
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
  const maxAnnual = rules.max_annual_income as number | undefined | null;
  const maxMonthly = rules.max_monthly_household_income as number | undefined | null;
  if (maxAnnual != null) {
    if (profile.annual_income == null) result.miss("annual_income");
    else if (Number(profile.annual_income) > Number(maxAnnual)) result.fail("max_annual_income");
    else result.ok("max_annual_income");
  }
  if (maxMonthly != null) {
    if (profile.monthly_household_income == null) result.miss("monthly_household_income");
    else if (Number(profile.monthly_household_income) > Number(maxMonthly))
      result.fail("max_monthly_household_income");
    else result.ok("max_monthly_household_income");
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
  const schemeOccs = (rules.occupations as string[] | undefined) || [];
  if (schemeOccs.length) {
    const profileOccs = normSet(profile.occupations);
    const schemeOccsN = normSet(schemeOccs);
    if (!profileOccs.size) result.miss("occupations");
    else {
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

    let intersection = false;
    for (const c of profileCats) {
      if (schemeCatsN.has(c)) {
        intersection = true;
        break;
      }
    }

    if (intersection) {
      result.ok("categories");
    } else if (!profileCats.size) {
      result.miss("categories");
      if (seccOnly) result.uncertain = true;
    } else if (seccOnly) {
      result.miss("categories");
      result.uncertain = true;
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
  if (rules.maternity_required) {
    const pregnant = profile.is_pregnant;
    const lactating = profile.is_lactating;
    const childMonths = profile.child_age_months;
    const positive =
      pregnant === true ||
      lactating === true ||
      (childMonths != null && Number(childMonths) >= 0 && Number(childMonths) <= 6);
    const explicitNegative =
      pregnant === false && lactating !== true && childMonths == null;
    const allUnknown = pregnant == null && lactating == null && childMonths == null;
    if (positive) result.ok("maternity_required");
    else if (explicitNegative) result.fail("maternity_required");
    else if (allUnknown) result.miss("is_pregnant");
    else if (
      pregnant === false &&
      lactating === false &&
      (childMonths == null || Number(childMonths) > 6)
    ) {
      result.fail("maternity_required");
    } else {
      result.miss("is_pregnant");
    }
  }

  // --- NFBS breadwinner ---
  if (rules.primary_breadwinner_deceased_required) {
    const flag = profile.primary_breadwinner_deceased;
    if (flag === true) result.ok("primary_breadwinner_deceased_required");
    else if (flag === false) result.fail("primary_breadwinner_deceased_required");
    else result.miss("primary_breadwinner_deceased");
  }

  return result;
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

  for (const scheme of schemes) {
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

  return {
    matched: truncated,
    excluded,
    needs_verification,
    message,
    count: truncated.length,
  };
}
