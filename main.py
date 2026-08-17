import os
import multiprocessing as mp
import shutil
import sys
import tempfile
from pathlib import Path

import src.frontend.UI.resources # This may not seem to be used, but it needs to be imported!.
from src.backend.config import app_settings
from src.backend.theme_manager import ThemeManager
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from src.backend.splashscreen import SplashController


# --- MULTIPROCESSING SAFE SPLASH SCREEN ---
# We check if this is the main process. If so, we initialize the GUI.
# If it's a child process, we skip GUI initialization and set them to None.
is_main_process = mp.current_process().name == 'MainProcess'

app = None
engine = None
splash = None

if is_main_process:
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    splash_qml_path = Path(__file__).resolve().parent / "src" / "frontend" / "UI" / "SplashScreen.qml"
    splash = SplashController(engine, str(splash_qml_path))
    splash.splash_window.show()
    app.processEvents()

def update_splash(msg: str):
    """Safely updates the splash screen only if we are in the main GUI process."""
    if is_main_process and splash and app:
        splash.showMessage(msg)
        app.processEvents()


def style_app():
    core_style = app_settings.core_style
    is_dark = app_settings.dark_mode
    accent_color = app_settings.accent_color
    os.environ["QT_QUICK_CONTROLS_STYLE"] = core_style

    if sys.platform == "linux":
        os.environ["QT_QPA_PLATFORMTHEME"] = "xdgdesktopportal"

    if core_style == "Material":  # Material UI is modern and looks great
        os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Dark" if is_dark else "Light"
        os.environ["QT_QUICK_CONTROLS_MATERIAL_ACCENT"] = accent_color
        os.environ["QT_QUICK_CONTROLS_MATERIAL_PRIMARY"] = accent_color

    elif core_style == "Universal":  # Universal is just bad and shit, don't use it lmao
        os.environ["QT_QUICK_CONTROLS_UNIVERSAL_THEME"] = "Dark" if is_dark else "Light"
        os.environ["QT_QUICK_CONTROLS_UNIVERSAL_ACCENT"] = accent_color

def disable_nuitka_splash():
    # Turn off Nuitka's own Splash Screen (only relevant for onefile mode in binaries
    # Turn off Nuitka's native splash screen if it exists

    if "NUITKA_ONEFILE_PARENT" in os.environ:
        splash_filename = os.path.join(
            tempfile.gettempdir(),
            f"onefile_{int(os.environ['NUITKA_ONEFILE_PARENT'])}_splash_feedback.tmp"
        )
        if os.path.exists(splash_filename):
            os.unlink(splash_filename)



update_splash("Importing (General).")
import re
import time
import uuid
import logging
import asyncio
import argparse
import markdown
import traceback
import webbrowser
from string import Template
from datetime import datetime
from asyncstdlib import chain
from contextlib import aclosing
from rich_argparse import RichHelpFormatter
from typing import AsyncGenerator, AsyncIterator
from base_api.modules.config import IteratorConfig
from base_api import DownloadConfigHLS, DownloadConfigRAW
from base_api.modules.logger import configure_app_logging
from importlib.metadata import metadata, packages_distributions, version

update_splash("Importing (Qt)")
import PySide6.QtAsyncio as QtAsyncio # Needed because porn fetch's network backend is now async since v3.9
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlEngine
from PySide6.QtGui import QIcon, QFontDatabase, QShortcut, QKeySequence
from PySide6.QtCore import (QTextStream, QLocale, QSize, QUrl, Signal, QFile, Slot, Property,
                            QTranslator, QCoreApplication, QStandardPaths, QObject, Qt, QTimer)
from PySide6.QtWidgets import (QButtonGroup, QFileDialog, QHeaderView, QTreeWidgetItem, QPushButton,
                               QInputDialog, QMainWindow, QComboBox)

update_splash("Importing (Backend)")
from src.backend import clients # Singleton instance for the client objects (really important)
import src.backend.config as config
from src.backend.license_manager import LicenseManager
from src.backend.license_bridge import LicenseBridge
import src.backend.shared_functions as shared_functions
from src.backend.config import (__version__, IS_SOURCE_RUN, TEMP_DIRECTORY,
                                TEMP_DIRECTORY_STATES, TEMP_DIRECTORY_SEGMENTS, app_settings)
from src.backend.shared_gui import (ui_popup, Signals,
                                    available_title_formatting_options)
from src.backend.helper_functions import (safe_rmtree, make_debug_log)
from src.backend.update_service import AutoUpdater, CheckUpdates, SparkleUpdater
from src.backend.installation import InstallPornFetch
from src.backend.uninstallation import UninstallPornFetch
from src.backend.sni_proxy_manager import SNIProxyManager
from src.backend.errors import (UnsupportedPlatform, AppNetworkError, AppNotFoundError,
                                AppBotBlocked, safe_api_call)
from src.backend.tests import run_smoke_tests
from src.backend.download_manager import (
    DownloadManager,
    DownloadListModel,
    VideoFilters,
    VideoObject,
    quality_requires_premium,
)
from src.backend.database import DatabaseBridge
from src.backend.proxy_tester import test_proxy as run_proxy_test, validate_proxy_url
from curl_cffi.requests.exceptions import SSLError

update_splash("Importing (Frontend).")
# Frontend imports
from src.frontend.translations.strings import (TRANSLATE_MAIN, TRANSLATE_PAGE_DOWNLOAD, TRANSLATE_PAGE_LOGIN,
                                              TRANSLATE_PAGE_SETTINGS, TRANSLATE_ERRORS)


update_splash("Importing (APIs).")
# Errors from different APIs
from base_api.modules.errors import (ProxySSLError, InvalidProxy, AccessDeniedError, BotProtectionDetected,
                                     SecurityAbort, RateLimitError, ChallengeMathError, DataNotLoadedError)
from pornhub_api.modules.errors import VideoDisabled, GifPendingReview


update_splash("Importing (AV - FFMPEG).")

