import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

import { DEFAULT_SKILLS_ROOT, listCatalogSkills } from "./presets.mjs";

export function getLockfilePath({
  global = false,
  cwd = process.cwd(),
  homeDir = homedir(),
  xdgStateHome = process.env.XDG_STATE_HOME,
} = {}) {
  if (!global) {
    return join(cwd, "skills-lock.json");
  }
  if (xdgStateHome) {
    return join(xdgStateHome, "skills", ".skill-lock.json");
  }
  return join(homeDir, ".agents", ".skill-lock.json");
}

function isOwnedLockEntry(skillName, entry, catalogSet) {
  if (!entry || typeof entry !== "object") return false;
  const source = String(entry.source ?? "").toLowerCase();
  const sourceUrl = String(entry.sourceUrl ?? "").toLowerCase();
  if (
    source.includes("thienqo/flutter-skills") ||
    sourceUrl.includes("thienqo/flutter-skills") ||
    source.includes("thiennc-tesoglobal/flutter-skills") ||
    sourceUrl.includes("thiennc-tesoglobal/flutter-skills")
  ) {
    return true;
  }
  return catalogSet.has(skillName) && source.includes("flutter-skills");
}

export function readInstalledFlutterSkills({
  global = false,
  cwd = process.cwd(),
  homeDir = homedir(),
  xdgStateHome = process.env.XDG_STATE_HOME,
  skillsRoot = DEFAULT_SKILLS_ROOT,
} = {}) {
  const lockPath = getLockfilePath({ global, cwd, homeDir, xdgStateHome });
  if (!existsSync(lockPath)) {
    return { lockPath, exists: false, skills: [] };
  }

  let parsed;
  try {
    parsed = JSON.parse(readFileSync(lockPath, "utf8"));
  } catch {
    return { lockPath, exists: true, invalid: true, skills: [] };
  }

  const rawSkills = parsed?.skills && typeof parsed.skills === "object" ? parsed.skills : {};
  const catalogSet = new Set(listCatalogSkills(skillsRoot));
  const installed = [];

  for (const [name, entry] of Object.entries(rawSkills)) {
    if (!isOwnedLockEntry(name, entry, catalogSet)) continue;
    installed.push({
      name,
      ref: entry.ref ?? null,
      source: entry.source ?? null,
      sourceUrl: entry.sourceUrl ?? null,
      updatedAt: entry.updatedAt ?? null,
    });
  }

  installed.sort((a, b) => a.name.localeCompare(b.name));
  return { lockPath, exists: true, skills: installed };
}
