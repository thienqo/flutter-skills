# Public benchmark

The music playback extension scored 100 on [queue identity and rapid skips](unreleased/flutter-music-queue.json), [system Pause during buffering and interruption](unreleased/flutter-music-system-pause.json), and [paused-session restoration](unreleased/flutter-music-session-restore.json). The [routing run](unreleased/flutter-music-routing.json) selected media for music and HLS playback and networking for text-only transport. Codex served as solver and judge with baselines skipped. Audible playback, lock-screen commands, and headset behavior were outside these runs.

The [behavior results from the initial location and maps run](unreleased/flutter-location-maps-behavior-initial.json) show scores of 100 on approximate location, address picking, and background tracking. The stale-fix and camera cases each scored 67 with a mandatory miss. The location reference now explicitly rechecks service and permission after returning from settings. The [stale-fix recheck](unreleased/flutter-location-maps-stale-fix-recheck.json) scored 100 after an intervening judge response lacked evidence and produced no result file. The camera reference now specifies cleanup when the controller binding changes. The [first camera follow-up](unreleased/flutter-location-maps-camera-followup.json) still missed subscription cancellation. The [calibrated camera case](unreleased/flutter-location-maps-camera-calibrated.json) states that the binding owns a subscription and scored 100 under the same rubric. The [background check after the reference edit](unreleased/flutter-location-maps-background-followup.json) also scored 100. These are same-family response results with Codex as solver and judge, with baselines skipped. Map rendering, provider responses, and background tracking on devices were outside the runs.

The final map guidance separates screen-owned fixes from controller-owned work. The expanded [camera ownership case](unreleased/flutter-location-maps-camera-ownership.json) scored 100 with a new mandatory check for a still-current fix surviving controller replacement. The [address and viewport ordering recheck](unreleased/flutter-location-maps-address-ownership.json) also scored 100.

The [final location and maps routing run](unreleased/flutter-location-maps-routing-final.json) passed all six cases. A store-finder prompt selected `flutter-location-maps`, and locked-screen courier tracking selected it with `flutter-background-execution`. The map-tab deep-link and opening-hours HTTP retry cases selected navigation and networking respectively. In a separate disposable project with four installed skills, Codex read the location skill and its references after a request that named no skill. Claude Code listed the skill but its expired OAuth credentials blocked prompt execution.

The new `flutter-media` skill has eight response cases, eight routing cases, and a fake-player executable fixture. With `codex-cli 0.167.0-alpha.3.2`, the final focused response evidence passes all eight cases across the [follow-up](unreleased/flutter-media-behavior-followup.json), [calibrated reconnect](unreleased/flutter-media-reconnect-calibrated.json), and [adjacent mode checks](unreleased/flutter-media-behavior-adjacent.json): camera 100, playback 100, interruption 100, broadcasting 100, reconnect 100, screen sharing 100, attachment recovery 90, and HLS 100. The [initial run](unreleased/flutter-media-behavior-initial.json) retains camera, audio, reconnect, and recovery misses. Camera/audio rubrics were narrowed to their actual preview/interruption scope; reconnect accepts equivalent controlled event replay rather than requiring the word "fake". Those calibration changes are not claimed as skill improvement. The entrypoint additionally requires explicit version/SDK responsibility and verification handoffs; the reconnect reference now makes departure/disposal and network-interruption checks explicit.

The [existing-specialist comparison under final rubrics](unreleased/flutter-media-existing-specialists-final.json) uses entrypoints from commit `d545e4a`: platform integration plus concurrency for camera (70), platform integration plus background execution for interruptions (45), and networking plus concurrency for reconnect (45). Exact injected bundles, prompts, rubrics, and hashes are retained. This is a small same-family response comparison, not a no-skill baseline or native capability proof. A [two-case exploratory calibration](unreleased/flutter-media-existing-specialists-calibrated.json) is also retained; an earlier exploratory three-case raw file was accidentally overwritten, so its observed scores are excluded from the comparison.

All eight [media routing cases](unreleased/flutter-media-routing-initial.json) passed, including a Vietnamese livestream request and text-chat, PDF-upload, and gallery-jank negative controls. The [adjacent catalog check](unreleased/flutter-media-routing-adjacent.json) passed three of four cases; the existing human-support-chat case unnecessarily selected app workflow. The [original 37-skill catalog](unreleased/flutter-media-adjacent-original-catalog.json) reproduced that selection with media absent. It remains an explicit workflow-routing backlog item, not a passing result or a reason to rewrite an unrelated specialist.

