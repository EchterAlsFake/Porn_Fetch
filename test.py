import os
import sys
import tempfile
from pathlib import Path
import src.frontend.UI.resources # This may not seem to be used, but it needs to be imported!.
from backend.config import app_settings
from src.backend.config import app_settings
from src.backend.theme_manager import ThemeManager
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication, QCursor

# Style must be applied before QML Application starts, otherwise they won't be applied
core_style = app_settings.core_style
is_dark = app_settings.dark_mode
accent_color = app_settings.accent_color
log_level = app_settings.log_level_map.get(app_settings.log_level)
os.environ["QT_QUICK_CONTROLS_STYLE"] = core_style

if core_style == "Material": # Material UI is modern and looks great
    os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Dark" if is_dark else "Light"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_ACCENT"] = accent_color
    os.environ["QT_QUICK_CONTROLS_MATERIAL_PRIMARY"] = accent_color

elif core_style == "Universal": # Universal is just bad and shit, don't use it lmao
    os.environ["QT_QUICK_CONTROLS_UNIVERSAL_THEME"] = "Dark" if is_dark else "Light"
    os.environ["QT_QUICK_CONTROLS_UNIVERSAL_ACCENT"] = accent_color


app = QGuiApplication(sys.argv)
app.setOrganizationName("EchterAlsFake")
app.setApplicationName("Porn Fetch")

engine = QQmlApplicationEngine()

from src.backend.splashscreen import SplashController

# Loading the Splashscreen and starting it
splash_qml_path = Path(__file__).resolve().parent / "src" / "frontend" / "UI" / "SplashScreen.qml"
splash = SplashController(engine, str(splash_qml_path))
splash.splash_window.show()
app.processEvents()

# Turn off Nuitka's own Splash Screen (only relevant for onefile mode in binaries
# Turn off Nuitka's native splash screen if it exists
if "NUITKA_ONEFILE_PARENT" in os.environ:
    splash_filename = os.path.join(
        tempfile.gettempdir(),
        f"onefile_{int(os.environ['NUITKA_ONEFILE_PARENT'])}_splash_feedback.tmp"
    )
    if os.path.exists(splash_filename):
        os.unlink(splash_filename)

splash.showMessage("Importing (General).")
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
from asyncstdlib import islice, chain
from typing import AsyncGenerator, AsyncIterator
from base_api.modules.logger import configure_app_logging

splash.showMessage("Importing (Qt)")
app.processEvents()

import PySide6.QtAsyncio as QtAsyncio # Needed because porn fetch's network backend is now async since v3.9
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlEngine
from PySide6.QtGui import QIcon, QFontDatabase, QShortcut, QKeySequence
from PySide6.QtCore import (QTextStream, QLocale, QSize, QUrl, Signal, QFile, Slot,
                            QTranslator, QCoreApplication, QStandardPaths, QObject, Qt)
from PySide6.QtWidgets import (QButtonGroup, QFileDialog, QHeaderView, QTreeWidgetItem, QPushButton,
                               QInputDialog, QMainWindow, QComboBox)

splash.showMessage("Importing (Backend)")
app.processEvents()

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


class ProcessVideos(QObject):
    error_signal = Signal(str)

    """
    This class is responsible for processing the videos in the background, loading the data, adjusting paths and
    handling errors
    """

    def __init__(self, iterator: AsyncGenerator, custom_path_options: str, max_attempts: int,
                 download_manager: DownloadManager, reverse_videos: bool, stop_flag: asyncio.Event, output_path: Path,
                 video_filters: VideoFilters, result_limit: int) -> None:
        super().__init__()
        self.iterator = iterator
        self.custom_path_options = custom_path_options
        self.max_attempts = max_attempts
        self.download_manager = download_manager
        self.reverse_videos = reverse_videos
        self.stop_flag = stop_flag
        self.output_path = output_path
        self.video_filters = video_filters
        self.result_limit = result_limit
        self.logger = configure_app_logging(logger_name="Porn Fetch - [ProcesVideos]", log_file="PornFetch.log", level=log_level)

    @staticmethod
    async def reverse_iterator(iterator: AsyncIterator):
        videos = []
        async for video in iterator:
            videos.append(video)  # This is very stupid, please don't use this „feature"!

        return videos.reverse()

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
        return Path(resolved_string).expanduser()

    async def start_processing(self):
        global last_index
        self.logger.info("Starting Processing of Iterator!")
        self.iterator = islice(self.iterator, self.result_limit)

        if self.reverse_videos:
            self.iterator = self.reverse_iterator(self.iterator)

        async for idx, video in shared_functions.aenumerate(self.iterator):
            last_error = None  # Keeps track of the

            if self.stop_flag.is_set():
                return  # User hit the abort button

            try:
                self.logger.debug(f"Current Index: {idx}")
                video, video_object = await safe_api_call(self.process_single_video, video)

                self.logger.info("Checking Filters...")
                if self.process_filter(self.video_filters, video_object):
                    identifier = uuid.uuid4().hex
                    self.logger.info(f"Successfully received Video! [Identifier ->: {identifier}]")
                    output_path = self.create_output_path(video_object, idx, self.custom_path_options)
                    video_object.output_path = output_path
                    video_object.identifier = identifier
                    video_object.index = idx

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

            finally:
                self.error_signal.emit(last_error)


class Backend(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str, str)
    def process_single_url(self, url: str, custom_options: str | None = None) -> bool:
        """
        This function processes either a single Video or a Short depending on the platform.
        """
        print(f"Received Video / Short URL: {url}")
        print(f"Custom Options: {custom_options}")





    @Slot(str, str)
    def process_model_url(self, url: str, custom_options: str | None = None) -> bool:
        """
        This function loads all the videos of a model, channel, creator or user object and loads them into the
        ListView to allow the user to individually select the videos for download
        """
        print(f"Received Model URL: {url}")

    @Slot(str, str)
    def process_playlist_url(self, url: str, custom_options: str | None = None) -> bool:
        """
        This function loads a Playlist or Collection object and puts all videos again into a ListView
        """
        print(f"Received Playlist URL: {url}")




def main():


    # --- 2. Inject Environment Variables for Styles ---
    # QML will read these automatically. No attached properties needed in QML!

    saved_style = app_settings.core_style
    QQuickStyle.setStyle(saved_style)
    theme_manager = ThemeManager()

    # 1. Instantiate backend object
    backend_instance = Backend()
    engine.rootContext().setContextProperty("backend", backend_instance)
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
    QtAsyncio.run(handle_sigint=True)


if __name__ == "__main__":
    main()