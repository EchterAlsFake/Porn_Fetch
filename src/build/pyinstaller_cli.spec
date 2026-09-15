# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all, collect_submodules

project_root = os.path.abspath(os.path.join(SPECPATH, "..", ".."))

providers = [
    "pornhub_api", "eporner_api", "xnxx_api", "xvideos_api", "xhamster_api",
    "spankbang_api", "youporn_api", "beeg_api", "porntrex_api", "xfreehd_api",
    "redtube_api", "thumbzilla_api", "tube8_api",
]
questionary_datas, questionary_binaries, questionary_hidden = collect_all("questionary")
rich_datas, rich_binaries, rich_hidden = collect_all("rich")
hiddenimports = questionary_hidden + rich_hidden + collect_submodules("src.cli") + collect_submodules("license_client") + providers

analysis = Analysis(
    [os.path.join(project_root, "Porn_Fetch_CLI.py")],
    pathex=[project_root],
    binaries=questionary_binaries + rich_binaries,
    datas=questionary_datas + rich_datas + [
        (os.path.join(project_root, "license_client", "production.json"), "license_client"),
        (os.path.join(project_root, "README", "CREDITS.md"), "README"),
    ],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=["PySide6", "hqporner_api", "colorama", "hue_shift"],
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