The [native implicit-discovery smoke](unreleased/flutter-media-native-discovery.json) installed media and five neighbors into a disposable project. Its natural-language request named no skill. Retained successful command events show Codex reading `flutter-media/SKILL.md` and its playback/verification references, alongside concurrency guidance. This proves implicit selection in that one CLI configuration with those six local skills, not every prompt, host, or full-catalog budget. The [executable agent result](unreleased/flutter-media-source-ownership-executable.json) separately passes format, analysis, and six deterministic fake-player ownership scenarios. CI verifies the passing oracle and seeded stale selection, resource leaks, stopped-owner revival, concurrent stop, and failed-close ownership defects. Actual camera/microphone access, codecs/decoding, audio hardware, and two-endpoint live delivery remain unverified; no independent-provider or human-calibration claim is made. See the [source and scope assessment](../.github/maintainer/media-skill-scope.md).

The `flutter-app-workflow` coordination cases ran with `codex-cli 0.167.0-alpha.3.2`, the default model, and the same Codex family as solver and judge, with baselines skipped. Under the fixed calibrated rubrics, reusable-package routing and shared-contract/blocker coordination scored 75 and 60 before the instruction changes, then 100 and 100 afterwards; see the [calibrated initial result](unreleased/flutter-app-workflow-coordination-calibrated-initial.json) and [final result](unreleased/flutter-app-workflow-coordination.json). The [earlier 60/45 result](unreleased/flutter-app-workflow-coordination-initial.json) used rubrics that over-specified unavailable interfaces and implementation ordering; it is retained as rubric calibration, not a comparable skill measurement.

The [adjacent checks](unreleased/flutter-app-workflow-coordination-adjacent.json) scored bounded implementation review at 100 and unavailable-specialist fallback at 67. The latter exposed an environment mismatch: the solver was explicitly tool-free, but the judge treated its access limitation as unsupported by the case prompt. The case now supplies its response-only environment and Flutter/ChangeNotifier/http constraints, and asks for an executable plan rather than inaccessible implementation. That [calibrated fallback case](unreleased/flutter-app-workflow-unavailable-specialists-calibrated.json) scored 100 with both mandatory constraints met. This is a case calibration, not evidence that the skill improved from 67 to 100. All four [adjacent routing boundaries](unreleased/flutter-app-workflow-coordination-routing.json) passed, separating broad feature delivery, a contained form, reusable plugins, and app-owned native bridges.

The [workflow feature executable result](unreleased/flutter-app-workflow-task-completion-executable.json) records an agent changing three Dart implementation files and adding one regression test, with the specialist library, acceptance tests, and package metadata preserved. The host checks passed locked offline dependency setup, formatting, analysis, seven immutable acceptance scenarios, and the agent's additional regression. The agent reported its own Flutter test attempts blocked by read-only SDK cache permissions and left those checks to the host rather than claiming they ran. The declared environment was Flutter 3.44.8/Dart 3.12.2, a controlled fake API, and unit/widget execution; neither a live backend nor a device was verified. Selected specialist reads are self-reported, not an audited tool trace or native-host discovery proof. CI separately proves a corrected oracle passes and seeded repository, duplicate-submit, disposal, and hidden-error defects fail. These focused runs are regression evidence, with no independent-provider or human-calibration claim.

The [responsive checkout executable result](unreleased/responsive-checkout-geometry-executable.json) records an agent changing only the allowed Dart library, followed by formatter, analyzer, and six widget-test checks. Earlier passing runs are retained from [before the text-truncation assertion](unreleased/responsive-checkout-geometry-executable-initial.json), [after that assertion](unreleased/responsive-checkout-geometry-executable-text-check.json), and [before the explicit 600-pixel breakpoint](unreleased/responsive-checkout-geometry-executable-pre-breakpoint.json). The separate CI fixture proof checks that seeded overlap, missing wide composition, validation clipping, sticky-action obstruction, and offscreen actions fail while the corrected oracle and its intentional badge overlay pass. These are Flutter widget-test results with simulated keyboard insets, not physical-device evidence.

The priority audit fixes were checked with six focused same-agent behavior cases, with baselines skipped. The [initial run](unreleased/priority-audit-fixes-initial.json) passed Hero matching, authentication, purchases, and hard line breaks at 100, but scored web execution and window announcements at 75. The web prompt lacked profiling evidence needed to select a concrete strategy; it now supplies a measured bottleneck and an existing compatible worker adapter. The announcement reference now explicitly derives localization from the originating window. Both cases scored 100 in the [follow-up](unreleased/priority-audit-fixes-followup.json). These are response-level regression results, not device or independent-judge evidence. An earlier interrupted attempt reported 67 and 75 for those two cases but ended before the runner persisted raw results; those incomplete observations are not included as a completed benchmark.

