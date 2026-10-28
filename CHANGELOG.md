# Changelog

## Unreleased

- Require the `flutter-webview` navigation policy to state explicit scheme, host, port, and path conditions per outcome and to cover redirect hops, popups, back handling, and load failures with automated tests instead of a manual device checklist. The `origin-policy-does-not-use-string-prefixes` case moved from 75, 58, and 62 across three runs to 88, 82, 88, and 88 across four.
- Require `flutter-product-analytics` to state the full event contract (identity, consent behavior, delivery semantics, retry and restart rule) with labeled conservative defaults instead of asking the user or deferring to the adapter. The `widget-rebuilds-do-not-own-business-events` case moved from 74, 72, and 62 across three runs to 96, 96, and 93.
- Tell `flutter-ui-patterns` to split files by responsibility, keep small single-use private widgets in their screen's file, and give a widget its own file only when it is reused, holds isolated state, or is tested alone. The `cohesive-widget-composition` case moved from 70, 62, and 35 across three runs to 96, 92, and 88.

## 0.11.0 - 2026-10-26

- Add a `flutter-device-testing` semantic UI inspection reference for driving a running app through the platform accessibility tree (`idb`, `uiautomator`) instead of repeated screenshots, re-reading after every action, preferring `Semantics(identifier:)` over coordinates, and diagnosing an empty Flutter semantics tree with a debug-only entrypoint. Approach adapted from conorluddy/ios-simulator-skill (MIT).
- Add appearance, text-size, status-bar or System UI demo-mode, and read-only persisted-data inspection commands with restore rules to the iOS Simulator and Android emulator references.
- Add two behavior cases (218 to 220), including a mandatory check that an empty semantics tree is not silently replaced by coordinate taps.
- Require the semantic inspection reference to diagnose an empty Flutter semantics tree before offering a labeled coordinate-tap fallback, even when the user asks for a pixel tap, and route new `Semantics(identifier:)` work to `flutter-accessibility`. The measured case moved from 35 with a mandatory failure to 96.
- Mark secret-handling, authorization, production-probing, fork-isolation, and no-publication expectations in `flutter-security` and `flutter-ci-cd` as mandatory.
- Add four routing boundaries (72 to 76): a frozen UI that is not jank, production cold-start signals that are not local profiling, a Figma node that contains a glass effect, and a blur added without redesign.
- Point repository, marketplace, plugin, npm metadata, CLI, and README install commands at `thienqo/flutter-skills` after the repository moved from `thiennc-tesoglobal`. The npm package `@thiennc/flutter-skills` and the Tessl plugin `thiennc-tesoglobal/flutter-skills` keep their registry names.

## 0.10.0 - 2026-10-05

- Complete `flutter-app-workflow` specialist routing so every relevant skill is named explicitly, and restructure its preflight into a checklist.
- Add concrete, attributed interventions to `flutter-performance` (repaint and rebuild scope, decode-size image caching, lazy builders, shader warm-up, isolate cost) and record the rendering backend when comparing traces.
- Add Riverpod and Bloc disposal and async-state pitfalls to `flutter-state-management`.
- Add `build_runner`, `freezed`, and `json_serializable` code-generation guidance to `dart-language`, covering regeneration instead of hand-editing generated files.
- Deepen `flutter-architecture` (no second DI container over an existing provider graph; map data-source types to domain models inside repositories), `flutter-navigation` (auth-driven `refreshListenable` redirects; `parentNavigatorKey` for routes that cover shell chrome), `flutter-animation` (`AnimatedSwitcher` identity; reusing designer-delivered Lottie or Rive assets), and `flutter-localization` (full CLDR plural categories; directional insets and alignment for RTL).
- Point `flutter-runtime-debugging`, `flutter-dependency-upgrades`, and `flutter-code-review` at the Dart and Flutter MCP server, fix two stale Flutter documentation URLs, and remove copy-pasted credential filler sentences.
- Add 15 behavior eval cases (203 to 218) while keeping reference coverage at 100%.

## 0.9.1 - 2026-09-30

