"use client";

import { useState } from "react";
import { currencySymbol } from "@/lib/countries";
import { isIndiaCountry } from "@/lib/matching/incomeBands";
import { t } from "@/lib/i18n";
import type { Lang, MatchResponse } from "@/lib/types";
import Disclaimer from "./Disclaimer";
import SchemeCard from "./SchemeCard";

interface Props {
  lang: Lang;
  data: MatchResponse;
  onRestart: () => void;
  shareUrl?: string | null;
  /** Annual income used for matching (local currency units), when the user provided income. */
  filteredAnnualIncome?: number | null;
  findingFor?: "self" | "child" | null;
}

function ShareButtons({
  lang,
  shareUrl,
}: {
  lang: Lang;
  shareUrl: string;
}) {
  const [copied, setCopied] = useState(false);

  const copyLink = async () => {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(shareUrl);
      } else {
        const ta = document.createElement("textarea");
        ta.value = shareUrl;
        ta.setAttribute("readonly", "");
        ta.style.position = "absolute";
        ta.style.left = "-9999px";
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        document.body.removeChild(ta);
      }
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      window.alert(t(lang, "shareCopyFailed"));
    }
  };

  const waText = `${t(lang, "shareMessage")} ${shareUrl}`;
  const waHref = `https://wa.me/?text=${encodeURIComponent(waText)}`;

  return (
    <div className="flex flex-col gap-2 sm:flex-row">
      <button
        type="button"
        onClick={() => void copyLink()}
        className="min-h-tap flex-1 rounded-xl border-2 border-brand-600 bg-brand-50 px-4 py-3 text-base font-bold text-brand-900"
      >
        {copied ? t(lang, "shareCopied") : t(lang, "shareCopyLink")}
      </button>
      <a
        href={waHref}
        target="_blank"
        rel="noopener noreferrer"
        className="min-h-tap flex-1 rounded-xl border-2 border-emerald-600 bg-emerald-50 px-4 py-3 text-center text-base font-bold text-emerald-900"
      >
        {t(lang, "shareWhatsApp")}
      </a>
    </div>
  );
}

export default function Results({
  lang,
  data,
  onRestart,
  shareUrl,
  filteredAnnualIncome,
  findingFor,
}: Props) {
  const matched = data.matched || [];
  const parentMode = findingFor === "child";

  if (matched.length === 0) {
    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">
          {t(lang, parentMode ? "resultsTitleChild" : "zeroTitle")}
        </h2>
        <p className="text-base leading-relaxed text-slate-700">{t(lang, "zeroBody")}</p>

      {parentMode ? (
        <p
          className="rounded-xl border border-violet-200 bg-violet-50 px-4 py-3 text-sm font-medium leading-relaxed text-violet-950"
          role="note"
        >
          {t(lang, "resultsParentModeBanner")}
        </p>
      ) : null}
        {filteredAnnualIncome != null && filteredAnnualIncome >= 0 ? (
          <p className="mt-1 text-sm text-slate-500">
            {t(lang, "resultsIncomeFilter", {
              currency: currencySymbol(data.country),
              amount: Math.round(filteredAnnualIncome).toLocaleString("en-IN"),
            })}
          </p>
        ) : null}
        {isIndiaCountry(data.country) && data.income_band && data.income_band_label ? (
          <p className="mt-1 text-sm text-slate-500">
            {t(lang, "resultsIncomeBand", { label: data.income_band_label })}
          </p>
        ) : null}
        {data.message ? (
          <p className="rounded-xl bg-slate-50 p-3 text-sm text-slate-600">{data.message}</p>
        ) : null}
        {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} /> : null}
        <p className="rounded-xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm font-medium leading-relaxed text-sky-950" role="note">{t(lang, "resultsConfirmBanner")}</p>
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
        <h2 className="text-2xl font-bold text-slate-900">
          {t(lang, parentMode ? "resultsTitleChild" : "resultsTitle")}
        </h2>
        <p className="mt-1 text-base text-slate-600">
          {t(lang, "resultsCount", { count: matched.length })}
        </p>

      {parentMode ? (
        <p
          className="rounded-xl border border-violet-200 bg-violet-50 px-4 py-3 text-sm font-medium leading-relaxed text-violet-950"
          role="note"
        >
          {t(lang, "resultsParentModeBanner")}
        </p>
      ) : null}
        {data.country || data.state ? (
          <p className="mt-1 text-sm text-slate-500">
            {data.country ? `${t(lang, "resultsCountry")}: ${data.country}` : ""}
            {data.country && data.state ? " · " : ""}
            {data.state ? `${t(lang, "resultsState")}: ${data.state}` : ""}
            {data.district ? ` · ${lang === "ml" ? "ജില്ല" : "District"}: ${data.district}` : ""}
          </p>
        ) : data.district ? (
          <p className="mt-1 text-sm text-slate-500">
            {lang === "ml" ? "ജില്ല" : "District"}: {data.district}
          </p>
        ) : null}
        {filteredAnnualIncome != null && filteredAnnualIncome >= 0 ? (
          <p className="mt-1 text-sm text-slate-500">
            {t(lang, "resultsIncomeFilter", {
              currency: currencySymbol(data.country),
              amount: Math.round(filteredAnnualIncome).toLocaleString("en-IN"),
            })}
          </p>
        ) : null}
        {isIndiaCountry(data.country) && data.income_band && data.income_band_label ? (
          <p className="mt-1 text-sm text-slate-500">
            {t(lang, "resultsIncomeBand", { label: data.income_band_label })}
          </p>
        ) : null}
      </div>

      {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} /> : null}

      <p
        className="rounded-xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm font-medium leading-relaxed text-sky-950"
        role="note"
      >
        {t(lang, "resultsConfirmBanner")}
      </p>

      <div className="space-y-3">
        {matched.map((s) => (
          <SchemeCard key={s.scheme_id} lang={lang} scheme={s} />
        ))}
      </div>

      <Disclaimer lang={lang} variant="results" />

      {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} /> : null}

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
