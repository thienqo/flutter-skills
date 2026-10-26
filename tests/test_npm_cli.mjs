import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import test from "node:test";

import {
  helpText,
  installerArguments,
  packageVersion,
  resolveSkillsCli,
  run,
  skillsSource,
} from "../lib/cli.mjs";

function outputCollector() {
  let value = "";
  return {
    stream: { write: (chunk) => (value += chunk) },
    value: () => value,
  };
}

test("pins installs to the GitHub tag matching the npm version", () => {
  assert.equal(
    skillsSource,
    `https://github.com/thienqo/flutter-skills#v${packageVersion}`,
  );
  assert.deepEqual(installerArguments(["--skill", "flutter-ui-design"]), [
    "add",
    skillsSource,
    "--skill",
    "flutter-ui-design",
  ]);
});

test("resolves the pinned upstream executable from package dependencies", () => {
  assert.equal(existsSync(resolveSkillsCli()), true);
});

test("forwards installer options without invoking a shell", () => {
  let invocation;
  const status = run(["--agent", "codex", "--global"], {
    cliPath: "/dependency/skills/bin/cli.mjs",
    nodePath: "/node",
    spawn: (command, args, options) => {
      invocation = { command, args, options };
      return { status: 0 };
    },
  });

  assert.equal(status, 0);
  assert.deepEqual(invocation, {
    command: "/node",
    args: [
      "/dependency/skills/bin/cli.mjs",
      "add",
      skillsSource,
      "--agent",
      "codex",
      "--global",
    ],
    options: { stdio: "inherit" },
  });
});

test("prints wrapper help and version without starting the installer", () => {
  const helpOutput = outputCollector();
  const versionOutput = outputCollector();
  const failIfSpawned = () => {
    throw new Error("installer should not start");
  };

  assert.equal(run(["--help"], { stdout: helpOutput.stream, spawn: failIfSpawned }), 0);
  assert.match(helpOutput.value(), /npx @thiennc\/flutter-skills/);
  assert.equal(helpOutput.value(), `${helpText()}\n`);

  assert.equal(
    run(["--version"], { stdout: versionOutput.stream, spawn: failIfSpawned }),
    0,
  );
  assert.equal(versionOutput.value(), `${packageVersion}\n`);
});

test("executable entrypoint reports the package version", () => {
  const result = spawnSync(process.execPath, ["bin/flutter-skills.mjs", "--version"], {
    cwd: new URL("..", import.meta.url),
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), packageVersion);
});

test("returns a failure when the upstream process cannot start", () => {
  const errorOutput = outputCollector();
  const status = run([], {
    cliPath: "/missing/skills.mjs",
    stderr: errorOutput.stream,
    spawn: () => ({ error: new Error("not found"), status: null }),
  });

  assert.equal(status, 1);
  assert.match(errorOutput.value(), /Unable to start the skills installer: not found/);
});
