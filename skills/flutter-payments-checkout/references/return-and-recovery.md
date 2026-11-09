# Return and recovery

Use the gateway's supported return path. Treat a payment return as untrusted input and a signal to refresh. Match the allowed return route and correlate it to the authenticated account, current order, and relevant attempt through the backend contract. Keep repeated, late, or malformed returns from overwriting another checkout. A closed browser or canceled UI reports an interaction outcome. Resolve the payment status separately.

Keep enough non-secret order or attempt identity to resume after process death, or recover the active checkout from the backend for the authenticated account. Scope recovery to that account and ignore old results after an account or checkout change. When returning or reopening, fetch authorized backend status. Keep processing and unknown outcomes distinct from confirmed failure or cancellation. Use bounded refresh or an explicit retry-status action while pending. Start another payment only when the backend permits it after reconciliation.

Test a redirect before backend verification, no redirect, repeated delivery, restart while pending, and switching accounts. Verify supported browser, wallet, and deep-link return paths on the affected device when those claims are in scope.

## Sources

- [Flutter deep linking](https://docs.flutter.dev/ui/navigation/deep-linking)
- [Stripe status verification and fulfillment](https://docs.stripe.com/payments/payment-intents/verifying-status)
- [MoMo redirect and server notification](https://developers.momo.vn/v3/docs/payment/api/result-handling/notification/)
- [VNPAY Return URL and IPN](https://sandbox.vnpayment.vn/apis/docs/faqs/)
