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

- Host Python 3.15 and PySide6 6.12.0, with the virtual environment outside the
  project to avoid Qt's QML scanner traversing installed packages.
- Buildozer is pinned to upstream commit
  `fe2a18cfedd28d45329d47eae8545c81c6e8fe9a` (Cython 3 support), with Cython
  3.3.0 for Python 3.15 host compatibility. Released Buildozer 1.6.0 requires
  Cython <3 and cannot resolve alongside Cython 3.3.0. The Android deployment
  spec preserves the Buildozer version installed by CI.
- Target Python and hostpython are both pinned to 3.15.2. Updating the host
  interpreter alone does not update python-for-android's embedded runtime.
  The wrapper rebuilds compiled caches when the target Python version changes,
  retaining downloaded archives.
- JDK 21, SDK Platform 36, Build Tools 36.0.0, NDK r28c / 28.2.13676358. This
  follows the companion guide's tested NDK choice; it does not rebuild Qt.
- The runner's `cmdline-tools/latest` directory is exposed at SDK `tools` for
  Buildozer 1.6's `tools/bin/sdkmanager` lookup. CI checks that this command runs
  before compilation. APK builds use Bash with `pipefail` so logging through
  `tee` preserves compilation failures and prevents subsequent signing steps.
- Minimum Android API 28, retained from the application's working Buildozer spec.
- Matching PySide6 and Shiboken6 `cp315-cp315` wheels from
  <https://github.com/EchterAlsFake/PySide6-to-Android/releases/tag/6.12.0-api28>.
  CI verifies both wheel checksums against the tracked
  `packaging/android_wheels.sha256` before the application's intentional wheel
  modifications. That file pins the eight wheels used by the four ABI jobs;
  adding other assets to the upstream release cannot change these checks.
  The release and selected wheel hashes are pinned together in the repository; no
  `ANDROID_WHEELS_RELEASE` or `ANDROID_WHEELS_SHA256SUMS_SHA256` environment
  variables are needed. Update the release and tracked checksums together when
  changing wheel builds.
  Wheel names remain
  `pyside6-6.12.0-6.12.0-cp315-cp315-android_<arch>.whl` and
  `shiboken6-6.12.0-6.12.0-cp315-cp315-android_<arch>.whl` for the four ABIs.
  These bindings target native API 28, matching `android.minapi` and
  `android.ndk_api`; SDK 36 remains the Java compilation target. Do not substitute
  the API 35 Python runtime archives from the older `6.12.0` release.
- QtAsyncio patch, verification, Android deploy patch, verification, then the
  existing Android build script. The wrapper patches the target wheel too.
  Host and target PySide6 initializers preload the executor before Qt installs
  its module attribute hook, preserving Python 3.15 `asyncio.to_thread` calls.
- Generated Qt recipes and JARs are recreated from the selected wheel. The
  checked-in developer cache must not supply another ABI's absolute wheel paths.
- The wrapper extracts the wheel's JARs and writes `android.add_jars` before
  invoking PySide deploy, including on a clean runner. It checks that the
  bindings JAR contains `QtActivity` before starting compilation.
- The p4a assembly hook renames the native preload copies of `Qt*.abi3.so` to
  `libQt*.abi3.so` and updates Qt's `load_local_libs` resource. Android 13 only
  extracts `lib*.so` from APK native libraries. The original Python wheel module
  names in the private Python bundle stay unchanged. The APK check rejects
  unextractable names and missing Qt/Python/Tor runtime files before signing.
- Local recipes build `curl_cffi` 0.17.0 for every ABI against checksum-verified
  curl-impersonate 2.3.1 Android libraries. CFFI 2.1.1 matches that version's
  runtime requirement. OpenSSL is pinned to the maintained 3.5.9 LTS release.
  Cryptography 50.0.2 uses the target Python installation
  for Rust/CFFI compilation so 32-bit targets never use 64-bit host headers.
  Maintained recipes live in `p4a-recipes`; the deploy patch copies them into
  `deployment/recipes` after PySide cleans its generated deployment directory.
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

For a first release with no existing signing identity, create a key once using
the JDK's `keytool`, in a private directory outside the checkout:

```bash
umask 077
keytool -genkeypair -storetype PKCS12 -keystore android-release.p12 \
  -alias pornfetch-release -keyalg RSA -keysize 4096 -validity 36500
```

Keep the keystore and its password in a separate encrypted backup. Reuse this
identity for every later release; an APK signed with another key cannot update
an existing installation. PKCS#12 stores use the same store and key password.

Upload the keystore directly through standard input, then enter the passwords
and alias at the CLI's hidden prompts:

```bash
python -c 'import base64, pathlib; print(base64.b64encode(pathlib.Path("android-release.p12").read_bytes()).decode())' \
  | gh secret set ANDROID_KEYSTORE_BASE64 --repo EchterAlsFake/Porn_Fetch --env beta
gh secret set ANDROID_KEYSTORE_PASSWORD --repo EchterAlsFake/Porn_Fetch --env beta
gh secret set ANDROID_KEY_ALIAS --repo EchterAlsFake/Porn_Fetch --env beta
gh secret set ANDROID_KEY_PASSWORD --repo EchterAlsFake/Porn_Fetch --env beta
gh secret list --repo EchterAlsFake/Porn_Fetch --env beta
```

Use `pornfetch-release` as the alias for the example key. For an existing
keystore, use its actual filename, alias and passwords. Base64 must have no
embedded line breaks because the workflow validates it strictly.

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

Workflow artifacts upload each APK directly, with `archive: false`, so the
download is the `.apk` itself. Checksums and legal archives are separate downloads.

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

After changing build scripts or workflow files, start a new workflow run from
the updated commit. Re-running failed jobs uses the original commit, although
newly configured environment secrets are available to those jobs.

### Confirmed failures on 2026-11-02

All four Android jobs in [run 41354113959](https://github.com/EchterAlsFake/Porn_Fetch/actions/runs/41354113959)
failed before compilation: the `6.12.0` release's whole `SHA256SUMS` no longer
matched the digest pinned by that commit. The current workflow uses API 28
Python 3.15 wheels and pins the eight selected files directly. All eight downloads
were checked against the new tracked manifest on 2026-11-02.

The Teclast T50 Pro (Android 13/API 33, ARM64, 4 KiB pages) reproduced a separate
startup failure: `QtLoader` could not find `nativeLibraryDir/QtCore.abi3.so`.
The file was inside the APK, but Android skipped extracting its name without a
`lib` prefix. A separately installed diagnostic copy with corrected native names
and loader resources reached the rendered QML interface and started again after
a cold restart. The original installed app and its data were preserved.
That test repackaged the tablet's existing APK (package version 3.8.1, Python
3.14); it validates the loader fix, not a complete new Python 3.15 build. A new CI
run from the updated commit is still needed for all four complete builds.

### Retry website publication without rebuilding

Use **Publish Existing Website Builds** (`publish_website.yml`) with the completed
Cross-Platform Build Pipeline run ID, its exact release version, and the original
website channel. Confirm the redistribution review for those artifacts. The job
reuses the run's original source commit and creation timestamp, downloads its
existing artifacts, and publishes both website downloads and the signed Android
feed. Existing staged manifests must match exactly; published releases remain
immutable. Artifacts must still be available in GitHub Actions.

The website upload server must support requests lasting longer than a normal
page request. Production uses Gunicorn's threaded workers (`--threads 4
--timeout 90`) so the worker can report that it is alive during a long upload.
A synchronous worker's default timeout can terminate an APK upload and appear
in CI as `BrokenPipeError`; inspect the server's worker-timeout log first.
