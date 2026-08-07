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
from string import Template
from PySide6.QtWidgets import QApplication, QSizePolicy

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Dark"

app = QApplication(sys.argv)

# macOS Setup...
if sys.platform == "darwin":
    from src.backend.macos_setup import macos_setup
    from src.backend.update_service import SparkleUpdater
    macos_setup()
    # Handles Sparkle Updates + macOS Installation

# Necessary imports for splashscreen
from PySide6.QtGui import QPixmap
from src.frontend.UI.splashscreen import ModernSplashScreen

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
import re
import time
import uuid
import logging
import asyncio
import argparse
import markdown
import traceback
import webbrowser

from pathlib import Path
from datetime import datetime
from threading import Event
from asyncstdlib import islice, chain
from typing import AsyncGenerator, AsyncIterator



splash.showMessage("Importing (PySide6).")
app.processEvents()
# Qt / PySide6 related imports
import PySide6.QtAsyncio as QtAsyncio # Needed because porn fetch's network backend is now async since v3.9
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlEngine
from PySide6.QtGui import QIcon, QFontDatabase, QShortcut, QKeySequence
from PySide6.QtCore import (QTextStream, QLocale, QSize, QUrl, Signal, QFile, Slot,
                            QTranslator, QCoreApplication, QStandardPaths, QObject, Qt)
from PySide6.QtWidgets import (QButtonGroup, QFileDialog, QHeaderView, QTreeWidgetItem, QPushButton,
                               QInputDialog, QMainWindow, QComboBox)


splash.showMessage("Importing (Backend).")
app.processEvents()
# Backend imports
from src.backend import clients # Singleton instance for the client objects (really important)
import src.backend.config as config
import src.backend.shared_functions as shared_functions
from src.backend.config import (__version__, IS_SOURCE_RUN, TEMP_DIRECTORY,
                                TEMP_DIRECTORY_STATES, TEMP_DIRECTORY_SEGMENTS, app_settings)
from src.backend.shared_gui import (ui_popup, Signals,
                                    available_title_formatting_options)
from src.backend.helper_functions import (safe_rmtree, make_debug_log)
from src.backend.update_service import CheckUpdates
from src.backend.installation import InstallPornFetch
from src.backend.uninstallation import UninstallPornFetch
from src.backend.errors import (UnsupportedPlatform, AppNetworkError, AppNotFoundError,
                                AppBotBlocked, safe_api_call)
from src.backend.download_manager import DownloadManager, VideoObject, VideoFilters

splash.showMessage("Importing (Frontend).")
app.processEvents()
# Frontend imports
from src.frontend.UI.ui_form_main_window import Ui_PornFetch_UI
from src.frontend.UI.custom_combo_box import ComboPopupFitter, make_quality_combobox
from backend.theme_manager import (apply_theme, apply_theme_light, mark, install_focus_outline,
                                   pretty_combo)
from src.frontend.translations.strings import (TRANSLATE_MAIN, TRANSLATE_PAGE_DOWNLOAD, TRANSLATE_PAGE_LOGIN,
                                              TRANSLATE_PAGE_SETTINGS, TRANSLATE_ERRORS)


splash.showMessage("Importing (APIs).")
app.processEvents()

# Errors from different APIs
from base_api.modules.errors import (ProxySSLError, InvalidProxy, AccessDeniedError, BotProtectionDetected,
                                     SecurityAbort, RateLimitError, ChallengeMathError, DataNotLoadedError)
from pornhub_api.modules.errors import VideoDisabled, GifPendingReview


splash.showMessage("Importing (AV - FFMPEG).")
app.processEvents()

try:
    from av import open as av_open  # Don't ask
    from av.audio.resampler import AudioResampler  # Don't ask
    FORCE_DISABLE_AV = False

except Exception:
    FORCE_DISABLE_AV = True

