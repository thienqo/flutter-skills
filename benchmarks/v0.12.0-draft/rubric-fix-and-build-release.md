# Rubric rewrites and the build-release signature check

Solver and judge: `claude` CLI, default model at run time (Sonnet 5.5), one judge, baseline skipped, 2026-11-01. Same-family judge, so not independent evidence. All runs reported.

## Five cases after the rubric rewrites, three runs

| Case | Before (3 runs) | After (3 runs) | After median | Mandatory failures after |
|---|---|---|---|---|
| flutter-build-release:signing-material-stays-out-of-the-repository | 62, 62, 62 | 88, 93, 95 | 93 | 0 |
| flutter-product-analytics:provider-ingestion-visible-but-attribution-unverified | 52, 62, 55 | 88, 80, 88 | 88 | 0 |
| flutter-package-development:dry-run-passes-but-publisher-or-version-mismatch | 62, 62, 62 | 82, 88, 62 | 82 | 0 |
| flutter-ci-cd:new-job-keeps-the-pinned-toolchain | 82, 62, 22 | 62, 62, 72 | 62 | 0 |
| flutter-figma-workflow:figma-dark-mode-differs-from-existing-theme | 42, 22, 22 | 55, 58, 58 | 58 | 0 |

- The signing case changed because of two edits at once: the `flutter-build-release` skill now names the signature check, and the rubric was not changed for that case. The expectation "verifies the signature of the produced artifact" had been missed 3 of 3 times before and was met afterwards.
- The analytics, package, ci-cd and figma cases changed only in rubric wording. Their scores measure the rewritten rubric, not a skill change, so they are not evidence that a skill improved.
- ci-cd and figma still sit below 80. ci-cd misses vary by run (reuse, permissions). figma misses the dark-mode parity-fixture plan in 3 of 6 judgments.
- The package case still has one run at 62.

## Build-release neighbors, one run before and after the skill edit

| Case | Original SKILL.md | With signature check |
|---|---|---|
| obfuscation-preserves-symbols | 88 | 92 |
| flavor-alignment-across-platforms | 58 | 62 |
| staging-release-artifact | 55 | 55 |
| version-follows-repository-policy | 22 | 22 |

No regression. Three of the four neighbors were already below 80 before the edit and are untouched by it. `version-follows-repository-policy` scores 22 on both versions: a measured weakness in the existing skill, not addressed here.

Raw results: `rubric-fix-run1.json`, `rubric-fix-run2.json`, `rubric-fix-run3.json`, `build-release-neighbors.json`, `build-release-neighbors-before.json`.
