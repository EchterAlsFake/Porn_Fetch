"""Real PocketBase and QML adapter, with controlled media transfers."""
import asyncio
import os
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor  # noqa: F401 - resolve Python 3.15 lazy import before Shiboken
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"
os.environ.setdefault("PORN_FETCH_TEST_ENV", "1")

import shiboken6
from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtQuick import QQuickWindow  # noqa: F401 - register the concrete QML window wrapper

from src.backend.creator_bridge import CreatorBridge
from src.backend.download_manager import DownloadListModel, DownloadManager
from src.database.creators import SUBSCRIPTIONS, VIDEOS
from src.database.errors import PocketBaseError
from src.database.tracker import PocketBaseTracker
from src.shared.media import VideoObject

_app = QGuiApplication.instance() or QGuiApplication([])
BINARY = os.environ.get("PORN_FETCH_TEST_POCKETBASE")


class Transfers:
    def __init__(self):
        self.premium = True
        self._downloads_model = DownloadListModel(premium_access=self.has_premium_access)
        self.download_manager = DownloadManager()
        self.download_manager.video_added.connect(lambda video: self._downloads_model.add_video(video, "720"))
        self._download_tasks = {}
        self._license_bridge = None
        self.starts = 0
        self.gate = asyncio.Event()
        self.gate.set()

    def has_premium_access(self):
        return self.premium

    def download_video(self, job):
        if job in self._download_tasks:
            return
        self.starts += 1
        async def download():
            self._downloads_model.set_status(job, "downloading")
            await self.gate.wait()
            self._downloads_model.set_status(job, "completed")
            self._downloads_model.update_progress(job, 100)
            self.download_manager.update_status(job, "completed")
            self.remove_video(job)  # Production transfers remove their completed rows immediately.
        self._download_tasks[job] = asyncio.create_task(download())

    def stop_download(self, job):
        task = self._download_tasks.get(job)
        if task:
            task.cancel()

    def remove_video(self, job):
        self._downloads_model.remove_video(job)
        self.download_manager.remove_video(job)


class CreatorAvailabilityTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="creator-availability-test-")
        self.tracker = PocketBaseTracker(self.folder.name, enabled=False, binary_path=BINARY)
        self.backend = Transfers()
        self.bridge = CreatorBridge(self.backend, self.tracker)

    async def asyncTearDown(self):
        await self.bridge.close()
        await self.tracker.close()
        self.folder.cleanup()

    async def test_startup_detects_missing_pocketbase_before_any_source_and_blocks_add(self):
        with patch("src.backend.creator_bridge.PocketBaseService.find_binary", side_effect=PocketBaseError("Runtime not installed")):
            self.assertFalse(self.bridge.available)
            self.bridge.start()
            await self.bridge._availability_task
        self.assertEqual(self.bridge.availability, "unavailable")
        self.assertIn("--install-pocketbase", self.bridge.availabilityHelp)
        self.assertEqual(self.bridge.availabilityError, "Runtime not installed")
        self.assertFalse((Path(self.folder.name) / "data.db").exists())
        self.assertEqual(self.bridge.defaultQuality, "best")

        engine = QQmlApplicationEngine()
        warnings = []
        engine.warnings.connect(lambda errors: warnings.extend(e.toString() for e in errors))
        component = QQmlComponent(engine)
        component.setData(b'''import QtQuick
QtObject { property bool dark_mode: true; property bool high_contrast: false
property string accent_color: "#a69bff"; property int font_size: 12
property bool anonymous_mode: false; property bool reduced_motion: true }''', QUrl())
        settings = component.create()
        engine.rootContext().setContextProperty("appSettings", settings)
        engine.rootContext().setContextProperty("creatorBridge", self.bridge)
        ui = Path(__file__).resolve().parents[2] / "frontend/UI/CreatorsPreview.qml"
        engine.load(QUrl.fromLocalFile(str(ui)))
        try:
            self.assertTrue(engine.rootObjects(), warnings)
            window = engine.rootObjects()[0]
            self.assertFalse(window.findChild(QObject, "creatorAddButton").property("enabled"))
            self.assertEqual(window.findChild(QObject, "creatorAvailabilityTitle").property("text"), "PocketBase is unavailable")
            self.assertTrue(window.findChild(QObject, "creatorCheckAvailabilityButton").property("visible"))
            self.assertEqual(warnings, [])
        finally:
            shiboken6.delete(engine)
            shiboken6.delete(settings)

    @unittest.skipUnless(BINARY, "Set PORN_FETCH_TEST_POCKETBASE for repair/recheck verification")
    async def test_check_again_recovers_after_pocketbase_is_installed(self):
        with patch("src.backend.creator_bridge.PocketBaseService.find_binary", side_effect=PocketBaseError("Runtime not installed")):
            self.bridge.start()
            await self.bridge._availability_task
        self.assertFalse(self.bridge.available)
        self.bridge.checkAvailability()
        await self.bridge._availability_task
        self.assertTrue(self.bridge.available)
        self.assertEqual(self.bridge.availabilityError, "")
        self.assertIsNotNone(self.bridge.library)
        self.assertEqual(self.bridge.sources, [])


