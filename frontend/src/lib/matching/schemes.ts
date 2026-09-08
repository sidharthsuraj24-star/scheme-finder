/** Load curated schemes from frontend/data/schemes.json */

import schemesJson from "../../../data/schemes.json";
import type { SchemeRecord, SchemeSummary } from "./types";

const schemes = schemesJson as SchemeRecord[];

export function getAllSchemes(): SchemeRecord[] {
  return schemes;
}

export function getSchemeById(id: string): SchemeRecord | undefined {
  return schemes.find((s) => s.id === id);
}

export function listSchemeSummaries(opts?: {
  state?: string | null;
  tag?: string | null;
  verify?: boolean | null;
  lang?: string | null;
}): SchemeSummary[] {
  const { state, tag, verify, lang } = opts || {};
  let list = schemes;

  if (state) {
    const needle = state.trim().toLowerCase();
    list = list.filter((s) => {
      const states = ((s.eligibility_rules || {}) as { states?: string[] }).states || [];
      return states.some(
        (st) => st.toLowerCase() === needle || st.toLowerCase() === "india",
      );
    });
  }
  if (tag) {
    const needle = tag.trim().toLowerCase();
    list = list.filter((s) => (s.tags || []).some((t) => t.toLowerCase() === needle));
  }
  if (verify != null) {
    list = list.filter(
      (s) => Boolean(((s.eligibility_rules || {}) as { verify?: boolean }).verify) === verify,
    );
  }

  return list.map((s) => {
    const name = { ...(s.scheme_name || {}) };
    if (lang === "ml" && name.ml) {
      /* keep both */
    } else if (lang === "en" && name.en) {
      /* keep both */
    }
    return {
      id: s.id,
      scheme_name: name,
      tags: s.tags || [],
      official_source_url: s.official_source_url ?? null,
      verify: Boolean(((s.eligibility_rules || {}) as { verify?: boolean }).verify),
    };
  });
}

export function schemeCount(): number {
  return schemes.length;
}
