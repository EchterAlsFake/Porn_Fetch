"""PocketBase schema and paginated repository for creator subscriptions."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

SUBSCRIPTIONS = "creator_subscriptions"
VIDEOS = "creator_videos"
MEMBERSHIPS = "creator_memberships"
SCANS = "creator_scans"
COUNTS = "creator_source_counts"
VIDEO_ORDER = "-first_seen,id"
MIGRATION_NAME = "202611160000_creator_library.js"

# The earlier draft remains immutable. This migration also preserves any draft data.
MIGRATION = r'''
migrate((app) => {
    const subscriptions = app.findCollectionByNameOrId("creator_subscriptions")
    for (const name of ["name", "kind", "mode", "folder", "quality", "last_success"]) subscriptions.fields.add(new TextField({name}))
    for (const name of ["startup", "baseline"]) subscriptions.fields.add(new BoolField({name}))
    app.save(subscriptions)
    const history = app.findCollectionByNameOrId("video_records")
    history.indexes = history.indexes.concat(["CREATE INDEX idx_video_records_video_id ON video_records (video_id)"])
    app.save(history)
    app.save(new Collection({name: "creator_videos", type: "base", fields: [
        {type: "text", name: "identity", required: true}, {type: "text", name: "url", required: true},
        {type: "text", name: "provider"}, {type: "text", name: "title"},
        {type: "text", name: "duration"}, {type: "text", name: "published"}, {type: "text", name: "status"},
        {type: "text", name: "job"}, {type: "text", name: "error"}, {type: "text", name: "owner"},
        {type: "text", name: "output_path"}, {type: "text", name: "quality"},
        {type: "number", name: "progress"}, {type: "json", name: "snapshot"}
    ], indexes: ["CREATE UNIQUE INDEX idx_creator_video_identity ON creator_videos (identity)",
                 "CREATE INDEX idx_creator_video_state ON creator_videos (status)"]}))
    app.save(new Collection({name: "creator_memberships", type: "base", fields: [
        {type: "relation", name: "subscription", collectionId: subscriptions.id, maxSelect: 1, cascadeDelete: true, required: true},
        {type: "relation", name: "video", collectionId: app.findCollectionByNameOrId("creator_videos").id, maxSelect: 1, required: true},
        {type: "bool", name: "ignored"}, {type: "text", name: "first_seen"}, {type: "text", name: "last_seen"}
    ], indexes: ["CREATE UNIQUE INDEX idx_creator_member ON creator_memberships (subscription, video)"]}))
    app.save(new Collection({name: "creator_scans", type: "base", fields: [
        {type: "relation", name: "subscription", collectionId: subscriptions.id, maxSelect: 1, cascadeDelete: true},
        {type: "text", name: "trigger"}, {type: "text", name: "started"}, {type: "text", name: "finished"},
        {type: "text", name: "status"}, {type: "text", name: "error"}, {type: "number", name: "discovered"}
    ]}))
    for (const old of app.findAllRecords("creator_items")) {
        let subscription
        try { subscription = app.findRecordById("creator_subscriptions", old.getString("subscription")) } catch (_) { continue }
        const prefix = subscription.getString("provider").toLowerCase() + ":video:"
        const previous = old.getString("identity")
        const identity = previous.startsWith(prefix) ? previous : prefix + previous
        let video
        try { video = app.findFirstRecordByData("creator_videos", "identity", identity) } catch (_) {
            video = new Record(app.findCollectionByNameOrId("creator_videos"))
            for (const name of ["url", "title", "job", "error"]) video.set(name, old.getString(name))
            video.set("identity", identity); video.set("provider", subscription.getString("provider"))
            video.set("status", old.getString("status") === "completed" ? "completed" : "new")
            app.save(video)
        }
        const member = new Record(app.findCollectionByNameOrId("creator_memberships"))
        member.set("subscription", subscription.id); member.set("video", video.id); app.save(member)
    }
    app.save(new Collection({name: "creator_source_counts", type: "view", viewQuery: `
        SELECT s.id, COUNT(m.id) AS total,
            COALESCE(SUM(CASE WHEN m.ignored = 0 AND v.status = 'new' THEN 1 ELSE 0 END),0) AS new_count,
            COALESCE(SUM(CASE WHEN m.ignored = 0 AND v.status IN ('pending','preparing','queued') THEN 1 ELSE 0 END),0) AS pending,
            COALESCE(SUM(CASE WHEN m.ignored = 0 AND v.status = 'downloading' THEN 1 ELSE 0 END),0) AS downloading,
            COALESCE(SUM(CASE WHEN m.ignored = 0 AND v.status = 'paused' THEN 1 ELSE 0 END),0) AS paused,
            COALESCE(SUM(CASE WHEN m.ignored = 0 AND v.status = 'failed' THEN 1 ELSE 0 END),0) AS failed,
            COALESCE(SUM(CASE WHEN m.ignored = 0 AND v.status = 'completed' THEN 1 ELSE 0 END),0) AS completed,
            COALESCE(SUM(CASE WHEN m.ignored = 1 THEN 1 ELSE 0 END),0) AS ignored
        FROM creator_subscriptions s LEFT JOIN creator_memberships m ON m.subscription = s.id
        LEFT JOIN creator_videos v ON v.id = m.video GROUP BY s.id
    `}))
}, (app) => {
    for (const name of ["creator_source_counts", "creator_scans", "creator_memberships", "creator_videos"]) app.delete(app.findCollectionByNameOrId(name))
})
'''


def now():
    return datetime.now(timezone.utc).isoformat()


def quoted(value):
    return json.dumps(str(value), ensure_ascii=False)


def record_id(namespace, value):
    # Deterministic IDs allow safe retries when a successful response was lost.
    return hashlib.sha256(f"{namespace}:{value}".encode()).hexdigest()[:15]


class CreatorRepository:
    def __init__(self, client):
        self.client = client

    async def page(self, collection, *, page=1, size=100, filter="", sort="", expand=""):
        return await self.client.request("GET", f"/api/collections/{collection}/records", query={
            "page": page, "perPage": size, "filter": filter, "sort": sort, "expand": expand})

    async def all(self, collection, *, filter=""):
        # Keyset traversal stays correct when callers change a filtered status.
        cursor = ""
        while True:
            expression = filter
            if cursor:
                expression = f"({filter}) && id > {quoted(cursor)}" if filter else f"id > {quoted(cursor)}"
            response = await self.page(collection, filter=expression, sort="id")
            rows = response.get("items", [])
            if not rows:
                break
            for row in rows:
                yield row
            cursor = rows[-1]["id"]

    async def enable_batches(self):
        await self.client.request("PATCH", "/api/settings", {"batch": {
            "enabled": True, "maxRequests": 100, "timeout": 10, "maxBodySize": 2097152}})

    async def remember_many(self, subscription, items, stamp):
        keys = " || ".join(f"identity = {quoted(item['identity'])}" for item in items)
        existing = {v["identity"]: v async for v in self.all(VIDEOS, filter=keys)}
        video_ids = [existing[item["identity"]]["id"] if item["identity"] in existing else record_id("video", item["identity"]) for item in items]
        member_filter = f"subscription = {quoted(subscription['id'])} && (" + " || ".join(f"video = {quoted(id)}" for id in video_ids) + ")"
        members = {m["video"]: m async for m in self.all(MEMBERSHIPS, filter=member_filter)}
        requests = []
        for item, video_id in zip(items, video_ids):
            if item["identity"] not in existing:
                requests.append({"method": "POST", "url": f"/api/collections/{VIDEOS}/records", "body": {
                    "id": video_id, **item, "status": "new"}})
            member = members.get(video_id)
            if member:
                requests.append({"method": "PATCH", "url": f"/api/collections/{MEMBERSHIPS}/records/{member['id']}", "body": {"last_seen": stamp}})
            else:
                requests.append({"method": "POST", "url": f"/api/collections/{MEMBERSHIPS}/records", "body": {
                    "id": record_id(subscription["id"], video_id), "subscription": subscription["id"], "video": video_id,
                    "first_seen": stamp, "last_seen": stamp}})
        if requests:
            await self.client.request("POST", "/api/batch", {"requests": requests})

    async def get(self, collection, id):
        return await self.client.request("GET", f"/api/collections/{collection}/records/{id}")

    async def find(self, collection, filter):
        rows = (await self.page(collection, size=1, filter=filter))["items"]
        return rows[0] if rows else None

    async def put(self, collection, id, data):
        return await self.client.update_record(collection, id, data)

    async def create(self, collection, data):
        return await self.client.create_record(collection, data)

    async def delete(self, collection, id):
        await self.client.request("DELETE", f"/api/collections/{collection}/records/{id}")

    async def preview_memberships(self, subscription):
        # Keep the same five identities across scans, retries and relaunches.
        # Ignoring a preview item must not make a sixth item eligible.
        return (await self.page(MEMBERSHIPS, size=5, filter=f"subscription = {quoted(subscription)}",
                                sort="first_seen,id", expand="video"))["items"]

    async def video_page(self, subscription, status="", page=1, *, preview=False):
        filter = f"subscription = {quoted(subscription)}"
        if preview:
            members = await self.preview_memberships(subscription)
            filter += " && (" + (" || ".join(f"id = {quoted(m['id'])}" for m in members) or 'id = ""') + ")"
        if status == "ignored":
            filter += " && ignored = true"
        elif status:
            states = "video.status = " + quoted(status)
            if status == "pending":
                states = '(video.status = "pending" || video.status = "preparing" || video.status = "queued")'
            filter += f" && ignored = false && ({states})"
        return await self.page(MEMBERSHIPS, page=page, size=12, filter=filter, sort=VIDEO_ORDER, expand="video")

    async def next_pending_video(self, subscription):
        # Dispatch in the same order as the unfiltered library, across all pages.
        result = await self.page(MEMBERSHIPS, size=1,
            filter=f"subscription = {quoted(subscription)} && ignored = false"
                   f' && video.owner = {quoted(subscription)} && video.status = "pending"',
            sort=VIDEO_ORDER, expand="video")
        return result["items"][0]["expand"]["video"] if result["items"] else None


POLISH_MIGRATION_NAME = "202611180000_creator_scan_progress.js"
POLISH_MIGRATION = r'''
migrate((app) => {
    const sources = app.findCollectionByNameOrId("creator_subscriptions")
    for (const name of ["scan_pages", "scan_discovered"]) sources.fields.add(new NumberField({name}))
    app.save(sources)
    const scans = app.findCollectionByNameOrId("creator_scans")
    scans.fields.add(new NumberField({name: "pages"}))
    scans.fields.add(new BoolField({name: "premium"}))
    app.save(scans)
}, (app) => {
    const sources = app.findCollectionByNameOrId("creator_subscriptions")
    for (const name of ["scan_pages", "scan_discovered"]) sources.fields.removeByName(name)
    app.save(sources)
    const scans = app.findCollectionByNameOrId("creator_scans")
    for (const name of ["pages", "premium"]) scans.fields.removeByName(name)
    app.save(scans)
})
'''
