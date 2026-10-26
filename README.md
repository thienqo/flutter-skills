# Flutter Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-37-2ea44f)](skills/)
[![Validation](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml/badge.svg)](https://github.com/thiennc-tesoglobal/flutter-skills/actions/workflows/validate-repository.yml)
[![License](https://img.shields.io/badge/License-BSD--3--Clause-blue)](LICENSE)

Agent Skills for building, reviewing, testing, and shipping Flutter and Dart apps, informed by real-world projects.

Give your coding agent focused guidance that respects your project's architecture and packages, checks API assumptions, and backs completion claims with verification evidence.

## Install

Choose your agent and skills interactively:

```sh
npx @thiennc/flutter-skills
```

Installs into the current project. Add `--global` to use across projects.

<details>
<summary>Install as a Codex or Claude Code plugin</summary>

Codex:

```sh
codex plugin marketplace add thiennc-tesoglobal/flutter-skills
codex plugin add flutter-skills@flutter-skills
```

Claude Code:

```sh
/plugin marketplace add thiennc-tesoglobal/flutter-skills
/plugin install flutter-core-skills@flutter-skills
```

Claude bundles: `all-flutter-skills`, `flutter-core-skills`, `flutter-ui-skills`, and `flutter-engineering-skills`.

</details>

## Use

Start with `flutter-app-workflow` for a feature, or name a specialist for a focused task:

```text
Use $flutter-openapi-client to read this Swagger contract and generate
the Customer APIs using this project's existing networking stack.
```

Skills guide the agent through implementation and verification, with clear reporting of what was tested and what remains unverified.

## Catalog

**37 skills** covering Dart, architecture, UI, APIs, testing, debugging, and release delivery.

<details>
<summary>Browse all skills</summary>

| Area | Skills |
|---|---|
| Workflow | `flutter-app-workflow`, `flutter-dependency-upgrades`, `flutter-build-release`, `flutter-ci-cd`, `flutter-device-testing` |
| Dart | `dart-language`, `dart-concurrency` |
| Architecture | `flutter-architecture`, `flutter-state-management` |
| UI | `flutter-ui-design`, `flutter-figma-workflow`, `flutter-visual-effects`, `flutter-ui-patterns`, `flutter-responsive-layout`, `flutter-text-rendering`, `flutter-animation`, `flutter-navigation` |
| Data & AI | `flutter-networking`, `flutter-openapi-client`, `flutter-persistence`, `flutter-ai-integration` |
| Identity & product | `flutter-authentication`, `flutter-in-app-purchases`, `flutter-product-analytics` |
| Quality | `flutter-code-review`, `flutter-security`, `flutter-testing`, `flutter-runtime-debugging`, `flutter-performance`, `flutter-observability`, `flutter-accessibility`, `flutter-localization` |
| Platform & packages | `flutter-background-execution`, `flutter-platform-integration`, `flutter-package-development`, `flutter-notifications`, `flutter-webview` |

</details>

## Quality

**220 behavior-focused evaluation cases** and **76 cross-catalog routing cases** define expected behavior and skill selection. See [measured results](benchmarks/README.md) and [contribution guidelines](CONTRIBUTING.md).

## License

[BSD 3-Clause](LICENSE). Independent project; not affiliated with or endorsed by Google or the Flutter team. Flutter and Dart are trademarks of Google LLC.
