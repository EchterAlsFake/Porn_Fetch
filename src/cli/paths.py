from __future__ import annotations

import os
from pathlib import Path


APP_NAME = "Porn Fetch"
APP_AUTHOR = "EchterAlsFake"


def _platform_path(kind: str) -> Path:
    try:
        from platformdirs import user_config_path, user_data_path
        function = user_config_path if kind == "config" else user_data_path
        return Path(function(APP_NAME, APP_AUTHOR))
    except ImportError:
        if os.name == "nt":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        elif sys_platform() == "darwin":
            base = Path.home() / "Library/Application Support"
        else:
            variable = "XDG_CONFIG_HOME" if kind == "config" else "XDG_DATA_HOME"
            fallback = ".config" if kind == "config" else ".local/share"
            base = Path(os.environ.get(variable, Path.home() / fallback))
        return base / APP_NAME


def sys_platform() -> str:
    import sys
    return sys.platform


def config_dir() -> Path:
    return _platform_path("config") / "cli"


def data_dir() -> Path:
    return _platform_path("data") / "cli"


def shared_data_dir() -> Path:
    """Data shared by the GUI and CLI, notably the licensing database."""
    return _platform_path("data")

