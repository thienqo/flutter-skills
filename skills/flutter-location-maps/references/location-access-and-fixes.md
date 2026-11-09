# Location access and fixes

Determine the minimum scope, precision, freshness, and update frequency the feature needs. Keep authorization, precision authorization, service availability, and fix quality separate. A grant can coexist with disabled services or a missing fix. An approximate grant can be sufficient for browsing nearby stores even when it cannot confirm an exact pickup point.

- Request access when the user chooses a location-dependent action. Handle denial, restricted or settings-only recovery, and a precision change while the app is open. On returning from settings, recheck both service availability and permission, including precision. Keep manual area or pin selection usable where the feature allows it. Avoid prompt loops and precision escalation without a task requirement.
- Model each fix with its acquisition time, source, and available accuracy. Apply feature-specific age and accuracy limits. Handle null, stale, and timed-out results explicitly. A cached fix can seed a clearly labeled rough map area when allowed, but cannot be presented as a fresh current fix. Request a bounded fresh fix only when permission, service availability, and user intent permit it.
- Scope subscriptions to the active feature or an explicitly owned tracking session. Revoke stale callback authority on stop, route or account change, or disposal. Choose update frequency and distance filters for the product and device cost.
- For tracking outside the visible app, verify the resolved plugin and native requirements for authorization, capability configuration, and permitted start/stop paths. Pair with background execution. Do not infer continuous delivery or survival after process termination from foreground success. Verify the actual requested lifecycle on the affected targets.

Use controlled permission/service transitions, a clock, and fake fixes to test degraded precision, stale data, timeout, and fallback. Verify real dialogs and returning from settings separately. Avoid recording exact user coordinates in diagnostic output.

## Sources

- [Android location permissions](https://developer.android.com/develop/sensors-and-location/location/permissions)
- [Android last known location](https://developer.android.com/develop/sensors-and-location/location/retrieve-current)
- [Apple accuracy authorization](https://developer.apple.com/documentation/corelocation/cllocationmanager/accuracyauthorization)
- [Apple background location updates](https://developer.apple.com/documentation/corelocation/handling-location-updates-in-the-background)
- [Example Flutter location adapter](https://pub.dev/packages/geolocator)
