import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { PRESETS } from "./presets.mjs";

export const AUTO_BASELINE_SKILLS = [
  ...PRESETS.core,
  "flutter-responsive-layout",
  "flutter-performance",
  "flutter-security",
];

export const PACKAGE_SKILL_MAP = {
  agora_rtc_engine: ["flutter-media"],
  amplitude_flutter: ["flutter-product-analytics"],
  appauth: ["flutter-authentication"],
  audio_service: ["flutter-media"],
  audioplayers: ["flutter-media"],
  auto_route: ["flutter-navigation"],
  awesome_notifications: ["flutter-notifications"],
  background_fetch: ["flutter-background-execution"],
  beamer: ["flutter-navigation"],
  bloc: ["flutter-state-management"],
  braintree: ["flutter-payments-checkout"],
  camera: ["flutter-media"],
  chewie: ["flutter-media"],
  chopper: ["flutter-networking"],
  dart_openai: ["flutter-ai-integration"],
  datadog_flutter_plugin: ["flutter-observability"],
  dio: ["flutter-networking"],
  drift: ["flutter-persistence"],
  easy_localization: ["flutter-localization"],
  ferry: ["flutter-networking"],
  ffi: ["flutter-platform-integration"],
  ffigen: ["flutter-platform-integration"],
  firebase_ai: ["flutter-ai-integration"],
  firebase_analytics: ["flutter-product-analytics"],
  firebase_auth: ["flutter-authentication"],
  firebase_crashlytics: ["flutter-observability"],
  firebase_messaging: ["flutter-notifications"],
  flutter_ai_toolkit: ["flutter-ai-integration"],
  flutter_animate: ["flutter-animation"],
  flutter_appauth: ["flutter-authentication"],
  flutter_background_service: ["flutter-background-execution"],
  flutter_bloc: ["flutter-state-management"],
  flutter_inappwebview: ["flutter-webview"],
  flutter_local_notifications: ["flutter-notifications"],
  flutter_localizations: ["flutter-localization"],
  flutter_map: ["flutter-location-maps"],
  flutter_riverpod: ["flutter-state-management"],
  flutter_secure_storage: ["flutter-security", "flutter-authentication"],
  flutter_stripe: ["flutter-payments-checkout"],
  flutter_webrtc: ["flutter-media"],
  freezed: ["dart-language"],
  geocoding: ["flutter-location-maps"],
  geolocator: ["flutter-location-maps"],
  get: ["flutter-state-management"],
  go_router: ["flutter-navigation"],
  golden_toolkit: ["flutter-testing"],
  google_generative_ai: ["flutter-ai-integration"],
  google_maps_flutter: ["flutter-location-maps"],
  google_sign_in: ["flutter-authentication"],
  graphql_flutter: ["flutter-networking"],
  hive: ["flutter-persistence"],
  hive_flutter: ["flutter-persistence"],
  hooks_riverpod: ["flutter-state-management"],
  http: ["flutter-networking"],
  image_picker: ["flutter-media"],
  in_app_purchase: ["flutter-in-app-purchases"],
  intl: ["flutter-localization"],
  isar: ["flutter-persistence"],
  json_serializable: ["dart-language"],
  just_audio: ["flutter-media"],
  livekit_client: ["flutter-media"],
  local_auth: ["flutter-authentication", "flutter-security"],
  location: ["flutter-location-maps"],
  lottie: ["flutter-animation"],
  mapbox_maps_flutter: ["flutter-location-maps"],
  media_kit: ["flutter-media"],
  mixpanel_flutter: ["flutter-product-analytics"],
  mobile_scanner: ["flutter-media"],
  mockito: ["flutter-testing"],
  mocktail: ["flutter-testing"],
  objectbox: ["flutter-persistence"],
  onesignal_flutter: ["flutter-notifications"],
  openapi_generator: ["flutter-openapi-client"],
  opentelemetry: ["flutter-observability"],
  patrol: ["flutter-testing", "flutter-device-testing"],
  pay: ["flutter-payments-checkout"],
  pigeon: ["flutter-platform-integration"],
  posthog_flutter: ["flutter-product-analytics"],
  provider: ["flutter-state-management"],
  purchases_flutter: ["flutter-in-app-purchases"],
  qr_code_scanner: ["flutter-media"],
  record: ["flutter-media"],
  retrofit: ["flutter-networking"],
  rive: ["flutter-animation"],
  riverpod: ["flutter-state-management"],
  sentry_flutter: ["flutter-observability"],
  shared_preferences: ["flutter-persistence"],
  sign_in_with_apple: ["flutter-authentication"],
  slang: ["flutter-localization"],
  socket_io_client: ["flutter-networking"],
  sqflite: ["flutter-persistence"],
  supabase_flutter: ["flutter-authentication"],
  swagger_parser: ["flutter-openapi-client"],
  video_player: ["flutter-media"],
  web_socket_channel: ["flutter-networking"],
  webview_flutter: ["flutter-webview"],
  workmanager: ["flutter-background-execution"],
};

