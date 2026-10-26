# Contributing to Flutter Skills

Contributions should solve a concrete agent behavior problem and remain focused enough to review, evaluate, and maintain.

## Skill rules

1. Use a lowercase, hyphenated folder name matching the `name` in `SKILL.md`.
2. Make the description explain both capability and selection boundary.
3. Inspect and preserve the target project's current architecture, packages, SDK constraints, and platforms.
4. Do not promote a third-party package as a universal default.
5. Keep primary instructions concise; move conditional detail into linked references.
6. Require proportionate evidence such as formatting, analysis, tests, profile data, or device behavior.
7. Add or update behavior-focused evaluation cases.

## Evaluation cases

Each public skill contains `evals/cases.json`. Cases require a stable `name`, a realistic `prompt`, and an array of observable `expectations`. Include at least one successful capability case and one boundary or preservation case.

When a case needs conditional material, list only directly linked skill references in its optional `resources` array. Do not inject every reference by default; cases without `resources` evaluate the entrypoint alone.

Cross-skill discovery conflicts belong in `.github/evals/routing-cases.json`. A routing case declares the smallest `required` set, acceptable `optional` specialists, and skills that are explicitly `forbidden` for that prompt.

The deterministic check validates every case without credentials:

```sh
python3 .github/scripts/run_behavior_evals.py
```

Forward execution is opt-in and defaults to one case to bound cost. It solves behavior cases both without and with the skill, judges observable expectations, and scores routing selections deterministically:

```sh
python3 .github/scripts/run_behavior_evals.py --execute --suite all --max-cases 1
```

## Local checks

```sh
python3 .github/scripts/validate_repository.py
python3 .github/scripts/run_behavior_evals.py
python3 -m unittest discover -s tests -v
npm ci
npm test
npm run pack:check
bash .github/scripts/run_dart_skills_lint.sh
npx skills add . --list
```

If marketplace metadata changes, also run:

```sh
claude plugin validate .
```

Before publishing, finalize the version heading in `CHANGELOG.md` with an ISO date and run:

```sh
python3 .github/scripts/validate_repository.py --release
```

The npm package uses trusted publishing. Configure `@thiennc/flutter-skills` on npm with GitHub Actions publisher `thienqo/flutter-skills`, workflow filename `release.yml`, and permission to run `npm publish`. The tag-only release workflow uses OIDC, publishes provenance, verifies the immutable registry version, and smoke-tests the installed CLI before continuing to Tessl and GitHub Release.

## Pull-request checklist

- [ ] The change addresses one clear problem.
- [ ] Frontmatter, links, and source claims are valid.
- [ ] Existing project choices remain respected.
- [ ] Evaluation coverage was added or updated.
- [ ] Validation and tests pass locally.
- [ ] Bundle membership and versions remain aligned.

By contributing, you agree that your contribution is distributed under the repository's BSD 3-Clause License.
