# Map interaction and lifecycle

Keep separate state for the device fix, displayed viewport, selected point or result, and camera intent. Define when the screen starts following a device fix, when a user drag leaves follow mode, and which explicit action can reenter it. A GPS update can refresh the position indicator while the camera remains where the user left it. Distinguish user gestures from programmatic movement using the resolved SDK's contract rather than assuming every callback identifies its cause.

Give markers stable domain identities. Derive markers and list results from the same accepted result set, then reconcile selection when an item disappears. Decide how to handle a camera command before readiness, an empty bounds fit, or a controller being replaced. Give browse, marker selection, and manual pin picking useful paths even if location access is unavailable.

Invalidate work owned by the map on exit and work owned by the controller binding on replacement. Cancel subscriptions owned by the retiring scope and detach or dispose the controller according to the installed SDK. Accept each success or error only for its active owner and latest request. A still-current fix owned by the active screen can update screen state after controller replacement. Any camera command from that fix must use the current controller and respect current camera intent. Keep independent tracking under its own lifecycle. A mounted check alone cannot detect an older viewport response. For tabs that stay mounted, tie tracking to the intended active scope.

Test the first-fix policy, manual pan followed by an update, explicit recenter, list-marker selection, and late completion after route or controller replacement. On the target, verify map initialization, gestures, marker hit behavior and layout. Check provider configuration without logging credentials. For a required client key, use the provider's application/API restrictions. Keep server-only credentials in the service boundary.

## Sources

- [Example Flutter marker integration](https://developers.google.com/maps/flutter-package/samples/marker)
- [Example map SDK configuration](https://developers.google.com/maps/flutter-package/config)
- [Google Maps Platform credential restrictions](https://developers.google.com/maps/api-security-best-practices)
- [Flutter State disposal and subscription ownership](https://api.flutter.dev/flutter/widgets/State/dispose.html)
