#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/build-venv/bin:$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
cd "$DEVICE_DIR/qt-src/pyside-setup"
"$DEVICE_DIR/build-venv/bin/python" setup.py bdist_wheel \
    --standalone --no-qt-tools --disable-pyi --skip-mypy-test --disable-numpy-support \
    --module-subset="${PYSIDE_MODULES:-Core,Gui,Network,OpenGL,Svg,Qml,Quick,QuickControls2}" \
    --shiboken-host-path="$DEVICE_DIR/../.venv/lib/python3.13/site-packages/shiboken6_generator" \
    --qt-host-path="$DEVICE_DIR/qt-host" --qt-target-path="$DEVICE_DIR/qt-ios15" \
    --python-target-path=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64 \
    --cmake-toolchain-file="$DEVICE_DIR/pyside-ios15-toolchain.cmake" \
    --plat-name=ios_arm64 --dist-dir="$DEVICE_DIR/wheels" --parallel=6 "$@"
