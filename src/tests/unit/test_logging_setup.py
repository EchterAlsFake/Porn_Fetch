import errno
import logging
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.shared.logging_setup import ConsoleHandler, configure_app_logging


class LoggingSetupTests(unittest.TestCase):
    def test_desktop_log_file_does_not_require_a_writable_working_directory(self):
        file_handler = logging.FileHandler

        def protected_directory(filename, *args, **kwargs):
            if not Path(filename).is_absolute():
                raise PermissionError("The installation directory is read-only")
            return file_handler(filename, *args, **kwargs)

        for platform in ("win32", "darwin"):
            with self.subTest(platform=platform):
                logger = logging.getLogger(f"test.{platform}.readonly")
                try:
                    with tempfile.TemporaryDirectory() as directory:
                        with patch("src.shared.logging_setup.sys.platform", platform), \
                                patch("src.shared.logging_setup.shared_data_dir", return_value=Path(directory)), \
                                patch("logging.FileHandler", side_effect=protected_directory):
                            configure_app_logging(logger_name=logger.name, log_file="PornFetch.log")
                            logger.warning("Startup from desktop launcher")
                        for handler in logger.handlers:
                            handler.close()
                        self.assertIn("Startup from desktop launcher", (Path(directory) / "logs/PornFetch.log").read_text())
                finally:
                    for handler in logger.handlers:
                        handler.close()
                    logger.handlers.clear()

    def test_invalid_windows_console_preserves_records_in_file(self):
        class BrokenConsole:
            def write(self, message):
                raise OSError(errno.EINVAL, "Invalid argument")

            def flush(self):
                pass

        with tempfile.TemporaryDirectory() as directory:
            handler = ConsoleHandler(BrokenConsole())
            record = logging.LogRecord("test", logging.WARNING, __file__, 1, "activation diagnostic", (), None)
            with patch("src.shared.logging_setup.sys.platform", "win32"), patch(
                "src.shared.logging_setup.shared_data_dir", return_value=Path(directory)
            ):
                handler.emit(record)
                handler.emit(record)
            handler.stream.close()
            text = (Path(directory) / "logs" / "console.log").read_text()
            self.assertEqual(text.count("activation diagnostic"), 2)

    def test_reconfiguration_does_not_duplicate_console_output(self):
        logger = logging.getLogger("test.windows.console")
        try:
            with patch("src.shared.logging_setup.sys.platform", "win32"):
                configure_app_logging(logger_name=logger.name)
                configure_app_logging(logger_name=logger.name)
            self.assertEqual(len(logger.handlers), 1)
            self.assertIsInstance(logger.handlers[0], ConsoleHandler)
        finally:
            logger.handlers.clear()
