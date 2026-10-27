"""Opt-in desktop Downloads QML workflows with real HLS and RAW media.

Run: uv run python -m src.tests.smoke.download_gui
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import re
import shutil
import tempfile
import time
import traceback
from contextlib import AsyncExitStack, ExitStack, contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

from src.cli.downloads import RAW_VIDEO_MODULES
from src.shared.media import VideoObject
from src.shared.provider_routing import PROVIDER_MODULES
from src.tests.smoke.download_lifecycle import lifecycle_fixtures, media_requests, require, validate_media

SCENARIOS = ("pause-resume", "cleanup", "remove")
MANUAL_PROVIDERS = {"spankbang": "Website/CDN playback issues; verify manually when playback works again"}


def make_report(args, workspace=None):
    import base_api

    packages = ["PySide6", "eaf-base-api"] + [f"unofficial-api-for-{provider}" for provider, _, _ in args.fixtures]
    return {"scope": "Real desktop DownloadsPage controls, provider clients and media files",
            "started_at_utc": datetime.now(timezone.utc).isoformat(),
            "workspace": str(workspace) if workspace is not None else None,
            "planned_cases": len(args.fixtures) * len(args.scenarios), "results": [], "interrupted": False,
            "manual_checks": args.manual_checks, "manual": len(args.manual_checks),
            "artifacts_retained": args.keep_artifacts,
            "base_api_source": str(Path(base_api.__file__).resolve()),
            "libraries": {name: version(name) for name in packages}}


def save_report(report, path):
    report["passed"] = sum(r.get("passed", False) for r in report["results"])
    report["failed"] = sum(not r.get("passed", False) and not r.get("interrupted", False)
                           and not r.get("blocked", False) for r in report["results"])
    report["blocked"] = sum(r.get("blocked", False) for r in report["results"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")


@contextmanager
def isolated_settings(directory):
    """Override runtime settings without saving anything to the user's profile."""
    from src.backend import application, clients, download_manager, video_processor

    class Overlay:
        def __init__(self, source):
            self.source = source

        def __getattr__(self, name):
            overrides = {"output_path": str(directory), "result_limit": 1, "processing_delay": 0,
                         "download_workers": 1, "retries": 2, "timeout": 25, "enable_logging": False,
                         "write_metadata": False, "skip_existing_files": True}
            return overrides[name] if name in overrides else getattr(self.source, name)

    with ExitStack() as stack:
        for module in (application, clients, download_manager, video_processor):
            stack.enter_context(patch.object(module, "app_settings", Overlay(module.app_settings)))
        stack.enter_context(patch.object(application, "TEMP_DIRECTORY_STATES", directory / "states"))
        stack.enter_context(patch.object(application, "TEMP_DIRECTORY_SEGMENTS", directory / "segments"))
        yield


