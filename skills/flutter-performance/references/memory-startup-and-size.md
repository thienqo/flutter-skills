# Memory, startup, and size

## Memory retention

Measure a repeated flow: establish a steady baseline, enter and leave the feature several times, force collection through the profiler when appropriate, then compare retained objects and ownership paths. Distinguish a bounded cache from unbounded growth.

Inspect lifecycle ownership of controllers, subscriptions, listeners, image caches, platform handles, and closures capturing widget state. Fix disposal or ownership at the source; do not hide retention by clearing every cache.

Treat a reported cause, such as "the images are full resolution", as a hypothesis. Before changing code, confirm it during the repeated flow: watch `imageCache.currentSizeBytes` and `liveImageCount`, or compare decoded image sizes with display sizes in the DevTools Memory view. State the measurement you will take and what result would confirm or reject the cause.

Read `ImageCache.currentSizeBytes` as cached entry size and `liveImageCount` as a separate count. Pair them with memory profiling and decoded dimensions before attributing growth. When oversized decodes are confirmed, use [platform-aware image sizing](profile-and-frame-analysis.md#common-interventions-once-attributed) to reduce the size at the source.

For oversized thumbnails, keep normal cache eviction and correct the decode size. Reject periodic whole-cache clearing as a fix because it discards reusable entries and leaves actively listened-to images live.

For web image-memory comparisons, repeat the same scroll in an isolated browser tab and sample its memory footprint at the same points before and after. Use a browser process metric such as Chrome Task Manager's Memory footprint and report it as aggregate memory. Record response dimensions and transfer bytes separately. A JS heap snapshot alone misses native allocations, and transfer size measures network cost.

## Startup

Define the user-visible milestone, such as first useful frame or first interactive content. Trace initialization on a representative device in profile or release mode. Defer only work that is not required for correctness, and preserve ordering for authentication, migrations, and dependency setup.

## App size

Compare like-for-like release artifacts for the same target, architecture splits, symbols, and build configuration. Use Flutter's size analysis to identify ownership before removing assets or dependencies. Verify runtime loading and licensing after changing fonts, icons, or deferred components.

## Sources

- [DevTools memory view](https://docs.flutter.dev/tools/devtools/memory)
- [ImageCache metrics](https://api.flutter.dev/flutter/painting/ImageCache-class.html)
- [Chrome memory diagnostics](https://developer.chrome.com/docs/devtools/memory-problems)
- [Measure app size](https://docs.flutter.dev/perf/app-size)
- [Flutter performance profiling](https://docs.flutter.dev/perf)
