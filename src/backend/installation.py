import sys
import logging
import config as config

from pathlib import Path
from src.backend.errors import UnsupportedPlatform
from base_api.modules.logger import configure_app_logging
from PySide6.QtCore import QStandardPaths, QFile, QCoreApplication
from src.backend.helper_functions import (chmod_755, write_text_atomic, copy_overwrite_atomic,
                                          get_original_executable_path)


logger = configure_app_logging(logger_name="PornFetch - [Install]", level=logging.DEBUG)


class InstallPornFetch:
    def __init__(self) -> None:
        super().__init__()
        QCoreApplication.setOrganizationName(config.__org_name__) # Needed for QSettings later on
        QCoreApplication.setApplicationName(config.__app_name__) # .__.
        self.install_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppLocalDataLocation)
        # This is the directory where the configuration, license etc. is stored later on
        self.apps_dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ApplicationsLocation)
        # This is the location where the actual executable is stored
        Path(self.apps_dir).mkdir(parents=True, exist_ok=True) # Creates the storage path
        Path(self.install_dir).mkdir(parents=True, exist_ok=True) # .__.

        try:
            self.source_executable = get_original_executable_path()  # Gets source executable path

        except FileNotFoundError as e:
            logger.error(f"Could not get Source Executable Path: {e}")
            logger.warning("Using Legacy algorithm to find the source file. Please note, that this can lead to more errors!")

            filename = None

            for file in Path("").iterdir():
                if file.is_file():
                    if "PornFetch" in file.name and ".exe" in file.name or "PornFetch" in file.name and ".bin" in file.name:
                        filename = file.name

            if not filename:
                logger.critical("Legacy algorithm failed too. How did you manage to do this lol? Aborting!")
                raise FileNotFoundError(f"Could not find the source file in {self.install_dir}")

            self.source_executable = Path(filename)

    def install(self) -> bool:
        if sys.platform.startswith("linux"):
            self._install_linux_user()  # Starts Linux install
            return True

        elif sys.platform == "win32":
            self._install_windows_user()  # Starts Windows install
            return True

        else:
            raise UnsupportedPlatform(f"Unsupported platform: {sys.platform}")  # lol

    def _install_linux_user(self) -> bool:
        filename = "PornFetch.bin"

        try:
            dst_exe = Path(self.install_dir).joinpath(filename)  # Creates the final path for the destination executable
            copy_overwrite_atomic(src=self.source_executable, dst=dst_exe)  # Copies the actual file

        except RuntimeError as e:
            logger.error(f"Couldn't copy executable into the final location: {e}")
            raise

        chmod_755(dst_exe)  # Grant execute permission
        icon_dst = Path(self.install_dir).joinpath("logo.png") # Creates the destination for the logo

        if not icon_dst.exists():
            QFile.copy(":/images/graphics/logo.png", str(icon_dst))
            # We get the logo directly from the embedded resources
            # On Linux .png files are typically fine, on Windows this is handled differently

        # Write desktop file atomically
        desktop_path = Path(self.apps_dir).joinpath(f"{config.__app_id__}.desktop")
        entry = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={config.__app_name__}
Exec="{dst_exe}" %F
Icon={icon_dst}
Path={self.install_dir}
Terminal=false
Categories=Utility;
StartupNotify=true
"""
        write_text_atomic(desktop_path, entry)  # Creates the desktop entry for running PF from start menu
        logger.info(f"Installed to {self.install_dir}, desktop entry {desktop_path}")
        return True

    # ----------------------------
    # Windows (user-local install)
    # ----------------------------
    def _install_windows_user(self) -> bool:
        import win32com.client  # pywin32; Only available on Windows systems
        filename = "PornFetch.exe"

        try:
            dst_exe = Path(self.install_dir).joinpath(filename)  # Creates the final path for the destination executable
            copy_overwrite_atomic(src=self.source_executable, dst=dst_exe)  # Copies the actual file

        except RuntimeError as e:
            logger.error(f"Couldn't copy executable into the final location: {e}")
            raise


        shortcut_path = Path(self.apps_dir).joinpath(f"{config.__app_name__}.lnk")
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(shortcut_path))
        shortcut.TargetPath = str(dst_exe)
        shortcut.WorkingDirectory = str(self.install_dir)
        shortcut.IconLocation = str(dst_exe)
        shortcut.Save()

        logger.info(f"Installed to {self.install_dir}, shortcut {shortcut_path}")
        return True