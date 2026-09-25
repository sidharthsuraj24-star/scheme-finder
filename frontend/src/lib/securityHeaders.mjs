/**
 * Shared security header definitions (imported by next.config.mjs and
 * src/middleware.ts, and asserted by e2e/security-headers.spec.ts).
 * Plain .mjs so next.config can import it without a TS loader.
 */

/** Static headers applied to every response (pages, API, static assets). */
export const STATIC_SECURITY_HEADERS = [
  // 2 years + subdomains + preload (matches Vercel's default for *.vercel.app).
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  // Share URLs carry an encoded profile (?p=…) — never leak it via Referer.
  { key: "Referrer-Policy", value: "no-referrer" },
  {
    key: "Permissions-Policy",
    value: [
      "accelerometer=()",
      "autoplay=()",
      "browsing-topics=()",
      "camera=()",
      "display-capture=()",
      "geolocation=()",
      "gyroscope=()",
      "magnetometer=()",
      "microphone=()",
      "midi=()",
      "payment=()",
      "publickey-credentials-get=()",
      "usb=()",
      "xr-spatial-tracking=()",
      "clipboard-write=(self)",
    ].join(", "),
  },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
  { key: "Cross-Origin-Resource-Policy", value: "same-origin" },
  { key: "X-DNS-Prefetch-Control", value: "off" },
  { key: "X-Permitted-Cross-Domain-Policies", value: "none" },
];

/** Origin of a dedicated API (NEXT_PUBLIC_API_URL) for connect-src, if any. */
export function apiOrigin(raw = process.env.NEXT_PUBLIC_API_URL) {
  const v = (raw || "").trim();
  if (!v) return null;
  try {
    const u = new URL(v);
    if (u.protocol !== "https:" && u.protocol !== "http:") return null;
    return u.origin;
  } catch {
    return null;
  }
}

/**
 * Strict nonce-based CSP for HTML pages.
 * - script-src: per-request nonce + 'strict-dynamic' (no 'unsafe-inline' /
 *   'unsafe-eval' in production). Next.js stamps the nonce on its own scripts.
 * - style-src: 'self' + the same nonce, no 'unsafe-inline' in production.
 *   CSS ships as <link> files; React `style={{…}}` props are applied through
 *   the CSSOM after hydration, which CSP does not block. `next dev` keeps
 *   'unsafe-inline' because HMR injects <style> tags.
 */
export function buildPageCsp(nonce, { dev = false, api = apiOrigin() } = {}) {
  const connect = ["'self'"];
  if (api) connect.push(api);
  if (dev) connect.push("ws:", "wss:"); // HMR
  const script = [`'self'`, `'nonce-${nonce}'`, "'strict-dynamic'"];
  if (dev) script.push("'unsafe-eval'"); // React Refresh in `next dev` only
  const style = dev ? ["'self'", "'unsafe-inline'"] : ["'self'", `'nonce-${nonce}'`];
  const directives = [
    "default-src 'self'",
    `script-src ${script.join(" ")}`,
    `style-src ${style.join(" ")}`,
    "img-src 'self' data: blob:",
    "font-src 'self'",
    `connect-src ${connect.join(" ")}`,
    "manifest-src 'self'",
    "worker-src 'self'",
    "object-src 'none'",
    "base-uri 'none'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "frame-src 'none'",
  ];
  if (!dev) directives.push("upgrade-insecure-requests");
  return directives.join("; ");
}

/** CSP for JSON API responses (nothing may load from them). */
export const API_CSP = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'";
