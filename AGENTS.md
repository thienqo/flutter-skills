# Repository instructions

## Purpose

This repository contains Agent Skills for Flutter and Dart app delivery. It is not a Flutter application or reusable Dart package. Treat changes as instruction, routing, evaluation, and distribution work.

## Required authoring workflow

Before creating or substantially revising a skill:

1. Follow the active Agent Skills authoring guidance available in the agent environment.
2. Inspect the affected skill, neighboring descriptions, evaluation cases, package manifests, and working tree.
3. Verify technical claims using the source rule below.
4. Preserve existing project architecture and package choices unless the user's task explicitly requests migration.
5. Add or update behavior-focused evaluation cases.

For any new or changed technical claim under `skills/`, verify it against current primary sources and record the applicable SDK, package version, or platform scope where it affects the guidance. Cite official documentation, publisher changelogs, or matching source code. Dart and Flutter MCP is optional for inspecting resolved symbols and running local checks.

## Git, branching, and pull request workflow

When implementing any feature, bug fix, refactor, evaluation, or documentation update:

1. **Always work in a separate branch (Never commit directly to `main`)**:
   - Before starting, ensure `main` is up to date:
     ```sh
     git checkout main && git pull origin main
     ```
   - Create and checkout a descriptive topic branch with an appropriate prefix:
     - `feature/<name>` for new capabilities, skills, or tooling (e.g. `feature/eval-coverage-gate`)
     - `fix/<name>` for bug fixes, corrections, or broken links (e.g. `fix/device-cleanup-guidance`)
     - `refactor/<name>` for restructuring without functional changes
     - `docs/<name>` for documentation-only updates
     - Or `<username>/<topic>` (e.g. `thiennc/phase2-eval-engine`)
     ```sh
     git checkout -b feature/<feature-name>
     # or
     git checkout -b fix/<fix-name>
     ```

2. **Validate locally before committing**:
   - Run the required validation commands:
     ```sh
     python3 .github/scripts/validate_repository.py
     python3 .github/scripts/run_behavior_evals.py --coverage
     python3 -m unittest discover -s tests -v
     npm test
     npm run pack:check
     ```

3. **Commit with semantic and atomic messages**:
   - Use conventional commit messages: `feat(...)`, `fix(...)`, `docs(...)`, `test(...)`, `refactor(...)`.

4. **Push and create a Pull Request**:
   - Push the branch to origin:
     ```sh
     git push -u origin <branch-name>
     ```
   - Create a Pull Request with a clear summary and verification plan:
     ```sh
     gh pr create --title "..." --body "..."
     ```

5. **Verify CI and merge**:
   - Monitor GitHub Actions status:
     ```sh
     gh pr checks <pr-number> --watch
     ```
   - Only merge after all CI checks pass:
     ```sh
     gh pr merge <pr-number> --squash --delete-branch
     ```
   - Switch back to `main` and pull the latest merge commit:
     ```sh
     git checkout main && git pull origin main
     ```

## Skill rules

- Keep `SKILL.md` concise and place conditional detail in directly linked references.
- Make frontmatter descriptions cheap, precise, and discriminating.
- Define boundaries between nearby specialists to prevent broad activation.
- Do not promote Provider, Riverpod, Bloc, Dio, Drift, go_router, or another third-party package as a universal default.
- Read `pubspec.yaml` and SDK constraints before recommending syntax or packages.
- Prefer current official Flutter and Dart documentation; use package-publisher documentation for package-specific behavior.
- Require evidence proportionate to the claim: formatting, analysis, tests, profile-mode measurements, or device behavior.
- Ensure all reference documents in `references/` are covered in `.github/evals/behavior/<name>/cases.json` (`python3 .github/scripts/run_behavior_evals.py --coverage` must report 100%).
- Designate critical correctness, security, or constraint expectations with `mandatory: true` to enforce strict evaluation gating.
- Keep maintainer-only workflows outside `skills/` so they do not enter the public catalog.

## Surfaces that must stay synchronized

When adding, removing, or renaming a skill, update:

- `skills/<name>/SKILL.md`
- `.github/evals/behavior/<name>/cases.json`
- `.codex-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `.tessl-plugin/plugin.json`
- `README.md` counts and catalog
- `CHANGELOG.md`

## Validation

Run before committing:

```sh
python3 .github/scripts/validate_repository.py
python3 .github/scripts/run_behavior_evals.py --coverage
python3 -m unittest discover -s tests -v
npm ci
npm test
npm run pack:check
bash .github/scripts/run_dart_skills_lint.sh
claude plugin validate .
npx skills add . --list
```

When forward-evaluation behavior changes, run the smallest relevant executed case or the fixed public profile and retain the raw result. Do not rewrite skills without a measured failure or a current primary-source change.

For a full audit or release review, follow [the maintainer audit workflow](.github/maintainer/flutter-skill-audit.md).

Before publishing, replace the version's `Unreleased` marker with an ISO date and run `python3 .github/scripts/validate_repository.py --release`.

## Safety and scope

- Preserve unrelated user changes.
- Do not publish packages, create releases, change signing material, upload apps, or mutate live services without explicit authorization.
- Do not claim device, build, test, or performance verification that was not actually performed.
- If credentials or platform tooling block verification, state the exact boundary instead of weakening the check.
