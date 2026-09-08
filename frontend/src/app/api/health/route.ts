import { cataloguePayload, jsonWithSecurity, schemeCount } from "@/lib/matching";

export const runtime = "nodejs";

export async function GET() {
  const freshness = cataloguePayload();
  return jsonWithSecurity({
    status: "ok",
    version: "0.2.0",
    scheme_count: schemeCount(),
    catalogue: freshness.catalogue,
    is_stale: freshness.is_stale,
  });
}
