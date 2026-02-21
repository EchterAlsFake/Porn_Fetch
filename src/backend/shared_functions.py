"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import os
import sys
import httpx
import logging
import datetime
import traceback

from typing import Any
from pathlib import Path
from configparser import ConfigParser
from base_api.base import setup_logger
from src.backend.config import __version__

# which is also affecting all other APIs when the refresh_clients function is called
# Initialize clients globally, so that we can override them later with a new configuration from BaseCore if needed

logger = setup_logger(name="Porn Fetch - [shared_functions]", log_file="PornFetch.log", level=logging.DEBUG)


def send_to_server(message: dict):
    try:
        response = httpx.post(
            url="https://echteralsfake.me/report",
            json=message,
            timeout=20)

        if response.status_code == 200:
            return(f"The error / feedback was successfully reported! Thanks :)")

        elif response.status_code == 500:
            return("An internal server error occurred. I am probably already fixing this.")

    except Exception:
        error = traceback.format_exc()
        return(f"Couldn't report to server due to error -->: {error}")


def build_quality_options(heights: list[int], include_auto=True):
    """
    Returns list of (label, value) where value is what you pass to download():
      - int heights: 720
      - auto labels: "best"/"half"/"worst"
    """
    opts: list[tuple[str, str | int]] = []
    if include_auto:
        opts += [("Worst", "worst"), ("Half", "half"), ("Best", "best")]
    for h in heights:
        opts.append((f"{h}p", h))
    return opts


def handle_error_gracefully(self, data: dict, error_message: str | dict, needs_network_log: bool= False, is_feedback=False):
    if is_feedback:
        send_to_server(message=error_message)
        return

    self.logger.error(error_message)
    if not data.get("supress_errors") is True:
        self.signals.error_signal.emit(error_message)

    if needs_network_log:
        if data.get("activate_logging"):
            self.logger.info(f"Logging Error: {error_message} to network server...")
            message = f"""
            An error occurred in Porn Fetch!
            Time: {datetime.datetime.now()}
            Version: {__version__}
            System: {sys.platform}
            Error message: {error_message}
            """
            payload = {"message": message}
            send_to_server(message=payload)

        else:
            self.logger.info("Logging is disabled. Error will NOT be reported!")


CONFIG_PATH = Path("config.ini")
DEFAULTS: dict[str, dict[str, Any]] = {
    "Misc": {
        "app_name": "none",
        "debug_mode": False,
        "first_run_gui": True,
        "license_accepted": False,
        "install_type": "unknown",
        "update_checks": False,
        "anonymous_mode": False,
        "disclaimer_shown": False,
        "network_logging": False,
        "first_run_cli": True,
        "downloaded_videos": 0,
        "failed_dialog": False,
        "notice_shown": False,
        "android_warning_shown": False,
        "supress_errors": False,
        "use_truststore": True
        # add this (important for migrations)
    },
    "Performance": {
        "semaphore": 1,
        "videos_concurrency": 10,
        "pages_concurrency": 2,
        "download_workers": 20,
        "timeout": 10,
        "retries": 4,
        "speed_limit": 0,
        "processing_delay": 0,
        "network_delay": 0,
    },
    "Video": {
        "quality": 6,
        "model_videos": 0,
        "result_limit": 50,
        "output_path": "./",
        "video_id_as_filename": False,
        "write_metadata": True,
        "skip_existing_files": True,
        "track_videos": False,
        "database_path": "./downloads.db",
        "directory_system": False,
    },
    "UI": {
        "language": 0,
        "font_size": 10,
        "theme": 0,
    },
}


def _to_ini_value(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def _atomic_write(cp: ConfigParser, path: Path) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        cp.write(f)
    os.replace(tmp, path)


def ensure_config_file(path: Path = CONFIG_PATH, force: bool = False) -> ConfigParser:
    """
    Loads config.ini and *merges defaults*:
    - existing values are kept
    - missing sections/keys are added
    - file is only written if something was missing OR file didn't exist

    If force is true, Porn Fetch will reset to default, but that only happens when you call it in the UI explicitly.
    """
    existing = ConfigParser(interpolation=None)
    if path.exists():
        existing.read(path, encoding="utf-8")

    merged = ConfigParser(interpolation=None)
    # seed defaults
    merged.read_dict({s: {k: _to_ini_value(v) for k, v in opts.items()} for s, opts in DEFAULTS.items()})
    # overlay user config (keeps user values)
    if path.exists():
        merged.read(path, encoding="utf-8")

    changed = not path.exists()

    # detect missing keys/sections (so we know whether to write back)
    for section, opts in DEFAULTS.items():
        if not existing.has_section(section) or force:
            changed = True
        for key in opts.keys():
            if not existing.has_option(section, key):
                changed = True

    if changed:
        _atomic_write(merged, path)

    return merged

"""
These are simple helper functions to return the correct data type that we expect, because the configuration
stores everything as strings, so we do a simple conversion. May look unnecessary, but when doing it a lot 
especially in CLI / GUI when it comes to loading and saving user settings, this is quite useful.
"""

def get_bool(cp: ConfigParser, section: str, key: str) -> bool:
    return cp.getboolean(section, key)

def get_int(cp: ConfigParser, section: str, key: str) -> int:
    return cp.getint(section, key)

def get_str(cp: ConfigParser, section: str, key: str) -> str:
    return cp.get(section, key)
