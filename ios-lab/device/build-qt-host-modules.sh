#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
export PATH="$DEVICE_DIR/../.venv/bin:/usr/local/bin:/usr/bin:/bin"
for module in qtshadertools qtdeclarative; do
    case "$module" in
        qtshadertools) build_dir="$DEVICE_DIR/qt-host-shaders-build" ;;
        qtdeclarative) build_dir="$DEVICE_DIR/qt-host-declarative-build" ;;
    esac
    extra_option=
    if [ "$module" = qtdeclarative ]; then
        extra_option=-DFEATURE_qml_animation=OFF
    fi
    cmake -S "$DEVICE_DIR/qt-src/$module" -B "$build_dir" -G Ninja \
        -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$DEVICE_DIR/qt-host" \
        -DCMAKE_PREFIX_PATH="$DEVICE_DIR/qt-host" -DCMAKE_OSX_ARCHITECTURES=x86_64 \
        -DCMAKE_OSX_SYSROOT=macosx -DQT_BUILD_TESTS=OFF -DQT_BUILD_EXAMPLES=OFF $extra_option
    cmake --build "$build_dir" --parallel 4
    cmake --install "$build_dir"
done
