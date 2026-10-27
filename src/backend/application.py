import os
import sys
import shutil
import tempfile
from pathlib import Path
import multiprocessing as mp

from PySide6.QtCore import QResource
_rcc_candidate = Path(__file__).resolve().parents[1] / "frontend" / "resources.rcc"
if _rcc_candidate.is_file():
    QResource.registerResource(str(_rcc_candidate))
else:
    import src.frontend.UI.resources # Fallback when binary resource is not pre-compiled
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from src.backend.android_storage import copy_download_file, folder_destination
from src.backend.theme_manager import ThemeManager
from src.backend.splashscreen import SplashController
from src.backend.qt_logging import install_wayland_message_filter


# --- MULTIPROCESSING SAFE SPLASH SCREEN ---
# We check if this is the main process. If so, we initialize the GUI.
# If it's a child process, we skip GUI initialization and set them to None.
is_android = (
    sys.platform == "android"
    or hasattr(sys, "getandroidapilevel")
    or "ANDROID_ARGUMENT" in os.environ
    or "ANDROID_BOOTSTRAP" in os.environ
    or "--android" in sys.argv
)
is_main_process = mp.current_process().name == 'MainProcess' and "unittest" not in sys.modules and not os.environ.get("PORN_FETCH_TEST_ENV")

app = None
engine = None
splash = None

if is_main_process:
    install_wayland_message_filter()
    if sys.platform == "win32":
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            ctypes.c_wchar_p("fi.echteralsfake.pornfetch")
        )
    app = QGuiApplication.instance() or QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon(":/images/graphics/logo.png"))
    engine = QQmlApplicationEngine()
    if not is_android and "--android" not in sys.argv:
        splash_qml_path = Path(__file__).resolve().parents[1] / "frontend" / "UI" / "SplashScreen.qml"
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
import asyncio
import argparse
import traceback
try:
    from rich_argparse import RichHelpFormatter
except ImportError:
    RichHelpFormatter = argparse.HelpFormatter  # type: ignore[assignment, misc]
from typing import AsyncIterator
from base_api.modules.config import IteratorConfig
from base_api import DownloadConfigHLS, DownloadConfigRAW
from base_api.modules.errors import DownloadCancelled
from src.shared.logging_setup import configure_app_logging
from importlib.metadata import metadata, packages_distributions, version

update_splash("Importing (Qt)")
import PySide6.QtAsyncio as QtAsyncio # Needed because porn fetch's network backend is now async since v3.9
from PySide6.QtCore import (QUrl, Signal, Slot, Property, QTranslator, QCoreApplication, QStandardPaths, QObject, Qt,
                            QTimer, QFile, QIODevice)

update_splash("Importing (Backend)")
from src.backend import clients # Singleton instance for the client objects (really important)
import src.backend.config as config
from src.backend.license_bridge import LicenseBridge, load_production_config
from src.backend.beta_disclaimer import BetaDisclaimerBridge
from src.licensing.service import create_license_service
from src.shared.paths import shared_data_dir
from src.shared.release import GITHUB_RELEASES_URL
from src.backend.config import (__version__, IS_SOURCE_RUN, TEMP_DIRECTORY,
                                TEMP_DIRECTORY_STATES, TEMP_DIRECTORY_SEGMENTS, app_settings)
from src.backend.shared_gui import ui_popup, set_mobile_notice_handler, Signals
from src.backend.helper_functions import safe_rmtree
from src.shared.error_reporting import ERROR_REPORT_DISCLOSURE, ERROR_REPORT_EXAMPLE, report_exception
from src.shared.metadata import write_tags
from src.shared.provider_routing import ContentKind, container_stream, resolve_container, route_url
from src.backend.login_manager import (
    LoginPornhub,
    LoginXVideos,
    LoginXhamster,
    get_account_video_iterator,
    provider_is_logged_in,
)
from pornhub_api.modules.errors import LoginFailed as phLoginFailed
from pornhub_api.modules.errors import ClientAlreadyLogged
from xhamster_api.modules.errors import LoginFailed as xhLoginFailed
from src.backend.update_service import AutoUpdater, CheckUpdates
from src.backend.installation import InstallPornFetch
from src.backend.uninstallation import UninstallPornFetch
from src.backend.sni_proxy_manager import SNIProxyManager
from src.shared.tor_transport import configure as configure_tor_transport
from src.shared.errors import UnsupportedPlatform, CookiesNotFound, LoginError
from src.backend.download_manager import (
    DownloadManager,
    DownloadListModel,
    VideoFilters,
    VideoObject,
    quality_requires_premium,
    select_allowed_quality,
)
from src.backend.video_processor import ProcessVideos
from src.database.bridge import DatabaseBridge
from src.backend.proxy_tester import test_proxy as run_proxy_test, validate_proxy_url
from curl_cffi.requests.exceptions import SSLError

update_splash("Importing (Frontend).")
# Frontend imports
from src.frontend.translations.strings import (TRANSLATE_MAIN, TRANSLATE_PAGE_DOWNLOAD, TRANSLATE_PAGE_LOGIN,
                                              TRANSLATE_PAGE_SETTINGS, TRANSLATE_ERRORS)


from src.shared.ffmpeg import has_ffmpeg

FORCE_DISABLE_AV = not has_ffmpeg()


stop_flag = asyncio.Event()
configure_tor_transport(app_settings)
sni_proxy_manager = None if is_android or "--android" in sys.argv else SNIProxyManager(app_settings)
log_level = app_settings.log_level_map.get(app_settings.log_level)


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

You have probably not executed the patch script in scripts/patch_qtasyncio.py
and applied it to your virtual environment.

