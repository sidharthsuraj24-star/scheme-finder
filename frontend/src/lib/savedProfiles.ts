/**
 * Privacy-first local saved profiles (device-only).
 * Never uploaded; see docs/PRIVACY.md and docs/PRODUCT.md.
 */
import type { Lang, ProfileAnswers } from "./types";

export const SAVED_PROFILES_KEY = "scheme-finder-saved-profiles-v1";
export const MAX_SAVED_PROFILES = 5;

export interface SavedProfile {
  id: string;
  /** Optional display name; never sent to analytics. */
  name: string;
  answers: ProfileAnswers;
  lang: Lang;
  saved_at: string; // ISO IST-ish local stamp
}

function nowIso(): string {
  try {
    return new Date().toISOString();
  } catch {
    return "1970-01-01T00:00:00.000Z";
  }
}

function newId(): string {
  try {
    if (typeof crypto !== "undefined" && crypto.randomUUID) {
      return crypto.randomUUID();
    }
  } catch {
    /* ignore */
  }
  return `p-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function readRaw(): SavedProfile[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(SAVED_PROFILES_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed)) return [];
    return parsed.filter(isSavedProfile).slice(0, MAX_SAVED_PROFILES);
  } catch {
    return [];
  }
}

function writeRaw(list: SavedProfile[]): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(SAVED_PROFILES_KEY, JSON.stringify(list.slice(0, MAX_SAVED_PROFILES)));
  } catch {
    /* quota / private mode */
  }
}

function isSavedProfile(v: unknown): v is SavedProfile {
  if (v == null || typeof v !== "object" || Array.isArray(v)) return false;
  const o = v as Record<string, unknown>;
  return (
    typeof o.id === "string" &&
    typeof o.name === "string" &&
    typeof o.lang === "string" &&
    typeof o.saved_at === "string" &&
    o.answers != null &&
    typeof o.answers === "object"
  );
}

export function listSavedProfiles(): SavedProfile[] {
  return readRaw();
}

export function saveProfile(opts: {
  answers: ProfileAnswers;
  lang: Lang;
  name?: string;
  /** Replace existing by id when updating. */
  id?: string;
}): SavedProfile | null {
  const list = readRaw();
  const name = (opts.name || "").trim().slice(0, 64);
  const entry: SavedProfile = {
    id: opts.id && list.some((p) => p.id === opts.id) ? opts.id : newId(),
    name,
    answers: opts.answers,
    lang: opts.lang === "hi" ? "hi" : opts.lang === "ml" ? "ml" : "en",
    saved_at: nowIso(),
  };
  const without = list.filter((p) => p.id !== entry.id);
  without.unshift(entry);
  writeRaw(without.slice(0, MAX_SAVED_PROFILES));
  return entry;
}

export function deleteSavedProfile(id: string): void {
  writeRaw(readRaw().filter((p) => p.id !== id));
}

export function clearSavedProfiles(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(SAVED_PROFILES_KEY);
  } catch {
    /* ignore */
  }
}
