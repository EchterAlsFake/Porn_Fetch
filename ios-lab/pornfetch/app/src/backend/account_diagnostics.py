"""Live account diagnostics through the actual QML pages and GUI list pipeline."""
from __future__ import annotations

import asyncio
import logging
import math
import re
from collections.abc import Awaitable, Callable
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

from base_api import BaseCore
from base_api.modules.static_functions import parse_retry_after
from PySide6.QtCore import QCoreApplication, QEvent, QMetaObject, QPointF, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow
from PySide6.QtTest import QSignalSpy, QTest

from src.backend.profile_diagnostics import make_test_backend

UI = Path(__file__).resolve().parents[1] / "frontend/UI"
PROVIDERS = ("PornHub", "XHamster", "XVideos")
COLLECTION_BUTTONS = {
    "desktop": {
        "PornHub": {"history": "Get Watch History", "recommended": "Get Recommended Videos",
                    "feed": "Get Subscription Feed", "favorites": "Get Favorite Videos"},
        "XHamster": {"liked": "Get Liked Videos", "playlist": "Get Playlist Videos"},
        "XVideos": {"watch_later": "Get Watch Later Videos", "history": "Get Watch History", "liked": "Get Liked Videos"},
    },
    "mobile": {
        "PornHub": {"history": "Watch history", "recommended": "Recommended", "feed": "Subscription feed", "favorites": "Favorites"},
        "XHamster": {"liked": "Liked videos", "playlist": "Get playlist videos"},
        "XVideos": {"watch_later": "Watch later", "history": "Watch history", "liked": "Liked videos"},
    },
}


def account_check_inventory(layouts, providers):
    checks = []
    for layout in layouts:
        for provider in providers:
            checks.append(f"{layout}.{provider}.help")
            checks.append(f"{layout}.{provider}.browser-login")
            checks.extend(f"{layout}.{provider}.{collection}" for collection in COLLECTION_BUTTONS[layout][provider])
            if provider == "XVideos":
                checks.extend((f"{layout}.{provider}.manual-tokens", f"{layout}.{provider}.token-liked"))
        checks.append(f"{layout}.validation-errors")
    return checks


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def extend_timeout_for_wait(timeout: asyncio.Timeout | None, seconds: float) -> None:
    if timeout is not None and not timeout.expired():
        deadline = timeout.when()
        if deadline is not None:
            timeout.reschedule(deadline + seconds)


def access_control_kind(status, html="", *, expected_private_denial=False):
    if status == 429:
        return "rate-limit"
    if status == 451:
        return "regional-access-control"
    if status in (401, 403) and not expected_private_denial:
        return "access-denied"
    if re.search(r"<title[^>]*>\s*(?:captcha|just a moment|security verification|verify you are human)", html, re.I):
        return "interactive-challenge"
    if 'onload="go()"' in html or "onload='go()'" in html:
        return "javascript-challenge"
    return None


def _native_pornhub_math_challenge(url, response_url, status, html):
    if status != 200 or 'onload="go()"' not in html:
        return False
    for address in (url, response_url or url):
        parsed = urlsplit(str(address))
        host = parsed.hostname or ""
        if parsed.scheme != "https" or not (host == "pornhub.com" or host.endswith(".pornhub.com")):
            return False
    # Recognize the payload accepted by BaseCore; arithmetic, cookies and retries
    # stay entirely in the native handler. Unknown go() pages remain blocked.
    return re.search(r'go\(\).*?{(.*?)n=l.*?KEY.*?s\+":(\d+):', html, re.DOTALL) is not None


class AccountAccessStopped(asyncio.CancelledError):
    """Stop access denials and unsupported/interactive challenges before native retries."""


