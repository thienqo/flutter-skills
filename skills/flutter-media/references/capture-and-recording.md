# Capture and recording

Identify the existing camera, picker, recorder, and platform implementation. Check the resolved package's feature/format matrix, permissions, and lifecycle contract. A ready camera preview does not prove microphone permission or a valid recorded file.

## Acquire and release

Separate denied, restricted, previously denied, canceled, unavailable-device, and initialization-failure outcomes. Offer the appropriate retry or settings path without repeatedly prompting or capturing without the requested user action. Ask only for permissions the operation actually needs.

For an app-owned camera preview, follow the installed plugin's lifecycle requirements. The Flutter `camera` package documents app-managed cleanup and reinitialization. Serialize close/reacquire operations when the backend requires exclusive access. Invalidate camera-switch and route-exit generations; if old initialization later succeeds, release that owned controller without displaying it. Cleanup and failed cleanup must not leave an undocumented second owner.

Stop/finalize recording through the installed recorder API before consuming output. Handle cancellation, interruption, write failure, and disposal while starting or stopping. A resumed app must not silently restart a recording.

## Picked and produced media

Use the picker's result types and temporary-file semantics, not an assumed filesystem path on every target. For `image_picker` on Android, inspect its lost-result recovery on relaunch; reconcile recovered attachments once and distinguish cancellation from an error. Copy temporary results to application-owned storage only when retention is required; preserve originals.

Validate actual codec/container, MIME, dimensions/orientation, duration, and size against the consumer's contract. Renaming an extension does not transcode. For crop, resize, compression, or frame processing, preserve required orientation and quality, bound pending frames/work, and measure expensive processing before choosing an isolate or native implementation. Pass verified output metadata to upload/storage owners without claiming it has been uploaded.

## Sources

Reviewed 2026-11-07; recheck the versions resolved by the consuming app.

- [Flutter camera lifecycle and permission behavior](https://pub.dev/packages/camera)
- [Flutter image picker recovery and temporary storage](https://pub.dev/packages/image_picker)
- [Recorder format/platform matrix](https://pub.dev/packages/record)
