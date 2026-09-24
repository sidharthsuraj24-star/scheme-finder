"use client";

import { useMemo, useState } from "react";
import {
  CATEGORIES,
  DISTRICT_FREE_TEXT_MAX,
  GENDERS,
  KERALA_DISTRICTS,
  MARITAL_STATUSES,
  OCCUPATIONS,
  TOTAL_STEPS,
} from "@/lib/constants";
import {
  COUNTRY_REGIONS,
  DEFAULT_COUNTRY,
  SUPPORTED_COUNTRIES,
  currencySymbol,
} from "@/lib/countries";
import { DEFAULT_STATE, INDIA_REGIONS } from "@/lib/indiaRegions";
import { t } from "@/lib/i18n";
import type { Lang, ProfileAnswers } from "@/lib/types";
import AgeLifeStage from "./AgeLifeStage";
import ProgressBar from "./ProgressBar";

const emptyAnswers = (): ProfileAnswers => ({
  country: DEFAULT_COUNTRY,
  state: null,
  age: null,
  income_amount: null,
  income_mode: "yearly",
  monthly_household_income: null,
  occupation: null,
  categories: [],
  land_ownership: null,
  disability: null,
  disability_percent: null,
  district: null,
  gender: null,
  marital_status: null,
  maternity: null,
  primary_breadwinner_deceased: null,
  finding_for: null,
});

interface Props {
  lang: Lang;
  onSubmit: (answers: ProfileAnswers) => void;
  /** Prefill from a device-saved profile (does not auto-submit). */
  initialAnswers?: ProfileAnswers | null;
}

