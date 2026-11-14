"""Portable, Qt-free metadata. Network-only artwork references are never serialized."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields


@dataclass(slots=True)
class Credit:
    name: str
    url: str | None = None


@dataclass(slots=True)
class LibraryMetadata:
    provider: str
    media_kind: str
    source_id: str
    source_url: str
    title: str
    description: str | None = None
    duration_seconds: float | None = None
    publication_date: str | None = None
    publication_raw: str | None = None
    publication_kind: str = "unknown"
    performers: list[Credit] = field(default_factory=list)
    performer_urls: list[str] = field(default_factory=list)
    uploader: Credit | None = None
    channels: list[Credit] = field(default_factory=list)
    publishers: list[Credit] = field(default_factory=list)
    content_providers: list[Credit] = field(default_factory=list)
    producers: list[Credit] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    extras: dict = field(default_factory=dict)
    image_url: str | None = field(default=None, repr=False)

    @property
    def identity(self) -> str:
        return f"{self.provider}:{self.media_kind}:{self.source_id}"

    def portable(self) -> dict:
        data = asdict(self)
        data.pop("image_url")
        return data

    @classmethod
    def from_portable(cls, data: dict) -> LibraryMetadata:
        """Read only the documented snapshot, never restore transient image URLs."""
        if not isinstance(data, dict):
            raise ValueError("Invalid Porn Fetch metadata snapshot")
        allowed = {item.name for item in fields(cls)} - {"image_url"}
        values = {name: value for name, value in data.items() if name in allowed}
        for name in ("provider", "media_kind", "source_id", "source_url", "title"):
            if not isinstance(values.get(name), str) or not values[name]:
                raise ValueError(f"Invalid metadata {name}")
        for name in ("performers", "channels", "publishers", "content_providers", "producers"):
            values[name] = [Credit(**item) for item in values.get(name, [])]
        if values.get("uploader"):
            values["uploader"] = Credit(**values["uploader"])
        return cls(**values)
