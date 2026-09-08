/** Input validation mirroring backend/app/models.py caps. */

import {
  AGE_MAX,
  AGE_MIN,
  FLAGS_MAX_KEYS,
  INCOME_ANNUAL_MAX,
  INCOME_MONTHLY_MAX,
  LIST_MAX,
  STR_MAX,
  ValidationError,
  type MatchOptions,
  type MatchProfile,
} from "./types";

function coerceStrList(v: unknown): string[] {
  if (v == null) return [];
  let items: string[];
  if (typeof v === "string") {
    items = v
      .replace(/;/g, ",")
      .split(",")
      .map((p) => p.trim())
      .filter(Boolean);
  } else if (Array.isArray(v)) {
    items = v.map((x) => String(x));
  } else {
    items = [String(v)];
  }
  if (items.length > LIST_MAX) {
    throw new ValidationError("list_too_long", `list longer than ${LIST_MAX} items`);
  }
  for (const item of items) {
    if (item.length > STR_MAX) {
      throw new ValidationError("item_too_long", `list item longer than ${STR_MAX} chars`);
    }
  }
  return items;
}

function limitFlags(v: unknown): Record<string, unknown> {
  if (v == null) return {};
  if (typeof v !== "object" || Array.isArray(v)) {
    throw new ValidationError("bad_flags", "flags must be an object");
  }
  const entries = Object.entries(v as Record<string, unknown>);
  if (entries.length > FLAGS_MAX_KEYS) {
    throw new ValidationError("flags_too_many", `flags has more than ${FLAGS_MAX_KEYS} keys`);
  }
  const out: Record<string, unknown> = {};
  for (const [k, val] of entries) {
    if (k.length > STR_MAX) {
      throw new ValidationError("flags_key_long", "flags key too long");
    }
    if (val !== null && typeof val === "object") {
      throw new ValidationError("flags_nested", "flags values must be scalars");
    }
    if (typeof val === "string" && val.length > 256) {
      throw new ValidationError("flags_value_long", "flags string value too long");
    }
    out[k] = val;
  }
  return out;
}

function optNumber(
  v: unknown,
  field: string,
  opts: { min?: number; max?: number; integer?: boolean } = {},
): number | null {
  if (v == null || v === "") return null;
  const n = typeof v === "number" ? v : Number(v);
  if (!Number.isFinite(n)) {
    throw new ValidationError("bad_number", `${field} must be a number`);
  }
  if (opts.integer && !Number.isInteger(n)) {
    throw new ValidationError("bad_integer", `${field} must be an integer`);
  }
  if (opts.min != null && n < opts.min) {
    throw new ValidationError("below_min", `${field} below minimum`);
  }
  if (opts.max != null && n > opts.max) {
    throw new ValidationError("above_max", `${field} above maximum`);
  }
  return n;
}

function optBool(v: unknown): boolean | null {
  if (v == null) return null;
  if (typeof v === "boolean") return v;
  if (v === "true" || v === 1 || v === "1") return true;
  if (v === "false" || v === 0 || v === "0") return false;
  return Boolean(v);
}

function optStr(v: unknown, field: string, max = STR_MAX): string | null {
  if (v == null) return null;
  const s = String(v);
  if (s.length > max) {
    throw new ValidationError("str_too_long", `${field} longer than ${max} chars`);
  }
  return s;
}

function landOwnership(v: unknown): boolean | string | null {
  if (v == null) return null;
  if (typeof v === "boolean") return v;
  const s = String(v);
  if (s.length > STR_MAX) {
    throw new ValidationError("land_too_long", `land_ownership longer than ${STR_MAX} chars`);
  }
  return s;
}

