export type Lang = "en" | "ml";

export interface ProfileAnswers {
  age: number | null;
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
}

export interface MatchRequestBody {
  profile: {
    age: number;
    gender?: string;
    state: string;
    district?: string;
    marital_status?: string;
    monthly_household_income: number;
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
