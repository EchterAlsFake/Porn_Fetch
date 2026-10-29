#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
SLICE=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64
SDK="$DEVELOPER_DIR/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
APP_NAME=${APP_NAME:-PythonNative}
APP="$DEVICE_DIR/../build/device/$APP_NAME.app"
mkdir -p "$APP/Frameworks" "$APP/python/lib"
"$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang" \
    -target arm64-apple-ios15.0 -isysroot "$SDK" -fobjc-arc \
    -F "$SLICE" -framework UIKit -framework Foundation -framework Python \
    -Wl,-rpath,@executable_path/Frameworks "$DEVICE_DIR/python-native/main.m" -o "$APP/$APP_NAME"
cp -R "$SLICE/Python.framework" "$APP/Frameworks/"
/usr/local/bin/python3 - "$APP" <<'PY'
from pathlib import Path
import plistlib, shutil, sys
app = Path(sys.argv[1])
base = app.parent / 'HelloNative.app/Info.plist'
info = plistlib.loads(base.read_bytes())
name = app.stem
info.update(CFBundleIdentifier='local.asuna.' + name, CFBundleName=name, CFBundleExecutable=name)
(app / 'Info.plist').write_bytes(plistlib.dumps(info))
source = Path('/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/lib/python3.15')
shutil.copytree(source, app / 'python/lib/python3.15', dirs_exist_ok=True,
    ignore=shutil.ignore_patterns('__pycache__', 'test', 'tests', 'idlelib', 'tkinter', 'ensurepip', 'turtledemo'))
PY
"$DEVICE_DIR/tools/ldid" -S "$APP/Frameworks/Python.framework/Python"
"$DEVICE_DIR/tools/ldid" -S "$APP/$APP_NAME"
tar -cf "$DEVICE_DIR/artifacts/$APP_NAME.tar" -C "$(dirname "$APP")" "$APP_NAME.app"
echo "Built $APP"
