"""Repair Qt framework references left unresolved in a Nuitka macOS bundle."""
from __future__ import annotations

import argparse
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

MACHO_MAGIC = {
    b"\xfe\xed\xfa\xce", b"\xce\xfa\xed\xfe",
    b"\xfe\xed\xfa\xcf", b"\xcf\xfa\xed\xfe",
    b"\xca\xfe\xba\xbe", b"\xbe\xba\xfe\xca",
    b"\xca\xfe\xba\xbf", b"\xbf\xba\xfe\xca",
}
QT_FRAMEWORK = re.compile(r"(?:^|/)(Qt[^/]+)\.framework/(?:Versions/[^/]+/)?\1$")


def is_macho(path: Path) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    with path.open("rb") as binary:
        return binary.read(4) in MACHO_MAGIC


def dependencies(path: Path) -> list[str]:
    output = subprocess.check_output(["otool", "-L", str(path)], text=True)
    # Universal binaries list dependencies for each slice; change each name once.
    return list(dict.fromkeys(
        line.strip().split(" (compatibility version", 1)[0]
        for line in output.splitlines()
        if line.startswith(("\t", " ")) and " (compatibility version" in line
    ))


def repair_bundle(bundle: Path) -> int:
    bundle = bundle.resolve()
    contents = bundle / "Contents"
    if not (contents / "MacOS").is_dir():
        raise ValueError(f"Not a macOS application bundle: {bundle}")

    binaries = [path for path in sorted(contents.rglob("*")) if is_macho(path)]
    qt_libraries: dict[str, list[Path]] = {}
    for binary in binaries:
        if binary.name.startswith("Qt"):
            qt_libraries.setdefault(binary.name, []).append(binary)

    # Plan every change before modifying the signed bundle. Do not borrow Qt
    # from a system installation or a different PySide6 build.
    changes: dict[Path, list[tuple[str, str]]] = {}
    for binary in binaries:
        for dependency in dependencies(binary):
            match = QT_FRAMEWORK.search(dependency)
            if not match or dependency.startswith(("/System/Library/", "/usr/lib/")):
                continue
            candidates = qt_libraries.get(match[1], [])
            if len(candidates) != 1:
                raise ValueError(
                    f"Expected one bundled {match[1]} binary, found {len(candidates)}; "
                    f"required by {binary.relative_to(bundle)}. Rebuild with matching PySide6 libraries."
                )
            target = candidates[0]
            if target == binary:
                continue  # otool also lists a framework's own install name.
            replacement = "@loader_path/" + os.path.relpath(target, binary.parent)
            if dependency != replacement:
                changes.setdefault(binary, []).append((dependency, replacement))

    for binary, replacements in changes.items():
        command = ["install_name_tool"]
        for original, replacement in replacements:
            command.extend(["-change", original, replacement])
        command.append(str(binary))
        mode = stat.S_IMODE(binary.stat().st_mode)
        binary.chmod(mode | stat.S_IWUSR)
        try:
            subprocess.run(command, check=True)
        finally:
            binary.chmod(mode)
        print(f"Repaired Qt dependencies: {binary.relative_to(bundle)}")

    if changes:
        # Mach-O edits invalidate the build's signature, including nested code.
        # Nuitka places some libraries under Contents/MacOS, outside the usual
        # framework/plugin directories traversed by codesign --deep.
        for binary in changes:
            subprocess.run(["codesign", "--force", "--sign", "-", str(binary)], check=True)
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(bundle)], check=True)
    return len(changes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("Bundle repair requires macOS (otool, install_name_tool and codesign).")
    try:
        count = repair_bundle(args.bundle)
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Bundle repair failed: {error}\n")
    print(f"Qt bundle repair complete: {count} binaries updated.")


if __name__ == "__main__":
    main()