- Add a Flutter 3.44.8 responsive checkout fixture with six viewport, breakpoint, text-scale, RTL, keyboard, geometry, and interaction scenarios; verify seeded overlap, missing wide composition, clipping, sticky-action, and offscreen-action failures against a passing oracle in CI.
- Add a compiler-backed responsive-layout case and ignore generated Flutter build caches while retaining package metadata integrity checks in executable evaluations.
- Redact lifecycle output before truncation so report boundaries cannot expose tokens or device identifiers; add regression checks for normal and timeout output.
- Correct Hero tag matching, Flutter web isolate limits, view-aware accessibility announcements, and text wrapping guidance; repair the TextOverflow source link.
- Add three behavior regressions, strengthen Hero flight verification, and make authentication and purchase correctness constraints mandatory.
- Harden `flutter-persistence` with resolved-package preflight, explicit durable-data classification, ordered skipped-version migrations, atomic failure recovery, and prior-release fixture verification.
- Add a mandatory migration-safety behavior case and two routing boundaries separating local schema evolution from remote OpenAPI contract changes.

## 0.9.0 - 2026-09-13

- Extend npm registry propagation verification to three minutes so a successful trusted publish is not reported as failed while npm is still processing the package.
- Harden `flutter-code-review` with compatibility proof obligations, adversarial safety-boundary checks, large-diff coverage tracking, and a final false-positive and duplication filter.
- Add three behavior cases and three routing cases covering report-schema compatibility, redaction order, large-diff completeness, review self-critique, and specialist scope boundaries.
- Expand `flutter-device-testing` with Android Emulator and iOS Simulator operation references, explicit native-system-UI automation boundaries, readiness checks, safe target ownership, focused evidence, and physical-hardware verification limits.
- Add lifecycle matrix version 2 with target and installed-app preflight, mandatory warm-state preconditions, safe target labels, opt-in device identifier retention, execution context, and version 1 compatibility.
- Add five device behavior cases and two routing cases covering target readiness, native permission dialogs, Simulator override cleanup, physical evidence boundaries, and warm-state correctness.
- Retain focused warm-state forward-evaluation results covering cleanup, bounded precondition, and schema-contract gaps plus the corrected outcome.
- Correct `flutter-text-rendering` flex guidance so constraints and truncation follow the failing axis and content contract instead of wrapping every text node mechanically.
- Document production ownership and disposal for inline gesture recognizers and include the ambient locale in localized `TextPainter` measurement.
- Add two behavior-focused regression cases for unbounded column flex and inline recognizer lifecycle handling.

## 0.8.0 - 2026-09-12

- Add multi-judge forward evaluation with strict mandatory gating, per-criterion agreement, score-range reporting, and backward-compatible primary judgment fields.
- Add hash-bound human-review sampling and per-judge human agreement summaries.
- Add a constrained executable-evaluation runner and a measured Dart concurrency fixture that verifies formatting, analysis, and runtime behavior without allowing test edits.
- Add PR, nightly all-skill, and full-release benchmark profiles, a Codex-only default matrix, and an optional Codex/Claude cross-judge matrix.
- Add a bounded post-implementation review loop to `flutter-app-workflow` and allow `flutter-code-review` to assess completed delivery work before completion.
- Require an evidence-based understanding gate before implementation, focused clarification for material ambiguity, and an impact map that keeps affected out-of-scope consumers visible without silently expanding the change.
- Add a clean-implementation gate that removes temporary residue and unintended churn, preserves strong regression assertions, and inspects the final diff after formatter, analyzer, lint, and test checks pass.
- Expand API evidence evaluations for absent, null, wrong-type, error-envelope, and environment-specific contract drift without weakening domain models or overstating live verification.
- Add replayable deep-link and notification lifecycle matrices covering cold/warm entry, authentication, Back behavior, obscured destinations, delayed APIs, account changes, and duplicate listeners.
- Add a shell-free lifecycle matrix runner with dry-run planning, bounded execution, cleanup, redacted JSON evidence, and Android/iOS trigger support.
- Harden accessibility test cleanup, rapid stream re-trigger ownership, asynchronous integration-test startup, and locale-aware orphan handling.
- Add 14 behavior-focused evaluation cases for understanding, impact, clean-code review, API, navigation, notification, device testing, accessibility, concurrency, and text rendering behavior.

