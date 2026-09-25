import { expect, test, type APIResponse, type Page } from "@playwright/test";
import { bootApp, completeWizard } from "./helpers";

/**
 * Security regression suite (Phase 2 free security pass, 2026-09-25).
 *
 *   npm run build && npm run test:security
 *
 * - Response headers on pages, API, static assets and well-known files.
 * - Strict nonce-based CSP with zero violations across the real user flows
 *   (wizard → results, share link copy + reopen, WhatsApp link, analytics
 *   POST, language switch, saved profiles, /ops).
 * - API hardening: body caps (incl. chunked), validation, no echoed input,
 *   generic ops 401, constant-time token gate, rate limiting.
 *
 * Ops-token checks run against a second server (OPS_TEST_BASE_URL, default
 * :3101) started with OPS_DASHBOARD_TOKEN=test-ops-token.
 */

const OPS_BASE = process.env.OPS_TEST_BASE_URL || "http://127.0.0.1:3101";
const OPS_TOKEN = process.env.OPS_TEST_TOKEN || "test-ops-token";

const COMMON: Record<string, RegExp> = {
  "strict-transport-security": /^max-age=63072000; includeSubDomains; preload$/,
  "x-content-type-options": /^nosniff$/,
  "referrer-policy": /^no-referrer$/,
  "permissions-policy": /^(?=.*\bcamera=\(\))(?=.*\bmicrophone=\(\))(?=.*\bgeolocation=\(\))/,
  "x-frame-options": /^DENY$/,
  "cross-origin-opener-policy": /^same-origin$/,
};

function expectCommon(res: APIResponse, what: string) {
  const h = res.headers();
  for (const [k, re] of Object.entries(COMMON)) {
    expect(h[k], `${what}: ${k}`).toMatch(re);
  }
  expect(h["x-powered-by"], `${what}: x-powered-by must not leak`).toBeUndefined();
}

function cspDirectives(csp: string): Map<string, string[]> {
  const m = new Map<string, string[]>();
  for (const part of csp.split(";")) {
    const [name, ...vals] = part.trim().split(/\s+/);
    if (name) m.set(name, vals);
  }
  return m;
}

