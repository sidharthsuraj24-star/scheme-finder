import { API_CSP, STATIC_SECURITY_HEADERS } from "./src/lib/securityHeaders.mjs";

const isDev = process.env.NODE_ENV !== "production";

/** @type {import('next').NextConfig} */
const nextConfig = {
  poweredByHeader: false,
  async headers() {
    return [
      {
        source: "/:path*",
        headers: STATIC_SECURITY_HEADERS,
      },
      {
        // JSON API (incl. 404s for unknown /api paths, which skip middleware).
        source: "/api/:path*",
        headers: [{ key: "Content-Security-Policy", value: API_CSP }],
      },
      {
        // Plain-text/static well-known files never need scripts or styles.
        source: "/.well-known/:path*",
        headers: [
          { key: "Content-Security-Policy", value: API_CSP },
          { key: "Cache-Control", value: "public, max-age=3600" },
        ],
      },
    ];
  },
  // Dev-only proxy to a local FastAPI. Never shipped to production (it would
  // be an open proxy to NEXT_PUBLIC_API_URL / localhost from the edge).
  async rewrites() {
    if (!isDev) return [];
    const api = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
    return [
      {
        source: "/backend/:path*",
        destination: `${api}/:path*`,
      },
    ];
  },
};

export default nextConfig;
