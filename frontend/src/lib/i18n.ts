import type { Lang } from "./types";
import { a11yEn, a11yHi, a11yMl } from "./i18nA11y";

type Dict = Record<string, string>;

const en: Dict = {
  appTitle: "Scheme Finder",
  appSubtitle: "Find welfare schemes you may be eligible for",
  langEn: "English",
  langHi: "हिंदी",
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
  shareMessage: "I found welfare schemes that may fit me on Scheme Finder:",
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
  applyLink: "Open official apply page",
  officialSource: "Official source",
  officialSourceConfirm: "Confirm on the official portal before applying",
  lastVerified: "Last verified: {date}",
  dataFreshConfirm:
    "Confirm eligibility on the official source before you apply.",
  dataStaleBanner:
    "Scheme data may be outdated (last updated {date}). Always confirm on the official site before applying.",
  dataFreshBanner:
    "Scheme data updated as of {date} · India + selected other countries (curated; not worldwide). Confirm eligibility on the official source before you apply.",
  resultsConfirmBanner:
    "Before applying: confirm eligibility on the official portal for each scheme below.",
  resultsFooterDisclaimer:
    "This tool does not guarantee eligibility. Before you apply, confirm eligibility on the official portal for each scheme and with your local body. Needs-verification matches are uncertain — never treat them as approved.",

  reason: "Why this may fit",
  expand: "Show details",
  collapse: "Hide details",
  disclaimer:
    "This is not legal advice and does not guarantee eligibility. Always confirm with your local body (panchayat / municipality / corporation) and on the official portal before applying.",
  qAge: "How old are you?",
  qAgeHint: "Enter your age in years",
  qIncome: "What is your household income?",
  qIncomeHint: "Choose Monthly or Yearly, then enter the approximate amount in local currency.",
  qIncomeMonthly: "Monthly",
  qIncomeYearly: "Yearly",
  qIncomeMonthlyLabel: "Monthly household income",
  qIncomeYearlyLabel: "Yearly household income",
  qIncomeAboutYear: "About {currency}{amount} per year",
  qIncomeAboutMonth: "About {currency}{amount} per month",
  qIncomeYearlyHelper: "Entering monthly? Switch to Monthly, or multiply by 12 for yearly.",
  qIncomeMonthlyHelper: "Entering yearly? Switch to Yearly, or divide by 12 for monthly.",
  qOccupation: "What do you do for work?",
  qCategory: "Do you belong to any of these categories?",
  qCategoryHint: "Select all that apply, or None",
  qLand: "Do you own cultivable land?",
  qDisability: "Do you have a disability?",
  qDisabilityPercent: "Disability percentage (if known)",
  qDisabilityPercentHint: "Optional — leave blank if unsure",
  qDistrict: "Which district do you live in?",
  qDistrictFreeHint: "Type your district / locality (free text; Kerala uses a district list).",
  qDistrictPlaceholder: "District name",
  qCountry: "Which country do you live in?",
  qCountryHint: "Catalogue covers India, neighbouring countries, the United States (federal + all states), the United Kingdom (UK-wide + England, Scotland, Wales, Northern Ireland) and Canada (federal + all 13 provinces and territories; amounts in C$ / CAD) — curated, not yet worldwide.",
  qRegion: "Which region / province do you live in?",
  qRegionHint: "Pick from the list or type your region / province (UK: pick your nation — England, Scotland, Wales or Northern Ireland; Canada: pick your province or territory).",
  qRegionPlaceholder: "Region / province",
  qRegionOrType: "You can pick a listed region or type another name below.",
  qState: "Which state or UT do you live in?",
  qStateHint: "Central schemes apply nationwide within India; state schemes appear for your selection.",
  resultsState: "State / region",
  resultsCountry: "Country",
  resultsIncomeFilter: "Filtered using annual income {currency}{amount}",
  resultsIncomeBand: "Based on PRICE ICE 360° household bands (2020–21 prices): {label}. ₹15 lakh is the Seekers→Strivers cut (Strivers ₹15–30 lakh). Not an official government classification — does not change scheme rules; only helps sort/explain.",
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
    "Scheme data updated as of 25 Sep 2026 · India + selected other countries incl. United States, United Kingdom and Canada (curated; not worldwide)",
  dataUpdatedShort: "Scheme data updated as of 25 Sep 2026",
  welcomeTitle: "Welcome",
  welcomeBody:
    "Pick your country (and region), then answer a few simple questions. We suggest curated welfare schemes that may help you.",
  start: "Start",

  findingForTitle: "Who are you finding schemes for?",
  findingForHint:
    "If you choose your child or dependent, age and disability answers should describe them (needed for US child savings such as Trump Accounts, Coverdell, 529, and ABLE).",
  findingForSelf: "For myself",
  findingForChild: "For my child / dependent",
  findingForChildShort: "child",
  qAgeChild: "How old is your child / dependent?",
  qAgeChildHint: "Enter their age in years (beneficiary age for child savings schemes)",
  qDisabilityChild: "Does your child / dependent have a disability?",
  resultsTitleChild: "Schemes that may fit your child / dependent",
  resultsParentModeBanner:
    "Parent / guardian mode: matches below are based on the child or dependent’s details you entered. Still confirm eligibility on each official portal before applying.",
  savedTitle: "Saved on this device",
  savedPrivacy:
    "Profiles stay in this browser’s local storage (up to 5). They are not uploaded unless you share a link. See Privacy.",
  savedNamePlaceholder: "Optional name (e.g. My profile)",
  savedSave: "Save on this device",
  savedLoad: "Load",
  savedDelete: "Delete",
  savedClearAll: "Clear all saved",
  savedClearConfirm: "Delete all device-saved profiles?",
  savedEmpty: "No saved profiles yet.",
  savedUnnamed: "Untitled profile",
  savedOk: "Saved on this device",
  savedFailed: "Could not save (storage full or blocked)",
  savedNeedAnswers: "Complete a search first, then save",

  stage_baby: "Baby",
  stage_child: "Child",
  stage_teen: "Teen",
  stage_young_adult: "Young adult",
  stage_adult: "Adult",
  stage_senior: "Senior",
};

