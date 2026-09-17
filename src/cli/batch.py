"""Argument parsing and headless CLI execution."""
from __future__ import annotations

import argparse
import asyncio
import sys

from src.backend.media import select_allowed_quality
from src.backend.error_reporting import report_exception
from .downloads import download_gallery, download_video
from .licensing import create_license_service
from .media import prepare_video
from .model_store import ModelStore
from .providers import ContentKind, ClientPool, PROVIDER_MODULES, route_url
from .settings import CliSettings, SettingsStore, prompt_error_reporting_consent
from .output import output_path_for


ACTION_DESTINATIONS = {
    "url", "model", "playlist", "add_model_to_database", "remove_model_from_database",
    "update_pending_urls", "update_models", "test_mode", "info", "quality", "output",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Porn_Fetch_CLI.py",
        description="Porn Fetch terminal application and batch downloader (search is not supported).",
    )
    parser.add_argument("--batch", action="store_true", help="force headless compatibility mode")
    parser.add_argument("--interactive", "-i", action="store_true", help="launch interactive terminal wizard")
    parser.add_argument("--info", action="store_true", help="show CLI usage and supported content types")
    parser.add_argument("--test-mode", action="store_true", help="run deterministic offline self-test")
    parser.add_argument("--url", action="append", default=[], help="video or album URL (repeatable)")
    parser.add_argument("--model", "--profile", dest="model", action="append", default=[], help="profile URL (repeatable)")
    parser.add_argument("--playlist", "--collection", dest="playlist", action="append", default=[], help="collection URL (repeatable)")
    parser.add_argument("--quality", help="quality override for this invocation")
    parser.add_argument("--output", help="output directory override for this invocation")
    parser.add_argument("--auto-process", "--auto_process", dest="auto_process", action="store_true", help="download every discovered item")
    parser.add_argument("--ignore-errors", "--ignore_errors", dest="ignore_errors", action="store_true", help="continue after a failed item")
    parser.add_argument(
        "--error-reporting",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="enable or disable redacted error reports and remember the choice",
    )
    parser.add_argument("--add-model-to-database", action="append", default=[], metavar="URL")
    parser.add_argument("--remove-model-from-database", action="append", default=[], metavar="URL")
    parser.add_argument("--update-pending-urls", action="store_true")
    parser.add_argument("--update-models", action="store_true")
    return parser


def has_action(args: argparse.Namespace) -> bool:
    return bool(args.batch or any(getattr(args, name, None) for name in ACTION_DESTINATIONS))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.info:
        parser.print_help()
        return 0
    if args.test_mode:
        return offline_self_test()

    raw_args = sys.argv[1:] if argv is None else argv
    is_interactive = getattr(args, "interactive", False) or len(raw_args) == 0

    if is_interactive:
        from .wizard import run_wizard
        return asyncio.run(run_wizard(args))

    return asyncio.run(run_batch(args))


def offline_self_test() -> int:
    """Packaged-build smoke test: no sessions, DNS, credentials or downloads."""
    examples = {
        "pornhub": "https://www.pornhub.com/view_video.php?viewkey=test",
        "eporner": "https://www.eporner.com/hd-porn/test/title/",
        "xnxx": "https://www.xnxx.com/video-test/title",
        "xvideos": "https://www.xvideos.com/video.test/title",
        "xhamster": "https://xhamster.com/videos/title-test",
        "spankbang": "https://spankbang.com/test/video/title",
        "youporn": "https://www.youporn.com/watch/test/title/",
        "beeg": "https://beeg.com/-test",
        "porntrex": "https://www.porntrex.com/video/test/title/",
        "xfreehd": "https://xfreehd.com/video/test/title",
        "redtube": "https://www.redtube.com/test",
        "thumbzilla": "https://www.thumbzilla.com/video/test/title",
        "tube8": "https://www.tube8.com/test/test/test/",
    }
    assert set(PROVIDER_MODULES) == set(examples)
    assert all(route_url(url).provider == provider for provider, url in examples.items())
    settings = CliSettings()
    settings.validate()
    assert select_allowed_quality("best", [360, 720, 1080], False) == "720"
    assert route_url("https://xfreehd.com/album/123/example").kind == ContentKind.GALLERY
    print("Porn Fetch CLI offline self-test passed")
    return 0


