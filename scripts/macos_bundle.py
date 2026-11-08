"""Keep macOS bundles self-contained and runtime data outside code locations."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from scripts import build_output

MACHO_MAGIC = {
    bytes.fromhex(value)
    for value in ("feedface", "cefaedfe", "feedfacf", "cffaedfe", "cafebabe", "bebafeca", "cafebabf", "bfbafeca")
}
BUNDLE_SUFFIXES = {".app", ".framework", ".xpc", ".appex", ".bundle"}
OPENSSL_ALIASES = {
    Path("Contents/MacOS/libcrypto.dylib"): "libcrypto.3.dylib",
    Path("Contents/MacOS/libssl.dylib"): "libssl.3.dylib",
}


def is_macho(path: Path) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    with path.open("rb") as source:
        return source.read(4) in MACHO_MAGIC


def dependencies(path: Path) -> list[str]:
    output = subprocess.check_output(["otool", "-L", str(path)], text=True)
    # Universal binaries list dependencies for each slice; change each name once.
    return list(dict.fromkeys(
        line.strip().split(" (compatibility version", 1)[0]
        for line in output.splitlines()
        if line.startswith(("\t", " ")) and " (compatibility version" in line
    ))


def install_names(path: Path) -> set[str]:
    output = subprocess.check_output(["otool", "-D", str(path)], text=True)
    return {line.strip() for line in output.splitlines() if line.strip() and not line.endswith(":")}


def repair_openssl_references(binary: Path, bundle: Path) -> bool:
    replacements = {}
    for dependency in dependencies(binary):
        path = Path(dependency)
        # Keep Homebrew's libraries separate from Python's versioned OpenSSL:
        # cryptography can require different build options.
        if not path.is_absolute() or not any(
            marker in dependency for marker in ("/opt/openssl@3/", "/Cellar/openssl@3/")
        ):
            continue
        for relative, versioned in OPENSSL_ALIASES.items():
            if path.name != versioned:
                continue
            target = bundle / relative
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
    build_output.detail(f"Repaired OpenSSL references: {binary.relative_to(bundle)}")
    return True


def verify_bundle_dependencies(bundle: Path) -> None:
    """Reject build-machine library paths even when those libraries exist locally."""
    for binary in sorted(bundle.rglob("*")):
        if not is_macho(binary):
            continue
        external = {
            dependency for dependency in dependencies(binary)
            if Path(dependency).is_absolute() and not dependency.startswith(("/System/Library/", "/usr/lib/"))
        }
        if not external:
            continue
        # A library's LC_ID_DYLIB is an identity, not a dependency to load.
        for dependency in sorted(external - install_names(binary)):
            raise ValueError(f"External library dependency in {binary.relative_to(bundle)}: {dependency}")


def relocate_resources(bundle: Path) -> int:
    """Move Nuitka data to Resources and retain relative runtime paths via symlinks."""
    macos = bundle / "Contents/MacOS"
    resources = bundle / "Contents/Resources/runtime"
    moved = 0
    for path in sorted(macos.rglob("*")):
        if path.is_symlink() or not path.is_file() or is_macho(path):
            continue
        relative = path.relative_to(macos)
        # Nested bundles already have their own resource/signature layout.
        if "_CodeSignature" in relative.parts or any(parent.suffix in BUNDLE_SUFFIXES for parent in relative.parents):
            continue
        target = resources / relative
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Bundle resource already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        path.rename(target)
        path.symlink_to(os.path.relpath(target, path.parent))
        moved += 1
    return moved
