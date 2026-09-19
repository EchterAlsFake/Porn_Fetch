#!/usr/bin/env python3
"""Download and extract the appropriate PocketBase executable for packaging."""
from __future__ import annotations

import argparse
import io
import platform
import stat
import sys
import urllib.request
import zipfile
from pathlib import Path

POCKETBASE_VERSION = "0.40.4"

# Mapping: (normalized_platform, normalized_arch) -> release_asset_name
ASSET_MAP: dict[tuple[str, str], str] = {
    ("darwin", "x64"): f"pocketbase_{POCKETBASE_VERSION}_darwin_amd64.zip",
    ("darwin", "arm64"): f"pocketbase_{POCKETBASE_VERSION}_darwin_arm64.zip",
    ("macos", "x64"): f"pocketbase_{POCKETBASE_VERSION}_darwin_amd64.zip",
    ("macos", "arm64"): f"pocketbase_{POCKETBASE_VERSION}_darwin_arm64.zip",
    ("linux", "x64"): f"pocketbase_{POCKETBASE_VERSION}_linux_amd64.zip",
    ("linux", "arm64"): f"pocketbase_{POCKETBASE_VERSION}_linux_arm64.zip",
    ("linux", "armv7"): f"pocketbase_{POCKETBASE_VERSION}_linux_armv7.zip",
    ("linux", "ppc64le"): f"pocketbase_{POCKETBASE_VERSION}_linux_ppc64le.zip",
    ("linux", "s390x"): f"pocketbase_{POCKETBASE_VERSION}_linux_s390x.zip",
    ("windows", "x64"): f"pocketbase_{POCKETBASE_VERSION}_windows_amd64.zip",
    ("windows", "arm64"): f"pocketbase_{POCKETBASE_VERSION}_windows_arm64.zip",
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


def download_pocketbase(
    target_platform: str,
    target_arch: str,
    destination: Path,
    version: str = POCKETBASE_VERSION,
) -> Path | None:
    norm_plat = normalize_platform(target_platform)
    norm_arch = normalize_arch(target_arch)

    asset_key = (norm_plat, norm_arch)
    asset_name = ASSET_MAP.get(asset_key)
    if not asset_name:
        print(
            f"Notice: No prebuilt PocketBase binary available for {norm_plat}-{norm_arch}. "
            f"PocketBase integration will rely on PATH or runtime discovery.",
            file=sys.stderr,
        )
        return None

    # Replace version in asset name if custom version requested
    if version != POCKETBASE_VERSION:
        asset_name = asset_name.replace(POCKETBASE_VERSION, version)

    binary_name = "pocketbase.exe" if norm_plat == "windows" else "pocketbase"
    url = f"https://github.com/pocketbase/pocketbase/releases/download/v{version}/{asset_name}"
    print(f"Downloading PocketBase v{version} for {norm_plat}-{norm_arch} from {url}...")

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Porn-Fetch-CI/3.9"},
    )
    with urllib.request.urlopen(request) as resp:
        zip_bytes = resp.read()

    destination.mkdir(parents=True, exist_ok=True)
    target_file = destination / binary_name

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        matching = [name for name in zf.namelist() if Path(name).name == binary_name]
        if not matching:
            raise FileNotFoundError(f"Binary '{binary_name}' not found inside archive '{asset_name}'")
        extracted_bytes = zf.read(matching[0])
        target_file.write_bytes(extracted_bytes)

    if norm_plat != "windows":
        target_file.chmod(target_file.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(f"Successfully saved PocketBase binary to: {target_file}")
    return target_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Download PocketBase executable for builds.")
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
        default=Path("."),
        help="Destination directory where pocketbase will be saved",
    )
    parser.add_argument(
        "--version",
        default=POCKETBASE_VERSION,
        help="PocketBase version to download (default: 0.40.4)",
    )
    args = parser.parse_args()

    result = download_pocketbase(
        target_platform=args.platform,
        target_arch=args.arch,
        destination=args.dest,
        version=args.version,
    )
    return 0 if result is not None or normalize_arch(args.arch) in ("x86", "riscv64") else 1


if __name__ == "__main__":
    raise SystemExit(main())
