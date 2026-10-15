"""Compatibility wrapper for packaging/prepare_deploy.py with macOS default."""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

_deploy_path = Path(__file__).resolve().parent / "prepare_deploy.py"
_spec = importlib.util.spec_from_file_location("_prepare_deploy", _deploy_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load prepare_deploy from {_deploy_path}")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

CONTROL_STYLES = _mod.CONTROL_STYLES
PROJECT_ROOT = _mod.PROJECT_ROOT
excluded_qml_modules = _mod.excluded_qml_modules
find_qmlimportscanner = _mod.find_qmlimportscanner
prepare_spec = _mod.prepare_spec
required_qml_modules = _mod.required_qml_modules

__all__ = [
    "CONTROL_STYLES",
    "PROJECT_ROOT",
    "excluded_qml_modules",
    "find_qmlimportscanner",
    "main",
    "prepare_spec",
    "required_qml_modules",
]


def main() -> None:
    import PySide6

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, default=PROJECT_ROOT / "packaging/pysidedeploy_macos.spec")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    prepare_spec(args.template, args.output, PROJECT_ROOT, Path(PySide6.__file__).resolve().parent)


if __name__ == "__main__":
    main()
