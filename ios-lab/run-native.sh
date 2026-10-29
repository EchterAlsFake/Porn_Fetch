#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$LAB_DIR/env.sh"
if [ "$(id -u)" = 0 ]; then
    echo 'Run this from Terminal as your normal macOS user, without sudo.' >&2
    exit 1
fi
"$LAB_DIR/build-native.sh" simulator
# Choose the simulator explicitly if several are installed.
SIM_ID=${1:-}
if [ -z "$SIM_ID" ]; then
    xcrun simctl list devices available
    echo 'Usage: ./run-native.sh SIMULATOR-UUID (copy a UUID from the list above)'
    exit 0
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
xcrun simctl install "$SIM_ID" "$LAB_DIR/build/simulator/HelloNative.app"
xcrun simctl launch "$SIM_ID" local.asuna.HelloNative
xcrun simctl io "$SIM_ID" screenshot "$LAB_DIR/build/native-screenshot.png"
