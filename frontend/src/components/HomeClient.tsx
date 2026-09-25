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
import { postAnalyticsEvent } from "@/lib/analytics";
import type { Lang, MatchResponse, ProfileAnswers } from "@/lib/types";
import CatalogueBadge from "./CatalogueBadge";
import Disclaimer from "./Disclaimer";
import LanguageToggle from "./LanguageToggle";
import Results from "./Results";
import SavedProfiles from "./SavedProfiles";
import Wizard from "./Wizard";

const LANG_KEY = "scheme-finder-lang";

function annualFromAnswers(answers: ProfileAnswers | null): number | null {
  if (!answers) return null;
  const raw = answers.income_amount ?? answers.monthly_household_income;
  if (raw == null || Number.isNaN(raw) || raw < 0) return null;
  const mode = answers.income_mode === "monthly" ? "monthly" : "yearly";
  return mode === "yearly" ? raw : raw * 12;
}


type Phase = "wizard" | "loading" | "results" | "error";

export default function HomeClient() {
  const [lang, setLang] = useState<Lang>("en");
  const [ready, setReady] = useState(false);
  const [phase, setPhase] = useState<Phase>("wizard");
  const [result, setResult] = useState<MatchResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [lastAnswers, setLastAnswers] = useState<ProfileAnswers | null>(null);
  const [shareUrl, setShareUrl] = useState<string | null>(null);
  const [draftAnswers, setDraftAnswers] = useState<ProfileAnswers | null>(null);
  const [wizardKey, setWizardKey] = useState(0);
  /** Text for the persistent polite live region (4.1.3 Status Messages). */
  const [status, setStatus] = useState("");
  /** Element id to focus after the next render (focus management on phase change). */
  const [focusId, setFocusId] = useState<string | null>(null);
  const bootstrapped = useRef(false);
  const langRef = useRef<Lang>("en");
  langRef.current = lang;

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
      setStatus(t(language, "loading"));
      setFocusId("loading-status");
      try {
        const body = answersToRequest(answers, language);
        const data = await postMatch(body);
        setResult(data);
        setPhase("results");
        const n = (data.matched || []).length;
        setStatus(
          n > 0 ? t(langRef.current, "resultsCount", { count: n }) : t(langRef.current, "zeroTitle"),
        );
        setFocusId("results-heading");
        void postAnalyticsEvent({
          event: "match_ok",
          country: answers.country,
          scheme_ids: (data.matched || []).slice(0, 10).map((m) => m.scheme_id),
          result_count: data.count ?? (data.matched || []).length,
        });
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
        setStatus(t(langRef.current, "errorTitle"));
        setFocusId("error-heading");
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
      if (saved === "en" || saved === "ml" || saved === "hi") initialLang = saved;
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

  // 3.1.1 Language of Page: keep <html lang> in sync with the UI language so
  // screen readers switch voice (Hindi / Malayalam) and hyphenation is right.
  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  // 2.4.2 Page Titled: title reflects language + phase.
  useEffect(() => {
    const app = t(lang, "appTitle");
    const sub =
      phase === "results" && result
        ? (result.matched || []).length
          ? t(lang, "resultsTitle")
          : t(lang, "zeroTitle")
        : phase === "error"
          ? t(lang, "errorTitle")
          : phase === "loading"
            ? t(lang, "loading")
            : "";
    document.title = sub ? `${sub} · ${app}` : app;
  }, [lang, phase, result]);

  useEffect(() => {
    if (!focusId) return;
    const el = document.getElementById(focusId);
    if (el) {
      el.focus();
      setFocusId(null);
    }
  }, [focusId, phase]);

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
    setDraftAnswers(null);
    setWizardKey((k) => k + 1);
    setPhase("wizard");
    setStatus("");
    setFocusId("welcome-heading");
    replaceShareQuery(null);
  };

  /** 3.3.7 Redundant Entry: go back to the wizard with previous answers filled in. */
  const editAnswers = () => {
    if (!lastAnswers) return restart();
    setDraftAnswers(lastAnswers);
    setWizardKey((k) => k + 1);
    setPhase("wizard");
    setResult(null);
    setErrorMsg(null);
    setShareUrl(null);
    setStatus("");
    setFocusId("welcome-heading");
    replaceShareQuery(null);
  };

  const loadSaved = (answers: ProfileAnswers, savedLang: Lang) => {
    setLang(savedLang);
    try {
      localStorage.setItem(LANG_KEY, savedLang);
    } catch {
      /* ignore */
    }
    setDraftAnswers(answers);
    setWizardKey((k) => k + 1);
    setPhase("wizard");
    setResult(null);
    setErrorMsg(null);
    setShareUrl(null);
    setStatus(t(savedLang, "savedLoaded"));
    setFocusId("welcome-heading");
    replaceShareQuery(null);
  };

  if (!ready) {
    return (
      <div
        className="flex min-h-[50vh] items-center justify-center text-slate-600"
        aria-busy="true"
      >
        <span aria-hidden="true">…</span>
      </div>
    );
  }

  return (
    <>
      {/* banner landmark: title + language switch (bypassed by the skip link) */}
      <header className="flex flex-wrap items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <h1 className="text-2xl font-extrabold tracking-tight text-brand-900 sm:text-3xl">
            {t(lang, "appTitle")}
          </h1>
          <p className="mt-1 text-sm leading-snug text-slate-700 sm:text-base">
            {t(lang, "appSubtitle")}
          </p>
        </div>
        <LanguageToggle lang={lang} onChange={changeLang} />
      </header>

      {/* Persistent polite live region: loading / result count / errors / saves. */}
      <p id="sr-status" className="sr-only" role="status" aria-live="polite" aria-atomic="true">
        {status}
      </p>

      <main id="main-content" className="mt-5 space-y-5" tabIndex={-1}>
        <CatalogueBadge lang={lang} />

        {phase === "wizard" ? (
          <>
            <SavedProfiles
              lang={lang}
              answers={lastAnswers || draftAnswers}
              onLoad={loadSaved}
              onStatus={setStatus}
            />
            <Wizard
              key={wizardKey}
              lang={lang}
              onSubmit={onSubmit}
              initialAnswers={draftAnswers}
            />
          </>
        ) : null}

        {phase === "loading" ? (
          <div
            id="loading-status"
            tabIndex={-1}
            className="flex min-h-[40vh] flex-col items-center justify-center gap-4 rounded-2xl bg-white p-6 shadow-sm"
            aria-busy="true"
          >
            <div
              className="h-12 w-12 animate-spin rounded-full border-4 border-brand-200 border-t-brand-700"
              aria-hidden="true"
            />
            <p className="text-lg font-semibold text-slate-800">{t(lang, "loading")}</p>
          </div>
        ) : null}

        {phase === "error" ? (
          <div className="space-y-4 rounded-2xl border border-red-200 bg-white p-5 shadow-sm">
            <h2
              id="error-heading"
              tabIndex={-1}
              data-focus-target=""
              className="text-xl font-bold text-red-800"
            >
              {t(lang, "errorTitle")}
            </h2>
            <p className="text-sm text-slate-700">{t(lang, "errorHint")}</p>
            {errorMsg ? (
              <div>
                <p className="text-xs font-semibold text-slate-700">{t(lang, "errorDetails")}</p>
                {/* Wraps instead of scrolling (1.4.10 reflow; no unfocusable scroll region). */}
                <pre
                  lang="en"
                  className="mt-1 whitespace-pre-wrap break-words rounded-lg bg-slate-50 p-3 text-xs text-slate-700"
                >
                  {errorMsg}
                </pre>
              </div>
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
                className="min-h-tap w-full rounded-xl border-2 border-slate-500 bg-white px-4 py-3 text-base font-bold text-slate-800"
                onClick={editAnswers}
              >
                {t(lang, "changeAnswers")}
              </button>
              <button
                type="button"
                className="min-h-tap w-full rounded-xl border-2 border-slate-500 bg-white px-4 py-3 text-base font-bold text-slate-800"
                onClick={restart}
              >
                {t(lang, "startOver")}
              </button>
            </div>
          </div>
        ) : null}

        {phase === "results" && result ? (
          <>
            <Results
              lang={lang}
              data={result}
              onRestart={restart}
              onEdit={editAnswers}
              shareUrl={shareUrl}
              filteredAnnualIncome={annualFromAnswers(lastAnswers)}
              findingFor={lastAnswers?.finding_for ?? null}
              onStatus={setStatus}
            />
            <SavedProfiles
              lang={lang}
              answers={lastAnswers}
              onLoad={loadSaved}
              onStatus={setStatus}
            />
          </>
        ) : null}

        {phase === "wizard" ? <Disclaimer lang={lang} /> : null}
      </main>

      {/* contentinfo landmark — same position in every phase (3.2.3 / 3.2.6) */}
      <footer className="pt-4 text-center text-xs text-slate-700">
        {t(lang, "dataUpdatedShort")}
      </footer>
    </>
  );
}
