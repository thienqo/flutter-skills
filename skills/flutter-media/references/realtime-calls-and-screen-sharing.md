# Realtime calls and screen sharing

Inspect the installed SDK's room, participant, track, device, event, and disconnect contracts. Keep a participant's identity separate from camera, microphone, and screen sources. Reconcile current SDK state using its stable identifiers; a new event does not necessarily mean a new participant or a new owned capture resource.

## Calls and reconnection

Subscribe and attach renderers once per intended track. Remove listeners/renderers when tracks or participants leave, and release only locally owned resources. Mute, unpublish, unsubscribe, stop capture, and disconnect are different operations; choose the documented operation for the user's intent.

Respect the SDK's built-in retry and track-republication behavior. For example, LiveKit documents replayed participant events and republished local tracks during a full reconnect. Do not create a second microphone/camera or append duplicate tiles on every reconnect event. Reconcile the current set idempotently; do not rely on tile indexes or a stale track instance surviving every reconnect. Keep reconnecting separate from confirmed recovered media, and stop recovery after explicit user leave or terminal denial.

For a reconnect fix, include participant departure and call disposal in the changed-path checks: detach their listeners/renderers and stop owned local capture. Show the reconnecting state until relevant remote media resumes, rather than clearing it solely on a signaling callback. Exercise repeated and reordered reconnect events as well as participant/track replay, then verify recovery with a deliberate network interruption between two endpoints when that environment is available.

## Screen sharing

Obtain the platform's capture consent. Check the resolved Flutter SDK's requirements for the running OS and deployment targets, including any required capture service, extension, entitlement, or browser gesture. Platform mechanisms change; a newer native SDK feature is not evidence that an older Flutter wrapper supports it. Add only capabilities required by the task.

Treat screen video, microphone, system audio, and camera as independently supported sources. Handle denied or canceled consent and user/system stop without silently restarting capture. Remove screen renderers/tracks and restore the intended call/camera state. Never promise system audio capture, protected-content capture, or background screen sharing on every target.

Replay repeated/reordered reconnect and participant events with fakes. Separately test two endpoints, real permissions, output routing, network changes, screen-share start/stop, and resource release on each affected target.

## Sources

- [Example reconnect and automatic republication](https://docs.livekit.io/intro/basics/connect/)
- [Example Flutter SDK setup and track API](https://docs.livekit.io/reference/client-sdk-flutter/)
- [SDK screen sharing and platform setup](https://docs.livekit.io/transport/media/screenshare/)
- [Android MediaProjection consent and lifecycle](https://developer.android.com/media/grow/media-projection)
- [Apple ReplayKit](https://developer.apple.com/documentation/replaykit)