You need to run this script, otherwise this application will NOT work!""")

class Backend(QObject):
    showMessage = Signal(str)
    mobileNotice = Signal(str, str)
    loginStateChanged = Signal()
    accountStateChanged = Signal()
    accountFetchStateChanged = Signal()
    downloadsChanged = Signal()
    busyChanged = Signal()
    activityChanged = Signal()
    updateAvailable = Signal("QVariantMap")
    updateProgress = Signal(int, int)
    updateStatus = Signal(str)
    updateFinished = Signal()
    proxyTestSucceeded = Signal(str, "QVariantMap")
    proxyTestFailed = Signal(str, str)
    proxySslError = Signal(str, str)
    proxyApplied = Signal(bool)
    shutdown_complete = Signal()

    def __init__(self, parent: QObject | None = None, *, mobile_layout: bool = False):
        super().__init__(parent)
        self._background_tasks: set[asyncio.Task[object]] = set()
        self._activity_active = False
        self._login_task: asyncio.Task[object] | None = None
        self._login_in_progress = False
        self._account_fetch_task: asyncio.Task[object] | None = None
        self._account_fetch_in_progress = False
        self._video_fetch_task: asyncio.Task[object] | None = None
        self._proxy_test_task: asyncio.Task[object] | None = None
        self._update_check_task: asyncio.Task[object] | None = None
        self._update_check_requested = False
        self._auto_update_task: asyncio.Task[object] | None = None
        self._shutdown_task: asyncio.Task[None] | None = None
        self._download_tasks: dict[str, asyncio.Task[object]] = {}
        self._download_stop_events: dict[str, asyncio.Event] = {}
        self._client_refresh_pending = False
        self._download_semaphore = asyncio.Semaphore(max(1, int(app_settings.parallel_downloads)))
        self._license_bridge: LicenseBridge | None = None
        self._restart_warning_shown = False
        self.logger = configure_app_logging(logger_name="Porn Fetch - [Backend]", level=log_level, log_file="PornFetch.log")
        self._downloads_model = DownloadListModel(self, premium_access=self.has_premium_access)
        self.download_manager = DownloadManager()
        self.download_manager.video_added.connect(self.video_added_signal)
        self.auto_updater = AutoUpdater(self, before_update=self._prepare_for_update, license_status=self._update_license_status)
        self.auto_updater.updateProgress.connect(self.updateProgress)
        self.auto_updater.statusReport.connect(self.updateStatus)
        self.auto_updater.finished.connect(self.updateFinished)
        self.showMessage.connect(self.handle_message)
        if is_android or mobile_layout:
            set_mobile_notice_handler(self.mobileNotice.emit)
        app_settings.restartRequired.connect(self.setting_requires_restart)
        self.database_bridge: DatabaseBridge | None = None
        self._pending_pocketbase_move: tuple[Path, Path] | None = None
        app_settings.movePocketBaseData.connect(self.pocketbase_data_changed)
        self._is_shutting_down = False
        self.ensure_temp()

        # ``clients`` creates its curl-cffi sessions during import. Apply all
        # saved request settings once the real GUI backend is initialized and
        # refresh them immediately when the content locale changes.
        self.load_clients()
        self.bind_runtime_settings()
        if not mobile_layout:
            self.bind_download_recovery()
        if sni_proxy_manager and sni_proxy_manager.last_error:
            QTimer.singleShot(
                0,
                lambda: ui_popup(
                    "SNI obfuscation failed to start and networking has been blocked.\n\n"
                    + str(sni_proxy_manager.last_error)
                ),
            )

    def has_premium_access(self) -> bool:
        return bool(self._license_bridge and self._license_bridge.isPremium)

    @Property(str, constant=True)
    def errorReportDisclosure(self) -> str:
        return ERROR_REPORT_DISCLOSURE

    @Property(str, constant=True)
    def errorReportExample(self) -> str:
        return ERROR_REPORT_EXAMPLE

    @Property(bool, notify=loginStateChanged)
    def loginInProgress(self) -> bool:
        return self._login_in_progress

    @Property(bool, notify=accountFetchStateChanged)
    def accountFetchInProgress(self) -> bool:
        return self._account_fetch_in_progress

    @Property(bool, notify=busyChanged)
    def busy(self) -> bool:
        return self._video_fetch_task is not None

    @Property(bool, notify=activityChanged)
    def activityActive(self) -> bool:
        return self._activity_active

    @Slot()
    def _update_activity(self) -> None:
        active = bool(
            self._background_tasks
            or (self._license_bridge is not None and self._license_bridge.busy)
            or (self.database_bridge is not None and self.database_bridge.busy)
            or self._is_shutting_down
        )
        if active != self._activity_active:
            self._activity_active = active
            self.activityChanged.emit()

    @Property("QVariantMap", notify=accountStateChanged)
    def accountLoginStatus(self) -> dict[str, bool]:
        return {
            provider: provider_is_logged_in(provider)
            for provider in ("PornHub", "XHamster", "XVideos")
        }

    def set_license_bridge(self, license_bridge: LicenseBridge) -> None:
        self._license_bridge = license_bridge
        license_bridge.statusChanged.connect(self._enforce_quality_access)
        license_bridge.statusChanged.connect(self._update_activity)
        license_bridge.entitlementChanged.connect(self.check_for_updates)
        self._enforce_quality_access()
        self._update_activity()

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
        """Request an update check, deferring it until QtAsyncio is running."""
        self._update_check_requested = True
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return
        self._start_update_check()

    def start_async_services(self) -> None:
        """Start deferred services from inside the running QtAsyncio loop."""
        clients.schedule_retired_session_cleanup()
        if self._update_check_requested:
            self._start_update_check()

    def _start_update_check(self) -> None:
        self._update_check_requested = False
        if self._update_check_task is not None and not self._update_check_task.done():
            return

        self._update_check_task = self._spawn(
            self._check_for_updates(),
            name="update-check",
        )

    async def _update_license_status(self):
        from src.licensing.client import LicenseStatus
        if self._license_bridge is None:
            return LicenseStatus("unlicensed", False)
        return await self._license_bridge._run_check(force=True)

    async def _check_for_updates(self) -> None:
        try:
            update = await CheckUpdates.check()
        except Exception as error:
            self.updateStatus.emit(f"Update check failed: {error}")
            return
        if update is None:
            self.updateStatus.emit("No update available.")
            return

        from src.shared.release import update_eligibility
        install_allowed = False
        message = update.get("entitlement_message", "Release metadata could not be authenticated.")
        if update.get("source") in {"signed_repository", "signed_android"}:
            status = await self._update_license_status()
            install_allowed, message = update_eligibility(status, update["release_timestamp"])
        details = {
            "install_allowed": install_allowed,
            "entitlement_message": message,
            "version": str(update.get("version", "")),
            "release_url": str(update.get("release_url") or GITHUB_RELEASES_URL),
            "important_info": str(update.get("important_info", "")),
            "changelog": str(update.get("changelog") or "Release notes are available on the GitHub releases page."),
            "changelog_format": str(update.get("changelog_format", "html")),
        }
        self.logger.info("New update found: %s", details["version"])
        self.updateAvailable.emit(details)

    @Slot()
    def cancel_update(self) -> None:
        if self._auto_update_task is not None and not self._auto_update_task.done():
            self._auto_update_task.cancel()

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

    @Slot(str, str)
    def export_download(self, job_id: str, destination_url: str) -> None:
        """Copy a completed private download to a user-selected Android document."""
        video = self._downloads_model.get_video(job_id)
        if video is None or self._downloads_model.get_status(job_id) != "completed":
            self.handle_message("Only completed downloads can be exported.")
            return
        source = Path(video.output_path)
        if not source.is_file():
            self.handle_message("The downloaded file could not be found.")
            return
        destination = QUrl(destination_url)
        if destination.scheme() not in ("content", "file"):
            self.handle_message("The selected save location is not supported.")
            return

        async def export() -> None:
            try:
                await asyncio.to_thread(self._copy_download_file, source,
                    destination.toString(QUrl.ComponentFormattingOption.FullyEncoded) if destination.scheme() == "content" else destination.toLocalFile())
                self.handle_message("Download exported successfully.")
            except Exception as error:
                self.handle_message(f"Could not export download: {error}")

        self._spawn(export(), name=f"export-{job_id}")

    _copy_download_file = staticmethod(copy_download_file)

    @Slot(str, result=QUrl)
    def download_file_url(self, job_id: str) -> QUrl:
        video = self._downloads_model.get_video(job_id)
        return QUrl.fromLocalFile(str(Path(video.output_path).resolve())) if video and video.output_path else QUrl()

    @Slot(str)
    def set_android_output_folder(self, folder_url: str) -> None:
        self.logger.info("Setting android output folder request: %r", folder_url)
        if not folder_url or not folder_url.strip():
            app_settings.android_output_folder = ""
            self.logger.info("Cleared android output folder setting")
            return
        cleaned = folder_url.strip()
        folder = QUrl.fromLocalFile(cleaned) if cleaned.startswith("/") else QUrl(cleaned)
        if folder.scheme() not in ("content", "file"):
            self.logger.warning("Invalid folder scheme: %r for URL %r", folder.scheme(), cleaned)
            self.handle_message("Choose a folder from the system picker.")
            return
        app_settings.android_output_folder = folder.toString(QUrl.ComponentFormattingOption.FullyEncoded)
        self.logger.info("Persisted android output folder: %r", app_settings.android_output_folder)

    async def _auto_export_android_download(self, source: Path) -> None:
        folder_url = QUrl(app_settings.android_output_folder)
        if not folder_url.isValid() or folder_url.scheme() not in ("content", "file"):
            return
        target_path = folder_destination(folder_url, source.name)
        try:
            def copy_to_folder() -> None:
                if app_settings.skip_existing_files and QFile.exists(target_path):
                    return
                self._copy_download_file(source, target_path)

            await asyncio.to_thread(copy_to_folder)
        except Exception as error:
            self.handle_message(f"Could not save to the selected folder: {error}. Choose the folder again in Settings.")

    async def _prepare_for_update(self) -> None:
        """Gracefully stop PocketBase and close sessions before the installer runs."""
        if self.database_bridge is not None:
            try:
                await self.database_bridge.close()
            except Exception as exc:
                self.logger.warning("Error closing database bridge before update: %s", exc)
        try:
            await clients.close_all_clients()
        except Exception as exc:
            self.logger.warning("Error closing network clients before update: %s", exc)

    @Slot(int)
    def toggle_user_interface_language(self, value: int) -> None:
        ...

    @Slot()
    def setting_requires_restart(self) -> None:
        if not self._restart_warning_shown:
            self._restart_warning_shown = True
            ui_popup("You have triggered an action that requires a restart before taking effect!")

    @Slot(str)
    def handle_message(self, message: str) -> None:
        ui_popup(text=message)

    @Slot(bool)
    def toggle_network_logging(self, value: bool) -> None:
        ...

    @Slot(str, str)
    def pocketbase_data_changed(self, old_path: str, new_path: str) -> None:
        old_directory = Path(old_path).expanduser().resolve()
        new_directory = Path(new_path).expanduser().resolve()
        if old_directory == new_directory:
            return
        if new_directory.exists():
            ui_popup(
                "The selected PocketBase data directory already exists. It will be used after restart, "
                "but the current data will not be moved into it."
            )
            return
        source = self._pending_pocketbase_move[0] if self._pending_pocketbase_move else old_directory
        self._pending_pocketbase_move = (source, new_directory)
        ui_popup("The PocketBase data directory will be moved after the application shuts down.")

    @staticmethod
    def _move_pocketbase_data(source: Path, destination: Path) -> None:
        if not source.is_dir() or destination.exists():
            return
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(destination))

    @Slot()
    def cancel_fetching(self):
        stop_flag.set()
        if self._video_fetch_task is not None:
            self._video_fetch_task.cancel()

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
                await report_exception(
                    e,
                    operation="install Porn Fetch",
                    location="Backend.install_pornfetch.run_installation",
                    enabled=app_settings.enable_logging,
                    version=__version__,
                )
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
        if self._is_shutting_down:
            return
        if any(not task.done() for task in self._background_tasks):
            self._client_refresh_pending = True
            self.logger.info("Deferring client refresh until active tasks finish")
            return

        self._client_refresh_pending = False
        clients.refresh_clients()
        self.logger.setLevel(app_settings.log_level_map.get(app_settings.log_level, "INFO"))
        self.accountStateChanged.emit()

    def bind_runtime_settings(self) -> None:
        """Use the same runtime wiring for normal startup and diagnostics."""
        app_settings.reloadClients.connect(self.load_clients)
        app_settings.parallelDownloadsChanged.connect(self.update_parallel_downloads)

    def bind_database_bridge(self, bridge: DatabaseBridge) -> None:
        """Connect download history and activity to the desktop database consumer."""
        self.database_bridge = bridge
        bridge.busyChanged.connect(self._update_activity)
        bridge.initializationFailed.connect(self.handle_message)
        self.download_manager.video_added.connect(bridge.on_video_updated)
        self.download_manager.video_updated.connect(bridge.on_video_updated)

    def bind_download_recovery(self) -> None:
        from src.backend.download_recovery import DownloadRecovery
        self._download_recovery = DownloadRecovery(self, Path(TEMP_DIRECTORY) / "download-queue.json")
        self._download_recovery.restore()

    @Slot(int)
    def update_parallel_downloads(self, limit: int) -> None:
        if any(not task.done() for task in self._download_tasks.values()):
            self._pending_parallel_limit = max(1, int(limit))
            return
        self._pending_parallel_limit = None
        self._download_semaphore = asyncio.Semaphore(max(1, int(limit)))

    def _spawn(self, coro, *, name: str) -> asyncio.Task:
        task = asyncio.create_task(coro, name=name)
        if self._is_shutting_down:
            task.cancel()
        self._background_tasks.add(task)
        task.add_done_callback(self._background_task_done)
        self._update_activity()
        return task

    def _background_task_done(self, task: asyncio.Task) -> None:
        self._background_tasks.discard(task)
        self._update_activity()

        if task.cancelled():
            self.logger.debug("Background task cancelled: %s", task.get_name())
        else:
            try:
                task.result()
            except Exception as error:
                self.logger.exception(
                    "Background task failed: %s",
                    task.get_name(),
                )
                if not self._is_shutting_down:
                    asyncio.create_task(
                        report_exception(
                            error,
                            operation="run GUI background task",
                            location="Backend._background_task_done",
                            context={"task_name": task.get_name()},
                            enabled=app_settings.enable_logging,
                            version=__version__,
                        ),
                        name=f"report-{task.get_name()}",
                    )

        if not self._is_shutting_down and self._client_refresh_pending and not any(
            not pending_task.done() for pending_task in self._background_tasks
        ):
            self.load_clients()

    @Slot(str, bool)
    def testProxy(self, proxy_url: str, verify_ssl: bool) -> None:
        """Test a proxy asynchronously without blocking the QML render thread."""
        if self._proxy_test_task is not None and not self._proxy_test_task.done():
            self._proxy_test_task.cancel()

        task = self._spawn(
            self._test_proxy(proxy_url, verify_ssl),
            name="proxy-connectivity-test",
        )
        self._proxy_test_task = task

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

    @Slot(str)
    def remove_video(self, job_id: str) -> None:
        """Remove a queue entry, cooperatively stopping active work first."""
        job_id = str(job_id)
        task = self._download_tasks.get(job_id)
        if task is not None and not task.done():
            self.stop_download(job_id)
            task.add_done_callback(lambda _: self.remove_video(job_id))
            return
        self._downloads_model.remove_video(job_id)
        self.download_manager.remove_video(job_id)

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
        if self._is_shutting_down:
            return
        job_id = str(job_id)
        existing_task = self._download_tasks.get(job_id)
        if existing_task is not None and not existing_task.done():
            return

        video = self._downloads_model.get_video(job_id)
        if video is None:
            self.logger.warning("Cannot download unknown video: %s", job_id)
            return
        allowed_quality = select_allowed_quality(
            video.selected_quality or "best",
            video.qualities or [],
            self.has_premium_access(),
        )
        if (not allowed_quality and self.has_premium_access()
                and isinstance(video.source_video, clients.yp_Video)
                and video.source_video.is_hls is False):
            # The provider exposes one MP4 without a reported resolution.
            # Licensed users can use it; free users still need a verified <=720p stream.
            allowed_quality = "best"
        if not allowed_quality:
            self.logger.warning("No permitted quality is available for this download")
            self.showMessage.emit(self.tr("No permitted quality is available for this video."))
            return
        if allowed_quality != str(video.selected_quality or ""):
            video.selected_quality = allowed_quality
            self._downloads_model.set_video_quality(job_id, allowed_quality)

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
            # A queued task can be cancelled before its coroutine first runs.
            # In that case _download_video cannot publish its final status.
            if task.cancelled() and self._downloads_model.get_status(job_id) in {"queued", "stopping"}:
                self._downloads_model.set_status(job_id, "cancelled")
                self.download_manager.update_status(job_id, "cancelled")
            self._download_tasks.pop(job_id, None)
            self._download_stop_events.pop(job_id, None)
            pending_limit = getattr(self, "_pending_parallel_limit", None)
            if pending_limit is not None and not self._download_tasks:
                self.update_parallel_downloads(pending_limit)

    @Slot(str)
    def stop_download(self, job_id: str) -> None:
        job_id = str(job_id)
        stop_event = self._download_stop_events.get(job_id)
        if stop_event is None:
            return
        was_queued = self._downloads_model.get_status(job_id) == "queued"
        stop_event.set()
        self._downloads_model.set_status(job_id, "stopping")
        if was_queued:
            # No writer has started. Cancel the semaphore wait immediately;
            # active downloads still use the cooperative stop event above.
            task = self._download_tasks.get(job_id)
            if task is not None and not task.done():
                task.cancel()

    async def _download_video(
        self,
        job_id: str,
        video: VideoObject,
        stop_event: asyncio.Event,
        cleanup_on_stop: bool,
    ) -> None:
        download_started = False
        try:
            async with self._download_semaphore:
                if stop_event.is_set():
                    video.status = "cancelled"
                    self._downloads_model.set_status(job_id, "cancelled")
                    self.download_manager.update_status(job_id, "cancelled")
                    return

                if video.source_video is None:
                    # Restored rows contain local metadata only. Resolve a fresh
                    # native video/session when the user explicitly resumes.
                    source = await clients.get_video(video.url)
                    fresh = await clients.load_video_attributes(source)
                    quality = select_allowed_quality(video.selected_quality, fresh.qualities, self.has_premium_access())
                    if not quality:
                        raise ValueError("The restored video no longer offers a permitted quality")
                    for attribute in ("title", "author", "length", "tags", "thumbnail_url", "video_id", "publish_date", "qualities"):
                        setattr(video, attribute, getattr(fresh, attribute))
                    video.source_video = source
                    self._downloads_model.refresh_metadata(job_id)
                    self._downloads_model.set_video_quality(job_id, quality)

                if app_settings.processing_delay:
                    await asyncio.sleep(int(app_settings.processing_delay))
                    if stop_event.is_set():
                        video.status = "cancelled"
                        self._downloads_model.set_status(job_id, "cancelled")
                        self.download_manager.update_status(job_id, "cancelled")
                        return

                output_path = Path(video.output_path or video.title)
                from src.shared.download_options import video_file_path
                output_path = video_file_path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                video.output_path = output_path

                if (output_path.exists() and app_settings.skip_existing_files
                        and video.status not in {"cancelled", "failed"}
                        and not Path(f"{output_path}.raw-state.json").exists()
                        and not (Path(TEMP_DIRECTORY_STATES) / job_id).exists()):
                    self._downloads_model.update_progress(job_id, 100)
                    self._downloads_model.set_status(job_id, "completed")
                    self.download_manager.update_status(job_id, "completed")
                    self._downloads_model.remove_video(job_id)
                    self.download_manager.remove_video(job_id)
                    return

                self._downloads_model.set_status(job_id, "downloading")
                download_started = True

                event_loop = asyncio.get_running_loop()
                last_reported_percentage = -1

                def update_progress(position: int, total: int) -> None:
                    nonlocal last_reported_percentage
                    if not total:
                        return
                    percentage = max(0, min(100, int(position * 100 / total)))
                    if percentage == last_reported_percentage:
                        return
                    last_reported_percentage = percentage
                    event_loop.call_soon_threadsafe(
                        self._downloads_model.update_progress,
                        job_id,
                        percentage,
                    )

                quality = video.selected_quality or "best"
                source_video = video.source_video
                if isinstance(source_video, clients.xf_Video):
                    from src.shared.media import xfreehd_quality
                    quality = xfreehd_quality(quality)
                raw_video_types = (clients.ep_Video, clients.pt_Video, clients.xf_Video, clients.ef_Video, clients.tf_Video)

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
                    video.is_hls = getattr(source_video, "is_hls", True) is not False
                    segment_dir = Path(TEMP_DIRECTORY_SEGMENTS) / job_id
                    segment_state_path = Path(TEMP_DIRECTORY_STATES) / job_id
                    from src.shared.download_recovery import discard_changed_hls_quality
                    await asyncio.to_thread(discard_changed_hls_quality, segment_state_path, segment_dir, quality)
                    segment_dir.mkdir(parents=True, exist_ok=True)
                    segment_state_path.parent.mkdir(parents=True, exist_ok=True)
                    can_remux = not FORCE_DISABLE_AV
                    configuration = DownloadConfigHLS(
                        quality=quality,
                        path=output_path,
                        callback=update_progress,
                        callback_remux=update_progress,
                        no_title=True,
                        stop_event=stop_event,
                        remux=can_remux,
                        metadata=video if (app_settings.write_metadata and can_remux) else None,
                        segment_state_path=str(segment_state_path),
                        segment_dir=str(segment_dir),
                        return_report=True,
                        cleanup_on_stop=cleanup_on_stop,
                        # cleanup_on_stop decides whether cancellation keeps
                        # segments. Completed downloads always release them.
                        keep_segment_dir=False,
                    )
                    if isinstance(source_video, clients.yp_Video):
                        backup_configuration = DownloadConfigRAW(
                            quality=quality,
                            path=output_path,
                            callback=update_progress,
                            no_title=True,
                            stop_event=stop_event,
                            max_workers=app_settings.download_workers,
                            read_timeout=float(app_settings.timeout),
                            max_retries=app_settings.retries,
                        )
                        result = await source_video.download(
                            configuration,
                            backup_configuration=backup_configuration,
                        )
                    else:
                        result = await source_video.download(configuration)

                report_status = getattr(result, "status", None)
                video.missing_segments = getattr(result, "missing", None)
                if stop_event.is_set() or report_status == "cancelled":
                    status = "cancelled"
                elif report_status in {"missing", "failed"} or result is False:
                    status = "failed"
                else:
                    status = "completed"

                video.status = status
                self._downloads_model.set_status(job_id, status)
                if status == "failed":
                    report_id = await report_exception(
                        RuntimeError(f"Downloader returned failure status: {report_status or 'false result'}"),
                        operation="download video",
                        location="Backend._download_video",
                        context={
                            "video_url": getattr(video, "url", None),
                            "provider": type(getattr(video, "source_video", None)).__module__,
                            "quality": getattr(video, "selected_quality", None),
                            "job_id": job_id,
                        },
                        enabled=app_settings.enable_logging,
                        version=__version__,
                    )
                    self.logger.error("Download %s failed [error %s]", job_id, report_id)
                    if not app_settings.supress_errors:
                        self.showMessage.emit(
                            self.tr("The video download failed. Error ID: %s") % report_id
                        )
                if status == "completed":
                    metadata_written = bool(getattr(result, "metadata_written", False))
                    if (
                        app_settings.write_metadata
                        and not FORCE_DISABLE_AV
                        and not metadata_written
                        and output_path.exists()
                    ):
                        try:
                            await asyncio.to_thread(write_tags, str(output_path), video)
                        except Exception:
                            self.logger.exception("Could not write metadata for download %s", job_id)
                    self._downloads_model.update_progress(job_id, 100)
                    if is_android or "--android" in sys.argv:
                        await self._auto_export_android_download(output_path)
                self.download_manager.update_status(job_id, status)
                if status == "completed":
                    self._downloads_model.remove_video(job_id)
                    self.download_manager.remove_video(job_id)
        except DownloadCancelled:
            video.status = "cancelled"
            self._downloads_model.set_status(job_id, "cancelled")
            self.download_manager.update_status(job_id, "cancelled")
        except asyncio.CancelledError:
            video.status = "cancelled"
            self._downloads_model.set_status(job_id, "cancelled")
            self.download_manager.update_status(job_id, "cancelled")
            raise
        except Exception as error:
            video.status = "failed"
            self._downloads_model.set_status(job_id, "failed")
            self.download_manager.update_status(job_id, "failed")
            self.logger.exception("Download failed for %s", job_id)
            report_id = await report_exception(
                error,
                operation="download video",
                location="Backend._download_video",
                context={
                    "video_url": getattr(video, "url", None),
                    "provider": type(getattr(video, "source_video", None)).__module__,
                    "quality": getattr(video, "selected_quality", None),
                    "job_id": job_id,
                },
                enabled=app_settings.enable_logging,
                version=__version__,
            )
            if not app_settings.supress_errors:
                self.showMessage.emit(
                    self.tr("The video download failed. Error ID: %s") % report_id
                )
        finally:
            if download_started and cleanup_on_stop and stop_event.is_set():
                # The provider has stopped and closed its writers before these
                # files are removed. Include the RAW checkpoint introduced by
                # resumable multipart downloads and the HLS assembly/state files.
                def cleanup_partial_files():
                    raw_state = Path(f"{output_path}.raw-state.json")
                    hls_state = Path(TEMP_DIRECTORY_STATES) / job_id
                    for path in (output_path, Path(f"{output_path}.tmp"), raw_state,
                                 Path(f"{raw_state}.tmp"), hls_state, Path(f"{hls_state}.tmp")):
                        try:
                            path.unlink(missing_ok=True)
                        except OSError:
                            self.logger.warning("Could not remove download temporary file: %s", path)
                    safe_rmtree(Path(TEMP_DIRECTORY_SEGMENTS) / job_id)
                await asyncio.to_thread(cleanup_partial_files)

    @Property(QObject, notify=downloadsChanged)
    def downloads(self):
        return self._downloads_model

    @Slot(object)
    def video_added_signal(self, video):
        quality = str(app_settings.mappings_quality.get(app_settings.quality))
        self._downloads_model.add_video(video=video, preferred_quality=quality)

    def on_download_progress(self, video_id: str, percentage: int):
        self._downloads_model.update_progress(video_id, percentage)

    def _start_video_fetch(self, coroutine, *, name: str) -> asyncio.Task | None:
        if self.busy or self._is_shutting_down:
            coroutine.close()
            return None
        stop_flag.clear()
        self._video_fetch_task = self._spawn(coroutine, name=name)
        self._video_fetch_task.add_done_callback(self._video_fetch_finished)
        self.busyChanged.emit()
        return self._video_fetch_task

    def _video_fetch_finished(self, task: asyncio.Task) -> None:
        if self._video_fetch_task is task:
            self._video_fetch_task = None
            self.busyChanged.emit()
        if self._account_fetch_task is task and self._account_fetch_in_progress:
            self._account_fetch_in_progress = False
            self.accountFetchStateChanged.emit()

    def _start_filtered_fetch(self, operation, url: str, custom_options: str, values: dict, name: str) -> None:
        from src.shared.download_options import title_template
        try:
            filters = VideoFilters(**values)
            filters.validate()
            title_template(custom_options)
        except (ValueError, TypeError) as error:
            self.showMessage.emit(str(error))
            return
        self._start_video_fetch(operation(url, custom_options, filters), name=name)

    @Slot(str, str, dict)
    def process_single_url(self, url: str, custom_options: str, filters: dict):
        """
        This function processes either a single Video or a Short depending on the platform.
        """
        print(f"Received Video / Short URL: {url}")
        self._start_filtered_fetch(self._process_single_url, url, custom_options, filters, "single-video-processing")

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
        process_videos.error_signal.connect(self.showMessage.emit)
        await process_videos.start_processing()

        self.logger.info("Finished preparing videos for the download list")

    @Slot(str, str, dict)
    def process_model_url(self, url: str, custom_options: str, filters: dict):
        """
        This function loads all the videos of a model, channel, creator or user object and loads them into the
        ListView to allow the user to individually select the videos for download
        """
        print(f"Received Model URL: {url}")
        self._start_filtered_fetch(self._process_model_url, url, custom_options, filters, "model-video-processing")

    async def _process_model_url(self, url: str, custom_options: str, filters: VideoFilters,
                                 *, pages: int = 30, iterator_config: IteratorConfig | None = None):
        try:
            route = route_url(url)
            if route.kind != ContentKind.PROFILE:
                raise ValueError("Please enter a supported profile or channel URL.")
            target = await resolve_container(clients.client_for(route.provider), route, pages=pages)
            options = iterator_config
            if options is None and route.provider == "eporner":
                sources = ("html",) if app_settings.strict_enforcement else ("api", "html")
                options = IteratorConfig(load_specific_sources=sources)
            mode = {0: "both", 1: "uploads", 2: "videos"}.get(app_settings.model_videos, "videos")
            videos = container_stream(target, pages=pages, provider=route.provider,
                                      profile_mode=route.profile_mode or mode, iterator_config=options)
        except ValueError as error:
            self.showMessage.emit(str(error))
            return
        await self.process_videos(
            iterator=videos, custom_options=custom_options, filters=filters,
            origin_iterator_url=url,
            origin_iterator_name=self._iterator_display_name(target, url, "model / channel"),
        )

    @Slot(str, str, dict)
    def process_playlist_url(self, url: str, custom_options: str, filters: dict):
        self._start_filtered_fetch(self._process_playlist_url, url, custom_options, filters, "playlist-video-processing")

    async def _process_playlist_url(self, url: str, custom_options: str, filters: VideoFilters):
        try:
            route = route_url(url)
            if route.kind != ContentKind.COLLECTION:
                raise ValueError("Please enter a supported public playlist or collection URL.")
            target = await resolve_container(clients.client_for(route.provider), route, pages=30)
            videos = container_stream(target, pages=30, provider=route.provider)
        except ValueError as error:
            self.showMessage.emit(str(error))
            return
        await self.process_videos(
            iterator=videos, custom_options=custom_options, filters=filters,
            origin_iterator_url=url,
            origin_iterator_name=self._iterator_display_name(target, url, "playlist / collection"),
        )

    @Slot(str, str, str)
    def fetch_account_videos(
        self,
        provider: str,
        collection: str,
        playlist_url: str = "",
    ) -> None:
        if self.busy or (self._account_fetch_task is not None and not self._account_fetch_task.done()):
            return

        self._account_fetch_in_progress = True
        self.accountFetchStateChanged.emit()
        self._account_fetch_task = self._start_video_fetch(
            self._run_fetch_account_videos(provider, collection, playlist_url),
            name=f"account-{provider.casefold()}-{collection.casefold()}",
        )

    async def _run_fetch_account_videos(
        self,
        provider: str,
        collection: str,
        playlist_url: str = "",
    ) -> None:
        try:
            iterator, source_name = get_account_video_iterator(
                provider=provider,
                collection=collection,
                playlist_url=playlist_url,
            )
            await self.process_videos(
                iterator=iterator,
                custom_options="",
                filters=VideoFilters(),
                origin_iterator_name=source_name,
            )
        except LoginError as error:
            self.showMessage.emit(str(error))
        except (phLoginFailed, xhLoginFailed):
            self.showMessage.emit(
                self.tr("Your %s login is no longer valid. Please log in again.") % provider
            )
        except Exception as error:
            self.logger.exception(
                "Could not fetch %s account collection %s",
                provider,
                collection,
            )
            await report_exception(
                error,
                operation="fetch account collection",
                location="Backend._run_fetch_account_videos",
                context={"provider": provider, "collection": collection, "playlist_url": playlist_url},
                enabled=app_settings.enable_logging,
                version=__version__,
            )
            self.showMessage.emit(
                self.tr("Could not fetch the account videos. Please check the log for details.")
            )
        finally:
            self._account_fetch_in_progress = False
            self.accountFetchStateChanged.emit()

    @Slot(str, str, str, bool)
    def login_account(
        self,
        provider: str,
        identity: str,
        secret: str,
        from_cookies: bool = False,
    ) -> None:
        if self._login_task is not None and not self._login_task.done():
            return

        self._login_in_progress = True
        self.loginStateChanged.emit()
        self._login_task = self._spawn(
            self._run_login_account(
                provider=provider,
                identity=identity,
                secret=secret,
                from_cookies=from_cookies,
            ),
            name=f"login-{provider.casefold()}",
        )

    async def _run_login_account(
        self,
        provider: str,
        identity: str,
        secret: str,
        from_cookies: bool = False,
    ) -> None:
        provider_key = provider.strip().casefold()

        try:
            if provider_key == "pornhub":
                succeeded = await LoginPornhub.login(
                    email=identity.strip(),
                    password=secret,
                    from_browser=from_cookies,
                )
            elif provider_key == "xhamster":
                succeeded = await LoginXhamster.login(
                    username=identity.strip(),
                    password=secret,
                    from_browser=from_cookies,
                )
            elif provider_key == "xvideos":
                token_cookies = None
                if not from_cookies:
                    token_cookies = {
                        "session_token": identity.strip(),
                        "session_token_auth": secret.strip(),
                    }
                succeeded = await LoginXVideos.login(
                    custom_cookies=token_cookies,
                    from_browser=from_cookies,
                )
            else:
                self.showMessage.emit(self.tr("The selected login provider is not supported."))
                return

            if succeeded:
                self.showMessage.emit(self.tr("You have successfully logged in."))
            else:
                self.showMessage.emit(self.tr("The login failed. Please verify your account details."))
        except CookiesNotFound as error:
            self.showMessage.emit(str(error))
        except (phLoginFailed, xhLoginFailed):
            self.showMessage.emit(
                self.tr("%s rejected the login. Please verify your account details.") % provider
            )
        except ClientAlreadyLogged:
            self.showMessage.emit(self.tr("You are already logged in."))
        except LoginError as error:
            self.showMessage.emit(str(error))
        except Exception as error:
            self.logger.exception("Unexpected %s login failure", provider)
            await report_exception(
                error,
                operation="log in to provider",
                location="Backend._run_login_account",
                context={"provider": provider},
                enabled=app_settings.enable_logging,
                version=__version__,
            )
            self.showMessage.emit(
                self.tr("An unexpected login error occurred. Please check the log for details.")
            )
        finally:
            # Cookie/token validation can clear an old account before failing.
            # Notify QML on failure/cancellation as well as successful login.
            self.accountStateChanged.emit()
            self._login_in_progress = False
            self.loginStateChanged.emit()

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
        self._update_activity()
        self.logger.info("Application closing. Initiating async teardown...")
        self._shutdown_task = asyncio.create_task(
            self._teardown_routine(),
            name="application-teardown",
        )

    async def _teardown_routine(self):
        """Stop writers, persist recovery/history, then close their transports."""
        try:
            downloads = set(self._download_tasks.values())
            for job in tuple(self._download_tasks):
                self.stop_download(job)
            tasks_to_await = set(self._background_tasks) - downloads
            if self._proxy_test_task and not self._proxy_test_task.done():
                tasks_to_await.add(self._proxy_test_task)

            if tasks_to_await:
                self.logger.info("Cancelling %d background tasks...", len(tasks_to_await))
                for task in tasks_to_await:
                    task.cancel()
                await asyncio.gather(*tasks_to_await, return_exceptions=True)
                self.logger.info("All background tasks stopped successfully.")

            if downloads:
                done, pending = await asyncio.wait(downloads, timeout=30)
                if pending:
                    self.logger.warning("Forcing cancellation of %d downloads after shutdown grace period", len(pending))
                    for task in pending:
                        task.cancel()
                await asyncio.gather(*downloads, return_exceptions=True)

            async def close_component(name: str, cleanup) -> None:
                try:
                    await cleanup()
                except Exception:
                    self.logger.exception("Could not close %s", name)

            recovery = getattr(self, "_download_recovery", None)
            if recovery is not None:
                await close_component("download recovery", recovery.close)
            if self.database_bridge is not None:
                await close_component("database service", self.database_bridge.close)
            app_settings.sync()

            await close_component("network clients", clients.close_all_clients)
            from src.backend.update_service import service_core
            from src.shared.tor_runtime import runtime
            await close_component("update transport", service_core.close)
            await close_component("Tor", lambda: asyncio.to_thread(runtime.stop))
            if self._license_bridge is not None:
                await close_component("license service", self._license_bridge.close)
            if sni_proxy_manager:
                try:
                    sni_proxy_manager.stop()
                except Exception:
                    self.logger.exception("Could not stop the SNI proxy")
            if self._pending_pocketbase_move is not None:
                await close_component(
                    "pending database move",
                    lambda: asyncio.to_thread(
                        self._move_pocketbase_data,
                        *self._pending_pocketbase_move,
                    ),
                )
        finally:
            self.logger.info("Application teardown finished. Exiting...")
            self.shutdown_complete.emit()
            asyncio.get_running_loop().stop()

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
    parser.add_argument("--smoke-test", action="store_true", help="Load bundled QML and resources offline, then exit")
    parser.add_argument("--test-profiles", action="store_true", help="Run live GUI profile metadata/playlist tests without media downloads")
    parser.add_argument("--test-profile-variants", action="store_true", help="Include localized/alias profile fixtures in live tests")
    parser.add_argument("--android", action="store_true", help="Preview the Android QML layout on desktop")

    args = parser.parse_args()
    if args.smoke_test and (args.test or args.test_profiles or args.test_profile_variants):
        parser.error("--smoke-test cannot be combined with the online --test mode")
    test_mode = False

    if args.version:
        print_runtime_version_info()
        sys.exit(0)

    if args.test or args.test_profiles or args.test_profile_variants:
        test_mode = True

    sys.unraisablehook = custom_unraisable_hook
    local_url = sni_proxy_manager.start() if sni_proxy_manager and not args.smoke_test else None
    if local_url:
        print(f"SNI proxy route: {local_url}")

    global app, engine, splash

    # Initialize the app + organization values
    # The organization values handle settings, licenses etc, please do not change this :)
    app.setOrganizationName(config.__org_name__)
    app.setApplicationName(config.__app_name__)
    app.setApplicationVersion(config.__version__)
    # The asyncio teardown decides when the process may exit. A compositor can
    # still destroy the native window without prematurely stopping QtAsyncio.
    app.setQuitOnLastWindowClosed(False)

    app.styleHints().setColorScheme(Qt.ColorScheme.Dark if app_settings.dark_mode else Qt.ColorScheme.Light)

    app_font = app.font()
    app_font.setPointSize(app_settings.font_size)
    app.setFont(app_font)



    # Loads the theme e.g., Material UI / Fusion + dark / light theme
    saved_style = app_settings.core_style
    QQuickStyle.setStyle("Material" if is_android or args.android else saved_style)
    theme_manager = ThemeManager(parent=engine)

    # The backend instance handles the main logic, see class above
    backend_instance = Backend(parent=engine, mobile_layout=is_android or args.android)

    # The test mode runs an automated test with the real QML / Backend environment, it tests basically everything
    if test_mode:
        from src.backend.diagnostics import run_smoke_tests

        # Diagnostics observe errors through QSignalSpy; modal dialogs would
        # otherwise stall an unattended run before it can report the failure.
        backend_instance.showMessage.disconnect(backend_instance.handle_message)

        async def run_diagnostics():
            try:
                return await run_smoke_tests(
                    backend=backend_instance, model=backend_instance._downloads_model,
                    profiles_only=args.test_profiles or (args.test_profile_variants and not args.test),
                    include_profile_variants=args.test_profile_variants,
                )
            finally:
                await clients.close_all_clients()

        exit_code = QtAsyncio.run(run_diagnostics(), keep_running=False)
        raise SystemExit(exit_code)


    database_bridge = DatabaseBridge(parent=engine, tracking_supported=not is_android)
    backend_instance.bind_database_bridge(database_bridge)

    license_service = create_license_service(
        app_settings,
        Path.cwd() / "licensing" if args.smoke_test else (
            Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)) if is_android else shared_data_dir()
        ),
        production_config=load_production_config(),
    )
    bridge_instance = LicenseBridge(license_service, parent=engine) # License bridge connects QML code to Python
    backend_instance.set_license_bridge(bridge_instance)
    # Gives some context to QML so that QML can directly access certain things
    engine.rootContext().setContextProperty("bridge", bridge_instance)
    engine.rootContext().setContextProperty("backend", backend_instance)
    engine.rootContext().setContextProperty("databaseBridge", database_bridge)
    engine.rootContext().setContextProperty("themeManager", theme_manager)
    engine.rootContext().setContextProperty("appSettings", app_settings)
    from src.backend.ui_translation import UiTranslation
    engine.ui_translation = UiTranslation(app_settings, engine)
    from src.backend.tor_status import TorStatus
    tor_status = TorStatus(parent=engine)
    tor_status.installResult.connect(backend_instance.updateStatus)
    engine.rootContext().setContextProperty("torStatus", tor_status)
    beta_disclaimer = BetaDisclaimerBridge(app_settings, parent=engine)
    engine.rootContext().setContextProperty("betaDisclaimer", beta_disclaimer)
    engine.rootContext().setContextProperty("androidLayout", is_android or args.android)
    from src.backend.android_display import AndroidDisplay
    display_geometry = AndroidDisplay(os.environ.get("ANDROID_PRIVATE", "") if is_android else "", parent=engine)
    engine.rootContext().setContextProperty("androidDisplay", display_geometry)
    for context_name, resource_path in (
        ("applicationLicenseText", ":/legal/LICENSE"),
        ("thirdPartyNoticesText", ":/legal/THIRD_PARTY_NOTICES.md"),
    ):
        resource = QFile(resource_path)
        if not resource.open(QIODevice.OpenModeFlag.ReadOnly):
            raise RuntimeError(f"Bundled legal notice is missing: {resource_path}")
        engine.rootContext().setContextProperty(context_name, bytes(resource.readAll()).decode("utf-8"))
        resource.close()

    update_splash("Loading Window...")

    # 3. Choose the native layout, or open the Android layout as a desktop preview.
    qml_file = Path(__file__).resolve().parents[1] / "frontend" / "UI" / (
        "AndroidMain.qml" if is_android or args.android else "Main.qml"
    )


    qml_warnings = []
    if args.smoke_test:
        engine.warnings.connect(lambda errors: qml_warnings.extend(error.toString() for error in errors))
        from src.shared.release import ROOT_FILE
        from tuf.api.metadata import Metadata, Root

        Metadata[Root].from_file(str(ROOT_FILE))
        load_production_config()
        for resource_path in (":/images/graphics/logo_transparent.png", ":/licensing/production.json"):
            if not QFile.exists(resource_path):
                raise RuntimeError(f"Bundled resource is missing: {resource_path}")

    existing_roots = engine.rootObjects()
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    window_roots = [root for root in engine.rootObjects() if root not in existing_roots]

    # 4. Check if QML loaded successfully
    if not window_roots:
        print("Failed to load QML file.")
        sys.exit(-1)

    if splash:
        splash.finish()
    disable_nuitka_splash()

    if args.smoke_test:
        # Only Qt runs here; asynchronous network, licensing and database startup is deferred below.
        for root in window_roots:
            root.setProperty("safeToClose", True)
        QTimer.singleShot(250, app.quit)
        app.exec()

        async def close_smoke_services():
            await bridge_instance.close()
            await database_bridge.close()
            await clients.close_all_clients()

        asyncio.run(close_smoke_services())
        splash = None
        engine = None
        if qml_warnings:
            raise RuntimeError("GUI smoke test reported QML errors:\n" + "\n".join(qml_warnings))
        print("GUI smoke test passed: QML, legal notices, licensing configuration and update trust root loaded offline.")
        return

    async def start_async_services() -> None:
        # This coroutine is first advanced by QtAsyncio after its loop is
        # running. QML loading alone is not a safe asyncio startup boundary.
        bridge_instance.start()
        database_bridge.start()
        backend_instance.start_async_services()

    # handle_sigint enables a clean shutdown when CTRL+C is pressed.
    QtAsyncio.run(
        start_async_services(),
        handle_sigint=True,
    )

    # SplashController also retains the engine. Release it first, then destroy
    # the QML object tree while all context properties are still alive.
    splash = None
    engine = None



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
          lic = meta.get('License-Expression') or meta.get('License') or 'Unknown'
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
