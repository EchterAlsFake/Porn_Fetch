# Managed Tor for updates and licensing

The GUI, CLI and Android app can route Porn Fetch service requests through:
`http://pornfetchc5ct7s7uiervf4ziymmus5gy33gyqc6vkdtqyr5pbxrxmid.onion`.

## Behavior

“Use Tor for updates and licensing” is off by default. Enabling it starts an
app-owned Tor client when a service request needs it. The bootstrap limit is
180 seconds and progress appears in the GUI. A failed Tor connection stops the
request; the client never falls back to a direct connection. Media traffic,
website credentials, custom media proxies and SNI settings use their existing
separate configuration.

The GUI migrates the old settings using `enable_tor && enable_tor_server_routing`.
The CLI has `service_transport` set to `direct` or `tor` in its settings menu.
Explicit service transports ignore environment proxy settings, use remote SOCKS
hostname resolution and refuse redirects. HTTP is allowed only for the exact
configured onion service while Tor mode is enabled; ordinary service requests
continue to require HTTPS. TLS validation is never disabled globally.

The Tor process has loopback-only SOCKS/control ports, cookie-authenticated
control access, a private persistent data directory and no relay role. It stops
when Tor is disabled in the GUI or the app exits. Android operation follows the
app's lifetime; this is not a system VPN or an always-on background service.
Tor hides the client's network address from the service, but the license and
installation identity continue to identify its entitlement. Existing offline
license permits, machine limits, signed certificates and update entitlement
rules are unchanged.

Failures on this service route open the same notification on desktop and Android,
including initial/background license and update checks. The notice distinguishes
Tor startup failures, an unreachable Porn Fetch onion service, and temporary
server errors; it does not claim that a server error means Tor itself is broken.
Users can keep Tor enabled or explicitly turn it off for updates and licensing,
then retry. Repeated identical notices are grouped for 60 seconds. The CLI keeps
the Tor explanation in update errors and licensing outage status. Video-provider
errors stay with the existing download/provider UI and never trigger this service
notification. Disabling service Tor does not change media proxy settings.

## Runtime packaging

`packaging/tor_sources.json` pins Tor Expert Bundle 15.0.26, Tor 0.4.9.14 and
archive hashes. The checksum manifest was verified against Tor Browser Developers
key `EF6E286DDA85EA2A4BA7DE684E2C6E8793298290` before pinning. When updating it,
verify the new signed upstream manifest and archive digests before committing.

`packaging/fetch_tor.py` prepares the runtime, dependency notices and provenance:

- Official bundles for Linux x64, Windows x64, macOS Intel/ARM64, and all four
  Android ABIs.
- Windows ARM64 uses the official x86 executable through OS emulation.
- Linux ARM64 builds the pinned official Tor source against static libevent,
  OpenSSL and zlib from the runner's development packages.
- Experimental desktop architectures and jailbroken iOS CLI have no bundled
  runtime in this phase. Selecting Tor without a runtime gives an error.

Desktop GUI and CLI builds include the executable and its private libraries.
Android installs `libTor.so` in the APK's native-library directory, with native
extraction enabled. It is not downloaded or executed from writable app storage.
Pluggable transports and bridge configuration are not included in this version.

Source runs can set `PORNFETCH_TOR_BINARY` to an installed Tor executable. Porn
Fetch still starts its own client process and data directory. Packaged builds use
their bundled runtime. Two processes sharing one Tor data directory can conflict;
the resulting startup failure never triggers a direct fallback.

## Updates and Android installation

Desktop installer updates retain signature verification and stream verified
repository files to local staging before launching the Qt Maintenance Tool.
Portable GUI installations retain their existing manual-install behavior.
Standalone CLI updates use TUF with the selected service transport.

Android uses a separate TUF feed at `/repo/android/`, with the existing update
trust root. Target metadata binds the ABI, package, version, release timestamp
and APK hash. The app checks update entitlement, downloads and verifies the APK,
then asks Android to open its installer using a read-only content URI.

The native bridge checks the package, newer version code, architecture and the
same signing identity as the installed app. If needed, Android asks the user to
allow installation from Porn Fetch; select Install update again afterwards.
Android then asks for installation confirmation. Cancelling, failing verification
or interrupting the download preserves the current installation. No silent APK
installation is attempted.

The website publisher signs Android metadata using `CLI_UPDATE_SIGNING_KEY`
after uploading signed APKs. The three-day metadata refresh workflow maintains
the feed between releases. See `ANDROID_CI.md` for APK signing secrets and the
server's `docs/TOR_SUPPORT.md` for gateway/storage deployment.

## Checks

The offline unit suite checks route selection, no-direct-fallback behavior,
runtime lifecycle, signed metadata, payload verification, installer handoff and
cancellation. GUI smoke tests cover both desktop and Android QML layouts. A real
Android APK build and device/emulator installation are still needed to validate
the native runtime and package-manager interaction for each ABI. Linux ARM64
compilation and platform code signing still need validation in their build jobs.
