"""Offline contracts for the opt-in metadata-only GUI profile diagnostics."""
from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

os.environ.setdefault("PORN_FETCH_TEST_ENV", "1")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from base_api import BaseCore

from src.backend.profile_diagnostics import (
    MetadataOnlyRequests,
    ProfileFeedUnavailable,
    fixture_path,
    load_profile_cases,
    make_test_backend,
    test_profile_url,
    verify_stream,
)
from src.shared.media import VideoObject
from src.shared.provider_routing import eporner_video_id, resolve_container, resolve_video, route_url


class ProfileDiagnosticTests(unittest.IsolatedAsyncioTestCase):
    async def test_profile_rows_keep_normalized_minutes_and_current_row_numbers(self):
        backend = make_test_backend()
        model = backend._downloads_model
        case = {"url": "https://pornhub.com/model/example", "provider": "pornhub"}

        def prepared(identifier):
            return VideoObject(
                url="https://pornhub.com/view_video.php?viewkey=example",
                title="Example", author="Author", length=12, tags=[],
                thumbnail_url="https://images.example/thumbnail.jpg", video_id=identifier,
                publish_date=None, qualities=[720], status="pending", identifier=identifier,
                index=1, source_video=object(), output_path=Path("unused-profile-test.mp4"),
                origin_iterator_url=case["url"], origin_iterator_name="Example",
            )

        # Reusing a list must not restart its display numbering on each fetch.
        model.add_video(prepared("existing"), "720")

        async def process(*args, **kwargs):
            model.add_video(prepared("new"), "720")

        backend._process_model_url = AsyncMock(side_effect=process)
        with patch("src.backend.profile_diagnostics.resolve_container",
                   AsyncMock(return_value=SimpleNamespace(name="Example"))), \
                patch("src.backend.profile_diagnostics.verify_stream",
                      AsyncMock(return_value={"kind": "direct", "url_resolved": True})):
            result = await test_profile_url(backend, model, case)
        self.assertEqual(result["rows"], 1)
        self.assertEqual(model.data(model.index(1, 0), model.TitleRole), "2) Example")
        self.assertEqual(model.data(model.index(1, 0), model.DurationRole), "12 min")

    def test_every_primary_branch_and_replacement_is_recorded(self):
        primary = load_profile_cases()
        self.assertEqual(len(primary), 33)
        self.assertEqual(len({case["provider"] for case in primary}), 13)
        self.assertTrue(all(case["expected_factory"] and case["sources"] for case in primary))
        all_cases = load_profile_cases(include_variants=True)
        self.assertTrue(any(case["http"]["status"] == 403 for case in all_cases))
        self.assertFalse(any(case["http"]["status"] in (0, 404) for case in all_cases))
        manifest = json.loads(fixture_path().read_text())
        by_id = {case["id"]: case for case in manifest["cases"]}
        excluded = [case for case in manifest["cases"] if not case["positive_smoke_candidate"]]
        self.assertEqual(len(excluded), 9)
        for case in excluded:
            self.assertTrue(by_id[case["replaced_by"]]["positive_smoke_candidate"])
            self.assertIn(case["id"], by_id[case["replaced_by"]]["replaces"])

    async def test_guard_blocks_downloads_before_transport_but_allows_playlists(self):
        transport = AsyncMock(return_value="metadata")
        core = BaseCore.__new__(BaseCore)
        with patch.object(BaseCore, "request", transport):
            with MetadataOnlyRequests() as guard:
                with self.assertRaises(AssertionError):
                    await core.request("https://cdn.example/segment.ts")
                with self.assertRaises(AssertionError):
                    await core.download(None)
                with self.assertRaises(AssertionError):
                    await core.fetch_bytes("https://cdn.example/opaque-stream")
                transport.assert_not_awaited()
                await core.request("https://cdn.example/video.mp4/master.m3u8")
                self.assertEqual(transport.await_count, 1)
                self.assertEqual(len(guard.blocked), 3)
            self.assertIs(BaseCore.request, transport)

    async def test_segments_are_resolved_without_fetching_them(self):
        source = SimpleNamespace(
            m3u8_base_url="https://cdn.example/master.m3u8",
            core=SimpleNamespace(get_segments=AsyncMock(return_value=["https://cdn.example/segment.ts"])),
        )
        self.assertEqual(await verify_stream(source, "720"), {"kind": "hls", "segments": 1})
        source.core.get_segments.assert_awaited_once_with(source.m3u8_base_url, "720")

    async def test_youporn_direct_fallback_is_never_read_as_a_playlist(self):
        from src.backend.clients import yp_Video

        source = Mock(spec=yp_Video)
        source.is_hls = False
        source.m3u8_base_url = "https://cdn.example/video.mp4"
        source.core.get_segments = AsyncMock()
        self.assertEqual(await verify_stream(source, "best"), {"kind": "direct", "url_resolved": True})
        source.core.get_segments.assert_not_awaited()

    async def test_localized_eporner_and_ajax_tab_identity_dispatch(self):
        client = SimpleNamespace(
            get_pornstar=AsyncMock(return_value=SimpleNamespace(resolved_url=None)),
            get_channel=AsyncMock(return_value=SimpleNamespace(resolved_url=None)),
            get_model=AsyncMock(return_value=SimpleNamespace(resolved_url=None)),
        )
        await resolve_container(client, route_url("https://de.eporner.com/pornostar/riley-reid/"))
        client.get_pornstar.assert_awaited_once()
        await resolve_container(client, route_url("https://www.xvideos.com/channels/Teddy/videos/best/0?q=hd#videos"))
        client.get_channel.assert_awaited_once_with("https://www.xvideos.com/channels/Teddy?q=hd", load_html=True)
        route = route_url("https://pornhub.com/model/Example/videos/upload?o=mr#videos")
        self.assertEqual(route.profile_mode, "uploads")
        await resolve_container(client, route)
        client.get_model.assert_awaited_once_with("https://pornhub.com/model/Example?o=mr", load_html=True)

    async def test_localized_video_ids_keep_their_case(self):
        url = "https://de.eporner.com/porno-video/AbC123xyZ/title/"
        self.assertEqual(eporner_video_id(url), "AbC123xyZ")
        client = SimpleNamespace(get_video=AsyncMock())
        await resolve_video(client, route_url(url))
        client.get_video.assert_awaited_once_with(
            "https://de.eporner.com/video-AbC123xyZ/", load_html=True, load_api=True,
        )

    async def test_xhamster_user_follows_its_linked_creator_identity(self):
        user, creator = SimpleNamespace(name="User"), SimpleNamespace(name="Creator")
        client = SimpleNamespace(
            get_creator=AsyncMock(side_effect=[user, creator]),
            core=SimpleNamespace(fetch_text=AsyncMock(return_value='''
                <a href="/creators/recommendation">Suggested creator</a>
                <div class="personal-info-block"><div class="user-details">
                    <a href="/creators/actual-creator">Creator profile</a>
                </div></div>
            ''')),
        )
        target = await resolve_container(client, route_url("https://xhamster.com/users/example"))
        self.assertIs(target, creator)
        self.assertEqual(client.get_creator.await_args_list[-1].args, ("https://xhamster.com/creators/actual-creator",))

    async def test_restricted_feed_is_attempted_and_unrelated_errors_still_fail(self):
        case = next(dict(case) for case in load_profile_cases() if case["id"] == "tube8.user")
        case["expected_factory"] = None
        backend = make_test_backend()
        backend._process_model_url = AsyncMock(side_effect=RuntimeError("Main video container not found"))
        with patch("src.backend.profile_diagnostics.resolve_container", AsyncMock(return_value=SimpleNamespace(name="Example"))):
            with self.assertRaises(ProfileFeedUnavailable) as skipped:
                await test_profile_url(backend, backend._downloads_model, case)
            self.assertTrue(skipped.exception.metadata["feed_attempted"])
            backend._process_model_url.assert_awaited_once()
            backend._process_model_url.side_effect = RuntimeError("DNS lookup failed")
            with self.assertRaisesRegex(RuntimeError, "DNS lookup failed"):
                await test_profile_url(backend, backend._downloads_model, case)
