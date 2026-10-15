#!/usr/bin/env python3
"""Download and extract the appropriate static FFmpeg executable for packaging."""
from __future__ import annotations

import argparse
import io
import platform
import stat
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

# yt-dlp publishes Linux/Windows builds; Martin Riedl provides macOS builds.
YTDLP_RELEASE = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest"
DOWNLOAD_URLS: dict[tuple[str, str], str] = {
    ("darwin", "x64"): "https://ffmpeg.martin-riedl.de/redirect/latest/macos/amd64/release/ffmpeg.zip",
    ("darwin", "arm64"): "https://ffmpeg.martin-riedl.de/redirect/latest/macos/arm64/release/ffmpeg.zip",
    ("linux", "x64"): f"{YTDLP_RELEASE}/ffmpeg-master-latest-linux64-gpl.tar.xz",
    ("linux", "arm64"): f"{YTDLP_RELEASE}/ffmpeg-master-latest-linuxarm64-gpl.tar.xz",
    ("windows", "x64"): f"{YTDLP_RELEASE}/ffmpeg-master-latest-win64-gpl.zip",
    ("windows", "arm64"): f"{YTDLP_RELEASE}/ffmpeg-master-latest-winarm64-gpl.zip",
}


def normalize_platform(target: str) -> str:
    t = target.lower()
    if "darwin" in t or "mac" in t:
        return "darwin"
    if "win" in t:
        return "windows"
    if "linux" in t:
        return "linux"
    return t


def normalize_arch(target: str) -> str:
    t = target.lower()
    if t in ("x86_64", "amd64", "x64"):
        return "x64"
    if t in ("aarch64", "arm64"):
        return "arm64"
    if t in ("i386", "i686", "x86"):
        return "x86"
    return t


def download_ffmpeg(
    target_platform: str,
    target_arch: str,
    destination: Path,
) -> Path | None:
    norm_plat = normalize_platform(target_platform)
    norm_arch = normalize_arch(target_arch)

    asset_key = (norm_plat, norm_arch)
    url = DOWNLOAD_URLS.get(asset_key)
    if not url:
        print(
            f"Notice: No prebuilt FFmpeg binary available for {norm_plat}-{norm_arch}. "
            f"FFmpeg integration will rely on PATH or runtime discovery.",
            file=sys.stderr,
        )
        return None

    binary_name = "ffmpeg.exe" if norm_plat == "windows" else "ffmpeg"
    asset_name = url.rsplit("/", 1)[-1]
    print(f"Downloading FFmpeg for {norm_plat}-{norm_arch} from {url}...")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Porn-Fetch-CI/3.9"},
    )
    with urllib.request.urlopen(request) as resp:
        archive_bytes = resp.read()

    destination.mkdir(parents=True, exist_ok=True)
    target_file = destination / binary_name

    if asset_name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(archive_bytes)) as zf:
            matching = [name for name in zf.namelist() if Path(name).name.lower() == binary_name.lower()]
            if not matching:
                raise FileNotFoundError(f"Binary '{binary_name}' not found inside archive '{asset_name}'")
            extracted_bytes = zf.read(matching[0])
            target_file.write_bytes(extracted_bytes)
    else:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:xz") as tf:
            matching_member = None
            for member in tf.getmembers():
                if Path(member.name).name == binary_name and member.isfile():
                    matching_member = member
                    break
            if not matching_member:
                raise FileNotFoundError(f"Binary '{binary_name}' not found inside archive '{asset_name}'")
            extracted_f = tf.extractfile(matching_member)
            if not extracted_f:
                raise RuntimeError(f"Could not extract {binary_name} from archive")
            target_file.write_bytes(extracted_f.read())

    if norm_plat != "windows":
        target_file.chmod(target_file.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Successfully saved FFmpeg binary to: {target_file} ({target_file.stat().st_size / (1024 * 1024):.1f} MB)")
    return target_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Download FFmpeg executable for builds.")
    parser.add_argument(
        "--platform",
        default=sys.platform,
        help="Target platform (linux, windows, macos/darwin)",
    )
    parser.add_argument(
        "--arch",
        default=platform.machine(),
        help="Target architecture (x64, arm64, etc.)",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("third_party"),
        help="Destination directory where ffmpeg will be saved",
    )
    args = parser.parse_args()

    result = download_ffmpeg(
        target_platform=args.platform,
        target_arch=args.arch,
        destination=args.dest,
    )
    return 0 if result is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
