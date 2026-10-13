"""Offline checks for the shared GUI activity state."""
from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, Mock, patch

from PySide6.QtCore import QObject

from src.backend.application import Backend
from src.backend.license_bridge import LicenseBridge
from src.database.bridge import DatabaseBridge
from src.database.tracker import PocketBaseTracker
from src.tests.integration.test_license_integration import FakeLicenseClient


class ActivityIndicatorTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Exercise the real task lifecycle without constructing network clients.
        self.backend = Backend.__new__(Backend)
        QObject.__init__(self.backend)
        self.backend._background_tasks = set()
        self.backend._activity_active = False
        self.backend._video_fetch_task = None
        self.backend._license_bridge = None
        self.backend.database_bridge = None
        self.backend._is_shutting_down = False
        self.backend._client_refresh_pending = False
        self.backend.logger = Mock()
        self.changes = []
        self.backend.activityChanged.connect(lambda: self.changes.append(self.backend.activityActive))

    async def test_parallel_work_stays_active_until_last_task_finishes(self):
        first_done = asyncio.Event()
        second_done = asyncio.Event()
        first = self.backend._spawn(first_done.wait(), name="first")
        second = self.backend._spawn(second_done.wait(), name="second")
        self.assertTrue(self.backend.activityActive)
        self.assertFalse(self.backend.busy)

        first_done.set()
        await first
        self.assertTrue(self.backend.activityActive)
        self.assertEqual(self.changes, [True])

        second_done.set()
        await second
        self.assertFalse(self.backend.activityActive)
        self.assertEqual(self.changes, [True, False])

    async def test_failure_and_cancellation_clear_activity(self):
        async def fail():
            raise ValueError("simulated failure")

        with patch("src.backend.application.report_exception", new_callable=AsyncMock) as report:
            task = self.backend._spawn(fail(), name="failing")
            await asyncio.gather(task, return_exceptions=True)
            await asyncio.sleep(0)
            self.assertFalse(self.backend.activityActive)
            report.assert_awaited_once()

        task = self.backend._spawn(asyncio.Event().wait(), name="cancelled")
        await asyncio.sleep(0)
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
        self.assertFalse(self.backend.activityActive)
        self.assertEqual(self.changes, [True, False, True, False])

    async def test_license_and_database_work_share_activity_with_backend_tasks(self):
        license_bridge = LicenseBridge(FakeLicenseClient())
        self.backend._enforce_quality_access = Mock()
        self.backend.set_license_bridge(license_bridge)
        database_bridge = DatabaseBridge(tracker=PocketBaseTracker(enabled=False))
        self.backend.database_bridge = database_bridge
        database_bridge.busyChanged.connect(self.backend._update_activity)

        license_done = asyncio.Event()
        database_done = asyncio.Event()
        backend_done = asyncio.Event()
        license_task = license_bridge._start(license_done.wait)
        database_task = asyncio.create_task(database_done.wait())
        database_bridge._track_task(database_task)
        backend_task = self.backend._spawn(backend_done.wait(), name="background")

        backend_done.set()
        await backend_task
        license_done.set()
        await license_task
        self.assertTrue(self.backend.activityActive)
        self.assertEqual(self.changes, [True])

        database_done.set()
        await database_task
        self.assertFalse(self.backend.activityActive)
        self.assertEqual(self.changes, [True, False])
        await license_bridge.close()
        await database_bridge.close()
