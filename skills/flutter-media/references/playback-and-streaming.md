# Playback and streaming

Establish whether the source is an asset, application-owned file, authenticated URL, on-demand stream, or live playback URL. Check actual container/codec, captions, player backend, platform coverage, seek/live-edge behavior, and source authorization. Use the installed player's contract; do not select a new package solely for familiarity.

## Controller and source ownership

Initialize once per intended source/owner and release controllers and listeners on replacement or exit. Treat readiness, playing, user pause, buffering, ended, and failed as different states. Expose a recoverable failure rather than an endless loading indicator. Remember user intent separately from lifecycle interruptions.

During source switching, accept only a still-current initialization. Release successfully initialized stale controllers, including completions after stop/disposal. Decide whether a failed replacement preserves the previous source or shows an error; do not accidentally revive a source the user abandoned. Await cleanup where the SDK requires it, and prevent duplicate release by transferring ownership before asynchronous cleanup.

## Delivery and platform checks

An HLS viewer URL does not require building a broadcasting room or ingest pipeline. HLS and interactive realtime media solve different delivery contracts. Low latency requires compatible encoder/packager, delivery, and player behavior; a playlist extension does not establish latency. Measure source-to-viewer delay when that claim matters.

On web, inspect autoplay/user-gesture rules, codec/HLS support, CORS, authentication, and whether the backend accepts headers/cookies for every playlist and segment request. Keep signed URLs and credentials out of diagnostics. Do not assume a file-path constructor or platform option exists on every backend. Keep HTTPS; add a narrowly justified transport exception only for an explicitly required source after checking platform guidance.

Test startup, buffering, retry, expired authorization, seek/live edge where supported, captions, source replacement, and cleanup. UI status or downloaded bytes alone do not prove decoded frames or audible output.

## Sources

- [Flutter video player setup and platform behavior](https://pub.dev/packages/video_player)
- [Apple HLS delivery](https://developer.apple.com/streaming/)
- [Low-Latency HLS delivery requirements](https://developer.apple.com/documentation/http-live-streaming/enabling-low-latency-http-live-streaming-hls)
- [Browser autoplay guidance](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay)
