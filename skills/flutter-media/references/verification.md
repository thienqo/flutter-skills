# Media verification

Tie important decisions to the installed SDK's documentation/API/source and actual target constraints. Record the source URL, resolved package/native version, review date, expected behavior, test, and observed result where they affect reproducibility. Current publisher documentation is a starting point; check changelogs/source for the version the app actually uses. Treat examples as examples rather than a universal package choice.

| Claim | Appropriate evidence |
|---|---|
| State, late initialization, event deduplication, owned cleanup | Deterministic fake-controlled unit tests, including reversed completion and stop/disposal while pending |
| Pending/error/retry/role UI | Widget tests with the real state owner and a controlled adapter |
| Native permission and camera/microphone/audio routing | Target runtime checks with actual platform/plugin and relevant hardware |
| Media file can be consumed | Inspect produced format/metadata and decode/play the output on the supported target |
| Livestream/call works | Distinct publishing and receiving endpoints, named service, actual received video/audio, and role restrictions |
| Latency, frame rate, memory, or quality improved | Equivalent before/after measurements, named target/build mode/network/source, and variance |

Choose checks for the changed behavior: permission denial and cancellation; initialization and failure; source/camera changes; user pause during interruption; background/foreground; stop/disposal; repeated reconnect; account/role changes; and unavailable devices. Do not expand every small playback task into every platform or mode.

For local fixtures use synthetic or explicitly authorized media. Record execution surface and data/service source independently. Mock adapter success does not prove OS permission flow, camera release, codec support, audible output, remote delivery, or live authorization. Ordinary widget interaction also does not prove native system-dialog behavior.

When runtime, hardware, credentials, a second participant, or a compatible SDK blocks a check, complete independent local checks and report that exact boundary as unverified. Do not label a call healthy from signaling alone, or a recording valid from a nonempty path. Keep credentials, signed media URLs, and private recordings out of retained diagnostics.

## Sources

- [Flutter testing surfaces](https://docs.flutter.dev/testing/overview)
- [Flutter integration-test boundaries](https://docs.flutter.dev/testing/integration-tests)
- [Example SDK connection/media diagnostics](https://docs.livekit.io/reference/client-sdk-flutter/)
