# -*- mode: python ; coding: utf-8 -*-
import os
import json
import runpy
import sys
import sysconfig
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

# Python 3.15 abi3t extensions also need python3t.dll on a GIL-enabled host.
# The legacy Windows installer puts the GIL-compatible forwarder in abi3t-compat;
# the root copy may belong to a separately installed free-threaded interpreter.
# Collect the matching DLL before dependency scanning and payload signing.
python_binaries = []
if sys.platform == "win32" and sys.version_info >= (3, 15):
    runtime_dir = Path(sys.base_prefix)
    compatibility_dir = runtime_dir / "abi3t-compat"
    if not sysconfig.get_config_var("Py_GIL_DISABLED") and compatibility_dir.is_dir():
        runtime_dir = compatibility_dir
    forwarder = runtime_dir / "python3t.dll"
    if not forwarder.is_file():
        raise FileNotFoundError(f"Python's abi3t runtime is missing: {forwarder}")
    python_binaries.append((str(forwarder), "."))

analysis = Analysis(
    [os.path.join(project_root, "Porn_Fetch_CLI.py")],
    pathex=[project_root],
    binaries=tor_binaries + python_binaries,
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
# Copy and sign every native dependency (including Tor) before onefile packing.
# Never modify installed wheels or the PyInstaller cache in place.
if sys.platform == "win32" and os.environ.get("PORN_FETCH_WINDOWS_SIGNING") == "1":
    sign_payload = runpy.run_path(str(Path(project_root) / "packaging/sign_pyinstaller_payload.py"))["sign_payload"]
    binary_count = len(analysis.binaries)
    signed_payload = sign_payload([*analysis.binaries, *analysis.datas], CONF["workpath"])
    analysis.binaries = signed_payload[:binary_count]
    analysis.datas = signed_payload[binary_count:]

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
    # UPX rewrites PE files and would invalidate embedded Authenticode signatures.
    upx=sys.platform != "win32",
    console=True,
)
