"use client";

import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

interface Props {
  lang: Lang;
  onChange: (lang: Lang) => void;
}

const OPTIONS: { code: Lang; key: string }[] = [
  { code: "en", key: "langEn" },
  { code: "hi", key: "langHi" },
  { code: "ml", key: "langMl" },
];

export default function LanguageToggle({ lang, onChange }: Props) {
  return (
    <div
      className="inline-flex max-w-full flex-wrap justify-end rounded-full border-2 border-brand-700 bg-white p-1 shadow-sm"
      role="group"
      aria-label={t(lang, "langGroup")}
    >
      {OPTIONS.map(({ code, key }) => (
        <button
          key={code}
          type="button"
          // 3.1.2 Language of Parts: each option is written in its own language.
          lang={code}
          className={`min-h-tap min-w-[3.25rem] rounded-full px-2.5 text-sm font-semibold transition sm:min-w-[4.25rem] sm:px-3 sm:text-base ${
            lang === code
              ? "bg-brand-700 text-white"
              : "text-brand-800 hover:bg-brand-50"
          }`}
          aria-pressed={lang === code}
          onClick={() => onChange(code)}
        >
          {t(code, key)}
        </button>
      ))}
    </div>
  );
}
