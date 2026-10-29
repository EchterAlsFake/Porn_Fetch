#!/bin/bash
set -eu
DEVICE_DIR=$(cd -- "$(dirname -- "$0")" && pwd)
APP_NAME=NativeModules /bin/sh "$DEVICE_DIR/build-python-native.sh"
APP="$DEVICE_DIR/../build/device/NativeModules.app"
/usr/local/bin/python3 - "$DEVICE_DIR" "$APP" <<'PY'
from pathlib import Path
import shutil, sys
device, app = map(Path, sys.argv[1:])
packages = app / 'packages'
packages.mkdir(exist_ok=True)
vendor = device.parent / 'pornfetch/vendor'
for name in ['cffi', 'pycparser', 'chompjs', 'selectolax', 'curl_cffi', 'curl_cffi-0.17.0.dist-info', 'certifi']:
    shutil.copytree(vendor / name, packages / name, dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('*.so', '*.fwork', '__pycache__'))
if (device / 'native/packages/cryptography/hazmat/bindings/_rust.abi3.so').exists():
    for name in ['cryptography', 'cryptography-50.0.2.dist-info']:
        shutil.copytree(vendor / name, packages / name, dirs_exist_ok=True,
            ignore=shutil.ignore_patterns('*.so', '*.fwork', '__pycache__'))
shutil.copytree(device / 'native/packages', packages, dirs_exist_ok=True)
shutil.copy2(device / 'python-native/probe.py', app / 'probe.py')
slice = Path('/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64')
shutil.copytree(slice / 'lib-arm64/python3.15', app / 'python/lib/python3.15', dirs_exist_ok=True)
PY
export PROJECT_DIR=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework
export CODESIGNING_FOLDER_PATH="$APP"
export PLATFORM_FAMILY_NAME=iOS PRODUCT_BUNDLE_IDENTIFIER=local.asuna.NativeModules
export EXPANDED_CODE_SIGN_IDENTITY=- EXPANDED_CODE_SIGN_IDENTITY_NAME=ad-hoc
source "$PROJECT_DIR/build/utils.sh"
process_dylibs . python/lib/python3.15/lib-dynload
process_dylibs . packages
/usr/local/bin/python3 - "$DEVICE_DIR" "$APP" <<'PY'
from pathlib import Path
import plistlib, subprocess, sys
device, app = map(Path, sys.argv[1:])
for framework in (app / 'Frameworks').glob('*.framework'):
    info = plistlib.loads((framework / 'Info.plist').read_bytes())
    subprocess.run([str(device / 'tools/ldid'), '-S', str(framework / info['CFBundleExecutable'])], check=True)
PY
tar -cf "$DEVICE_DIR/artifacts/NativeModules.tar" -C "$(dirname "$APP")" NativeModules.app
