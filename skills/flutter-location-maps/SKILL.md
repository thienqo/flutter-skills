---
name: flutter-location-maps
description: Use for Flutter location permissions, GPS fixes, map camera and markers, nearby search, reverse geocoding, and address picking.
---

# Flutter Location and Maps

Inspect the app's SDK constraints, lockfile, location and map adapters, target platforms, permission configuration, and tests. Preserve the current map, location, search provider, and state ownership when they meet the task. Identify which parts need device location, which can use a user-selected area, and whether the app needs a one-time fix or ongoing tracking.

Read only the relevant references:

- [Location access and fixes](references/location-access-and-fixes.md) for permission, approximate accuracy, service availability, cached fixes, and tracking.
- [Map interaction and lifecycle](references/map-interaction-and-lifecycle.md) for camera intent, markers, map readiness, and cleanup.
- [Nearby search and address picking](references/nearby-search-and-address-picking.md) for spatial queries, geocoding, and results arriving out of order.

Keep device location, the visible map area, and user-selected coordinates distinct. A location update must respect the user's current camera mode and selection. Give subscriptions and requests a lifecycle owner. Invalidate stale successes and errors when the scope changes or the owner exits.

Choose deterministic tests for affected state, ordering, and fallback behavior. Verify permissions, real map rendering, provider behavior, and background delivery on the affected targets when those claims are in scope. Name the remaining device, provider, or credentials boundary if it cannot be checked.

Use `flutter-navigation` for screen routing and deep links, `flutter-networking` for general transport, and `flutter-platform-integration` for custom native bridges. Pair with `flutter-background-execution` when the requested tracking must continue outside the visible app. Route concrete device operation to `flutter-device-testing`.
