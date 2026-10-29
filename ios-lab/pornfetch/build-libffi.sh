#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
. "$LAB_DIR/env.sh"
NATIVE="$LAB_DIR/pornfetch/native"
SDK="$DEVELOPER_DIR/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk"
TOOLBIN="$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin"
mkdir -p "$NATIVE/libffi-build"
cd "$NATIVE/libffi-build"
CC="$TOOLBIN/clang" CFLAGS="-target x86_64-apple-ios18.0-simulator -isysroot $SDK -O2 -fPIC" \
    LDFLAGS="-target x86_64-apple-ios18.0-simulator -isysroot $SDK" \
    ../libffi-3.8.0/configure --host=x86_64-apple-darwin \
    --prefix="$NATIVE/libffi-ios" --disable-shared --enable-static \
    --disable-multi-os-directory --disable-docs
make -j4
make install
