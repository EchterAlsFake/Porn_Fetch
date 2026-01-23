import os
import sys
import shutil
import platform

from pathlib import Path
from base_api.base import setup_logger
from PySide6.QtCore import QFile, QFileDevice, QIODevice, QDir, QSaveFile, QStandardPaths


logger = setup_logger(name=".ff")
# TODO

def get_original_executable_path() -> str:
    """
    This function is needed because if we use Qt's native version to get the file source, it gives us the issue,
    that Qt thinks the real file, so our execution file would be the extracted one inside the Nuitka container inside
    the /tmp directory.

    So, when I then compile the file, we don't compile the real file, but the extracted one which will give a segmentation
    fault because it misses the bootstrapper.
    """

    # 1) Nuitka: best source for onefile
    try:
        import __compiled__  # provided by Nuitka
        orig = getattr(__compiled__, "original_argv0", None)
        if orig and os.path.exists(orig):
            return os.path.realpath(orig)
    except Exception:
        pass

    # 2) AppImage-style runtime env var (often set in onefile on Linux)
    appimage = os.environ.get("APPIMAGE")
    if appimage and os.path.exists(appimage):
        return os.path.realpath(appimage)

    # 3) Fallback: argv[0] (often the real onefile path)
    if sys.argv and os.path.exists(sys.argv[0]):
        return os.path.realpath(sys.argv[0])


def copy_overwrite_atomic(src: str, dst: str):
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    tmp = dst + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)

    shutil.copy2(src, tmp)  # full binary-safe copy
    os.replace(tmp, dst)  # atomic swap

    # sanity check
    if os.path.getsize(src) != os.path.getsize(dst):
        raise RuntimeError(
            f"Copy verification failed: {src} ({os.path.getsize(src)}) != {dst} ({os.path.getsize(dst)})"
        )


def mkpath(path: str) -> None:
    if not path:
        raise RuntimeError("Got empty path from QStandardPaths.")
    if not QDir().mkpath(path):
        raise RuntimeError(f"Failed to create directory: {path}")


def move_or_copy(src: str, dst: str) -> None:
    # Prefer atomic-ish rename, but fall back to copy+remove (cross-device, etc.)
    if QFile.exists(dst):
        QFile.remove(dst)

    if QFile.rename(src, dst):
        return

    if not QFile.copy(src, dst):
        raise RuntimeError(f"Could not move/copy '{src}' -> '{dst}'")

    # Only remove original after successful copy
    QFile.remove(src)


def write_text_atomic(path: str, text: str) -> None:
    f = QSaveFile(path)
    if not f.open(QIODevice.OpenModeFlag.WriteOnly | QIODevice.OpenModeFlag.Text):
        raise RuntimeError(f"Could not open for writing: {path}")
    f.write(text.encode("utf-8"))
    if not f.commit():
        raise RuntimeError(f"Could not commit: {path}")


def chmod_755(path: str) -> None:
    perms = (
        QFileDevice.Permission.ReadOwner | QFileDevice.Permission.WriteOwner | QFileDevice.Permission.ExeOwner |
        QFileDevice.Permission.ReadGroup | QFileDevice.Permission.ExeGroup |
        QFileDevice.Permission.ReadOther | QFileDevice.Permission.ExeOther
    )
    QFile.setPermissions(path, perms)


def default_license_path() -> Path:
    cfg = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation)
    return Path(cfg) / "porn_fetch.license"


def safe_unlink(path: str):
    """Delete a file if it exists (ignore missing)."""
    try:
        if path and os.path.isfile(path):
            os.remove(path)
    except FileNotFoundError:
        pass

def safe_rmtree(path: str):
    """Delete a directory tree if it exists (ignore missing)."""
    try:
        if path and os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False)
    except FileNotFoundError:
        pass


def normalized_arch() -> str:
    m = platform.machine().lower()
    if m in ("x86_64", "amd64"):
        return "x86_64"
    if m in ("arm64", "aarch64"):
        return "arm64"

    else:
        logger.warning(f"Couldn't normalize platform: {m}, please report this")
        return m