@unittest.skipUnless(BINARY, "Set PORN_FETCH_TEST_POCKETBASE for real database checks")
class CreatorBridgeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="creator-bridge-test-")
        self.tracker = PocketBaseTracker(self.folder.name, enabled=False, binary_path=BINARY)
        self.backend = Transfers()
        self.bridge = CreatorBridge(self.backend, self.tracker)
        await self.bridge.ensure_ready()
        self.source = await self.bridge.repo.create(SUBSCRIPTIONS, {"url": "https://www.bellesa.co/channels/demo", "provider": "bellesa", "name": "Real library", "folder": self.folder.name, "quality": "720", "status": "complete"})
        await self.bridge.repo.remember_many(self.source, [{"identity": "bellesa:video:123", "provider": "bellesa", "url": "https://www.bellesa.co/videos/123", "title": "Persisted video"}], "2026-11-16")
        await self.bridge._refresh()

    async def asyncTearDown(self):
        await self.bridge.close()
        await self.tracker.close()
        self.folder.cleanup()

    async def wait_for(self, condition):
        for _ in range(200):
            _app.processEvents()
            if await condition():
                return
            await asyncio.sleep(.02)
        self.fail(f"Operation did not reach its expected state: selection={self.bridge._selection!r}, total={self.bridge.videoTotal}, message={self.bridge.message}, refresh={self.bridge._refresh_task!r}, sources={self.bridge.sources!r}")

    async def test_real_controller_renders_persisted_rows(self):
        engine = QQmlApplicationEngine()
        warnings = []
        engine.warnings.connect(lambda errors: warnings.extend(e.toString() for e in errors))
        component = QQmlComponent(engine)
        component.setData(b'''import QtQuick
QtObject { property bool dark_mode: true; property bool high_contrast: false
property string accent_color: "#a69bff"; property int font_size: 12
property bool anonymous_mode: false; property bool reduced_motion: true }''', QUrl())
        settings = component.create()
        engine.rootContext().setContextProperty("appSettings", settings)
        engine.rootContext().setContextProperty("creatorBridge", self.bridge)
        ui = Path(__file__).resolve().parents[2] / "frontend/UI/CreatorsPreview.qml"
        engine.load(QUrl.fromLocalFile(str(ui)))
        try:
            self.assertTrue(engine.rootObjects(), warnings)
            window = engine.rootObjects()[0]
            page = window.findChild(QObject, "creatorsPage")
            page.setProperty("selectedId", self.source["id"])
            self.assertEqual(self.bridge._selection[0], self.source["id"], str(page.property("dataSource")))
            async def populated():
                return self.bridge.videoTotal == 1
            await self.wait_for(populated)
            self.assertEqual(page.property("pageCount"), 1)
            self.assertTrue(page.property("detailOpen"))
            self.assertEqual(self.bridge.sources[0]["name"], "Real library")
            self.assertEqual(self.bridge.videos[0]["title"], "Persisted video")
            self.assertEqual(warnings, [])
        finally:
            shiboken6.delete(engine)
            shiboken6.delete(settings)

    async def test_dispatch_persists_snapshot_and_does_not_duplicate_transfer(self):
        async def metadata(native):
            return VideoObject(url="https://www.bellesa.co/videos/123", title="Fresh title", author="Studio", length=10,
                tags=[], thumbnail_url="", video_id="123", publish_date=None, qualities=[480, 720], status="pending")
        await self.bridge.repo.put(SUBSCRIPTIONS, self.source["id"], {"quality": "480"})
        with patch("src.backend.creator_bridge.clients.get_video", AsyncMock(return_value=object())), patch("src.backend.creator_bridge.clients.load_video_attributes", metadata):
            await self.bridge.library.queue(self.source["id"], "download")
            async def completed():
                return (await self.bridge.repo.page(VIDEOS, filter='status = "completed"'))["totalItems"] == 1
            await self.wait_for(completed)
            row = (await self.bridge.repo.page(VIDEOS))["items"][0]
            self.assertTrue(row["snapshot"])
            self.assertEqual(row["snapshot"]["selected_quality"], "480")
            self.assertTrue(row["output_path"].startswith(self.folder.name))
            self.assertEqual(self.backend.starts, 1)
            await self.bridge.library.queue(self.source["id"], "download")
            await asyncio.sleep(.1)
            self.assertEqual(self.backend.starts, 1)
            self.assertEqual(self.backend._downloads_model.rowCount(), 0)

    async def test_resume_refreshes_metadata_and_retains_path_and_job(self):
        video = (await self.bridge.repo.page(VIDEOS))["items"][0]
        snapshot = {"url": video["url"], "title": "Old title", "author": "", "length": 10, "tags": [], "video_id": "123",
            "publish_date": None, "qualities": [720], "status": "cancelled", "identifier": "savedjob", "output_path": str(Path(self.folder.name) / "original.mp4"), "selected_quality": "720"}
        await self.bridge.repo.put(VIDEOS, video["id"], {"status": "pending", "owner": self.source["id"], "job": "savedjob", "snapshot": snapshot})
        fresh = VideoObject(url=video["url"], title="Changed title", author="", length=10, tags=[], thumbnail_url="", video_id="123", publish_date=None, qualities=[720], status="pending")
        with patch("src.backend.creator_bridge.clients.get_video", AsyncMock(return_value=object())), patch("src.backend.creator_bridge.clients.load_video_attributes", AsyncMock(return_value=fresh)):
            self.bridge.request_refresh()
            async def completed():
                return (await self.bridge.repo.get(VIDEOS, video["id"]))["status"] == "completed"
            await self.wait_for(completed)
        row = await self.bridge.repo.get(VIDEOS, video["id"])
        self.assertEqual(row["job"], "savedjob")
        self.assertEqual(row["output_path"], snapshot["output_path"])

    async def test_android_dispatch_stages_privately_and_keeps_shared_destination(self):
        destination = "content://com.android.externalstorage.documents/tree/primary%3AMovies"
        await self.bridge.repo.put(SUBSCRIPTIONS, self.source["id"], {"folder": destination})
        fresh = VideoObject(url="https://bellesa.co/videos/123", title="Android fixture", author="", length=1,
            tags=[], thumbnail_url="", video_id="123", publish_date=None, qualities=[720], status="pending")
        with patch("src.backend.creator_bridge.IS_ANDROID", True), \
             patch("src.backend.creator_bridge.TEMP_DIRECTORY", Path(self.folder.name) / "private-state"), \
             patch("src.backend.creator_bridge.clients.get_video", AsyncMock(return_value=object())), \
             patch("src.backend.creator_bridge.clients.load_video_attributes", AsyncMock(return_value=fresh)):
            await self.bridge.library.queue(self.source["id"], "download")
            async def completed():
                return (await self.bridge.repo.page(VIDEOS, filter='status = "completed"'))["totalItems"] == 1
            await self.wait_for(completed)
            row = (await self.bridge.repo.page(VIDEOS))["items"][0]
            self.assertEqual(row["snapshot"]["export_destination"], destination)
            self.assertTrue(Path(row["output_path"]).is_relative_to(Path(self.folder.name) / "private-state/creator-downloads"))

    async def test_unavailable_resume_quality_keeps_progress_and_reports_failure(self):
        from src.shared.download_recovery import queue_record
        row = (await self.bridge.repo.page(VIDEOS))["items"][0]
        output = Path(self.folder.name) / "retained.mp4"
        output.write_bytes(b"retained-partial-data")
        saved = VideoObject(url=row["url"], title="Saved title", author="", length=10, tags=[], thumbnail_url="", video_id="123",
            publish_date=None, qualities=[720], status="cancelled", identifier="qualityjob", output_path=output, selected_quality="720")
        await self.bridge.repo.put(VIDEOS, row["id"], {"status": "pending", "owner": self.source["id"], "job": "qualityjob", "snapshot": queue_record(saved)})
        fresh = VideoObject(url=row["url"], title="New metadata", author="", length=10, tags=[], thumbnail_url="", video_id="123",
            publish_date=None, qualities=[1080], status="pending")
        with patch("src.backend.creator_bridge.clients.get_video", AsyncMock(return_value=object())), patch("src.backend.creator_bridge.clients.load_video_attributes", AsyncMock(return_value=fresh)):
            self.bridge.request_refresh()
            async def failed():
                return (await self.bridge.repo.get(VIDEOS, row["id"]))["status"] == "failed"
            await self.wait_for(failed)
            await asyncio.sleep(.4)  # Delayed progress writes must not erase the failure.
        latest = await self.bridge.repo.get(VIDEOS, row["id"])
        self.assertEqual(latest["status"], "failed")
        self.assertIn("saved quality", latest["error"])
        self.assertEqual(output.read_bytes(), b"retained-partial-data")
        self.assertEqual(self.backend.starts, 0)

    async def test_completed_history_matches_stable_id_across_url_variants(self):
        await self.bridge.repo.create("video_records", {"url": "https://bellesa.co/videos/123/old-title", "video_id": "123", "status": "completed", "output_path": str(Path(self.folder.name) / "already-downloaded.mp4")})
        with patch("src.backend.creator_bridge.clients.get_video", AsyncMock(side_effect=AssertionError("Completed history must not start a transfer"))):
            await self.bridge.library.queue(self.source["id"], "download")
            async def completed():
                return (await self.bridge.repo.page(VIDEOS, filter='status = "completed"'))["totalItems"] == 1
            await self.wait_for(completed)
        self.assertEqual(self.backend.starts, 0)

    async def test_free_preview_downloads_five_at_720p_and_does_not_expand_after_rescan(self):
        from src.shared.access import bulk_video_requires_premium
        self.backend.premium = False
        await self.bridge.repo.put(SUBSCRIPTIONS, self.source["id"], {"quality": "best"})
        await self.bridge.repo.remember_many(self.source, [
            {"identity": f"bellesa:video:{i}", "provider": "bellesa", "url": f"https://bellesa.co/videos/{i}"}
            for i in range(1, 7)], "2026-11-17")
        async def metadata(url):
            return VideoObject(url=url, title="Free preview", author="", length=1, tags=[], thumbnail_url="",
                video_id=url.rsplit("/", 1)[-1], publish_date=None, qualities=[480, 720, 1080, 2160], status="pending")
        with patch("src.backend.creator_bridge.clients.get_video", AsyncMock(side_effect=lambda url: url)), \
             patch("src.backend.creator_bridge.clients.load_video_attributes", metadata):
            await self.bridge.library.queue(self.source["id"], "download")
            async def completed():
                return (await self.bridge.repo.page(VIDEOS, filter='status = "completed"'))["totalItems"] == 5
            await self.wait_for(completed)
            self.assertEqual(self.backend.starts, 5)
            for row in (await self.bridge.repo.page(VIDEOS, filter='status = "completed"'))["items"]:
                self.assertEqual(row["snapshot"]["selected_quality"], "720")
                self.assertFalse(bulk_video_requires_premium(SimpleNamespace(**row["snapshot"])))
            preview_before = [m["id"] for m in await self.bridge.repo.preview_memberships(self.source["id"])]
            await self.bridge.repo.remember_many(self.source, [
                {"identity": "bellesa:video:999", "provider": "bellesa", "url": "https://bellesa.co/videos/999"}], "2026-11-18")
            self.assertEqual([m["id"] for m in await self.bridge.repo.preview_memberships(self.source["id"])], preview_before)
            await self.bridge.library.queue(self.source["id"], "download")
            outside = (await self.bridge.repo.page(VIDEOS, filter='status = "new"'))["items"][0]
            await self.bridge.repo.put(VIDEOS, outside["id"], {"status": "pending", "owner": self.source["id"]})
            self.bridge.request_refresh()
            async def blocked():
                return (await self.bridge.repo.get(VIDEOS, outside["id"]))["status"] == "paused"
            await self.wait_for(blocked)
            self.assertEqual(self.backend.starts, 5)
            with self.assertRaisesRegex(PermissionError, "Automatic"):
                await self.bridge.library.queue(self.source["id"], "automatic")
            visible = await self.bridge.repo.video_page(self.source["id"], preview=True)
            self.assertEqual(visible["totalItems"], 5)
            counts = (await self.bridge.library.subscriptions())[0]["counts"]
            self.assertEqual((counts["total"], counts["completed"]), (5, 5))
