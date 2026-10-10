#!/usr/bin/env python3
"""
Safely patch PySide6 6.11/6.12 QtAsyncio for Python 3.14, descriptor-based I/O,
and nested Qt event loops.

The patch adds QSocketNotifier-backed implementations of:

    add_reader / remove_reader / add_writer / remove_writer

and, when required, adds QAsyncioTask._make_cancelled_error() for Python 3.14.
It makes each task capture its creation context so ContextVar values survive
across awaits, and makes futures retain the context registered with each done
callback, matching asyncio Task and Future semantics.
It also defers task steps that Qt dispatches re-entrantly while another asyncio
task is active, which can otherwise happen when application code opens a nested
QEventLoop for a modal dialog.

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
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Sequence

PATCH_ID = "qtasyncio-compat-v2"
SUPPORTED_PYSIDE_MAJOR_MINORS = ((6, 11), (6, 12))

EVENTS_IMPORT_MARKER = f"{PATCH_ID}:qsocketnotifier-import"
EVENTS_INIT_MARKER = f"{PATCH_ID}:fd-state"
EVENTS_CLOSE_MARKER = f"{PATCH_ID}:fd-close"
EVENTS_METHODS_MARKER = f"{PATCH_ID}:fd-methods"
FUTURES_CALLBACK_CONTEXT_MARKER = f"{PATCH_ID}:future-callback-context"
FUTURES_CALLBACK_REMOVAL_MARKER = f"{PATCH_ID}:future-callback-removal"
TASKS_METHOD_MARKER = f"{PATCH_ID}:cancelled-error"
TASKS_CONTEXT_MARKER = f"{PATCH_ID}:task-context"
TASKS_REENTRANCY_GUARD_MARKER = f"{PATCH_ID}:task-reentrancy-guard"
TASKS_SELF_REENTRANCY_MARKER = f"{PATCH_ID}:task-self-reentrancy-drop"
TASKS_REENTRANCY_DRAIN_MARKER = f"{PATCH_ID}:task-reentrancy-drain"


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
    futures_path: Path
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

FUTURE_SCHEDULE_CALLBACKS = f'''\
    # {FUTURES_CALLBACK_CONTEXT_MARKER}
    def _schedule_callbacks(self):
        """Schedule done callbacks in the contexts captured when registered."""
        callbacks = self._callbacks
        self._callbacks = []
        for callback, context in callbacks:
            self._loop.call_soon(callback, self, context=context)
'''

FUTURE_ADD_DONE_CALLBACK = '''\
    def add_done_callback(self, cb: Callable, *,
                          context: contextvars.Context | None = None) -> None:
        if context is None:
            context = contextvars.copy_context()
        if self.done():
            self._loop.call_soon(cb, self, context=context)
        else:
            self._callbacks.append((cb, context))
'''

FUTURE_REMOVE_DONE_CALLBACK = f'''\
    # {FUTURES_CALLBACK_REMOVAL_MARKER}
    def remove_done_callback(self, cb: Callable) -> int:
        original_len = len(self._callbacks)
        self._callbacks = [
            (callback, context)
            for callback, context in self._callbacks
            if callback != cb
        ]
        return original_len - len(self._callbacks)
'''

TASK_CONTEXT_CAPTURE = f'''\

        # {TASKS_CONTEXT_MARKER}
        # asyncio.Task snapshots the current context when no explicit context
        # is supplied. Without this, Qt callbacks can resume one coroutine in
        # different Context objects on either side of an await.
        if self._context is None:
            self._context = contextvars.copy_context()
'''

REENTRANT_STEP_GUARD = f'''\

        # {TASKS_REENTRANCY_GUARD_MARKER}
        # A modal/nested Qt event loop can dispatch another QAsyncioTask step
        # before the currently entered task has yielded. CPython rejects that
        # re-entrancy. Attach the step to the active task so it can release the
        # work immediately after leaving its asyncio task context.
        active_task = asyncio.current_task(loop=self._loop)

        # {TASKS_SELF_REENTRANCY_MARKER}
        # A task can receive its own completion callback synchronously before
        # its coroutine has yielded the completed future. Queuing that callback
        # would advance the coroutine a second time during its next await. The
        # normal handling below will register a fresh callback for the yielded
        # future, so this early self-step must simply be discarded.
        if active_task is self:
            return

        if active_task is not None:
            deferred_steps = getattr(
                active_task, "_qtasyncio_deferred_steps", None
            )
            if deferred_steps is None:
                deferred_steps = []
                active_task._qtasyncio_deferred_steps = deferred_steps
            deferred_steps.append((self, exception_or_future))
            return
'''

REENTRANT_STEP_DRAIN = f'''\

        # {TASKS_REENTRANCY_DRAIN_MARKER}
        deferred_steps = getattr(self, "_qtasyncio_deferred_steps", ())
        self._qtasyncio_deferred_steps = []
        for deferred_task, deferred_result in deferred_steps:
            self._loop.call_soon(
                deferred_task._step,
                deferred_result,
                context=deferred_task._context,
            )
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
import PySide6.QtAsyncio.futures as futures
import PySide6.QtAsyncio.tasks as tasks

print(json.dumps({
    "prefix": sys.prefix,
    "python_version": list(sys.version_info[:3]),
    "pyside_version": PySide6.__version__,
    "events_path": events.__file__,
    "futures_path": futures.__file__,
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
        futures_path=Path(data["futures_path"]).resolve(),
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


def is_self_method_call(node: ast.AST, method_name: str) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == method_name
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "self"
    )


def find_task_done_guard_line(step_method: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    for statement in step_method.body:
        if isinstance(statement, ast.If) and is_self_method_call(statement.test, "done"):
            return statement.end_lineno or statement.lineno
    raise PatchError("Could not find QAsyncioTask._step() done guard")


def find_super_init_line(init_method: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    for statement in init_method.body:
        if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
            continue
        call = statement.value
        if (
            isinstance(call.func, ast.Attribute)
            and call.func.attr == "__init__"
            and isinstance(call.func.value, ast.Call)
            and isinstance(call.func.value.func, ast.Name)
            and call.func.value.func.id == "super"
        ):
            return statement.end_lineno or statement.lineno
    raise PatchError("Could not find QAsyncioTask.__init__() super call")


def find_task_step_try(step_method: ast.FunctionDef | ast.AsyncFunctionDef) -> ast.Try:
    for statement in step_method.body:
        if not isinstance(statement, ast.Try):
            continue
        for node in ast.walk(statement):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "asyncio"
                and node.func.attr == "_enter_task"
            ):
                return statement
    raise PatchError("Could not find the task-entry try block in QAsyncioTask._step()")


def find_active_task_assignment(
        step_method: ast.FunctionDef | ast.AsyncFunctionDef,
) -> ast.Assign:
    for statement in step_method.body:
        if not isinstance(statement, ast.Assign):
            continue
        if any(
                isinstance(target, ast.Name) and target.id == "active_task"
                for target in statement.targets
        ):
            return statement
    raise PatchError("Could not find active_task assignment in QAsyncioTask._step()")


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
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise PatchError(f"tasks.py does not parse: {error}") from error

    task_class = find_class(tree, "QAsyncioTask")
    edits: list[LineEdit] = []
    descriptions: list[str] = []

    if TASKS_CONTEXT_MARKER not in source:
        init_method = class_method(task_class, "__init__")
        if init_method is None:
            raise PatchError("Could not find QAsyncioTask.__init__()")
        insertion_line = find_super_init_line(init_method)
        edits.append(LineEdit(
            start=insertion_line,
            end=insertion_line,
            replacement=TASK_CONTEXT_CAPTURE,
            description="capture each task's context",
        ))
        descriptions.append("made task ContextVar state persist across awaits")

    if target_python >= (3, 14, 0):
        existing = class_method(task_class, "_make_cancelled_error")

        if existing is not None:
            # Native Qt implementations win. An already-marked method is
            # idempotent. The small implementation produced by the original v1
            # patch is recognized and upgraded automatically.
            if TASKS_METHOD_MARKER not in source:
                existing_lines = source.splitlines(keepends=True)[
                    existing.lineno - 1:(existing.end_lineno or existing.lineno)
                ]
                existing_source = "".join(existing_lines)
                legacy_patch = (
                    "_cancel_message" in existing_source
                    and "_cancelled_exc" not in existing_source
                    and "CancelledError" in existing_source
                )
                if legacy_patch or force:
                    edits.append(LineEdit(
                        start=existing.lineno - 1,
                        end=existing.end_lineno or existing.lineno,
                        replacement=CANCELLED_ERROR_METHOD.rstrip("\n"),
                        description="replace _make_cancelled_error",
                    ))
                    descriptions.append(
                        "added Python 3.14 cancellation compatibility"
                    )
        else:
            get_coro = class_method(task_class, "get_coro")
            if get_coro is not None:
                insertion_line = get_coro.lineno - 1
            elif task_class.body:
                insertion_line = (
                    task_class.body[-1].end_lineno or task_class.body[-1].lineno
                )
            else:
                raise PatchError("QAsyncioTask has no body")

            edits.append(LineEdit(
                start=insertion_line,
                end=insertion_line,
                replacement=CANCELLED_ERROR_METHOD,
                description="add _make_cancelled_error",
            ))
            descriptions.append("added Python 3.14 cancellation compatibility")

    reentrancy_markers = (
        TASKS_REENTRANCY_GUARD_MARKER in source,
        TASKS_REENTRANCY_DRAIN_MARKER in source,
    )
    if any(reentrancy_markers) and not all(reentrancy_markers):
        raise PatchError("tasks.py contains an incomplete task re-entrancy patch")

    step_method = class_method(task_class, "_step")
    if step_method is None:
        raise PatchError("Could not find QAsyncioTask._step()")

    if not any(reentrancy_markers):
        done_guard_line = find_task_done_guard_line(step_method)
        task_step_try = find_task_step_try(step_method)
        edits.extend((
            LineEdit(
                start=done_guard_line,
                end=done_guard_line,
                replacement=REENTRANT_STEP_GUARD,
                description="guard against re-entrant task steps",
            ),
            LineEdit(
                start=task_step_try.end_lineno or task_step_try.lineno,
                end=task_step_try.end_lineno or task_step_try.lineno,
                replacement=REENTRANT_STEP_DRAIN,
                description="release deferred task steps after yielding",
            ),
        ))
        descriptions.append("deferred task steps dispatched by nested Qt event loops")
    elif TASKS_SELF_REENTRANCY_MARKER not in source:
        active_task_assignment = find_active_task_assignment(step_method)
        self_reentrancy_guard = f'''\

        # {TASKS_SELF_REENTRANCY_MARKER}
        # Drop synchronous callbacks that try to advance the task which is
        # already running. Its yielded future will schedule the real next step.
        if active_task is self:
            return
'''
        insertion_line = (
            active_task_assignment.end_lineno or active_task_assignment.lineno
        )
        edits.append(LineEdit(
            start=insertion_line,
            end=insertion_line,
            replacement=self_reentrancy_guard,
            description="discard premature self-reentrant task steps",
        ))
        descriptions.append("made task re-entrancy handling self-step safe")

    modified = apply_line_edits(source, edits) if edits else source
    try:
        compile(modified, "tasks.py", "exec")
    except SyntaxError as error:
        raise PatchError(f"Generated tasks.py does not compile: {error}") from error
    return modified, tuple(descriptions)


def patch_futures_source(source: str, *, force: bool) -> tuple[str, tuple[str, ...]]:
    try:
        tree = ast.parse(source)
    except SyntaxError as error:
        raise PatchError(f"futures.py does not parse: {error}") from error

    context_is_patched = FUTURES_CALLBACK_CONTEXT_MARKER in source
    removal_is_patched = FUTURES_CALLBACK_REMOVAL_MARKER in source
    if context_is_patched and removal_is_patched:
        return source, ()

    future_class = find_class(tree, "QAsyncioFuture")
    schedule_callbacks = class_method(future_class, "_schedule_callbacks")
    add_done_callback = class_method(future_class, "add_done_callback")
    remove_done_callback = class_method(future_class, "remove_done_callback")
    if schedule_callbacks is None or add_done_callback is None or remove_done_callback is None:
        raise PatchError("Could not find QAsyncioFuture callback methods")

    edits = []
    descriptions = []
    if not context_is_patched:
        schedule_source = "".join(source.splitlines(keepends=True)[
            schedule_callbacks.lineno - 1:(schedule_callbacks.end_lineno or schedule_callbacks.lineno)
        ])
        add_source = "".join(source.splitlines(keepends=True)[
            add_done_callback.lineno - 1:(add_done_callback.end_lineno or add_done_callback.lineno)
        ])
        legacy_callbacks = (
            "for cb in self._callbacks" in schedule_source
            and "self._callbacks.append(cb)" in add_source
            and "context if context else self._context" in schedule_source + add_source
        )
        if not legacy_callbacks and not force:
            raise PatchError(
                "QAsyncioFuture contains an unfamiliar callback implementation. "
                "Refusing to overwrite it without --force."
            )
        edits.extend((LineEdit(
            start=schedule_callbacks.lineno - 1,
            end=schedule_callbacks.end_lineno or schedule_callbacks.lineno,
            replacement=FUTURE_SCHEDULE_CALLBACKS.rstrip("\n"),
            description="schedule future callbacks in their registered contexts",
        ),
        LineEdit(
            start=add_done_callback.lineno - 1,
            end=add_done_callback.end_lineno or add_done_callback.lineno,
            replacement=FUTURE_ADD_DONE_CALLBACK.rstrip("\n"),
            description="capture each future callback's context",
        )))
        descriptions.append("preserved ContextVar state for future callbacks")

    if not removal_is_patched:
        edits.append(LineEdit(
            start=remove_done_callback.lineno - 1,
            end=remove_done_callback.end_lineno or remove_done_callback.lineno,
            replacement=FUTURE_REMOVE_DONE_CALLBACK.rstrip("\n"),
            description="remove context-aware future callbacks",
        ))
        descriptions.append("made callback removal context-aware")

    modified = apply_line_edits(source, edits)
    try:
        compile(modified, "futures.py", "exec")
    except SyntaxError as error:
        raise PatchError(f"Generated futures.py does not compile: {error}") from error
    return modified, tuple(descriptions)


def build_changes(environment: EnvironmentInfo, *, force: bool) -> list[SourceChange]:
    events_original = environment.events_path.read_text(encoding="utf-8")
    futures_original = environment.futures_path.read_text(encoding="utf-8")
    tasks_original = environment.tasks_path.read_text(encoding="utf-8")

    events_modified, events_descriptions = patch_events_source(
        events_original, force=force
    )
    futures_modified, futures_descriptions = patch_futures_source(
        futures_original, force=force
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
            environment.futures_path,
            futures_original,
            futures_modified,
            futures_descriptions,
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
    futures = environment.futures_path.read_text(encoding="utf-8")
    tasks = environment.tasks_path.read_text(encoding="utf-8")
    problems: list[str] = []

    try:
        compile(events, str(environment.events_path), "exec")
    except SyntaxError as error:
        problems.append(f"events.py does not compile: {error}")
    try:
        compile(futures, str(environment.futures_path), "exec")
    except SyntaxError as error:
        problems.append(f"futures.py does not compile: {error}")
    try:
        compile(tasks, str(environment.tasks_path), "exec")
    except SyntaxError as error:
        problems.append(f"tasks.py does not compile: {error}")

    for marker in (EVENTS_INIT_MARKER, EVENTS_CLOSE_MARKER, EVENTS_METHODS_MARKER):
        if marker not in events:
            problems.append(f"events.py is missing marker {marker}")
    if "QSocketNotifier" not in events:
        problems.append("events.py does not import QSocketNotifier")
    if FUTURES_CALLBACK_CONTEXT_MARKER not in futures:
        problems.append(f"futures.py is missing marker {FUTURES_CALLBACK_CONTEXT_MARKER}")
    if FUTURES_CALLBACK_REMOVAL_MARKER not in futures:
        problems.append(f"futures.py is missing marker {FUTURES_CALLBACK_REMOVAL_MARKER}")

    if environment.python_version >= (3, 14, 0):
        tree = ast.parse(tasks)
        task_class = find_class(tree, "QAsyncioTask")
        if class_method(task_class, "_make_cancelled_error") is None:
            problems.append("tasks.py lacks QAsyncioTask._make_cancelled_error()")

    for marker in (
        TASKS_CONTEXT_MARKER,
        TASKS_REENTRANCY_GUARD_MARKER,
        TASKS_SELF_REENTRANCY_MARKER,
        TASKS_REENTRANCY_DRAIN_MARKER,
    ):
        if marker not in tasks:
            problems.append(f"tasks.py is missing marker {marker}")

    return problems


def verify_imports(
        environment: EnvironmentInfo, *, require_patch: bool = True) -> None:
    probe = r'''
import asyncio
import sys
from contextlib import contextmanager
from contextvars import ContextVar
from PySide6 import QtAsyncio
import PySide6.QtAsyncio.events as events
import PySide6.QtAsyncio.futures as futures
import PySide6.QtAsyncio.tasks as tasks

if REQUIRE_PATCH:
    required = ("add_reader", "remove_reader", "add_writer", "remove_writer")
    missing = [name for name in required if not hasattr(events.QAsyncioEventLoop, name)]
    if missing:
        raise RuntimeError(f"QAsyncioEventLoop missing: {missing}")

    if (sys.version_info >= (3, 14)
            and not hasattr(tasks.QAsyncioTask, "_make_cancelled_error")):
        raise RuntimeError("QAsyncioTask._make_cancelled_error is missing")

    value = ContextVar("qtasyncio_patch_verify", default=None)

    @contextmanager
    def context_scope():
        token = value.set("active")
        try:
            yield
        finally:
            value.reset(token)

    async def verify_context_across_await():
        with context_scope():
            await asyncio.sleep(0.001)
        if value.get() is not None:
            raise RuntimeError("QAsyncioTask leaked ContextVar state")

    QtAsyncio.run(verify_context_across_await(), keep_running=False)

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
    print(f"futures.py    : {environment.futures_path}")
    print(f"tasks.py      : {environment.tasks_path}")


def validate_version(environment: EnvironmentInfo, *, force: bool) -> None:
    version = parse_version(environment.pyside_version)
    if version[:2] not in SUPPORTED_PYSIDE_MAJOR_MINORS and not force:
        supported = " or ".join(".".join(map(str, minor)) + ".x"
                                for minor in SUPPORTED_PYSIDE_MAJOR_MINORS)
        raise PatchError(
            f"This patcher targets PySide6 {supported}, but found "
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
