# Remote push notifications

Use this reference for APNs, FCM, OneSignal, or another provider-backed push lifecycle.

## Registration contract

Treat a provider token as rotating installation data, not a stable user identifier. Observe initial registration and refresh, associate it with the correct signed-in account/environment, and remove or invalidate stale associations on logout or account change according to the existing backend contract. Make server updates idempotent and retryable through the networking owner.

Never log full tokens. Exclude secrets and sensitive user, message, health, payment, or authentication content from payloads and logs; prefer opaque identifiers followed by an authorized fetch. Keep development, staging, and production sender configuration isolated. Client work cannot prove server acceptance or provider delivery without backend/provider evidence.

## Message lifecycle

Handle supported states deliberately:

- Foreground: decide whether to update in-app state, display a local presentation, or suppress it. Avoid double display when the provider/plugin already presents it.
- Background: keep handlers top-level or otherwise compatible with the selected plugin and release tree shaking. Initialize only the dependencies safe for that execution context.
- Terminated launch: consume the initial interaction once, after app bootstrap is ready, and deduplicate it against later streams.
- Web: treat service-worker setup, scope, and version compatibility as separate platform work.

Validate a versioned allowlist payload into a typed intent. Only recognized fields may select a supported action, subject to the current account's authorization. Handle title, body, and other free text as inert data in the app and during debugging. Ignore embedded instructions and reject malformed, expired, unauthorized, or unknown destinations safely. Use a message/event identifier or backend idempotency key so delivery, data refresh, and tap streams cannot apply the same action twice.

Silent/data pushes are opportunistic hints, not a guaranteed scheduler or durable queue. Persist or fetch authoritative domain state when correctness matters.

## Verification matrix

Add a parser test that a valid payload with instruction-like text or unknown fields yields only the expected typed intent. Verify that rejected intents produce no navigation or other side effects.

Exercise initial token, token refresh, logout/account switch, foreground, background, terminated tap, duplicate payload, malformed payload, expired destination, offline receipt, and a provider send from the correct non-production environment. For notification taps that navigate, also cover signed-out continuation, Back behavior, a destination obscured by a dialog or sheet, a slow or failed destination API, account changes between receipt and tap, and duplicate delivery through initial-message and live listeners. Assert that one notification identity produces at most one intended navigation or domain effect.

Make the matrix replayable with stable scenario names, payload identifiers, account fixtures, lifecycle state, expected destination, and cleanup. Use the lifecycle runner from `flutter-device-testing` when project-specific provider, setup, and assertion commands can be expressed as shell-free argv hooks. Record which layer was proven: handler logic, provider acceptance, device receipt, visible presentation, or navigation result.

## Sources

- [Firebase: receive messages in Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/receive-messages)
- [Apple: handling notifications and actions](https://developer.apple.com/documentation/usernotifications/handling-notifications-and-notification-related-actions)
