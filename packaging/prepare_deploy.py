"""Limit Nuitka's broad QML inclusion to the application's Qt import graph across all desktop platforms."""
from __future__ import annotations

import argparse
import configparser
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONTROL_STYLES = ("Basic", "Fusion", "Material", "Universal", "Windows", "macOS")


def find_qmlimportscanner(pyside: Path) -> Path:
    candidates = [
        pyside / "qmlimportscanner.exe",
        pyside / "qmlimportscanner",
        pyside / "Qt/libexec/qmlimportscanner",
        pyside / "Qt/libexec/qmlimportscanner.exe",
        pyside / "Qt/bin/qmlimportscanner",
        pyside / "Qt/bin/qmlimportscanner.exe",
    ]
    for c in candidates:
        if c.is_file() and (sys.platform == "win32" or os.access(c, os.X_OK)):
            return c
    # Fallback to PATH
    import shutil
    if which_scanner := shutil.which("qmlimportscanner"):
        return Path(which_scanner)
    raise FileNotFoundError(f"Could not find qmlimportscanner in {pyside} or PATH")


def find_qml_root(pyside: Path) -> Path:
    for candidate in (pyside / "qml", pyside / "Qt/qml"):
        if candidate.is_dir():
            return candidate
    raise FileNotFoundError(f"Could not find QML imports in {pyside / 'qml'} or {pyside / 'Qt/qml'}")


def required_qml_modules(project: Path, pyside: Path) -> set[Path]:
    qml_root = find_qml_root(pyside)
    qml_files = sorted((project / "src/frontend/UI").glob("*.qml"))
    if not qml_files:
        raise ValueError("No application QML files found")
    scanner = find_qmlimportscanner(pyside)
    with tempfile.TemporaryDirectory(prefix="pornfetch-qml-imports-") as temporary:
        # Styles are chosen at runtime, so add their imports to the static scan.
        styles = Path(temporary) / "Styles.qml"
        styles.write_text("\n".join(
            f"import QtQuick.Controls.{style}"
            for style in CONTROL_STYLES
            if (qml_root / "QtQuick/Controls" / style / "qmldir").is_file()
        ) + "\nimport QtQuick\nItem {}\n", encoding="utf-8")
        output = subprocess.check_output([
            str(scanner),
            "-importPath", str(qml_root), "-qmlFiles",
            *map(str, qml_files), str(styles),
        ], text=True)
    required = {
        Path(item["path"]).resolve().relative_to(qml_root.resolve())
        for item in json.loads(output)
        if item.get("type") == "module" and item.get("path")
        and Path(item["path"]).resolve().is_relative_to(qml_root.resolve())
    }
    if not {Path("QtQuick"), Path("QtQml"), Path("QtQuick/Controls")} <= required:
        raise ValueError("QML import scan did not resolve the application's core modules")
    return required


def excluded_qml_modules(qml_root: Path, required: set[Path]) -> list[Path]:
    modules = {path.parent.relative_to(qml_root) for path in qml_root.rglob("qmldir")}
    excluded = sorted(module for module in modules - required
                      if not any(keep.is_relative_to(module) for keep in required))
    # An excluded parent already covers its entire subtree.
    return [module for module in excluded
            if not any(parent in excluded for parent in module.parents)]


def prepare_spec(template: Path, output: Path, project: Path, pyside: Path) -> None:
    required = required_qml_modules(project, pyside)
    excluded = excluded_qml_modules(find_qml_root(pyside), required)
    config = configparser.ConfigParser()
    config.read(template, encoding="utf-8")
    arguments = shlex.split(config.get("nuitka", "extra_args"))
    for module in excluded:
        relative = module.as_posix()
        arguments.extend([
            f"--noinclude-dlls=*/qml/{relative}/*",
            f"--noinclude-data-files=PySide6/qml/{relative}/**",
        ])
    config.set("nuitka", "extra_args", shlex.join(arguments))
    config.set("app", "input_file", str(project / "main.py"))
    config.set("app", "project_dir", str(project))
    config.set("qt", "qml_files", ",".join(
        path.relative_to(project).as_posix()
        for path in sorted((project / "src/frontend/UI").glob("*.qml"))
    ))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as stream:
        config.write(stream)
    print(f"QML packaging: keeping {len(required)} modules; excluding {len(excluded)} unused module trees.")


def main() -> None:
    import PySide6

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=PROJECT_ROOT / "packaging/pysidedeploy_linux.spec")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    prepare_spec(args.template, args.output, PROJECT_ROOT, Path(PySide6.__file__).resolve().parent)


if __name__ == "__main__":
    main()
