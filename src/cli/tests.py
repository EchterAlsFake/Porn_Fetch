"""Comprehensive self-test suite for Porn Fetch CLI."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
import fractions
import os
from pathlib import Path
import tempfile
import time
from typing import Any, Callable, Coroutine

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from src.backend.media import VideoObject, select_allowed_quality
from src.backend.metadata import write_tags
from .downloads import (
    DownloadController,
    DownloadOutcome,
    DownloadState,
    PausedStore,
    clear_resume_state,
    has_resume_state,
    download_video,
)
from .media import prepare_video
from .model_store import ModelStore
from .output import output_path_for
from .providers import ClientPool, ContentKind, Route, route_url, PROVIDER_MODULES
from .settings import CliSettings, SettingsStore
from .licensing import create_license_service


# Single URLs identical to GUI smoke tests (src/backend/tests.py)
SINGLE_VIDEO_TESTS = [
    ("PornHub", "https://www.pornhub.com/view_video.php?viewkey=67bd0f66a8fce"),
    ("XHamster", "https://xhamster.com/videos/yoga-instructor-guides-us-during-hardcore-sex-xhLLvCd"),
    ("XNXX", "https://www.xnxx.com/video-i60z5ca/als_der_stiefbruder_amara_der_heissen_kleinen_schwester_ihr_tagebuch_findet_weiss_er_dass_es_der_weg_zu_ihrer_sussen_muschi_ist._sieh_zu_wie_sie_seinen_schwanz_bis_zu_einem_gesicht_voller_sperma_lutscht_und_fickt_nur_um_sie_dreckig_zu_halten"),
    ("xvideos", "https://de.xvideos.com/video.omtdluc3e5f/52563166/0/my_slutty_stepsister_was_getting_ready_for_a_date_but_i_sto_p_d_her_and_fucked_her_myself"),
    ("eporner", "https://www.eporner.com/video-cENxynmNow9/the-best-of-miak-onlyf-4k-hdr/"),
    ("spankbang", "https://spankbang.com/a4u5v/video/dogfart+from+parking+war+to+hardcore+fuck+adira+allure+vs+monster+neighbor+cock"),
    ("youporn", "https://www.youporn.com/watch/196323191/"),
    ("beeg", "https://beeg.com/-0785353135636417"),
    ("redtube", "https://de.redtube.com/191071081"),
    ("thumbzilla", "https://www.thumbzilla.com/watch/264561861/"),
    ("tube8", "https://www.tube8.com/porn-video/264330411/"),
    ("xfreehd", "https://beta.xfreehd.com/video/1073182/braless-neighbor-in-the-morning-mina-sakura"),
    ("porntrex", "https://www.porntrex.com/video/3002169/gaia-on-top-anal-creampie"),
]

SHORTS_TESTS = [
    ("PornHub Short", "https://www.pornhub.com/shorties/6a346596ea4ff"),
    ("XHamster Short", "https://xhamster.com/shorts/female-boss-wanted-employee-mind-xh8WCYr"),
]

GALLERY_TESTS = [
    ("XFreeHD Album", "https://beta.xfreehd.com/album/14805/woman-boy-18-nudists"),
]

PLAYLIST_TESTS = [
    ("PornHub Playlist", "https://www.pornhub.com/playlist/119820351"),
    ("Xvideos Playlist", "https://de.xvideos.com/favorite/89127817/playlist_3"),
    ("YouPorn Collection", "https://www.youporn.com/collections/videos/38771091/"),
    ("RedTube Playlist", "https://de.redtube.com/playlist/4237321"),
]

PROFILE_TESTS = [
    ("PornHub Model", "https://www.pornhub.com/model/teddy-tarantino"),
    ("PornHub Channel", "https://www.pornhub.com/channels/brazzers"),
    ("Eporner Pornstar", "https://www.eporner.com/pornstar/riley-reid/"),
    ("XNXX User", "https://www.xnxx.com/pornstar/cory-chase"),
    ("Xvideos Pornstar", "https://de.xvideos.com/pornstars/sweetie-fox1"),
    ("Xvideos Channel", "https://de.xvideos.com/teddy_tarantino"),
    ("XHamster Pornstar", "https://xhamster.com/pornstars/polly-yangs"),
    ("XHamster Creator", "https://xhamster.com/creators/comatozze"),
    ("Spankbang Pornstar", "https://spankbang.com/32/pornstar/angela+white/"),
    ("Spankbang Creator", "https://spankbang.com/kxrn/creator/yvonna/"),
    ("YouPorn Pornstar", "https://www.youporn.com/pornstar/eva-elfie/"),
    ("YouPorn Channel", "https://www.youporn.com/channel/mia-khalifa/"),
    ("Porntrex Model", "https://www.porntrex.com/models/rose/"),
    ("Porntrex Channel", "https://www.porntrex.com/channels/nubile-films/"),
    ("RedTube Pornstar", "https://de.redtube.com/pornstar/leny+evil"),
    ("RedTube Channel", "https://de.redtube.com/channels/freeuse"),
    ("RedTube Amateur", "https://de.redtube.com/amateur/littlereislin-ph-2"),
    ("Thumbzilla Pornstar", "https://www.thumbzilla.com/pornstar/alina-angel/"),
    ("Thumbzilla Channel", "https://www.thumbzilla.com/channel/brazzers/"),
    ("Thumbzilla Amateur", "https://www.thumbzilla.com/amateur/0princesspeachy0-ph/"),
    ("Tube8 Pornstar", "https://www.tube8.com/pornstar/alina-angel/"),
    ("Tube8 Channel", "https://www.tube8.com/channel/teamskeet/"),
    ("Tube8 Amateur", "https://www.tube8.com/amateur/e6cd031-ph/"),
]


@dataclass
class TestResult:
    category: str
    name: str
    target: str
    passed: bool
    details: str
    duration_s: float
    error: str | None = None


async def run_offline_tests() -> list[TestResult]:
    """Test non-network CLI subsystems: routing, quality rules, settings, model store, paths."""
    results: list[TestResult] = []

    # 1. Routing test
    t0 = time.perf_counter()
    try:
        routing_samples = {
            "pornhub": ("https://www.pornhub.com/view_video.php?viewkey=ph123", ContentKind.VIDEO),
            "eporner": ("https://www.eporner.com/video-123/title/", ContentKind.VIDEO),
            "xnxx": ("https://www.xnxx.com/video-123/title", ContentKind.VIDEO),
            "xvideos": ("https://www.xvideos.com/video.123/title", ContentKind.VIDEO),
            "xhamster": ("https://xhamster.com/videos/title-123", ContentKind.VIDEO),
            "spankbang": ("https://spankbang.com/123/video/title", ContentKind.VIDEO),
            "youporn": ("https://www.youporn.com/watch/123/title/", ContentKind.VIDEO),
            "beeg": ("https://beeg.com/-123", ContentKind.VIDEO),
            "porntrex": ("https://www.porntrex.com/video/123/title/", ContentKind.VIDEO),
            "xfreehd": ("https://xfreehd.com/video/123/title", ContentKind.VIDEO),
            "redtube": ("https://www.redtube.com/123", ContentKind.VIDEO),
            "thumbzilla": ("https://www.thumbzilla.com/video/123/title", ContentKind.VIDEO),
            "tube8": ("https://www.tube8.com/video/123/title/", ContentKind.VIDEO),
            "xfreehd_album": ("https://beta.xfreehd.com/album/14805/test", ContentKind.GALLERY),
            "ph_playlist": ("https://www.pornhub.com/playlist/123", ContentKind.COLLECTION),
            "xv_playlist": ("https://de.xvideos.com/favorite/123/playlist_1", ContentKind.COLLECTION),
            "ph_model": ("https://www.pornhub.com/model/test", ContentKind.PROFILE),
            "xnxx_pornstar": ("https://www.xnxx.com/pornstar/test", ContentKind.PROFILE),
        }
        for expected_provider, (sample_url, expected_kind) in routing_samples.items():
            route = route_url(sample_url)
            if "_" not in expected_provider:
                assert route.provider == expected_provider, f"Expected {expected_provider}, got {route.provider}"
            assert route.kind == expected_kind, f"Expected {expected_kind}, got {route.kind} for {sample_url}"
        results.append(TestResult("Offline", "URL Routing & Classification", f"{len(routing_samples)} rules", True, "All routes mapped correctly", time.perf_counter() - t0))
    except Exception as exc:
        results.append(TestResult("Offline", "URL Routing & Classification", "Routing rules", False, "", time.perf_counter() - t0, str(exc)))

    # 2. Quality selection rules
    t0 = time.perf_counter()
    try:
        available = [240, 480, 720, 1080, 2160]
        assert select_allowed_quality("best", available, has_premium=False) == "720", "Free limit should cap at 720p"
        assert select_allowed_quality("best", available, has_premium=True) == "2160", "Premium should select best"
        assert select_allowed_quality("1080", available, has_premium=False) == "720", "Requesting 1080p without premium falls back to 720p"
        assert select_allowed_quality("1080", available, has_premium=True) == "1080", "Requesting 1080p with premium grants 1080p"
        results.append(TestResult("Offline", "Quality Tier Enforcement", "Free vs Premium", True, "Quality selection limits verified", time.perf_counter() - t0))
    except Exception as exc:
        results.append(TestResult("Offline", "Quality Tier Enforcement", "Free vs Premium", False, "", time.perf_counter() - t0, str(exc)))

    # 3. Output path formatting
    t0 = time.perf_counter()
    try:
        dummy_video = VideoObject(
            url="https://example.com/video/123",
            title="Sample Test Title",
            author="Sample Author",
            length=10,
            tags=["tag1"],
            thumbnail_url="",
            video_id="12345",
            publish_date=None,
            qualities=[720],
            status="pending",
        )
        settings = CliSettings(path_template="$author/$title [$video_id]", output_path="/tmp/downloads")
        path = output_path_for(dummy_video, settings)
        assert "Sample Author" in str(path) and "Sample Test Title [12345]" in str(path)
        results.append(TestResult("Offline", "Output Template Formatter", "$author/$title [$video_id]", True, f"Formatted: {path.name}", time.perf_counter() - t0))
    except Exception as exc:
        results.append(TestResult("Offline", "Output Template Formatter", "Template evaluation", False, "", time.perf_counter() - t0, str(exc)))

    # 4. ModelStore lifecycle in isolated temp file
    t0 = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_models.json"
            store = ModelStore(path=db_path)
            model_url = "https://www.pornhub.com/model/test-model"
            video_url1 = "https://www.pornhub.com/view_video.php?viewkey=v1"
            video_url2 = "https://www.pornhub.com/view_video.php?viewkey=v2"

            store.add(model_url)
            assert len(store.models()) == 1
            store.update_pending(model_url, [video_url1, video_url2])
            state = dict(store.models())[model_url]
            assert len(state["pending"]) == 2

            store.mark_downloaded(model_url, video_url1)
            state = dict(store.models())[model_url]
            assert video_url1 in state["downloaded"]
            assert video_url1 not in state["pending"]

            store.remove(model_url)
            assert len(store.models()) == 0
        results.append(TestResult("Offline", "ModelStore Lifecycle", "CRUD operations", True, "Add, update, mark, remove passed", time.perf_counter() - t0))
    except Exception as exc:
        results.append(TestResult("Offline", "ModelStore Lifecycle", "CRUD operations", False, "", time.perf_counter() - t0, str(exc)))

    # 5. SettingsStore persistence
    t0 = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg_path = Path(tmp_dir) / "settings.json"
            sstore = SettingsStore(path=cfg_path)
            loaded = sstore.load()
            overridden = loaded.overridden(quality="1080", parallel_downloads=7)
            sstore.save(overridden)

            reloaded = sstore.load()
            assert reloaded.quality == "1080"
            assert reloaded.parallel_downloads == 7
        results.append(TestResult("Offline", "SettingsStore Persistence", "Atomic JSON load/save", True, "Persistence verified", time.perf_counter() - t0))
    except Exception as exc:
        results.append(TestResult("Offline", "SettingsStore Persistence", "Atomic JSON load/save", False, "", time.perf_counter() - t0, str(exc)))

    return results


def _format_error(exc: Exception, timeout: float) -> str:
    if isinstance(exc, (TimeoutError, asyncio.TimeoutError)):
        return f"Timed out after {timeout:.0f}s"
    msg = str(exc).strip() or type(exc).__name__
    return msg.split("\n")[0][:120]


async def test_single_url(name: str, url: str, pool: ClientPool, timeout: float = 60.0) -> TestResult:
    """Test resolving a single video URL and loading its media metadata."""
    t0 = time.perf_counter()
    try:
        async def _resolve_and_prepare():
            route, source = await pool.resolve(url)
            return await prepare_video(source, route.provider)

        media = await asyncio.wait_for(_resolve_and_prepare(), timeout=timeout)
        if not media.title or media.title == "Untitled":
            raise AssertionError(f"Title empty or missing: {media.title!r}")
        if not media.qualities:
            raise AssertionError("No available qualities extracted")

        details = f"Qualities: {media.qualities} | Author: {media.author[:25]}"
        return TestResult("Single URLs", name, url, True, details, time.perf_counter() - t0)
    except Exception as exc:
        return TestResult("Single URLs", name, url, False, "", time.perf_counter() - t0, _format_error(exc, timeout))


async def test_short_url(name: str, url: str, pool: ClientPool, timeout: float = 60.0) -> TestResult:
    """Test short/moment URL resolution and metadata extraction."""
    t0 = time.perf_counter()
    try:
        async def _resolve():
            route, source = await pool.resolve(url)
            return await prepare_video(source, route.provider)

        media = await asyncio.wait_for(_resolve(), timeout=timeout)
        if not media.title or media.title == "Untitled":
            raise AssertionError(f"Short title missing: {media.title!r}")

        details = f"Title: {media.title[:30]} | Qualities: {media.qualities}"
        return TestResult("Shorts", name, url, True, details, time.perf_counter() - t0)
    except Exception as exc:
        return TestResult("Shorts", name, url, False, "", time.perf_counter() - t0, _format_error(exc, timeout))


async def test_gallery_url(name: str, url: str, pool: ClientPool, timeout: float = 60.0) -> TestResult:
    """Test gallery/album URL resolution."""
    t0 = time.perf_counter()
    try:
        async def _resolve():
            route, source = await pool.resolve(url)
            return route, source

        route, album = await asyncio.wait_for(_resolve(), timeout=timeout)
        title = getattr(album, "title", None) or "Untitled"
        images = getattr(album, "images", None) or getattr(album, "photos", None) or []
        details = f"Title: {str(title)[:30]} | Items: {len(images)}"
        return TestResult("Galleries", name, url, True, details, time.perf_counter() - t0)
    except Exception as exc:
        return TestResult("Galleries", name, url, False, "", time.perf_counter() - t0, _format_error(exc, timeout))


async def test_stream_url(
    category: str, name: str, url: str, pool: ClientPool, timeout: float = 60.0,
) -> TestResult:
    """Test container streaming for models, channels, playlists and collections."""
    t0 = time.perf_counter()
    try:
        async def _stream():
            route = route_url(url)
            items = []
            async for video in pool.media_stream(url, pages=1):
                items.append(video)
                if len(items) >= 1:
                    break
            return route, items

        route, items = await asyncio.wait_for(_stream(), timeout=timeout)
        if not items:
            raise AssertionError("Media stream yielded 0 items")

        first = items[0]
        title = getattr(first, "title", None) or getattr(first, "video_id", None) or "Item"
        details = f"Kind: {route.kind.value} | Sample item: {str(title)[:30]}"
        return TestResult(category, name, url, True, details, time.perf_counter() - t0)
    except Exception as exc:
        return TestResult(category, name, url, False, "", time.perf_counter() - t0, _format_error(exc, timeout))


async def test_licensing_service(settings: CliSettings) -> TestResult:
    """Test offline/online licensing service initialization and check."""
    t0 = time.perf_counter()
    service = create_license_service(settings.to_runtime_config())
    try:
        status = await service.check()
        assert status is not None
        details = f"State: {status.state} | Allowed: {status.allowed}"
        return TestResult("Licensing", "License Service Check", "Local License Service", True, details, time.perf_counter() - t0)
    except Exception as exc:
        return TestResult("Licensing", "License Service Check", "Local License Service", False, "", time.perf_counter() - t0, _format_error(exc, 10.0))
    finally:
        await service.close()


async def test_synthetic_pyav_tagging() -> TestResult:
    start = time.perf_counter()
    try:
        import av
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            sample_mp4 = f.name

        try:
            with av.open(sample_mp4, mode="w", format="mp4") as container:
                stream = container.add_stream("h264", rate=24)
                stream.width = 64
                stream.height = 64
                stream.pix_fmt = "yuv420p"
                stream.time_base = fractions.Fraction(1, 24)
                for i in range(10):
                    frame = av.VideoFrame(64, 64, "yuv420p")
                    frame.pts = i
                    for packet in stream.encode(frame):
                        container.mux(packet)
                for packet in stream.encode():
                    container.mux(packet)

            vo = VideoObject(
                url="https://example.com/test",
                title="Self-Test Video Title",
                author="Test Model Name",
                length=10,
                tags=["tag1", "tag2"],
                thumbnail_url="https://example.com/thumb.jpg",
                video_id="test1234",
                publish_date=datetime(2026, 9, 18),
                qualities=[720],
                status="ready",
            )
            tagged = write_tags(sample_mp4, vo)
            if not tagged:
                return TestResult("Downloads", "PyAV Tagging (Synthetic)", sample_mp4, False, "", time.perf_counter() - start, "write_tags returned False")

            with av.open(sample_mp4) as c:
                meta = c.metadata
                assert meta.get("title") == "Self-Test Video Title", f"Title mismatch: {meta.get('title')}"
                assert meta.get("artist") == "Test Model Name", f"Artist mismatch: {meta.get('artist')}"
                assert meta.get("genre") == "XXX", f"Genre mismatch: {meta.get('genre')}"
                assert "2026-09-18" in meta.get("date", ""), f"Date mismatch: {meta.get('date')}"

            return TestResult(
                "Downloads", "PyAV Tagging (Synthetic)", "Synthetic MP4", True,
                "Tagged & verified title, artist, genre, date via av.open()",
                time.perf_counter() - start,
            )
        finally:
            if os.path.exists(sample_mp4):
                os.unlink(sample_mp4)
    except Exception as e:
        return TestResult("Downloads", "PyAV Tagging (Synthetic)", "Synthetic MP4", False, "", time.perf_counter() - start, str(e))


async def test_download_controller_logic() -> TestResult:
    start = time.perf_counter()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "test_ctrl.mp4"
            store_file = Path(tmpdir) / "paused.json"
            store = PausedStore(store_file)

            ctrl = DownloadController(
                url="https://example.com/video1",
                target=target,
                title="Controller Test",
                quality="720",
                provider="pornhub",
            )
            assert ctrl.state == DownloadState.PENDING
            assert not ctrl.stop_event.is_set()

            # Test Pause
            ctrl.pause()
            assert ctrl.state == DownloadState.PAUSED
            assert ctrl.is_paused
            assert ctrl.stop_event.is_set()

            # Test Resume
            ctrl.resume()
            assert ctrl.state == DownloadState.DOWNLOADING
            assert not ctrl.stop_event.is_set()

            # Test Cancel
            ctrl.cancel(cleanup=True)
            assert ctrl.state == DownloadState.CANCELLED
            assert ctrl.is_cancelled

        return TestResult(
            "Downloads", "Controller & State Transitions", "DownloadController / PausedStore", True,
            "PENDING -> PAUSED -> DOWNLOADING -> CANCELLED states verified",
            time.perf_counter() - start,
        )
    except Exception as e:
        return TestResult(
            "Downloads", "Controller & State Transitions", "DownloadController", False, "",
            time.perf_counter() - start, str(e),
        )


async def test_live_download_and_pyav(pool: ClientPool, settings: CliSettings) -> TestResult:
    start = time.perf_counter()
    url = "https://www.pornhub.com/shorties/6a346596ea4ff"
    try:
        route, source = await pool.resolve(url)
        media = await prepare_video(source, route.provider)
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "live_short.mp4"
            outcome = await download_video(
                media.source_video,
                target,
                quality="worst",
                settings=settings,
                has_premium=False,
                available_qualities=media.qualities,
            )
            if outcome.status != "completed":
                return TestResult("Downloads", "Live Download & Metadata Tagging", url, False, "", time.perf_counter() - start, f"Download status {outcome.status}")
            if not target.exists() or target.stat().st_size == 0:
                return TestResult("Downloads", "Live Download & Metadata Tagging", url, False, "", time.perf_counter() - start, "Output file empty or missing")

            size_mb = target.stat().st_size / (1024 * 1024)
            tagged = write_tags(str(target), media)
            if not tagged:
                return TestResult("Downloads", "Live Download & Metadata Tagging", url, False, "", time.perf_counter() - start, "write_tags failed")

            import av
            with av.open(str(target)) as c:
                title_tag = c.metadata.get("title") or ""
                artist_tag = c.metadata.get("artist") or ""

            return TestResult(
                "Downloads", "Live Download & Metadata Tagging", f"{media.title[:30]} ({size_mb:.1f} MB)", True,
                f"Downloaded & tagged metadata: title='{title_tag[:20]}...', artist='{artist_tag}'",
                time.perf_counter() - start,
            )
    except Exception as e:
        return TestResult("Downloads", "Live Download & Metadata Tagging", url, False, "", time.perf_counter() - start, str(e))


async def test_live_pause_and_resume_flow(pool: ClientPool, settings: CliSettings) -> TestResult:
    start = time.perf_counter()
    url = "https://www.pornhub.com/shorties/6a346596ea4ff"
    try:
        route, source = await pool.resolve(url)
        media = await prepare_video(source, route.provider)
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "pause_resume_short.mp4"
            ctrl = DownloadController(
                url=url, target=target, title=media.title, quality="worst", provider=route.provider,
            )

            paused_once = False
            def on_progress(pos, total, unit="items"):
                nonlocal paused_once
                if pos >= 1 and not paused_once:
                    paused_once = True
                    ctrl.pause()

            outcome1 = await download_video(
                media.source_video, target, "worst", settings,
                has_premium=False, available_qualities=media.qualities,
                controller=ctrl, progress=on_progress,
            )
            if outcome1.status != "paused" or not ctrl.is_paused:
                return TestResult("Downloads", "Live Pause & Resume Flow", url, False, "", time.perf_counter() - start, f"Expected paused, got {outcome1.status}")
            if not has_resume_state(target):
                return TestResult("Downloads", "Live Pause & Resume Flow", url, False, "", time.perf_counter() - start, "Resume state not preserved on pause")

            # Resume
            ctrl.resume()
            outcome2 = await download_video(
                media.source_video, target, "worst", settings,
                has_premium=False, available_qualities=media.qualities,
                controller=ctrl,
            )
            if outcome2.status != "completed":
                return TestResult("Downloads", "Live Pause & Resume Flow", url, False, "", time.perf_counter() - start, f"Resume failed with status {outcome2.status}")
            if not target.exists() or target.stat().st_size == 0:
                return TestResult("Downloads", "Live Pause & Resume Flow", url, False, "", time.perf_counter() - start, "Final target missing or empty")

            size_mb = target.stat().st_size / (1024 * 1024)
            return TestResult(
                "Downloads", "Live Pause & Resume Flow", f"Paused @ seg 1 -> Resumed ({size_mb:.1f} MB)", True,
                "Paused mid-download and resumed to 100% completion",
                time.perf_counter() - start,
            )
    except Exception as e:
        return TestResult("Downloads", "Live Pause & Resume Flow", url, False, "", time.perf_counter() - start, str(e))


async def test_live_cancel_and_cleanup_flow(pool: ClientPool, settings: CliSettings) -> TestResult:
    start = time.perf_counter()
    url = "https://www.pornhub.com/shorties/6a346596ea4ff"
    try:
        route, source = await pool.resolve(url)
        media = await prepare_video(source, route.provider)
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "cancel_cleanup_short.mp4"
            ctrl = DownloadController(
                url=url, target=target, title=media.title, quality="worst", provider=route.provider,
            )

            def on_progress(pos, total, unit="items"):
                if pos >= 1:
                    ctrl.cancel(cleanup=True)

            outcome = await download_video(
                media.source_video, target, "worst", settings,
                has_premium=False, available_qualities=media.qualities,
                controller=ctrl, progress=on_progress,
            )
            if outcome.status != "cancelled" or not ctrl.is_cancelled:
                return TestResult("Downloads", "Live Cancel & Cleanup Flow", url, False, "", time.perf_counter() - start, f"Expected cancelled, got {outcome.status}")
            if has_resume_state(target):
                return TestResult("Downloads", "Live Cancel & Cleanup Flow", url, False, "", time.perf_counter() - start, "Partial segments were not cleaned up")

            return TestResult(
                "Downloads", "Live Cancel & Cleanup Flow", "Cancellation with cleanup=True", True,
                "Cancelled mid-download and confirmed partial segments purged",
                time.perf_counter() - start,
            )
    except Exception as e:
        return TestResult("Downloads", "Live Cancel & Cleanup Flow", url, False, "", time.perf_counter() - start, str(e))


async def run_cli_self_test(
    filter_pattern: str | None = None,
    concurrency: int = 2,
    include_downloads: bool = False,
) -> int:
    """Execute the comprehensive CLI self-test suite and display summary."""
    console = Console()
    console.print()
    console.print(Panel(
        "[bold #00e5ff]PORN FETCH CLI[/] [bold #ff2a85]Comprehensive Self-Test Suite[/]\n"
        "[dim]Testing offline subsystems, single URLs, shorts, galleries, playlists, and profiles...[/]",
        border_style="#ff2a85",
        padding=(0, 2),
    ))
    console.print()

    settings = CliSettings()
    pool = ClientPool(settings.to_runtime_config())
    results: list[TestResult] = []
    semaphore = asyncio.Semaphore(concurrency)

    async def with_limit(coro: Coroutine[Any, Any, TestResult]) -> TestResult:
        async with semaphore:
            res = await coro
            status_style = "bold green" if res.passed else "bold red"
            status_text = "PASS" if res.passed else "FAIL"
            dur = f"{res.duration_s:.1f}s"
            console.print(
                f"  [{status_style}]{status_text:<4}[/] [cyan]{res.category:<12}[/] "
                f"[bold white]{res.name:<25}[/] [dim]({dur})[/] "
                f"{res.details if res.passed else f'[red]{res.error}[/]'}"
            )
            return res

    start_total = time.perf_counter()

    try:
        # Filter helper
        def should_run(category: str, name: str, url: str) -> bool:
            if not filter_pattern:
                return True
            pat = filter_pattern.lower().strip()
            aliases = {pat}
            if pat.endswith("ies"):
                aliases.add(pat[:-3] + "y")
            elif pat.endswith("y"):
                aliases.add(pat[:-1] + "ies")
            elif pat.endswith("s"):
                aliases.add(pat[:-1])
            else:
                aliases.add(pat + "s")

            search_text = f"{category} {name} {url}".lower()
            return any(alias in search_text for alias in aliases)

        run_offline = not filter_pattern or any(k in filter_pattern.lower() for k in ("offline", "core", "setting", "model", "rout", "qual"))

        # Phase 1: Offline tests
        if run_offline:
            console.print("[bold cyan]=== [1/6] Core Subsystems & Offline Features ===[/]")
            offline_results = await run_offline_tests()
            for res in offline_results:
                status_style = "bold green" if res.passed else "bold red"
                status_text = "PASS" if res.passed else "FAIL"
                console.print(
                    f"  [{status_style}]{status_text:<4}[/] [cyan]{res.category:<12}[/] "
                    f"[bold white]{res.name:<25}[/] [dim]({res.duration_s:.2f}s)[/] "
                    f"{res.details if res.passed else f'[red]{res.error}[/]'}"
                )
            results.extend(offline_results)

            # Licensing test
            lic_result = await test_licensing_service(settings)
            status_style = "bold green" if lic_result.passed else "bold red"
            status_text = "PASS" if lic_result.passed else "FAIL"
            console.print(
                f"  [{status_style}]{status_text:<4}[/] [cyan]{lic_result.category:<12}[/] "
                f"[bold white]{lic_result.name:<25}[/] [dim]({lic_result.duration_s:.2f}s)[/] "
                f"{lic_result.details if lic_result.passed else f'[red]{lic_result.error}[/]'}"
            )
            results.append(lic_result)
            console.print()

        # Phase 2: Single Video URLs (same as GUI)
        single_tasks = [
            with_limit(test_single_url(name, url, pool))
            for name, url in SINGLE_VIDEO_TESTS
            if should_run("Single URLs", name, url)
        ]
        if single_tasks:
            console.print("[bold cyan]=== [2/6] Single Video URLs (13 Supported Providers) ===[/]")
            results.extend(await asyncio.gather(*single_tasks))
            console.print()

        # Phase 3: Shorts
        shorts_tasks = [
            with_limit(test_short_url(name, url, pool))
            for name, url in SHORTS_TESTS
            if should_run("Shorts", name, url)
        ]
        if shorts_tasks:
            console.print("[bold cyan]=== [3/6] Shorts & Moments ===[/]")
            results.extend(await asyncio.gather(*shorts_tasks))
            console.print()

        # Phase 4: Galleries / Albums
        gallery_tasks = [
            with_limit(test_gallery_url(name, url, pool))
            for name, url in GALLERY_TESTS
            if should_run("Galleries", name, url)
        ]
        if gallery_tasks:
            console.print("[bold cyan]=== [4/6] Photo Albums & Galleries ===[/]")
            results.extend(await asyncio.gather(*gallery_tasks))
            console.print()

        # Phase 5: Playlists & Collections
        playlist_tasks = [
            with_limit(test_stream_url("Playlists", name, url, pool))
            for name, url in PLAYLIST_TESTS
            if should_run("Playlists", name, url)
        ]
        if playlist_tasks:
            console.print("[bold cyan]=== [5/6] Playlists & Collections ===[/]")
            results.extend(await asyncio.gather(*playlist_tasks))
            console.print()

        # Phase 6: Models, Channels, Creators & Pornstars
        profile_tasks = [
            with_limit(test_stream_url("Profiles", name, url, pool))
            for name, url in PROFILE_TESTS
            if should_run("Profiles", name, url)
        ]
        if profile_tasks:
            console.print("[bold cyan]=== [6/6] Models, Channels, Creators & Profiles ===[/]")
            results.extend(await asyncio.gather(*profile_tasks))
            console.print()

        # Phase 7: Downloads, Pause / Resume & PyAV Metadata Tagging (Strictly Opt-in via --test-downloads)
        if include_downloads:
            console.print("[bold cyan]=== [7/7] Live Downloads, Pause / Resume & PyAV Metadata Tagging ===[/]")
            dl_tasks = [
                with_limit(test_synthetic_pyav_tagging()),
                with_limit(test_download_controller_logic()),
                with_limit(test_live_download_and_pyav(pool, settings)),
                with_limit(test_live_pause_and_resume_flow(pool, settings)),
                with_limit(test_live_cancel_and_cleanup_flow(pool, settings)),
            ]
            results.extend(await asyncio.gather(*dl_tasks))
            console.print()
        else:
            console.print("[dim]💡 Tip: Live download, pause/resume, and PyAV metadata tagging tests are opt-in. Run with --test-downloads to include them.[/]\n")

    finally:
        await pool.close()

    total_time = time.perf_counter() - start_total

    # Summary table
    passed_count = sum(1 for r in results if r.passed)
    failed_count = sum(1 for r in results if not r.passed)
    total_count = len(results)

    summary_table = Table(title="Test Results Summary by Category", border_style="#ff2a85")
    summary_table.add_column("Category", style="cyan", no_wrap=True)
    summary_table.add_column("Total", justify="right")
    summary_table.add_column("Passed", justify="right", style="green")
    summary_table.add_column("Failed", justify="right", style="red")

    categories = list(dict.fromkeys(r.category for r in results))
    for cat in categories:
        cat_results = [r for r in results if r.category == cat]
        p = sum(1 for r in cat_results if r.passed)
        f = sum(1 for r in cat_results if not r.passed)
        summary_table.add_row(cat, str(len(cat_results)), str(p), str(f))

    console.print(summary_table)
    console.print()

    # Failures breakdown
    if failed_count > 0:
        failures_table = Table(title="Failed Tests Breakdown", border_style="red")
        failures_table.add_column("Category", style="cyan", no_wrap=True)
        failures_table.add_column("Test Name", style="bold white")
        failures_table.add_column("Target URL / Subject", style="dim")
        failures_table.add_column("Error Message", style="red")

        for r in results:
            if not r.passed:
                failures_table.add_row(r.category, r.name, r.target, str(r.error))

        console.print(failures_table)
        console.print()

    # Final banner
    overall_color = "green" if failed_count == 0 else "yellow"
    summary_text = Text()
    summary_text.append(f"Self-Test Complete in {total_time:.1f}s — ", style="bold")
    summary_text.append(f"{passed_count} Passed", style="bold green")
    summary_text.append(" | ", style="dim")
    summary_text.append(f"{failed_count} Failed", style="bold red" if failed_count else "dim")
    summary_text.append(" | ", style="dim")
    summary_text.append(f"{total_count} Total", style="bold cyan")

    console.print(Panel(summary_text, border_style=overall_color, padding=(0, 2)))
    return 0 if failed_count == 0 else 1
