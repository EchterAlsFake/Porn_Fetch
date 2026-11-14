"""Premium NFO/artwork exports, with ownership checks and independent retry."""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import math
import os
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

from .access import require_library_export
from .download_options import filename_component
from .library_metadata import LibraryMetadata
from .provider_metadata import collect_library_metadata
from .provider_metadata import value as provider_value
from .provider_routing import ContentKind, route_url

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ExportOptions:
    mode: str = "off"
    layout: str = "alongside"
    genres: bool = False
    studio_fallback: bool = False

    @classmethod
    def from_settings(cls, settings) -> ExportOptions:
        return cls(getattr(settings, "metadata_export", "off"), getattr(settings, "metadata_layout", "alongside"),
                   getattr(settings, "metadata_genres", False), getattr(settings, "metadata_studio_fallback", False))

    def validate(self):
        if self.mode not in {"off", "jellyfin"} or self.layout not in {"alongside", "scene-folder"}:
            raise ValueError("Invalid media library export mode or layout")


@dataclass(slots=True)
class ExportResult:
    files: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notification_error: str | None = None
    retryable: bool = False


def snapshot_for(video) -> LibraryMetadata:
    if video.library_metadata is None:
        provider = route_url(video.url).provider
        video.library_metadata = collect_library_metadata(provider, video.source_video, video)
    return video.library_metadata


def library_video_path(original: Path, video, options: ExportOptions) -> Path:
    """Only choose an organized destination before starting a new download."""
    if options.mode != "jellyfin" or options.layout != "scene-folder":
        return original
    metadata = snapshot_for(video)
    year = f" ({metadata.publication_date[:4]})" if metadata.publication_date else ""
    # Keep enough room for the identity even for long provider titles.
    title = filename_component(metadata.title).encode("utf-8")[:150].decode("utf-8", errors="ignore")
    name = filename_component(f"{title}{year} - {metadata.provider}-{metadata.media_kind}-{metadata.source_id}")
    if original.parent.name == name and original.stem == name:
        return original
    return original.parent / name / (name + original.suffix)


def export_paths(video_path: Path, layout: str) -> tuple[Path, Path, str]:
    if layout == "scene-folder":
        return video_path.parent / "movie.nfo", video_path.parent / "pornfetch.json", "poster"
    return video_path.with_suffix(".nfo"), video_path.with_name(video_path.stem + ".pornfetch.json"), video_path.stem + "-poster"