qml_engine = QQmlEngine()
qml_engine.rootContext().setContextProperty("appSettings", app_settings)
FORCE_PORTABLE_RUN: bool = False # Holds a value for argparse later (see main function)
total_segments: int = 0 # Total segments kept in a queue (for total progress tracking)
downloaded_segments: int = 0 # Amount of segments that have been downloaded (for total progress tracking)
total_downloaded_videos: int = 0  # All videos that actually successfully downloaded
session_urls: list = []  # This list saves all URLs used in the current session. Used for the URL export function (CTRL + E)
logger = shared_functions.configure_app_logging(logger_name="Porn Fetch - [MAIN]", log_file="PornFetch.log", level=logging.DEBUG)
license_storage_path: str = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation), "pornfetch.license")
last_index = 0 # Tracks the last index of the tree widget in case the user does not have auto-clear enabled
x: bool = False # Don't ask (this is a secret ;)
w = None




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
        self.settings = None
        self.last_update_time = time.time()
        self.signals = Signals()
        self.signals.error_signal.connect(ui_popup)
        self.download_manager = DownloadManager() # Used to track all videos
        #self.download_manager.video_added.connect() # TODO

        self.update_app_font(app_settings.font_size)
        app_settings.fontSizeChanged.connect(self.update_app_font)
        app_settings.themeChanged.connect(self.theme_changed)
        self.ui = Ui_PornFetch_UI()
        self.ui.setupUi(self)
        self.logger = shared_functions.configure_app_logging(logger_name="Porn Fetch - [PornFetch]", log_file="PornFetch.log", level=logging.DEBUG)

        # Inject the Settings QML Widget
        settings_widget = QQuickWidget(qml_engine, self)
        settings_widget.rootContext().setContextProperty("appSettings", app_settings)
        settings_widget.setClearColor(Qt.GlobalColor.transparent)
        settings_widget.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        settings_widget.setSource(QUrl.fromLocalFile("src/frontend/UI/SettingsPage.qml"))
        self.ui.settings_vlayout_1.addWidget(settings_widget)


        self.last_index = 0  # Keeps track of the last index of videos added to the tree widget
        self._anonymous_mode = False
        #self.ensure_temp()
        #self._row = {} # Video ID -> dict of widgets + state
        self.load_style()
        #self._setup_modern_tabs()
        #self.load_strings()
        #self.license_manager = LicenseManager(storage_path=default_license_path(), public_key_b64=PUBLIC_KEY_B64)
        #self.setup_license_restrictions()

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
        #self.shortcuts()  # Activates the keyboard shortcuts
        self.logger.debug("Startup: [3/5] Initialized the User Interface")
        self.logger.debug("Startup: [4/5] Loaded the user settings")
        #self.download_scheduler = DownloadScheduler(self.app_config, self)
        #self.download_scheduler.worker_started.connect(self._wire_worker_signals)
        #self.progress_widgets = {}  # video_id -> {'label': QLabel, 'progressbar': QProgressBar}

        #if config.app_settings.update_checks:
        #    self.logger.info("Running update checks")
        #    self.check_for_updates()

        #if config.app_settings.anonymous_mode:
        #    self.logger.info("Enabling anonymous mode")
        #    self.anonymous_mode()

        #self.semaphore = asyncio.Semaphore(config.app_settings.parallel_downloads)
        #self.logger.debug("Startup: [5/5] OK")


        #self.initialize_pornfetch()

    """
    The following functions just switch the Stacked Widget to the different widgets
    """

    """Stacked Widget Main:"""



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

    async def start_model(self, url: str | None = None):
        """Starts the model downloads"""
        # 1. Clean up variable assignment
    async def start_playlist(self):
        url = self.ui.download_lineedit_playlist_url.text()
        self.ui.download_lineedit_playlist_url.clear()
        self.logger.info(f"Requesting playlist videos for -->: {url}")







    """
    The following functions are used to connect data between Threads and the Main UI
    """

    def on_error_message(self, message: str) -> None:
        ui_popup(message)

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


    @staticmethod
    def update_app_font(size: int):
        """Updates the global application font size."""
        font = app.font()
        font.setPointSize(size)
        app.setFont(font)

        for widget in app.allWidgets():
            widget.setFont(font)
            widget.update()

    @Slot(bool)
    def anonymous_mode_changed(self, val):
        ...

    @Slot(bool)
    def update_checks_changed(self, val):
        if val is True:
            self.check_for_updates() # Start an immediate update check, once user enabled it

    @Slot(float)
    def speed_limit_changed(self, val):
        clients.config.max_bandwidth_mb = val
        clients.refresh_clients(debug_mode=app_settings.debug_mode)


    @Slot(bool)
    def debug_mode_changed(self, val):
        if val:
            clients.refresh_clients(debug_mode=val)


    @Slot(int)
    def language_changed(self, val):
        ...

    @Slot(int)
    def theme_changed(self, val):
        apply_theme(app, val)


def main(args: argparse.Namespace):
    global FORCE_PORTABLE_RUN
    global FORCE_TEST_RUN
    global app, w
    if args.version:
        print(__version__)
        return

    if args.test_mode:
        FORCE_TEST_RUN = True

    if args.portable:
        FORCE_PORTABLE_RUN = True

    splash.showMessage("Setup (Configuration).")
    app.processEvents()
    app.setStyle("Fusion")
    language = config.app_settings.language

    splash.showMessage("Setup (UI - Theme).")
    app.processEvents()
    theme = config.app_settings.theme
    apply_theme(app, theme)

    font_size = config.app_settings.font_size
    sys_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
    sys_font.setPointSize(int(font_size))
    app.setFont(sys_font)
    app.setWindowIcon(QIcon(":/images/graphics/logo_transparent.png"))

    splash.showMessage("Setup (UI - Language).")
    app.processEvents()

    language_code = "en"

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



async def main() -> int:
    from PySide6.QtQml import QQmlApplicationEngine

    # This object owns the application-facing state and commands.
    #controller = AppController(parent=app)
    splash.finish(w)
    engine = QQmlApplicationEngine()

    # Pass the controller to the root QML object.
    #
    # Main.qml must contain:
    #     required property var backend
    #engine.setInitialProperties({
    #    "backend": controller,
    #})

    qml_file = Path(__file__).parent / "src" / "frontend" / "UI" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))

    # If QML contains a syntax/import error, no root object is created.
    if not engine.rootObjects():
        return 1

    return app.exec()


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
    #main(args)
    QtAsyncio.run(main())

# EOF
