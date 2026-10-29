"""Run the real GUI startup in a disposable, offline build-test environment."""
from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from PySide6.QtCore import QSettings


def run_isolated_smoke() -> int:
    previous_directory = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="pornfetch-smoke-") as temporary:
        # Configure Qt before importing the application's global SettingsManager.
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        for scope in (QSettings.Scope.UserScope, QSettings.Scope.SystemScope):
            QSettings.setPath(QSettings.Format.IniFormat, scope, temporary)
        os.environ.pop("PORN_FETCH_TEST_ENV", None)
        os.environ["XDG_CACHE_HOME"] = str(Path(temporary) / "cache")
        os.environ.setdefault("QT_QUICK_BACKEND", "software")
        os.chdir(temporary)
        try:
            from src.backend.application import main

            main()
            return 0
        finally:
            # Windows cannot remove the temporary directory while log files are open.
            logging.shutdown()
            os.chdir(previous_directory)