try:
    from av import open as av_open  # Don't ask
    from av.audio.resampler import AudioResampler  # Don't ask
    FORCE_DISABLE_AV = False

except Exception:
    FORCE_DISABLE_AV = True


stop_flag = asyncio.Event()
last_index = 0
sni_proxy_manager = SNIProxyManager(app_settings)


class DownloadStopEvent(asyncio.Event):
    """An asyncio stop flag whose identity survives API config copies."""

    def __deepcopy__(self, memo: dict[int, object]) -> "DownloadStopEvent":
        memo[id(self)] = self
        return self


def custom_unraisable_hook(unraisable):
  # Check if the error originates from the cffi callback or your specific issue
  if unraisable.exc_type is NotImplementedError:
    print(f"Caught target exception: {unraisable.exc_value}")
    ui_popup("""
CRITICAL ERROR!

I tried doing an asynchronous operation with curl-cffi, however, Qt Asyncio raised
an issue. 

You have probably not executed the patch script in src/scripts/patch_qtasyncio.py
and applied it to your virtual environment.

You need to run this script, otherwise this application will NOT work!""")


class ProcessVideos(QObject):
    error_signal = Signal(str)

    """
    This class is responsible for processing the videos in the background, loading the data, adjusting paths and
    handling errors
    """

    def __init__(self, iterator: AsyncGenerator, custom_path_options: str, video_filters: VideoFilters,
                 download_manager: DownloadManager, reverse_videos: bool, stop_flag: asyncio.Event,
                 origin_iterator_url: str | None = None, origin_iterator_name: str | None = None) -> None:
        super().__init__()
        self.iterator = iterator
        self.custom_path_options = custom_path_options
        self.download_manager = download_manager
        self.reverse_videos = reverse_videos
        self.stop_flag = stop_flag
        self.video_filters = video_filters
        self.origin_iterator_url = origin_iterator_url
        self.origin_iterator_name = origin_iterator_name
        self.max_attempts = app_settings.retries
        self.output_path = app_settings.output_path
        self.result_limit = app_settings.result_limit
        self.logger = configure_app_logging(logger_name="Porn Fetch - [ProcesVideos]", log_file="PornFetch.log", level=log_level)

    @staticmethod
    async def reverse_iterator(iterator: AsyncIterator):
        videos = []
        async for video in iterator:
            videos.append(video)  # This is very stupid, please don't use this „feature"!

        return reversed(videos)

    def process_filter(self, filters: VideoFilters, attributes: VideoObject) -> bool:
        # 1. Duration Filters
        if filters.duration_minimum is not None or filters.duration_maximum is not None:
            if filters.duration_minimum is not None and attributes.length < filters.duration_minimum:
                return False
            if filters.duration_maximum is not None and attributes.length > filters.duration_maximum:
                return False

        # 2. Regex Filters
        if filters.author_regex:
            if not re.search(filters.author_regex, attributes.author, re.IGNORECASE):
                return False

        if filters.title_regex:
            if not re.search(filters.title_regex, attributes.title, re.IGNORECASE):
                return False

        if filters.tags_regex:
            # Fails immediately if the video has no tags to match against
            if not attributes.tags:
                return False
            pattern = re.compile(filters.tags_regex, re.IGNORECASE)
            # Passes if at least one tag matches the regex
            if not any(pattern.search(tag) for tag in attributes.tags):
                return False

        # 3. Quality Filters (Evaluated based on the highest available quality)
        if filters.quality_minimum or filters.quality_maximum:
            max_quality = self._get_max_quality(attributes.qualities)

            if filters.quality_minimum:
                min_q = self._parse_quality(filters.quality_minimum)
                if max_quality < min_q:
                    return False

            if filters.quality_maximum:
                max_q = self._parse_quality(filters.quality_maximum)
                if max_quality > max_q:
                    return False

        # 4. Date Filters
        if filters.published_after:
            # .replace(tzinfo=None) safely handles timezone-aware datetimes for comparison
            after_date = datetime.fromisoformat(filters.published_after).replace(tzinfo=None)
            pub_date = attributes.publish_date.replace(tzinfo=None)
            if pub_date < after_date:
                return False

        if filters.published_before:
            before_date = datetime.fromisoformat(filters.published_before).replace(tzinfo=None)
            pub_date = attributes.publish_date.replace(tzinfo=None)
            if pub_date > before_date:
                return False

        # If it survives all the checks, all applied filters are True!
        return True

    @staticmethod
    def _parse_quality(quality_str: str) -> int:
        """Extracts the integer resolution from strings like '1080p', '720', '4K'."""
        if not quality_str:
            return 0

        # Simple handler for "4k" edge cases
        if quality_str.lower() == "4k":
            return 2160

        # Strips all non-digit characters (e.g., "1080p60" -> 108060, so we just grab the resolution part safely)
        # Assuming typical formats like "1080p", "720p"
        match = re.search(r'\d+', quality_str)
        return int(match.group()) if match else 0

    def _get_max_quality(self, qualities: list[str]) -> int:
        """Finds the highest resolution available in the list of qualities."""
        if not qualities:
            return 0
        parsed_qualities = [self._parse_quality(q) for q in qualities]
        return max(parsed_qualities)

    @staticmethod
    async def process_single_video(video_object: str | clients.AllowedVideoType) -> tuple[
        clients.AllowedVideoType, VideoObject]:
        video = await clients.get_video(video_object)
        video_attributes = await clients.load_video_attributes(video=video)
        return video, video_attributes

    def create_output_path(self, video_attributes: VideoObject, index: int, user_pattern: str) -> Path:
        base_path = self.output_path
        context = {
            "output_path": base_path,
            "author": video_attributes.author,
            "title": video_attributes.title,
            "video_id": video_attributes.video_id,
            "index": f"{index:02d}",  # Zero-padded index (01, 02, etc.)
            "publish_date": video_attributes.publish_date,
            "length": video_attributes.length,
        }

        template = Template(user_pattern)
        resolved_string = template.safe_substitute(context)
        resolved_path = Path(resolved_string).expanduser()
        uses_output_path = "$output_path" in user_pattern or "${output_path}" in user_pattern
        if not resolved_path.is_absolute() and not uses_output_path:
            resolved_path = Path(base_path).expanduser() / resolved_path
        return resolved_path

    async def start_processing(self):
        global last_index
        self.logger.info("Starting Processing of Iterator!")

        if self.reverse_videos:
            self.iterator = self.reverse_iterator(self.iterator)

        async with aclosing(self.iterator) as iterator:
            idx = 0
            async for video in iterator:
                if self.result_limit is not None and idx >= self.result_limit:
                    break

                last_error = None  # Keeps track of the

                if self.stop_flag.is_set():
                    return  # User hit the abort button

                try:
                    self.logger.debug(f"Current Index: {idx}")
                    video, video_object = await safe_api_call(self.process_single_video, video)
                    print(f"Video: {video}")

                    self.logger.info("Checking Filters...")
                    if self.process_filter(self.video_filters, video_object):
                        identifier = uuid.uuid4().hex
                        self.logger.info(f"Successfully received Video! [Identifier ->: {identifier}]")
                        output_path = self.create_output_path(video_object, idx, self.custom_path_options)

                        quality = app_settings.mappings_quality.get(int(app_settings.quality))
                        quality = quality if quality in video_object.qualities else (video_object.qualities[0] if video_object.qualities else "best")

                        video_object.output_path = output_path
                        video_object.identifier = identifier
                        video_object.index = idx
                        video_object.selected_quality = quality
                        video_object.source_video = video
                        video_object.origin_iterator_url = self.origin_iterator_url
                        video_object.origin_iterator_name = self.origin_iterator_name

                        self.download_manager.add_video(video_object)
                        last_index += 1

                # General Errors
                except AppNetworkError as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="""
                    A network error happened, I'll try retrying...""")
                    continue  # Maybe it solves by itself ;)

                except AppNotFoundError as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="""
                    I was trying to access a website, but turns out, it doesn't exist. Please verify if you entered
                    the correct URL.
    
                    If you are sure you did, please report this issue
                    """)

                    break  # If the resource is not there, it won't magically appear lmao

                except (VideoDisabled, GifPendingReview) as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="""
                    The Video / GIF seems to be disabled or pending a review! It can't be downloaded (yet) :(
                    """)
                    break

                except (SecurityAbort, ChallengeMathError, ChallengeMathError) as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="""
                    An error occurred while solving a challenge from PornHub, please report this immediately, I need to 
                    fix this quickly!""")
                    break

                except RateLimitError as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="""
                    You got rate limited by the server. I have already tried solving this, which didn't work. 
                    Please use a (different) proxy or VPN.""")
                    break

                except DataNotLoadedError as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message=f"""
                    If you see this I fucked up developing my API packages and you should immediately open an issue on 
                    GitHub lol""")
                    break

                except (AccessDeniedError, BotProtectionDetected, AppBotBlocked) as e:
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="""
                    The website denied access, probably because it detected you as a bot. Please report this, as I probably
                    need to update the headers. 
                    """)

                except Exception as e:
                    self.logger.error(f"UNHANDLED EXCEPTION in start_processing: {e}", exc_info=True)
                    last_error = make_debug_log(e=e, video_url=video.url, function="start_processing", user_message="An unexpected error occurred.")
                    break

                finally:
                    if last_error is not None:
                        self.error_signal.emit(last_error)

                idx += 1


