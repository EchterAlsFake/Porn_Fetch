"""
This sets up the database, which is needed to track downloaded videos.
It will also track which videos failed to download, so that you can re-try later.
"""

import json
import sqlite3
import traceback


def init_db(database_path: str) -> str | bool:
    """
    This initializes the database and creates basic tables
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE,
                url TEXT,
                title TEXT,
                author TEXT,
                length INTEGER,
                tags TEXT,
                publish_date TEXT,
                thumbnail TEXT,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
        return True

    except Exception:
        error = traceback.format_exc()
        return error


def save_video_metadata(video_id: int, data: dict, database_path: str) -> bool | str:
    """
    This saves the metadata of each video into the database, so that you can always see which videos you have downloaded
    and have a little local backup of what you did.
    May not seem that important, and it probably isn't but only takes a few kilobytes, so why not.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO videos (video_id, url, title, author, length, tags, publish_date, thumbnail)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video_id,
            data.get("url"),
            data.get("title"),
            data.get("author"),
            data.get("length"),
            json.dumps(data.get("tags")),  # store tags list as JSON
            data.get("publish_date"),
            data.get("thumbnail")
        ))
        conn.commit()
        conn.close()
        return True

    except Exception:
        error = traceback.format_exc()
        return error


# EOF