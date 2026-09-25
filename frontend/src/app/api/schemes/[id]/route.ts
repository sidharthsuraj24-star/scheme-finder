import { getSchemeById, jsonWithSecurity } from "@/lib/matching";

export const runtime = "nodejs";

/** Catalogue ids are lowercase slugs; reject anything else before lookup. */
const SCHEME_ID_RE = /^[a-z0-9][a-z0-9_-]{0,127}$/;

export async function GET(
  _request: Request,
  context: { params: Promise<{ id: string }> },
) {
  const { id } = await context.params;
  if (!id || !SCHEME_ID_RE.test(id)) {
    return jsonWithSecurity(
      { error: { code: "invalid_scheme_id", message: "Invalid scheme id" } },
      { status: 400 },
    );
  }
  const scheme = getSchemeById(id);
  if (!scheme) {
    return jsonWithSecurity(
      { error: { code: "scheme_not_found", message: "Unknown scheme id" } },
      { status: 404 },
    );
  }
  return jsonWithSecurity(scheme);
}