class DownloadWindow:
    """Render the production page and send actual mouse/keyboard events to it."""

    def __init__(self, timeout, *, parallel=1, application_close=False):
        from PySide6.QtCore import QUrl
        from PySide6.QtQml import QQmlApplicationEngine

        from src.backend.account_diagnostics import UI, make_account_backend
        from src.backend.config import app_settings
        from src.frontend.UI import resources

        resources.qInitResources()
        self.backend = make_account_backend()
        self.backend.logger = logging.getLogger("desktop-download-test")
        self.backend._download_semaphore = asyncio.Semaphore(parallel)
        self.timeout = timeout
        self.active_timeout = None
        self.check_access = lambda: None
        self.closed = False
        self.warnings = []
        self.errors = []
        self.backend.showMessage.connect(self.errors.append)
        self.engine = QQmlApplicationEngine()
        self.engine.warnings.connect(lambda errors: self.warnings.extend(str(error) for error in errors))
        self.engine.rootContext().setContextProperty("backend", self.backend)
        self.engine.rootContext().setContextProperty("appSettings", app_settings)
        self.engine.rootContext().setContextProperty("applicationClose", application_close)
        self.engine.loadData(b'''
import QtQuick
import QtQuick.Controls
ApplicationWindow {
    id: window
    visible: true; width: 1600; height: 1100
    property bool androidLayout: false
    property QtObject bridge: QtObject { property bool isPremium: false }
    ApplicationShutdown { targetWindow: window; backendController: backend; active: applicationClose }
    DownloadsPage { anchors.fill: parent }
}
''', QUrl.fromLocalFile(str(UI / "DownloadDiagnostic.qml")))
        require(bool(self.engine.rootObjects()), "Production DownloadsPage failed to load")
        self.window = self.engine.rootObjects()[0]
        self.pump()

    @staticmethod
    def pump():
        from PySide6.QtGui import QGuiApplication
        QGuiApplication.processEvents()

    def controls(self, name, job=None):
        from src.backend.account_diagnostics import visual_items
        root = self.window.contentItem()
        if job is not None:
            rows = [item for item in visual_items(root)
                    if item.objectName() == "downloadRow" and item.property("jobId") == job]
            if not rows:
                return []
            root = rows[0]
        return [item for item in visual_items(root)
                if item.objectName() == name and item.isVisible()]

    def control(self, name, job=None):
        found = self.controls(name, job)
        require(len(found) == 1, f"Expected one visible {name}, found {len(found)}")
        return found[0]

    def click(self, name, job=None):
        from PySide6.QtCore import QPointF, Qt
        from PySide6.QtTest import QTest
        item = self.control(name, job)
        require(item.isEnabled(), f"Control {name} is disabled")
        point = item.mapToScene(QPointF(item.width() / 2, item.height() / 2)).toPoint()
        require(0 <= point.x() < self.window.width() and 0 <= point.y() < self.window.height(),
                f"Control {name} is outside the window")
        QTest.mouseClick(self.window, Qt.MouseButton.LeftButton, pos=point)

    async def wait(self, predicate, message):
        self.active_timeout = asyncio.timeout(self.timeout)
        try:
            async with self.active_timeout:
                while True:
                    self.pump()
                    self.check_access()
                    require(not self.warnings, f"Production QML warnings: {self.warnings[:2]}")
                    require(not self.errors, f"GUI reported an error: {self.errors[:1]}")
                    if predicate():
                        return
                    await asyncio.sleep(.01)
        except TimeoutError as error:
            raise AssertionError(message) from error
        finally:
            self.active_timeout = None

    async def load(self, url, quality, *, append=False, filename=None) -> tuple[str, VideoObject]:
        from PySide6.QtCore import QMetaObject, Qt
        from PySide6.QtTest import QTest
        model = self.backend._downloads_model
        before = model.rowCount()
        require(append or before == 0, "A previous workflow left rows in the list")
        if filename is not None:
            self.click("downloadAdvancedButton")
            self.pump()
            self.control("downloadTitlePattern").setProperty("text", filename)
            self.click("downloadListButton")
            self.pump()
        self.control("videoUrlInput").setProperty("text", url)
        self.pump()
        self.click("getVideoButton")
        task = self.backend._video_fetch_task
        assert task is not None, "Get Video did not start the real preparation task"
        await self.wait(lambda: task.done(), "Video preparation timed out")
        await task
        await asyncio.sleep(0)
        await self.wait(lambda: model.rowCount() == before + 1, "Prepared video never reached the GUI")
        await self.wait(lambda: self.control("downloadList").property("count") == before + 1,
                        "The ListView did not receive the prepared row")
        job = model.data(model.index(before, 0), model.JobIdRole)
        assert isinstance(job, str) and job, "Prepared row has no job identity"
        QMetaObject.invokeMethod(self.control("downloadList"), "forceLayout", Qt.ConnectionType.DirectConnection)
        await self.wait(lambda: bool(self.controls("downloadRow", job)), "The ListView did not render its delegate")
        video = model.get_video(job)
        assert video is not None and video.source_video is not None, "Row lost its real provider video"
        assert video.output_path is not None, "Prepared row has no output path"
        labels = [item.property("text") for item in self.visual_row(job)]
        require(f"{before + 1}) {video.title}" in labels and video.author in labels,
                "Rendered metadata differs from the video")
        allowed = sorted(q for q in video.qualities if q <= 720)
        require(bool(allowed), "No verified free quality at or below 720p")
        selected = min(allowed) if quality is None else quality
        require(selected in allowed, f"Requested {selected}p is unavailable: {allowed}")
        combo = self.control("downloadQualityCombo", job)
        index = [str(q) for q in video.qualities].index(str(selected))
        # Open the real popup and select its item using keyboard navigation.
        self.click("downloadQualityCombo", job)
        self.pump()
        QTest.keyClick(self.window, Qt.Key.Key_Home)
        for _ in range(index):
            QTest.keyClick(self.window, Qt.Key.Key_Down)
        QTest.keyClick(self.window, Qt.Key.Key_Return)
        self.pump()
        # Material popups animate closed. Let the real popup release its
        # overlay/focus before another row or navigation button is clicked.
        QTest.qWait(180)
        self.pump()
        require(str(video.selected_quality) == str(selected)
                and str(combo.property("currentText")) == str(selected),
                f"Quality control did not update row {before + 1}: expected {selected}, "
                f"model {video.selected_quality}, displayed {combo.property('currentText')}")
        require(model.get_status(job) == "pending" and not video.output_path.exists(),
                "Preparing a row unexpectedly created media")
        return job, video

    def visual_row(self, job=None):
        from src.backend.account_diagnostics import visual_items
        return list(visual_items(self.control("downloadRow", job)))

    def set_cleanup(self, enabled):
        self.click("downloadAdvancedButton")
        self.pump()
        checkbox = self.control("cleanupStopCheck")
        if bool(checkbox.property("checked")) != enabled:
            self.click("cleanupStopCheck")
        require(bool(checkbox.property("checked")) == enabled, "Cleanup toggle did not change")
        self.click("downloadListButton")
        self.pump()

    async def shutdown(self):
        from PySide6.QtCore import QCoreApplication, QEvent
        if self.closed:
            return
        self.closed = True
        # Stop the real writers before closing their cores or deleting test files.
        for event in self.backend._download_stop_events.values():
            event.set()
        tasks = tuple(self.backend._background_tasks)
        if tasks:
            try:
                await asyncio.wait_for(asyncio.shield(asyncio.gather(*tasks, return_exceptions=True)), 15)
            except TimeoutError:
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
        self.window.close()
        self.window.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        self.engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)