/** Build MatchProfile from a plain object (nested profile or flat fields). */
export function buildProfile(raw: Record<string, unknown>): MatchProfile {
  const age = optNumber(raw.age, "age", { min: AGE_MIN, max: AGE_MAX, integer: true });
  let annual = optNumber(raw.annual_income, "annual_income", {
    min: 0,
    max: INCOME_ANNUAL_MAX,
  });
  let monthly = optNumber(raw.monthly_household_income, "monthly_household_income", {
    min: 0,
    max: INCOME_MONTHLY_MAX,
  });

  if (annual == null && monthly != null) {
    const derived = monthly * 12;
    if (derived > INCOME_ANNUAL_MAX) {
      throw new ValidationError("derived_income", "derived annual_income exceeds cap");
    }
    annual = derived;
  }
  if (monthly == null && annual != null) {
    monthly = annual / 12;
  }

  let disability = optBool(raw.disability);
  const disability_percent = optNumber(raw.disability_percent, "disability_percent", {
    min: 0,
    max: 100,
  });
  if (disability == null && disability_percent != null) {
    disability = disability_percent > 0;
  }

  let occupations = coerceStrList(raw.occupations);
  const is_student = optBool(raw.is_student);
  if (is_student && !occupations.some((o) => o.toLowerCase() === "student")) {
    occupations = [...occupations, "student"];
  }

  return {
    age,
    gender: optStr(raw.gender, "gender"),
    state: optStr(raw.state, "state") || "Kerala",
    district: optStr(raw.district, "district"),
    marital_status: optStr(raw.marital_status, "marital_status"),
    annual_income: annual,
    monthly_household_income: monthly,
    occupations,
    categories: coerceStrList(raw.categories),
    disability,
    disability_percent,
    land_ownership: landOwnership(raw.land_ownership),
    language: optStr(raw.language, "language", 16),
    is_student,
    is_pregnant: optBool(raw.is_pregnant),
    pregnancy_order: optNumber(raw.pregnancy_order, "pregnancy_order", {
      min: 0,
      max: 20,
      integer: true,
    }),
    is_lactating: optBool(raw.is_lactating),
    child_age_months: optNumber(raw.child_age_months, "child_age_months", {
      min: 0,
      max: 216,
      integer: true,
    }),
    housing_status: optStr(raw.housing_status, "housing_status"),
    residence_type: optStr(raw.residence_type, "residence_type"),
    income_tax_payer: optBool(raw.income_tax_payer),
    kawwf_member: optBool(raw.kawwf_member),
    agri_labour_years: optNumber(raw.agri_labour_years, "agri_labour_years", {
      min: 0,
      max: 80,
      integer: true,
    }),
    primary_breadwinner_deceased: optBool(raw.primary_breadwinner_deceased),
    deceased_breadwinner_age: optNumber(raw.deceased_breadwinner_age, "deceased_breadwinner_age", {
      min: AGE_MIN,
      max: AGE_MAX,
      integer: true,
    }),
    flags: limitFlags(raw.flags),
  };
}

const FLAT_KEYS = [
  "age",
  "gender",
  "state",
  "district",
  "marital_status",
  "annual_income",
  "monthly_household_income",
  "occupations",
  "categories",
  "disability",
  "disability_percent",
  "land_ownership",
  "language",
  "is_student",
  "is_pregnant",
  "pregnancy_order",
  "is_lactating",
  "child_age_months",
  "housing_status",
  "residence_type",
  "income_tax_payer",
  "kawwf_member",
  "agri_labour_years",
  "primary_breadwinner_deceased",
  "deceased_breadwinner_age",
  "flags",
] as const;

/** Resolve nested {profile, options} or flat Phase-2 body. */
export function resolveMatchRequest(body: unknown): {
  profile: MatchProfile;
  options: MatchOptions;
} {
  if (body == null || typeof body !== "object" || Array.isArray(body)) {
    throw new ValidationError("bad_body", "Request body must be a JSON object");
  }
  const raw = body as Record<string, unknown>;
  const base: Record<string, unknown> =
    raw.profile && typeof raw.profile === "object" && !Array.isArray(raw.profile)
      ? { ...(raw.profile as Record<string, unknown>) }
      : {};

  for (const key of FLAT_KEYS) {
    if (raw[key] !== undefined && raw[key] !== null) {
      base[key] = raw[key];
    }
  }
  if (base.state == null) base.state = "Kerala";

  const profile = buildProfile(base);

  const optsRaw =
    raw.options && typeof raw.options === "object" && !Array.isArray(raw.options)
      ? { ...(raw.options as Record<string, unknown>) }
      : {};
  if (typeof raw.lang === "string") optsRaw.lang = raw.lang;
  if (typeof raw.language === "string" && optsRaw.lang == null) optsRaw.lang = raw.language;

  const include =
    optsRaw.include_verify_uncertain == null
      ? true
      : Boolean(optsRaw.include_verify_uncertain);
  const lang = typeof optsRaw.lang === "string" ? optsRaw.lang.slice(0, 8) : "en";
  let max_results = 50;
  if (optsRaw.max_results != null) {
    const n = Number(optsRaw.max_results);
    if (!Number.isFinite(n) || n < 1 || n > 100) {
      throw new ValidationError("bad_max_results", "max_results must be 1..100");
    }
    max_results = Math.floor(n);
  }

  return {
    profile,
    options: { include_verify_uncertain: include, lang, max_results },
  };
}
