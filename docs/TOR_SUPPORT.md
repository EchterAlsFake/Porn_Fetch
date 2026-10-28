# Managed Tor routing

The GUI, CLI and Android app can route Porn Fetch service requests through:
`http://pornfetchc5ct7s7uiervf4ziymmus5gy33gyqc6vkdtqyr5pbxrxmid.onion`.

## Behavior

Privacy settings offer three Tor routes, with Off as the default:

- **Updates + licensing only**: service requests use the Porn Fetch onion service.
  Media and provider requests keep their existing network settings.
- **All app traffic (including downloads)**: service requests still use the onion
  service; provider pages, account requests, playlists, HLS segments and raw MP4
  downloads use Tor exits. Error reports and PocketBase installation downloads
  also use Tor. Loopback PocketBase communication stays local. External browser
  links and other applications are outside this app's routing.
- **Off**: the usual service and media network settings apply.

Selecting All app traffic requires acknowledging the notice reserving Tor video
downloads for people in censored countries where consuming pornography is illegal
and can lead to jail time or other punishments. It explains the bandwidth cost
to other Tor users and discourages unnecessary downloads. Cancelling preserves
the previous route. Finish active work before changing the routing selector.

An app-owned Tor client starts when a routed request needs it. The bootstrap
limit is 180 seconds and progress appears in the GUI. A failed Tor connection
stops the request; there is no direct fallback. All app traffic takes precedence
over the custom media proxy, SNI proxy, interface binding, environment proxies
and bypass lists. It uses SOCKS5 remote hostname resolution, disables DoH/ECH
lookups and forces HTTP/2 over TCP to avoid DNS or QUIC bypasses. Certificates
remain verified. The stored custom networking settings are restored when leaving
All app traffic.

The GUI migrates the old settings using `enable_tor && enable_tor_server_routing`.
The CLI has `service_transport` set to `direct`, `tor` (services only) or
`tor_all` (all app traffic) in its settings menu, with the same notice.
Explicit service transports ignore environment proxy settings, use remote SOCKS
hostname resolution and refuse redirects. HTTP is allowed only for the exact
configured onion service while Tor mode is enabled; ordinary service requests
continue to require HTTPS. TLS validation is never disabled globally.

The Tor process has loopback-only SOCKS/control ports, cookie-authenticated
control access, a private persistent data directory and no relay role. It stops
when Tor is disabled in the GUI or the app exits. Android operation follows the
app's lifetime; this is not a system VPN or an always-on background service.
Tor hides the client's network address from the service. License keys and
installation IDs are randomly generated values containing no personal
information; they do not identify a user as a person. Existing offline
license permits, machine limits, signed certificates and premium version entitlement
rules are unchanged. Automatic app updates are free and do not require licensing requests.

Failures on this service route open the same notification on desktop and Android,
including initial/background license and update checks. The notice distinguishes
Tor startup failures, an unreachable Porn Fetch onion service, and temporary
server errors; it does not claim that a server error means Tor itself is broken.
Users can keep Tor enabled or explicitly turn it off,
then retry. Repeated identical notices are grouped for 60 seconds. The CLI keeps
the Tor explanation in update errors and licensing outage status. Video-provider
errors stay with the existing download/provider UI and never trigger this service
notification. Turning Tor off restores the stored media proxy settings.

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
and APK hash. The app downloads and verifies the APK without a license check,
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
cancellation. A local SOCKS fixture checks remote hostname resolution for provider
requests, HLS segments and raw MP4 streams without public network traffic. GUI
checks cover routing selection and accepting/cancelling the all-traffic notice.
GUI smoke tests cover both desktop and Android QML layouts. A real
Android APK build and device/emulator installation are still needed to validate
the native runtime and package-manager interaction for each ABI. Linux ARM64
compilation and platform code signing still need validation in their build jobs.
