#!/usr/bin/env bash
set -euo pipefail

sources="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
workspace="$(mktemp -d -t flutter-skill-lifecycle.XXXXXX)"
trap 'rm -rf -- "$workspace"' EXIT

for version in 2.6.1 3.2.0; do
  project="$workspace/riverpod-${version}"
  mkdir -p "$project/test"
  cp "$sources/riverpod_owner_test.dart" "$project/test/"
  cp "$sources/riverpod_${version%%.*}_guard.dart" "$project/test/riverpod_guard.dart"
  cat > "$project/pubspec.yaml" <<EOF
name: skill_riverpod_lifecycle_verification
publish_to: none
environment:
  sdk: '>=3.7.0 <4.0.0'
dependencies:
  flutter:
    sdk: flutter
  flutter_riverpod: $version
dev_dependencies:
  flutter_test:
    sdk: flutter
EOF
  printf '\nRunning Flutter widget tests with flutter_riverpod %s\n' "$version"
  (
    cd "$project"
    flutter pub get
    flutter test --no-pub --reporter expanded
  )
done

cp "$sources/purchase_recovery.dart" "$workspace/"
dart run "$workspace/purchase_recovery.dart"
