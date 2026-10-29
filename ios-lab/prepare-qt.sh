#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$LAB_DIR/env.sh"
cd "$LAB_DIR"
# Separate from both the app environment and the older desktop PySide environment.
python3 -m venv .venv
.venv/bin/python -m pip install --no-cache-dir 'PySide6-Essentials==6.12.0'
.venv/bin/python -m pip install -r "$LAB_DIR/.venv/lib/python3.13/site-packages/PySide6/scripts/requirements-ios.txt"
mkdir -p wheels
cd wheels
# qtpip 0.2.0 requires commercial credentials here. Use Qt's public release files.
for PACKAGE in pyside6 shiboken6; do
    WHEEL="$PACKAGE-6.12.0-6.12.0-cp315-cp315-ios_x86_64_simulator.whl"
    URL="https://download.qt.io/official_releases/QtForPython/$PACKAGE/$WHEEL"
    if [ ! -f "$WHEEL" ]; then
        curl -fLSs --retry 2 "$URL" -o "$WHEEL.part"
        mv "$WHEEL.part" "$WHEEL"
    fi
    curl -fLSs --retry 2 "$URL.sha256" -o "$WHEEL.sha256"
    shasum -a 256 -c "$WHEEL.sha256"
done
cd "$LAB_DIR"
# Require one pair; don't silently choose between mixed versions or architectures.
.venv/bin/python - <<'PY'
from pathlib import Path
import subprocess

root = Path.cwd()
wheels = list((root / "wheels").rglob("*.whl"))
def choose(package):
    matches = [p for p in wheels if p.name.lower().startswith(package + "-")
               and "ios" in p.name and "x86_64" in p.name]
    if len(matches) != 1:
        raise SystemExit(f"Expected one Intel iOS {package} wheel, found {matches}. "
                         "Review wheels/ and qtpip output before continuing.")
    return matches[0]

pyside = choose("pyside6")
shiboken = choose("shiboken6")
if pyside.name.split("-")[1] != "6.12.0" or shiboken.name.split("-")[1] != "6.12.0":
    raise SystemExit("Downloaded wheels do not match the pinned 6.12.0 host tools. "
                     "Use qtpip --help to select matching wheels before proceeding.")
subprocess.run([
    str(root / ".venv/bin/pyside6-ios-deploy"), str(root / "qt/main.py"),
    "--name", "HelloPySide", "--wheel-pyside", str(pyside),
    "--wheel-shiboken", str(shiboken),
], cwd=root / "qt", check=True)
projects = list((root / "qt/deployment").rglob("HelloPySide.xcodeproj"))
for project in projects:
    print(f"Generated {project}")
    subprocess.run(["open", str(project)], check=True)
PY