The fixed profile in [public-benchmark.json](../.github/evals/public-benchmark.json) compares normal agent behavior with the same agent receiving the selected skill and separately checks catalog routing.

Run it with:

```sh
python3 .github/scripts/run_behavior_evals.py \
  --execute \
  --agent codex \
  --judge-agent codex \
  --agent-timeout 180 \
  --profile .github/evals/public-benchmark.json \
  --output benchmarks/v0.3.0/codex-default.json
```

Raw results are intentionally committed without removing responses, judgments, selections, or failed cases. Case identifiers resolve to the versioned prompts and rubrics under `skills/*/evals` and `.github/evals`. The current profile is a six-case behavior and seven-case routing sample on one agent configuration; it is useful regression evidence, not proof of quality across every model, app, or skill.

The default evaluation matrix uses the existing Codex CLI session and does not require a second provider account:

```sh
python3 .github/scripts/run_eval_matrix.py \
  --execute \
  --output-dir benchmarks/matrix
```

This same-model score is regression screening, not independent evidence. Pair published results with compiler-backed checks and a 10–15% human sample. When another authenticated provider is available, use the optional cross-agent matrix; every judge must pass the threshold and mandatory criteria:

```sh
python3 .github/scripts/run_eval_matrix.py \
  --execute \
  --matrix .github/evals/cross-agent-matrix.json \
  --output-dir benchmarks/matrix
```

Use [evaluation strategy](../.github/maintainer/evaluation-strategy.md) for PR, nightly, release, executable, cross-agent, and human-review workflows. External-agent execution remains explicit; ordinary CI validates inputs without spending model quota.

## Claude Code catalog baseline (2026-11-03)

Claude Code was both solver and judge with its default model, one judge and an 80-point threshold. The run covered one case per skill: the six public-profile cases in [claude-public-baseline.json](v0.12.0-draft/claude-public-baseline.json), and the first case with a mandatory expectation for each of the other 31 skills in [claude-catalog-sweep.json](v0.12.0-draft/claude-catalog-sweep.json). Both files contain baselines. Across the 37 skills, the mean is 61.8 without the skill and 84.4 with it (+22.6). Baseline responses failed a mandatory expectation in 13 cases. On the six public-profile cases the delta is +26.3; the v0.3.0 Codex run measured +57.0. With one case per skill and the same model family judging, a small delta is a signal to measure more cases, not proof that a skill adds nothing. Routing passed 7/7 and 1/1.

