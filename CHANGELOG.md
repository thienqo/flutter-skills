# Changelog

## Unreleased

- Correct Riverpod async disposal guidance by version and distinguish Google Play consumable ordering from StoreKit finish. Add two behavior cases and strengthen adjacent lifecycle and billing evaluations.

- Extend `flutter-media` with QR and barcode scanning guidance for repeat detection, payload validation, manual entry, and camera lifecycle. Add three behavior cases and two routing cases.

- Add `flutter-payments-checkout` for external-gateway order payments, idempotent attempts, redirect recovery, verified results, and fulfillment. Add four behavior cases and extend checkout routing coverage.

- Extend `flutter-media` with music queues, shared app and system media controls, and paused-session restoration. Add three behavior cases and one routing case.

- Add `flutter-location-maps` for permission-aware location, map camera and marker behavior, nearby search, and address picking. Add three source-linked references, five behavior cases, and six routing cases. The catalog now has 39 skills, 251 behavior cases, and 90 routing cases.

- Add `flutter-media` for camera/media picking, audio/video recording and playback, livestreams, realtime calls, and screen sharing, preserving existing SDK/provider choices. Add six source-linked references, eight mandatory-gated behavior cases, eight positive/negative routing cases including Vietnamese, and a fake-player resource-ownership executable fixture. The catalog now has 38 skills, 246 behavior cases, and 84 routing cases.
- Connect media to app workflow, platform integration, and networking boundaries; keep implicit invocation enabled by default and explain natural-language versus explicit skill use. Synchronize discovery, Tessl membership, public counts, and nightly/release evaluation estimates.

- Complete `flutter-app-workflow` routing with conditional reusable-package ownership and validate that its specialist inventory stays synchronized with all 36 specialists.
- Define shared-contract ownership, concrete handoffs, conflict resolution, and local work around external verification blockers in a conditionally loaded coordination reference. Add two mandatory-gated behavior cases (236 to 238) and retain their measured failures and reruns.
- Add a pinned Flutter feature fixture spanning repository, ChangeNotifier state, and UI, with immutable acceptance tests, a selective local specialist library, input hashes, and an executed agent patch. CI verifies a passing oracle and seeded contract, duplicate-submit, disposal, and hidden-error defects without invoking a model.
- Calibrate the unavailable-specialist case to explicitly declare its response-only environment and supplied stack; keep the original failed result separate from the revised case. Document executable sandbox limits and the exact locked, offline Flutter dependency setup allowed by the host.

## 0.13.0 - 2026-11-06

- Redact cookie values that start on the next line and scan lifecycle report URLs in linear time. Allow a later Dart search to retry after subscription cancellation fails.

- Clarify Flutter web and native thumbnail sizing, reproducible visual and keyboard checks, and policy shared across repositories. Add focused behavior cases for all three.

- Harden lifecycle report redaction, cleanup, and simulator failure handling. Fix manual ADB examples, serialize stream cleanup across retriggers, and ask for clarification only when a material app decision remains unresolved.

- Quote Android lifecycle runner arguments for the device shell and redact credentials in lifecycle reports. Keep behavior eval fixtures outside installed skill directories and require a finalized changelog for release validation.

- Clarify how five skills handle untrusted GitHub, dependency, Figma, notification, and OpenAPI content. Add behavior cases that exercise embedded instructions while preserving the requested workflow.

- Package the catalog for DeepSeek Harness and VS Code, and document Zed installation.

- Package the Flutter and Dart skills for Google Antigravity and Gemini CLI.