class Backend(QObject):
    showMessage = Signal(str)
    downloadsChanged = Signal()
    updateAvailable = Signal("QVariantMap")
    updateProgress = Signal(int, int)
    updateStatus = Signal(str)
    proxyTestSucceeded = Signal(str, "QVariantMap")
    proxyTestFailed = Signal(str, str)
    proxySslError = Signal(str, str)
    proxyApplied = Signal(bool)
    shutdown_complete = Signal()

    def __init__(self):
        super().__init__()
        self._background_tasks: set[asyncio.Task[object]] = set()
        self._proxy_test_task: asyncio.Task[object] | None = None
        self._update_check_task: asyncio.Task[object] | None = None
        self._auto_update_task: asyncio.Task[object] | None = None
        self._download_tasks: dict[str, asyncio.Task[object]] = {}
        self._download_stop_events: dict[str, asyncio.Event] = {}
        self._download_semaphore = asyncio.Semaphore(max(1, int(app_settings.parallel_downloads)))
        self._license_bridge: LicenseBridge | None = None
        self.logger = configure_app_logging(logger_name="Porn Fetch - [Backend]", level=log_level, log_file="PornFetch.log")
        self._downloads_model = DownloadListModel(self, premium_access=self.has_premium_access)
        self.download_manager = DownloadManager(database_bridge=self.database_bridge)
        self.download_manager.video_added.connect(self.video_added_signal)
        self.auto_updater = AutoUpdater(self)
        self.auto_updater.updateProgress.connect(self.updateProgress)
        self.auto_updater.statusReport.connect(self.updateStatus)
        self.showMessage.connect(self.handle_message)
        app_settings.restartRequired.connect(self.setting_requires_restart)
        app_settings.moveDatabase.connect(self.database_changed)
        self._is_shutting_down = False
        self.ensure_temp()

        # ``clients`` creates its curl-cffi sessions during import. Apply all
        # saved request settings once the real GUI backend is initialized and
        # refresh them immediately when the content locale changes.
        self.load_clients()
        app_settings.reloadClients.connect(self.load_clients)
        QTimer.singleShot(0, clients.schedule_retired_session_cleanup)
        if sni_proxy_manager.last_error:
            QTimer.singleShot(
                0,
                lambda: ui_popup(
                    "SNI obfuscation failed to start and networking has been blocked.\n\n"
                    + str(sni_proxy_manager.last_error)
                ),
            )

    def has_premium_access(self) -> bool:
        return bool(self._license_bridge and self._license_bridge.isPremium)

    def set_license_bridge(self, license_bridge: LicenseBridge) -> None:
        self._license_bridge = license_bridge
        license_bridge.statusChanged.connect(self._enforce_quality_access)
        self._enforce_quality_access()

    def _enforce_quality_access(self) -> None:
        preferred_quality = app_settings.mappings_quality.get(app_settings.quality, "best")
        if not self.has_premium_access() and quality_requires_premium(preferred_quality):
            # 720p is the highest unrestricted entry in mappings_quality.
            app_settings.quality = 6
        else:
            self._downloads_model.enforce_quality_access()

    @Slot(int)
    def set_default_quality(self, quality_index: int) -> None:
        quality = app_settings.mappings_quality.get(quality_index)
        if quality is None:
            return
        if quality_requires_premium(quality) and not self.has_premium_access():
            self.logger.warning("Rejected locked default quality: %s", quality)
            return
        app_settings.quality = quality_index

    # Slots / Signals connected to the Configuration / Settings

    @Slot(bool)
    def toggle_anonymous_mode(self, value: bool) -> None:
        ...

    @Slot(bool)
    def toggle_update_checks(self, value: bool) -> None:
        ...

    @Slot()
    def check_for_updates(self) -> None:
        """Schedule a platform-appropriate check after Qt's event loop starts."""
        QTimer.singleShot(0, self._start_update_check)

    def _start_update_check(self) -> None:
        if sys.platform == "darwin":
            try:
                if not hasattr(self, "sparkle"):
                    self.sparkle = SparkleUpdater()
                self.sparkle.check_for_updates()
            except Exception:
                self.logger.exception("Could not start the Sparkle updater")
            return

        if self._update_check_task is not None and not self._update_check_task.done():
            return

        self._update_check_task = self._spawn(
            self._check_for_updates(),
            name="update-check",
        )

    async def _check_for_updates(self) -> None:
        update = await CheckUpdates.check()
        if update is None:
            return

        details = {
            "version": str(update.get("version", "")),
            "url": str(update.get("url", "")),
            "anonymous_download": str(update.get("anonymous_download", "")),
            "important_info": str(update.get("important_info", "")),
            "changelog": str(update.get("changelog", "")),
        }
        self.logger.info("New update found: %s", details["version"])
        self.updateAvailable.emit(details)

    @Slot()
    def auto_update(self) -> None:
        """Download and install the available update without blocking QML."""
        if IS_SOURCE_RUN:
            self.updateStatus.emit(
                "Update failed: Automatic updates are only available in installed builds. "
                "Use one of the download links instead."
            )
            return

        if self._auto_update_task is not None and not self._auto_update_task.done():
            return

        self._auto_update_task = self._spawn(
            self.auto_updater.run(),
            name="auto-update",
        )

    @Slot(int)
    def toggle_user_interface_language(self, value: int) -> None:
        ...

    @Slot()
    def setting_requires_restart(self) -> None:
        ui_popup("You have triggered an action that requires a restart before taking effect!")

    @Slot(str)
    def handle_message(self, message: str) -> None:
        ui_popup(text=message)

    @Slot(bool)
    def toggle_network_logging(self, value: bool) -> None:
        ...

    @Slot(str, str)
    def database_changed(self, old_path: str, new_path: str) -> None:
        old_database = Path(old_path).expanduser()
        new_database = Path(new_path).expanduser()

        if old_database == new_database:
            return

        new_database.parent.mkdir(parents=True, exist_ok=True)
        if not old_database.is_file():
            return

        if new_database.exists():
            ui_popup(
                "The selected database already exists, so the old database was not overwritten."
            )
            return

        shutil.move(str(old_database), str(new_database))
        ui_popup("Your old database has been moved to the new path.")

    @Slot()
    def cancel_fetching(self):
        stop_flag.set()

    @Slot()
    def clear_temporary_files(self):
        safe_rmtree(TEMP_DIRECTORY_STATES)
        safe_rmtree(TEMP_DIRECTORY_SEGMENTS)
        safe_rmtree(TEMP_DIRECTORY)
        self.ensure_temp()
        ui_popup("Temporary files (segments, state files) have been deleted!")

    @Slot()
    def reset_pornfetch(self):
        app_settings.reset()
        ui_popup("Porn Fetch has been reset to its default values. Please restart the application immediately.")

    @Slot()
    def handle_abort(self):
        pass

    @Slot(str)
    def install_pornfetch(self, app_name: str) -> None:
        if app_name:
            config.__app_name__ = app_name

        installer = InstallPornFetch()

        async def run_installation():
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

        self._spawn(run_installation(), name="installer-")

    @Slot()
    def uninstall_pornfetch(self):
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

        async def run_uninstaller():
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

            except UnsupportedPlatform:
                ui_popup(TRANSLATE_ERRORS.installation_unsupported)

        self._spawn(run_uninstaller(), name="uninstaller-")

    @Slot(object)
    def load_clients(self, _locale: str | None = None) -> None:
        clients.refresh_clients()

    def _spawn(self, coro, *, name: str) -> asyncio.Task:
        task = asyncio.create_task(coro, name=name)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_task_done)
        return task

    def _background_task_done(self, task: asyncio.Task) -> None:
        self._background_tasks.discard(task)

        if task.cancelled():
            self.logger.debug("Background task cancelled: %s", task.get_name())
            return

        try:
            task.result()
        except Exception:
            self.logger.exception(
                "Background task failed: %s",
                task.get_name(),
            )

    @Slot(str, bool)
    def testProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        """Test a proxy asynchronously without blocking the QML render thread."""
        if self._proxy_test_task is not None and not self._proxy_test_task.done():
            self._proxy_test_task.cancel()

        task = asyncio.create_task(
            self._test_proxy(proxy_url, verify_ssl),
            name="proxy-connectivity-test",
        )
        self._proxy_test_task = task
        self._background_tasks.add(task)
        task.add_done_callback(self._background_task_done)

    async def _test_proxy(self, proxy_url: str, verify_ssl: bool) -> None:
        try:
            result = await run_proxy_test(
                proxy_url,
                timeout=float(app_settings.timeout),
                verify_ssl=verify_ssl,
            )
        except asyncio.CancelledError:
            raise
        except ValueError as error:
            self.proxyTestFailed.emit(proxy_url, str(error))
        except SSLError as error:
            self.logger.warning(
                "Proxy SSL test failed with curl error code %s",
                error.code,
            )
            if verify_ssl:
                self.proxySslError.emit(
                    proxy_url,
                    self.tr(
                        "Warning: The SSL connection or certificate verification failed. "
                        "Continuing without verification "
                        "can expose your traffic and credentials to interception."
                    ),
                )
            else:
                self.proxyTestFailed.emit(
                    proxy_url,
                    self.tr("The SSL connection failed even with certificate verification disabled."),
                )
        except Exception as error:
            # Do not surface exception strings: curl errors can include a proxy
            # URL and therefore the user's password.
            self.logger.warning(
                f"Proxy connectivity test failed with %s {error}",
                type(error).__name__,
            )
            self.proxyTestFailed.emit(
                proxy_url,
                self.tr("Could not connect through this proxy. Check the address and credentials."),
            )
        else:
            self.proxyTestSucceeded.emit(proxy_url, result.as_qml_map())

    @Slot(str, bool)
    def applyProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        """Persist the tested proxy and rebuild all curl-cffi sessions."""
        if proxy_url:
            try:
                proxy_url = validate_proxy_url(proxy_url)
            except ValueError as error:
                self.proxyTestFailed.emit(proxy_url, str(error))
                return

        # Disabling a proxy always restores the secure default.
        verify_ssl = bool(verify_ssl) if proxy_url else True
        app_settings.apply_proxy_settings(proxy_url, verify_ssl)
        app_settings.sync()
        self.proxyApplied.emit(bool(proxy_url))

    @Slot(str, str)
    def update_video_quality(self, job_id: str, new_quality: str):
        if not self._downloads_model.set_video_quality(job_id, new_quality):
            self.logger.warning("Rejected unavailable or locked quality: %s", new_quality)
            return

        self.logger.info(f"User changed quality for {job_id} to {new_quality}")

        video = self.download_manager.get_video(job_id)
        if video:
            video.selected_quality = new_quality
            self.logger.info(f"Updated backend quality for: {job_id} to: {new_quality}")

    @Slot(str, bool)
    def set_video_selected(self, job_id: str, selected: bool) -> None:
        self._downloads_model.set_selected(job_id, selected)

    @Slot(bool)
    def select_all_videos(self, selected: bool) -> None:
        self._downloads_model.set_all_selected(selected)

    @Slot(bool)
    def download_selected_videos(self, cleanup_on_stop: bool = False) -> None:
        for job_id in self._downloads_model.selected_job_ids():
            self.download_video(job_id, cleanup_on_stop)

    @Slot(str, bool)
    def download_video(self, job_id: str, cleanup_on_stop: bool = False) -> None:
        job_id = str(job_id)
        existing_task = self._download_tasks.get(job_id)
        if existing_task is not None and not existing_task.done():
            return

        video = self._downloads_model.get_video(job_id)
        if video is None or video.source_video is None:
            self.logger.warning("Cannot download unknown video: %s", job_id)
            return

        is_resume = self._downloads_model.get_status(job_id) in {"cancelled", "failed"}
        stop_event = DownloadStopEvent()
        self._download_stop_events[job_id] = stop_event
        self._downloads_model.set_status(job_id, "queued")
        if not is_resume:
            self._downloads_model.update_progress(job_id, 0)

        task = self._spawn(
            self._download_video(job_id, video, stop_event, cleanup_on_stop),
            name=f"video-download-{job_id}",
        )
        self._download_tasks[job_id] = task
        task.add_done_callback(
            lambda completed_task, current_job_id=job_id: self._download_task_finished(
                current_job_id, completed_task
            )
        )

    @Slot(str, bool)
    def resume_download(self, job_id: str, cleanup_on_stop: bool = False) -> None:
        """Retry a row using its existing output and HLS resume state."""
        self.download_video(job_id, cleanup_on_stop)

    def _download_task_finished(self, job_id: str, task: asyncio.Task[object]) -> None:
        if self._download_tasks.get(job_id) is task:
            self._download_tasks.pop(job_id, None)
            self._download_stop_events.pop(job_id, None)

    @Slot(str)
    def stop_download(self, job_id: str) -> None:
        job_id = str(job_id)
        stop_event = self._download_stop_events.get(job_id)
        if stop_event is None:
            return
        stop_event.set()
        self._downloads_model.set_status(job_id, "stopping")

    async def _download_video(
        self,
        job_id: str,
        video: VideoObject,
        stop_event: asyncio.Event,
        cleanup_on_stop: bool,
    ) -> None:
        try:
            async with self._download_semaphore:
                if stop_event.is_set():
                    video.status = "cancelled"
                    self._downloads_model.set_status(job_id, "cancelled")
                    self.download_manager.update_status(job_id, "cancelled")
                    return

                if app_settings.processing_delay:
                    await asyncio.sleep(int(app_settings.processing_delay))
                    if stop_event.is_set():
                        video.status = "cancelled"
                        self._downloads_model.set_status(job_id, "cancelled")
                        self.download_manager.update_status(job_id, "cancelled")
                        return

                output_path = Path(video.output_path or video.title)
                if not output_path.suffix:
                    output_path = output_path.with_suffix(".mp4")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                video.output_path = output_path

                if output_path.exists() and app_settings.skip_existing_files:
                    self._downloads_model.update_progress(job_id, 100)
                    self._downloads_model.set_status(job_id, "completed")
                    self.download_manager.update_status(job_id, "completed")
                    return

                self._downloads_model.set_status(job_id, "downloading")

                def update_progress(position: int, total: int) -> None:
                    if not total:
                        return
                    percentage = max(0, min(100, int(position * 100 / total)))
                    self._downloads_model.update_progress(job_id, percentage)

                quality = video.selected_quality or "best"
                source_video = video.source_video
                raw_video_types = (clients.ep_Video, clients.pt_Video, clients.xf_Video)

                if isinstance(source_video, raw_video_types):
                    video.is_hls = False
                    configuration = DownloadConfigRAW(
                        quality=quality,
                        path=output_path,
                        callback=update_progress,
                        no_title=True,
                        stop_event=stop_event,
                        max_workers=app_settings.download_workers,
                        read_timeout=float(app_settings.timeout),
                        max_retries=app_settings.retries,
                    )
                    if isinstance(source_video, clients.ep_Video):
                        result = await source_video.download(configuration, mode="h264")
                    else:
                        result = await source_video.download(configuration)
                else:
                    video.is_hls = True
                    segment_dir = Path(TEMP_DIRECTORY_SEGMENTS) / job_id
                    segment_state_path = Path(TEMP_DIRECTORY_STATES) / job_id
                    configuration = DownloadConfigHLS(
                        quality=quality,
                        path=output_path,
                        callback=update_progress,
                        callback_remux=update_progress,
                        no_title=True,
                        stop_event=stop_event,
                        remux=not FORCE_DISABLE_AV,
                        segment_state_path=str(segment_state_path),
                        segment_dir=str(segment_dir),
                        return_report=True,
                        cleanup_on_stop=cleanup_on_stop,
                        keep_segment_dir=not cleanup_on_stop,
                    )
                    result = await source_video.download(configuration)

                report_status = getattr(result, "status", None)
                video.missing_segments = getattr(result, "missing", None)
                if stop_event.is_set() or report_status == "cancelled":
                    status = "cancelled"
                elif report_status == "missing" or result is False:
                    status = "failed"
                else:
                    status = "completed"

                video.status = status
                self._downloads_model.set_status(job_id, status)
                if status == "completed":
                    self._downloads_model.update_progress(job_id, 100)
                self.download_manager.update_status(job_id, status)
        except asyncio.CancelledError:
            video.status = "cancelled"
            self._downloads_model.set_status(job_id, "cancelled")
            self.download_manager.update_status(job_id, "cancelled")
            raise
        except Exception:
            video.status = "failed"
            self._downloads_model.set_status(job_id, "failed")
            self.download_manager.update_status(job_id, "failed")
            self.logger.exception("Download failed for %s", job_id)
            self.showMessage.emit(self.tr("The video download failed. Please check the log for details."))

    @Property(QObject, notify=downloadsChanged)
    def downloads(self):
        return self._downloads_model

    @Slot(object)
    def video_added_signal(self, video):
        quality = str(app_settings.mappings_quality.get(app_settings.quality))
        self._downloads_model.add_video(video=video, preferred_quality=quality)

    def on_download_progress(self, video_id: str, percentage: int):
        self._downloads_model.update_progress(video_id, percentage)

    @Slot(str, str, dict)
    def process_single_url(self, url: str, custom_options: str, filters: dict):
        """
        This function processes either a single Video or a Short depending on the platform.
        """
        print(f"Received Video / Short URL: {url}")
        filters = VideoFilters(**filters)
        asyncio.create_task(self._process_single_url(url=url, custom_options=custom_options, filters=filters))

    async def _process_single_url(self, url: str, custom_options: str, filters: VideoFilters):
        self.logger.info(f"[Download (1/10) - Preparing] -->: {url}")

        async def single_url_stream():
            yield url # Patch for the process_video class (look at it and you'll understand why I did this here)

        await self.process_videos(iterator=single_url_stream(), custom_options=custom_options, filters=filters)

    async def process_videos(self, iterator: AsyncIterator, custom_options: str, filters: VideoFilters,
                             origin_iterator_url: str | None = None,
                             origin_iterator_name: str | None = None):
        """
        The add_to_tree_widget function is basically the whole magic behind Porn Fetch. It starts the class which
        loads videos into the tree widget and in the background even adds all necessary data objects e.g.,
        title, author, duration, etc. to it, so that it can be processed and used later.
        This makes it possible to only use one network request and use the videos across entire Porn Fetch
        """
        if not custom_options:
            custom_options = "$title"  # Default, otherwise only .mp4 will be the output lol

        process_videos = ProcessVideos(iterator=iterator, custom_path_options=custom_options,
                                       video_filters=filters, download_manager=self.download_manager, reverse_videos=False,
                                       stop_flag=stop_flag, origin_iterator_url=origin_iterator_url,
                                       origin_iterator_name=origin_iterator_name)
        await process_videos.start_processing()

        self.logger.info(f"[Download (2/10) - Started Preparing Thread]")
        self.logger.debug("Started the thread for adding videos...")

    @Slot(str, str, dict)
    def process_model_url(self, url: str, custom_options: str, filters: dict):
        """
        This function loads all the videos of a model, channel, creator or user object and loads them into the
        ListView to allow the user to individually select the videos for download
        """
        print(f"Received Model URL: {url}")
        filters = VideoFilters(**filters)
        self._spawn(self._process_model_url(url=url, custom_options=custom_options, filters=filters), name="Deine-Mutter")

    async def _process_model_url(self, url: str, custom_options: str, filters: VideoFilters):
        videos = None
        target_obj = None

        # 2. Group by platform to eliminate redundant 'in' checks
        if "pornhub" in url:
            if "pornstar" in url or "model" in url:
                model_object = await clients.ph_client.get_pornstar(url)
                target_obj = model_object
                model_type = app_settings.model_videos

                if model_type == 0:
                    videos = chain(model_object.get_uploads(pages=30), model_object.get_videos(pages=30))
                elif model_type == 1:
                    videos = model_object.get_videos(pages=30)
                elif model_type == 2:
                    videos = model_object.get_uploads(pages=30)

            elif "user" in url or "channel" in url:
                target_obj = await clients.ph_client.get_channel(load_html=True, url=url)
                videos = target_obj.get_videos(pages=30)

        elif "eporner" in url:
            target_obj = await clients.ep_client.get_pornstar(url=url, load_html=True)

        elif "xnxx" in url:
            target_obj = await clients.xn_client.get_user(url=url)

        elif "youporn" in url:
            if "channel" in url:
                target_obj = await clients.yp_client.get_channel(url=url)
            else:
                target_obj = await clients.yp_client.get_pornstar(url=url)

        elif "xvideos" in url:
            if "model" in url or "pornstar" in url:
                target_obj = await clients.xv_client.get_pornstar(url=url)
            else:
                target_obj = await clients.xv_client.get_channel(url=url)

        elif "spankbang" in url:
            if "pornstar" in url:
                target_obj = await clients.sp_client.get_pornstar(url=url)
            elif "creator" in url:
                target_obj = await clients.sp_client.get_creator(url=url)
            elif "channel" in url:
                target_obj = await clients.sp_client.get_channel(url=url)

        elif "xhamster" in url:
            if "pornstars" in url:
                target_obj = await clients.xh_client.get_pornstar(url=url)
            elif "creators" in url:
                target_obj = await clients.xh_client.get_creator(url=url)
            elif "channels" in url:
                target_obj = await clients.xh_client.get_channel(url=url)

        elif "porntrex" in url:
            if "channel" in url:
                target_obj = await clients.pt_client.get_channel(url=url)
            elif "model" in url:
                target_obj = await clients.pt_client.get_model(url=url)

        else:
            self.showMessage.emit(self.tr("The model URL you entered seems to be invalid. Please check your input",
                             disambiguation=None))
            return

        if target_obj and "pornhub" not in url:
            if "eporner" in url and app_settings.strict_enforcement:
                videos = target_obj.videos(
                    pages=30,
                    iterator_config=IteratorConfig(load_specific_sources=("html",)),
                )
            else:
                videos = target_obj.videos(pages=30)

        print(f"Iterator: {type(videos)}")
        await self.process_videos(
            iterator=videos,
            custom_options=custom_options,
            filters=filters,
            origin_iterator_url=url,
            origin_iterator_name=self._iterator_display_name(target_obj, url, "model / channel"),
        )

    @Slot(str, str, dict)
    def process_playlist_url(self, url: str, custom_options: str, filters: dict):
        """
        This function loads a Playlist or Collection object and puts all videos again into a ListView
        """
        print(f"Received Playlist URL: {url}")
        filters = VideoFilters(**filters)
        self._spawn(self._process_playlist_url(url=url, custom_options=custom_options, filters=filters), name="Fortnite")

    async def _process_playlist_url(self, url: str, custom_options: str, filters: VideoFilters):
        source_obj = None
        if "pornhub" in str(url) and "playlist" in str(url):
            playlist = await clients.ph_client.get_playlist(url=url, load_html=True)
            source_obj = playlist
            videos = playlist.get_videos()

        elif "xvideos" in url:
            videos = await clients.xv_client.get_playlist(url=url, pages=400)

        elif "youporn" in str(url) and "collection" in str(url):
            source_obj = await clients.yp_client.get_collection(url)
            videos = source_obj.videos()

        else:
            self.showMessage.emit(TRANSLATE_ERRORS.invalid_input)
            self.logger.error(f"Unsupported Input provided: {url}")
            return

        await self.process_videos(
            iterator=videos,
            custom_options=custom_options,
            filters=filters,
            origin_iterator_url=url,
            origin_iterator_name=self._iterator_display_name(source_obj, url, "playlist / collection"),
        )

    @staticmethod
    def _iterator_display_name(iterator_object, url: str, source_kind: str) -> str:
        """Prefer an API-provided iterator name and never expose its URL in the UI."""
        if iterator_object is not None:
            for attribute in ("name", "title", "display_name", "username"):
                value = getattr(iterator_object, attribute, None)
                if value and not callable(value):
                    return str(value)

        platform_names = {
            "pornhub": "Pornhub",
            "eporner": "Eporner",
            "xnxx": "XNXX",
            "xvideos": "XVideos",
            "youporn": "YouPorn",
            "spankbang": "SpankBang",
            "xhamster": "xHamster",
            "porntrex": "PornTrex",
        }
        normalized_url = url.lower()
        platform = next((name for key, name in platform_names.items() if key in normalized_url), "Unknown")
        return f"{platform} {source_kind}"

    @Slot()
    def initiate_shutdown(self):
        """Called by QML when the user clicks the close button."""
        if self._is_shutting_down:
            return

        self._is_shutting_down = True
        self.logger.info("Application closing. Initiating async teardown...")
        # Spawn the cleanup routine as one final task
        asyncio.create_task(self._teardown_routine())

    async def _teardown_routine(self):
        """Safely cancel all tracked tasks and wait for them to close."""
        tasks_to_await = list(self._background_tasks)

        if self._proxy_test_task and not self._proxy_test_task.done():
            tasks_to_await.append(self._proxy_test_task)

        if tasks_to_await:
            self.logger.info(f"Cancelling {len(tasks_to_await)} background tasks...")

            # Send cancellation requests to all tasks
            for task in tasks_to_await:
                task.cancel()

            # Wait for all tasks to acknowledge cancellation and finish
            # return_exceptions=True prevents CancelledError from bubbling up and crashing this routine
            await asyncio.gather(*tasks_to_await, return_exceptions=True)
            self.logger.info("All background tasks stopped successfully.")

        await clients.close_all_clients()
        sni_proxy_manager.stop()

        # If DownloadManager handles downloads in separate C++ threads or
        # distinct processes, tell it to stop here too.
        # self.download_manager.stop_all()

        # Tell the Qt Event Loop to exit
        self.shutdown_complete.emit()

    @staticmethod
    def ensure_temp():
        os.makedirs(TEMP_DIRECTORY, exist_ok=True)
        os.makedirs(TEMP_DIRECTORY_STATES, exist_ok=True)
        os.makedirs(TEMP_DIRECTORY_SEGMENTS, exist_ok=True)


