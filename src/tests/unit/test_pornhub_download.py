"""Porn Fetch delegates recovery to the released PornHub API."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from base_api import DownloadConfigHLS, DownloadConfigRAW
from pornhub_api.modules.errors import SourcesUnavailable

from src.shared.pornhub_download import PornHubSourcesUnavailable, download


class PornHubRecoveryTests(unittest.IsolatedAsyncioTestCase):
    async def test_delegates_both_configurations_and_mode_callback(self):
        video = SimpleNamespace(download=AsyncMock(return_value=True))
        hls = DownloadConfigHLS(quality=720, path='fixture.mp4')
        raw = DownloadConfigRAW(quality=720, path='fixture.mp4')
        on_raw = Mock()
        self.assertTrue(await download(video, hls, raw, on_raw=on_raw))
        video.download.assert_awaited_once_with(hls, backup_configuration=raw, on_raw=on_raw)

    async def test_exhausted_sources_show_porn_fetch_message_and_keep_cause(self):
        cause = SourcesUnavailable('No working source')
        video = SimpleNamespace(download=AsyncMock(side_effect=cause))
        with self.assertRaisesRegex(PornHubSourcesUnavailable, 'not Porn Fetch') as raised:
            await download(video, DownloadConfigHLS(720), DownloadConfigRAW(720))
        self.assertIs(raised.exception.__cause__, cause)

    async def test_unrelated_failures_keep_their_original_error(self):
        video = SimpleNamespace(download=AsyncMock(side_effect=OSError('Disk full')))
        with self.assertRaisesRegex(OSError, 'Disk full'):
            await download(video, DownloadConfigHLS(720), DownloadConfigRAW(720))
