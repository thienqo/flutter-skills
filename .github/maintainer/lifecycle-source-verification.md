# Lifecycle source verification

Reviewed 2026-11-09. The table records the guidance changed in this review and the evidence that applies to it.

| Rule | Applicable version or product | Primary source | Verification |
| --- | --- | --- | --- |
| Register cancellation or invalidate a captured lifetime with `ref.onDispose` before awaiting. Guard success and error before publishing. | Riverpod 2.x. Widget checks use `flutter_riverpod` and `riverpod` 2.6.1. | [Riverpod cancellation guide](https://riverpod.dev/docs/how_to/cancel) and [Riverpod 2.6.1 changelog](https://pub.dev/packages/riverpod/versions/2.6.1/changelog). | [Riverpod 2 behavior eval](../../benchmarks/unreleased/flutter-audit-fixes-riverpod-2.json) and widget checks for removing the watching screen and invalidating a provider. |
| `Ref.mounted` is available in Riverpod 3. Capture the request's ref and guard stale completions. Keep an explicit lifetime or generation guard for rebuilds on older 3.x versions. | Introduced in 3.0. The stale-ref rebuild fix is in 3.2.0. Widget checks use `flutter_riverpod` and `riverpod` 3.2.0. | [Riverpod 3 release notes](https://riverpod.dev/docs/whats_new#refmounted) and [3.2.0 changelog](https://pub.dev/packages/riverpod/changelog#320---2026-01-17). | [Riverpod 3 behavior eval](../../benchmarks/unreleased/flutter-audit-fixes-riverpod-checks.json) and widget checks for late success, late error, and old completion after invalidation. |
| Keep the established Play consumable ordering. Before requesting consumption in a consume-first flow, save the verified transaction. After an ambiguous response, reconcile the saved token and grant once after confirmed consumption. | Google Play consumable one-time purchases with a trusted backend and an existing supported consume-first or grant-first flow. | [Play purchase processing](https://developer.android.com/google/play/billing/integrate#process) and [server-side purchase and consumption status](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products/get). | [Consume-first behavior eval](../../benchmarks/unreleased/flutter-audit-fixes-play-consume-calibrated.json), [grant-first behavior eval](../../benchmarks/unreleased/flutter-audit-fixes-duplicate-updates.json), and fake-store replay for a lost consume response. |
| Deliver content or enable the service before calling `finish()`. Replaying an unfinished transaction must preserve single delivery. | Apple StoreKit 2 verified transactions. | [StoreKit Transaction.finish](https://developer.apple.com/documentation/storekit/transaction/finish%28%29). | [Store ordering behavior eval](../../benchmarks/unreleased/flutter-audit-fixes-play-consume-calibrated.json) and fake-store replay after interruption between delivery and finish. |

Run the focused checks from the repository root with Flutter 3.44.8 and Dart 3.12.2 on `PATH`.

```sh
bash .github/maintainer/verification/run-lifecycle-checks.sh
```

The run passed three Flutter widget checks on each Riverpod version and three fake-store recovery checks. The widget checks use actual Riverpod and Flutter with controlled futures. The purchase checks recreate a processor with a retained in-memory journal and fake store state. Physical devices, app process termination, durable database writes, and store sandbox calls are outside these checks. [Execution output](../../benchmarks/unreleased/flutter-audit-lifecycle-runtime.txt)
