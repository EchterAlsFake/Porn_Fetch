# Android builds in GitHub Actions

The Cross-Platform Build Pipeline builds four Android APKs using
`scripts/build_android.py`: `aarch64` → `arm64-v8a`, `armv7a` → `armeabi-v7a`,
`x86_64` → `x86_64`, and `i686` → `x86`.

Choose `build_target: android` to iterate without desktop compilation, `gui` for
desktop and Android GUI builds, or `both` to also build the CLI. The existing
release version and timestamp are stamped into the Android app and deployment
specs. CLI-only runs skip Android. Each ABI runs in its own Ubuntu runner, with
`fail-fast: false` so one failure does not discard the other build logs.

## Toolchain and patches

- Host Python 3.14 and PySide6 6.12.0, with the virtual environment outside the
  project to avoid Qt's QML scanner traversing installed packages.
- JDK 21, SDK Platform 36, Build Tools 36.0.0, NDK r28c / 28.2.13676358. This
  follows the companion guide's tested NDK choice; it does not rebuild Qt.
- Minimum Android API 28, retained from the application's working Buildozer spec.
- Matching PySide6 and Shiboken6 `cp314-cp314` wheels from
  <https://github.com/EchterAlsFake/PySide6-to-Android/releases/tag/6.12.0>.
  CI verifies the pinned SHA256SUMS digest and both wheel checksums before the
  application's intentional wheel modifications.
- QtAsyncio patch, verification, Android deploy patch, verification, then the
  existing Android build script. The wrapper patches the target wheel too.
- Generated Qt recipes and JARs are recreated from the selected wheel. The
  checked-in developer cache must not supply another ABI's absolute wheel paths.
- `packaging/prepare_android_ci.py` keeps app requirements, package identity,
  permissions and minimum API, replacing machine paths and the release version.
  It uses the tracked Android PySide deployment template, not desktop settings.

Reference setup instructions:
<https://github.com/EchterAlsFake/PySide6-to-Android#environment-setup-sdkndk>.

## Signing and publication

In the app repository's GitHub environment **beta**, add:

| Secret | Value |
| --- | --- |
| `ANDROID_KEYSTORE_BASE64` | Base64 of the existing release keystore |
| `ANDROID_KEYSTORE_PASSWORD` | Keystore password |
| `ANDROID_KEY_ALIAS` | Release key alias |
| `ANDROID_KEY_PASSWORD` | Private-key password; often the same as the store password |

Use the existing Android signing identity so updates can replace earlier APKs.
Keep the keystore backed up separately. Do not generate a different key on each
runner. The workflow decodes it in the runner's temporary directory, passes
passwords through environment variables, verifies each signature, and removes
the temporary keystore. It does not upload signing material.

Without a keystore, build-only runs retain explicitly named `_unsigned.apk`
artifacts for build diagnostics; those need signing before installation.
`deploy_website` or `create_release` requires all four signing secrets up front.
There is no unsigned fallback for public publishing.

For website publishing, also configure `WEBSITE_RELEASE_TOKEN` and optionally
`WEBSITE_ORIGIN` as described in the server's `docs/WEBSITE_DOWNLOADS.md`. Choose a
new version, enable `deploy_website`, select the website channel, and complete the
existing release-review acknowledgment. A GitHub Release is optional.

The publisher waits for all four Android matrix jobs. It receives signed
`PornFetch_android_GUI_<ABI>.apk` files, SHA-256 sidecars and legal archives. An
Android-only release can be published without replacing existing desktop variants.
Desktop updater feeds remain controlled by their existing workflow inputs.

## First build and troubleshooting

Start with `build_target: android`, with publishing disabled. Inspect each ABI's
job log and `android-build-diagnostics-<architecture>` artifact, which contains
the deployment specs and build log when available. Diagnostics are excluded from
public release assets. No device or emulator run is performed by this workflow.

The companion wheels and application dependency recipes still need a real CI
build and device testing. Native dependency compilation, ABI-specific runtime
issues and SDK/Gradle compatibility may need follow-up fixes. The matrix builds
the APKs; passing workflow lint or offline packaging tests alone does not prove
that an APK starts successfully on Android.
