# Navigation and content policy

## Define the trust model

Inventory the initial content, every expected redirect, subresource or iframe dependency, popup, external application handoff, downloadable content, and custom scheme. Separate first-party content, trusted provider content, and arbitrary external content. Prefer HTTPS and reject cleartext or certificate-error exceptions unless a separately reviewed platform requirement proves they are necessary.

Implement one testable policy that returns an explicit outcome such as allow in WebView, open in the system browser, hand to a known application route, or block with a recoverable user state. Match parsed URI components, not `startsWith`, substring, or suffix checks. Normalize hosts, account for ports and internationalized names, and reject user-info tricks or lookalike domains. Decide whether query and path constraints matter for privileged flows. State the path rule explicitly even when the requested prefix has none (for example, any path under the exact origin, after normalizing dot segments and encoded separators), and write the scheme, host, port, and path conditions for each outcome: in WebView, external app, and blocked.

## Navigation outcomes

- Keep arbitrary external browsing out of a privileged bridge-enabled WebView.
- Open ordinary external links in the system browser when that matches the product contract.
- Accept only enumerated non-HTTP schemes. Verify the destination before handing it to the operating system and provide a safe fallback when no handler exists.
- Treat popups and new-window requests as new navigation decisions, not automatic trusted children of the current page.
- Coordinate WebView history with Flutter back behavior deliberately. Define whether back navigates web history, exits the screen, closes a modal, or returns to an app route.
- Distinguish top-level failure from optional subresource failure where the package provides that signal. Model loading, content, recoverable error, blocked navigation, and offline states explicitly.

Do not continue past TLS or certificate errors. Do not infer a successful identity, checkout, or document-signing result from reaching a URL; confirm the outcome through the owning backend or platform protocol.

## Verification

Unit-test the pure URI policy with exact allowed origins and adversarial near-matches. Write the cases, do not only list them: near-match hosts, user-info, wrong port or scheme, malformed or unparsable URLs, and the destination of each redirect hop and popup request passed through the same policy. Do not defer redirects, popups, back, and failures to a manual checklist: keep the policy, back handler, and error mapping in plain Dart that takes the launcher and controller as parameters, and write at least one automated test for each. Feed a redirect chain through the policy hop by hop; send a popup or new-window URL through the same policy; assert the back handler for web history, no history, and after an external handoff; and assert that a main-frame error, an unparsable URL, and a failed external launch each yield a recoverable state. Leave on-device runs only for what a system WebView proves. On each supported system WebView, exercise server redirects, back/forward, external schemes, blocked popups, offline behavior, HTTP errors, TLS failure behavior, and process recreation. Record unsupported callbacks instead of assuming parity across platforms or packages.

## Sources

- [webview_flutter NavigationDelegate](https://pub.dev/documentation/webview_flutter/latest/webview_flutter/NavigationDelegate-class.html)
- [Android WebView security checklist](https://developer.android.com/privacy-and-security/security-tips#WebView)
