/** Client helper for privacy-preserving aggregate events (no profile PII). */

export type AnalyticsEventName = "match_ok" | "match_error" | "share_copy" | "ops_view";

export async function postAnalyticsEvent(payload: {
  event: AnalyticsEventName;
  country?: string | null;
  scheme_ids?: string[];
  result_count?: number;
  result_count_bucket?: string;
}): Promise<void> {
  try {
    await fetch("/api/analytics/event", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({
        event: payload.event,
        country: payload.country || undefined,
        scheme_ids: (payload.scheme_ids || []).slice(0, 10),
        result_count: payload.result_count,
        result_count_bucket: payload.result_count_bucket,
      }),
      keepalive: true,
    });
  } catch {
    /* fail open */
  }
}
