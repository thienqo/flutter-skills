import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { homedir } from "node:os";
import { dirname, join } from "node:path";

import { detectProjectSkills } from "./detect.mjs";
import { readInstalledFlutterSkills } from "./lockfile.mjs";
import {
  DEFAULT_SKILLS_ROOT,
  PRESETS,
  PRESET_DESCRIPTIONS,
  listCatalogSkills,
  resolvePresetNames,
} from "./presets.mjs";

const require = createRequire(import.meta.url);
const packageMetadata = JSON.parse(
  readFileSync(new URL("../package.json", import.meta.url), "utf8"),
);

export const packageVersion = packageMetadata.version;
export const targetRef = `v${packageVersion}`;
export const repository = "thienqo/flutter-skills";
export const skillsSource = `https://github.com/${repository}#${targetRef}`;

export function installerArguments(args) {
  return ["add", skillsSource, ...args];
}

export function helpText() {
  return `Flutter Skills ${packageVersion}

Usage:
  npx @thiennc/flutter-skills [options]
  npx @thiennc/flutter-skills <command> [options]

Commands:
  add [options]          Install Flutter skills (default)
  presets                List available preset bundles
  status [-g]            Check installed Flutter skills and versions
  update [-g] [-y]       Update installed Flutter skills to ${targetRef}
  remove [skills...]     Uninstall Flutter skills safely

Install options:
  -p, --preset <names>   Install preset(s): core, ui, data, ship, platform, full, auto
      --detect           Auto-detect packages from pubspec.yaml (same as --preset auto)
  -s, --skill <skills>   Install selected skills
  -a, --agent <agents>   Install for selected agents
  -g, --global           Install or manage skills at user level
  -l, --list             List available skills
  -y, --yes              Skip confirmation prompts
      --all              Install every skill for every agent (or remove all Flutter skills)
      --no-telemetry     Disable telemetry in the upstream installer
  -h, --help             Show this help
  -v, --version          Show the wrapper version

Source: ${skillsSource}`;
}

export function resolveSkillsCli() {
  const packagePath = require.resolve("skills/package.json");
  return join(dirname(packagePath), "bin", "cli.mjs");
}

function stripNoTelemetryFlag(args) {
  let noTelemetry = false;
  const remaining = [];
  for (const arg of args) {
    if (arg === "--no-telemetry") {
      noTelemetry = true;
    } else {
      remaining.push(arg);
    }
  }
  return { noTelemetry, remaining };
}

function parseInstallOptions(args) {
  const presets = [];
  const skills = [];
  const passthrough = [];
  let detect = false;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--detect") {
      detect = true;
      continue;
    }
    if (arg === "-p" || arg === "--preset") {
      const value = args[i + 1];
      if (!value || value.startsWith("-")) {
        throw new Error(`${arg} requires a preset name.`);
      }
      presets.push(value);
      i += 1;
      continue;
    }
    if (arg.startsWith("--preset=")) {
      const value = arg.slice("--preset=".length);
      if (!value) {
        throw new Error("--preset= requires a preset name.");
      }
      presets.push(value);
      continue;
    }
    if (arg === "-s" || arg === "--skill") {
      let j = i + 1;
      while (j < args.length && !args[j].startsWith("-")) {
        skills.push(args[j]);
        j += 1;
      }
      i = j - 1;
      continue;
    }
    passthrough.push(arg);
  }

  return { presets, skills, passthrough, detect };
}

function formatPresetsText(skillsRoot = DEFAULT_SKILLS_ROOT) {
  const catalogCount = listCatalogSkills(skillsRoot).length;
  const lines = [`Flutter Skills ${packageVersion} — Presets`, ""];
  for (const [name, list] of Object.entries(PRESETS)) {
    lines.push(`  ${name.padEnd(10)} (${String(list.length).padStart(2)} skills)  ${PRESET_DESCRIPTIONS[name]}`);
  }
  lines.push(`  ${"full".padEnd(10)} (${String(catalogCount).padStart(2)} skills)  ${PRESET_DESCRIPTIONS.full}`);
  lines.push(`  ${"auto".padEnd(10)} (detected)   ${PRESET_DESCRIPTIONS.auto}`);
  lines.push("");
  lines.push("Example: npx @thiennc/flutter-skills --preset core,ui --agent codex");
  return lines.join("\n");
}

