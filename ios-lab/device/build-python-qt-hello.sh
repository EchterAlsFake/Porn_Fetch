#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$(id -u)" = 0 ]; then
    exec sudo -H -u asuna /bin/sh "$0" "$@"
fi
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
xcodebuild -project "$DEVICE_DIR/python-qt-hello/deployment/ios_arm64/PythonQtPhoneHello.xcodeproj" \
    -scheme PythonQtPhoneHello -configuration Release -sdk iphoneos \
    -destination 'generic/platform=iOS' -derivedDataPath "$DEVICE_DIR/python-qt-derived" \
    -jobs 4 CODE_SIGNING_ALLOWED=NO CODE_SIGNING_REQUIRED=NO CODE_SIGN_IDENTITY=- \
    EXPANDED_CODE_SIGN_IDENTITY=- build
/usr/local/bin/python3 "$DEVICE_DIR/finalize-qt-app.py" \
    "$DEVICE_DIR/python-qt-derived/Build/Products/Release-iphoneos/PythonQtPhoneHello.app"
