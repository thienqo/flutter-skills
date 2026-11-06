# Profile and frame analysis

Use one reproducible interaction, representative data, a named device, and a profile build. Record a baseline trace before editing.

## Attribute the bottleneck

1. Locate the slow frames and compare UI-thread and raster-thread time.
2. For UI work, inspect CPU samples and timeline events around build, layout, parsing, sorting, and synchronous I/O.
3. For raster work, inspect image decode/upload, clipping, saveLayer use, shaders, and large repaints.
4. Use rebuild and repaint diagnostics to confirm scope; counts alone are not a bug.
5. Change the smallest owner of the measured work, then repeat the identical flow.

Do not prescribe `const`, list caching, isolates, repaint boundaries, or smaller images until the trace supports that intervention. Warm up both runs when shader compilation or caches would otherwise distort the comparison. Report median or a small distribution when a single run is noisy.

## Common interventions, once attributed

Apply the smallest intervention that matches the attributed cause, then repeat the same flow:

- **Unnecessary repaints**: wrap the smallest subtree that actually repaints independently in `RepaintBoundary`; a boundary placed around a large, frequently rebuilding ancestor adds compositing cost without isolating the paint. Confirm scope with the repaint rainbow or layer visualizer rather than wrapping speculatively.
- **Unnecessary rebuilds**: narrow the state subscription scope (`Selector`, `select`, a scoped `Consumer`) before adding `const` everywhere; `const` only skips rebuild for a widget whose own arguments are unchanged, not for an ancestor that still rebuilds to reach it.
- **Image decode/raster cost**: size thumbnails for the physical pixels needed by the displayed image and its fit or crop. On native targets, use one decode dimension when preserving the source aspect ratio, or use an already cropped variant. Passing both exact dimensions for a non-matching source can stretch it before `BoxFit.cover` runs. On web, `Image.network` ignores `cacheWidth` and `cacheHeight`. Request an appropriately sized variant from the image source or CDN and verify dimensions, sharpness, and cost in the browser.
- **Long or unbounded lists**: use a lazy builder (`ListView.builder`, `SliverList.builder`) instead of eagerly building every child, and add `itemExtent` or a `prototypeItem` when items share a size so the viewport can estimate layout without measuring each one.
- **Shader or first-use jank**: separate one-time shader compilation cost from steady-state cost with a warm-up pass before comparing; attributing a first-frame-only cost to ongoing code leads to the wrong fix.
- **Isolates**: move work to an isolate only after the trace shows sustained UI-thread CPU work; isolate setup and message-copy cost is real and is not a default fix for jank.

Record which rendering backend (Impeller or the legacy Skia backend) was active for every trace compared. The two backends have different cost profiles for clipping, blur, and `saveLayer`-heavy scenes, so a cross-device or before/after comparison that mixes backends can look like a regression or a win that isn't one.

## Web

Use a Flutter web profile build and the Chrome DevTools Performance panel for Flutter timeline events. Record browser, renderer, viewport, and network/CPU throttling. Use browser network or memory tools when those metrics drive the investigation.

## Sources

- [Flutter UI performance](https://docs.flutter.dev/perf/ui-performance)
- [Flutter performance metrics](https://docs.flutter.dev/perf/metrics)
- [DevTools CPU profiler](https://docs.flutter.dev/tools/devtools/cpu-profiler)
- [Flutter web performance profiling](https://docs.flutter.dev/perf/web-performance)
- [Image.network decode sizing](https://api.flutter.dev/flutter/widgets/Image/Image.network.html)
- [ResizeImage sizing policy](https://api.flutter.dev/flutter/painting/ResizeImagePolicy.html)
