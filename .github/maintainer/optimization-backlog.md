# Measured optimization backlog

Use this file for failures and weak signals observed in executed forward evaluations. Do not rewrite a public skill from intuition alone: link the raw result, identify the failed behavior, add the smallest regression case, and rerun that case before changing broader guidance.

## Open

| Priority | Evidence | Measured signal | Next evaluation |
|---|---|---|---|
| P2 | [`rubric-fix-and-build-release.md`](../../benchmarks/v0.12.0-draft/rubric-fix-and-build-release.md) | `flutter-build-release:version-follows-repository-policy` scores 62, 62, and 72 after the rubric asks for a plan: the solver still states "always raise the build number" as a rule before it has read the repository policy. `flavor-alignment-across-platforms` (58 to 62) never says it will check the built application ID or bundle identifier. | Add one sentence to `flutter-build-release` that a build-number rule is read from the repository, not assumed, and that flavor verification checks the built artifact's application ID. Run both cases three times. |
| P2 | same report | `flutter-ci-cd:new-job-keeps-the-pinned-toolchain` (62, 62, 72) misses job-convention reuse and a stated least-privilege `permissions` block on some runs; `flutter-figma-workflow:figma-dark-mode-differs-from-existing-theme` (55, 58, 58) misses the explicit "parity not rendered" statement. | Collect two more runs each before changing either skill, because the misses differ between runs. |
| P3 | `phase1-new-cases-variance.md` | `flutter-observability:crash-context-excludes-pii-and-payloads` sometimes omits retention and an opt-in payload path (72, 90, 72). | Add a run with the rewritten rubric before judging the skill. |

## Closed and retained as regressions

- `flutter-persistence:migration-failure-preserves-prior-user-data`: the [initial 60-point run](../../benchmarks/unreleased/flutter-persistence-migration-safety-initial.json) preserved durable rows but omitted explicit released prior-version fixtures, the exact target-version assertion, and resolved package and SDK contract inspection. The package-neutral migration and recovery reference now requires all three, and the [focused rerun](../../benchmarks/unreleased/flutter-persistence-migration-safety.json) passed at 100; both [routing boundaries](../../benchmarks/unreleased/flutter-persistence-routing-boundaries.json) also passed.
- `flutter-runtime-debugging:runtime-fix-repeats-original-flow`: require a clean launch for every affected target and record unsupported-platform behavior instead of extrapolating from hot reload.
- `flutter-in-app-purchases:sandbox-readiness-is-not-store-publication`: accept an executable sandbox evidence plan when store credentials or consoles are unavailable; never fabricate readiness or publish.
- `flutter-product-analytics:sdk-log-is-not-end-to-end-proof`: record client dispatch, provider ingestion, and downstream dashboard or funnel evidence separately.
- `flutter-webview` routing: the first focused run interpreted “existing Flutter WebView package” as reusable-package development and selected `flutter-package-development`. The app-focused prompt now states that the existing dependency is not being changed or distributed; both WebView and OAuth boundary cases pass in the retained rerun.
- `flutter-openapi-client:swagger-ui-discovery-does-not-execute-remote-javascript`: the first focused run chose safe static inspection but omitted unsupported executable syntax and the acquisition boundary. The skill now requires a discovery ledger; the retained rerun passed at 96.
- `flutter-openapi-client:external-refs-do-not-expand-network-or-credential-authority`: the first focused run blocked the explicit metadata target but omitted per-hop handling, all inherited sensitive material, and traversal bounds. The skill now constrains network, filesystem, credential-origin, redirect, and resource authority; the retained rerun passed at 100.
- `flutter-product-analytics:provider-ingestion-visible-but-attribution-unverified`: added for the case where provider ingestion is visible but warehouse and experiment attribution are not. After the rubric asked for a per-boundary ledger, the three-run scores were 88, 80, and 88 ([rubric-fix runs](../../benchmarks/v0.12.0-draft/rubric-fix-and-build-release.md)). Earlier scores were 52, 62, and 55 under a rubric that demanded exact queries a response-only solver cannot name.
- `flutter-package-development:dry-run-passes-but-publisher-or-version-mismatch`: added for a passing dry run with a mismatched version and publisher. The mandatory stop-publication expectation held in every run; the three-run scores were 82, 88, and 62 after the rubric asked for a readiness plan instead of completed checks. One run stays below 80.
- Capability-aware evaluator validation: `validate_repository.py` now accepts an optional case `capabilities` field and warns when an expectation asks a response-only solver for device, design-tool, provider-console, or registry evidence without the declaration. Covered by a unit test; no forward run applies.
- Forward-evaluation execution: bound each solver invocation so a stalled agent cannot hang the full profile.

## Promotion rule

Move an item to closed only after the focused executed case passes and the raw before-and-after result is retained. A current primary-source correction can bypass the measured-failure requirement, but must cite the changed source and receive a behavior or routing regression case where practical.
