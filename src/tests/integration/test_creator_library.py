"""Creator persistence checks against an explicitly supplied, disposable PocketBase."""
import asyncio
import os
import tempfile
import unittest

from src.database.creators import CreatorRepository, MEMBERSHIPS, SCANS, SUBSCRIPTIONS, VIDEOS
from src.database.tracker import PocketBaseTracker
from src.shared.creator_library import CreatorLibrary
from src.shared.provider_routing import route_url

BINARY = os.environ.get("PORN_FETCH_TEST_POCKETBASE")


@unittest.skipUnless(BINARY, "Set PORN_FETCH_TEST_POCKETBASE to run real PocketBase integration checks")
class CreatorLibraryTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="creator-library-test-")
        self.tracker = PocketBaseTracker(self.folder.name, enabled=False, binary_path=BINARY)
        self.repo = CreatorRepository(await self.tracker.open_database())
        await self.repo.enable_batches()
        self.items = 30
        self.fail = False
        self.gate = None
        self.gate_reached = asyncio.Event()

        async def scan(source, premium):
            for i in range(self.items):
                yield {"identity": f"bellesa:video:{i}", "provider": "bellesa", "url": f"https://www.bellesa.co/videos/{i}", "title": f"Video {i}"}
            if self.gate:
                self.gate_reached.set()
                await self.gate.wait()
            if self.fail:
                raise ValueError("Advertised next page failed")
        self.library = CreatorLibrary(self.repo, scan)

    async def asyncTearDown(self):
        await self.library.close()
        await self.tracker.close()
        self.folder.cleanup()

    async def add(self, slug="sample"):
        url = "https://www.bellesa.co/channels/" + slug
        async def resolve(value):
            return route_url(value), value, "Channel"
        id = await self.library.save("", {"url": url, "name": slug, "folder": self.folder.name, "quality": "720p", "automatic": True}, resolve)
        return id

    async def finish(self, id):
        await self.library.scan_tasks[id]
        return await self.repo.get(SUBSCRIPTIONS, id)

    async def test_baseline_rescan_and_shared_video_identity(self):
        id = await self.add()
        source = await self.finish(id)
        self.assertTrue(source["baseline"])
        self.assertEqual((await self.repo.page(VIDEOS))["totalItems"], 30)
        self.assertEqual((await self.repo.page(VIDEOS, filter='status = "pending"'))["totalItems"], 0)
        self.items = 31
        self.library.scan(id)
        await self.finish(id)
        self.assertEqual((await self.repo.page(VIDEOS, filter='status = "pending"'))["totalItems"], 1)
        second = await self.add("another")
        await self.finish(second)
        self.assertEqual((await self.repo.page(VIDEOS))["totalItems"], 31)
        self.assertEqual((await self.repo.page(MEMBERSHIPS))["totalItems"], 62)
        await self.library.remove(second)
        self.assertEqual((await self.repo.page(VIDEOS))["totalItems"], 31)
        self.assertEqual((await self.repo.page(MEMBERSHIPS))["totalItems"], 31)
        self.assertFalse(self.tracker.enabled)

    async def test_cancel_reopen_replay_and_incomplete_scan(self):
        self.gate = asyncio.Event()
        id = await self.add()
        await self.gate_reached.wait()
        await self.library.cancel_scan(id)
        source = await self.finish(id)
        self.assertEqual(source["status"], "stopped")
        self.assertEqual((await self.repo.page(MEMBERSHIPS))["totalItems"], 30)
        self.gate = None
        self.fail = True
        self.items = 32
        self.library.scan(id)
        source = await self.finish(id)
        self.assertEqual(source["status"], "incomplete")
        self.assertFalse(source["baseline"])
        self.fail = False
        self.library.scan(id)
        source = await self.finish(id)
        self.assertEqual(source["status"], "complete")
        self.assertEqual((await self.repo.page(MEMBERSHIPS))["totalItems"], 32)
        await self.library.queue(id, "download")
        await self.library.close()
        await self.tracker.close()
        self.tracker = PocketBaseTracker(self.folder.name, enabled=False, binary_path=BINARY)
        self.repo = CreatorRepository(await self.tracker.open_database())
        self.library = CreatorLibrary(self.repo, None)
        await self.library.recover()
        self.assertEqual((await self.repo.page(VIDEOS, filter='status = "paused"'))["totalItems"], 32)

    async def test_draft_migration_preserves_existing_membership(self):
        from pathlib import Path
        from src.database.constants import _SCHEMA_MIGRATION, MIGRATION_NAME, CREATOR_MIGRATION, CREATOR_MIGRATION_NAME
        from src.database.service import PocketBaseService
        with tempfile.TemporaryDirectory(prefix="creator-draft-upgrade-") as folder:
            service = PocketBaseService(folder, binary_path=BINARY)
            migrations = service.migrations_directory
            migrations.mkdir()
            (migrations / MIGRATION_NAME).write_text(_SCHEMA_MIGRATION)
            (migrations / CREATOR_MIGRATION_NAME).write_text(CREATOR_MIGRATION)
            (migrations / "202611150000_seed_draft.js").write_text('''
migrate((app) => {
 const source = new Record(app.findCollectionByNameOrId("creator_subscriptions"))
 source.set("url", "https://www.bellesa.co/channels/draft"); source.set("provider", "bellesa"); app.save(source)
 const item = new Record(app.findCollectionByNameOrId("creator_items"))
 item.set("subscription", source.id); item.set("identity", "123"); item.set("url", "https://www.bellesa.co/videos/123")
 item.set("title", "Retained draft"); item.set("status", "completed"); app.save(item)
}, (app) => {})
''')
            await service._run_command(Path(BINARY), "superuser", "upsert", f"--dir={folder}", f"--migrationsDir={migrations}", "--", "test@localhost.invalid", "disposable-fixture-password")
            tracker = PocketBaseTracker(folder, enabled=False, binary_path=BINARY)
            try:
                repository = CreatorRepository(await tracker.open_database())
                rows = await repository.page(VIDEOS)
                self.assertEqual(rows["totalItems"], 1)
                self.assertEqual(rows["items"][0]["title"], "Retained draft")
                self.assertEqual(rows["items"][0]["status"], "completed")
                self.assertEqual(rows["items"][0]["identity"], "bellesa:video:123")
                self.assertEqual((await repository.page(MEMBERSHIPS))["totalItems"], 1)
            finally:
                await tracker.close()

    async def test_recovery_updates_every_record_across_database_pages(self):
        self.items = 120
        id = await self.add()
        await self.finish(id)
        await self.library.queue(id, "download")
        await self.library.recover()
        self.assertEqual((await self.repo.page(VIDEOS, filter='status = "paused"'))["totalItems"], 120)
        result = await self.repo.video_page(id, "paused", 2)
        self.assertEqual(len(result["items"]), 12)
        self.assertEqual(result["totalItems"], 120)

    async def test_scan_mode_is_fixed_at_start_and_progress_is_persisted(self):
        premium = False
        self.library.premium = lambda: premium
        gate = asyncio.Event()
        started = asyncio.Event()
        async def scan(source, full):
            started.set()
            await gate.wait()
            source["_progress"]["pages"] = 3 if full else 1
            for i in range(30 if full else 5):
                yield {"identity": f"bellesa:video:{i}", "provider": "bellesa", "url": f"https://bellesa.co/videos/{i}"}
        self.library.scan_source = scan
        async def resolve(url):
            return route_url(url), url, "Channel"
        id = await self.library.save("", {"name": "Mode fixture", "url": "https://bellesa.co/channels/mode", "folder": self.folder.name}, resolve)
        await started.wait()
        premium = True  # Activating during a preview must not establish a full baseline.
        gate.set()
        source = await self.finish(id)
        self.assertEqual(source["status"], "preview")
        self.assertFalse(source["baseline"])
        self.assertEqual(source["scan_discovered"], 5)
        self.assertEqual(source["scan_pages"], 1)
        gate.clear(); started.clear()
        self.library.scan(id)
        await started.wait()
        premium = False  # A running full traversal still reports its true coverage.
        gate.set()
        source = await self.finish(id)
        self.assertEqual(source["status"], "complete")
        self.assertEqual(source["scan_pages"], 3)
        self.assertTrue(source["baseline"])
        attempts = (await self.repo.page(SCANS, sort="started,id"))["items"]
        self.assertEqual([(row["premium"], row["discovered"]) for row in attempts], [(False, 5), (True, 30)])


if __name__ == "__main__":
    unittest.main()