def main() -> None:
    mp.freeze_support()
    parser = argparse.ArgumentParser(
        prog=f"Porn Fetch v{__version__}",
        description="A source available Adult Archiver that respects your privacy.",
        formatter_class=RichHelpFormatter
    )

    parser.add_argument("--test", "-t", action="store_true", help="""
        Runs an automated Test of Porn Fetch where each supported website will be simulated with real network requests
        and loaded into the Graphical User Interface which will then be validated.

        This is recommended to run if you want to buy a license so that you can see the current state of the application
        before maybe buying something that doesn't work anymore.""")
    parser.add_argument("--version", "-v", action="store_true", help="Shows the current version of Porn Fetch")

    args = parser.parse_args()
    test_mode = False

    if args.version:
        print_runtime_version_info()
        sys.exit(0)

    if args.test:
        test_mode = True

    sys.unraisablehook = custom_unraisable_hook
    local_url = sni_proxy_manager.start()
    if local_url:
        print(f"SNI proxy route: {local_url}")

    global app, engine, splash

    # Initialize the app + organization values
    # The organization values handle settings, licenses etc, please do not change this :)
    app.setOrganizationName(config.__org_name__)
    app.setApplicationName(config.__app_name__)
    app.setApplicationVersion(config.__version__)
    app.setWindowIcon(QIcon("qrc:/images/graphics/logo.png"))

    app.styleHints().setColorScheme(Qt.ColorScheme.Dark if app_settings.dark_mode else Qt.ColorScheme.Light)

    app_font = app.font()
    app_font.setPointSize(app_settings.font_size)
    app.setFont(app_font)



    # Loads the theme e.g., Material UI / Fusion + dark / light theme
    saved_style = app_settings.core_style
    QQuickStyle.setStyle(saved_style)
    theme_manager = ThemeManager()

    # The backend instance handles the main logic, see class above
    backend_instance = Backend()

    # The test mode runs an automated test with the real QML / Backend environment, it tests basically everything
    if "--test" in sys.argv:
        exit_code = QtAsyncio.run(run_smoke_tests(backend=backend_instance, model=backend_instance._downloads_model), keep_running=False)
        raise SystemExit(exit_code)


    database_bridge = DatabaseBridge(parent=engine)
    # Database bridge is used for tracking the downloads / creating statistics (optional feature)

    # Download manager connects to QML to manage downloads and create the actual rows in the ListView
    download_manager = backend_instance.download_manager
    download_manager.video_added.connect(database_bridge.on_video_updated) # Writes to database (optional)
    download_manager.video_updated.connect(database_bridge.on_video_updated) # Updates existing entry (optional)

    storage_path = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)) / "license.lic"
    lic_manager = LicenseManager(public_key_b64=config.PUBLIC_KEY_B64, storage_path=storage_path)
    # Loads the license, if you have imported it before. Stores in APPDATA / .local/share

    bridge_instance = LicenseBridge(lic_manager) # License bridge connects QML code to Python
    backend_instance.set_license_bridge(bridge_instance)
    # Gives some context to QML so that QML can directly access certain things
    engine.rootContext().setContextProperty("bridge", bridge_instance)
    engine.rootContext().setContextProperty("backend", backend_instance)
    engine.rootContext().setContextProperty("databaseBridge", database_bridge)
    engine.rootContext().setContextProperty("themeManager", theme_manager)
    engine.rootContext().setContextProperty("appSettings", app_settings)

    splash.showMessage("Loading Window...")

    # 3. Resolve path to Main.qml relative to this script
    qml_file = Path(__file__).resolve().parent / "src" / "frontend" / "UI"/ "Main.qml"


    engine.load(QUrl.fromLocalFile(str(qml_file)))

    # 4. Check if QML loaded successfully
    if not engine.rootObjects():
        print("Failed to load QML file.")
        sys.exit(-1)

    splash.finish()
    QtAsyncio.run(handle_sigint=True) # sigint means that when someone presses CTRL+C it gets a clean exit



