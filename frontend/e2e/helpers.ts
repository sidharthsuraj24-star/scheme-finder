import AxeBuilder from "@axe-core/playwright";
import type { Page } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";

export type Lang = "en" | "hi" | "ml";

/** WCAG 2.0/2.1/2.2 A + AA rules, plus axe best-practice (reported, not gating). */
export const WCAG_TAGS = [
  "wcag2a",
  "wcag2aa",
  "wcag21a",
  "wcag21aa",
  "wcag22a",
  "wcag22aa",
];

export const LANG_KEY = "scheme-finder-lang";

/** Seed language (and optionally clean storage) before the app boots. */
export async function bootApp(page: Page, lang: Lang, urlPath = "/") {
  await page.addInitScript(
    ([key, l]) => {
      try {
        if (!sessionStorage.getItem("__a11y_seeded")) {
          localStorage.clear();
          localStorage.setItem(key, l);
          sessionStorage.setItem("__a11y_seeded", "1");
        }
      } catch {
        /* ignore */
      }
    },
    [LANG_KEY, lang] as const,
  );
  await page.goto(urlPath);
  await page.locator("main#main-content").waitFor();
}

/** Welcome → step 1 ("for myself" = first primary button; child = the button after it). */
export async function startWizard(page: Page, mode: "self" | "child" = "self") {
  const self = page.locator("main button.primary-btn").first();
  if (mode === "self") await self.click();
  else await self.locator("xpath=following-sibling::button[1]").click();
  await page.locator("#country").waitFor();
}

export async function clickNext(page: Page) {
  await page.locator("main button.primary-btn").last().click();
}

/** fieldset(i) → choice button(j) inside the wizard card. */
export async function pickChoice(page: Page, fieldsetIdx: number, choiceIdx: number) {
  await page
    .locator(".wizard-card fieldset")
    .nth(fieldsetIdx)
    .locator("button.choice-btn")
    .nth(choiceIdx)
    .click();
}

export interface Path {
  country: "India" | "United States";
  state: string;
  district?: string;
}

export const INDIA_KERALA: Path = { country: "India", state: "Kerala", district: "Ernakulam" };
export const US_CA: Path = { country: "United States", state: "California", district: "Los Angeles" };

/**
 * Advance from welcome to wizard step `target` (1..9) filling valid answers.
 * Leaves the page ON step `target` without filling it.
 */
export async function goToStep(page: Page, target: number, p: Path = INDIA_KERALA) {
  await startWizard(page);
  for (let s = 1; s < target; s++) {
    await fillStep(page, s, p);
    await clickNext(page);
  }
}

export async function fillStep(page: Page, s: number, p: Path = INDIA_KERALA) {
  switch (s) {
    case 1:
      await page.locator("#country").selectOption(p.country);
      break;
    case 2:
      await page.locator("select#state").selectOption(p.state);
      break;
    case 3:
      await page.locator("#age").fill("34");
      break;
    case 4:
      await page.locator("#income").fill("90000");
      break;
    case 5:
      await pickChoice(page, 0, 4); // other
      break;
    case 6:
      await pickChoice(page, 0, 0); // none
      break;
    case 7:
      await pickChoice(page, 0, 1); // no land
      break;
    case 8:
      await pickChoice(page, 0, 0); // no disability
      break;
    case 9: {
      const d = page.locator("#district");
      const tag = await d.evaluate((el) => el.tagName.toLowerCase());
      if (tag === "select") await d.selectOption(p.district || "Ernakulam");
      else await d.fill(p.district || "Los Angeles");
      await pickChoice(page, 0, 0); // female
      await pickChoice(page, 1, 1); // married
      await pickChoice(page, 2, 2); // maternity: neither
      await pickChoice(page, 3, 1); // breadwinner deceased: no
      break;
    }
  }
}

export async function completeWizard(page: Page, p: Path = INDIA_KERALA) {
  await goToStep(page, 9, p);
  await fillStep(page, 9, p);
  await clickNext(page);
}

