#!/usr/bin/env python3
"""
Patch PySide6's QtAsyncio event loop to support add_reader / remove_reader /
add_writer / remove_writer using QSocketNotifier.

These four methods are part of the asyncio event-loop API for watching file
descriptors, but PySide6's QAsyncioEventLoop ships them as NotImplementedError
stubs.  Libraries that rely on low-level fd watching (e.g. curl_cffi) will
fail without this patch.

Usage
-----
    python patch_qtasyncio.py                  # auto-detect .venv in cwd
    python patch_qtasyncio.py /path/to/.venv   # explicit venv path

The script is idempotent - running it twice is safe.

Platform support
----------------
Works on Linux, macOS, and Windows.  QSocketNotifier supports network sockets
on all three platforms, which is what consumer libraries (curl_cffi, etc.) use.
"""

from __future__ import annotations

import argparse
import glob
import os
import shutil
import sys

# ---------------------------------------------------------------------------
# 1.  Locate the file to patch
# ---------------------------------------------------------------------------

RELATIVE_PATH = os.path.join("PySide6", "QtAsyncio", "events.py")


def find_events_py(venv_dir: str) -> str | None:
    """Return the absolute path to PySide6/QtAsyncio/events.py inside *venv_dir*."""
    patterns = [
        # Unix: .venv/lib/python3.*/site-packages/...
        os.path.join(venv_dir, "lib", "python3.*", "site-packages", RELATIVE_PATH),
        # Windows: .venv/Lib/site-packages/...
        os.path.join(venv_dir, "Lib", "site-packages", RELATIVE_PATH),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    return None


# ---------------------------------------------------------------------------
# 2.  Define the individual patches (old text -> new text)
# ---------------------------------------------------------------------------

# Each entry is (description, old_text, new_text).
# The old_text must appear *exactly once* in the unpatched file.
# If old_text is not found the patch is assumed to be already applied.

PATCH_IMPORT = (
    "Add QSocketNotifier to QtCore imports",

    "from PySide6.QtCore import (QCoreApplication, QDateTime, QDeadlineTimer,\n"
    "                            QEventLoop, QObject, QTimer, QThread, Slot)",

    "from PySide6.QtCore import (QCoreApplication, QDateTime, QDeadlineTimer,\n"
    "                            QEventLoop, QObject, QSocketNotifier, QTimer,\n"
    "                            QThread, Slot)",
)

PATCH_INIT = (
    "Add _readers/_writers state to __init__",

    '        self._debug = bool(os.getenv("PYTHONASYNCIODEBUG", False))\n'
    "\n"
    "        self._application.aboutToQuit.connect(self._about_to_quit_cb)",

    '        self._debug = bool(os.getenv("PYTHONASYNCIODEBUG", False))\n'
    "\n"
    "        # Dictionaries mapping file descriptors to (QSocketNotifier, handle)\n"
    "        # tuples, used by add_reader/remove_reader/add_writer/remove_writer.\n"
    "        self._readers: dict[int, tuple[QSocketNotifier, asyncio.Handle]] = {}\n"
    "        self._writers: dict[int, tuple[QSocketNotifier, asyncio.Handle]] = {}\n"
    "\n"
    "        self._application.aboutToQuit.connect(self._about_to_quit_cb)",
)

PATCH_CLOSE = (
    "Clean up fd watchers in close()",

    "        if self.is_closed():\n"
    "            return\n"
    "        if self._default_executor is not None:",

    "        if self.is_closed():\n"
    "            return\n"
    "\n"
    "        # Clean up all registered fd watchers.\n"
    "        for fd in list(self._readers):\n"
    "            self.remove_reader(fd)\n"
    "        for fd in list(self._writers):\n"
    "            self.remove_writer(fd)\n"
    "\n"
    "        if self._default_executor is not None:",
)

_METHODS_NEW = '''\
    # Watching file descriptors

    @staticmethod
    def _fileobj_to_fd(fileobj) -> int:
        """Return a file descriptor from a file object.

        Parameters:
        fileobj -- either an int (already a fd) or an object with a fileno()
                   method (which returns an int fd). An invalid descriptor
                   raises ValueError.
        """
        if isinstance(fileobj, int):
            fd = fileobj
        else:
            try:
                fd = int(fileobj.fileno())
            except (AttributeError, TypeError, ValueError):
                raise ValueError(
                    f"Invalid file object: {fileobj!r}") from None
        if fd < 0:
            raise ValueError(f"Invalid file descriptor: {fd}")
        return fd

    def add_reader(self, fd, callback, *args):
        """Add a reader callback.  Return a Handle instance."""
        if self.is_closed():
            raise RuntimeError("Event loop is closed")
        fileno = self._fileobj_to_fd(fd)

        # If a reader already exists for this fd, remove it first.
        self.remove_reader(fileno)

        handle = asyncio.Handle(callback, args, self)
        notifier = QSocketNotifier(fileno, QSocketNotifier.Type.Read)
        notifier.activated.connect(lambda: self._reader_cb(fileno))
        self._readers[fileno] = (notifier, handle)
        return handle

    def _reader_cb(self, fd: int) -> None:
        """Internal callback invoked by QSocketNotifier when fd is readable."""
        entry = self._readers.get(fd)
        if entry is None:
            return
        _notifier, handle = entry
        if not handle.cancelled():
            handle._run()

    def remove_reader(self, fd) -> bool:
        """Remove a reader callback.  Return True if a reader was removed."""
        if self.is_closed():
            return False
        fileno = self._fileobj_to_fd(fd)
        entry = self._readers.pop(fileno, None)
        if entry is None:
            return False
        notifier, handle = entry
        notifier.setEnabled(False)
        # Prevent the QSocketNotifier preventing the fd from being closed by
        # its owner, by disconnecting all slots and scheduling deletion.
        notifier.activated.disconnect()
        notifier.deleteLater()
        handle.cancel()
        return True

    def add_writer(self, fd, callback, *args):
        """Add a writer callback.  Return a Handle instance."""
        if self.is_closed():
            raise RuntimeError("Event loop is closed")
        fileno = self._fileobj_to_fd(fd)

        # If a writer already exists for this fd, remove it first.
        self.remove_writer(fileno)

        handle = asyncio.Handle(callback, args, self)
        notifier = QSocketNotifier(fileno, QSocketNotifier.Type.Write)
        notifier.activated.connect(lambda: self._writer_cb(fileno))
        self._writers[fileno] = (notifier, handle)
        return handle

    def _writer_cb(self, fd: int) -> None:
        """Internal callback invoked by QSocketNotifier when fd is writable."""
        entry = self._writers.get(fd)
        if entry is None:
            return
        _notifier, handle = entry
        if not handle.cancelled():
            handle._run()

    def remove_writer(self, fd) -> bool:
        """Remove a writer callback.  Return True if a writer was removed."""
        if self.is_closed():
            return False
        fileno = self._fileobj_to_fd(fd)
        entry = self._writers.pop(fileno, None)
        if entry is None:
            return False
        notifier, handle = entry
        notifier.setEnabled(False)
        notifier.activated.disconnect()
        notifier.deleteLater()
        handle.cancel()
        return True'''

PATCH_METHODS = (
    "Implement add_reader/remove_reader/add_writer/remove_writer",

    "    # Watching file descriptors\n"
    "\n"
    "    def add_reader(self, fd, callback, *args):\n"
    '        raise NotImplementedError("QAsyncioEventLoop.add_reader() is not implemented yet")\n'
    "\n"
    "    def remove_reader(self, fd):\n"
    '        raise NotImplementedError("QAsyncioEventLoop.remove_reader() is not implemented yet")\n'
    "\n"
    "    def add_writer(self, fd, callback, *args):\n"
    '        raise NotImplementedError("QAsyncioEventLoop.add_writer() is not implemented yet")\n'
    "\n"
    "    def remove_writer(self, fd):\n"
    '        raise NotImplementedError("QAsyncioEventLoop.remove_writer() is not implemented yet")',

    _METHODS_NEW,
)

PATCHES = [PATCH_IMPORT, PATCH_INIT, PATCH_CLOSE, PATCH_METHODS]


# ---------------------------------------------------------------------------
# 3.  Apply patches
# ---------------------------------------------------------------------------

def is_already_patched(source: str) -> bool:
    """Quick check: if QSocketNotifier is already imported, we're done."""
    return "QSocketNotifier" in source and "_readers" in source


def apply_patches(filepath: str, *, dry_run: bool = False) -> bool:
    """
    Apply all patches to *filepath*.

    Returns True if the file was modified (or would be, in dry-run mode).
    """
    with open(filepath, "r", encoding="utf-8") as fh:
        original = fh.read()

    if is_already_patched(original):
        print(f"  Already patched: {filepath}")
        return False

    modified = original
    applied = 0

    for description, old_text, new_text in PATCHES:
        if old_text not in modified:
            print(f"  Skipped (text not found, maybe already applied): {description}")
            continue
        count = modified.count(old_text)
        if count != 1:
            print(f"  ERROR: Expected 1 occurrence but found {count}: {description}")
            print("    The installed PySide6 version may be incompatible with this patch.")
            sys.exit(1)
        modified = modified.replace(old_text, new_text, 1)
        applied += 1
        print(f"  Applied: {description}")

    if applied == 0:
        print("  Nothing to do.")
        return False

    if dry_run:
        print(f"\n  Dry run: {applied} patch(es) would be applied.")
        return True

    # Back up the original file.
    backup_path = filepath + ".bak"
    shutil.copy2(filepath, backup_path)
    print(f"  Backup saved to: {backup_path}")

    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(modified)

    print(f"  Patched file written ({applied} change(s)).")
    return True


# ---------------------------------------------------------------------------
# 4.  CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Patch PySide6 QtAsyncio to support add_reader/add_writer "
                    "(required by curl_cffi and similar libraries).",
    )
    parser.add_argument(
        "venv",
        nargs="?",
        default=".venv",
        help="Path to the virtual-environment directory (default: .venv)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without modifying any files.",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore the original events.py from the .bak backup.",
    )
    args = parser.parse_args()

    venv_dir = os.path.abspath(args.venv)
    if not os.path.isdir(venv_dir):
        print(f"Error: venv directory not found: {venv_dir}", file=sys.stderr)
        sys.exit(1)

    target = find_events_py(venv_dir)
    if target is None:
        print(
            f"Error: Could not find PySide6/QtAsyncio/events.py inside {venv_dir}\n"
            f"       Is PySide6 installed in this virtual environment?",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Target: {target}\n")

    if args.restore:
        backup = target + ".bak"
        if not os.path.exists(backup):
            print("Error: No backup file found. Cannot restore.", file=sys.stderr)
            sys.exit(1)
        shutil.copy2(backup, target)
        print("  Restored original file from backup.")
        return

    apply_patches(target, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
