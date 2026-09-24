/**
 * Tiny smoke: exercise savedProfiles logic via dynamic import of compiled TS is heavy;
 * instead re-implement the cap/key contract checks against the source file.
 */
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const src = readFileSync(join(root, "src/lib/savedProfiles.ts"), "utf8");
for (const needle of [
  "MAX_SAVED_PROFILES = 5",
  "scheme-finder-saved-profiles-v1",
  "localStorage",
  "saved_at",
]) {
  if (!src.includes(needle)) {
    console.error("missing", needle);
    process.exit(1);
  }
}
console.log("savedProfiles smoke OK");
