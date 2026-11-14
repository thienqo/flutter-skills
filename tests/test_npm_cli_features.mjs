import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  run,
  skillsSource,
  targetRef,
} from "../lib/cli.mjs";
import {
  AUTO_BASELINE_SKILLS,
  PACKAGE_SKILL_MAP,
  detectProjectSkills,
  parsePubspecDependencies,
} from "../lib/detect.mjs";
import {
  PRESETS,
  listCatalogSkills,
  resolvePresetNames,
} from "../lib/presets.mjs";
import {
  readInstalledFlutterSkills,
  repositoryIdentity,
} from "../lib/lockfile.mjs";

function outputCollector() {
  let value = "";
  return {
    stream: { write: (chunk) => (value += chunk) },
    value: () => value,
  };
}

test("all preset and pubspec-mapped skills exist in the skills catalog", () => {
  const catalog = new Set(listCatalogSkills());
  assert.ok(catalog.size >= 40);

  for (const [presetName, skills] of Object.entries(PRESETS)) {
    assert.ok(skills.length > 0, `Preset ${presetName} must not be empty`);
    for (const skill of skills) {
      assert.ok(catalog.has(skill), `Unknown skill "${skill}" in preset "${presetName}"`);
    }
  }

  for (const skill of AUTO_BASELINE_SKILLS) {
    assert.ok(catalog.has(skill), `Unknown skill "${skill}" in AUTO_BASELINE_SKILLS`);
  }

  for (const [pkg, skills] of Object.entries(PACKAGE_SKILL_MAP)) {
    for (const skill of skills) {
      assert.ok(catalog.has(skill), `Unknown skill "${skill}" mapped from package "${pkg}"`);
    }
  }
});

test("expands --preset and merges with --skill without duplicates", () => {
  let invocation;
  const status = run(
    ["--preset", "core,platform", "--skill", "flutter-media", "dart-language", "-y"],
    {
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args, options) => {
        invocation = { command, args, options };
        return { status: 0 };
      },
    },
  );

  assert.equal(status, 0);
  const expectedSkills = Array.from(
    new Set(["flutter-media", "dart-language", ...PRESETS.core, ...PRESETS.platform]),
  );
  assert.deepEqual(invocation.args, [
    "/dependency/skills/bin/cli.mjs",
    "add",
    skillsSource,
    "--skill",
    ...expectedSkills,
    "-y",
  ]);
});

test("rejects unknown presets before starting the upstream installer", () => {
  const err = outputCollector();
  const status = run(["--preset", "nonexistent"], {
    stderr: err.stream,
    spawn: () => {
      throw new Error("installer should not start");
    },
  });

  assert.equal(status, 1);
  assert.match(err.value(), /Unknown preset "nonexistent"/);
});

test("resolves full preset to every catalog skill", () => {
  const resolved = resolvePresetNames(["full"]);
  assert.deepEqual(resolved, listCatalogSkills());
});

test("prints presets catalog without starting the installer", () => {
  const out = outputCollector();
  const status = run(["presets"], {
    stdout: out.stream,
    spawn: () => {
      throw new Error("installer should not start");
    },
  });

  assert.equal(status, 0);
  assert.match(out.value(), /core\s+\(\s*\d+ skills\)/);
  assert.match(out.value(), /auto\s+\(detected\)/);
});

