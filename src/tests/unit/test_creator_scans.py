"""Completion and identity contracts at the creator/provider boundary."""
import unittest
from types import SimpleNamespace

from src.shared.creator_library import identity, listing_item, source_url
from src.shared.creator_scans import discover
from src.shared.provider_routing import route_url


class Stream:
    def __init__(self, status):
        self.summary = SimpleNamespace(status=status, exhausted=status == "exhausted")
        self.closed = False
        self.values = iter([SimpleNamespace(url="https://www.bellesa.co/videos/1", video_id="1")])

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.values)
        except StopIteration:
            raise StopAsyncIteration

    async def aclose(self):
        self.closed = True


class CreatorScanTests(unittest.IsolatedAsyncioTestCase):
    async def test_non_exhausted_summary_cannot_be_reported_as_complete(self):
        for status in ("incomplete", "limit_reached", "failed", "cancelled"):
            stream = Stream(status)
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, "incomplete"):
                async for _ in discover(stream, route_url("https://www.bellesa.co/channels/example")):
                    pass
            self.assertTrue(stream.closed)

    async def test_complete_stream_deduplicates_and_closes(self):
        stream = Stream("exhausted")
        item = SimpleNamespace(url="https://www.bellesa.co/videos/1", video_id="1")
        stream.values = iter([item, item])
        items = [key async for key, _ in discover(stream, route_url("https://www.bellesa.co/channels/example"))]
        self.assertEqual(items, ["bellesa:video:1"])
        self.assertTrue(stream.closed)

    def test_listing_metadata_can_be_absent_without_loading_a_player(self):
        from dataclasses import dataclass
        @dataclass
        class Video:
            url: str = "https://www.bellesa.co/videos/123"
            video_id: str = "123"
            title: str = "Listing title"
            def is_field_loaded(self, name):
                if name not in self.__dataclass_fields__:
                    raise ValueError("Unknown field")
                return True
        result = listing_item(route_url("https://www.bellesa.co/channels/example"), Video())
        self.assertEqual(result["title"], "Listing title")
        self.assertEqual(result["duration"], "")
        self.assertEqual(result["published"], "")

    def test_video_identity_survives_title_and_host_variants(self):
        self.assertEqual(identity("bellesa", "https://www.bellesa.co/videos/123/old-title"), identity("bellesa", "https://bellesa.co/videos/123/new-title", "123"))
        self.assertEqual(identity("porntrex", "https://www.porntrex.com/video/123/old-title"), identity("porntrex", "https://www.porntrex.com/video/123/new-title", "123"))
        self.assertEqual(source_url("https://www.youjizz.com/most-popular/9.html"), "https://www.youjizz.com/most-popular/1.html")
        self.assertEqual(source_url("https://xhamster.com/creators/example/3?page=3"), "https://xhamster.com/creators/example")
