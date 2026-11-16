#!/usr/bin/env python3
"""Build the embedded PocketBase runtime using Go and the Android NDK.

Outputs stay in build/android-pocketbase/<ABI>. The normal Android wrapper
invokes this automatically before packaging; no downloads occur on the device.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from urllib.request import urlopen

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import build_output

GO_VERSION = "1.27.4"
GO_ARCHIVES = {
    ("linux", "x86_64"): ("linux-amd64", "7226736c2339719cda28fbf3a54d71aa63bcefe376e98cef00034268dab24840"),
    ("darwin", "x86_64"): ("darwin-amd64", "2b799377704ef12db39bd254995d5c348c9cc8d86562ca817724390e56c38f43"),
    ("darwin", "arm64"): ("darwin-arm64", "91a44a2b8a716600ad94a4f143e156116620db8828086a6e3602291be9bd0bb4"),
}
TARGETS = {
    "aarch64": ("arm64-v8a", "arm64", "aarch64-linux-android"),
    "armv7a": ("armeabi-v7a", "arm", "armv7a-linux-androideabi"),
    "x86_64": ("x86_64", "amd64", "x86_64-linux-android"),
    "i686": ("x86", "386", "i686-linux-android"),
}
LIBRARY = "libpornfetch_pocketbase.so"


def go_tool(root: Path) -> Path:
    """Use the pinned compiler, fetching a verified archive when absent."""
    installed = shutil.which("go")
    if installed and subprocess.check_output([installed, "version"], text=True).split()[2] == "go" + GO_VERSION:
        return Path(installed)
    key = (sys.platform, platform.machine().lower())
    if key not in GO_ARCHIVES:
        raise RuntimeError(f"Install Go {GO_VERSION} on PATH for this build host: {key}")
    tag, checksum = GO_ARCHIVES[key]
    directory = root / "build/toolchains" / ("go" + GO_VERSION + "-" + tag)
    executable = directory / "go/bin/go"
    if executable.is_file():
        return executable
    directory.mkdir(parents=True, exist_ok=True)
    archive = directory / "toolchain.tar.gz"
    build_output.message(f"Downloading Go {GO_VERSION} for {tag} (SHA-256 verified)")
    with urlopen(f"https://go.dev/dl/go{GO_VERSION}.{tag}.tar.gz", timeout=120) as response, archive.open("wb") as output:
        shutil.copyfileobj(response, output)
    if hashlib.file_digest(archive.open("rb"), "sha256").hexdigest() != checksum:
        raise RuntimeError("Go toolchain checksum mismatch")
    with tarfile.open(archive) as package:
        package.extractall(directory, filter="data")
    archive.unlink()
    return executable


def collect_notices(go: Path, source: Path, destination: Path, environment: dict):
    """Retain Go/PocketBase/dependency notices alongside the APK's Python notices."""
    shutil.rmtree(destination, ignore_errors=True)
    destination.mkdir(parents=True)
    for name in ("main.go", "go.mod", "go.sum", "README.md"):
        shutil.copy2(source / name, destination / name)
    goroot = Path(subprocess.check_output([str(go), "env", "GOROOT"], text=True, env=environment).strip())
    shutil.copy2(goroot / "LICENSE", destination / "Go-LICENSE")
    modules = subprocess.check_output([str(go), "list", "-m", "-json", "all"], cwd=source, env=environment, text=True)
    decoder, position, inventory = json.JSONDecoder(), 0, []
    while position < len(modules):
        position += len(modules[position:]) - len(modules[position:].lstrip())
        if position >= len(modules):
            break
        module, position = decoder.raw_decode(modules, position)
        if module.get("Main"):
            continue
        directory = Path(module.get("Dir", ""))
        notices = []
        if module.get("Dir"):
            for path in directory.iterdir():
                if path.is_file() and path.name.upper().startswith(("LICENSE", "LICENCE", "COPYING", "NOTICE", "AUTHORS")):
                    target = destination / module["Path"] / path.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, target)
                    notices.append(str(target.relative_to(destination)))
        inventory.append({"module": module["Path"], "version": module.get("Version"), "notices": notices,
                          "source": f"https://proxy.golang.org/{module['Path']}/@v/{module.get('Version')}.zip"})
    (destination / "modules.json").write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")


def build(root: Path, architecture: str, ndk: Path, *, go: Path | None = None) -> Path:
    abi, goarch, triple = TARGETS[architecture]
    host = "darwin-x86_64" if sys.platform == "darwin" else "linux-x86_64"
    compiler = ndk / "toolchains/llvm/prebuilt" / host / "bin" / (triple + "28-clang")
    if not compiler.is_file():
        raise RuntimeError(f"Android NDK compiler is missing: {compiler}")
    go = go or go_tool(root)
    source = root / "native/pocketbase"
    destination = root / "build/android-pocketbase" / abi
    destination.mkdir(parents=True, exist_ok=True)
    environment = dict(os.environ, GOOS="android", GOARCH=goarch, CGO_ENABLED="1", CC=str(compiler),
                       GOARM="7", GOTOOLCHAIN="local")
    command = [str(go), "build", "-mod=readonly", "-buildmode=c-shared", "-trimpath",
               "-ldflags=-s -w -extldflags=-Wl,-z,max-page-size=16384", "-o", str(destination / LIBRARY), "."]
    build_output.run(command, label=f"Build Android PocketBase {abi}", cwd=source, env=environment)
    collect_notices(go, source, destination / "legal", environment)
    manifest = {"pocketbase": "0.40.4", "go": GO_VERSION, "abi": abi, "api": 28,
                "sha256": hashlib.file_digest((destination / LIBRARY).open("rb"), "sha256").hexdigest()}
    (destination / "build.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    build_output.message(f"Embedded PocketBase ready: {destination / LIBRARY}", "ok")
    return destination / LIBRARY


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", choices=[*TARGETS, "all"], default="all")
    parser.add_argument("--ndk", type=Path, required=True)
    parser.add_argument("--go", type=Path, help="explicit compatible Go compiler")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for architecture in TARGETS if args.architecture == "all" else [args.architecture]:
        build(root, architecture, args.ndk.resolve(), go=args.go)


if __name__ == "__main__":
    main()
