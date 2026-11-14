import asyncio
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.shared.jellyfin import _batches, api_key, notify_jellyfin, save_api_key, server_path


class JellyfinTests(unittest.IsolatedAsyncioTestCase):
    async def test_batch_and_server_paths(self):
        calls = []

        class Core:
            def __init__(self, configuration):
                self.configuration = configuration

            async def __aenter__(self):
                return self

            async def __aexit__(self, *_):
                pass

            async def request(self, url, **kwargs):
                calls.append((self.configuration, url, kwargs))
                return SimpleNamespace(status_code=204)

        with tempfile.TemporaryDirectory() as directory:
            settings = SimpleNamespace(jellyfin_url="http://localhost:8096/jellyfin/", jellyfin_local_root=directory,
                                       jellyfin_server_root="/media", service_transport="tor_all")
            first, second = Path(directory) / "first.mp4", Path(directory) / "sub" / "second.mp4"
            with patch.dict(os.environ, {"PORNFETCH_JELLYFIN_API_KEY": "test-key"}), patch("src.shared.tor_transport.MediaCore", Core):
                await asyncio.gather(notify_jellyfin(first, settings), notify_jellyfin(second, settings))
            self.assertEqual(len(calls), 1)
            configuration, url, request = calls[0]
            self.assertEqual(configuration.service_transport, "tor_all")
            self.assertEqual(url, "http://localhost:8096/jellyfin/Library/Media/Updated")
            self.assertFalse(request["allow_redirects"])
            self.assertEqual([item["Path"] for item in request["json_data"]["Updates"]], ["/media/first.mp4", "/media/sub/second.mp4"])
            self.assertFalse(_batches)
            with self.assertRaises(ValueError):
                server_path(Path(directory).parent / "outside.mp4", directory, "/media")

    async def test_key_is_separate_from_settings_and_can_be_cleared(self):
        with tempfile.TemporaryDirectory() as directory, patch("src.shared.jellyfin.shared_data_dir", return_value=Path(directory)), patch.dict(os.environ, {"PORNFETCH_JELLYFIN_API_KEY": ""}):
            save_api_key("test-key")
            self.assertEqual(api_key(), "test-key")
            if os.name != "nt":
                self.assertEqual((Path(directory) / "jellyfin-api-key").stat().st_mode & 0o777, 0o600)
            save_api_key("")
            with self.assertRaises(ValueError):
                api_key()
