"""PocketBase collection names and the bundled schema migration."""

ORIGIN_COLLECTION = "origin_iterators"
VIDEO_COLLECTION = "video_records"
SUPERUSER_EMAIL = "porn-fetch@localhost.invalid"
MIGRATION_NAME = "202608280000_create_download_tracking.js"

_SCHEMA_MIGRATION = r'''
migrate((app) => {
    const origins = new Collection({
        id: "pf_origins_0001",
        type: "base",
        name: "origin_iterators",
        fields: [
            { type: "text", name: "url", required: true },
            { type: "text", name: "name", required: true },
        ],
        indexes: [
            "CREATE UNIQUE INDEX idx_origin_iterators_url ON origin_iterators (url)",
        ],
    })
    app.save(origins)

    const videos = new Collection({
        id: "pf_videos__0001",
        type: "base",
        name: "video_records",
        fields: [
            { type: "text", name: "url", required: true },
            { type: "text", name: "title" },
            { type: "text", name: "video_id" },
            { type: "text", name: "author" },
            { type: "text", name: "length" },
            { type: "text", name: "thumbnail_url" },
            { type: "date", name: "publish_date" },
            { type: "text", name: "status" },
            { type: "json", name: "tags" },
            { type: "json", name: "qualities" },
            { type: "text", name: "identifier" },
            { type: "text", name: "output_path" },
            { type: "text", name: "selected_quality" },
            { type: "number", name: "file_size_mb" },
            { type: "date", name: "downloaded_at" },
            { type: "bool", name: "is_hls" },
            { type: "json", name: "missing_segments" },
            { type: "bool", name: "is_from_account" },
            { type: "text", name: "origin_iterator_url" },
            {
                type: "relation",
                name: "origin_iterator",
                collectionId: "pf_origins_0001",
                cascadeDelete: false,
                maxSelect: 1,
            },
        ],
        indexes: [
            "CREATE UNIQUE INDEX idx_video_records_url ON video_records (url)",
            "CREATE INDEX idx_video_records_status ON video_records (status)",
            "CREATE INDEX idx_video_records_origin ON video_records (origin_iterator)",
        ],
    })
    app.save(videos)
}, (app) => {
    app.delete(app.findCollectionByNameOrId("video_records"))
    app.delete(app.findCollectionByNameOrId("origin_iterators"))
})
'''.lstrip()
