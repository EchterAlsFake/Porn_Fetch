#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
. "$LAB_DIR/env.sh"
TARGET=${1:-simulator}
case "$TARGET" in
    simulator) PLATFORM=iPhoneSimulator; TRIPLE=x86_64-apple-ios15.0-simulator; SUPPORTED=iPhoneSimulator ;;
    device) PLATFORM=iPhoneOS; TRIPLE=arm64-apple-ios15.0; SUPPORTED=iPhoneOS ;;
    *) echo 'Usage: build-native.sh [simulator|device]' >&2; exit 1 ;;
esac
SDK="$DEVELOPER_DIR/Platforms/$PLATFORM.platform/Developer/SDKs/$PLATFORM.sdk"
CLANG="$DEVELOPER_DIR/Toolchains/XcodeDefault.xctoolchain/usr/bin/clang"
APP="$LAB_DIR/build/$TARGET/HelloNative.app"
mkdir -p "$APP" "$LAB_DIR/build/module-cache"
"$CLANG" -target "$TRIPLE" -isysroot "$SDK" -fobjc-arc \
    -fmodules-cache-path="$LAB_DIR/build/module-cache" \
    -framework UIKit -framework Foundation "$LAB_DIR/native/main.m" -o "$APP/HelloNative"
cat > "$APP/Info.plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>CFBundleIdentifier</key><string>local.asuna.HelloNative</string>
<key>CFBundleExecutable</key><string>HelloNative</string>
<key>CFBundleName</key><string>HelloNative</string>
<key>CFBundlePackageType</key><string>APPL</string>
<key>CFBundleVersion</key><string>1</string>
<key>CFBundleShortVersionString</key><string>1.0</string>
<key>MinimumOSVersion</key><string>15.0</string>
<key>CFBundleSupportedPlatforms</key><array><string>$SUPPORTED</string></array>
<key>UIDeviceFamily</key><array><integer>1</integer><integer>2</integer></array>
<key>UILaunchScreen</key><dict/>
<key>UISupportedInterfaceOrientations</key><array><string>UIInterfaceOrientationPortrait</string></array>
</dict></plist>
EOF
if [ "$TARGET" = simulator ]; then
    /usr/bin/codesign --force --sign - "$APP"
else
    echo 'Device build is unsigned. Signing/installing on the phone is a separate step.'
fi
echo "Built $APP"