| Skill | Case | Baseline | With skill | Delta | Passed |
|---|---|---:|---:|---:|---|
| `flutter-device-testing` | `verifies-deep-link-on-device` | 15 | 95 | +80 | yes |
| `flutter-dependency-upgrades` | `stages-production-major-upgrades` | 22 | 92 | +70 | yes |
| `flutter-runtime-debugging` | `runtime-fix-repeats-original-flow` | 40 | 95 | +55 | yes |
| `flutter-ui-design` | `preserves-existing-brand-system` | 40 | 95 | +55 | yes |
| `flutter-networking` | `runtime-response-does-not-become-the-whole-contract` | 42 | 94 | +52 | yes |
| `flutter-observability` | `trace-checkout-without-pii` | 30 | 78 | +48 | no |
| `flutter-notifications` | `notification-tap-matrix-is-repeatable-and-idempotent` | 45 | 92 | +47 | yes |
| `flutter-testing` | `cleans-only-ai-created-disposable-test-probe` | 38 | 85 | +47 | yes |
| `flutter-in-app-purchases` | `sandbox-readiness-is-not-store-publication` | 35 | 72 | +37 | no |
| `flutter-background-execution` | `uses-os-scheduler-for-terminated-sync` | 55 | 90 | +35 | yes |
| `flutter-navigation` | `preserves-existing-go-router` | 55 | 85 | +30 | yes |
| `flutter-product-analytics` | `sdk-log-is-not-end-to-end-proof` | 65 | 95 | +30 | yes |
| `flutter-responsive-layout` | `navigation-adapts-to-window-width` | 65 | 95 | +30 | yes |
| `flutter-webview` | `origin-policy-does-not-use-string-prefixes` | 62 | 90 | +28 | yes |
| `flutter-authentication` | `native-client-secret-is-not-secret` | 65 | 92 | +27 | yes |
| `flutter-ui-patterns` | `no-side-effects-in-build` | 67 | 88 | +21 | yes |
| `flutter-openapi-client` | `documented-fields-and-observed-response-stay-distinct` | 58 | 78 | +20 | no |
| `flutter-code-review` | `delivery-workflow-review-stays-within-task-impact` | 68 | 85 | +17 | yes |
| `flutter-visual-effects` | `gates-experimental-liquid-renderer` | 78 | 95 | +17 | yes |
| `flutter-figma-workflow` | `maps-figma-frame-to-existing-design-system` | 76 | 92 | +16 | yes |
| `flutter-accessibility` | `announcements-use-the-owning-view` | 30 | 45 | +15 | no |
| `flutter-build-release` | `obfuscation-preserves-symbols` | 88 | 100 | +12 | yes |
| `flutter-persistence` | `migration-failure-preserves-prior-user-data` | 82 | 94 | +12 | yes |
| `flutter-architecture` | `reuses-existing-di-mechanism` | 90 | 100 | +10 | yes |
| `flutter-performance` | `resizes-images-before-clearing-cache` | 35 | 45 | +10 | no |
| `flutter-security` | `hardcoded-service-secret-is-not-fixed-by-obfuscation` | 90 | 100 | +10 | yes |
| `flutter-ci-cd` | `harden-existing-github-actions` | 85 | 91 | +6 | yes |
| `flutter-localization` | `plural-and-formatting` | 84 | 90 | +6 | yes |
| `dart-language` | `records-not-for-domain-identity` | 95 | 100 | +5 | yes |
| `flutter-ai-integration` | `skill-install-needs-no-provider-key` | 95 | 100 | +5 | yes |
| `flutter-package-development` | `dry-run-does-not-authorize-publish` | 90 | 94 | +4 | yes |
| `flutter-state-management` | `state-disposed-with-lifecycle-owner` | 67 | 70 | +3 | no |
| `flutter-text-rendering` | `soft-wrap-does-not-remove-hard-breaks` | 94 | 95 | +1 | yes |
| `dart-concurrency` | `web-compute-does-not-provide-parallelism` | 100 | 100 | +0 | yes |
| `flutter-platform-integration` | `plugin-before-custom-channel` | 10 | 8 | -2 | no |
| `flutter-animation` | `chooses-implicit-animation` | 100 | 93 | -7 | yes |
| `flutter-app-workflow` | `ticket-scoped-branch-commit-and-push-boundary` | 30 | 15 | -15 | no |

### Three-case follow-up for the low-delta skills

The twelve skills with a delta of +12 or less in the table above were rerun on two more cases each, with baselines, using the same Claude Code setup. Files: `v0.12.0-draft/claude-groupb-<skill>.json`. Each mean covers three cases (the first case plus two more). Nine of the twelve skills now show a delta between +6 and +27, so a one-case delta understated them and no skill was trimmed. `flutter-text-rendering` (baseline 98) adds almost nothing on these cases. `flutter-ci-cd` and `flutter-package-development` score below 80 with the skill. The `flutter-ci-cd` matrix case scored 72, 55, and 62 after its rubric was reworded to accept a plan, and one run missed a mandatory expectation, so it remains open. The package-development means include the case fixed in this release.

| Skill | Baseline mean | With-skill mean | Delta |
|---|---:|---:|---:|
| `dart-language` | 54 | 81 | +27 |
| `flutter-persistence` | 75 | 94 | +19 |
| `flutter-ai-integration` | 76 | 94 | +18 |
| `flutter-build-release` | 68 | 84 | +16 |
| `dart-concurrency` | 72 | 86 | +14 |
| `flutter-architecture` | 72 | 85 | +13 |
| `flutter-security` | 75 | 84 | +9 |
| `flutter-localization` | 77 | 85 | +8 |
| `flutter-package-development` | 64 | 70 | +6 |
| `flutter-animation` | 75 | 81 | +6 |
| `flutter-text-rendering` | 98 | 96 | -2 |
| `flutter-ci-cd` | 76 | 70 | -7 |

## Unreleased focused result

The `flutter-device-testing` semantic inspection cases ran with Claude Code 2.1.310 as both solver and judge, with baselines skipped. The accessibility-tree navigation case scored 92 and the empty-semantics-tree case scored 35 with a mandatory failure in the [initial result](unreleased/flutter-device-testing-semantic-inspection-initial.json): the agent led with the requested coordinate tap and gave the diagnosis afterwards, and it did not route the missing identifier to `flutter-accessibility`. After the reference required that diagnosis first and that routing, the case scored 96; see the [final result](unreleased/flutter-device-testing-semantic-inspection.json).

