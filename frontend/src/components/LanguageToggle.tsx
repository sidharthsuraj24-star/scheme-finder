"use client";

import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

interface Props {
  lang: Lang;
  onChange: (lang: Lang) => void;
}

export default function LanguageToggle({ lang, onChange }: Props) {
  return (
    <div
      className="inline-flex rounded-full border-2 border-brand-700 bg-white p-1 shadow-sm"
      role="group"
      aria-label="Language"
    >
      <button
        type="button"
        className={`min-h-tap min-w-[4.5rem] rounded-full px-3 text-base font-semibold transition ${
          lang === "en"
            ? "bg-brand-700 text-white"
            : "text-brand-800 hover:bg-brand-50"
        }`}
        aria-pressed={lang === "en"}
        onClick={() => onChange("en")}
      >
        {t(lang, "langEn")}
      </button>
      <button
        type="button"
        className={`min-h-tap min-w-[4.5rem] rounded-full px-3 text-base font-semibold transition ${
          lang === "ml"
            ? "bg-brand-700 text-white"
            : "text-brand-800 hover:bg-brand-50"
        }`}
        aria-pressed={lang === "ml"}
        onClick={() => onChange("ml")}
      >
        {t(lang, "langMl")}
      </button>
    </div>
  );
}
