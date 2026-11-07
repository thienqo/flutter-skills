# Media skill scope and evidence

Owner: repository maintainers. Source review: 2026-11-07. This is maintainer evidence, not an installed workflow or a claim of device verification.

## Why a distinct owner

Three realistic requests were first assessed with existing specialist bundles:

| Request | Existing guidance tried | Gap to measure |
|---|---|---|
| Camera initialization finishes after route exit | Platform integration + Dart concurrency | Capture permissions, resolved SDK setup, exclusive hardware cleanup, and target-specific evidence |
| User pauses a podcast during a phone-call interruption | Platform integration + background execution | Audio-session ownership and current user intent versus OS resumption hints |
| A call reconnect duplicates tiles and microphone tracks | Networking + Dart concurrency | SDK track republication, participant/source reconciliation, renderer cleanup, and two-peer media evidence |

These tasks use existing application SDKs, not custom native bridges or ordinary text/data transport. A media owner gives them one discoverable entrypoint; native implementation, OS continuation, transport, identity, and device operation retain their existing owners. The retained existing-specialist runs include exact injected bundles, prompts, rubrics, and hashes. They are response-only comparison conditions, not no-skill or device baselines. See the public benchmark notes for the retained results and calibration history.

The [final comparison](../../benchmarks/unreleased/flutter-media-existing-specialists-final.json) explicitly uses original specialist entrypoints from commit `d545e4a` and the final media rubrics. The [two-case exploratory calibration](../../benchmarks/unreleased/flutter-media-existing-specialists-calibrated.json) is retained separately. An earlier three-case exploratory artifact was accidentally overwritten by that calibration; its scores are excluded from published comparisons rather than reconstructed as raw evidence.

## Source-to-case map

Resolve the consuming app's actual versions before applying any package-specific guidance. Reviewed publisher pages included camera 0.12.2, image_picker 1.2.4, video_player 2.14.1, record 7.1.2, and audio_session 0.2.4. These are review identities, not recommended upgrades or minimum-version requirements.

| Reference | Primary contracts reviewed | Behavioral cases |
|---|---|---|
| Capture and recording | [camera](https://pub.dev/packages/camera), [image_picker](https://pub.dev/packages/image_picker), [record](https://pub.dev/packages/record) | camera lifecycle; picker recovery/output validation |
| Playback and streaming | [video_player](https://pub.dev/packages/video_player), [HLS](https://developer.apple.com/streaming/), [low-latency HLS](https://developer.apple.com/documentation/http-live-streaming/enabling-low-latency-http-live-streaming-hls), [autoplay](https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Autoplay) | source switching; HLS viewer scope; output validation |
| Audio interruptions and routing | [Apple interruptions](https://developer.apple.com/documentation/avfaudio/handling-audio-interruptions), [Android focus](https://developer.android.com/media/optimize/audio-focus), [audio_session](https://pub.dev/packages/audio_session) | explicit pause during interruption; versioned screen-share/audio support |
| Live broadcasting | [SDK connections](https://docs.livekit.io/intro/basics/connect/), [grants](https://docs.livekit.io/frontends/reference/tokens-grants/), [HLS](https://developer.apple.com/streaming/) | host/viewer service authority; connection versus received media; viewer-only HLS |
| Calls and screen sharing | [Flutter SDK](https://docs.livekit.io/reference/client-sdk-flutter/), [screen sharing](https://docs.livekit.io/transport/media/screenshare/), [MediaProjection](https://developer.android.com/media/grow/media-projection), [ReplayKit](https://developer.apple.com/documentation/replaykit) | reconnect replay; capture consent/platform setup |
| Verification | [Flutter test surfaces](https://docs.flutter.dev/testing/overview), [integration boundaries](https://docs.flutter.dev/testing/integration-tests) | fake versus native/device/two-endpoint evidence across the cases |

LiveKit is one concrete publisher contract used to verify examples, not a preferred provider. Check the installed SDK's own contracts; newer native APIs and older Flutter wrappers can have different supported capture or interruption mechanisms.

## Acceptance boundaries

- Catalog routing includes five positive media requests and three negative controls, with a Vietnamese host/viewer request. These are model-selection tests using the repository's policy-assisted routing prompt.
- The optional native discovery smoke installs six neighboring skills into a disposable project and invokes Codex with a natural-language request naming no skill. Inspect retained command events for an actual instruction read; installation success or a final self-report alone does not prove implicit activation.
- The executable fake-player fixture verifies six ownership scenarios: reversed completion, stop while opening, disposal, replacement/concurrent stop, failed replacement, and failed cleanup. Its backend deliberately supports overlapping opens and returns distinct handles. This is not a camera-exclusive acquisition recipe.
- CI checks the corrected oracle and seeded stale-selection, stale-handle leak, stop revival, replacement leak, concurrent stop, and failed-close ownership defects. No external model is invoked by that CI proof.
- Native camera/microphone permissions, actual file recording/decoding, audio hardware routing, protected-content restrictions, and two-endpoint service delivery remain runtime verification boundaries. No fake test upgrades those claims.

Run the artifact proof with `python3 .github/scripts/verify_media_fixture.py`. Run local installation discovery with `python3 .github/scripts/check_media_discovery.py --output /tmp/media-install.json`; add `--execute` only for an intentional bounded Codex invocation. Keep raw outcomes and calibration changes in the public benchmark notes.
