# Public benchmark

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
