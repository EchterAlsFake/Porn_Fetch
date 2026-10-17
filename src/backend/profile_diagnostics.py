"""Opt-in live profile diagnostics through the real GUI preparation pipeline."""
from __future__ import annotations

import asyncio
import json
import re
import tempfile
from contextlib import ExitStack, contextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest import SkipTest
from unittest.mock import patch
from urllib.parse import urlsplit

from base_api import BaseCore, ErrorMode, make_iterator_config
from PySide6.QtTest import QSignalSpy

from src.shared.media import VideoFilters
from src.shared.provider_routing import ContentKind, resolve_container, route_url


def fixture_path() -> Path:
    bundled = Path(__file__).with_name("profile_fixtures.json")
    return bundled if bundled.exists() else Path(__file__).resolve().parents[2] / "docs/url-routing-audit/profile-fixtures.json"


class ProfileFeedUnavailable(SkipTest):
    """A public identity exists, but its video feed is not publicly exposed."""

    def __init__(self, message: str, metadata: dict):
        super().__init__(message)
        self.metadata = metadata


def load_profile_cases(*, include_variants: bool = False, pattern: str = "") -> list[dict]:
    cases = json.loads(fixture_path().read_text(encoding="utf-8"))["cases"]
    selected, seen = [], set()
    for case in cases:
        if not case["positive_smoke_candidate"]:
            continue
        if not include_variants and case["tier"] != "primary":
            continue
        if pattern and pattern.casefold() not in f"{case['id']} {case['url']}".casefold():
            continue
        if case["url"] in seen:
            continue
        seen.add(case["url"])
        selected.append(case)
    if not selected:
        raise ValueError("No positive profile fixtures match this selection")
    return selected


class MetadataOnlyRequests:
    """Block download entry points and video/segment GETs during diagnostics."""

    def __init__(self):
        self.blocked: list[str] = []
        self.requests = 0
        self._stack = ExitStack()

    def reject(self, operation):
        self.blocked.append(operation)
        raise AssertionError(f"Media download attempted during metadata-only diagnostics: {operation}")

    def __enter__(self):
        original = BaseCore.request
        guard = self

        async def request(core, url, *args, **kwargs):
            path = urlsplit(url).path.lower()
            if kwargs.get("method", "GET").upper() != "HEAD" and not path.endswith(".m3u8") and re.search(
                r"\.(?:mp4|m4s|ts|m2ts|webm|mkv|mov|flv|aac|mp3)(?:/|$)", path,
            ):
                guard.reject("media/segment GET")
            guard.requests += 1
            return await original(core, url, *args, **kwargs)

        self._stack.enter_context(patch.object(BaseCore, "request", request))
        for name in (
            "download", "download_segment", "threaded_download", "_threaded_download",
            "legacy_download", "_legacy_download", "fetch_bytes",
        ):
            async def forbidden(*args, operation=name, **kwargs):
                guard.reject(operation)
            self._stack.enter_context(patch.object(BaseCore, name, forbidden))
        return self

    def __exit__(self, *error):
        return self._stack.__exit__(*error)


@contextmanager
def diagnostic_settings(*, items: int = 2):
    """Bound work without writing test settings into the user's QSettings."""
    from src.backend import application, clients, download_manager, video_processor

    class Overlay:
        def __init__(self, source, overrides):
            self.source, self.overrides = source, overrides

        def __getattr__(self, name):
            return self.overrides[name] if name in self.overrides else getattr(self.source, name)

    with tempfile.TemporaryDirectory(prefix="porn-fetch-profile-test-") as directory, ExitStack() as stack:
        for module in (application, clients, download_manager, video_processor):
            stack.enter_context(patch.object(module, "app_settings", Overlay(module.app_settings, {
                "result_limit": items, "output_path": directory, "retries": 1,
                "model_videos": 2, "enable_logging": False,
            })))
        yield Path(directory)


def _http_url(value) -> bool:
    return isinstance(value, str) and urlsplit(value).scheme in {"http", "https"} and bool(urlsplit(value).hostname)


async def verify_stream(source, quality: str | int) -> dict:
    """Resolve URLs only. In particular, never GET an MP4 or HLS segment."""
    from src.backend import clients

    master = clients._safe_getattr(source, "m3u8_base_url")
    if isinstance(source, clients.yp_Video) and source.is_hls is False:
        url = master  # This provider stores its MP4 fallback in the same field.
    elif master:
        segments = await source.core.get_segments(master, quality)
        if not segments or not all(_http_url(url) for url in segments):
            raise AssertionError("HLS playlist did not resolve to a nonempty list of absolute segment URLs")
        return {"kind": "hls", "segments": len(segments)}
    else:
        url = await clients.get_direct_url_legacy(source, quality)
    if not _http_url(url):
        raise AssertionError("Direct-file metadata did not contain a usable HTTP(S) stream URL")
    return {"kind": "direct", "url_resolved": True}


