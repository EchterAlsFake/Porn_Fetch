# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

project_root = os.path.abspath(os.path.join(SPECPATH, ".."))
tor_root = Path(project_root) / "src/shared/tor"
tor_binaries = [(str(path), "src/shared/tor") for path in tor_root.iterdir() if path.is_file() and path.name != "provenance.json"] if tor_root.is_dir() else []
tor_data = [(str(tor_root / "notices"), "src/shared/tor/notices"),
            (str(tor_root / "provenance.json"), "src/shared/tor")] if tor_root.is_dir() else []

providers = [
    "pornhub_api", "eporner_api", "xnxx_api", "xvideos_api", "xhamster_api",
    "spankbang_api", "youporn_api", "beeg_api", "porntrex_api", "xfreehd_api",
    "redtube_api", "thumbzilla_api", "tube8_api",
]
questionary_datas, questionary_binaries, questionary_hidden = collect_all("questionary")
rich_datas, rich_binaries, rich_hidden = collect_all("rich")
hiddenimports = (
    questionary_hidden
    + rich_hidden
    + collect_submodules("src.cli")
    + collect_submodules("src.licensing")
    + collect_submodules("src.database")
    + collect_submodules("src.shared")
    + providers
)

analysis = Analysis(
    [os.path.join(project_root, "Porn_Fetch_CLI.py")],
    pathex=[project_root],
    binaries=questionary_binaries + rich_binaries + tor_binaries,
    datas=questionary_datas + rich_datas + tor_data + collect_data_files("certifi") + [
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
