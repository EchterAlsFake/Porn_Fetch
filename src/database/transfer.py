"""Portable PocketBase library exports and transactional imports.

Only application records are imported. A native PocketBase snapshot is included
for independent recovery, but imported schemas and executable migrations are
never installed into the running application.
"""
from __future__ import annotations

import asyncio
import json
import secrets
import shutil
import tempfile
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from .constants import ORIGIN_COLLECTION, VIDEO_COLLECTION
from .creators import MEMBERSHIPS, SCANS, SUBSCRIPTIONS, VIDEOS, now

COLLECTIONS = (ORIGIN_COLLECTION, VIDEO_COLLECTION, SUBSCRIPTIONS, VIDEOS, MEMBERSHIPS, SCANS)
RELATIONS = {VIDEO_COLLECTION: {"origin_iterator": ORIGIN_COLLECTION},
             VIDEOS: {"owner": SUBSCRIPTIONS},
             MEMBERSHIPS: {"subscription": SUBSCRIPTIONS, "video": VIDEOS},
             SCANS: {"subscription": SUBSCRIPTIONS}}
NATURAL_KEYS = {ORIGIN_COLLECTION: ("url",), VIDEO_COLLECTION: ("url",),
                SUBSCRIPTIONS: ("url",), VIDEOS: ("identity",),
                MEMBERSHIPS: ("subscription", "video")}


async def records(repo):
    return {name: [r async for r in repo.all(name)] for name in COLLECTIONS}


async def batch(repo, requests):
    """One PocketBase transaction, including large libraries; restore API limits."""
    if not requests:
        return
    client = repo.client
    previous = (await client.request("GET", "/api/settings"))["batch"]
    timeout = client.timeout
    try:
        client.timeout = max(timeout, 180)
        size = len(json.dumps({"requests": requests}).encode("utf-8"))
        await client.request("PATCH", "/api/settings", {"batch": {
            "enabled": True, "maxRequests": max(100, len(requests)), "timeout": 120,
            "maxBodySize": max(2097152, size * 2)}})
        await client.request("POST", "/api/batch", {"requests": requests})
    finally:
        try:
            await client.request("PATCH", "/api/settings", {"batch": previous})
        finally:
            client.timeout = timeout


def request(method, collection, id="", body=None):
    result = {"method": method, "url": f"/api/collections/{collection}/records" + (f"/{id}" if id else "")}
    if body is not None:
        result["body"] = body
    return result


async def native_backup(repo, data_directory):
    name = "pornfetch_" + secrets.token_hex(12) + ".zip"
    timeout = repo.client.timeout
    try:
        repo.client.timeout = max(timeout, 180)
        await repo.client.request("POST", "/api/backups", {"name": name})
    finally:
        repo.client.timeout = timeout
    path = Path(data_directory) / "backups" / name
    if not path.is_file():
        raise ValueError("PocketBase did not create a local backup. Check its backup storage settings.")
    return path


async def export_library(repo, data_directory, destination):
    destination = Path(destination).expanduser().resolve()
    data = {"format": "pornfetch-library", "version": 1, "exported_at": now(), "collections": await records(repo)}
    backup = await native_backup(repo, data_directory)
    def write():
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation preserves an existing backup if the user reuses a name.
        with tempfile.TemporaryDirectory(dir=destination.parent) as folder:
            temporary = Path(folder) / "library.zip"
            with ZipFile(temporary, "w", ZIP_DEFLATED) as archive:
                archive.writestr("library.json", json.dumps(data, ensure_ascii=False))
                archive.write(backup, "pocketbase.zip")
            created = False
            try:
                with destination.open("xb") as output, temporary.open("rb") as source:
                    created = True
                    shutil.copyfileobj(source, output)
            except BaseException:
                if created:
                    destination.unlink(missing_ok=True)
                raise
    try:
        await asyncio.to_thread(write)
    finally:
        await repo.client.request("DELETE", f"/api/backups/{backup.name}")
    return sum(len(rows) for rows in data["collections"].values())


