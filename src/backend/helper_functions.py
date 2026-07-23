import os
import sys
import shutil
import traceback

from pathlib import Path
from base_api.base import configure_app_logging
from PySide6.QtCore import QIODevice, QSaveFile, QStandardPaths


logger = configure_app_logging(logger_name="Helper Functions")


def make_debug_log(e: Exception, video_url: str, user_message: str, function: str) -> str:
    return f"""
    {user_message}

    Debug for GitHub
    --{type(e).__name__}: [{function}] -> {video_url}
    DEBUG: {traceback.format_exc()}
    System: {sys.platform}
    """

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


def copy_overwrite_atomic(src: Path, dst: Path) -> None:
    """
    Copies a file to a temp destination first, then atomically replaces the target.
    Prevents corrupting the application executable if interrupted mid-copy.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(f"{dst}.tmp")
    old = Path(f"{dst}.old")

    tmp.unlink(missing_ok=True)
    old.unlink(missing_ok=True)

    shutil.copy2(src, tmp)  # Full binary + metadata copy

    # On Windows, replacing a running executable fails with PermissionError.
    # However, renaming a running executable is permitted.
    if sys.platform == "win32" and dst.exists():
        try:
            dst.rename(old)
        except OSError as e:
            logger.warning(f"Failed to rename existing executable: {e}")

    tmp.replace(dst)  # Atomic swap on POSIX & modern Windows

    # Verification check
    if src.stat().st_size != dst.stat().st_size:
        raise RuntimeError(f"Copy verification failed: {src} -> {dst}")


def write_text_atomic(path: Path | str, text: str) -> None:
    """Uses Qt's QSaveFile to write text safely, preventing file corruption on crash."""
    f = QSaveFile(str(path))
    if not f.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
        raise RuntimeError(f"Could not open for writing: {path}")

    f.write(text.encode("utf-8"))
    if not f.commit():
        raise RuntimeError(f"Could not commit save to: {path}")


def chmod_755(path: Path | str) -> None:
    """Grant rwxr-xr-x permissions (useful for Linux binaries/AppImages)."""
    Path(path).chmod(0o755)
    logger.debug(f"Applied 755 permissions to: {path}")


def default_license_path() -> Path:
    cfg = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    return Path(cfg) / "porn_fetch.license"


def safe_rmtree(path: str):
    """Delete a directory tree if it exists (ignore missing)."""
    try:
        if path and os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False)
            logger.info(f"Deleted directory: {path}")
    except FileNotFoundError:
        pass
