"""Exercise real child output, retained logs and failure codes without compiling."""
import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from scripts import build_output

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
            self.assertEqual(result.stderr.count("compiler failed"), 1)
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
                    while "compiler stderr ready" not in received:
                        line = process.stderr.readline()
                        if not line:
                            break
                        received += line
                    self.assertIn("compiler stdout ready", received)
                    self.assertIn("compiler stderr ready", received)
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


if __name__ == "__main__":
    unittest.main()
