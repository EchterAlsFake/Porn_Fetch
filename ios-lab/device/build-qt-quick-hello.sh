#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
cmake -S "$DEVICE_DIR/qt-quick-hello" -B "$DEVICE_DIR/qt-quick-hello-build" -G Ninja \
    -DCMAKE_TOOLCHAIN_FILE="$DEVICE_DIR/qt-ios15/lib/cmake/Qt6/qt.toolchain.cmake" \
    -DCMAKE_BUILD_TYPE=Release -DQT_HOST_PATH="$DEVICE_DIR/qt-host" \
    -DCMAKE_OSX_DEPLOYMENT_TARGET=15.0 -DCMAKE_OSX_ARCHITECTURES=arm64 \
    -DCMAKE_OSX_SYSROOT=iphoneos -DCMAKE_XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED=NO
cmake --build "$DEVICE_DIR/qt-quick-hello-build" --parallel 4
APP="$DEVICE_DIR/qt-quick-hello-build/QtQuickPhoneHello.app"
/usr/local/bin/python3 "$DEVICE_DIR/finalize-qt-app.py" "$APP"
