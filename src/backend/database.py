"""Optional PocketBase-backed download tracking and statistics."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import secrets
import shutil
import socket
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.backend.media import VideoObject

try:
    from PySide6.QtCore import QObject, Signal, Slot
    _HAS_PYSIDE = True
except ImportError:  # Pragma: no cover
    _HAS_PYSIDE = False
    class QObject:  # type: ignore
        def __init__(self, parent: Any = None): pass
    def Signal(*args: Any, **kwargs: Any) -> Any:  # type: ignore
        class _Signal:
            def emit(self, *a: Any, **k: Any) -> None: pass
            def connect(self, *a: Any, **k: Any) -> None: pass
        return _Signal()
    def Slot(*args: Any, **kwargs: Any) -> Any:  # type: ignore
        return lambda fn: fn

logger = logging.getLogger(__name__)

ORIGIN_COLLECTION = "origin_iterators"
VIDEO_COLLECTION = "video_records"
SUPERUSER_EMAIL = "porn-fetch@localhost.invalid"
MIGRATION_NAME = "202608280000_create_download_tracking.js"

_SCHEMA_MIGRATION = r'''
migrate((app) => {
    const origins = new Collection({
        id: "pf_origins_0001",
        type: "base",
        name: "origin_iterators",
        fields: [
            { type: "text", name: "url", required: true },
            { type: "text", name: "name", required: true },
        ],
        indexes: [
            "CREATE UNIQUE INDEX idx_origin_iterators_url ON origin_iterators (url)",
        ],
    })
    app.save(origins)

    const videos = new Collection({
        id: "pf_videos__0001",
        type: "base",
        name: "video_records",
        fields: [
            { type: "text", name: "url", required: true },
            { type: "text", name: "title" },
            { type: "text", name: "video_id" },
            { type: "text", name: "author" },
            { type: "text", name: "length" },
            { type: "text", name: "thumbnail_url" },
            { type: "date", name: "publish_date" },
            { type: "text", name: "status" },
            { type: "json", name: "tags" },
            { type: "json", name: "qualities" },
            { type: "text", name: "identifier" },
            { type: "text", name: "output_path" },
            { type: "text", name: "selected_quality" },
            { type: "number", name: "file_size_mb" },
            { type: "date", name: "downloaded_at" },
            { type: "bool", name: "is_hls" },
            { type: "json", name: "missing_segments" },
            { type: "bool", name: "is_from_account" },
            { type: "text", name: "origin_iterator_url" },
            {
                type: "relation",
                name: "origin_iterator",
                collectionId: "pf_origins_0001",
                cascadeDelete: false,
                maxSelect: 1,
            },
        ],
        indexes: [
            "CREATE UNIQUE INDEX idx_video_records_url ON video_records (url)",
            "CREATE INDEX idx_video_records_status ON video_records (status)",
            "CREATE INDEX idx_video_records_origin ON video_records (origin_iterator)",
        ],
    })
    app.save(videos)
}, (app) => {
    app.delete(app.findCollectionByNameOrId("video_records"))
    app.delete(app.findCollectionByNameOrId("origin_iterators"))
})
'''.lstrip()


def _find_original_executable() -> Path | None:
    """Returns the true executable path without pulling in GUI widgets."""
    try:
        import __compiled__
        orig = getattr(__compiled__, "original_argv0", None)
        if orig and Path(orig).exists():
            return Path(orig).resolve()
    except (ImportError, Exception):
        pass
    if appimage := os.environ.get("APPIMAGE"):
        if Path(appimage).exists():
            return Path(appimage).resolve()
    if sys.argv and Path(sys.argv[0]).exists():
        return Path(sys.argv[0]).resolve()
    return None


class PocketBaseError(RuntimeError):
    """Raised when the embedded PocketBase service or API request fails."""


class PocketBaseClient:
    """Small async client for the PocketBase endpoints used by this application."""

    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token = ""

    async def authenticate(self, email: str, password: str) -> None:
        response = await self.request(
            "POST",
            "/api/collections/_superusers/auth-with-password",
            {"identity": email, "password": password},
            authenticated=False,
        )
        self.token = str(response["token"])

    async def request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        *,
        query: dict[str, Any] | None = None,
        authenticated: bool = True,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self._request_sync, method, path, body, query, authenticated
        )

    def _request_sync(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
        query: dict[str, Any] | None,
        authenticated: bool,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        encoded_body = None
        headers = {"Accept": "application/json"}
        if body is not None:
            encoded_body = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if authenticated and self.token:
            headers["Authorization"] = self.token

        request = Request(url, data=encoded_body, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read()
        except HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")
            raise PocketBaseError(
                f"PocketBase returned HTTP {error.code} for {method} {path}: {details}"
            ) from error
        except (OSError, URLError) as error:
            raise PocketBaseError(f"PocketBase request failed for {method} {path}: {error}") from error
        if not payload:
            return {}
        try:
            return json.loads(payload)
        except json.JSONDecodeError as error:
            raise PocketBaseError(f"PocketBase returned invalid JSON for {method} {path}") from error

    async def list_records(
        self, collection: str, *, filter_expression: str = "", sort: str = ""
    ) -> list[dict[str, Any]]:
        page = 1
        records: list[dict[str, Any]] = []
        while True:
            query: dict[str, Any] = {"page": page, "perPage": 500}
            if filter_expression:
                query["filter"] = filter_expression
            if sort:
                query["sort"] = sort
            response = await self.request(
                "GET", f"/api/collections/{collection}/records", query=query
            )
            records.extend(response.get("items", []))
            if page >= int(response.get("totalPages", 1)):
                return records
            page += 1

    async def find_by_url(self, collection: str, url: str) -> dict[str, Any] | None:
        quoted_url = json.dumps(url, ensure_ascii=False)
        records = await self.list_records(collection, filter_expression=f"url = {quoted_url}")
        return records[0] if records else None

    async def create_record(self, collection: str, data: dict[str, Any]) -> dict[str, Any]:
        return await self.request("POST", f"/api/collections/{collection}/records", data)

    async def update_record(
        self, collection: str, record_id: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        return await self.request(
            "PATCH", f"/api/collections/{collection}/records/{record_id}", data
        )


class PocketBaseService:
    """Owns the bundled PocketBase child process and its authenticated client."""

    def __init__(self, data_directory: str | Path, binary_path: str | Path | None = None):
        self.data_directory = Path(data_directory).expanduser().resolve()
        self.binary_path = Path(binary_path).expanduser().resolve() if binary_path else None
        self.migrations_directory = self.data_directory / "_porn_fetch_migrations"
        self.process: subprocess.Popen[bytes] | None = None
        self.client: PocketBaseClient | None = None

    def find_binary(self, custom_path: str | Path | None = None) -> Path:
        target_path = custom_path or self.binary_path
        if target_path:
            p = Path(target_path).expanduser()
            if p.is_file() and (sys.platform == "win32" or os.access(p, os.X_OK)):
                return p.resolve()
        name = "pocketbase.exe" if sys.platform == "win32" else "pocketbase"
        candidates: list[Path] = []
        if configured := os.environ.get("PORN_FETCH_POCKETBASE_BINARY"):
            candidates.append(Path(configured).expanduser())
        orig = _find_original_executable()
        if orig is not None:
            candidates.append(orig.parent / name)
        project_root = Path(__file__).resolve().parents[2]
        candidates.extend([
            project_root / name,
            project_root / "src" / "build" / "pocketbase" / name,
            project_root / "src" / "build" / "pocketbase" / sys.platform / name,
        ])
        if installed := shutil.which("pocketbase"):
            candidates.append(Path(installed))
        for candidate in candidates:
            if candidate.is_file() and (sys.platform == "win32" or os.access(candidate, os.X_OK)):
                return candidate.resolve()
        searched = ", ".join(str(path) for path in candidates)
        raise PocketBaseError(
            "PocketBase tracking is enabled, but the PocketBase binary was not found. "
            "Place it beside the Porn Fetch executable, install it on PATH, or set "
            f"PORN_FETCH_POCKETBASE_BINARY. Searched: {searched}"
        )

    async def start(self) -> PocketBaseClient:
        if self.client is not None:
            return self.client
        if self.data_directory.exists() and not self.data_directory.is_dir():
            raise PocketBaseError(f"PocketBase data path is not a directory: {self.data_directory}")
        self.migrations_directory.mkdir(parents=True, exist_ok=True)
        migration_path = self.migrations_directory / MIGRATION_NAME
        await asyncio.to_thread(migration_path.write_text, _SCHEMA_MIGRATION, "utf-8")

        binary = self.find_binary()
        password = secrets.token_urlsafe(32)
        flags = [
            f"--dir={self.data_directory}",
            f"--migrationsDir={self.migrations_directory}",
        ]
        await self._run_command(
            binary, "superuser", "upsert", SUPERUSER_EMAIL, password, *flags
        )

        port = self._reserve_port()
        self.process = await asyncio.to_thread(
            self._spawn_server,
            binary,
            port,
            flags,
        )
        client = PocketBaseClient(f"http://127.0.0.1:{port}")
        try:
            await self._wait_until_healthy(client)
            await client.authenticate(SUPERUSER_EMAIL, password)
        except Exception:
            await self.stop()
            raise
        self.client = client
        return client

    async def _run_command(self, binary: Path, *arguments: str) -> None:
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                [str(binary), *arguments],
                cwd=str(binary.parent),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=15,
                check=False,
                creationflags=creation_flags,
            )
        except subprocess.TimeoutExpired:
            raise PocketBaseError(f"PocketBase command timed out: {' '.join(arguments[:2])}")
        if result.returncode:
            details = result.stdout.decode("utf-8", errors="replace").strip()
            raise PocketBaseError(
                f"PocketBase command failed ({' '.join(arguments[:2])}): {details}"
            )

    @staticmethod
    def _spawn_server(binary: Path, port: int, flags: list[str]) -> subprocess.Popen[bytes]:
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        return subprocess.Popen(
            [str(binary), "serve", f"--http=127.0.0.1:{port}", "--automigrate=false", *flags],
            cwd=str(binary.parent),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags,
        )

    @staticmethod
    def _reserve_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])

    async def _wait_until_healthy(self, client: PocketBaseClient) -> None:
        for _ in range(50):
            if self.process is not None and self.process.poll() is not None:
                raise PocketBaseError(
                    f"PocketBase exited during startup with code {self.process.returncode}"
                )
            try:
                await client.request("GET", "/api/health", authenticated=False)
                return
            except PocketBaseError:
                await asyncio.sleep(0.1)
        raise PocketBaseError("PocketBase did not become healthy within 5 seconds")

    async def stop(self) -> None:
        self.client = None
        process, self.process = self.process, None
        if process is None or process.poll() is not None:
            return
        process.terminate()
        try:
            await asyncio.to_thread(process.wait, 5)
        except subprocess.TimeoutExpired:
            process.kill()
            await asyncio.to_thread(process.wait)


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


class DatabaseBridge(QObject):
    """QML bridge for asynchronously persisted PocketBase tracking data."""

    iteratorsChanged = Signal()
    statisticsChanged = Signal()
    downloadSaved = Signal(str)
    initializationFailed = Signal(str)

    def __init__(self, parent: QObject | None = None, tracker: PocketBaseTracker | None = None):
        super().__init__(parent)
        if tracker is not None:
            self._tracker = tracker
        else:
            try:
                from src.backend.config import app_settings
                enabled = bool(app_settings.track_videos)
                data_path = app_settings.pocketbase_data_path
                legacy_path = app_settings.legacy_database_path
            except ImportError:
                enabled = False
                data_path = "./pocketbase_data"
                legacy_path = "./downloads.db"
            self._tracker = PocketBaseTracker(
                data_path=data_path,
                enabled=enabled,
                legacy_sqlite_path=legacy_path,
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
        """Start PocketBase after the QtAsyncio event loop is running."""
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


def _format_date(value: Any) -> str:
    if not value:
        return ""
    if isinstance(value, datetime):
        if value.tzinfo:
            return value.astimezone().isoformat(timespec="milliseconds")
        return value.isoformat(timespec="milliseconds")
    return str(value)


def _load_json(value: Any) -> Any:
    if value in (None, ""):
        return []
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []
    return value


def _read_legacy_sqlite(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Read the previous Peewee database without retaining Peewee as a dependency."""
    with sqlite3.connect(f"file:{path}?mode=ro", uri=True) as connection:
        connection.row_factory = sqlite3.Row
        tables = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        if not {"originiterator", "videorecord"}.issubset(tables):
            return [], []
        origins = [dict(row) for row in connection.execute("SELECT url, name FROM originiterator")]
        raw_videos = [dict(row) for row in connection.execute("SELECT * FROM videorecord")]
    videos = []
    for record in raw_videos:
        videos.append({
            "url": record.get("url") or "",
            "title": record.get("title") or "",
            "video_id": record.get("video_id") or "",
            "author": record.get("author") or "",
            "length": record.get("length") or "",
            "thumbnail_url": record.get("thumbnail_url") or "",
            "publish_date": record.get("publish_date") or "",
            "status": record.get("status") or "",
            "tags": _load_json(record.get("tags_json")),
            "qualities": _load_json(record.get("qualities_json")),
            "identifier": record.get("identifier") or "",
            "output_path": record.get("output_path") or "",
            "selected_quality": record.get("selected_quality") or "",
            "file_size_mb": float(record.get("file_size_mb") or 0),
            "downloaded_at": record.get("downloaded_at") or "",
            "is_hls": bool(record.get("is_hls")),
            "missing_segments": _load_json(record.get("missing_segments")),
            "is_from_account": bool(record.get("is_from_account")),
            "origin_iterator_url": record.get("origin_iterator_url") or "",
        })
    return origins, videos