def read_library(path):
    with ZipFile(path) as archive:
        if archive.getinfo("library.json").file_size > 256 * 1024 * 1024:
            raise ValueError("The library manifest is too large.")
        data = json.loads(archive.read("library.json"))
    if not isinstance(data, dict) or data.get("format") != "pornfetch-library" or data.get("version") != 1:
        raise ValueError("Choose a supported Porn Fetch library export.")
    tables = data.get("collections")
    if not isinstance(tables, dict) or set(tables) != set(COLLECTIONS):
        raise ValueError("The export is missing library collections.")
    for name, rows in tables.items():
        if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
            raise ValueError(f"Invalid records in {name}.")
        ids = [r.get("id") for r in rows]
        if any(not isinstance(id, str) or len(id) != 15 or not id.isascii() or not id.isalnum() for id in ids) or len(set(ids)) != len(ids):
            raise ValueError(f"Invalid or duplicate record IDs in {name}.")
    ids_by_table = {name: {r["id"] for r in rows} for name, rows in tables.items()}
    for table, relations in RELATIONS.items():
        for row in tables[table]:
            for field, target in relations.items():
                value = row.get(field)
                # Removed subscription owners are permitted on retained shared jobs.
                if value and value not in ids_by_table[target] and field != "owner":
                    raise ValueError(f"The export contains a broken {table}.{field} relation.")
    return tables


async def import_library(repo, tables, mode):
    if mode not in {"merge", "replace"}:
        raise ValueError("Choose whether to merge or replace the library.")
    current = await records(repo)
    operations = []
    if mode == "replace":
        for name in reversed(COLLECTIONS):
            operations.extend(request("DELETE", name, r["id"]) for r in current[name])
        # The obsolete draft table must not repopulate retained legacy rows.
        async for row in repo.all("creator_items"):
            operations.append(request("DELETE", "creator_items", row["id"]))
    maps = {name: {} for name in COLLECTIONS}
    for name in COLLECTIONS:
        schema = await repo.client.request("GET", f"/api/collections/{name}")
        fields = {f["name"] for f in schema["fields"]} - {"id", "created", "updated"}
        existing = current[name] if mode == "merge" else []
        keys = NATURAL_KEYS.get(name, ("id",))
        index = {tuple(r.get(k, "") for k in keys): r for r in existing}
        used_ids = {r["id"] for r in existing}
        for incoming in tables[name]:
            row = {k: v for k, v in incoming.items() if k in fields}
            for field, target in RELATIONS.get(name, {}).items():
                row[field] = maps[target].get(row.get(field), "")
            key = tuple(row.get(k, incoming["id"] if k == "id" else "") for k in keys)
            old = index.get(key)
            id = old["id"] if old else incoming["id"]
            while old is None and id in used_ids:
                id = secrets.token_hex(8)[:15]
            maps[name][incoming["id"]] = id
            if old:
                # Preserve local preferences, memberships and saved partial jobs.
                if name in {VIDEOS, VIDEO_COLLECTION} and row.get("status") == "completed" and old.get("status") != "completed":
                    operations.append(request("PATCH", name, id, {"status": "completed", "output_path": row.get("output_path", ""),
                        "sha256": row.get("sha256", ""), "file_fingerprint": row.get("file_fingerprint"), "integrity": row.get("integrity", ""), "integrity_checked": row.get("integrity_checked", ""),
                        **({"progress": 100, "job": "", "snapshot": None, "error": ""} if name == VIDEOS else {})}))
                continue
            if name == SUBSCRIPTIONS:
                row.update(startup=False, automatic=False)
                if row.get("status") == "scanning":
                    row["status"] = "stopped"
            if name == VIDEOS:
                row.update(job="", snapshot=None)
                if row.get("status") in {"pending", "preparing", "queued", "downloading"}:
                    row["status"] = "paused"
                if row.get("status") != "completed":
                    row["progress"] = 0
            if name == SCANS and row.get("status") == "running":
                row.update(status="cancelled", finished=now())
            row["id"] = id
            operations.append(request("POST", name, body=row))
            used_ids.add(id)
            index[key] = row
    await batch(repo, operations)
    return len(operations)
