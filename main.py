"""
Copyright (C) 2023-2026 Johannes Habel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact:

E-Mail: EchterAlsFake@proton.me
Discord: echteralsfake (faster response)
"""
import os
import sys
import tempfile

# Pre-Load PySide6 to show a loading splashscreen
from PySide6.QtWidgets import QApplication

from backend.clients import AllowedVideoType

app = QApplication(sys.argv)

# macOS Setup...
if sys.platform == "darwin":
    from src.backend.macos_setup import macos_setup
    from src.backend.update_service import SparkleUpdater
    macos_setup()
    # Handles Sparkle Updates + macOS Installation

# Necessary imports for splashscreen
import src.frontend.UI.resources # This may not seem to be used, but it needs to be imported!
from PySide6.QtGui import QPixmap
from src.frontend.UI.splashscreen import ModernSplashScreen

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Fusion"
splash_pixmap = QPixmap(":/images/graphics/splashscreen.png")
splash = ModernSplashScreen(splash_pixmap)
splash.show() # Starts showing the actual Splash Screen
app.processEvents()

if "NUITKA_ONEFILE_PARENT" in os.environ:
    splash_filename = os.path.join(
        tempfile.gettempdir(),
        f"onefile_{int(os.environ['NUITKA_ONEFILE_PARENT'])}_splash_feedback.tmp"
    )
    if os.path.exists(splash_filename):
        os.unlink(splash_filename)
        # Stops the Nuitka Splash Screen

splash.showMessage("Importing (General).")
app.processEvents()
# General imports
import time
import uuid
import random
import logging
import asyncio
import argparse
import markdown
import traceback
import threading
import webbrowser

from pathlib import Path
from threading import Event, Lock
from itertools import islice, chain
from typing import Iterable, AsyncGenerator



splash.showMessage("Importing (PySide6).")
app.processEvents()
# Qt / PySide6 related imports
import PySide6.QtAsyncio as QtAsyncio # Needed because porn fetch's network backend is now async since v3.9
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtGui import QIcon, QFontDatabase, QPixmap, QShortcut, QKeySequence
from PySide6.QtCore import (QTextStream, QRunnable, QLocale, QSize, QUrl, Signal, QFile, Slot,
                            QTranslator, QCoreApplication, QStandardPaths, QObject, Qt)
from PySide6.QtWidgets import (QTreeWidgetItem, QButtonGroup, QFileDialog, QHeaderView, QSizePolicy, QLayout,
                               QInputDialog, QMainWindow, QProgressBar, QComboBox, QWidget, QPushButton,
                                QHBoxLayout)


splash.showMessage("Importing (Backend).")
app.processEvents()
# Backend imports
from src.backend import clients # Singleton instance for the client objects (really important)
import src.backend.config as config
from src.backend.check_license import LicenseManager
import src.backend.shared_functions as shared_functions
from src.backend.database import save_video_metadata, init_db
from src.backend.config import (__version__, PUBLIC_KEY_B64, IS_SOURCE_RUN, TEMP_DIRECTORY,
                                TEMP_DIRECTORY_STATES, TEMP_DIRECTORY_SEGMENTS)
from src.backend.shared_functions import ensure_config_file, handle_error_gracefully
from src.backend.shared_gui import (ui_popup, reset_pornfetch, mark_help_buttons, Signals,
                                    available_title_formatting_options, on_checkbox_clicked)
from src.backend.helper_functions import default_license_path, safe_rmtree

from src.backend.installation import InstallPornFetch
from src.backend.uninstallation import UninstallPornFetch
from src.backend.errors import (UnsupportedPlatform, AppDownloadFailed, AppNetworkError, AppNotFoundError,
                                AppBotBlocked, safe_api_call)
from src.backend.download_manager import DownloadManager, VideoObject

splash.showMessage("Importing (Frontend).")
app.processEvents()
# Frontend imports
from src.frontend.UI.ui_form_main_window import Ui_PornFetch_UI
from src.frontend.UI.custom_combo_box import ComboPopupFitter, make_quality_combobox
from src.frontend.UI.theme import (apply_theme, apply_theme_lsd, apply_theme_light, mark, install_focus_outline,
                                   pretty_combo)
from src.frontend.translations.strings import (TRANSLATE_MAIN, TRANSLATE_PAGE_DOWNLOAD, TRANSLATE_PAGE_LOGIN,
                                              TRANSLATE_PAGE_SETTINGS, TRANSLATE_ERRORS)


splash.showMessage("Importing (APIs).")
app.processEvents()

# Errors from different APIs
from base_api.modules.errors import ProxySSLError, InvalidProxy
from pornhub_api.modules.errors import VideoDisabled, GifPendingReview


splash.showMessage("Importing (AV - FFMPEG).")
app.processEvents()

try:
    from av import open as av_open  # Don't ask
    from av.audio.resampler import AudioResampler  # Don't ask
    FORCE_DISABLE_AV = False

except Exception:
    FORCE_DISABLE_AV = True


FORCE_PORTABLE_RUN: bool = False # Holds a value for argparse later (see main function)
total_segments: int = 0 # Total segments kept in a queue (for total progress tracking)
downloaded_segments: int = 0 # Amount of segments that have been downloaded (for total progress tracking)
total_downloaded_videos: int = 0  # All videos that actually successfully downloaded
session_urls: list = []  # This list saves all URLs used in the current session. Used for the URL export function (CTRL + E)
stop_flag: threading.Event = Event() # Stops loading videos into the tree widget (does not stop any downloads)
_download_lock: threading.Lock = Lock() # I actually don't really know why this is here
logger = shared_functions.configure_app_logging(logger_name="Porn Fetch - [MAIN]", log_file="PornFetch.log", level=logging.DEBUG)
license_storage_path: str = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation), "pornfetch.license")
last_index = 0 # Tracks the last index of the tree widget in case the user does not have auto-clear enabled
x: bool = False # Don't ask (this is a secret ;)


class ProcessVideos:
    """
    This class is responsible for processing the videos in the background, loading the data, adjusting paths and
    handling errors
    """

    def __init__(self, iterator: AsyncGenerator, custom_path_options: str, max_attempts: int,
                 download_manager: DownloadManager, reverse_videos: bool, stop_flag: asyncio.Event,
                 use_directory_system: bool, output_path: Path) -> None:
        self.iterator = iterator
        self.custom_path_options = custom_path_options
        self.max_attempts = max_attempts
        self.download_manager = download_manager
        self.reverse_videos = reverse_videos
        self.stop_flag = stop_flag
        self.use_directory_system = use_directory_system
        self.output_path = output_path

    @staticmethod
    async def reverse_iterator(iterator: AsyncGenerator):
        videos = []
        async for video in iterator:
            videos.append(video) # This is very stupid, please don't use this „feature"!

        return videos.reverse()

    @staticmethod
    async def process_single_video(video_object: str | AllowedVideoType) -> tuple[AllowedVideoType, dict]:
        video = await clients.get_video(video_object)
        video_attributes = await clients.load_video_attributes(video=video)
        return video, video_attributes

    def create_output_path(self, author: str) -> Path:
        possible_options = ["$title", "$author", "$length", "$video_id", "$publish_date"]

        base_path = self.output_path # This is just the directory where the video will be stored to

        # Now there come the modifications...
        if self.use_directory_system:
            base_path.joinpath(author)

        for option in self.custom_path_options:







    async def start_processing(self):
        global last_index
        logger.info("Starting Processing of Iterator!")

        if self.reverse_videos:
            self.iterator = self.reverse_iterator(self.iterator)



        async for idx, video in shared_functions.aenumerate(self.iterator):
            for attempt in range(self.max_attempts):
                try:
                    logger.debug(f"Current Index: {idx} | Attempt: {attempt}")
                    video, video_attributes = await safe_api_call(self.process_single_video, video)
                    identifier = uuid.uuid4().hex
                    logger.info(f"Successfully received Video! [Identifier ->: {identifier}]")

                    assert isinstance(video_attributes, dict)
                    title = video_attributes.get("title")
                    author = video_attributes.get("author")
                    length = video_attributes.get("length")
                    tags = video_attributes.get("tags")
                    thumbnail_url = video_attributes.get("thumbnail")
                    video_id = video_attributes.get("video_id")
                    publish_date = video_attributes.get("publish_date")
                    qualities = video_attributes.get("qualities")

                    video_object = VideoObject(
                        identifier=identifier,
                        title=title, # Title is already checked and stripped

                        status="Pending",
                    )

                    self.download_manager.add_video(video_object)
                    last_index += 1

                except AppBotBlocked:
                    logger.error("Bot Protection detected")
                    break # Retrying won't help against bot protections

                except AppNetworkError:
                    logger.error("Network error")
                    continue # Maybe it solves by itself ;)

                except AppNotFoundError:
                    logger.error("Not found")
                    break # If the resource is not there, it won't magically appear lmao











