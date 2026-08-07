#!/usr/bin/env python3
"""
Safely patch PySide6 6.11 QtAsyncio for Python 3.14 and descriptor-based I/O.

The patch adds QSocketNotifier-backed implementations of:

    add_reader / remove_reader / add_writer / remove_writer

and, when required, adds QAsyncioTask._make_cancelled_error() for Python 3.14.

Unlike a blind string-replacement script, this tool:

* discovers the exact PySide6 installation through the target interpreter;
* validates the PySide6 and Python versions;
* uses Python's AST to locate the classes and methods it modifies;
* refuses to overwrite a native/non-placeholder implementation unless --force;
* writes atomically and creates hash-verified, timestamped backups;
* is idempotent and can restore the latest backup;
* compiles and imports the patched modules before reporting success.

Typical usage:

    python patch_qtasyncio.py .venv
    python patch_qtasyncio.py .venv --dry-run
    python patch_qtasyncio.py .venv --verify
    python patch_qtasyncio.py .venv --restore

This is an application-local compatibility patch, not an upstream Qt fix.
Re-run --verify after upgrading PySide6, and prefer removing the patch once
QtAsyncio provides native descriptor-watcher support.
"""

from __future__ import annotations

import argparse
import ast
import dataclasses
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Iterable, Sequence


PATCH_ID = "qtasyncio-compat-v2"
SUPPORTED_PYSIDE_MAJOR_MINOR = (6, 11)

EVENTS_IMPORT_MARKER = f"{PATCH_ID}:qsocketnotifier-import"
EVENTS_INIT_MARKER = f"{PATCH_ID}:fd-state"
EVENTS_CLOSE_MARKER = f"{PATCH_ID}:fd-close"
EVENTS_METHODS_MARKER = f"{PATCH_ID}:fd-methods"
TASKS_METHOD_MARKER = f"{PATCH_ID}:cancelled-error"


class PatchError(RuntimeError):
    """Raised when the installed source is incompatible with this patcher."""


@dataclasses.dataclass(frozen=True)
class EnvironmentInfo:
    target: Path
    python: Path
    prefix: Path
    pyside_version: str
    python_version: tuple[int, int, int]
    events_path: Path
    tasks_path: Path


@dataclasses.dataclass(frozen=True)
class SourceChange:
    path: Path
    original: str
    modified: str
    descriptions: tuple[str, ...]

    @property
    def changed(self) -> bool:
        return self.original != self.modified


@dataclasses.dataclass(frozen=True)
class LineEdit:
    """Replace source lines [start, end) with replacement."""

    start: int
    end: int
    replacement: str
    description: str


# ---------------------------------------------------------------------------
# Source inserted into PySide6.QtAsyncio.events
# ---------------------------------------------------------------------------

