# Audio interruptions and routing

Inspect which installed player/recorder/call SDK already owns audio-session activation, focus, ducking, and routing. Avoid a second independent handler that fights the SDK or changes the whole application's audio policy. Coordinate multiple media plugins through the existing owner.

Track explicit user playback intent separately from playing/interrupted state. After an interruption, resume only when current user intent, platform recommendation/permission, and successful activation allow it. A user Pause during a call remains a pause after the call. Permanent loss, app stop, and denied activation must not turn into unconditional auto-resume.

Handle route changes such as unplugged headphones, Bluetooth loss, or a selected device disappearing according to the product's privacy and playback expectations. Distinguish microphone input selection from speaker output and screen/system audio; support varies by SDK/backend. Do not unexpectedly start private audio on a loudspeaker or restart recording to recover an output route.

Use APIs available to the resolved Flutter plugin, native SDK, deployment target, and running OS. Apple audio interruption/lifecycle APIs evolve; a new native notification is not automatically exposed by an older Flutter package. Android focus and background eligibility likewise depend on target SDK and service state. Read the appropriate current contract rather than applying one OS version's recipe universally. Pair with background execution for required media continuation; enabling unrelated background modes does not establish support.

Use deterministic event sequences for user pause versus transient loss, permanent loss, repeated interruptions, failed activation, and route changes. Verify actual native behavior separately on affected targets and relevant audio hardware.

## Sources

- [Apple audio interruptions and lifecycle](https://developer.apple.com/documentation/avfaudio/handling-audio-interruptions)
- [Android audio focus and eligibility](https://developer.android.com/media/optimize/audio-focus)
- [An example Flutter audio-session integration contract](https://pub.dev/packages/audio_session)