class AccountAccessGuard:
    def __init__(self, *, initial_delay=0.0, cooldown=30.0, recovery_delay=5.0, max_rate_retries=2,
                 on_wait: Callable[[float], None] | None = None,
                 on_rate_limit: Callable[[dict], None] | None = None):
        self.blocked: dict[str, str | int | None] | None = None
        self.expected_private_denial = False
        self.sessions = []
        self.request_delay = max(0.0, float(initial_delay))
        self.cooldown = max(30.0, float(cooldown))
        self.recovery_delay = max(5.0, float(recovery_delay))
        self.max_rate_retries = max(0, int(max_rate_retries))
        self.rate_limit_events = []
        self.native_challenge_events = []
        self.total_wait_seconds = 0.0
        self.on_wait, self.on_rate_limit = on_wait, on_rate_limit
        self._request_lock = asyncio.Lock()
        self._next_request = 0.0
        self._clock = lambda: asyncio.get_running_loop().time()
        self._sleep: Callable[[float], Awaitable[None]] = asyncio.sleep

    @staticmethod
    def may_retry(method, url):
        if method.upper() in {"GET", "HEAD", "OPTIONS"}:
            return True
        # These provider POST endpoints only read account lists. Never replay
        # password submissions or other mutations automatically.
        return method.upper() == "POST" and re.fullmatch(
            r"/(?:history|videos-i-like|watch-later)/\d+/?", urlsplit(str(url)).path,
        ) is not None

    async def wait_for_turn(self):
        delay = max(0.0, self._next_request - self._clock())
        if delay:
            if self.on_wait is not None:
                self.on_wait(delay)
            started = self._clock()
            try:
                await self._sleep(delay)
            finally:
                self.total_wait_seconds += max(0.0, self._clock() - started)

    def raise_if_blocked(self):
        if self.blocked is not None:
            raise AccountAccessStopped("Account diagnostics stopped at an access control")

    def __enter__(self):
        original_initialize = BaseCore.initialize_session
        guard = self

        def initialize(core):
            original_initialize(core)
            session = core.session
            if session is None or getattr(session, "_account_access_guard", False):
                return
            request = session.request

            async def guarded(method, url, **kwargs):
                # Serialize requests across cores, including helper prefetches,
                # so none can slip through a cooldown or overwhelm the site.
                async with guard._request_lock:
                    for attempt in range(guard.max_rate_retries + 1):
                        guard.raise_if_blocked()
                        await guard.wait_for_turn()
                        response = await request(method, url, **kwargs)
                        content_type = response.headers.get("content-type", "").casefold()
                        html = response.text if not content_type or "html" in content_type else ""
                        challenge = access_control_kind(200, html)
                        native_math = challenge == "javascript-challenge" and _native_pornhub_math_challenge(
                            url, getattr(response, "url", None), response.status_code, html,
                        )
                        if native_math:
                            event = {"kind": "pornhub-math-challenge", "http_status": response.status_code,
                                     "host": urlsplit(str(url)).hostname, "handler": "eaf_base_api"}
                            guard.native_challenge_events.append(event)
                            logging.getLogger("account-access-control").info(
                                "Delegating supported PornHub math challenge to eaf_base_api")
                        if challenge and not native_math:
                            guard.blocked = {"kind": challenge, "http_status": response.status_code,
                                             "host": urlsplit(str(url)).hostname}
                            guard.raise_if_blocked()
                        if response.status_code == 429:
                            retry_after = parse_retry_after(logging.getLogger("account-rate-control"), response)
                            if retry_after is None or not math.isfinite(retry_after):
                                retry_after = 0.0
                            delay = max(guard.cooldown, retry_after)
                            guard.request_delay = max(guard.request_delay, guard.recovery_delay)
                            guard._next_request = guard._clock() + delay
                            retry = guard.may_retry(method, url) and attempt < guard.max_rate_retries
                            event = {"host": urlsplit(str(url)).hostname, "http_status": 429,
                                     "attempt": attempt + 1, "retry": retry,
                                     "wait_seconds": delay if retry else 0.0,
                                     "retry_after_seconds": retry_after,
                                     "request_delay_seconds": guard.request_delay}
                            guard.rate_limit_events.append(event)
                            if guard.on_rate_limit is not None:
                                guard.on_rate_limit(event)
                            if retry:
                                continue
                        guard._next_request = guard._clock() + guard.request_delay
                        kind = access_control_kind(response.status_code, "" if native_math else html,
                                                   expected_private_denial=guard.expected_private_denial)
                        if kind:
                            guard.blocked = {"kind": kind, "http_status": response.status_code,
                                             "host": urlsplit(str(url)).hostname}
                            guard.raise_if_blocked()
                        return response
                    guard.raise_if_blocked()
                    raise AssertionError("Rate-limit retry loop ended without a response")

            guard.sessions.append((session, request))
            session.request = guarded
            session._account_access_guard = True

        self.patch = patch.object(BaseCore, "initialize_session", initialize)
        self.patch.__enter__()
        return self

    @contextmanager
    def private_denial_probe(self):
        self.expected_private_denial = True
        try:
            yield
        finally:
            self.expected_private_denial = False

    def __exit__(self, *error):
        self.patch.__exit__(*error)
        for session, original in self.sessions:
            session.request = original
            session._account_access_guard = False



def visual_items(item):
    yield item
    for child in item.childItems():
        yield from visual_items(child)


def make_account_backend():
    backend = make_test_backend()
    backend.logger = logging.getLogger("account-diagnostics")
    backend._background_tasks = set()
    backend._activity_active = False
    backend._login_task = None
    backend._login_in_progress = False
    backend._video_fetch_task = None
    backend._account_fetch_task = None
    backend._account_fetch_in_progress = False
    backend._license_bridge = None
    backend.database_bridge = None
    backend._is_shutting_down = False
    backend._client_refresh_pending = False
    backend._download_tasks = {}
    backend._download_stop_events = {}
    return backend


