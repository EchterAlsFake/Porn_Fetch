"""PocketBase automated platform detection, download, and installation."""
from __future__ import annotations

import logging
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from collections.abc import Callable
from pathlib import Path

from .errors import PocketBaseError

logger = logging.getLogger(__name__)

DEFAULT_POCKETBASE_VERSION = "0.40.4"


def resolve_platform(
    os_name: str | None = None,
    machine: str | None = None,
) -> tuple[str, str, str]:
    """Map system platform and architecture to PocketBase release asset identifiers.

    Returns:
        (os_label, arch_label, binary_name)
        e.g. ("linux", "amd64", "pocketbase") or ("windows", "amd64", "pocketbase.exe")
    """
    raw_os = (os_name or platform.system()).lower()
    raw_machine = (machine or platform.machine()).lower()

    if raw_os in {"windows", "win32"}:
        os_label = "windows"
        binary_name = "pocketbase.exe"
    elif raw_os in {"darwin", "macos"}:
        os_label = "darwin"
        binary_name = "pocketbase"
    elif raw_os.startswith("linux"):
        os_label = "linux"
        binary_name = "pocketbase"
    else:
        raise PocketBaseError(f"Unsupported operating system for PocketBase: {raw_os}")

    if raw_machine in {"x86_64", "amd64", "x64"}:
        arch_label = "amd64"
    elif raw_machine in {"aarch64", "arm64"}:
        arch_label = "arm64"
    elif raw_machine in {"armv7l", "armv7"}:
        arch_label = "armv7"
    else:
        raise PocketBaseError(f"Unsupported architecture for PocketBase: {raw_machine}")

    return os_label, arch_label, binary_name


def get_pocketbase_download_url(
    version: str = DEFAULT_POCKETBASE_VERSION,
    os_name: str | None = None,
    machine: str | None = None,
) -> tuple[str, str]:
    """Return the GitHub release download URL and expected executable name."""
    clean_version = version.lstrip("v")
    os_label, arch_label, binary_name = resolve_platform(os_name, machine)
    asset_name = f"pocketbase_{clean_version}_{os_label}_{arch_label}.zip"
    url = f"https://github.com/pocketbase/pocketbase/releases/download/v{clean_version}/{asset_name}"
    return url, binary_name


def check_system_path() -> Path | None:
    """Return the path to a PocketBase binary found on PATH, or None."""
    binary_name = "pocketbase.exe" if sys.platform == "win32" else "pocketbase"
    which = shutil.which(binary_name) or shutil.which("pocketbase")
    if which:
        candidate = Path(which).resolve()
        if candidate.is_file() and (sys.platform == "win32" or os.access(candidate, os.X_OK)):
            return candidate
    return None


def get_default_bin_dir() -> Path:
    """Return the platform-appropriate directory for user-installed binaries."""
    try:
        from src.cli.paths import shared_data_dir
        return shared_data_dir() / "bin"
    except Exception:
        if sys.platform == "win32":
            base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif sys.platform == "darwin":
            base = Path.home() / "Library" / "Application Support"
        else:
            base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        return base / "Porn Fetch" / "bin"


def verify_pocketbase_binary(binary_path: Path) -> str:
    """Run `pocketbase --version` to ensure the binary is functional and compatible."""
    if not binary_path.is_file():
        raise PocketBaseError(f"PocketBase binary file does not exist: {binary_path}")
    if sys.platform != "win32" and not os.access(binary_path, os.X_OK):
        raise PocketBaseError(f"PocketBase binary is not executable: {binary_path}")

    try:
        creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        proc = subprocess.run(
            [str(binary_path), "--version"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            text=True,
            check=False,
            creationflags=creation_flags,
        )
        if proc.returncode != 0:
            error_output = (proc.stderr or proc.stdout).strip()
            raise PocketBaseError(f"PocketBase check failed with code {proc.returncode}: {error_output}")
        output = (proc.stdout or "").strip()
        logger.info("Verified PocketBase binary at %s (%s)", binary_path, output)
        return output
    except Exception as exc:
        if isinstance(exc, PocketBaseError):
            raise
        raise PocketBaseError(f"Failed to execute PocketBase binary at {binary_path}: {exc}") from exc


def download_and_extract_pocketbase(
    target_dir: Path | None = None,
    version: str = DEFAULT_POCKETBASE_VERSION,
    os_name: str | None = None,
    machine: str | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
) -> Path:
    """Download the official PocketBase zip archive and extract the binary into target_dir."""
    dest_dir = (target_dir or get_default_bin_dir()).resolve()
    dest_dir.mkdir(parents=True, exist_ok=True)

    url, binary_name = get_pocketbase_download_url(version, os_name, machine)
    target_binary = dest_dir / binary_name

    logger.info("Downloading PocketBase from %s to %s", url, target_binary)

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Porn-Fetch-Installer/3.9"},
    )

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
        tmp_path = Path(tmp_file.name)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                total_size = int(response.headers.get("Content-Length", 0))
                bytes_downloaded = 0
                chunk_size = 64 * 1024

                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    tmp_file.write(chunk)
                    bytes_downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(bytes_downloaded, total_size)

            tmp_file.flush()
            tmp_file.close()

            # Extract executable from zip
            with zipfile.ZipFile(tmp_path, "r") as archive:
                member_names = archive.namelist()
                matched_name = None
                for name in member_names:
                    if Path(name).name.lower() == binary_name.lower():
                        matched_name = name
                        break
                if not matched_name:
                    raise PocketBaseError(
                        f"PocketBase archive did not contain expected binary '{binary_name}'. "
                        f"Found: {member_names}"
                    )

                extracted_path = archive.extract(matched_name, path=dest_dir)
                final_path = Path(extracted_path)
                if final_path != target_binary:
                    shutil.move(str(final_path), str(target_binary))

        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    # Ensure executable permissions on Unix
    if sys.platform != "win32":
        current_mode = target_binary.stat().st_mode
        target_binary.chmod(current_mode | 0o755)

    verify_pocketbase_binary(target_binary)
    return target_binary.resolve()


def install_pocketbase(
    force_download: bool = False,
    target_dir: Path | None = None,
    version: str = DEFAULT_POCKETBASE_VERSION,
    progress_callback: Callable[[int, int], None] | None = None,
) -> tuple[Path, str]:
    """Check PATH first (unless force_download=True); otherwise download and install.

    Returns:
        tuple[Path, str]: (binary_path, "path" | "downloaded")
    """
    if not force_download:
        if path_binary := check_system_path():
            try:
                verify_pocketbase_binary(path_binary)
                return path_binary, "path"
            except Exception as exc:
                logger.warning("PocketBase on PATH was found at %s but failed verification: %s", path_binary, exc)

    installed_binary = download_and_extract_pocketbase(
        target_dir=target_dir,
        version=version,
        progress_callback=progress_callback,
    )
    return installed_binary, "downloaded"
