"""XVideos rows should use existing uploader metadata before fetching a profile."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from src.backend import clients


class XvideosMetadataTests(unittest.IsolatedAsyncioTestCase):
    def fixture(self, *, name):
        class MetadataFixture(SimpleNamespace):
            @property
            def get_author(self):
                async def load():
                    self.author_calls += 1
                    return SimpleNamespace(name="Legacy studio")
                return load()

        return MetadataFixture(loader_methods={}, title="Example", url="https://www.xvideos.com/video.example/title",
                               author_name=name, author_calls=0, length="10:00", tags=[], publish_date=None,
                               thumbnail_url="", video_qualities=[240, 720])

    async def test_video_uploader_does_not_fetch_channel_statistics(self):
        source = self.fixture(name="Studio 日本語")
        with patch.object(clients, "xv_Video", type(source)):
            metadata = await clients.load_video_attributes(source)
        self.assertEqual(metadata.author, "Studio 日本語")
        self.assertEqual(source.author_calls, 0)

    async def test_older_library_or_absent_video_name_keeps_native_author_lookup(self):
        for missing in (False, True):
            with self.subTest(missing=missing):
                source = self.fixture(name=None)
                if missing:
                    del source.author_name
                with patch.object(clients, "xv_Video", type(source)):
                    metadata = await clients.load_video_attributes(source)
                self.assertEqual(metadata.author, "Legacy studio")
                self.assertEqual(source.author_calls, 1)
