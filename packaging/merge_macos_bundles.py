"""Merge matching native binaries and verify every Mach-O has both macOS slices."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path


def is_macho(path: Path) -> bool:
    return "Mach-O" in subprocess.check_output(["file", "-b", str(path)], text=True)


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
            sources = ((intel / relative, "x86_64"), (arm / relative, "arm64"))
            if all(source.is_file() and is_macho(source) for source, _ in sources):
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
                print(f"Fusing: {relative}")
                # Separate slices avoid duplicate architectures and in-place lipo input/output.
                subprocess.run(["lipo", "-create", *slices, "-output", str(destination)], check=True)
            subprocess.run(["lipo", str(destination), "-verify_arch", "x86_64", "arm64"], check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intel", type=Path)
    parser.add_argument("arm", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    merge_bundles(args.intel, args.arm, args.output)