The newly mandatory `flutter-security` and `flutter-ci-cd` expectations were checked with the same Claude Code setup. Every mandatory expectation was met. All four [CI/CD cases](unreleased/flutter-ci-cd-mandatory.json) passed (86, 92, 90, 92). The security cases scored 100, 72, 87, 95, and 75; each has its own raw file, for example [token storage](unreleased/flutter-security-token-storage-has-a-lifecycle.json) and [static audit](unreleased/flutter-security-static-audit-does-not-become-live-penetration-test.json). Two cases fell below the 80 threshold on a non-mandatory expectation. The token-storage response did not define expiry or account-switching behavior, which the reference already requires. The static-audit response described a report structure without a categorized report, because the solver ran tool-free outside a Flutter repository. Neither result changed a skill. A first combined security run stopped with `agent did not return a JSON object` and wrote no results; the cases were rerun one at a time.

Four new routing boundaries all passed with Claude Code 2.1.310; see the [routing result](unreleased/routing-boundaries-debugging-effects.json). They cover a frozen UI that is not jank, production cold-start signals that are not local profiling, a Figma node with a frosted glass surface, and a blur added without redesign.

The `flutter-persistence` migration-safety case now scores 100 with `codex-cli 0.154.0`; see the [final](unreleased/flutter-persistence-migration-safety.json) and retained [60-point initial](unreleased/flutter-persistence-migration-safety-initial.json) raw results. The first run preserved durable data but did not explicitly require released prior-version fixtures, assert the exact target schema version, or inspect the resolved package and SDK contract before selecting APIs. Both focused routing boundaries passed: local database migration selected persistence and testing, while a remote API schema change selected the OpenAPI client without persistence; see the [routing result](unreleased/flutter-persistence-routing-boundaries.json). These runs skipped baselines and used one Codex family, so they are focused regression evidence rather than independent cross-provider validation.

The three `flutter-code-review` output-quality cases scored 100 with `codex-cli 0.154.0`, improving from an initial 72.33 average with one mandatory failure; see the [final](unreleased/flutter-code-review-output-quality.json) and [initial](unreleased/flutter-code-review-output-quality-initial.json) raw results. All three focused routing boundaries also passed: review of a test diff selected code review, a repository-wide threat audit selected security without generic code review, and a requested async implementation did not preload the review skill; see the [routing result](unreleased/flutter-code-review-routing-boundaries.json). These runs use one Codex family and prove focused response and selection behavior rather than independent cross-provider quality.

The `flutter-text-rendering` constraint, recognizer-ownership, and localized-measurement cases passed at 85, 100, and 100 with `codex-cli 0.154.0`; see the [raw focused result](unreleased/flutter-text-rendering-correctness.json). The run skipped baselines and used the same Codex family for solving and judging, so it is regression evidence rather than independent validation.

The `flutter-device-testing` warm-state case now scores 100 with `codex-cli 0.154.0`; see the [final result](unreleased/flutter-device-testing-warm-precondition.json). Retained runs at [67](unreleased/flutter-device-testing-warm-precondition-initial.json), [50](unreleased/flutter-device-testing-warm-precondition-bounded-cleanup-initial.json), [60](unreleased/flutter-device-testing-warm-precondition-tool-free-initial.json), and [80](unreleased/flutter-device-testing-warm-precondition-dry-run-gate-initial.json) exposed the failure-safe cleanup, per-step timeout, versioned schema, tool-free evidence, and successful dry-run gates. The focused run skipped baselines and used the same Codex family for solving and judging, so it proves response behavior rather than independent cross-provider validation.

The first compiler-backed fixture passed with `codex-cli 0.153.4`; see [the raw executable result](unreleased/dart-concurrency-latest-wins-executable.json). The agent changed only the allowed Dart library, while immutable verification passed `dart format`, `dart analyze`, and a deterministic reversed-completion runtime check. No cross-provider score is claimed; the default workflow is intentionally Codex-only and records independent human calibration separately.

