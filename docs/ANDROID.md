# Android GUI development

The Android GUI uses `AndroidMain.qml` and shares the existing Python download and
account backend with desktop. The phone layout has bottom navigation and download
cards; wide tablet layouts use a navigation rail. Android downloads are staged in
the app's private data directory. Downloads offers a destination folder picker
until a folder is selected; later changes are available in Settings. Completed
videos are then copied to the selected folder automatically.
**Save elsewhere** on a completed card remains available for an individual copy.
Download history, persistent tracking, and statistics are not available on Android.
No tracking database or PocketBase process is started, even if an older installation
had tracking enabled. Desktop tracking continues to use PocketBase. Licensing's
private storage is separate and unchanged; existing Android history files are left
untouched but are no longer read or updated.

## Preview the layout on desktop

Run `uv run main.py --android` from the repository root. The window opens at
phone size; resize it to at least 960 logical pixels wide to see the tablet
navigation rail. This is a layout preview: Python services, paths, and file
pickers still run on the desktop operating system. Use an APK on a device to
check Android platform behavior. SNI proxy features are disabled in the Android
layout, including the desktop preview. Download tracking is also disabled in this preview.

## Build inputs

The Android deployment configuration is
`packaging/pysidedeploy_android.spec`. Build on Linux or macOS with the matching
Android SDK/NDK and PySide6 and Shiboken6 Android wheels for the selected Qt
version and architecture. With the dependencies installed in a dedicated build
environment, start with:

```bash
pyside6-android-deploy --config-file packaging/pysidedeploy_android.spec \
  --wheel-pyside /path/to/PySide6-android.whl \
  --wheel-shiboken /path/to/shiboken6-android.whl \
  --keep-deployment-files
```

The build wrapper defaults to a **release APK** and requires **NDK r28c**
(`28.2.13676358`). It checks `source.properties`, uses the same NDK path for
PySide, Buildozer and python-for-android, and explicitly sets
`android.release_artifact = apk`. Stale NDK environment variables are ignored
during discovery; an explicit `--ndk-path` pointing to another revision fails.
Use `--build-mode=debug` only when a debug APK is wanted. Release APKs use
Buildozer's existing signing configuration; without signing credentials the
result is an unsigned release APK.

The current source requires Python 3.14 and uses native packages, including
`curl-cffi` and `cryptography`. Their Android compatibility must be resolved for
the target architecture before the APK can be built. The desktop deployment
specs and Python wheels cannot stand in for Android wheels. The build should
bundle the QML files under `src/frontend/UI`, the compiled Qt resources, and
the legal and licensing resources.

After updating the host PySide6 installation, apply and verify the deployment
patch before invoking `pyside6-android-deploy` directly:

```bash
uv run --no-sync python scripts/patch_android_deploy.py .venv
uv run --no-sync python scripts/patch_android_deploy.py .venv --verify
```

The patch keeps python-for-android on `develop` with `p4a.commit = HEAD`.
PySide6 6.12 otherwise changes the toolchain to an older release on `master`,
whose final pip install can bundle host Linux extensions into an Android APK.
Setting the branch alone is insufficient while that release commit remains pinned.

The deployment patch leaves Buildozer's cache in the project's `.buildozer/`
directory across runs, including failed builds. Buildozer and python-for-android
can then reuse downloaded archives, hostpython, libffi, other compiled recipes,
and compatible distributions. PySide's generated recipes and jars are still
refreshed. `--keep-deployment-files` retains those generated deployment files;
the Buildozer cache is retained regardless of that flag.

The wrapper `./build_android.sh --architecture=aarch64 --wheels-dir=/path/to/wheels`
applies and verifies the patch automatically. It also restores a cache left in
`deployment/.buildozer/` by an older deployment before cleaning or building.
Subsequent runs keep it at `.buildozer/` so compiled paths stay stable.

Add `--clean` to the wrapper command after changing Qt wheels, native recipes,
or the toolchain. This removes the selected architecture's compiled build and
distribution cache while keeping downloaded dependency archives and other
architectures' builds. Python/QML-only changes can use the normal incremental build.
When first upgrading an existing cache to the pinned NDK, the wrapper rebuilds
that architecture's native output once, preserving its downloaded archives.

## Device checks

Use at least one narrow phone and one tablet in portrait and landscape. Check
navigation, software keyboard and Back behavior, single and model URL fetching,
quality licensing, pause/resume, automatic copies to a selected Android folder,
folder access after an app restart, save elsewhere through the document picker,
license import through the picker, and account login. Confirm that the Android
layout has no history/statistics tab or tracking toggle.
Automatic desktop installation and desktop update flows are not exposed in the
Android layout. CI setup is intentionally deferred.
