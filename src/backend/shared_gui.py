import sys
import httpx
import datetime

from PySide6.QtGui import QFont, QPixmap
from src.backend.config import __version__
from PySide6.QtWidgets import QMessageBox, QMainWindow
from src.backend.shared_functions import setup_config_file
from PySide6.QtCore import Signal, QObject, QCoreApplication


def ui_popup(text, title="Notice"):
    """A styled UI popup for small messages to the user."""
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setFont(QFont("Segoe UI", 12))

    # Apply custom style sheet
    message_box.setStyleSheet("""
        QMessageBox {
            background-color: #2e2e2e;
            color: white;
            border: 2px solid #4CAF50;
            border-radius: 10px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 6px 12px;
            font-size: 10pt;
            min-width: 80px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
    """)

    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()


def handle_error_gracefully(self, data: dict, error_message: str, needs_network_log: bool= False):
    self.logger.error(error_message)
    if not data.get("supress_errors") is True:
        self.signals.error_signal.emit(error_message)

    if needs_network_log:
        if data.get("activate_logging"):
            self.logger.info(f"Logging Error: {error_message} to network server...")
            message = f"""
            An error occurred in Porn Fetch - [AddToTreeWidget]
            Time: {datetime.datetime.now()}
            Version: {__version__}
            System: {sys.platform}
            Error message: {error_message}
            """

            payload = {"message": message}
            try:
                response = httpx.post(
                url="https://echteralsfake.duckdns.org:443/report",
                json=payload,
                timeout=20)

                if response.status_code == 200:
                    self.logger.info("Successfully reported the Error!")

            except Exception as e:
                self.logger.error(f"Couldn't report the error. Maybe you don't have an IPv6 connection: {e}")
        else:
            self.logger.info("Logging is disabled. Error will NOT be reported!")


def reset_pornfetch():
    setup_config_file(force=True)
    ui_popup(QCoreApplication.translate("main", "Done! Please restart.", None))


class VideoData:
    """
    This class stores the video objects and their loaded data across Porn Fetch.
    It allows for re-fetching data if needed, update data if needed and handles caching thanks to
    a dictionary.

    (Okay, I am overhyping it a bit, but yeah, let's put that away xD)
    """

    data_objects = {}
    consistent_data = {}  # This dictionary stores other important data which will be re-used for the entire
    # run of Porn Fetch

    """
    If a video object isn't used anymore e.g., the video finished downloading or the tree widget was loaded with other
    videos, than those videos will be cleaned up in the dictionary, to be as memory and performance efficient as
    possible.
    """

    def clean_dict(self, video_titles):
        if not isinstance(video_titles, list):  # In case we only have one video title to delete
            video_titles = [video_titles]

        for video_title in video_titles:
            del self.data_objects[video_title]  # Del is faster than pop :)


class Signals(QObject):
    """Signals for the Download class"""
    # Progress Signal
    total_progress = Signal(int) # Sets the current value for the progressbar
    total_progress_range = Signal(int) # Sets the maximum for the total progressbar
    progress_add_to_tree_widget = Signal(int, int)  # Tracks the number of videos
    # loaded and processed into the tree widget

    progress_video = Signal(int, int, int)
    progress_video_range = Signal(int, int)
    progress_video_converting = Signal(int, int)

    error_signal = Signal(object)

    # Animations
    start_undefined_range = Signal()  # Starts the loading animation progressbar
    stop_undefined_range = Signal()  # Stops the loading animation progressbar

    # Operations / Reportings
    install_finished = Signal(object)  # Reports if the Porn Fetch installation was finished
    internet_check = Signal(object)  # Reports if the internet checks were successful
    update_check = Signal(bool, dict)
    result = Signal(dict)  # Reports the result of the internet checks if something went wrong
    clear_tree_widget_signal = Signal()  # A signal to clear the tree widget
    text_data_to_tree_widget = Signal(int)  # Sends the text data in the form of a dictionary to the main class
    download_completed = Signal(object)  # Reports a successfully downloaded video
    progress_send_video = Signal(object,
                                 object)  # Sends the selected video objects from the tree widget to the main class
    tree_widget_finished = Signal()
    # to download them
    url_iterators = Signal(object, object)  # Sends the processed URLs from the file to Porn Fetch


def mark_help_buttons(ui: QMainWindow, pixmap: QPixmap):
    """Applies a little notification icon to buttons with a tooltip"""
    labels = ["label_tooltip_quality", "label_tooltip_model_videos", "label_tooltip_result_limit",
              "label_tooltip_track_videos", "label_tooltip_write_metadata", "label_tooltip_skip_existing_files",
              "label_tooltip_use_directory_system", "label_tooltip_download_mode", "label_tooltip_simultaneous_downloads",
              "label_tooltip_maximum_timeout", "label_tooltip_speed_limit", "label_tooltip_pages_concurrency",
              "label_tooltip_network_delay", "label_tooltip_maximum_retries", "label_tooltip_processing_delay",
              "label_tooltip_videos_concurrency", "label_tooltip_download_workers", "label_tooltip_update_checks",
              "label_tooltip_anonymous_mode", "label_tooltip_supress_errors", "label_tooltip_network_logging"

    ]

    for label in labels:
        ui.__getattribute__(label).setPixmap(pixmap)