function runUpstream(upstreamArgs, { noTelemetry, options }) {
  const spawn = options.spawn ?? spawnSync;
  const cliPath = options.cliPath ?? resolveSkillsCli();
  const nodePath = options.nodePath ?? process.execPath;
  const stderr = options.stderr ?? process.stderr;

  const spawnOptions = { stdio: "inherit" };
  if (noTelemetry) {
    spawnOptions.env = {
      ...(options.env ?? process.env),
      DISABLE_TELEMETRY: "1",
    };
  }

  const result = spawn(nodePath, [cliPath, ...upstreamArgs], spawnOptions);
  if (result.error) {
    stderr.write(`Unable to start the skills installer: ${result.error.message}\n`);
    return 1;
  }
  return Number.isInteger(result.status) ? result.status : 1;
}

function handleStatus(args, options) {
  const stdout = options.stdout ?? process.stdout;
  const isGlobal = args.includes("-g") || args.includes("--global");
  const cwd = options.cwd ?? process.cwd();
  const homeDir = options.homeDir ?? homedir();
  const xdgStateHome = options.xdgStateHome ?? process.env.XDG_STATE_HOME;
  const skillsRoot = options.skillsRoot ?? DEFAULT_SKILLS_ROOT;

  const state = readInstalledFlutterSkills({
    global: isGlobal,
    cwd,
    homeDir,
    xdgStateHome,
    skillsRoot,
  });

  const scopeLabel = isGlobal ? "global" : "project";
  if (state.skills.length === 0) {
    stdout.write(
      `No ${scopeLabel} Flutter skills recorded in ${state.lockPath}.\n` +
        `Run: npx @thiennc/flutter-skills --preset core${isGlobal ? " -g" : ""}\n`,
    );
    return 0;
  }

  let outdatedCount = 0;
  stdout.write(`Installed Flutter skills (${scopeLabel}, target ${targetRef}):\n`);
  for (const item of state.skills) {
    const refLabel = item.ref ?? "unpinned";
    const isCurrent = item.ref === targetRef;
    if (!isCurrent) outdatedCount += 1;
    const statusLabel = isCurrent ? "up to date" : `outdated -> ${targetRef}`;
    stdout.write(`  - ${item.name} (${refLabel}, ${statusLabel})\n`);
  }

  if (outdatedCount > 0) {
    stdout.write(
      `\n${outdatedCount} skill(s) can be updated. Run: npx @thiennc/flutter-skills update${isGlobal ? " -g" : ""}\n`,
    );
  } else {
    stdout.write(`\nAll ${state.skills.length} installed Flutter skill(s) are at ${targetRef}.\n`);
  }
  return 0;
}

function handleUpdate(args, { noTelemetry, options }) {
  const stdout = options.stdout ?? process.stdout;
  const isGlobal = args.includes("-g") || args.includes("--global");
  const force = args.includes("--force") || args.includes("-f");
  const cwd = options.cwd ?? process.cwd();
  const homeDir = options.homeDir ?? homedir();
  const xdgStateHome = options.xdgStateHome ?? process.env.XDG_STATE_HOME;
  const skillsRoot = options.skillsRoot ?? DEFAULT_SKILLS_ROOT;

  const state = readInstalledFlutterSkills({
    global: isGlobal,
    cwd,
    homeDir,
    xdgStateHome,
    skillsRoot,
  });

  if (state.skills.length === 0) {
    const scopeLabel = isGlobal ? "global" : "project";
    stdout.write(`No ${scopeLabel} Flutter skills found to update in ${state.lockPath}.\n`);
    return 0;
  }

  const requestedSkills = [];
  const passthrough = [];
  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === "--force" || arg === "-f") continue;
    if (arg === "-s" || arg === "--skill") {
      let j = i + 1;
      while (j < args.length && !args[j].startsWith("-")) {
        requestedSkills.push(args[j]);
        j += 1;
      }
      i = j - 1;
      continue;
    }
    if (!arg.startsWith("-")) {
      requestedSkills.push(arg);
      continue;
    }
    passthrough.push(arg);
  }

  const installedNames = new Set(state.skills.map((item) => item.name));
  const targets =
    requestedSkills.length > 0
      ? requestedSkills.filter((name) => installedNames.has(name))
      : state.skills
          .filter((item) => force || item.ref !== targetRef)
          .map((item) => item.name);

  if (requestedSkills.length > 0 && targets.length === 0) {
    stdout.write("None of the specified skills are installed from flutter-skills.\n");
    return 1;
  }

  if (targets.length === 0) {
    stdout.write(`All ${state.skills.length} installed Flutter skill(s) are already at ${targetRef}.\n`);
    return 0;
  }

  stdout.write(`Updating ${targets.length} Flutter skill(s) to ${targetRef}...\n`);
  return runUpstream(
    installerArguments(["--skill", ...targets, ...passthrough]),
    { noTelemetry, options },
  );
}