## 0.7.0 - 2026-09-09

- Add ticket-first scope locking, correct branch-base selection, scoped ticket-linked commits, explicit push authorization, and protection against committing installed skill artifacts to `flutter-app-workflow`.
- Separate documented API contracts and examples from mock fixtures and observed server responses across `flutter-networking` and `flutter-openapi-client`, including redacted drift evidence and bounded compatibility handling.
- Require verification reports to identify both the execution surface and data source so simulator, physical-device, mock, and real-service claims remain precise.
- Harden `flutter-testing` with an ownership-aware disposable-test lifecycle that removes only AI-created temporary probes after pass or failure, preserves durable regressions, and verifies scoped Git cleanliness before commit.
- Add `flutter-text-rendering` skill to diagnose and fix Flutter text display defects, including orphaned words (widows), text overflow in flex layouts, multi-style inline spans, pre-layout `TextPainter` measurement, and accessibility under enlarged text scaling.
- Add technical reference `references/text-overflow-and-wrapping.md` covering non-breaking spaces (`\u00A0`), flex layout constraints, and text measurement.
- Add 5 behavior-focused evaluation cases and 3 cross-catalog routing cases.

## 0.6.0 - 2026-09-06

- Deliver Milestone 2A: Trustworthy Evaluation Engine & Coverage.
- Support structured and mandatory expectation criteria (`{"text": "...", "mandatory": true}`) in `run_behavior_evals.py` and repository validation.
- Enforce strict gating in the behavior evaluation engine: any failed mandatory expectation fails the case and increments `mandatory_failures` regardless of the overall score.
- Add `--coverage` flag and `reference_coverage_report()` to `run_behavior_evals.py` to measure and report evaluation coverage of skill reference documents across the catalog.
- Connect all 17 previously uncovered reference documents into evaluation cases across 10 skills (`dart-concurrency`, `dart-language`, `flutter-accessibility`, `flutter-animation`, `flutter-build-release`, `flutter-device-testing`, `flutter-localization`, `flutter-navigation`, `flutter-responsive-layout`, `flutter-state-management`), achieving 100% reference document coverage (87/87 references).
- Add 5 realistic Vietnamese routing test cases (`vietnamese-layout-overflow`, `vietnamese-parse-json-isolate`, `vietnamese-deep-link-navigation`, `vietnamese-secure-storage`, `vietnamese-form-validation`), expanding the cross-catalog routing evaluation suite from 57 to 62 cases.
- Record execution run metadata including git commit SHA, branch, working tree dirty state, timestamp, and runner version (`1.1.0`).
- Establish explicit Git branching, validation, and PR delivery workflow rules in `AGENTS.md` and `CLAUDE.md` requiring branch isolation (`feature/*`, `fix/*`, `refactor/*`), pre-commit local validation, and green-CI squash merges.

## 0.5.1 - 2026-09-05

- Deliver Phase 1 defect corrections and responsive layout guidance across the catalog.
- Add geometry, hit-test, SDK-compatible bounded viewport-matrix, and deterministic fixture guidance to `flutter-responsive-layout`, with focused overlap and automated-matrix regressions.
- Correct device-cleanup guidance in `flutter-device-testing` so uninstalling applications or clearing data requires an explicit data-preservation and authorization decision; prefer disposable test targets.
- Correct Dart 3 switch guard syntax in `dart-language` for switch expressions (`when`) and switch statements (`case ... when ...:`).
- Clarify isolate guidance in `dart-concurrency` to recommend background isolates for synchronous SQLite/FFI database calls and clarify `TransferableTypedData` construction copy cost versus $O(1)$ zero-copy isolate transfer.
- Document Hero tag scoping hazards for persistent tab shells in `flutter-animation` and distinguish in-memory tab preservation from OS process-death restoration in `flutter-navigation`.
- Update dynamic accessibility announcements in `flutter-accessibility` to resolve text direction from `Directionality.of(context)` and support modern `assertiveness` options.
- Separate preservation from authorized-migration cases in `flutter-app-workflow`, expanding the catalog to 165 behavior-focused evaluation cases.

