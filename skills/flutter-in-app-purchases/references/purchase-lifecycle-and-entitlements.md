# Purchase lifecycle and entitlements

Use this reference for transaction processing and the boundary between the store, application, backend, and delivered capability.

## Listener and reconciliation ownership

Create one clearly owned purchase-update subscription early enough to receive updates after launch and resume. Dispose it according to the package lifecycle without creating duplicate listeners. Re-query or reconcile current purchases when the store contract requires it because transactions may complete while the application is stopped, on another device, or outside the current flow.

Do not associate a transaction only with the screen or button that initiated it. Persist or recover enough non-sensitive correlation to attribute a returned transaction safely, and handle updates when no purchase screen exists.

## Processing sequence

For each transaction identity:

1. Normalize product, store, transaction identity, account context, state, and verification material.
2. Reject or defer pending, cancelled, failed, malformed, mismatched, or unverified results.
3. Verify with the established trusted store or backend boundary.
4. Persist the verified transaction and its processing progress so retries can recover from interruption. Deliver the entitlement once per verified transaction identity, using an atomic grant and delivery record or an equivalent idempotent operation.
5. Follow the store and product-specific ordering below.

Make retries safe at every step. Duplicate callbacks, backend notifications, restores, and app restarts must not deliver a consumable twice or create contradictory entitlement state.

## Account and trust boundary

A purchase token, receipt, or signed transaction is sensitive evidence, not an application secret and not an entitlement by itself. Avoid logging or exposing it unnecessarily. Bind verified purchases to the correct authenticated account using the existing backend design where cross-device access or fraud resistance requires it.

If the user changes account during a transaction, stop automatic attribution until the owning account can be determined safely. Never carry cached premium state from one account to another.

## Product types

- **Apple StoreKit**: Deliver the purchased content or enable the service before calling `finish()` on a verified transaction. Reconcile unfinished updates without delivering again.
- **Google Play non-consumables and subscriptions**: Grant verified entitlement before required acknowledgement. Acknowledge initial subscription purchases as required. Subscription renewals update access from verified effective state and access period without repeating the initial acknowledgement.
- **Google Play consumables**: Preserve the existing supported ordering. With grant-first, durably grant once per verified purchase token, then consume. With consume-first, persist the verified purchase and recovery identity before requesting consumption. Grant once after verified consumption, and recover an ambiguous or lost response through the existing trusted store contract. Reconcile from the durable record after a restart even if the consumed purchase no longer appears in the client purchase list. Keep an unconfirmed outcome pending.

Keep product identifiers and entitlement names centrally mapped and environment-aware. Missing, duplicated, or unknown products should fail visibly without inventing price or access state.

Use a fake store to test interruptions on both sides of the store operation used by the app. For Play consume-first, simulate successful consumption with a lost response, restart, reconcile the saved token, and replay callbacks. Assert the balance changes once. For StoreKit, test a crash after delivery and before `finish()`, then verify reprocessing finishes without granting again. Verify real consumption, token lookup, and transaction updates separately in the relevant store sandbox or test track.

## Sources

- [Google Play purchase processing and consumables](https://developer.android.com/google/play/billing/integrate#process)
- [Google Play one-time purchase state](https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products/get)
- [StoreKit Transaction.finish](https://developer.apple.com/documentation/storekit/transaction/finish%28%29)
