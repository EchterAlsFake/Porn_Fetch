"""Opt-in live pause/resume and cleanup checks using real provider libraries.

Run: uv run python -m src.tests.smoke.download_lifecycle
No requests are made by importing this module or by normal test discovery.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import logging
import re
import shutil
import tempfile
import time
import traceback
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from base_api.modules.static_functions import segment_file_path

from src.cli.downloads import RAW_VIDEO_MODULES, DownloadController, download_video, get_resume_paths
from src.cli.media import prepare_video
from src.cli.providers import ClientPool, route_url
from src.cli.selftest.cases import ACTIVE_DOWNLOAD_URL, SINGLE_VIDEO_TESTS
from src.cli.settings import CliSettings
from src.shared.ffmpeg import find_ffmpeg
from src.shared.provider_routing import PROVIDER_MODULES, ContentKind
from src.shared.tor_transport import MediaCore


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def public_url(url):
    """Keep request evidence without signed CDN query parameters or credentials."""
    parts = urlsplit(str(url))
    return urlunsplit((parts.scheme, parts.hostname or "", parts.path, "", ""))


def lifecycle_fixtures(overrides=None):
    """Reuse the maintained live-video inventory and cover every registered provider."""
    videos = {route_url(url).provider: url for _, url in SINGLE_VIDEO_TESTS}
    require(set(videos) == set(PROVIDER_MODULES),
            f"Video fixtures and providers differ: {set(videos) ^ set(PROVIDER_MODULES)}")
    # Keep the already-verified short fixture for PornHub's lifecycle checks.
    videos["pornhub"] = ACTIVE_DOWNLOAD_URL
    videos.update(overrides or {})
    fixtures = []
    for provider, url in videos.items():
        route = route_url(url)
        require(route.provider == provider and route.kind == ContentKind.VIDEO,
                f"Fixture must be a {provider} video URL: {url}")
        transport = ("raw" if PROVIDER_MODULES[provider] in RAW_VIDEO_MODULES
                     else "auto" if provider == "youporn" else "hls")
        fixtures.append((provider, transport, url))
    return fixtures


class ObservedCore(MediaCore):
    """Passively record real requests; all transport and downloading stay upstream."""

    def __init__(self, configuration):
        super().__init__(configuration)
        self.phase = "prepare"
        self.requests = []
        self.segment_requests = []
        self.segment_plans = []
        self.raw_urls = set()

    def initialize_session(self):
        super().initialize_session()
        session = self.session
        if session is None or getattr(session, "_lifecycle_observed", False):
            return
        original = session.request

        async def observed(method, url, **kwargs):
            headers = kwargs.get("headers") or {}
            entry = {"phase": self.phase, "method": method.upper(), "url": public_url(url),
                     "range": headers.get("Range") or headers.get("range"), "status": None,
                     "body_bytes_read": 0}
            self.requests.append(entry)
            try:
                response = await original(method, url, **kwargs)
                entry.update(status=response.status_code,
                             content_range=response.headers.get("Content-Range"),
                             content_length=response.headers.get("Content-Length"),
                             content_type=response.headers.get("Content-Type", ""))
                if kwargs.get("stream"):
                    original_content = response.aiter_content

                    async def observed_content(*args, **options):
                        async for data in original_content(*args, **options):
                            entry["body_bytes_read"] += len(data)
                            yield data

                    response.aiter_content = observed_content
                else:
                    entry["body_bytes_read"] = len(response.content)
                return response
            except Exception as error:
                entry["error_type"] = type(error).__name__
                raise

        session.request = observed
        session._lifecycle_observed = True

    async def download_segment(self, url, timeout, stop_event=None):
        self.segment_requests.append((self.phase, url))
        return await super().download_segment(url, timeout, stop_event)

    async def get_segments(self, m3u8_url_master, quality):
        segments = await super().get_segments(m3u8_url_master, quality)
        self.segment_plans.append({"phase": self.phase, "quality": str(quality), "segments": list(segments)})
        return segments

    async def legacy_download(self, url, configuration):
        self.raw_urls.add(public_url(url))
        return await super().legacy_download(url, configuration)


async def validate_media(path, ffmpeg, expected_minutes):
    require(path.is_file() and path.stat().st_size > 0, "No nonempty completed media file")
    process = await asyncio.create_subprocess_exec(
        str(ffmpeg), "-hide_banner", "-nostdin", "-i", str(path),
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    try:
        _, stderr = await asyncio.wait_for(process.communicate(), 30)
    finally:
        if process.returncode is None:
            process.kill()
            await process.wait()
    # Probing without an output intentionally exits 1 on FFmpeg. Validate its
    # parsed video stream and duration, rather than treating that exit as success.
    require(process.returncode in (0, 1), f"FFmpeg probe exited unexpectedly: {process.returncode}")
    info = stderr.decode(errors="replace")
    duration = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", info)
    require("Video:" in info and duration is not None, "FFmpeg could not read video streams and duration")
    hours, minutes, seconds = map(float, duration.groups())
    actual = hours * 3600 + minutes * 60 + seconds
    require(actual > 0, "Completed video has no positive duration")
    if expected_minutes:
        expected = expected_minutes * 60
        require(abs(actual - expected) <= max(90, expected * .05),
                f"Output duration {actual:.1f}s differs from provider metadata ({expected}s)")
    return {"bytes": path.stat().st_size, "duration_seconds": actual, "video_stream_readable": True}


def media_requests(core, phase):
    return [entry for entry in core.requests if entry["phase"] == phase and entry["method"] == "GET"
            and entry["body_bytes_read"] > 0
            and (entry["url"] in core.raw_urls or entry["range"] or "video/" in entry.get("content_type", ""))]


def no_partial_files(target, state_directory):
    state, segments = get_resume_paths(target, state_directory=state_directory)
    raw_state = Path(f"{target}.raw-state.json")
    remaining = [str(path) for path in (target, Path(f"{target}.tmp"), state, Path(f"{state}.tmp"),
                                      raw_state, raw_state.with_name(raw_state.name + ".tmp"))
                 if path.exists()]
    if segments.exists():
        remaining.extend(str(path) for path in segments.rglob("*") if path.is_file())
    require(not remaining, f"Cleanup left partial files: {remaining}")


async def check_case(provider, transport, url, scenario, directory, timeout, ffmpeg, result, *, quality=None):
    settings = CliSettings(
        output_path=str(directory), write_metadata=False, skip_existing=True,
        download_workers=1, request_attempts=2, timeout=30,
        response_cache_mb=0, segment_cache_mb=0,
    )
    target = directory / "video.mp4"
    state_directory = directory / "state"
    controller = DownloadController(url=url, target=target, provider=provider, state_directory=state_directory)
    async with ClientPool(settings.to_runtime_config(), core_factory=ObservedCore) as pool:
        result["stage"] = "prepare"
        route = route_url(url)
        require(route.provider == provider, f"Expected {provider}, got {route.provider}")
        pool.client(provider)
        core = pool.cores[provider]
        result["requests"] = core.requests
        _, source = await asyncio.wait_for(pool.resolve(url), min(timeout, 90))
        media = await asyncio.wait_for(prepare_video(source, provider), min(timeout, 90))
        actual_transport = ("raw" if PROVIDER_MODULES[provider] in RAW_VIDEO_MODULES
                            or getattr(source, "is_hls", None) is False else "hls")
        result.update(expected_transport=transport, transport=actual_transport)
        require(transport == "auto" or actual_transport == transport,
                f"Expected {transport.upper()}, provider selected {actual_transport.upper()}")
        transport = actual_transport
        if transport == "hls":
            require(bool(getattr(source, "m3u8_base_url", None)), "Provider exposed no HLS master playlist")
        permitted = [quality for quality in media.qualities if quality <= 720]
        require(bool(permitted), "Provider exposed no verified quality at or below 720p; "
                "a quality-unknown MP4 fallback cannot establish this test's quality limit")
        if quality is None:
            quality = min(permitted)
        require(quality in permitted,
                f"Requested {quality}p is unavailable; verified qualities at or below 720p: {permitted}")
        controller.title = media.title
        controller.quality = quality
        result.update(quality=quality, library=type(source).__module__, expected_duration_minutes=media.length)

        async def transfer(phase, interrupt=False):
            core.phase = phase
            result["stage"] = phase
            progress = {"first": None, "position": 0, "total": 0, "stop_requested": False}
            result.setdefault("progress", {})[phase] = progress

            def on_progress(position, total, unit="items"):
                if unit != ("segments" if transport == "hls" else "bytes"):
                    return
                if progress["first"] is None:
                    progress["first"] = position
                progress.update(position=position, total=total)
                threshold = 2 if transport == "hls" else min(1024 * 1024, max(65536, total // 10))
                if interrupt and not progress["stop_requested"] and 0 < position < total and position >= threshold:
                    progress["stop_requested"] = True
                    if scenario == "pause-resume":
                        controller.pause()
                    else:
                        controller.cancel(cleanup=True)

            task = asyncio.create_task(download_video(
                source, target, quality, settings, has_premium=False,
                controller=controller, available_qualities=media.qualities, progress=on_progress,
            ))
            try:
                outcome = await asyncio.wait_for(asyncio.shield(task), timeout)
            finally:
                if not task.done():
                    controller.stop_event.set()
                    try:
                        await asyncio.wait_for(task, 15)
                    except (Exception, asyncio.CancelledError):
                        task.cancel()
                        await asyncio.gather(task, return_exceptions=True)
            require(not outcome.skipped, "Partial download was incorrectly skipped as an existing completed file")
            errors = [entry for entry in core.requests if entry["phase"] == phase
                      and (entry["status"] or 0) >= 400]
            result.setdefault("transfers", {})[phase] = {
                "status": outcome.status, "missing_segments": list(outcome.missing_segments),
                "http_errors": dict(Counter(entry["status"] for entry in errors)),
                "first_http_error": errors[0] if errors else None,
            }
            if interrupt:
                require(progress["stop_requested"], "Media completed or failed before a meaningful interruption")
            return outcome, progress

        def require_completed(outcome, phase):
            details = result["transfers"][phase]
            first_error = details["first_http_error"]
            message = f"{phase.capitalize()} ended as {outcome.status}; {len(outcome.missing_segments)} missing segments"
            if first_error:
                counts = ", ".join(f"HTTP {status}: {count} requests"
                                   for status, count in details["http_errors"].items())
                message += f"; {counts}; first failing URL: {first_error['url']}"
            require(outcome.status == "completed", message)

        outcome, paused_progress = await transfer("interrupt", interrupt=True)
        state, segments = get_resume_paths(target, state_directory=state_directory)
        if scenario == "pause-resume":
            result["stage"] = "verify-pause"
            require(outcome.status == "paused", f"Expected paused, got {outcome.status}")
            saved = controller.paused_store.load()
            require(any(item.get("url") == url for item in saved), "Paused job was not persisted")
            retained = set()
            if transport == "hls":
                require(state.is_file(), "No persisted HLS segment state")
                payload = json.loads(state.read_text())
                retained = {segment for index, segment in enumerate(payload["segments"])
                            if (saved_segment := Path(segment_file_path(
                                segments, index, payload["segment_index_width"]))).is_file()
                            and saved_segment.stat().st_size > 0}
                require(0 < len(retained) < len(payload["segments"]), "Expected a partially downloaded segment set")
                result["retained_segments"] = len(retained)
            else:
                require(target.is_file() and target.stat().st_size >= paused_progress["position"] > 0,
                        "No retained RAW bytes after pause")
                prefix_size = min(65536, paused_progress["position"])
                with target.open("rb") as file:
                    prefix_hash = hashlib.sha256(file.read(prefix_size)).hexdigest()
                result["retained_bytes"] = paused_progress["position"]
                raw_state = Path(f"{target}.raw-state.json")
                require(raw_state.is_file(), "No persisted RAW checkpoint; install the base-api RAW resume fix")
                checkpoint = json.loads(raw_state.read_text())
                require(sum(checkpoint["progress"]) == paused_progress["position"],
                        "RAW checkpoint does not match reported retained progress")
            controller.resume()
            outcome, resumed_progress = await transfer("resume")
            require_completed(outcome, "resume")
            result["stage"] = "verify-resume"
            if transport == "hls":
                fetched = {url for phase, url in core.segment_requests if phase == "resume"}
                require(bool(fetched), "Resume made no requests for missing segments")
                require(not retained.intersection(fetched), "Resume downloaded previously saved HLS segments again")
                require(resumed_progress["first"] is not None and resumed_progress["first"] >= len(retained),
                        "Resume progress did not start from retained segments")
                result["reuse_verified"] = True
            else:
                requests = media_requests(core, "resume")
                require(bool(requests), "RAW resume made no media requests")
                require(resumed_progress["first"] == result["retained_bytes"],
                        "RAW resume progress did not start from its retained byte count")
                for entry in requests:
                    byte_range = re.fullmatch(r"bytes=(\d+)-(\d*)", entry["range"] or "")
                    served_range = re.fullmatch(r"bytes (\d+)-(\d+)/(\d+)", entry.get("content_range") or "")
                    require(byte_range is not None and int(byte_range[1]) >= result["retained_bytes"]
                            and entry["status"] == 206 and served_range is not None
                            and int(served_range[1]) == int(byte_range[1])
                            and int(served_range[3]) == paused_progress["total"],
                            f"RAW resume requested {entry['range']!r} with HTTP {entry['status']} "
                            f"and Content-Range {entry.get('content_range')!r}; expected HTTP 206 "
                            f"starting at or after retained byte {result['retained_bytes']}")
                require(target.stat().st_size == paused_progress["total"], "RAW final length differs from server total")
                with target.open("rb") as file:
                    require(hashlib.sha256(file.read(prefix_size)).hexdigest() == prefix_hash,
                            "Resuming changed the retained RAW prefix")
                result["reuse_verified"] = True
        else:
            result["stage"] = "verify-cleanup"
            require(outcome.status == "cancelled", f"Expected cancelled, got {outcome.status}")
            no_partial_files(target, state_directory)
            require(not controller.paused_store.load(), "Cleanup left a resumable paused job")
            result["cleanup_verified"] = True
            controller.resume()
            outcome, restarted_progress = await transfer("restart")
            require_completed(outcome, "restart")
            if transport == "hls":
                plans = [plan["segments"] for plan in core.segment_plans if plan["phase"] == "restart"]
                restarted = {url for phase, url in core.segment_requests if phase == "restart"}
                require(bool(plans) and bool(plans[-1]) and set(plans[-1]) <= restarted,
                        "Fresh HLS download did not request every segment in its fresh manifest")
                require(restarted_progress["first"] in (0, 1),
                        "Fresh HLS download started with retained segment progress after cleanup")
                result["fresh_segments_requested"] = len(plans[-1])
            else:
                requests = media_requests(core, "restart")
                require(bool(requests) and (requests[0]["range"] or "bytes=0-").startswith("bytes=0-"),
                        "Fresh RAW download did not start at byte zero")
            result["fresh_download_verified"] = True
        result["stage"] = "validate"
        result["media"] = await validate_media(target, ffmpeg, media.length)
        require(not state.exists() and not (segments.exists() and any(segments.iterdir())),
                "Completed download left HLS resume artifacts")
        raw_state = Path(f"{target}.raw-state.json")
        require(not raw_state.exists() and not Path(f"{raw_state}.tmp").exists(),
                "Completed download left RAW resume artifacts")
        require(not controller.paused_store.load(), "Completed download left a stale paused job")
        result["stage"] = "completed"


async def run(args, workspace, ffmpeg):
    import base_api

    scenarios = ("pause-resume", "cleanup") if args.scenario == "all" else (args.scenario,)
    packages = ["eaf-base-api", "curl-cffi"] + [
        f"unofficial-api-for-{provider}" for provider, _, _ in args.fixtures
    ]
    report = {
        "scope": "Live CLI download/controller workflows; real libraries, HTTP requests and media",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace), "artifacts_retained": args.keep_artifacts,
        "providers": [provider for provider, _, _ in args.fixtures],
        "planned_cases": len(args.fixtures) * len(scenarios),
        "libraries": {name: version(name) for name in packages},
        "base_api_source": str(Path(base_api.__file__).resolve()),
        "results": [], "passed": 0, "failed": 0, "interrupted": False,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)

    def save_report():
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    save_report()
    log_path = args.report.with_suffix(".log")
    with log_path.open("w", encoding="utf-8") as log:
        handler = logging.StreamHandler(log)
        logging.getLogger().addHandler(handler)
        try:
            for provider, transport, url in args.fixtures:
                for scenario in scenarios:
                    number = len(report["results"]) + 1
                    print(f"[{number}/{report['planned_cases']}] RUN {provider} {scenario}", flush=True)
                    directory = workspace / provider / scenario
                    directory.mkdir(parents=True)
                    result = {"provider": provider, "transport": transport, "url": url,
                              "scenario": scenario, "passed": False,
                              "artifacts_directory": str(directory)}
                    started = time.monotonic()
                    with redirect_stdout(log), redirect_stderr(log):
                        try:
                            await check_case(provider, transport, url, scenario, directory, args.timeout, ffmpeg, result,
                                             quality=args.quality)
                            result["passed"] = True
                        except asyncio.CancelledError:
                            # asyncio.run turns the first Ctrl+C into task cancellation.
                            # check_case has already stopped its downloader and closed
                            # the real client pool before cancellation reaches here.
                            result.update(interrupted=True, error_type="CancelledError",
                                          error="Interrupted by user")
                            report["interrupted"] = True
                        except Exception as error:
                            result.update(error_type=type(error).__name__, error=str(error))
                            traceback.print_exc(file=log)
                    result["elapsed_seconds"] = round(time.monotonic() - started, 2)
                    report["results"].append(result)
                    report["passed"] = sum(case["passed"] for case in report["results"])
                    report["failed"] = sum(not case["passed"] and not case.get("interrupted", False)
                                           for case in report["results"])
                    save_report()
                    status = "STOP" if result.get("interrupted") else "PASS" if result["passed"] else "FAIL"
                    print(f"[{number}/{report['planned_cases']}] {status} "
                          f"{provider} {scenario} ({result['transport'].upper()}) "
                          f"[{result.get('stage', 'prepare')}] {result.get('error', '')}", flush=True)
                    if not args.keep_artifacts:
                        shutil.rmtree(directory)
                    if report["interrupted"]:
                        print(f"Stopped. {report['passed']} passed, {report['failed']} failed, "
                              f"1 interrupted. Partial report: {args.report}", flush=True)
                        return 130
        finally:
            logging.getLogger().removeHandler(handler)
            handler.close()
    print(f"{report['passed']} passed, {report['failed']} failed. Report: {args.report}")
    return int(report["failed"] != 0)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=("all", *PROVIDER_MODULES), action="append",
                        help="Select a provider; repeat for several. Default: all 15 providers")
    parser.add_argument("--scenario", choices=("all", "pause-resume", "cleanup"), default="all")
    parser.add_argument("--quality", type=int, metavar="HEIGHT",
                        help="Require this exact resolution (at most 720p); default: lowest available")
    parser.add_argument("--url", action="append", default=[], metavar="PROVIDER=URL",
                        help="Replace a provider's video fixture; repeat for several providers")
    parser.add_argument("--hls-url", help="Replace the PornHub video fixture")
    parser.add_argument("--raw-url", help="Replace the Eporner video fixture")
    parser.add_argument("--list", action="store_true", help="List selected fixtures/cases without network requests")
    parser.add_argument("--timeout", type=float, default=600, help="Maximum seconds per download phase")
    parser.add_argument("--report", type=Path,
                        default=Path(tempfile.gettempdir()) / "porn-fetch-download-lifecycle.json")
    parser.add_argument("--artifacts-dir", type=Path, help="Parent folder for an isolated run directory")
    parser.add_argument("--keep-artifacts", action="store_true", help="Retain media and state for inspection")
    args = parser.parse_args(argv)
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.quality is not None and not 0 < args.quality <= 720:
        parser.error("--quality must be a positive resolution at or below 720p")
    overrides = {}
    if args.hls_url:
        overrides["pornhub"] = args.hls_url
    if args.raw_url:
        overrides["eporner"] = args.raw_url
    for item in args.url:
        provider, separator, url = item.partition("=")
        if separator != "=" or provider not in PROVIDER_MODULES or not url.strip():
            parser.error("--url must be PROVIDER=URL with a supported provider and a video URL")
        overrides[provider] = url.strip()
    try:
        fixtures = lifecycle_fixtures(overrides)
    except (ValueError, AssertionError) as error:
        parser.error(str(error))
    selected = set(args.provider or ["all"])
    args.fixtures = [fixture for fixture in fixtures if "all" in selected or fixture[0] in selected]
    return args


def main():
    args = parse_args()
    if args.list:
        scenarios = ("pause-resume", "cleanup") if args.scenario == "all" else (args.scenario,)
        for provider, transport, url in args.fixtures:
            print(f"{provider:12} {transport.upper():4} {', '.join(scenarios)}\n  {url}")
        print(f"{len(args.fixtures)} providers, {len(args.fixtures) * len(scenarios)} cases. No network requests.")
        return 0
    ffmpeg = find_ffmpeg()
    if ffmpeg is None:
        raise SystemExit("FFmpeg is required for HLS remuxing and completed-media validation")
    if args.artifacts_dir:
        args.artifacts_dir.mkdir(parents=True, exist_ok=True)
    workspace = Path(tempfile.mkdtemp(prefix="porn-fetch-download-lifecycle-", dir=args.artifacts_dir))
    print(f"Live media downloads: {len(args.fixtures)} providers, {args.scenario}. Workspace: {workspace}", flush=True)
    try:
        return asyncio.run(run(args, workspace, ffmpeg))
    except KeyboardInterrupt:
        # A second Ctrl+C may interrupt cooperative shutdown itself.
        print(f"\nStopped. Last saved report: {args.report}", flush=True)
        return 130
    finally:
        if not args.keep_artifacts:
            shutil.rmtree(workspace)


if __name__ == "__main__":
    raise SystemExit(main())
