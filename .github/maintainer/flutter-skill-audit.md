# Flutter Skill Audit

Audit skills as operational instructions for coding agents, not as general Flutter tutorials. Keep the audit read-only unless implementation is explicitly requested.

## Modes

- **Focused:** one skill, its references, evaluations, and neighboring routing boundaries.
- **Collection:** inventory, discovery cost, overlap, sources, package metadata, and evaluation coverage.
- **Release:** collection audit plus versions, clean installation, credentials, tag, and publishing gates.

## Checks

### Discovery

- Folder and frontmatter names align.
- Descriptions state capability and activation boundary.
- Neighboring skills do not compete unnecessarily.
- Combined discovery text remains proportionate to the catalog.

### Instructions

- Guidance preserves the target project's SDK constraints, architecture, packages, and platforms.
- Absolute rules correspond to correctness, safety, or external authorization.
- Conditional detail is in a directly linked reference.
- Third-party packages are selected by project evidence rather than popularity.

### Technical accuracy

- Flutter and Dart claims match current official documentation.
- Package claims match current publisher documentation and compatible constraints.
- Debug, profile, and release evidence are distinguished correctly.
- Device-only or native behavior is not presented as widget-test evidence.
- Examples account for lifecycle, async ownership, error handling, accessibility, and disposal where relevant.

### Evaluations

- Prompts resemble real work.
- Expectations test observable decisions or evidence, not exact wording.
- Each skill has a successful case and a boundary/preservation case.
- Demonstrated regressions receive focused cases.
- Use [evaluation strategy](evaluation-strategy.md) to choose focused, nightly, release, cross-judge, human-review, and compiler-backed evidence without overstating coverage.

## Collection validation

```sh
python3 .github/scripts/validate_repository.py
python3 .github/scripts/run_behavior_evals.py --coverage
python3 .github/scripts/run_executable_evals.py
python3 .github/scripts/run_eval_matrix.py
python3 .github/scripts/run_eval_matrix.py --matrix .github/evals/cross-agent-matrix.json
python3 -m unittest discover -s tests -v
claude plugin validate .
npx skills add . --list
```

Confirm exact membership across `skills/`, Codex plugin metadata, the Claude plugin, and Tessl metadata. Review version alignment, README counts, changelog entries, CI status, npm registry state, and missing release credentials.

## Release gate

A release is ready only when validation passes, clean discovery returns the expected catalog, changed behavior has executed evaluation evidence, versions align, the npm trusted publisher targets `release.yml`, and release notes describe user-visible changes. Run `python3 .github/scripts/validate_repository.py --release` to require a dated version heading and reject an `Unreleased` marker before publication.

Do not create a tag, GitHub Release, Tessl publication, or other registry release without user authorization.
