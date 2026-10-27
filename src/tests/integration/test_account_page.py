"""Account control wiring and deterministic GUI recovery contracts.

Live data/list checks live in account_gui. This module never submits credentials
or fabricates provider responses: its recording bridge checks QML arguments,
and explicit exceptions exercise backend recovery without real failed logins.
"""
from __future__ import annotations

import asyncio
import os
import unittest
from unittest.mock import AsyncMock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("PORN_FETCH_TEST_ENV", "1")

from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlEngine, QQmlExpression

_app = QGuiApplication.instance() or QGuiApplication([])

from src.backend.account_diagnostics import COLLECTION_BUTTONS, PROVIDERS, AccountWindow, make_account_backend
from src.backend.download_manager import DownloadListModel
from src.shared.errors import CookiesNotFound, LoginError


class RecordingAccountBridge(QObject):
    loginStateChanged = Signal()
    accountStateChanged = Signal()
    accountFetchStateChanged = Signal()
    busyChanged = Signal()

    def __init__(self):
        super().__init__()
        self.model = DownloadListModel(self)
        self.logins, self.fetches = [], []
        self.status = {provider: False for provider in PROVIDERS}
        self.login_busy, self.fetch_busy = False, False

    @Property(QObject, constant=True)
    def downloads(self):
        return self.model

    @Property("QVariantMap", notify=accountStateChanged)
    def accountLoginStatus(self):
        return self.status

    @Property(bool, notify=loginStateChanged)
    def loginInProgress(self):
        return self.login_busy

    @Property(bool, notify=accountFetchStateChanged)
    def accountFetchInProgress(self):
        return self.fetch_busy

    @Property(bool, notify=busyChanged)
    def busy(self):
        return self.fetch_busy

    @Slot(str, str, str, bool)
    def login_account(self, provider, identity, secret, cookies):
        self.logins.append((provider, identity, secret, cookies))

    @Slot(str, str, str)
    def fetch_account_videos(self, provider, collection, url):
        self.fetches.append((provider, collection, url))

    def set_state(self, *, provider=None, logged=None, login=False, fetch=False):
        if provider is not None:
            self.status = dict(self.status, **{provider: logged})
            self.accountStateChanged.emit()
        self.login_busy, self.fetch_busy = login, fetch
        self.loginStateChanged.emit()
        self.accountFetchStateChanged.emit()
        self.busyChanged.emit()
        _app.processEvents()


class AccountPageControlTests(unittest.TestCase):
    def test_every_provider_form_and_collection_action_on_both_layouts(self):
        for layout in ("desktop", "mobile"):
            bridge = RecordingAccountBridge()
            window = AccountWindow(bridge, layout)
            try:
                for provider in PROVIDERS:
                    with self.subTest(layout=layout, provider=provider):
                        window.provider(provider)
                        window.verify_action_inventory(provider)
                        for collection in COLLECTION_BUTTONS[layout][provider]:
                            self.assertFalse(window.collection_button(provider, collection).property("enabled"))
                        token = provider == "XVideos"
                        if token:
                            fields = ("Enter session_token", "Enter session_token_auth") if layout == "desktop" else (
                                "session_token", "session_token_auth")
                        else:
                            fields = (("Enter your username" if provider == "XHamster" else "Enter your email address"),
                                      "Enter your password") if layout == "desktop" else (
                                          "Username" if provider == "XHamster" else "Email address", "Password")
                        window.field(fields[0], "")
                        window.field(fields[1], "")
                        button_text = ("Login with Session Tokens" if token else "Login") if layout == "desktop" else "Sign in"
                        button = window.control("text", button_text)
                        self.assertFalse(button.property("enabled"))
                        window.field(fields[0], "identity-fixture")
                        self.assertFalse(button.property("enabled"))
                        window.field(fields[1], "secret-fixture")
                        field = window.control("placeholderText", fields[1])
                        expression = QQmlExpression(QQmlEngine.contextForObject(field), field, "Number(echoMode)")
                        self.assertEqual(expression.evaluate()[0], 2)
                        window.click(button_text)
                        self.assertEqual(bridge.logins[-1], (provider, "identity-fixture", "secret-fixture", False))
                        if layout == "desktop":
                            if provider == "PornHub":
                                window.field("PornHub username for browser cookies (not email)", "profile-fixture")
                            window.click("Login with Browser Cookies")
                            self.assertEqual(bridge.logins[-1][0], provider)
                            self.assertEqual(bridge.logins[-1][2:], ("", True))
                        else:
                            self.assertFalse(window.controls("text", "Login with Browser Cookies"))
                        bridge.set_state(provider=provider, logged=True)
                        for collection in COLLECTION_BUTTONS[layout][provider]:
                            url = ""
                            if collection == "playlist":
                                placeholder = "https://xhamster.com/my/playlists/..." if layout == "desktop" else "Account playlist URL"
                                url = "https://xhamster.com/my/favorites/videos/fixture"
                                window.field(placeholder, " " + url + " ")
                            window.click(COLLECTION_BUTTONS[layout][provider][collection])
                            self.assertEqual(bridge.fetches[-1], (provider, collection, url))
                        for phase in ("login", "fetch"):
                            bridge.set_state(**{phase: True})
                            self.assertFalse(button.property("enabled"))
                            self.assertTrue(all(not window.collection_button(provider, c).property("enabled")
                                                for c in COLLECTION_BUTTONS[layout][provider]))
                            bridge.set_state()
                            self.assertTrue(button.property("enabled"))
                        self.assertIn(provider, window.control("text", "How to login").property("helpText"))
                self.assertEqual(window.warnings, [])
            finally:
                window.close()