def artifacts(directory, video, job):
    target = video.output_path
    raw = Path(f"{target}.raw-state.json")
    state = directory / "states" / job
    segments = directory / "segments" / job
    paths = (target, Path(f"{target}.tmp"), raw, Path(f"{raw}.tmp"), state, Path(f"{state}.tmp"))
    return [path for path in paths if path.exists()] + ([p for p in segments.rglob("*") if p.is_file()]
                                                        if segments.exists() else [])


async def check_case(args, provider, transport, url, scenario, directory, ffmpeg, result):
    from base_api.modules.static_functions import segment_file_path
    from PySide6.QtTest import QSignalSpy

    from src.backend import application, clients
    from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait
    from src.cli.providers import ClientPool
    from src.cli.settings import CliSettings
    from src.tests.smoke.download_lifecycle import ObservedCore

    runtime = CliSettings(download_workers=1, request_attempts=2, timeout=25,
                          response_cache_mb=0, segment_cache_mb=0).to_runtime_config()
    runtime.ffmpeg_path = str(ffmpeg)
    with isolated_settings(directory):
        gui = DownloadWindow(args.timeout)
        guard = AccountAccessGuard(on_wait=lambda seconds: extend_timeout_for_wait(gui.active_timeout, seconds))
        gui.check_access = guard.raise_if_blocked
        try:
            async with AsyncExitStack() as lifecycle:
                pool = await lifecycle.enter_async_context(ClientPool(runtime, core_factory=ObservedCore))
                lifecycle.push_async_callback(gui.shutdown)
                core = pool.client(provider).core
                result["requests"] = core.requests
                original_report = application.report_exception

                async def observed_error(error, **options):
                    result.setdefault("backend_errors", []).append(type(error).__name__)
                    traceback.print_exception(error)
                    return await original_report(error, **options)
                # Only inject real isolated native clients. GUI URL routing,
                # preparation, downloads, callbacks and controls stay unchanged.
                with (patch.object(clients, "client_for", pool.client),
                      patch.object(application, "report_exception", observed_error), guard):
                    result["stage"] = "prepare"
                    job, video = await gui.load(url, args.quality)
                    result["quality"] = video.selected_quality
                    actual_transport = ("raw" if PROVIDER_MODULES[provider] in RAW_VIDEO_MODULES
                                        or getattr(video.source_video, "is_hls", None) is False else "hls")
                    result.update(expected_transport=transport, transport=actual_transport)
                    require(transport == "auto" or actual_transport == transport,
                            f"Expected {transport.upper()}, provider selected {actual_transport.upper()}")
                    transport = actual_transport
                    if transport == "hls":
                        require(bool(getattr(video.source_video, "m3u8_base_url", None)),
                                "Provider exposed no HLS master playlist")
                    if scenario == "remove":
                        gui.click("downloadRemoveButton")
                        await gui.wait(lambda: gui.backend._downloads_model.rowCount() == 0,
                                       "Removing a pending row failed")
                        require(gui.backend.download_manager.get_video(job) is None, "Manager retained a removed row")
                        result["pending_removal_verified"] = True
                        job, video = await gui.load(url, args.quality)
                    target = video.output_path
                    assert target is not None, "Prepared row has no output path"
                    backend, model = gui.backend, gui.backend._downloads_model
                    progress = []
                    statuses = []
                    stopped = False
                    removed = QSignalSpy(model.rowsRemoved)

                    def observe_progress():
                        nonlocal stopped
                        if model.get_video(job) is None:
                            return
                        status = model.get_status(job)
                        statuses.append(status)
                        percentage = int(model.data(model.index(0, 0), model.ProgressRole) or 0)
                        progress.append(percentage)
                        if core.phase == "interrupt" and not stopped and status == "downloading" and 1 <= percentage < 95:
                            # Stop from a real progress notification, so fast downloads
                            # cannot finish between a polling interval and the click.
                            stopped = True
                            result["interrupted_at_percent"] = percentage
                            row = gui.control("downloadRow")
                            require(row.property("progress") == percentage, "Rendered row lost live progress")
                            require(int(gui.control("downloadProgressBar").property("value")) == percentage,
                                    "Visible progress bar differs from the model")
                            gui.click("downloadRemoveButton" if scenario == "remove" else "downloadStopResumeButton")

                    def changed(*_):
                        # Qt signal handlers cannot propagate exceptions back
                        # into the async runner. Preserve them as test failures.
                        try:
                            observe_progress()
                        except Exception as error:
                            gui.errors.append(str(error))
                            for event in backend._download_stop_events.values():
                                event.set()

                    model.dataChanged.connect(changed)
                    try:
                        cleanup = scenario != "pause-resume"
                        gui.set_cleanup(cleanup)
                        core.phase = "interrupt"
                        result["stage"] = "interrupt"
                        if scenario == "pause-resume":
                            gui.click("downloadSelectCheck")
                            require(model.selected_job_ids() == [job], "Selection checkbox did not select this job")
                            gui.click("downloadSelectedButton")
                        else:
                            gui.click("downloadStartButton")
                        await gui.wait(lambda: job not in backend._download_tasks, "Stop did not finish cooperatively")
                        # The real backend appends .mp4 when the title pattern
                        # has no suffix; inspect its final canonical path.
                        target = video.output_path
                        assert target is not None, "Download lost its output path"
                        require(stopped, "Download finished/failed before a meaningful GUI interruption")
                        require(video.status == "cancelled", f"Interrupted video ended as {video.status}")
                        require("downloading" in statuses and "stopping" in statuses and max(progress) > 0,
                                "GUI did not expose download/progress/stopping transitions")
                        result["live_progress_verified"] = True
                        result["stop_control_verified"] = True
                        if scenario == "remove":
                            await gui.wait(lambda: model.rowCount() == 0, "Active row was not removed after stopping")
                            require(backend.download_manager.get_video(job) is None, "Active entry remained in manager")
                            require(not artifacts(directory, video, job), "Active removal with cleanup left partial files")
                            result.update(active_removal_verified=True, cleanup_verified=True, stage="completed")
                            return
                        require(model.rowCount() == 1 and model.get_status(job) == "cancelled",
                                "Stopped download disappeared instead of offering Resume")
                        gui.pump()
                        require(gui.control("downloadStopResumeButton").isEnabled()
                                and gui.control("downloadStopResumeButton").property("text") == "▶",
                                "Stopped row did not offer its Resume control")
                        retained = set()
                        checkpoint_bytes = 0
                        if cleanup:
                            require(not artifacts(directory, video, job), "Cleanup left media, segments or checkpoints")
                            result["cleanup_verified"] = True
                        elif transport == "hls":
                            state = directory / "states" / job
                            require(state.is_file(), "Pause retained no HLS checkpoint")
                            payload = json.loads(state.read_text())
                            segment_dir = directory / "segments" / job
                            retained = {url for i, url in enumerate(payload["segments"])
                                        if (p := Path(segment_file_path(segment_dir, i, payload["segment_index_width"]))).is_file()
                                        and p.stat().st_size > 0}
                            require(0 < len(retained) < len(payload["segments"]), "No partial HLS segment set retained")
                            result["retained_segments"] = len(retained)
                        else:
                            raw = Path(f"{target}.raw-state.json")
                            require(target.is_file() and raw.is_file(), "Pause retained no RAW output/checkpoint")
                            payload = json.loads(raw.read_text())
                            checkpoint_bytes = sum(payload["progress"])
                            require(0 < checkpoint_bytes < payload["size"], "RAW checkpoint has no partial progress")
                            with target.open("rb") as file:
                                prefix = file.read(min(65536, checkpoint_bytes))
                            prefix_hash = hashlib.sha256(prefix).hexdigest()
                            result["retained_bytes"] = checkpoint_bytes
                        core.phase = "restart" if cleanup else "resume"
                        result["stage"] = core.phase
                        gui.click("downloadStopResumeButton")
                        require(job in backend._download_tasks, "Resume control did not start a task")
                        await gui.wait(lambda: job not in backend._download_tasks, "Resumed download timed out")
                        require(video.status == "completed", f"Resume/restart ended as {video.status}")
                        require(model.rowCount() == 0 and backend.download_manager.get_video(job) is None
                                and removed.count() == 1, "Completed download did not automatically clear both lists")
                        await gui.wait(lambda: gui.control("downloadList").property("count") == 0,
                                       "Completed delegate remained visible")
                        result["automatic_removal_verified"] = True
                        if transport == "hls":
                            fetched = {u for phase, u in core.segment_requests if phase == core.phase}
                            require(bool(fetched), "Resume/restart made no real segment requests")
                            if cleanup:
                                plans = [p["segments"] for p in core.segment_plans if p["phase"] == "restart"]
                                require(bool(plans) and set(plans[-1]) <= fetched, "Restart did not fetch every fresh segment")
                            else:
                                require(not retained.intersection(fetched), "Resume re-fetched retained HLS segments")
                        else:
                            requests = media_requests(core, core.phase)
                            require(bool(requests), "Resume/restart consumed no RAW media")
                            for request_index, entry in enumerate(requests):
                                requested = re.fullmatch(r"bytes=(\d+)-(\d*)", entry["range"] or "bytes=0-")
                                assert requested is not None, "RAW request had an invalid Range"
                                if cleanup:
                                    # Native multipart RAW downloads may request
                                    # later chunks separately, even with one worker.
                                    require(request_index > 0 or int(requested[1]) == 0,
                                            "Clean restart did not begin at byte zero")
                                else:
                                    served = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", entry.get("content_range") or "")
                                    require(int(requested[1]) >= checkpoint_bytes and entry["status"] == 206
                                            and served is not None and int(served[1]) == int(requested[1])
                                            and int(served[3]) == payload["size"], "RAW resume did not reuse retained bytes")
                            if not cleanup:
                                require(target.stat().st_size == payload["size"], "RAW output length differs from server total")
                                with target.open("rb") as file:
                                    require(hashlib.sha256(file.read(len(prefix))).hexdigest() == prefix_hash,
                                            "RAW resume changed the retained prefix")
                        result["fresh_download_verified" if cleanup else "reuse_verified"] = True
                        result["stage"] = "validate"
                        result["media"] = await validate_media(target, ffmpeg, video.length)
                        require(artifacts(directory, video, job) == [target], "Completion left resume artifacts")
                        result["stage"] = "completed"
                    finally:
                        model.dataChanged.disconnect(changed)
                        result["status_transitions"] = [status for i, status in enumerate(statuses)
                                                        if i == 0 or status != statuses[i - 1]]
                        result["progress_observations"] = len(progress)
                        result["maximum_progress_percent"] = max(progress, default=0)
        finally:
            # Also covers preparation failures before progress observers exist.
            await gui.shutdown()
            result["access_control"] = guard.blocked
            result["rate_limit_recovery"] = guard.rate_limit_events


