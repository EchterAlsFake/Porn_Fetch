# Native iPhone deployment result

On 2026-10-28 the native UIKit Hello World was built for arm64 with minimum iOS 15.0, signed with upstream Procursus ldid v2.1.5-procursus7, installed under `/var/jb/Applications/HelloNative.app`, registered with `uicache -p`, and launched using `uiopen --bundleid local.asuna.HelloNative`.

The phone reported a live HelloNative process. The user confirmed that its screen displayed **“Hello World! Apple toolchain works.”** This proves native installation/signing/launch on this exact iPhone 7, iOS 15.8.8, palera1n rootless setup.

The app's data container at registration was `/private/var/mobile/Containers/Data/Application/C857E5DB-100A-4A43-81A9-10990C12C8FC`. App bundle identifier is `local.asuna.HelloNative`. No SpringBoard restart or phone reboot was needed.

Tools discovered on the phone live under `/var/jb/usr/bin`; `/bin/sh` and gzip were absent. The transfer used an uncompressed tar archive over SSH. Privileged installation used the existing sudo setup with interactive authentication; no password was saved to a script or file and no sudoers configuration was changed.

Signer binary: `tools/ldid`, downloaded from the official [Procursus release](https://github.com/ProcursusTeam/ldid/releases/tag/v2.1.5-procursus7). Build source and command remain in `../native/main.m` and `../build-native.sh device`. Archive: `artifacts/HelloNative.tar`.

The next active task is a Qt 6.12 source build for arm64/iOS 15. Host Qt build uses `build-qt-host.sh`. Target Qt base build uses `build-qt-device-base.sh`. Source revisions are pinned by the cloned v6.12.0 tags. The target build enables availability diagnostics as errors to expose unguarded APIs newer than iOS 15. Success is not yet established for Qt/PySide on the phone; the simulator is preserved separately.
