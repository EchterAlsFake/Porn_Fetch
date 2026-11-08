"""Run the real GUI startup in a disposable, offline build-test environment."""
from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from PySide6.QtCore import QSettings


def run_isolated_smoke() -> int:
    previous_log_directory = os.environ.get("PORN_FETCH_LOG_DIR")
    with tempfile.TemporaryDirectory(prefix="pornfetch-smoke-") as temporary:
        # Configure Qt before importing the application's global SettingsManager.
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        for scope in (QSettings.Scope.UserScope, QSettings.Scope.SystemScope):
            QSettings.setPath(QSettings.Format.IniFormat, scope, temporary)
        os.environ.pop("PORN_FETCH_TEST_ENV", None)
        os.environ["XDG_CACHE_HOME"] = str(Path(temporary) / "cache")
        os.environ["PORN_FETCH_LOG_DIR"] = str(Path(temporary) / "logs")
        os.environ.setdefault("QT_QUICK_BACKEND", "software")
        try:
            from src.backend.application import main

            main()
            return 0
        finally:
            # Windows cannot remove the temporary directory while log files are open.
            logging.shutdown()
            if previous_log_directory is None:
                os.environ.pop("PORN_FETCH_LOG_DIR", None)
            else:
                os.environ["PORN_FETCH_LOG_DIR"] = previous_log_directory
