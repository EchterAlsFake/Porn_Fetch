# Android

Porn Fetch has an Android GUI. After the first-launch notices, setup asks you to
choose a video folder with Android's system picker. Open or create a folder and
allow Porn Fetch to use it. Cancelling the picker returns to setup so you can try
again. An existing saved folder skips this step; access is retained across launches.
Completed videos are copied there automatically. Change the folder in Settings → Video.
Android has no persistent download history or statistics. Notifications do not
keep downloads running after Android stops the app.

The app checks for updates at startup after setup. Under Settings → System & data,
you can disable startup checks or update dialogs and check manually. Installing
an offered update downloads and verifies the APK before Android asks you to
confirm installation.

To preview the layout on desktop:

```sh
uv run --no-sync main.py --android
```

This checks the layout only. Android storage, signing and notifications need a
real device. The interface is English-only.

## Build an APK

Use Linux and a separate Python 3.15 environment. Install Git, a C/C++ compiler,
make, CMake, Ninja, zip/unzip, autoconf, automake, libtool, pkg-config and JDK 21.
The working toolchain uses SDK Platform 36, Build Tools 36.0.0 and
**NDK r28c (28.2.13676358)**. The minimum Android version is API 28.
See the [companion setup guide](https://github.com/EchterAlsFake/PySide6-to-Android#environment-setup-sdkndk)
for SDK installation. Set `ANDROID_HOME` to your SDK directory, then install
and accept the required packages:

```sh
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" \
  'platform-tools' 'platforms;android-36' 'build-tools;36.0.0' 'ndk;28.2.13676358'
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --licenses
# Buildozer also looks for tools/bin/sdkmanager. Keep any existing tools folder.
if [ ! -e "$ANDROID_HOME/tools" ]; then
  ln -s "$ANDROID_HOME/cmdline-tools/latest" "$ANDROID_HOME/tools"
fi
"$ANDROID_HOME/tools/bin/sdkmanager" --version
```

If the last command fails, fix the SDK tools path before continuing.

From the repository root, create the host environment outside the checkout:

```sh
uv venv --python 3.15 ../pornfetch-android-env
export VIRTUAL_ENV="$(cd ../pornfetch-android-env && pwd)"
export UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"
export PATH="$VIRTUAL_ENV/bin:$PATH"
uv sync --upgrade --extra gui --extra build --extra android-build
uv pip install --python "$VIRTUAL_ENV/bin/python" 'PySide6==6.12.0' 'Cython==3.3.0' \
  'buildozer @ git+https://github.com/kivy/buildozer.git@fe2a18cfedd28d45329d47eae8545c81c6e8fe9a'
```

Buildozer's pinned commit supports Cython 3; the older release requires Cython 2.
These host tools must match the selected target wheels. Do not install desktop
wheels into the Android app.

Download the PySide6 and Shiboken6 wheels from
[6.12.0-api28](https://github.com/EchterAlsFake/PySide6-to-Android/releases/tag/6.12.0-api28).
Use the `cp315-cp315` pair for your architecture. Verify the original downloads
against `packaging/android_wheels.sha256` before the wrapper patches them.
To download and verify all four pairs with GitHub CLI:

```sh
mkdir -p android-wheels
gh release download 6.12.0-api28 --repo EchterAlsFake/PySide6-to-Android \
  --pattern '*cp315-cp315-android_*.whl' --dir android-wheels
(cd android-wheels && sha256sum -c ../packaging/android_wheels.sha256)
```

Build a debug APK for your own device (replace the SDK paths):

```sh
./build_android.sh --architecture aarch64 --wheels-dir "$PWD/android-wheels" \
  --sdk-path "$ANDROID_HOME" --ndk-path "$ANDROID_HOME/ndk/28.2.13676358" \
  --build-mode debug --output-dir "$PWD/dist/android"
```

Architectures are `aarch64`, `armv7a`, `x86_64`, `i686`, or `all`.
The wrapper regenerates machine paths from the tracked templates, patches Qt
and QtAsyncio, extracts the required JARs and checks the APK. Use `--clean`
after changing native recipes or Qt wheels. Downloaded archives are retained.
The wrapper keeps `.buildozer/` between runs. Qt preload libraries must be named
`libQt*.abi3.so` in the APK so Android 13 extracts them; the assembly hook does this.
The deployment patch preserves the template's Qt modules during PySide's base
configuration initialization. The template explicitly includes QtSvg and its
SVG image/icon plugins in the APK's native library folder so payment logos,
flags and help icons render on Android. The APK check requires these libraries.

The default build mode is release. Supply your own keystore with `--keystore`
and `--key-alias`, or use `--unsigned` to sign later. An unsigned release APK
cannot be installed. A debug APK uses a development key. Neither has the
publisher's signature, and neither can update an official installation signed
with a different key. Keep your own key safe if you want to update your builds.
Android or security software may warn about sideloaded or self-built APKs.

The **Cross-Platform Build Pipeline** has an `android` target for all four ABIs.
It uses the same wrapper. See [release operations](RELEASING.md) for signing
secrets and publication. SDK, native recipes and target wheels are updated as a
set; ordinary Python package resolution uses fresh compatible dependencies.

## Termux CLI

Termux runs the CLI without Qt. Its system Python must be 3.15. From this checkout:

```sh
bash scripts/install_termux.sh
.venv-termux/bin/python Porn_Fetch_CLI.py
```

The script installs system build tools, FFmpeg and current compatible Python
packages. Some native dependencies may need compilation. It runs from source;
it does not promise a portable Android executable. Use current Termux packages.

## Check on a device

Check startup, touch and Back navigation, the keyboard, URL loading, license
import, account login, pause/resume, and output-folder access after a restart.
Try a phone and a tablet in both orientations. Confirm completed files play.
Successful compilation alone does not show that these features work on a device.
