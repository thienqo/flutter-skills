# Live broadcasting

Identify the existing service and the required topology: a host publishing to a room, interactive guests, or a broadcast ingest distributed to viewers. Separate ingest credentials, viewer playback URLs, realtime participants, and recorded output. Preserve the existing provider; do not assume one protocol, CDN, or room model fits every broadcast.

## Authority and live state

Keep provider server secrets and administrative operations in the authorized backend. Obtain participant/stream credentials through the established service, with identity, room, role, scope, and lifetime appropriate to that provider. Enforce viewer publish denial at the media service; hiding a button is not an authorization boundary. Coordinate role changes, reconnects, token renewal, and account changes without granting a new publish capability locally.

Distinguish permission acquisition, local preview, connecting, ready-to-publish, actually live, reconnecting, ended, and failed. Do not publish a preview before the user chooses to go live. Define retry/idempotency, mute and camera-switch semantics, and what viewers see when a host temporarily disappears.

Leaving as one participant and ending the broadcast for everyone are different operations. Execute the service-wide operation only when authorized, and reconcile the resulting state rather than assuming a local disconnect ended the broadcast. Release owned capture, tracks, subscriptions, renderers, and listeners on exit; do not automatically re-enter after user stop.

## Delivery evidence

Check signaling connection, local capture, publication/ingest, remote subscription/delivery, and actual remote decoding/rendering or audible audio separately. A connected room or local preview proves neither viewer delivery nor broadcast quality. Validate reconnect with the installed SDK's republish behavior rather than layering another independent retry loop.

Use separate host/viewer identities to verify publish permissions, going live, late join, mute, role transitions, network interruption, leaving, and authorized ending. Measure latency/quality under named conditions; never infer them from a protocol label. Local mocks remain local evidence when the service or second endpoint is unavailable.

## Sources

- [HLS live/on-demand delivery](https://developer.apple.com/streaming/)
- [Example Flutter realtime SDK](https://docs.livekit.io/reference/client-sdk-flutter/)
- [Example connection/reconnection contract](https://docs.livekit.io/intro/basics/connect/)
- [Example backend-issued token grants](https://docs.livekit.io/frontends/reference/tokens-grants/)