FD_METHODS = f'''\
    # {EVENTS_METHODS_MARKER}
    # QSocketNotifier callbacks are deliberately not run inline. Qt can emit
    # activated() re-entrantly, especially for write-ready descriptors. The
    # notifier is disabled immediately and the registered asyncio.Handle is
    # scheduled onto the loop. This preserves asyncio callback context and
    # exception handling while preventing a write-notifier busy loop.

    @staticmethod
    def _qtasyncio_fileobj_to_fd(fileobj) -> int:
        if isinstance(fileobj, int):
            fd = fileobj
        else:
            try:
                fd = int(fileobj.fileno())
            except (AttributeError, TypeError, ValueError):
                raise ValueError(f"Invalid file object: {{fileobj!r}}") from None

        if fd < 0:
            raise ValueError(f"Invalid file descriptor: {{fd}}")
        return fd

    def _qtasyncio_add_fd_watcher(
            self, fileobj, callback, args, notifier_type, watchers) -> None:
        if self.is_closed():
            raise RuntimeError("Event loop is closed")
        if not callable(callback):
            raise TypeError("callback must be callable")

        fd = self._qtasyncio_fileobj_to_fd(fileobj)
        self._qtasyncio_remove_fd_watcher(fd, watchers)

        token = object()
        handle = asyncio.Handle(callback, args, self)
        notifier = None

        try:
            notifier = QSocketNotifier(fd, notifier_type)
            notifier.setEnabled(False)
            notifier.activated.connect(
                lambda *_signal_args, _fd=fd, _token=token, _watchers=watchers:
                    self._qtasyncio_fd_activated(_fd, _token, _watchers)
            )
            watchers[fd] = (notifier, handle, token)
            notifier.setEnabled(True)
        except BaseException:
            handle.cancel()
            watchers.pop(fd, None)
            if notifier is not None:
                notifier.setEnabled(False)
                notifier.deleteLater()
            raise

    def _qtasyncio_fd_activated(self, fd: int, token: object, watchers) -> None:
        entry = watchers.get(fd)
        if entry is None or entry[2] is not token:
            return

        notifier, handle, _token = entry
        if handle.cancelled():
            self._qtasyncio_remove_fd_watcher(fd, watchers)
            return

        # Qt recommends disabling write notifiers after activation. Doing the
        # same for readers also prevents duplicate/re-entrant dispatch before
        # the asyncio callback has had a chance to consume the readiness.
        notifier.setEnabled(False)

        try:
            self.call_soon(self._qtasyncio_run_fd_handle,
                           fd, token, watchers)
        except RuntimeError:
            # The loop was closed between activation and scheduling.
            self._qtasyncio_remove_fd_watcher(fd, watchers)

    def _qtasyncio_run_fd_handle(
            self, fd: int, token: object, watchers) -> None:
        entry = watchers.get(fd)
        if entry is None or entry[2] is not token:
            return

        notifier, handle, _token = entry
        try:
            if not handle.cancelled():
                # Handle._run() is also what asyncio's own event loop uses to
                # execute a callback in its captured context and report errors
                # through call_exception_handler().
                handle._run()
        finally:
            current = watchers.get(fd)
            if (current is entry and not handle.cancelled()
                    and not self.is_closed() and notifier.isValid()):
                notifier.setEnabled(True)

    @staticmethod
    def _qtasyncio_remove_fd_watcher(fd: int, watchers) -> bool:
        entry = watchers.pop(fd, None)
        if entry is None:
            return False

        notifier, handle, _token = entry
        notifier.setEnabled(False)
        try:
            notifier.activated.disconnect()
        except (RuntimeError, TypeError):
            pass
        handle.cancel()
        notifier.deleteLater()
        return True

    def add_reader(self, fd, callback, *args):
        """Register a callback for read readiness, replacing any old one."""
        self._qtasyncio_add_fd_watcher(
            fd, callback, args, QSocketNotifier.Type.Read,
            self._qtasyncio_readers)

    def remove_reader(self, fd):
        """Remove the read callback for *fd* and return whether one existed."""
        if self.is_closed():
            return False
        fileno = self._qtasyncio_fileobj_to_fd(fd)
        return self._qtasyncio_remove_fd_watcher(
            fileno, self._qtasyncio_readers)

    def add_writer(self, fd, callback, *args):
        """Register a callback for write readiness, replacing any old one."""
        self._qtasyncio_add_fd_watcher(
            fd, callback, args, QSocketNotifier.Type.Write,
            self._qtasyncio_writers)

    def remove_writer(self, fd):
        """Remove the write callback for *fd* and return whether one existed."""
        if self.is_closed():
            return False
        fileno = self._qtasyncio_fileobj_to_fd(fd)
        return self._qtasyncio_remove_fd_watcher(
            fileno, self._qtasyncio_writers)
'''

INIT_STATE = f'''\

        # {EVENTS_INIT_MARKER}
        # fd -> (QSocketNotifier, asyncio.Handle, identity token)
        self._qtasyncio_readers = {{}}
        self._qtasyncio_writers = {{}}
'''

CLOSE_CLEANUP = f'''\

        # {EVENTS_CLOSE_MARKER}
        # Remove notifiers while the loop is still open; remove_reader() and
        # remove_writer() intentionally become no-ops after closure.
        for fd in tuple(self._qtasyncio_readers):
            self.remove_reader(fd)
        for fd in tuple(self._qtasyncio_writers):
            self.remove_writer(fd)
'''

