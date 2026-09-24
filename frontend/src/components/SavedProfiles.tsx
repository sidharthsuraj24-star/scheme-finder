"use client";

import { useCallback, useEffect, useState } from "react";
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

export default function SavedProfiles({ lang, answers, onLoad }: Props) {
  const [items, setItems] = useState<SavedProfile[]>([]);
  const [name, setName] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

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
    window.setTimeout(() => setMsg(null), 2500);
  };

  const onDelete = (id: string) => {
    deleteSavedProfile(id);
    refresh();
  };

  const onClear = () => {
    if (!window.confirm(t(lang, "savedClearConfirm"))) return;
    clearSavedProfiles();
    refresh();
  };

  return (
    <section
      className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
      aria-labelledby="saved-profiles-heading"
    >
      <h2 id="saved-profiles-heading" className="text-lg font-bold text-slate-900">
        {t(lang, "savedTitle")}
      </h2>
      <p className="mt-1 text-xs leading-relaxed text-slate-600">{t(lang, "savedPrivacy")}</p>

      <div className="mt-3 flex flex-col gap-2 sm:flex-row">
        <input
          type="text"
          maxLength={64}
          placeholder={t(lang, "savedNamePlaceholder")}
          className="min-h-tap flex-1 rounded-xl border-2 border-slate-300 px-3 text-sm"
          value={name}
          onChange={(e) => setName(e.target.value)}
          aria-label={t(lang, "savedNamePlaceholder")}
        />
        <button
          type="button"
          onClick={onSave}
          disabled={!answers}
          className="min-h-tap rounded-xl bg-brand-700 px-4 py-2 text-sm font-bold text-white disabled:opacity-40"
        >
          {t(lang, "savedSave")}
        </button>
      </div>
      {msg ? (
        <p className="mt-2 text-xs font-medium text-brand-800" role="status">
          {msg}
        </p>
      ) : null}

      {items.length === 0 ? (
        <p className="mt-3 text-sm text-slate-500">{t(lang, "savedEmpty")}</p>
      ) : (
        <ul className="mt-3 space-y-2">
          {items.map((p) => (
            <li
              key={p.id}
              className="flex flex-col gap-2 rounded-xl border border-slate-100 bg-slate-50 px-3 py-2 sm:flex-row sm:items-center sm:justify-between"
            >
              <div className="min-w-0">
                <p className="truncate text-sm font-semibold text-slate-900">
                  {p.name || t(lang, "savedUnnamed")}
                  {p.answers.finding_for === "child" ? (
                    <span className="ml-2 text-xs font-medium text-sky-800">
                      ({t(lang, "findingForChildShort")})
                    </span>
                  ) : null}
                </p>
                <p className="text-[11px] text-slate-500">
                  {formatSavedAt(p.saved_at)} · {p.answers.country || "—"} ·{" "}
                  {p.answers.age != null ? `${p.answers.age}y` : "—"}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  className="min-h-tap flex-1 rounded-lg border border-brand-600 px-3 py-1.5 text-xs font-bold text-brand-800 sm:flex-none"
                  onClick={() => onLoad(p.answers, p.lang)}
                >
                  {t(lang, "savedLoad")}
                </button>
                <button
                  type="button"
                  className="min-h-tap flex-1 rounded-lg border border-red-300 px-3 py-1.5 text-xs font-bold text-red-800 sm:flex-none"
                  onClick={() => onDelete(p.id)}
                >
                  {t(lang, "savedDelete")}
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
          className="mt-3 text-xs font-medium text-slate-500 underline"
        >
          {t(lang, "savedClearAll")} ({items.length}/{MAX_SAVED_PROFILES})
        </button>
      ) : null}
    </section>
  );
}
