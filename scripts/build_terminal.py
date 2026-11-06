"""Keep terminal-aware compiler progress active while saving its output."""

from __future__ import annotations

import codecs
import errno
import os
import shutil
import signal
import subprocess
import sys
import time
from contextlib import contextmanager, suppress
from pathlib import Path


@contextmanager
def _open_terminal(command, cwd, environment):
    columns, rows = shutil.get_terminal_size()
    if sys.platform == "win32":
        from winpty import PTY, WinptyError
        from winpty.enums import Backend

        terminal = PTY(columns, rows, backend=Backend.ConPTY)
        executable = shutil.which(str(command[0]), path=environment.get("PATH"))
        if executable is None:
            raise FileNotFoundError(f"Build executable not found: {command[0]}")
        spawned = terminal.spawn(
            executable, cmdline=" " + subprocess.list2cmdline([str(arg) for arg in command[1:]]),
            cwd=str(Path(cwd or os.getcwd()).resolve()),
            env="\0".join(f"{key}={value}" for key, value in environment.items()) + "\0",
        )
        if not spawned:
            raise OSError(f"Could not start compiler in ConPTY: {executable}")

        def read():
            try:
                output = terminal.read(blocking=False)
            except EOFError:
                return None
            except WinptyError:
                if terminal.iseof() or not terminal.isalive():
                    return None
                raise
            if not output and not terminal.isalive():
                return None
            return output.encode("utf-8")

        def wait():
            while terminal.isalive():
                time.sleep(0.05)
            status = terminal.get_exitstatus()
            if status is None:
                raise RuntimeError("Compiler terminal closed without an exit status")
            return status

        try:
            yield read, wait
        finally:
            if terminal.isalive():
                os.kill(terminal.pid, signal.SIGTERM)
            with suppress(WinptyError):
                terminal.cancel_io()
    else:
        import select
        import termios

        reader, writer = os.openpty()
        process = None
        try:
            termios.tcsetwinsize(writer, (rows, columns))
            process = subprocess.Popen(command, cwd=cwd, env=environment, stdin=subprocess.DEVNULL,
                                       stdout=writer, stderr=writer)
            os.close(writer)
            writer = None

            def read():
                if not select.select([reader], [], [], 0)[0]:
                    return b""
                try:
                    return os.read(reader, 65536) or None
                except OSError as error:
                    if error.errno == errno.EIO:
                        return None
                    raise

            yield read, process.wait
        finally:
            if writer is not None:
                os.close(writer)
            os.close(reader)
            if process is not None and process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


def run_terminal(command, *, cwd, environment, log_path, on_silence) -> int:
    """Relay raw terminal output, including carriage returns and ANSI controls."""
    decoder = codecs.getincrementaldecoder("utf-8")(errors="replace")
    last_output = time.monotonic()
    with Path(log_path).open("wb") as log, _open_terminal(command, cwd, environment) as (read, wait):
        while True:
            output = read()
            if output is None:
                break
            if output:
                log.write(output)
                log.flush()
                sys.stderr.write(decoder.decode(output))
                sys.stderr.flush()
                last_output = time.monotonic()
            else:
                if time.monotonic() - last_output >= 60:
                    on_silence()
                    last_output = time.monotonic()
                time.sleep(0.05)
        sys.stderr.write(decoder.decode(b"", final=True))
        sys.stderr.flush()
        return wait()
