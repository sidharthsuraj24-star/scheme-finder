"use client";

import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

export default function CatalogueBadge({ lang }: { lang: Lang }) {
  return (
    <div
      className="rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs leading-snug text-emerald-950"
      role="status"
    >
      {t(lang, "dataUpdated")}
    </div>
  );
}