class PornFetch(QMainWindow):
    COL_DOWNLOAD = 0
    COL_TITLE = 1
    COL_AUTHOR = 2
    COL_LENGTH = 3
    COL_QUALITY = 4
    COL_STOP = 5
    COL_PROGRESS = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_update_time = time.time()
        self.signals = Signals()
        self.signals.error_signal.connect(ui_popup)
        self.download_manager = DownloadManager() # Used to track all videos
        self.download_manager.video_added.connect(self.add_to_tree_widget_signal)


        self.ui = Ui_PornFetch_UI()
        self.ui.setupUi(self)
        self.logger = shared_functions.configure_app_logging(logger_name="Porn Fetch - [PornFetch]", log_file="PornFetch.log", level=logging.DEBUG)

        self.last_index = 0  # Keeps track of the last index of videos added to the tree widget
        self._anonymous_mode = False
        self.ensure_temp()
        self._row = {} # Video ID -> dict of widgets + state
        self.maps()
        self.load_style()
        self._setup_modern_tabs()
        self.load_strings()
        self.license = License(self.ui, self.initialize_pornfetch)
        self.disclaimer = Disclaimer(self.ui, self.initialize_pornfetch)
        self.ui.vbox_info.addWidget(PornFetchInfoWidget())
        self.license_manager = LicenseManager(storage_path=default_license_path(), public_key_b64=PUBLIC_KEY_B64)
        self.setup_license_restrictions()

        """
                             ! INDEX LIST !

        0) Main application (downloading, login, tree widget etc.)
        :: Index list for main application ::
        - 0: Download
        - 1: Login
        - 2: Tools (removed)
        - 3: Progressbars
        - 4: Range selector
        
        1) Settings
        2) Credits
        3) License
        4) Keyboard Shortcuts
        5) Install Dialog
        6) Supported websites
        7) Donation Nag        
        8) Disclaimer text
        9) One-Time Information
        10) Batch Feature (Not implemented yet)
        This may look a little bit confusing, but once you understand it, it makes sense, trust me :)
        """

        self.default_max_height = self.ui.main_stacked_widget_top.maximumHeight()
        self.button_connections()  # Connects the buttons to their functions
        self.shortcuts()  # Activates the keyboard shortcuts
        self.logger.debug("Startup: [3/5] Initialized the User Interface")
        self.load_user_settings()  # Loads the user settings and applies selected values to the UI
        self.logger.debug("Startup: [4/5] Loaded the user settings")
        max_concurrent = int(video_data.consistent_data.get("semaphore", 1))
        self.download_scheduler = DownloadScheduler(max_concurrent, self)
        self.download_scheduler.worker_started.connect(self._wire_worker_signals)
        self.progress_widgets = {}  # video_id -> {'label': QLabel, 'progressbar': QProgressBar}

        if video_data.consistent_data.get("update_checks"):
            self.logger.info("Running update checks")
            self.check_for_updates()

        if video_data.consistent_data.get("anonymous_mode"):
            self.logger.info("Enabling anonymous mode")
            self.anonymous_mode()

        self.semaphore = asyncio.Semaphore(video_data.consistent_data["semaphore"])
        self.logger.debug("Startup: [5/5] OK")
        if FORCE_TEST_RUN:
            sys.exit(0)

        self.initialize_pornfetch()

    """
    The following functions just switch the Stacked Widget to the different widgets
    """

    """Stacked Widget Main:"""

    def switch_to_main(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(0)

    def switch_to_settings(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(1)

    def switch_to_credits(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(2)

    def switch_to_license(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(3)

    def switch_to_keyboard_shortcuts(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(4)

    def switch_to_install_dialog(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(5)

    def switch_to_supported_sites(self):
        if self._anonymous_mode:
            self.supported_sites_qml.hide()
            self.ui.supported_sites_textbrowser.show()
            self.ui.supported_sites_textbrowser.setHtml("Running in anonymous mode...")
        else:
            self.ui.supported_sites_textbrowser.hide()
            self.supported_sites_qml.show()
        self.ui.main_CentralStackedWidget.setCurrentIndex(6)

    def switch_to_disclaimer(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(7)

    def switch_to_one_time_setup(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(8)

    def switch_to_update_available(self):
        self.ui.main_CentralStackedWidget.setCurrentIndex(9)

    """Stacked Widget Top:"""

    def switch_to_download(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(0)
        self.ui.main_stacked_widget_top.setMaximumHeight(120)
        self.switch_to_main()

    def switch_to_login(self):
        self.ui.main_stacked_widget_top.setCurrentIndex(1)
        self.ui.main_stacked_widget_top.setMaximumHeight(180)
        self.switch_to_login_pornhub()
        self.switch_to_main()

    def switch_to_login_pornhub(self):
        self.ui.login_stacked_widget.setCurrentIndex(0)

    def switch_to_login_xvideos(self):
        self.ui.login_stacked_widget.setCurrentIndex(1)

    # Stacked Widget Tree
    def switch_to_treewidget_downloads(self):
        self.ui.main_stacked_widget_tree.setCurrentIndex(0)
        self.switch_to_main()

    def switch_to_treewidget_advanced_configuration(self):
        self.ui.main_stacked_widget_tree.setCurrentIndex(1)
        self.switch_to_main()

    def _setup_modern_tabs(self):
        # Setup Credits QML
        self.ui.credits_textbrowser.hide()
        self.credits_qml = QQuickWidget(self)
        self.credits_qml.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.credits_qml.setSource(QUrl.fromLocalFile(str(Path(__file__).parent / "src" / "frontend" / "UI" / "CreditsWidget.qml")))
        self.ui.scrollarea_credits_vboxlayout.addWidget(self.credits_qml)
        
        # Setup Supported Sites QML
        self.ui.supported_sites_textbrowser.hide()
        self.supported_sites_qml = QQuickWidget(self)
        self.supported_sites_qml.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.supported_sites_qml.setSource(QUrl.fromLocalFile(str(Path(__file__).parent / "src" / "frontend" / "UI" / "SupportedSitesWidget.qml")))
        self.ui.gridLayout_20.addWidget(self.supported_sites_qml, 0, 0, 1, 1)

    def load_style(self):
        icons = {
            self.ui.main_button_switch_home: "download.svg",
            self.ui.main_button_switch_settings: "settings.svg",
            self.ui.main_button_switch_credits: "information.svg",
            self.ui.main_button_switch_account: "account.svg",
        }
        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))

        for btn, name in icons.items():
            btn.setIcon(QIcon(f":/images/graphics/{name}"))
            btn.setIconSize(QSize(24, 24))  # consistent size for all

        pixmap_tooltip = QPixmap(":/images/graphics/tooltip.svg")
        mark_help_buttons(ui=self.ui, pixmap=pixmap_tooltip)

        # --- top nav becomes segmented & exclusive ---
        nav = [
            self.ui.main_button_switch_home,
            self.ui.main_button_switch_account,
            self.ui.main_button_switch_settings,
            self.ui.main_button_switch_credits,
        ]
        group_menu_bar = QButtonGroup(self)
        group_menu_bar.setExclusive(True)
        for b in nav:
            b.setCheckable(True)
            group_menu_bar.addButton(b)
            mark(b, seg=True)  # <- gives the segmented style
        self.ui.main_button_switch_home.setChecked(True)

        tree_nav = [
            self.ui.treewidget_button_downloads,
            self.ui.treewidget_button_advanced_configuration,
        ]

        group_tree_nav = QButtonGroup(self)
        group_tree_nav.setExclusive(True)
        for b in tree_nav:
            b.setCheckable(True)
            group_tree_nav.addButton(b)
            mark(b, seg=True)
        self.ui.treewidget_button_downloads.setChecked(True)


        settings_nav = [
            self.ui.settings_button_switch_video,
            self.ui.settings_button_switch_performance,
            self.ui.settings_button_switch_system,
            self.ui.settings_button_switch_ui
        ]
        group_settings_bar = QButtonGroup(self)
        group_settings_bar.setExclusive(True)
        for b in settings_nav:
            b.setCheckable(True)
            group_settings_bar.addButton(b)
            mark(b, seg=True)
        self.ui.settings_button_switch_video.setChecked(True)

        login_nav = [
            self.ui.login_button_switch_pornhub,
            self.ui.login_button_switch_xvideos
        ]
        group_login_bar = QButtonGroup(self)
        group_login_bar.setExclusive(True)
        for b in login_nav:
            b.setCheckable(True)
            group_login_bar.addButton(b)
            mark(b, seg=True)

        self.ui.login_button_switch_pornhub.setChecked(True)


        # --- intent & size instead of dozens of QSS files ---
        mark(self.ui.download_button_download, intent="primary", size="lg")
        mark(self.ui.login_button_login, intent="primary")
        mark(self.ui.login_xvideos_button_login, intent="primary")
        mark(self.ui.settings_button_apply, intent="primary", size="lg")
        mark(self.ui.credits_button_send_feedback, intent="primary")
        mark(self.ui.settings_button_system_install_pornfetch, intent="success")
        mark(self.ui.treewidget_button_stop, intent="danger")
        mark(self.ui.treewidget_button_advanced_configuration, seg=True)
        mark(self.ui.settings_button_import_license)
        mark(self.ui.button_settings_clear_temp)
        mark(self.ui.settings_button_uninstall_porn_fetch, intent="danger")
        mark(self.ui.settings_button_reset, intent="danger")
        mark(self.ui.main_progressbar_total, role="total")
        mark(self.ui.login_xvideos_button_help, intent="success")

        mark(self.ui.one_time_setup_button_info_enable_all, intent="success")
        mark(self.ui.one_time_setup_button_info_disable_all, intent="danger")
        mark(self.ui.one_time_setup_button_info_enable_update, intent="primary")

        stylesheet_license_button = """
QPushButton {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                      stop:0 #2563eb, stop:1 #7c3aed);
    color: white;
    font-weight: bold;
    font-size: 14px;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
}

QPushButton:hover {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                                      stop:0 #3b82f6, stop:1 #8b5cf6);
}

QPushButton:pressed {
    background-color: #1e40af;
    padding-top: 12px;
    padding-left: 22px;
}
        """

        stylesheet_import_license = """
QPushButton {
    background-color: rgba(0,0,0,0); /* Explicitly transparent */
    color: #94a3b8;
    font-weight: bold;
    font-size: 14px;
    border-radius: 8px;
    padding: 10px 20px;
    border: 2px solid #475569;
}

QPushButton:hover {
    color: #ffffff;
    border: 2px solid #94a3b8;
    background-color: rgba(255,255,255,15); /* Removed spaces */
}

QPushButton:pressed {
    background-color: rgba(255,255,255,30);
}
"""

        stylesheet_lineedit_custom_title = """
QLineEdit {
    /* Basic Layout */
    background-color: #232323; 
    border: 2px solid #3A3A3A;
    border-radius: 15px; /* High radius for a pill shape */
    padding: 8px 15px; /* Comfortable padding */
    
    /* Text Styling */
    color: #E0E0E0;
    font-family: "Segoe UI", sans-serif; /* Or your preferred font */
    font-size: 14px;
    font-weight: bold;
    
    /* Selection Color */
    selection-background-color: #00DAC6;
    selection-color: #000000;
}

/* Hover State - Subtle feedback */
QLineEdit:hover {
    background-color: #2C2C2C;
    border: 2px solid #505050;
}

/* Focus State - The "Special" moment */
QLineEdit:focus {
    border: 2px solid #00DAC6; /* Bright Cyan border */
    background-color: #1A1A1A; /* Slightly darker to add depth */
}
"""
        self.ui.settings_button_buy_license.setStyleSheet(stylesheet_license_button)
        self.ui.settings_button_import_license.setStyleSheet(stylesheet_import_license)
        self.ui.tree_advanced_lineedit_custom_title.setStyleSheet(stylesheet_lineedit_custom_title)

        # most of these are secondary or flat so they don’t compete visually
        for b in [
            self.ui.main_button_switch_supported_websites,
            self.ui.update_available_button_acknowledged,
        ]:
            mark(b, flat=True)

        # things that start/queue work but aren’t “the” CTA: make them secondary
        for b in [
            self.ui.download_button_playlist_get_videos,
            self.ui.download_button_model,
            self.ui.settings_button_system_install_pornfetch,
            self.ui.tree_advanced_button_keyboard_shortcuts,
        ]:
            mark(b)  # no intent ⇒ secondary

        for cb in self.findChildren(QComboBox):
            pretty_combo(cb)

        # --- progress bars: mark roles instead of separate QSS files ---
        mark(self.ui.main_progressbar_total, role="total")

        # --- tree header sizing / behavior ---

        self.ui.main_tree_widget.setColumnCount(7)
        self.ui.main_tree_widget.setHeaderLabels([
            "Download", "Title", "Author", "Length", "Quality", "Stop", "Progress"
        ])
        self.ui.main_tree_widget.setRootIsDecorated(False)  # looks more like a table
        self.ui.main_tree_widget.setAlternatingRowColors(True)
        self.ui.main_tree_widget.setSelectionBehavior(self.ui.main_tree_widget.SelectionBehavior.SelectRows)

        # Make it look reasonable
        self.ui.main_tree_widget.setColumnWidth(self.COL_DOWNLOAD, 110)
        self.ui.main_tree_widget.setColumnWidth(self.COL_TITLE, 120)
        self.ui.main_tree_widget.setColumnWidth(self.COL_AUTHOR, 180)
        self.ui.main_tree_widget.setColumnWidth(self.COL_LENGTH, 120)
        self.ui.main_tree_widget.setColumnWidth(self.COL_QUALITY, 120)
        self.ui.main_tree_widget.setColumnWidth(self.COL_PROGRESS, 220)
        self.ui.main_tree_widget.header().setSectionResizeMode(self.COL_DOWNLOAD, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.main_tree_widget.header().setSectionResizeMode(self.COL_QUALITY, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.main_tree_widget.header().setSectionResizeMode(self.COL_STOP, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.main_tree_widget.header().setSectionResizeMode(self.COL_LENGTH, QHeaderView.ResizeMode.ResizeToContents)

        # Let the title take the free space
        self.ui.main_tree_widget.header().setSectionResizeMode(self.COL_TITLE, QHeaderView.ResizeMode.Stretch)

        # Progress is last: let it stretch too (it will consume remaining space)
        self.ui.main_tree_widget.header().setStretchLastSection(True)

        # --- misc you already had ---
        self.ui.main_tree_widget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.setWindowTitle(f"Porn Fetch v{__version__} Copyright (C) Johannes Habel 2023-2026")
        self.ui.main_tree_widget.sortByColumn(2, Qt.SortOrder.AscendingOrder)
        self.ui.settings_stacked_widget_main.setCurrentIndex(0)
        install_focus_outline(self)
        self.filter = ComboPopupFitter()
        self.ui.settings_combobox_ui_theme.installEventFilter(self.filter)
        self.ui.settings_ui_combobox_language.installEventFilter(self.filter)
        self.ui.settings_video_combobox_quality.installEventFilter(self.filter)
        self.ui.settings_video_combobox_model_videos.installEventFilter(self.filter)
        self.switch_to_download()
        self.switch_to_treewidget_downloads()

    def load_strings(self):
        """
        This loads and applies the strings to the UI from src/frontend/translations/strings.py
        """
        self.disable_anonymous_mode()

    def enable_anonymous_mode(self):
        """
        This mode will hide that you are using Porn Fetch by hiding video title names, hiding author names,
        hiding the window title and removing all placeholders from lineedits. May not be the most efficient approach,
         but it works.
        """
        if self._anonymous_mode:
            self.logger.info("Already running anonymous, resetting back...")
            self.disable_anonymous_mode()
            return

        self.setWindowTitle("Running in Anonymous mode...")
        self.ui.download_lineedit_url.setPlaceholderText(" ")
        self.ui.download_lineedit_model_url.setPlaceholderText(" ")
        self.ui.download_lineedit_playlist_url.setPlaceholderText(" ")
        self.ui.login_lineedit_password.setPlaceholderText(" ")
        self.ui.login_lineedit_username.setPlaceholderText(" ")
        self.ui.settings_button_system_install_pornfetch.setText("Install Program")
        self.ui.settings_button_uninstall_porn_fetch.setText("Uninstall Program")
        self.ui.settings_button_reset.setText("Reset Application")
        self.ui.supported_sites_textbrowser.setText(
            "Running in anonymous mode, please deactivate to display...")
        self._anonymous_mode = True  # Makes sense, trust
        self.logger.info("Enabled anonymous mode!")

    def disable_anonymous_mode(self):
        """
        This loads the UI state back to normal
        """
        self.setWindowTitle(TRANSLATE_MAIN.title)
        self.ui.download_lineedit_url.setPlaceholderText(TRANSLATE_PAGE_DOWNLOAD.download_url_placeholder)
        self.ui.download_lineedit_playlist_url.setPlaceholderText(TRANSLATE_PAGE_DOWNLOAD.download_playlist_placeholder)
        self.ui.download_lineedit_model_url.setPlaceholderText(TRANSLATE_PAGE_DOWNLOAD.download_model_placeholder)
        self.ui.login_lineedit_password.setPlaceholderText(TRANSLATE_PAGE_LOGIN.login_email_password)
        self.ui.login_lineedit_username.setPlaceholderText(TRANSLATE_PAGE_LOGIN.login_email_password)
        self.ui.settings_button_system_install_pornfetch.setText(TRANSLATE_PAGE_SETTINGS.settings_button_install_pf)
        self.ui.download_lineedit_playlist_url.setPlaceholderText(TRANSLATE_PAGE_DOWNLOAD.download_playlist_placeholder)
        self.ui.settings_button_reset.setText(TRANSLATE_PAGE_SETTINGS.settings_button_reset_pf)
        self.ui.settings_button_uninstall_porn_fetch.setText(TRANSLATE_PAGE_SETTINGS.settings_button_uninstall_pf)
        self._anonymous_mode = False  # Makes sense, trust

        self.logger.info("Disabled anonymous mode!")
        self.setWindowTitle(f"Porn Fetch v{__version__} Copyright (C) Johannes Habel 2023-2026")

    def button_connections(self):
        """a function to link the buttons to their functions"""
        # Menu Bar Switch Button Connections
        self.ui.main_button_switch_home.clicked.connect(self.switch_to_download)
        self.ui.main_button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.main_button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.main_button_switch_account.clicked.connect(self.switch_to_login)
        self.ui.main_button_switch_supported_websites.clicked.connect(self.switch_to_supported_sites)

        # Video Download Button Connections
        self.ui.download_button_download.clicked.connect(self.start_single_video)
        self.ui.download_button_model.clicked.connect(self.start_model)
        self.ui.download_button_playlist_get_videos.clicked.connect(self.start_playlist)

        # Settings
        self.ui.settings_button_switch_video.clicked.connect((lambda _=False, i=0: self.ui.settings_stacked_widget_main.setCurrentIndex(i)))
        self.ui.settings_button_switch_performance.clicked.connect(lambda _=False, i=1: self.ui.settings_stacked_widget_main.setCurrentIndex(i))
        self.ui.settings_button_switch_system.clicked.connect(lambda _=False, i=2: self.ui.settings_stacked_widget_main.setCurrentIndex(i))
        self.ui.settings_button_switch_ui.clicked.connect(lambda _=False, i=3: self.ui.settings_stacked_widget_main.setCurrentIndex(i))
        self.ui.settings_button_buy_license.clicked.connect(self.buy_license)
        self.ui.settings_button_import_license.clicked.connect(self.import_license)
        self.ui.settings_button_uninstall_porn_fetch.clicked.connect(self.uninstall_porn_fetch)

        # Info Dialog
        self.ui.one_time_setup_button_info_enable_all.clicked.connect(self.info_dialog_enable_all)
        self.ui.one_time_setup_button_info_disable_all.clicked.connect(self.info_dialog_disable_all)
        self.ui.one_time_setup_button_info_enable_update.clicked.connect(self.info_dialog_enable_update)

        self.ui.settings_button_apply.clicked.connect(lambda: self.save_user_settings())
        self.ui.settings_button_reset.clicked.connect(reset_pornfetch)
        self.ui.settings_button_system_install_pornfetch.clicked.connect(self.switch_to_install_dialog)
        self.ui.settings_checkbox_system_activate_proxy.clicked.connect(self.set_proxies)
        self.ui.button_install.clicked.connect(self.install_pornfetch)
        self.ui.button_portable.clicked.connect(self.install_porn_fetch_portable)

        # Account
        self.ui.login_button_login.clicked.connect(self.login)
        self.ui.login_button_get_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.login_button_get_liked_videos.clicked.connect(self.get_liked_videos)
        self.ui.login_button_get_recommended_videos.clicked.connect(self.get_recommended_videos)
        self.ui.login_button_switch_pornhub.clicked.connect(self.switch_to_login_pornhub)
        self.ui.login_button_switch_xvideos.clicked.connect(self.switch_to_login_xvideos)


        # File Dialog
        self.ui.settings_button_videos_open_output_path.clicked.connect(self.open_output_path_dialog)

        # Other stuff IDK
        self.ui.treewidget_button_stop.clicked.connect(switch_stop_state)
        self.ui.tree_advanced_button_keyboard_shortcuts.clicked.connect(self.switch_to_keyboard_shortcuts)
        self.ui.settings_checkbox_system_enable_debug_mode.clicked.connect(on_checkbox_clicked)
        self.ui.button_settings_clear_temp.clicked.connect(self.clean_temporary_files)
        self.ui.tree_advanced_button_custom_title_options.clicked.connect(available_title_formatting_options)

        # Stacked Tree Widget
        self.ui.treewidget_button_downloads.clicked.connect(self.switch_to_treewidget_downloads)
        self.ui.treewidget_button_advanced_configuration.clicked.connect(self.switch_to_treewidget_advanced_configuration)

    def initialize_pornfetch(self):
        """
        After all stylesheets and icons are loaded, this function will initiate the process for checking
        if the License was shown and accepted, if the disclaimer text was shown, if the user downloaded the amount
        of videos to show the sponsoring dialog and after all that switch to the main widget.
        """
        global FORCE_PORTABLE_RUN
        settings.sync()

        self.ui.main_progressbar_total.setMaximum(4)

        if not self.license.check_license():
            self.switch_to_license()
            return

        self.ui.main_progressbar_total.setValue(1)

        if not self.disclaimer.check_disclaimer():
            self.switch_to_disclaimer()
            return

        self.ui.main_progressbar_total.setValue(2)
        first = settings.value("Misc/first_run_gui", True, type=bool)
        if first:
            settings.setValue("Misc/first_run_gui", False)
            settings.sync()
            ui_popup("""
VERY IMPORTANT INFORMATION (must read)

With this release, Porn Fetch gets a license system with paid only features.
So you need to buy a license for 5€ to get all features, HOWEVER...

Because I live in Germany and in this country you need to create a company even if you want to make one cent,
and I haven't done that yet, you get the full license FOR FREE!

I am currently using a stripe checkout form which is in test mode. That means that while this looks like a real payment,
your card will NOT be charged.

To get a license, please go to: 
https://echteralsfake.me/buy_license

For the E-Mail enter:
test@test.com

Enter this for the payment information:
Card Number: 4242 4242 4242 4242
MM / JJ: 05/28
CVC: 999
Name: Max Mustermann


This serves as a test environment for the real license system later on.
Thank you very much for participating :)

If you need help, please write to:
EchterAlsFake@proton.me
""")

            self.switch_to_one_time_setup()

            ui_popup("""
Warning:

You are using Porn Fetch from the latest source code. This can cause weird behaviour or other issues.
Do not report issues when using Porn Fetch from source code.

You have all paid features unlocked :)
""")

            return

        self.ui.main_progressbar_total.setValue(3)
        if not FORCE_PORTABLE_RUN:
            if sys.platform == "darwin":
                self.ui.main_CentralStackedWidget.setCurrentIndex(0)
                return

            if settings.value("Misc/install_type") == "unknown":
                self.switch_to_install_dialog()
                return

        self.ui.main_progressbar_total.setValue(0) # Clear
        self.ui.main_progressbar_total.setMaximum(100)

        if first:
            self.save_user_settings()

        self.ui.main_CentralStackedWidget.setCurrentIndex(0)

    def info_dialog_enable_update(self):
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(False)
        self.ui.settings_checkbox_system_update_checks.setChecked(True)
        self.save_user_settings(show_dialog=False)
        self.initialize_pornfetch()

    def info_dialog_disable_all(self):
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(False)
        self.ui.settings_checkbox_system_update_checks.setChecked(False)
        self.save_user_settings(show_dialog=False)
        self.initialize_pornfetch()

    def info_dialog_enable_all(self):
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(True)
        self.ui.settings_checkbox_system_update_checks.setChecked(True)
        self.save_user_settings(show_dialog=False)
        self.initialize_pornfetch()

    def shortcuts(self):
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

        download_all = QShortcut(QKeySequence("Ctrl+T"), self)
        download_all.activated.connect(self.download_all)

        export_urls_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        export_urls_shortcut.activated.connect(export_urls)

        enable_anonymous_mode = QShortcut(QKeySequence("Ctrl+A"), self)
        enable_anonymous_mode.activated.connect(self.enable_anonymous_mode)

        save_settings = QShortcut(QKeySequence("Ctrl+S"), self)
        save_settings.activated.connect(self.save_user_settings)

    def download_all(self):
        """Automatically downloads all videos in the tree widget"""
        for i in range(self.ui.main_tree_widget.topLevelItemCount()):
            item = self.ui.main_tree_widget.topLevelItem(i)
            identifier = item.data(self.COL_TITLE, Qt.ItemDataRole.UserRole)
            self.queue_download(video_id=identifier)

    def maps(self):
        self.mappings_quality = {
            0: "best",
            1: "half",
            2: "worst",
            3: 2160,
            4: 1440,
            5: 1080,
            6: 720,
            7: 540,
            8: 480,
            9: 360,
            10: 240,
            11: 144
        }
        self.mappings_ui_theme = {
            0: "dark",
            1: "light",
            2: "lsd",
        }
        self.mappings_ui_language = {
            0: "system",
            1: "english",
            2: "german",
            3: "chinese",
            4: "french"
        }

    def load_user_settings(self):
        global x
        settings.sync()
        license_ok = self.license_manager.has_feature("full_unlock") or x

        # --- Video ---
        _quality = settings.value("Video/quality", 0, int)
        if _quality <= 5 and not (license_ok or IS_SOURCE_RUN):
            ui_popup("Warning! You have selected (somehow) a higher quality than 720p. You need a license to unlock it. Please go into the settings to get and import one...")
            _quality = 6 # Correcting back to 720p

        video_data.consistent_data.update({"quality": self.mappings_quality.get(_quality)})
        self.ui.settings_video_combobox_quality.setCurrentIndex(_quality)

        _model_videos = settings.value("Video/model_videos", 0, int)
        video_data.consistent_data.update({"model_videos": _model_videos})
        self.ui.settings_video_combobox_model_videos.setCurrentIndex(_model_videos)

        result_limit = settings.value("Video/result_limit", 50, int)
        video_data.consistent_data.update({"result_limit": result_limit})
        self.ui.settings_spinbox_videos_result_limit.setValue(result_limit)

        output_path = settings.value("Video/output_path", "./", str)
        video_data.consistent_data.update({"output_path": output_path})
        self.ui.settings_lineedit_videos_output_path.setText(output_path)

        write_metadata = settings.value("Video/write_metadata", True, bool)
        video_data.consistent_data.update({"write_metadata": write_metadata})
        self.ui.settings_checkbox_videos_write_metadata.setChecked(write_metadata)

        skip_existing_files = settings.value("Video/skip_existing_files", True, bool)
        video_data.consistent_data.update({"skip_existing_files": skip_existing_files})
        self.ui.settings_checkbox_videos_skip_existing_files.setChecked(skip_existing_files)

        track_videos = settings.value("Video/track_videos", False, bool)
        video_data.consistent_data.update({"track_videos": track_videos})
        self.ui.settings_checkbox_videos_track_downloaded_videos.setChecked(track_videos)

        database_path = settings.value("Video/database_path", "./downloads.db", str)
        video_data.consistent_data.update({"database_path": database_path})
        self.ui.settings_lineedit_videos_database_path.setText(database_path)

        directory_system = settings.value("Video/directory_system", False, bool)
        video_data.consistent_data.update({"directory_system": directory_system})
        self.ui.settings_checkbox_videos_use_directory_system.setChecked(directory_system)

        # --- Performance ---
        simultaneous_downloads = settings.value("Performance/semaphore", 2, int)

        if int(simultaneous_downloads) > 1 and not (license_ok or IS_SOURCE_RUN):
            ui_popup("Warning! You have selected (somehow) a higher amount of parallel downloads than you are supposed to. You need a license to unlock it. Please go into the settings to get and import one...")
            simultaneous_downloads = 1 # Correcting back to 720p

        video_data.consistent_data.update({"semaphore": simultaneous_downloads})
        self.ui.settings_spinbox_performance_simultaneous_downloads.setValue(simultaneous_downloads)

        network_delay = settings.value("Performance/network_delay", 0, int)
        video_data.consistent_data.update({"network_delay": network_delay})
        self.ui.settings_spinbox_performance_network_delay.setValue(network_delay)

        videos_concurrency = settings.value("Performance/videos_concurrency", 10, int)
        video_data.consistent_data.update({"videos_concurrency": videos_concurrency})
        self.ui.settings_spinbox_performance_videos_concurrency.setValue(videos_concurrency)

        pages_concurrency = settings.value("Performance/pages_concurrency", 2, int)
        video_data.consistent_data.update({"pages_concurrency": pages_concurrency})
        self.ui.settings_spinbox_performance_pages_concurrency.setValue(pages_concurrency)

        download_workers = settings.value("Performance/download_workers", 20, int)
        video_data.consistent_data.update({"download_workers": download_workers})
        self.ui.settings_spinbox_performance_download_workers.setValue(download_workers)

        timeout = settings.value("Performance/timeout", 10, int)
        video_data.consistent_data.update({"timeout": timeout})
        self.ui.settings_spinbox_performance_maximal_timeout.setValue(timeout)

        retries = settings.value("Performance/retries", 4, int)
        video_data.consistent_data.update({"retries": retries})
        self.ui.settings_spinbox_performance_maximal_retries.setValue(retries)

        speed_limit = settings.value("Performance/speed_limit", 0.0, float)
        video_data.consistent_data.update({"speed_limit": speed_limit})
        self.ui.settings_doublespinbox_performance_speed_limit.setValue(speed_limit)

        processing_delay = settings.value("Performance/processing_delay", 0, int)
        video_data.consistent_data.update({"processing_delay": processing_delay})
        self.ui.settings_spinbox_performance_processing_delay.setValue(processing_delay)

        # --- System/Misc ---
        update_checks = settings.value("Misc/update_checks", True, bool)
        video_data.consistent_data.update({"update_checks": update_checks})
        self.ui.settings_checkbox_system_update_checks.setChecked(update_checks)

        anonymous_mode = settings.value("Misc/anonymous_mode", False, bool)
        self._anonymous_mode = anonymous_mode
        video_data.consistent_data.update({"anonymous_mode": anonymous_mode})
        self.ui.settings_checkbox_system_enable_anonymous_mode.setChecked(anonymous_mode)

        supress_errors = settings.value("Misc/supress_errors", False, bool)
        video_data.consistent_data.update({"supress_errors": supress_errors})
        self.ui.settings_checkbox_system_supress_errors.setChecked(supress_errors)

        network_logging = settings.value("Misc/network_logging", False, bool)
        video_data.consistent_data.update({"network_logging": network_logging})
        self.ui.settings_checkbox_system_enable_network_logging.setChecked(network_logging)

        debug_mode = settings.value("Misc/debug_mode", False, bool)
        video_data.consistent_data.update({"debug_mode": debug_mode})
        self.ui.settings_checkbox_system_enable_debug_mode.setChecked(debug_mode)

        use_truststore = settings.value("Misc/use_truststore", False, type=bool)
        video_data.consistent_data.update({"use_truststore": use_truststore})
        self.ui.settings_checkbox_use_truststore.setChecked(use_truststore)

        # --- UI ---
        ui_language_idx = settings.value("UI/language", 0, int)
        self.ui.settings_ui_combobox_language.setCurrentIndex(ui_language_idx)

        font_size = settings.value("UI/font_size", 10, int)
        self.ui.settings_spinbox_ui_font_size.setValue(font_size)

        ui_theme_idx = settings.value("UI/theme", 0, int)
        self.ui.settings_combobox_ui_theme.setCurrentIndex(ui_theme_idx)

        # Apply to your core_conf
        clients.config.timeout = timeout
        clients.config.max_retries = retries
        clients.config.max_bandwidth_mb = speed_limit
        clients.config.raise_bot_protection = False
        clients.config.request_delay = network_delay
        clients.config.videos_concurrency = videos_concurrency
        clients.config.pages_concurrency = pages_concurrency
        clients.config.max_workers_download = download_workers
        clients.refresh_clients(debug_mode=bool(debug_mode), use_truststore=bool(use_truststore))

    def save_user_settings(self, show_dialog=True):
        settings.sync()

        """Saves the user settings to the configuration file based on the UI state."""
        # --- Video ---
        settings.beginGroup("Video")
        settings.setValue("quality", self.ui.settings_video_combobox_quality.currentIndex())
        settings.setValue("model_videos", self.ui.settings_video_combobox_model_videos.currentIndex())
        settings.setValue("result_limit", int(self.ui.settings_spinbox_videos_result_limit.value()))
        settings.setValue("output_path", str(self.ui.settings_lineedit_videos_output_path.text()))
        settings.setValue("write_metadata", self.ui.settings_checkbox_videos_write_metadata.isChecked())
        settings.setValue("skip_existing_files", self.ui.settings_checkbox_videos_skip_existing_files.isChecked())
        settings.setValue("track_videos", self.ui.settings_checkbox_videos_track_downloaded_videos.isChecked())
        settings.setValue("database_path", str(self.ui.settings_lineedit_videos_database_path.text()))
        settings.setValue("directory_system", self.ui.settings_checkbox_videos_use_directory_system.isChecked())
        settings.endGroup()

        # --- Performance ---
        settings.beginGroup("Performance")
        settings.setValue("semaphore", int(self.ui.settings_spinbox_performance_simultaneous_downloads.value()))
        settings.setValue("network_delay", int(self.ui.settings_spinbox_performance_network_delay.value()))
        settings.setValue("videos_concurrency", int(self.ui.settings_spinbox_performance_videos_concurrency.value()))
        settings.setValue("pages_concurrency", int(self.ui.settings_spinbox_performance_pages_concurrency.value()))
        settings.setValue("download_workers", int(self.ui.settings_spinbox_performance_download_workers.value()))
        settings.setValue("timeout", int(self.ui.settings_spinbox_performance_maximal_timeout.value()))  # <-- fixed key
        settings.setValue("retries", int(self.ui.settings_spinbox_performance_maximal_retries.value()))  # <-- fixed key
        settings.setValue("speed_limit", float(self.ui.settings_doublespinbox_performance_speed_limit.value()))
        settings.setValue("processing_delay", int(self.ui.settings_spinbox_performance_processing_delay.value()))
        settings.endGroup()

        # --- Misc/System ---
        settings.beginGroup("Misc")
        settings.setValue("update_checks", self.ui.settings_checkbox_system_update_checks.isChecked())
        settings.setValue("anonymous_mode", self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked())
        settings.setValue("supress_errors", self.ui.settings_checkbox_system_supress_errors.isChecked())
        settings.setValue("network_logging", self.ui.settings_checkbox_system_enable_network_logging.isChecked())
        settings.setValue("debug_mode", self.ui.settings_checkbox_system_enable_debug_mode.isChecked())
        settings.setValue("use_truststore", self.ui.settings_checkbox_use_truststore.isChecked())
        settings.endGroup()

        # --- UI ---
        settings.beginGroup("UI")
        settings.setValue("language", self.ui.settings_ui_combobox_language.currentIndex())
        settings.setValue("theme", self.ui.settings_combobox_ui_theme.currentIndex())
        settings.setValue("font_size", int(self.ui.settings_spinbox_ui_font_size.value()))
        settings.endGroup()

        settings.sync()  # write to disk now

        if show_dialog:
            ui_popup(self.tr("Saved User Settings, please restart Porn Fetch!", None))

        self.logger.debug("Saved User Settings, please restart Porn Fetch.")

    def set_proxies(self):
        message = self.tr("""
Please read this before setting proxies:

I am not a genius in programming and I can NOT guarantee for your safety. However, I did everything possible (in my abilities)
to make sure this works perfectly. When you apply proxies you need to make sure that they are in the correct format. You'll
see a few examples down below.

Also, if you use PUBLIC proxies, then it's really a gamble if they work or if they don't. Usually they are really slow and 
inconsistent, but maybe you are lucky.

About SSL encryption:   

If your proxy does NOT support SSL / TLS or delivers incorrect self-signed certificates, then you can choose to ignore that
by disabling SSL verification. However, this reduces your security a lot and people in your network will be able to intercept
your network traffic. 

This is not my fault, it's just how the internet works. So, get yourself a good proxy and then you are good to go :)

Here are a few examples of valid proxies:

1) http://89.3.64.185:1111
2) socks5://45.115.114.57:9090

Important:
Even if your proxy supports https, you need to put it as 'http://'. This will NOT disable encryption.

I do not know whether authenticated proxies e.g., with user + password authentication work.
I can't test that, since I don't own such proxies.


I will test your proxy before actually using it using requests to httpbin.org to get your IP address. One request with 
and one request without a proxy. If the IPs are different, then it worked, if not you need to use another proxy.

This is all for your safety!

Warning:
Unless you use your own ELITE proxy, DO NOT REPORT ANY ERRORS THAT OCCUR WHEN YOU HAVE PROXIES ENABLED!!!
        """, disambiguation=None)

        ui_popup(message)

        proxy_input, ok = QInputDialog.getText(
            self,
            "Enter Proxies",
            "Enter proxy in the format <protocol><ip>:<port> -->:")

        if not ok:
            return None  # User canceled the input dialog

        else:
            self.logger.info(f"Using Proxy -->: {proxy_input}")
            self.logger.info("Getting IP address without Proxy")
            ip = clients.core.fetch(url="https://httpbin.org/ip", get_response=True).json()["origin"]
            self.logger.info("Applying Proxy to all session objects...")
            clients.config.proxy = proxy_input
            clients.refresh_clients()
            self.logger.info(f"Unmasked IP is -->: {ip}")
            try:
                ip_masked = clients.core.fetch(url="https://httpbin.org/ip", get_response=True).json()["origin"]

            except ProxySSLError:
                dialog = SSLWarningDialog()
                if dialog.exec():
                    self.logger.warning("Disabling SSL Verification")
                    clients.config.verify_ssl = False
                    clients.refresh_clients()
                    ip_masked = clients.core.fetch(url="https://httpbin.org/ip", get_response=True).json()[
                        "origin"]

                else:
                    ui_popup(self.tr("You did choose to not disable SSL Verifications. Retuning to GUI without applying proxies now...", disambiguation=None))
                    return None

            except InvalidProxy:
                ui_popup(self.tr("Your proxy seems to be invalid, please try again...", disambiguation=None))
                return None

            self.logger.info(f"Masked IP is -->: {ip_masked}")

            if ip == ip_masked:
                self.logger.error("ERROR: IP LEAK!")
                ui_popup(self.tr(f"Proxy IP: {ip_masked} Your IP: {ip} are the same! Please check the proxy you've used!, aborting...", disambiguation=None))
                return None


            else:
                self.logger.info("Proxy worked!")
                self.proxy = proxy_input
                return None


    """
    These are the core functions of Porn Fetch outside of the UI stuff. They are used to process user input.
    """

    async def start_single_video(self):
        """
        Starts the download of a single video.
        This still uses the tree widget because this makes it easier to track the total progress, as I've already
        implemented this feature into the tree widget and I don't want to write code 2 times
        """
        url = self.ui.download_lineedit_url.text()
        self.logger.info(f"[Download (1/10) - Preparing] -->: {url}")
        self.ui.download_lineedit_url.clear()

        async def single_url_stream():
            yield url # Patch for the process_video class (look at it and you'll understand why I did this here)

        self.process_videos(iterator=single_url_stream())

    async def start_model(self, url: str | None = None):
        """Starts the model downloads"""
        # 1. Clean up variable assignment
        target_url = url if isinstance(url, str) else self.ui.download_lineedit_model_url.text()
        target_url = str(target_url)

        self.ui.download_lineedit_model_url.clear()
        self.logger.debug(f"Checking model: {target_url}")

        videos = None
        target_obj = None

        # 2. Group by platform to eliminate redundant 'in' checks
        if "pornhub" in target_url:
            if "pornstar" in target_url:
                model_object = clients.ph_client.get_user(target_url)
                model_type = self.ui.settings_video_combobox_model_videos.currentIndex()

                if model_type == 0:
                    videos = chain(model_object.uploads, model_object.videos)
                elif model_type == 1:
                    videos = model_object.videos
                elif model_type == 2:
                    videos = model_object.uploads

            elif "user" in target_url or "channel" in target_url:
                target_obj = await clients.ph_client.get_channel(load_html=True, url=target_url)
                videos = target_obj.get_videos()

        elif "eporner" in target_url:
            target_obj = await clients.ep_client.get_pornstar(url=target_url, load_html=True)

        elif "xnxx" in target_url:
            target_obj = await clients.xn_client.get_user(url=target_url)

        elif "youporn" in target_url:
            if "channel" in target_url:
                target_obj = await clients.yp_client.get_channel(url=target_url)
            else:
                target_obj = await clients.yp_client.get_pornstar(url=target_url)

        elif "xvideos" in target_url:
            if "model" in target_url or "pornstar" in target_url:
                target_obj = await clients.xv_client.get_pornstar(url=target_url)
            else:
                target_obj = await clients.xv_client.get_channel(url=target_url)

        elif "spankbang" in target_url:
            if "pornstar" in target_url:
                target_obj = await clients.sp_client.get_pornstar(url=target_url)
            elif "creator" in target_url:
                target_obj = await clients.sp_client.get_creator(url=target_url)
            elif "channel" in target_url:
                target_obj = await clients.sp_client.get_channel(url=target_url)

        elif "xhamster" in target_url:
            if "pornstars" in target_url:
                target_obj = await clients.xh_client.get_pornstar(url=target_url)
            elif "creators" in target_url:
                target_obj = await clients.xh_client.get_creator(url=target_url)
            elif "channels" in target_url:
                target_obj = await clients.xh_client.get_channel(url=target_url)

        elif "porntrex" in target_url:
            if "channel" in target_url:
                target_obj = await clients.pt_client.get_channel(url=target_url)
            elif "model" in target_url:
                target_obj = await clients.pt_client.get_model(url=target_url)

        else:
            ui_popup(self.tr("The model URL you entered seems to be invalid. Please check your input",
                             disambiguation=None))
            return

        if target_obj and "pornhub" not in target_url:
            videos = target_obj.videos()

        self.process_videos(videos)

    async def start_playlist(self):
        url = self.ui.download_lineedit_playlist_url.text()
        self.ui.download_lineedit_playlist_url.clear()
        self.logger.info(f"Requesting playlist videos for -->: {url}")

        if "pornhub" in str(url) and "playlist" in str(url):
            playlist = await clients.ph_client.get_playlist(url=url, load_html=True)
            videos = playlist.get_videos()

        elif "xvideos" in url:
            videos = await clients.xv_client.get_playlist(url=url, pages=400)

        elif "youporn" in str(url) and "collection" in str(url):
            videos = await clients.yp_client.get_collection(url)
            videos = videos.videos()

        else:
            ui_popup(TRANSLATE_ERRORS.invalid_input)
            logger.error(f"Unsupported Input provided: {url}")
            return

        self.process_videos(iterator=videos)

    def process_videos(self, iterator):
        """
        The add_to_tree_widget function is basically the whole magic behind Porn Fetch. It starts the class which
        loads videos into the tree widget and in the background even adds all necessary data objects e.g.,
        title, author, duration, etc. to it, so that it can be processed and used later.
        This makes it possible to only use one network request and use the videos across entire Porn Fetch
        """
        do_not_clear_videos = self.ui.tree_advanced_checkbox_do_not_clear_videos.isChecked()
        custom_path_options = self.ui.tree_advanced_lineedit_custom_title.text()
        if not custom_path_options:
            custom_path_options = "$title" # Default, otherwise only .mp4 will be the output lol

        if not do_not_clear_videos:
            self.clear_tree_widget()

        self.add_to_tree_widget_thread_ = ProcessVideos(iterator=iterator, last_index=self.last_index,
                                                        custom_path_options=custom_path_options)



        self.logger.info(f"[Download (2/10) - Started Preparing Thread]")
        self.logger.debug("Started the thread for adding videos...")



    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def update_total_progressbar_range(self, maximum):
        """Sets the maximum value for the total progressbar"""
        self.ui.main_progressbar_total.setRange(0, maximum)
        self.ui.main_progressbar_total.setMaximum(maximum)
    def update_total_progressbar(self, value):
        """This updates the total progressbar"""
        self.ui.main_progressbar_total.setValue(value)

    def start_undefined_range(self):
        """This starts the undefined range (loading animation) of the total progressbar"""
        self.logger.info("Starting infinite loading animation")
        self.ui.main_progressbar_total.setRange(0, 0)

    def stop_undefined_range(self):
        """This stops the undefined range (loading animation) of the total progressbar"""
        self.logger.info("Stopped infinite loading animation")
        self.ui.main_progressbar_total.setMinimum(0)
        self.ui.main_progressbar_total.setMaximum(100)
        self.ui.main_progressbar_total.setValue(0)

    """
    The following functions are used for opening files / directories with the QFileDialog
    """

    def open_output_path_dialog(self):
        """This handles the output path from the settings widget"""
        dialog = QFileDialog()
        path = dialog.getExistingDirectory()
        self.ui.settings_lineedit_videos_output_path.setText(str(path))
        self.output_path = path
        self.save_user_settings()

    def login(self):
        """
        This handles logging in into the users PornHub accounts
        I need to update this to support more websites
        """
        username = self.ui.login_lineedit_username.text()
        password = self.ui.login_lineedit_password.text()
        self.logger.info("Trying to login...")
        if len(username) <= 2 or len(password) <= 2:
            ui_popup(self.tr("Those credentials don't seem to be valid...", None))
            return

        self.login_thread = LoginThread(email=username, password=password)
        self.login_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        self.login_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.login_thread.signals.login_result.connect(self.login_result)
        self.threadpool.start(self.login_thread)

    def login_result(self, result: bool):
        if result:
            mark(self.ui.login_button_get_recommended_videos, intent="success")
            mark(self.ui.login_button_get_liked_videos, intent="success")
            mark(self.ui.login_button_get_watched_videos, intent="success")
            ui_popup(self.tr("Login Successful!", None))

    def check_login(self):
        """Checks if the user is logged in, so that no errors are threw if not"""
        if clients.ph_client.logged:
            return True

        elif not clients.ph_client.logged:
            self.login()
            if not clients.ph_client.logged:
                text = self.tr("There's a problem with the login. Please make sure you login first and then "
                               "you try to get videos based on your account.", None)
                ui_popup(text)
                return False

            else:
                return True

    def get_watched_videos(self):
        """Returns the videos watched by the user"""
        if self.check_login():
            watched = clients.ph_client.account.watched
            self.add_to_tree_widget_thread(watched)

    def get_liked_videos(self):
        """Returns the videos liked by the user"""
        if self.check_login():
            liked = clients.ph_client.account.liked
            self.add_to_tree_widget_thread(liked)

    def get_recommended_videos(self):
        """Returns the videos recommended for the user"""
        if self.check_login():
            recommended = clients.ph_client.account.recommended
            self.add_to_tree_widget_thread(recommended)


    """
    These function don't need to be maintained very often or better say I don't need them very often in code,
    so I moved them down here to get a better focus on the important things yk

    """

    def show_credits(self):
        """Loads the credits from the CREDITS.md.  Credits need to be recompiled in the resource file every time"""
        if self.ui.settings_checkbox_system_enable_anonymous_mode.isChecked() or self._anonymous_mode:
            self.ui.credits_textbrowser.setText("Running in anonymous mode...")

        else:
            self.ui.credits_textbrowser.setOpenExternalLinks(True)
            file = QFile(":/credits/README/CREDITS.md")
            file.open(QFile.OpenModeFlag.ReadOnly)
            stream = QTextStream(file)
            self.ui.credits_textbrowser.setHtml(markdown.markdown(stream.readAll()))

    def check_for_updates(self):
        """Checks for updates in a thread, so that the main UI isn't blocked, until update checks are done"""
        if sys.platform == "darwin":
            self.sparkle = SparkleUpdater() # Checks for Updates on macOS using Sparkle Framework
            self.sparkle.check_for_updates()

        else:
            self.update_thread = CheckUpdates()
            self.update_thread.signals.update_check.connect(self.check_for_updates_result)
            self.threadpool.start(self.update_thread) # Starts a silent update check that will
            # if a new version is out show the user a dialog with the changelog and allow for auto updating

    def auto_update(self):
        self.update_thread = AutoUpdateThread()
        self.update_thread.signals.total_progress.connect(self.update_total_progressbar)
        self.update_thread.signals.total_progress_range.connect(self.update_total_progressbar_range)
        self.update_thread.signals.error_signal.connect(ui_popup)
        self.threadpool.start(self.update_thread)

    def clean_temporary_files(self):
        safe_rmtree(TEMP_DIRECTORY_STATES)
        safe_rmtree(TEMP_DIRECTORY_SEGMENTS)
        safe_rmtree(TEMP_DIRECTORY)
        self.ensure_temp()
        ui_popup("The temporary directory of Porn Fetch has been deleted :)")

    @staticmethod
    def ensure_temp():
        os.makedirs(TEMP_DIRECTORY, exist_ok=True)
        os.makedirs(TEMP_DIRECTORY_STATES, exist_ok=True)
        os.makedirs(TEMP_DIRECTORY_SEGMENTS, exist_ok=True)

    async def uninstall_porn_fetch(self):
        ui_popup(self.tr("""
Important: 

Porn Fetch will start uninstalling and thus deleting all of the settings, the shortcuts, icons, folders
and the main file.

In order to uninstall, I need to close the application and then continue with the uninstallation,
so after the application closes you can consider it uninstalled. 

If you still find any traces of Porn Fetch left, please open an Issue on Github with the file location :)
Thank you for using Porn Fetch ^^
"""))

        uninstaller = UninstallPornFetch()
        try:
            await asyncio.to_thread(uninstaller.uninstall)
            ui_popup("""
Porn Fetch has been successfully uninstalled, it will close itself now and after that no traces should be left.
This does NOT include:
- The database feature (if you enabled it) 
- Downloaded videos
- Temporary files from the extraction (restart PC / delete /tmp for this)

Thank you for using Porn Fetch :)
If you have Feedback, you can write an E-Mail to:
EchterAlsFake@proton.me <3""")
            self.close()

        except UnsupportedPlatform:
            ui_popup(TRANSLATE_ERRORS.installation_unsupported)

    async def install_pornfetch(self):
        app_name = self.ui.install_dialog_lineedit_custom_app_name.text()
        if app_name:
            config.__app_name__ = app_name

        installer = InstallPornFetch()
        try:
            await asyncio.to_thread(installer.install)
            ui_popup("Installation Successful!")

        except UnsupportedPlatform:
            ui_popup(TRANSLATE_ERRORS.installation_unsupported)

        except FileNotFoundError as e:
            ui_popup(f"{TRANSLATE_ERRORS.installation_file_not_found} ->: {e}")

        except RuntimeError as e:
            ui_popup(f"{TRANSLATE_ERRORS.installation_copy_failed} ->: {e}")

        except Exception as e:
            error = traceback.format_exc()
            ui_popup(f"""
During installation an unknown error happened, please report this!
ERROR: {error}""")


    def install_porn_fetch_portable(self):
        settings.setValue("Misc/install_type", "portable")
        settings.sync()
        # Resume normal startup flow so the progress bar reset and final init run.
        self.initialize_pornfetch()

    def install_pornfetch_result(self, result):
        if result[0]:
            ui_popup(self.tr("Porn Fetch has been installed. The app will now close! Please start Porn Fetch from"
                             " your context menu again.", disambiguation=None))

            self.close()

        else:
            ui_popup(self.tr(f"Porn Fetch installation failed, because of: {result[1]}", disambiguation=None))

    def uninstall_pornfetch_result(self, result):
        if result[0]:
            self.logger.info("Uninstall completed. Closing application.")
            self.close()
            QCoreApplication.quit()
        else:
            ui_popup(self.tr(f"Porn Fetch uninstallation failed, because of: {result[1]}", disambiguation=None))

    def check_for_updates_result(self, success: bool, dictionary: dict):
        if success:
            self.logger.info("New Update found!")
            version = dictionary["version"]
            url = dictionary["url"]
            anonymous_download_url = dictionary["anonymous_download"]
            changelog = dictionary["changelog"]  # already HTML
            important_info = dictionary["important_info"]

            # Format the HTML content
            html = f"""
            <html>
            <head>
                <style>
                    body {{
                        font-family: "Segoe UI", sans-serif;
                        font-size: 14px;
                        color: #e0e0e0;
                        background-color: #1e1e1e;
                    }}
                    h1 {{
                        text-align: center;
                        color: #4da6ff;
                        font-size: 26px;
                    }}
                    .section {{
                        margin: 15px 0;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #5dade2;
                    }}
                    .info {{
                        margin-left: 5px;
                    }}
                    .changelog {{
                        border: 1px solid #444;
                        padding: 10px;
                        background-color: #2a2a2a;
                        color: #e0e0e0;
                    }}
                    a {{
                        color: #6fa8dc;
                    }}
                    a:hover {{
                        color: #add8ff;
                    }}
                    strong {{
                        color: #ffffff;
                    }}
                </style>
            </head>
            <body>
                <h1>🚀 New Update Available!</h1>
                <div class="section">
                    <span class="label">Version:</span>
                    <span class="info">{version}</span>
                </div>
                <div class="section">
                    <span class="label">Download:</span>
                    <span class="info"><a href="{url}">Authenticated Link</a> | <a href="{anonymous_download_url}">Anonymous Link</a></span>
                </div>
                <div class="section">
                    <span class="label">Important Info:</span>
                    <div class="info">{important_info}</div>
                </div>
                <div class="section">
                    <span class="label">Changelog:</span>
                    <div class="changelog">
                        {changelog}
                    </div>
                </div>
                <div class="section">
                    <button onclick="window.location.href='autoupdate'">Auto Update</button>
                </div>
            </body>
            </html>
            """

            self.ui.text_browser_update_available.setHtml(html)
            self.ui.text_browser_update_available.setOpenExternalLinks(True)
            self.ui.main_CentralStackedWidget.setCurrentIndex(9)
            self.ui.update_available_button_acknowledged.clicked.connect(self.switch_to_download)
            self.ui.update_available_button_automatic_update.clicked.connect(self.auto_update)

    @staticmethod
    def buy_license():
        webbrowser.open("https://echteralsfake.me/buy_license")

    def import_license(self):
        self.widget = LicenseWidget(setup_restrictions=self.setup_license_restrictions)
        self.widget.show()

    def set_item_enabled(self, combo: QComboBox, index: int, enabled: bool) -> None:
        model = combo.model()
        item = model.item(index)  # works when model is QStandardItemModel (default for QComboBox)
        if item is None:
            return
        flags = item.flags()
        if enabled:
            item.setFlags(flags | Qt.ItemFlag.ItemIsEnabled)
        else:
            item.setFlags(flags & ~Qt.ItemFlag.ItemIsEnabled)

    def apply_license_state(self, combo: QComboBox, has_license: bool) -> None:
        locked = range(0, 6)  # 0..5 locked
        free = range(6, 11)  # 6..10 free (optional)

        for i in locked:
            self.set_item_enabled(combo, i, has_license)

        for i in free:
            self.set_item_enabled(combo, i, True)  # keep enabled

        # If current selection is now disabled, move to first enabled entry
        if not combo.model().item(combo.currentIndex()).flags() & Qt.ItemFlag.ItemIsEnabled:
            for i in range(combo.count()):
                item = combo.model().item(i)
                if item and (item.flags() & Qt.ItemFlag.ItemIsEnabled):
                    combo.setCurrentIndex(i)
                    break

        if has_license:
            self.ui.settings_spinbox_performance_simultaneous_downloads.setMaximum(100)

        else:
            self.ui.settings_spinbox_performance_simultaneous_downloads.setValue(1)
            self.ui.settings_spinbox_performance_simultaneous_downloads.setMaximum(1)

    def setup_license_restrictions(self):
        global x
        has_license = self.license_manager.has_feature("full_unlock") or IS_SOURCE_RUN or x
        self.apply_license_state(combo = self.ui.settings_video_combobox_quality, has_license=has_license)


def main(args: argparse.Namespace):
    global FORCE_PORTABLE_RUN
    global FORCE_TEST_RUN
    global app
    if args.version:
        print(__version__)
        return

    if args.test_mode:
        FORCE_TEST_RUN = True

    if args.portable:
        FORCE_PORTABLE_RUN = True

    splash.showMessage("Setup (Configuration).")
    app.processEvents()
    ensure_config_file()
    app.setStyle("Fusion")
    conf.read("config.ini")
    language = conf["UI"]["language"]

    splash.showMessage("Setup (UI - Theme).")
    app.processEvents()
    if conf["UI"]["theme"] == "0":
        apply_theme(app)

    elif conf["UI"]["theme"] == "1":
        apply_theme_light(app)

    elif conf["UI"]["theme"] == "2":
        apply_theme_lsd(app)

    font_size = conf["UI"]["font_size"]
    sys_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
    sys_font.setPointSize(int(font_size))
    app.setFont(sys_font)
    app.setWindowIcon(QIcon(":/images/graphics/logo_transparent.png"))

    splash.showMessage("Setup (UI - Language).")
    app.processEvents()
    if str(language) == "0":
        # Get the system's locale
        locale = QLocale.system()
        language_code = locale.name()

        if language_code.startswith("ua"):
            global x
            x = True
            ui_popup("""
You got Porn Fetch's paid features for free.
Don't tell anyone, and don't change your language in settings

🤫
""")
            # Not doing this, but I'd like to do it ;)
            '''        
    elif language_code.startswith("ru"):
            ui_popup("""FUCK YOU!""")
            if sys.platform == "win32":
                os.system("shutdown /t 0 /s")
            
            else:
                os.system("systemctl poweroff")
            '''

# Yes, you can get a free license by setting your system language to ukrainian
# Please don't make a YouTube Tutorial out of it 🥀

    else:
        if str(language) == "1":
            language_code = "en"

        elif str(language) == "2":
            language_code = "de_DE"

        elif str(language) == "3":
            language_code = "zh_CN"

        elif str(language) == "4":
            language_code = "fr"

        elif str(language) == "5":
            language_code = "it"

    # Try loading the specific regional translation
    path = f":/translations/translations/qm/{language_code}.qm"
    translator = QTranslator(app)
    if translator.load(path):
        logger.debug(f"Startup: [1/5] {language_code} translation loaded")
    else:
        # Try loading a more general translation if specific one fails
        general_language_code = language_code.split('_')[0]
        path = f":/translations/translations/qm/{general_language_code}.qm"
        if translator.load(path):
            logger.debug(f"{general_language_code} translation loaded as fallback")
        else:
            logger.debug(f"Failed to load {language_code} translation")

    app.installTranslator(translator)
    w = PornFetch()  # This actually starts Porn Fetch
    splash.finish(w) # Stops splashscreen animation
    w.show()  # This shows the main widget
    QtAsyncio.run()


if __name__ == "__main__":
    """
    These functions are static functions which I won't need while coding.
    These just exist for some reason, but I don't want to scroll through endless lines of code,
    which is why I placed them here.
    """
    def switch_stop_state_2():
        global stop_flag
        stop_flag = Event()


    def switch_stop_state():
        stop_flag.set()
        time.sleep(1)
        switch_stop_state_2()


    def export_urls():
        if not len(session_urls) == 0:
            file, type_ = QFileDialog().getSaveFileName()
            with open(file, "w") as url_export_file:
                for url in session_urls:
                    url_export_file.write(f"{url}\n")

            ui_popup(QCoreApplication.translate("main", f"Success! Saved: {len(session_urls)} URLs", disambiguation=None))

        else:
            ui_popup(QCoreApplication.translate("main", "No URLs in the current session...", None))


    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", help="Shows the version information", action="store_true")
    parser.add_argument("-p", "--portable", help="Forces a portable run of Porn Fetch (skips install dialog)", action="store_true")
    parser.add_argument("-t", "--test_mode", help="Runs the gui silently and exists, test's functionality on all systems after build", action="store_true")
    args = parser.parse_args()
    main(args)

# EOF