export default function Wizard({ lang, onSubmit, initialAnswers }: Props) {
  const [step, setStep] = useState(0); // 0 = welcome
  const [answers, setAnswers] = useState<ProfileAnswers>(() =>
    initialAnswers ? { ...emptyAnswers(), ...initialAnswers } : emptyAnswers(),
  );
  const [error, setError] = useState<string | null>(null);

  const isIndia = (answers.country || DEFAULT_COUNTRY) === "India";
  const isKerala = isIndia && answers.state === "Kerala";
  const currency = currencySymbol(answers.country || DEFAULT_COUNTRY);

  const choiceBtn = (active: boolean) =>
    `choice-btn ${active ? "choice-btn--active" : "choice-btn--idle"}`;

  const validateDistrict = (): boolean => {
    const d = (answers.district || "").trim();
    if (!d) return false;
    if (d.length > DISTRICT_FREE_TEXT_MAX) return false;
    if (isKerala) {
      return (KERALA_DISTRICTS as readonly string[]).includes(d);
    }
    return true;
  };

  const validate = (s: number): boolean => {
    switch (s) {
      case 1:
        return !!answers.country;
      case 2:
        return !!answers.state;
      case 3:
        return answers.age != null && answers.age >= 0 && answers.age <= 120;
      case 4: {
        const amount = answers.income_amount;
        if (amount == null || amount < 0) return false;
        const max = answers.income_mode === "yearly" ? 100_000_000 : 10_000_000;
        return amount <= max;
      }
      case 5:
        return !!answers.occupation;
      case 6:
        return answers.categories.length > 0;
      case 7:
        return answers.land_ownership === "yes" || answers.land_ownership === "no";
      case 8:
        return answers.disability === "yes" || answers.disability === "no";
      case 9: {
        const base = validateDistrict() && !!(answers.gender && answers.marital_status);
        const maternityOk =
          answers.gender !== "female" || answers.maternity != null;
        const breadwinnerOk = answers.primary_breadwinner_deceased != null;
        return base && maternityOk && breadwinnerOk;
      }
      default:
        return true;
    }
  };

  const goNext = () => {
    if (step === 0) {
      setAnswers((a) => ({ ...a, finding_for: a.finding_for || "self" }));
      setStep(1);
      setError(null);
      return;
    }
    if (!validate(step)) {
      setError(t(lang, "required"));
      return;
    }
    setError(null);
    if (step >= TOTAL_STEPS) {
      onSubmit({
        ...answers,
        finding_for: answers.finding_for || "self",
        district: answers.district ? answers.district.trim() : null,
        country: answers.country || DEFAULT_COUNTRY,
        state: answers.state || (isIndia ? DEFAULT_STATE : answers.state),
      });
      return;
    }
    setStep((s) => s + 1);
  };

  const goBack = () => {
    setError(null);
    setStep((s) => Math.max(0, s - 1));
  };

  const toggleCategory = (cat: string) => {
    setAnswers((prev) => {
      if (cat === "none") {
        return { ...prev, categories: ["none"] };
      }
      const withoutNone = prev.categories.filter((c) => c !== "none");
      if (withoutNone.includes(cat)) {
        const next = withoutNone.filter((c) => c !== cat);
        return { ...prev, categories: next.length ? next : [] };
      }
      return { ...prev, categories: [...withoutNone, cat] };
    });
  };

  const setCountry = (name: string) => {
    setAnswers((a) => ({
      ...a,
      country: name,
      state: a.country === name ? a.state : null,
      district: a.country === name ? a.district : null,
    }));
  };

  const setState = (name: string) => {
    setAnswers((a) => ({
      ...a,
      state: name,
      // Clear district when leaving Kerala select list / entering free-text
      district: a.state === name ? a.district : null,
    }));
  };

  const field = useMemo(() => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-3">
            <label htmlFor="country" className="block text-xl font-bold text-slate-900">
              {t(lang, "qCountry")}
            </label>
            <p className="text-sm text-slate-600">{t(lang, "qCountryHint")}</p>
            <select
              id="country"
              name="country"
              className="min-h-tap w-full rounded-xl border-2 border-slate-300 bg-white px-4 text-base transition focus:border-brand-600"
              value={answers.country ?? ""}
              onChange={(e) => {
                const v = e.target.value;
                if (v) setCountry(v);
                else setAnswers((a) => ({ ...a, country: null, state: null, district: null }));
              }}
            >
              <option value="">—</option>
              {SUPPORTED_COUNTRIES.map((c) => (
                <option key={c} value={c}>
                  {c}
                </option>
              ))}
            </select>
          </div>
        );
      case 2: {
        const country = answers.country || DEFAULT_COUNTRY;
        const regions = COUNTRY_REGIONS[country] || [];
        if (country === "India") {
          return (
            <div className="space-y-3">
              <label htmlFor="state" className="block text-xl font-bold text-slate-900">
                {t(lang, "qState")}
              </label>
              <p className="text-sm text-slate-600">{t(lang, "qStateHint")}</p>
              <select
                id="state"
                name="state"
                className="min-h-tap w-full rounded-xl border-2 border-slate-300 bg-white px-4 text-base transition focus:border-brand-600"
                value={answers.state ?? ""}
                onChange={(e) => {
                  const v = e.target.value;
                  if (v) setState(v);
                  else setAnswers((a) => ({ ...a, state: null, district: null }));
                }}
              >
                <option value="">—</option>
                <optgroup label={lang === "ml" ? "സംസ്ഥാനങ്ങൾ" : "States"}>
                  {INDIA_REGIONS.filter((r) => r.kind === "state").map((r) => (
                    <option key={r.name} value={r.name}>
                      {r.short && lang === "ml" && r.name === "Kerala"
                        ? `${r.name} (${r.short})`
                        : r.name}
                    </option>
                  ))}
                </optgroup>
                <optgroup label={lang === "ml" ? "കേന്ദ്രഭരണ പ്രദേശങ്ങൾ" : "Union Territories"}>
                  {INDIA_REGIONS.filter((r) => r.kind === "ut").map((r) => (
                    <option key={r.name} value={r.name}>
                      {r.short ? `${r.name} (${r.short})` : r.name}
                    </option>
                  ))}
                </optgroup>
              </select>
            </div>
          );
        }
        return (
          <div className="space-y-3">
            <label htmlFor="state" className="block text-xl font-bold text-slate-900">
              {t(lang, "qRegion")}
            </label>
            <p className="text-sm text-slate-600">{t(lang, "qRegionHint")}</p>
            {regions.length ? (
              <select
                id="state"
                name="state"
                className="min-h-tap w-full rounded-xl border-2 border-slate-300 bg-white px-4 text-base transition focus:border-brand-600"
                value={regions.includes(answers.state || "") ? answers.state ?? "" : ""}
                onChange={(e) => {
                  const v = e.target.value;
                  if (v) setState(v);
                  else setAnswers((a) => ({ ...a, state: null, district: null }));
                }}
              >
                <option value="">—</option>
                {regions.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            ) : null}
            <input
              id="state_free"
              name="state_free"
              type="text"
              maxLength={DISTRICT_FREE_TEXT_MAX}
              placeholder={t(lang, "qRegionPlaceholder")}
              className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 text-lg transition focus:border-brand-600"
              value={answers.state && !regions.includes(answers.state) ? answers.state : regions.includes(answers.state || "") ? "" : answers.state ?? ""}
              onChange={(e) => {
                const v = e.target.value.trim();
                setAnswers((a) => ({
                  ...a,
                  state: v || null,
                  district: a.state === v ? a.district : null,
                }));
              }}
            />
            <p className="text-xs text-slate-500">{t(lang, "qRegionOrType")}</p>
          </div>
        );
      }
      case 3: {
        const forChild = answers.finding_for === "child";
        return (
          <div className="space-y-3">
            <label htmlFor="age" className="block text-xl font-bold text-slate-900">
              {t(lang, forChild ? "qAgeChild" : "qAge")}
            </label>
            <p className="text-sm text-slate-600">
              {t(lang, forChild ? "qAgeChildHint" : "qAgeHint")}
            </p>
            <input
              id="age"
              name="age"
              type="number"
              inputMode="numeric"
              min={0}
              max={120}
              className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 text-lg transition focus:border-brand-600"
              value={answers.age ?? ""}
              onChange={(e) =>
                setAnswers((a) => ({
                  ...a,
                  age: e.target.value === "" ? null : Number(e.target.value),
                }))
              }
            />
            <AgeLifeStage age={answers.age} lang={lang} />
          </div>
        );
      }
      case 4: {
        const mode = answers.income_mode === "monthly" ? "monthly" : "yearly";
        const amount = answers.income_amount;
        const fmt = (n: number) =>
          Math.round(n).toLocaleString("en-IN");
        const conversion =
          amount != null && amount >= 0
            ? mode === "monthly"
              ? t(lang, "qIncomeAboutYear", {
                  currency,
                  amount: fmt(amount * 12),
                })
              : t(lang, "qIncomeAboutMonth", {
                  currency,
                  amount: fmt(amount / 12),
                })
            : null;
        const setMode = (next: "monthly" | "yearly") => {
          setAnswers((a) => ({
            ...a,
            income_mode: next,
            // Keep typed amount; only change unit interpretation.
            monthly_household_income:
              a.income_amount == null
                ? null
                : next === "monthly"
                  ? a.income_amount
                  : a.income_amount / 12,
          }));
        };
        return (
          <div className="space-y-3">
            <label htmlFor="income" className="block text-xl font-bold text-slate-900">
              {t(lang, mode === "yearly" ? "qIncomeYearlyLabel" : "qIncomeMonthlyLabel")}
            </label>
            <p className="text-sm text-slate-600">{t(lang, "qIncomeHint")}</p>
            <div className="flex gap-2" role="group" aria-label={t(lang, "qIncome")}>
              <button
                type="button"
                className={choiceBtn(mode === "yearly")}
                onClick={() => setMode("yearly")}
                aria-pressed={mode === "yearly"}
              >
                {t(lang, "qIncomeYearly")}
              </button>
              <button
                type="button"
                className={choiceBtn(mode === "monthly")}
                onClick={() => setMode("monthly")}
                aria-pressed={mode === "monthly"}
              >
                {t(lang, "qIncomeMonthly")}
              </button>
            </div>
            <div className="relative">
              <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-lg font-bold text-slate-500">
                {currency}
              </span>
              <input
                id="income"
                name="income"
                type="number"
                inputMode="numeric"
                min={0}
                className="min-h-tap w-full rounded-xl border-2 border-slate-300 py-3 pl-10 pr-4 text-lg transition focus:border-brand-600"
                value={answers.income_amount ?? ""}
                onChange={(e) => {
                  const v = e.target.value === "" ? null : Number(e.target.value);
                  setAnswers((a) => ({
                    ...a,
                    income_amount: v,
                    monthly_household_income:
                      v == null
                        ? null
                        : a.income_mode === "monthly"
                          ? v
                          : v / 12,
                  }));
                }}
              />
            </div>
            {conversion ? (
              <p className="text-sm font-medium text-brand-700">{conversion}</p>
            ) : null}
            <p className="text-xs text-slate-500">
              {t(lang, mode === "yearly" ? "qIncomeYearlyHelper" : "qIncomeMonthlyHelper")}
            </p>
          </div>
        );
      }
      case 5:
        return (
          <fieldset className="space-y-3">
            <legend className="text-xl font-bold text-slate-900">{t(lang, "qOccupation")}</legend>
            <div className="space-y-2">
              {OCCUPATIONS.map((occ) => (
                <button
                  key={occ}
                  type="button"
                  className={choiceBtn(answers.occupation === occ)}
                  onClick={() => setAnswers((a) => ({ ...a, occupation: occ }))}
                  aria-pressed={answers.occupation === occ}
                >
                  {t(lang, `occ_${occ}`)}
                </button>
              ))}
            </div>
          </fieldset>
        );
      case 6:
        return (
          <fieldset className="space-y-3">
            <legend className="text-xl font-bold text-slate-900">{t(lang, "qCategory")}</legend>
            <p className="text-sm text-slate-600">{t(lang, "qCategoryHint")}</p>
            <div className="space-y-2">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  type="button"
                  className={choiceBtn(answers.categories.includes(cat))}
                  onClick={() => toggleCategory(cat)}
                  aria-pressed={answers.categories.includes(cat)}
                >
                  {t(lang, `cat_${cat}`)}
                </button>
              ))}
            </div>
          </fieldset>
        );
      case 7:
        return (
          <fieldset className="space-y-3">
            <legend className="text-xl font-bold text-slate-900">{t(lang, "qLand")}</legend>
            <div className="space-y-2">
              <button
                type="button"
                className={choiceBtn(answers.land_ownership === "yes")}
                onClick={() => setAnswers((a) => ({ ...a, land_ownership: "yes" }))}
                aria-pressed={answers.land_ownership === "yes"}
              >
                {t(lang, "yes")}
              </button>
              <button
                type="button"
                className={choiceBtn(answers.land_ownership === "no")}
                onClick={() => setAnswers((a) => ({ ...a, land_ownership: "no" }))}
                aria-pressed={answers.land_ownership === "no"}
              >
                {t(lang, "no")}
              </button>
            </div>
          </fieldset>
        );
      case 8:
        return (
          <fieldset className="space-y-3">
            <legend className="text-xl font-bold text-slate-900">{t(lang, "qDisability")}</legend>
            <div className="space-y-2">
              <button
                type="button"
                className={choiceBtn(answers.disability === "no")}
                onClick={() =>
                  setAnswers((a) => ({
                    ...a,
                    disability: "no",
                    disability_percent: null,
                  }))
                }
                aria-pressed={answers.disability === "no"}
              >
                {t(lang, "no")}
              </button>
              <button
                type="button"
                className={choiceBtn(answers.disability === "yes")}
                onClick={() => setAnswers((a) => ({ ...a, disability: "yes" }))}
                aria-pressed={answers.disability === "yes"}
              >
                {t(lang, "yes")}
              </button>
            </div>
            {answers.disability === "yes" ? (
              <div className="space-y-2 pt-2">
                <label htmlFor="disability_percent" className="block font-semibold text-slate-800">
                  {t(lang, "qDisabilityPercent")}
                </label>
                <p className="text-sm text-slate-600">{t(lang, "qDisabilityPercentHint")}</p>
                <input
                  id="disability_percent"
                  name="disability_percent"
                  type="number"
                  inputMode="numeric"
                  min={0}
                  max={100}
                  className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 text-lg transition focus:border-brand-600"
                  value={answers.disability_percent ?? ""}
                  onChange={(e) =>
                    setAnswers((a) => ({
                      ...a,
                      disability_percent:
                        e.target.value === "" ? null : Number(e.target.value),
                    }))
                  }
                />
              </div>
            ) : null}
          </fieldset>
        );
      case 9:
        return (
          <div className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="district" className="block text-xl font-bold text-slate-900">
                {t(lang, "qDistrict")}
              </label>
              {isKerala ? (
                <select
                  id="district"
                  name="district"
                  className="min-h-tap w-full rounded-xl border-2 border-slate-300 bg-white px-4 text-base transition focus:border-brand-600"
                  value={answers.district ?? ""}
                  onChange={(e) =>
                    setAnswers((a) => ({
                      ...a,
                      district: e.target.value || null,
                    }))
                  }
                >
                  <option value="">—</option>
                  {KERALA_DISTRICTS.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              ) : (
                <>
                  <p className="text-sm text-slate-600">{t(lang, "qDistrictFreeHint")}</p>
                  <input
                    id="district"
                    name="district"
                    type="text"
                    maxLength={DISTRICT_FREE_TEXT_MAX}
                    autoComplete="address-level2"
                    placeholder={t(lang, "qDistrictPlaceholder")}
                    className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 text-lg transition focus:border-brand-600"
                    value={answers.district ?? ""}
                    onChange={(e) =>
                      setAnswers((a) => ({
                        ...a,
                        district: e.target.value === "" ? null : e.target.value,
                      }))
                    }
                  />
                </>
              )}
            </div>

            <fieldset className="space-y-2">
              <legend className="text-xl font-bold text-slate-900">{t(lang, "qGender")}</legend>
              {GENDERS.map((g) => (
                <button
                  key={g}
                  type="button"
                  className={choiceBtn(answers.gender === g)}
                  onClick={() =>
                    setAnswers((a) => ({
                      ...a,
                      gender: g,
                      maternity: g === "female" ? a.maternity : null,
                    }))
                  }
                  aria-pressed={answers.gender === g}
                >
                  {t(lang, `gen_${g}`)}
                </button>
              ))}
            </fieldset>

            <fieldset className="space-y-2">
              <legend className="text-xl font-bold text-slate-900">{t(lang, "qMarital")}</legend>
              {MARITAL_STATUSES.map((m) => (
                <button
                  key={m}
                  type="button"
                  className={choiceBtn(answers.marital_status === m)}
                  onClick={() => setAnswers((a) => ({ ...a, marital_status: m }))}
                  aria-pressed={answers.marital_status === m}
                >
                  {t(lang, `mar_${m}`)}
                </button>
              ))}
            </fieldset>

            {answers.gender === "female" ? (
              <fieldset className="space-y-2">
                <legend className="text-xl font-bold text-slate-900">{t(lang, "qMaternity")}</legend>
                <p className="text-sm text-slate-600">{t(lang, "qMaternityHint")}</p>
                {(
                  [
                    ["pregnant", "mat_pregnant"],
                    ["lactating", "mat_lactating"],
                    ["neither", "mat_neither"],
                  ] as const
                ).map(([val, key]) => (
                  <button
                    key={val}
                    type="button"
                    className={choiceBtn(answers.maternity === val)}
                    onClick={() => setAnswers((a) => ({ ...a, maternity: val }))}
                    aria-pressed={answers.maternity === val}
                  >
                    {t(lang, key)}
                  </button>
                ))}
              </fieldset>
            ) : null}

            <fieldset className="space-y-2">
              <legend className="text-xl font-bold text-slate-900">{t(lang, "qBreadwinner")}</legend>
              <p className="text-sm text-slate-600">{t(lang, "qBreadwinnerHint")}</p>
              <button
                type="button"
                className={choiceBtn(answers.primary_breadwinner_deceased === "yes")}
                onClick={() =>
                  setAnswers((a) => ({ ...a, primary_breadwinner_deceased: "yes" }))
                }
                aria-pressed={answers.primary_breadwinner_deceased === "yes"}
              >
                {t(lang, "yes")}
              </button>
              <button
                type="button"
                className={choiceBtn(answers.primary_breadwinner_deceased === "no")}
                onClick={() =>
                  setAnswers((a) => ({ ...a, primary_breadwinner_deceased: "no" }))
                }
                aria-pressed={answers.primary_breadwinner_deceased === "no"}
              >
                {t(lang, "no")}
              </button>
            </fieldset>
          </div>
        );
      default:
        return null;
    }
  }, [step, answers, lang, isKerala, currency]);

  if (step === 0) {
    const startAs = (mode: "self" | "child") => {
      setAnswers((a) => ({ ...a, finding_for: mode }));
      setError(null);
      setStep(1);
    };
    return (
      <div className="space-y-6 animate-pop-in">
        <div className="wizard-card bg-gradient-to-br from-brand-50 via-white to-brand-100/60">
          <h2 className="text-2xl font-bold text-brand-900">{t(lang, "welcomeTitle")}</h2>
          <p className="mt-3 text-base leading-relaxed text-brand-900">
            {t(lang, "welcomeBody")}
          </p>
          <p className="mt-4 text-sm font-semibold text-brand-900">{t(lang, "findingForTitle")}</p>
          <p className="mt-1 text-sm leading-relaxed text-brand-800/90">
            {t(lang, "findingForHint")}
          </p>
        </div>
        <button
          type="button"
          onClick={() => startAs("self")}
          className="primary-btn w-full text-lg"
        >
          {t(lang, "findingForSelf")}
        </button>
        <button
          type="button"
          onClick={() => startAs("child")}
          className="min-h-tap w-full rounded-xl border-2 border-brand-700 bg-white px-4 py-3 text-lg font-bold text-brand-900 transition active:scale-95"
        >
          {t(lang, "findingForChild")}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-5 animate-pop-in">
      <ProgressBar lang={lang} step={step} />
      <div className="wizard-card">{field}</div>
      {error ? (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm font-medium text-red-800" role="alert">
          {error}
        </p>
      ) : null}
      <div className="flex gap-3 pt-2">
        <button
          type="button"
          onClick={goBack}
          className="min-h-tap flex-1 rounded-xl border-2 border-slate-300 px-4 py-3 text-base font-bold text-slate-800 transition active:scale-95"
        >
          {t(lang, "back")}
        </button>
        <button type="button" onClick={goNext} className="primary-btn flex-[2] text-base">
          {step >= TOTAL_STEPS ? t(lang, "submit") : t(lang, "next")}
        </button>
      </div>
    </div>
  );
}
