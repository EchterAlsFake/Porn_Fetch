# Android GUI development

The Android GUI uses `AndroidMain.qml` and shares the existing Python download and
account backend with desktop. The phone layout has bottom navigation and download
cards; tablet widths use a navigation rail. Android downloads are written to the
app's private data directory. A completed card's **Save to device** action uses
the native document picker to copy it to a user-chosen location. The history
database uses in-process SQLite on Android, while desktop keeps PocketBase.

## Preview the layout on desktop

Run `uv run main.py --android` from the repository root. The window opens at
phone size; resize it to at least 700 logical pixels wide to see the tablet
navigation rail. This is a layout preview: Python services, paths, and file
pickers still run on the desktop operating system. Use an APK on a device to
check Android platform behavior.

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

The current source requires Python 3.14 and uses native packages, including
`curl-cffi` and `cryptography`. Their Android compatibility must be resolved for
the target architecture before the APK can be built. The desktop deployment
specs and Python wheels cannot stand in for Android wheels. The build should
bundle the QML files under `src/frontend/UI`, the compiled Qt resources, and
the legal and licensing resources.

## Device checks

Use at least one narrow phone and one tablet in portrait and landscape. Check
navigation, software keyboard and Back behavior, single and model URL fetching,
quality licensing, pause/resume, save through the Android document picker,
license import through the picker, account login, and history after relaunch.
Automatic desktop installation and desktop update flows are not exposed in the
Android layout. CI setup is intentionally deferred.
