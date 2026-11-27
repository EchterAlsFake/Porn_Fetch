"""Offline coverage for guest playback and account collection separation."""

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from base_api import BaseCore
from base_api.modules.config import RuntimeConfig

from src.cli.downloads import download_video
from src.cli.providers import ClientPool
from src.shared.download_recovery import prepare_public_checkpoint
from src.shared.provider_routing import resolve_video, route_url
from src.shared.public_media import (
    RestrictedMediaError,
    account_video_row,
    rejected_public_media,
    require_public_media,
)
from src.shared.tor_transport import MediaCore


class PublicMediaTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_clients_do_not_share_account_cookies_or_headers(self):
        configuration = RuntimeConfig()
        configuration.cookies = {"login_fixture": "configured"}
        async with ClientPool(configuration) as pool:
            for provider in ("pornhub", "xvideos", "xhamster"):
                with self.subTest(provider=provider):
                    account = pool.account_client(provider).core
                    account.session.cookies.set("account_fixture", "session-only")
                    account.session.headers["Authorization"] = "Bearer fixture"
                    public = pool.client(provider).core
                    self.assertIsNot(public.configuration, account.configuration)
                    self.assertIsNot(public.session, account.session)
                    self.assertTrue(account.account_only)
                    self.assertFalse(public.account_only)
                    self.assertNotIn("login_fixture", public.session.cookies)
                    self.assertNotIn("account_fixture", public.session.cookies)
                    self.assertNotIn("Authorization", public.session.headers)

    def test_account_row_keeps_display_metadata_and_only_the_canonical_url(self):
        source = SimpleNamespace(
            core=SimpleNamespace(account_only=True),
            url="https://www.pornhub.com/view_video.php?viewkey=fixture&token=session#fragment",
            title="Fixture", is_private=True,
        )
        row = account_video_row(source, "pornhub")
        self.assertEqual(row.url, "https://www.pornhub.com/view_video.php?viewkey=fixture")
        self.assertEqual(row.title, "Fixture")
        self.assertEqual(row.thumbnail_url, "")
        self.assertIsNone(row.source_video)
        self.assertTrue(row.is_from_account)
        self.assertTrue(row.provider_restricted)

    async def test_guest_resolution_keeps_unknown_items_and_blocks_positive_markers(self):
        route = route_url("https://www.pornhub.com/view_video.php?viewkey=fixture")
        video = SimpleNamespace(url=route.url, is_premium=None)
        client = SimpleNamespace(get_video=AsyncMock(return_value=video))
        self.assertIs(await resolve_video(client, route), video)
        video.is_premium = True
        with self.assertRaises(RestrictedMediaError):
            await resolve_video(client, route)
        client.get_video.reset_mock()
        restricted = route_url("https://www.pornhubpremium.com/view_video.php?viewkey=fixture")
        with self.assertRaises(RestrictedMediaError):
            await resolve_video(client, restricted)
        client.get_video.assert_not_awaited()

    async def test_download_dispatch_rejects_account_media_before_creating_files(self):
        source = SimpleNamespace(core=SimpleNamespace(account_only=True), download=AsyncMock())
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "new-folder" / "fixture.mp4"
            with self.assertRaises(RestrictedMediaError):
                await download_video(source, output, "240", None, has_premium=False)
            self.assertFalse(output.parent.exists())
        source.download.assert_not_awaited()

    async def test_public_transport_rejects_known_hosts_and_closes_restricted_redirects(self):
        core = MediaCore(RuntimeConfig())
        response = SimpleNamespace(
            url="https://www.xvideos.red/fixture", aclose=AsyncMock(), quit_now=asyncio.Event(),
        )
        request = AsyncMock(return_value=response)
        core.session = SimpleNamespace(request=request)
        with patch.object(BaseCore, "initialize_session"):
            core.initialize_session()
            with self.assertRaises(RestrictedMediaError):
                await core.session.request("GET", "https://www.xvideos.red/fixture", stream=True)
            request.assert_not_awaited()
            with self.assertRaises(RestrictedMediaError):
                await core.session.request("GET", "https://www.xvideos.com/fixture", stream=True)
        request.assert_awaited_once()
        response.aclose.assert_awaited_once()
        self.assertTrue(response.quit_now.is_set())

    async def test_renewed_core_keeps_guest_routing_and_validation(self):
        initial = MediaCore(RuntimeConfig())
        renewed = initial.clone_for_retry(RuntimeConfig())
        self.assertFalse(renewed.account_only)
        self.assertIs(renewed.routing_settings, initial.routing_settings)
        self.assertIs(renewed.tor_manager, initial.tor_manager)
        with self.assertRaises(RestrictedMediaError):
            renewed.validate_playback("https://www.pornhub.com/view_video.php?viewkey=fixture", is_premium=True)
        require_public_media(SimpleNamespace(core=renewed))

    def test_wrapped_http_rejection_is_distinct_from_a_timeout(self):
        error = RuntimeError()
        rejection = RuntimeError()
        rejection.status_code = 403
        error.__cause__ = rejection
        self.assertTrue(rejected_public_media(error))
        self.assertFalse(rejected_public_media(TimeoutError()))

    def test_resume_preserves_only_checkpoints_created_by_the_same_guest_download(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            output = folder / "fixture.mp4"
            raw_state = folder / "fixture.mp4.raw-state.json"
            checkpoint = folder / "state"
            segments = folder / "segments"
            segments.mkdir()
            (segments / "0001.ts").write_bytes(b"legacy segment")
            for path in (output, raw_state, checkpoint):
                path.write_bytes(b"legacy partial")
            url = "https://www.xvideos.com/fixture"
            prepare_public_checkpoint(output, checkpoint, segments, url, "240")
            for path in (output, raw_state, checkpoint, segments):
                self.assertFalse(path.exists())
                self.assertEqual(len(list(folder.glob(f"{path.name}.unverified-*"))), 1)
            checkpoint.write_bytes(b"guest partial")
            prepare_public_checkpoint(output, checkpoint, segments, url, "240")
            self.assertEqual(checkpoint.read_bytes(), b"guest partial")
            prepare_public_checkpoint(output, checkpoint, segments, url, "360")
            self.assertFalse(checkpoint.exists())