def get_imported_licenses():
  """Dynamically fetches packages, versions, and licenses
  of third-party libraries currently imported in memory for transparency reasons.
  """
  pkg_map = packages_distributions()

  # Get root names of all modules currently loaded in sys.modules
  loaded_modules = {mod.split('.')[0] for mod in sys.modules}

  results = []
  seen = set()

  for mod in sorted(loaded_modules):
    # Find matching installed distribution packages for this import name
    for dist in pkg_map.get(mod, []):
      if dist not in seen:
        seen.add(dist)
        try:
          meta = metadata(dist)
          ver = version(dist)
          # Some packages store full license text or short names
          lic = meta.get('License', 'Unknown')
          # Clean up line breaks if the metadata contains text blobs
          lic = ' '.join(lic.splitlines()) or 'Unknown'

          results.append({'Package': dist, 'Version': ver, 'License': lic})
        except Exception:
          pass
  return results


def print_runtime_version_info():
  """Prints a nicely formatted table of imported packages."""
  libs = get_imported_licenses()

  print(f'Python Interpreter: {sys.executable}')
  print(f'Python Version:     {sys.version.split()[0]}\n')

  print(f"{'Package':<25} {'Version':<15} {'License':<25}")
  print('=' * 65)
  for lib in libs:
    # Truncate license string slightly if it's overly verbose text
    lic_display = (
        lib['License'][:22] + '...'
        if len(lib['License']) > 25
        else lib['License']
    )
    print(f"{lib['Package']:<25} {lib['Version']:<15} {lic_display:<25}")
  print('=' * 65)



if __name__ == "__main__":
    main()