class AccountWindow:
    """Load production account/download pages, including real ListView delegates."""

    def __init__(self, backend, layout):
        from src.backend.config import app_settings
        from src.frontend.UI import resources

        resources.qInitResources()
        self.backend, self.layout = backend, layout
        self.engine = QQmlApplicationEngine()
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(errors))
        self.engine.rootContext().setContextProperty("backend", backend)
        self.engine.rootContext().setContextProperty("appSettings", app_settings)
        account = ('AccountPage { backendController: backend;' if layout == "desktop" else 'AndroidAccountPage {')
        downloads = "DownloadsPage" if layout == "desktop" else "AndroidDownloadsPage"
        source = '''
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
ApplicationWindow {
    visible: true; width: WIDTH; height: 1100
    property bool androidLayout: false
    property QtObject bridge: QtObject { property bool isPremium: false }
    RowLayout {
        anchors.fill: parent
        ACCOUNT objectName: "accountPage"; Layout.fillWidth: true; Layout.fillHeight: true; Layout.preferredWidth: 700 }
        DOWNLOADS { objectName: "downloadsPage"; Layout.fillWidth: true; Layout.fillHeight: true; Layout.preferredWidth: 1200 }
    }
}
'''.replace("WIDTH", "1900" if layout == "desktop" else "1200").replace("ACCOUNT", account).replace("DOWNLOADS", downloads)
        self.engine.loadData(source.encode(), QUrl.fromLocalFile(str(UI / "AccountDiagnostic.qml")))
        require(bool(self.engine.rootObjects()), "The real QML account/download pages did not load")
        self.window = self.engine.rootObjects()[0]
        require(isinstance(self.window, QQuickWindow), "Account diagnostic root is not a Quick window")
        self.page = next(item for item in visual_items(self.window.contentItem()) if item.objectName() == "accountPage")
        self.downloads = next(item for item in visual_items(self.window.contentItem()) if item.objectName() == "downloadsPage")
        QGuiApplication.processEvents()

    def controls(self, property_name, value):
        return [item for item in visual_items(self.page)
                if item.isVisible() and item.property(property_name) == value]

    def control(self, property_name, value):
        items = self.controls(property_name, value)
        require(bool(items), "An expected account control is absent")
        return items[0]

    def click(self, text):
        button = self.control("text", text)
        require(button.property("enabled"), "An expected account action is disabled")
        require(QMetaObject.invokeMethod(button, "clicked", Qt.ConnectionType.DirectConnection), "QML click failed")
        QGuiApplication.processEvents()

    def provider(self, name):
        button = self.control("text", name)
        point = button.mapToScene(QPointF(button.width() / 2, button.height() / 2)).toPoint()
        QTest.mouseClick(self.window, Qt.MouseButton.LeftButton, pos=point)
        QGuiApplication.processEvents()
        key = "selectedProvider" if self.layout == "desktop" else "provider"
        require(self.page.property(key) == name, "Provider selection did not update")

    def field(self, placeholder, text):
        self.control("placeholderText", placeholder).setProperty("text", text)
        QGuiApplication.processEvents()

    def collection_button(self, provider, collection):
        return self.control("text", COLLECTION_BUTTONS[self.layout][provider][collection])

    def verify_action_inventory(self, provider):
        actual = {item.property("text") for item in visual_items(self.page)
                  if item.isVisible() and item.inherits("QQuickAbstractButton")}
        expected = set(PROVIDERS) | {"How to login"} | set(COLLECTION_BUTTONS[self.layout][provider].values())
        if self.layout == "desktop":
            expected |= {"Login with Browser Cookies", "Login with Session Tokens" if provider == "XVideos" else "Login"}
        else:
            expected.add("Sign in")
        require(actual == expected, "Visible account actions differ from the complete action inventory")
        return len(expected)

    async def finish(self, task):
        require(task is not None, "The QML action did not start a backend task")
        try:
            while not task.done():
                QGuiApplication.processEvents()
                await asyncio.sleep(.01)
            await task
            await asyncio.sleep(0)
            QGuiApplication.processEvents()
        finally:
            if not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
        require(not self.warnings, "The production QML pages emitted binding errors")

    def verify_rows(self, *, before=0, limit=2):
        model = self.backend._downloads_model
        count = model.rowCount() - before
        require(1 <= count <= limit, "Expected bounded, nonempty account rows in the GUI model")
        expected_roles = {b"jobId", b"title", b"author", b"duration", b"availableQualities", b"selectedQuality",
                          b"progress", b"selected", b"status"}
        require(set(bytes(role) for role in model.roleNames().values()) == expected_roles, "List role contract changed")
        view = next(item for item in visual_items(self.downloads) if item.inherits("QQuickListView"))
        view.setProperty("contentY", 0)
        QMetaObject.invokeMethod(view, "forceLayout")
        QTest.qWait(30)
        require(view.property("count") == model.rowCount(), "ListView count differs from its Qt model")
        for row in range(before, model.rowCount()):
            index = model.index(row, 0)
            job = model.data(index, model.JobIdRole)
            video = model.get_video(job)
            if video is None or video.source_video is None:
                raise AssertionError("A row lost its native video")
            require(video.title.strip() and video.author.strip(), "A row has missing title/author metadata")
            require(isinstance(video.length, int) and video.length > 0, "A row has no positive normalized duration")
            require(video.url.startswith("https://") and video.thumbnail_url.startswith("https://"), "A row has missing media/thumbnail URLs")
            require(bool(video.video_id) and isinstance(video.tags, list), "A row has missing identity/tags")
            require(video.output_path is not None and not video.output_path.exists(), "Account loading created a media file")
            expected = {
                "jobId": job, "title": f"{row + 1}) {video.title}", "author": video.author,
                "duration": model.tr("%d min") % video.length,
                "availableQualities": [str(q) for q in video.qualities],
                "selectedQuality": video.selected_quality, "progress": 0, "selected": False, "status": "pending",
            }
            # The model may choose another concrete free quality than the provider's preferred one.
            expected["selectedQuality"] = model.data(index, model.SelectedQualityRole)
            require(expected["selectedQuality"] in expected["availableQualities"], "Selected quality is unavailable")
            delegates = [item for item in visual_items(view) if item.property("jobId") == job]
            require(bool(delegates), "The actual Downloads ListView did not instantiate an account row")
            delegate = delegates[0]
            for role, value in model.roleNames().items():
                name = bytes(value).decode()
                require(model.data(index, role) == expected[name], "A QML model role differs from prepared metadata")
                actual = delegate.property(name)
                if hasattr(actual, "toVariant"):
                    actual = actual.toVariant()
                require(actual == expected[name], "A rendered ListView delegate received incorrect metadata")
            labels = [item.property("text") for item in visual_items(delegate)]
            rendered = (expected["title"], expected["author"] + " · " + expected["duration"]) if self.layout == "mobile" else (
                expected["title"], expected["author"], expected["duration"])
            require(all(text in labels for text in rendered),
                    "A rendered account row does not display its title, author and duration")
            require(bool(video.origin_iterator_name), "Account rows lost their collection identity")
        require(not self.warnings, "Rendered account delegates emitted QML binding errors")
        return {"rows": count, "roles_verified": len(expected_roles), "rendered_delegates_verified": count}

    def clear_rows(self):
        model = self.backend._downloads_model
        for row in reversed(range(model.rowCount())):
            self.backend.remove_video(model.data(model.index(row, 0), model.JobIdRole))
        QGuiApplication.processEvents()
        require(model.rowCount() == 0, "Removing prepared account rows did not clear the list")

    def close(self):
        self.window.close()
        self.window.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        self.engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)


