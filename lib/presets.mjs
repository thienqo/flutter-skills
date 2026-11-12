import { readdirSync } from "node:fs";

export const DEFAULT_SKILLS_ROOT = new URL("../skills", import.meta.url);

export const PRESETS = {
  core: [
    "flutter-app-workflow",
    "dart-language",
    "dart-concurrency",
    "flutter-architecture",
    "flutter-state-management",
    "flutter-navigation",
    "flutter-ui-patterns",
    "flutter-testing",
    "flutter-code-review",
  ],
  ui: [
    "flutter-ui-design",
    "flutter-figma-workflow",
    "flutter-visual-effects",
    "flutter-ui-patterns",
    "flutter-responsive-layout",
    "flutter-text-rendering",
    "flutter-animation",
    "flutter-accessibility",
    "flutter-localization",
  ],
  data: [
    "flutter-networking",
    "flutter-openapi-client",
    "flutter-persistence",
    "flutter-authentication",
    "flutter-security",
    "flutter-ai-integration",
    "flutter-location-maps",
    "flutter-media",
    "flutter-webview",
  ],
  ship: [
    "flutter-device-testing",
    "flutter-runtime-debugging",
    "flutter-performance",
    "flutter-observability",
    "flutter-product-analytics",
    "flutter-build-release",
    "flutter-ci-cd",
    "flutter-dependency-upgrades",
    "flutter-in-app-purchases",
    "flutter-payments-checkout",
  ],
  platform: [
    "flutter-background-execution",
    "flutter-platform-integration",
    "flutter-package-development",
    "flutter-notifications",
  ],
};

export const PRESET_DESCRIPTIONS = {
  core: "Daily Flutter essentials (workflow, Dart 3, architecture, state, navigation, UI patterns, testing, review)",
  ui: "UI design, Figma translation, visual effects, responsive layout, text, animation, accessibility, localization",
  data: "Networking, OpenAPI, persistence, auth, security, AI, location/maps, media, WebView",
  ship: "Device testing, debugging, performance, observability, analytics, release, CI/CD, upgrades, IAP/checkout",
  platform: "Background execution, native bridges, package development, push/local notifications",
  full: "All skills in the catalog",
  auto: "Core essentials plus specialists detected from pubspec.yaml",
};

export function listCatalogSkills(skillsRoot = DEFAULT_SKILLS_ROOT) {
  return readdirSync(skillsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && !entry.name.startsWith("."))
    .map((entry) => entry.name)
    .sort();
}

export function resolvePresetNames(rawPresets, skillsRoot = DEFAULT_SKILLS_ROOT) {
  const names = rawPresets
    .flatMap((value) => String(value).split(","))
    .map((value) => value.trim().toLowerCase())
    .filter(Boolean);

  if (names.length === 0) {
    throw new Error("Missing preset name.");
  }

  const validNames = [...Object.keys(PRESETS), "full"];
  const selected = new Set();

  for (const name of names) {
    if (name === "full") {
      for (const skill of listCatalogSkills(skillsRoot)) {
        selected.add(skill);
      }
      continue;
    }
    const preset = PRESETS[name];
    if (!preset) {
      throw new Error(
        `Unknown preset "${name}". Available presets: ${validNames.join(", ")}, auto.`,
      );
    }
    for (const skill of preset) {
      selected.add(skill);
    }
  }

  return Array.from(selected);
}
