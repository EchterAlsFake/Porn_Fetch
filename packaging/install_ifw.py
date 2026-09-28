"""Install pinned Qt Installer Framework build tools for CI."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

IFW_ARCHIVES = {
    "linux": (
        "https://download.qt.io/online/qtsdkrepository/linux_x64/ifw/tools_ifw_411/"
        "qt.tools.ifw.411/4.11.0-0-202603231357ifw-linux-x64.7z",
        "79ef906970c7e4be9ec15447fd5acb0a8ae2ab41aef5f9184086ce3972eddbc7",
    ),
    "windows": (
        "https://download.qt.io/online/qtsdkrepository/windows_x86/ifw/tools_ifw_411/"
        "qt.tools.ifw.411/4.11.0-0-202603231357ifw-win-x64.7z",
        "c47201c4f6a82a8b607daa245237f40831d78425e904edd1514b71fd17efefc1",
    ),
    "macos": (
        "https://download.qt.io/online/qtsdkrepository/mac_x64/ifw/tools_ifw_411/"
        "qt.tools.ifw.411/4.11.0-0-202603311245ifw-mac-universal.7z",
        "140397cb4776a00a8efb76e5b8a362f8e6adc9a213da7a074e81b9b912f0c8f3",
    ),
}


def _extractor() -> str:
    found = shutil.which("7z") or shutil.which("7zz")
    if found:
        return found
    if sys.platform == "win32":
        windows_7z = Path("C:/Program Files/7-Zip/7z.exe")
        if windows_7z.is_file():
            return str(windows_7z)
    raise RuntimeError("7z is required to extract Qt Installer Framework")


def install(platform: str, destination: Path, archive: Path | None = None) -> Path:
    url, expected_hash = IFW_ARCHIVES[platform]
    destination.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temporary:
        download = Path(temporary) / "ifw.7z"
        if archive is not None:
            shutil.copyfile(archive, download)
        else:
            with urllib.request.urlopen(url, timeout=60) as response, download.open("wb") as output:
                shutil.copyfileobj(response, output)

        with download.open("rb") as source:
            actual_hash = hashlib.file_digest(source, "sha256").hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"Qt IFW archive hash mismatch for {platform}: {actual_hash}")

        subprocess.run([_extractor(), "x", "-y", f"-o{destination}", str(download)], check=True)

    suffix = ".exe" if platform == "windows" else ""
    binarycreator = destination / "bin" / f"binarycreator{suffix}"
    repogen = destination / "bin" / f"repogen{suffix}"
    installerbase = destination / "bin" / f"installerbase{suffix}"
    if not all(tool.is_file() for tool in (binarycreator, repogen, installerbase)):
        raise FileNotFoundError("Qt IFW archive did not contain binarycreator, repogen, and installerbase")
    if platform != "windows":
        for tool in (binarycreator, repogen, installerbase):
            tool.chmod(tool.stat().st_mode | 0o111)
    return binarycreator.parent.resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=IFW_ARCHIVES, required=True)
    parser.add_argument("--dest", type=Path, required=True)
    parser.add_argument("--archive", type=Path, help="Use a local archive, still verifying its pinned hash")
    args = parser.parse_args()
    print(install(args.platform, args.dest, args.archive))


if __name__ == "__main__":
    main()
