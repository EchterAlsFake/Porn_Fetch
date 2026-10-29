#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
. "$LAB_DIR/env.sh"
NATIVE="$LAB_DIR/pornfetch/native"
export CARGO_HOME="$LAB_DIR/toolchains/cargo"
export RUSTUP_HOME="$LAB_DIR/toolchains/rustup"
export PATH="$CARGO_HOME/bin:$LAB_DIR/.venv/bin:$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin:/usr/local/bin:/usr/bin:/bin"
PYFRAMEWORK=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64_x86_64-simulator
mkdir -p "$NATIVE/python-target/include" "$NATIVE/python-target/lib"
if [ ! -e "$NATIVE/python-target/include/python3.15" ]; then
    ln -s "$PYFRAMEWORK/Python.framework/Headers" "$NATIVE/python-target/include/python3.15"
fi
if [ -L "$NATIVE/python-target/lib/python3.15" ]; then
    unlink "$NATIVE/python-target/lib/python3.15"
fi
mkdir -p "$NATIVE/python-target/lib/python3.15"
cp "$PYFRAMEWORK/lib-x86_64/python3.15/"_sysconfigdata*.py "$NATIVE/python-target/lib/python3.15/"
if [ ! -e "$NATIVE/python-target/lib/python3.15/libpython3.15.dylib" ]; then
    ln -s "$PYFRAMEWORK/Python.framework/Python" "$NATIVE/python-target/lib/python3.15/libpython3.15.dylib"
fi
export PYO3_CROSS=1
export PYO3_CROSS_PYTHON_VERSION=3.15
export PYO3_CROSS_LIB_DIR="$NATIVE/python-target/lib/python3.15"
export PYO3_PYTHON="$LAB_DIR/.venv/bin/python"
export OPENSSL_DIR="$NATIVE/openssl-ios"
export OPENSSL_STATIC=1
export IPHONEOS_DEPLOYMENT_TARGET=18.0
export SDKROOT="$DEVELOPER_DIR/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk"
export CC_x86_64_apple_ios="$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
export CFLAGS_x86_64_apple_ios="-target x86_64-apple-ios18.0-simulator -isysroot $SDKROOT"
export CARGO_TARGET_X86_64_APPLE_IOS_LINKER="$CC_x86_64_apple_ios"
export RUSTFLAGS="-C link-arg=-undefined -C link-arg=dynamic_lookup"
cd "$NATIVE/cryptography-src/cryptography-50.0.2"
cargo build --locked --release --target x86_64-apple-ios \
    --manifest-path src/rust/Cargo.toml --features pyo3/extension-module -j4
mkdir -p "$NATIVE/packages/cryptography/hazmat/bindings"
cp target/x86_64-apple-ios/release/libcryptography_rust.dylib \
    "$NATIVE/packages/cryptography/hazmat/bindings/_rust.abi3.so"
