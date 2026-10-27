"""Shared async download dispatch, progress conversion and gallery support."""
from __future__ import annotations

import asyncio
import hashlib
import inspect
import json
import logging
import re
import shutil
from contextlib import aclosing
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from src.shared.media import select_allowed_quality, xfreehd_quality
from src.shared.paths import data_dir

from .concurrency import run_workers
from .settings import CliSettings

logger = logging.getLogger(__name__)


ProgressCallback = Callable[..., None]
KNOWN_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
RAW_VIDEO_MODULES = frozenset({"eporner_api", "porntrex_api", "xfreehd_api", "empflix_api", "tnaflix_api"})


class DownloadState(StrEnum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"


def get_resume_paths(target: str | Path, *, state_directory: Path | None = None) -> tuple[Path, Path]:
    """Return HLS persistence paths, optionally under an isolated state root."""
    key = hashlib.sha256(str(Path(target).resolve()).encode()).hexdigest()[:20]
    resume = (state_directory if state_directory is not None else data_dir()) / "resume"
    state_path = resume / "states" / key
    segment_dir = resume / "segments" / key
    return state_path, segment_dir


def has_resume_state(target: str | Path, *, state_directory: Path | None = None) -> bool:
    """Return whether HLS segments/state or a RAW checkpoint exist for *target*."""
    state_path, segment_dir = get_resume_paths(target, state_directory=state_directory)
    if state_path.exists():
        return True
    if Path(f"{target}.raw-state.json").exists():
        return True
    if segment_dir.exists() and any(segment_dir.iterdir()):
        return True
    return False


def clear_resume_state(target: str | Path, *, state_directory: Path | None = None) -> None:
    """Purge HLS/RAW resume state, segments and assembly temporary files."""
    state_path, segment_dir = get_resume_paths(target, state_directory=state_directory)
    raw_state = Path(f"{target}.raw-state.json")
    for temporary in (state_path, Path(f"{state_path}.tmp"), Path(f"{target}.tmp"),
                      raw_state, raw_state.with_name(raw_state.name + ".tmp")):
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
    if segment_dir.exists():
        try:
            shutil.rmtree(segment_dir, ignore_errors=True)
        except OSError:
            pass


class PausedStore:
    """Persist and track paused download jobs to allow later resumption."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (data_dir() / "paused_downloads.json")

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def save(self, items: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(items, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def add(
        self,
        url: str,
        target: str | Path,
        title: str,
        quality: str | int,
        kind: str = "video",
        provider: str = "",
    ) -> None:
        items = self.load()
        resolved = str(Path(target).resolve())
        items = [
            i for i in items
            if i.get("url") != url and str(Path(i.get("target", "")).resolve()) != resolved
        ]
        items.append({
            "url": url,
            "target": str(target),
            "title": title,
            "quality": str(quality),
            "kind": kind,
            "provider": provider,
            "paused_at": datetime.now(timezone.utc).isoformat(),
        })
        self.save(items)

    def remove(self, url_or_target: str | Path) -> None:
        items = self.load()
        val = str(url_or_target)
        resolved = str(Path(url_or_target).resolve())
        new_items = [
            i for i in items
            if i.get("url") != val and i.get("target") != val and str(Path(i.get("target", "")).resolve()) != resolved
        ]
        if len(new_items) != len(items):
            self.save(new_items)

    def clear(self) -> None:
        if self.path.exists():
            try:
                self.path.unlink()
            except OSError as error:
                logger.debug("Could not remove paused-download state %s: %s", self.path, error)


class DownloadController:
    """Provides thread-safe and async-safe pause, cancel, and resume controls."""

    def __init__(
        self,
        *,
        url: str | None = None,
        target: Path | str | None = None,
        title: str | None = None,
        quality: str | int | None = None,
        kind: str = "video",
        provider: str = "",
        on_state_change: Callable[[DownloadState], None] | None = None,
        state_directory: Path | None = None,
    ) -> None:
        self.url = url
        self.target = Path(target) if target else None
        self.title = title or ""
        self.quality = quality
        self.kind = kind
        self.provider = provider
        self.on_state_change = on_state_change
        self.state_directory = state_directory
        self.paused_store = PausedStore(
            state_directory / "paused_downloads.json" if state_directory is not None else None
        )
        self._download_running = False
        self.cleanup_on_cancel = False

        self._state: DownloadState = DownloadState.PENDING
        self._stop_event: asyncio.Event = asyncio.Event()

    @property
    def stop_event(self) -> asyncio.Event:
        return self._stop_event

    @property
    def state(self) -> DownloadState:
        return self._state

    @property
    def is_paused(self) -> bool:
        return self._state == DownloadState.PAUSED

    @property
    def is_cancelled(self) -> bool:
        return self._state == DownloadState.CANCELLED

    @property
    def is_active(self) -> bool:
        return self._state in (DownloadState.PENDING, DownloadState.DOWNLOADING)

    def set_state(self, new_state: DownloadState) -> None:
        if self._state != new_state:
            self._state = new_state
            if self.on_state_change:
                self.on_state_change(new_state)

    def pause(self) -> None:
        """Pause downloading. The partial segments/data are preserved."""
        self.set_state(DownloadState.PAUSED)
        self._stop_event.set()
        if self.url and self.target:
            self.paused_store.add(
                url=self.url,
                target=self.target,
                title=self.title or self.target.name,
                quality=self.quality or "best",
                kind=self.kind,
                provider=self.provider,
            )

    def cancel(self, cleanup: bool = False) -> None:
        """Cancel downloading. Optionally clean up partially downloaded segments."""
        self.cleanup_on_cancel = cleanup
        self.set_state(DownloadState.CANCELLED)
        self._stop_event.set()
        if self.target:
            # Active writers must finish before their files can be removed.
            if cleanup and not self._download_running:
                clear_resume_state(self.target, state_directory=self.state_directory)
                if self.target.exists() and not self.target.is_dir():
                    try:
                        self.target.unlink()
                    except OSError:
                        pass
            self.paused_store.remove(self.target)
        if self.url:
            self.paused_store.remove(self.url)

    def resume(self) -> None:
        """Reset the stop event to allow downloading to resume."""
        self._stop_event = asyncio.Event()
        self.cleanup_on_cancel = False
        self.set_state(DownloadState.DOWNLOADING)


def _dispatch_progress(
    cb: Callable[..., None] | None,
    position: int,
    total: int,
    unit: str = "items",
) -> None:
    if not cb:
        return
    try:
        sig = inspect.signature(cb)
        params = len(sig.parameters)
    except (ValueError, TypeError):
        params = 1
    if params >= 3:
        cb(position, total, unit)
    elif params >= 2:
        cb(position, total)
    else:
        cb(progress_percentage(position, total))


@dataclass(frozen=True, slots=True)
class DownloadOutcome:
    status: str
    path: Path
    missing_segments: tuple[int, ...] = ()
    skipped: bool = False
    metadata_written: bool = False


def progress_percentage(position: int, total: int) -> int | None:
    if total <= 0:
        return None
    return max(0, min(100, int(position * 100 / total)))


async def download_video(
    video: Any,
    path: str | Path,
    quality: str | int,
    settings: CliSettings,
    *,
    has_premium: bool,
    stop_event: asyncio.Event | None = None,
    progress: ProgressCallback | None = None,
    available_qualities: list[str | int] | None = None,
    controller: DownloadController | None = None,
    metadata: Any = None,
) -> DownloadOutcome:
    """Dispatch RAW/HLS downloads and enforce licensing at dispatch time."""
    from base_api import DownloadConfigHLS, DownloadConfigRAW
    from base_api.modules.errors import DownloadCancelled

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    state_directory = controller.state_directory if controller else None
    paused_store = controller.paused_store if controller else PausedStore()
    resuming = has_resume_state(target, state_directory=state_directory) or any(
        item.get("target") and Path(item["target"]).resolve() == target.resolve()
        for item in paused_store.load()
    )
    if target.exists() and settings.skip_existing and not resuming:
        if progress:
            progress(100)
        return DownloadOutcome("completed", target, skipped=True)

    available: Any = available_qualities
    if available is None:
        available = getattr(video, "available_qualities", None)
        if callable(available):
            available = available()
        if not available:
            fallback = getattr(video, "video_qualities", [])
            available = fallback() if callable(fallback) else fallback
    available = list(available or [])
    selected = select_allowed_quality(quality, available, has_premium)
    if not selected:
        selected = str(quality) if has_premium else select_allowed_quality("720", available, False)
    if not selected:
        selected = "best" if has_premium else "720"

    configuration_quality: str | int = selected
    module = type(video).__module__.split(".", 1)[0]
    if module == "xfreehd_api":
        configuration_quality = xfreehd_quality(selected)

    if controller is not None:
        controller.target = target
        controller.quality = selected
        event = controller.stop_event
        controller.set_state(DownloadState.DOWNLOADING)
    else:
        event = stop_event or asyncio.Event()

    loop = asyncio.get_running_loop()
    raw = module in RAW_VIDEO_MODULES

    def make_callback(unit: str) -> Callable[[int, int], None]:
        def callback(position: int, total: int) -> None:
            if progress:
                loop.call_soon_threadsafe(_dispatch_progress, progress, position, total, unit)

        return callback

    raw_config = DownloadConfigRAW(
        quality=configuration_quality, path=target, callback=make_callback("bytes"), no_title=True,
        stop_event=event, max_workers=settings.download_workers,
        read_timeout=float(settings.timeout), max_retries=settings.request_attempts,
    )
    if not raw:
        state_path, segment_dir = get_resume_paths(target, state_directory=state_directory)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        segment_dir.mkdir(parents=True, exist_ok=True)
        can_remux = _has_av()
        hls_config = DownloadConfigHLS(
            quality=configuration_quality, path=target, callback=make_callback("segments"),
            callback_remux=make_callback("segments"),
            no_title=True, stop_event=event, remux=can_remux,
            metadata=metadata if (settings.write_metadata and can_remux) else None,
            segment_state_path=str(state_path),
            segment_dir=str(segment_dir), return_report=True,
            cleanup_on_stop=False, keep_segment_dir=True,
        )
    if controller:
        controller._download_running = True
    try:
        if raw:
            result = await video.download(raw_config, mode="h264") if module == "eporner_api" else await video.download(raw_config)
        elif module == "youporn_api":
            result = await video.download(hls_config, backup_configuration=raw_config)
        else:
            result = await video.download(hls_config)
    except DownloadCancelled:
        if not event.is_set():
            raise
        # RAW providers raise on cooperative stop; HLS can return a report.
        result = None
    finally:
        if controller:
            controller._download_running = False
            if event.is_set() and controller.cleanup_on_cancel:
                clear_resume_state(target, state_directory=state_directory)
                target.unlink(missing_ok=True)

    status_value = getattr(result, "status", None)
    missing = tuple(getattr(result, "missing", None) or ())
    metadata_written = bool(getattr(result, "metadata_written", False))

    if (controller and controller.is_paused) or (event.is_set() and controller and controller.is_paused):
        status = "paused"
        if controller:
            controller.set_state(DownloadState.PAUSED)
    elif event.is_set() or status_value == "cancelled":
        status = "cancelled"
        if controller:
            controller.set_state(DownloadState.CANCELLED)
    elif result is False or status_value in {"missing", "failed"}:
        status = "failed"
        if controller:
            controller.set_state(DownloadState.FAILED)
    else:
        status = "completed"
        if controller:
            controller.set_state(DownloadState.COMPLETED)
        clear_resume_state(target, state_directory=state_directory)
        paused_store.remove(target)

    if status == "completed" and progress:
        _dispatch_progress(progress, 100, 100)
    return DownloadOutcome(status, target, missing, metadata_written=metadata_written)


async def download_gallery(
    album: Any,
    output_root: str | Path,
    *,
    stop_event: asyncio.Event | None = None,
    progress: ProgressCallback | None = None,
    concurrency: int = 5,
    controller: DownloadController | None = None,
) -> DownloadOutcome:
    await _load_album(album)
    fallback_title = "album-" + Path(urlparse(getattr(album, "url", "")).path).name
    title = _sanitize(str(getattr(album, "title", None) or fallback_title))
    directory = Path(output_root) / title
    directory.mkdir(parents=True, exist_ok=True)

    if controller is not None:
        controller.target = directory
        controller.kind = "gallery"
        event = controller.stop_event
        controller.set_state(DownloadState.DOWNLOADING)
    else:
        event = stop_event or asyncio.Event()

    completed = 0
    discovered = 0
    discovery_done = False

    async def images():
        nonlocal discovered, discovery_done
        if hasattr(album, "get_photos"):
            pages = int(getattr(album, "total_pages", None) or 1)
            async with aclosing(album.get_photos(pages=pages)) as photos:
                async for photo in photos:
                    if event.is_set():
                        break
                    if url := photo.get("download_url"):
                        discovered += 1
                        yield discovered, url
        else:
            urls = await album.get_all_images()
            for index, url in enumerate(urls, 1):
                if event.is_set():
                    break
                discovered = index
                yield index, url
        discovery_done = True

    async def fetch(item: tuple[int, str]) -> None:
        nonlocal completed
        index, url = item
        if event.is_set():
            return
        suffix = Path(urlparse(url).path).suffix.casefold()
        if suffix not in KNOWN_IMAGE_EXTENSIONS:
            suffix = ".jpg"
        destination = directory / f"{index:04d}{suffix}"
        if not destination.exists():
            content = await album.core.fetch_bytes(url)
            if event.is_set():
                return
            destination.write_bytes(content)
        completed += 1
        if progress:
            _dispatch_progress(progress, completed, discovered if discovery_done else 0)

    await run_workers(images(), fetch, concurrency)
    if not discovered and not event.is_set():
        raise ValueError("No downloadable images were found in this album")
    if progress and not event.is_set():
        _dispatch_progress(progress, completed, discovered)

    if (controller and controller.is_paused) or (event.is_set() and controller and controller.is_paused):
        status = "paused"
        if controller:
            controller.set_state(DownloadState.PAUSED)
    elif event.is_set():
        status = "cancelled"
        if controller:
            controller.set_state(DownloadState.CANCELLED)
    else:
        status = "completed"
        if controller:
            controller.set_state(DownloadState.COMPLETED)
        PausedStore().remove(directory)

    return DownloadOutcome(status, directory)


async def _load_album(album: Any) -> None:
    loaders = getattr(album, "loader_methods", {}) or {}
    if "html" in loaders:
        await album.load_sources("html")


def _sanitize(value: str) -> str:
    return re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", value).strip(" .") or "album"


def _has_av() -> bool:
    from src.shared.ffmpeg import has_ffmpeg

    return has_ffmpeg()
