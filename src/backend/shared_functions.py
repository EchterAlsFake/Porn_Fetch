"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import sys
import logging
import datetime
import platform
import traceback

from curl_cffi import post
from base_api.base import configure_app_logging
from src.backend.config import __version__

# which is also affecting all other APIs when the refresh_clients function is called
# Initialize clients globally, so that we can override them later with a new configuration from BaseCore if needed
logger = configure_app_logging(logger_name="Porn Fetch - [shared_functions]", log_file="PornFetch.log", level=logging.DEBUG)


async def aenumerate(async_iterable, start=0):
    """Async equivalent of enumerate()."""
    n = start
    async for item in async_iterable:
        yield n, item
        n += 1


def send_to_server(message: dict):
    try:
        response = post(
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



"""
These are simple helper functions to return the correct data type that we expect, because the configuration
stores everything as strings, so we do a simple conversion. May look unnecessary, but when doing it a lot 
especially in CLI / GUI when it comes to loading and saving user settings, this is quite useful.
"""


def get_os_and_arch():
    """
    Detects if the system is Windows/Linux and x64/ARM64.
    Returns a string identifier or 'unsupported' if no match is found.
    """
    os_name = platform.system().lower()
    machine = platform.machine().lower()

    if os_name == 'windows':
        # Windows identifies 64-bit x86 as 'amd64'
        if machine in ['amd64', 'x86_64']:
            return "windows_x64"
        # Windows identifies ARM64 as 'arm64'
        elif machine in ['arm64', 'aarch64']:
            return "windows_arm64"

    elif os_name == 'linux':
        # Linux identifies 64-bit x86 as 'x86_64'
        if machine in ['x86_64', 'amd64']:
            return "linux_x64"
        # Linux identifies ARM64 as 'aarch64'
        elif machine in ['aarch64', 'arm64']:
            return "linux_arm64"

    # Fallback for Macs (Darwin), 32-bit systems, etc.
    return f"unsupported ({os_name}_{machine})"