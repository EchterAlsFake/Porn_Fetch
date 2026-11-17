"""Storage moves and migration against disposable PocketBase libraries."""
import asyncio
import os
import shutil
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

from src.database.creators import MEMBERSHIPS, SCANS, SUBSCRIPTIONS, VIDEOS, CreatorRepository
from src.database.relocate import apply_relocation, plan_relocation
from src.database.tracker import PocketBaseTracker
from src.database.transfer import export_library, import_library, read_library, records

BINARY = os.environ.get("PORN_FETCH_TEST_POCKETBASE")


@unittest.skipUnless(BINARY, "Set PORN_FETCH_TEST_POCKETBASE for storage integration checks")
class LibraryStorageTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix="library-storage-")
        self.root = Path(self.folder.name)
        self.tracker = PocketBaseTracker(self.root / "db", enabled=False, binary_path=BINARY)
        self.repo = CreatorRepository(await self.tracker.open_database())
        await self.repo.enable_batches()
        self.old = self.root / "old"
        self.old.mkdir()
        self.source = await self.repo.create(SUBSCRIPTIONS, {"url": "https://www.bellesa.co/channels/demo", "provider": "bellesa",
            "name": "Original", "folder": str(self.old), "quality": "720", "startup": True, "automatic": True})
        await self.repo.remember_many(self.source, [{"identity": "bellesa:video:123", "provider": "bellesa",
            "url": "https://www.bellesa.co/videos/123", "title": "Completed"}], "2026-11-17")
        self.video = (await self.repo.page(VIDEOS))["items"][0]
        self.file = self.old / "nested" / "completed.mp4"
        self.file.parent.mkdir()
        self.file.write_bytes(b"completed-media")
        self.file.with_suffix(".nfo").write_text("metadata")
        await self.repo.put(VIDEOS, self.video["id"], {"status": "completed", "progress": 100,
            "output_path": str(self.file), "snapshot": {"output_path": str(self.file)}})
        await self.tracker.record_download(self.video["url"], "Completed", video_id="123", output_path=self.file,
            origin_iterator_url=self.source["url"], origin_iterator_name="Original")

    async def asyncTearDown(self):
        await self.tracker.close()
        self.folder.cleanup()

    async def test_move_updates_creator_history_snapshot_and_sidecars_then_locate(self):
        new = self.root / "new"
        plan = await plan_relocation(self.repo, str(self.old), str(new), "move")
        self.assertEqual((plan["videos"], plan["folders"]), (1, 1))
        progress, committed = [], []
        async def paths_updated():
            committed.append((await self.repo.get(SUBSCRIPTIONS, self.source["id"]))["folder"])
            self.assertTrue(self.file.exists())  # UI can update before originals are removed.
        self.assertEqual(await apply_relocation(self.repo, plan,
            progress=lambda done, total: progress.append((done, total)), paths_updated=paths_updated), 0)
        self.assertEqual(committed, [str(new)])
        self.assertTrue(any(done == total and total > 0 for done, total in progress))
        target = new / "nested/completed.mp4"
        self.assertEqual(target.read_bytes(), b"completed-media")
        self.assertEqual(target.with_suffix(".nfo").read_text(), "metadata")
        self.assertFalse(self.file.exists())
        row = await self.repo.get(VIDEOS, self.video["id"])
        self.assertEqual(row["output_path"], str(target))
        self.assertEqual(row["snapshot"]["output_path"], str(target))
        history = (await self.repo.page("video_records"))["items"][0]
        self.assertEqual(history["output_path"], str(target))
        external = self.root / "external"
        shutil.move(new, external)
        plan = await plan_relocation(self.repo, str(new), str(external), "locate")
        await apply_relocation(self.repo, plan)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["output_path"], str(external / "nested/completed.mp4"))
        self.assertEqual((await self.repo.get(SUBSCRIPTIONS, self.source["id"]))["folder"], str(external))

    async def test_integrity_baseline_detects_changes_missing_files_and_restoration(self):
        from src.database.integrity import verify_downloads
        stop = threading.Event()
        async def check():
            return await verify_downloads(self.repo, asyncio.Lock(), self.tracker._save_lock, stop)
        original = self.file.read_bytes()
        history = (await self.repo.page("video_records"))["items"][0]
        await self.repo.put("video_records", history["id"], {"sha256": "", "integrity": ""})
        first = await check()
        self.assertEqual((first["checked"], first["baselines"]), (1, 1))
        saved = (await self.repo.get(VIDEOS, self.video["id"]))["sha256"]
        self.assertEqual(len(saved), 64)
        await self.repo.put(VIDEOS, self.video["id"], {"sha256": ""})
        # A known history checksum must protect a legacy creator row too.
        stat = self.file.stat()
        self.file.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
        os.utime(self.file, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        changed = await check()
        self.assertEqual(changed["changed"], 1)
        row = await self.repo.get(VIDEOS, self.video["id"])
        self.assertEqual(row["sha256"], saved)
        self.assertEqual(row["status"], "failed")
        self.assertEqual(row["integrity"], "changed")
        self.file.write_bytes(original)
        self.assertEqual((await check())["changed"], 0)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["status"], "completed")
        self.file.unlink()
        self.assertEqual((await check())["missing"], 1)
        self.assertEqual((await self.repo.page("video_records"))["items"][0]["integrity"], "missing")
        self.file.write_bytes(original)
        self.assertEqual((await check())["missing"], 0)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["sha256"], saved)
        stop.set()
        self.assertIsNone(await check())

    async def test_quick_check_avoids_file_reads_and_database_writes_for_unchanged_files(self):
        from src.database.integrity import verify_downloads
        from src.shared.file_integrity import file_digest
        stop = threading.Event()
        async def check(full=False):
            return await verify_downloads(self.repo, asyncio.Lock(), self.tracker._save_lock, stop, full=full)
        await check()
        before = (await self.repo.get(VIDEOS, self.video["id"]))["integrity_checked"]
        with patch("src.database.integrity.file_digest", side_effect=AssertionError("Unchanged files must not be read")),              patch.object(self.repo.client, "request", wraps=self.repo.client.request) as requests:
            quick = await check()
        self.assertEqual((quick["unchanged"], quick["hashed"]), (1, 0))
        self.assertTrue(all(call.args[0] == "GET" for call in requests.call_args_list))
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["integrity_checked"], before)
        with patch("src.database.integrity.file_digest", wraps=file_digest) as digest:
            full = await check(full=True)
        self.assertEqual(full["hashed"], 1)
        self.assertEqual(digest.call_count, 1)
        original = self.file.read_bytes()
        self.file.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
        self.assertEqual((await check())["changed"], 1)
        with patch("src.database.integrity.file_digest", side_effect=AssertionError("Known bad, unchanged files must not be re-read")):
            known_bad = await check()
        self.assertEqual((known_bad["unchanged"], known_bad["changed"]), (1, 1))
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["status"], "failed")

    async def test_integrity_updates_are_bounded_batches(self):
        from src.database.integrity import verify_downloads
        for start in range(0, 120, 20):
            items = []
            for i in range(start, start + 20):
                path = self.old / f"{i}.mp4"
                path.write_bytes(f"media {i}".encode())
                items.append({"identity": f"bellesa:video:{i}", "url": f"https://bellesa.co/videos/{i}", "provider": "bellesa"})
            await self.repo.remember_many(self.source, items, "2026-11-17")
        async for row in self.repo.all(VIDEOS, filter='status = "new"'):
            i = row["url"].rsplit("/", 1)[-1]
            await self.repo.put(VIDEOS, row["id"], {"status": "completed", "output_path": str(self.old / f"{i}.mp4")})
        with patch.object(self.repo.client, "request", wraps=self.repo.client.request) as requests:
            result = await verify_downloads(self.repo, asyncio.Lock(), self.tracker._save_lock, threading.Event())
        batches = [call.args[2]["requests"] for call in requests.call_args_list if call.args[:2] == ("POST", "/api/batch")]
        self.assertEqual(result["checked"], 121)
        self.assertEqual(len(batches), 2)
        self.assertTrue(all(len(batch) <= 100 for batch in batches))
        self.assertFalse(any(call.args[0] == "PATCH" for call in requests.call_args_list))

    async def test_integrity_flagged_files_can_be_relinked_after_an_external_move(self):
        from src.database.integrity import verify_downloads
        stop = threading.Event()
        await verify_downloads(self.repo, asyncio.Lock(), self.tracker._save_lock, stop)
        new = self.root / "moved"
        shutil.move(self.old, new)
        await verify_downloads(self.repo, asyncio.Lock(), self.tracker._save_lock, stop)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["integrity"], "missing")
        plan = await plan_relocation(self.repo, str(self.old), str(new), "locate")
        await apply_relocation(self.repo, plan)
        result = await verify_downloads(self.repo, asyncio.Lock(), self.tracker._save_lock, stop)
        self.assertEqual(result["missing"], 0)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["status"], "completed")

    async def test_move_previews_missing_files_without_changing_them_until_apply(self):
        missing = self.old / "missing.mp4"
        await self.repo.remember_many(self.source, [{"identity": "bellesa:video:missing", "provider": "bellesa",
            "url": "https://bellesa.co/videos/missing"}], "2026-11-15")
        row = (await self.repo.page(VIDEOS, filter='identity = "bellesa:video:missing"'))["items"][0]
        await self.repo.put(VIDEOS, row["id"], {"status": "completed", "output_path": str(missing)})
        new = self.root / "new"
        plan = await plan_relocation(self.repo, str(self.old), str(new), "move")
        self.assertEqual(plan["missing"], [str(missing)])
        self.assertEqual(plan["videos"], 1)
        self.assertEqual((await self.repo.get(VIDEOS, row["id"]))["status"], "completed")
        await apply_relocation(self.repo, plan)
        self.assertEqual((await self.repo.get(VIDEOS, row["id"]))["status"], "failed")
        self.assertEqual((await self.repo.get(SUBSCRIPTIONS, self.source["id"]))["folder"], str(new))
        self.assertEqual((new / "nested/completed.mp4").read_bytes(), b"completed-media")

    async def test_move_refuses_collision_and_locate_refuses_missing_files(self):
        target = self.root / "new/nested/completed.mp4"
        target.parent.mkdir(parents=True)
        target.write_bytes(b"keep-existing")
        with self.assertRaisesRegex(ValueError, "already contains"):
            await plan_relocation(self.repo, str(self.old), str(target.parents[1]), "move")
        self.assertEqual(target.read_bytes(), b"keep-existing")
        target.unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            await plan_relocation(self.repo, str(self.old), str(target.parents[1]), "locate")
        self.assertTrue(self.file.exists())
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["output_path"], str(self.file))

    async def test_relink_requires_a_matching_saved_checksum(self):
        new = self.root / "new"
        target = new / "nested/completed.mp4"
        target.parent.mkdir(parents=True)
        original = self.file.read_bytes()
        self.file.rename(target)
        target.write_bytes(b"different-media")

        for mode in ("move", "locate"):
            with self.subTest(mode=mode):
                plan = await plan_relocation(self.repo, str(self.old), str(new), mode)
                with self.assertRaisesRegex(ValueError, "saved checksum"):
                    await apply_relocation(self.repo, plan)
                creator = await self.repo.get(VIDEOS, self.video["id"])
                history = (await self.repo.page("video_records"))["items"][0]
                self.assertEqual(creator["output_path"], str(self.file))
                self.assertEqual(history["output_path"], str(self.file))
                self.assertEqual(target.read_bytes(), b"different-media")

        target.write_bytes(original)
        plan = await plan_relocation(self.repo, str(self.old), str(new), "move")
        await apply_relocation(self.repo, plan)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["output_path"], str(target))

    @unittest.skipIf(os.name == "nt", "POSIX-side migration from Windows paths")
    async def test_locate_can_map_windows_paths_on_a_new_posix_computer(self):
        windows_root = "C:\\Users\\example\\Videos"
        windows_file = windows_root + "\\nested\\completed.mp4"
        await self.repo.put(VIDEOS, self.video["id"], {"output_path": windows_file})
        await self.repo.put(SUBSCRIPTIONS, self.source["id"], {"folder": windows_root})
        plan = await plan_relocation(self.repo, windows_root, str(self.old), "locate")
        await apply_relocation(self.repo, plan)
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["output_path"], str(self.file))
        self.assertEqual((await self.repo.get(SUBSCRIPTIONS, self.source["id"]))["folder"], str(self.old))

    async def test_failed_replacement_rolls_back_every_deleted_record(self):
        tables = await records(self.repo)
        tables[VIDEOS][0]["url"] = ""  # Required field forces a transaction failure.
        with self.assertRaises(Exception):
            await import_library(self.repo, tables, "replace")
        self.assertEqual((await self.repo.get(VIDEOS, self.video["id"]))["status"], "completed")
        self.assertEqual((await self.repo.page(MEMBERSHIPS))["totalItems"], 1)
        self.assertEqual((await self.repo.page("video_records"))["totalItems"], 1)
        self.assertTrue(self.file.exists())

    async def test_export_import_large_library_merge_and_replace(self):
        for start in range(0, 60, 20):
            await self.repo.remember_many(self.source, [{"identity": f"bellesa:video:{i}", "provider": "bellesa",
                "url": f"https://www.bellesa.co/videos/{i}", "title": f"Video {i}"} for i in range(start, start + 20)], "2026-11-17")
        await self.repo.create(SCANS, {"subscription": self.source["id"], "status": "complete"})
        export = self.root / "export.zip"
        count = await export_library(self.repo, self.tracker.data_path, export)
        self.assertGreater(count, 100)
        with ZipFile(export) as archive:
            self.assertEqual(set(archive.namelist()), {"library.json", "pocketbase.zip"})
            with archive.open("pocketbase.zip") as snapshot, ZipFile(snapshot) as native:
                self.assertIn("data.db", native.namelist())
        tables = read_library(export)
        other = PocketBaseTracker(self.root / "other-db", enabled=False, binary_path=BINARY)
        try:
            repo = CreatorRepository(await other.open_database())
            await repo.enable_batches()
            await import_library(repo, tables, "merge")
            source = (await repo.page(SUBSCRIPTIONS))["items"][0]
            self.assertFalse(source["automatic"])
            self.assertFalse(source["startup"])
            self.assertEqual((await repo.page(MEMBERSHIPS))["totalItems"], 61)
            self.assertEqual((await repo.page(VIDEOS, filter='status = "completed"'))["totalItems"], 1)
            await repo.put(SUBSCRIPTIONS, source["id"], {"name": "Local preferences"})
            await import_library(repo, tables, "merge")
            self.assertEqual((await repo.get(SUBSCRIPTIONS, source["id"]))["name"], "Local preferences")
            self.assertEqual((await repo.page(VIDEOS))["totalItems"], 61)
            await repo.create(SUBSCRIPTIONS, {"name": "Local only", "provider": "bellesa", "url": "https://www.bellesa.co/channels/local"})
            await import_library(repo, tables, "replace")
            self.assertEqual((await repo.page(SUBSCRIPTIONS))["totalItems"], 1)
            self.assertEqual((await repo.page("video_records"))["totalItems"], 1)
            self.assertEqual((await repo.page("origin_iterators"))["totalItems"], 1)
            self.assertEqual((await repo.client.request("GET", "/api/settings"))["batch"]["maxRequests"], 100)
        finally:
            await other.close()
