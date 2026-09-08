import { jsonWithSecurity, schemeCount } from "@/lib/matching";
import catalogueMeta from "../../../../data/catalogue_meta.json";

export const runtime = "nodejs";

export async function GET() {
  return jsonWithSecurity({
    status: "ok",
    version: "0.2.0",
    scheme_count: schemeCount(),
    catalogue: catalogueMeta,
  });
}