class AccountPaginationTests(unittest.TestCase):
    def test_only_missing_later_pages_are_skipped(self):
        from base_api import ErrorAction, ScrapeErrorContext
        from base_api.modules.errors import HTTPStatusError
        from base_api.modules.type_hints import ScrapeStage

        from src.backend.login_manager import _account_page_error, _account_video_iterator_config

        for index, status, expected in ((1, 404, ErrorAction.SKIP), (0, 404, ErrorAction.YIELD),
                                        (1, 403, ErrorAction.YIELD), (1, 500, ErrorAction.YIELD)):
            error = HTTPStatusError("HTTP failure", status_code=status, url="https://example.test/account")
            context = ScrapeErrorContext(ScrapeStage.PAGE, "https://example.test/account", error, 1, 1, index, None)
            self.assertEqual(_account_page_error(context), expected)
        config = _account_video_iterator_config(post=True)
        self.assertEqual(config._page_request_method, "POST")
        self.assertEqual(config.item_error_mode.value, "yield")


class AccountAccessControlTests(unittest.IsolatedAsyncioTestCase):
    def test_access_controls_stop_before_retry_or_challenge_handling(self):
        from src.backend.account_diagnostics import AccountAccessGuard, AccountAccessStopped, access_control_kind

        self.assertEqual(access_control_kind(429), "rate-limit")
        self.assertEqual(access_control_kind(403), "access-denied")
        self.assertEqual(access_control_kind(451), "regional-access-control")
        self.assertEqual(access_control_kind(200, '<body onload="go()">'), "javascript-challenge")
        self.assertEqual(access_control_kind(200, '<title>CAPTCHA verification</title>'), "interactive-challenge")
        self.assertIsNone(access_control_kind(200, '"recaptchaKey":"page configuration"'))
        self.assertIsNone(access_control_kind(403, expected_private_denial=True))
        self.assertEqual(access_control_kind(429, expected_private_denial=True), "rate-limit")
        guard = AccountAccessGuard()
        guard.blocked = {"kind": "rate-limit", "http_status": 429}
        with self.assertRaises(AccountAccessStopped):
            guard.raise_if_blocked()

    async def test_session_guard_makes_no_further_request_after_rate_limit(self):
        from types import SimpleNamespace

        from base_api import BaseCore
        from curl_cffi.requests import Response
        from curl_cffi.requests.headers import Headers

        from src.backend.account_diagnostics import AccountAccessGuard, AccountAccessStopped

        # Protocol-level failure fixture, never a fabricated account/video result.
        response = Response()
        response.status_code = 429
        response.headers = Headers({"content-type": "text/html"})
        response.content = b"Too many requests"
        transport = AsyncMock(return_value=response)
        session = SimpleNamespace(request=transport)
        core = BaseCore.__new__(BaseCore)
        setattr(core, "session", session)
        with patch.object(BaseCore, "initialize_session", lambda _core: None):
            with AccountAccessGuard(max_rate_retries=0) as guard:
                core.initialize_session()
                for _ in range(2):
                    with self.assertRaises(AccountAccessStopped):
                        await session.request("GET", "https://example.test/account")
                self.assertEqual(transport.await_count, 1)
                assert guard.blocked is not None
                self.assertEqual(guard.blocked["http_status"], 429)
            self.assertIs(session.request, transport)

    async def test_429_recovery_honors_retry_after_and_paces_other_cores(self):
        from types import SimpleNamespace

        from base_api import BaseCore
        from curl_cffi.requests import Response
        from curl_cffi.requests.headers import Headers

        from src.backend.account_diagnostics import AccountAccessGuard

        responses = []
        for status in (429, 200, 200):
            response = Response()
            response.status_code = status
            response.headers = Headers({"content-type": "text/plain", "Retry-After": "60"})
            response.content = b"Protocol fixture"
            responses.append(response)
        clock, starts, waits = [0.0], [], []
        async def request(*args, **kwargs):
            starts.append(clock[0])
            return responses.pop(0)
        async def sleep(delay):
            waits.append(delay)
            clock[0] += delay
        first, second = BaseCore.__new__(BaseCore), BaseCore.__new__(BaseCore)
        first_session, second_session = SimpleNamespace(request=request), SimpleNamespace(request=request)
        setattr(first, "session", first_session)
        setattr(second, "session", second_session)
        guard = AccountAccessGuard()
        guard._clock, guard._sleep = lambda: clock[0], sleep
        with patch.object(BaseCore, "initialize_session", lambda _core: None), guard:
            first.initialize_session()
            second.initialize_session()
            await first_session.request("POST", "https://www.xvideos.com/videos-i-like/0")
            await second_session.request("GET", "https://example.test/metadata")
        self.assertEqual(starts, [0, 60, 65])
        self.assertEqual(waits, [60, 5])
        self.assertEqual(guard.request_delay, 5)
        self.assertIsNone(guard.blocked)

    async def test_repeated_429_has_a_30_second_floor_and_bounded_retries(self):
        from types import SimpleNamespace

        from base_api import BaseCore
        from curl_cffi.requests import Response
        from curl_cffi.requests.headers import Headers

        from src.backend.account_diagnostics import AccountAccessGuard, AccountAccessStopped

        response = Response()
        response.status_code = 429
        response.headers = Headers({"Retry-After": "1"})
        response.content = b"Limited"
        transport = AsyncMock(return_value=response)
        clock, waits = [0.0], []
        async def sleep(delay):
            waits.append(delay)
            clock[0] += delay
        core = BaseCore.__new__(BaseCore)
        session = SimpleNamespace(request=transport)
        setattr(core, "session", session)
        guard = AccountAccessGuard(max_rate_retries=1)
        guard._clock, guard._sleep = lambda: clock[0], sleep
        with patch.object(BaseCore, "initialize_session", lambda _core: None), guard:
            core.initialize_session()
            with self.assertRaises(AccountAccessStopped):
                await session.request("GET", "https://example.test/metadata")
        self.assertEqual(waits, [30])
        self.assertEqual(transport.await_count, 2)
        self.assertEqual([event["retry"] for event in guard.rate_limit_events], [True, False])

    async def test_password_submissions_are_not_replayed_after_429(self):
        from src.backend.account_diagnostics import AccountAccessGuard

        self.assertFalse(AccountAccessGuard.may_retry("POST", "https://example.test/account"))
        self.assertFalse(AccountAccessGuard.may_retry("POST", "https://example.test/front/authenticate"))

    async def test_intentional_wait_extends_the_network_timeout_budget(self):
        from src.backend.account_diagnostics import extend_timeout_for_wait

        async with asyncio.timeout(.01) as timeout:
            deadline = timeout.when()
            assert deadline is not None
            extend_timeout_for_wait(timeout, 30)
            await asyncio.sleep(.02)
            self.assertEqual(timeout.when(), deadline + 30)
            self.assertFalse(timeout.expired())

    async def test_captcha_on_a_429_stops_without_rate_limit_retries(self):
        from types import SimpleNamespace

        from base_api import BaseCore
        from curl_cffi.requests import Response
        from curl_cffi.requests.headers import Headers

        from src.backend.account_diagnostics import AccountAccessGuard, AccountAccessStopped

        response = Response()
        response.status_code = 429
        response.headers = Headers({"content-type": "text/html"})
        response.content = b"<title>CAPTCHA verification</title>"
        transport = AsyncMock(return_value=response)
        session = SimpleNamespace(request=transport)
        core = BaseCore.__new__(BaseCore)
        setattr(core, "session", session)
        with patch.object(BaseCore, "initialize_session", lambda _core: None), AccountAccessGuard() as guard:
            core.initialize_session()
            with self.assertRaises(AccountAccessStopped):
                await session.request("GET", "https://example.test/account")
            self.assertEqual(transport.await_count, 1)
            self.assertEqual(guard.rate_limit_events, [])


class AccountBackendRecoveryTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.backend = make_account_backend()
        old_disabled = self.backend.logger.disabled
        self.backend.logger.disabled = True
        self.addCleanup(setattr, self.backend.logger, "disabled", old_disabled)
        self.messages = []
        self.backend.showMessage.connect(self.messages.append)

    async def test_each_native_login_dispatch_and_normal_failure(self):
        cases = (("PornHub", "LoginPornhub", {"email": "identity", "password": "secret", "from_browser": False}),
                 ("XHamster", "LoginXhamster", {"username": "identity", "password": "secret", "from_browser": False}),
                 ("XVideos", "LoginXVideos", {"custom_cookies": {"session_token": "identity", "session_token_auth": "secret"}, "from_browser": False}))
        for provider, name, options in cases:
            for result in (True, False):
                self.backend._login_in_progress = True
                with patch(f"src.backend.application.{name}.login", AsyncMock(return_value=result)) as login:
                    await self.backend._run_login_account(provider, " identity ", "secret")
                login.assert_awaited_once_with(**options)
                self.assertFalse(self.backend.loginInProgress)
        with patch("src.backend.application.LoginXVideos.login", AsyncMock(return_value=True)) as login:
            await self.backend._run_login_account("XVideos", "", "", True)
        login.assert_awaited_once_with(custom_cookies=None, from_browser=True)

    async def test_login_errors_always_restore_idle_and_notify_user(self):
        from pornhub_api.modules.errors import ClientAlreadyLogged, LoginFailed
        from xhamster_api.modules.errors import LoginFailed as XhLoginFailed

        errors = (CookiesNotFound(), LoginFailed("rejected"), XhLoginFailed("rejected"), ClientAlreadyLogged(),
                  LoginError("invalid input"), RuntimeError("unexpected"))
        for error in errors:
            self.backend._login_in_progress = True
            before = len(self.messages)
            with patch("src.backend.application.LoginPornhub.login", AsyncMock(side_effect=error)), \
                    patch("src.backend.application.report_exception", AsyncMock()):
                await self.backend._run_login_account("PornHub", "identity", "secret")
            self.assertFalse(self.backend.loginInProgress)
            self.assertEqual(len(self.messages), before + 1)
        await self.backend._run_login_account("Unknown", "", "")
        self.assertIn("not supported", self.messages[-1])

    async def test_failed_token_relogin_notifies_qml_that_the_old_account_was_cleared(self):
        from PySide6.QtTest import QSignalSpy

        from src.backend import clients

        changed = QSignalSpy(self.backend.accountStateChanged)
        old_account = clients.xv_client.account
        self.addCleanup(setattr, clients.xv_client, "account", old_account)
        clients.xv_client.account = object()
        async def rejected(**kwargs):
            clients.xv_client.account = None
            raise LoginError("Session expired")
        with patch("src.backend.application.LoginXVideos.login", rejected):
            await self.backend._run_login_account("XVideos", "fixture", "fixture")
        self.assertFalse(self.backend.property("accountLoginStatus")["XVideos"])
        self.assertEqual(changed.count(), 1)

    async def test_fetch_errors_always_restore_idle_without_rows(self):
        from pornhub_api.modules.errors import LoginFailed
        from xhamster_api.modules.errors import LoginFailed as XhLoginFailed

        for error in (LoginError("invalid collection"), LoginFailed("expired"), XhLoginFailed("expired"), RuntimeError("failure")):
            self.backend._account_fetch_in_progress = True
            before = len(self.messages)
            with patch("src.backend.application.get_account_video_iterator", side_effect=error), \
                    patch("src.backend.application.report_exception", AsyncMock()):
                await self.backend._run_fetch_account_videos("PornHub", "history")
            self.assertFalse(self.backend.accountFetchInProgress)
            self.assertEqual(len(self.messages), before + 1)
            self.assertEqual(self.backend.downloads.rowCount(), 0)

    async def test_cancelling_login_restores_idle_and_duplicate_login_is_ignored(self):
        pending = asyncio.Event()

        async def blocked(**kwargs):
            await pending.wait()
        with patch("src.backend.application.LoginPornhub.login", blocked):
            self.backend.login_account("PornHub", "identity", "secret")
            task = self.backend._login_task
            assert task is not None
            self.backend.login_account("XHamster", "other", "other")
            self.assertIs(self.backend._login_task, task)
            await asyncio.sleep(0)
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
            await asyncio.sleep(0)
        self.assertFalse(self.backend.loginInProgress)

    async def test_cancelling_fetch_restores_idle_and_allows_another_request(self):
        from src.backend.application import stop_flag

        self.addCleanup(stop_flag.clear)
        pending = asyncio.Event()
        async def stream():
            await pending.wait()
            if False:
                yield None
        with patch("src.backend.application.get_account_video_iterator", return_value=(stream(), "Account fixture")):
            self.backend.fetch_account_videos("PornHub", "history")
            task = self.backend._account_fetch_task
            await asyncio.sleep(0)
            self.backend.cancel_fetching()
            await asyncio.gather(task, return_exceptions=True)
            await asyncio.sleep(0)
        self.assertFalse(self.backend.accountFetchInProgress)
        self.assertFalse(self.backend.busy)
        with patch("src.backend.application.get_account_video_iterator", side_effect=LoginError("invalid collection")):
            self.backend.fetch_account_videos("PornHub", "invalid")
            task = self.backend._account_fetch_task
            assert task is not None
            await task
            await asyncio.sleep(0)
        self.assertFalse(stop_flag.is_set())
        self.assertFalse(self.backend.busy)


if __name__ == "__main__":
    unittest.main()
