# Variance of the seven Phase 1 cases

Solver and judge: `claude` CLI, default model at run time (Sonnet 5.5), one judge, baseline skipped, 2026-11-01. Same-family judge, so not independent evidence. Three runs, all reported.

| Case | Run 1 | Run 2 | Run 3 | Min / median / max | Mandatory failures |
|---|---|---|---|---|---|
| flutter-build-release:signing-material-stays-out-of-the-repository | 62 | 62 | 62 | 62 / 62 / 62 | 0 |
| flutter-ci-cd:new-job-keeps-the-pinned-toolchain | 82 | 62 | 22 | 22 / 62 / 82 | 2 of 3 |
| flutter-figma-workflow:figma-dark-mode-differs-from-existing-theme | 42 | 22 | 22 | 22 / 22 / 42 | 3 of 3 |
| flutter-observability:crash-context-excludes-pii-and-payloads | 72 | 90 | 72 | 72 / 72 / 90 | 0 |
| flutter-package-development:dry-run-passes-but-publisher-or-version-mismatch | 62 | 62 | 62 | 62 / 62 / 62 | 0 |
| flutter-product-analytics:provider-ingestion-visible-but-attribution-unverified | 52 | 62 | 55 | 52 / 55 / 62 | 0 |
| flutter-ui-patterns:list-item-state-follows-identity | 85 | 88 | 72 | 72 / 85 / 88 | 0 |

Flaky by the 20-point rule: ci-cd (60), figma (20), observability (18 is below the rule), ui-patterns (16 is below the rule). Only ci-cd exceeds it.

Expectations missed every run (stable, so a property of the case or the skill, not noise):

- build-release: "verifies the signature of the produced artifact" (3 of 3). The solver plans a build and never names a signature check.
- package-development: "completes the readiness review that needs no publication" (3 of 3). The solver lists the review steps but does not perform them, and a response-only solver cannot read the changelog or diff the API.
- figma: reports token differences and renders the Disabled variant (a response-only solver cannot inspect or render).
- analytics: separate boundaries and a per-boundary evidence ledger (2 of 3).

CI/CD mandatory failures: in runs 2 and 3 the solver offered or recommended `channel: stable` without a pin because the prompt asks for "latest stable". The prompt is an explicit user request, so the expectation may be too strict.

Raw results: `phase1-new-cases-run1.json`, `phase1-new-cases-run2.json`, `phase1-new-cases-run3.json`.