const ml: Dict = {
  appTitle: "പദ്ധതി കണ്ടെത്തൽ",
  appSubtitle: "നിങ്ങൾക്ക് യോഗ്യമായേക്കാവുന്ന ക്ഷേമ പദ്ധതികൾ കണ്ടെത്തുക",
  langEn: "English",
  langHi: "हिंदी",
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
  shareMessage: "സ്കീം ഫൈൻഡറിൽ എനിക്ക് യോജിച്ചേക്കാവുന്ന ക്ഷേമ പദ്ധതികൾ കണ്ടെത്തി:",
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
  applyLink: "ഔദ്യോഗിക അപേക്ഷാ പേജ് തുറക്കുക",
  officialSource: "ഔദ്യോഗിക ഉറവിടം",
  officialSourceConfirm: "അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക പോർട്ടലിൽ സ്ഥിരീകരിക്കുക",
  lastVerified: "അവസാനം സ്ഥിരീകരിച്ചത്: {date}",
  dataFreshConfirm:
    "അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക ഉറവിടത്തിൽ യോഗ്യത സ്ഥിരീകരിക്കുക.",
  dataStaleBanner:
    "പദ്ധതി വിവരങ്ങൾ കാലഹരണപ്പെട്ടിരിക്കാം (അവസാനം പുതുക്കിയത് {date}). അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക സൈറ്റിൽ എല്ലായ്പ്പോഴും ഉറപ്പാക്കുക.",
  dataFreshBanner:
    "പദ്ധതി വിവരങ്ങൾ {date} വരെ പുതുക്കിയത് · ഇന്ത്യ + തിരഞ്ഞെടുത്ത മറ്റ് രാജ്യങ്ങൾ (ലോകവ്യാപകമല്ല). അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഔദ്യോഗിക ഉറവിടത്തിൽ യോഗ്യത ഉറപ്പാക്കുക.",
  resultsConfirmBanner:
    "അപേക്ഷിക്കുന്നതിന് മുമ്പ്: താഴെയുള്ള ഓരോ പദ്ധതിയുടെയും ഔദ്യോഗിക പോർട്ടലിൽ യോഗ്യത സ്ഥിരീകരിക്കുക.",
  resultsFooterDisclaimer:
    "ഈ ഉപകരണം യോഗ്യത ഉറപ്പ് നൽകുന്നില്ല. അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഓരോ പദ്ധതിയുടെയും ഔദ്യോഗിക പോർട്ടലിലും തദ്ദേശ സ്ഥാപനത്തിലും യോഗ്യത ഉറപ്പാക്കുക. «സ്ഥിരീകരണം വേണം» എന്ന പൊരുത്തങ്ങൾ അനിശ്ചിതമാണ് — അംഗീകരിച്ചതായി കരുതരുത്.",

  reason: "എന്തുകൊണ്ട് ഇത് യോജിച്ചേക്കാം",
  expand: "വിശദാംശങ്ങൾ കാണുക",
  collapse: "മറയ്ക്കുക",
  disclaimer:
    "ഇത് നിയമോപദേശമല്ല; യോഗ്യത ഉറപ്പ് നൽകുന്നില്ല. അപേക്ഷിക്കുന്നതിന് മുമ്പ് തദ്ദേശ സ്ഥാപനത്തിലും ഔദ്യോഗിക പോർട്ടലിലും സ്ഥിരീകരിക്കുക.",
  qAge: "നിങ്ങളുടെ പ്രായം എത്ര?",
  qAgeHint: "വയസ്സ് നൽകുക",
  qIncome: "കുടുംബ വരുമാനം എത്ര?",
  qIncomeHint: "മാസം / വർഷം തിരഞ്ഞെടുത്ത് ഏകദേശ തുക പ്രാദേശിക കറൻസിയിൽ നൽകുക.",
  qIncomeMonthly: "മാസം",
  qIncomeYearly: "വർഷം",
  qIncomeMonthlyLabel: "മാസ കുടുംബ വരുമാനം",
  qIncomeYearlyLabel: "വാർഷിക കുടുംബ വരുമാനം",
  qIncomeAboutYear: "ഏകദേശം വർഷം {currency}{amount}",
  qIncomeAboutMonth: "ഏകദേശം മാസം {currency}{amount}",
  qIncomeYearlyHelper: "മാസ വരുമാനമാണോ? Monthly തിരഞ്ഞെടുക്കുക, അല്ലെങ്കിൽ 12 കൊണ്ട് ഗുണിക്കുക.",
  qIncomeMonthlyHelper: "വാർഷിക വരുമാനമാണോ? Yearly തിരഞ്ഞെടുക്കുക, അല്ലെങ്കിൽ 12 കൊണ്ട് ഹരിക്കുക.",
  qOccupation: "തൊഴിൽ എന്താണ്?",
  qCategory: "ഈ വിഭാഗങ്ങളിൽ ഉൾപ്പെടുന്നുണ്ടോ?",
  qCategoryHint: "ബാധകമായവ തിരഞ്ഞെടുക്കുക, അല്ലെങ്കിൽ ഒന്നുമില്ല",
  qLand: "കൃഷിയോഗ്യമായ ഭൂമി ഉണ്ടോ?",
  qDisability: "വൈകല്യം ഉണ്ടോ?",
  qDisabilityPercent: "വൈകല്യ ശതമാനം (അറിയാമെങ്കിൽ)",
  qDisabilityPercentHint: "ഓപ്ഷണൽ — അറിയില്ലെങ്കിൽ ശൂന്യമാക്കി വയ്ക്കുക",
  qDistrict: "ജില്ല ഏതാണ്?",
  qDistrictFreeHint: "ജില്ലയുടെ പേര് ടൈപ്പ് ചെയ്യുക (കേരളം ഒഴികെയുള്ള സംസ്ഥാനങ്ങൾക്ക്).",
  qDistrictPlaceholder: "ജില്ലയുടെ പേര്",
  qCountry: "നിങ്ങൾ താമസിക്കുന്ന രാജ്യം ഏത്?",
  qCountryHint: "കാറ്റലോഗ് ഇന്ത്യ, അയൽരാജ്യങ്ങൾ, യുണൈറ്റഡ് സ്റ്റേറ്റ്സ് (ഫെഡറൽ + എല്ലാ സംസ്ഥാനങ്ങളും), യുണൈറ്റഡ് കിംഗ്ഡം (യുകെ മുഴുവൻ + ഇംഗ്ലണ്ട്, സ്കോട്ട്‌ലൻഡ്, വെയിൽസ്, നോർത്തേൺ അയർലൻഡ്), കാനഡ (ഫെഡറൽ + 13 പ്രവിശ്യകളും ടെറിട്ടറികളും; തുക C$ / CAD-ൽ) ഉൾക്കൊള്ളുന്നു — ക്യൂറേറ്റഡ്, ഇനിയും ലോകവ്യാപകമല്ല.",
  qRegion: "നിങ്ങൾ താമസിക്കുന്ന പ്രദേശം / പ്രവിശ്യ ഏത്?",
  qRegionHint: "പട്ടികയിൽ നിന്ന് തിരഞ്ഞെടുക്കുക അല്ലെങ്കിൽ ടൈപ്പ് ചെയ്യുക (യുകെ: ഇംഗ്ലണ്ട്, സ്കോട്ട്‌ലൻഡ്, വെയിൽസ് അല്ലെങ്കിൽ നോർത്തേൺ അയർലൻഡ്; കാനഡ: നിങ്ങളുടെ പ്രവിശ്യ അല്ലെങ്കിൽ ടെറിട്ടറി).",
  qRegionPlaceholder: "പ്രദേശം / പ്രവിശ്യ",
  qRegionOrType: "പട്ടികയിൽ നിന്ന് തിരഞ്ഞെടുക്കാം അല്ലെങ്കിൽ താഴെ മറ്റൊരു പേര് ടൈപ്പ് ചെയ്യാം.",
  qState: "നിങ്ങൾ താമസിക്കുന്ന സംസ്ഥാനം / കേന്ദ്രഭരണ പ്രദേശം ഏത്?",
  qStateHint: "കേന്ദ്ര പദ്ധതികൾ ഇന്ത്യയിൽ രാജ്യവ്യാപകം; സംസ്ഥാന പദ്ധതികൾ നിങ്ങളുടെ തിരഞ്ഞെടുപ്പിന് അനുസരിച്ച്.",
  resultsState: "സംസ്ഥാനം / പ്രദേശം",
  resultsCountry: "രാജ്യം",
  resultsIncomeFilter: "വാർഷിക വരുമാനം {currency}{amount} ഉപയോഗിച്ച് ഫിൽട്ടർ ചെയ്തു",
  resultsIncomeBand: "PRICE ICE 360° കുടുംബ വരുമാന ബാൻഡുകൾ (2020–21 വില): {label}. ₹15 ലക്ഷം Seekers→Strivers അതിർത്തി (Strivers ₹15–30 ലക്ഷം). ഔദ്യോഗിക സർക്കാർ വർഗ്ഗീകരണമല്ല — സ്കീം നിയമങ്ങൾ മാറ്റില്ല; ക്രമീകരണത്തിന് സഹായിക്കുന്നു.",
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
    "പദ്ധതി വിവരങ്ങൾ 25 സെപ് 2026 വരെ പുതുക്കിയത് · ഇന്ത്യ + തിരഞ്ഞെടുത്ത മറ്റ് രാജ്യങ്ങൾ ഉൾപ്പെടെ യുണൈറ്റഡ് സ്റ്റേറ്റ്സ്, യുണൈറ്റഡ് കിംഗ്ഡം, കാനഡ (ലോകവ്യാപകമല്ല)",
  dataUpdatedShort: "പദ്ധതി വിവരങ്ങൾ 25 സെപ് 2026 വരെ പുതുക്കിയത്",
  welcomeTitle: "സ്വാഗതം",
  welcomeBody:
    "രാജ്യം (ഒപ്പം പ്രദേശം) തിരഞ്ഞെടുക്കുക, പിന്നെ കുറച്ച് ലളിതമായ ചോദ്യങ്ങൾക്ക് ഉത്തരം നൽകൂ. ക്ഷേമ പദ്ധതികൾ ഞങ്ങൾ നിർദ്ദേശിക്കും.",
  start: "തുടങ്ങുക",

  findingForTitle: "ആർക്കുവേണ്ടിയാണ് പദ്ധതികൾ തിരയുന്നത്?",
  findingForHint:
    "കുട്ടി / ആശ്രിതന് വേണ്ടിയാണെങ്കിൽ പ്രായവും വൈകല്യ വിവരങ്ങളും അവരുടേതായിരിക്കണം (യുഎസ് കുട്ടി സേവിംഗ്‌സ് പദ്ധതികൾക്ക്).",
  findingForSelf: "എനിക്ക് വേണ്ടി",
  findingForChild: "എന്റെ കുട്ടി / ആശ്രിതന് വേണ്ടി",
  findingForChildShort: "കുട്ടി",
  qAgeChild: "കുട്ടി / ആശ്രിതന്റെ പ്രായം എത്ര?",
  qAgeChildHint: "വയസ്സ് നൽകുക (കുട്ടി സേവിംഗ്‌സ് പദ്ധതികൾക്ക് ഗുണഭോക്താവിന്റെ പ്രായം)",
  qDisabilityChild: "കുട്ടി / ആശ്രിതന് വൈകല്യമുണ്ടോ?",
  resultsTitleChild: "കുട്ടി / ആശ്രിതന് യോജിച്ചേക്കാവുന്ന പദ്ധതികൾ",
  resultsParentModeBanner:
    "രക്ഷിതാവ് മോഡ്: താഴെയുള്ള പൊരുത്തങ്ങൾ നൽകിയ കുട്ടി / ആശ്രിത വിവരങ്ങളെ അടിസ്ഥാനമാക്കിയതാണ്. അപേക്ഷിക്കുന്നതിന് മുമ്പ് ഓരോ ഔദ്യോഗിക പോർട്ടലിലും യോഗ്യത ഉറപ്പാക്കുക.",
  savedTitle: "ഈ ഉപകരണത്തിൽ സേവ് ചെയ്തത്",
  savedPrivacy:
    "പ്രൊഫൈലുകൾ ഈ ബ്രൗസറിന്റെ local storage-ൽ മാത്രം (പരമാവധി 5). ലിങ്ക് പങ്കിടാതെ അപ്‌ലോഡ് ചെയ്യില്ല. സ്വകാര്യത കാണുക.",
  savedNamePlaceholder: "ഓപ്ഷണൽ പേര്",
  savedSave: "ഈ ഉപകരണത്തിൽ സേവ് ചെയ്യുക",
  savedLoad: "ലോഡ്",
  savedDelete: "ഇല്ലാതാക്കുക",
  savedClearAll: "എല്ലാം മായ്ക്കുക",
  savedClearConfirm: "ഉപകരണത്തിലെ എല്ലാ സേവ് ചെയ്ത പ്രൊഫൈലുകളും ഇല്ലാതാക്കണോ?",
  savedEmpty: "സേവ് ചെയ്ത പ്രൊഫൈലുകളില്ല.",
  savedUnnamed: "പേരില്ലാത്ത പ്രൊഫൈൽ",
  savedOk: "ഈ ഉപകരണത്തിൽ സേവ് ചെയ്തു",
  savedFailed: "സേവ് ചെയ്യാനായില്ല",
  savedNeedAnswers: "ആദ്യം തിരച്ചിൽ പൂർത്തിയാക്കി പിന്നീട് സേവ് ചെയ്യുക",

  stage_baby: "കുഞ്ഞ്",
  stage_child: "കുട്ടി",
  stage_teen: "കൗമാരം",
  stage_young_adult: "യുവാവ്",
  stage_adult: "മുതിർന്നവർ",
  stage_senior: "മുതിർന്ന പൗരർ",
};

