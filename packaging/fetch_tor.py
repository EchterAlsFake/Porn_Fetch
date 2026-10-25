"""Bundle a pinned Tor client and notices; never start Tor during a build."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path

SOURCES = Path(__file__).with_name("tor_sources.json")
ARCH = {"x64": "x86_64", "arm64": "aarch64", "x86": "i686", "x32": "i686",
        "arm64-v8a": "aarch64", "armeabi-v7a": "armv7", "armv7a": "armv7"}


def download(url, digest, destination):
    if destination.exists():
        with destination.open("rb") as source:
            if hashlib.file_digest(source, "sha256").hexdigest() == digest:
                return destination
        destination.unlink()
    with urllib.request.urlopen(url, timeout=120) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)
    with destination.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != digest:
            destination.unlink()
            raise ValueError("Tor source checksum mismatch")
    return destination


def build_linux_arm64(config, destination, work):
    source = config["linux_arm64_source"]
    archive = download(source["url"], source["sha256"], work / "tor-source.tar.gz")
    tree = work / "source"
    tree.mkdir(exist_ok=True)
    with tarfile.open(archive) as bundle:
        bundle.extractall(tree, filter="data")
    build = next(tree.glob("tor-*"))
    subprocess.run(["./configure", "--enable-static-tor", "--with-libevent-dir=/usr",
                    "--with-openssl-dir=/usr", "--with-zlib-dir=/usr", "--disable-asciidoc",
                    "--disable-manpage", "--disable-html-manual", "--disable-unittests",
                    "--disable-system-torrc", "--disable-lzma", "--disable-zstd"], cwd=build, check=True)
    subprocess.run(["make", "-j", str(min(os.cpu_count() or 2, 4))], cwd=build, check=True)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(build / "src/app/tor", destination / "tor")
    (destination / "notices").mkdir(exist_ok=True)
    for name in ("LICENSE", "COPYING"):
        if (build / name).exists():
            shutil.copy2(build / name, destination / "notices" / name)
    # libevent/OpenSSL/zlib are linked statically from the runner's dev packages.
    for package in ("libevent-dev", "libssl-dev", "zlib1g-dev"):
        path = Path("/usr/share/doc") / package / "copyright"
        shutil.copy2(path, destination / "notices" / (package + ".txt"))


def fetch(platform, architecture, destination, work):
    config = json.loads(SOURCES.read_text())
    work.mkdir(parents=True, exist_ok=True)
    if platform == "linux" and architecture in {"arm64", "aarch64"}:
        build_linux_arm64(config, destination, work)
    else:
        arch = ARCH.get(architecture, architecture)
        if platform == "windows" and architecture == "arm64":
            arch = "i686"  # Supported on Windows 10/11 ARM through x86 emulation.
        if platform == "android":
            arch = {"armv7a": "armv7", "i686": "x86", "arm64-v8a": "aarch64",
                    "armeabi-v7a": "armv7"}.get(architecture, architecture)
        name = f"tor-expert-bundle-{platform}-{arch}-{config['bundle_version']}.tar.gz"
        if name not in config["assets"]:
            raise ValueError(f"No pinned Tor bundle for {platform}/{architecture}")
        archive = download(config["base_url"] + name, config["assets"][name], work / name)
        with tempfile.TemporaryDirectory(dir=work) as temporary:
            root = Path(temporary)
            with tarfile.open(archive) as bundle:
                bundle.extractall(root, filter="data")
            shutil.copytree(root / "tor", destination, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("pluggable_transports"))
            shutil.copytree(root / "docs", destination / "notices", dirs_exist_ok=True)
    notices = destination / "notices"
    notices.mkdir(exist_ok=True)
    (notices / "SOURCE.md").write_text(
        "Tor runtime sources and reproducible build information\n\n"
        + config["linux_arm64_source"]["url"] + "\n"
        + config["base_url"] + "\n"
        + "https://gitlab.torproject.org/tpo/applications/tor-browser-build\n"
        + "Bundled components retain their included licenses.\n",
        encoding="utf-8",
    )
    shutil.copy2(SOURCES, destination / "provenance.json")
    for path in destination.rglob("*"):
        if path.is_file() and path.name in {"tor", "libTor.so"}:
            path.chmod(0o755)
    print(f"Prepared Tor runtime: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", choices=("linux", "windows", "macos", "android"), required=True)
    parser.add_argument("--arch", required=True)
    parser.add_argument("--dest", type=Path, default=Path(__file__).resolve().parents[1] / "src/shared/tor")
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    fetch(args.platform, args.arch, args.dest, args.work_dir)