function handleRemove(args, { noTelemetry, options }) {
  const skillsRoot = options.skillsRoot ?? DEFAULT_SKILLS_ROOT;
  const hasAll = args.includes("--all");
  const filtered = args.filter((arg) => arg !== "--all");

  if (!hasAll) {
    return runUpstream(["remove", ...filtered], { noTelemetry, options });
  }

  // Never forward --all to `skills remove`, because upstream deletes skills from every repo.
  const catalogSkills = listCatalogSkills(skillsRoot);
  const removeArgs = ["remove", "--skill", ...catalogSkills, ...filtered];
  if (!filtered.includes("-y") && !filtered.includes("--yes")) {
    removeArgs.push("-y");
  }
  return runUpstream(removeArgs, { noTelemetry, options });
}

export function run(args, options = {}) {
  const stdout = options.stdout ?? process.stdout;
  const stderr = options.stderr ?? process.stderr;
  const cwd = options.cwd ?? process.cwd();
  const skillsRoot = options.skillsRoot ?? DEFAULT_SKILLS_ROOT;

  if (args.includes("--help") || args.includes("-h")) {
    stdout.write(`${helpText()}\n`);
    return 0;
  }
  if (args.includes("--version") || args.includes("-v")) {
    stdout.write(`${packageVersion}\n`);
    return 0;
  }

  const { noTelemetry, remaining } = stripNoTelemetryFlag(args);
  const first = remaining[0];

  if (first === "presets") {
    stdout.write(`${formatPresetsText(skillsRoot)}\n`);
    return 0;
  }

  if (first === "status" || first === "ls") {
    return handleStatus(remaining.slice(1), options);
  }

  if (first === "update" || first === "upgrade") {
    return handleUpdate(remaining.slice(1), { noTelemetry, options });
  }

  if (first === "remove" || first === "rm" || first === "uninstall") {
    return handleRemove(remaining.slice(1), { noTelemetry, options });
  }

  const installArgs = first === "add" || first === "install" || first === "i"
    ? remaining.slice(1)
    : remaining;

  let parsed;
  try {
    parsed = parseInstallOptions(installArgs);
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 1;
  }

  const resolvedSkills = new Set(parsed.skills);
  const regularPresets = [];
  let wantsAuto = parsed.detect;

  for (const raw of parsed.presets) {
    for (const part of String(raw).split(",")) {
      const normalized = part.trim().toLowerCase();
      if (!normalized) continue;
      if (normalized === "auto") {
        wantsAuto = true;
      } else {
        regularPresets.push(normalized);
      }
    }
  }

  if (regularPresets.length > 0) {
    try {
      for (const skill of resolvePresetNames(regularPresets, skillsRoot)) {
        resolvedSkills.add(skill);
      }
    } catch (error) {
      stderr.write(`${error.message}\n`);
      return 1;
    }
  }

  if (wantsAuto) {
    const detected = detectProjectSkills(cwd);
    if (detected.pubspecFiles.length === 0) {
      stdout.write("No pubspec.yaml found; using core essentials.\n");
    } else if (detected.detectedPackages.length > 0) {
      stdout.write(
        `Detected packages (${detected.detectedPackages.join(", ")}) -> selected ${detected.skills.length} skills.\n`,
      );
    } else {
      stdout.write(
        `Found pubspec.yaml (no specialized packages mapped) -> selected ${detected.skills.length} baseline skills.\n`,
      );
    }
    for (const skill of detected.skills) {
      resolvedSkills.add(skill);
    }
  }

  const finalArgs =
    resolvedSkills.size > 0
      ? ["--skill", ...Array.from(resolvedSkills), ...parsed.passthrough]
      : parsed.passthrough;

  return runUpstream(installerArguments(finalArgs), { noTelemetry, options });
}
