# QR and barcode scanning

Inspect the resolved scanner plugin, platform backends, required symbologies, camera permissions, and lifecycle contract. Preserve the installed scanner when it meets the feature's needs. Check whether image import, scan region, torch, or offline decoding is supported on the target when required. For app-owned frame analysis, limit formats to the feature's needs and bound queued frames. Let a plugin that already manages frame delivery keep that responsibility.

## Accept one result at the right time

- Treat detection, validation, and the resulting domain action as separate steps. A detector can emit the same value across frames or return multiple candidates together. Choose the candidate using the product's policy, such as the code in the scan region or an explicit selection.
- For single-result flows, reserve the current scan attempt before awaiting validation, lookup, or navigation. Ignore overlapping detections while it is reserved. On success, consume the attempt once. On recoverable rejection, rearm according to the product's retry policy without creating a loop while the same bad code stays in view. For batch flows, scope repeat suppression to the operation so a later intentional scan can count. A scanner's detection throttle does not replace an app-level action guard.

## Validate decoded and typed input

Check the expected symbology and payload shape for camera input. Treat decoded text and bytes as untrusted. Validate length, syntax, and domain constraints before lookup or navigation. For link-based codes, parse the URI and check the scheme, host, port, and route against the accepted contract. Never automatically execute arbitrary URLs or commands. Resolve account permissions, ticket validity, or payment status with the owning backend. Keep raw tokens and sensitive payloads out of logs.

When the product supports manual entry, keep it available for denied permission or unreadable codes. Apply the same domain validation and action guard to both sources, with camera-only format checks at the scanner boundary. Route accepted in-app destinations through the existing navigation owner.

## Own camera lifecycle and verification

Give the active scanner session one owner for the camera controller and event subscription. Follow the resolved plugin's start, stop, and disposal contract. Pause scanning when the owning route becomes inactive, even if it stays mounted, and stop or release resources when that scope ends. Invalidate late detections and asynchronous results from the old scope. Resume only while the scan flow is active, permission is available, and its next attempt is armed. Avoid a second lifecycle handler that competes with the plugin.

Use controlled detection and lookup events to test that one valid, authorized scan opens the intended destination once. Where manual entry is supported, test an authorized submission with the camera unavailable and assert that malformed input never reaches lookup. Also cover repeated frames, invalid or multiple codes, backend rejection, and late results after covering or leaving the route. On the affected device, verify camera permission grant and denial separately from successful decoding with representative symbologies and lighting. Test rotation, focus, or offline model readiness when claimed.

## Sources

- [Example Flutter scanner lifecycle and platform support](https://pub.dev/packages/mobile_scanner)
- [ML Kit barcode scanning and frame handling](https://developers.google.com/ml-kit/vision/barcode-scanning/android)
- [Apple decoded barcode value](https://developer.apple.com/documentation/avfoundation/avmetadatamachinereadablecodeobject/stringvalue)
- [Android deep-link validation](https://developer.android.com/privacy-and-security/risks/unsafe-use-of-deeplinks)
