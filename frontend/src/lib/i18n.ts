import type { Lang } from "./types";

type Dict = Record<string, string>;

const en: Dict = {
  appTitle: "Scheme Finder",
  appSubtitle: "Find Kerala welfare schemes you may be eligible for",
  langEn: "English",
  langMl: "മലയാളം",
  progress: "Step {current} of {total}",
  next: "Next",
  back: "Back",
  submit: "Find schemes",
  startOver: "Start over",
  loading: "Searching schemes…",
  errorTitle: "Could not reach the server",
  errorRetry: "Try again",
  errorHint: "Check your connection, hard-refresh the page, and try again. (API is served from this site.)",
  shareCopyLink: "Copy link",
  shareCopied: "Link copied",
  shareWhatsApp: "Share on WhatsApp",
  shareMessage: "I found Kerala welfare schemes that may fit me on Scheme Finder:",
  shareCopyFailed: "Could not copy — copy the address bar link instead",

  zeroTitle: "No matching schemes right now",
  zeroBody:
    "Based on what you shared, we did not find a clear match. You can change your answers and try again, or ask your local panchayat / municipality for help.",
  resultsTitle: "Schemes that may fit you",
  resultsCount: "{count} scheme(s) found",
  verifyBadge: "Needs verification",
  uncertainBadge: "Uncertain — confirm locally",
  likelyBadge: "Likely eligible",
  benefits: "Benefits",
  documents: "Documents needed",
  howToApply: "How to apply",
  applyLink: "Open apply / official page",
  officialSource: "Official source",
  officialSourceConfirm: "Official source — confirm here",
  lastVerified: "Last verified: {date}",
  dataFreshConfirm:
    "Confirm eligibility on the official source before you apply.",
  dataStaleBanner:
    "Scheme data may be outdated (last updated {date}). Always confirm on the official site before applying.",
  dataFreshBanner:
    "Scheme data updated as of {date} · Curated central + Kerala set (not every scheme in India). Confirm eligibility on the official source before you apply.",
  resultsFooterDisclaimer:
    "This tool does not guarantee eligibility. Always confirm on the official source and with your local body before applying. Needs-verification matches are uncertain — never treat them as approved.",

  reason: "Why this may fit",
  expand: "Show details",
  collapse: "Hide details",
  disclaimer:
    "This is not legal advice and does not guarantee eligibility. Always confirm with your local body (panchayat / municipality / corporation) and the official portal before applying.",
  qAge: "How old are you?",
  qAgeHint: "Enter your age in years",
  qIncome: "What is your monthly household income?",
  qIncomeHint: "Approximate amount in ₹ (rupees)",
  qOccupation: "What do you do for work?",
  qCategory: "Do you belong to any of these categories?",
  qCategoryHint: "Select all that apply, or None",
  qLand: "Do you own cultivable land?",
  qDisability: "Do you have a disability?",
  qDisabilityPercent: "Disability percentage (if known)",
  qDisabilityPercentHint: "Optional — leave blank if unsure",
  qDistrict: "Which district do you live in?",
  qGender: "Gender",
  qMarital: "Marital status",
  yes: "Yes",
  no: "No",
  rupee: "₹",
  required: "Please answer this to continue",
  occ_agricultural_labour: "Agricultural labour",
  occ_farmer: "Farmer / landholding farmer",
  occ_student: "Student",
  occ_unemployed: "Unemployed",
  occ_other: "Other",
  cat_none: "None",
  cat_General: "General",
  cat_SC: "SC",
  cat_ST: "ST",
  cat_OBC: "OBC",
  cat_BPL: "BPL",
  gen_female: "Female",
  gen_male: "Male",
  gen_other: "Other",
  mar_unmarried: "Unmarried",
  mar_married: "Married",
  mar_widow: "Widow",
  mar_widower: "Widower",
  mar_divorced: "Divorced",
  mar_deserted: "Deserted",
  qMaternity: "Are you pregnant or a new mother?",
  qMaternityHint: "Needed for maternity schemes such as PMMVY / JSY",
  mat_pregnant: "Pregnant",
  mat_lactating: "Recently delivered / lactating",
  mat_neither: "Neither",
  qBreadwinner: "Has the main earning member of your household died?",
  qBreadwinnerHint: "Used for bereavement schemes such as NFBS",
  dataUpdated:
    "Scheme data updated as of 8 Sep 2026 · Curated central + Kerala set (not every scheme in India)",
  dataUpdatedShort: "Scheme data updated as of 8 Sep 2026",
  welcomeTitle: "Welcome",
  welcomeBody:
    "Answer a few simple questions. We will suggest government schemes that may help you.",
  start: "Start",
};

