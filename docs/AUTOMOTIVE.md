# Automotive

Porn Fetch adapts its Android APK for direct installation on Android Automotive OS
(AAOS) and compatible Android head units. It remains a downloader, with a parked
interface. These changes do not create a projected Android Auto or CarPlay app.
A new APK is required because input and vehicle status use native activity hooks.

## Platforms and distribution

The following distinctions were checked against platform documentation on
2026-11-16. Manufacturer branding alone is insufficient to identify which system
an installation uses.

| System | What it means for Porn Fetch |
| --- | --- |
| Android Automotive OS | Android runs in the vehicle. The APK can be installed where the vehicle permits sideloading. Detect `FEATURE_AUTOMOTIVE`, use the vehicle's restrictions, and adapt to its display and input. |
| AAOS with Google built-in | The same OS adds Google apps and services. Availability differs from phones; Porn Fetch's networking, licensing and APK updater do not require Google Play services. |
| AAOS without Google services | Use the same public Android/car API paths. Do not assume a browser, file picker, app store or particular keyboard is installed. |
| Android Auto | Runs supported phone apps through projection. Its currently supported parked category is games. Porn Fetch does not qualify as a game, audio app or driving-task app. Adding `CAR_LAUNCHER` is insufficient. |
| Generic Android head unit | May run ordinary Android without the automotive feature or car services. The manual **Car layout** preference supplies larger controls; receiving raw rotary input also enables controller focus. There is no reliable vehicle-restriction guarantee on such devices. |
| Apple CarPlay | A separate iOS integration using Apple's framework, approved entitlements and supported vehicle capabilities. Current video support concerns playback in supported cars, not arbitrary projection of a QML downloader. |

