# Feature boundaries and dependency rules

Group code by user-facing capability when it has distinct state, behavior, or data ownership. A feature may expose a small public surface while keeping widgets, state, models, and data adapters private to itself.

## Dependency rules

- UI depends on presentation state, not concrete HTTP, database, or plugin clients.
- Repositories own domain-facing data policy and coordinate services or caches.
- Services translate external protocols and platform APIs; they do not own UI state.
- Cross-feature reuse goes through a stable capability contract or shared domain concept, not another feature's internal files.
- `core` contains genuinely cross-cutting infrastructure, not code that lacks an owner.

Use an interface when multiple implementations, isolation from an external dependency, or meaningful test substitution justifies it. Avoid speculative abstractions and pass-through layers.

Keep independent repositories focused on their own data. Compose data from multiple repositories in presentation logic when it is specific to one screen. Put reusable or complex business policy in a focused use case above the repositories. For example, let checkout and reorder share one eligibility policy that consumes cart and membership data. Test the policy with both inputs and verify that unavailable inputs follow the existing product contract.

Validate with import/dependency rules where the repository already supports them, plus tests at the feature boundary. A diagram is useful only if it matches actual imports and runtime ownership.

## Dependency injection and data mapping

- Resolve dependencies through whatever mechanism the project already uses for object construction and lifetime — Riverpod providers, an existing `get_it`/`injectable` registration, or constructor injection through a composition root. Adding a second DI container (for example `get_it` on top of an app that already builds its graph through Riverpod providers) creates two places that can each construct or dispose the same dependency, and the two containers do not share lifecycle or override behavior in tests.
- A repository returns domain models, not the data source's own types. Map a Drift row, a `Dio` `Response`, a Firestore `DocumentSnapshot`, or a generated API client's DTO into the feature's domain model inside the repository, not in presentation code. A repository that forwards the raw data-source type ties every caller to that source and defeats the replacement and testing purpose the repository boundary exists for.

## Sources

- [Flutter architecture concepts](https://docs.flutter.dev/app-architecture/concepts)
- [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide)
- [Flutter dependency injection case study](https://docs.flutter.dev/app-architecture/case-study/dependency-injection)