/** Let entrance animations (pop-in ≈450ms, age counter ≤1.2s) settle before scanning. */
export async function settle(page: Page, ms = 1300) {
  await page.waitForTimeout(ms);
}

export interface ScanRecord {
  state: string;
  lang: string;
  project: string;
  url: string;
  violations: {
    id: string;
    impact: string | null;
    tags: string[];
    help: string;
    helpUrl: string;
    nodes: { target: string; summary: string }[];
  }[];
  /** axe "needs review" (e.g. contrast over gradients) — not gating, triaged manually. */
  incomplete: { id: string; impact: string | null; nodes: { target: string; summary: string }[] }[];
}

export async function scan(page: Page, opts: { state: string; lang: string; project: string }) {
  const res = await new AxeBuilder({ page })
    .withTags([...WCAG_TAGS, "best-practice"])
    .analyze();
  // Second pass: axe cannot compute contrast over the body's decorative
  // gradient (reports "incomplete"). Re-run color-contrast with the body
  // flattened to its darkest gradient stop (#dcfce7 ≈ worst case for dark
  // text) so low-contrast text is actually caught.
  await page.evaluate(() => {
    const st = document.createElement("style");
    st.id = "__a11y_flat_bg";
    st.textContent =
      "body{background:#dcfce7 !important}.wizard-card{backdrop-filter:none !important}";
    document.head.appendChild(st);
  });
  const flat = await new AxeBuilder({ page }).withRules(["color-contrast"]).analyze();
  await page.evaluate(() => document.getElementById("__a11y_flat_bg")?.remove());
  const seen = new Set(
    res.violations
      .filter((v) => v.id === "color-contrast")
      .flatMap((v) => v.nodes.map((n) => n.target.join(" "))),
  );
  for (const v of flat.violations) {
    const extra = v.nodes.filter((n) => !seen.has(n.target.join(" ")));
    if (!extra.length) continue;
    const existing = res.violations.find((x) => x.id === v.id);
    if (existing) existing.nodes.push(...extra);
    else res.violations.push({ ...v, nodes: extra });
  }
  const rec: ScanRecord = {
    ...opts,
    url: page.url(),
    violations: res.violations.map((v) => ({
      id: v.id,
      impact: v.impact ?? null,
      tags: v.tags,
      help: v.help,
      helpUrl: v.helpUrl,
      nodes: v.nodes.map((n) => ({
        target: n.target.join(" "),
        summary: (n.failureSummary || "").slice(0, 400),
      })),
    })),
    incomplete: res.incomplete.map((v) => ({
      id: v.id,
      impact: v.impact ?? null,
      nodes: v.nodes.map((n) => ({
        target: n.target.join(" "),
        summary: (n.failureSummary || "").slice(0, 300),
      })),
    })),
  };
  const out = process.env.A11Y_REPORT_DIR;
  if (out) {
    fs.mkdirSync(out, { recursive: true });
    const file = path.join(
      out,
      `${opts.project}__${opts.lang}__${opts.state}`.replace(/[^\w.-]+/g, "_") + ".json",
    );
    fs.writeFileSync(file, JSON.stringify(rec, null, 2));
  }
  return rec;
}

/** Gating rule: WCAG-tagged violations with serious/critical impact. */
export function blocking(rec: ScanRecord) {
  return rec.violations.filter(
    (v) =>
      (v.impact === "serious" || v.impact === "critical") &&
      v.tags.some((t) => WCAG_TAGS.includes(t)),
  );
}

export function describe(rec: ScanRecord["violations"]) {
  return rec
    .map((v) => `${v.impact} ${v.id}: ${v.help}\n    ${v.nodes.map((n) => n.target).join("\n    ")}`)
    .join("\n");
}

export const MOCK_ZERO = {
  matched: [],
  excluded: [],
  needs_verification: [],
  message: "No scheme matched these answers.",
  count: 0,
  country: "India",
  state: "Kerala",
  district: "Ernakulam",
};
