# Android layout

The Android QML frontend uses the existing Qt Quick Material controls and async
backend. Desktop download rows are unaffected.

Design references consulted:
- [Android window size classes](https://developer.android.com/develop/adaptive-apps/guides/use-window-size-classes): adapt to available window width, including split screen.
- [Responsive navigation](https://developer.android.com/develop/ui/views/layout/build-responsive-navigation): bottom navigation, rail, then expanded sidebar.
- [Material lists](https://m3.material.io/components/lists/overview): prioritize primary and supporting text and avoid crowding rows with actions.
- [Android touch targets](https://support.google.com/accessibility/android/answer/7101858): minimum 48dp interactive targets.

## Decisions

- Below 600 logical pixels, show bottom navigation; from 600, show an 88px rail;
  from 840, show a 204px sidebar. Navigation scrolls in short windows.
- Keep the queue as the main screen. Add videos opens a modal bottom sheet with
  scrolling input and collapsible filters. The folder destination stays accessible.
- Each video shows a two-line title, creator/duration, status/quality, and one
  action appropriate to its state. Progress appears for active jobs. Tap the title
  or chevron to expose the full title and quality picker. Premium quality rules
  and anonymous mode still apply.
- Select opens explicit bulk controls. Checkboxes use backend selection state,
  so scrolling or hiding the selection toolbar does not reset selections.
- Cap queue width at 960 and account forms at 640 to avoid stretched tablet forms.
  Account provider choices stack on narrow screens.

## Validation

Run `uv run python -m unittest src.tests.integration.test_android_download_layout`.
The offline QML harness checks populated queues at 320×640, 400×800, 800×400,
600×960, and 1280×800, details/quality, selection, and opening the add sheet.
It disables disk caching so stale generated QML bytecode cannot hide edits.

Before release, check on Android hardware or an emulator: keyboard visibility and
sheet scrolling, system bars/insets, native folder/export pickers, Back dismissal,
TalkBack, large system text, rotation and split screen during an active download.
These platform behaviors are not established by the desktop offscreen checks.

## Display outline and row fixes

VideoObject.length is rounded minutes (see provider_parsing.parse_length); list
labels display minutes without inventing second precision. The row chevron is
Qt geometry instead of a Unicode glyph, avoiding missing device-font symbols.

On Android 12+, the build hook installs `scripts/android/PornFetchDisplay.java`.
It reads WindowInsets rounded corners after native layouts and writes changed
geometry atomically to the app-private `display-outline.json`. AndroidDisplay
watches that directory and exposes the geometry to QML without polling or JNI
Python dependencies. Corner centers are relative to the content view, accounting
for system-bar offsets; Canvas clips the outline to the Qt overlay. Only geometry
and color changes repaint, while the existing opacity animation provides pulsing.
Older systems and unreported corners retain square edges. This detects the screen
outline, not the physical curvature of glass. See Android's
[rounded-corner API](https://developer.android.com/develop/ui/views/layout/insets/rounded-corners).

The connected Xiaomi reported 134px radii at all four corners during development.
Java compilation and offline rendering were checked; verifying the native-to-QML
alignment on hardware requires rebuilding the APK with the new Java helper.
