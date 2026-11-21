# Fetch, activation, and verification

Fetching and activating are separate steps in most providers, and the difference decides when a user sees a change.

## Fetch versus activate

Firebase Remote Config stores fetched values in the SDK; `activate()` makes them available to the app, and `fetchAndActivate()` performs both. Activating at a deliberate boundary (app start, next session, or an explicit foreground refresh) avoids a value changing in the middle of a screen or gesture. The FlutterFire guide recommends activating at a time that keeps the experience smooth, such as the user's next app open.

Never fetch from `build`, a gesture handler, or a per-frame path. A short adapter that owns initialization, fetch, activation, and the last-known-good cache is the unit to test.

## Freshness, throttling, and real time

- Firebase Remote Config has a minimum fetch interval (12 hours by default) and throttles excessive fetches; `lastFetchStatus` reports `RemoteConfigFetchStatus.throttle`. Lower intervals are for development only and can hit service-side quotas when distributed broadly.
- Real-time Remote Config (`onConfigUpdated`) automatically fetches a published version and bypasses the minimum interval in recent Flutter SDKs, but real-time config is not available on Web. Do not assume real-time delivery on every platform.
- Web and Windows support depends on the plugin version; check the resolved `firebase_remote_config` version and its documented platforms before promising behavior.

## Offline and failure behavior

Define what happens when the network is unavailable, the provider is unreachable, or the fetch times out:

- use the last known good values when they are still valid for the running app version;
- otherwise use the in-app defaults, never a crash or an empty screen;
- keep initialization bounded with a timeout, and never block the first frame on a fetch.

Client SDKs commonly store the latest variation values and fall back to values defined in code when none exist; LaunchDarkly documents this for its client-side SDKs and provides an offline mode suitable for tests. The exact API is provider-specific; the required behavior is not.

## Evidence per boundary

A successful fetch, a console value, or a local print proves only that one boundary worked. Report separately:

1. the client received and parsed the expected value (deterministic test or debug log, without leaking values);
2. the configured audience or rollout evaluated to that value in an authorized non-production environment;
3. the app behavior actually changed, observed on a supported runtime;
4. any downstream consumer of the value, when the task includes one.

State which of these were not observed. A console screenshot is configuration evidence, not runtime evidence; a widget test with a fake source is not audience evidence.

## Tests to keep

- default → fetched → activated transition, and activation not applied mid-session unless intended;
- fetch failure, timeout, and offline, each falling back predictably;
- malformed and out-of-range values falling back to the default;
- version-gated rollout: an older app version keeps the conservative path;
- kill switch disable path;
- no secret or personal data in any value or log.

## Sources

- [Firebase Remote Config for Flutter — getting started (fetch, activate, throttling, real time)](https://firebase.google.com/docs/remote-config/get-started?platform=flutter)
- [Firebase Remote Config loading strategies](https://firebase.google.com/docs/remote-config/loading)
- [firebase_remote_config package (platform support and version)](https://pub.dev/packages/firebase_remote_config)
- [LaunchDarkly offline mode (stored values and fallbacks)](https://launchdarkly.com/docs/sdk/features/offline-mode)
