#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
. "$LAB_DIR/env.sh"
NATIVE="$LAB_DIR/pornfetch/native"
mkdir -p "$NATIVE/openssl-build"
cd "$NATIVE/openssl-build"
perl ../openssl-3.5.9/Configure iossimulator-x86_64-xcrun \
    no-shared no-tests --prefix="$NATIVE/openssl-ios" \
    -mios-simulator-version-min=18.0
make -j6 build_libs
make install_sw
