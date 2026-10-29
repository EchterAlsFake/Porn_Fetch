#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$LAB_DIR/env.sh"
if [ "$(id -u)" = 0 ]; then
    echo 'Run from your normal Terminal user, without sudo around the script.' >&2
    exit 1
fi
df -h /
echo 'Downloading/installing an iOS runtime needs substantial free disk space.'
echo 'The universal variant includes the Intel simulator needed by this VM.'
sudo /usr/bin/env DEVELOPER_DIR="$DEVELOPER_DIR" /usr/bin/xcodebuild -runFirstLaunch
xcodebuild -downloadPlatform iOS -architectureVariant universal
xcrun simctl list runtimes
xcrun simctl list devices available
echo 'If there are no devices, open Simulator and use File > New Simulator.'
echo 'Then run ./run-native.sh and copy a simulator UUID from the displayed list.'
