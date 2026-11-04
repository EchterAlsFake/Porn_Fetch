"""Feature-policy tests, independent of license activation and server state."""
import asyncio
import unittest
from contextlib import aclosing
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from src.shared.access import download_parallelism, public_collection_items


class PremiumAccessTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_preview_stops_at_five_without_reading_six_and_closes_source(self):
        read = []
        closed = []

        async def source():
            try:
                for index in range(20):
                    read.append(index)
                    yield index
            finally:
                closed.append(True)

        self.assertEqual([item async for item in public_collection_items(source(), False)], list(range(5)))
        self.assertEqual(read, list(range(5)))
        self.assertEqual(closed, [True])
        self.assertEqual([item async for item in public_collection_items(source(), True)], list(range(20)))

    async def test_cancelling_preview_closes_upstream(self):
        closed = []

        async def source():
            try:
                yield 1
                yield 2
            finally:
                closed.append(True)

        async with aclosing(public_collection_items(source(), False)) as preview:
            async for _ in preview:
                break
        self.assertEqual(closed, [True])

    def test_free_parallelism_is_one_even_with_stale_settings(self):
        self.assertEqual(download_parallelism(20, False), 1)
        self.assertEqual(download_parallelism(3, True), 3)

    async def test_cli_direct_video_queue_is_serial_without_premium(self):
        from src.cli.batch import _download_many
        active = maximum = 0

        async def download(*args):
            nonlocal active, maximum
            active += 1
            maximum = max(active, maximum)
            await asyncio.sleep(0)
            active -= 1
            return True

        with patch("src.cli.batch._download_url", AsyncMock(side_effect=download)):
            settings = SimpleNamespace(parallel_downloads=4, processing_delay=0)
            self.assertTrue(all(await _download_many(None, ["a", "b", "c"], settings, False)))
        self.assertEqual(maximum, 1)
