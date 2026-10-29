#!/bin/sh
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$DEVICE_DIR/../env.sh"
NATIVE="$DEVICE_DIR/native"
SOURCE="$DEVICE_DIR/../pornfetch/native"
export CARGO_HOME="$DEVICE_DIR/../toolchains/cargo"
export RUSTUP_HOME="$DEVICE_DIR/../toolchains/rustup"
export PATH="$CARGO_HOME/bin:$DEVICE_DIR/../.venv/bin:$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin:/usr/local/bin:/usr/bin:/bin"
export SDKROOT="$DEVELOPER_DIR/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS.sdk"
export IPHONEOS_DEPLOYMENT_TARGET=15.0
rustup target add aarch64-apple-ios
if [ ! -f "$NATIVE/openssl-ios/lib/libcrypto.a" ] || [ "${REBUILD_OPENSSL:-0}" = 1 ]; then
    mkdir -p "$NATIVE/openssl-build"
    cd "$NATIVE/openssl-build"
    perl "$SOURCE/openssl-3.5.9/Configure" ios64-xcrun no-shared no-tests \
        --prefix="$NATIVE/openssl-ios" -miphoneos-version-min=15.0
    make -j2 build_libs
    make install_dev
fi
PYTHON_SLICE=/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64
mkdir -p "$NATIVE/python-target/lib/python3.15" "$NATIVE/python-target/include"
ln -sfn "$PYTHON_SLICE/Python.framework/Headers" "$NATIVE/python-target/include/python3.15"
cp "$PYTHON_SLICE/lib-arm64/python3.15/"_sysconfigdata*.py "$NATIVE/python-target/lib/python3.15/"
ln -sf "$PYTHON_SLICE/Python.framework/Python" "$NATIVE/python-target/lib/python3.15/libpython3.15.dylib"
export PYO3_CROSS=1 PYO3_CROSS_PYTHON_VERSION=3.15
export PYO3_CROSS_LIB_DIR="$NATIVE/python-target/lib/python3.15"
export PYO3_PYTHON="$DEVICE_DIR/../.venv/bin/python"
export OPENSSL_DIR="$NATIVE/openssl-ios" OPENSSL_STATIC=1
export CC_aarch64_apple_ios="$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
export CFLAGS_aarch64_apple_ios="-target arm64-apple-ios15.0 -isysroot $SDKROOT"
export CARGO_TARGET_AARCH64_APPLE_IOS_LINKER="$CC_aarch64_apple_ios"
export CARGO_TARGET_DIR="$NATIVE/cryptography-target"
export RUSTFLAGS="-C link-arg=-undefined -C link-arg=dynamic_lookup"
cd "$SOURCE/cryptography-src/cryptography-50.0.2"
cargo build --locked --release --target aarch64-apple-ios \
    --manifest-path src/rust/Cargo.toml --features pyo3/extension-module -j2
mkdir -p "$NATIVE/packages/cryptography/hazmat/bindings"
cp "$CARGO_TARGET_DIR/aarch64-apple-ios/release/libcryptography_rust.dylib" \
    "$NATIVE/packages/cryptography/hazmat/bindings/_rust.abi3.so"
