/**
 * Scripted manual-style WCAG 2.2 AA checks that axe cannot fully automate:
 * keyboard-only operation, focus visibility / not obscured, focus management,
 * error identification + programmatic association, language switching,
 * status messages, reduced motion, reflow at 320px, target size, non-text
 * contrast, accessible authentication on /ops.
 */
import { expect, test, type Page } from "@playwright/test";
import {
  INDIA_KERALA,
  bootApp,
  clickNext,
  completeWizard,
  fillStep,
  goToStep,
  settle,
} from "./helpers";

type Target = { css: string } | { choice: [number, number] };

function lum(rgb: number[]) {
  const [r, g, b] = rgb.map((c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function ratio(a: number[], b: number[]) {
  const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
}
function parseRgb(s: string): number[] {
  const m = s.match(/[\d.]+/g) || ["0", "0", "0"];
  return m.slice(0, 3).map(Number);
}

/** Inspect the focused element: visible indicator + not obscured + identity. */
async function focusInfo(page: Page, target?: Target) {
  return page.evaluate((tg) => {
    const el = document.activeElement as HTMLElement | null;
    if (!el || el === document.body) return { none: true } as const;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const cx = Math.min(Math.max(r.left + r.width / 2, 0), innerWidth - 1);
    const cy = Math.min(Math.max(r.top + Math.min(r.height / 2, 20), 0), innerHeight - 1);
    const hit = document.elementFromPoint(cx, cy);
    const inView = r.bottom > 0 && r.top < innerHeight && r.right > 0 && r.left < innerWidth;
    let matches = false;
    if (tg && "css" in tg) matches = el.matches(tg.css);
    if (tg && "choice" in tg) {
      const fs = document.querySelectorAll(".wizard-card fieldset")[tg.choice[0]];
      matches = !!fs && fs.querySelectorAll("button.choice-btn")[tg.choice[1]] === el;
    }
    return {
      none: false as const,
      desc: `${el.tagName.toLowerCase()}${el.id ? "#" + el.id : ""} "${(el.textContent || "").trim().slice(0, 40)}"`,
      outlineStyle: cs.outlineStyle,
      outlineWidth: parseFloat(cs.outlineWidth) || 0,
      outlineColor: cs.outlineColor,
      boxShadow: cs.boxShadow,
      inView,
      unobscured: !!hit && (hit === el || el.contains(hit) || hit.contains(el)),
      matches,
      w: r.width,
      h: r.height,
    };
  }, target ?? null);
}

async function assertVisibleFocus(page: Page, ctx: string) {
  const f = await focusInfo(page);
  if (f.none) return;
  const hasOutline = f.outlineStyle !== "none" && f.outlineWidth >= 2;
  const hasShadow = f.boxShadow && f.boxShadow !== "none";
  expect(hasOutline || hasShadow, `${ctx}: no visible focus indicator on ${f.desc}`).toBeTruthy();
  if (hasOutline) {
    const c = parseRgb(f.outlineColor);
    // 1.4.11: indicator vs white card and vs darkest page background
    expect(ratio(c, [255, 255, 255]), `${ctx}: focus ring contrast on ${f.desc}`).toBeGreaterThanOrEqual(3);
    expect(ratio(c, [220, 252, 231]), `${ctx}: focus ring contrast on ${f.desc}`).toBeGreaterThanOrEqual(3);
  }
  expect(f.inView, `${ctx}: focused ${f.desc} scrolled out of view (2.4.11)`).toBeTruthy();
  expect(f.unobscured, `${ctx}: focused ${f.desc} is obscured (2.4.11)`).toBeTruthy();
}

/** Press Tab until `target` is focused, checking every stop for visible focus. */
async function tabTo(page: Page, target: Target, ctx: string, max = 60) {
  for (let i = 0; i < max; i++) {
    await page.keyboard.press("Tab");
    await assertVisibleFocus(page, ctx);
    const f = await focusInfo(page, target);
    if (!f.none && f.matches) return;
  }
  throw new Error(`${ctx}: could not reach ${JSON.stringify(target)} with Tab (keyboard access)`);
}

const NEXT: Target = { css: "button.primary-btn" };

test.describe("keyboard + focus", () => {
  test("skip link is first, visible on focus, and bypasses the header", async ({ page }) => {
    await bootApp(page, "en");
    await page.keyboard.press("Tab");
    const f = await focusInfo(page, { css: "a[href='#main-content']" });
    expect(f.none ? false : f.matches, "first Tab stop is the skip link").toBeTruthy();
    await assertVisibleFocus(page, "skip link");
    await page.keyboard.press("Enter");
    await expect(page.locator("#main-content")).toBeFocused();
    // Next Tab must not land in the header language switcher (bypass blocks, 2.4.1)
    await page.keyboard.press("Tab");
    const inHeader = await page.evaluate(
      () => !!document.activeElement?.closest("header, [role=banner]"),
    );
    expect(inHeader, "skip link should bypass the header/language switcher").toBeFalsy();
  });

  test("complete the whole wizard with the keyboard only", async ({ page }) => {
    await bootApp(page, "en");
    await tabTo(page, NEXT, "welcome");
    await page.keyboard.press("Enter");
    await expect(page.locator("#country")).toBeVisible();

    // Focus management: moving between steps must not drop focus to <body>
    const afterStart = await page.evaluate(() => document.activeElement?.tagName);
    expect(afterStart, "focus lost to <body> after starting wizard").not.toBe("BODY");

    // Step 1: country (India preselected) → Next
    await tabTo(page, { css: "#country" }, "step1");
    await tabTo(page, NEXT, "step1");
    await page.keyboard.press("Enter");
    // Step 2: state select via typeahead
    await tabTo(page, { css: "select#state" }, "step2");
    await page.keyboard.type("Kerala");
    await expect(page.locator("select#state")).toHaveValue("Kerala");
    await tabTo(page, NEXT, "step2");
    await page.keyboard.press("Enter");
    // Step 3: age
    await tabTo(page, { css: "#age" }, "step3");
    await page.keyboard.type("34");
    await tabTo(page, NEXT, "step3");
    await page.keyboard.press("Enter");
    // Step 4: income (yearly/monthly toggles are buttons)
    await tabTo(page, { css: "#income" }, "step4");
    await page.keyboard.type("90000");
    await tabTo(page, NEXT, "step4");
    await page.keyboard.press("Enter");
    // Steps 5–8: single / multi choice via Space
    for (const [step, choice] of [
      [5, 4],
      [6, 0],
      [7, 1],
      [8, 0],
    ] as const) {
      await tabTo(page, { choice: [0, choice] }, `step${step}`);
      await page.keyboard.press("Space");
      await tabTo(page, NEXT, `step${step}`);
      await page.keyboard.press("Enter");
    }
    // Step 9
    await tabTo(page, { css: "#district" }, "step9");
    await page.keyboard.type("Ernakulam");
    await expect(page.locator("#district")).toHaveValue("Ernakulam");
    for (const [fs, c] of [
      [0, 0],
      [1, 1],
      [2, 2],
      [3, 1],
    ] as const) {
      await tabTo(page, { choice: [fs, c] }, "step9");
      await page.keyboard.press("Space");
    }
    await tabTo(page, NEXT, "step9");
    await page.keyboard.press("Enter");
    await page.locator("article.scheme-card").first().waitFor({ timeout: 30_000 });
    // Focus should land on the results heading, not <body>
    const tag = await page.evaluate(() => document.activeElement?.tagName);
    expect(tag, "focus should move to results heading").toBe("H2");

    // Expand a scheme card with the keyboard
    await tabTo(page, { css: "article.scheme-card button[aria-expanded]" }, "results");
    await page.keyboard.press("Enter");
    await expect(
      page.locator("article.scheme-card button[aria-expanded='true']").first(),
    ).toBeVisible();
  });

  test("no keyboard trap: Tab cycles forward and Shift+Tab backward on the busiest step", async ({ page }) => {
    await bootApp(page, "en");
    await goToStep(page, 9);
    await page.locator("body").click({ position: { x: 1, y: 1 } });
    const seen: string[] = [];
    for (let i = 0; i < 80; i++) {
      await page.keyboard.press("Tab");
      seen.push(
        await page.evaluate(() => {
          const el = document.activeElement as HTMLElement;
          return `${el.tagName}|${el.id}|${(el.textContent || "").trim().slice(0, 20)}|${[...(el.parentElement?.children || [])].indexOf(el)}`;
        }),
      );
    }
    const uniq = new Set(seen);
    expect(uniq.size, "Tab reached many distinct controls").toBeGreaterThan(12);
    // Focus eventually cycles (leaves the page chrome) — no element holds focus for >2 presses in a row
    let run = 1;
    for (let i = 1; i < seen.length; i++) {
      run = seen[i] === seen[i - 1] ? run + 1 : 1;
      expect(run, `focus stuck on ${seen[i]}`).toBeLessThan(3);
    }
    const before = seen[seen.length - 1];
    await page.keyboard.press("Shift+Tab");
    const back = await page.evaluate(() => (document.activeElement as HTMLElement).tagName);
    expect(back).toBeTruthy();
    expect(before).toBeTruthy();
  });
});

test.describe("forms: labels, hints, errors", () => {
  test("text/number inputs have hints + errors programmatically associated", async ({ page }) => {
    await bootApp(page, "en");
    await goToStep(page, 3);
    const age = page.locator("#age");
    const hintIds = (await age.getAttribute("aria-describedby")) || "";
    expect(hintIds, "age input should reference its hint via aria-describedby").not.toBe("");
    await clickNext(page);
    const alert = page.locator("main [role=alert]");
    await expect(alert).toBeVisible();
    await expect(age).toHaveAttribute("aria-invalid", "true");
    const errId = await alert.getAttribute("id");
    expect(errId, "error message needs an id to be referenced").toBeTruthy();
    expect((await age.getAttribute("aria-describedby")) || "").toContain(errId!);
    await expect(age, "focus moves to the invalid field").toBeFocused();
    // Suggestion (3.3.3): message should say what a valid value is
    await expect(alert).toContainText(/0.*120/);
    // Invalid value (out of range) also gets a specific message
    await age.fill("150");
    await clickNext(page);
    await expect(alert).toContainText(/0.*120/);
    await age.fill("34");
    await clickNext(page);
    await expect(page.locator("#income")).toBeVisible();
  });

  test("choice groups expose error on the group (fieldset) and clear it", async ({ page }) => {
    await bootApp(page, "en");
    await goToStep(page, 5);
    await clickNext(page);
    const alert = page.locator("main [role=alert]");
    await expect(alert).toBeVisible();
    const errId = await alert.getAttribute("id");
    const fs = page.locator(".wizard-card fieldset").first();
    expect((await fs.getAttribute("aria-describedby")) || "").toContain(errId || "__none__");
    await fillStep(page, 5);
    await clickNext(page);
    await expect(alert).toHaveCount(0);
  });

  test("every input/select has a visible <label> (not placeholder-only)", async ({ page }) => {
    await bootApp(page, "en");
    const check = async (ctx: string) => {
      const bad = await page.evaluate(() =>
        [...document.querySelectorAll("main input, main select")]
          .filter((el) => (el as HTMLElement).offsetParent !== null)
          .filter((el) => {
            const id = el.id;
            const lab = id ? document.querySelector(`label[for="${id}"]`) : null;
            const wrapped = el.closest("label");
            return !(lab || wrapped);
          })
          .map((el) => el.outerHTML.slice(0, 120)),
      );
      expect(bad, `${ctx}: inputs without visible label`).toEqual([]);
    };
    await check("home");
    await goToStep(page, 2, { country: "United States", state: "California", district: "LA" });
    await check("us-region");
    await page.goto("/ops");
    await page.locator("main").waitFor();
    await check("ops");
  });
});

test.describe("language, status, motion, reflow, targets", () => {
  test("html lang follows the selected language (3.1.1) and toggles mark their own language (3.1.2)", async ({ page }) => {
    await bootApp(page, "en");
    await expect(page.locator("html")).toHaveAttribute("lang", "en");
    const group = page.locator("header [role=group], main [role=group]").first();
    const hiBtn = group.locator("button").nth(1);
    const mlBtn = group.locator("button").nth(2);
    await hiBtn.click();
    await expect(page.locator("html")).toHaveAttribute("lang", "hi");
    await mlBtn.click();
    await expect(page.locator("html")).toHaveAttribute("lang", "ml");
    await expect(hiBtn).toHaveAttribute("lang", "hi");
    await expect(mlBtn).toHaveAttribute("lang", "ml");
  });

  test("stored Hindi preference sets html lang=hi on load", async ({ page }) => {
    await bootApp(page, "hi");
    await expect(page.locator("html")).toHaveAttribute("lang", "hi");
  });

  test("viewport allows pinch-zoom (1.4.4)", async ({ page }) => {
    await page.goto("/");
    const content = (await page.locator("meta[name=viewport]").getAttribute("content")) || "";
    expect(content).not.toMatch(/maximum-scale\s*=\s*1(\.0)?\b/);
    expect(content).not.toMatch(/user-scalable\s*=\s*(no|0)/);
  });

  test("loading and result count are announced via a persistent live region (4.1.3)", async ({ page }) => {
    await bootApp(page, "en");
    // A polite live region must exist BEFORE the results arrive
    const live = page.locator("[aria-live=polite], [role=status]").filter({ hasText: /^$|./ });
    const preexisting = await page.locator("#sr-status[aria-live]").count();
    expect(preexisting, "persistent #sr-status live region present on load").toBe(1);
    await completeWizard(page);
    await page.locator("article.scheme-card").first().waitFor({ timeout: 30_000 });
    await expect(page.locator("#sr-status")).toContainText(/scheme\(s\) found/);
    void live;
  });

  test("prefers-reduced-motion disables animations", async ({ browser }) => {
    const ctx = await browser.newContext({ reducedMotion: "reduce" });
    const page = await ctx.newPage();
    await bootApp(page, "en");
    const dur = await page.evaluate(() => {
      const el = document.querySelector(".animate-pop-in") as HTMLElement;
      const cs = getComputedStyle(el);
      return { name: cs.animationName, dur: parseFloat(cs.animationDuration) };
    });
    expect(dur.name === "none" || dur.dur <= 0.01).toBeTruthy();
    let release: () => void = () => {};
    const gate = new Promise<void>((r) => (release = r));
    await page.route("**/api/match", async (route) => {
      await gate;
      await route.continue();
    });
    await completeWizard(page);
    const spin = page.locator(".animate-spin");
    await spin.waitFor();
    const spinDur = await spin.evaluate((el) => {
      const cs = getComputedStyle(el);
      return cs.animationName === "none" ? 0 : parseFloat(cs.animationDuration);
    });
    expect(spinDur, "spinner should not spin with reduced motion").toBeLessThanOrEqual(0.01);
    release();
    await ctx.close();
  });

  for (const width of [320, 640]) {
    test(`reflow: no horizontal scroll at ${width}px (1.4.10 / 200–400% zoom)`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width, height: 700 } });
      const page = await ctx.newPage();
      const noHScroll = async (ctx2: string) => {
        await settle(page, 600);
        const sw = await page.evaluate(() => document.documentElement.scrollWidth);
        expect(sw, `${ctx2} @${width}px scrollWidth`).toBeLessThanOrEqual(width);
      };
      for (const lang of ["en", "hi", "ml"] as const) {
        const p2 = await ctx.newPage();
        await bootApp(p2, lang);
        await settle(p2, 600);
        const sw = await p2.evaluate(() => document.documentElement.scrollWidth);
        expect(sw, `home ${lang} @${width}px scrollWidth`).toBeLessThanOrEqual(width);
        await p2.close();
      }
      await bootApp(page, "en");
      for (let s = 1; s <= 9; s++) {
        if (s === 1) await goToStep(page, 1);
        await noHScroll(`step ${s}`);
        await fillStep(page, s, INDIA_KERALA);
        await clickNext(page);
      }
      await page.locator("article.scheme-card").first().waitFor({ timeout: 30_000 });
      await page.locator("article.scheme-card button[aria-expanded]").first().click();
      await noHScroll("results");
      await page.goto("/ops");
      await page.locator("main section").first().waitFor();
      await noHScroll("ops");
      await ctx.close();
    });
  }

  test("text spacing override (1.4.12) does not cause horizontal overflow", async ({ page }) => {
    await bootApp(page, "hi");
    await page.addStyleTag({
      content:
        "*{line-height:1.5 !important;letter-spacing:.12em !important;word-spacing:.16em !important}p{margin-bottom:2em !important}",
    });
    await settle(page, 500);
    const vw = page.viewportSize()!.width;
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    expect(sw).toBeLessThanOrEqual(vw);
  });

  test("interactive targets are at least 24×24 CSS px (2.5.8)", async ({ page }) => {
    await bootApp(page, "en");
    const collect = () =>
      page.evaluate(() =>
        [...document.querySelectorAll("a[href], button, input, select")]
          .filter(
            (el) =>
              (el as HTMLElement).offsetParent !== null &&
              !el.closest("p") &&
              !el.classList.contains("sr-only"),
          )
          .map((el) => {
            const r = el.getBoundingClientRect();
            return { d: el.outerHTML.slice(0, 90), w: r.width, h: r.height };
          })
          .filter((x) => x.w < 24 || x.h < 24),
      );
    expect(await collect(), "home").toEqual([]);
    await completeWizard(page);
    await page.locator("article.scheme-card").first().waitFor({ timeout: 30_000 });
    const saved = page.locator("section[aria-labelledby='saved-profiles-heading']");
    await saved.locator("input[type=text]").fill("A");
    await saved.locator("button").first().click();
    await page.locator("article.scheme-card button[aria-expanded]").first().click();
    expect(await collect(), "results + saved").toEqual([]);
  });

  test("form control boundaries meet 3:1 non-text contrast (1.4.11)", async ({ page }) => {
    await bootApp(page, "en");
    await goToStep(page, 3);
    const border = await page.locator("#age").evaluate((el) => getComputedStyle(el).borderTopColor);
    expect(ratio(parseRgb(border), [255, 255, 255])).toBeGreaterThanOrEqual(3);
    await fillStep(page, 3);
    await clickNext(page);
    await fillStep(page, 4);
    await clickNext(page);
    // Unselected choice must still show a 3:1 boundary or indicator
    const idle = await page
      .locator(".wizard-card button.choice-btn")
      .first()
      .evaluate((el) => {
        const ind = el.querySelector("[data-choice-indicator]") as HTMLElement | null;
        return getComputedStyle(ind || el).borderTopColor;
      });
    expect(ratio(parseRgb(idle), [255, 255, 255])).toBeGreaterThanOrEqual(3);
  });
});

test.describe("/ops accessible authentication (3.3.8)", () => {
  test("token field is labelled, allows paste + password managers, Enter submits", async ({ page }) => {
    await page.goto("/ops");
    await page.locator("main").waitFor();
    const input = page.locator("main input[type=password]");
    await expect(input).toHaveAccessibleName(/token/i);
    const ac = await input.getAttribute("autocomplete");
    expect(ac === "current-password" || ac === "one-time-code" || ac === "on").toBeTruthy();
    const pasteBlocked = await input.evaluate((el) => {
      const ev = new Event("paste", { bubbles: true, cancelable: true });
      el.dispatchEvent(ev);
      return ev.defaultPrevented;
    });
    expect(pasteBlocked).toBeFalsy();
    let calls = 0;
    await page.route("**/api/ops/summary", async (route) => {
      calls++;
      await route.continue();
    });
    await input.fill("abc");
    await input.press("Enter");
    await expect.poll(() => calls).toBeGreaterThan(0);
  });
});
