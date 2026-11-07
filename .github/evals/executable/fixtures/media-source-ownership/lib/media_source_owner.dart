abstract interface class MediaHandle {
  Future<void> close();
}

class MediaSourceOwner {
  MediaHandle? current;

  Future<void> start(Future<MediaHandle> Function() open) async {
    current = await open();
  }

  Future<void> stop() async {
    await current?.close();
    current = null;
  }

  Future<void> dispose() => stop();
}
