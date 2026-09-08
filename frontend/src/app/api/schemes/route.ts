import { jsonWithSecurity, listSchemeSummaries } from "@/lib/matching";

export const runtime = "nodejs";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const lang = url.searchParams.get("lang");
  const state = url.searchParams.get("state");
  const tag = url.searchParams.get("tag");
  const verifyParam = url.searchParams.get("verify");
  let verify: boolean | null = null;
  if (verifyParam === "true") verify = true;
  else if (verifyParam === "false") verify = false;

  if (lang && lang !== "en" && lang !== "ml") {
    return jsonWithSecurity(
      { error: { code: "bad_lang", message: "lang must be en or ml" } },
      { status: 400 },
    );
  }
  if (state && state.length > 64) {
    return jsonWithSecurity(
      { error: { code: "bad_state", message: "state too long" } },
      { status: 400 },
    );
  }
  if (tag && tag.length > 64) {
    return jsonWithSecurity(
      { error: { code: "bad_tag", message: "tag too long" } },
      { status: 400 },
    );
  }

  const schemes = listSchemeSummaries({ state, tag, verify, lang });
  return jsonWithSecurity({ count: schemes.length, schemes });
}
