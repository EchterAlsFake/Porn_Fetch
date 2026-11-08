"""Keep desktop diagnostics writable independently of the launch directory."""
from __future__ import annotations

import errno
import logging
import os
import sys
from pathlib import Path

from base_api.modules.logger import configure_app_logging as _configure_app_logging

from src.shared.paths import shared_data_dir


def log_file_path(filename: str) -> str:
    """Keep desktop logs out of protected application/working folders."""
    path = Path(filename)
    directory = os.environ.get("PORN_FETCH_LOG_DIR")
    if not path.is_absolute() and (directory or sys.platform in {"win32", "darwin"}):
        path = (Path(directory).resolve() if directory else shared_data_dir() / "logs") / path
        path.parent.mkdir(parents=True, exist_ok=True)
    return str(path)


class ConsoleHandler(logging.StreamHandler):
    def handleError(self, record: logging.LogRecord) -> None:
        error = sys.exc_info()[1]
        if sys.platform == "win32" and isinstance(error, OSError) and error.errno == errno.EINVAL:
            # A detached/invalid console can still look writable to Python.
            # Retain its output in a persistent file instead of repeatedly failing.
            self.stream = Path(log_file_path("console.log")).open("a", encoding="utf-8")
            self.emit(record)
            return
        super().handleError(record)


def configure_app_logging(logger_name: str | None = None, log_file: str | None = None, **kwargs) -> logging.Logger:
    logger = _configure_app_logging(logger_name=logger_name,
                                    log_file=log_file_path(log_file) if log_file else None, **kwargs)
    if sys.platform == "win32":
        for target in (logger, logging.getLogger()):
            existing = next((handler for handler in target.handlers if isinstance(handler, ConsoleHandler)), None)
            for handler in tuple(target.handlers):
                if type(handler) is logging.StreamHandler:
                    if existing is not None:
                        target.removeHandler(handler)
                        continue
                    replacement = ConsoleHandler(handler.stream)
                    replacement.setFormatter(handler.formatter)
                    replacement.setLevel(handler.level)
                    for filter_ in handler.filters:
                        replacement.addFilter(filter_)
                    target.removeHandler(handler)
                    target.addHandler(replacement)
                    existing = replacement
    return logger
