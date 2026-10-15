"""Build the pinned LGPL-only FFmpeg executable for local remuxing and MP4 tags."""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VERSION = "9.0.2"
SOURCE_URL = f"https://ffmpeg.org/releases/ffmpeg-{VERSION}.tar.xz"
SOURCE_SHA256 = "8c3850283eb25fa026482078a04051e0be17347b09ef81a0849bec15a96e002e"
FLAGS_FILE = Path(__file__).with_name("ffmpeg_configure_flags.txt")


def normalize_platform(value: str) -> str:
    return {"macos": "darwin", "win32": "windows"}.get(value.lower(), value.lower())


def normalize_arch(value: str) -> str:
    return {"amd64": "x64", "x86_64": "x64", "aarch64": "arm64"}.get(value.lower(), value.lower())


async def download_source(destination: Path) -> None:
    from base_api import BaseCore

    async with BaseCore() as core:
        response = await core.request(url=SOURCE_URL, timeout=120)
        response.raise_for_status()
        destination.write_bytes(response.content)


def build_tools(target_platform: str, arch: str, msys2_root: Path | None) -> tuple[str, str, dict[str, str]]:
    environment = os.environ.copy()
    if target_platform != "windows":
        return shutil.which("bash") or "bash", shutil.which("make") or "make", environment
    if msys2_root is None:
        raise ValueError("Windows FFmpeg builds require --msys2-root pointing to the MSYS2 installation")
    root = msys2_root.resolve()
    tools = root / "usr/bin"
    bash, make = tools / "bash.exe", tools / "make.exe"
    for executable in (bash, make):
        if not executable.is_file():
            raise FileNotFoundError(executable)
    compiler = root / ("clangarm64/bin" if arch == "arm64" else "clang64/bin")
    environment["PATH"] = os.pathsep.join((str(compiler), str(tools), environment.get("PATH", "")))
    return str(bash), str(make), environment


