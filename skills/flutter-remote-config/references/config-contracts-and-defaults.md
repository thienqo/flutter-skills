# Config contracts and defaults

Remote config is a runtime input, not a trusted source of truth. Treat every fetched value as data that may be missing, stale, malformed, or written for a different app version.

## In-app defaults are part of the contract

Set in-app defaults before any value is read, so the app behaves correctly before the first fetch and whenever the backend has no value for a key. A key that exists only in the console has no safe behavior when the fetch fails or the device is offline.

For each key record:

- the type and allowed values or range;
- the in-app default;
- the behavior when the backend value is absent, invalid, or older than the app expects;
- the owner who can change it and the environments where it applies.

Firebase Remote Config uses `setDefaults` before `fetch`/`activate`, and falls back to those defaults when the backend does not define a value. See the FlutterFire getting-started guide in Sources.

## Parse into a bounded type

Provider APIs return typed getters (`getBool`, `getInt`, `getDouble`, `getString`) or strings; neither validates domain meaning. Wrap reads in one accessor layer that:

- maps a string to an enum with an explicit fallback for unknown values;
- clamps numbers to a supported range and rejects non-finite values;
- caps payload length and nesting depth for JSON-in-string keys;
- ignores unknown keys instead of failing, and logs the key name (not its value) once per session;
- returns the in-app default on any parse failure instead of throwing in a widget.

Never evaluate configuration as code, and never let a config payload choose an arbitrary widget, route, or native entry point without a fixed allowlist.

## Schema evolution

Config is shared with releases you cannot see. Use versioned keys or an explicit schema version in the payload, add new keys with defaults before code depends on them, and remove old keys only after the supported app versions no longer read them. A removed key must degrade to the in-app default, not to an exception or a blank screen.

## What must never live in config

A remote-config value is available to the client instance; end users can access any default or fetched parameter that reaches the app. Therefore config must not carry:

- credentials, API secrets, server keys, or signing material;
- personal data or free-form user content;
- authorization decisions, entitlement grants, or price truth;
- large assets or content that belongs in a CDN or backend.

Firebase's documentation states that confidential data must not be stored in Remote Config parameter keys or values. Provider-specific wording varies; the constraint is the same for every client-side config service.

## Sources

- [Firebase Remote Config for Flutter — getting started](https://firebase.google.com/docs/remote-config/get-started?platform=flutter)
- [Firebase Remote Config loading strategies](https://firebase.google.com/docs/remote-config/loading)
- [firebase_remote_config package (platform support and version)](https://pub.dev/packages/firebase_remote_config)
