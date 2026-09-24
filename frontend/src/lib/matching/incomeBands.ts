/**
 * India household income-band classification (PRICE ICE 360°).
 *
 * Source of truth (NOT a Government of India statutory definition):
 * PRICE ICE 360° / "The Rise of India's Middle Class" — 2020–21 prices.
 * Primary PDF: https://www.price360.in/Executive_Summary_Middle_Class.pdf
 *
 * ₹15 lakh is the Seekers → Strivers cut (Strivers are ₹15–30 lakh annual).
 * These bands are for UX labels and soft ranking only — NEVER invent scheme
 * eligibility ceilings (max_annual_income) from PRICE bands.
 * INDIA-ONLY: never map USD (or other currencies) onto these INR thresholds;
 * non-India countries must return null band fields and skip PRICE boosts.
 *
 * Mirror of backend/app/income_bands.py — keep thresholds/labels in sync.
 */

export const INCOME_BAND_SOURCE =
  "PRICE ICE 360° (2020–21 prices; not official GoI)";

export const INCOME_BAND_NOTE =
  "India-only household income bands from PRICE ICE 360° / The Rise of India's Middle Class " +
  "(2020–21 prices). Not a Government of India statutory classification. " +
  "Used for UX labels and soft ranking only — does not change scheme eligibility rules. " +
  "₹15 lakh is the Seekers→Strivers boundary (Strivers: ₹15–30 lakh). " +
  "Do not apply these INR bands to United States or other countries.";

export interface IncomeBandResult {
  band_id: string | null;
  band_label: string | null;
  income_class: string | null;
  source: string | null;
  note: string | null;
}

const BANDS: Array<{
  lo: number;
  hi: number | null;
  band_id: string;
  band_label: string;
}> = [
  { lo: 0, hi: 124_999, band_id: "destitute", band_label: "Destitute" },
  { lo: 125_000, hi: 499_999, band_id: "aspirer", band_label: "Aspirer" },
  {
    lo: 500_000,
    hi: 1_499_999,
    band_id: "seeker",
    band_label: "Middle class (Seekers)",
  },
  {
    lo: 1_500_000,
    hi: 2_999_999,
    band_id: "striver",
    band_label: "Upper middle class (Strivers)",
  },
  { lo: 3_000_000, hi: 4_999_999, band_id: "near_rich", band_label: "Near rich" },
  { lo: 5_000_000, hi: 9_999_999, band_id: "clear_rich", band_label: "Clear rich" },
  {
    lo: 10_000_000,
    hi: 19_999_999,
    band_id: "sheer_rich",
    band_label: "Sheer rich",
  },
  { lo: 20_000_000, hi: null, band_id: "super_rich", band_label: "Super rich" },
];

const BAND_TO_CLASS: Record<string, string> = {
  destitute: "destitute",
  aspirer: "aspirer",
  seeker: "middle_class",
  striver: "middle_class",
  near_rich: "rich",
  clear_rich: "rich",
  sheer_rich: "rich",
  super_rich: "rich",
};

export const BAND_RANGE_HINT: Record<string, string> = {
  destitute: "under ₹1.25 lakh",
  aspirer: "₹1.25–5 lakh",
  seeker: "₹5–15 lakh",
  striver: "₹15–30 lakh",
  near_rich: "₹30–50 lakh",
  clear_rich: "₹50 lakh–1 crore",
  sheer_rich: "₹1–2 crore",
  super_rich: "₹2 crore+",
};

function normCountry(country: string | null | undefined): string {
  if (!country) return "india";
  return String(country)
    .trim()
    .toLowerCase()
    .replace(/-/g, "_")
    .replace(/ /g, "_");
}

export function isIndiaCountry(country: string | null | undefined): boolean {
  return normCountry(country || "India") === "india";
}

const EMPTY: IncomeBandResult = {
  band_id: null,
  band_label: null,
  income_class: null,
  source: null,
  note: null,
};

export function classifyIndiaAnnualIncome(
  annual: number | null | undefined,
  country: string | null | undefined = "India",
): IncomeBandResult {
  // Hard country gate — PRICE INR thresholds must never run for US/others.
  if (!isIndiaCountry(country)) return { ...EMPTY };
  if (annual == null) return { ...EMPTY };
  const value = Number(annual);
  if (!Number.isFinite(value) || value < 0) return { ...EMPTY };

  for (const b of BANDS) {
    if (value < b.lo) continue;
    if (b.hi == null || value <= b.hi) {
      return {
        band_id: b.band_id,
        band_label: b.band_label,
        income_class: BAND_TO_CLASS[b.band_id],
        source: INCOME_BAND_SOURCE,
        note: INCOME_BAND_NOTE,
      };
    }
  }
  return {
    band_id: "super_rich",
    band_label: "Super rich",
    income_class: "rich",
    source: INCOME_BAND_SOURCE,
    note: INCOME_BAND_NOTE,
  };
}

export function formatBandSentence(band: IncomeBandResult): string | null {
  if (!band.band_id || !band.band_label) return null;
  const hint = BAND_RANGE_HINT[band.band_id] || "";
  const rangePart = hint ? ` (${hint})` : "";
  return (
    `Based on PRICE ICE 360 household bands (2020–21 prices): ` +
    `${band.band_label}${rangePart}. ` +
    `Not an official government classification — does not change scheme rules; ` +
    `only helps sort and explain results.`
  );
}

/** Soft ranking boosts — mirror backend/app/income_bands.py */
export const MIDDLE_HIGH_BOOST_TAGS: Record<string, number> = {
  "upper-middle-class": 0.1,
  "high-income-eligible": 0.1,
  "middle-class": 0.08,
  tax: 0.06,
  savings: 0.06,
  universal: 0.05,
};
export const MIDDLE_HIGH_BOOST_CAP = 0.12;
export const MIDDLE_HIGH_BANDS = new Set([
  "seeker",
  "striver",
  "near_rich",
  "clear_rich",
  "sheer_rich",
  "super_rich",
]);

export const LOW_INCOME_BOOST_TAGS: Record<string, number> = {
  welfare: 0.04,
  bpl: 0.04,
  pension: 0.03,
};
export const LOW_INCOME_IMPLIES_BOOST = 0.04;
export const LOW_INCOME_BOOST_CAP = 0.05;
export const LOW_INCOME_BANDS = new Set(["destitute", "aspirer"]);

export function incomeBandScoreBoost(
  bandId: string | null | undefined,
  tags: string[] | null | undefined,
  impliesLowIncome = false,
): number {
  if (!bandId) return 0;
  const tagSet = new Set(
    (tags || []).map((t) => String(t).trim().toLowerCase()).filter(Boolean),
  );

  if (MIDDLE_HIGH_BANDS.has(bandId)) {
    let bump = 0;
    for (const [tag, amount] of Object.entries(MIDDLE_HIGH_BOOST_TAGS)) {
      if (tagSet.has(tag)) bump = Math.max(bump, amount);
    }
    return Math.min(bump, MIDDLE_HIGH_BOOST_CAP);
  }

  if (LOW_INCOME_BANDS.has(bandId)) {
    let bump = 0;
    for (const [tag, amount] of Object.entries(LOW_INCOME_BOOST_TAGS)) {
      if (tagSet.has(tag)) bump = Math.max(bump, amount);
    }
    if (impliesLowIncome) bump = Math.max(bump, LOW_INCOME_IMPLIES_BOOST);
    return Math.min(bump, LOW_INCOME_BOOST_CAP);
  }

  return 0;
}
