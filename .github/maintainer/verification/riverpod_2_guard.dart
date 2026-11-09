part of 'riverpod_owner_test.dart';

bool Function() captureLifetime(Ref ref) {
  var current = true;
  ref.onDispose(() => current = false);
  return () => current;
}
