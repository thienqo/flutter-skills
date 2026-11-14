import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

const require = createRequire(import.meta.url);
const packageMetadata = JSON.parse(
  readFileSync(new URL("../package.json", import.meta.url), "utf8"),
);

export const packageVersion = packageMetadata.version;
export const repository = "thienqo/flutter-skills";
export const skillsSource = `https://github.com/${repository}#v${packageVersion}`;

export function installerArguments(args) {
  return ["add", skillsSource, ...args];
}

export function helpText() {
  return `Flutter Skills ${packageVersion}

Usage:
  npx @thiennc/flutter-skills [options]

Options:
  -s, --skill <skills>   Install selected skills
  -a, --agent <agents>   Install for selected agents
  -g, --global           Install at user level
  -l, --list             List available skills
  -y, --yes              Skip confirmation prompts
      --all              Install every skill for every agent
  -h, --help             Show this help
  -v, --version          Show the wrapper version

All installation options are forwarded to skills@${packageMetadata.dependencies.skills}.
Source: ${skillsSource}`;
}

export function resolveSkillsCli() {
  const packagePath = require.resolve("skills/package.json");
  return join(dirname(packagePath), "bin", "cli.mjs");
}

export function run(args, options = {}) {
  const stdout = options.stdout ?? process.stdout;
  const stderr = options.stderr ?? process.stderr;

  if (args.includes("--help") || args.includes("-h")) {
    stdout.write(`${helpText()}\n`);
    return 0;
  }
  if (args.includes("--version") || args.includes("-v")) {
    stdout.write(`${packageVersion}\n`);
    return 0;
  }

  const spawn = options.spawn ?? spawnSync;
  const cliPath = options.cliPath ?? resolveSkillsCli();
  const nodePath = options.nodePath ?? process.execPath;
  const result = spawn(nodePath, [cliPath, ...installerArguments(args)], {
    stdio: "inherit",
  });

  if (result.error) {
    stderr.write(`Unable to start the skills installer: ${result.error.message}\n`);
    return 1;
  }
  return Number.isInteger(result.status) ? result.status : 1;
}
