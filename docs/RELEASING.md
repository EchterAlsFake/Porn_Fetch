# Build and publish a release

For a personal unsigned build, use [the installation guide](INSTALLATION.md).
This page is for maintainers publishing official artifacts.

## Build inputs

Run **Cross-Platform Build Pipeline** from the intended commit. Choose a full
three-part numeric `release_version` (major.minor.patch), such as `3.9.77`, and a target: `cli`, `gui`, `both`,
`android`, or `ios`. GUI includes Android and iOS; CLI-only skips both. Mobile-only targets skip desktop builds. Optional experimental
architectures have separate checks. A tag build uses the tag's version.

The experimental RISC-V job uses GCC 14 explicitly. Ubuntu 24.04's default
GCC 13 rejects the `-mno-omit-leaf-frame-pointer` flag inherited from Python 3.15
when compiling native dependencies.

All workflow host tools are pinned to Python 3.15.2. Android embeds Python 3.15.2; iOS reuses the pinned Python 3.15.0rc2 runtime and matching native archives. Updating that iOS runtime requires rebuilding and publishing the matching toolchain.

CI resolves current compatible Python dependencies with `uv sync --upgrade`.
It does not use a committed `uv.lock`. Each job keeps its environment unchanged
after setup and records dependency information with its legal/build output.
GitHub Actions are pinned to verified commits, with daily Dependabot updates.
Native mobile wheels and checksum-verified tool/source downloads keep matching
versions and hashes. Review and update those together.

All binaries and update metadata use the chosen version and the original workflow
timestamp. A rerun keeps that timestamp. Use a newer version than the published
one. CLI publication checks this before compilation. After changing source or
workflow files, start a new run; rerunning an old job uses its old commit.

GitHub release asset collection copies existing GUI archives, installers, mobile
packages, checksums and platform-specific legal archives unchanged. Only CLI
payloads are bundled with their helpers. Shared files such as `LICENSE` remain
inside bundles and legal archives, avoiding filename collisions between platforms.

Start with publication disabled. Inspect the build logs, signatures and platform
smoke checks. Then test the actual artifacts on clean systems. Passing Python
tests is not a substitute for installation and device tests.

## Signing credentials

PR tests never need production signing keys. Desktop signing uses the GitHub
Environment `signing`:

| Secret | Use |
| --- | --- |
| `CERTUM_EMAIL` | Certum SimplySign account |
| `CERTUM_OTP` | Base32 TOTP seed or otpauth URI, not a current six-digit code |
| `MACOS_CERT_P12_BASE64` | P12 with one Developer ID Application identity and private key |
| `MACOS_CERT_PASSWORD` | P12 password |
| `APPLE_ID` | Apple notarization account |
| `APPLE_APP_PASSWORD` | App-specific password |
| `APPLE_TEAM_ID` | Apple Developer team ID |

Android signing uses Environment `beta`: `ANDROID_KEYSTORE_BASE64`,
`ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS`, `ANDROID_KEY_PASSWORD`.
Reuse the same Android key for updates and keep an encrypted backup. See
[Android](ANDROID.md) for local signing.

The updater uses `CLI_UPDATE_SIGNING_KEY` in `beta`, containing the complete
online PEM key. The deployment API uses repository secret `CI_TOKEN`. Website
publication uses `WEBSITE_RELEASE_TOKEN` and optional variable `WEBSITE_ORIGIN`.
Do not put private keys, session files or keystores in artifacts or source control.

## Windows

`packaging/sign_windows.ps1` signs EXE/DLL/PYD files and verifies Authenticode.
Native dependencies are signed before packaging; the final EXE/setup is signed
last. Valid vendor signatures are preserved. Drivers must retain their valid
vendor signature. A publisher certificate cannot replace driver signing.

The CLI signs copies of native payloads before creating the onefile executable.
UPX is disabled for signed Windows/macOS payloads. Windows x64 installers include
a signed maintenance component, not just a signed setup EXE. CI installs it in a
temporary folder, checks the installed maintenance binary, then uninstalls it.
Windows ARM64 currently uses the portable GUI build.

The application requires `eaf-base-api>=4.2.6` for FFmpeg remux/tagging launches
that do not inherit Windows console input handles. Publish the matching library
release before building the app; a fix in a sibling checkout does not reach CI's
PyPI dependency installation. The Windows FFmpeg fixture checks include a real
windowless child process with an invalid inherited input handle, matching the
Explorer/Start Menu failure mode.

Certum sessions live only in the runner's temporary folder and are cleaned up
on failure too. Signing or timestamp failures stop the release job.

Windows can display the whole signing-certificate subject as the publisher,
including country, state, locality, organization and common name. Repeating a
personal name in organization (`O`) and common name (`CN`) is valid. The app's
version information, IFW Publisher and `ssign --name` do not override this identity.
Inspect a published executable in PowerShell with
`(Get-AuthenticodeSignature -LiteralPath '.\Porn Fetch.exe').SignerCertificate.Subject`.
Changing those signed identity fields requires a certificate reissue through
Certum, subject to its validation requirements; changing app metadata cannot
remove location fields from an existing certificate.

## macOS

`packaging/sign_macos.py` creates a temporary keychain, imports the Developer ID
identity, checks notarization credentials, and removes the keychain afterwards.
Local builds are only ad-hoc signed; official releases must not fall back to that.

