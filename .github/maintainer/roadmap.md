# Flutter Skills Roadmap

Planning baseline: 2026-09-05. This is a proposed sequence, not a release promise or evidence that planned checks have run.

## Product objective

Help coding agents deliver correct Flutter changes with appropriate evidence while preserving the consuming project's SDK, architecture, packages, and user intent. Installation remains static guidance with no provider account or API key requirement. Execution-heavy maintainer evaluations stay optional and separate from installation.

## Current state

- Published baseline: v0.5.0; 36 skills.
- Working tree: responsive-layout geometry and viewport guidance, 164 behavior cases, 57 routing cases, and retained focused evaluation results. These changes are not yet committed or released.
- The overlap and viewport-matrix response evaluations passed their final runs. Matrix prompt/rubric changes mean the 67-to-100 scores are not a controlled measurement of skill improvement.
- One temporary Flutter widget test exercised the geometry snippet. A reusable fixture suite and CI execution of generated Flutter artifacts are still needed.
- The fixed public benchmark remains a six-behavior/seven-routing v0.3 sample. Catalog-wide case definitions do not establish catalog-wide executed coverage.

## Phase 1: Correct known defects and deliver the current work

Priority: P1 for destructive cleanup guidance; P2 for the technical and evaluation defects below.

Work:

1. Review and commit the responsive-layout change with its retained results on a `feature/thiennc-<task>` branch; submit a focused PR to main.
2. Correct device-cleanup guidance so uninstalling an app with user-owned data requires an appropriate data-preservation and authorization decision; prefer disposable test targets.
3. Correct the Dart switch guard example and verify the executable sample with the supported SDK.
4. Correct isolate guidance for synchronous SQLite/FFI work and clarify transferable-data construction versus transfer cost and ownership.
5. Correct Hero tag scope and distinguish in-memory tab preservation from configured process-death restoration.
6. Update accessibility announcement guidance according to the consuming project's SDK and current Flutter API contract.
7. Correct the app-workflow eval that explicitly requests a migration but grades it as unrequested. Keep separate preservation and authorized-migration cases.

Acceptance:

- Each correction has a source-backed explanation or a reproducible failure, plus a focused regression where appropriate.
- Executable examples analyze and their focused tests pass.
- No unresolved P1 from the audit remains in the release scope.
- Release metadata, candidate tag, changelog, installation and distribution contents agree. Publish an immutable patch release only after normal release authorization and gates.

Suggested PR split: responsive-layout guidance; technical correctness corrections; contradictory eval correction. Keep release preparation separate from skill authoring.

## Phase 2: Make evaluation results trustworthy

Depends on the relevant Phase 1 corrections. Complete this before optimizing scores across the full catalog.

Work:

1. Separate response-only, artifact-execution, and device/backend evaluations. Declare required capabilities and supplied evidence for every case.
2. Give expectations stable identifiers. Reject missing, duplicated, unknown, or mismatched judgment entries.
3. Define mandatory expectations for consequential behavior. A failed mandatory expectation must fail the case even when its aggregate score exceeds the threshold. Keep noncritical quality scoring separate.
4. Add a reference-to-case coverage report. First connect the 10 v0.5 references currently absent from all case resource lists; then review other unexercised references individually. Do not inject every reference into every case.
5. Store commit/dirty-state identity, instruction and resource hashes, exact prompt and rubric, runner version, model configuration when available, and execution environment with raw results. Unknown model identity remains explicitly unknown.
6. Distinguish prompt/rubric calibration from measured skill improvement. Compare before/after only under the same case, rubric, capabilities, and model configuration.
7. Expand the fixed benchmark with responsive layout, OpenAPI and known regressions. Keep a separate holdout set that is not used to tune instructions.
8. Add unguided routing evaluation alongside the current policy-assisted routing prompt, plus paraphrased and Vietnamese requests.

Acceptance:

- Synthetic contradictory judgments cannot pass mandatory criteria.
- Response-only cases never demand inaccessible runtime evidence as a condition of success.
- Every changed reference has a relevant executed case or a documented alternative verification.
- Reports distinguish case definitions, executed cases, skips, failures, and environment blocks.
- A bounded repeated run establishes variance for the release-critical subset; report all runs instead of selecting the best result.

## Phase 3: Verify real Flutter artifacts

Start with responsive layout and OpenAPI. Keep maintainer fixtures outside the public skill catalog unless a tested reusable asset materially helps installed users.

### Responsive layout

Create a small version-pinned fixture project and a reproducible runner. Cover:

- A sticky action obscuring the last field without a framework overflow.
- Independent controls that intersect, clipped error text, and an offscreen action.
- A valid badge or intentional overlay that must not be classified as an error.
- Compact/wide viewports, actual breakpoint boundaries, enlarged text, long strings, RTL and simulated keyboard insets.
- Scroll-to-reveal, disjoint/containment/gap contracts, action hit testing, and observable interaction results.

Acceptance: deliberately broken fixtures fail for the intended reason; corrected fixtures pass; valid overlays pass; test view and fixture state do not leak between cases. Retain representative rendered evidence for appearance claims. Widget tests do not establish real OS keyboard or platform-view behavior.

### OpenAPI

