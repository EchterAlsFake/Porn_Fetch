"""Repair native dependencies left unresolved in a Nuitka macOS bundle."""
from __future__ import annotations

import argparse
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_output  # noqa: E402
from scripts.macos_bundle import (  # noqa: E402
    OPENSSL_ALIASES,
    dependencies,
    install_names,
    is_macho,
    relocate_resources,
    repair_openssl_references,
    verify_bundle_dependencies,
)

QT_FRAMEWORK = re.compile(r"(?:^|/)(Qt[^/]+)\.framework/(?:Versions/[^/]+/)?\1$")


def pyside_qt_lib_dir() -> Path:
    import PySide6

    return Path(PySide6.__file__).resolve().parent / "Qt" / "lib"


def repair_bundle(bundle: Path, qt_lib_dir: Path | None = None) -> int:
    bundle = bundle.resolve()
    contents = bundle / "Contents"
    if not (contents / "MacOS").is_dir():
        raise ValueError(f"Not a macOS application bundle: {bundle}")

    binaries = [path for path in sorted(contents.rglob("*")) if is_macho(path)]
    qt_libraries: dict[str, list[Path]] = {}
    for binary in binaries:
        if binary.name.startswith("Qt"):
            qt_libraries.setdefault(binary.name, []).append(binary)

    # Read the whole dependency graph before modifying the signed bundle.
    # Missing frameworks must come from the PySide6 environment used to build it.
    pending = [(binary, binary) for binary in binaries]
    frameworks_to_copy: dict[Path, Path] = {}
    libraries_to_copy: dict[Path, Path] = {}
    copied_binaries: list[Path] = []
    changes: dict[Path, list[tuple[str, str]]] = {}
    for source_binary, binary in pending:
        linked = dependencies(source_binary)
        absolute = [name for name in linked if Path(name).is_absolute()
                    and not name.startswith(("/System/Library/", "/usr/lib/"))]
        own_names = install_names(source_binary) if absolute else set()
        for dependency in linked:
            if dependency in own_names or dependency.startswith(("/System/Library/", "/usr/lib/")):
                continue
            match = QT_FRAMEWORK.search(dependency)
            if not match:
                if dependency not in absolute:
                    continue
                source = Path(dependency)
                if source.name in OPENSSL_ALIASES.values() and any(
                    marker in dependency for marker in ("/opt/openssl@3/", "/Cellar/openssl@3/")
                ):
                    continue  # Relink Homebrew OpenSSL separately from Python's copy below.
                target = contents / "MacOS" / source.name
                if not target.is_file():
                    target = contents / "Frameworks" / source.name
                if not target.is_file() and target not in libraries_to_copy:
                    if not is_macho(source):
                        raise ValueError(f"Missing source library {dependency}; required by {binary.relative_to(bundle)}")
                    libraries_to_copy[target] = source
                    pending.append((source, target))
                    copied_binaries.append(target)
                changes.setdefault(binary, []).append((
                    dependency, "@loader_path/" + os.path.relpath(target, binary.parent),
                ))
                continue
            candidates = qt_libraries.get(match[1], [])
            if not candidates:
                if qt_lib_dir is None:
                    qt_lib_dir = pyside_qt_lib_dir()
                source_framework = qt_lib_dir / f"{match[1]}.framework"
                target_framework = contents / "Frameworks" / source_framework.name
                if not source_framework.is_dir():
                    raise ValueError(
                        f"Missing bundled {match[1]} binary and source framework {source_framework}; "
                        f"required by {binary.relative_to(bundle)}. "
                        "Run repair in the PySide6 environment used for this build, or pass --qt-lib-dir."
                    )
                if target_framework.exists():
                    raise ValueError(f"Incomplete framework already exists: {target_framework}")
                for source in sorted(source_framework.rglob("*")):
                    if is_macho(source):
                        target = target_framework / source.relative_to(source_framework)
                        pending.append((source, target))
                        copied_binaries.append(target)
                        qt_libraries.setdefault(source.name, []).append(target)
                frameworks_to_copy[target_framework] = source_framework
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

    relocated = relocate_resources(bundle)
    for target, source in frameworks_to_copy.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, symlinks=True)
        build_output.detail(f"Bundled missing Qt framework: {target.relative_to(bundle)}")
    for target, source in libraries_to_copy.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        build_output.detail(f"Bundled missing native library: {target.relative_to(bundle)}")

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
        build_output.detail(f"Repaired native dependencies: {binary.relative_to(bundle)}")

    openssl_changes = {
        binary for binary in [*binaries, *copied_binaries]
        if repair_openssl_references(binary, bundle)
    }
    verify_bundle_dependencies(bundle)

    if changes or frameworks_to_copy or relocated or openssl_changes:
        # Mach-O edits invalidate the build's signature, including nested code.
        # Nuitka places some libraries under Contents/MacOS, outside the usual
        # framework/plugin directories traversed by codesign --deep.
        for binary in sorted(set(changes) | set(copied_binaries)):
            subprocess.run(["codesign", "--force", "--sign", "-", str(binary)], check=True)
        for framework in frameworks_to_copy:
            subprocess.run(["codesign", "--force", "--sign", "-", str(framework)], check=True)
        subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(bundle)], check=True)
    return len(set(changes) | openssl_changes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument(
        "--qt-lib-dir", type=Path,
        help="Qt/lib directory from the PySide6 environment used for this build (default: current PySide6)",
    )
    build_output.add_arguments(parser)
    args = parser.parse_args()
    build_output.configure(args)
    if sys.platform != "darwin":
        parser.error("Bundle repair requires macOS (otool, install_name_tool and codesign).")
    try:
        count = repair_bundle(args.bundle, args.qt_lib_dir)
    except (ImportError, OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Bundle repair failed: {error}\n")
    build_output.message(f"Native bundle repaired and dependencies verified: {count} binaries updated.", "ok")


if __name__ == "__main__":
    main()
