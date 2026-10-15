#!/usr/bin/env python3
"""Ahead-of-time bytecode compilation of QML files using pyside6-qmlcachegen."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
UI_DIR = PROJECT_ROOT / "src" / "frontend" / "UI"


def find_qmlcachegen() -> Path:
    """Find the pyside6-qmlcachegen executable."""
    # 1. PATH or venv scripts
    for name in ("pyside6-qmlcachegen", "qmlcachegen"):
        if found := shutil.which(name):
            return Path(found)

    # 2. Virtualenv location
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

    # 3. Direct PySide6 inspection
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

    raise FileNotFoundError("pyside6-qmlcachegen executable could not be found.")


def compile_all_qml() -> int:
    try:
        cachegen = find_qmlcachegen()
    except FileNotFoundError as err:
        print(f"Warning: {err} Skipping QML AOT bytecode compilation.", file=sys.stderr)
        return 0

    qml_files = sorted(UI_DIR.glob("*.qml"))
    if not qml_files:
        print("No QML files found to compile.", file=sys.stderr)
        return 0

    print(f"Compiling {len(qml_files)} QML files to .qmlc bytecode using {cachegen.name}...")
    failures = 0
    for qml in qml_files:
        cache_path = qml.with_suffix(".qmlc")
        cmd = [str(cachegen), "-I", str(UI_DIR), str(qml), "-o", str(cache_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"  [FAIL] {qml.name}: {res.stderr.strip()}", file=sys.stderr)
            failures += 1

    if failures == 0:
        print(f"[✓] Successfully compiled all {len(qml_files)} QML files to .qmlc.")
    else:
        print(f"[!] Warning: {failures}/{len(qml_files)} QML files failed to compile.", file=sys.stderr)

    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(compile_all_qml())
