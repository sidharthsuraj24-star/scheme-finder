import { defineConfig, devices } from "@playwright/test";

/**
 * Accessibility regression suite (axe-core + scripted keyboard checks).
 *
 *   npm run build && npm run test:a11y
 *
 * Uses a production `next start` on :3100 with the /ops demo gate open.
 * Set A11Y_BASE_URL to audit an already-running server instead.
 */
const PORT = Number(process.env.A11Y_PORT || 3100);
const BASE = process.env.A11Y_BASE_URL || `http://127.0.0.1:${PORT}`;

export default defineConfig({
  testDir: "./e2e",
  timeout: 120_000,
  fullyParallel: true,
  workers: process.env.CI ? 2 : 4,
  reporter: [["list"]],
  use: {
    baseURL: BASE,
    trace: "off",
  },
  projects: [
    {
      name: "desktop",
      use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 800 } },
    },
    {
      name: "mobile-375",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 375, height: 812 },
        deviceScaleFactor: 2,
        hasTouch: true,
        isMobile: true,
      },
    },
  ],
  webServer: process.env.A11Y_BASE_URL
    ? undefined
    : {
        command: `npx next start -p ${PORT}`,
        url: `${BASE}/api/health`,
        reuseExistingServer: true,
        timeout: 120_000,
        env: { NEXT_PUBLIC_SHOW_OPS: "1" },
      },
});
