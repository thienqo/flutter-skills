abstract interface class MediaHandle {
  Future<void> close();
}

class MediaSourceOwner {
  MediaHandle? current;
  int _generation = 0;
  bool _disposed = false;

  Future<void> start(Future<MediaHandle> Function() open) async {
    if (_disposed) return;
    final generation = ++_generation;
    final handle = await open();
    if (_disposed || generation != _generation) {
      await handle.close();
      return;
    }
    final previous = current;
    current = handle;
    await previous?.close();
  }

  Future<void> stop() async {
    _generation++;
    final handle = current;
    current = null;
    await handle?.close();
  }

  Future<void> dispose() async {
    if (_disposed) return;
    _disposed = true;
    await stop();
  }
}
