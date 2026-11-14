"""Real GUI slots regenerate a completed file's sidecars without provider traffic."""
import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from PySide6.QtCore import QObject

from src.shared.library_export import ExportOptions, export_library_bundle
from src.shared.library_metadata import LibraryMetadata


class LibraryExportWorkflowTests(unittest.IsolatedAsyncioTestCase):
    async def test_gui_preview_and_export_use_saved_snapshot_offline(self):
        from src.backend import application

        backend = application.Backend.__new__(application.Backend)
        QObject.__init__(backend)
        backend._library_task = None
        backend._library_selection = None
        backend._library_pending = {}
        backend._license_bridge = SimpleNamespace(isPremium=True)
        previews, outcomes = [], []
        backend.libraryPreviewReady.connect(previews.append)
        backend.libraryExportFinished.connect(outcomes.append)
        settings = SimpleNamespace(metadata_export="off", metadata_layout="alongside", metadata_genres=False,
                                   metadata_studio_fallback=False, jellyfin_url="")

        def spawn(self, coroutine, *, name):
            return asyncio.create_task(coroutine, name=name)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "example.mp4"
            path.write_bytes(b"completed video")
            metadata = LibraryMetadata("bellesa", "video", "123", "https://bellesa.co/videos/123", "Example")
            await export_library_bundle(path, metadata, ExportOptions("jellyfin"), premium=True)
            path.with_suffix(".nfo").unlink()
            with patch.object(application, "app_settings", settings), patch.object(application.Backend, "_spawn", spawn), patch.object(application.clients, "get_video", AsyncMock(side_effect=AssertionError("No provider request expected"))):
                backend.preview_library_export(str(path), "")
                await backend._library_task
                self.assertIn("Title: Example", previews[-1])
                backend.export_library_metadata()
                await backend._library_task
            self.assertTrue(path.with_suffix(".nfo").exists())
            self.assertIn("Library metadata saved", outcomes[-1])
            self.assertEqual(path.read_bytes(), b"completed video")
