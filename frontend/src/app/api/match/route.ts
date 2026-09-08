import {
  ValidationError,
  allowMatchRequest,
  checkContentLength,
  clientIp,
  getAllSchemes,
  jsonWithSecurity,
  matchSchemes,
  maxBodyBytes,
  rateLimitWindowSec,
  resolveMatchRequest,
} from "@/lib/matching";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const sizeErr = checkContentLength(request);
  if (sizeErr) {
    // Re-wrap with security headers
    const body = await sizeErr.json();
    return jsonWithSecurity(body, { status: sizeErr.status });
  }

  const ip = clientIp(request);
  if (!allowMatchRequest(ip)) {
    return jsonWithSecurity(
      {
        error: {
          code: "rate_limited",
          message: "Too many match requests; try again shortly.",
        },
      },
      {
        status: 429,
        headers: { "Retry-After": String(Math.floor(rateLimitWindowSec())) },
      },
    );
  }

  let rawText: string;
  try {
    rawText = await request.text();
  } catch {
    return jsonWithSecurity(
      { error: { code: "bad_body", message: "Could not read request body" } },
      { status: 400 },
    );
  }

  if (rawText.length > maxBodyBytes()) {
    return jsonWithSecurity(
      {
        error: {
          code: "payload_too_large",
          message: `Request body exceeds ${maxBodyBytes()} bytes`,
        },
      },
      { status: 413 },
    );
  }

  let parsed: unknown;
  try {
    parsed = rawText ? JSON.parse(rawText) : {};
  } catch {
    return jsonWithSecurity(
      { error: { code: "invalid_json", message: "Body must be valid JSON" } },
      { status: 400 },
    );
  }

  try {
    const { profile, options } = resolveMatchRequest(parsed);
    const result = matchSchemes(getAllSchemes(), profile, options);
    return jsonWithSecurity(result);
  } catch (err) {
    if (err instanceof ValidationError) {
      return jsonWithSecurity(
        { error: { code: err.code, message: err.message } },
        { status: 422 },
      );
    }
    console.error("match error", err);
    return jsonWithSecurity(
      { error: { code: "internal_error", message: "Match failed" } },
      { status: 500 },
    );
  }
}
