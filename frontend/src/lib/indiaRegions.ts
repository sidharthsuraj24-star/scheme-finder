/**
 * Canonical States + Union Territories of India (as of 2026).
 * 28 States + 8 UTs. English names are canonical for matching.
 */

export type RegionKind = "state" | "ut";

export interface IndiaRegion {
  /** Canonical English name used in profiles / scheme.states */
  name: string;
  kind: RegionKind;
  /** Optional short / local label for UI */
  short?: string;
  /** ISO 3166-2:IN code where stable */
  code?: string;
}

/** All current States (28) + UTs (8), sorted with States first then UTs. */
export const INDIA_REGIONS: readonly IndiaRegion[] = [
  // --- States (28) ---
  { name: "Andhra Pradesh", kind: "state", code: "IN-AP" },
  { name: "Arunachal Pradesh", kind: "state", code: "IN-AR" },
  { name: "Assam", kind: "state", code: "IN-AS" },
  { name: "Bihar", kind: "state", code: "IN-BR" },
  { name: "Chhattisgarh", kind: "state", code: "IN-CT" },
  { name: "Goa", kind: "state", code: "IN-GA" },
  { name: "Gujarat", kind: "state", code: "IN-GJ" },
  { name: "Haryana", kind: "state", code: "IN-HR" },
  { name: "Himachal Pradesh", kind: "state", code: "IN-HP" },
  { name: "Jharkhand", kind: "state", code: "IN-JH" },
  { name: "Karnataka", kind: "state", code: "IN-KA" },
  { name: "Kerala", kind: "state", short: "കേരളം", code: "IN-KL" },
  { name: "Madhya Pradesh", kind: "state", code: "IN-MP" },
  { name: "Maharashtra", kind: "state", code: "IN-MH" },
  { name: "Manipur", kind: "state", code: "IN-MN" },
  { name: "Meghalaya", kind: "state", code: "IN-ML" },
  { name: "Mizoram", kind: "state", code: "IN-MZ" },
  { name: "Nagaland", kind: "state", code: "IN-NL" },
  { name: "Odisha", kind: "state", code: "IN-OR" },
  { name: "Punjab", kind: "state", code: "IN-PB" },
  { name: "Rajasthan", kind: "state", code: "IN-RJ" },
  { name: "Sikkim", kind: "state", code: "IN-SK" },
  { name: "Tamil Nadu", kind: "state", code: "IN-TN" },
  { name: "Telangana", kind: "state", code: "IN-TG" },
  { name: "Tripura", kind: "state", code: "IN-TR" },
  { name: "Uttar Pradesh", kind: "state", code: "IN-UP" },
  { name: "Uttarakhand", kind: "state", code: "IN-UT" },
  { name: "West Bengal", kind: "state", code: "IN-WB" },
  // --- Union Territories (8) ---
  { name: "Andaman and Nicobar Islands", kind: "ut", short: "A & N Islands", code: "IN-AN" },
  { name: "Chandigarh", kind: "ut", code: "IN-CH" },
  { name: "Dadra and Nagar Haveli and Daman and Diu", kind: "ut", short: "DNH & DD", code: "IN-DH" },
  { name: "Delhi", kind: "ut", short: "NCT of Delhi", code: "IN-DL" },
  { name: "Jammu and Kashmir", kind: "ut", short: "J&K", code: "IN-JK" },
  { name: "Ladakh", kind: "ut", code: "IN-LA" },
  { name: "Lakshadweep", kind: "ut", code: "IN-LD" },
  { name: "Puducherry", kind: "ut", code: "IN-PY" },
] as const;

export const DEFAULT_STATE = "Kerala";

export const INDIA_REGION_NAMES: readonly string[] = INDIA_REGIONS.map((r) => r.name);

const NAME_SET = new Set(INDIA_REGION_NAMES.map((n) => n.toLowerCase()));

export function isKnownIndiaRegion(name: string | null | undefined): boolean {
  if (!name) return false;
  return NAME_SET.has(name.trim().toLowerCase());
}

export function normalizeRegionName(name: string | null | undefined): string | null {
  if (!name) return null;
  const trimmed = name.trim();
  const hit = INDIA_REGIONS.find((r) => r.name.toLowerCase() === trimmed.toLowerCase());
  return hit ? hit.name : null;
}

/** Display label: English + optional short/local. */
export function regionLabel(region: IndiaRegion, preferLocal = false): string {
  if (preferLocal && region.short) return `${region.name} (${region.short})`;
  return region.short ? `${region.name}` : region.name;
}
