#!/usr/bin/env bash
set -euo pipefail
PORT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$(id -u)" = 0 ]; then exec sudo -H -u asuna "$PORT_DIR/run-application.sh" "$@"; fi
LAB_DIR=$(dirname "$PORT_DIR")
. "$LAB_DIR/env.sh"
export PATH="$LAB_DIR/.venv/bin:/usr/local/bin:/usr/bin:/bin"
: "${SIM_ID:?Export SIM_ID from xcrun simctl list devices available}"
mkdir -p "$LAB_DIR/build"
PROJECT="$PORT_DIR/app/deployment/ios_x86_64_simulator/PornFetch.xcodeproj"
STATE=$(xcrun simctl list devices -j | python -c '
import json,sys
devices=json.load(sys.stdin)["devices"]
print(next(d["state"] for group in devices.values() for d in group if d["udid"]==sys.argv[1]))
' "$SIM_ID")
if [ "$STATE" != Booted ]; then xcrun simctl boot "$SIM_ID"; fi
open "$DEVELOPER_DIR/Applications/Simulator.app"
xcrun simctl bootstatus "$SIM_ID" -b
if [ "${1:-}" != --launch-only ]; then
xcodebuild -project "$PROJECT" -scheme PornFetch -configuration Debug \
    -destination "id=$SIM_ID" -derivedDataPath "$LAB_DIR/build/app-derived" \
    -jobs 4 build 2>&1 | tee "$LAB_DIR/build/app-build.log"
xcrun simctl install "$SIM_ID" "$LAB_DIR/build/app-derived/Build/Products/Debug-iphonesimulator/PornFetch.app"
fi
xcrun simctl launch --terminate-running-process \
    --stdout="$LAB_DIR/build/app-runtime.log" --stderr="$LAB_DIR/build/app-runtime.err" \
    "$SIM_ID" to.pornfetch.ioslab
