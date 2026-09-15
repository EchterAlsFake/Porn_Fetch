"""Persistent tracked-profile state with ordered URL lists."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Iterable

from .paths import data_dir


class ModelStore:
    def __init__(
        self,
        path: str | Path | None = None,
        legacy_paths: Iterable[str | Path] | None = None,
    ) -> None:
        self.path = Path(path) if path else data_dir() / "model_database.json"
        if not self.path.exists():
            candidates = list(legacy_paths or (Path.cwd() / "model_database.json",))
            legacy = next((Path(item) for item in candidates if Path(item).is_file()), None)
            if legacy:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(legacy, self.path)

    def _read(self) -> dict[str, dict[str, list[str]]]:
        if not self.path.exists():
            return {}
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("model database must contain an object")
        result: dict[str, dict[str, list[str]]] = {}
        for model, state in raw.items():
            if not isinstance(model, str) or not isinstance(state, dict):
                continue
            downloaded = _ordered_unique(state.get("downloaded", []))
            pending = [url for url in _ordered_unique(state.get("pending", [])) if url not in downloaded]
            result[model] = {"downloaded": downloaded, "pending": pending}
        return result

    def _write(self, state: dict[str, dict[str, list[str]]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{self.path.name}.", dir=self.path.parent, text=True,
        )
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                json.dump(state, handle, indent=2, ensure_ascii=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, self.path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def models(self) -> list[tuple[str, dict[str, list[str]]]]:
        return list(self._read().items())

    def add(self, url: str) -> bool:
        url = url.strip()
        if not url:
            raise ValueError("model URL cannot be blank")
        state = self._read()
        if url in state:
            return False
        state[url] = {"downloaded": [], "pending": []}
        self._write(state)
        return True

    def remove(self, url: str) -> bool:
        state = self._read()
        if url not in state:
            return False
        del state[url]
        self._write(state)
        return True

    def update_pending(self, model_url: str, discovered: Iterable[str]) -> int:
        state = self._read()
        entry = state.setdefault(model_url, {"downloaded": [], "pending": []})
        known = set(entry["downloaded"]) | set(entry["pending"])
        added = 0
        for url in discovered:
            if url and url not in known:
                entry["pending"].append(url)
                known.add(url)
                added += 1
        self._write(state)
        return added

    def mark_downloaded(self, model_url: str, video_url: str) -> None:
        state = self._read()
        entry = state.setdefault(model_url, {"downloaded": [], "pending": []})
        entry["pending"] = [url for url in entry["pending"] if url != video_url]
        if video_url not in entry["downloaded"]:
            entry["downloaded"].append(video_url)
        self._write(state)

    def counts(self, model_url: str) -> tuple[int, int]:
        entry = self._read().get(model_url, {"downloaded": [], "pending": []})
        return len(entry["downloaded"]), len(entry["pending"])


def _ordered_unique(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return list(dict.fromkeys(value for value in values if isinstance(value, str)))
