#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
. "$LAB_DIR/env.sh"
SDK="$DEVELOPER_DIR/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk"
PYFRAMEWORK=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64_x86_64-simulator/Python.framework
CLANG="$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
NATIVE="$LAB_DIR/pornfetch/native"
OUT="$NATIVE/packages"
mkdir -p "$OUT"
# Compile against the embedded Python headers and the iOS Simulator SDK.
# These are compile/link probes; simulator import/runtime validation still follows.
"$CLANG" -target x86_64-apple-ios18.0-simulator -isysroot "$SDK" \
    -dynamiclib -undefined dynamic_lookup -O2 -I "$PYFRAMEWORK/Headers" \
    "$NATIVE/chompjs-src/chompjs-1.4.1/_chompjs/module.c" \
    "$NATIVE/chompjs-src/chompjs-1.4.1/_chompjs/parser.c" \
    "$NATIVE/chompjs-src/chompjs-1.4.1/_chompjs/buffer.c" \
    -o "$OUT/_chompjs.cpython-315-iphonesimulator.so"
if [ -n "${LIBFFI_IOS_PREFIX:-}" ]; then
"$CLANG" -target x86_64-apple-ios18.0-simulator -isysroot "$SDK" \
    -dynamiclib -undefined dynamic_lookup -O2 -I "$PYFRAMEWORK/Headers" \
    -I "$LIBFFI_IOS_PREFIX/include" -DFFI_BUILDING=1 -DUSE__THREAD -DHAVE_SYNC_SYNCHRONIZE \
    "$NATIVE/cffi-src/cffi-2.1.1/src/c/_cffi_backend.c" "$LIBFFI_IOS_PREFIX/lib/libffi.a" \
    -o "$OUT/_cffi_backend.cpython-315-iphonesimulator.so"
else
    echo 'CFFI deferred: set LIBFFI_IOS_PREFIX to a libffi build for the Intel iOS simulator.'
fi
file "$OUT"/*.so
