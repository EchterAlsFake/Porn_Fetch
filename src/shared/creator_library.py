"""Durable creator discovery and download intent, without Qt dependencies."""
from __future__ import annotations

import asyncio
import re
from contextlib import aclosing
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from src.database.creators import (
    COUNTS,
    MEMBERSHIPS,
    SCANS,
    SUBSCRIPTIONS,
    VIDEOS,
    CreatorRepository,
    now,
    quoted,
)
from src.shared.provider_routing import ContentKind, route_url

ACTIVE = {"pending", "preparing", "queued", "downloading"}


def source_url(value):
    value = value.strip()
    route = route_url(value)
    if route.kind not in {ContentKind.PROFILE, ContentKind.COLLECTION}:
        raise ValueError("Enter a creator, channel, playlist or collection URL.")
    p = urlsplit(value)
    path = p.path.rstrip("/")
    if route.provider in {"xhamster", "eporner"} and len(path.strip("/").split("/")) > 2:
        path = re.sub(r"(?<=/)[0-9]+$", "", path).rstrip("/")
    if route.provider == "youjizz":
        path = re.sub(r"(?<=[/-])[1-9][0-9]*(?=\.html$)", "1", path)
    # Provider resolvers normalize their own zero-based path/feed positions.
    query = [(k, v) for k, v in parse_qsl(p.query) if k.lower() not in {"page", "p", "pg", "from"}]
    return urlunsplit(("https", p.netloc.lower(), path, urlencode(sorted(query)), ""))


def loaded(video, field, default=None):
    fields = getattr(type(video), "__dataclass_fields__", None)
    if fields is not None and field not in fields:
        return default
    check = getattr(video, "is_field_loaded", None)
    if check is not None and not check(field):
        return default
    value = getattr(video, field, default)
    return value if value is not None else default


def identity(provider, url, video_id=None):
    p = urlsplit(url)
    query = dict(parse_qsl(p.query))
    path = p.path.rstrip("/")
    key = None
    if provider == "pornhub":
        key = query.get("viewkey")
    elif provider in {"xvideos", "xnxx"}:
        match = re.search(r"/video(?:[.-])?([^/]+)", path)
        key = match[1] if match else None
    elif provider in {"porn", "bellesa", "porndoe", "redgifs"}:
        match = re.search(r"/(?:scene|videos|watch|embed)/([^/]+)", path)
        key = match[1].lower() if match else None
    elif provider == "eporner":
        match = re.search(r"/(?:hd-porn/|video-)([^/]+)", path)
        key = match[1] if match else None
    elif provider in {"youporn", "thumbzilla", "tube8", "porntrex", "xfreehd"}:
        match = re.search(r"/(?:watch|porn-video|video)/(\d+)", path)
        key = match[1] if match else None
    elif provider == "redtube":
        key = path.strip("/") if path.strip("/").isdigit() else None
    elif provider == "spankbang":
        match = re.search(r"/([^/]+)/video(?:/|$)", path)
        key = match[1] if match else None
    elif provider in {"empflix", "tnaflix"}:
        match = re.search(r"/video(\d+)", path)
        key = match[1] if match else None
    elif provider == "youjizz":
        match = re.search(r"-(\d+)\.html$", path)
        key = match[1] if match else None
    elif provider == "xhamster":
        match = re.search(r"/videos/[^/]*-([^- /]+)$", path)
        key = match[1] if match else None
    elif provider == "pornhat":
        # Pornhat's public identity is its slug, including after detail loading.
        key = path
    key = key or video_id or path + ("?" + urlencode(sorted(parse_qsl(p.query))) if p.query else "")
    return f"{provider}:video:{key}"


def listing_item(route, video):
    url = str(video.url)
    title = str(loaded(video, "title", "") or "")
    duration = loaded(video, "duration", loaded(video, "length", ""))
    if isinstance(duration, (int, float)):
        seconds = max(0, round(duration))
        duration = f"{seconds // 60}:{seconds % 60:02d}"
    published = loaded(video, "publish_date", "")
    if hasattr(published, "isoformat"):
        published = published.isoformat()[:10]
    return {"identity": identity(route.provider, url, loaded(video, "video_id")),
            "provider": route.provider, "url": url, "title": title,
            "duration": str(duration or ""), "published": str(published or "")}


