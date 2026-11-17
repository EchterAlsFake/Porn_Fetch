"""Streaming SHA-256 checks and metadata fingerprints for local media files."""
from __future__ import annotations

import hashlib
import os
import stat
import time
from pathlib import Path


def stat_fingerprint(info):
    if not stat.S_ISREG(info.st_mode):
        raise OSError("The saved destination is not a regular file")
    # Strings retain nanosecond timestamps/file IDs through PocketBase's JSON
    # transport, where large JSON numbers can otherwise lose precision.
    result = {"size": str(info.st_size), "mtime_ns": str(info.st_mtime_ns),
              "device": str(info.st_dev), "inode": str(info.st_ino)}
    if os.name != "nt":
        result["ctime_ns"] = str(info.st_ctime_ns)
    return result


def file_fingerprint(path):
    return stat_fingerprint(Path(path).stat())


def file_digest(path, stop=None, *, pause=None, bytes_per_second=0):
    path = Path(path)
    digest = hashlib.sha256()
    with path.open("rb") as source:
        before = stat_fingerprint(os.fstat(source.fileno()))
        while True:
            if stop is not None and stop.is_set():
                raise InterruptedError("Integrity check stopped")
            if pause is not None and pause.is_set():
                time.sleep(.05)
                continue
            started = time.monotonic()
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            if bytes_per_second:
                until = started + len(chunk) / bytes_per_second
                while time.monotonic() < until:
                    if stop is not None and stop.is_set():
                        raise InterruptedError("Integrity check stopped")
                    time.sleep(min(.05, max(0, until - time.monotonic())))
        after = file_fingerprint(path)
    if before != after:
        raise InterruptedError("The file changed during the integrity check")
    return digest.hexdigest(), after


def file_sha256(path, stop=None):
    return file_digest(path, stop)[0]
