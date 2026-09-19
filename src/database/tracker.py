"""Download tracking orchestration and statistics backed by PocketBase."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from src.shared.media import VideoObject

from .client import PocketBaseClient
from .constants import ORIGIN_COLLECTION, VIDEO_COLLECTION
from .errors import PocketBaseError
from .legacy import _format_date, _read_legacy_sqlite
from .service import PocketBaseService

logger = logging.getLogger(__name__)


class PocketBaseTracker:
    """Pure-Python asynchronous tracker for PocketBase download records and statistics.

    Shared between the PySide6 GUI and Qt-free CLI frontends.
    """

    def __init__(
        self,
        data_path: str | Path = "./pocketbase_data",
        *,
        enabled: bool = True,
        binary_path: str | Path | None = None,
        legacy_sqlite_path: str | Path | None = None,
    ):
        self.data_path = Path(data_path).expanduser().resolve()
        self.enabled = bool(enabled)
        self.binary_path = Path(binary_path).expanduser().resolve() if binary_path else None
        self.legacy_sqlite_path = Path(legacy_sqlite_path).expanduser().resolve() if legacy_sqlite_path else None
        self._service: PocketBaseService | None = (
            PocketBaseService(self.data_path, binary_path=self.binary_path) if self.enabled else None
        )
        self._client: PocketBaseClient | None = None
        self._startup_task: asyncio.Task[None] | None = None
        self._tasks: set[asyncio.Task[Any]] = set()
        self._save_lock = asyncio.Lock()
        self._iterators: dict[str, dict[str, Any]] = {}
        self._videos: dict[str, dict[str, Any]] = {}

        # Callbacks for GUI / external listeners
        self.on_download_saved: Callable[[str], None] | None = None
        self.on_iterators_changed: Callable[[], None] | None = None
        self.on_statistics_changed: Callable[[], None] | None = None
        self.on_initialization_failed: Callable[[str], None] | None = None

    @property
    def is_running(self) -> bool:
        return self._service is not None and self._service.process is not None and self._service.process.poll() is None

    def schedule_startup(self) -> asyncio.Task[None]:
        if self._startup_task is None:
            self._startup_task = self._spawn(self._initialize(), "pocketbase-startup")
        return self._startup_task

    def _spawn(self, coroutine: Any, name: str) -> asyncio.Task[Any]:
        task = asyncio.create_task(coroutine, name=name)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def start(self) -> PocketBaseClient | None:
        if not self.enabled:
            return None
        return await self._ensure_client()

    async def _initialize(self) -> None:
        assert self._service is not None
        try:
            self._client = await self._service.start()
            await self._import_legacy_sqlite()
            await self.refresh_cache()
        except asyncio.CancelledError:
            raise
        except Exception as error:
            logger.warning("Could not initialize PocketBase download tracking: %s", error)
            self._initialization_error = str(error)
            if self.on_initialization_failed:
                self.on_initialization_failed(str(error))

    async def _ensure_client(self) -> PocketBaseClient:
        if self._client is not None:
            return self._client
        self.schedule_startup()
        assert self._startup_task is not None
        await self._startup_task
        if self._client is None:
            err = getattr(self, "_initialization_error", None) or "PocketBase could not be initialized"
            raise PocketBaseError(err)
        return self._client

    def spawn_save_video(self, video: VideoObject) -> asyncio.Task[Any]:
        return self._spawn(self.save_video(video), f"pocketbase-save-{video.identifier or video.video_id}")

    async def save_video(self, video: VideoObject) -> dict[str, Any]:
        async with self._save_lock:
            client = await self._ensure_client()
            iterator_record = await self._upsert_iterator(client, video)
            payload = self.create_video_payload(video, iterator_record)
            existing = await client.find_by_url(VIDEO_COLLECTION, video.url)
            if existing:
                record = await client.update_record(VIDEO_COLLECTION, existing["id"], payload)
            else:
                record = await client.create_record(VIDEO_COLLECTION, payload)
            self._videos[video.url] = record

        if self.on_download_saved:
            self.on_download_saved(str(record.get("video_id", video.video_id)))
        if self.on_iterators_changed:
            self.on_iterators_changed()
        if self.on_statistics_changed:
            self.on_statistics_changed()
        return record

    async def record_download(
        self,
        url: str,
        title: str = "",
        *,
        video_id: str = "",
        author: str = "",
        length: int | None = None,
        thumbnail_url: str = "",
        status: str = "completed",
        output_path: str | Path | None = None,
        selected_quality: str = "",
        is_hls: bool = False,
        missing_segments: list[int] | None = None,
        origin_iterator_url: str = "",
        origin_iterator_name: str = "",
        tags: list[str] | None = None,
        qualities: list[int] | None = None,
        publish_date: datetime | str | None = None,
        is_from_account: bool = False,
    ) -> dict[str, Any]:
        """Convenience method to save a download record from primitives."""
        date_val = publish_date if isinstance(publish_date, datetime) else None
        video = VideoObject(
            url=url,
            title=title,
            author=author,
            length=length,
            tags=tags or [],
            thumbnail_url=thumbnail_url,
            video_id=video_id or title or url,
            publish_date=date_val,
            qualities=qualities or [],
            status=status,
            output_path=Path(output_path) if output_path else None,
            selected_quality=selected_quality,
            origin_iterator_url=origin_iterator_url or None,
            origin_iterator_name=origin_iterator_name or None,
            is_hls=is_hls,
            missing_segments=missing_segments,
            is_from_account=is_from_account,
        )
        return await self.save_video(video)

    async def _upsert_iterator(
        self, client: PocketBaseClient, video: VideoObject
    ) -> dict[str, Any] | None:
        if not video.origin_iterator_url:
            return None
        name = video.origin_iterator_name or "Unknown Source"
        existing = await client.find_by_url(ORIGIN_COLLECTION, video.origin_iterator_url)
        if existing:
            if existing.get("name") != name:
                existing = await client.update_record(
                    ORIGIN_COLLECTION, existing["id"], {"name": name}
                )
            record = existing
        else:
            record = await client.create_record(
                ORIGIN_COLLECTION, {"url": video.origin_iterator_url, "name": name}
            )
        self._iterators[video.origin_iterator_url] = record
        return record

    @staticmethod
    def create_video_payload(
        video: VideoObject, iterator_record: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        file_size_mb = 0.0
        if video.output_path:
            try:
                p = Path(video.output_path)
                if p.is_file():
                    file_size_mb = p.stat().st_size / (1024 * 1024)
                elif p.is_dir():
                    file_size_mb = sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / (1024 * 1024)
            except OSError:
                pass
        return {
            "url": video.url,
            "title": video.title or "",
            "video_id": video.video_id or "",
            "author": video.author or "",
            "length": str(video.length) if video.length is not None else "",
            "thumbnail_url": video.thumbnail_url or "",
            "publish_date": _format_date(video.publish_date),
            "status": video.status or "",
            "tags": video.tags or [],
            "qualities": video.qualities or [],
            "identifier": video.identifier or "",
            "output_path": str(video.output_path) if video.output_path else "",
            "selected_quality": str(video.selected_quality) if video.selected_quality is not None else "",
            "file_size_mb": round(file_size_mb, 2),
            "downloaded_at": _format_date(datetime.now().astimezone()),
            "is_hls": bool(video.is_hls),
            "missing_segments": video.missing_segments or [],
            "is_from_account": bool(getattr(video, "is_from_account", False)),
            "origin_iterator_url": video.origin_iterator_url or "",
            "origin_iterator": iterator_record["id"] if iterator_record else "",
        }

    async def refresh_cache(self) -> None:
        client = await self._ensure_client()
        iterators, videos = await asyncio.gather(
            client.list_records(ORIGIN_COLLECTION, sort="name"),
            client.list_records(VIDEO_COLLECTION, sort="-downloaded_at"),
        )
        self._iterators = {record["url"]: record for record in iterators}
        self._videos = {record["url"]: record for record in videos}
        if self.on_iterators_changed:
            self.on_iterators_changed()
        if self.on_statistics_changed:
            self.on_statistics_changed()

    def get_available_iterators(self) -> list[dict[str, Any]]:
        return [
            {"id": record.get("id", ""), "name": record.get("name", ""), "url": record["url"]}
            for record in sorted(self._iterators.values(), key=lambda item: item.get("name", ""))
        ]

    def get_failed_videos(self, iterator_url: str | None = None) -> list[dict[str, Any]]:
        return [
            {
                "title": video.get("title", ""),
                "url": video.get("url", ""),
                "video_id": video.get("video_id", ""),
                "status": video.get("status", ""),
                "origin_iterator_url": video.get("origin_iterator_url", ""),
            }
            for video in self._videos.values()
            if (iterator_url is None or video.get("origin_iterator_url") == iterator_url)
            and self.status_bucket(video.get("status")) == "failed"
        ]

    @staticmethod
    def status_bucket(status: str | None) -> str:
        normalized = (status or "").strip().lower()
        if normalized in {"complete", "completed", "downloaded", "finished", "success", "successful"}:
            return "successful"
        if normalized in {"error", "failed", "failure"} or "fail" in normalized or "error" in normalized:
            return "failed"
        return "other"

    def get_dashboard_stats(self) -> dict[str, Any]:
        totals = {"successful": 0, "failed": 0, "other": 0}
        sources: dict[str, dict[str, Any]] = {}
        total_size = 0.0
        last_downloaded = ""
        iterator_names = {
            record.get("id", ""): record.get("name", "Unknown Source")
            for record in self._iterators.values()
        }
        for video in self._videos.values():
            bucket = self.status_bucket(video.get("status"))
            totals[bucket] += 1
            total_size += float(video.get("file_size_mb") or 0)
            last_downloaded = max(last_downloaded, str(video.get("downloaded_at") or ""))
            name = iterator_names.get(video.get("origin_iterator", ""), "Direct downloads")
            source = sources.setdefault(
                name, {"name": name, "total": 0, "successful": 0, "failed": 0, "other": 0}
            )
            source["total"] += 1
            source[bucket] += 1
        total = sum(totals.values())
        downloaded = totals["successful"] + totals["failed"]
        return {
            "enabled": self.enabled,
            "total": total,
            **totals,
            "successRate": round((totals["successful"] / downloaded) * 100) if downloaded else 0,
            "totalSizeMb": round(total_size, 1),
            "lastDownloaded": last_downloaded,
            "sources": sorted(sources.values(), key=lambda source: source["total"], reverse=True),
        }

    async def _import_legacy_sqlite(self) -> None:
        if self._service is None or self.legacy_sqlite_path is None:
            return
        legacy_path = self.legacy_sqlite_path
        marker = self._service.data_directory / ".sqlite_import_complete"
        if marker.exists() or not legacy_path.is_file():
            return
        origins, videos = await asyncio.to_thread(_read_legacy_sqlite, legacy_path)
        client = await self._ensure_client()
        origin_records: dict[str, dict[str, Any]] = {}
        for origin in origins:
            record = await client.find_by_url(ORIGIN_COLLECTION, origin["url"])
            if record is None:
                record = await client.create_record(ORIGIN_COLLECTION, origin)
            origin_records[origin["url"]] = record
        for video in videos:
            origin = origin_records.get(video.get("origin_iterator_url") or "")
            video["origin_iterator"] = origin["id"] if origin else ""
            existing = await client.find_by_url(VIDEO_COLLECTION, video["url"])
            if existing:
                await client.update_record(VIDEO_COLLECTION, existing["id"], video)
            else:
                await client.create_record(VIDEO_COLLECTION, video)
        await asyncio.to_thread(
            marker.write_text, f"Imported {len(videos)} records from {legacy_path}\n", "utf-8"
        )
        logger.info("Imported %d legacy SQLite video records into PocketBase", len(videos))

    async def close(self) -> None:
        tasks = [
            task for task in self._tasks
            if task is not asyncio.current_task() and not task.done()
        ]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        if self._service is not None:
            await self._service.stop()
