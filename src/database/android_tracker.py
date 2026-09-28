"""In-process download history for Android, where bundled child processes are unsuitable."""
from __future__ import annotations

import asyncio
import json
import sqlite3
from pathlib import Path
from typing import Any

from src.shared.media import VideoObject

from .tracker import PocketBaseTracker


class AndroidTracker(PocketBaseTracker):
    """Keep the GUI tracker contract while storing records in app-private SQLite."""

    def __init__(self, data_path: str | Path, *, enabled: bool = True):
        super().__init__(data_path, enabled=False)
        self.enabled = bool(enabled)
        self.database_path = self.data_path / "downloads.sqlite3"

    @staticmethod
    def _connect(path: Path) -> sqlite3.Connection:
        path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(path)
        connection.execute("CREATE TABLE IF NOT EXISTS videos (url TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        connection.execute("CREATE TABLE IF NOT EXISTS origins (url TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        return connection

    def schedule_startup(self) -> asyncio.Task[None]:
        if self._startup_task is None:
            self._startup_task = self._spawn(self._load(), "android-history-startup")
        return self._startup_task

    async def _load(self) -> None:
        if not self.enabled:
            return

        def read() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
            with self._connect(self.database_path) as connection:
                origins = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM origins")]
                videos = [json.loads(row[0]) for row in connection.execute("SELECT payload FROM videos")]
            return origins, videos

        try:
            origins, videos = await asyncio.to_thread(read)
            self._iterators = {item["url"]: item for item in origins}
            self._videos = {item["url"]: item for item in videos}
            if self.on_iterators_changed:
                self.on_iterators_changed()
            if self.on_statistics_changed:
                self.on_statistics_changed()
        except Exception as error:
            if self.on_initialization_failed:
                self.on_initialization_failed(str(error))

    def spawn_save_video(self, video: VideoObject) -> asyncio.Task[dict[str, Any]]:
        return self._spawn(self.save_video(video), f"android-history-save-{video.identifier or video.video_id}")

    async def save_video(self, video: VideoObject) -> dict[str, Any]:
        if not self.enabled:
            return {}
        async with self._save_lock:
            if self._startup_task is None:
                self.schedule_startup()
            assert self._startup_task is not None
            await self._startup_task
            origin = None
            if video.origin_iterator_url:
                origin = {
                    "id": video.origin_iterator_url,
                    "url": video.origin_iterator_url,
                    "name": video.origin_iterator_name or video.origin_iterator_url,
                }
            record = self.create_video_payload(video, origin)

            def write() -> None:
                with self._connect(self.database_path) as connection:
                    if origin:
                        connection.execute(
                            "INSERT OR REPLACE INTO origins (url, payload) VALUES (?, ?)",
                            (origin["url"], json.dumps(origin)),
                        )
                    connection.execute(
                        "INSERT OR REPLACE INTO videos (url, payload) VALUES (?, ?)",
                        (record["url"], json.dumps(record)),
                    )

            await asyncio.to_thread(write)
            if origin:
                self._iterators[origin["url"]] = origin
            self._videos[record["url"]] = record

        if self.on_download_saved:
            self.on_download_saved(str(record.get("video_id", "")))
        if self.on_iterators_changed:
            self.on_iterators_changed()
        if self.on_statistics_changed:
            self.on_statistics_changed()
        return record
