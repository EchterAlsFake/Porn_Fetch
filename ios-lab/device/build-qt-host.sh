#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
cmake -S "$DEVICE_DIR/qt-src/qtbase" -B "$DEVICE_DIR/qt-host-build" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$DEVICE_DIR/qt-host" \
    -DCMAKE_OSX_ARCHITECTURES=x86_64 -DCMAKE_OSX_SYSROOT=macosx \
    -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF -DFEATURE_widgets=OFF \
    -DFEATURE_printsupport=OFF -DFEATURE_sql=OFF -DFEATURE_testlib=OFF -DFEATURE_dbus=OFF
cmake --build "$DEVICE_DIR/qt-host-build" --parallel 6
cmake --install "$DEVICE_DIR/qt-host-build"
