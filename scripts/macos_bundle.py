"""Keep runtime data discoverable without placing it in macOS code locations."""

from __future__ import annotations

import os
from pathlib import Path

MACHO_MAGIC = {
    bytes.fromhex(value)
    for value in ("feedface", "cefaedfe", "feedfacf", "cffaedfe", "cafebabe", "bebafeca", "cafebabf", "bfbafeca")
}
BUNDLE_SUFFIXES = {".app", ".framework", ".xpc", ".appex", ".bundle"}


def is_macho(path: Path) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    with path.open("rb") as source:
        return source.read(4) in MACHO_MAGIC


def relocate_resources(bundle: Path) -> int:
    """Move Nuitka data to Resources and retain relative runtime paths via symlinks."""
    macos = bundle / "Contents/MacOS"
    resources = bundle / "Contents/Resources/runtime"
    moved = 0
    for path in sorted(macos.rglob("*")):
        if path.is_symlink() or not path.is_file() or is_macho(path):
            continue
        relative = path.relative_to(macos)
        # Nested bundles already have their own resource/signature layout.
        if "_CodeSignature" in relative.parts or any(parent.suffix in BUNDLE_SUFFIXES for parent in relative.parents):
            continue
        target = resources / relative
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Bundle resource already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        path.rename(target)
        path.symlink_to(os.path.relpath(target, path.parent))
        moved += 1
    return moved
