#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$(id -u)" = 0 ]; then
    exec sudo -H -u asuna "$LAB_DIR/run-qt.sh" "$@"
fi
. "$LAB_DIR/env.sh"
SIM_ID=${1:-7DFE048D-AB3D-453F-AE58-D474EF4C4569}
APP="$LAB_DIR/build/qt-derived/Build/Products/Debug-iphonesimulator/HelloPySide.app"
if [ ! -d "$APP" ]; then
    echo 'Build HelloPySide.xcodeproj for the simulator first.' >&2
    exit 1
fi
STATE=$(xcrun simctl list devices -j | /usr/local/bin/python3 -c '
import json, sys
devices = json.load(sys.stdin)["devices"]
matches = [d for group in devices.values() for d in group if d["udid"] == sys.argv[1]]
if not matches:
    sys.exit("Simulator UUID not found")
print(matches[0]["state"])
' "$SIM_ID")
if [ "$STATE" != Booted ]; then xcrun simctl boot "$SIM_ID"; fi
open "$DEVELOPER_DIR/Applications/Simulator.app"
xcrun simctl bootstatus "$SIM_ID" -b
xcrun simctl install "$SIM_ID" "$APP"
SIMCTL_CHILD_QT_QUICK_BACKEND=rhi SIMCTL_CHILD_QSG_RHI_BACKEND=opengl \
SIMCTL_CHILD_QSG_RENDER_LOOP=basic xcrun simctl launch --terminate-running-process \
    --stdout="$LAB_DIR/build/qt-runtime.log" --stderr="$LAB_DIR/build/qt-runtime.err" \
    "$SIM_ID" com.example.HelloPySide
