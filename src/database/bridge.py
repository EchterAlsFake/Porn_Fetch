"""Qt/QML adapter for the Qt-free PocketBase services."""
from __future__ import annotations

import sys
from typing import Any

from PySide6.QtCore import QObject, Signal, Slot

from src.backend.config import app_settings
from src.shared.media import VideoObject

from .android_tracker import AndroidTracker
from .client import PocketBaseClient
from .service import PocketBaseService
from .tracker import PocketBaseTracker


class DatabaseBridge(QObject):
    """Expose download tracking and dashboard data to QML."""

    iteratorsChanged = Signal()
    statisticsChanged = Signal()
    downloadSaved = Signal(str)
    initializationFailed = Signal(str)

    def __init__(self, parent: QObject | None = None, tracker: PocketBaseTracker | None = None):
        super().__init__(parent)
        self._tracker = tracker or (
            AndroidTracker(data_path=app_settings.pocketbase_data_path, enabled=bool(app_settings.track_videos))
            if (sys.platform == "android" or hasattr(sys, "getandroidapilevel")) else PocketBaseTracker(
                data_path=app_settings.pocketbase_data_path,
                enabled=bool(app_settings.track_videos),
                legacy_sqlite_path=app_settings.legacy_database_path,
            )
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

    def start(self) -> None:
        if self._tracker.enabled:
            self._tracker.schedule_startup()

    @Slot(object)
    def on_video_updated(self, video: VideoObject) -> None:
        if self._tracker.enabled:
            self._tracker.spawn_save_video(video)

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
        await self._tracker.close()