def build(target_platform: str, arch: str, destination: Path, work: Path,
          source_archive: Path | None = None, jobs: int = 2, msys2_root: Path | None = None) -> Path:
    target_platform = normalize_platform(target_platform)
    arch = normalize_arch(arch)
    host = (normalize_platform(sys.platform), normalize_arch(platform.machine()))
    if ((target_platform, arch) != host or target_platform not in {"linux", "darwin", "windows"}
            or arch not in {"x64", "arm64"}):
        raise ValueError(f"Build natively on {target_platform}/{arch}; current host is {host[0]}/{host[1]}")
    bash, make, environment = build_tools(target_platform, arch, msys2_root)
    work = work.resolve()
    destination = destination.resolve()
    work.mkdir(parents=True, exist_ok=True)
    archive = source_archive.resolve() if source_archive else work / f"ffmpeg-{VERSION}.tar.xz"
    if not archive.is_file():
        if source_archive:
            raise FileNotFoundError(archive)
        asyncio.run(download_source(archive))
    with archive.open("rb") as source:
        if hashlib.file_digest(source, "sha256").hexdigest() != SOURCE_SHA256:
            raise ValueError("FFmpeg source archive does not match the pinned SHA-256")

    source_dir = work / f"ffmpeg-{VERSION}"
    build_dir = work / "compile"
    # A fresh source tree ensures the published archive matches what was compiled.
    for directory in (source_dir, build_dir):
        if directory.exists():
            shutil.rmtree(directory)
    with tarfile.open(archive, "r:xz") as bundle:
        bundle.extractall(work, filter="data")
    build_dir.mkdir()
    flags = FLAGS_FILE.read_text(encoding="utf-8").splitlines()
    flags.append(f"--arch={'aarch64' if arch == 'arm64' else 'x86_64'}")
    if target_platform == "windows":
        # Run inside an MSYS2 CLANG64 / CLANGARM64 shell. No MSYS DLLs are linked.
        flags.extend(["--target-os=mingw32", "--cc=clang", "--strip=llvm-strip",
                      "--extra-ldflags=-static", "--disable-pthreads", "--enable-w32threads"])
    elif target_platform == "darwin":
        flags.extend(["--cc=clang", "--extra-cflags=-mmacosx-version-min=11.0",
                      "--extra-ldflags=-mmacosx-version-min=11.0"])
    command = [bash, (source_dir / "configure").as_posix(), *flags]
    subprocess.run(command, cwd=build_dir, env=environment, check=True)
    config = (build_dir / "config.h").read_text(encoding="utf-8")
    for option in ("GPL", "VERSION3", "NONFREE"):
        if f"#define CONFIG_{option} 0" not in config:
            raise ValueError(f"FFmpeg must be built with CONFIG_{option}=0")
    components = (build_dir / "config_components.h").read_text(encoding="utf-8")
    if re.search(r"^#define CONFIG_\w+_ENCODER 1$", components, re.MULTILINE):
        raise ValueError("The remux-only FFmpeg build must not contain encoders")
    binary_name = "ffmpeg.exe" if target_platform == "windows" else "ffmpeg"
    subprocess.run([make, f"-j{jobs}", binary_name], cwd=build_dir, env=environment, check=True)
    executable = build_dir / binary_name
    license_text = subprocess.check_output([str(executable), "-hide_banner", "-L"],
                                          stderr=subprocess.STDOUT, text=True)
    if "GNU Lesser General Public" not in license_text or "version 2.1" not in license_text:
        raise ValueError("The FFmpeg executable does not report the expected LGPL license")

    destination.mkdir(parents=True, exist_ok=True)
    result = destination / binary_name
    shutil.copy2(executable, result)
    result.chmod(0o755)
    legal = destination / "ffmpeg-legal"
    legal.mkdir(exist_ok=True)
    shutil.copy2(archive, legal / f"ffmpeg-{VERSION}.tar.xz")
    for name in ("COPYING.LGPLv2.1", "LICENSE.md"):
        shutil.copy2(source_dir / name, legal / name)
    for name in ("config.h", "config_components.h"):
        shutil.copy2(build_dir / name, legal / name)
    (legal / "version.txt").write_text(subprocess.check_output(
        [str(result), "-version"], stderr=subprocess.STDOUT, text=True), encoding="utf-8")
    if target_platform == "windows":
        # The Windows executable statically links MSYS2's permissively licensed zlib.
        include = subprocess.check_output(["pkg-config", "--variable=includedir", "zlib"],
                                          env=environment, text=True).strip()
        include = subprocess.check_output(["cygpath", "-w", include], env=environment, text=True).strip()
        shutil.copy2(Path(include) / "zlib.h", legal / "zlib.h")
    (legal / "configuration.txt").write_text(
        shlex.join(["bash", f"ffmpeg-{VERSION}/configure", *flags]) + f"\nmake {binary_name}\n", encoding="utf-8")
    (legal / "build.json").write_text(json.dumps({
        "version": VERSION, "platform": target_platform, "arch": arch,
        "source_url": SOURCE_URL, "source_sha256": SOURCE_SHA256,
        "binary_sha256": hashlib.sha256(result.read_bytes()).hexdigest(),
        "configure_flags": flags,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Built LGPL-only FFmpeg: {result} ({result.stat().st_size / 1024**2:.2f} MiB)")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform", default=sys.platform)
    parser.add_argument("--arch", default=platform.machine())
    parser.add_argument("--dest", type=Path, default=PROJECT_ROOT / "third_party")
    parser.add_argument("--work-dir", type=Path, default=PROJECT_ROOT / "build/ffmpeg")
    parser.add_argument("--source-archive", type=Path)
    parser.add_argument("--msys2-root", type=Path, help="Windows: MSYS2 installation directory")
    parser.add_argument("--jobs", type=int, default=min(os.cpu_count() or 2, 4))
    args = parser.parse_args()
    build(args.platform, args.arch, args.dest, args.work_dir, args.source_archive, args.jobs, args.msys2_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
