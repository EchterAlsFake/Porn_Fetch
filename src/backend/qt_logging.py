"""Keep Qt diagnostics while silencing one redundant Wayland focus warning."""

import re
import sys
import warnings

from PySide6.QtCore import QtMsgType, qFormatLogMessage, qInstallMessageHandler

_unfocused_disable = re.compile(
    r".*\bQWaylandTextInputv3::disableSurface\([^\n]*\) "
    r"Trying to disable 0x[0-9a-fA-F]+ but 0x0 is focused"
)
_installed = False
_previous_handler = None


def _message_handler(message_type, context, message):
    # Qt 6.12 can request disable after its text-input focus was already cleared.
    # Suppress only this warning, not other focus mismatches or critical errors.
    if (
        message_type == QtMsgType.QtWarningMsg
        and context.category == "qt.qpa.wayland.textinput"
        and _unfocused_disable.fullmatch(message)
    ):
        return

    if _previous_handler is not None:
        _previous_handler(message_type, context, message)
    else:
        # PySide6 returns None for Qt's default handler. Preserve its message
        # pattern for the terminal output rather than dropping other messages.
        # PySide6 6.12 reports the deprecated QtSystemMsg alias when formatting
        # QtCriticalMsg. Keep critical output without adding this binding warning.
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=r"Enum value 'QtMsgType\.QtSystemMsg' is marked as deprecated,.*",
                category=DeprecationWarning,
            )
            formatted = qFormatLogMessage(message_type, context, message)
        if formatted and sys.stderr is not None:
            sys.stderr.write(formatted + "\n")
            sys.stderr.flush()


def install_wayland_message_filter() -> None:
    """Install once, before creating the Linux GUI and its first native window."""
    global _installed, _previous_handler
    if sys.platform != "linux" or _installed:
        return
    _previous_handler = qInstallMessageHandler(_message_handler)
    _installed = True
