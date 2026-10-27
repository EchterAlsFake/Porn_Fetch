"""Opt-in desktop statistics/history with real HLS, RAW and PocketBase."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import os
import shutil
import tempfile
import time
import traceback
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from src.tests.smoke.download_lifecycle import lifecycle_fixtures, require, validate_media

if TYPE_CHECKING:
    from src.database.bridge import DatabaseBridge
    from src.database.client import PocketBaseClient

CHECKS = (
    "tracking-disabled", "empty-dashboard", "pending-history", "hls-stop-resume",
    "raw-failure-retry", "source-history", "privacy", "refresh-from-disk",
    "history-after-restart", "disabled-preserves-history", "database-startup-failure",
)


class Dashboard:
    def __init__(self, bridge, settings):
        from PySide6.QtCore import QObject, QUrl
        from PySide6.QtQml import QQmlApplicationEngine

        from src.backend.account_diagnostics import UI
        self.engine = QQmlApplicationEngine()
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(str(error) for error in errors))
        self.engine.rootContext().setContextProperty("databaseBridge", bridge)
        self.engine.rootContext().setContextProperty("appSettings", settings)
        self.engine.loadData(b'''
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
ApplicationWindow {
    visible: true; width: 1250; height: 1100
    Material.theme: appSettings.dark_mode ? Material.Dark : Material.Light
    StatisticsPage { anchors.fill: parent }
}
''', QUrl.fromLocalFile(str(UI / "StatisticsDiagnostic.qml")))
        require(bool(self.engine.rootObjects()), "Production StatisticsPage did not load")
        self.window = self.engine.rootObjects()[0]
        self.page = self.window.findChild(QObject, "statisticsPage")
        assert self.page is not None, "Statistics page disappeared"

    def control(self, name):
        from src.backend.account_diagnostics import visual_items
        items = [item for item in visual_items(self.window.contentItem()) if item.objectName() == name]
        require(len(items) == 1, f"Expected one {name}, got {len(items)}")
        return items[0]

    def statistics(self):
        assert self.page is not None
        value = self.page.property("statistics")
        return value.toVariant() if hasattr(value, "toVariant") else value

    def close(self):
        from PySide6.QtCore import QCoreApplication, QEvent
        self.window.close()
        self.window.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        self.engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)


class HistoryChecks:
    def __init__(self, args, directory, settings, gui):
        self.args, self.directory, self.settings, self.gui = args, directory, settings, gui
        self._bridge: DatabaseBridge | None = None
        self._dashboard: Dashboard | None = None
        self.videos = {}
        self.saved = []
        self.ids = {}
        self.fixtures = {provider: url for provider, _, url in lifecycle_fixtures()}

    @property
    def bridge(self) -> DatabaseBridge:
        assert self._bridge is not None, "No database bridge is attached"
        return self._bridge

    @property
    def dashboard(self) -> Dashboard:
        assert self._dashboard is not None, "No dashboard is attached"
        return self._dashboard

    @property
    def client(self) -> PocketBaseClient:
        client = self.bridge.tracker._client
        assert client is not None, "No real database client is running"
        return client

    async def attach(self, enabled):
        from src.database.bridge import DatabaseBridge
        await self.detach()
        self.settings.track_videos = enabled
        self._bridge = DatabaseBridge(parent=self.gui.engine)
        self.gui.backend.bind_database_bridge(self.bridge)
        self.bridge.downloadSaved.connect(self.saved.append)
        self._dashboard = Dashboard(self.bridge, self.settings)
        self.bridge.start()
        await self.drain()

    async def detach(self):
        if self._dashboard is not None:
            self.dashboard.close()
            self._dashboard = None
        if self._bridge is not None:
            manager = self.gui.backend.download_manager
            manager.video_added.disconnect(self.bridge.on_video_updated)
            manager.video_updated.disconnect(self.bridge.on_video_updated)
            self.bridge.busyChanged.disconnect(self.gui.backend._update_activity)
            self.bridge.initializationFailed.disconnect(self.gui.backend.handle_message)
            await self.bridge.close()
            self.gui.backend.database_bridge = None
            self.bridge.deleteLater()
            self._bridge = None

    async def drain(self):
        await self.gui.wait(lambda: not self.bridge.busy, "History writes did not settle")
        await asyncio.sleep(0)
        self.gui.pump()
        require(not self.dashboard.warnings, f"Statistics QML warnings: {self.dashboard.warnings[:2]}")

    async def load(self, provider, name):
        self.gui.window.requestActivate()
        self.gui.pump()
        job, video = await self.gui.load(self.fixtures[provider], None,
                                         append=True, filename=name + ".mp4")
        self.videos[video.url] = video
        await self.drain()
        return job, video

    async def records(self):
        from src.database.constants import VIDEO_COLLECTION
        return await self.client.list_records(VIDEO_COLLECTION)

    async def verify(self):
        """Compare the REST history and rendered dashboard to actual workflow outcomes."""
        from src.backend.account_diagnostics import visual_items
        from src.database.constants import ORIGIN_COLLECTION
        await self.drain()
        records = await self.records()
        require(len(records) == len(self.videos), "Missing history or duplicate records for repeated attempts")
        origins = await self.client.list_records(ORIGIN_COLLECTION)
        origin_names = {row["id"]: row["name"] for row in origins}
        counts = {"successful": 0, "failed": 0, "other": 0}
        sources = {}
        for record in records:
            video = self.videos[record["url"]]
            for key, expected in {"title": video.title, "author": video.author, "video_id": video.video_id,
                                  "length": str(video.length) if video.length is not None else "", "status": video.status,
                                  "output_path": str(video.output_path), "identifier": video.identifier,
                                  "origin_iterator_url": video.origin_iterator_url or ""}.items():
                require(record[key] == expected,
                        f"Persisted {key} differs from the real video: {record[key]!r} != {expected!r}")
            require(record["tags"] == video.tags and record["qualities"] == video.qualities,
                    "Persisted media metadata differs from the provider")
            require(datetime.fromisoformat(record["downloaded_at"].replace("Z", "+00:00")), "Invalid history date")
            previous_id = self.ids.setdefault(video.url, record["id"])
            require(record["id"] == previous_id, "Retry changed the history identity instead of updating it")
            bucket = "successful" if video.status == "completed" else "failed" if video.status == "failed" else "other"
            counts[bucket] += 1
            source = origin_names.get(record.get("origin_iterator"), "Direct downloads")
            item = sources.setdefault(source, {"name": source, "total": 0, "successful": 0, "failed": 0, "other": 0})
            item["total"] += 1
            item[bucket] += 1
            if video.status == "completed":
                require(str(record["selected_quality"]) == str(video.selected_quality)
                        and record["is_hls"] == video.is_hls, "Final quality/transport did not persist")
                expected_size = round(video.output_path.stat().st_size / (1024 * 1024), 2)
                require(record["file_size_mb"] == expected_size, "History size differs from the real downloaded file")
        finished = counts["successful"] + counts["failed"]
        expected = {"enabled": True, "total": len(records), **counts,
                    "successRate": round(100 * counts["successful"] / finished) if finished else 0,
                    "totalSizeMb": round(sum(row["file_size_mb"] for row in records), 1),
                    "lastDownloaded": max((row["downloaded_at"] for row in records), default="")}
        stats = self.dashboard.statistics()
        require(all(stats[key] == value for key, value in expected.items()),
                f"Rendered statistics differ from history: expected {expected}, got {stats}")
        require({row["name"]: row for row in stats["sources"]} == sources, "Source grouping/counts are incorrect")
        require([row["total"] for row in stats["sources"]] == sorted((row["total"] for row in sources.values()), reverse=True),
                "Source activity is not sorted by count")
        for name, value in {"statisticsTotal": len(records), "statisticsSuccessful": counts["successful"],
                            "statisticsFailed": counts["failed"], "statisticsSuccessRate": str(expected["successRate"]) + "%"}.items():
            card = self.dashboard.control(name)
            require(str(card.property("value")) == str(value), f"{name} displays the wrong count")
            require(str(value) in [str(item.property("text")) for item in visual_items(card)],
                    f"{name} does not render its value")
        assert self.dashboard.page is not None
        require(self.dashboard.page.property("outcomeTotal") == len(records), "Outcome chart has stale totals")
        require(not self.dashboard.control("trackingDisabledNotice").isVisible(), "Enabled history shows disabled notice")
        require(self.dashboard.control("statisticsEmptySources").isVisible() == (not records), "Empty-source state is stale")
        require("nan" not in self.dashboard.control("statisticsFileSize").property("text").lower(), "Invalid displayed size")
        require(bool(self.dashboard.control("statisticsLastActivity").property("text")), "Last activity was not rendered")
        return expected

    async def disabled(self):
        await self.attach(False)
        require(self.dashboard.control("trackingDisabledNotice").isVisible(), "Disabled notice is hidden")
        require(self.dashboard.statistics()["total"] == 0 and self.bridge._service is None, "Disabled tracking started a database")
        if not self.args.offline_only:
            job, video = await self.load("pornhub", "untracked")
            self.gui.click("downloadRemoveButton", job)
            self.videos.clear()
            require(not self.saved, "Disabled tracking saved a real prepared video")
        require(not Path(self.settings.pocketbase_data_path).exists(), "Disabled tracking created a database folder")
        return {"disabled_notice": True, "no_database_or_saved_records": True,
                "real_preparation_checked": not self.args.offline_only}

    async def empty(self):
        await self.attach(True)
        expected = await self.verify()
        require(expected["total"] == 0 and self.bridge.tracker.is_running, "Fresh real database is not empty/running")
        return expected

    async def pending(self):
        self.hls_job, self.hls = await self.load("pornhub", "history-hls")
        require(self.hls.status.casefold() == "pending" and not self.hls.output_path.exists(),
                "Preparation unexpectedly downloaded media")
        stats = await self.verify()
        require(stats["other"] == 1 and stats["successRate"] == 0, "Pending row counted as a completed attempt")
        return stats

    async def hls_resume(self):
        self.gui.set_cleanup(False)
        model = self.gui.backend._downloads_model
        self.gui.click("downloadStartButton", self.hls_job)
        await self.gui.wait(lambda: 0 < model.data(model.index(0, 0), model.ProgressRole) < 95,
                            "No real HLS progress before completion")
        self.gui.click("downloadStopResumeButton", self.hls_job)
        await self.gui.wait(lambda: not self.gui.backend._download_tasks, "Stopping did not settle")
        require(self.hls.status == "cancelled", "The real transfer did not stop")
        stopped = await self.verify()
        require(stopped["other"] == 1 and stopped["failed"] == 0, "Stopped download counted as failed")
        self.gui.click("downloadStopResumeButton", self.hls_job)
        await self.gui.wait(lambda: not self.gui.backend._download_tasks, "HLS resume did not finish")
        require(self.hls.status == "completed" and self.hls.is_hls, "HLS resume did not complete")
        probe = await validate_media(self.hls.output_path, self.args.ffmpeg, self.hls.length)
        require(model.rowCount() == 0, "Completed row did not clear")
        stats = await self.verify()
        require(stats["total"] == stats["successful"] == 1, "Resume duplicated or lost history")
        return {"statistics": stats, "media": probe, "transport": "HLS", "provider": "pornhub"}

    async def fail(self, job, video):
        # A real filesystem failure, before native media writes; no fake provider result.
        original = video.output_path
        blocker = self.directory / (job + "-blocked-parent")
        blocker.write_bytes(b"owned path conflict")
        video.output_path = blocker / "failed.mp4"
        self.gui.click("downloadStartButton", job)
        await self.gui.wait(lambda: not self.gui.backend._download_tasks, "Failed download did not settle")
        require(video.status == "failed", "The real path conflict did not produce a failed download")
        stats = await self.verify()
        return original, stats

    async def raw_retry(self):
        job, video = await self.load("eporner", "history-raw")
        original, failed = await self.fail(job, video)
        require(failed["failed"] == 1 and failed["successRate"] == 50, "Failure statistics are incorrect")
        require([row["url"] for row in self.bridge.getFailedVideosForIterator("")] == [video.url],
                "Direct failed-history query missed the real failure")
        video.output_path = original
        self.gui.click("downloadStopResumeButton", job)
        await self.gui.wait(lambda: not self.gui.backend._download_tasks, "RAW retry did not finish")
        require(video.status == "completed" and not video.is_hls, "Real RAW retry did not complete")
        probe = await validate_media(video.output_path, self.args.ffmpeg, video.length)
        stats = await self.verify()
        require(stats["total"] == stats["successful"] == 2 and not stats["failed"], "Retry left a duplicate/stale failed record")
        require(not self.bridge.getFailedVideosForIterator(""), "Completed retry remains in failed history")
        return {"statistics": stats, "media": probe, "transport": "RAW", "provider": "eporner"}

    async def source(self):
        from src.backend.account_diagnostics import visual_items
        from src.cli.selftest.cases import PROFILE_TESTS
        model = self.gui.backend._downloads_model
        url = next(url for name, url in PROFILE_TESTS if name == "PornHub Model")
        field = next(item for item in visual_items(self.gui.window.contentItem())
                     if item.property("placeholderText") == "Enter a model or channel URL")
        field.setProperty("text", url)
        field.accepted.emit()
        task = self.gui.backend._video_fetch_task
        require(task is not None, "Model input did not start the real profile pipeline")
        await self.gui.wait(task.done, "Profile history preparation did not finish")
        await task
        require(model.rowCount() == 1, "Expected one bounded real profile row")
        job = model.data(model.index(0, 0), model.JobIdRole)
        video = model.get_video(job)
        require(video.origin_iterator_url == url and bool(video.origin_iterator_name), "Real profile source identity was lost")
        self.videos[video.url] = video
        await self.drain()
        await self.fail(job, video)
        origins = self.bridge.getAvailableIterators()
        require(len(origins) == 1 and origins[0]["url"] == url, "Source history did not save the real profile")
        failed = self.bridge.getFailedVideosForIterator(url)
        require(len(failed) == 1 and failed[0]["url"] == video.url and failed[0]["status"] == "failed",
                "Failed-history query did not retain the profile association")
        self.gui.click("downloadRemoveButton", job)
        require(model.rowCount() == 0, "Manual removal did not clear the pending list")
        stats = await self.verify()
        require(stats["total"] == 3 and stats["successRate"] == 67, "Removing a list row erased or changed stored history")
        return stats

    async def privacy(self):
        from src.backend.account_diagnostics import visual_items
        original = await self.records()
        for enabled in (True, False):
            self.settings.anonymous_mode = enabled
            self.gui.pump()
            names = [item.property("text") for item in visual_items(self.dashboard.window.contentItem())
                     if item.objectName() == "statisticsSourceName"]
            require(names and (all(name == "Hidden source" for name in names) if enabled else "Direct downloads" in names),
                    "Privacy setting did not change rendered source names")
            visible = [str(item.property("text")) for item in visual_items(self.dashboard.window.contentItem()) if item.isVisible()]
            require(not any("https://" in text for text in visible), "Statistics exposed a source URL")
        require(await self.records() == original, "Privacy masking modified persisted history")
        return {"rendered_source_masking": True, "history_retained": True}

    async def refresh(self):
        from PySide6.QtCore import QPointF, Qt
        from PySide6.QtTest import QTest

        from src.database.client import PocketBaseClient
        from src.database.constants import ORIGIN_COLLECTION
        # An actual independent REST edit proves Refresh reads disk/server data.
        client = self.client
        external = PocketBaseClient(client.base_url)
        external.token = client.token
        origin = (await external.list_records(ORIGIN_COLLECTION))[0]
        renamed = origin["name"] + " (renamed)"
        await external.update_record(ORIGIN_COLLECTION, origin["id"], {"name": renamed})
        require(renamed not in [item["name"] for item in self.dashboard.statistics()["sources"]],
                "Independent write unexpectedly mutated the in-memory cache")
        button = self.dashboard.control("statisticsRefreshButton")
        self.dashboard.window.requestActivate()
        self.gui.pump()
        point = button.mapToScene(QPointF(button.width() / 2, button.height() / 2)).toPoint()
        QTest.mouseClick(self.dashboard.window, Qt.MouseButton.LeftButton, pos=point)
        require(self.bridge.busy or renamed in [item["name"] for item in self.dashboard.statistics()["sources"]],
                "Refresh did not schedule a real database reload")
        await self.gui.wait(lambda: renamed in [item["name"] for item in self.dashboard.statistics()["sources"]],
                            "Refresh did not reload the actual persisted history")
        return await self.verify()

    async def restart(self):
        previous = await self.records()
        service = self.bridge.tracker._service
        assert service is not None and service.process is not None
        process = service.process
        await self.attach(True)
        require(process.poll() is not None, "Previous PocketBase process did not stop")
        require(await self.records() == previous, "Fresh service/bridge lost persisted history")
        return await self.verify()

    async def disabled_existing(self):
        expected = await self.records()
        await self.detach()
        path = Path(self.settings.pocketbase_data_path)
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in path.glob("*.db")}
        await self.attach(False)
        require(self.bridge._service is None and not self.bridge.busy, "Disabled tracking started an existing database")
        require(before == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in path.glob("*.db")},
                "Disabling tracking modified existing history")
        await self.attach(True)
        require(await self.records() == expected, "Re-enabling tracking lost existing history")
        return await self.verify()

    async def startup_failure(self):
        from src.database.bridge import DatabaseBridge
        from src.database.tracker import PocketBaseTracker
        path = self.directory / "not-a-database-directory"
        path.write_bytes(b"owned path conflict")
        bridge = DatabaseBridge(tracker=PocketBaseTracker(data_path=path))
        errors = []
        bridge.initializationFailed.connect(errors.append)
        try:
            bridge.start()
            await self.gui.wait(lambda: not bridge.busy, "Failed database startup left the activity indicator busy")
            require(len(errors) == 1 and "not a directory" in errors[0], "Real database startup failure was not exposed")
            require(not bridge.tracker.is_running, "Failed startup left PocketBase running")
        finally:
            await bridge.close()
        return {"real_startup_error_signalled": True, "busy_cleared": True}


async def run(args, directory):
    from PySide6.QtCore import QSettings

    from src.backend import clients
    from src.backend.account_diagnostics import AccountAccessGuard, extend_timeout_for_wait
    from src.backend.config import app_settings
    from src.database.installer import download_and_extract_pocketbase
    from src.database.service import PocketBaseService
    from src.tests.smoke.download_gui import DownloadWindow

    selected = CHECKS[:1] if args.offline_only else CHECKS
    report = {"scope": "Desktop statistics and persisted download history; real providers/media/PocketBase",
              "started_at_utc": datetime.now(timezone.utc).isoformat(), "offline_only": args.offline_only,
              "results": [{"check": name, "status": "PENDING"} for name in selected]}
    args.report.parent.mkdir(parents=True, exist_ok=True)

    def save():
        report["offline_http_attempts"] = args.offline_http_attempts
        for state in ("PASS", "FAIL", "BLOCKED", "PENDING"):
            report[state.lower()] = sum(item["status"] == state for item in report["results"])
        args.report.write_text(json.dumps(report, indent=2) + "\n")

    old_storage, old_custom = app_settings._settings, app_settings._custom_settings
    disk = QSettings(str(directory / "settings.ini"), QSettings.Format.IniFormat)
    for key, value in {"Video/output_path": str(directory / "media"), "Video/result_limit": 1,
                       "Video/pocketbase_data_path": str(directory / "history"),
                       "Video/database_path": str(directory / "legacy.db"), "Video/track_videos": False,
                       "Video/write_metadata": False, "Privacy/dns_over_https": False,
                       "Privacy/encrypted_ch": False, "Privacy/service_transport": "direct",
                       "Privacy/sni_obfuscation": False, "Misc/network_logging": False,
                       "Misc/supress_errors": True, "Misc/trust_environment": False,
                       "Performance/retries": 2, "Performance/timeout": 25,
                       "Performance/download_workers": 1, "Performance/videos_concurrency": 1,
                       "Performance/pages_concurrency": 1, "Performance/speed_limit": args.bandwidth}.items():
        disk.setValue(key, value)
    app_settings.set_settings_storage(disk)
    gui = DownloadWindow(args.timeout)
    gui.backend.load_clients()
    checks = HistoryChecks(args, directory, app_settings, gui)
    active_timeout = None
    guard = AccountAccessGuard(on_wait=lambda seconds: (extend_timeout_for_wait(active_timeout, seconds),
                                                        extend_timeout_for_wait(gui.active_timeout, seconds)))
    gui.check_access = guard.raise_if_blocked
    operations = (checks.disabled, checks.empty, checks.pending, checks.hls_resume, checks.raw_retry,
                  checks.source, checks.privacy, checks.refresh, checks.restart, checks.disabled_existing, checks.startup_failure)
    try:
        with args.report.with_suffix(".log").open("w") as log, guard:
            if not args.offline_only:
                try:
                    binary = PocketBaseService(directory / "probe").find_binary()
                except Exception:
                    with redirect_stdout(log), redirect_stderr(log):
                        binary = await asyncio.to_thread(download_and_extract_pocketbase, target_dir=directory / "bin")
                os.environ["PORN_FETCH_POCKETBASE_BINARY"] = str(binary)
            for result, operation in zip(report["results"], operations):
                print(f"RUN {result['check']}", flush=True)
                started = time.monotonic()
                try:
                    with redirect_stdout(log), redirect_stderr(log):
                        active_timeout = asyncio.timeout(args.timeout)
                        async with active_timeout:
                            result["evidence"] = await operation()
                    result["status"] = "PASS"
                except asyncio.CancelledError:
                    result["status"] = "BLOCKED" if guard.blocked else "INTERRUPTED"
                    result["access_control"] = guard.blocked
                    raise
                except Exception as error:
                    traceback.print_exc(file=log)
                    result.update(status="FAIL", error_type=type(error).__name__, error=str(error))
                    break  # Later checks depend on this real history state.
                finally:
                    active_timeout = None
                    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
                    save()
                    print(f"{result['status']} {result['check']}" + (f": {result['error']}" if result.get('error') else ""), flush=True)
    except asyncio.CancelledError:
        return 1 if guard.blocked else 130
    finally:
        # Stop real writers before disconnecting persistence or deleting their files.
        for event in gui.backend._download_stop_events.values():
            event.set()
        tasks = tuple(gui.backend._background_tasks)
        if tasks:
            try:
                await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 30)
            except TimeoutError:
                pass
        await checks.detach()
        await gui.shutdown()
        await clients.close_all_clients()
        app_settings._settings, app_settings._custom_settings = old_storage, old_custom
        report["rate_limit_recovery"] = guard.rate_limit_events
        save()
    print(f"{report['pass']} passed, {report['fail']} failed, {report['pending']} not run. Report: {args.report}")
    return int(bool(report["fail"] or report["blocked"] or report["pending"]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List checks without Qt or network startup")
    parser.add_argument("--offline-only", action="store_true", help="Only the real disabled/empty GUI contract; no network")
    parser.add_argument("--timeout", type=float, default=240, help="Per-workflow timeout in seconds")
    parser.add_argument("--bandwidth", type=float, default=2, help="Native media bandwidth cap in MiB/s")
    parser.add_argument("--report", type=Path, default=Path(tempfile.gettempdir()) / "porn-fetch-statistics.json")
    args = parser.parse_args()
    args.offline_http_attempts = 0
    if args.timeout <= 0 or args.bandwidth <= 0:
        parser.error("Timeout and bandwidth must be positive")
    if args.list:
        print("\n".join(CHECKS))
        return 0
    args.report = args.report.resolve()
    args.ffmpeg = shutil.which("ffmpeg")
    if not args.offline_only:
        require(args.ffmpeg and shutil.which("ffprobe"), "FFmpeg and ffprobe are required")
    os.environ["PORN_FETCH_TEST_ENV"] = "1"
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    os.environ["QML_DISABLE_DISK_CACHE"] = "1"
    logging.disable(logging.CRITICAL)
    with tempfile.TemporaryDirectory(prefix="porn-fetch-statistics-") as temporary:
        directory = Path(temporary)
        for kind in ("CONFIG", "CACHE", "DATA"):
            os.environ[f"XDG_{kind}_HOME"] = str(directory / kind.lower())
        previous = Path.cwd()
        os.chdir(directory)
        try:
            from PySide6.QtGui import QGuiApplication
            from PySide6.QtQuickControls2 import QQuickStyle
            QQuickStyle.setStyle("Material")
            app = QGuiApplication.instance() or QGuiApplication([])
            app.setQuitOnLastWindowClosed(False)
            with ExitStack() as safety:
                if args.offline_only:
                    from unittest.mock import patch

                    from base_api import BaseCore
                    from curl_cffi.requests import AsyncSession

                    def forbidden_sync(*params, **options):
                        args.offline_http_attempts += 1
                        raise AssertionError("HTTP attempted during the offline statistics check")

                    async def forbidden(*params, **options):
                        return forbidden_sync(*params, **options)

                    safety.enter_context(patch.object(BaseCore, "request", forbidden))
                    safety.enter_context(patch.object(AsyncSession, "request", forbidden))
                    safety.enter_context(patch("src.database.client.urlopen", forbidden_sync))
                result = asyncio.run(run(args, directory))
            app.processEvents()
            return result or int(bool(args.offline_http_attempts))
        except KeyboardInterrupt:
            print(f"Stopped. Partial report: {args.report}")
            return 130
        finally:
            os.chdir(previous)


if __name__ == "__main__":
    raise SystemExit(main())
