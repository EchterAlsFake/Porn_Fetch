"""Qt/QML adapter for the Qt-free PocketBase services."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from src.backend.config import IS_ANDROID, app_settings
from src.shared.media import VideoObject

from .client import PocketBaseClient
from .service import PocketBaseService
from .tracker import PocketBaseTracker


class DatabaseBridge(QObject):
    """Expose download tracking and dashboard data to QML."""

    iteratorsChanged = Signal()
    statisticsChanged = Signal()
    downloadSaved = Signal(str)
    initializationFailed = Signal(str)
    busyChanged = Signal()

    def __init__(
        self,
        parent: QObject | None = None,
        tracker: PocketBaseTracker | None = None,
        *,
        tracking_supported: bool = True,
    ):
        super().__init__(parent)
        self._tasks: set[asyncio.Task[Any]] = set()
        self._refresh_task: asyncio.Task[None] | None = None
        self._closing = False
        # Reuse the disabled tracker contract on Android; no database is created or started.
        self._tracker = tracker or PocketBaseTracker(
            data_path=app_settings.pocketbase_data_path,
            enabled=tracking_supported and not IS_ANDROID and bool(app_settings.track_videos),
            legacy_sqlite_path=app_settings.legacy_database_path,
        )
        self._tracker.on_download_saved = self.downloadSaved.emit
        self._tracker.on_iterators_changed = self.iteratorsChanged.emit
        self._tracker.on_statistics_changed = self.statisticsChanged.emit
        self._tracker.on_initialization_failed = self.initializationFailed.emit

    @property
    def tracker(self) -> PocketBaseTracker:
        return self._tracker

    @property
    def _enabled(self) -> bool:
        return self._tracker.enabled

    @property
    def _service(self) -> PocketBaseService | None:
        return self._tracker._service

    @property
    def _client(self) -> PocketBaseClient | None:
        return self._tracker._client

    @property
    def _iterators(self) -> dict[str, dict[str, Any]]:
        return self._tracker._iterators

    @property
    def _videos(self) -> dict[str, dict[str, Any]]:
        return self._tracker._videos

    @Property(bool, notify=busyChanged)
    def busy(self) -> bool:
        return bool(self._tasks)

    def _track_task(self, task: asyncio.Task[Any]) -> None:
        if task.done() or task in self._tasks:
            return
        was_busy = self.busy
        self._tasks.add(task)
        task.add_done_callback(self._task_done)
        if not was_busy:
            self.busyChanged.emit()

    def _task_done(self, task: asyncio.Task[Any]) -> None:
        self._tasks.discard(task)
        if not task.cancelled() and (error := task.exception()) is not None:
            if self._closing:
                logging.getLogger(__name__).error("History write failed during shutdown: %s", error)
            else:
                self.initializationFailed.emit(f"Could not save download history: {error}")
        if not self._tasks:
            self.busyChanged.emit()

    def start(self) -> None:
        if self._tracker.enabled and not self._closing:
            self._track_task(self._tracker.schedule_startup())

    @Slot()
    def refresh(self) -> None:
        """Reload persisted history without blocking the GUI or duplicating requests."""
        if self._closing or not self._tracker.enabled or (self._refresh_task is not None and not self._refresh_task.done()):
            return
        self._refresh_task = asyncio.create_task(self._refresh_history(), name="history-refresh")
        self._track_task(self._refresh_task)

    async def _refresh_history(self) -> None:
        try:
            await self._tracker.refresh_cache()
        except asyncio.CancelledError:
            raise
        except Exception as error:
            self.initializationFailed.emit(f"Could not refresh download history: {error}")

    @Slot(object)
    def on_video_updated(self, video: VideoObject) -> None:
        if self._tracker.enabled and not self._closing:
            self._track_task(self._tracker.spawn_save_video(video))

    @Slot(result=list)
    def getAvailableIterators(self) -> list[dict[str, Any]]:
        return self._tracker.get_available_iterators()

    @Slot(str, result=list)
    def getFailedVideosForIterator(self, iterator_url: str) -> list[dict[str, Any]]:
        return self._tracker.get_failed_videos(iterator_url)

    @staticmethod
    def _status_bucket(status: str | None) -> str:
        return PocketBaseTracker.status_bucket(status)

    @staticmethod
    def _video_payload(video: VideoObject, iterator_record: dict[str, Any] | None) -> dict[str, Any]:
        return PocketBaseTracker.create_video_payload(video, iterator_record)

    @Slot(result="QVariantMap")
    def getDashboardStats(self) -> dict[str, Any]:
        return self._tracker.get_dashboard_stats()

    async def close(self) -> None:
        self._closing = True
        if self._refresh_task is not None and not self._refresh_task.done():
            self._refresh_task.cancel()
            await asyncio.gather(self._refresh_task, return_exceptions=True)
        writes = tuple(self._tasks)
        if writes:
            _, pending = await asyncio.wait(writes, timeout=15)
            if pending:
                logging.getLogger(__name__).warning("Timed out flushing %d history tasks", len(pending))
                for task in pending:
                    task.cancel()
            await asyncio.gather(*writes, return_exceptions=True)
        await self._tracker.close()