async def run(args, workspace, ffmpeg):
    from src.backend import clients

    report = make_report(args, workspace)

    def save():
        save_report(report, args.report)

    save()
    try:
        with args.report.with_suffix(".log").open("w") as log:
            for provider, transport, url in args.fixtures:
                for scenario in args.scenarios:
                    number = len(report["results"]) + 1
                    print(f"[{number}/{report['planned_cases']}] RUN {provider} desktop {scenario}", flush=True)
                    directory = workspace / provider / scenario
                    directory.mkdir(parents=True)
                    result = {"provider": provider, "transport": transport, "scenario": scenario, "passed": False}
                    started = time.monotonic()
                    with redirect_stdout(log), redirect_stderr(log):
                        try:
                            await check_case(args, provider, transport, url, scenario, directory, ffmpeg, result)
                            result["passed"] = True
                        except asyncio.CancelledError:
                            if result.get("access_control"):
                                result["blocked"] = True
                            else:
                                result["interrupted"] = True
                                report["interrupted"] = True
                        except Exception as error:
                            result.update(error_type=type(error).__name__, error=str(error))
                            traceback.print_exc(file=log)
                    result["elapsed_seconds"] = round(time.monotonic() - started, 2)
                    report["results"].append(result)
                    save()
                    print(f"[{number}/{report['planned_cases']}] "
                          f"{'STOP' if result.get('interrupted') else 'BLOCKED' if result.get('blocked') else 'PASS' if result['passed'] else 'FAIL'} "
                          f"{provider} {scenario} [{result.get('stage', 'prepare')}] {result.get('error', '')}", flush=True)
                    if not args.keep_artifacts:
                        shutil.rmtree(directory)
                    if report["interrupted"] or result.get("access_control"):
                        print(f"Stopped. Partial report: {args.report}", flush=True)
                        return 130 if report["interrupted"] and not result.get("access_control") else 1
    finally:
        await clients.close_all_clients()
    print(f"{report['passed']} passed, {report['failed']} failed, {report['manual']} manual. Report: {args.report}", flush=True)
    return int(report["failed"] != 0)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("all", *PROVIDER_MODULES), action="append",
                        help="Repeat to select providers; default all. SpankBang remains manual")
    parser.add_argument("--scenario", choices=("all", *SCENARIOS), default="all")
    parser.add_argument("--quality", type=int, help="Exact resolution, at most 720p; default lowest available")
    parser.add_argument("--timeout", type=float, default=600, help="Maximum seconds per preparation/download phase")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-download-gui.json")
    parser.add_argument("--artifacts-dir", type=Path)
    parser.add_argument("--keep-artifacts", action="store_true")
    parser.add_argument("--list", action="store_true", help="Show selected cases without requests or Qt startup")
    args = parser.parse_args(argv)
    if args.timeout <= 0 or (args.quality is not None and not 0 < args.quality <= 720):
        parser.error("Timeout must be positive and quality must be between 1 and 720")
    selected = set(args.provider or ("all",))
    fixtures = [f for f in lifecycle_fixtures() if "all" in selected or f[0] in selected]
    args.fixtures = [f for f in fixtures if f[0] not in MANUAL_PROVIDERS]
    args.scenarios = SCENARIOS if args.scenario == "all" else (args.scenario,)
    args.manual_checks = [{"provider": provider, "scenario": scenario, "status": "MANUAL",
                           "reason": MANUAL_PROVIDERS[provider]}
                          for provider, _, _ in fixtures if provider in MANUAL_PROVIDERS
                          for scenario in args.scenarios]
    return args


