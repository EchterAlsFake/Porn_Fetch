"""Title templates and portable path components, independent of Qt/providers."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path
from string import Template

PLACEHOLDERS = {"title", "author", "video_id", "index", "publish_date", "length", "output_path"}
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".mov", ".m4v", ".ts"}


def title_template(pattern: str) -> Template:
    template = Template(pattern or "$title")
    if not template.is_valid():
        raise ValueError("Invalid title template. Use $title or ${title}, and $$ for a literal dollar sign.")
    unknown = set(template.get_identifiers()) - PLACEHOLDERS
    if unknown:
        raise ValueError("Unknown title placeholder: " + ", ".join("$" + name for name in sorted(unknown)))
    if template.template.endswith(("/", "\\")):
        raise ValueError("Title formatting must end with a filename, not a folder separator.")
    if ".." in Path(template.template).parts:
        raise ValueError("Title formatting cannot contain parent-folder traversal (..).")
    return template


def filename_component(value: object, fallback: str = "untitled") -> str:
    """Keep Unicode names while replacing separators, controls and reserved names."""
    text = unicodedata.normalize("NFC", str(value))
    text = re.sub(r'[<>:"/\\|?*\x00-\x1f\x7f\u202a-\u202e\u2066-\u2069]', "_", text).strip(" .")
    text = text or fallback
    if re.fullmatch(r"CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]", text.split(".", 1)[0], re.IGNORECASE):
        text = "_" + text
    if len(text.encode("utf-8")) > 240:
        suffix = Path(text).suffix
        suffix = suffix if len(suffix.encode("utf-8")) <= 12 else ""
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
        stem = text[:-len(suffix)] if suffix else text
        budget = 240 - len(suffix.encode("utf-8")) - len(digest) - 1
        text = stem.encode("utf-8")[:budget].decode("utf-8", errors="ignore").rstrip(" .") + "_" + digest + suffix
    return text


def video_output_path(video, index: int, pattern: str, output_folder: str | Path) -> Path:
    template = title_template(pattern)
    base = Path(output_folder).expanduser().resolve()
    context = {"title": video.title or "untitled", "author": video.author or "unknown",
               "video_id": video.video_id or "unknown", "index": f"{index:02d}",
               "publish_date": video.publish_date.date().isoformat() if video.publish_date else "unknown",
               "length": str(video.length) if video.length is not None else "unknown"}
    # Only separators typed in the template may create directories; metadata
    # always occupies one component, including titles containing slashes.
    context = {key: filename_component(value) for key, value in context.items()}
    context["output_path"] = str(base)
    # Expand a home directory only when the user wrote it in the template;
    # a video titled "~" must remain inside the configured output folder.
    if template.template.startswith("~"):
        template = Template(str(Path(template.template).expanduser()))
    path = Path(template.substitute(context))
    if ".." in path.parts:
        raise ValueError("Title formatting cannot contain parent-folder traversal (..).")
    anchor = Path(path.anchor) if path.is_absolute() else base
    parts = path.parts[1:] if path.is_absolute() else path.parts
    if path.is_relative_to(base):
        anchor, parts = base, path.relative_to(base).parts
    if not parts:
        raise ValueError("Title formatting must include a filename.")
    return anchor.joinpath(*(filename_component(part) for part in parts))


def video_file_path(path: Path) -> Path:
    """Dots in ordinary titles must not suppress the media extension."""
    return path if path.suffix.casefold() in VIDEO_EXTENSIONS else Path(str(path) + ".mp4")
