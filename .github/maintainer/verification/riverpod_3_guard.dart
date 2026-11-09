part of 'riverpod_owner_test.dart';

bool Function() captureLifetime(Ref ref) =>
    () => ref.mounted;
