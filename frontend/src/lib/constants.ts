export const KERALA_DISTRICTS = [
  "Thiruvananthapuram",
  "Kollam",
  "Pathanamthitta",
  "Alappuzha",
  "Kottayam",
  "Idukki",
  "Ernakulam",
  "Thrissur",
  "Palakkad",
  "Malappuram",
  "Kozhikode",
  "Wayanad",
  "Kannur",
  "Kasaragod",
] as const;

export const OCCUPATIONS = [
  "agricultural_labour",
  "farmer",
  "student",
  "unemployed",
  "other",
] as const;

export const CATEGORIES = [
  "none",
  "General",
  "SC",
  "ST",
  "OBC",
  "BPL",
] as const;

export const GENDERS = ["female", "male", "other"] as const;

export const MARITAL_STATUSES = [
  "unmarried",
  "married",
  "widow",
  "widower",
  "divorced",
  "deserted",
] as const;

/** Wizard question steps after welcome (country → region/state → … → details). */
export const TOTAL_STEPS = 9;

export const DISTRICT_FREE_TEXT_MAX = 64;
