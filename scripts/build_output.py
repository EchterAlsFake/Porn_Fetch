"""Console and subprocess helpers for build tools.

Can also wrap an external tool: python scripts/build_output.py --label Build -- command
"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def verbose() -> bool:
    """Compatibility for build helpers: full diagnostics are always enabled."""
    return True


def add_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("-v", "--verbose", action="store_true", default=verbose(),
                        help="accepted for compatibility; full build output is always shown")


def configure(args: argparse.Namespace) -> None:
    os.environ["PORN_FETCH_BUILD_VERBOSE"] = "1"


def message(text: str, kind: str = "info") -> None:
    color = "NO_COLOR" not in os.environ and (
        sys.stderr.isatty() or os.environ.get("GITHUB_ACTIONS") == "true"
        or os.environ.get("FORCE_COLOR", "0") != "0"
    )
    label = {"info": "INFO", "ok": " OK ", "warn": "WARN", "error": "FAIL"}[kind]
    prefix = f"[{label}]"
    if color:
        code = {"info": 36, "ok": 32, "warn": 33, "error": 31}[kind]
        prefix = f"\033[1;{code}m{prefix}\033[0m"
    print(f"{prefix} {text}", file=sys.stderr, flush=True)


def detail(text: str) -> None:
    print(text, file=sys.stderr, flush=True)


def run(command, *, label: str, cwd=None, env=None, log_path: Path | None = None,
        terminal: bool = False) -> subprocess.CompletedProcess:
    """Stream complete child output to the terminal and retain it on disk.

    Use only for unattended commands. Password prompts and other interactive
    tools must retain their own terminal output.
    """
    if log_path is None:
        directory = Path(os.environ.get("PORN_FETCH_BUILD_LOG_DIR") or
                         Path(os.environ.get("RUNNER_TEMP") or tempfile.gettempdir()) / "porn-fetch-build-logs")
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        descriptor, name = tempfile.mkstemp(prefix="build-", suffix=".log", dir=directory)
        os.close(descriptor)
        log_path = Path(name)
    else:
        log_path.parent.mkdir(parents=True, exist_ok=True)
    message(f"{label} — log: {log_path}")
    detail(shlex.join([str(part) for part in command]))
    started = time.monotonic()
    last_activity = started
    environment = dict(os.environ if env is None else env, PYTHONUNBUFFERED="1")
    if terminal and (sys.stderr.isatty() or sys.stdin.isatty()):
        from scripts.build_terminal import run_terminal

        returncode = run_terminal(
            command, cwd=cwd, environment=environment, log_path=log_path,
            on_silence=lambda: message(f"{label}: still running ({int(time.monotonic() - started)}s)"),
        )
        if returncode:
            message(f"{label} failed (exit {returncode}). Full log: {log_path}", "error")
            raise subprocess.CalledProcessError(returncode, command)
        message(f"{label} finished ({int(time.monotonic() - started)}s)", "ok")
        return subprocess.CompletedProcess(command, returncode)
    with log_path.open("wb") as output, log_path.open(encoding="utf-8", errors="replace") as reader:
        with subprocess.Popen(command, cwd=cwd, env=environment, stdout=output, stderr=subprocess.STDOUT) as process:
            try:
                while True:
                    pending = reader.read()
                    if pending:
                        sys.stderr.write(pending)
                        sys.stderr.flush()
                        last_activity = time.monotonic()
                    elif time.monotonic() - last_activity >= 60:
                        message(f"{label}: still running ({int(time.monotonic() - started)}s)")
                        last_activity = time.monotonic()
                    try:
                        process.wait(timeout=0.2)
                        break
                    except subprocess.TimeoutExpired:
                        pass
                sys.stderr.write(reader.read())
                sys.stderr.flush()
            except BaseException:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                raise
    if process.returncode:
        message(f"{label} failed (exit {process.returncode}). Full log: {log_path}", "error")
        raise subprocess.CalledProcessError(process.returncode, command)
    message(f"{label} finished ({int(time.monotonic() - started)}s)", "ok")
    return subprocess.CompletedProcess(command, process.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_arguments(parser)
    parser.add_argument("--label", default="Build")
    parser.add_argument("--log-file", type=Path)
    parser.add_argument("--terminal", action="store_true", help="preserve compiler progress bars in an interactive terminal")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="command after --")
    args = parser.parse_args()
    configure(args)
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("a command is required after --")
    try:
        run(command, label=args.label, log_path=args.log_file, terminal=args.terminal)
    except subprocess.CalledProcessError as error:
        return error.returncode if error.returncode > 0 else 1
    except OSError as error:
        message(str(error), "error")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
