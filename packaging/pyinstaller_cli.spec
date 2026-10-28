# -*- mode: python ; coding: utf-8 -*-
import os
import json
import runpy
from pathlib import Path
from PyInstaller.config import CONF
from PyInstaller.utils.hooks import collect_data_files

project_root = os.path.abspath(os.path.join(SPECPATH, ".."))
tor_root = Path(project_root) / "src/shared/tor"
tor_binaries = [(str(path), "src/shared/tor") for path in tor_root.iterdir() if path.is_file() and path.name != "provenance.json"] if tor_root.is_dir() else []
tor_data = [(str(tor_root / "notices"), "src/shared/tor/notices"),
            (str(tor_root / "provenance.json"), "src/shared/tor")] if tor_root.is_dir() else []

# Provider clients are loaded by import_module; everything else uses Python imports.
providers = runpy.run_path(str(Path(project_root) / "src/shared/provider_routing.py"))["PROVIDER_MODULES"]
hiddenimports = list(providers.values())

analysis = Analysis(
    [os.path.join(project_root, "Porn_Fetch_CLI.py")],
    pathex=[project_root],
    binaries=tor_binaries,
    datas=tor_data + collect_data_files("certifi") + [
        (os.path.join(project_root, "src", "licensing", "production.json"), "src/licensing"),
        (os.path.join(project_root, "docs", "CREDITS.md"), "docs"),
        (os.path.join(project_root, "LICENSE"), "."),
        (os.path.join(project_root, "THIRD_PARTY_NOTICES.md"), "."),
        (os.path.join(project_root, "LICENSES", "Provider-permission.txt"), "LICENSES"),
        (os.path.join(project_root, "src", "cli", "update_root.json"), "src/cli"),
        (os.path.join(project_root, "src", "cli", "update_build.json"), "src/cli"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["PySide6", "pydivert", "src.database.bridge", "src.backend", "src.frontend"],
    noarchive=False,
)
# Preserve an inventory outside the release payload to explain onefile size.
Path(CONF["workpath"], "payload-inventory.json").write_text(json.dumps({
    kind: [{"name": name, "bytes": Path(source).stat().st_size if Path(source).is_file() else 0}
           for name, source, _ in entries]
    for kind, entries in (("modules", analysis.pure), ("binaries", analysis.binaries), ("data", analysis.datas))
}, indent=2), encoding="utf-8")
archive = PYZ(analysis.pure)
executable = EXE(
    archive,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="Porn_Fetch_CLI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
