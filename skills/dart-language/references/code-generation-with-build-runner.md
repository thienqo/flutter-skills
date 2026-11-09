# Code Generation with build_runner

Use this reference when a class in scope is annotated for `build_runner`-driven generation (`freezed`, `json_serializable`, `json_annotation`, or a similar generator), or when generated code is stale, conflicting, or failing to build.

## Regenerate through the project's own command

- Never hand-edit a generated file (`*.g.dart`, `*.freezed.dart`, `*.gr.dart`, or any file whose header marks it as generated). Edit the annotated source class, then regenerate.
- Use the project's documented generation command, typically `dart run build_runner build`, and check the resolved version before recommending flags. In `build_runner` 2.15.0, `--delete-conflicting-outputs` is accepted for compatibility and ignored. For older versions, follow the installed version's documented conflict behavior and confirm which files are generated before removing any outputs.
- Prefer a single `build` for a one-off change. Use `watch` only when the project's own workflow expects a long-running watcher, and do not leave a watcher running silently across unrelated work.
- A generated file that is missing or stale immediately after editing an annotated class is expected until the next build, not evidence of a broken generator.

## freezed classes

- Treat the generated union/`copyWith` surface as part of the public contract: adding or renaming a constructor case, a field, or a `@Default` changes call sites and generated equality/`copyWith` behavior together.
- Match the project's existing `@freezed`/`@Freezed` conventions (sealed unions vs. a single data class, `mixin _$ClassName`, `part 'x.freezed.dart';`) instead of introducing a different generator convention.
- `copyWith` on one union member only copies that member's own fields; calling it does not switch which constructor case is active.

## json_serializable

- Match an existing field's `@JsonKey` conventions (name mapping, nullability, `defaultValue`, custom `fromJson`/`toJson` converters) instead of hand-writing ad hoc parsing beside generated code.
- Distinguish a field that is nullable because the wire contract can omit it from one that is merely given a generator default; a silent default can mask the actual wire contract that `flutter-openapi-client` or `flutter-networking` evidence captured.
- Do not duplicate the generated `fromJson`/`toJson` logic by hand elsewhere "to be safe." One generated boundary should own serialization for a given type.

## Conflicts and failures

- A `part of`/`part` mismatch, two generators targeting the same output, or a missing `build.yaml` entry usually surfaces as a build_runner failure that names the file and generator; read that message before changing annotations speculatively.
- A code-generator or build_runner version bump belongs to `flutter-dependency-upgrades` ("Regenerate only through project-owned commands, inspect API and generated diffs..."); this reference covers writing and regenerating against an already-pinned generator version.
- A successful `build_runner build` proves the generator ran, not that the generated code is behaviorally correct. Still run analysis and the narrowest relevant tests against the regenerated output.

## Sources

- [build_runner 2.15.0 command-line options](https://github.com/dart-lang/build/blob/build_runner-v2.15.0/build_runner/lib/src/build_runner_command_line.dart#L166-L178)
- [build_runner 2.15.0 handling of removed options](https://github.com/dart-lang/build/blob/build_runner-v2.15.0/build_runner/lib/src/build_runner.dart#L114-L121)
