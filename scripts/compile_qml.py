#!/usr/bin/env python3
"""Ahead-of-time bytecode compilation of QML files using pyside6-qmlcachegen."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import build_output  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UI_DIR = PROJECT_ROOT / "src" / "frontend" / "UI"


def find_qmlcachegen() -> Path:
    """Find the pyside6-qmlcachegen executable."""
    # Prefer the tool matching the active Python/PySide environment. A generic
    # qmlcachegen on PATH can belong to a different Qt version (including Qt 5).
    venv_dir = Path(sys.prefix)
    candidates = [
        venv_dir / "bin" / "pyside6-qmlcachegen",
        venv_dir / "Scripts" / "pyside6-qmlcachegen.exe",
        venv_dir / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages" / "PySide6" / "Qt" / "libexec" / "qmlcachegen",
        venv_dir / "Lib" / "site-packages" / "PySide6" / "Qt" / "bin" / "qmlcachegen.exe",
    ]
    for cand in candidates:
        if cand.is_file():
            return cand

    # Direct PySide6 inspection
    try:
        import PySide6
        pyside_dir = Path(PySide6.__file__).resolve().parent
        for cand in (
            pyside_dir / "Qt" / "libexec" / "qmlcachegen",
            pyside_dir / "Qt" / "bin" / "qmlcachegen.exe",
        ):
            if cand.is_file():
                return cand
    except ImportError:
        pass

    for name in ("pyside6-qmlcachegen", "qmlcachegen"):
        if found := shutil.which(name):
            return Path(found)

    raise FileNotFoundError("pyside6-qmlcachegen executable could not be found.")


def compile_all_qml() -> int:
    try:
        cachegen = find_qmlcachegen()
    except FileNotFoundError as err:
        build_output.message(f"{err} Skipping QML bytecode compilation.", "warn")
        return 0

    qml_files = sorted(UI_DIR.glob("*.qml"))
    if not qml_files:
        build_output.message("No QML files found to compile.", "warn")
        return 0

    build_output.message(f"Compile {len(qml_files)} QML files")
    failures = 0
    for qml in qml_files:
        cache_path = qml.with_suffix(".qmlc")
        cmd = [str(cachegen), "-I", str(UI_DIR), str(qml), "-o", str(cache_path)]
        try:
            build_output.run(cmd, label=f"Compile QML {qml.name}")
        except subprocess.CalledProcessError:
            failures += 1

    if failures == 0:
        build_output.message(f"Compiled {len(qml_files)} QML files.", "ok")
    else:
        build_output.message(f"{failures}/{len(qml_files)} QML files failed to compile.", "warn")

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    build_output.add_arguments(parser)
    args = parser.parse_args()
    build_output.configure(args)
    raise SystemExit(compile_all_qml())
