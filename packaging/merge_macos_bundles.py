"""Merge macOS bundles and repair OpenSSL library layout differences."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

# PyCryptodome loads these only when the CPU supports AES-NI or CLMUL.
# ARM uses _raw_aes and _ghash_portable, which must still have both slices.
INTEL_ONLY_ACCELERATORS = {
    Path("Contents/MacOS/Cryptodome/Cipher/_raw_aesni.so"),
    Path("Contents/MacOS/Cryptodome/Hash/_ghash_clmul.so"),
}
OPENSSL_ALIASES = {
    Path("Contents/MacOS/libcrypto.dylib"): "libcrypto.3.dylib",
    Path("Contents/MacOS/libssl.dylib"): "libssl.3.dylib",
}


def is_macho(path: Path) -> bool:
    return "Mach-O" in subprocess.check_output(["file", "-b", str(path)], text=True)


def openssl_source(bundle: Path, relative: Path) -> Path:
    source = bundle / relative
    if source.exists() or relative not in OPENSSL_ALIASES:
        return source
    fallback = source.with_name(OPENSSL_ALIASES[relative])
    if fallback.is_file() and is_macho(fallback):
        print(f"Using {fallback.relative_to(bundle)} for missing {relative}")
        return fallback
    return source


def verify_openssl_abi(source: Path, expected: str) -> None:
    output = subprocess.check_output(["otool", "-D", str(source)], text=True)
    names = {Path(line.strip()).name for line in output.splitlines()
             if line.strip() and not line.endswith(":")}
    if names != {expected}:
        raise ValueError(f"Expected OpenSSL 3 install name {expected}, found {names}: {source}")


def repair_openssl_references(binary: Path, output: Path) -> bool:
    dependencies = subprocess.check_output(["otool", "-L", str(binary)], text=True)
    replacements = {}
    for line in dependencies.splitlines():
        if not line.startswith(("\t", " ")) or " (compatibility version" not in line:
            continue
        dependency = line.strip().split(" (compatibility version", 1)[0]
        path = Path(dependency)
        # The unversioned Homebrew copies must stay separate from Python's
        # versioned OpenSSL: cryptography can require different build options.
        if not path.is_absolute() or not any(
            marker in dependency for marker in ("/opt/openssl@3/", "/Cellar/openssl@3/")
        ):
            continue
        for relative, versioned in OPENSSL_ALIASES.items():
            if path.name != versioned:
                continue
            target = output / relative
            if target == binary:
                continue  # otool -L includes a dylib's own install name.
            if not target.is_file():
                raise ValueError(f"Missing bundled OpenSSL library for {dependency}: {binary}")
            replacements[dependency] = "@loader_path/" + os.path.relpath(target, binary.parent)
    if not replacements:
        return False
    command = ["install_name_tool"]
    for original, replacement in replacements.items():
        command.extend(["-change", original, replacement])
    subprocess.run([*command, str(binary)], check=True)
    # --deep does not reliably visit native extensions under Contents/MacOS.
    subprocess.run(["codesign", "--force", "--sign", "-", str(binary)], check=True)
    print(f"Repaired OpenSSL references: {binary.relative_to(output)}")
    return True


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
                print(f"Fusing: {relative}")
                # Separate slices avoid duplicate architectures and in-place lipo input/output.
                subprocess.run(["lipo", "-create", *slices, "-output", str(destination)], check=True)
            elif relative in INTEL_ONLY_ACCELERATORS and not (arm / relative).exists():
                print(f"Keeping Intel-only accelerator: {relative}")
                required_architectures = ("x86_64",)
            subprocess.run(["lipo", str(destination), "-verify_arch", *required_architectures], check=True)

    for binary in sorted(output.rglob("*")):
        if not binary.is_symlink() and binary.is_file() and is_macho(binary):
            repair_openssl_references(binary, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("intel", type=Path)
    parser.add_argument("arm", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    merge_bundles(args.intel, args.arm, args.output)
