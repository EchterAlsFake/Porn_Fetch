"""Gallery diagnostics must reject missing images and downloaded error pages."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from xfreehd_api import Album

from src.cli.downloads import download_gallery
from src.cli.selftest.downloads import test_active_gallery_download
from src.cli.selftest.online import test_gallery


class GalleryDiagnosticsTests(unittest.IsolatedAsyncioTestCase):
    async def test_xfreehd_photo_pages_are_resolved_before_saving_image_bytes(self):
        photo_url = "https://beta.xfreehd.com/photo/123/"
        image_url = "https://image.xfreehd.com/media/photos/123.jpg"
        core = SimpleNamespace(
            fetch_text=AsyncMock(return_value=f'<img class="img-responsive-mw" src="{image_url}">'),
            fetch_bytes=AsyncMock(return_value=b"\xff\xd8\xffsample"),
        )
        album = Album(url="https://beta.xfreehd.com/album/123/", core=core)
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(Album, "_load_html", AsyncMock(return_value={"title": "Example", "total_pages_count": 1})), \
                patch.object(Album, "get_all_images", AsyncMock(return_value=[photo_url])):
            outcome = await download_gallery(album, directory)
            self.assertEqual((outcome.path / "0001.jpg").read_bytes(), b"\xff\xd8\xffsample")
        core.fetch_text.assert_awaited_once_with(photo_url)
        core.fetch_bytes.assert_awaited_once_with(image_url)

    def pool(self, *, title="Example album", images=None):
        album = SimpleNamespace(title=title, get_all_images=AsyncMock(return_value=images or []))
        return SimpleNamespace(resolve=AsyncMock(return_value=(None, album)))

    async def test_metadata_rejects_missing_title_or_empty_image_list(self):
        for pool in (self.pool(title=None, images=["https://images.example/1.jpg"]), self.pool()):
            result = await test_gallery("Example", "https://example.test/album", pool)
            self.assertFalse(result.passed)
        result = await test_gallery("Example", "https://example.test/album",
                                    self.pool(images=["https://images.example/1.jpg"]))
        self.assertTrue(result.passed)

    async def test_download_checks_image_bytes_instead_of_only_completed_status(self):
        for content, passed in ((b"<html>Access denied</html>", False), (b"\xff\xd8\xffsample", True)):
            with self.subTest(passed=passed), tempfile.TemporaryDirectory() as directory:
                path = Path(directory)
                (path / "0001.jpg").write_bytes(content)
                outcome = SimpleNamespace(status="completed", path=path)
                with patch("src.cli.selftest.downloads.download_gallery", AsyncMock(return_value=outcome)):
                    result = await test_active_gallery_download(
                        "Example", "https://example.test/album", self.pool(images=["https://images.example/1.jpg"]),
                    )
                self.assertEqual(result.passed, passed)