def nfo_bytes(metadata: LibraryMetadata, options: ExportOptions) -> bytes:
    root = ET.Element("movie")

    def add(name, content):
        if content is not None and str(content).strip():
            ET.SubElement(root, name).text = str(content)

    add("title", metadata.title)
    add("plot", metadata.description)
    if metadata.publication_date:
        add("premiered", metadata.publication_date)
        add("year", metadata.publication_date[:4])
    if metadata.duration_seconds and math.isfinite(metadata.duration_seconds):
        add("runtime", max(1, round(metadata.duration_seconds / 60)))
    for credit in metadata.performers:
        ET.SubElement(ET.SubElement(root, "actor"), "name").text = credit.name
    studios = list(metadata.producers)
    if options.studio_fallback:
        studios += metadata.content_providers + metadata.publishers + metadata.channels
    for name in dict.fromkeys(credit.name for credit in studios):
        add("studio", name)
    for tag in metadata.tags:
        add("tag", tag)
    if options.genres:
        for category in metadata.categories:
            add("genre", category)
    ET.SubElement(root, "uniqueid", type="pornfetch", default="true").text = metadata.identity
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _atomic_write(path: Path, data: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".pornfetch-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_export(video_path: Path, layout="alongside") -> tuple[LibraryMetadata, dict]:
    _, manifest, _ = export_paths(video_path, layout)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    if payload.get("schema") != 1 or payload.get("video") != video_path.name:
        raise ValueError("The saved metadata does not describe this video file")
    metadata = LibraryMetadata.from_portable(payload["metadata"])
    if route_url(metadata.source_url).provider != metadata.provider:
        raise ValueError("The saved source URL and metadata provider disagree")
    return metadata, payload


def plan_export(video_path: Path, metadata: LibraryMetadata, options: ExportOptions) -> dict:
    options.validate()
    nfo, manifest, poster = export_paths(video_path, options.layout)
    return {"identity": metadata.identity, "video": str(video_path), "nfo": str(nfo), "json": str(manifest),
            "artwork_basename": poster, "metadata": metadata.portable()}


async def prepare_existing_export(video_path, source_url, settings, *, premium, resolve_source):
    """Resolve descriptive fields without preparing streams or selecting quality."""
    require_library_export(premium)
    path = Path(video_path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError("Choose an existing completed video file")
    options = ExportOptions.from_settings(settings)
    options = ExportOptions("jellyfin", "alongside", options.genres, options.studio_fallback)
    if source_url.strip():
        route = route_url(source_url)
        if route.kind != ContentKind.VIDEO:
            raise ValueError("Enter a supported video source URL")
        source = await resolve_source(source_url)
        prepared = SimpleNamespace(url=str(provider_value(source, "url") or route.url),
                                   title=str(provider_value(source, "title") or path.stem))
        return collect_library_metadata(route.provider, source, prepared), getattr(source, "core", None), options
    for layout in ("alongside", "scene-folder"):
        _, manifest, _ = export_paths(path, layout)
        if manifest.exists():
            metadata, payload = load_export(path, layout)
            return metadata, None, ExportOptions("jellyfin", layout, options.genres, options.studio_fallback)
    raise ValueError("Enter the original video URL, or choose a file with saved Porn Fetch metadata")


def _image_extension(data: bytes) -> str | None:
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    return None


def _write_bundle(video_path, metadata, options, image, force) -> ExportResult:
    result = ExportResult()
    nfo, manifest, poster = export_paths(video_path, options.layout)
    old = {}
    if manifest.exists():
        try:
            old_metadata, old = load_export(video_path, options.layout)
            if old_metadata.identity != metadata.identity:
                raise ValueError("Existing export describes a different source")
        except (ValueError, KeyError, TypeError):
            if not force:
                raise ValueError("Existing Porn Fetch JSON was preserved; review it before replacing metadata") from None
    owned = old.get("generated", {})
    payloads = {nfo: nfo_bytes(metadata, options)}
    old_artwork = []
    if image:
        extension = _image_extension(image)
        if extension:
            target = video_path.parent / (poster + extension)
            old_artwork = [video_path.parent / (poster + suffix) for suffix in (".jpg", ".jpeg", ".png", ".webp")
                           if suffix != extension and (video_path.parent / (poster + suffix)).exists()]
            if not force and any(_digest(path.read_bytes()) != owned.get(path.name) for path in old_artwork):
                result.warnings.append("Preserved existing or edited primary artwork.")
                old_artwork = []
            else:
                payloads[target] = image
        else:
            result.warnings.append("Artwork was not a supported JPEG, PNG or WebP image.")
    generated = dict(owned)
    for path, data in payloads.items():
        if path.exists() and not force and _digest(path.read_bytes()) != owned.get(path.name):
            result.warnings.append(f"Preserved existing or edited sidecar: {path.name}")
            continue
        _atomic_write(path, data)
        generated[path.name] = _digest(data)
        result.files.append(path)
    for path in old_artwork:
        path.unlink()
        generated.pop(path.name, None)
    # Preserve only safe relative filenames in the ownership record.
    generated = {name: digest for name, digest in generated.items()
                 if isinstance(name, str) and Path(name).name == name and name not in {".", ".."}}
    payload = {"schema": 1, "video": video_path.name, "exported_at": datetime.now(UTC).isoformat(),
               "metadata": metadata.portable(), "generated": generated,
               "options": {"layout": options.layout, "genres": options.genres, "studio_fallback": options.studio_fallback}}
    _atomic_write(manifest, (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
    result.files.append(manifest)
    return result


async def export_library_bundle(video_path: Path, metadata: LibraryMetadata, options: ExportOptions, *,
                                premium: bool, core=None, thumbnail=None, force=False, dry_run=False):
    require_library_export(premium)
    options.validate()
    video_path = Path(video_path)
    if not video_path.is_file():
        raise FileNotFoundError("Choose an existing completed video file")
    if dry_run:
        return plan_export(video_path, metadata, options)
    warnings = []
    image = thumbnail
    if not image and metadata.image_url and core:
        try:
            image = await core.fetch_bytes(metadata.image_url)
        except Exception:
            warnings.append("Artwork could not be downloaded. Video metadata was exported; retry to add artwork.")
    result = await asyncio.to_thread(_write_bundle, video_path, metadata, options, image, force)
    result.warnings[:0] = warnings
    result.retryable = bool(warnings)
    return result


@dataclass(slots=True)
class FinalizationResult:
    export: ExportResult | None = None
    warnings: list[str] = field(default_factory=list)
    embedded_written: bool = False


async def finalize_video(video_path, video, settings, *, premium, metadata_written=False,
                         write_embedded=True, notify=True) -> FinalizationResult:
    """A saved video's status is independent from tagging/export/notification."""
    result = FinalizationResult()
    if (write_embedded and getattr(settings, "write_metadata", True) and not metadata_written
            and Path(video_path).suffix.casefold() == ".mp4" and Path(video_path).is_file()):
        try:
            from .metadata import write_tags
            result.embedded_written = bool(await asyncio.to_thread(write_tags, str(video_path), video))
        except Exception:
            result.warnings.append("The video was saved, but embedded metadata could not be written.")
    options = ExportOptions.from_settings(settings)
    if options.mode == "off":
        return result
    try:
        source = video.source_video
        core = getattr(source, "core", None)
        result.export = await export_library_bundle(Path(video_path), snapshot_for(video), options,
                                                     premium=premium, core=core, thumbnail=video.thumbnail_data)
        result.warnings.extend(result.export.warnings)
    except PermissionError:
        result.warnings.append("Media Library Export requires an active Premium license. The video was saved.")
        return result
    except Exception as error:
        logger.warning("Library export failed (%s)", type(error).__name__)
        result.warnings.append("The video was saved, but library export failed. Retry metadata export for this file.")
        return result
    if notify and getattr(settings, "jellyfin_url", ""):
        try:
            from .jellyfin import notify_jellyfin
            await notify_jellyfin(Path(video_path), settings)
        except Exception:
            result.export.notification_error = "Metadata was saved, but Jellyfin could not be notified. Retry the notification."
            result.warnings.append(result.export.notification_error)
    return result