const ml: Dict = {
  appTitle: "പദ്ധതി കണ്ടെത്തൽ",
  appSubtitle: "നിങ്ങൾക്ക് യോഗ്യമായേക്കാവുന്ന കേരള ക്ഷേമ പദ്ധതികൾ കണ്ടെത്തുക",
  langEn: "English",
  langMl: "മലയാളം",
  progress: "ഘട്ടം {current} / {total}",
  next: "അടുത്തത്",
  back: "തിരികെ",
  submit: "പദ്ധതികൾ കണ്ടെത്തുക",
  startOver: "വീണ്ടും തുടങ്ങുക",
  loading: "പദ്ധതികൾ തിരയുന്നു…",
  errorTitle: "സെർവറുമായി ബന്ധപ്പെടാനായില്ല",
  errorRetry: "വീണ്ടും ശ്രമിക്കുക",
  errorHint: "കണക്ഷൻ പരിശോധിക്കുക, പേജ് ഹാർഡ്-റിഫ്രഷ് ചെയ്ത് വീണ്ടും ശ്രമിക്കുക. (API ഈ സൈറ്റിൽ നിന്ന് തന്നെ.)",
  shareCopyLink: "ലിങ്ക് പകർത്തുക",
  shareCopied: "ലിങ്ക് പകർത്തി",
  shareWhatsApp: "വാട്ട്‌സ്ആപ്പിൽ പങ്കിടുക",
  shareMessage: "സ്കീം ഫൈൻഡറിൽ എനിക്ക് യോജിച്ചേക്കാവുന്ന കേരള ക്ഷേമ പദ്ധതികൾ കണ്ടെത്തി:",
  shareCopyFailed: "പകർത്താനായില്ല — അഡ്രസ് ബാറിലെ ലിങ്ക് പകർത്തുക",

  zeroTitle: "ഇപ്പോൾ യോജിക്കുന്ന പദ്ധതികളില്ല",
  zeroBody:
    "നൽകിയ വിവരങ്ങൾ അനുസരിച്ച് വ്യക്തമായ പൊരുത്തം കണ്ടെത്തിയില്ല. ഉത്തരങ്ങൾ മാറ്റി വീണ്ടും ശ്രമിക്കാം, അല്ലെങ്കിൽ നിങ്ങളുടെ പഞ്ചായത്ത് / മുനിസിപ്പാലിറ്റിയിൽ ചോദിക്കുക.",
  resultsTitle: "നിങ്ങൾക്ക് യോജിച്ചേക്കാവുന്ന പദ്ധതികൾ",
  resultsCount: "{count} പദ്ധതി(കൾ) കണ്ടെത്തി",
  verifyBadge: "സ്ഥിരീകരണം വേണം",
  uncertainBadge: "അനിശ്ചിതം — പ്രാദേശികമായി ഉറപ്പാക്കുക",
  likelyBadge: "യോഗ്യതയുണ്ടാകാം",
  benefits: "ആനുകൂല്യങ്ങൾ",
  documents: "വേണ്ട രേഖകൾ",
  howToApply: "എങ്ങനെ അപേക്ഷിക്കാം",
  applyLink: "അപേക്ഷ / ഔദ്യോഗിക പേജ് തുറക്കുക",
  officialSource: "ഔദ്യോഗിക ഉറവിടം",
  officialSourceConfirm: "ഔദ്യോഗിക ഉറവിടം — ഇവിടെ സ്ഥിരീകരിക്കുക",
  lastVerified: "അവസാനം സ്ഥിരീകരിച്ചത്: {date}",
  dataFreshConfirm:
    "അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക ഉറവിടത്തിൽ യോഗ്യത സ്ഥിരീകരിക്കുക.",
  dataStaleBanner:
    "പദ്ധതി വിവരങ്ങൾ കാലഹരണപ്പെട്ടിരിക്കാം (അവസാനം പുതുക്കിയത് {date}). അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക സൈറ്റിൽ എല്ലായ്പ്പോഴും ഉറപ്പാക്കുക.",
  dataFreshBanner:
    "പദ്ധതി വിവരങ്ങൾ {date} വരെ പുതുക്കിയത് · തിരഞ്ഞെടുത്ത കേന്ദ്ര + കേരള പദ്ധതികൾ (ഇന്ത്യയിലെ എല്ലാ പദ്ധതികളുമല്ല). അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക ഉറവിടത്തിൽ യോഗ്യത ഉറപ്പാക്കുക.",
  resultsFooterDisclaimer:
    "ഈ ഉപകരണം യോഗ്യത ഉറപ്പ് നൽകുന്നില്ല. അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക ഉറവിടത്തിലും തദ്ദേശ സ്ഥാപനത്തിലും ഉറപ്പാക്കുക. «സ്ഥിരീകരണം വേണം» എന്ന പൊരുത്തങ്ങൾ അനിശ്ചിതമാണ് — അംഗീകരിച്ചതായി കരുതരുത്.",

  reason: "എന്തുകൊണ്ട് ഇത് യോജിച്ചേക്കാം",
  expand: "വിശദാംശങ്ങൾ കാണുക",
  collapse: "മറയ്ക്കുക",
  disclaimer:
    "ഇത് നിയമോപദേശമല്ല; യോഗ്യത ഉറപ്പ് നൽകുന്നില്ല. അപേക്ഷിക്കുന്നതിന് മുമ്പ് തദ്ദേശ സ്ഥാപനത്തിലും ഔദ്യോഗിക പോർട്ടലിലും സ്ഥിരീകരിക്കുക.",
  qAge: "നിങ്ങളുടെ പ്രായം എത്ര?",
  qAgeHint: "വയസ്സ് നൽകുക",
  qIncome: "മാസ കുടുംബ വരുമാനം എത്ര?",
  qIncomeHint: "ഏകദേശ തുക ₹ (രൂപ)",
  qOccupation: "തൊഴിൽ എന്താണ്?",
  qCategory: "ഈ വിഭാഗങ്ങളിൽ ഉൾപ്പെടുന്നുണ്ടോ?",
  qCategoryHint: "ബാധകമായവ തിരഞ്ഞെടുക്കുക, അല്ലെങ്കിൽ ഒന്നുമില്ല",
  qLand: "കൃഷിയോഗ്യമായ ഭൂമി ഉണ്ടോ?",
  qDisability: "വൈകല്യം ഉണ്ടോ?",
  qDisabilityPercent: "വൈകല്യ ശതമാനം (അറിയാമെങ്കിൽ)",
  qDisabilityPercentHint: "ഓപ്ഷണൽ — അറിയില്ലെങ്കിൽ ശൂന്യമാക്കി വയ്ക്കുക",
  qDistrict: "ജില്ല ഏതാണ്?",
  qGender: "ലിംഗം",
  qMarital: "വൈവാഹിക നില",
  yes: "ഉണ്ട്",
  no: "ഇല്ല",
  rupee: "₹",
  required: "തുടരാൻ ഉത്തരം നൽകുക",
  occ_agricultural_labour: "കാർഷിക തൊഴിലാളി",
  occ_farmer: "കർഷകൻ / ഭൂവുടമ കർഷകൻ",
  occ_student: "വിദ്യാർത്ഥി",
  occ_unemployed: "തൊഴിലില്ലാത്തവർ",
  occ_other: "മറ്റുള്ളവ",
  cat_none: "ഒന്നുമില്ല",
  cat_General: "പൊതു",
  cat_SC: "SC",
  cat_ST: "ST",
  cat_OBC: "OBC",
  cat_BPL: "BPL",
  gen_female: "സ്ത്രീ",
  gen_male: "പുരുഷൻ",
  gen_other: "മറ്റുള്ളവ",
  mar_unmarried: "അവിവാഹിത",
  mar_married: "വിവാഹിത",
  mar_widow: "വിധവ",
  mar_widower: "വിധുരൻ",
  mar_divorced: "വിവാഹമോചിത",
  mar_deserted: "ഉപേക്ഷിക്കപ്പെട്ടത്",
  qMaternity: "നിങ്ങൾ ഗർഭിണിയോ പുതിയ അമ്മയോ ആണോ?",
  qMaternityHint: "PMMVY / JSY പോലുള്ള മാതൃത്വ പദ്ധതികൾക്ക് വേണ്ടി",
  mat_pregnant: "ഗർഭിണി",
  mat_lactating: "അടുത്തിടെ പ്രസവിച്ചു / മുലയൂട്ടുന്നു",
  mat_neither: "അല്ല",
  qBreadwinner: "കുടുംബത്തിലെ പ്രധാന വരുമാനദാതാവ് മരിച്ചിട്ടുണ്ടോ?",
  qBreadwinnerHint: "NFBS പോലുള്ള പദ്ധതികൾക്ക്",
  dataUpdated:
    "പദ്ധതി വിവരങ്ങൾ 8 സെപ് 2026 വരെ പുതുക്കിയത് · തിരഞ്ഞെടുത്ത കേന്ദ്ര + കേരള പദ്ധതികൾ (ഇന്ത്യയിലെ എല്ലാ പദ്ധതികളുമല്ല)",
  dataUpdatedShort: "പദ്ധതി വിവരങ്ങൾ 8 സെപ് 2026 വരെ പുതുക്കിയത്",
  welcomeTitle: "സ്വാഗതം",
  welcomeBody:
    "കുറച്ച് ലളിതമായ ചോദ്യങ്ങൾക്ക് ഉത്തരം നൽകൂ. നിങ്ങൾക്ക് സഹായകമായേക്കാവുന്ന സർക്കാർ പദ്ധതികൾ ഞങ്ങൾ നിർദ്ദേശിക്കും.",
  start: "തുടങ്ങുക",
};

const TABLES: Record<Lang, Dict> = { en, ml };

export function t(lang: Lang, key: string, vars?: Record<string, string | number>): string {
  const table = TABLES[lang] || en;
  let s = table[key] ?? en[key] ?? key;
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      s = s.replace(`{${k}}`, String(v));
    }
  }
  return s;
}

export function pickLocalized(
  lang: Lang,
  value: { en?: string; ml?: string } | string | string[] | null | undefined,
): string {
  if (value == null) return "";
  if (typeof value === "string") return value;
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") {
    const o = value as { en?: string; ml?: string };
    if (lang === "ml" && o.ml) return o.ml;
    return o.en || o.ml || "";
  }
  return String(value);
}

export function pickLocalizedList(
  lang: Lang,
  value: unknown,
): string[] {
  if (value == null) return [];
  if (Array.isArray(value)) return value.map(String);
  if (typeof value === "object") {
    const o = value as Record<string, unknown>;
    const list = (lang === "ml" ? o.ml : o.en) ?? o.en ?? o.ml;
    if (Array.isArray(list)) return list.map(String);
    if (typeof list === "string") return [list];
  }
  if (typeof value === "string") return [value];
  return [];
}
