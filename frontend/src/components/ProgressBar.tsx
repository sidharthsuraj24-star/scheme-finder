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
  const label = t(lang, "progress", { current: step, total: TOTAL_STEPS });
  return (
    <div className="w-full">
      {/* Visible text already conveys progress; the bar itself is decorative for
          sighted users but exposed as a named progressbar for AT (4.1.2). */}
      <div className="mb-2 flex justify-between text-sm font-medium text-brand-900" aria-hidden="true">
        <span>{label}</span>
        <span>{pct}%</span>
      </div>
      <div className="h-3 w-full overflow-hidden rounded-full bg-brand-100 shadow-inner">
        <div
          className="h-full rounded-full bg-gradient-to-r from-brand-500 to-brand-700 transition-[width] duration-500 ease-out"
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-label={label}
          aria-valuenow={step}
          aria-valuemin={0}
          aria-valuemax={TOTAL_STEPS}
          aria-valuetext={label}
        />
      </div>
    </div>
  );
}
