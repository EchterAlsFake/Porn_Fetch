"""
This file contains functions which are needed for the Graphical User Interface, as well as the CLI.
If you know what you do, you can change a few things here :)
"""

import logging
import platform

from base_api.base import configure_app_logging
from src.backend.config import __version__
from src.backend.error_reporting import report_exception, report_public_error

# which is also affecting all other APIs when the refresh_clients function is called
# Initialize clients globally, so that we can override them later with a new configuration from BaseCore if needed
logger = configure_app_logging(logger_name="Porn Fetch - [shared_functions]", log_file="PornFetch.log", level=logging.DEBUG)


async def aenumerate(async_iterable, start=0):
    """Async equivalent of enumerate()."""
    n = start
    async for item in async_iterable:
        yield n, item
        n += 1


async def send_to_server(message: str | dict) -> bool:
    """Compatibility wrapper for the narrow public error relay."""
    if isinstance(message, dict):
        message = str(message.get("message", ""))
    return await report_public_error(message)


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


async def handle_error_gracefully(
    self, data: dict, error_message: str | Exception,
    needs_network_log: bool = False, is_feedback: bool = False,
):
    if is_feedback:
        logger.warning("Feedback is not accepted by the error-log relay")
        return

    display_message = str(error_message)
    self.logger.error(display_message)
    if not data.get("supress_errors") is True:
        self.signals.error_signal.emit(display_message)

    if needs_network_log:
        if data.get("enable_logging", data.get("activate_logging", False)):
            error = error_message if isinstance(error_message, Exception) else RuntimeError(str(error_message))
            await report_exception(
                error,
                operation="handle application error",
                location=f"{type(self).__name__}.handle_error_gracefully",
                context=data.get("error_context"),
                enabled=True,
                version=__version__,
            )

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
