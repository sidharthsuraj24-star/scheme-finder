import {
  CATEGORIES,
  GENDERS,
  KERALA_DISTRICTS,
  MARITAL_STATUSES,
  OCCUPATIONS,
} from "./constants";
import type { Lang, ProfileAnswers } from "./types";

/** Compact v1 payload stored in ?p= (base64url JSON). */
export interface SharePayloadV1 {
  v: 1;
  l: Lang;
  a: number;
  i: number;
  o: string;
  c: string[];
  lo: "yes" | "no";
  d: "yes" | "no";
  dp: number | null;
  di: string;
  g: string;
  m: string;
  mat: "pregnant" | "lactating" | "neither" | null;
  bw: "yes" | "no";
}

const MAX_PARAM_CHARS = 2048;
const MAX_DECODED_CHARS = 1536;
const OCC_SET = new Set<string>(OCCUPATIONS);
const CAT_SET = new Set<string>(CATEGORIES);
const DIST_SET = new Set<string>(KERALA_DISTRICTS);
const GEN_SET = new Set<string>(GENDERS);
const MAR_SET = new Set<string>(MARITAL_STATUSES);
const MAT_SET = new Set(["pregnant", "lactating", "neither"]);

function bytesToBase64Url(bytes: Uint8Array): string {
  let bin = "";
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]!);
  const b64 =
    typeof btoa === "function"
      ? btoa(bin)
      : Buffer.from(bytes).toString("base64");
  return b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
}

function base64UrlToBytes(s: string): Uint8Array | null {
  try {
    const pad = s.length % 4 === 0 ? "" : "=".repeat(4 - (s.length % 4));
    const b64 = s.replace(/-/g, "+").replace(/_/g, "/") + pad;
    if (typeof atob === "function") {
      const bin = atob(b64);
      const out = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
      return out;
    }
    return new Uint8Array(Buffer.from(b64, "base64"));
  } catch {
    return null;
  }
}

function isIntInRange(n: unknown, min: number, max: number): n is number {
  return typeof n === "number" && Number.isFinite(n) && Number.isInteger(n) && n >= min && n <= max;
}

function isNumInRange(n: unknown, min: number, max: number): n is number {
  return typeof n === "number" && Number.isFinite(n) && n >= min && n <= max;
}

export function answersToSharePayload(
  answers: ProfileAnswers,
  lang: Lang,
): SharePayloadV1 | null {
  if (
    answers.age == null ||
    answers.monthly_household_income == null ||
    !answers.occupation ||
    !answers.categories.length ||
    (answers.land_ownership !== "yes" && answers.land_ownership !== "no") ||
    (answers.disability !== "yes" && answers.disability !== "no") ||
    !answers.district ||
    !answers.gender ||
    !answers.marital_status ||
    (answers.primary_breadwinner_deceased !== "yes" &&
      answers.primary_breadwinner_deceased !== "no")
  ) {
    return null;
  }
  if (answers.gender === "female" && answers.maternity == null) return null;

  return {
    v: 1,
    l: lang === "ml" ? "ml" : "en",
    a: Math.min(120, Math.max(0, Math.floor(answers.age))),
    i: Math.min(10_000_000, Math.max(0, Math.floor(answers.monthly_household_income))),
    o: answers.occupation,
    c: answers.categories.slice(0, 8),
    lo: answers.land_ownership,
    d: answers.disability,
    dp:
      answers.disability === "yes" && answers.disability_percent != null
        ? Math.min(100, Math.max(0, Math.floor(answers.disability_percent)))
        : null,
    di: answers.district,
    g: answers.gender,
    m: answers.marital_status,
    mat: answers.gender === "female" ? answers.maternity : null,
    bw: answers.primary_breadwinner_deceased,
  };
}

export function sharePayloadToAnswers(p: SharePayloadV1): ProfileAnswers {
  return {
    age: p.a,
    monthly_household_income: p.i,
    occupation: p.o,
    categories: [...p.c],
    land_ownership: p.lo,
    disability: p.d,
    disability_percent: p.d === "yes" ? p.dp : null,
    district: p.di,
    gender: p.g,
    marital_status: p.m,
    maternity: p.g === "female" ? p.mat : null,
    primary_breadwinner_deceased: p.bw,
  };
}

