#!/bin/sh
# Installs only one of the lab's own app bundles. SSH/sudo authenticates normally.
set -eu
DEVICE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if [ "$(id -u)" = 0 ]; then
    exec sudo -H -u asuna /bin/sh "$0" "$@"
fi
APP_NAME=${1:?Usage: deploy-app.sh AppName}
case "$APP_NAME" in
    HelloNative|PythonNative|NativeModules|QtPhoneHello|QtQuickPhoneHello|PythonQtPhoneHello|PornFetch) ;;
    *) echo 'Unknown lab app name' >&2; exit 2 ;;
esac
CONFIG="$DEVICE_DIR/../ssh/config"
ssh -F "$CONFIG" -o BatchMode=yes ios-phone \
    "/var/jb/usr/bin/killall -TERM '$APP_NAME' '${APP_NAME}_bin' 2>/dev/null || true"
ssh -F "$CONFIG" -o BatchMode=yes ios-phone \
    "/var/jb/usr/bin/mkdir -p /var/mobile/ios-lab; /var/jb/usr/bin/rm -rf /var/mobile/ios-lab/$APP_NAME.app"
ssh -F "$CONFIG" -o BatchMode=yes ios-phone \
    '/var/jb/usr/bin/tar -xf - -C /var/mobile/ios-lab' < "$DEVICE_DIR/artifacts/$APP_NAME.tar"
ssh -tt -F "$CONFIG" -o BatchMode=yes ios-phone \
    "sudo /var/jb/usr/bin/sh -c 'set -e; PATH=/var/jb/usr/bin:/var/jb/bin:/usr/bin:/bin:/usr/sbin:/sbin; export PATH; test -d /var/mobile/ios-lab/$APP_NAME.app; rm -rf /var/jb/Applications/$APP_NAME.app; cp -a /var/mobile/ios-lab/$APP_NAME.app /var/jb/Applications/; chown -R root:wheel /var/jb/Applications/$APP_NAME.app; for executable in /var/jb/Applications/$APP_NAME.app/$APP_NAME /var/jb/Applications/$APP_NAME.app/${APP_NAME}_bin; do if test -f \"\$executable\"; then chmod 755 \"\$executable\"; fi; done; /var/jb/usr/bin/uicache -p /var/jb/Applications/$APP_NAME.app'"
ssh -F "$CONFIG" -o BatchMode=yes ios-phone \
    "/var/jb/usr/bin/uiopen --bundleid local.asuna.$APP_NAME; /var/jb/usr/bin/uicache -i local.asuna.$APP_NAME"
