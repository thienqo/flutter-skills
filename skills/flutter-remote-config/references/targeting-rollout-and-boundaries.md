# Targeting, rollout, and boundaries

Configuration changes behavior for a population, not a single screen. Decide who receives a value, how much of the population, and how the change is undone before writing any client code.

## Targeting inputs

Providers target by app version, platform, locale, and user properties or audiences. Keep the attribute set small, stable, and explainable; every attribute is a debugging dimension and a privacy surface. Confirm an attribute exists in the environment before using it, because conditions that reference an absent attribute silently do not match.

Firebase Remote Config conditions that target user properties or audiences require Google Analytics to be enabled for the project; verify that prerequisite before promising targeting behavior.

## Staged rollout and kill switches

- A rollout plan names the percentage or audience, the metric or signal that gates expansion, and the condition that stops it.
- A kill switch must be reachable by the same operator in the same environment, and its disabled path must be tested before it is needed.
- Rollback is a configuration change, not an app release: if reverting requires a build, the change belongs in the release plan.
- State the observation window; expanding a rollout without one is a decision to keep it.

## Version gating

The oldest supported app version may not contain the code path the flag enables. Gate new behavior behind both the config value and an app-version check, and make the default for unknown versions the conservative one. When a key is removed, older builds must fall back to their in-app default rather than to a broken state.

## Config is never authorization

A client-readable value cannot decide access. Config may shape presentation and non-sensitive behavior, but entitlement, authorization, pricing, and safety decisions stay with the trusted owner:

- entitlements with `flutter-in-app-purchases` and `flutter-payments-checkout`;
- authorization and secrets with `flutter-security` and the backend;
- pricing truth in the backend, never in a flag.

Anyone able to see a value can also observe the decision it drives; do not put sensitive logic on the client and rely on the flag being hard to find.

## Experiment boundary

Config-delivered variants and analytics exposure are different events. Coordinate with `flutter-product-analytics`: log an exposure only when the subject actually receives the variant, deduplicate it for the definition window, and never log an exposure for every config read. Targeting attributes used for experiments must not become identifiers in logs.

## Change checklist

Before enabling a change, record: audience, percentage, default for out-of-audience users, app versions that understand it, kill-switch owner, rollback path, and the evidence required to expand. If any item is unknown, the change is not ready.

## Sources

- [Firebase Remote Config for Flutter — getting started (conditions and Analytics prerequisite)](https://firebase.google.com/docs/remote-config/get-started?platform=flutter)
- [Firebase Remote Config parameters and conditions](https://firebase.google.com/docs/remote-config/parameters)
- [LaunchDarkly Flutter SDK reference](https://launchdarkly.com/docs/sdk/client-side/flutter)
