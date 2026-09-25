"use client";

import { useEffect, useRef, useState } from "react";
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

interface WizardError {
  message: string;
  /** ids of invalid inputs / fieldsets */
  fields: string[];
  nonce?: number;
}

const ERROR_ID = "wizard-error";

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
  const [error, setError] = useState<WizardError | null>(null);
  /** Set by navigation so the next render moves focus to the new question. */
  const focusQuestion = useRef(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const isIndia = (answers.country || DEFAULT_COUNTRY) === "India";
  const isKerala = isIndia && answers.state === "Kerala";
  const currency = currencySymbol(answers.country || DEFAULT_COUNTRY);

  const choiceBtn = (active: boolean) =>
    `choice-btn ${active ? "choice-btn--active" : "choice-btn--idle"}`;

  /** Visible shape indicator so selection is not conveyed by colour alone. */
  const indicator = (active: boolean, kind: "radio" | "check" = "radio") => (
    <span
      data-choice-indicator=""
      aria-hidden="true"
      className={`choice-indicator ${kind === "check" ? "choice-indicator--check" : "choice-indicator--radio"}`}
    >
      {active ? "✓" : ""}
    </span>
  );

  const validateDistrict = (): boolean => {
    const d = (answers.district || "").trim();
    if (!d) return false;
    if (d.length > DISTRICT_FREE_TEXT_MAX) return false;
    if (isKerala) {
      return (KERALA_DISTRICTS as readonly string[]).includes(d);
    }
    return true;
  };

  /**
   * Returns null when the step is valid, otherwise a specific, translated
   * message (3.3.1 Error Identification, 3.3.3 Error Suggestion) and the ids
   * of the invalid controls / groups so they can get aria-invalid +
   * aria-describedby and receive focus.
   */
  const validate = (s: number): WizardError | null => {
    const err = (key: string, fields: string[], vars?: Record<string, string>) => ({
      message: t(lang, key, vars),
      fields,
    });
    switch (s) {
      case 1:
        return answers.country ? null : err("errCountry", ["country"]);
      case 2:
        return answers.state ? null : err("errState", ["state", "state_free"]);
      case 3:
        return answers.age != null &&
          Number.isFinite(answers.age) &&
          answers.age >= 0 &&
          answers.age <= 120
          ? null
          : err("errAge", ["age"]);
      case 4: {
        const amount = answers.income_amount;
        if (amount == null || !Number.isFinite(amount) || amount < 0)
          return err("errIncome", ["income"]);
        const max = answers.income_mode === "yearly" ? 100_000_000 : 10_000_000;
        return amount <= max ? null : err("errIncomeMax", ["income"]);
      }
      case 5:
        return answers.occupation ? null : err("errChooseOne", ["q-occupation"]);
      case 6:
        return answers.categories.length > 0
          ? null
          : err("errCategory", ["q-categories"], { none: t(lang, "cat_none") });
      case 7:
        return answers.land_ownership === "yes" || answers.land_ownership === "no"
          ? null
          : err("errChooseOne", ["q-land"]);
      case 8: {
        if (answers.disability !== "yes" && answers.disability !== "no")
          return err("errChooseOne", ["q-disability"]);
        const pct = answers.disability_percent;
        if (answers.disability === "yes" && pct != null && (!Number.isFinite(pct) || pct < 0 || pct > 100))
          return err("errDisabilityPercent", ["disability_percent"]);
        return null;
      }
      case 9: {
        const missing: { id: string; q: string }[] = [];
        if (!validateDistrict()) missing.push({ id: "district", q: "qDistrict" });
        if (!answers.gender) missing.push({ id: "q-gender", q: "qGender" });
        if (!answers.marital_status) missing.push({ id: "q-marital", q: "qMarital" });
        if (answers.gender === "female" && answers.maternity == null)
          missing.push({ id: "q-maternity", q: "qMaternity" });
        if (answers.primary_breadwinner_deceased == null)
          missing.push({ id: "q-breadwinner", q: "qBreadwinner" });
        if (!missing.length) return null;
        if (missing.length === 1 && missing[0].id === "district")
          return err(isKerala ? "errDistrictKerala" : "errDistrict", ["district"]);
        return err("errMissingList", missing.map((m) => m.id), {
          list: missing.map((m) => t(lang, m.q)).join(" · "),
        });
      }
      default:
        return null;
    }
  };

  const goNext = () => {
    if (step === 0) {
      setAnswers((a) => ({ ...a, finding_for: a.finding_for || "self" }));
      focusQuestion.current = true;
      setStep(1);
      setError(null);
      return;
    }
    const problem = validate(step);
    if (problem) {
      setError({ ...problem, nonce: Date.now() });
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
    focusQuestion.current = true;
    setStep((s) => s + 1);
  };

  const goBack = () => {
    setError(null);
    focusQuestion.current = true;
    setStep((s) => Math.max(0, s - 1));
  };

  // 2.4.3 Focus Order / 4.1.3: after Next/Back the old controls unmount, so
  // move focus to the new question heading instead of letting it fall to <body>.
  useEffect(() => {
    if (!focusQuestion.current) return;
    focusQuestion.current = false;
    const target = containerRef.current?.querySelector<HTMLElement>("[data-focus-target]");
    target?.focus();
  }, [step]);

  // On a validation error, focus the first invalid control (or the first
  // option of an invalid group) so keyboard/SR users land on the problem.
  useEffect(() => {
    if (!error) return;
    const first = error.fields
      .map((id) => document.getElementById(id))
      .find((el): el is HTMLElement => !!el);
    if (!first) return;
    const focusable =
      first.tagName === "FIELDSET"
        ? first.querySelector<HTMLElement>("button, input, select")
        : first;
    focusable?.focus();
  }, [error]);

  // Clear the error as soon as the step becomes valid.
  useEffect(() => {
    if (error && !validate(step)) setError(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [answers]);

  const invalid = (id: string) => !!error?.fields.includes(id);
  /** aria-describedby: hints first, then the error message when relevant. */
  const describedBy = (id: string, ...hints: (string | false | null | undefined)[]) => {
    const ids = hints.filter(Boolean) as string[];
    if (invalid(id)) ids.push(ERROR_ID);
    return ids.length ? ids.join(" ") : undefined;
  };
  const fieldAria = (id: string, ...hints: (string | false | null | undefined)[]) => ({
    "aria-invalid": invalid(id) ? (true as const) : undefined,
    "aria-describedby": describedBy(id, ...hints),
  });
  const stepPrefix = (
    <span className="sr-only">{t(lang, "progress", { current: step, total: TOTAL_STEPS })}: </span>
  );
  const qHeading = "block text-xl font-bold text-slate-900";

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

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-3">
            <h2 className={qHeading} tabIndex={-1} data-focus-target="">
              {stepPrefix}
              <label htmlFor="country">{t(lang, "qCountry")}</label>
            </h2>
            <p id="country-hint" className="text-sm text-slate-600">{t(lang, "qCountryHint")}</p>
            <select
              id="country"
              name="country"
              autoComplete="country-name"
              className="field-input text-base"
              value={answers.country ?? ""}
              {...fieldAria("country", "country-hint")}
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
              <h2 className={qHeading} tabIndex={-1} data-focus-target="">
                {stepPrefix}
                <label htmlFor="state">{t(lang, "qState")}</label>
              </h2>
              <p id="state-hint" className="text-sm text-slate-600">{t(lang, "qStateHint")}</p>
              <select
                id="state"
                name="state"
                autoComplete="address-level1"
                className="field-input text-base"
                value={answers.state ?? ""}
                {...fieldAria("state", "state-hint")}
                onChange={(e) => {
                  const v = e.target.value;
                  if (v) setState(v);
                  else setAnswers((a) => ({ ...a, state: null, district: null }));
                }}
              >
                <option value="">—</option>
                <optgroup label={t(lang, "statesGroup")}>
                  {INDIA_REGIONS.filter((r) => r.kind === "state").map((r) => (
                    <option key={r.name} value={r.name}>
                      {r.short && lang === "ml" && r.name === "Kerala"
                        ? `${r.name} (${r.short})`
                        : r.name}
                    </option>
                  ))}
                </optgroup>
                <optgroup label={t(lang, "utGroup")}>
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
            <h2 className={qHeading} tabIndex={-1} data-focus-target="">
              {stepPrefix}
              {regions.length ? (
                <label htmlFor="state">{t(lang, "qRegion")}</label>
              ) : (
                <label htmlFor="state_free">{t(lang, "qRegion")}</label>
              )}
            </h2>
            <p id="state-hint" className="text-sm text-slate-600">{t(lang, "qRegionHint")}</p>
            {regions.length ? (
              <select
                id="state"
                name="state"
                autoComplete="address-level1"
                className="field-input text-base"
                value={regions.includes(answers.state || "") ? answers.state ?? "" : ""}
                {...fieldAria("state", "state-hint")}
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
            {regions.length ? (
              <label htmlFor="state_free" className="block pt-1 font-semibold text-slate-800">
                {t(lang, "qRegionTypeLabel")}
              </label>
            ) : null}
            <p id="state-free-hint" className="text-sm text-slate-600">{t(lang, "qRegionOrType")}</p>
            <input
              id="state_free"
              name="state_free"
              type="text"
              autoComplete="address-level1"
              maxLength={DISTRICT_FREE_TEXT_MAX}
              placeholder={t(lang, "qRegionPlaceholder")}
              className="field-input"
              {...fieldAria("state_free", "state-free-hint")}
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
          </div>
        );
      }
      case 3: {
        const forChild = answers.finding_for === "child";
        return (
          <div className="space-y-3">
            <h2 className={qHeading} tabIndex={-1} data-focus-target="">
              {stepPrefix}
              <label htmlFor="age">{t(lang, forChild ? "qAgeChild" : "qAge")}</label>
            </h2>
            <p id="age-hint" className="text-sm text-slate-600">
              {t(lang, forChild ? "qAgeChildHint" : "qAgeHint")}
            </p>
            <input
              id="age"
              name="age"
              type="number"
              inputMode="numeric"
              min={0}
              max={120}
              className="field-input"
              {...fieldAria("age", "age-hint")}
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
            <h2 className={qHeading} tabIndex={-1} data-focus-target="">
              {stepPrefix}
              <label htmlFor="income">
                {t(lang, mode === "yearly" ? "qIncomeYearlyLabel" : "qIncomeMonthlyLabel")}
              </label>
            </h2>
            <p id="income-hint" className="text-sm text-slate-600">{t(lang, "qIncomeHint")}</p>
            <div className="flex gap-2" role="group" aria-label={t(lang, "qIncome")}>
              <button
                type="button"
                className={choiceBtn(mode === "yearly")}
                onClick={() => setMode("yearly")}
                aria-pressed={mode === "yearly"}
              >
                {indicator(mode === "yearly")}
                {t(lang, "qIncomeYearly")}
              </button>
              <button
                type="button"
                className={choiceBtn(mode === "monthly")}
                onClick={() => setMode("monthly")}
                aria-pressed={mode === "monthly"}
              >
                {indicator(mode === "monthly")}
                {t(lang, "qIncomeMonthly")}
              </button>
            </div>
            <div className="relative">
              <span
                id="income-currency"
                className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-lg font-bold text-slate-700"
              >
                {currency}
              </span>
              <input
                id="income"
                name="income"
                type="number"
                inputMode="numeric"
                min={0}
                className="field-input py-3 pl-10 pr-4"
                {...fieldAria("income", "income-currency", "income-hint", "income-helper")}
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
              <p className="text-sm font-medium text-brand-800">{conversion}</p>
            ) : null}
            <p id="income-helper" className="text-sm text-slate-600">
              {t(lang, mode === "yearly" ? "qIncomeYearlyHelper" : "qIncomeMonthlyHelper")}
            </p>
          </div>
        );
      }
      case 5:
        return (
          <fieldset id="q-occupation" className="space-y-3" {...fieldAria("q-occupation")}>
            <legend>
              <h2 className={qHeading} tabIndex={-1} data-focus-target="">
                {stepPrefix}
                {t(lang, "qOccupation")}
              </h2>
            </legend>
            <div className="space-y-2">
              {OCCUPATIONS.map((occ) => (
                <button
                  key={occ}
                  type="button"
                  className={choiceBtn(answers.occupation === occ)}
                  onClick={() => setAnswers((a) => ({ ...a, occupation: occ }))}
                  aria-pressed={answers.occupation === occ}
                >
                  {indicator(answers.occupation === occ)}
                  {t(lang, `occ_${occ}`)}
                </button>
              ))}
            </div>
          </fieldset>
        );
      case 6:
        return (
          <fieldset
            id="q-categories"
            className="space-y-3"
            {...fieldAria("q-categories", "q-categories-hint")}
          >
            <legend>
              <h2 className={qHeading} tabIndex={-1} data-focus-target="">
                {stepPrefix}
                {t(lang, "qCategory")}
              </h2>
            </legend>
            <p id="q-categories-hint" className="text-sm text-slate-600">{t(lang, "qCategoryHint")}</p>
            <div className="space-y-2">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  type="button"
                  className={choiceBtn(answers.categories.includes(cat))}
                  onClick={() => toggleCategory(cat)}
                  aria-pressed={answers.categories.includes(cat)}
                >
                  {indicator(answers.categories.includes(cat), "check")}
                  {t(lang, `cat_${cat}`)}
                </button>
              ))}
            </div>
          </fieldset>
        );
      case 7:
        return (
          <fieldset id="q-land" className="space-y-3" {...fieldAria("q-land")}>
            <legend>
              <h2 className={qHeading} tabIndex={-1} data-focus-target="">
                {stepPrefix}
                {t(lang, "qLand")}
              </h2>
            </legend>
            <div className="space-y-2">
              {(["yes", "no"] as const).map((v) => (
                <button
                  key={v}
                  type="button"
                  className={choiceBtn(answers.land_ownership === v)}
                  onClick={() => setAnswers((a) => ({ ...a, land_ownership: v }))}
                  aria-pressed={answers.land_ownership === v}
                >
                  {indicator(answers.land_ownership === v)}
                  {t(lang, v)}
                </button>
              ))}
            </div>
          </fieldset>
        );
      case 8: {
        const forChild = answers.finding_for === "child";
        return (
          <fieldset id="q-disability" className="space-y-3" {...fieldAria("q-disability")}>
            <legend>
              <h2 className={qHeading} tabIndex={-1} data-focus-target="">
                {stepPrefix}
                {t(lang, forChild ? "qDisabilityChild" : "qDisability")}
              </h2>
            </legend>
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
                {indicator(answers.disability === "no")}
                {t(lang, "no")}
              </button>
              <button
                type="button"
                className={choiceBtn(answers.disability === "yes")}
                onClick={() => setAnswers((a) => ({ ...a, disability: "yes" }))}
                aria-pressed={answers.disability === "yes"}
              >
                {indicator(answers.disability === "yes")}
                {t(lang, "yes")}
              </button>
            </div>
            {answers.disability === "yes" ? (
              <div className="space-y-2 pt-2">
                <label htmlFor="disability_percent" className="block font-semibold text-slate-800">
                  {t(lang, "qDisabilityPercent")}
                </label>
                <p id="disability-percent-hint" className="text-sm text-slate-600">
                  {t(lang, "qDisabilityPercentHint")}
                </p>
                <input
                  id="disability_percent"
                  name="disability_percent"
                  type="number"
                  inputMode="numeric"
                  min={0}
                  max={100}
                  className="field-input"
                  {...fieldAria("disability_percent", "disability-percent-hint")}
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
      }
      case 9:
        return (
          <div className="space-y-6">
            <div className="space-y-2">
              <h2 className={qHeading} tabIndex={-1} data-focus-target="">
                {stepPrefix}
                <label htmlFor="district">{t(lang, "qDistrict")}</label>
              </h2>
              {isKerala ? (
                <select
                  id="district"
                  name="district"
                  autoComplete="address-level2"
                  className="field-input text-base"
                  {...fieldAria("district")}
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
                  <p id="district-hint" className="text-sm text-slate-600">{t(lang, "qDistrictFreeHint")}</p>
                  <input
                    id="district"
                    name="district"
                    type="text"
                    maxLength={DISTRICT_FREE_TEXT_MAX}
                    autoComplete="address-level2"
                    placeholder={t(lang, "qDistrictPlaceholder")}
                    className="field-input"
                    {...fieldAria("district", "district-hint")}
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

            <fieldset id="q-gender" className="space-y-2" {...fieldAria("q-gender")}>
              <legend className="mb-2">
                <h2 className={qHeading}>{t(lang, "qGender")}</h2>
              </legend>
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
                  {indicator(answers.gender === g)}
                  {t(lang, `gen_${g}`)}
                </button>
              ))}
            </fieldset>

            <fieldset id="q-marital" className="space-y-2" {...fieldAria("q-marital")}>
              <legend className="mb-2">
                <h2 className={qHeading}>{t(lang, "qMarital")}</h2>
              </legend>
              {MARITAL_STATUSES.map((m) => (
                <button
                  key={m}
                  type="button"
                  className={choiceBtn(answers.marital_status === m)}
                  onClick={() => setAnswers((a) => ({ ...a, marital_status: m }))}
                  aria-pressed={answers.marital_status === m}
                >
                  {indicator(answers.marital_status === m)}
                  {t(lang, `mar_${m}`)}
                </button>
              ))}
            </fieldset>

            {answers.gender === "female" ? (
              <fieldset
                id="q-maternity"
                className="space-y-2"
                {...fieldAria("q-maternity", "q-maternity-hint")}
              >
                <legend className="mb-2">
                  <h2 className={qHeading}>{t(lang, "qMaternity")}</h2>
                </legend>
                <p id="q-maternity-hint" className="text-sm text-slate-600">{t(lang, "qMaternityHint")}</p>
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
                    {indicator(answers.maternity === val)}
                    {t(lang, key)}
                  </button>
                ))}
              </fieldset>
            ) : null}

            <fieldset
              id="q-breadwinner"
              className="space-y-2"
              {...fieldAria("q-breadwinner", "q-breadwinner-hint")}
            >
              <legend className="mb-2">
                <h2 className={qHeading}>{t(lang, "qBreadwinner")}</h2>
              </legend>
              <p id="q-breadwinner-hint" className="text-sm text-slate-600">{t(lang, "qBreadwinnerHint")}</p>
              {(["yes", "no"] as const).map((v) => (
                <button
                  key={v}
                  type="button"
                  className={choiceBtn(answers.primary_breadwinner_deceased === v)}
                  onClick={() =>
                    setAnswers((a) => ({ ...a, primary_breadwinner_deceased: v }))
                  }
                  aria-pressed={answers.primary_breadwinner_deceased === v}
                >
                  {indicator(answers.primary_breadwinner_deceased === v)}
                  {t(lang, v)}
                </button>
              ))}
            </fieldset>
          </div>
        );
      default:
        return null;
    }
  };

  if (step === 0) {
    const startAs = (mode: "self" | "child") => {
      setAnswers((a) => ({ ...a, finding_for: mode }));
      setError(null);
      focusQuestion.current = true;
      setStep(1);
    };
    return (
      <div ref={containerRef} className="space-y-6 animate-pop-in">
        <div className="wizard-card bg-gradient-to-br from-brand-50 via-white to-brand-100/60">
          <h2
            id="welcome-heading"
            className="text-2xl font-bold text-brand-900"
            tabIndex={-1}
            data-focus-target=""
          >
            {t(lang, "welcomeTitle")}
          </h2>
          <p className="mt-3 text-base leading-relaxed text-brand-900">
            {t(lang, "welcomeBody")}
          </p>
          {initialAnswers ? (
            <p className="mt-3 rounded-lg bg-white px-3 py-2 text-sm font-medium text-brand-900">
              {t(lang, "wizardEditing")}
            </p>
          ) : null}
          <p id="finding-for-title" className="mt-4 text-sm font-semibold text-brand-900">
            {t(lang, "findingForTitle")}
          </p>
          <p id="finding-for-hint" className="mt-1 text-sm leading-relaxed text-brand-900">
            {t(lang, "findingForHint")}
          </p>
        </div>
        <div
          role="group"
          aria-labelledby="finding-for-title"
          aria-describedby="finding-for-hint"
          className="space-y-6"
        >
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
      </div>
    );
  }

  return (
    <div ref={containerRef} className="space-y-5 animate-pop-in">
      <ProgressBar lang={lang} step={step} />
      <div className="wizard-card space-y-4">
        {renderStep()}
        {error ? (
          <p id={ERROR_ID} className="field-error" role="alert" key={error.nonce}>
            {error.message}
          </p>
        ) : null}
      </div>
      <div className="flex gap-3 pt-2">
        <button
          type="button"
          onClick={goBack}
          className="min-h-tap flex-1 rounded-xl border-2 border-slate-500 bg-white px-4 py-3 text-base font-bold text-slate-800 transition active:scale-95"
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