Create local Swagger 2.0/OpenAPI 3.x and Swagger UI fixtures with expected operation inventories and wire behaviors. Include external references, cycles, malformed input, nullable/required fields, enums, multipart, empty responses and parameter encoding. Use controlled fake fetchers to verify redirect, origin, credential and traversal policy without contacting sensitive destinations.

Have the agent perform a bounded client-generation task in an isolated project. Analyze the produced Dart and test requests/responses with a fake transport. Check deterministic regeneration and preservation of handwritten files.

Acceptance: inventory matches the fixture oracle; unsupported constructs are disclosed; generated consumers compile; wire tests pass; no live mutation is needed.

### Subsequent artifact coverage

Expand to async form submission, stale search results, authentication refresh/account switching, and persistence migrations according to observed failures. Maintain a supported SDK matrix with a pinned baseline and deliberate compatibility updates.

Prefer fast unit/widget checks and a small integration suite for important platform boundaries, following [Flutter testing guidance](https://docs.flutter.dev/testing/overview). Native permission dialogs and platform views require an appropriate runtime tool, beyond ordinary widget interaction.

## Phase 4: Improve the existing catalog from measurements

Work through skills in risk order:

1. Authentication, purchases, security, persistence and publication: account isolation, idempotency, destructive actions and authority boundaries.
2. Responsive layout, testing, code review, Dart concurrency, navigation and OpenAPI: reproducible defects, false positives and executable output.
3. Analytics and observability: distinguish client dispatch, ingestion and downstream consumer evidence. Add the missing publisher/version mismatch and partially verified analytics cases from the optimization backlog.
4. UI design, effects and performance: representative renders, intentional visual exceptions, and equivalent before/after performance measurements.

For each observed failure: reproduce, classify whether it belongs to routing/instructions/resources/eval/environment, apply the smallest correction, run the regression and adjacent cases, and retain evidence.

Reduce duplicated instructions only when a shared owner or reference preserves behavior and reduces loaded context. Measure discovery size and selected-context size; avoid fixed word-count targets as a proxy for quality. Keep architecture and package preservation cases alongside explicit migration cases.

Acceptance: improved failure behavior on fixed cases and no regression on their neighboring or holdout cases. Report unresolved boundaries rather than a universal quality score.

## Phase 5: Expand only for demonstrated gaps

Candidate areas to investigate, not committed additions:

| Candidate | Distinct work to validate | Existing owner to try first |
|---|---|---|
| Flutter media capture and playback | Camera/audio/video lifecycle, permissions and interruption | platform integration, device testing |
| Flutter maps and location | Location state, map lifecycle, coordinates and foreground/background transitions | platform integration, background execution |
| Flutter app links and sharing | Incoming shared files, intents and outgoing share lifecycle | navigation, platform integration |

Before creating a skill, collect at least three materially different realistic requests, demonstrate why existing specialists plus a reference are insufficient, define positive and negative routing cases, identify primary sources and verification tools, and assign maintenance ownership.

If the work fits an existing skill, add conditional guidance there. Keep `flutter analyze` in delivery verification, test cases in `flutter-testing`, and overlap checks in `flutter-responsive-layout` unless measured usage proves a separate activation boundary.

Acceptance for any new skill: clear ownership, installed discovery works, meaningful executed evaluation, appropriate artifact/runtime evidence, synchronized manifests and documented limitations. Do not set a target skill count.

## Phase 6: Sustainable maintenance and releases

- Per PR: validate metadata, references, packages, eval inputs, package contents and focused deterministic regressions. Run executed evals for changed behavior and adjacent routing when relevant.
- Before release: run the bounded release profile and applicable artifact suite, review warnings/blocks, verify exact candidate installation, then publish through the existing workflow. Confirm each distribution channel independently and retain recovery instructions for partial publication.
- Monthly proposal: review source-content changes, open failures and flaky cases. Link liveness alone is not technical freshness; track reviewed source claims and dates by affected area.
- Quarterly proposal: sample holdout tasks, recheck supported SDK/platform combinations, and retire or consolidate unused guidance with routing evidence.
- Bound evaluation concurrency, time, retained artifacts and spending. Fast local validation must continue to work without provider credentials. Scheduled model execution is optional and should have an explicit budget.

## Quality dashboard

Use these as proposed acceptance targets, not current achievements:

| Measure | Initial target |
|---|---|
| Confirmed P1 issues in release scope | Zero unresolved |
| Mandatory behavior regressions | All pass in the declared release environment |
| Changed instructions and references | Relevant executed evidence or an explicit verification boundary |
| Geometry detector validity | Seeded failures caught; intentional overlays accepted |
| Runnable examples | Analyze and tests pass under the declared SDK |
| Routing | Record missed specialists and unnecessary activations; set a target after measuring baseline |
| Reproducibility | Exact inputs/rubric hashes and raw failures retained |
| Distribution | Candidate version resolves consistently across supported install paths |
| Cost and latency | Report per suite; choose budgets from the first stable baseline |

## Suggested sequence and effort

For one maintainer, reserve roughly one focused work cycle for correctness, one for evaluation integrity, and two for the initial artifact fixtures. The calendar duration depends on SDK/device access and model execution time; reassess after each phase rather than promising a release date.

Prioritize the next three deliverables: finish the existing responsive-layout PR, close known correctness defects, then implement capability-aware and mandatory-criterion evaluation. Afterward, commit the responsive-layout fixture suite and OpenAPI artifact evaluation before considering new catalog entries.
