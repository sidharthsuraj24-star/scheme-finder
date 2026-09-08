/** Types mirroring backend/app/models.py for the Next.js matcher. */

export type StatusLiteral = "likely_eligible" | "uncertain" | "not_eligible";

export const AGE_MIN = 0;
export const AGE_MAX = 120;
export const INCOME_ANNUAL_MAX = 100_000_000;
export const INCOME_MONTHLY_MAX = 10_000_000;
export const LIST_MAX = 32;
export const STR_MAX = 64;
export const FLAGS_MAX_KEYS = 20;
export const MAX_BODY_BYTES = 64 * 1024;
export const RATE_LIMIT_WINDOW_SEC = 60;
export const RATE_LIMIT_MAX = 30;

export interface LocalizedText {
  en: string;
  ml: string;
}

export interface MatchProfile {
  age: number | null;
  gender: string | null;
  state: string;
  district: string | null;
  marital_status: string | null;
  annual_income: number | null;
  monthly_household_income: number | null;
  occupations: string[];
  categories: string[];
  disability: boolean | null;
  disability_percent: number | null;
  land_ownership: boolean | string | null;
  language: string | null;
  is_student: boolean | null;
  is_pregnant: boolean | null;
  pregnancy_order: number | null;
  is_lactating: boolean | null;
  child_age_months: number | null;
  housing_status: string | null;
  residence_type: string | null;
  income_tax_payer: boolean | null;
  kawwf_member: boolean | null;
  agri_labour_years: number | null;
  primary_breadwinner_deceased: boolean | null;
  deceased_breadwinner_age: number | null;
  flags: Record<string, unknown>;
}

export interface MatchOptions {
  include_verify_uncertain: boolean;
  lang: string;
  max_results: number;
}

export interface MatchedScheme {
  scheme_id: string;
  score: number;
  status: StatusLiteral;
  matched_rules: string[];
  unmatched_rules: string[];
  missing_profile_fields: string[];
  verify: boolean;
  verify_notes: string;
  explanation: LocalizedText;
  scheme_name: Record<string, string>;
  description?: Record<string, string> | null;
  benefits?: unknown;
  documents?: unknown;
  how_to_apply?: unknown;
  apply_url?: string | null;
  official_source_url?: string | null;
  tags: string[];
}

export interface ExcludedScheme {
  scheme_id: string;
  status: StatusLiteral;
  reasons: string[];
}

export interface NeedsVerificationItem {
  scheme_id: string;
  status: StatusLiteral;
  verify_notes: string;
}

export interface MatchResponse {
  matched: MatchedScheme[];
  excluded: ExcludedScheme[];
  needs_verification: NeedsVerificationItem[];
  message: string | null;
  count: number;
}

export interface SchemeRecord {
  id: string;
  scheme_name?: Record<string, string>;
  description?: Record<string, string>;
  eligibility_rules?: Record<string, unknown>;
  benefits?: unknown;
  required_documents?: unknown;
  how_to_apply?: unknown;
  apply_url?: string | null;
  official_source_url?: string | null;
  tags?: string[];
  [key: string]: unknown;
}

export interface SchemeSummary {
  id: string;
  scheme_name: Record<string, string>;
  tags: string[];
  official_source_url: string | null;
  verify: boolean;
}

export class ValidationError extends Error {
  code: string;
  constructor(code: string, message: string) {
    super(message);
    this.code = code;
    this.name = "ValidationError";
  }
}