const hi: Dict = {
  appTitle: "योजना खोजक",
  appSubtitle: "वे कल्याण योजनाएँ खोजें जिनके लिए आप पात्र हो सकते हैं",
  langEn: "English",
  langHi: "हिंदी",
  langMl: "മലയാളം",
  progress: "चरण {current} / {total}",
  next: "आगे",
  back: "पीछे",
  submit: "योजनाएँ खोजें",
  startOver: "फिर से शुरू करें",
  loading: "योजनाएँ खोज रहे हैं…",
  errorTitle: "सर्वर से संपर्क नहीं हो सका",
  errorRetry: "फिर कोशिश करें",
  errorHint: "कनेक्शन जाँचें, पेज हार्ड-रिफ़्रेश करें और फिर कोशिश करें। (API इसी साइट से मिलती है।)",
  shareCopyLink: "लिंक कॉपी करें",
  shareCopied: "लिंक कॉपी हो गया",
  shareWhatsApp: "व्हाट्सऐप पर साझा करें",
  shareMessage: "स्कीम फ़ाइंडर पर मुझे उपयुक्त लगने वाली कल्याण योजनाएँ मिलीं:",
  shareCopyFailed: "कॉपी नहीं हो सका — एड्रेस बार का लिंक कॉपी करें",

  zeroTitle: "अभी कोई मिलान वाली योजना नहीं",
  zeroBody:
    "आपकी दी गई जानकारी के आधार पर स्पष्ट मिलान नहीं मिला। उत्तर बदलकर फिर कोशिश करें, या अपने स्थानीय पंचायत / नगरपालिका से मदद लें।",
  resultsTitle: "आपके लिए उपयुक्त हो सकने वाली योजनाएँ",
  resultsCount: "{count} योजना(एँ) मिलीं",
  verifyBadge: "सत्यापन आवश्यक",
  uncertainBadge: "अनिश्चित — स्थानीय रूप से पुष्टि करें",
  likelyBadge: "संभवतः पात्र",
  benefits: "लाभ",
  documents: "आवश्यक दस्तावेज़",
  howToApply: "आवेदन कैसे करें",
  applyLink: "आधिकारिक आवेदन पृष्ठ खोलें",
  officialSource: "आधिकारिक स्रोत",
  officialSourceConfirm: "आवेदन से पहले आधिकारिक पोर्टल पर पुष्टि करें",
  lastVerified: "अंतिम सत्यापन: {date}",
  dataFreshConfirm:
    "आवेदन करने से पहले आधिकारिक स्रोत पर पात्रता की पुष्टि करें।",
  dataStaleBanner:
    "योजना डेटा पुराना हो सकता है (अंतिम अद्यतन {date})। आवेदन से पहले हमेशा आधिकारिक साइट पर पुष्टि करें।",
  dataFreshBanner:
    "योजना डेटा {date} तक अद्यतन · भारत + चुनिंदा अन्य देश (दुनियाभर नहीं)। आवेदन से पहले आधिकारिक स्रोत पर पात्रता की पुष्टि करें।",
  resultsConfirmBanner:
    "आवेदन से पहले: नीचे दी गई प्रत्येक योजना के आधिकारिक पोर्टल पर पात्रता की पुष्टि करें।",
  resultsFooterDisclaimer:
    "यह उपकरण पात्रता की गारंटी नहीं देता। आवेदन से पहले प्रत्येक योजना के आधिकारिक पोर्टल और स्थानीय निकाय पर पात्रता की पुष्टि करें। «सत्यापन आवश्यक» मिलान अनिश्चित हैं — उन्हें स्वीकृत न समझें।",

  reason: "यह क्यों उपयुक्त हो सकता है",
  expand: "विवरण दिखाएँ",
  collapse: "विवरण छिपाएँ",
  disclaimer:
    "यह कानूनी सलाह नहीं है और पात्रता की गारंटी नहीं देता। आवेदन से पहले अपने स्थानीय निकाय (पंचायत / नगरपालिका / निगम) और आधिकारिक पोर्टल से पुष्टि करें।",
  qAge: "आपकी आयु कितनी है?",
  qAgeHint: "वर्षों में आयु दर्ज करें",
  qIncome: "आपकी घरेलू आय कितनी है?",
  qIncomeHint: "मासिक या वार्षिक चुनें, फिर लगभग राशि स्थानीय मुद्रा में दर्ज करें।",
  qIncomeMonthly: "मासिक",
  qIncomeYearly: "वार्षिक",
  qIncomeMonthlyLabel: "मासिक घरेलू आय",
  qIncomeYearlyLabel: "वार्षिक घरेलू आय",
  qIncomeAboutYear: "लगभग {currency}{amount} प्रति वर्ष",
  qIncomeAboutMonth: "लगभग {currency}{amount} प्रति माह",
  qIncomeYearlyHelper: "मासिक दर्ज कर रहे हैं? मासिक चुनें, या वार्षिक के लिए 12 से गुणा करें।",
  qIncomeMonthlyHelper: "वार्षिक दर्ज कर रहे हैं? वार्षिक चुनें, या मासिक के लिए 12 से भाग दें।",
  qOccupation: "आप क्या काम करते हैं?",
  qCategory: "क्या आप इनमें से किसी श्रेणी में आते हैं?",
  qCategoryHint: "लागू सभी चुनें, या कोई नहीं",
  qLand: "क्या आपके पास कृषि योग्य भूमि है?",
  qDisability: "क्या आपको कोई दिव्यांगता है?",
  qDisabilityPercent: "दिव्यांगता प्रतिशत (यदि ज्ञात हो)",
  qDisabilityPercentHint: "वैकल्पिक — अनिश्चित होने पर खाली छोड़ें",
  qDistrict: "आप किस ज़िले में रहते हैं?",
  qDistrictFreeHint: "अपने ज़िले का नाम लिखें (केरल के अलावा अन्य राज्यों के लिए मुक्त पाठ)।",
  qDistrictPlaceholder: "ज़िले का नाम",
  qCountry: "आप किस देश में रहते हैं?",
  qCountryHint: "कैटलॉग भारत, पड़ोसी देश, संयुक्त राज्य अमेरिका (संघीय + सभी राज्य), यूनाइटेड किंगडम (पूरा यूके + इंग्लैंड, स्कॉटलैंड, वेल्स, नॉर्दर्न आयरलैंड) और कनाडा (संघीय + सभी 13 प्रांत व क्षेत्र; राशि C$ / CAD में) को कवर करता है — क्यूरेटेड, अभी पूरी दुनिया नहीं।",
  qRegion: "आप किस क्षेत्र / प्रांत में रहते हैं?",
  qRegionHint: "सूची से चुनें या अपना क्षेत्र / प्रांत टाइप करें (यूके: इंग्लैंड, स्कॉटलैंड, वेल्स या नॉर्दर्न आयरलैंड चुनें; कनाडा: अपना प्रांत या क्षेत्र चुनें)।",
  qRegionPlaceholder: "क्षेत्र / प्रांत",
  qRegionOrType: "सूची से चुन सकते हैं या नीचे दूसरा नाम टाइप कर सकते हैं।",
  qState: "आप किस राज्य या केंद्र शासित प्रदेश में रहते हैं?",
  qStateHint: "केंद्रीय योजनाएँ भारत में पूरे देश में लागू; राज्य योजनाएँ आपके चयन के अनुसार दिखेंगी।",
  resultsState: "राज्य / क्षेत्र",
  resultsCountry: "देश",
  resultsIncomeFilter: "वार्षिक आय {currency}{amount} से फ़िल्टर किया गया",
  resultsIncomeBand: "PRICE ICE 360° घरेलू आय बैंड (2020–21 कीमतें): {label}. ₹15 लाख Seekers→Strivers सीमा है (Strivers ₹15–30 लाख). आधिकारिक सरकारी वर्गीकरण नहीं — योजना नियम नहीं बदलता; केवल क्रम/व्याख्या में मदद।",
  qGender: "लिंग",
  qMarital: "वैवाहिक स्थिति",
  yes: "हाँ",
  no: "नहीं",
  rupee: "₹",
  required: "आगे बढ़ने के लिए कृपया उत्तर दें",
  occ_agricultural_labour: "कृषि मज़दूर",
  occ_farmer: "किसान / भूमिधारक किसान",
  occ_student: "विद्यार्थी",
  occ_unemployed: "बेरोजगार",
  occ_other: "अन्य",
  cat_none: "कोई नहीं",
  cat_General: "सामान्य",
  cat_SC: "SC",
  cat_ST: "ST",
  cat_OBC: "OBC",
  cat_BPL: "BPL",
  gen_female: "महिला",
  gen_male: "पुरुष",
  gen_other: "अन्य",
  mar_unmarried: "अविवाहित",
  mar_married: "विवाहित",
  mar_widow: "विधवा",
  mar_widower: "विधुर",
  mar_divorced: "तलाकशुदा",
  mar_deserted: "परित्यक्त",
  qMaternity: "क्या आप गर्भवती हैं या नई माँ हैं?",
  qMaternityHint: "PMMVY / JSY जैसी मातृत्व योजनाओं के लिए आवश्यक",
  mat_pregnant: "गर्भवती",
  mat_lactating: "हाल ही में प्रसव / स्तनपान",
  mat_neither: "न तो / न ही",
  qBreadwinner: "क्या आपके परिवार का मुख्य कमाने वाला सदस्य निधन हो गया है?",
  qBreadwinnerHint: "NFBS जैसी शोक-सहायता योजनाओं के लिए",
  dataUpdated:
    "योजना डेटा 25 सितं 2026 तक अद्यतन · भारत + चुनिंदा अन्य देश सहित संयुक्त राज्य अमेरिका, यूनाइटेड किंगडम और कनाडा (दुनियाभर नहीं)",
  dataUpdatedShort: "योजना डेटा 25 सितं 2026 तक अद्यतन",
  welcomeTitle: "स्वागत है",
  welcomeBody:
    "अपना देश (और क्षेत्र) चुनें, फिर कुछ सरल प्रश्नों के उत्तर दें। हम चुनिंदा कल्याण योजनाएँ सुझाएँगे।",
  start: "शुरू करें",

  findingForTitle: "आप किसके लिए योजनाएँ खोज रहे हैं?",
  findingForHint:
    "यदि बच्चे / आश्रित के लिए चुनें, तो आयु और विकलांगता उनके बारे में बताएँ (अमेरिकी बाल बचत योजनाओं जैसे Trump Accounts, Coverdell, 529, ABLE के लिए).",
  findingForSelf: "मेरे लिए",
  findingForChild: "मेरे बच्चे / आश्रित के लिए",
  findingForChildShort: "बच्चा",
  qAgeChild: "आपके बच्चे / आश्रित की आयु कितनी है?",
  qAgeChildHint: "वर्षों में आयु दर्ज करें (बाल बचत योजनाओं के लिए लाभार्थी की आयु)",
  qDisabilityChild: "क्या आपके बच्चे / आश्रित को विकलांगता है?",
  resultsTitleChild: "योजनाएँ जो आपके बच्चे / आश्रित के लिए उपयुक्त हो सकती हैं",
  resultsParentModeBanner:
    "अभिभावक मोड: नीचे दिए मिलान आपके द्वारा दर्ज बच्चे / आश्रित विवरण पर आधारित हैं। आवेदन से पहले प्रत्येक आधिकारिक पोर्टल पर पात्रता की पुष्टि करें।",
  savedTitle: "इस डिवाइस पर सहेजा गया",
  savedPrivacy:
    "प्रोफ़ाइल केवल इस ब्राउज़र की local storage में रहती हैं (अधिकतम 5)। लिंक साझा करने तक अपलोड नहीं होतीं। गोपनीयता देखें।",
  savedNamePlaceholder: "वैकल्पिक नाम",
  savedSave: "इस डिवाइस पर सहेजें",
  savedLoad: "लोड",
  savedDelete: "हटाएँ",
  savedClearAll: "सभी साफ़ करें",
  savedClearConfirm: "सभी डिवाइस-सहेजी प्रोफ़ाइल हटाएँ?",
  savedEmpty: "अभी कोई सहेजी प्रोफ़ाइल नहीं।",
  savedUnnamed: "बिना नाम की प्रोफ़ाइल",
  savedOk: "इस डिवाइस पर सहेजा गया",
  savedFailed: "सेव नहीं हो सका",
  savedNeedAnswers: "पहले खोज पूरी करें, फिर सेव करें",

  stage_baby: "शिशु",
  stage_child: "बच्चा",
  stage_teen: "किशोर",
  stage_young_adult: "युवा",
  stage_adult: "वयस्क",
  stage_senior: "वरिष्ठ नागरिक",
};

