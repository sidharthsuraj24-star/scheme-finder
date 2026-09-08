/** Template explanations — mirror backend/app/explanations.py (no LLM). */

import type { LocalizedText, MatchProfile, SchemeRecord } from "./types";

export const DISCLAIMER_EN =
  "Based on published eligibility rules only; confirm with the implementing office. Not legal advice.";
export const DISCLAIMER_ML =
  "പ്രസിദ്ധീകരിച്ച യോഗ്യതാ നിബന്ധനകളെ അടിസ്ഥാനമാക്കി മാത്രം; നടപ്പാക്കുന്ന ഓഫീസുമായി സ്ഥിരീകരിക്കുക. നിയമ ഉപദേശമല്ല.";

function fmtIncome(value: number | null | undefined): string {
  if (value == null) return "n/a";
  return `Rs.${Math.trunc(value).toLocaleString("en-IN")}`;
}

function rulePhraseEn(rule: string, scheme: SchemeRecord, profile: MatchProfile): string {
  const rules = (scheme.eligibility_rules || {}) as Record<string, unknown>;
  switch (rule) {
    case "min_age":
      return `age ${profile.age} meets minimum age ${rules.min_age}`;
    case "max_age":
      return `age ${profile.age} within maximum age ${rules.max_age}`;
    case "max_annual_income":
      return `annual income ${fmtIncome(profile.annual_income)} within cap ${fmtIncome(rules.max_annual_income as number)}`;
    case "max_monthly_household_income":
      return `monthly household income ${fmtIncome(profile.monthly_household_income)} within cap ${fmtIncome(rules.max_monthly_household_income as number)}`;
    case "gender":
      return `gender '${profile.gender}' matches required '${rules.gender}'`;
    case "marital_status":
      return `marital status '${profile.marital_status}' is in allowed list`;
    case "deserted_7_years_over_50":
      return `deserted case with age ${profile.age} (≥50 required)`;
    case "disability_required":
      return "disability requirement satisfied";
    case "min_disability_percent":
      return `disability ${profile.disability_percent}% meets minimum ${rules.min_disability_percent}%`;
    case "occupations":
      return "occupation intersects scheme occupation list";
    case "categories":
      return "category intersects scheme category list";
    case "states":
      return `state '${profile.state || "Kerala"}' is in scheme states`;
    case "land_ownership":
      return "land ownership requirement satisfied";
    case "land_ownership_landless":
      return "profile indicates landless / no ownership";
    case "maternity_required":
      return "maternity / recent delivery signal present (pregnant, lactating, or child ≤6 months)";
    case "primary_breadwinner_deceased_required":
      return "primary breadwinner deceased flag set";
    default:
      return rule.replace(/_/g, " ");
  }
}

