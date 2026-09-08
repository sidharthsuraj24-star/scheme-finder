import { getSchemeById, jsonWithSecurity } from "@/lib/matching";

export const runtime = "nodejs";

export async function GET(
  _request: Request,
  context: { params: Promise<{ id: string }> },
) {
  const { id } = await context.params;
  if (!id || id.length > 128) {
    return jsonWithSecurity(
      { error: { code: "invalid_scheme_id", message: "scheme_id too long" } },
      { status: 400 },
    );
  }
  const scheme = getSchemeById(id);
  if (!scheme) {
    return jsonWithSecurity(
      { error: { code: "scheme_not_found", message: `Unknown scheme id: ${id}` } },
      { status: 404 },
    );
  }
  return jsonWithSecurity(scheme);
}
