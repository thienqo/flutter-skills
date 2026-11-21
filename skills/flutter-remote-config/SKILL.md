---
name: flutter-remote-config
description: Implement or review Flutter remote config and feature flags — typed contracts, defaults, fetch/activation, targeting, rollout, kill switches, offline fallback, verification. Use for config behavior; not analytics or entitlements.
---

# Flutter Remote Config

Remote configuration is untrusted runtime input, not authority. Preserve the project's provider, transport, state architecture, and release process unless migration is requested. Do not enable collection, change live targeting, flip production flags, or alter console configuration without explicit authorization.

## Preflight

Read the project before proposing behavior:

- `pubspec.yaml` and lockfile: which provider and version, and which platforms the plugin actually supports.
- Existing config wrapper, initialization order, environments, and where values are consumed.
- Current key inventory, owners, defaults, conditions or audiences, rollout percentages, and kill-switch ownership.
- App-version policy: which code paths exist in the oldest supported release.
- Consent, privacy, and logging rules that apply to config reads.

State the key set, the default for each key, the behavior when fetching fails, and who can change live targeting. Treat any missing owner statement as an assumption to confirm, not as permission to invent policy.

## Load references conditionally

- Read [config contracts and defaults](references/config-contracts-and-defaults.md) for typed parsing, in-app defaults, schema evolution, payload bounds, and what must never live in config.
- Read [targeting, rollout, and boundaries](references/targeting-rollout-and-boundaries.md) for conditions and audiences, staged rollout, version gating, kill switches, and why config is never an authorization or entitlement source.
- Read [fetch, activation, and verification](references/fetch-activation-and-verification.md) for fetch versus activate semantics, throttling and minimum intervals, real-time limits, offline fallback, and per-boundary evidence.

## Boundaries

- `flutter-product-analytics` owns experiment exposure and outcome events. A config read is not an exposure.
- `flutter-in-app-purchases` and `flutter-payments-checkout` own verified entitlements and payment truth; config may reflect their outcome but never grants access.
- `flutter-security` owns secrets and broad threat review; a remote-config value is client-readable.
- `flutter-observability` owns logs and traces; do not log full config payloads or targeting attributes.
- `flutter-build-release` and `flutter-ci-cd` own app builds and store delivery; config cannot ship native code or bypass a release.
- `flutter-architecture` owns where configuration is injected and owned; `flutter-state-management` owns reactive state. A flag is not a state-management design.

## Rules

1. **Default every key.** Ship an in-app default for each key and define behavior when the fetch fails, the device is offline, the payload is malformed, or the value is out of range. Never block the first frame or a critical path on a network fetch.
2. **Parse into a bounded contract.** Convert raw strings into validated types, enums, and ranges with a fallback; ignore unknown keys; cap payload size and depth; never `eval` or execute config content.
3. **Fetch and activate at defined boundaries.** Choose launch or next-session activation, or a user-initiated foreground refresh, instead of fetching inside `build`, incidental gesture handlers, or a mid-interaction screen. Respect the provider's minimum fetch interval and throttling; never build fetch loops.
4. **Target deliberately.** Use provider audiences and user properties; keep targeting attributes minimal. Never use config for authorization, entitlement, pricing truth, or safety-critical decisions, and gate new UI behind both the flag and the app version that contains it.
5. **Make changes reversible.** Staged rollout needs a documented percentage, audience, stop condition, and rollback; every kill switch must be tested in the same environment that would raise it. A change that cannot be rolled back is a release, not a config change.
6. **Keep secrets and PII out.** Config keys and values are readable by the client instance. Credentials, tokens, personal data, and access rules belong to a trusted backend or the owning domain.
7. **Verify per boundary.** Test defaults, offline, malformed values, activation timing, targeting, and version gating deterministically. A console value or a local print is not end-to-end proof.

## Verification

- Deterministic tests with a fake config source: default values, fetch failure and offline path, invalid or missing keys, activation before and after the boundary, version-gated rollout, and kill switch.
- A test that asserts no secret, token, or personal data appears in any config value or its logs.
- Real evidence only in an authorized non-production project: confirm the audience or rollout actually evaluates, and that the app's behavior changes as intended. Report the console, client, and downstream observations separately, and state which are unverified.
