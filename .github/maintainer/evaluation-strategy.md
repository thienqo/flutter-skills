# Evaluation strategy

Use the least expensive tier that can answer the current question. Forward evaluation invokes external agents and must remain an explicit maintainer action; repository CI only validates cases, profiles, fixtures, and matrix configuration.

## Trust model

- The default workflow needs only the authenticated Codex CLI: Codex solves and scores the fixed cases, compiler-backed fixtures verify executable behavior, and a named human reviews 10–15% of any published run.
- Treat same-model scoring as regression screening, not independent judgment. It must not be reported as cross-provider evidence.
- When another authenticated provider is available, prefer an independent primary judge and add the solver family as a second judge to measure agreement. A behavior case passes only when every judge reaches the threshold and every mandatory criterion passes.
- Treat model agreement as calibration evidence, not proof that either judge is correct.
- Keep raw failed and successful results. Do not discard disagreement or failed cases to improve reported averages.
- Do not claim cross-provider evidence when either CLI is unauthenticated, unavailable, or timed out.

## Cost tiers

### Pull request

Run only changed-skill cases during ordinary authoring. Use the fixed [PR smoke profile](../evals/profiles/pr-smoke.json) when shared routing, runner, or catalog behavior changes.

```sh
python3 .github/scripts/run_eval_matrix.py \
  --execute \
  --output-dir benchmarks/matrix
```

The default [Codex matrix](../evals/codex-matrix.json) skips baselines and needs 19 model invocations for the six behavior and seven routing cases. It uses the existing Codex CLI login; no Claude account or OpenAI API key is added or required.

### Nightly or periodic audit

The [nightly representative profile](../evals/profiles/nightly-representative.json) contains one behavior case for every skill and all routing cases. The Codex-only matrix with skipped baselines needs 174 model invocations (two per behavior case plus one per routing case). Refresh baselines only when measuring skill lift.

### Release

The [release profile](../evals/profiles/release-full.json) resolves all behavior and routing cases. The default Codex-only run with skipped baselines needs 638 model invocations before retries (two per behavior case plus one per routing case). Run it only with an explicit budget and retained output.

## Holdout cases

[`holdout.json`](../evals/holdout/holdout.json) reserves 23 behavior cases, at least one for each high-risk skill, to detect overfitting. `validate_repository.py` fails when a holdout case is unknown, repeated, or listed in a tuning profile (`pr-smoke` and `nightly-representative`).

- Read holdout results only at release review, after tuning is finished.
- Do not reword a skill to match a holdout prompt or expectation. Fix the behavior with a separate tuning case, then re-measure the holdout.
- When a holdout case must change, replace it with another case from the same skill and record the reason in `CHANGELOG.md`.
- The `release-full` profile selects every case and is a release audit, not a tuning run.

## Response-only capabilities

A behavior case runs against a response-only solver by default. A case whose expectations ask the solver to carry out device, design-tool, provider-console, or registry work declares it with `"capabilities": ["device"]`. `validate_repository.py` rejects unknown capability names and warns when an expectation asks for that evidence without the declaration. Expectations that ask for a plan or an explicit unverified boundary are not flagged.

## Optional cross-agent matrix

Normal validation checks the Codex-only default without invoking a model:

```sh
python3 .github/scripts/run_eval_matrix.py
```

The optional [cross-agent matrix](../evals/cross-agent-matrix.json) is also validated in CI but never executed there. Use it only after both CLIs are authenticated:

```sh
python3 .github/scripts/run_eval_matrix.py \
  --execute \
  --matrix .github/evals/cross-agent-matrix.json \
  --output-dir benchmarks/matrix
```

The PR profile needs 50 model invocations for the two skipped-baseline role-swap runs. Use `--profile profiles/nightly-representative.json` or `--profile profiles/release-full.json` for a broader tier. If Claude is unavailable, skip this matrix and report Codex, executable, and human-review evidence separately.

