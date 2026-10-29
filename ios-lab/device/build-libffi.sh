#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
NATIVE="$DEVICE_DIR/native"
SDK="$DEVELOPER_DIR/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
TOOLBIN="$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin"
mkdir -p "$NATIVE/libffi-build"
cd "$NATIVE/libffi-build"
CC="$TOOLBIN/clang" CFLAGS="-target arm64-apple-ios15.0 -isysroot $SDK -O2 -fPIC" \
    LDFLAGS="-target arm64-apple-ios15.0 -isysroot $SDK" \
    "$DEVICE_DIR/../pornfetch/native/libffi-3.8.0/configure" --host=aarch64-apple-darwin \
    --prefix="$NATIVE/libffi-ios" --disable-shared --enable-static \
    --disable-multi-os-directory --disable-docs
make -j2
make install
