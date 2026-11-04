import os
import sys
import shutil

from pathlib import Path
from src.shared.logging_setup import configure_app_logging

logger = configure_app_logging(logger_name="Helper Functions")


def get_original_executable_path() -> Path:
    """Returns the true source executable path, ignoring onefile extraction paths."""
    # 1. Nuitka onefile
    try:
        import __compiled__
        orig = getattr(__compiled__, "original_argv0", None)
        if orig and Path(orig).exists():
            return Path(orig).resolve()
    except ImportError:
        pass

    # 2. Linux AppImage
    if appimage := os.environ.get("APPIMAGE"):
        if Path(appimage).exists():
            return Path(appimage).resolve()

    # 3. Fallback
    if sys.argv and Path(sys.argv[0]).exists():
        return Path(sys.argv[0]).resolve()

    raise FileNotFoundError("Could not determine original executable location.")


def safe_rmtree(path: str):
    """Delete a directory tree if it exists (ignore missing)."""
    try:
        if path and os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False)
            logger.info(f"Deleted directory: {path}")
    except FileNotFoundError:
        pass


