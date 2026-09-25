"use client";

import { useEffect, useState } from "react";
import { t } from "@/lib/i18n";
import type { Lang } from "@/lib/types";

/**
 * Skip link localised to the current document language. HomeClient sets
 * <html lang>; we observe it so the skip link text (and its own lang) follow
 * the EN / HI / ML switch without prop-drilling through the root layout.
 */
function readLang(): Lang {
  if (typeof document === "undefined") return "en";
  const l = document.documentElement.lang;
  return l === "hi" || l === "ml" ? l : "en";
}

export default function SkipLink() {
  const [lang, setLang] = useState<Lang>("en");

  useEffect(() => {
    setLang(readLang());
    const obs = new MutationObserver(() => setLang(readLang()));
    obs.observe(document.documentElement, { attributes: true, attributeFilter: ["lang"] });
    return () => obs.disconnect();
  }, []);

  return (
    <a href="#main-content" className="skip-link" lang={lang}>
      {t(lang, "skipToContent")}
    </a>
  );
}
