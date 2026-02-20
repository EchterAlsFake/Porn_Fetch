from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QMessageBox
from src.backend.shared_functions import ensure_config_file
from PySide6.QtCore import Signal, QObject, QCoreApplication


def ui_popup(text, title="Notice"):
    """A styled UI popup for small messages to the user."""
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)

    # Apply custom style sheet
    message_box.setStyleSheet("""
    /* Dialog surface */
    QMessageBox {
      background: #FFFFFF;
      color: #111827;
      border: 1px solid #E5E7EB;
      border-radius: 12px;
    }

    /* Main text */
    QMessageBox QLabel#qt_msgbox_label {
      color: #111827;
      font-size: 11pt;
      padding: 2px 0px;
    }

    /* Optional informative text (if you use setInformativeText) */
    QMessageBox QLabel#qt_msgbox_informativelabel {
      color: #374151;
      font-size: 10pt;
      padding-top: 4px;
    }

    /* Icon spacing */
    QMessageBox QLabel#qt_msgboxex_icon_label {
      padding-right: 14px;
    }

    /* Button row spacing */
    QMessageBox QDialogButtonBox {
      margin-top: 12px;
    }

    /* Buttons (mirror your global QPushButton rule) */
    QMessageBox QPushButton {
      border: 1px solid #D1D5DB;
      background: #FFFFFF;
      color: #111827;
      border-radius: 8px;
      padding: 6px 12px;
      min-width: 96px;
    }

    QMessageBox QPushButton:hover {
      background: #F3F4F6;
      border-color: #93C5FD;
    }

    QMessageBox QPushButton:pressed {
      background: #E5E7EB;
    }

    /* Make the default action look like your primary intent */
    QMessageBox QPushButton:default {
      background: #2563EB;
      border-color: #2563EB;
      color: white;
    }

    QMessageBox QPushButton:default:hover {
      background: #1D4ED8;
      border-color: #1D4ED8;
    }

    /* Disabled */
    QMessageBox QPushButton:disabled {
      color: #9CA3AF;
      background: #F3F4F6;
      border-color: #E5E7EB;
    }
    """)

    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()


def reset_pornfetch():
    ensure_config_file(force=True)
    ui_popup(QCoreApplication.translate("main", "Done! Please restart.", None))


def show_error(message):
    ui_popup(text=message, title="Error")


class Signals(QObject):
    """Signals for the Download class"""
    # Progress Signal
    total_progress = Signal(int) # Sets the current value for the progressbar
    total_progress_range = Signal(int) # Sets the maximum for the total progressbar
    progress_add_to_tree_widget = Signal(int, int)  # Tracks the number of videos
    # loaded and processed into the tree widget
    progress_video_range = Signal(int, int)         # video_id, total
    progress_video = Signal(int, int, int)          # video_id, pos, total
    progress_remux = Signal(int, int, int)          # video_id, pos, total   <-- NEW
    download_completed = Signal(int, dict)                # video_id

    error_signal = Signal(object)

    # Animations
    start_undefined_range = Signal()  # Starts the loading animation progressbar
    stop_undefined_range = Signal()  # Stops the loading animation progressbar

    # Operations / Reportings
    install_finished = Signal(object)  # Reports if the Porn Fetch installation was finished
    uninstall_finished = Signal(object)  # Reports if the Porn Fetch uninstallation was finished
    internet_check = Signal(object)  # Reports if the internet checks were successful
    update_check = Signal(bool, dict)
    result = Signal(dict)  # Reports the result of the internet checks if something went wrong
    clear_tree_widget_signal = Signal()  # A signal to clear the tree widget
    text_data_to_tree_widget = Signal(int)  # Sends the text data in the form of a dictionary to the main class
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
              "label_tooltip_anonymous_mode", "label_tooltip_supress_errors", "label_tooltip_network_logging",
              "tree_advanced_label_tooltip_index_videos", "label_tooltip_ssl_context"

    ]

    for label in labels:
        ui.__getattribute__(label).setPixmap(pixmap)


def on_checkbox_clicked(checked: bool):
    if checked:
        debug_mode_warning()


def debug_mode_warning():
    text = QCoreApplication.translate("main",
"""
Debug mode is only intended for developing with Porn Fetch or for very specific error traceback. It will print a lot of things,
that are going on into your Terminal and will save VERY detailed log files that can contain sensitive information.

If you are using only the GUI this will not affect your user experience, but may slow down your system.""")
    ui_popup(text)


def available_title_formatting_options():
    text = QCoreApplication.translate("main",
"""
The following options are supported:

$title (The video Title) 
$video_id
$author
$length
$tags
$publish_date
$publish_dt
$video

Notice: Not every video supports all options. If something is not supported,
it will be skipped. 

The $publish_dt option supports a literal datetime object e.g.,: 
${publish_dt:%Y-%m-%d} → 2025-10-27

Same goes for length:
${length:0.0f}min → 12min

The $video references the literal video object class in the code, which allows
you to tweak it further e.g., for PornHub you can do:
${video.author.name}

Please note, that this is intended for advanced users. I will not show general
examples or ways to use all this. Please ask ChatGPT if you need further information.
""")
    ui_popup(text)
