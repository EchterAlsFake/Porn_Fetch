import os
import sys
import tempfile
import subprocess
import logging
import config as config

from pathlib import Path

from backend.errors import UnsupportedPlatform
from src.backend.helper_functions import safe_rmtree
from base_api.modules.logger import configure_app_logging
from PySide6.QtCore import QStandardPaths, QCoreApplication


logger = configure_app_logging(logger_name="PornFetch - [Uninstall]", level=logging.DEBUG)


class UninstallPornFetch:
    """
    Uninstalls the *user-local installed* version:
      - Linux: removes ~/.local/share/applications/<app_id>.desktop
               removes AppLocalDataLocation payload folder (binary/icon)
      - Windows: removes Start Menu shortcut
                 removes AppLocalDataLocation payload folder
                 uses a .bat helper to delete after app exit (because Windows locks running exe)
    """

    def __init__(self) -> None:
        self.app_id = config.__app_id__
        self.app_name = config.__app_name__
        self.org_name = config.__org_name__

    def uninstall(self) -> bool:
        # We can also set app name and org name for paths to match correctly
        QCoreApplication.setOrganizationName(self.org_name)
        QCoreApplication.setApplicationName(self.app_name)

        if sys.platform.startswith("linux"):
            self._uninstall_linux_user()
            return True

        elif sys.platform == "win32":
            self._uninstall_windows_user()
            return True

        else:
            raise UnsupportedPlatform(f"Unsupported platform: {sys.platform}")

    def _uninstall_linux_user(self) -> None:
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        apps_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)

        if not apps_dir:
            apps_dir = os.path.expanduser("~/.local/share/applications")

        desktop_path = Path(apps_dir).joinpath(f"{self.app_id}.desktop")

        # Remove desktop entry
        if desktop_path.exists():
            desktop_path.unlink()

        # Remove payload files (best effort)
        if install_dir and os.path.isdir(install_dir):
            safe_rmtree(install_dir)

        logger.info(f"Uninstalled (Linux). Removed: {desktop_path} and {install_dir}")
        return True

    def _uninstall_windows_user(self) -> None:
        install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        start_menu_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)

        if not start_menu_dir:
            start_menu_dir = os.path.join(os.getenv("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")

        shortcut_path = Path(start_menu_dir).joinpath(f"{self.app_name}.lnk")

        # Remove shortcut now (usually possible even while app runs)
        if shortcut_path.exists():
            shortcut_path.unlink()

        # Now remove install_dir.
        # On Windows you typically cannot delete the running exe, so we spawn a helper bat
        # that waits for this process to exit, then deletes the folder.
        if install_dir and os.path.isdir(install_dir):
            self._spawn_windows_cleanup_bat(
                pid=os.getpid(),
                install_dir=install_dir,
                shortcut_path=str(shortcut_path),
            )

        logger.info(f"Uninstall scheduled (Windows). Shortcut removed: {shortcut_path}, install_dir: {install_dir}")
        return True

    def _spawn_windows_cleanup_bat(self, pid: int, install_dir: str, shortcut_path: str) -> None:
        """
        Creates and runs a .bat that waits until PID exits, then deletes install_dir.
        The .bat deletes itself at the end.
        """
        bat_path = Path(tempfile.gettempdir()).joinpath(f"{self.app_id}_uninstall_cleanup.bat")

        # Use rmdir /s /q for full folder wipe
        # "tasklist /FI" loop waits until PID is gone
        script = rf"""@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Wait for the app process to exit
:loop
tasklist /FI "PID eq {pid}" 2>NUL | find /I "{pid}" >NUL
if "%ERRORLEVEL%"=="0" (
    timeout /t 1 /nobreak >NUL
    goto loop
)

REM Remove shortcut (best effort)
del /f /q "{shortcut_path}" >NUL 2>&1

REM Remove install folder
rmdir /s /q "{install_dir}" >NUL 2>&1

REM Self-delete
del /f /q "%~f0" >NUL 2>&1
endlocal
"""

        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(script)

        # Launch hidden
        try:
            creationflags = subprocess.CREATE_NO_WINDOW
        except AttributeError:
            creationflags = 0

        subprocess.Popen(
            ["cmd.exe", "/c", str(bat_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags,
            close_fds=True,
        )