const DEPENDENCY_SECTION_NAMES = new Set([
  "dependencies",
  "dev_dependencies",
  "dependency_overrides",
]);

export function parsePubspecDependencies(yamlContent) {
  const packages = new Set();
  let inSection = false;
  let sectionIndent = null;

  for (const rawLine of yamlContent.split(/\r?\n/)) {
    const withoutComment = rawLine.replace(/#.*$/, "");
    if (!withoutComment.trim()) continue;

    const indent = withoutComment.match(/^(\s*)/)[1].length;
    const trimmed = withoutComment.trim();

    if (indent === 0) {
      const topMatch = trimmed.match(/^([A-Za-z0-9_]+)\s*:/);
      inSection = Boolean(topMatch && DEPENDENCY_SECTION_NAMES.has(topMatch[1]));
      sectionIndent = null;
      continue;
    }

    if (!inSection) continue;

    if (sectionIndent === null) {
      sectionIndent = indent;
    }
    if (indent !== sectionIndent) continue;

    const depMatch = trimmed.match(/^([A-Za-z0-9_]+)\s*:/);
    if (depMatch) {
      packages.add(depMatch[1]);
    }
  }

  return Array.from(packages);
}

export function findPubspecFiles(cwd = process.cwd()) {
  const found = [];
  const rootPubspec = join(cwd, "pubspec.yaml");
  if (existsSync(rootPubspec)) {
    found.push(rootPubspec);
  }

  for (const container of ["apps", "packages"]) {
    const containerDir = join(cwd, container);
    if (!existsSync(containerDir)) continue;
    try {
      for (const entry of readdirSync(containerDir, { withFileTypes: true })) {
        if (!entry.isDirectory() || entry.name.startsWith(".")) continue;
        const nestedPubspec = join(containerDir, entry.name, "pubspec.yaml");
        if (existsSync(nestedPubspec)) {
          found.push(nestedPubspec);
        }
      }
    } catch {
      // Ignore unreadable directories.
    }
  }

  return found;
}

export function detectProjectSkills(cwd = process.cwd()) {
  const pubspecFiles = findPubspecFiles(cwd);
  const detectedPackages = new Set();
  const skills = new Set(AUTO_BASELINE_SKILLS);

  for (const filePath of pubspecFiles) {
    try {
      const content = readFileSync(filePath, "utf8");
      for (const pkg of parsePubspecDependencies(content)) {
        if (PACKAGE_SKILL_MAP[pkg]) {
          detectedPackages.add(pkg);
          for (const skill of PACKAGE_SKILL_MAP[pkg]) {
            skills.add(skill);
          }
        }
      }
    } catch {
      // Ignore unreadable pubspec files.
    }
  }

  return {
    pubspecFiles,
    detectedPackages: Array.from(detectedPackages).sort(),
    skills: Array.from(skills),
  };
}
