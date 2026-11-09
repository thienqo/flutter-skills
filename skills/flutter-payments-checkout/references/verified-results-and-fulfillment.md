# Verified results and fulfillment

Verify the gateway's notification signature before trusting the payload or changing state. Reject invalid signatures. Match verified data to the expected merchant and environment, order and attempt, and amount and currency. Resolve missing order or attempt identifiers from the backend's trusted mapping. If the event lacks a required transaction fact such as the actual amount, obtain it from the gateway's authenticated status query. Keep the outcome unconfirmed if the match cannot be established. Treat authorization, processing, capture or confirmed collection, and refunds as distinct outcomes where supported. Apply the order's fulfillment policy only after the required payment outcome is verified.

Expect notifications to repeat, arrive late, or race with a status query. Deduplicate deliveries with the provider's documented event or transaction identity. Protect the payment transition and fulfillment decision across concurrent deliveries and crashes. Use an atomic state change and durable fulfillment intent or an equivalent existing mechanism. Make the fulfillment consumer idempotent per order and fulfillment operation. If an old event conflicts with newer verified state, reconcile through the provider rather than letting arrival order regress the order. Handle refunds and other legitimate later transitions under their own policy.

Authorize access to the specific order before the backend returns payment or fulfillment status to the app. Test unauthorized order access, invalid signatures, mismatched amounts, wrong environments, duplicate or reordered delivery, and interruption between verification and fulfillment. Exercise the actual gateway sandbox and backend callback and status-query paths before claiming provider verification.

## Sources

- [Stripe webhook verification and event delivery](https://docs.stripe.com/webhooks)
- [MoMo payment notifications](https://developers.momo.vn/v3/docs/payment/api/result-handling/notification/)
- [MoMo transaction status](https://developers.momo.vn/v3/docs/payment/api/payment-api/query/)
- [VNPAY payment IPN](https://sandbox.vnpayment.vn/apis/docs/thanh-toan-pay/pay.html)
- [VNPAY transaction query](https://sandbox.vnpayment.vn/apis/docs/truy-van-hoan-tien/querydr%26refund.html)
