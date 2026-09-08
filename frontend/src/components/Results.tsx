"use client";

import { useState } from "react";
import { t } from "@/lib/i18n";
import type { Lang, MatchResponse } from "@/lib/types";
import Disclaimer from "./Disclaimer";
import SchemeCard from "./SchemeCard";

interface Props {
  lang: Lang;
  data: MatchResponse;
  onRestart: () => void;
  shareUrl?: string | null;
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

export default function Results({ lang, data, onRestart, shareUrl }: Props) {
  const matched = data.matched || [];

  if (matched.length === 0) {
    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">{t(lang, "zeroTitle")}</h2>
        <p className="text-base leading-relaxed text-slate-700">{t(lang, "zeroBody")}</p>
        {data.message ? (
          <p className="rounded-xl bg-slate-50 p-3 text-sm text-slate-600">{data.message}</p>
        ) : null}
        {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} /> : null}
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

      {shareUrl ? <ShareButtons lang={lang} shareUrl={shareUrl} /> : null}

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
