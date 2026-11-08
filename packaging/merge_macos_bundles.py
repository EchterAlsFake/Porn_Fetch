"""Merge macOS bundles and repair OpenSSL library layout differences."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_output  # noqa: E402
from scripts.macos_bundle import (  # noqa: E402
    OPENSSL_ALIASES,
    repair_openssl_references,
    verify_bundle_dependencies,
)

# PyCryptodome loads these only when the CPU supports AES-NI or CLMUL.
# ARM uses _raw_aes and _ghash_portable, which must still have both slices.
INTEL_ONLY_ACCELERATORS = {
    Path("Contents/MacOS/Cryptodome/Cipher/_raw_aesni.so"),
    Path("Contents/MacOS/Cryptodome/Hash/_ghash_clmul.so"),
}


def is_macho(path: Path) -> bool:
    return "Mach-O" in subprocess.check_output(["file", "-b", str(path)], text=True)


def openssl_source(bundle: Path, relative: Path) -> Path:
    source = bundle / relative
    if source.exists() or relative not in OPENSSL_ALIASES:
        return source
    fallback = source.with_name(OPENSSL_ALIASES[relative])
    if fallback.is_file() and is_macho(fallback):
        build_output.detail(f"Using {fallback.relative_to(bundle)} for missing {relative}")
        return fallback
    return source


def verify_openssl_abi(source: Path, expected: str) -> None:
    output = subprocess.check_output(["otool", "-D", str(source)], text=True)
    names = {Path(line.strip()).name for line in output.splitlines()
             if line.strip() and not line.endswith(":")}
    if names != {expected}:
        raise ValueError(f"Expected OpenSSL 3 install name {expected}, found {names}: {source}")


def merge_bundles(intel: Path, arm: Path, output: Path) -> None:
    shutil.copytree(intel, output, symlinks=True)
    for source in sorted(arm.rglob("*")):
        destination = output / source.relative_to(arm)
        if source.is_symlink():
            if not destination.exists() and not destination.is_symlink():
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.symlink_to(source.readlink())
        elif source.is_file() and not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    with tempfile.TemporaryDirectory() as temporary:
        for destination in sorted(output.rglob("*")):
            if destination.is_symlink() or not destination.is_file() or not is_macho(destination):
                continue
            relative = destination.relative_to(output)
            sources = ((openssl_source(intel, relative), "x86_64"), (openssl_source(arm, relative), "arm64"))
            required_architectures = ("x86_64", "arm64")
            if all(source.is_file() and is_macho(source) for source, _ in sources):
                if relative in OPENSSL_ALIASES:
                    for source, _ in sources:
                        verify_openssl_abi(source, OPENSSL_ALIASES[relative])
                slices = []
                for source, architecture in sources:
                    thin = Path(temporary) / architecture
                    architectures = subprocess.check_output(["lipo", "-archs", str(source)], text=True).split()
                    if architecture not in architectures:
                        raise ValueError(f"Missing {architecture} slice: {source}")
                    if len(architectures) == 1:
                        shutil.copy2(source, thin)
                    else:
                        subprocess.run(["lipo", str(source), "-thin", architecture, "-output", str(thin)], check=True)
                    slices.append(str(thin))
                build_output.detail(f"Fusing: {relative}")
                # Separate slices avoid duplicate architectures and in-place lipo input/output.
                subprocess.run(["lipo", "-create", *slices, "-output", str(destination)], check=True)
            elif relative in INTEL_ONLY_ACCELERATORS and not (arm / relative).exists():
                build_output.detail(f"Keeping Intel-only accelerator: {relative}")
                required_architectures = ("x86_64",)
            subprocess.run(["lipo", str(destination), "-verify_arch", *required_architectures], check=True)

    for binary in sorted(output.rglob("*")):
        if not binary.is_symlink() and binary.is_file() and is_macho(binary):
            repair_openssl_references(binary, output)
    verify_bundle_dependencies(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intel", type=Path)
    parser.add_argument("arm", type=Path)
    parser.add_argument("output", type=Path)
    build_output.add_arguments(parser)
    args = parser.parse_args()
    build_output.configure(args)
    build_output.message("Merge macOS architectures")
    merge_bundles(args.intel, args.arm, args.output)
    build_output.message(f"Universal macOS bundle: {args.output}", "ok")
