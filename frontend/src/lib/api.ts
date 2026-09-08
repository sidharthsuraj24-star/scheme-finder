import type { Lang, MatchRequestBody, MatchResponse, ProfileAnswers } from "./types";

const FALLBACK_API = "http://127.0.0.1:8000";

/** Accept only http(s) absolute API bases; never javascript: or relative junk. */
export function resolveApiBase(raw: string | undefined | null): string {
  const candidate = (raw || FALLBACK_API).trim().replace(/\/$/, "");
  try {
    const u = new URL(candidate);
    if (u.protocol !== "http:" && u.protocol !== "https:") {
      return FALLBACK_API;
    }
    // Block obvious userinfo / credential-in-URL footguns in public builds.
    if (u.username || u.password) {
      return FALLBACK_API;
    }
    return candidate;
  } catch {
    return FALLBACK_API;
  }
}

function baseUrl(): string {
  return resolveApiBase(process.env.NEXT_PUBLIC_API_URL);
}

/** Only render http(s) links from API/scheme data as markup hrefs. */
export function safeHttpUrl(url: string | null | undefined): string | null {
  if (!url || typeof url !== "string") return null;
  const trimmed = url.trim();
  try {
    const u = new URL(trimmed);
    if (u.protocol === "http:" || u.protocol === "https:") {
      return trimmed;
    }
  } catch {
    /* ignore */
  }
  return null;
}

export function answersToRequest(answers: ProfileAnswers, lang: Lang): MatchRequestBody {
  const occupations: string[] = [];
  if (answers.occupation) occupations.push(answers.occupation);
  // Seed PM-KISAN accepts farmer | landholding_farmer
  if (answers.occupation === "farmer" && answers.land_ownership === "yes") {
    occupations.push("landholding_farmer");
  }

  const categories = answers.categories.filter((c) => c && c !== "none");

  const land =
    answers.land_ownership === "yes"
      ? "cultivable_own"
      : answers.land_ownership === "no"
        ? "none"
        : "none";

  const disability = answers.disability === "yes";
  const disability_percent =
    disability && answers.disability_percent != null && !Number.isNaN(answers.disability_percent)
      ? answers.disability_percent
      : disability
        ? null
        : 0;

  const is_pregnant = answers.maternity === "pregnant";
  const is_lactating = answers.maternity === "lactating";

  // Clamp absurd client-side values (server also validates).
  const age = Math.min(120, Math.max(0, answers.age ?? 0));
  const monthly = Math.min(10_000_000, Math.max(0, answers.monthly_household_income ?? 0));

  return {
    profile: {
      age,
      gender: answers.gender || undefined,
      state: "Kerala",
      district: answers.district || undefined,
      marital_status: answers.marital_status || undefined,
      monthly_household_income: monthly,
      occupations,
      categories,
      disability: answers.disability === null ? undefined : disability,
      disability_percent: answers.disability === "yes" ? disability_percent : answers.disability === "no" ? 0 : undefined,
      land_ownership: land,
      is_student: answers.occupation === "student",
      is_pregnant: answers.gender === "female" ? is_pregnant : false,
      is_lactating: answers.gender === "female" ? is_lactating : false,
      primary_breadwinner_deceased: answers.primary_breadwinner_deceased === "yes",
    },
    options: {
      include_verify_uncertain: true,
      lang,
      max_results: 30,
    },
  };
}

/**
 * Backend exposes both /match and /api/v1/match (see backend/app/main.py).
 * Prefer /api/v1/match (contract); fall back to /match if needed.
 */
export async function postMatch(body: MatchRequestBody): Promise<MatchResponse> {
  const base = baseUrl();
  const paths = [`${base}/api/v1/match`, `${base}/match`];
  let lastError: Error | null = null;

  for (const url of paths) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) {
        const text = await res.text().catch(() => "");
        lastError = new Error(`HTTP ${res.status} from ${url}: ${text.slice(0, 200)}`);
        // 404 on first path → try alternate prefix
        if (res.status === 404) continue;
        throw lastError;
      }
      // Trust JSON shape only; never treat response fields as HTML markup.
      return (await res.json()) as MatchResponse;
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));
      // network error on first path → try second
      continue;
    }
  }
  throw lastError ?? new Error("Match request failed");
}