- Package the Flutter and Dart skills as a Cursor plugin.
- Show the Claude plugin as `thienqo-flutter` in the directory. The plugin name and install command are unchanged.
- Add `PRIVACY.md` and link it from the Claude plugin manifest for the plugin directory listing.
- Move the npm executable from `bin/` to `cli/`, because the Claude plugin directory cannot install a plugin with a top-level `bin/` on Cowork or the Claude apps. The `flutter-skills` command is unchanged.
- Replace the four Claude Code bundles with one plugin, `thienqo-flutter-skills`, and add `.claude-plugin/plugin.json`, because the Claude plugin directory rejects skills declared in `marketplace.json`. Breaking for Claude Code: `all-flutter-skills`, `flutter-core-skills`, `flutter-ui-skills`, and `flutter-engineering-skills` no longer exist; run `/plugin install thienqo-flutter-skills@flutter-skills` after removing the old plugin. Codex, Tessl, and npm installs are unchanged.
- Re-measure the catalog on Claude Code with baselines, one case per skill (37 cases): mean 61.8 without the skill and 84.4 with it (+22.6). On the six public-profile cases the delta is +26.3, against +57.0 measured with Codex in v0.3.0. See `benchmarks/README.md`.
- Rerun the twelve low-delta skills on two more cases each with baselines. Nine show a delta between +6 and +27 over three cases, so no skill was trimmed. `flutter-text-rendering` (baseline 98) adds almost nothing, and `flutter-ci-cd` (70 with the skill against 76 without) and `flutter-package-development` (70 against 64) score below 80. The `flutter-ci-cd` matrix case fell to 72, 55, and 62 after its rubric was reworded to accept a response-only plan, with one mandatory miss on protected-environment secrets, so it stays open.
- Tell `flutter-platform-integration` not to replace an adequate plugin the project already uses with custom native code until the user names the requirement the plugin fails. `plugin-before-custom-channel` moved from 8, with a mandatory failure, to 100, 100, and 100. The contrast case `typed-native-contract` scored 86, 84, and 86 in the same runs.
- Tell `flutter-performance` to treat a cause named in the request as a hypothesis and confirm it first, for images with `imageCache.currentSizeBytes`, `liveImageCount`, or DevTools Memory. `resizes-images-before-clearing-cache` moved from 45, with a mandatory failure, to 93, 95, and 96.
- Tell `flutter-accessibility` that save confirmations and similar ordinary feedback belong in visible status text under `Semantics(liveRegion: true)`, not in a per-platform explicit announcement. `announcements-use-the-owning-view` moved from 45, with a mandatory failure, to 92, 92, and 93.
- Reword three mandatory expectations in `flutter-app-workflow` `ticket-scoped-branch-commit-and-push-boundary` so a response-only solver can meet them by giving the exact read, branch, and commit steps without claiming them. The change is to the rubric, not to the skill. The case moved from 15 to 90, 90, and 88.
- Tell `flutter-package-development` that an up-front conditional go-ahead ("publish if the dry run passes") does not cover metadata or file changes the agent made afterwards: stop after the dry run, report the result, and ask before `dart pub publish`. Publishing to pub.dev is permanent. The `dry-run-does-not-authorize-publish` case failed its mandatory expectation in all three `pr-smoke` runs (78, 62, 62), because each response treated the instruction as standing authorization. After the change it scored 92, 92, and 92 with every expectation met (Claude Code solver and judge, baseline skipped); see `benchmarks/unreleased/flutter-package-development-conditional-publish-run1.json` to `run3.json`.
- Add the behavior case `exact-unchanged-version-publish-is-not-blocked` (227 to 228), so the fix is not rewarded for asking twice when the user named the exact unchanged package, version, and publisher. It scored 85, 85, and 85 in the same runs, with the mandatory no-second-confirmation expectation met each time.

## 0.12.0 - 2026-11-02

- Mark 31 existing consequence-bearing expectations as mandatory across the 13 skills that had none (`flutter-ai-integration`, `flutter-background-execution`, `flutter-dependency-upgrades`, `flutter-figma-workflow`, `flutter-observability`, `flutter-package-development`, `flutter-platform-integration`, `flutter-product-analytics`, `flutter-runtime-debugging`, `flutter-ui-design`, `flutter-ui-patterns`, `flutter-visual-effects`, `flutter-webview`), so all 37 skills now gate on at least one mandatory expectation.
- Add seven behavior cases (220 to 227): analytics evidence per boundary, package publisher and version mismatch behind a passing dry run, signing material kept out of the repository, a new CI job that keeps the pinned toolchain, Figma dark mode that differs from the app theme, PII and payloads kept out of crash context, and list state that follows item identity. These also close the open P1 analytics and package-development backlog items. The cases are defined but not yet run against a forward evaluator.
- Add a holdout manifest (`.github/evals/holdout/holdout.json`, 23 cases across 17 high-risk skills) and a repository check that fails when a holdout case is unknown, repeated, or listed in the `pr-smoke` or `nightly-representative` tuning profiles.
- Add an optional `capabilities` case field (`device`, `design-tool`, `provider-console`, `registry`). The repository check rejects unknown names and warns when an expectation asks for that evidence without declaring it.
- Tell `flutter-build-release` to verify the produced artifact's signature without uploading it (`apksigner verify`, `jarsigner -verify`, `codesign --verify`). The `signing-material-stays-out-of-the-repository` case moved from 62, 62, and 62 across three runs to 88, 93, and 95. The four other `flutter-build-release` cases scored the same before and after the edit in one run each; three of them were already below 80.
- Reword expectations in four of the seven new cases (`flutter-ci-cd`, `flutter-figma-workflow`, `flutter-package-development`, `flutter-product-analytics`) so they ask a response-only solver for a plan and an explicit unverified boundary instead of evidence it cannot produce. Those cases now score a median of 62, 58, 82, and 88; the change is to the rubric, not to a skill.
- Reword four expectations in `flutter-build-release` (`staging-release-artifact`, `version-follows-repository-policy`) that asked a response-only solver to inspect, build, or read files. `staging-release-artifact` moved from 55 to 88, 88, and 82; `version-follows-repository-policy` from 22 to 62, 62, and 72, and stays below 80.
- Correct the model-call estimates in the evaluation strategy: two calls per behavior case plus one per routing case gives 150 for the nightly profile and 530 for the release profile, replacing 139 and 443.
- Move the two P1 backlog items and the capability-validator item to closed, and record the remaining weak cases as open.
- Record variance reports in `benchmarks/v0.12.0-draft/` (`pr-smoke`, three runs, largest spread 16 points) and `benchmarks/unreleased/` (the seven new cases, three runs, before the rubric rewrites).

## 0.11.1 - 2026-11-01

- Point the `flutter-product-analytics` Google Play user data policy source at its canonical Play Console Help page. The old `play.google.com/about` URL returned 404 to the scheduled source audit. The audit now confirms a HEAD 404 with a one-byte GET, because `support.google.com` answers HEAD with 404 for pages that exist.
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
