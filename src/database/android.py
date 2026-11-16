"""In-process Android PocketBase, using the same client, schema and repository.

The APK contains a source-built Go shared library in its native library folder.
No executable is downloaded or launched from writable application storage.
"""
from __future__ import annotations

import asyncio
import ctypes
import json
import os
import secrets
from pathlib import Path

from .client import PocketBaseClient
from .constants import SUPERUSER_EMAIL
from .errors import PocketBaseError
from .service import PocketBaseService

# Go shared libraries must remain loaded for the lifetime of the Python process.
_libraries: dict[str, ctypes.CDLL] = {}


def native_library() -> Path:
    directory = os.environ.get("PORNFETCH_ANDROID_NATIVE_LIB_DIR")
    if not directory:
        try:
            info = Path(os.environ["ANDROID_PRIVATE"]) / "pornfetch-platform.json"
            directory = json.loads(info.read_text(encoding="utf-8"))["nativeLibraryDir"]
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise PocketBaseError("Android did not publish its native library directory. Rebuild the APK with the platform helper.") from error
    path = Path(directory) / "libpornfetch_pocketbase.so"
    if not path.is_file():
        raise PocketBaseError("This APK does not contain PocketBase for its Android architecture. Rebuild it with scripts/build_android.py.")
    return path


class AndroidPocketBaseService(PocketBaseService):
    """One native instance for the tracker and creator library; history stays off."""

    def __init__(self, data_directory, *, library_path=None):
        super().__init__(data_directory)
        self.library_path = library_path
        self._native = None
        self._running = False

    @property
    def is_running(self):
        return self._running

    def _load(self):
        if self._native is None:
            path = str(self.library_path or native_library())
            if path in _libraries:
                self._native = _libraries[path]
                return
            library = ctypes.CDLL(path)
            library.PFStart.argtypes = [ctypes.c_char_p] * 4
            library.PFStart.restype = ctypes.c_void_p
            library.PFStop.argtypes = []
            library.PFStop.restype = ctypes.c_void_p
            library.PFFree.argtypes = [ctypes.c_void_p]
            library.PFFree.restype = None
            self._native = library  # Retain it until process exit; Go must never be dlclosed.
            _libraries[path] = library

    def _call(self, name, *arguments):
        self._load()
        pointer = getattr(self._native, name)(*arguments)
        if not pointer:
            raise PocketBaseError("PocketBase returned an empty native result")
        try:
            result = json.loads(ctypes.string_at(pointer))
        finally:
            self._native.PFFree(pointer)
        if result.get("error"):
            raise PocketBaseError(result["error"])
        return result

    async def start(self):
        if self.client is not None:
            return self.client
        await self.write_migrations()
        password = secrets.token_urlsafe(32)
        # Finish a native startup even if the caller is cancelled, so shutdown
        # never leaves an unowned Go database/server behind.
        task = asyncio.create_task(asyncio.to_thread(self._call, "PFStart", *[
            str(value).encode("utf-8") for value in
            (self.data_directory, self.migrations_directory, SUPERUSER_EMAIL, password)]))
        try:
            result = await asyncio.shield(task)
        except asyncio.CancelledError:
            await task
            self._running = True
            await self.stop()
            raise
        self._running = True
        client = PocketBaseClient(result["endpoint"])
        try:
            await client.authenticate(SUPERUSER_EMAIL, password)
        except BaseException:
            await self.stop()
            raise
        self.client = client
        return client

    async def stop(self):
        self.client = None
        if self._running:
            try:
                await asyncio.to_thread(self._call, "PFStop")
            finally:
                self._running = False
