/**
 * axe-core WCAG 2.2 A/AA sweep over every route + wizard step + results +
 * saved profiles + /ops, in EN / HI / ML, on desktop and 375px mobile
 * (see playwright.config.ts projects). Fails on serious/critical WCAG
 * violations; writes full JSON per state when A11Y_REPORT_DIR is set.
 */
import { expect, test, type Page } from "@playwright/test";
import {
  INDIA_KERALA,
  MOCK_ZERO,
  US_CA,
  blocking,
  bootApp,
  clickNext,
  completeWizard,
  describe,
  fillStep,
  goToStep,
  scan,
  settle,
  type Lang,
} from "./helpers";

// These specs audit accessibility, not CSP: they inject helper <style> tags
// (contrast flattening, WCAG 1.4.12 text-spacing override) that the strict
// production CSP would rightly block. CSP itself is covered, without bypass,
// by e2e/security-headers.spec.ts.
test.use({ bypassCSP: true });

const LANGS: Lang[] = ["en", "hi", "ml"];

async function check(page: Page, state: string, lang: string, project: string) {
  await settle(page);
  const rec = await scan(page, { state, lang, project });
  const bad = blocking(rec);
  expect.soft(bad, `${state} [${lang}/${project}]\n${describe(bad)}`).toEqual([]);
}

for (const lang of LANGS) {
  test.describe(`axe ${lang}`, () => {
    test("home / welcome", async ({ page }, info) => {
      await bootApp(page, lang);
      await check(page, "home-welcome", lang, info.project.name);
    });

    for (let step = 1; step <= 9; step++) {
      test(`wizard step ${step} (India/Kerala)`, async ({ page }, info) => {
        await bootApp(page, lang);
        await goToStep(page, step, INDIA_KERALA);
        if (step === 3) await fillStep(page, 3); // show life-stage widget
        if (step === 8) await page.locator(".wizard-card fieldset").first().locator("button.choice-btn").nth(1).click();
        if (step === 9) {
          await page.locator(".wizard-card fieldset").first().locator("button.choice-btn").first().click();
        }
        await check(page, `step-${step}-india`, lang, info.project.name);
      });
    }

    test("wizard steps 2 + 9 (United States: region + free-text district)", async ({ page }, info) => {
      await bootApp(page, lang);
      await goToStep(page, 2, US_CA);
      await check(page, "step-2-us", lang, info.project.name);
      for (let s = 2; s < 9; s++) {
        await fillStep(page, s, US_CA);
        await clickNext(page);
      }
      await check(page, "step-9-us", lang, info.project.name);
    });

    test("wizard validation error (empty age)", async ({ page }, info) => {
      await bootApp(page, lang);
      await goToStep(page, 3);
      await clickNext(page);
      await check(page, "step-3-error", lang, info.project.name);
    });

    test("parent-for-child mode step 3", async ({ page }, info) => {
      await bootApp(page, lang);
      const self = page.locator("main button.primary-btn").first();
      await self.locator("xpath=following-sibling::button[1]").click();
      await fillStep(page, 1);
      await clickNext(page);
      await fillStep(page, 2);
      await clickNext(page);
      await check(page, "step-3-child", lang, info.project.name);
    });

    test("loading state", async ({ page }, info) => {
      await bootApp(page, lang);
      let release: () => void = () => {};
      const gate = new Promise<void>((r) => (release = r));
      await page.route("**/api/match", async (route) => {
        await gate;
        await route.continue();
      });
      await completeWizard(page);
      await page.locator(".animate-spin").waitFor();
      await check(page, "loading", lang, info.project.name);
      release();
    });

    test("results + expanded card + saved profiles", async ({ page }, info) => {
      await bootApp(page, lang);
      await completeWizard(page);
      const card = page.locator("article.scheme-card").first();
      await card.waitFor({ timeout: 30_000 });
      await check(page, "results", lang, info.project.name);
      await card.locator("button").first().click();
      await check(page, "results-expanded", lang, info.project.name);
      // Save this profile on-device, then start over → saved list visible
      const saved = page.locator("section[aria-labelledby='saved-profiles-heading']");
      await saved.locator("input[type=text]").fill("Test profile");
      await saved.locator("button").first().click();
      await check(page, "results-saved", lang, info.project.name);
      await page.goto("/");
      await page.locator("main#main-content").waitFor();
      await page.locator("section[aria-labelledby='saved-profiles-heading'] li").first().waitFor();
      await check(page, "home-saved-profiles", lang, info.project.name);
    });

    test("zero results", async ({ page }, info) => {
      await bootApp(page, lang);
      await page.route("**/api/match", (route) =>
        route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(MOCK_ZERO) }),
      );
      await completeWizard(page);
      await page.locator("main h2").first().waitFor();
      await check(page, "results-zero", lang, info.project.name);
    });

    test("server error state", async ({ page }, info) => {
      await bootApp(page, lang);
      await page.route("**/api/match", (route) => route.abort());
      await completeWizard(page);
      await page.locator("main pre").first().waitFor({ timeout: 15_000 });
      await check(page, "error", lang, info.project.name);
    });
  });
}

test.describe("axe ops + misc routes", () => {
  test("/ops (open demo gate)", async ({ page }, info) => {
    await page.goto("/ops");
    await page.locator("main section").first().waitFor();
    await check(page, "ops", "en", info.project.name);
  });

  test("/ops (token required)", async ({ page }, info) => {
    await page.route("**/api/ops/summary", (route) =>
      route.fulfill({
        status: 401,
        contentType: "application/json",
        body: JSON.stringify({ error: { code: "unauthorized", message: "Ops token required" } }),
      }),
    );
    await page.goto("/ops");
    await page.locator("main [role=alert]").waitFor();
    await check(page, "ops-locked", "en", info.project.name);
  });

  test("404 page", async ({ page }, info) => {
    await page.goto("/this-route-does-not-exist");
    await check(page, "not-found", "en", info.project.name);
  });
});
