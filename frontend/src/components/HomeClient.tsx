"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { answersToRequest, postMatch } from "@/lib/api";
import { t } from "@/lib/i18n";
import {
  buildShareUrl,
  decodeShareParam,
  encodeShareParam,
  replaceShareQuery,
} from "@/lib/shareProfile";
import type { Lang, MatchResponse, ProfileAnswers } from "@/lib/types";
import CatalogueBadge from "./CatalogueBadge";
import Disclaimer from "./Disclaimer";
import LanguageToggle from "./LanguageToggle";
import Results from "./Results";
import Wizard from "./Wizard";

const LANG_KEY = "scheme-finder-lang";

type Phase = "wizard" | "loading" | "results" | "error";

export default function HomeClient() {
  const [lang, setLang] = useState<Lang>("en");
  const [ready, setReady] = useState(false);
  const [phase, setPhase] = useState<Phase>("wizard");
  const [result, setResult] = useState<MatchResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [lastAnswers, setLastAnswers] = useState<ProfileAnswers | null>(null);
  const [shareUrl, setShareUrl] = useState<string | null>(null);
  const bootstrapped = useRef(false);

  const changeLang = useCallback((next: Lang) => {
    setLang(next);
    try {
      localStorage.setItem(LANG_KEY, next);
    } catch {
      /* ignore */
    }
  }, []);

  const runMatch = useCallback(
    async (answers: ProfileAnswers, language: Lang, opts?: { updateUrl?: boolean }) => {
      setPhase("loading");
      setErrorMsg(null);
      setLastAnswers(answers);
      try {
        const body = answersToRequest(answers, language);
        const data = await postMatch(body);
        setResult(data);
        setPhase("results");
        const encoded = encodeShareParam(answers, language);
        if (encoded) {
          const url = buildShareUrl(encoded);
          setShareUrl(url);
          if (opts?.updateUrl !== false) replaceShareQuery(encoded);
        } else {
          setShareUrl(null);
        }
      } catch (err) {
        setErrorMsg(err instanceof Error ? err.message : String(err));
        setPhase("error");
        setShareUrl(null);
      }
    },
    [],
  );

  useEffect(() => {
    if (bootstrapped.current) return;
    bootstrapped.current = true;

    let initialLang: Lang = "en";
    try {
      const saved = localStorage.getItem(LANG_KEY);
      if (saved === "en" || saved === "ml") initialLang = saved;
    } catch {
      /* ignore */
    }

    let shared: ReturnType<typeof decodeShareParam> = null;
    try {
      const params = new URLSearchParams(window.location.search);
      shared = decodeShareParam(params.get("p"));
    } catch {
      shared = null;
    }

    if (shared) {
      setLang(shared.lang);
      try {
        localStorage.setItem(LANG_KEY, shared.lang);
      } catch {
        /* ignore */
      }
      setReady(true);
      void runMatch(shared.answers, shared.lang, { updateUrl: true });
      return;
    }

    setLang(initialLang);
    setReady(true);
  }, [runMatch]);

  // Keep share URL in sync when user toggles language on results.
  useEffect(() => {
    if (phase !== "results" || !lastAnswers) return;
    const encoded = encodeShareParam(lastAnswers, lang);
    if (!encoded) return;
    const url = buildShareUrl(encoded);
    setShareUrl(url);
    replaceShareQuery(encoded);
  }, [lang, phase, lastAnswers]);

  const onSubmit = (answers: ProfileAnswers) => {
    void runMatch(answers, lang);
  };

  const restart = () => {
    setResult(null);
    setErrorMsg(null);
    setLastAnswers(null);
    setShareUrl(null);
    setPhase("wizard");
    replaceShareQuery(null);
  };

  if (!ready) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center text-slate-500">
        …
      </div>
    );
  }

  return (
    <main className="space-y-5">
      <header className="flex items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-extrabold tracking-tight text-brand-900 sm:text-3xl">
            {t(lang, "appTitle")}
          </h1>
          <p className="mt-1 text-sm leading-snug text-slate-600 sm:text-base">
            {t(lang, "appSubtitle")}
          </p>
        </div>
        <LanguageToggle lang={lang} onChange={changeLang} />
      </header>

      <CatalogueBadge lang={lang} />

      {phase === "wizard" ? <Wizard lang={lang} onSubmit={onSubmit} /> : null}

      {phase === "loading" ? (
        <div
          className="flex min-h-[40vh] flex-col items-center justify-center gap-4 rounded-2xl bg-white p-6 shadow-sm"
          role="status"
          aria-live="polite"
        >
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-brand-200 border-t-brand-700" />
          <p className="text-lg font-semibold text-slate-800">{t(lang, "loading")}</p>
        </div>
      ) : null}

      {phase === "error" ? (
        <div className="space-y-4 rounded-2xl border border-red-200 bg-white p-5 shadow-sm">
          <h2 className="text-xl font-bold text-red-800">{t(lang, "errorTitle")}</h2>
          <p className="text-sm text-slate-700">{t(lang, "errorHint")}</p>
          {errorMsg ? (
            <pre className="overflow-x-auto rounded-lg bg-slate-50 p-3 text-xs text-slate-600">
              {errorMsg}
            </pre>
          ) : null}
          <div className="flex flex-col gap-2">
            <button
              type="button"
              className="min-h-tap w-full rounded-xl bg-brand-700 px-4 py-3 text-base font-bold text-white"
              onClick={() => lastAnswers && void runMatch(lastAnswers, lang)}
              disabled={!lastAnswers}
            >
              {t(lang, "errorRetry")}
            </button>
            <button
              type="button"
              className="min-h-tap w-full rounded-xl border-2 border-slate-300 px-4 py-3 text-base font-bold text-slate-800"
              onClick={restart}
            >
              {t(lang, "startOver")}
            </button>
          </div>
        </div>
      ) : null}

      {phase === "results" && result ? (
        <Results
          lang={lang}
          data={result}
          onRestart={restart}
          shareUrl={shareUrl}
        />
      ) : null}

      {phase === "wizard" ? <Disclaimer lang={lang} /> : null}

      <footer className="pt-2 text-center text-[11px] text-slate-400">
        {t(lang, "dataUpdatedShort")}
      </footer>
    </main>
  );
}