CANCELLED_ERROR_METHOD = f'''\
    # {TASKS_METHOD_MARKER}
    def _make_cancelled_error(self):
        """Create the CancelledError used while unwinding a cancelled task.

        Mirrors asyncio.Future._make_cancelled_error() closely enough for
        Python 3.14's task/future cancellation path. A previously captured
        cancellation exception is consumed once so its traceback/context is
        not retained indefinitely.
        """
        import asyncio

        cancelled_exc = getattr(self, "_cancelled_exc", None)
        if cancelled_exc is not None:
            self._cancelled_exc = None
            return cancelled_exc

        cancel_message = getattr(self, "_cancel_message", None)
        if cancel_message is None:
            return asyncio.exceptions.CancelledError()
        return asyncio.exceptions.CancelledError(cancel_message)

'''


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_version(version: str) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", version)
    return tuple(int(value) for value in numbers[:3])


def target_python(target: Path) -> Path:
    target = target.expanduser().resolve()

    if target.is_file():
        return target

    candidates = (
        target / "bin" / "python",
        target / "bin" / "python3",
        target / "Scripts" / "python.exe",
        target / "Scripts" / "python3.exe",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise PatchError(
        f"Could not find a Python interpreter inside {target}. "
        "Pass a virtual-environment directory or its Python executable."
    )


def inspect_environment(target: Path) -> EnvironmentInfo:
    python = target_python(target)
    probe = r'''
import json
import sys
import PySide6
import PySide6.QtAsyncio.events as events
import PySide6.QtAsyncio.tasks as tasks

print(json.dumps({
    "prefix": sys.prefix,
    "python_version": list(sys.version_info[:3]),
    "pyside_version": PySide6.__version__,
    "events_path": events.__file__,
    "tasks_path": tasks.__file__,
}))
'''
    process = subprocess.run(
        [str(python), "-I", "-c", probe],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise PatchError(
            f"Could not import PySide6.QtAsyncio with {python}:\n"
            f"{process.stderr.strip()}"
        )

    try:
        data = json.loads(process.stdout.strip())
    except json.JSONDecodeError as error:
        raise PatchError(
            f"Unexpected output while probing {python}: {process.stdout!r}"
        ) from error

    return EnvironmentInfo(
        target=target.expanduser().resolve(),
        python=python,
        prefix=Path(data["prefix"]).resolve(),
        pyside_version=str(data["pyside_version"]),
        python_version=tuple(data["python_version"]),
        events_path=Path(data["events_path"]).resolve(),
        tasks_path=Path(data["tasks_path"]).resolve(),
    )


def find_class(tree: ast.Module, name: str) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise PatchError(f"Could not find class {name!r}")


def class_method(class_node: ast.ClassDef, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


def is_not_implemented_placeholder(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    body = list(node.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
        if isinstance(body[0].value.value, str):
            body = body[1:]

    if len(body) != 1 or not isinstance(body[0], ast.Raise):
        return False

    raised = body[0].exc
    if not isinstance(raised, ast.Call):
        return False
    func = raised.func
    return isinstance(func, ast.Name) and func.id == "NotImplementedError"


def apply_line_edits(source: str, edits: Sequence[LineEdit]) -> str:
    lines = source.splitlines(keepends=True)
    occupied: list[tuple[int, int, str]] = []

    for edit in sorted(edits, key=lambda item: (item.start, item.end)):
        for start, end, description in occupied:
            if edit.start < end and start < edit.end:
                raise PatchError(
                    f"Overlapping edits: {description!r} and {edit.description!r}"
                )
        occupied.append((edit.start, edit.end, edit.description))

    for edit in sorted(edits, key=lambda item: (item.start, item.end), reverse=True):
        replacement = edit.replacement
        if replacement and not replacement.endswith("\n"):
            replacement += "\n"
        lines[edit.start:edit.end] = replacement.splitlines(keepends=True)

    return "".join(lines)


def render_import_from(node: ast.ImportFrom, extra_name: str, marker: str) -> str:
    names = list(node.names)
    if not any(alias.name == extra_name for alias in names):
        names.append(ast.alias(name=extra_name))

    rendered = []
    for alias in names:
        value = alias.name
        if alias.asname:
            value += f" as {alias.asname}"
        rendered.append(value)

    rendered.sort(key=lambda value: value.lower())
    body = "\n".join(f"    {value}," for value in rendered)
    return f"# {marker}\nfrom {node.module} import (\n{body}\n)\n"


def find_qtcore_import(tree: ast.Module) -> ast.ImportFrom:
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module == "PySide6.QtCore":
            return node
    raise PatchError("Could not find the 'from PySide6.QtCore import ...' statement")


def find_close_insertion_line(close_method: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    for statement in close_method.body:
        if not isinstance(statement, ast.If):
            continue
        test = statement.test
        if not isinstance(test, ast.Call) or test.args or test.keywords:
            continue
        func = test.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "is_closed"
            and isinstance(func.value, ast.Name)
            and func.value.id == "self"
        ):
            return statement.end_lineno or statement.lineno

    # Fall back to immediately after a possible docstring.
    if close_method.body:
        first = close_method.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
            if isinstance(first.value.value, str):
                return first.end_lineno or first.lineno
    return close_method.lineno


def patch_events_source(source: str, *, force: bool) -> tuple[str, tuple[str, ...]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise PatchError(f"events.py does not parse: {error}") from error

    edits: list[LineEdit] = []
    descriptions: list[str] = []
    loop_class = find_class(tree, "QAsyncioEventLoop")

    if "QSocketNotifier" not in source:
        import_node = find_qtcore_import(tree)
        edits.append(LineEdit(
            start=import_node.lineno - 1,
            end=import_node.end_lineno or import_node.lineno,
            replacement=render_import_from(
                import_node, "QSocketNotifier", EVENTS_IMPORT_MARKER
            ),
            description="add QSocketNotifier import",
        ))
        descriptions.append("added QSocketNotifier import")

    if EVENTS_INIT_MARKER not in source:
        init_method = class_method(loop_class, "__init__")
        if init_method is None or not init_method.body:
            raise PatchError("Could not find QAsyncioEventLoop.__init__()")
        insertion_line = init_method.body[-1].end_lineno or init_method.body[-1].lineno
        edits.append(LineEdit(
            start=insertion_line,
            end=insertion_line,
            replacement=INIT_STATE,
            description="initialize descriptor watcher state",
        ))
        descriptions.append("initialized reader/writer watcher state")

    if EVENTS_CLOSE_MARKER not in source:
        close_method = class_method(loop_class, "close")
        if close_method is None:
            raise PatchError("Could not find QAsyncioEventLoop.close()")
        insertion_line = find_close_insertion_line(close_method)
        edits.append(LineEdit(
            start=insertion_line,
            end=insertion_line,
            replacement=CLOSE_CLEANUP,
            description="clean up descriptor watchers during close",
        ))
        descriptions.append("added descriptor watcher cleanup to close()")

    if EVENTS_METHODS_MARKER not in source:
        names = ("add_reader", "remove_reader", "add_writer", "remove_writer")
        methods = [class_method(loop_class, name) for name in names]
        if any(method is None for method in methods):
            missing = [name for name, method in zip(names, methods) if method is None]
            raise PatchError(f"Missing event-loop methods: {', '.join(missing)}")

        concrete_methods = [method for method in methods if method is not None]
        placeholders = [is_not_implemented_placeholder(method) for method in concrete_methods]
        legacy_patch = (
            "self._readers" in source
            and "self._writers" in source
            and "QSocketNotifier.Type.Read" in source
            and "QSocketNotifier.Type.Write" in source
            and "handle._run()" in source
        )
        if not all(placeholders) and not legacy_patch and not force:
            raise PatchError(
                "QtAsyncio already contains a non-placeholder descriptor watcher "
                "implementation. Refusing to overwrite it. Upgrade/remove this patch "
                "or rerun with --force after reviewing the installed source."
            )

        body_indexes = [loop_class.body.index(method) for method in concrete_methods]
        block = loop_class.body[min(body_indexes):max(body_indexes) + 1]
        allowed_names = set(names)
        if legacy_patch:
            allowed_names.update({"_reader_cb", "_writer_cb"})
        unrelated = [
            node.name if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            else type(node).__name__
            for node in block
            if not (
                isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in allowed_names
            )
        ]
        if unrelated:
            raise PatchError(
                "Unexpected class members occur inside the descriptor-watcher block: "
                + ", ".join(unrelated)
            )

        start = concrete_methods[0].lineno - 1
        end = concrete_methods[-1].end_lineno or concrete_methods[-1].lineno
        edits.append(LineEdit(
            start=start,
            end=end,
            replacement=FD_METHODS,
            description="implement descriptor watchers with QSocketNotifier",
        ))
        descriptions.append(
            "migrated legacy descriptor watcher implementation"
            if legacy_patch
            else "implemented add/remove reader/writer"
        )

    modified = apply_line_edits(source, edits) if edits else source
    try:
        compile(modified, "events.py", "exec")
    except SyntaxError as error:
        raise PatchError(f"Generated events.py does not compile: {error}") from error
    return modified, tuple(descriptions)


def patch_tasks_source(
        source: str,
        *,
        target_python: tuple[int, int, int],
        force: bool,
) -> tuple[str, tuple[str, ...]]:
    if target_python < (3, 14, 0):
        return source, ()

    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise PatchError(f"tasks.py does not parse: {error}") from error

    task_class = find_class(tree, "QAsyncioTask")
    existing = class_method(task_class, "_make_cancelled_error")

    if existing is not None:
        # Native Qt implementations win. An already-marked method is
        # idempotent. The small implementation produced by the original v1
        # patch is recognized and upgraded automatically.
        if TASKS_METHOD_MARKER in source:
            return source, ()
        existing_lines = source.splitlines(keepends=True)[
            existing.lineno - 1:(existing.end_lineno or existing.lineno)
        ]
        existing_source = "".join(existing_lines)
        legacy_patch = (
            "_cancel_message" in existing_source
            and "_cancelled_exc" not in existing_source
            and "CancelledError" in existing_source
        )
        if not legacy_patch and not force:
            return source, ()

        edit = LineEdit(
            start=existing.lineno - 1,
            end=existing.end_lineno or existing.lineno,
            replacement=CANCELLED_ERROR_METHOD.rstrip("\n"),
            description="replace _make_cancelled_error",
        )
    else:
        get_coro = class_method(task_class, "get_coro")
        if get_coro is not None:
            insertion_line = get_coro.lineno - 1
        elif task_class.body:
            insertion_line = task_class.body[-1].end_lineno or task_class.body[-1].lineno
        else:
            raise PatchError("QAsyncioTask has no body")

        edit = LineEdit(
            start=insertion_line,
            end=insertion_line,
            replacement=CANCELLED_ERROR_METHOD,
            description="add _make_cancelled_error",
        )

    modified = apply_line_edits(source, [edit])
    try:
        compile(modified, "tasks.py", "exec")
    except SyntaxError as error:
        raise PatchError(f"Generated tasks.py does not compile: {error}") from error
    return modified, ("added Python 3.14 cancellation compatibility",)


def build_changes(environment: EnvironmentInfo, *, force: bool) -> list[SourceChange]:
    events_original = environment.events_path.read_text(encoding="utf-8")
    tasks_original = environment.tasks_path.read_text(encoding="utf-8")

    events_modified, events_descriptions = patch_events_source(
        events_original, force=force
    )
    tasks_modified, tasks_descriptions = patch_tasks_source(
        tasks_original,
        target_python=environment.python_version,
        force=force,
    )

    return [
        SourceChange(
            environment.events_path,
            events_original,
            events_modified,
            events_descriptions,
        ),
        SourceChange(
            environment.tasks_path,
            tasks_original,
            tasks_modified,
            tasks_descriptions,
        ),
    ]


def default_backup_root(environment: EnvironmentInfo) -> Path:
    return environment.prefix / ".qtasyncio-patch-backups"


def backup_changes(
        environment: EnvironmentInfo,
        changes: Sequence[SourceChange],
        backup_root: Path,
) -> Path:
    timestamp = dt.datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    backup_dir = backup_root / timestamp
    suffix = 1
    while backup_dir.exists():
        backup_dir = backup_root / f"{timestamp}-{suffix}"
        suffix += 1

    backup_dir.mkdir(parents=True, exist_ok=False)
    records = []

    for index, change in enumerate(changes):
        if not change.changed:
            continue
        backup_name = f"{index}-{change.path.name}"
        backup_path = backup_dir / backup_name
        shutil.copy2(change.path, backup_path)
        records.append({
            "path": str(change.path),
            "backup": backup_name,
            "before_sha256": sha256_text(change.original),
            "after_sha256": sha256_text(change.modified),
        })

    manifest = {
        "patch_id": PATCH_ID,
        "created_at": dt.datetime.now().astimezone().isoformat(),
        "python": str(environment.python),
        "python_version": list(environment.python_version),
        "pyside_version": environment.pyside_version,
        "files": records,
    }
    (backup_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return backup_dir


def atomic_write_text(path: Path, text: str) -> None:
    original_mode = path.stat().st_mode
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, original_mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def apply_changes(
        environment: EnvironmentInfo,
        changes: Sequence[SourceChange],
        backup_root: Path,
) -> Path | None:
    changed = [change for change in changes if change.changed]
    if not changed:
        return None

    backup_dir = backup_changes(environment, changed, backup_root)
    written: list[SourceChange] = []
    try:
        for change in changed:
            atomic_write_text(change.path, change.modified)
            written.append(change)
    except BaseException:
        for change in reversed(written):
            atomic_write_text(change.path, change.original)
        raise

    return backup_dir


def latest_backup(backup_root: Path) -> Path:
    if not backup_root.is_dir():
        raise PatchError(f"No backup directory exists at {backup_root}")

    candidates = sorted(
        (path for path in backup_root.iterdir() if (path / "manifest.json").is_file()),
        key=lambda path: path.name,
        reverse=True,
    )
    if not candidates:
        raise PatchError(f"No QtAsyncio patch backups found in {backup_root}")
    return candidates[0]


def restore_backup(backup_dir: Path, *, force: bool) -> None:
    manifest_path = backup_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("patch_id") != PATCH_ID:
        raise PatchError(f"Unsupported backup manifest: {manifest_path}")

    records = manifest.get("files", [])
    if not records:
        raise PatchError(f"Backup contains no files: {backup_dir}")

    for record in records:
        target = Path(record["path"])
        expected_after = record["after_sha256"]
        if target.exists() and sha256_file(target) != expected_after and not force:
            raise PatchError(
                f"Refusing to restore {target}: it changed after patching. "
                "Use --force to overwrite the newer file."
            )

    for record in records:
        target = Path(record["path"])
        backup = backup_dir / record["backup"]
        atomic_write_text(target, backup.read_text(encoding="utf-8"))


def verify_sources(environment: EnvironmentInfo) -> list[str]:
    events = environment.events_path.read_text(encoding="utf-8")
    tasks = environment.tasks_path.read_text(encoding="utf-8")
    problems: list[str] = []

    try:
        compile(events, str(environment.events_path), "exec")
    except SyntaxError as error:
        problems.append(f"events.py does not compile: {error}")
    try:
        compile(tasks, str(environment.tasks_path), "exec")
    except SyntaxError as error:
        problems.append(f"tasks.py does not compile: {error}")

    for marker in (EVENTS_INIT_MARKER, EVENTS_CLOSE_MARKER, EVENTS_METHODS_MARKER):
        if marker not in events:
            problems.append(f"events.py is missing marker {marker}")
    if "QSocketNotifier" not in events:
        problems.append("events.py does not import QSocketNotifier")

    if environment.python_version >= (3, 14, 0):
        tree = ast.parse(tasks)
        task_class = find_class(tree, "QAsyncioTask")
        if class_method(task_class, "_make_cancelled_error") is None:
            problems.append("tasks.py lacks QAsyncioTask._make_cancelled_error()")

    return problems


def verify_imports(
        environment: EnvironmentInfo, *, require_patch: bool = True) -> None:
    probe = r'''
import sys
import PySide6.QtAsyncio.events as events
import PySide6.QtAsyncio.tasks as tasks

if REQUIRE_PATCH:
    required = ("add_reader", "remove_reader", "add_writer", "remove_writer")
    missing = [name for name in required if not hasattr(events.QAsyncioEventLoop, name)]
    if missing:
        raise RuntimeError(f"QAsyncioEventLoop missing: {missing}")

    if (sys.version_info >= (3, 14)
            and not hasattr(tasks.QAsyncioTask, "_make_cancelled_error")):
        raise RuntimeError("QAsyncioTask._make_cancelled_error is missing")

print("ok")
'''.replace("REQUIRE_PATCH", repr(require_patch))
    process = subprocess.run(
        [str(environment.python), "-I", "-c", probe],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if process.returncode != 0:
        raise PatchError(
            "The patched QtAsyncio modules failed to import:\n"
            + process.stderr.strip()
        )


def print_environment(environment: EnvironmentInfo) -> None:
    python_version = ".".join(map(str, environment.python_version))
    print(f"Target Python : {environment.python}")
    print(f"Python version: {python_version}")
    print(f"PySide6       : {environment.pyside_version}")
    print(f"events.py     : {environment.events_path}")
    print(f"tasks.py      : {environment.tasks_path}")


def validate_version(environment: EnvironmentInfo, *, force: bool) -> None:
    version = parse_version(environment.pyside_version)
    if version[:2] != SUPPORTED_PYSIDE_MAJOR_MINOR and not force:
        supported = ".".join(map(str, SUPPORTED_PYSIDE_MAJOR_MINOR))
        raise PatchError(
            f"This patcher targets PySide6 {supported}.x, but found "
            f"{environment.pyside_version}. Use --force only after reviewing "
            "the installed QtAsyncio source."
        )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        default=sys.prefix if sys.prefix != sys.base_prefix else ".venv",
        type=Path,
        help="virtual environment directory or its Python executable",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--restore",
        action="store_true",
        help="restore the newest hash-verified backup",
    )
    action.add_argument(
        "--verify",
        action="store_true",
        help="verify patch markers, compilation and imports without modifying files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show planned changes without writing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="override version/native-implementation/hash safety checks",
    )
    parser.add_argument(
        "--backup-root",
        type=Path,
        help="custom backup directory (default: <venv>/.qtasyncio-patch-backups)",
    )
    args = parser.parse_args(argv)

    try:
        environment = inspect_environment(args.target)
        validate_version(environment, force=args.force)
        backup_root = (
            args.backup_root.expanduser().resolve()
            if args.backup_root
            else default_backup_root(environment)
        )

        print_environment(environment)

        if args.restore:
            backup_dir = latest_backup(backup_root)
            restore_backup(backup_dir, force=args.force)
            verify_imports(environment, require_patch=False)
            print(f"\nRestored backup: {backup_dir}")
            return 0

        if args.verify:
            problems = verify_sources(environment)
            if problems:
                print("\nVerification failed:", file=sys.stderr)
                for problem in problems:
                    print(f"  - {problem}", file=sys.stderr)
                return 1
            verify_imports(environment)
            print("\nQtAsyncio compatibility patch verified successfully.")
            return 0

        changes = build_changes(environment, force=args.force)
        changed = [change for change in changes if change.changed]

        if not changed:
            problems = verify_sources(environment)
            if problems:
                raise PatchError(
                    "No source edits were generated, but verification failed:\n  - "
                    + "\n  - ".join(problems)
                )
            verify_imports(environment)
            print("\nNothing to do; the compatibility patch is already installed.")
            return 0

        print("\nPlanned changes:")
        for change in changed:
            print(f"  {change.path.name}:")
            for description in change.descriptions:
                print(f"    - {description}")
            print(f"    {sha256_text(change.original)[:12]} -> "
                  f"{sha256_text(change.modified)[:12]}")

        if args.dry_run:
            print("\nDry run only; no files were modified.")
            return 0

        backup_dir = apply_changes(environment, changes, backup_root)
        try:
            problems = verify_sources(environment)
            if problems:
                raise PatchError(
                    "Post-write verification failed:\n  - "
                    + "\n  - ".join(problems)
                )
            verify_imports(environment)
        except BaseException:
            if backup_dir is not None:
                restore_backup(backup_dir, force=True)
            raise

        print(f"\nPatched successfully. Backup: {backup_dir}")
        print("Run again with --verify after any PySide6 upgrade.")
        return 0

    except PatchError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())