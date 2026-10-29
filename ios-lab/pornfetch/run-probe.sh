#!/bin/sh
set -eu
PORT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$(id -u)" = 0 ]; then exec sudo -H -u asuna "$PORT_DIR/run-probe.sh" "$@"; fi
LAB_DIR=$(dirname "$PORT_DIR")
. "$LAB_DIR/env.sh"
export PATH="$LAB_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin"
SIM_ID=7DFE048D-AB3D-453F-AE58-D474EF4C4569
PROJECT="$PORT_DIR/probe/deployment/ios_x86_64_simulator/NativeProbe.xcodeproj"
if ! xcodebuild -project "$PROJECT" -scheme NativeProbe -configuration Debug \
    -destination "id=$SIM_ID" -derivedDataPath "$LAB_DIR/build/probe-derived" \
    -jobs 4 build > "$LAB_DIR/build/probe-build.log" 2>&1; then
    tail -n 50 "$LAB_DIR/build/probe-build.log"
    exit 1
fi
xcrun simctl install "$SIM_ID" "$LAB_DIR/build/probe-derived/Build/Products/Debug-iphonesimulator/NativeProbe.app"
xcrun simctl launch --terminate-running-process \
    --stdout="$LAB_DIR/build/probe-runtime.log" --stderr="$LAB_DIR/build/probe-runtime.err" \
    "$SIM_ID" local.asuna.NativeProbe