Four hardening cases now score 100 with `codex-cli 0.153.4`: [accessibility semantics cleanup](unreleased/flutter-accessibility-semantics-cleanup.json), [rapid stream re-trigger ownership](unreleased/dart-concurrency-rapid-retrigger.json), [signature-aware integration startup](unreleased/flutter-device-testing-integration-startup.json), and [locale-bounded orphan handling](unreleased/flutter-text-rendering-locale-orphan.json). Retained initial results document the measured gaps and rubric calibration: [semantics cleanup 67](unreleased/flutter-accessibility-semantics-cleanup-initial.json), [stream ownership 75](unreleased/dart-concurrency-rapid-retrigger-initial.json), and integration startup at [67](unreleased/flutter-device-testing-integration-startup-initial.json) then [65](unreleased/flutter-device-testing-integration-startup-signature-initial.json). These focused runs skip baselines and prove response behavior only.

The `flutter-app-workflow` understanding-gate case now scores 100 with `codex-cli 0.153.4`; see the [final result](unreleased/flutter-app-workflow-understanding-gate.json). The retained [65-point first run](unreleased/flutter-app-workflow-understanding-gate-initial.json), [75-point tool-free calibration run](unreleased/flutter-app-workflow-understanding-gate-tool-free-initial.json), and [80-point impact-map run](unreleased/flutter-app-workflow-understanding-gate-impact-map-initial.json) showed that asking the right question is insufficient by itself: the agent must first state current versus intended behavior and connect every affected boundary to concrete code, contract, or test evidence without fabricating unavailable inspection.

The new `flutter-app-workflow` post-implementation review case scored 100 with `codex-cli 0.153.4`; see the [final result](unreleased/flutter-app-workflow-post-implementation-review.json). The retained [25-point initial result](unreleased/flutter-app-workflow-post-implementation-review-initial.json) showed that a tool-free forward evaluation must assess the required completion plan rather than demand file edits and executed checks that its harness forbids.

The new `flutter-responsive-layout` overlap and bounded viewport-matrix cases each scored 100 with `codex-cli 0.153.1`. The focused runs skipped baselines and prove response behavior only; see the [overlap result](unreleased/flutter-responsive-layout-overlap.json) and [matrix result](unreleased/flutter-responsive-layout-matrix.json). The matrix's two 67-point runs are retained as [the initial result](unreleased/flutter-responsive-layout-matrix-initial.json) and [the compatibility-gate result](unreleased/flutter-responsive-layout-matrix-compatibility-gate-initial.json); they showed that a tool-free prompt must supply inspected SDK capabilities before requiring concrete compatible APIs.

## v0.3.0 result

Run on 2026-08-30 with `codex-cli 0.151.0-alpha.7.2`, its default model, the same agent as solver and judge, and an 80-point behavior threshold.

| Behavior case | Baseline | With skill | Delta |
|---|---:|---:|---:|
| `flutter-package-development` | 30 | 96 | +66 |
| `flutter-runtime-debugging` | 15 | 100 | +85 |
| `flutter-ai-integration` | 0 | 100 | +100 |
| `flutter-authentication` | 100 | 100 | 0 |
| `flutter-in-app-purchases` | 42 | 100 | +58 |
| `flutter-product-analytics` | 67 | 100 | +33 |
| **Average** | **42.33** | **99.33** | **+57.0** |

All six behavior cases and all seven routing cases passed. See [codex-default.json](v0.3.0/codex-default.json) for the final raw run. The first run is retained as [codex-default-initial.json](v0.3.0/codex-default-initial.json); its analytics failure showed that “end-to-end pending” did not identify the unavailable provider-ingestion and downstream-dashboard boundaries precisely enough, so the skill now records those boundaries explicitly as unverified.

## v0.2.0 result

Run on 2026-08-24 with `codex-cli 0.149.0-alpha.4.1`, its default model, the same agent as solver and judge, and an 80-point behavior threshold.

| Behavior case | Baseline | With skill | Delta |
|---|---:|---:|---:|
| `flutter-ui-design` | 78 | 100 | +22 |
| `flutter-figma-workflow` | 91 | 96 | +5 |
| `flutter-architecture` | 75 | 100 | +25 |
| `flutter-performance` | 0 | 100 | +100 |
| `flutter-testing` | 75 | 100 | +25 |
| **Average** | **63.8** | **99.2** | **+35.4** |

All five routing cases passed. See [codex-default.json](v0.2.0/codex-default.json) for every prompt, response, judgment, and selected skill.

The first run is retained as [codex-default-initial.json](v0.2.0/codex-default-initial.json). It exposed an impossible Figma eval that demanded implementation and screenshots while the eval harness intentionally disallowed files and tools. The case was changed to evaluate an implementation plan from already-inspected design evidence, then the full fixed profile was rerun; the failed raw run remains available for audit.
