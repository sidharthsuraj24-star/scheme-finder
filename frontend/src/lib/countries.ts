/** Curated countries supported in the wizard (not worldwide). */
export const SUPPORTED_COUNTRIES = [
  "India",
  "Bangladesh",
  "Nepal",
  "Sri Lanka",
  "Maldives",
  "United States",
  "United Kingdom",
] as const;

export type SupportedCountry = (typeof SUPPORTED_COUNTRIES)[number];

export const DEFAULT_COUNTRY: SupportedCountry = "India";

/** Small fixed region lists for non-India countries; free-text also allowed. */
export const COUNTRY_REGIONS: Record<string, readonly string[]> = {
  Bangladesh: [
    "Dhaka",
    "Chattogram",
    "Khulna",
    "Rajshahi",
    "Barishal",
    "Sylhet",
    "Rangpur",
    "Mymensingh",
  ],
  Nepal: [
    "Koshi",
    "Madhesh",
    "Bagmati",
    "Gandaki",
    "Lumbini",
    "Karnali",
    "Sudurpashchim",
  ],
  "Sri Lanka": [
    "Western",
    "Central",
    "Southern",
    "Northern",
    "Eastern",
    "North Western",
    "North Central",
    "Uva",
    "Sabaragamuwa",
  ],
  Maldives: ["Malé", "Addu", "Other atoll / island"],
  "United States": [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "District of Columbia",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
  ],
  /** UK nations — devolved benefits (e.g. Scottish Child Payment) are nation-tagged. */
  "United Kingdom": ["England", "Scotland", "Wales", "Northern Ireland"],
};

export function isSupportedCountry(name: string | null | undefined): boolean {
  if (!name) return false;
  return (SUPPORTED_COUNTRIES as readonly string[]).includes(name);
}

export function currencySymbol(country: string | null | undefined): string {
  switch (country) {
    case "Bangladesh":
      return "৳";
    case "Nepal":
      return "रू";
    case "Sri Lanka":
      return "Rs";
    case "Maldives":
      return "MVR";
    case "United States":
      return "$";
    case "United Kingdom":
      return "£";
    default:
      return "₹";
  }
}
