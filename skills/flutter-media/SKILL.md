---
name: flutter-media
description: Implement Flutter camera capture, QR/barcode scanning, audio/video recording and playback, music players, livestreams, calls, and screen sharing. Use for media tracks, permissions, and interruptions; route text-only realtime transport to flutter-networking and native bridges to flutter-platform-integration.
---

# Flutter Media

Deliver media behavior that respects the user's intent, the resolved player or capture SDK, and each target's lifecycle. Preserve existing packages and architecture. Installing this skill requires no provider account, server key, room, stream URL, or camera/microphone access.

## Establish the media contract

Read `pubspec.yaml`, the lockfile, SDK constraints, current adapters/controllers, native configuration, and tests. Establish:

- Capture, recorded-file playback, live viewing, broadcasting, or interactive calling; an image-buffer stream is not an encoded broadcast.
- Source and output, format/codec, target platforms, permissions, foreground/background requirements, and intended behavior on interruption or exit.
- For live sessions, service ownership, participant identity, host/viewer permissions, and what proves actual remote media delivery.

Use the current SDK's supported facilities before adding another player, audio-session owner, signaling stack, or provider. Inspect version-specific native/browser requirements instead of copying setup or API names from a newer release. Keep secrets in the authorized service boundary, not in Flutter or logs.

## Read the relevant mode

- [Capture and recording](references/capture-and-recording.md): camera, microphone, media picking, transforms, encoded outputs, and recovery.
- [QR and barcode scanning](references/qr-and-barcode-scanning.md) for camera detection, repeat suppression, payload validation, and manual entry.
- [Playback and streaming](references/playback-and-streaming.md): audio/video controllers, source switching, buffering, HLS/live viewing, and browser constraints.
- [Music playback](references/music-playback.md) for music queues, system media controls, and restoring listening progress.
- [Audio interruptions and routing](references/audio-interruptions-and-routing.md): focus, session activation, user pause intent, calls, and output-device changes.
- [Live broadcasting](references/live-broadcasting.md): preview, going live, host/viewer authority, delivery stages, and ending a broadcast.
- [Realtime calls and screen sharing](references/realtime-calls-and-screen-sharing.md): participants/tracks, reconnect, device selection, capture consent, and screen-share setup.

Read [verification](references/verification.md) before claiming capture, playback, live delivery, or target compatibility. Read several mode references only when the task crosses their boundaries.

## Keep ownership explicit

Give each controller, track, subscription, renderer, temporary file, and session one lifecycle owner. Invalidate abandoned asynchronous work; release resources returned by stale successful initialization instead of only ignoring its UI update. Handle cleanup failures explicitly and follow SDK-specific ordering for exclusive hardware acquisition. Do not reopen capture or resume audio merely because the app or connection resumes.

Model permission denial, initialization, ready/live, interruption/reconnection, terminal error, user stop, and disposal as distinct outcomes where relevant. Keep permission prompts and media effects outside widget `build`. Stop only resources this feature owns; protect user-authored and retained recordings from disposable-test cleanup.

## Close the evidence loop

For an implementation or a tool-free plan, explicitly identify the resolved package/Flutter/native contract checks and existing SDK responsibilities before adding lifecycle, focus, or recovery handlers. A package being present does not establish who already owns those effects. At the affected boundary, state the stop/leave cleanup and the focused acceptance checks, including the native or two-endpoint scenario still needed. Label unavailable inspection and execution as pending; do not substitute a list of fake tests for the media behavior they cannot prove.

## Neighbor boundaries

- Networking owns ordinary HTTP/WebSocket/SSE messages and upload transport; this skill owns audio/video capture, playback, and media sessions.
- Platform integration owns custom native bridges/plugins; background execution owns OS continuation/scheduling when required. Pair them only when that boundary changes.
- Authentication/security own identity lifecycle and wider threat audits. Media integration still respects service-enforced publish permissions and confidential credentials.
- Device testing operates concrete targets; performance owns measured jank/latency/memory diagnosis. UI design owns visual art direction.
- Document parsing/PDF editing, generic file management/sharing, and text-only chat are outside this skill. Media capture does not authorize uploading or publishing its output.
