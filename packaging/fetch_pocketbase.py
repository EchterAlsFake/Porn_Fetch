"""Build-time tool to fetch and stage PocketBase binaries for packaging (Qt IFW, Nuitka)."""
from __future__ import annotations

import argparse
import logging
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Add project root to sys.path so we can import src.database
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database.installer import (
    DEFAULT_POCKETBASE_VERSION,
    download_and_extract_pocketbase,
    resolve_platform,
    verify_pocketbase_binary,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("fetch_pocketbase")


def create_macos_universal_binary(
    dest_path: Path,
    version: str = DEFAULT_POCKETBASE_VERSION,
) -> Path:
    """Download Intel and Apple Silicon macOS binaries and combine them with lipo."""
    if sys.platform != "darwin" and not shutil.which("lipo"):
        raise RuntimeError("Creating a macOS Universal2 binary requires the 'lipo' utility.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        intel_dir = tmp / "intel"
        arm_dir = tmp / "arm"
        intel_dir.mkdir(parents=True)
        arm_dir.mkdir(parents=True)

        logger.info("Downloading macOS Intel (amd64) binary...")
        intel_bin = download_and_extract_pocketbase(
            target_dir=intel_dir,
            version=version,
            os_name="darwin",
            machine="x86_64",
        )

        logger.info("Downloading macOS Apple Silicon (arm64) binary...")
        arm_bin = download_and_extract_pocketbase(
            target_dir=arm_dir,
            version=version,
            os_name="darwin",
            machine="arm64",
        )

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = ["lipo", "-create", "-output", str(dest_path), str(intel_bin), str(arm_bin)]
        logger.info("Running lipo to create universal binary: %s", " ".join(cmd))
        subprocess.run(cmd, check=True)
        dest_path.chmod(0o755)

    logger.info("Successfully created macOS Universal binary at: %s", dest_path)
    return dest_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch PocketBase binary for Qt Installer Framework / Nuitka packaging.",
    )
    parser.add_argument(
        "--platform",
        dest="target_platform",
        choices=["linux", "windows", "macos", "darwin", "win32"],
        default=None,
        help="Target operating system (defaults to current OS)",
    )
    parser.add_argument(
        "--arch",
        dest="target_arch",
        default=None,
        help="Target CPU architecture: x64/amd64, arm64/aarch64, armv7 (defaults to current arch)",
    )
    parser.add_argument(
        "--dest",
        dest="dest_dir",
        type=Path,
        default=None,
        help="Destination directory to place the binary (e.g. Qt IFW packages/.../data/)",
    )
    parser.add_argument(
        "--version",
        dest="version",
        default=DEFAULT_POCKETBASE_VERSION,
        help=f"PocketBase release version (default: {DEFAULT_POCKETBASE_VERSION})",
    )
    parser.add_argument(
        "--universal",
        action="store_true",
        help="Create a macOS Universal2 binary (lipo Intel + ARM64)",
    )

    args = parser.parse_args(argv)

    target_os = args.target_platform or platform.system().lower()
    target_arch = args.target_arch or platform.machine().lower()

    os_label, arch_label, binary_name = resolve_platform(target_os, target_arch)

    # Default destination: packaging/pocketbase/{os_label}
    dest_dir = args.dest_dir or (PROJECT_ROOT / "packaging" / "pocketbase" / os_label)
    dest_dir.mkdir(parents=True, exist_ok=True)
    target_binary = dest_dir / binary_name

    logger.info("Target: %s (%s)", os_label, arch_label)
    logger.info("Output: %s", target_binary)

    if args.universal or (target_os in {"darwin", "macos"} and target_arch in {"universal", "universal2"}):
        create_macos_universal_binary(target_binary, version=args.version)
    else:
        download_and_extract_pocketbase(
            target_dir=dest_dir,
            version=args.version,
            os_name=os_label,
            machine=arch_label,
        )

    logger.info("PocketBase successfully staged at %s", target_binary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
