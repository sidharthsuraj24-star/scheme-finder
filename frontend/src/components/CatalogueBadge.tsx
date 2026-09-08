"use client";

import catalogueMeta from "../../data/catalogue_meta.json";
import { isCatalogueStale } from "@/lib/matching/catalogue";
import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

function formatAsOf(isoDate: string, lang: Lang): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(isoDate);
  if (!m) return isoDate;
  const y = Number(m[1]);
  const mo = Number(m[2]);
  const d = Number(m[3]);
  const monthsEn = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
  ];
  if (lang === "ml") {
    return `${d} ${monthsEn[mo - 1]} ${y}`;
  }
  return `${d} ${monthsEn[mo - 1]} ${y}`;
}

export default function CatalogueBadge({ lang }: { lang: Lang }) {
  const asOf = catalogueMeta.updated_as_of as string;
  const stale = isCatalogueStale(catalogueMeta as Parameters<typeof isCatalogueStale>[0]);
  const dateLabel = formatAsOf(asOf, lang);

  if (stale) {
    return (
      <div
        className="rounded-xl border border-amber-300 bg-amber-50 px-3 py-2 text-xs leading-snug text-amber-950"
        role="status"
      >
        {t(lang, "dataStaleBanner", { date: dateLabel })}
      </div>
    );
  }

  return (
    <div
      className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs leading-snug text-emerald-950"
      role="status"
    >
      <p>{t(lang, "dataFreshBanner", { date: dateLabel })}</p>
      <p className="mt-1 font-medium">{t(lang, "dataFreshConfirm")}</p>
    </div>
  );
}
