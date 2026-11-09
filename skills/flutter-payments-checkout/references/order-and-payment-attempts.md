# Order and payment attempts

Have the backend authorize the order for the current account and derive the payable amount and currency from the trusted order or quote. Convert to the gateway's expected units at the adapter boundary. Keep the order ID, merchant attempt ID, and provider transaction reference distinct. Bind attempts to the applicable order version and merchant environment.

Disable duplicate submission in the UI for feedback and enforce idempotency on the backend. For an ambiguous timeout, first look up or resume the existing attempt. If replaying the same operation, reuse the original operation identity and parameters under the resolved gateway contract. Persist the order-to-attempt association so another device, a concurrent request, or process restart can reconcile the same attempt. Provider idempotency scope and expiry vary. Recover uncertain outcomes before replaying outside that window or creating a replacement. A changed quote or a confirmed terminal failure follows the backend's replacement policy rather than reusing a key for a different operation.

Test concurrent creation, a lost response after successful creation, retries after restart, quote changes, and a legitimate new attempt. Assert the backend creates at most one chargeable attempt for the same operation. Disabling a button alone cannot establish that invariant.

## Sources

- [Stripe Payment Intents and interrupted checkout](https://docs.stripe.com/payments/payment-intents#best-practices)
- [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)
- [MoMo API idempotency](https://developers.momo.vn/v3/docs/payment/api/result-handling/idempotency/)
- [VNPAY payment request parameters](https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html)
