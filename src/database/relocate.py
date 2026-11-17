"""Move completed media or relink an externally moved folder without overwrites."""
from __future__ import annotations

import asyncio
import os
import shutil
import time
from pathlib import Path, PureWindowsPath

from .constants import VIDEO_COLLECTION
from .creators import SUBSCRIPTIONS, VIDEOS
from .transfer import batch, request


def source_path(value):
    if os.name != "nt" and PureWindowsPath(value).is_absolute():
        return PureWindowsPath(value)
    return Path(value).expanduser()


def mapped_path(value, old, new):
    if not value or str(value).startswith(("content:", "mediastore:", "file:")):
        return None
    path, old = source_path(str(value)), source_path(str(old))
    if not path.is_absolute():
        return None
    try:
        relative = path.relative_to(old)
        if ".." in relative.parts:
            return None
        return new.joinpath(*relative.parts)
    except ValueError:
        return None


async def plan_relocation(repo, old_folder, new_folder, mode):
    old_folder, new_folder = old_folder.strip(), new_folder.strip()
    if mode not in {"move", "locate"}:
        raise ValueError("Choose Move files or Locate moved files.")
    if not old_folder.strip() or not new_folder.strip():
        raise ValueError("Choose both the old and new folders.")
    if any(v.startswith(("content:", "mediastore:", "file:")) for v in (old_folder, new_folder)):
        raise ValueError("Moving or locating files requires local filesystem folders.")
    old = source_path(old_folder)
    if isinstance(old, PureWindowsPath):
        if mode == "move":
            raise ValueError("Use Locate moved files to relink folders from another operating system.")
    else:
        old = old.resolve()
    new = Path(new_folder).expanduser().resolve()
    if old == new or old in new.parents or new in old.parents:
        raise ValueError("Choose separate folders that are not inside one another.")
    operations, files = [], {}
    completed_paths, missing = set(), set()
    for collection in (VIDEOS, VIDEO_COLLECTION):
        async for row in repo.all(collection, filter='status = "completed" || (status = "failed" && integrity != "")'):
            target = mapped_path(row.get("output_path"), old, new)
            if target is None:
                continue
            source = Path(row["output_path"])
            if mode == "locate":
                if not await asyncio.to_thread(target.is_file):
                    raise ValueError(f"A completed video is missing from the new folder: {target.name}. Keep the same filenames and subfolders.")
            else:
                if not await asyncio.to_thread(source.is_file):
                    if not await asyncio.to_thread(target.is_file):
                        missing.add(str(source))
                        payload = {"status": "failed", "output_path": ""}
                        if collection == VIDEOS:
                            payload.update(progress=0, job="", snapshot=None,
                                error="The recorded file is missing. Download again to save it to the new destination.")
                        operations.append(request("PATCH", collection, row["id"], payload))
                        continue
                else:
                    files[source] = target
            completed_paths.add(str(target))
            payload = {"output_path": str(target)}
            if collection == VIDEOS:
                if row.get("snapshot"):
                    payload["snapshot"] = dict(row["snapshot"], output_path=str(target))
            operations.append(request("PATCH", collection, row["id"], payload))
    folders = 0
    async for row in repo.all(SUBSCRIPTIONS):
        target = mapped_path(row.get("folder"), old, new)
        if target is not None:
            folders += 1
            operations.append(request("PATCH", SUBSCRIPTIONS, row["id"], {"folder": str(target)}))
    if not operations:
        raise ValueError("No completed downloads or subscription destinations use that old folder.")
    if mode == "move":
        # Preserve the known alongside and scene-folder metadata/artwork layouts.
        for source in tuple(files):
            names = [source.with_suffix(".nfo"), source.with_name(source.stem + ".pornfetch.json")]
            names += [source.with_name(source.stem + "-poster" + ext) for ext in (".jpg", ".jpeg", ".png", ".webp")]
            if (source.parent / "pornfetch.json").is_file():
                names += [source.parent / name for name in ("movie.nfo", "pornfetch.json", "poster.jpg", "poster.jpeg", "poster.png", "poster.webp")]
            for companion in names:
                if companion.is_file():
                    files[companion] = new / companion.relative_to(old)
        for source, target in files.items():
            if source.is_symlink() or old not in source.resolve().parents:
                raise ValueError("Moving files through symbolic links is not supported. Choose the actual folder.")
            if target.exists():
                raise ValueError(f"The destination already contains {target.name}. No files were changed.")
    return {"operations": operations, "files": files, "videos": len(completed_paths), "folders": folders,
            "missing": sorted(missing), "mode": mode, "old": str(old), "new": str(new)}


async def apply_relocation(repo, plan, *, progress=lambda done, total: None, paths_updated=None):
    copied = []
    loop = asyncio.get_running_loop()
    def copy():
        total = sum(source.stat().st_size for source in plan["files"])
        done, last_report = 0, 0
        loop.call_soon_threadsafe(progress, done, total)
        try:
            for source, target in plan["files"].items():
                target.parent.mkdir(parents=True, exist_ok=True)
                # Reserve the name exclusively, including races after preview.
                with target.open("xb") as output:
                    copied.append(target)
                    with source.open("rb") as input:
                        while chunk := input.read(1024 * 1024):
                            output.write(chunk)
                            done += len(chunk)
                            stamp = time.monotonic()
                            if stamp - last_report >= .1:
                                loop.call_soon_threadsafe(progress, done, total)
                                last_report = stamp
                shutil.copystat(source, target)
            loop.call_soon_threadsafe(progress, done, total)
        except BaseException:
            for path in copied:
                path.unlink(missing_ok=True)
            raise
    # Keep the original files until the database commits every new path.
    await asyncio.to_thread(copy)
    progress(0, 0)  # Saving paths has no byte-based progress.
    try:
        await batch(repo, plan["operations"])
    except Exception as error:
        # A timeout can arrive after commit. Keep both copies so either set of
        # recorded paths remains valid, and never delete originals on uncertainty.
        raise ValueError("The path update could not be confirmed. Original files and any new copies were kept. Check the library paths before retrying; Locate moved files can finish relinking.") from error
    if paths_updated is not None:
        await paths_updated()
    retained = 0
    for source in plan["files"]:
        try:
            await asyncio.to_thread(source.unlink)
        except OSError:
            retained += 1  # The valid destination and database paths are retained.
    return retained