function validatePayload(raw: unknown): SharePayloadV1 | null {
  if (raw == null || typeof raw !== "object" || Array.isArray(raw)) return null;
  const o = raw as Record<string, unknown>;
  if (o.v !== 1) return null;
  if (o.l !== "en" && o.l !== "ml") return null;
  if (!isIntInRange(o.a, 0, 120)) return null;
  if (!isNumInRange(o.i, 0, 10_000_000)) return null;
  if (typeof o.o !== "string" || !OCC_SET.has(o.o)) return null;
  if (!Array.isArray(o.c) || o.c.length < 1 || o.c.length > 8) return null;
  for (const c of o.c) {
    if (typeof c !== "string" || c.length > 32 || !CAT_SET.has(c)) return null;
  }
  if (o.lo !== "yes" && o.lo !== "no") return null;
  if (o.d !== "yes" && o.d !== "no") return null;
  let dp: number | null = null;
  if (o.dp != null) {
    if (!isIntInRange(o.dp, 0, 100)) return null;
    dp = o.dp;
  }
  if (typeof o.di !== "string" || !DIST_SET.has(o.di)) return null;
  if (typeof o.g !== "string" || !GEN_SET.has(o.g)) return null;
  if (typeof o.m !== "string" || !MAR_SET.has(o.m)) return null;
  let mat: SharePayloadV1["mat"] = null;
  if (o.g === "female") {
    if (o.mat == null || typeof o.mat !== "string" || !MAT_SET.has(o.mat)) return null;
    mat = o.mat as SharePayloadV1["mat"];
  } else if (o.mat != null) {
    return null;
  }
  if (o.bw !== "yes" && o.bw !== "no") return null;

  return {
    v: 1,
    l: o.l,
    a: o.a,
    i: Math.floor(o.i),
    o: o.o,
    c: o.c as string[],
    lo: o.lo,
    d: o.d,
    dp: o.d === "yes" ? dp : null,
    di: o.di,
    g: o.g,
    m: o.m,
    mat,
    bw: o.bw,
  };
}

/** Encode completed answers + lang into a base64url `p` value. */
export function encodeShareParam(answers: ProfileAnswers, lang: Lang): string | null {
  const payload = answersToSharePayload(answers, lang);
  if (!payload) return null;
  const json = JSON.stringify(payload);
  if (json.length > MAX_DECODED_CHARS) return null;
  const bytes = new TextEncoder().encode(json);
  const encoded = bytesToBase64Url(bytes);
  if (encoded.length > MAX_PARAM_CHARS) return null;
  return encoded;
}

/** Decode + validate `p`. Rejects huge / malicious / incomplete payloads. */
export function decodeShareParam(
  param: string | null | undefined,
): { answers: ProfileAnswers; lang: Lang } | null {
  if (!param || typeof param !== "string") return null;
  if (param.length > MAX_PARAM_CHARS) return null;
  if (!/^[A-Za-z0-9_-]+$/.test(param)) return null;
  const bytes = base64UrlToBytes(param);
  if (!bytes || bytes.length > MAX_DECODED_CHARS) return null;
  let text: string;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    return null;
  }
  if (text.length > MAX_DECODED_CHARS) return null;
  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch {
    return null;
  }
  const payload = validatePayload(parsed);
  if (!payload) return null;
  return { answers: sharePayloadToAnswers(payload), lang: payload.l };
}

/** Share URL for current origin + path + ?p=… */
export function buildShareUrl(encodedP: string): string {
  if (typeof window === "undefined") return `?p=${encodedP}`;
  const path = window.location.pathname || "/";
  return `${window.location.origin}${path}?p=${encodedP}`;
}

export function replaceShareQuery(encodedP: string | null): void {
  if (typeof window === "undefined") return;
  try {
    const url = new URL(window.location.href);
    if (encodedP) url.searchParams.set("p", encodedP);
    else url.searchParams.delete("p");
    window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
  } catch {
    /* ignore */
  }
}
