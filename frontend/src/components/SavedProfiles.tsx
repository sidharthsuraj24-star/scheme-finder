"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { t } from "@/lib/i18n";
import {
  MAX_SAVED_PROFILES,
  clearSavedProfiles,
  deleteSavedProfile,
  listSavedProfiles,
  saveProfile,
  type SavedProfile,
} from "@/lib/savedProfiles";
import type { Lang, ProfileAnswers } from "@/lib/types";

interface Props {
  lang: Lang;
  /** Current wizard/results answers — enable Save when present. */
  answers: ProfileAnswers | null;
  onLoad: (answers: ProfileAnswers, lang: Lang) => void;
  /** Announce via the page live region (4.1.3). */
  onStatus?: (msg: string) => void;
}

function formatSavedAt(iso: string): string {
  try {
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleString("en-IN", { timeZone: "Asia/Kolkata", dateStyle: "medium", timeStyle: "short" });
  } catch {
    return iso;
  }
}

export default function SavedProfiles({ lang, answers, onLoad, onStatus }: Props) {
  const [items, setItems] = useState<SavedProfile[]>([]);
  const [name, setName] = useState("");
  const [msg, setMsg] = useState<string | null>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);

  const refresh = useCallback(() => {
    setItems(listSavedProfiles());
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const onSave = () => {
    if (!answers) {
      setMsg(t(lang, "savedNeedAnswers"));
      return;
    }
    const entry = saveProfile({ answers, lang, name });
    if (!entry) {
      setMsg(t(lang, "savedFailed"));
      return;
    }
    setName("");
    setMsg(t(lang, "savedOk"));
    refresh();
    window.setTimeout(() => setMsg(null), 4000);
  };

  // The activated button disappears after delete/clear, so move focus to the
  // section heading (2.4.3) and announce the outcome (4.1.3).
  const onDelete = (id: string) => {
    deleteSavedProfile(id);
    refresh();
    setMsg(t(lang, "savedDeleted"));
    onStatus?.(t(lang, "savedDeleted"));
    headingRef.current?.focus();
  };

  const onClear = () => {
    if (!window.confirm(t(lang, "savedClearConfirm"))) return;
    clearSavedProfiles();
    refresh();
    setMsg(t(lang, "savedCleared"));
    onStatus?.(t(lang, "savedCleared"));
    headingRef.current?.focus();
  };

  return (
    <section
      className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
      aria-labelledby="saved-profiles-heading"
    >
      <h2
        id="saved-profiles-heading"
        ref={headingRef}
        tabIndex={-1}
        data-focus-target=""
        className="text-lg font-bold text-slate-900"
      >
        {t(lang, "savedTitle")}
      </h2>
      <p id="saved-privacy" className="mt-1 text-xs leading-relaxed text-slate-700">
        {t(lang, "savedPrivacy")}
      </p>

      <label htmlFor="saved-profile-name" className="mt-3 block text-sm font-semibold text-slate-800">
        {t(lang, "savedNameLabel")}
      </label>
      <div className="mt-1 flex flex-col gap-2 sm:flex-row">
        <input
          id="saved-profile-name"
          type="text"
          maxLength={64}
          autoComplete="off"
          placeholder={t(lang, "savedNamePlaceholder")}
          className="min-h-tap flex-1 rounded-xl border-2 border-slate-500 bg-white px-3 text-base"
          value={name}
          onChange={(e) => setName(e.target.value)}
          aria-describedby={!answers ? "saved-need-answers" : undefined}
        />
        <button
          type="button"
          onClick={onSave}
          disabled={!answers}
          className="min-h-tap rounded-xl bg-brand-700 px-4 py-2 text-sm font-bold text-white disabled:bg-slate-500 disabled:opacity-70"
        >
          {t(lang, "savedSave")}
        </button>
      </div>
      {!answers ? (
        <p id="saved-need-answers" className="mt-1 text-xs text-slate-700">
          {t(lang, "savedNeedAnswers")}
        </p>
      ) : null}
      {/* Always-mounted live region so "Saved" is reliably announced. */}
      <p className="mt-2 min-h-[1rem] text-xs font-medium text-brand-800" role="status" aria-live="polite">
        {msg}
      </p>

      {items.length === 0 ? (
        <p className="mt-1 text-sm text-slate-700">{t(lang, "savedEmpty")}</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {items.map((p) => (
            <li
              key={p.id}
              className="flex flex-col gap-2 rounded-xl border border-slate-100 bg-slate-50 px-3 py-2 sm:flex-row sm:items-center sm:justify-between"
            >
              <div className="min-w-0">
                <p className="break-words text-sm font-semibold text-slate-900">
                  {p.name || t(lang, "savedUnnamed")}
                  {p.answers.finding_for === "child" ? (
                    <span className="ml-2 text-xs font-medium text-sky-900">
                      ({t(lang, "findingForChildShort")})
                    </span>
                  ) : null}
                </p>
                <p className="text-xs text-slate-700">
                  {formatSavedAt(p.saved_at)} · {p.answers.country || "—"} ·{" "}
                  {p.answers.age != null ? `${p.answers.age}y` : "—"}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  className="min-h-tap flex-1 rounded-lg border-2 border-brand-700 bg-white px-3 py-1.5 text-sm font-bold text-brand-800 sm:flex-none"
                  onClick={() => onLoad(p.answers, p.lang)}
                >
                  {t(lang, "savedLoad")}
                  <span className="sr-only">: {p.name || t(lang, "savedUnnamed")}</span>
                </button>
                <button
                  type="button"
                  className="min-h-tap flex-1 rounded-lg border-2 border-red-700 bg-white px-3 py-1.5 text-sm font-bold text-red-800 sm:flex-none"
                  onClick={() => onDelete(p.id)}
                >
                  {t(lang, "savedDelete")}
                  <span className="sr-only">: {p.name || t(lang, "savedUnnamed")}</span>
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {items.length > 0 ? (
        <button
          type="button"
          onClick={onClear}
          className="mt-3 inline-flex min-h-[44px] items-center px-1 text-sm font-medium text-slate-700 underline"
        >
          {t(lang, "savedClearAll")} ({items.length}/{MAX_SAVED_PROFILES})
        </button>
      ) : null}
    </section>
  );
}
