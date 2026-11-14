from __future__ import annotations

import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from src.cli.downloads import DownloadController, download_video
from src.cli.settings import CliSettings
from src.shared.library_export import (
    ExportOptions,
    export_library_bundle,
    finalize_video,
    library_video_path,
    load_export,
    nfo_bytes,
    prepare_existing_export,
)
from src.shared.library_metadata import Credit, LibraryMetadata
from src.shared.media import VideoObject
from src.shared.provider_metadata import PROVIDER_FIELDS, collect_library_metadata, source_identity
from src.shared.provider_routing import PROVIDER_MODULES


def video(url="https://www.bellesa.co/videos/123", source=None):
    return VideoObject(url=url, title="Example & <scene>", author="Uploader", length=2,
                       tags=[], thumbnail_url="", video_id="title-is-not-an-id", publish_date=None,
                       qualities=[720], status="Pending", source_video=source)


class ProviderMetadataTests(unittest.TestCase):
    def test_every_registered_provider_has_an_explicit_mapping(self):
        self.assertEqual(set(PROVIDER_FIELDS), set(PROVIDER_MODULES))
        for provider in PROVIDER_MODULES:
            with self.subTest(provider=provider):
                source = SimpleNamespace(title="Title", duration=67, length="01:07", length_seconds=67,
                                         tags=["Tag"], categories=[{"name": "Category"}], pornstars=["Actor"],
                                         performers=[{"name": "Actor", "url": "/profile/actor"}],
                                         pornstars_names=["Actor"], author_name="Uploader", author="Uploader")
                prepared = video()
                metadata = collect_library_metadata(provider, source, prepared)
                self.assertEqual(metadata.title, prepared.title)
                self.assertEqual(metadata.producers, [])
                if provider in {"thumbzilla", "tube8", "spankbang", "xnxx", "xfreehd", "porntrex", "redgifs", "youjizz", "beeg"}:
                    self.assertFalse(metadata.performers)

    def test_credits_are_not_inferred_from_author_and_artwork_urls_are_transient(self):
        source = SimpleNamespace(author="Credited supplier", author_link="/channels/supplier", pornstars=["Actor"],
                                 description="Example & <scene>", thumbnail_url="https://cdn.example/cover.webp?token=secret",
                                 publish_date="2026-10-01T12:00:00Z", duration=121)
        metadata = collect_library_metadata("bellesa", source, video(source=source))
        self.assertEqual(metadata.content_providers[0].name, "Credited supplier")
        self.assertEqual(metadata.performers[0].name, "Actor")
        self.assertIsNone(metadata.uploader)
        self.assertIsNone(metadata.description)
        self.assertNotIn("secret", json.dumps(metadata.portable()))
        self.assertIsNone(ET.fromstring(nfo_bytes(metadata, ExportOptions())).find("studio"))

    def test_ambiguous_and_relative_dates_are_not_exported(self):
        for provider, raw in [("beeg", "2026-10-01"), ("xnxx", "2026-10-01"), ("xvideos", "2026-10-01"), ("redtube", "3 years ago")]:
            with self.subTest(provider=provider):
                metadata = collect_library_metadata(provider, SimpleNamespace(publish_date=raw), video())
                self.assertIsNone(metadata.publication_date)
                self.assertEqual(metadata.publication_raw, raw)
        metadata = collect_library_metadata("xhamster", SimpleNamespace(created_timestamp=1790856000, date_ago="2 years ago"), video())
        self.assertIsNotNone(metadata.publication_date)

    def test_direct_and_listing_identifiers_use_public_identity(self):
        for provider, url in [("xnxx", "https://xnxx.com/video-abc/title"), ("xvideos", "https://xvideos.com/video.abc/title")]:
            self.assertEqual(source_identity(provider, url), source_identity(provider, url, SimpleNamespace(video_id="999", title="Title")))
        self.assertEqual(source_identity("xhamster", "https://xhamster.com/videos/title-xhABC")[1], "xhABC")
        self.assertEqual(source_identity("xhamster", "https://xhamster.com/videos/changed-title-xhABC")[1], "xhABC")
        self.assertEqual(source_identity("pornhub", "https://pornhub.com/shorties/key")[0], "short")

    def test_nfo_escapes_text_and_keeps_explicit_producer_and_cast(self):
        metadata = LibraryMetadata("bellesa", "video", "123", "https://bellesa.co/videos/123", "A & <B>",
                                   producers=[Credit("Producer")], performers=[Credit("Actor")], tags=["A & B"])
        root = ET.fromstring(nfo_bytes(metadata, ExportOptions()))
        self.assertEqual(root.findtext("title"), "A & <B>")
        self.assertEqual(root.findtext("studio"), "Producer")
        self.assertEqual(root.findtext("actor/name"), "Actor")
        self.assertEqual(root.findtext("uniqueid"), "bellesa:video:123")


class LibraryExportTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "example.mp4"
        self.path.write_bytes(b"original video bytes")
        self.metadata = LibraryMetadata("bellesa", "video", "123", "https://bellesa.co/videos/123", "Example",
                                        image_url="https://cdn.example/image?token=secret")
        self.options = ExportOptions("jellyfin")

    async def test_export_offline_regeneration_and_preserved_manual_edit(self):
        core = SimpleNamespace(fetch_bytes=AsyncMock(return_value=b"\xff\xd8\xffimage"))
        result = await export_library_bundle(self.path, self.metadata, self.options, premium=True, core=core)
        self.assertEqual(len(result.files), 3)
        snapshot, _ = load_export(self.path)
        self.assertIsNone(snapshot.image_url)
        nfo = self.path.with_suffix(".nfo")
        nfo.write_text("<movie><title>Manual edit</title></movie>")
        settings = SimpleNamespace(metadata_genres=False, metadata_studio_fallback=False)
        resolver = AsyncMock(side_effect=AssertionError("Offline regeneration must not fetch the provider"))
        saved, empty_core, options = await prepare_existing_export(self.path, "", settings, premium=True, resolve_source=resolver)
        self.assertIsNone(empty_core)
        result = await export_library_bundle(self.path, saved, options, premium=True)
        self.assertEqual(ET.parse(nfo).findtext("title"), "Manual edit")
        self.assertTrue(result.warnings)
        self.assertEqual(self.path.read_bytes(), b"original video bytes")
        self.assertNotIn("secret", self.path.with_suffix(".pornfetch.json").read_text())

    async def test_dry_run_and_premium_enforcement_do_not_write(self):
        with self.assertRaises(PermissionError):
            await export_library_bundle(self.path, self.metadata, self.options, premium=False)
        result = await export_library_bundle(self.path, self.metadata, self.options, premium=True, dry_run=True)
        self.assertEqual(result["identity"], self.metadata.identity)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    async def test_cli_metadata_only_uses_saved_json_and_prints_preview(self):
        from src.cli.batch import _metadata_actions, build_parser
        await export_library_bundle(self.path, self.metadata, self.options, premium=True)
        args = build_parser().parse_args(["--export-metadata-for", str(self.path), "--dry-run"])
        pool = SimpleNamespace(resolve=AsyncMock(side_effect=AssertionError("No provider resolution expected")))
        output = io.StringIO()
        with redirect_stdout(output):
            status = await _metadata_actions(args, pool, CliSettings(write_metadata=False), True)
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output.getvalue())["identity"], self.metadata.identity)
        pool.resolve.assert_not_awaited()

    async def test_artwork_failure_does_not_lose_metadata_or_video(self):
        core = SimpleNamespace(fetch_bytes=AsyncMock(side_effect=OSError("unavailable")))
        result = await export_library_bundle(self.path, self.metadata, self.options, premium=True, core=core)
        self.assertTrue(result.warnings)
        self.assertTrue(self.path.with_suffix(".nfo").exists())
        self.assertTrue(self.path.exists())

    async def test_metadata_only_does_not_prepare_streams(self):
        source = SimpleNamespace(url=self.metadata.source_url, title="Example", core=object(), description="Description")
        resolver = AsyncMock(return_value=source)
        snapshot, _, options = await prepare_existing_export(self.path, self.metadata.source_url, SimpleNamespace(),
                                                             premium=True, resolve_source=resolver)
        self.assertEqual(snapshot.description, "Description")
        self.assertEqual(options.layout, "alongside")
        self.assertIsNone(snapshot.duration_seconds)

    async def test_server_failure_is_separate_from_saved_bundle(self):
        media = video()
        media.library_metadata = self.metadata
        settings = SimpleNamespace(metadata_export="jellyfin", write_metadata=False, jellyfin_url="http://server")
        with patch("src.shared.jellyfin.notify_jellyfin", AsyncMock(side_effect=OSError("offline"))):
            result = await finalize_video(self.path, media, settings, premium=True)
        self.assertIsNotNone(result.export.notification_error)
        self.assertTrue(self.path.with_suffix(".nfo").is_file())

    async def test_scene_layout_is_idempotent(self):
        media = video()
        media.library_metadata = self.metadata
        options = ExportOptions("jellyfin", "scene-folder")
        target = library_video_path(self.path, media, options)
        self.assertEqual(target, library_video_path(target, media, options))
        self.assertIn("bellesa-video-123", target.name)

    async def test_cli_keeps_metadata_title_and_sanitizes_only_the_path(self):
        from src.cli.media import prepare_video
        from src.cli.output import output_path_for
        source = SimpleNamespace(loader_methods={}, title='A / title. Part 2', url='https://www.xvideos.com/video.abc/title',
                                 video_qualities=[720], tags=[], author_name='Uploader')
        media = await prepare_video(source, 'xvideos')
        self.assertEqual(media.title, 'A / title. Part 2')
        self.assertEqual(media.library_metadata.title, media.title)
        target = output_path_for(media, CliSettings(output_path=str(self.path.parent)))
        self.assertEqual(target.name, 'A _ title. Part 2.mp4')
        self.assertEqual(target.parent, self.path.parent)

    async def test_download_completion_exports_and_cancelled_download_does_not(self):
        class Source:
            async def download(inner, configuration, **kwargs):
                Path(configuration.path).write_bytes(b"completed provider fixture")
                return SimpleNamespace(status=inner.status, metadata_written=True)

        Source.__module__ = "eporner_api.api"
        source = Source()
        source.status = "completed"
        media = video(source=source)
        media.library_metadata = self.metadata
        target = self.path.parent / "new.mp4"
        settings = CliSettings(write_metadata=False, metadata_export="jellyfin", metadata_layout="scene-folder")
        controller = DownloadController(target=target, state_directory=self.path.parent / "state")
        result = await download_video(source, target, "720", settings, has_premium=True, available_qualities=[720],
                                      controller=controller, metadata=media)
        self.assertEqual(result.status, "completed")
        self.assertTrue((result.path.parent / "movie.nfo").is_file())
        self.assertEqual(result.path.parent.name, result.path.stem)
        source.status = "cancelled"
        media.library_metadata = LibraryMetadata("bellesa", "video", "456", self.metadata.source_url, "Cancelled")
        other = self.path.parent / "cancelled.mp4"
        result = await download_video(source, other, "720", settings, has_premium=True, available_qualities=[720],
                                      controller=DownloadController(target=other, state_directory=self.path.parent / "state2"), metadata=media)
        self.assertEqual(result.status, "cancelled")
        self.assertFalse((result.path.parent / "movie.nfo").exists())


if __name__ == "__main__":
    unittest.main()
