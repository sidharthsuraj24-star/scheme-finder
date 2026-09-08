/** Catalogue freshness helpers shared by health + match APIs. */

import catalogueMetaJson from "../../../data/catalogue_meta.json";

export interface CatalogueMeta {
  updated_as_of: string;
  updated_as_of_iso?: string;
  scheme_count?: number;
  scope?: string;
  auto_update?: string;
  stale_after_days: number;
  disclaimer: string;
}

export const catalogueMeta = catalogueMetaJson as CatalogueMeta;

/** Days between updated_as_of (date-only) and today (UTC calendar date). */
export function daysSinceUpdated(asOf: string, today = new Date()): number {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(asOf.trim());
  if (!m) return Number.POSITIVE_INFINITY;
  const updated = Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3]));
  const now = Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate());
  return Math.floor((now - updated) / 86_400_000);
}

export function isCatalogueStale(
  meta: CatalogueMeta = catalogueMeta,
  today = new Date(),
): boolean {
  const days = daysSinceUpdated(meta.updated_as_of, today);
  const limit = meta.stale_after_days ?? 30;
  return days > limit;
}

export function cataloguePayload(today = new Date()) {
  return {
    catalogue: catalogueMeta,
    is_stale: isCatalogueStale(catalogueMeta, today),
  };
}

/** Resolve last_verified for a scheme, defaulting to catalogue stamp. */
export function resolveLastVerified(scheme: { last_verified?: unknown }): string | null {
  const v = scheme.last_verified;
  if (typeof v === "string" && v.trim()) return v.trim();
  return catalogueMeta.updated_as_of || null;
}