test.describe("security headers", () => {
  test.beforeEach(({}, info) => {
    test.skip(info.project.name !== "desktop", "header checks are viewport-independent");
  });

  test("HTML pages: full header set + strict per-request nonce CSP", async ({ request }) => {
    const nonces: string[] = [];
    for (const path of ["/", "/ops", "/?p=bogus", "/this-page-does-not-exist"]) {
      const res = await request.get(path);
      expectCommon(res, path);
      const csp = res.headers()["content-security-policy"];
      expect(csp, `${path}: CSP`).toBeTruthy();
      const d = cspDirectives(csp);
      const script = d.get("script-src") || [];
      expect(script, `${path}: script-src`).toContain("'strict-dynamic'");
      expect(script.join(" "), `${path}: no unsafe-inline/eval scripts`).not.toMatch(
        /'unsafe-inline'|'unsafe-eval'/,
      );
      expect((d.get("style-src") || []).join(" "), `${path}: no unsafe-inline styles`).not.toContain(
        "'unsafe-inline'",
      );
      const nonce = script.find((s) => s.startsWith("'nonce-"));
      expect(nonce, `${path}: nonce`).toBeTruthy();
      nonces.push(nonce!);
      expect(d.get("frame-ancestors")).toEqual(["'none'"]);
      expect(d.get("object-src")).toEqual(["'none'"]);
      expect(d.get("base-uri")).toEqual(["'none'"]);
      expect(d.get("form-action")).toEqual(["'self'"]);
      expect(d.get("default-src")).toEqual(["'self'"]);
      // Every <script> tag in the document carries the nonce.
      if (res.headers()["content-type"]?.includes("text/html")) {
        const html = await res.text();
        const raw = nonce!.slice("'nonce-".length, -1);
        const tags = html.match(/<script\b[^>]*>/g) || [];
        expect(tags.length).toBeGreaterThan(0);
        for (const tag of tags) expect(tag, `${path}: script without nonce`).toContain(`nonce="${raw}"`);
      }
    }
    expect(new Set(nonces).size, "nonce must be unique per request").toBe(nonces.length);
  });

  test("API routes: strict JSON CSP, no-store, same header set", async ({ request }) => {
    for (const path of ["/api/health", "/api/schemes", "/api/ops/summary"]) {
      const res = await request.get(path);
      expectCommon(res, path);
      const h = res.headers();
      expect(h["content-security-policy"]).toContain("default-src 'none'");
      expect(h["cache-control"], `${path}: cache-control`).toBe("no-store");
      expect(h["content-type"]).toContain("application/json");
    }
  });

  test("static assets and security.txt", async ({ request }) => {
    const html = await (await request.get("/")).text();
    const asset = html.match(/\/_next\/static\/[^"']+\.js/)?.[0];
    expect(asset).toBeTruthy();
    const a = await request.get(asset!);
    expect(a.status()).toBe(200);
    expectCommon(a, asset!);

    const s = await request.get("/.well-known/security.txt");
    expect(s.status()).toBe(200);
    expectCommon(s, "security.txt");
    const body = await s.text();
    expect(body).toMatch(
      /^Contact: https:\/\/github\.com\/sidharthsuraj24-star\/scheme-finder\/security\/advisories\/new$/m,
    );
    const exp = body.match(/^Expires: (.+)$/m)?.[1];
    expect(exp && Date.parse(exp) > Date.now(), "security.txt Expires in the future").toBeTruthy();
    expect(body, "no invented email contacts").not.toMatch(/Contact: mailto:/);
  });
});

async function trackCsp(page: Page): Promise<string[]> {
  const violations: string[] = [];
  page.on("console", (msg) => {
    const t = msg.text();
    if (/Content Security Policy/i.test(t)) violations.push(`console: ${t}`);
  });
  await page.addInitScript(() => {
    document.addEventListener("securitypolicyviolation", (e) => {
      const w = window as unknown as { __csp?: string[] };
      (w.__csp ||= []).push(`${e.violatedDirective} ${e.blockedURI} ${e.sourceFile}:${e.lineNumber}`);
    });
  });
  return violations;
}

async function pageViolations(page: Page): Promise<string[]> {
  return page.evaluate(() => (window as unknown as { __csp?: string[] }).__csp || []);
}

test.describe("CSP does not break the app", () => {
  test("wizard → results, analytics POST, share link, WhatsApp, i18n, saved profiles", async ({
    page,
    context,
  }) => {
    const console = await trackCsp(page);
    await context.grantPermissions(["clipboard-read", "clipboard-write"]);
    await bootApp(page, "en");
    const analytics = page.waitForResponse(
      (r) => r.url().includes("/api/analytics/event") && r.request().method() === "POST",
    );
    await completeWizard(page);
    await page.locator("article.scheme-card").first().waitFor({ timeout: 30_000 });
    expect((await analytics).status(), "analytics POST accepted").toBe(200);

    // Share link lands in the URL (?p=) and the copy button works.
    await expect(page).toHaveURL(/[?&]p=/);
    const shareUrl = page.url();
    const copyBtn = page.getByRole("button", { name: /copy link/i }).first();
    await copyBtn.click();
    await expect(page.getByRole("button", { name: /copied/i }).first()).toBeVisible();

    const wa = page.locator('a[href^="https://wa.me/"]').first();
    await expect(wa).toHaveAttribute("href", /https:\/\/wa\.me\/\?text=.*p%3D/);
    await expect(wa).toHaveAttribute("rel", /noopener/);

    // Language switch re-renders translated UI.
    const group = page.locator("header [role=group], main [role=group]").first();
    await group.locator("button").nth(1).click();
    await expect(page.locator("html")).toHaveAttribute("lang", "hi");
    await group.locator("button").nth(0).click();
    await expect(page.locator("html")).toHaveAttribute("lang", "en");

    // Saved profiles (localStorage) still work.
    const name = page.locator("#saved-profile-name");
    if (await name.count()) {
      await name.fill("CSP test");
      await name.locator("xpath=following-sibling::button[1]").click();
      await expect(page.getByText("CSP test").first()).toBeVisible();
    }

    // Opening the share link in a fresh page restores the results.
    const p2 = await context.newPage();
    const console2 = await trackCsp(p2);
    await p2.goto(shareUrl);
    await p2.locator("article.scheme-card").first().waitFor({ timeout: 30_000 });

    expect([...console, ...(await pageViolations(page))], "CSP violations (main)").toEqual([]);
    expect([...console2, ...(await pageViolations(p2))], "CSP violations (share)").toEqual([]);
  });

  test("/ops renders under CSP", async ({ page }) => {
    const console = await trackCsp(page);
    await page.goto("/ops");
    await expect(page.locator("main")).toBeVisible();
    await expect(page.getByText(/scheme/i).first()).toBeVisible();
    // Token field has no name → a native (pre-hydration) submit can never put it in the URL.
    await expect(page.locator("#ops-token")).not.toHaveAttribute("name", /.*/);
    await page.locator("#ops-token").fill("abc");
    await page.locator("#ops-token").press("Enter");
    await page.waitForTimeout(500);
    expect(page.url()).not.toContain("abc");
    expect([...console, ...(await pageViolations(page))]).toEqual([]);
  });
});

test.describe("API hardening", () => {
  test.beforeEach(({}, info) => {
    test.skip(info.project.name !== "desktop", "API checks are viewport-independent");
  });

  test("match: Content-Length cap, chunked cap, invalid JSON is generic", async ({ request, baseURL }) => {
    const big = JSON.stringify({ profile: { occupation: "x".repeat(70 * 1024) } });
    const r = await request.post("/api/match", {
      data: big,
      headers: { "content-type": "application/json" },
    });
    expect(r.status()).toBe(413);

    // Chunked (no Content-Length): the streaming reader must still cap it.
    const chunk = new TextEncoder().encode("x".repeat(16 * 1024));
    let sent = 0;
    const stream = new ReadableStream<Uint8Array>({
      pull(ctrl) {
        if (sent >= 8) return ctrl.close();
        sent += 1;
        ctrl.enqueue(chunk);
      },
    });
    const chunked = await fetch(`${baseURL}/api/match`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: stream,
      // @ts-expect-error Node fetch streaming option
      duplex: "half",
    });
    expect(chunked.status).toBe(413);

    const bad = await fetch(`${baseURL}/api/match`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: "{not json",
    });
    expect(bad.status).toBe(400);
    const txt = await bad.text();
    expect(txt).not.toMatch(/at \w+ \(|node_modules|SyntaxError|\/workspace\//);
  });

  test("schemes/[id]: validated, 404 does not echo input", async ({ request }) => {
    const probe = "zz-not-a-real-scheme-12345";
    const nf = await request.get(`/api/schemes/${probe}`);
    expect(nf.status()).toBe(404);
    expect(await nf.text()).not.toContain(probe);
    const bad = await request.get(`/api/schemes/${encodeURIComponent("<script>alert(1)</script>")}`);
    expect(bad.status()).toBe(400);
    expect(await bad.text()).not.toContain("<script>");
  });

  test("analytics: validation, size cap, sanitised fields", async ({ request }) => {
    const ok = await request.post("/api/analytics/event", {
      data: { event: "share_copy", country: "India", scheme_ids: ["pm-kisan", "<bad id>"] },
    });
    expect(ok.status()).toBe(200);
    const badEvt = await request.post("/api/analytics/event", { data: { event: "steal_profile" } });
    expect(badEvt.status()).toBe(400);
    const big = await request.post("/api/analytics/event", {
      data: { event: "match_ok", pad: "x".repeat(8 * 1024) },
    });
    expect(big.status()).toBe(413);
    const arr = await request.post("/api/analytics/event", { data: [1, 2, 3] });
    expect(arr.status()).toBe(400);
  });

  test("ops (demo gate open): 200 without token", async ({ request }) => {
    const r = await request.get("/api/ops/summary");
    expect(r.status()).toBe(200);
  });

  test("ops token gate: header-only, constant-time, generic 401, rate limited", async ({ playwright }) => {
    const api = await playwright.request.newContext({ baseURL: OPS_BASE });
    const health = await api.get("/api/health").catch(() => null);
    test.skip(!health || !health.ok(), `ops-token server not running at ${OPS_BASE}`);

    const none = await api.get("/api/ops/summary");
    expect(none.status()).toBe(401);
    const body = await none.text();
    expect(body).not.toMatch(/OPS_DASHBOARD_TOKEN|NEXT_PUBLIC_SHOW_OPS/);
    expect(body).not.toContain(OPS_TOKEN);
    expect(none.headers()["www-authenticate"]).toContain("Bearer");

    expect((await api.get("/api/ops/summary", { headers: { Authorization: "Bearer wrong" } })).status()).toBe(401);
    // Prefix / suffix of the real token must fail.
    expect(
      (await api.get("/api/ops/summary", { headers: { Authorization: `Bearer ${OPS_TOKEN.slice(0, -1)}` } })).status(),
    ).toBe(401);
    expect(
      (await api.get("/api/ops/summary", { headers: { Authorization: `Bearer ${OPS_TOKEN}x` } })).status(),
    ).toBe(401);
    // Token in the URL is never accepted.
    for (const q of ["token", "ops-token", "ops_token", "access_token"]) {
      expect((await api.get(`/api/ops/summary?${q}=${OPS_TOKEN}`)).status(), q).toBe(401);
    }
    expect(
      (await api.get("/api/ops/summary", { headers: { Authorization: `Bearer ${OPS_TOKEN}` } })).status(),
    ).toBe(200);
    expect((await api.get("/api/ops/summary", { headers: { "X-Ops-Token": OPS_TOKEN } })).status()).toBe(200);

    // Brute-force throttle (limit 30/min/IP on this server; keep this last).
    let limited = false;
    for (let i = 0; i < 40 && !limited; i++) {
      const r = await api.get("/api/ops/summary", { headers: { Authorization: `Bearer guess-${i}` } });
      if (r.status() === 429) limited = true;
      else expect(r.status()).toBe(401);
    }
    expect(limited, "ops auth attempts must be rate limited").toBe(true);
    await api.dispose();
  });
});
