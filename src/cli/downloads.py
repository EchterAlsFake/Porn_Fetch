"""Shared async download dispatch, progress conversion and gallery support."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
import hashlib
import inspect
from pathlib import Path
import re
from typing import Any, Callable
from urllib.parse import urlparse

from src.backend.media import select_allowed_quality
from .paths import data_dir
from .settings import CliSettings


ProgressCallback = Callable[..., None]
KNOWN_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


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
        # Some RAW providers do not expose a quality list until download starts.
        selected = "best" if has_premium else "720"

    configuration_quality: str | int = selected
    module = type(video).__module__.split(".", 1)[0]
    if module == "xfreehd_api":
        text_quality = str(selected).casefold()
        try:
            configuration_quality = "hd" if int(text_quality.removesuffix("p")) >= 720 else "sd"
        except ValueError:
            configuration_quality = "sd" if text_quality == "worst" else "hd"

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
        key = hashlib.sha256(str(target).encode()).hexdigest()[:20]
        resume = data_dir() / "resume"
        (resume / "states").mkdir(parents=True, exist_ok=True)
        (resume / "segments").mkdir(parents=True, exist_ok=True)
        hls_config = DownloadConfigHLS(
            quality=configuration_quality, path=target, callback=make_callback("segments"),
            callback_remux=make_callback("segments"),
            no_title=True, stop_event=event, remux=_has_av(),
            segment_state_path=str(resume / "states" / key),
            segment_dir=str(resume / "segments" / key), return_report=True,
            cleanup_on_stop=False, keep_segment_dir=True,
        )
        if module == "youporn_api":
            result = await video.download(hls_config, backup_configuration=raw_config)
        else:
            result = await video.download(hls_config)

    status_value = getattr(result, "status", None)
    missing = tuple(getattr(result, "missing", None) or ())
    if event.is_set() or status_value == "cancelled":
        status = "cancelled"
    elif result is False or status_value == "missing":
        status = "failed"
    else:
        status = "completed"
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
) -> DownloadOutcome:
    await _load_album(album)
    urls = list(await album.get_all_images())
    title = _sanitize(str(getattr(album, "title", None) or "album"))
    directory = Path(output_root) / title
    directory.mkdir(parents=True, exist_ok=True)
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
    status = "cancelled" if event.is_set() else "completed"
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