async def run_batch(args: argparse.Namespace) -> int:
    store = SettingsStore()
    persisted = store.load()
    explicit_reporting_choice = getattr(args, "error_reporting", None)
    if explicit_reporting_choice is not None:
        persisted = persisted.overridden(
            error_reporting=explicit_reporting_choice,
            error_reporting_decided=True,
        )
        store.save(persisted)
    elif not persisted.error_reporting_decided:
        if sys.stdin.isatty() and sys.stderr.isatty():
            persisted = await prompt_error_reporting_consent(persisted, store)
        else:
            print(
                "Error reporting is disabled because no consent choice has been saved. "
                "Use --error-reporting or --no-error-reporting to save a choice.",
                file=sys.stderr,
            )

    settings = persisted.overridden(
        quality=args.quality,
        output_path=args.output,
    )
    models = ModelStore()
    for url in args.add_model_to_database:
        models.add(url)
    for url in args.remove_model_from_database:
        models.remove(url)

    pool = ClientPool(settings.to_runtime_config())
    license_service = create_license_service(settings.to_runtime_config())
    failures = 0
    try:
        license_status = await license_service.check()
        if args.update_pending_urls:
            for model_url, _ in models.models():
                failures += await _scan_model(pool, models, model_url, settings, args.ignore_errors)
        if args.update_models:
            for model_url, state in models.models():
                pending = list(state["pending"])
                outcomes = await _download_many(pool, pending, settings, license_status.allowed)
                for video_url, outcome in zip(pending, outcomes):
                    if outcome:
                        models.mark_downloaded(model_url, video_url)
                    else:
                        failures += 1

        direct_outcomes = await _download_many(pool, args.url, settings, license_status.allowed)
        for outcome in direct_outcomes:
            if not outcome:
                failures += 1
                if not args.ignore_errors:
                    break
        for source_url in [*args.model, *args.playlist]:
            try:
                prepared = []
                async for source in pool.media_stream(source_url, pages=5):
                    route = route_url(source_url)
                    prepared.append(await prepare_video(source, route.provider))
                    if len(prepared) >= settings.result_limit:
                        break
                semaphore = asyncio.Semaphore(settings.parallel_downloads)
                async def dispatch(media):
                    async with semaphore:
                        if settings.processing_delay:
                            await asyncio.sleep(settings.processing_delay)
                        return await _download_prepared(media, settings, license_status.allowed)
                for outcome in await asyncio.gather(*(dispatch(media) for media in prepared)):
                    if not outcome:
                        failures += 1
                        if not args.ignore_errors:
                            break
            except Exception as error:
                failures += 1
                report_id = await report_exception(
                    error,
                    operation="scrape profile or collection",
                    location="src.cli.batch.run_batch",
                    context={"source_url": source_url},
                    enabled=settings.error_reporting,
                )
                print(f"Failed: {source_url}: {error} [error {report_id}]", file=sys.stderr)
                if not args.ignore_errors:
                    break
    finally:
        await license_service.close()
        await pool.close()
    return 1 if failures else 0


async def _download_many(
    pool: ClientPool, urls: list[str], settings: CliSettings, premium: bool,
) -> list[bool]:
    semaphore = asyncio.Semaphore(settings.parallel_downloads)

    async def dispatch(url: str) -> bool:
        async with semaphore:
            if settings.processing_delay:
                await asyncio.sleep(settings.processing_delay)
            return await _download_url(pool, url, settings, premium)

    return list(await asyncio.gather(*(dispatch(url) for url in urls)))


async def _scan_model(
    pool: ClientPool, store: ModelStore, model_url: str,
    settings: CliSettings, ignore_errors: bool,
) -> int:
    urls: list[str] = []
    try:
        async for video in pool.media_stream(model_url, pages=5):
            url = getattr(video, "url", None)
            if url:
                urls.append(str(url))
            if len(urls) >= settings.result_limit:
                break
        store.update_pending(model_url, urls)
        return 0
    except Exception as error:
        report_id = await report_exception(
            error,
            operation="scan tracked model",
            location="src.cli.batch._scan_model",
            context={"model_url": model_url},
            enabled=settings.error_reporting,
        )
        print(f"Failed to scan {model_url}: {error} [error {report_id}]", file=sys.stderr)
        if not ignore_errors:
            raise
        return 1


async def _download_url(pool: ClientPool, url: str, settings: CliSettings, premium: bool) -> bool:
    try:
        route, source = await pool.resolve(url)
        if route.kind == ContentKind.GALLERY:
            result = await download_gallery(
                source, settings.output_path, concurrency=settings.videos_concurrency,
                progress=lambda value: _print_progress(url, value),
            )
            if result.status not in {"completed", "cancelled"}:
                await report_exception(
                    RuntimeError(f"Gallery downloader returned status {result.status}"),
                    operation="download gallery",
                    location="src.cli.batch._download_url",
                    context={"source_url": url, "provider": route.provider},
                    enabled=settings.error_reporting,
                )
            return result.status == "completed"
        media = await prepare_video(source, route.provider)
        return await _download_prepared(media, settings, premium)
    except Exception as error:
        report_id = await report_exception(
            error,
            operation="resolve and download URL",
            location="src.cli.batch._download_url",
            context={"video_url": url},
            enabled=settings.error_reporting,
        )
        print(f"Failed: {url}: {error} [error {report_id}]", file=sys.stderr)
        return False


async def _download_prepared(media, settings: CliSettings, premium: bool) -> bool:
    quality = select_allowed_quality(settings.quality, media.qualities, premium)
    if not quality:
        print(f"No permitted quality is available for {media.title}", file=sys.stderr)
        return False
    target = output_path_for(media, settings)
    result = await download_video(
        media.source_video, target, quality, settings, has_premium=premium,
        available_qualities=media.qualities,
        progress=lambda value: _print_progress(media.title, value),
    )
    if result.status == "completed" and settings.write_metadata and not result.skipped:
        try:
            from src.backend.metadata import write_tags
            write_tags(str(result.path), media)
        except Exception as error:
            report_id = await report_exception(
                error,
                operation="write downloaded video metadata",
                location="src.cli.batch._download_prepared",
                context={
                    "video_url": getattr(media, "url", None),
                    "provider": type(getattr(media, "source_video", None)).__module__,
                },
                enabled=settings.error_reporting,
            )
            print(f"Metadata warning for {media.title}: {error} [error {report_id}]", file=sys.stderr)
    print(f"{result.status}: {media.title}")
    if result.status not in {"completed", "cancelled"}:
        await report_exception(
            RuntimeError(f"Downloader returned status {result.status}"),
            operation="download prepared video",
            location="src.cli.batch._download_prepared",
            context={
                "video_url": getattr(media, "url", None),
                "provider": type(getattr(media, "source_video", None)).__module__,
                "quality": quality,
            },
            enabled=settings.error_reporting,
        )
    return result.status == "completed"


def _print_progress(label: str, value: int | None) -> None:
    shown = "…" if value is None else f"{value}%"
    print(f"\r{label}: {shown}", end="", flush=True)