const TABLES: Record<Lang, Dict> = {
  en: { ...a11yEn, ...en },
  ml: { ...a11yMl, ...ml },
  hi: { ...a11yHi, ...hi },
};

export function t(lang: Lang, key: string, vars?: Record<string, string | number>): string {
  const table = TABLES[lang] || en;
  let s = table[key] ?? TABLES.en[key] ?? key;
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      s = s.replace(`{${k}}`, String(v));
    }
  }
  return s;
}

export type LocalizedFields = { en?: string; ml?: string; hi?: string };

export function pickLocalized(
  lang: Lang,
  value: LocalizedFields | string | string[] | null | undefined,
): string {
  if (value == null) return "";
  if (typeof value === "string") return value;
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") {
    const o = value as LocalizedFields;
    if (lang === "hi" && o.hi) return o.hi;
    if (lang === "ml" && o.ml) return o.ml;
    if (lang === "en" && o.en) return o.en;
    // Prefer English when requested lang missing (legal/official names).
    return o.en || o.ml || o.hi || "";
  }
  return String(value);
}

/**
 * Like pickLocalized, but also reports which language the returned text is in,
 * so fallback English inside a Hindi/Malayalam page can be marked lang="en"
 * (WCAG 3.1.2 Language of Parts).
 */
export function pickLocalizedWithLang(
  lang: Lang,
  value: LocalizedFields | string | string[] | null | undefined,
): { text: string; lang: Lang } {
  if (value == null) return { text: "", lang };
  if (typeof value === "object" && !Array.isArray(value)) {
    const o = value as LocalizedFields;
    if (o[lang]) return { text: o[lang] as string, lang };
    if (o.en) return { text: o.en, lang: "en" };
    if (o.ml) return { text: o.ml, lang: "ml" };
    if (o.hi) return { text: o.hi, lang: "hi" };
    return { text: "", lang };
  }
  // Plain strings in the catalogue are English source text.
  return { text: pickLocalized(lang, value), lang: "en" };
}

export function pickLocalizedList(
  lang: Lang,
  value: unknown,
): string[] {
  if (value == null) return [];
  if (Array.isArray(value)) return value.map(String);
  if (typeof value === "object") {
    const o = value as Record<string, unknown>;
    const preferred =
      lang === "hi" ? o.hi : lang === "ml" ? o.ml : o.en;
    const list = preferred ?? o.en ?? o.ml ?? o.hi;
    if (Array.isArray(list)) return list.map(String);
    if (typeof list === "string") return [list];
  }
  if (typeof value === "string") return [value];
  return [];
}

/** List variant of pickLocalizedWithLang (3.1.2 Language of Parts). */
export function pickLocalizedListWithLang(
  lang: Lang,
  value: unknown,
): { items: string[]; lang: Lang } {
  if (value && typeof value === "object" && !Array.isArray(value)) {
    const o = value as Record<string, unknown>;
    for (const code of [lang, "en", "ml", "hi"] as Lang[]) {
      const list = o[code];
      if (Array.isArray(list) && list.length) return { items: list.map(String), lang: code };
      if (typeof list === "string" && list) return { items: [list], lang: code };
    }
    return { items: [], lang };
  }
  return { items: pickLocalizedList(lang, value), lang: "en" };
}
