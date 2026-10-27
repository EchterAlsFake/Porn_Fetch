"""Opt-in real-cookie account-page checks through Qt/QML and the Downloads list.

Run: uv run python -m src.tests.smoke.account_gui --browser brave
"""
from __future__ import annotations

import argparse
import asyncio
import inspect
import io
import json
import logging
import os
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from functools import partial
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch


async def run(args):
    import xhamster_api
    from PySide6.QtCore import QMetaObject, Qt, qInstallMessageHandler
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtTest import QAbstractItemModelTester, QSignalSpy
    from xhamster_api.modules.consts import extractor_videos as xhamster_extractor

    from src.backend import application, clients, login_manager, video_processor
    from src.backend.account_diagnostics import (
        COLLECTION_BUTTONS,
        PROVIDERS,
        AccountAccessGuard,
        AccountWindow,
        account_check_inventory,
        extend_timeout_for_wait,
        make_account_backend,
        require,
        test_account_collection,
    )
    from src.backend.profile_diagnostics import MetadataOnlyRequests, diagnostic_settings
    from src.shared.provider_accounts import verify_account_session
    from src.tests.smoke.account_cookies import discover_playlist

    report = {"scope": "Actual QML account buttons, real browser cookies/provider APIs, GUI preparation and rendered Downloads list roles",
              "started_at_utc": datetime.now(timezone.utc).isoformat(), "browser": args.browser,
              "checks": [], "layouts": args.layouts, "interrupted": False,
              "offline_contracts": args.contracts,
              "xhamster_source": str(Path(xhamster_api.__file__).resolve()),
              "libraries": {name: version(name) for name in ("PySide6", "browser-cookie3", "eaf-base-api",
                            "unofficial-api-for-pornhub", "unofficial-api-for-xhamster", "unofficial-api-for-xvideos")}}
    planned = account_check_inventory(args.layouts, args.providers)
    if args.xvideos_playlist:
        planned.append("XVideos.playlist-listview")
        if args.xvideos_private:
            planned.append("XVideos.private-playlist-authorization")
    report["planned_checks"] = planned
    report["scope_exclusions"] = ["Source line/branch coverage is not this checklist metric",
                                  "XVideos password login is unsupported",
                                  "Mobile QML is tested on desktop, not Android OS cookie storage"]
    report["private_playlist"] = {"configured": args.xvideos_private, "verified": False}
    try:
        report["xhamster_account_json_fix"] = "likedVideosListProps" in inspect.getsource(xhamster_extractor)
    except (OSError, TypeError):
        report["xhamster_account_json_fix"] = None
    args.report.parent.mkdir(parents=True, exist_ok=True)
    pipeline_errors = []
    model_errors = []
    active_timeout: asyncio.Timeout | None = None
    console = sys.stdout

    def recovery_wait(seconds):
        # Intentional backoff/pacing is not network execution time. Keep the
        # per-check network budget intact while the GUI remains responsive.
        extend_timeout_for_wait(active_timeout, seconds)

    def rate_limit(event):
        event["check"] = active_check
        if event["retry"]:
            print(f"HTTP 429 from {event['host']}: waiting {event['wait_seconds']:.0f}s, "
                  f"then requests at least {event['request_delay_seconds']:.0f}s apart.", file=console, flush=True)
        else:
            print("HTTP 429 retry budget exhausted or request not safe to replay; stopping.", file=console, flush=True)

    active_check = ""
    access_guard = AccountAccessGuard(initial_delay=args.request_delay, cooldown=args.rate_cooldown,
                                      recovery_delay=args.recovery_delay, max_rate_retries=args.rate_retries,
                                      on_wait=recovery_wait, on_rate_limit=rate_limit)

    def qt_message(_kind, _context, message):
        if message.startswith("FAIL!"):
            model_errors.append(True)

    async def observe_report(original, error, *params, **options):
        status = None
        current = error
        seen = set()
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            status = getattr(current, "status_code", None) or status
            current = current.__cause__
        pipeline_errors.append({"error_type": type(error).__name__, "http_status": status,
                                "operation": options.get("operation")})
        return await original(error, *params, **options)

    def save():
        report["native_challenges"] = access_guard.native_challenge_events
        report["rate_limit_recovery"] = {"events": access_guard.rate_limit_events,
                                         "wait_seconds": round(access_guard.total_wait_seconds, 3),
                                         "request_delay_seconds": access_guard.request_delay}
        report["counts"] = {status: sum(check["status"] == status for check in report["checks"])
                            for status in ("PASS", "FAIL", "UNVERIFIED", "BLOCKED", "INTERRUPTED")}
        passed = {item["id"] for item in report["checks"] if item["status"] == "PASS"}
        report["action_coverage"] = {
            "metric": "Selected account GUI action checklist", "planned": len(planned),
            "passed": len(set(planned) & passed), "percent": round(100 * len(set(planned) & passed) / len(planned), 1),
            "not_passed": sorted(set(planned) - passed),
        }
        fd = os.open(args.report, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)
            file.write("\n")

    async def check(name, operation):
        nonlocal active_timeout, active_check
        active_check = name
        print(f"RUN {name}", flush=True)
        result = {"id": name, "status": "FAIL"}
        pipeline_errors.clear()
        started = time.monotonic()
        try:
            # ProcessVideos prints native objects/URLs. Discard these rather than
            # persisting account data, signed URLs or cookie-bearing exceptions.
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                active_timeout = asyncio.timeout(args.timeout)
                async with active_timeout:
                    result.update(await operation() or {})
            require(not model_errors, "QAbstractItemModelTester reported a model contract failure")
            result["status"] = "PASS"
        except asyncio.CancelledError:
            if access_guard.blocked is not None:
                result["status"] = "BLOCKED"
                result["access_control"] = access_guard.blocked
                report["stopped_by_access_control"] = access_guard.blocked
            else:
                result["status"] = "INTERRUPTED"
                report["interrupted"] = True
            raise
        except Exception as error:
            result["error_type"] = type(error).__name__
            result["error"] = str(error) if type(error) is AssertionError else "Upstream details omitted to protect session data"
            if (name.endswith(".XHamster.liked") and "nonempty account rows" in result["error"]
                    and report["libraries"]["unofficial-api-for-xhamster"] == "2.6.3"
                    and report["xhamster_account_json_fix"] is False):
                result["error"] += "; installed XHamster 2.6.3 lacks the account JSON fix. Use the fixed source checkout via PYTHONPATH or update the provider package."
        finally:
            active_timeout = None
            if pipeline_errors:
                result["pipeline_errors"] = list(pipeline_errors)
            result["elapsed_seconds"] = round(time.monotonic() - started, 2)
            report["model_tester_failures"] = len(model_errors)
            report["checks"].append(result)
            save()
            print(f"{result['status']} {name}" + (f": {result['error']}" if result.get("error") else ""), flush=True)
        return result["status"] == "PASS"

    original_reader = login_manager.get_site_cookies
    backend = make_account_backend()
    tester = QAbstractItemModelTester(backend._downloads_model, QAbstractItemModelTester.FailureReportingMode.Warning)
    for provider in PROVIDERS:
        cfg = clients.client_for(provider.casefold()).core.configuration
        cfg.timeout, cfg.request_attempts, cfg.request_delay = 20, 1, 0
        cfg.pages_concurrency, cfg.videos_concurrency = 1, 1
        cfg.response_cache_size_bytes, cfg.segment_cache_size_bytes = 0, 0
    save()
    try:
        with ExitStack() as stack:
            previous_handler = qInstallMessageHandler(qt_message)
            stack.callback(qInstallMessageHandler, previous_handler)
            stack.enter_context(MetadataOnlyRequests())
            stack.enter_context(access_guard)
            stack.enter_context(diagnostic_settings(items=args.items))
            stack.enter_context(patch.object(login_manager, "get_site_cookies", partial(original_reader, browser_name=args.browser)))
            for module in (application, video_processor):
                stack.enter_context(patch.object(module, "report_exception", partial(observe_report, module.report_exception)))
            xh_playlist = args.xhamster_playlist
            for layout in args.layouts:
                window = AccountWindow(backend, layout)
                try:
                    for provider in args.providers:
                        window.provider(provider)

                        async def help_dialog():
                            window.verify_action_inventory(provider)
                            help_button = window.control("text", "How to login")
                            require(provider in help_button.property("helpText"), "Help text does not describe the selected provider")
                            window.click("How to login")
                            # Popups are QObjects outside the visual item tree.
                            from PySide6.QtCore import QObject
                            dialogs = [obj for obj in window.window.findChildren(QObject)
                                       if obj.property("visible") and obj.property("title") == "Help"]
                            require(bool(dialogs), "How to login did not open the real help dialog")
                            QMetaObject.invokeMethod(dialogs[0], "close", Qt.ConnectionType.DirectConnection)
                            QGuiApplication.processEvents()
                            return {"provider_help_verified": True}

                        await check(f"{layout}.{provider}.help", help_dialog)
                        async def cookie_login():
                            if layout != "desktop":
                                # Desktop browser sessions supply the mobile QML
                                # data checks; Android has no cookie-import button.
                                backend.login_account(provider, "", "", True)
                            else:
                                if provider == "PornHub":
                                    jar = await asyncio.to_thread(original_reader, "pornhub", browser_name=args.browser)
                                    client = clients.ph_client
                                    session = client.core.session
                                    require(session is not None, "The PornHub session was not initialized")
                                    if session is None:
                                        raise AssertionError("The PornHub session was not initialized")
                                    session.cookies.update(jar)
                                    username = await verify_account_session(client, "pornhub")
                                    client.logged = False
                                    backend.accountStateChanged.emit()
                                    window.field("PornHub username for browser cookies (not email)", username)
                                window.click("Login with Browser Cookies")
                            require(backend.loginInProgress, "Login did not expose a busy state")
                            task = backend._login_task
                            backend.login_account(provider, "", "", True)
                            require(task is backend._login_task, "A duplicate login was started while busy")
                            await window.finish(task)
                            require(backend.property("accountLoginStatus")[provider], "The real server did not authenticate imported cookies")
                            require(not backend.loginInProgress, "Login did not return to idle")
                            return {"server_authenticated": True, "busy_and_duplicate_guard_verified": True}

                        if not await check(f"{layout}.{provider}.browser-login", cookie_login):
                            continue
                        if not backend.property("accountLoginStatus")[provider]:
                            continue
                        for collection in COLLECTION_BUTTONS[layout][provider]:
                            async def collection_check(name=collection):
                                nonlocal xh_playlist
                                if name == "playlist" and not xh_playlist:
                                    xh_playlist = await discover_playlist(clients.xh_client, "xhamster")
                                require(name != "playlist" or bool(xh_playlist), "No populated XHamster account playlist fixture was found")
                                return await test_account_collection(window, provider, name, playlist_url=xh_playlist or "", items=args.items)
                            await check(f"{layout}.{provider}.{collection}", collection_check)

                        if provider == "XVideos":
                            async def token_login():
                                jar = await asyncio.to_thread(original_reader, "xvideos", browser_name=args.browser)
                                tokens = {c.name: c.value for c in jar if c.name in {"session_token", "session_token_auth"} and c.value}
                                require(len(tokens) == 2, "The selected browser has no complete XVideos token fixture")
                                client = clients.xv_client
                                client.account = None
                                backend.accountStateChanged.emit()
                                placeholders = ("session_token", "session_token_auth")
                                for placeholder in placeholders:
                                    field = "Enter " + placeholder if layout == "desktop" else placeholder
                                    window.field(field, tokens[placeholder])
                                text = "Login with Session Tokens" if layout == "desktop" else "Sign in"
                                window.click(text)
                                await window.finish(backend._login_task)
                                for placeholder in placeholders:
                                    window.field("Enter " + placeholder if layout == "desktop" else placeholder, "")
                                require(backend.property("accountLoginStatus")[provider], "Two-token login did not confirm an authenticated server session")
                                return {"server_authenticated": True, "browser_session_not_reused": True}
                            if await check(f"{layout}.{provider}.manual-tokens", token_login):
                                await check(f"{layout}.{provider}.token-liked", partial(
                                    test_account_collection, window, provider, "liked", items=args.items))

                    async def error_recovery():
                        window.clear_rows()
                        errors = QSignalSpy(backend.showMessage)
                        backend.fetch_account_videos("XHamster", "playlist", "https://example.invalid/not-a-playlist")
                        await window.finish(backend._account_fetch_task)
                        require(errors.count() == 1 and not backend.busy and not backend.accountFetchInProgress,
                                "Invalid playlist did not emit an error and restore idle controls")
                        require(backend._downloads_model.rowCount() == 0, "Invalid playlist unexpectedly inserted rows")
                        backend.login_account("Unsupported", "", "", True)
                        await window.finish(backend._login_task)
                        require(errors.count() == 2 and not backend.loginInProgress, "Unsupported login did not restore idle controls")
                        return {"errors_verified": 2, "no_network_failure_simulation": True}
                    await check(f"{layout}.validation-errors", error_recovery)
                    if args.xvideos_playlist and layout == args.layouts[-1]:
                        async def playlist_rows():
                            window.clear_rows()
                            errors = QSignalSpy(backend.showMessage)
                            backend.process_playlist_url(args.xvideos_playlist, "", {})
                            await window.finish(backend._video_fetch_task)
                            require(errors.count() == 0, "The XVideos playlist pipeline reported an error")
                            return window.verify_rows(limit=args.items)
                        playlist_ok = await check("XVideos.playlist-listview", playlist_rows)
                        if args.xvideos_private:
                            async def private_authorization():
                                from contextlib import aclosing

                                from base_api import is_resource_gone
                                from base_api.modules.errors import AccessDeniedError

                                from src.cli.providers import ClientPool
                                from src.cli.settings import CliSettings
                                from src.shared.provider_routing import unwrap_scrape_result

                                require(playlist_ok, "Authenticated private-playlist loading did not pass")
                                try:
                                    async with ClientPool(CliSettings(timeout=20, request_attempts=1).to_runtime_config()) as clean:
                                        stream = clean.client("xvideos").get_playlist(args.xvideos_playlist, pages=1)
                                        with access_guard.private_denial_probe():
                                            async with aclosing(stream):
                                                async for result in stream:
                                                    unwrap_scrape_result(result)
                                                    raise AssertionError("Declared-private playlist exposes videos to an anonymous client")
                                except Exception as error:
                                    current = error
                                    while current is not None:
                                        if isinstance(current, AccessDeniedError) or is_resource_gone(current):
                                            break
                                        current = current.__cause__
                                    if current is None:
                                        raise
                                report["private_playlist"]["verified"] = True
                                return {"authenticated_rows_verified": True, "anonymous_video_access_denied": True}
                            await check("XVideos.private-playlist-authorization", private_authorization)
                    report["list_roles"] = 9
                finally:
                    window.close()
    except asyncio.CancelledError:
        if access_guard.blocked is not None:
            print(f"Stopped at access control. Partial report: {args.report}", flush=True)
            return 1
        return 130
    finally:
        for task in tuple(backend._background_tasks):
            task.cancel()
        await asyncio.gather(*tuple(backend._background_tasks), return_exceptions=True)
        await clients.close_all_clients()
        application.stop_flag.clear()
        del tester
    counts = report["counts"]
    print(f"{counts['PASS']} passed, {counts['FAIL']} failed. Report: {args.report}")
    return int(bool(counts["FAIL"] or counts["UNVERIFIED"] or report["action_coverage"]["not_passed"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", default="brave", choices=("brave", "chrome", "firefox", "edge", "vivaldi", "opera", "librewolf"))
    parser.add_argument("--layout", choices=("desktop", "mobile", "all"), default="all")
    parser.add_argument("--provider", choices=("pornhub", "xhamster", "xvideos"), action="append")
    parser.add_argument("--xhamster-playlist", default="")
    parser.add_argument("--xvideos-playlist", default="", help="Optional XVideos playlist fixture for the GUI list pipeline")
    parser.add_argument("--xvideos-private", action="store_true", help="Also require anonymous access to this declared-private playlist to be denied")
    parser.add_argument("--items", choices=(1, 2, 3), type=int, default=2)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--request-delay", type=float, default=0, help="Minimum spacing between requests before any 429")
    parser.add_argument("--rate-cooldown", type=float, default=30, help="Minimum 429 cooldown in seconds (at least 30)")
    parser.add_argument("--recovery-delay", type=float, default=5, help="Spacing after a 429, for the rest of the run (at least 5 seconds)")
    parser.add_argument("--rate-retries", type=int, default=2, help="Maximum 429 retries per safe read request; 0 stops immediately")
    parser.add_argument("--live-only", action="store_true", help="Skip deterministic control/error contracts for a focused live diagnostic")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-account-gui.json")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.request_delay < 0 or args.rate_cooldown < 30 or args.recovery_delay < 5 or args.rate_retries < 0:
        parser.error("Request delay must be nonnegative, cooldown at least 30s, recovery delay at least 5s, and retries nonnegative")
    if args.xvideos_private and not args.xvideos_playlist:
        parser.error("--xvideos-private requires --xvideos-playlist")
    if args.xvideos_playlist:
        from src.shared.provider_routing import ContentKind, route_url
        try:
            route = route_url(args.xvideos_playlist)
            valid = route.provider == "xvideos" and route.kind == ContentKind.COLLECTION and args.xvideos_playlist.startswith("https://")
        except ValueError:
            valid = False
        if not valid:
            parser.error("--xvideos-playlist requires an HTTPS XVideos playlist URL")
    args.layouts = ("desktop", "mobile") if args.layout == "all" else (args.layout,)
    args.providers = [{"pornhub": "PornHub", "xhamster": "XHamster", "xvideos": "XVideos"}[p]
                      for p in dict.fromkeys(args.provider or ("pornhub", "xhamster", "xvideos"))]
    if args.xvideos_playlist and "XVideos" not in args.providers:
        parser.error("The XVideos playlist fixture requires --provider xvideos or the default all-provider run")
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(prefix="porn-fetch-account-gui-config-") as configuration:
        os.environ["XDG_CONFIG_HOME"] = configuration
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtQuickControls2 import QQuickStyle

        QQuickStyle.setStyle("Material")
        app = QGuiApplication.instance() or QGuiApplication([])
        args.contracts = {"run": False}
        if not args.live_only:
            suite = unittest.defaultTestLoader.loadTestsFromName("src.tests.integration.test_account_page")
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            args.contracts = {"run": True, "tests": result.testsRun,
                              "failed": len(result.failures), "errors": len(result.errors)}
            if not result.wasSuccessful():
                print("Account control/error contracts failed; live checks were not started.")
                return 1
        try:
            status = asyncio.run(run(args))
        except KeyboardInterrupt:
            status = 130
        app.processEvents()
        return status


if __name__ == "__main__":
    raise SystemExit(main())
