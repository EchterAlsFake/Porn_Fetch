"""Background verification of persisted desktop downloads against saved hashes."""
from __future__ import annotations

import asyncio
from pathlib import Path

from src.shared.file_integrity import file_digest, file_fingerprint

from .constants import VIDEO_COLLECTION
from .creators import VIDEOS, now, quoted

MIGRATION_NAME = "202611190000_download_integrity.js"
MIGRATION = r'''
migrate((app) => {
    for (const name of ["creator_videos", "video_records"]) {
        const collection = app.findCollectionByNameOrId(name)
        for (const field of ["sha256", "integrity", "integrity_checked"])
            collection.fields.add(new TextField({name: field}))
        app.save(collection)
    }
}, (app) => {
    for (const name of ["creator_videos", "video_records"]) {
        const collection = app.findCollectionByNameOrId(name)
        for (const field of ["sha256", "integrity", "integrity_checked"])
            collection.fields.removeByName(field)
        app.save(collection)
    }
})
'''

FINGERPRINT_MIGRATION_NAME = "202611200000_integrity_fingerprint.js"
FINGERPRINT_MIGRATION = r'''
migrate((app) => {
    for (const name of ["creator_videos", "video_records"]) {
        const collection = app.findCollectionByNameOrId(name)
        collection.fields.add(new JSONField({name: "file_fingerprint"}))
        app.save(collection)
    }
}, (app) => {
    for (const name of ["creator_videos", "video_records"]) {
        const collection = app.findCollectionByNameOrId(name)
        collection.fields.removeByName("file_fingerprint")
        app.save(collection)
    }
})
'''

PROBLEMS = {"missing", "changed", "unreadable"}
ERRORS = {
    "missing": "Integrity check: the downloaded file is missing. Restore it to its saved location or download it again.",
    "changed": "Integrity check: the file differs from its saved SHA-256 checksum. It may have been edited or corrupted. The original checksum has been kept.",
    "unreadable": "Integrity check: the downloaded file could not be read. Check that the drive is connected and readable.",
}


async def verify_downloads(repo, write_lock, history_lock, stop, *, full=False, pause=None,
                           progress=lambda done, total: None, changed=lambda: None,
                           bytes_per_second=64 * 1024 * 1024):
    groups = {}
    for collection in (VIDEOS, VIDEO_COLLECTION):
        async for row in repo.all(collection, filter='status = "completed" || (status = "failed" && integrity != "")'):
            if stop.is_set():
                return None
            value = row.get("output_path", "")
            if not value or value.startswith(("content:", "mediastore:", "file:")) or not Path(value).is_absolute():
                continue
            groups.setdefault(value, []).append((collection, row))
    result = dict.fromkeys(("checked", "unchanged", "hashed", "baselines", "missing", "changed", "unreadable", "skipped"), 0)
    pending = []

    async def flush():
        if not pending:
            return
        async with write_lock, history_lock:
            # Recheck only records with updates, in bounded reads/transactions.
            current = {}
            for collection in {c for c, _, _ in pending}:
                ids = " || ".join(f"id = {quoted(r['id'])}" for c, r, _ in pending if c == collection)
                page = await repo.page(collection, size=100, filter=ids)
                current.update(((collection, r["id"]), r) for r in page["items"])
            requests = []
            for collection, previous, data in pending:
                row = current.get((collection, previous["id"]))
                if row is None or any(row.get(k) != previous.get(k) for k in ("status", "output_path", "sha256", "file_fingerprint")):
                    continue
                requests.append({"method": "PATCH", "url": f"/api/collections/{collection}/records/{row['id']}", "body": data})
            if requests:
                await repo.client.request("POST", "/api/batch", {"requests": requests})
                changed()
        pending.clear()

    progress(0, len(groups))
    for path, references in sorted(groups.items()):
        if stop.is_set():
            return None
        digest, fingerprint, problem = "", None, ""
        known = {row["sha256"] for _, row in references if row.get("sha256")}
        shared_checksum = next(iter(known)) if len(known) == 1 else ""
        try:
            fingerprint = await asyncio.to_thread(file_fingerprint, path)
            states = {row.get("integrity") for _, row in references}
            cached = not full and len(known) == 1 and len(states) == 1 and states <= {"ok", "changed"} and all(
                row.get("sha256") == shared_checksum
                and row.get("file_fingerprint") == fingerprint for _, row in references)
            if cached:
                result["checked"] += 1
                result["unchanged"] += 1
                result["changed"] += int("changed" in states)
                progress(result["checked"] + result["skipped"], len(groups))
                continue  # No content reads, record fetches, timestamps or writes.
            digest, fingerprint = await asyncio.to_thread(file_digest, path, stop,
                pause=pause, bytes_per_second=bytes_per_second)
            result["hashed"] += 1
        except FileNotFoundError:
            problem = "missing"
        except InterruptedError:
            if stop.is_set():
                return None
            result["skipped"] += 1
            progress(result["checked"] + result["skipped"], len(groups))
            continue
        except OSError:
            problem = "unreadable"
        detected, baseline = set(), False
        for collection, previous in references:
            expected = previous.get("sha256") or shared_checksum
            state = problem or ("changed" if (expected and expected != digest) or (not expected and len(known) > 1) else "ok")
            data = {"integrity": state}
            if digest:
                data.update(integrity_checked=now(), file_fingerprint=fingerprint)
            if not previous.get("sha256") and shared_checksum:
                data["sha256"] = shared_checksum
            if state == "ok":
                if not expected:
                    data["sha256"] = digest
                    baseline = True
                if previous.get("integrity") in PROBLEMS:
                    data["status"] = "completed"
                if collection == VIDEOS:
                    data.update(error="", progress=100)
            else:
                detected.add(state)
                data["status"] = "failed"
                if collection == VIDEOS:
                    data["error"] = ERRORS[state]
            # Repeated missing/unreadable verdicts also need no database writes.
            data = {key: value for key, value in data.items() if previous.get(key) != value}
            if data:
                pending.append((collection, previous, data))
                if len(pending) >= 100:
                    await flush()
        result["checked"] += 1
        result["baselines"] += int(baseline)
        for state in detected:
            result[state] += 1
        progress(result["checked"] + result["skipped"], len(groups))
    await flush()
    return result
