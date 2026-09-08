"use client";

import { useMemo, useState } from "react";
import {
  CATEGORIES,
  GENDERS,
  KERALA_DISTRICTS,
  MARITAL_STATUSES,
  OCCUPATIONS,
  TOTAL_STEPS,
} from "@/lib/constants";
import { t } from "@/lib/i18n";
import type { Lang, ProfileAnswers } from "@/lib/types";
import ProgressBar from "./ProgressBar";

const emptyAnswers = (): ProfileAnswers => ({
  age: null,
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
});

interface Props {
  lang: Lang;
  onSubmit: (answers: ProfileAnswers) => void;
}

export default function Wizard({ lang, onSubmit }: Props) {
  const [step, setStep] = useState(0); // 0 = welcome
  const [answers, setAnswers] = useState<ProfileAnswers>(emptyAnswers);
  const [error, setError] = useState<string | null>(null);

  const choiceBtn = (active: boolean) =>
    `min-h-tap w-full rounded-xl border-2 px-4 py-3 text-left text-base font-semibold transition ${
      active
        ? "border-brand-700 bg-brand-100 text-brand-900"
        : "border-slate-200 bg-white text-slate-800 hover:border-brand-500"
    }`;

  const validate = (s: number): boolean => {
    switch (s) {
      case 1:
        return answers.age != null && answers.age >= 0 && answers.age <= 120;
      case 2:
        return (
          answers.monthly_household_income != null &&
          answers.monthly_household_income >= 0
        );
      case 3:
        return !!answers.occupation;
      case 4:
        return answers.categories.length > 0;
      case 5:
        return answers.land_ownership === "yes" || answers.land_ownership === "no";
      case 6:
        return answers.disability === "yes" || answers.disability === "no";
      case 7: {
        const base = !!(answers.district && answers.gender && answers.marital_status);
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
      onSubmit(answers);
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

  const field = useMemo(() => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-3">
            <label htmlFor="age" className="block text-xl font-bold text-slate-900">
              {t(lang, "qAge")}
            </label>
            <p className="text-sm text-slate-600">{t(lang, "qAgeHint")}</p>
            <input
              id="age"
              name="age"
              type="number"
              inputMode="numeric"
              min={0}
              max={120}
              className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 text-lg"
              value={answers.age ?? ""}
              onChange={(e) =>
                setAnswers((a) => ({
                  ...a,
                  age: e.target.value === "" ? null : Number(e.target.value),
                }))
              }
            />
          </div>
        );
      case 2:
        return (
          <div className="space-y-3">
            <label htmlFor="income" className="block text-xl font-bold text-slate-900">
              {t(lang, "qIncome")}
            </label>
            <p className="text-sm text-slate-600">{t(lang, "qIncomeHint")}</p>
            <div className="relative">
              <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-lg font-bold text-slate-500">
                {t(lang, "rupee")}
              </span>
              <input
                id="income"
                name="income"
                type="number"
                inputMode="numeric"
                min={0}
                className="min-h-tap w-full rounded-xl border-2 border-slate-300 py-3 pl-10 pr-4 text-lg"
                value={answers.monthly_household_income ?? ""}
                onChange={(e) =>
                  setAnswers((a) => ({
                    ...a,
                    monthly_household_income:
                      e.target.value === "" ? null : Number(e.target.value),
                  }))
                }
              />
            </div>
          </div>
        );
      case 3:
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
      case 4:
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
      case 5:
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
      case 6:
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
                  className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 text-lg"
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
      case 7:
        return (
          <div className="space-y-6">
            <div className="space-y-2">
              <label htmlFor="district" className="block text-xl font-bold text-slate-900">
                {t(lang, "qDistrict")}
              </label>
              <select
                id="district"
                name="district"
                className="min-h-tap w-full rounded-xl border-2 border-slate-300 bg-white px-4 text-base"
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
  }, [step, answers, lang]);

  if (step === 0) {
    return (
      <div className="space-y-6">
        <div className="rounded-2xl bg-brand-50 p-5">
          <h2 className="text-2xl font-bold text-brand-900">{t(lang, "welcomeTitle")}</h2>
          <p className="mt-3 text-base leading-relaxed text-brand-900">
            {t(lang, "welcomeBody")}
          </p>
        </div>
        <button
          type="button"
          onClick={goNext}
          className="min-h-tap w-full rounded-xl bg-brand-700 px-4 py-3 text-lg font-bold text-white"
        >
          {t(lang, "start")}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <ProgressBar lang={lang} step={step} />
      {field}
      {error ? (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm font-medium text-red-800" role="alert">
          {error}
        </p>
      ) : null}
      <div className="flex gap-3 pt-2">
        <button
          type="button"
          onClick={goBack}
          className="min-h-tap flex-1 rounded-xl border-2 border-slate-300 px-4 py-3 text-base font-bold text-slate-800"
        >
          {t(lang, "back")}
        </button>
        <button
          type="button"
          onClick={goNext}
          className="min-h-tap flex-[2] rounded-xl bg-brand-700 px-4 py-3 text-base font-bold text-white"
        >
          {step >= TOTAL_STEPS ? t(lang, "submit") : t(lang, "next")}
        </button>
      </div>
    </div>
  );
}