Do not add another provider until its CLI has a verified non-interactive input/output contract, bounded timeout behavior, model selection, authentication failure handling, and equivalent tool isolation.

## Human calibration

Create a deterministic 15% sample tied to the raw result and response hashes:

```sh
python3 .github/scripts/review_eval_results.py sample \
  benchmarks/matrix/codex-solver.json \
  --rate 0.15 \
  --seed 20260911 \
  --output benchmarks/matrix/codex-solver-human-review.json
```

Fill `reviewer`, `reviewed_at`, each `human_met`, and optional notes. Then report agreement per judge:

```sh
python3 .github/scripts/review_eval_results.py summarize \
  benchmarks/matrix/codex-solver.json \
  benchmarks/matrix/codex-solver-human-review.json
```

Changing the source result or sampled response invalidates the hashes and blocks summarization.

## Compiler-backed fixtures

Executable cases live under `.github/evals/executable`. Validate their manifests in normal CI:

```sh
python3 .github/scripts/run_executable_evals.py
```

Run a case only with explicit authorization:

```sh
python3 .github/scripts/run_executable_evals.py \
  --execute \
  --case dart-concurrency-latest-wins \
  --output benchmarks/unreleased/dart-concurrency-latest-wins-executable.json
```

The runner copies a fixture to a temporary workspace, instructs the agent to avoid network and external services, allows only declared source owners to change, rejects verifier or package-metadata edits, and then executes allowlisted `dart` or `flutter` checks with timeouts. The agent uses the Codex workspace-write sandbox; the post-run file guard and check allowlist are not a network or shell security sandbox. Keep fixtures deterministic, dependency-light, free of credentials, and independent of live services. Add `flutter build` only when compilation at that platform boundary is material; prefer format, analysis, focused tests, and runtime assertions for ordinary cases.

The `responsive-checkout-geometry` case uses Flutter 3.44.8 and immutable widget tests. Its CI proof runs the broken starter, a passing oracle, and isolated clipping, sticky-action, and offscreen-action mutations via `.github/scripts/verify_responsive_fixture.py`. The starter also proves that a missing wide composition fails at the 600-pixel boundary. This verifies the test oracle before an agent run. An executed agent result additionally shows whether the skill led the agent to a passing code change; widget tests do not establish real OS keyboard or screen-reader behavior.

The `app-workflow-task-completion` case uses the same pinned Flutter SDK and integrates a repository, ChangeNotifier owner, and widget with a controlled API. The agent can inspect a local catalog of optional specialists and read only relevant instructions/references; the copied library and acceptance tests are immutable. Only `lib` and agent-authored `test/regression` changes are allowed. The runner retains the prompt, input hashes, response, patch, and host checks; a final statement of skill selection is self-reported, not a tool-read audit. The host permits only the exact `flutter pub get --offline --enforce-lockfile` setup command in addition to ordinary checks, so populate the pinned package cache before execution.

Run `python3 .github/scripts/verify_app_workflow_fixture.py` to prove the corrected oracle passes seven acceptance scenarios and seeded repository, duplicate-submit, late-disposal, and hidden-error defects fail. CI runs that deterministic proof without invoking an agent. Executed agent results demonstrate a bounded feature implementation against fake-API unit/widget checks, not a device test, live-backend test, or proof of native skill discovery in every agent host.

The `media-source-ownership` case uses a dependency-free fake player that supports overlapping opens and returns distinct handles. Its six runtime scenarios verify latest-source ownership, stale-handle release, stop/disposal, replacement, and cleanup errors. `verify_media_fixture.py` proves the oracle and seeded failures in CI; it does not test exclusive camera acquisition or a real media backend. `check_media_discovery.py --output /tmp/media-install.json` smoke-tests local installation. Its optional `--execute` invokes Codex once with no skill named in the request and retains successful command-read evidence plus full events. That native smoke is separate from policy-assisted catalog routing and never runs a model in ordinary CI.
