"""Exercise real child output, retained logs and failure codes without compiling."""
import importlib.util
import io
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from scripts import build_output, build_terminal

WRAPPER = Path(build_output.__file__)


class BuildOutputTests(unittest.TestCase):
    def invoke(self, directory, code, *options, verbose="0"):
        log = Path(directory) / "compiler.log"
        environment = {**os.environ, "PORN_FETCH_BUILD_VERBOSE": verbose, "NO_COLOR": "1"}
        result = subprocess.run(
            [sys.executable, str(WRAPPER), "--label", "Fixture", "--log-file", str(log),
             *options, "--", sys.executable, "-c", code],
            capture_output=True, text=True, env=environment, timeout=10,
        )
        return result, log

    def test_default_streams_and_retains_both_output_streams(self):
        with tempfile.TemporaryDirectory() as directory:
            result, log = self.invoke(directory, "import sys; print('compiler output'); print('diagnostic', file=sys.stderr)")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertIn("compiler output", result.stderr)
            self.assertIn("diagnostic", result.stderr)
            self.assertIn("Fixture finished", result.stderr)
            self.assertIn(str(log), result.stderr)
            self.assertIn("compiler output", log.read_text())
            self.assertIn("diagnostic", log.read_text())

    def test_verbose_flag_streams_and_retains_full_output(self):
        with tempfile.TemporaryDirectory() as directory:
            result, log = self.invoke(directory, "print('compiler details')", "--verbose")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("compiler details", result.stderr)
            self.assertIn("compiler details", log.read_text())

    def test_environment_enables_verbose_output_in_child_build_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            result, _ = self.invoke(directory, "import os; print('verbose=' + os.environ['PORN_FETCH_BUILD_VERBOSE'])",
                                    verbose="true")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("verbose=1", result.stderr)

    def test_old_quiet_environment_cannot_hide_build_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            result, _ = self.invoke(directory, "import os; print('verbose=' + os.environ['PORN_FETCH_BUILD_VERBOSE'])")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("verbose=1", result.stderr)
        with patch.dict(os.environ, {"PORN_FETCH_BUILD_VERBOSE": "0"}), redirect_stderr(io.StringIO()) as output:
            build_output.detail("patch diagnostics")
        self.assertIn("patch diagnostics", output.getvalue())

    def test_failure_preserves_full_terminal_output_log_and_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            result, log = self.invoke(directory, "import sys; print('earlier details'); "
                                      "[print('line ' + str(i), flush=True) for i in range(40)]; "
                                      "print('compiler failed', file=sys.stderr); sys.exit(17)")
            self.assertEqual(result.returncode, 17)
            self.assertIn("compiler failed", result.stderr)
            self.assertIn("exit 17", result.stderr)
            self.assertIn(str(log), result.stderr)
            self.assertIn("earlier details", result.stderr)
            self.assertEqual(result.stderr.splitlines().count("compiler failed"), 1)
            self.assertIn("earlier details", log.read_text())

    def test_default_output_reaches_terminal_and_log_before_child_exits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            release = root / "continue-build"
            log = root / "compiler.log"
            # The child deliberately omits flush=True; the wrapper must also
            # disable Python buffering in nested deploy/compiler processes.
            code = """
import pathlib, sys, time
print('compiler stdout ready')
print('compiler stderr ready', file=sys.stderr)
for _ in range(500):
    if pathlib.Path(sys.argv[1]).exists():
        break
    time.sleep(0.01)
print('compiler finished')
"""
            with subprocess.Popen(
                [sys.executable, str(WRAPPER), "--label", "Live fixture", "--log-file", str(log),
                 "--", sys.executable, "-c", code, str(release)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                env={**os.environ, "PORN_FETCH_BUILD_VERBOSE": "0", "NO_COLOR": "1"},
            ) as process:
                try:
                    received = ""
                    while "compiler stderr ready" not in received.splitlines():
                        line = process.stderr.readline()
                        if not line:
                            break
                        received += line
                    self.assertIn("compiler stdout ready", received.splitlines())
                    self.assertIn("compiler stderr ready", received.splitlines())
                    self.assertIsNone(process.poll(), received)
                    retained = log.read_text()
                    self.assertIn("compiler stdout ready", retained)
                    self.assertIn("compiler stderr ready", retained)
                    self.assertNotIn("compiler finished", retained)
                finally:
                    release.touch()
                    _, remaining = process.communicate(timeout=10)
                self.assertEqual(process.returncode, 0, received + remaining)
                self.assertIn("compiler finished", log.read_text())

    @unittest.skipIf(sys.platform == "win32" and importlib.util.find_spec("winpty") is None,
                     "Windows terminal builds need the desktop-build extra")
    def test_terminal_mode_keeps_tty_and_carriage_returns_in_terminal_and_log(self):
        class TerminalOutput(io.StringIO):
            def isatty(self):
                return True

        code = "import sys; print('tty=' + str(sys.stdout.isatty() and sys.stderr.isatty())); " \
               "sys.stdout.write('progress 25%\\rprogress 100%\\n'); sys.stdout.flush(); sys.exit(17)"
        with tempfile.TemporaryDirectory() as directory, redirect_stderr(TerminalOutput()) as output:
            log = Path(directory) / "progress.log"
            with self.assertRaises(subprocess.CalledProcessError) as failure:
                build_output.run([sys.executable, "-c", code], label="Progress", log_path=log, terminal=True)
            self.assertEqual(failure.exception.returncode, 17)
            self.assertIn("tty=True", output.getvalue())
            self.assertIn("progress 25%\rprogress 100%", output.getvalue())
            self.assertIn(b"progress 25%\rprogress 100%", log.read_bytes())

    @unittest.skipUnless(importlib.util.find_spec("nuitka"), "Nuitka is needed for its native progress regression")
    @unittest.skipIf(sys.platform == "win32" and importlib.util.find_spec("winpty") is None,
                     "Windows terminal builds need the desktop-build extra")
    def test_native_nuitka_compiler_progress_survives_log_capture(self):
        class TerminalOutput(io.StringIO):
            def isatty(self):
                return True

        code = """
import time
from nuitka.build.SconsProgress import (
    enableSconsProgressBar, setSconsProgressBarTotal, updateSconsProgressBar,
)
enableSconsProgressBar('auto')
setSconsProgressBarTotal('Backend', 10)
for _ in range(10):
    updateSconsProgressBar()
    time.sleep(0.03)
"""
        with tempfile.TemporaryDirectory() as directory, redirect_stderr(TerminalOutput()) as output:
            log = Path(directory) / "nuitka.log"
            build_output.run([sys.executable, "-c", code], label="Nuitka", log_path=log, terminal=True)
            self.assertIn("Backend C", output.getvalue())
            self.assertRegex(output.getvalue(), r"\d+(?:\.\d+)?%")
            self.assertIn(b"/10 files", log.read_bytes())
            self.assertIn(b"Backend C linking", log.read_bytes())

    def test_windows_conpty_quotes_arguments_retains_output_and_propagates_exit_code(self):
        class WinptyError(Exception):
            pass

        terminal = Mock()
        terminal.read.side_effect = ["compiler 50%\rcompiler 100%\r\n", WinptyError("end of terminal")]
        terminal.iseof.return_value = True
        terminal.isalive.return_value = False
        terminal.get_exitstatus.return_value = 23
        constructor = Mock(return_value=terminal)
        modules = {"winpty": SimpleNamespace(PTY=constructor, WinptyError=WinptyError),
                   "winpty.enums": SimpleNamespace(Backend=SimpleNamespace(ConPTY=0))}
        with tempfile.TemporaryDirectory() as directory, redirect_stderr(io.StringIO()) as output:
            log = Path(directory) / "windows.log"
            with patch.dict(sys.modules, modules), patch.object(build_terminal.sys, "platform", "win32"), \
                    patch.object(build_terminal.shutil, "which", return_value="C:\\Build Tools\\python.exe"):
                result = build_terminal.run_terminal(
                    ["python.exe", "module with spaces.py", "--mode=compile"], cwd=directory,
                    environment={"PATH": "C:\\Build Tools", "BUILD_VALUE": "kept"}, log_path=log,
                    on_silence=Mock(),
                )
            self.assertEqual(result, 23)
            self.assertIn("compiler 50%\rcompiler 100%", output.getvalue())
            self.assertIn(b"compiler 50%\rcompiler 100%", log.read_bytes())
            self.assertEqual(terminal.spawn.call_args.kwargs["cmdline"], ' "module with spaces.py" --mode=compile')
            self.assertIn("BUILD_VALUE=kept\0", terminal.spawn.call_args.kwargs["env"])
            terminal.cancel_io.assert_called_once()

    def test_no_color_overrides_forced_color(self):
        with patch.dict(os.environ, {"FORCE_COLOR": "1"}), redirect_stderr(io.StringIO()) as output:
            os.environ.pop("NO_COLOR", None)
            build_output.message("Warning", "warn")
            self.assertIn("\033[1;33m", output.getvalue())
            output.seek(0)
            output.truncate()
            os.environ["NO_COLOR"] = "1"
            build_output.message("Warning", "warn")
            self.assertNotIn("\033[", output.getvalue())


@unittest.skipUnless(shutil.which("bash"), "Shell build wrappers require bash")
class ShellBuildOutputTests(unittest.TestCase):
    def test_shell_wrappers_stream_both_streams_keep_logs_and_return_failure(self):
        project = WRAPPER.parents[1]
        for name in ("scripts/install.sh", "scripts/install_termux.sh", "packaging/build_linux_x86.sh"):
            with self.subTest(script=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                release = root / "continue-build"
                source = (project / name).read_text()
                function = "run() {\n" + source.split("\nrun() {\n", 1)[1].split("\n}\n", 1)[0] + "\n}\n"
                code = """
import pathlib, sys, time
print('stdout ready', flush=True)
print('stderr ready', file=sys.stderr, flush=True)
for _ in range(500):
    if pathlib.Path(sys.argv[1]).exists():
        break
    time.sleep(0.01)
print('later compiler output', flush=True)
sys.exit(17)
"""
                label = "" if name == "scripts/install.sh" else "'Fixture' "
                script = ("set -euo pipefail\ncmd() { :; }\ninfo() { :; }\nerror() { :; }\n"
                          "build_status() { :; }\n" + function +
                          f'run {label}"$1" -c {shlex.quote(code)} "$2"\n')
                with subprocess.Popen(
                    ["bash", "-c", script, "fixture", sys.executable, str(release)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    env={**os.environ, "TMPDIR": directory, "PORN_FETCH_BUILD_VERBOSE": "0"},
                ) as process:
                    try:
                        received = ""
                        while "stderr ready" not in received:
                            line = process.stdout.readline()
                            if not line:
                                break
                            received += line
                        self.assertIn("stdout ready", received)
                        self.assertIn("stderr ready", received)
                        self.assertIsNone(process.poll(), received)
                    finally:
                        release.touch()
                        remaining, errors = process.communicate(timeout=10)
                    self.assertEqual(process.returncode, 17, received + remaining + errors)
                    self.assertIn("later compiler output", remaining)
                    log, = root.glob("pornfetch-build.*")
                    self.assertIn("stdout ready", log.read_text())
                    self.assertIn("stderr ready", log.read_text())
                    self.assertIn("later compiler output", log.read_text())


if __name__ == "__main__":
    unittest.main()
