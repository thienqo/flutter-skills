# Music playback

Inspect the resolved player and media-session integration to see which layer already owns queue advancement, commands, and state. Keep that owner and derive the in-app player and system controls from its accepted state. Match its lifetime to the feature. An app-wide player survives navigation away from a screen when that is the intended behavior. Follow [audio interruptions and routing](audio-interruptions-and-routing.md) for focus, ducking, and output changes.

## Keep selection stable as the queue changes

- Track the current queue entry by stable identity. Use a distinct entry ID when the same track can appear twice. Derive the index from the current order and keep shuffle order, repeat policy, and track completion consistent with the installed player's behavior. Define what happens when the current item is removed or the queue empties.
- Resolve Next and Previous against the latest intended selection so rapid commands can advance through several entries before any source is ready. Invalidate older loads, metadata lookups, and player events when selection changes. Old successes and errors must leave the current selection, metadata, and controls intact. If overlapping source calls can mutate the same player, use the SDK's cancellation or serialize those calls to prevent an obsolete load from replacing the audible source. Release resources returned by abandoned loads as required by the adapter.

## Share one command path

Send in-app and system Play, Pause, Next, Previous, and Seek through the same playback owner where supported. Project its accepted track, title/artwork, position, supported actions, and playback state to each surface. Apply commands and interruptions to the current user intent. A Pause from the lock screen during buffering or interruption must prevent late readiness or an interruption-ended hint from starting audio. Keep loading or buffering separate from audible playback.

Use the resolved integration's media-session contract for lock-screen and headset behavior. If playback must continue with the screen locked, verify the target's required background configuration and pair with background execution when that OS boundary changes. Treat UI dismissal, locked-screen playback, cold launch, and explicit system playback resumption as separate paths.

## Restore the listening position

Save the queue context, selected entry identity, position, and user intent together. On restoration, resolve the entry against current content and authorization, reacquire sources through the existing adapter, and validate the saved position against the current seek range. Persist stable identifiers instead of signed playback URLs. Handle removed, inaccessible, or expired content with the existing fallback policy. Reopening the app can restore a paused session without playing. Treat an explicit app or system Play command as a separate request to start where supported.

Use a fake player and controllable events to test rapid skips, duplicate tracks, removal of the active entry, old results, a remote Pause during buffering, and restoration after the queue changes. Verify audible output, lock-screen commands, headset events, and claimed background or resumption behavior on the affected targets.

## Sources

- [Android Media3 playback controls](https://developer.android.com/media/media3/session/control-playback)
- [Android Media3 background playback and resumption](https://developer.android.com/media/media3/session/background-playback)
- [Apple Now Playing sessions and remote commands](https://developer.apple.com/documentation/mediaplayer/mpnowplayingsession)
- [Example Flutter audio-session handler contract](https://pub.dev/documentation/audio_service/latest/audio_service/AudioHandler-class.html)
