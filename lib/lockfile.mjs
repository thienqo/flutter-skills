import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export const OWNED_REPOSITORIES = new Set([
  "thienqo/flutter-skills",
  "thiennc-tesoglobal/flutter-skills",
]);

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

// Reduce any supported source spelling (owner/repo, https URL, git@ URL, with or
// without a `#ref` suffix) to an exact `owner/repo` identity so that similarly
// named repositories such as `thienqo/flutter-skills-extra` are not mistaken for
// this package.
export function repositoryIdentity(value) {
  const raw = String(value ?? "").trim().toLowerCase();
  if (!raw) return null;
  const cleaned = raw
    .replace(/^git\+/, "")
    .replace(/^[a-z][a-z0-9+.-]*:\/\//, "")
    .replace(/^[^@/]+@/, "")
    .replace(/^github\.com[:/]/, "")
    .split(/[#?]/)[0]
    .replace(/\.git\/?$/, "")
    .replace(/\/+$/, "");
  const [owner, name] = cleaned.split("/").filter(Boolean);
  if (!owner || !name) return null;
  return `${owner}/${name}`;
}

export function isOwnedLockEntry(entry) {
  if (!entry || typeof entry !== "object") return false;
  return (
    OWNED_REPOSITORIES.has(repositoryIdentity(entry.source)) ||
    OWNED_REPOSITORIES.has(repositoryIdentity(entry.sourceUrl))
  );
}

export function readInstalledFlutterSkills({
  global = false,
  cwd = process.cwd(),
  homeDir = homedir(),
  xdgStateHome = process.env.XDG_STATE_HOME,
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
  const installed = [];

  for (const [name, entry] of Object.entries(rawSkills)) {
    if (!isOwnedLockEntry(entry)) continue;
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
