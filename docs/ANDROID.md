# Android

Porn Fetch has an Android GUI. After the first-launch notices, setup asks you to
choose a video folder with Android's system picker. Open or create a folder and
allow Porn Fetch to use it. On Android 10+, you can instead select **Use shared
Downloads/Porn Fetch**, which saves through Android's MediaStore without a picker
or broad storage permission. This also works on TV and Automotive images whose
file picker only displays a "not supported" message. Shared files remain after
uninstalling Porn Fetch. Cancelling the picker returns to setup so you can try
again or use that alternative. An existing destination skips this step; the
choice is retained across launches.
Completed videos are copied there automatically. Change the folder in Settings → Video.
The MediaStore fallback needs a new APK containing `PornFetchStorage.java`; a
Python-only update to an older APK cannot add the native helper. Android 9 still
requires a working document-tree picker.
Android has no persistent download history or statistics. Notifications do not
keep downloads running after Android stops the app.

The interface supports portrait and landscape. Android chooses the orientation
using the device's normal behavior and the user's rotation settings. Layouts
adapt to the available window width, with no separate orientation rules for
phones, tablets, TV or Automotive devices. The build wrapper preserves this
policy when regenerating deployment settings; existing APKs need a rebuild.

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
Install Apache Ant as well: `sudo pacman -S --needed apache-ant` on Arch Linux,
or `sudo apt-get install ant` on Debian/Ubuntu. The wrapper finds its installation
through `ANT_HOME`, the resolved `ant` executable on `PATH`, or a valid configured
`android.ant_path`. It reports a missing installation before building, rather
than downloading Buildozer's legacy Ant archive or writing into `/usr/share`.
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

The build wrapper also creates this compatibility link automatically when
`tools` is absent. It supports both `cmdline-tools/latest` and the direct
`cmdline-tools` layout installed by Qt's `cross_compile_android/main.py
--download-only --auto-accept-license` helper. It links the whole directory so
sdkmanager can find its libraries. Existing `tools` directories and symlinks are
preserved; an unusable one produces an error before compilation.

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

Buildozer's pinned commit supports Cython 3; release 1.6.0 requires Cython <3.
The wrapper installs that same pinned commit into the selected build environment
when it is missing or different, preventing the local Cython dependency conflict.
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
It also inspects the compressed Python bundle for PyJWT's `jwt` package.
Licensing imports that package during startup, before the first-use screen;
missing it prevents the app from opening even when every native library is present.

Every build is aligned, signed and verified automatically. The default build
mode is release: it uses `my-release-key.jks` / `my-key-alias` in the project root
when present, otherwise it uses the standard `~/.android/debug.keystore`.
Debug builds use that debug key too. The wrapper creates it with JDK `keytool`
when missing and reuses it on later builds, without password prompts.
The final output is `app-signed.apk` in the project root or `--output-dir`;
`--architecture all` adds architecture suffixes. Alignment intermediates stay
in a temporary directory. Signing tools are found on `PATH` or in the selected
SDK's `build-tools` directory.

Supply a release key explicitly with `--keystore` and `--key-alias`.
An explicit missing keystore or a signing failure stops the build, preserving
any previous signed output. Set `ANDROID_KEYSTORE_PASSWORD` and
`ANDROID_KEY_PASSWORD` to sign without prompts; `ANDROID_KEY_ALIAS` sets the
default release alias. Otherwise apksigner asks for release passwords.
A development key cannot update an official installation signed with a different
key. Keep your own key safe if you want to update your builds.
Android or security software may warn about sideloaded or self-built APKs.

The **Cross-Platform Build Pipeline** has an `android` target for all four ABIs.
It uses the same wrapper and release signing credentials when configured.
Build-only runs without credentials produce debug-signed, installable APKs;
publishing requires complete release credentials. See [release operations](RELEASING.md) for signing
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
