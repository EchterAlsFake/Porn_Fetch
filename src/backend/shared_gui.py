"""Nonblocking compatibility entry points for GUI feedback."""

import weakref
from collections import deque
from collections.abc import Callable

from PySide6.QtCore import QCoreApplication, QObject, Signal
from PySide6.QtGui import QGuiApplication

_notice_handler = None
_pending_notices = deque(maxlen=50)


def set_notice_handler(handler: Callable | None) -> None:
    global _notice_handler
    _notice_handler = weakref.WeakMethod(handler) if handler is not None else None
    if handler is not None:
        while _pending_notices:
            args, kwargs = _pending_notices.popleft()
            handler(*args, **kwargs)


def ui_popup(text, title="", *, severity="info", key="", action="", details=""):
    """Publish to the active frontend on every platform, returning immediately."""
    args = (str(text or ""), str(title or ""), severity)
    kwargs = dict(key=key, action=action, details=details)
    handler = _notice_handler() if _notice_handler is not None else None
    if handler is not None:
        handler(*args, **kwargs)
    elif QGuiApplication.instance() is not None:
        _pending_notices.append((args, kwargs))
    else:
        print(f"[{title or severity}] {text}")


def reset_pornfetch():
    # TODO
    ui_popup(QCoreApplication.translate("main", "Done! Please restart.", None))


def show_error(message):
    ui_popup(text=message, severity="error")


class Signals(QObject):
    """Signals for the Download class"""

    # Progress Signal
    total_progress = Signal(int)  # Sets the current value for the progressbar
    total_progress_range = Signal(int)  # Sets the maximum for the total progressbar
    progress_add_to_tree_widget = Signal(int, int)  # Tracks the number of videos
    # loaded and processed into the tree widget
    progress_video_range = Signal(int, int)  # video_id, total
    progress_video = Signal(int, int, int)  # video_id, pos, total
    progress_remux = Signal(int, int, int)  # video_id, pos, total   <-- NEW
    download_completed = Signal(int, dict)  # video_id

    error_signal = Signal(object)
    login_result = Signal(object)

    # Animations
    start_undefined_range = Signal()  # Starts the loading animation progressbar
    stop_undefined_range = Signal()  # Stops the loading animation progressbar

    # Operations / Reportings
    internet_check = Signal(object)  # Reports if the internet checks were successful
    update_check = Signal(bool, dict)
    result = Signal(dict)  # Reports the result of the internet checks if something went wrong
    clear_tree_widget_signal = Signal()  # A signal to clear the tree widget
    text_data_to_tree_widget = Signal(int)  # Sends the text data in the form of a dictionary to the main class
    progress_send_video = Signal(
        object, object
    )  # Sends the selected video objects from the tree widget to the main class
    tree_widget_finished = Signal()
    # to download them
    url_iterators = Signal(object, object)  # Sends the processed URLs from the file to Porn Fetch


def on_checkbox_clicked(checked: bool):
    if checked:
        debug_mode_warning()


def debug_mode_warning():
    text = QCoreApplication.translate(
        "main",
        """
Debug mode is only intended for developing with Porn Fetch or for very specific error traceback. It will print a lot of things,
that are going on into your Terminal and will save VERY detailed log files that can contain sensitive information.

If you are using only the GUI this will not affect your user experience, but may slow down your system.""",
    )
    ui_popup(text)
