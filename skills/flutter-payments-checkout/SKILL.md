---
name: flutter-payments-checkout
description: Use for Flutter checkout with external payment gateways, including payment retries, redirects, pending recovery, and reconciliation.
---

# Flutter Payments Checkout

Use for order payments for physical goods or services delivered outside the app. Route App Store and Google Play billing to `flutter-in-app-purchases`. For digital goods or mixed carts, confirm the current distribution, storefront, and product rules before proposing a payment method.

Inspect `pubspec.yaml`, SDK constraints, the installed gateway integration, the order and payment-attempt API, return paths, backend verification, and sandbox setup. Preserve the gateway, supported checkout surface, router, and state ownership. Use provider-supported collection of payment details. Keep gateway server keys and webhook verification secrets on the backend. Keep payment credentials and sensitive payloads out of logs, URLs, and local storage.

Read only the relevant references.

- [Order and payment attempts](references/order-and-payment-attempts.md) for amounts, duplicate submission, and ambiguous retries.
- [Return and recovery](references/return-and-recovery.md) for redirects, app restart, and pending status.
- [Verified results and fulfillment](references/verified-results-and-fulfillment.md) for gateway verification, event ordering, and single fulfillment.

Keep order, payment attempt, and fulfillment state distinct. Use the backend's authorized status to show an order as paid. A client callback, redirect, or network timeout must not settle an order or trigger fulfillment. Verify state and ordering with deterministic tests and name the gateway sandbox, backend, and device paths actually exercised.

Use `flutter-navigation` for link delivery and routing, `flutter-webview` for an embedded browser boundary, and `flutter-networking` for ordinary transport. This skill owns the payment meaning of the result and the backend contract needed by the app.

## Sources

- [Apple App Review Guidelines on payments](https://developer.apple.com/app-store/review/guidelines/#payments)
- [Google Play Payments policy](https://support.google.com/googleplay/android-developer/answer/9858738?hl=en)
