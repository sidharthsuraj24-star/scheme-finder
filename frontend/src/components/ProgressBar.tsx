"use client";

import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";
import { TOTAL_STEPS } from "@/lib/constants";

interface Props {
  lang: Lang;
  step: number;
}

export default function ProgressBar({ lang, step }: Props) {
  const pct = Math.round((step / TOTAL_STEPS) * 100);
  return (
    <div className="w-full" aria-label={t(lang, "progress", { current: step, total: TOTAL_STEPS })}>
      <div className="mb-2 flex justify-between text-sm font-medium text-brand-900">
        <span>{t(lang, "progress", { current: step, total: TOTAL_STEPS })}</span>
        <span>{pct}%</span>
      </div>
      <div className="h-3 w-full overflow-hidden rounded-full bg-brand-100">
        <div
          className="h-full rounded-full bg-brand-600 transition-all duration-300"
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
    </div>
  );
}
