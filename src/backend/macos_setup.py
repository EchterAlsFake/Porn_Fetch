"""
This basically detects if the application runs from macOS and if it's inside the /Volumes path. If yes, it means
that it is being run from a macOS container. It will try to automatically move to the applications folder...
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox

app_path = Path(sys.argv[0]).resolve()


def _is_running_from_dmg(path: Path) -> bool:
    # /Volumes is the mountpoint for .dmg files
    return str(path).startswith("/Volumes")


def _find_app_bundle(path: Path) -> Path:
    """
    Walk up until we find the .app bundle root.
    E.g. /Volumes/Porn Fetch/Porn Fetch.app/Contents/MacOS/Porn Fetch
         --> /Volumes/Porn Fetch/Porn Fetch.app
    """
    for parent in path.parents:
        if parent.suffix == ".app":
            return parent
    return path


def _install_and_relaunch_mac(app_exec_path: Path) -> bool:
    """
    Copy the .app bundle to ~/Applications and relaunch it.
    Returns True if we successfully launched the installed copy.
    """
    import shutil
    import subprocess
    from pathlib import Path

    app_bundle = _find_app_bundle(app_exec_path)
    app_name = app_bundle.name   # e.g. "Porn Fetch.app"

    user_apps = Path.home() / "Applications"
    try:
        user_apps.mkdir(exist_ok=True)
    except Exception:
        # If this somehow fails, give up
        return False

    dest_app = user_apps / app_name

    # If we already installed it before, just open that one
    if dest_app.exists():
        subprocess.Popen(["open", "-n", str(dest_app)])
        return True

    try:
        # Copy the whole .app bundle
        shutil.copytree(app_bundle, dest_app, symlinks=True)
    except Exception:
        # Could not copy for some reason (permissions etc.)
        return False

    # Launch the installed copy
    subprocess.Popen(["open", "-n", str(dest_app)])
    return True


def macos_setup():

    if sys.platform == "darwin" and _is_running_from_dmg(app_path):
        # Small confirmation dialog instead of manual drag & drop
        app = QApplication(sys.argv)
        reply = QMessageBox.question(
            None,
            "Install Porn Fetch",
            (
                "Porn Fetch is running from a read-only disk image.\n\n"
                "I can automatically copy it to your Applications folder and "
                "relaunch it from there (so it can save its settings).\n\n"
                "Do you want me to do that now?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )

        if reply == QMessageBox.Yes:
            if _install_and_relaunch_mac(app_path):
                # New instance is launching; this one can exit
                sys.exit(0)
            else:
                QMessageBox.critical(
                    None,
                    "Install failed",
                    "I couldn't copy Porn Fetch to your Applications folder.\n"
                    "Please move it manually."
                )
                sys.exit(1)
        else:
            # User declined: you can either exit or fall back to your old notice
            sys.exit(0)