class CreatorLibrary:
    def __init__(self, repository: CreatorRepository, scan_source, *, changed=lambda: None, premium=lambda: True, mobile=False):
        self.repo = repository
        self.scan_source = scan_source
        self.changed = changed
        self.premium = premium
        self.mobile = mobile
        self.scan_tasks = {}
        self.scan_lock = asyncio.Lock()
        self.write_lock = asyncio.Lock()
        self.closing = False

    async def recover(self):
        async for video in self.repo.all(VIDEOS, filter='status = "pending" || status = "preparing" || status = "queued" || status = "downloading"'):
            await self.repo.put(VIDEOS, video["id"], {"status": "paused"})
        async for source in self.repo.all(SUBSCRIPTIONS, filter='status = "scanning"'):
            await self.repo.put(SUBSCRIPTIONS, source["id"], {"status": "stopped"})
        async for scan in self.repo.all(SCANS, filter='status = "running"'):
            await self.repo.put(SCANS, scan["id"], {"status": "cancelled", "finished": now()})

    async def subscriptions(self):
        premium = self.premium()
        counts = {r["id"]: r async for r in self.repo.all(COUNTS)} if premium else {}
        result = []
        async for row in self.repo.all(SUBSCRIPTIONS):
            count = counts.get(row["id"], {})
            if not premium:
                members = await self.repo.preview_memberships(row["id"])
                count = dict.fromkeys(["new_count", "pending", "downloading", "paused", "failed", "completed", "ignored"], 0)
                count["total"] = len(members)
                for member in members:
                    status = member.get("expand", {}).get("video", {}).get("status", "new")
                    bucket = "ignored" if member["ignored"] else {"new": "new_count", "preparing": "pending", "queued": "pending"}.get(status, status)
                    if bucket in count:
                        count[bucket] += 1
            count["newCount"] = count.get("new_count", 0)
            row = dict(row, counts=count, scan=row.get("status") or "stopped", lastScan=row.get("last_scan") or "Not scanned yet")
            row["initials"] = "".join(p[0] for p in (row.get("name") or row["provider"]).split()[:2]).upper()
            result.append(row)
        return result

    async def save(self, id, values, resolve):
        adding = not id
        name = str(values.get("name", "")).strip()
        if not name:
            raise ValueError("Give this subscription a name.")
        folder = str(values.get("folder", "")).strip()
        if not folder:
            raise ValueError("Choose a download destination.")
        if self.mobile:
            if not (folder.startswith(("content://", "file://")) or folder == "mediastore:Download/Porn Fetch"):
                raise ValueError("Choose the Android download folder in Settings first.")
        else:
            folder = str(Path(folder).expanduser().resolve())
        quality = str(values.get("quality", "best")).removesuffix("p")
        if quality not in {"144", "240", "250", "360", "480", "540", "720", "1080", "1440", "2160", "best", "half", "worst"}:
            raise ValueError("Choose a supported download quality.")
        url = source_url(str(values.get("url", "")))
        data = {"name": name, "folder": folder, "quality": quality,
                "startup": bool(values.get("startup", True)), "automatic": bool(values.get("automatic", False))}
        if data["automatic"] and not self.premium():
            raise PermissionError("Automatic creator downloads require Premium.")
        async with self.write_lock:
            if id:
                existing = await self.repo.get(SUBSCRIPTIONS, id)
                if url != existing["url"]:
                    raise ValueError("Add a new subscription to follow a different URL.")
                await self.repo.put(SUBSCRIPTIONS, id, data)
            else:
                route, canonical, kind = await resolve(url)
                if await self.repo.find(SUBSCRIPTIONS, f"url = {quoted(canonical)}"):
                    raise ValueError("That source is already in your subscriptions.")
                row = await self.repo.create(SUBSCRIPTIONS, {**data, "url": canonical, "provider": route.provider,
                    "kind": kind, "mode": route.profile_mode or "videos", "status": "stopped"})
                id = row["id"]
        self.changed()
        if adding:
            self.scan(id, "initial")
        return id

    def scan(self, id, trigger="manual"):
        task = self.scan_tasks.get(id)
        if self.closing or (task is not None and not task.done()):
            return task
        task = asyncio.create_task(self._scan(id, trigger), name=f"creator-scan-{id}")
        self.scan_tasks[id] = task
        return task

    async def cancel_scan(self, id):
        task = self.scan_tasks.get(id)
        if task and not task.done():
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def _scan(self, id, trigger):
        async with self.scan_lock:
            source = await self.repo.get(SUBSCRIPTIONS, id)
            stamp = now()
            premium_mode = bool(self.premium())
            progress = {"pages": 0}
            run = await self.repo.create(SCANS, {"subscription": id, "trigger": trigger, "started": stamp, "status": "running", "premium": premium_mode})
            await self.repo.put(SUBSCRIPTIONS, id, {"status": "scanning", "error": "", "last_scan": stamp, "scan_pages": 0, "scan_discovered": 0})
            self.changed()
            count = 0
            batch = []
            last_update = asyncio.get_running_loop().time()
            outcome, error = "complete", ""
            try:
                # Streaming writes are the checkpoint. A restarted traversal replays safely.
                stream = self.scan_source(dict(source, _progress=progress), premium_mode)
                async with aclosing(stream):
                    async for item in stream:
                        batch.append(item)
                        count += 1
                        if len(batch) >= 25 or asyncio.get_running_loop().time() - last_update >= .5:
                            await self._flush(source, batch, stamp)
                            batch = []
                            await self.repo.put(SCANS, run["id"], {"discovered": count, "pages": progress["pages"]})
                            await self.repo.put(SUBSCRIPTIONS, id, {"scan_discovered": count, "scan_pages": progress["pages"]})
                            last_update = asyncio.get_running_loop().time()
                            self.changed()
                if not premium_mode:
                    outcome = "preview"
            except asyncio.CancelledError:
                outcome = "stopped"
            except Exception as exc:
                outcome, error = "incomplete", str(exc)
            finally:
                if batch:
                    await self._flush(source, batch, stamp)
                await self.repo.put(SCANS, run["id"], {"status": outcome, "error": error, "finished": now(), "discovered": count, "pages": progress["pages"]})
                data = {"status": outcome, "error": error, "scan_pages": progress["pages"], "scan_discovered": count}
                if outcome == "complete":
                    data.update(baseline=True, last_success=now())
                    # Only additions after a successful baseline are automatic candidates.
                    current = await self.repo.get(SUBSCRIPTIONS, id)
                    if source.get("baseline") and current.get("automatic") and self.premium() and not self.closing:
                        await self.queue(id, "automatic", since=source.get("last_success", ""))
                await self.repo.put(SUBSCRIPTIONS, id, data)
                self.changed()

    async def _flush(self, source, batch, stamp):
        async def write():
            async with self.write_lock:
                await self.repo.remember_many(source, batch, stamp)
        task = asyncio.create_task(write())
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError:
            await task  # A page committed before cancellation must finish checkpointing.
            raise

    async def queue(self, id, action, *, since=""):
        premium = self.premium()
        if not premium and action == "automatic":
            raise PermissionError("Automatic creator downloads require Premium. Try five videos manually at up to 720p.")
        states = {"new", "paused", "failed"} if action == "download" else {"failed"} if action == "retry" else {"new"}
        filter = f"subscription = {quoted(id)} && ignored = false"
        if not premium:
            preview = await self.repo.preview_memberships(id)
            filter += " && (" + (" || ".join(f"id = {quoted(m['id'])}" for m in preview) or 'id = ""') + ")"
        if since:
            filter += f" && first_seen > {quoted(since)}"
        async with self.write_lock:
            async for member in self.repo.all(MEMBERSHIPS, filter=filter):
                video = await self.repo.get(VIDEOS, member["video"])
                if video["status"] in states:
                    await self.repo.put(VIDEOS, video["id"], {"status": "pending", "owner": (video.get("owner") or id) if premium else id, "error": ""})
        self.changed()

    async def download_index(self, subscription, video_id):
        """The normal engine rechecks this public-collection position at dispatch."""
        if self.premium():
            return 6
        for index, member in enumerate(await self.repo.preview_memberships(subscription), 1):
            if member["video"] == video_id and not member["ignored"]:
                return index
        raise PermissionError("The free creator preview includes five videos per subscription at up to 720p. Downloading the full library requires Premium.")

    async def remove(self, id):
        await self.cancel_scan(id)
        # Relations remove membership/scan records. Shared jobs and history remain.
        await self.repo.delete(SUBSCRIPTIONS, id)
        self.changed()

    async def close(self):
        self.closing = True
        tasks = [t for t in self.scan_tasks.values() if not t.done()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
