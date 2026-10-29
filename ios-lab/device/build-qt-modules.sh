#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
for module in qtshadertools qtsvg qtdeclarative qt5compat; do
    build_dir="$DEVICE_DIR/$module-device-build"
    cmake -S "$DEVICE_DIR/qt-src/$module" -B "$build_dir" -G Ninja \
        -DCMAKE_TOOLCHAIN_FILE="$DEVICE_DIR/qt-ios15/lib/cmake/Qt6/qt.toolchain.cmake" \
        -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$DEVICE_DIR/qt-ios15" \
        -DQT_HOST_PATH="$DEVICE_DIR/qt-host" -DCMAKE_OSX_ARCHITECTURES=arm64 \
        -DCMAKE_OSX_SYSROOT=iphoneos -DCMAKE_OSX_DEPLOYMENT_TARGET=15.0 \
        -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF \
        -DCMAKE_C_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new' \
        -DCMAKE_CXX_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new' \
        -DCMAKE_OBJC_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new' \
        -DCMAKE_OBJCXX_FLAGS='-Werror=unguarded-availability -Werror=unguarded-availability-new'
    cmake --build "$build_dir" --parallel 6
    cmake --install "$build_dir"
done
