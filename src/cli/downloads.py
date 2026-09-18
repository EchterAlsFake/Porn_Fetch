"""Shared async download dispatch, progress conversion and gallery support."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import hashlib
import inspect
import json
from pathlib import Path
import re
import shutil
from typing import Any, Callable
from urllib.parse import urlparse

from src.backend.media import select_allowed_quality
from .paths import data_dir
from .settings import CliSettings


ProgressCallback = Callable[..., None]
KNOWN_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


class DownloadState(StrEnum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILED = "failed"


def get_resume_paths(target: str | Path) -> tuple[Path, Path]:
    """Return the (state_path, segment_dir) for HLS segment persistence."""
    key = hashlib.sha256(str(Path(target).resolve()).encode()).hexdigest()[:20]
    resume = data_dir() / "resume"
    state_path = resume / "states" / key
    segment_dir = resume / "segments" / key
    return state_path, segment_dir


def has_resume_state(target: str | Path) -> bool:
    """Return whether partial segments or state file exist for *target*."""
    state_path, segment_dir = get_resume_paths(target)
    if state_path.exists():
        return True
    if segment_dir.exists() and any(segment_dir.iterdir()):
        return True
    return False


def clear_resume_state(target: str | Path) -> None:
    """Purge temporary HLS resume files and segment directories for *target*."""
    state_path, segment_dir = get_resume_paths(target)
    if state_path.exists():
        try:
            state_path.unlink()
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
        try:
            resolved = str(Path(url_or_target).resolve())
        except Exception:
            resolved = val
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
            except OSError:
                pass


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
    ) -> None:
        self.url = url
        self.target = Path(target) if target else None
        self.title = title or ""
        self.quality = quality
        self.kind = kind
        self.provider = provider
        self.on_state_change = on_state_change

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
            PausedStore().add(
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
            if cleanup:
                clear_resume_state(self.target)
                if self.target.exists() and not self.target.is_dir():
                    try:
                        self.target.unlink()
                    except OSError:
                        pass
            PausedStore().remove(self.target)
        if self.url:
            PausedStore().remove(self.url)

    def resume(self) -> None:
        """Reset the stop event to allow downloading to resume."""
        self._stop_event = asyncio.Event()
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
) -> DownloadOutcome:
    """Dispatch RAW/HLS downloads and enforce licensing at dispatch time."""
    from base_api import DownloadConfigHLS, DownloadConfigRAW

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and settings.skip_existing:
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
        text_quality = str(selected).casefold()
        try:
            configuration_quality = "hd" if int(text_quality.removesuffix("p")) >= 720 else "sd"
        except ValueError:
            configuration_quality = "sd" if text_quality == "worst" else "hd"

    if controller is not None:
        controller.target = target
        controller.quality = selected
        event = controller.stop_event
        controller.set_state(DownloadState.DOWNLOADING)
    else:
        event = stop_event or asyncio.Event()

    loop = asyncio.get_running_loop()
    raw = module in {"eporner_api", "porntrex_api", "xfreehd_api"}

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
    if raw:
        result = await video.download(raw_config, mode="h264") if module == "eporner_api" else await video.download(raw_config)
    else:
        state_path, segment_dir = get_resume_paths(target)
        state_path.parent.mkdir(parents=True, exist_ok=True)
        segment_dir.mkdir(parents=True, exist_ok=True)
        hls_config = DownloadConfigHLS(
            quality=configuration_quality, path=target, callback=make_callback("segments"),
            callback_remux=make_callback("segments"),
            no_title=True, stop_event=event, remux=_has_av(),
            segment_state_path=str(state_path),
            segment_dir=str(segment_dir), return_report=True,
            cleanup_on_stop=False, keep_segment_dir=True,
        )
        if module == "youporn_api":
            result = await video.download(hls_config, backup_configuration=raw_config)
        else:
            result = await video.download(hls_config)

    status_value = getattr(result, "status", None)
    missing = tuple(getattr(result, "missing", None) or ())

    if (controller and controller.is_paused) or (event.is_set() and controller and controller.is_paused):
        status = "paused"
        if controller:
            controller.set_state(DownloadState.PAUSED)
    elif event.is_set() or status_value == "cancelled":
        status = "cancelled"
        if controller:
            controller.set_state(DownloadState.CANCELLED)
            if getattr(controller, "cleanup_on_cancel", False):
                clear_resume_state(target)
                if target.exists() and not target.is_dir():
                    try:
                        target.unlink()
                    except OSError:
                        pass
    elif result is False or status_value == "missing":
        status = "failed"
        if controller:
            controller.set_state(DownloadState.FAILED)
    else:
        status = "completed"
        if controller:
            controller.set_state(DownloadState.COMPLETED)
        clear_resume_state(target)
        PausedStore().remove(target)

    if status == "completed" and progress:
        _dispatch_progress(progress, 100, 100)
    return DownloadOutcome(status, target, missing)


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
    urls = list(await album.get_all_images())
    title = _sanitize(str(getattr(album, "title", None) or "album"))
    directory = Path(output_root) / title
    directory.mkdir(parents=True, exist_ok=True)

    if controller is not None:
        controller.target = directory
        controller.kind = "gallery"
        event = controller.stop_event
        controller.set_state(DownloadState.DOWNLOADING)
    else:
        event = stop_event or asyncio.Event()

    semaphore = asyncio.Semaphore(max(1, concurrency))
    completed = 0
    width = max(4, len(str(max(1, len(urls)))))

    async def fetch(index: int, url: str) -> None:
        nonlocal completed
        if event.is_set():
            return
        suffix = Path(urlparse(url).path).suffix.casefold()
        if suffix not in KNOWN_IMAGE_EXTENSIONS:
            suffix = ".jpg"
        destination = directory / f"{index:0{width}d}{suffix}"
        async with semaphore:
            if event.is_set():
                return
            if not destination.exists():
                content = await album.core.fetch_bytes(url)
                destination.write_bytes(content)
        completed += 1
        if progress:
            _dispatch_progress(progress, completed, len(urls))

    await asyncio.gather(*(fetch(index, url) for index, url in enumerate(urls, 1)))

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
    try:
        import av  # noqa: F401
        return True
    except ImportError:
        return False