## 0.5.0 - 2026-09-04

- Achieve 100% reference document coverage across the full catalog by adding 10 technical reference guides for `dart-concurrency`, `dart-language`, `flutter-accessibility`, `flutter-build-release`, and `flutter-device-testing`.
- Deepen `dart-concurrency` with isolate communication, worker pools, and stream cancellation/debouncing references.
- Deepen `dart-language` with Dart 3 patterns/records migration and sealed class hierarchies references.
- Deepen `flutter-accessibility` with semantics/screen-reader annotations and touch-target/contrast guidelines.
- Deepen `flutter-build-release` with flavor/scheme alignment and obfuscation/symbol preservation guides.
- Deepen `flutter-device-testing` with device discovery and integration test workflow references.
- Establish catalog-wide evaluation parity (minimum 4 behavior cases per skill) by expanding `flutter-app-workflow`, `flutter-ci-cd`, `flutter-notifications`, and `flutter-observability` from 3 to 4 cases (158 to 162 total evals).
- Expand cross-catalog routing cases from 54 to 57 to cleanly separate local flavor configuration from CI pipelines, OS periodic sync from notifications, and semantics accessibility audits from visual redesigns.

## 0.4.0 - 2026-09-02

- Constrain `flutter-openapi-client` external references and redirects by network, filesystem, credential-origin, and bounded-traversal trust policies so an untrusted contract cannot silently expand acquisition authority.
- Add provider-neutral `flutter-openapi-client` for safe Swagger UI discovery, complete OpenAPI inventory, scoped Dart client generation, schema fidelity, and consumer-aware contract drift without adding credentials or replacing the project's networking stack by default.
- Add neutral Swagger 2.0, OpenAPI 3.1, and inline Swagger UI fixtures plus behavior and routing regressions that distinguish contract generation from ordinary HTTP transport and reusable package publication.
- Add provider-neutral `flutter-webview` for embedded content policy, JavaScript bridges, cookies and sessions, file flows, permissions, and lifecycle verification without adding credentials or changing packages by default.
- Add behavior and routing regressions that distinguish embedded first-party web content from OAuth external-user-agent flows, Flutter navigation, API transport, and broad WebView security audits.
- Record a maintainer-only optimization backlog from executed benchmark failures and coverage gaps.

## 0.3.0 - 2026-08-31

- Add `flutter-in-app-purchases` for store transaction lifecycles, trusted verification, idempotent entitlements, subscriptions, restoration, and sandbox evidence.
- Add provider-neutral `flutter-authentication` for OAuth and OIDC redirects, PKCE, coordinated session refresh, logout, account switching, passkeys, and device re-authentication.
- Add provider-neutral `flutter-product-analytics` for semantic event contracts, consent-aware identity, deduplication, funnels, experiments, and end-to-end ingestion verification.
- Add behavior and routing evaluations that distinguish store billing from physical checkout, authentication from broad security review, and product analytics from operational observability.
- Calibrate sandbox-readiness evaluation to require explicit inspection and deterministic store evidence without fabricating repository or console access.
- Tighten authentication discovery boundaries across security and networking, and add an authenticated-transport routing regression.
- Refresh the fixed public benchmark for the six specialist boundaries added across v0.2.1 and v0.3.0.
- Strengthen package dry-run inspection and native-plugin clean-start verification from measured forward-evaluation failures.
- Calibrate the package-readiness evaluation to reward an executable evidence plan when its tool-free harness cannot inspect the repository.
- Bound each forward-evaluation agent invocation so a stalled solver cannot hang the full benchmark indefinitely.
- Make unavailable analytics ingestion and dashboard boundaries explicit instead of reporting only a generic pending state.

## 0.2.1 - 2026-08-30

