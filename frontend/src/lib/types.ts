export type Lang = "en" | "ml" | "hi";

export type IncomeInputMode = "monthly" | "yearly";

export interface ProfileAnswers {
  /** ISO-ish country name; default India for share-link backward compat */
  country: string | null;
  /** State/UT (India) or region/province (other countries) */
  state: string | null;
  age: number | null;
  /**
   * Amount the user typed in the wizard, in the units of income_mode.
   * Prefer yearly mode for clarity (users often type annual figures).
   */
  income_amount: number | null;
  /** Monthly vs yearly entry; API gets annual_income or monthly_household_income accordingly. */
  income_mode: IncomeInputMode;
  /**
   * @deprecated Prefer income_amount + income_mode. Kept as monthly equivalent for share links.
   */
  monthly_household_income: number | null;
  occupation: string | null;
  categories: string[];
  land_ownership: "yes" | "no" | null;
  disability: "no" | "yes" | null;
  disability_percent: number | null;
  district: string | null;
  gender: string | null;
  marital_status: string | null;
  /** female-only: pregnant | lactating | neither */
  maternity: "pregnant" | "lactating" | "neither" | null;
  primary_breadwinner_deceased: "yes" | "no" | null;
}

export interface LocalizedText {
  en?: string;
  ml?: string;
  hi?: string;
}

export interface MatchedScheme {
  scheme_id: string;
  score: number;
  status: "likely_eligible" | "uncertain" | "not_eligible";
  matched_rules: string[];
  unmatched_rules: string[];
  missing_profile_fields: string[];
  verify: boolean;
  verify_notes: string;
  explanation: LocalizedText;
  scheme_name: LocalizedText;
  description?: LocalizedText | null;
  benefits?: LocalizedText | string[] | Record<string, unknown> | null;
  documents?: LocalizedText | string[] | Record<string, unknown> | null;
  how_to_apply?: LocalizedText | null;
  apply_url?: string | null;
  official_source_url?: string | null;
  last_verified?: string | null;
  tags?: string[];
}

export interface MatchResponse {
  matched: MatchedScheme[];
  excluded: { scheme_id: string; status: string; reasons: string[] }[];
  needs_verification: {
    scheme_id: string;
    status: string;
    verify_notes: string;
  }[];
  message?: string | null;
  count: number;
  district?: string | null;
  state?: string | null;
  country?: string | null;
  catalogue?: {
    updated_as_of?: string;
    stale_after_days?: number;
    disclaimer?: string;
    [key: string]: unknown;
  };
  is_stale?: boolean;
  /** PRICE ICE 360° household band (India only; UX/ranking — not GoI statutory). */
  income_band?: string | null;
  income_band_label?: string | null;
  income_class?: string | null;
  income_band_source?: string | null;
}

export interface MatchRequestBody {
  profile: {
    age: number;
    gender?: string;
    country?: string;
    state: string;
    district?: string;
    marital_status?: string;
    monthly_household_income?: number;
    annual_income?: number;
    occupations: string[];
    categories: string[];
    disability?: boolean;
    disability_percent?: number | null;
    land_ownership: string;
    is_student?: boolean;
    is_pregnant?: boolean;
    is_lactating?: boolean;
    primary_breadwinner_deceased?: boolean;
  };
  options: {
    include_verify_uncertain: boolean;
    lang: Lang;
    max_results: number;
  };
}
