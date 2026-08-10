import os
import sys
import tempfile
from pathlib import Path
import src.frontend.UI.resources # This may not seem to be used, but it needs to be imported!.
from src.backend.config import app_settings
from src.backend.download_manager import DownloadListModel
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
log_level = app_settings.log_level_map.get(int(app_settings.log_level))
os.environ["QT_QUICK_CONTROLS_STYLE"] = core_style

if sys.platform == "linux":
    os.environ["QT_QPA_PLATFORMTHEME"] = "xdgdesktopportal"

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
import atexit
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
from typing import AsyncGenerator, AsyncIterator
from base_api.modules.logger import configure_app_logging

splash.showMessage("Importing (Qt)")
app.processEvents()

import PySide6.QtAsyncio as QtAsyncio # Needed because porn fetch's network backend is now async since v3.9
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtQml import QQmlEngine
from PySide6.QtGui import QIcon, QFontDatabase, QShortcut, QKeySequence
from PySide6.QtCore import (QTextStream, QLocale, QSize, QUrl, Signal, QFile, Slot, Property,
                            QTranslator, QCoreApplication, QStandardPaths, QObject, Qt)
from PySide6.QtWidgets import (QButtonGroup, QFileDialog, QHeaderView, QTreeWidgetItem, QPushButton,
                               QInputDialog, QMainWindow, QComboBox)

splash.showMessage("Importing (Backend)")
app.processEvents()

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
from src.backend.update_service import CheckUpdates, SparkleUpdater
from src.backend.installation import InstallPornFetch
from src.backend.uninstallation import UninstallPornFetch
from src.backend.sni_fragment_proxy_lite import FragmentingProxyConfig, FragmentingProxyProcess
from src.backend.sni_fragment_proxy_strict import StrictFragmentingProxyConfig, StrictFragmentingProxyProcess
from src.backend.errors import (UnsupportedPlatform, AppNetworkError, AppNotFoundError,
                                AppBotBlocked, safe_api_call)
from src.backend.download_manager import DownloadManager, VideoObject, VideoFilters
from src.backend.proxy_tester import test_proxy as run_proxy_test, validate_proxy_url
from curl_cffi.requests.exceptions import SSLError

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


stop_flag = asyncio.Event()
last_index = 0

def start_proxy_lite():
    proxy_config = FragmentingProxyConfig(
        listen_host="127.0.0.1",
        listen_port=0,
        upstream_proxy=app_settings.proxy
    )

    proxy_proces = FragmentingProxyProcess(proxy_config)
    local_url = proxy_proces.start()
    print(f"Fragmenting Proxy running at: {local_url}")
    atexit.register(proxy_proces.stop)
    return local_url


def start_proxy_strict():
    proxy_config = StrictFragmentingProxyConfig(
        listen_host="127.0.0.1",
        listen_port=0,
        upstream_proxy=app_settings.proxy
    )

    proxy_process = StrictFragmentingProxyProcess(proxy_config)
    local_url = proxy_process.start()
    print(f"[STRICT] Fragmenting Proxy running at: {local_url}")
    atexit.register(proxy_process.stop)
    return local_url