async def test_profile_url(backend, model, case: dict, *, timeout: float = 90, items: int = 2) -> dict:
    from src.backend import clients

    async def check():
        route = route_url(case["url"])
        if route.provider != case["provider"] or route.kind != ContentKind.PROFILE:
            raise AssertionError(f"Wrong provider/content route: {route}")
        target = await resolve_container(clients.client_for(route.provider), route, pages=1)
        name = getattr(target, "name", None)
        profile_metadata = {}
        if route.provider == "xnxx" and name is None:
            # XNXX's public User schema exposes counts, but no name field.
            for field in ("total_videos_count", "total_pages_count"):
                value = getattr(target, field)
                if not isinstance(value, int) or value <= 0:
                    raise AssertionError(f"Profile has no positive {field}")
                profile_metadata[field] = value
            name = backend._iterator_display_name(target, case["url"], "model / channel")
        elif not isinstance(name, str) or name.strip().casefold() in {"", "unknown", "n/a"}:
            raise AssertionError("The profile did not load a meaningful name")
        expected = case.get("expected_factory")
        if expected and type(target).__name__.casefold() != expected.removeprefix("get_"):
            raise AssertionError(f"Expected {expected}, got {type(target).__name__}")
        before = model.rowCount()
        inserted = QSignalSpy(model.rowsInserted)
        errors = QSignalSpy(backend.showMessage)
        options = make_iterator_config(
            load_specific_sources=(), max_page_concurrency=1, max_item_concurrency=1,
            page_error_mode=ErrorMode.RAISE, item_error_mode=ErrorMode.RAISE,
        )
        try:
            await backend._process_model_url(
                case["url"], "$index-$title", VideoFilters(), pages=1, iterator_config=options,
            )
        except Exception as error:
            # Tube8's verified public User page has no video container. Only
            # this recorded feed failure qualifies; unrelated errors still fail.
            expected_error = case.get("public_feed_error")
            if (case.get("public_video_feed_unavailable") and expected_error
                    and expected_error in str(error) and model.rowCount() == before):
                raise ProfileFeedUnavailable(
                    "Public profile metadata verified; the public User page exposes no video listing",
                    {"profile": type(target).__name__, "profile_name": name, "rows": 0,
                     "feed_attempted": True, "feed_error": str(error)},
                ) from error
            raise
        count = model.rowCount() - before
        if count == 0 and case.get("public_video_feed_unavailable"):
            raise ProfileFeedUnavailable(
                "Public profile metadata verified; this User's video feed is login-only or not publicly exposed",
                {"profile": type(target).__name__, "profile_name": name, "rows": 0,
                 "feed_attempted": True, "gui_errors": [errors.at(i)[0] for i in range(errors.count())]},
            )
        if not 1 <= count <= items or inserted.count() != count:
            details = errors.at(0)[0] if errors.count() else "no GUI error emitted"
            raise AssertionError(f"Expected 1..{items} signalled list rows, got {count}; {details}")
        if errors.count():
            raise AssertionError(f"GUI preparation reported {errors.count()} error(s): {errors.at(0)[0]}")
        streams = []
        for row in range(before, model.rowCount()):
            index = model.index(row, 0)
            job_id = model.data(index, model.JobIdRole)
            video = model.get_video(job_id)
            if video is None or video.source_video is None:
                raise AssertionError("List row lost its prepared/source media object")
            if video.title.strip().casefold() in {"", "untitled", "unknown"}:
                raise AssertionError("List row has an empty/placeholder title")
            if not isinstance(video.length, int) or video.length <= 0:
                raise AssertionError("List row has no positive video duration")
            if not _http_url(video.url) or not _http_url(video.thumbnail_url) or not video.video_id:
                raise AssertionError("List row has missing video/thumbnail URLs or media identity")
            if not isinstance(video.tags, list) or not isinstance(video.author, str) or not video.author.strip():
                raise AssertionError("List row has invalid author/tag metadata")
            if model.data(index, model.TitleRole) != f"{video.index}) {video.title}":
                raise AssertionError("QML title role differs from the prepared video")
            if model.data(index, model.AuthorRole) != video.author:
                raise AssertionError("QML author role differs from the prepared video")
            minutes, seconds = divmod(video.length, 60)
            if model.data(index, model.DurationRole) != model.tr("%d min %02d sec") % (minutes, seconds):
                raise AssertionError("QML duration role differs from the prepared video")
            available = model.data(index, model.AvailableQualitiesRole)
            if available != [str(q) for q in video.qualities]:
                raise AssertionError("QML qualities differ from the prepared video")
            selected = model.data(index, model.SelectedQualityRole)
            if selected and selected not in available:
                raise AssertionError("Selected quality is not one of the available qualities")
            if model.data(index, model.ProgressRole) != 0 or model.data(index, model.StatusRole) != "pending":
                raise AssertionError("A prepared row unexpectedly started downloading")
            if video.origin_iterator_url != case["url"] or video.origin_iterator_name != name:
                raise AssertionError("List row lost its originating profile identity")
            if video.output_path is None or video.output_path.exists():
                raise AssertionError("A media output file was unexpectedly created")
            quality = selected or (min(video.qualities) if video.qualities else "best")
            streams.append(await verify_stream(video.source_video, quality))
        return {"profile": type(target).__name__, "profile_name": name, "profile_metadata": profile_metadata,
                "rows": count, "streams": streams}

    with MetadataOnlyRequests() as guard, diagnostic_settings(items=items):
        try:
            result = await asyncio.wait_for(check(), timeout)
        finally:
            if guard.blocked:
                raise AssertionError(f"Blocked media download attempts: {guard.blocked}")
        result["metadata_requests"] = guard.requests
    return result


def make_test_backend():
    """Use real Qt objects/signals, without database/license/update startup."""
    from PySide6.QtCore import QObject

    from src.backend.application import Backend
    from src.backend.download_manager import DownloadListModel, DownloadManager

    backend = Backend.__new__(Backend)
    QObject.__init__(backend)
    backend.logger = SimpleNamespace(info=lambda *args: None)
    backend.download_manager = DownloadManager()
    backend._downloads_model = DownloadListModel(backend)
    backend.download_manager.video_added.connect(backend.video_added_signal)
    return backend
