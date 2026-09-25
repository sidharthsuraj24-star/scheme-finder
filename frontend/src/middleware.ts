import { NextResponse, type NextRequest } from "next/server";
import { buildPageCsp } from "./lib/securityHeaders.mjs";

/**
 * Per-request CSP nonce for HTML pages. Next.js reads the nonce from the
 * request's Content-Security-Policy header and applies it to the framework's
 * inline + external scripts (requires dynamic rendering; see app/layout.tsx).
 */
export function middleware(request: NextRequest) {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  const nonce = btoa(String.fromCharCode(...bytes));
  const csp = buildPageCsp(nonce, { dev: process.env.NODE_ENV !== "production" });

  const requestHeaders = new Headers(request.headers);
  requestHeaders.set("x-nonce", nonce);
  requestHeaders.set("Content-Security-Policy", csp);

  const response = NextResponse.next({ request: { headers: requestHeaders } });
  response.headers.set("Content-Security-Policy", csp);
  return response;
}

export const config = {
  matcher: [
    {
      // Pages only: skip API routes (strict JSON CSP set by the handlers and
      // next.config for unknown /api paths), static assets, and well-known files.
      source: "/((?!api/|_next/static|_next/image|\\.well-known/).*)",
      missing: [
        { type: "header", key: "next-router-prefetch" },
        { type: "header", key: "purpose", value: "prefetch" },
      ],
    },
  ],
};