test("parses pubspec.yaml dependencies and detects monorepo skills", () => {
  const deps = parsePubspecDependencies(`
name: sample_app
dependencies:
  flutter:
    sdk: flutter
  dio: ^5.0.0 # networking
  geolocator: ^13.0.0
dev_dependencies:
  mocktail: ^1.0.0
`);
  assert.deepEqual(deps.sort(), ["dio", "flutter", "geolocator", "mocktail"]);

  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-detect-"));
  try {
    mkdirSync(join(tempDir, "packages", "media_kit"), { recursive: true });
    writeFileSync(
      join(tempDir, "pubspec.yaml"),
      "name: root_app\ndependencies:\n  go_router: ^14.0.0\n",
      "utf8",
    );
    writeFileSync(
      join(tempDir, "packages", "media_kit", "pubspec.yaml"),
      "name: media_kit\ndependencies:\n  camera: ^0.11.0\n",
      "utf8",
    );

    const detected = detectProjectSkills(tempDir);
    assert.deepEqual(detected.detectedPackages, ["camera", "go_router"]);
    assert.ok(detected.skills.includes("flutter-media"));
    assert.ok(detected.skills.includes("flutter-navigation"));
    assert.ok(detected.skills.includes("flutter-app-workflow"));

    let invocation;
    const out = outputCollector();
    const status = run(["--preset", "auto", "--agent", "codex"], {
      cwd: tempDir,
      stdout: out.stream,
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args) => {
        invocation = { command, args };
        return { status: 0 };
      },
    });
    assert.equal(status, 0);
    assert.match(out.value(), /Detected packages \(camera, go_router\)/);
    assert.ok(invocation.args.includes("flutter-media"));
    assert.ok(invocation.args.includes("--agent"));
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("status reports installed Flutter skills and detects outdated refs", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-status-"));
  try {
    writeFileSync(
      join(tempDir, "skills-lock.json"),
      JSON.stringify({
        version: 1,
        skills: {
          "dart-language": { source: "thienqo/flutter-skills", ref: targetRef },
          "flutter-media": { source: "thienqo/flutter-skills", ref: "v0.13.0" },
          "other-skill": { source: "vercel-labs/skills", ref: "main" },
        },
      }),
      "utf8",
    );

    const out = outputCollector();
    const status = run(["status"], {
      cwd: tempDir,
      stdout: out.stream,
      spawn: () => {
        throw new Error("installer should not start");
      },
    });

    assert.equal(status, 0);
    assert.match(out.value(), /dart-language.*up to date/);
    assert.match(out.value(), new RegExp(`flutter-media.*outdated -> ${targetRef}`));
    assert.doesNotMatch(out.value(), /other-skill/);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("update upgrades only outdated Flutter skills in lockfile", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-update-"));
  try {
    mkdirSync(join(tempDir, ".agents"), { recursive: true });
    writeFileSync(
      join(tempDir, ".agents", ".skill-lock.json"),
      JSON.stringify({
        version: 3,
        skills: {
          "dart-language": { source: "thienqo/flutter-skills", ref: targetRef },
          "flutter-media": { source: "thienqo/flutter-skills", ref: "v0.13.0" },
          "other-skill": { source: "vercel-labs/skills", ref: "main" },
        },
      }),
      "utf8",
    );

    let invocation;
    const out = outputCollector();
    const status = run(["update", "-g", "-y"], {
      homeDir: tempDir,
      stdout: out.stream,
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args) => {
        invocation = { command, args };
        return { status: 0 };
      },
    });

    assert.equal(status, 0);
    assert.deepEqual(invocation.args, [
      "/dependency/skills/bin/cli.mjs",
      "add",
      skillsSource,
      "--skill",
      "flutter-media",
      "-g",
      "-y",
    ]);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("update keeps option values when forwarding to the installer", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-update-agent-"));
  try {
    writeFileSync(
      join(tempDir, "skills-lock.json"),
      JSON.stringify({
        version: 3,
        skills: {
          "dart-language": { source: "thienqo/flutter-skills", ref: "v0.13.0" },
        },
      }),
      "utf8",
    );

    let invocation;
    const status = run(["update", "--agent", "codex", "-y"], {
      cwd: tempDir,
      stdout: outputCollector().stream,
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args) => {
        invocation = { command, args };
        return { status: 0 };
      },
    });

    assert.equal(status, 0);
    assert.deepEqual(invocation.args, [
      "/dependency/skills/bin/cli.mjs",
      "add",
      skillsSource,
      "--skill",
      "dart-language",
      "--agent",
      "codex",
      "-y",
    ]);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("update rejects names that are not installed from this package", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-update-unknown-"));
  try {
    writeFileSync(
      join(tempDir, "skills-lock.json"),
      JSON.stringify({
        skills: { "dart-language": { source: "thienqo/flutter-skills", ref: targetRef } },
      }),
      "utf8",
    );

    const out = outputCollector();
    const status = run(["update", "deprecated-flutter-skill"], {
      cwd: tempDir,
      stdout: out.stream,
      spawn: () => {
        throw new Error("installer should not start");
      },
    });

    assert.equal(status, 1);
    assert.match(out.value(), /Not installed from flutter-skills: deprecated-flutter-skill/);
    assert.match(out.value(), /Installed skills: dart-language/);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("remove --all removes only lockfile-owned skills and keeps confirmation", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-remove-all-"));
  try {
    writeFileSync(
      join(tempDir, "skills-lock.json"),
      JSON.stringify({
        skills: {
          "dart-language": { source: "thienqo/flutter-skills", ref: "v0.13.0" },
          "flutter-media": {
            sourceUrl: "https://github.com/thienqo/flutter-skills#v0.13.0",
            ref: "v0.13.0",
          },
          "someone-else-skill": { source: "someone/flutter-skills-fork", ref: "main" },
          "extra-skill": { source: "thienqo/flutter-skills-extra", ref: "main" },
        },
      }),
      "utf8",
    );

    let invocation;
    const status = run(["remove", "--all"], {
      cwd: tempDir,
      stdout: outputCollector().stream,
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args) => {
        invocation = { command, args };
        return { status: 0 };
      },
    });

    assert.equal(status, 0);
    assert.equal(invocation.args[1], "remove");
    assert.equal(invocation.args[2], "--skill");
    assert.deepEqual(invocation.args.slice(3), ["dart-language", "flutter-media"]);
    assert.ok(!invocation.args.includes("--all"));
    assert.ok(!invocation.args.includes("-y"));
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("remove --all forwards an explicit -y flag", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-remove-all-yes-"));
  try {
    writeFileSync(
      join(tempDir, "skills-lock.json"),
      JSON.stringify({
        skills: { "dart-language": { source: "thienqo/flutter-skills", ref: "v0.13.0" } },
      }),
      "utf8",
    );

    let invocation;
    const status = run(["remove", "--all", "-y"], {
      cwd: tempDir,
      stdout: outputCollector().stream,
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args) => {
        invocation = { command, args };
        return { status: 0 };
      },
    });

    assert.equal(status, 0);
    assert.deepEqual(invocation.args.slice(1), ["remove", "--skill", "dart-language", "-y"]);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("remove --all reads the global lockfile and forwards -g", () => {
  const homeDir = mkdtempSync(join(tmpdir(), "flutter-skills-remove-global-"));
  const projectDir = mkdtempSync(join(tmpdir(), "flutter-skills-remove-global-cwd-"));
  try {
    mkdirSync(join(homeDir, ".agents"), { recursive: true });
    writeFileSync(
      join(homeDir, ".agents", ".skill-lock.json"),
      JSON.stringify({
        skills: {
          "dart-language": { source: "thienqo/flutter-skills", ref: "v0.13.0" },
          "someone-else-skill": { source: "someone/flutter-skills-fork", ref: "main" },
        },
      }),
      "utf8",
    );

    let invocation;
    const status = run(["remove", "--all", "-g"], {
      cwd: projectDir,
      homeDir,
      stdout: outputCollector().stream,
      cliPath: "/dependency/skills/bin/cli.mjs",
      nodePath: "/node",
      spawn: (command, args) => {
        invocation = { command, args };
        return { status: 0 };
      },
    });

    assert.equal(status, 0);
    assert.deepEqual(invocation.args.slice(1), ["remove", "--skill", "dart-language", "-g"]);
  } finally {
    rmSync(homeDir, { recursive: true, force: true });
    rmSync(projectDir, { recursive: true, force: true });
  }
});

test("remove --all without owned skills does not start the installer", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-remove-all-empty-"));
  try {
    const out = outputCollector();
    const status = run(["remove", "--all"], {
      cwd: tempDir,
      stdout: out.stream,
      spawn: () => {
        throw new Error("installer should not start");
      },
    });

    assert.equal(status, 0);
    assert.match(out.value(), /No project Flutter skills found to remove/);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("lockfile ownership distinguishes exact repositories from similar names", () => {
  const tempDir = mkdtempSync(join(tmpdir(), "flutter-skills-ownership-"));
  try {
    writeFileSync(
      join(tempDir, "skills-lock.json"),
      JSON.stringify({
        skills: {
          "dart-language": { source: "thienqo/flutter-skills", ref: "v1" },
          "flutter-media": {
            sourceUrl: "https://github.com/thienqo/flutter-skills#v1",
            ref: "v1",
          },
          "clone-skill": { source: "someone/flutter-skills-fork", ref: "v1" },
          "extra-skill": { source: "thienqo/flutter-skills-extra", ref: "v1" },
          "lab-skill": { source: "https://github.com/thienqo/flutter-skills-lab", ref: "v1" },
        },
      }),
      "utf8",
    );

    const state = readInstalledFlutterSkills({ cwd: tempDir });
    assert.deepEqual(state.skills.map((skill) => skill.name), [
      "dart-language",
      "flutter-media",
    ]);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test("repositoryIdentity normalizes supported source spellings", () => {
  assert.equal(repositoryIdentity("thienqo/flutter-skills"), "thienqo/flutter-skills");
  assert.equal(
    repositoryIdentity("https://github.com/thienqo/flutter-skills#v0.15.0"),
    "thienqo/flutter-skills",
  );
  assert.equal(
    repositoryIdentity("git@github.com:thiennc-tesoglobal/flutter-skills.git"),
    "thiennc-tesoglobal/flutter-skills",
  );
  assert.equal(repositoryIdentity("thienqo/flutter-skills-extra"), "thienqo/flutter-skills-extra");
  assert.equal(repositoryIdentity(""), null);
  assert.equal(repositoryIdentity(null), null);
});

test("passes DISABLE_TELEMETRY=1 when --no-telemetry is set", () => {
  let spawnOptions;
  const status = run(["--no-telemetry", "--agent", "codex"], {
    cliPath: "/dependency/skills/bin/cli.mjs",
    nodePath: "/node",
    env: { PATH: "/usr/bin" },
    spawn: (_command, _args, options) => {
      spawnOptions = options;
      return { status: 0 };
    },
  });

  assert.equal(status, 0);
  assert.equal(spawnOptions.env.DISABLE_TELEMETRY, "1");
  assert.equal(spawnOptions.env.PATH, "/usr/bin");
});
