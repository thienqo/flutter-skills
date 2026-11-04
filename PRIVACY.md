# Privacy Policy

Last updated: 2026-11-04

This policy covers the `thienqo-flutter-skills` plugin and the Flutter Skills collection in this repository.

## Summary

The maintainer does not run a service for this plugin and does not collect, receive, or store your data. The plugin has no telemetry, analytics, or accounts.

## What the plugin contains

- Skills: Markdown instructions that your AI agent reads.
- One optional helper script, `skills/flutter-device-testing/scripts/run_lifecycle_matrix.py`.
- No hooks, MCP servers, connectors, or background processes.

## How data is handled

**Skills.** Your agent reads the skills during your session, alongside your prompts and project files. The provider of your AI agent processes that content under its own terms and privacy policy. It is not sent to the maintainer.

**Helper script.** The script runs only when you or your agent starts it. It uses `adb` or `xcrun simctl` to drive a device or simulator on your machine, and sends nothing over the network itself. With `--report`, it writes results to the local path you choose. It redacts common bearer tokens, access tokens, refresh tokens, and cookies, but this is best effort, so review a report before sharing it.

**Commands your agent runs.** Skills can guide your agent to run tools in your project, such as build, test, or API commands. Those commands reach only the services your project or your request names, and they run under your agent's permission settings.

## Third-party services

These services are not operated by the maintainer and have their own privacy terms:

- **npm registry.** The repository includes `package.json` and `package-lock.json`, so installing the plugin can download the pinned `skills` package. Installing through `@thiennc/flutter-skills` also uses npm.
- **GitHub.** The plugin and the npm installer download files from this repository.

## Retention

The maintainer retains no data from your use of the plugin. If you open a GitHub issue or pull request, what you post is public and governed by GitHub's terms.

## Children

The plugin is intended for software developers and is not directed at people under 18.

## Changes

Changes to this policy are recorded in this file's Git history.

## Contact

Open an issue at <https://github.com/thienqo/flutter-skills/issues>.