function rulePhraseMl(rule: string, scheme: SchemeRecord, profile: MatchProfile): string {
  const rules = (scheme.eligibility_rules || {}) as Record<string, unknown>;
  switch (rule) {
    case "min_age":
      return `പ്രായം ${profile.age} ഏറ്റവും കുറഞ്ഞ പ്രായം ${rules.min_age} നിറവേറ്റുന്നു`;
    case "max_annual_income":
      return `വാർഷിക വരുമാനം ${fmtIncome(profile.annual_income)} പരിധി ${fmtIncome(rules.max_annual_income as number)} യിൽ ഉൾപ്പെടുന്നു`;
    case "max_monthly_household_income":
      return `മാസ വരുമാനം ${fmtIncome(profile.monthly_household_income)} പരിധിക്കുള്ളിൽ`;
    case "gender":
      return `ലിംഗം '${profile.gender}' യോജിക്കുന്നു`;
    case "marital_status":
      return `വൈവാഹിക നില '${profile.marital_status}' അനുവദനീയമാണ്`;
    case "disability_required":
      return "ഭിന്നശേഷി നിബന്ധന നിറവേറ്റുന്നു";
    case "min_disability_percent":
      return `ഭിന്നശേഷി ${profile.disability_percent}% കുറഞ്ഞത് ${rules.min_disability_percent}% നിറവേറ്റുന്നു`;
    case "occupations":
      return "തൊഴിൽ പട്ടികയുമായി യോജിക്കുന്നു";
    case "categories":
      return "വിഭാഗം പട്ടികയുമായി യോജിക്കുന്നു";
    case "states":
      return `സംസ്ഥാനം '${profile.state || "Kerala"}' യോജിക്കുന്നു`;
    case "land_ownership":
      return "ഭൂമി ഉടമസ്ഥത നിബന്ധന നിറവേറ്റുന്നു";
    case "maternity_required":
      return "ഗർഭം / മുലയൂട്ടൽ / 6 മാസത്തിനുള്ളിൽ കുട്ടി എന്ന സിഗ്നൽ ഉണ്ട്";
    case "primary_breadwinner_deceased_required":
      return "പ്രധാന വരുമാനദാതാവ് മരിച്ചുവെന്ന ഫ്ലാഗ് സജ്ജമാണ്";
    default:
      return rule.replace(/_/g, " ") + " [ML]";
  }
}

export function buildExplanation(args: {
  scheme: SchemeRecord;
  profile: MatchProfile;
  matched_rules: string[];
  unmatched_rules: string[];
  missing_fields: string[];
  status: string;
}): LocalizedText {
  const { scheme, profile, matched_rules, unmatched_rules, missing_fields, status } = args;
  const name_en = (scheme.scheme_name || {}).en || scheme.id || "scheme";
  const name_ml = (scheme.scheme_name || {}).ml || name_en;

  let body_en: string;
  let body_ml: string;
  if (matched_rules.length) {
    body_en = matched_rules.map((r) => rulePhraseEn(r, scheme, profile)).join("; ") + ".";
    body_ml = matched_rules.map((r) => rulePhraseMl(r, scheme, profile)).join("; ") + ".";
  } else {
    body_en = "No structured hard-filter fields constrained this match.";
    body_ml = "ഘടനാപരമായ കഠിന ഫിൽട്ടറുകൾ ഈ പൊരുത്തത്തെ നിയന്ത്രിച്ചില്ല.";
  }

  const prefix_en =
    status === "uncertain"
      ? `Possibly relevant for ${name_en} (needs verification). `
      : `Likely eligible for ${name_en}: `;
  const prefix_ml =
    status === "uncertain"
      ? `${name_ml} — സ്ഥിരീകരണം ആവശ്യം. `
      : `${name_ml} യ്ക്ക് യോഗ്യതയുണ്ടാകാം: `;

  let extra_en = "";
  let extra_ml = "";
  if (missing_fields.length) {
    extra_en += ` Missing profile fields: ${missing_fields.join(", ")}.`;
    extra_ml += ` കുറവുള്ള ഫീൽഡുകൾ: ${missing_fields.join(", ")}.`;
  }
  if (unmatched_rules.length) {
    extra_en += ` Unmatched: ${unmatched_rules.join(", ")}.`;
  }
  const rules = (scheme.eligibility_rules || {}) as Record<string, unknown>;
  if (rules.verify) {
    const notes = String(rules.verify_notes || "");
    extra_en += " Official rules marked verify=true";
    if (notes) {
      extra_en += ` (${notes.slice(0, 180)}${notes.length > 180 ? "…" : ""})`;
    }
    extra_en += ".";
    extra_ml += " ഔദ്യോഗിക നിബന്ധനകൾ verify=true ആയി അടയാളപ്പെടുത്തിയിരിക്കുന്നു.";
  }

  return {
    en: (prefix_en + body_en + extra_en + " " + DISCLAIMER_EN).trim(),
    ml: (prefix_ml + body_ml + extra_ml + " " + DISCLAIMER_ML).trim(),
  };
}
