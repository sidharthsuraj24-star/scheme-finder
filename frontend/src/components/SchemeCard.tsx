"use client";

import { useId, useState } from "react";
import { safeHttpUrl } from "@/lib/api";
import {
  pickLocalizedListWithLang,
  pickLocalizedWithLang,
  t,
} from "@/lib/i18n";
import type { Lang, MatchedScheme } from "@/lib/types";

interface Props {
  lang: Lang;
  scheme: MatchedScheme;
}

/** Mark fallback-language text (e.g. English scheme body on a Hindi page) — 3.1.2. */
const partLang = (page: Lang, text: Lang) => (text !== page ? text : undefined);

export default function SchemeCard({ lang, scheme }: Props) {
  const [open, setOpen] = useState(false);
  const uid = useId();
  const nameId = `${uid}-name`;
  const detailsId = `${uid}-details`;

  const name = pickLocalizedWithLang(lang, scheme.scheme_name);
  const reason = pickLocalizedWithLang(lang, scheme.explanation);
  const benefits = pickLocalizedWithLang(
    lang,
    scheme.benefits as { en?: string; ml?: string; hi?: string },
  );
  const docs = pickLocalizedListWithLang(lang, scheme.documents);
  const how = pickLocalizedWithLang(lang, scheme.how_to_apply);

  const applyUrl = safeHttpUrl(scheme.apply_url);
  const sourceUrl = safeHttpUrl(scheme.official_source_url);
  const confirmUrl = sourceUrl || applyUrl;

  const badge =
    scheme.verify || scheme.status === "uncertain"
      ? {
          label: t(lang, scheme.verify ? "verifyBadge" : "uncertainBadge"),
          cls: "bg-amber-100 text-amber-900 border-amber-400",
        }
      : { label: t(lang, "likelyBadge"), cls: "bg-brand-100 text-brand-900 border-brand-700" };

  // Structure (1.3.1 / 4.1.2): the scheme name is a real <h3> (headings
  // navigable), badge + reason are normal text (previously hidden from AT by
  // the toggle's aria-label), and a separate disclosure button controls the
  // details region via aria-expanded + aria-controls.
  return (
    <article
      className="scheme-card rounded-2xl border border-slate-300 bg-white shadow-sm"
      aria-labelledby={nameId}
    >
      <div className="p-4">
        <div className="mb-2 flex flex-wrap items-center gap-2">
          <span
            className={`inline-block rounded-full border px-2.5 py-0.5 text-xs font-semibold ${badge.cls}`}
          >
            {badge.label}
          </span>
          {scheme.last_verified ? (
            <span className="text-xs font-medium text-slate-700">
              {t(lang, "lastVerified", { date: scheme.last_verified })}
            </span>
          ) : null}
        </div>
        <h3
          id={nameId}
          className="text-lg font-bold leading-snug text-slate-900"
          lang={partLang(lang, name.lang)}
        >
          {name.text}
        </h3>
        {reason.text ? (
          <p className="mt-2 text-sm leading-relaxed text-slate-700">
            <span className="font-semibold">{t(lang, "reason")}: </span>
            <span lang={partLang(lang, reason.lang)}>{reason.text}</span>
          </p>
        ) : null}
        <button
          type="button"
          className="mt-2 flex min-h-tap w-full items-center justify-between gap-3 rounded-xl border-2 border-brand-700 bg-white px-3 py-2 text-left text-sm font-semibold text-brand-800 hover:bg-brand-50"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          aria-controls={detailsId}
        >
          <span>
            {open ? t(lang, "collapse") : t(lang, "expand")}
            <span className="sr-only">
              {": "}
              <span lang={partLang(lang, name.lang)}>{name.text}</span>
            </span>
          </span>
          <span className="text-2xl leading-none" aria-hidden="true">
            {open ? "−" : "+"}
          </span>
        </button>
      </div>

      <div
        id={detailsId}
        hidden={!open}
        className="space-y-4 border-t border-slate-200 px-4 pb-4 pt-3 text-sm leading-relaxed text-slate-800"
      >
        {open ? (
          <>
            {benefits.text ? (
              <section>
                <h4 className="mb-1 font-bold text-slate-900">{t(lang, "benefits")}</h4>
                <p lang={partLang(lang, benefits.lang)}>{benefits.text}</p>
              </section>
            ) : null}

            {docs.items.length > 0 ? (
              <section>
                <h4 className="mb-1 font-bold text-slate-900">{t(lang, "documents")}</h4>
                <ul className="list-disc space-y-1 pl-5" lang={partLang(lang, docs.lang)}>
                  {docs.items.map((d) => (
                    <li key={d}>{d}</li>
                  ))}
                </ul>
              </section>
            ) : null}

            {how.text ? (
              <section>
                <h4 className="mb-1 font-bold text-slate-900">{t(lang, "howToApply")}</h4>
                <p lang={partLang(lang, how.lang)}>{how.text}</p>
              </section>
            ) : null}

            {scheme.verify && scheme.verify_notes ? (
              <section className="rounded-lg bg-amber-50 p-3 text-amber-950">
                <p className="font-semibold">{t(lang, "verifyBadge")}</p>
                <p className="mt-1" lang={lang === "en" ? undefined : "en"}>
                  {scheme.verify_notes}
                </p>
                <p className="mt-2 text-xs font-medium">{t(lang, "dataFreshConfirm")}</p>
              </section>
            ) : null}

            <div className="flex flex-col gap-2 pt-1">
              {confirmUrl ? (
                <a
                  href={confirmUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex min-h-tap items-center justify-center rounded-xl bg-brand-700 px-4 py-3 text-center font-semibold text-white"
                >
                  {t(lang, "officialSourceConfirm")}
                  <span className="sr-only">
                    {" — "}
                    <span lang={partLang(lang, name.lang)}>{name.text}</span> {t(lang, "opensNewTab")}
                  </span>
                </a>
              ) : null}
              {confirmUrl ? (
                <p className="text-xs text-slate-700">{t(lang, "dataFreshConfirm")}</p>
              ) : null}
              {applyUrl && sourceUrl && applyUrl !== sourceUrl ? (
                <a
                  href={applyUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex min-h-tap items-center justify-center rounded-xl border-2 border-brand-700 px-4 py-3 text-center font-semibold text-brand-800"
                >
                  {t(lang, "applyLink")}
                  <span className="sr-only">
                    {" — "}
                    <span lang={partLang(lang, name.lang)}>{name.text}</span> {t(lang, "opensNewTab")}
                  </span>
                </a>
              ) : null}
            </div>
          </>
        ) : null}
      </div>
    </article>
  );
}
