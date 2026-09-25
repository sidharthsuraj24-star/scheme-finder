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
  /** Return to the wizard with the same answers prefilled (3.3.7). */
  onEdit?: () => void;
  /** Push a message to the page's polite live region (4.1.3). */
  onStatus?: (msg: string) => void;
  shareUrl?: string | null;
  /** Annual income used for matching (local currency units), when the user provided income. */
  filteredAnnualIncome?: number | null;
  findingFor?: "self" | "child" | null;
}

function ShareButtons({
  lang,
  shareUrl,
  onStatus,
}: {
  lang: Lang;
  shareUrl: string;
  onStatus?: (msg: string) => void;
}) {
  const [copied, setCopied] = useState(false);
  const [failed, setFailed] = useState(false);

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
      setFailed(false);
      onStatus?.(t(lang, "shareCopied"));
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      // Inline, announced message instead of a blocking alert().
      setFailed(true);
      onStatus?.(t(lang, "shareCopyFailedInline"));
    }
  };

  const waText = `${t(lang, "shareMessage")} ${shareUrl}`;
  const waHref = `https://wa.me/?text=${encodeURIComponent(waText)}`;

  return (
    <div className="space-y-2">
    <div className="flex flex-col gap-2 sm:flex-row">
      <button
        type="button"
        onClick={() => void copyLink()}
        className="min-h-tap flex-1 rounded-xl border-2 border-brand-700 bg-brand-50 px-4 py-3 text-base font-bold text-brand-900"
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
        <span className="sr-only"> {t(lang, "opensNewTab")}</span>
      </a>
    </div>
    {failed ? (
      <p className="text-sm font-medium text-red-800">{t(lang, "shareCopyFailedInline")}</p>
    ) : null}
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
  onEdit,
  onStatus,
}: Props) {
  const matched = data.matched || [];
  const parentMode = findingFor === "child";
  const headingProps = {
    id: "results-heading",
    tabIndex: -1,
    "data-focus-target": "",
  } as const;
  const actions = (
    <div className="flex flex-col gap-2">
      {onEdit ? (
        <button
          type="button"
          onClick={onEdit}
          className="min-h-tap w-full rounded-xl bg-brand-700 px-4 py-3 text-lg font-bold text-white"
        >
          {t(lang, "changeAnswers")}
        </button>
      ) : null}
      <button
        type="button"
        onClick={onRestart}
        className="min-h-tap w-full rounded-xl border-2 border-brand-700 bg-white px-4 py-3 text-lg font-bold text-brand-800"
      >
        {t(lang, "startOver")}
      </button>
    </div>
  );

  if (matched.length === 0) {
    return (
      <div className="space-y-4">
        <h2 {...headingProps} className="text-2xl font-bold text-slate-900">
          {t(lang, "zeroTitle")}
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
          <p className="mt-1 text-sm text-slate-700">
            {t(lang, "resultsIncomeFilter", {
              currency: currencySymbol(data.country),
              amount: Math.round(filteredAnnualIncome).toLocaleString("en-IN"),
            })}
          </p>
        ) : null}
        {isIndiaCountry(data.country) && data.income_band && data.income_band_label ? (
          <p className="mt-1 text-sm text-slate-700">
            {t(lang, "resultsIncomeBand", { label: data.income_band_label })}
          </p>
        ) : null}
        {data.message ? (
          <p className="rounded-xl bg-slate-50 p-3 text-sm text-slate-700" lang={lang === "en" ? undefined : "en"}>
            {data.message}
          </p>
        ) : null}
        {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} onStatus={onStatus} /> : null}
        <p className="rounded-xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm font-medium leading-relaxed text-sky-950" role="note">{t(lang, "resultsConfirmBanner")}</p>
        <Disclaimer lang={lang} variant="results" />
        {actions}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h2 {...headingProps} className="text-2xl font-bold text-slate-900">
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
          <p className="mt-1 text-sm text-slate-700">
            {data.country ? `${t(lang, "resultsCountry")}: ${data.country}` : ""}
            {data.country && data.state ? " · " : ""}
            {data.state ? `${t(lang, "resultsState")}: ${data.state}` : ""}
            {data.district ? ` · ${t(lang, "resultsDistrict")}: ${data.district}` : ""}
          </p>
        ) : data.district ? (
          <p className="mt-1 text-sm text-slate-700">
            {t(lang, "resultsDistrict")}: {data.district}
          </p>
        ) : null}
        {filteredAnnualIncome != null && filteredAnnualIncome >= 0 ? (
          <p className="mt-1 text-sm text-slate-700">
            {t(lang, "resultsIncomeFilter", {
              currency: currencySymbol(data.country),
              amount: Math.round(filteredAnnualIncome).toLocaleString("en-IN"),
            })}
          </p>
        ) : null}
        {isIndiaCountry(data.country) && data.income_band && data.income_band_label ? (
          <p className="mt-1 text-sm text-slate-700">
            {t(lang, "resultsIncomeBand", { label: data.income_band_label })}
          </p>
        ) : null}
      </div>

      {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} onStatus={onStatus} /> : null}

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

      {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} onStatus={onStatus} /> : null}

      {actions}
    </div>
  );
}
