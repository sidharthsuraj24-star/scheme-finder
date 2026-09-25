#!/usr/bin/env node
/**
 * Summarise axe JSON records written by e2e/a11y-axe.spec.ts (A11Y_REPORT_DIR).
 *   node scripts/a11y-summarize.mjs <dir> [--json]
 * Counts: scans, violation instances (rule × state × node) by impact, and
 * distinct rules by impact. "unique" dedupes identical rule+target across states.
 */
import fs from "node:fs";
import path from "node:path";

const dir = process.argv[2];
if (!dir) {
  console.error("usage: a11y-summarize.mjs <dir> [--json]");
  process.exit(2);
}
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json"));
const WCAG = new Set(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22a", "wcag22aa"]);
const impacts = ["critical", "serious", "moderate", "minor"];
const byImpactNodes = Object.fromEntries(impacts.map((i) => [i, 0]));
const rules = new Map();
const uniq = new Set();
for (const f of files) {
  const rec = JSON.parse(fs.readFileSync(path.join(dir, f), "utf8"));
  for (const v of rec.violations) {
    const wcag = v.tags.some((t) => WCAG.has(t));
    const key = v.id;
    if (!rules.has(key))
      rules.set(key, { id: v.id, impact: v.impact, wcag, help: v.help, nodes: 0, states: new Set(), targets: new Set() });
    const r = rules.get(key);
    r.nodes += v.nodes.length;
    r.states.add(`${rec.project}/${rec.lang}/${rec.state}`);
    for (const n of v.nodes) {
      r.targets.add(n.target);
      uniq.add(`${v.id}|${n.target}`);
    }
    byImpactNodes[v.impact] = (byImpactNodes[v.impact] || 0) + v.nodes.length;
  }
}
const rows = [...rules.values()].sort(
  (a, b) => impacts.indexOf(a.impact) - impacts.indexOf(b.impact) || b.nodes - a.nodes,
);
const summary = {
  scans: files.length,
  instances_by_impact: byImpactNodes,
  distinct_rules_by_impact: Object.fromEntries(
    impacts.map((i) => [i, rows.filter((r) => r.impact === i).length]),
  ),
  unique_rule_target_pairs: uniq.size,
  rules: rows.map((r) => ({
    id: r.id,
    impact: r.impact,
    wcag: r.wcag,
    help: r.help,
    instances: r.nodes,
    states: r.states.size,
    sample_targets: [...r.targets].slice(0, 6),
  })),
};
if (process.argv.includes("--json")) {
  console.log(JSON.stringify(summary, null, 2));
} else {
  console.log(`scans: ${summary.scans}`);
  console.log("instances by impact:", summary.instances_by_impact);
  console.log("distinct rules by impact:", summary.distinct_rules_by_impact);
  console.log(`unique rule+target pairs: ${summary.unique_rule_target_pairs}`);
  for (const r of summary.rules) {
    console.log(
      `- [${r.impact}]${r.wcag ? "" : " (best-practice)"} ${r.id} — ${r.help} — ${r.instances} instances in ${r.states} scans`,
    );
    for (const t of r.sample_targets) console.log(`    ${t}`);
  }
}