Runtime data is moved to `Contents/Resources/runtime` before signing, with relative
symlinks preserving the paths expected by bundled packages. Data must not occupy
macOS code locations; see [Apple's bundle layout guidance](https://developer.apple.com/library/archive/technotes/tn2206/).
The macOS deployment template excludes `src/frontend/graphics/ios`: its source
asset catalog is only used by iOS staging and breaks macOS signing if copied into
`Contents/MacOS` as an uncompiled nested bundle.

1. Repair native dependencies, sign inner Mach-O files and bundles, then sign
   the app. Use hardened runtime and only the required entitlements.
2. Notarize and staple the app, then make, sign, notarize and staple its DMG.
3. Re-sign the Universal app after merging architecture slices.
4. IFW removes optional helpers from its app payload. Sign/notarize that exact
   staged app again. Ship a signed maintenance app and updater component.
5. Verify the installed app and maintenance tool before publishing.

Notarization must return `Accepted`. Bare CLI executables and ZIP files cannot
be stapled; macOS retrieves their tickets online. Rejections and missing credentials
fail the job. Each upload records its submission ID before waiting up to 60 minutes.
If the wait times out, CI checks that same submission and retains its status and
the tool's stdout/stderr in the build diagnostics. `In Progress` means Apple is
still processing it; use the recorded ID with `notarytool info` or `wait` and your
notarization credentials to check it later. See
[Apple's notarization guide](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow)
and [Qt's maintenance component procedure](https://doc.qt.io/qtinstallerframework/ifw-updates.html#populating-the-maintenance-tool-component).

## Installers and update feeds

Desktop installers use Qt Installer Framework. The core app is required; FFmpeg
and PocketBase are optional. Optional tools live outside the macOS app bundle so
adding or removing one does not invalidate the app signature.

For a local installer/repository, prepare the IFW tools with
`uv run --no-sync python packaging/install_ifw.py --help`, then run:

```sh
uv run --no-sync python packaging/generate_repository.py \
  --dist-dir /path/to/complete/app-folder --platform linux --arch x64 \
  --pocketbase-binary /path/to/pocketbase --ffmpeg-binary /path/to/ffmpeg \
  --output-repo /path/to/repository \
  --output-installer /path/to/PornFetch_Setup
```

Do not pass a lone GUI executable as `--dist-dir`. On macOS supply the app bundle.
Keep these local outputs separate from production repositories. The local command
has no release publisher signature unless you configure and run signing yourself.

Desktop updates verify signed metadata and stage verified repository bytes before
launching Qt Maintenance Tool. CLI updates use TUF; Android uses a separate TUF
feed and asks the OS installer for permission and confirmation. Updates are free
and do not need a Premium license. Portable GUI/source copies update manually.

Update payloads use HTTP/1.1: the production HTTP/2 route was observed resetting
CLI transfers at exactly 1 MiB. TUF downloads resume interrupted streams with a
validated HTTP Range response, with at most three attempts; final signed lengths
and hashes are still mandatory. Desktop staging retries interrupted transfers
before launching IFW and shows download progress. Successful launch uses the
normal cooperative shutdown to save the queue and release services.

The signed maintenance component stays forced, virtual and a dependency of the
core app, but is not Essential. IFW prioritizes Essential updates and requires a
restart before installing other updates, which caused Windows users to run each
release update twice. The signed replacement tool can be installed alongside
the app using IFW's deferred tool replacement.

`src/cli/update_root.json` is the shared public trust anchor. Keep its root private
key offline, with verified encrypted backups. The online key signs release/update
metadata. Never upload the root private key to GitHub or a deployment server.
After clients have shipped, rotate trust roots with signatures from both the old
and new roots. A new unrelated version-1 root cannot update those clients.
`packaging/init_cli_updates.py` is for deliberate initialization, not an automatic
repair for missing private keys.

Publish signed repositories before announcing a release. The pipeline runs
`packaging/verify_deployment.py` after upload to verify public metadata and actual
payload downloads. Do not ignore a stale, expired or invalid feed. The scheduled
refresh workflow renews metadata between releases; monitor failures before the
seven-day timestamp expiry. CLI publishing and refresh share a concurrency group.

Use **Publish website release** to retry publication from an eligible existing
build without compiling again. Android-only and iOS-only publication retain desktop variants from earlier releases. iOS publishes the native ARM64 IPA for iOS 15+, its checksum and dependency notices. Users re-sign and provision it with their sideloading tool. Public APKs must be signed; `_unsigned.apk` files are diagnostics.

## Notices, logs and size

Run `packaging/collect_legal.py` on each build environment and distribute its
output. Include exact dependency notices, Qt license information, FFmpeg source
and build files, and the app license. Review contribution/provider permissions
before distribution; see [licensing](LICENSING.md).

Calculate checksums and update metadata **after** signing and stapling. Any later
change invalidates those hashes. Publish checksum and legal files beside the app.
Do not publish compiler logs, private credentials or diagnostic-only artifacts.

`packaging/report_sizes.py --help` explains payload reports. Nuitka's compilation
report and PyInstaller's payload inventory help find oversized dependencies.
`generate_repository.py --benchmark-compression` compares IFW archive choices;
changing compression does not remove the need to test the resulting installer.
