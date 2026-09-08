"use client";

import { useState } from "react";
import { pickLocalized, pickLocalizedList, t } from "@/lib/i18n";
import type { Lang, MatchedScheme } from "@/lib/types";

interface Props {
  lang: Lang;
  scheme: MatchedScheme;
}

export default function SchemeCard({ lang, scheme }: Props) {
  const [open, setOpen] = useState(false);
  const name = pickLocalized(lang, scheme.scheme_name);
  const reason = pickLocalized(lang, scheme.explanation);
  const benefits = pickLocalized(lang, scheme.benefits as { en?: string; ml?: string });
  const docs = pickLocalizedList(lang, scheme.documents);
  const how = pickLocalized(lang, scheme.how_to_apply);

  const badge =
    scheme.verify || scheme.status === "uncertain"
      ? { label: t(lang, scheme.verify ? "verifyBadge" : "uncertainBadge"), cls: "bg-amber-100 text-amber-900 border-amber-300" }
      : { label: t(lang, "likelyBadge"), cls: "bg-brand-100 text-brand-900 border-brand-300" };

  return (
    <article className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <button
        type="button"
        className="flex w-full items-start gap-3 p-4 text-left min-h-tap"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
      >
        <div className="flex-1">
          <div className="mb-2">
            <span className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-semibold ${badge.cls}`}>
              {badge.label}
            </span>
          </div>
          <h3 className="text-lg font-bold leading-snug text-slate-900">{name}</h3>
          {reason ? (
            <p className="mt-2 text-sm leading-relaxed text-slate-700">
              <span className="font-semibold">{t(lang, "reason")}: </span>
              {reason}
            </p>
          ) : null}
          <p className="mt-2 text-sm font-medium text-brand-700">
            {open ? t(lang, "collapse") : t(lang, "expand")}
          </p>
        </div>
        <span className="mt-1 text-2xl text-slate-400" aria-hidden>
          {open ? "−" : "+"}
        </span>
      </button>

      {open ? (
        <div className="space-y-4 border-t border-slate-100 px-4 pb-4 pt-3 text-sm leading-relaxed text-slate-800">
          {benefits ? (
            <section>
              <h4 className="mb-1 font-bold text-slate-900">{t(lang, "benefits")}</h4>
              <p>{benefits}</p>
            </section>
          ) : null}

          {docs.length > 0 ? (
            <section>
              <h4 className="mb-1 font-bold text-slate-900">{t(lang, "documents")}</h4>
              <ul className="list-disc space-y-1 pl-5">
                {docs.map((d) => (
                  <li key={d}>{d}</li>
                ))}
              </ul>
            </section>
          ) : null}

          {how ? (
            <section>
              <h4 className="mb-1 font-bold text-slate-900">{t(lang, "howToApply")}</h4>
              <p>{how}</p>
            </section>
          ) : null}

          {scheme.verify && scheme.verify_notes ? (
            <section className="rounded-lg bg-amber-50 p-3 text-amber-950">
              <p className="font-semibold">{t(lang, "verifyBadge")}</p>
              <p className="mt-1">{scheme.verify_notes}</p>
            </section>
          ) : null}

          <div className="flex flex-col gap-2 pt-1">
            {scheme.apply_url ? (
              <a
                href={scheme.apply_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex min-h-tap items-center justify-center rounded-xl bg-brand-700 px-4 py-3 text-center font-semibold text-white"
              >
                {t(lang, "applyLink")}
              </a>
            ) : null}
            {scheme.official_source_url ? (
              <a
                href={scheme.official_source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex min-h-tap items-center justify-center rounded-xl border-2 border-brand-700 px-4 py-3 text-center font-semibold text-brand-800"
              >
                {t(lang, "officialSource")}
              </a>
            ) : null}
          </div>
        </div>
      ) : null}
    </article>
  );
}