class ProcessVideos(QObject):
    error_signal = Signal(str)

    """
    This class is responsible for processing the videos in the background, loading the data, adjusting paths and
    handling errors
    """

    def __init__(self, iterator: AsyncGenerator, custom_path_options: str, video_filters: VideoFilters,
                 download_manager: DownloadManager, reverse_videos: bool, stop_flag: asyncio.Event) -> None:
        super().__init__()
        self.iterator = iterator
        self.custom_path_options = custom_path_options
        self.download_manager = download_manager
        self.reverse_videos = reverse_videos
        self.stop_flag = stop_flag
        self.video_filters = video_filters
        self.max_attempts = app_settings.retries
        self.output_path = app_settings.output_path
        self.result_limit = app_settings.result_limit
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
    showMessage = Signal(str, str, str)
    downloadsChanged = Signal()
    proxyTestSucceeded = Signal(str, "QVariantMap")
    proxyTestFailed = Signal(str, str)
    proxySslError = Signal(str, str)
    proxyApplied = Signal(bool)

    def __init__(self):
        super().__init__()
        self._background_tasks: set[asyncio.Task[object]] = set()
        self._proxy_test_task: asyncio.Task[object] | None = None
        self.logger = configure_app_logging(logger_name="Porn Fetch - [Backend]", level=log_level, log_file="PornFetch.log")
        self._downloads_model = DownloadListModel(self)
        self.download_manager = DownloadManager()
        self.download_manager.video_added.connect(self.video_added_signal)

        # ``clients`` creates its curl-cffi sessions during import, so apply a
        # previously saved proxy once the real GUI backend is initialized.
        if app_settings.proxy:
            clients.config.proxy = app_settings.proxy
            clients.config.verify_ssl = app_settings.proxy_ssl_verification
            clients.refresh_clients(debug_mode=app_settings.debug_mode)

    def _spawn(self, coro, *, name: str) -> None:
        task = asyncio.create_task(coro, name=name)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_task_done)

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
        app_settings.proxy = proxy_url
        app_settings.proxy_ssl_verification = verify_ssl
        app_settings.sync()
        clients.config.proxy = proxy_url or None
        clients.config.verify_ssl = verify_ssl
        clients.refresh_clients(debug_mode=app_settings.debug_mode)
        self.proxyApplied.emit(bool(proxy_url))

    @Slot(str, str)
    def update_video_quality(self, job_id: str, new_quality: str):
        self._downloads_model.set_video_quality(job_id, new_quality)
        self.logger.info(f"User changed quality for {job_id} to {new_quality}")

        video = self.download_manager.get_video(job_id)
        if video:
            video.selected_quality = new_quality
            self.logger.info(f"Updated backend quality for: {job_id} to: {new_quality}")

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

    async def process_videos(self, iterator: AsyncIterator, custom_options: str, filters: VideoFilters):
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
                                       stop_flag=stop_flag)
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
            videos = target_obj.videos(pages=30)

        print(f"Iterator: {type(videos)}")
        await self.process_videos(iterator=videos, custom_options=custom_options, filters=filters)

    @Slot(str, str, dict)
    def process_playlist_url(self, url: str, custom_options: str, filters: dict):
        """
        This function loads a Playlist or Collection object and puts all videos again into a ListView
        """
        print(f"Received Playlist URL: {url}")
        filters = VideoFilters(**filters)
        self._spawn(self._process_playlist_url(url=url, custom_options=custom_options, filters=filters), name="Fortnite")

    async def _process_playlist_url(self, url: str, custom_options: str, filters: VideoFilters):
        if "pornhub" in str(url) and "playlist" in str(url):
            playlist = await clients.ph_client.get_playlist(url=url, load_html=True)
            videos = playlist.get_videos()

        elif "xvideos" in url:
            videos = await clients.xv_client.get_playlist(url=url, pages=400)

        elif "youporn" in str(url) and "collection" in str(url):
            videos = await clients.yp_client.get_collection(url)
            videos = videos.videos()

        else:
            self.showMessage.emit(TRANSLATE_ERRORS.invalid_input)
            self.logger.error(f"Unsupported Input provided: {url}")
            return

        await self.process_videos(iterator=videos, custom_options=custom_options, filters=filters)



def main():


    # --- 2. Inject Environment Variables for Styles ---
    # QML will read these automatically. No attached properties needed in QML!

    saved_style = app_settings.core_style
    QQuickStyle.setStyle(saved_style)
    theme_manager = ThemeManager()

    # 1. Instantiate backend object
    backend_instance = Backend()
    storage_path = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)) / "EchterAlsFake" / "PornFetch" / "license.lic"
    lic_manager = LicenseManager(public_key_b64=config.PUBLIC_KEY_B64, storage_path=storage_path)
    bridge_instance = LicenseBridge(lic_manager)
    engine.rootContext().setContextProperty("bridge", bridge_instance)
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
    local_url = None

    if app_settings.sni_obfuscation:
        if app_settings.sni_obfuscation_strict:
            local_url = start_proxy_strict()

        elif app_settings.sni_obfuscation_lite:
            local_url = start_proxy_lite()

    main()
