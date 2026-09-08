import type { Lang, MatchRequestBody, MatchResponse, ProfileAnswers } from "./types";

function baseUrl(): string {
  const raw = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
  return raw.replace(/\/$/, "");
}

export function answersToRequest(answers: ProfileAnswers, lang: Lang): MatchRequestBody {
  const occupations: string[] = [];
  if (answers.occupation) occupations.push(answers.occupation);

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

  return {
    profile: {
      age: answers.age ?? 0,
      gender: answers.gender || undefined,
      state: "Kerala",
      district: answers.district || undefined,
      marital_status: answers.marital_status || undefined,
      monthly_household_income: answers.monthly_household_income ?? 0,
      occupations,
      categories,
      disability: answers.disability === null ? undefined : disability,
      disability_percent: answers.disability === "yes" ? disability_percent : answers.disability === "no" ? 0 : undefined,
      land_ownership: land,
      is_student: answers.occupation === "student",
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
      return (await res.json()) as MatchResponse;
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));
      // network error on first path → try second
      continue;
    }
  }
  throw lastError ?? new Error("Match request failed");
}
