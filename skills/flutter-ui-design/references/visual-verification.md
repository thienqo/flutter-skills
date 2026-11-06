# Visual verification

Visual quality requires repeatable evidence, not a single hand-picked screenshot.

## Define fixtures

Use deterministic data and capture the same representative fixtures before and after a redesign. Include only relevant combinations from:

- Loaded with typical and long content
- Loading, empty, partial error, full error, offline, and retrying
- Light and dark themes
- Compact and wide constraints
- Default and enlarged text
- Left-to-right and right-to-left locales
- Touch, pointer, keyboard focus, selected, pressed, and disabled states

Keep the matrix small enough to maintain while covering the highest-risk visual differences.

## Choose the evidence

Use screenshot or golden tests for stable component and screen states. Use emulator or real-device captures when system chrome, fonts, safe areas, platform controls, GPU effects, keyboard behavior, or input mode matters. Behavioral widget tests remain separate evidence.

For golden tests, match the CI operating system and pinned Flutter version, explicitly load the product fonts, and fix viewport, device pixel ratio, theme, and fixture data. Inspect expected, actual, and diff images under those conditions before updating a baseline. For critical actions, separately test keyboard traversal, visible focus, and activation on the relevant input surface.

Do not approve visual output solely from source review. Render it at the intended sizes.

## Inspect systematically

- Primary task and action are immediately identifiable.
- Reading order remains clear without accent color.
- Text wraps, scales, and localizes without clipping or hiding actions.
- Foreground/background pairs maintain contrast in every theme and state. For translucent or gradient surfaces, check the rendered foreground against representative backdrops, including the lowest-contrast region behind text or controls.
- Spacing and alignment follow the token rhythm.
- Components have coherent shape, icon, elevation, and state treatment.
- Empty, loading, error, offline, disabled, and focus states feel designed rather than appended.
- Touch targets, keyboard focus, hover, and platform conventions remain usable.
- Images preserve useful crops and have loading/error fallbacks.
- No decorative effect competes with content or introduces avoidable rendering cost.
- The visual identity remains recognizable after replacing copy with gray blocks; it does not depend only on a logo or accent color.
- Framework defaults do not dominate a brief that asks for a visible transformation.
- Reference comparisons use equivalent viewport, theme, content density, and state.

## Compare and report

Describe changes in observable terms: reduced competing accents, clearer title/action hierarchy, fewer redundant surfaces, consistent typography roles, stable loading geometry, or improved state coverage.

For a visible redesign, use a render-critique-render loop:

1. Capture the baseline and first implementation with the same fixture.
2. Name the three largest remaining visual gaps.
3. Fix material gaps rather than polishing incidental pixels.
4. Capture the accepted state and retain enough evidence to reproduce the comparison.

A successful build or passing widget test proves implementation health, not visual quality. Do not mark visual work complete until a rendered artifact has been inspected.

If the result depends on subjective brand direction that the repository and brief do not establish, present a restrained default and record the open choice. Do not invent a redesign mandate or claim universal aesthetic superiority.

## Sources

- [Flutter golden test rendering and fonts](https://api.flutter.dev/flutter/flutter_test/matchesGoldenFile.html)
- [Flutter accessibility testing](https://docs.flutter.dev/ui/accessibility/accessibility-testing)