- Add `flutter-package-development` for reusable public APIs, plugin shape, federation, consumer compatibility, and publication readiness.
- Add `flutter-runtime-debugging` for evidence-driven reproduction, process attachment, DevTools diagnosis, restart boundaries, and runtime verification.
- Add provider-neutral `flutter-ai-integration` for model service boundaries, streaming state, tool calls, structured output, and optional Flutter AI Toolkit or GenUI adoption without requiring provider credentials to install the skill.
- Add behavior and routing evaluations that distinguish the new specialists from app-owned platform bridges, planned device testing, ordinary APIs, and human chat.
- Calibrate the runtime-debugging forward-evaluation rubric to require honest evidence without demanding fabricated tool execution from a tool-free response.
- Add trusted npm publishing with provenance, registry verification, and tag-only release gates.
- Add native Codex plugin and marketplace metadata for the full skill catalog.
- Record exact agent versions in opt-in local forward-evaluation results.
- Extend repository validation and tests across npm, Codex, Claude, Tessl, and evaluation workflows.
- Correct the performance forward-evaluation rubric so a tool-free response is judged on requiring evidence rather than fabricating traces.

## 0.2.0 - 2026-08-27

- Add `flutter-figma-workflow` for evidence-based Figma-to-Flutter mapping and screenshot parity.
- Add `flutter-background-execution` for OS-scheduled jobs, foreground services, headless callbacks, and interruption-safe delivery.
- Add `flutter-dependency-upgrades` for staged SDK, package, lockfile, resolution, and native toolchain migrations.
- Deepen performance, testing, and architecture guidance through case-selected references.
- Add representative raw benchmark results and a reproducible benchmark profile.
- Close routing gaps for Dart language, animation, architecture, performance, and Figma work.
- Add a scheduled source-freshness audit with machine-readable artifacts.
- Expand evaluation coverage from 97 to 117 behavior cases across 10 skills.
- Add reference documents for state management, navigation, animation, localization, and responsive layout.
- Add 3 routing cases for localization+layout, animation+testing, and SDK upgrade+signing scenarios.
- Add empty-directory and low-eval-count advisory warnings to the repository validator.

## 0.1.1 - 2026-08-24

- Add the `@thiennc/flutter-skills` npm CLI for version-pinned one-command installation.
- Validate npm metadata, wrapper behavior, and package contents in CI.
- Expand `flutter-networking` with progressive GraphQL and realtime transport guidance plus focused routing and behavior evaluations.

## 0.1.0 - 2026-08-24

- Add a 25-skill Flutter and Dart delivery collection.
- Add `flutter-app-workflow` for end-to-end project coordination.
- Add `flutter-ui-design` for platform-aware visual direction, complete UI states, and repeatable visual verification.
- Upgrade `flutter-ui-design` with ambition calibration, reference parity, default-widget residue review, deterministic populated fixtures, and a render-critique-render completion gate.
- Add `flutter-visual-effects` for glass, blur, refraction, shaders, iOS effect translation, renderer-aware fallbacks, and profile-backed package decisions.
- Refine `flutter-visual-effects` with evidence-first selection across existing solutions, Flutter core, maintained packages, custom shaders, and native rendering.
- Add `flutter-security` for threat-driven application hardening and scoped security review.
- Add `flutter-code-review` for evidence-backed Flutter and Dart diff review without implicit edits.
- Add `flutter-notifications` for package-neutral local scheduling and remote push lifecycles with platform delivery verification.
- Add `flutter-observability` for privacy-aware logs, errors, traces, release correlation, symbols, and end-to-end telemetry verification.
- Add `flutter-ci-cd` for provider-neutral quality gates, secure artifact pipelines, and explicit publication boundaries.
- Add conditional caching, offline-sync, forms, Widget Previewer, FFI, and plugin-development references to existing specialists.
- Add package-neutral routing for architecture and state management.
- Add behavior evaluations, repository validation, tests, and clean discovery checks.
- Add opt-in baseline-versus-skill forward evaluations and cross-catalog routing cases.
- Keep `flutter-app-workflow` functional when optional specialists are not installed.
- Add capability-aware Dart and Flutter MCP guidance with CLI fallbacks.
- Strengthen specification, catalog, bundle, and documentation synchronization checks.
- Keep workflow routing focused, evaluate only case-selected references, and block release publication while changelog metadata remains `Unreleased`.
- Add Claude Code and Tessl bundle metadata.