Sources: [AAOS overview](https://developer.android.com/training/cars/platforms/automotive-os),
[Google services on AAOS](https://developer.android.com/training/cars/platforms/automotive-os/google-play),
[Android Auto parked categories](https://developer.android.com/training/cars/parked/auto),
[CarPlay](https://developer.apple.com/carplay/).
The generic-head-unit fallback is an application design choice, not an assertion
that every aftermarket unit implements AAOS interfaces.

Google Play prohibits apps promoting pornography. Porn Fetch should not present
its APK adaptations as Google Play eligibility or approval. Its purpose also
differs from the streaming-playback categories described in Android's car guides.
See [Google Play content policy](https://support.google.com/googleplay/android-developer/answer/9878810)
and [car app categories](https://developer.android.com/training/cars).

## Input and navigation

Cars can combine touchscreens, directional nudges, rotary encoders and hardware
Back/center controls. Native AAOS rotary navigation is commonly mediated by
`RotaryService`, using accessibility focus, `FocusParkingView` and `FocusArea`.
A raw wheel event and an OEM-managed rotary controller are distinct integration
paths. See the [AOSP app integration guide](https://source.android.com/docs/automotive/hmi/rotary_controller/app_developers).

Porn Fetch implements:

- Existing D-pad, Tab, center and Back paths, including modal focus containment,
  lazy lists and focus visibility.
- Raw `SOURCE_ROTARY_ENCODER` scroll events, including multiple detents and
  fractional deltas. Mouse wheels retain their normal scrolling behavior.
- System-navigation nudge events delivered to the activity, translated into
  directional keys. Media, volume and Home keys remain with Android.
- Sequential rotation through available controls. Center enters field editing
  or value adjustment; rotation adjusts selected sliders and number controls;
  Back returns to navigation. Long document readers scroll before focus advances.
- Switching back to touch clears the controller focus policy. Pausing the activity
  clears partial rotary input and exits QML editing/adjustment mode.

An OEM may consume controller events in `RotaryService` before they reach the Qt
activity. This implementation does not install native `FocusArea` or
`FocusParkingView` wrappers around the QML scene. It therefore does not establish
complete OEM-managed rotary accessibility integration. Such systems require an
OEM/Qt accessibility integration pass and testing with that controller. Keyboard
navigation, raw encoder checks and a successful build cannot certify that path.

The vehicle's IME owns rotary text entry. If an OEM supplies no rotary-capable
keyboard, the app cannot manufacture that capability by translating wheel events.
The guide above documents this dependency.

## Vehicle restrictions and lifecycle

`PornFetchAutomotive.java` publishes native device, controller and lifecycle state
through an atomic private file. `PornFetchCarService.java` is loaded only on AAOS
and connects asynchronously to the public `android.car` library. It listens to
`CarUxRestrictionsManager` and uses `isRequiresDistractionOptimization`, rather
than interpreting speed or gear values itself.

When restrictions are reported, the app blocks the interface and shows a parked-use
screen with an exit action. It suppresses browser launches, preserves page history
and unfinished setup, and restores focus when restrictions clear. A car-service
connection loss blocks the app's interface while status is unavailable. If the
optional car API cannot load at all, ordinary AAOS activity restrictions remain
the fallback. No activity is marked `distractionOptimized`.

The APK declares the automotive feature and `android.car` library as optional, so
phones and TVs remain installable. It opts into display compatibility mode; on
vehicles advertising that feature, duplicate application-level Back/close controls
are hidden. Other car screens have explicit Back and **Close app** controls.
See [parked-app restrictions](https://developer.android.com/training/cars/parked/automotive-os)
and [AAOS compatibility mode](https://developer.android.com/training/cars/platforms/automotive-os/compatibility-mode).

Lifecycle state does not add background downloading, a wake lock, an ignition
listener or a power-off scheduler. Android/OEM process and suspend limits still
apply. Existing queue recovery and cooperative shutdown remain responsible for
resuming downloads. See [AAOS power management](https://source.android.com/docs/automotive/power/power).

## Displays, storage and account actions

AAOS supports fixed portrait and landscape displays, wide/ultrawide layouts,
cutouts, system bars and passenger/distant displays. The app respects system
orientation, uses QML safe areas, adds a screen-edge margin and larger default
text for car layouts, and gives shared buttons, fields, selectors and number
controls 64-pixel minimum layout heights. This is not a claim that every screen
meets all car-quality tiers; those also specify spacing and typography criteria.
See [car app quality](https://developer.android.com/develop/adaptive-apps/quality-guidelines/car-app-quality).

On ordinary Android head units, enable **Settings → Appearance → Car layout**
when automatic identification is unavailable. That preference does not claim to
read driving state or add restrictions supplied by missing vehicle services.

Existing MediaStore shared Downloads avoids a missing document-tree picker on
Android 10+. Android 9 still requires a working picker. Pasted license-file import
avoids a missing license-file picker. Web links show an address for another device,
so account/help/purchase actions do not assume an installed car browser. Completed
video playback belongs to another application, outside Porn Fetch's UI lifecycle.

## Build and verification

The normal Android build hook stages both helpers, patches fresh and incremental
Qt activities, adds the SDK's `android.car` compile library and keeps that library
optional at runtime. No car UI Maven artifact, commercial Qt Automotive module,
platform signature or vehicle-control permission was added.

Useful offline checks:

```sh
QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software QML_DISABLE_DISK_CACHE=1 \
  .venv/bin/python -m unittest \
  src.tests.unit.test_android_automotive \
  src.tests.integration.test_android_display \
  src.tests.integration.test_android_navigation \
  src.tests.integration.test_android_remote_navigation
```

On a rebuilt app, check both portrait and landscape, a narrow screen and an
ultrawide/passenger display. Use touch, D-pad, encoder rotation and center/Back.
Verify setup, license entry, selectors, sliders, long queues, dialogs, shared
exports and update installation. Enter/leave the system's restricted state and
confirm that the underlying interface stays inaccessible and resumes with its
history intact. Verify Home and return separately from a true process restart.
Preserve existing application settings when doing these checks.

Debug AAOS images can inject controller input using the commands in the AOSP
rotary guide. Production/user emulator images can reject those commands; do not
interpret that as evidence that a controller path passed. Full APK integration,
OEM-managed rotary focus, the car keyboard and actual vehicle restriction
transitions require device-specific verification.

On 2026-11-16, an isolated native probe on the existing AAOS API 33 distant-display
emulator connected to the real car UX service and read its initial unrestricted
state. Production native helpers passed injected encoder direction, aggregate and
fractional detents, delivered nudge translation, mouse preservation,
touch/controller switching and Home/resume checks. A pause-generation counter
retains lifecycle changes even when Qt only reads the resumed state. A synthetic
restriction callback verified private-state publication and suppressed rotary actions; it
did not simulate the vehicle entering a real driving restriction. The probe was
separate from the installed Porn Fetch app. Offline QML checks cover the resulting
restriction screen, focus/history restoration and lifecycle adjustment reset.
The probe was uninstalled and the emulator session closed afterward.
