"use client";

import { t } from "@/lib/i18n";
import type { Lang, MatchResponse } from "@/lib/types";
import Disclaimer from "./Disclaimer";
import SchemeCard from "./SchemeCard";

interface Props {
  lang: Lang;
  data: MatchResponse;
  onRestart: () => void;
}

export default function Results({ lang, data, onRestart }: Props) {
  const matched = data.matched || [];

  if (matched.length === 0) {
    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">{t(lang, "zeroTitle")}</h2>
        <p className="text-base leading-relaxed text-slate-700">{t(lang, "zeroBody")}</p>
        {data.message ? (
          <p className="rounded-xl bg-slate-50 p-3 text-sm text-slate-600">{data.message}</p>
        ) : null}
        <Disclaimer lang={lang} variant="results" />
        <button
          type="button"
          onClick={onRestart}
          className="min-h-tap w-full rounded-xl border-2 border-brand-700 px-4 py-3 text-lg font-bold text-brand-800"
        >
          {t(lang, "startOver")}
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">{t(lang, "resultsTitle")}</h2>
        <p className="mt-1 text-base text-slate-600">
          {t(lang, "resultsCount", { count: matched.length })}
        </p>
        {data.district ? (
          <p className="mt-1 text-sm text-slate-500">
            {lang === "ml" ? "ജില്ല" : "District"}: {data.district}
          </p>
        ) : null}
      </div>

      <div className="space-y-3">
        {matched.map((s) => (
          <SchemeCard key={s.scheme_id} lang={lang} scheme={s} />
        ))}
      </div>

      <Disclaimer lang={lang} variant="results" />

      <button
        type="button"
        onClick={onRestart}
        className="min-h-tap w-full rounded-xl border-2 border-brand-700 px-4 py-3 text-lg font-bold text-brand-800"
      >
        {t(lang, "startOver")}
      </button>
    </div>
  );
}