async def test_account_collection(window, provider, collection, *, playlist_url="", items=2):
    backend = window.backend
    model = backend._downloads_model
    window.clear_rows()
    window.provider(provider)
    if collection == "playlist":
        placeholder = "https://xhamster.com/my/playlists/..." if window.layout == "desktop" else "Account playlist URL"
        window.field(placeholder, playlist_url)
    inserted, errors = QSignalSpy(model.rowsInserted), QSignalSpy(backend.showMessage)
    states = QSignalSpy(backend.accountFetchStateChanged)
    window.click(COLLECTION_BUTTONS[window.layout][provider][collection])
    require(backend.accountFetchInProgress and backend.busy, "Fetch did not expose its loading state")
    task = backend._account_fetch_task
    require(not window.collection_button(provider, collection).property("enabled"), "Collection controls remained enabled while loading")
    # A second request while busy must keep the same task, with no duplicate fetch.
    backend.fetch_account_videos(provider, collection, playlist_url)
    require(backend._account_fetch_task is task, "A duplicate fetch was started while busy")
    await window.finish(task)
    require(not backend.busy and not backend.accountFetchInProgress, "Fetch left the GUI busy")
    require(states.count() >= 2, "Loading notifications did not return to idle")
    require(errors.count() == 0, "The real account pipeline reported an error")
    require(inserted.count() == model.rowCount(), "Inserted rows were not signalled individually")
    return window.verify_rows(limit=items)