def main():
    args = parse_args()
    if args.list:
        for provider, transport, _ in args.fixtures:
            for scenario in args.scenarios:
                print(f"{provider} {transport.upper()} desktop {scenario}")
        for check in args.manual_checks:
            print(f"MANUAL {check['provider']} desktop {check['scenario']}: {check['reason']}")
        print(f"{len(args.fixtures) * len(args.scenarios)} automated, {len(args.manual_checks)} manual workflows. No network requests.")
        return 0
    for provider in dict.fromkeys(check["provider"] for check in args.manual_checks):
        print(f"MANUAL {provider}: {MANUAL_PROVIDERS[provider]}; no automated requests", flush=True)
    if not args.fixtures:
        save_report(make_report(args), args.report)
        print(f"0 automated workflows; {len(args.manual_checks)} manual, unverified. Report: {args.report}")
        return 0
    from src.shared.ffmpeg import find_ffmpeg
    ffmpeg = find_ffmpeg()
    if ffmpeg is None:
        raise SystemExit("FFmpeg is required to validate real completed videos")
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    if args.artifacts_dir:
        args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="porn-fetch-download-gui-", dir=args.artifacts_dir))
    print(f"Live desktop downloads: {len(args.fixtures) * len(args.scenarios)} cases. Workspace: {workspace}", flush=True)
    try:
        with tempfile.TemporaryDirectory(prefix="porn-fetch-download-gui-config-") as configuration:
            os.environ["XDG_CONFIG_HOME"] = configuration
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            status = asyncio.run(run(args, workspace, ffmpeg))
            app.processEvents()
            return status
    except KeyboardInterrupt:
        print(f"Stopped. Partial report: {args.report}", flush=True)
        return 130
    finally:
        if not args.keep_artifacts:
            shutil.rmtree(workspace)


if __name__ == "__main__":
    raise SystemExit(main())
