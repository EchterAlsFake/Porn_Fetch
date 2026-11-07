"""Complete the iOS FFmpeg source and rebuild bundle for a verified native extension."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def prepare(device: Path, archive: Path, *, binary_sha256: str | None = None) -> Path:
    provenance = json.loads((ROOT / "ios-lab/device/BUILD-REVISIONS.json").read_text())["ffmpeg"]
    binary = device / "native/packages/_ios_ffmpeg.cpython-315-iphoneos.so"
    if sha256(archive) != provenance["source_sha256"]:
        raise ValueError("iOS FFmpeg source archive does not match its pinned SHA-256")
    expected_binary = binary_sha256 or provenance["native_extension_sha256"]
    if sha256(binary) != expected_binary:
        raise ValueError("iOS FFmpeg extension does not match the recorded build; rebuild its legal materials with the extension")

    legal = device / "native/packages/ffmpeg-legal"
    # These are produced by the native build and must describe the actual binary.
    for name in ("COPYING.LGPLv2.1", "LICENSE.md", "config.h", "config_components.h", "configuration.txt"):
        if not (legal / name).is_file():
            raise FileNotFoundError(legal / name)
    shutil.copy2(archive, legal / archive.name)
    for name in ("bridge.c", "apple-probe.m"):
        shutil.copy2(ROOT / "ios-lab/device/ffmpeg" / name, legal / name)
    shutil.copy2(ROOT / "ios-lab/device/build-ffmpeg.py", legal / "build-ffmpeg.py")
    shutil.copy2(ROOT / "packaging/ffmpeg_configure_flags.txt", legal / "ffmpeg_configure_flags.txt")
    shutil.copy2(Path(__file__), legal / "prepare_ios_legal.py")
    shutil.copy2(ROOT / "ios-lab/device/ffmpeg/REBUILD.md", legal / "REBUILD.md")
    (legal / "build.json").write_text(json.dumps({
        "version": provenance["version"],
        "source_url": provenance["source_url"],
        "source_sha256": provenance["source_sha256"],
        "native_extension_sha256": expected_binary,
        "target": provenance["target"],
        "rebuild_instructions": "REBUILD.md",
    }, indent=2) + "\n", encoding="utf-8")
    return legal


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    args = parser.parse_args()
    print(f"Prepared iOS FFmpeg source and rebuild materials: {prepare(args.device, args.source_archive)}")
