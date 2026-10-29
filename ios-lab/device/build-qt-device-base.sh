#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
cmake -S "$DEVICE_DIR/qt-src/qtbase" -B "$DEVICE_DIR/qt-device-build" -G Ninja \
    -DCMAKE_SYSTEM_NAME=iOS -DCMAKE_SYSTEM_PROCESSOR=arm64 \
    -DCMAKE_OSX_ARCHITECTURES=arm64 -DCMAKE_OSX_SYSROOT=iphoneos \
    -DCMAKE_OSX_DEPLOYMENT_TARGET=15.0 -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX="$DEVICE_DIR/qt-ios15" -DQT_HOST_PATH="$DEVICE_DIR/qt-host" \
    -DBUILD_SHARED_LIBS=OFF -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF \
    -DFEATURE_sql=OFF -DFEATURE_testlib=OFF -DFEATURE_dbus=OFF \
    -DCMAKE_C_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new' \
    -DCMAKE_CXX_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new' \
    -DCMAKE_OBJC_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new' \
    -DCMAKE_OBJCXX_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new'
cmake --build "$DEVICE_DIR/qt-device-build" --parallel 6
cmake --install "$DEVICE_DIR/qt-device-build"
