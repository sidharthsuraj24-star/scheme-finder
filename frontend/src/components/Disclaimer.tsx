"use client";

import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

export default function Disclaimer({
  lang,
  variant = "default",
}: {
  lang: Lang;
  variant?: "default" | "results";
}) {
  const key = variant === "results" ? "resultsFooterDisclaimer" : "disclaimer";
  return (
    <p className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-relaxed text-amber-950">
      {t(lang, key)}
    </p>
  );
}
