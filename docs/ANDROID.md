# Android GUI development

The Android GUI uses `AndroidMain.qml` and shares the existing Python download and
account backend with desktop. The phone layout has bottom navigation and download
cards; wide tablet layouts use a navigation rail. Android downloads are staged in
the app's private data directory. The user can choose a destination folder from
Downloads or Settings; completed videos are then copied there automatically.
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

The current source requires Python 3.14 and uses native packages, including
`curl-cffi` and `cryptography`. Their Android compatibility must be resolved for
the target architecture before the APK can be built. The desktop deployment
specs and Python wheels cannot stand in for Android wheels. The build should
bundle the QML files under `src/frontend/UI`, the compiled Qt resources, and
the legal and licensing resources.

## Device checks

Use at least one narrow phone and one tablet in portrait and landscape. Check
navigation, software keyboard and Back behavior, single and model URL fetching,
quality licensing, pause/resume, automatic copies to a selected Android folder,
folder access after an app restart, save elsewhere through the document picker,
license import through the picker, and account login. Confirm that the Android
layout has no history/statistics tab or tracking toggle.
Automatic desktop installation and desktop update flows are not exposed in the
Android layout. CI setup is intentionally deferred.
