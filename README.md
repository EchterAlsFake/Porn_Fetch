
# Security Warning v3.8 (DO NOT USE!)
Porn Fetch v3.8 is affected by the recently discovered Brotli vulnerability. An attacker can theoretically execute code on your machine through a compromised CDN, DNS or website that Porn Fetch requests.

The attack surface is very theoretical, however it is possible. I strongly advice you to use the beta v3.8.2
instead. You can get it from https://pornfetch.to/download 

The beta is still unstable and being tested, but I would rather give you a broken app, than a working app with a backdoor!


> [!CAUTION]
> **This README describes the current 3.9 source code and the planned first beta.**
> The downloadable 3.8 release is an older GPL release. Its app, license,
> screenshots, install process, and supported platforms may be different. If
> you need information about 3.8, use the documentation from its release tag.
> I'm actively working on this rewrite. Some features and builds can still fail;
> please report problems with the commit ID or beta version you used.

<div align = center>
<img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/master/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="350"/>
<br>
<h1 align="center">Porn Fetch - Source-Available Adult Media Downloader</h1>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_all.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_all.yml/badge.svg" alt="Build Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/total?style=social&logo=github&logoColor=purple">

<br>

<a href="https://pornfetch.to/checklist">
  <img src="https://pornfetch.to/checklist/progress.svg" alt="Version 3.9 Development Progress" width="400"/>
</a>

---

**[<kbd><strong>&nbsp;<br>&nbsp;Download (v3.8)&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.8)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Screenshots&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/SCREENSHOTS.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Supported Websites&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/WEBSITES.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;FAQ&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/FAQ.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Changelog&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/CHANGELOG.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Development Status&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/STATUS.md)** 

---
</div>

# The 3.9 rewrite

This branch is where I am building the next version of Porn Fetch. It has a
PySide6 desktop app, a Qt-free CLI, and a different licensing system from 3.8.
The first beta is for finding problems, and I will keep working on them as
quickly as I can. See the [development status](docs/STATUS.md) and the
[installation guide](docs/INSTALLATION.md) before trying it.

# About the License

The 3.9 source is under the [Porn Fetch Source-Available License 1.0](LICENSE).
Earlier GPL releases keep their GPL rights. The source license and a premium
feature credential are separate things.

Automatic app updates are free for everyone on desktop, Android, and CLI, without a license.
Premium features require a signed license on the commercial policy. It covers premium features in builds released within
31,556,952 seconds (approximately one year) from first activation, with permanent premium use of those builds
on up to ten installations. First activation attempts online validation. A valid signed production license
gets up to three days from first import only for connection failures/timeouts,
never for explicit rejection, HTTP errors, malformed responses or TLS trust failures.
Reimport/restart does not reset that period. Subsequent offline use is limited to
seven days after successful validation. A rejection blocks access through later outages. Older beta credentials are rejected explicitly.

**Payment deployment is still sandboxed as of 6 October 2026; Patreon is disabled.**
Do not assume this client change enables real payments. See the
[licensing architecture and release requirements](docs/LICENSING_ARCHITECTURE.md).

### #FreeHongKong

> [!WARNING]
> Porn Fetch is NOT associated with the websites. Porn Fetch is AGAINST the Terms of Services of EVERY website! Usage is on YOUR risk.

> [!IMPORTANT]
> Porn Fetch may get flagged by your antivirus software. See [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/ANTIVIRUS_FLAGS.md) for an explanation why this is.
> If your antivirus flags a beta build, check the download source and report the
> detection before making changes to your security settings.

## 🚀 Quick Links
- [Features](#-features)
- [Installation & Building](#-installation--building-from-source)
- [Donations](#sponsoring--donations)
- [Supported Websites](#-supported-websites)
- [Developer Guide](docs/FOR_DEVELOPERS.md)
- [Qt installer work](docs/QT_INSTALLER_FRAMEWORK.md)
- [Credits](#-credits)
- [License](#-license)

## 🌟 Features
- Cross-platform
- Downloading Videos
- Downloading Playlists
- Downloading whole model / channel accounts
- Multithreaded downloading
- Automatic resuming
- Installer updates for desktop builds and signed self-updates for standalone CLI builds
- Custom template for filenames based on video metadata
- Dark mode and CLI support
- No ads or mandatory logins
- Multiple supported websites 
- modern looking user interface
- Proxy support
- Model Batch download with database updating (CLI only)
- A lot of available settings
- In-App speed limit
- Automatic file tagging (metadata)
- Automatic conversion from MPEG-TS to mp4 (within seconds)
- Build scripts for supported desktop and CLI targets
- Independent Open-Source [Server](https://github.com/EchterAlsFake/Server)
- Source-available application, made with ❤️ in 🇩🇪

## 📦 Installation & Building from Source

There are three ways to get Porn Fetch running:
1. **[Pre-built Binaries & Installers](#1-pre-built-binaries--installers)** (fastest)
2. **[One-Liner Install Scripts](#2-one-liner-install-scripts)** (automatic build)
3. **[Building from Source](#3-building--running-from-source)** (recommended for development)

> [!TIP]
> For the complete multi-platform guide with system package instructions and troubleshooting, see the [Installation & Build Guide](docs/INSTALLATION.md).

### 1. Pre-built Binaries & Installers
Grab the latest release for your platform from [GitHub Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases):

- **Qt Installer Framework (`*_Setup` installers):**
  Installs the desktop application and configures the Qt `maintenancetool` for repository-based in-app updates.
  - **Windows:** `PornFetch_windows_GUI_x64_Setup.exe`
  - **Linux:** `PornFetch_linux_GUI_x64_Setup.run` (run `chmod +x` before launching)
  - **macOS:** `PornFetch_macos_GUI_Universal_Setup.dmg`
- **Standalone Portable Bundles (`.zip` / `.dmg`):**
  Extract the ZIP to any folder. Make sure the bundled `pocketbase` (or `pocketbase.exe`) stays right next to the app binary—Porn Fetch needs it for download tracking and queue management.
- **Standalone Headless CLI:**
  Single portable binary (`PornFetch_linux_CLI_x64`, `PornFetch_windows_CLI_x64.exe`, etc.) with built-in cryptographically verified self-updating:
  ```bash
  ./PornFetch_linux_CLI_x64 self-update --check
  ./PornFetch_linux_CLI_x64 self-update
  ```

### 2. One-Liner Install Scripts
To automatically install dependencies, clone, and build the latest code on your machine:

- **Linux & macOS:**
  ```bash
  curl -sSL https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/scripts/install.sh | bash
  ```
- **Windows (PowerShell as Administrator):**
  ```powershell
  irm https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/scripts/install_windows.ps1 | iex
  ```

### 3. Building & Running from Source
The source tree targets Python 3.14 and uses [`uv`](https://docs.astral.sh/uv/) for dependency management.

```bash
# 1. Clone the repository
git clone https://github.com/EchterAlsFake/Porn_Fetch.git
cd Porn_Fetch

# 2. Sync dependencies (uv automatically provisions Python 3.14)
uv sync --extra gui --group dev

# 3. Fetch PocketBase (required for database and queue persistence)
uv run python scripts/fetch_pocketbase.py

# 4. Patch QtAsyncio (required for the GUI under Python 3.14)
uv run python scripts/patch_qtasyncio.py .venv

# 5. Launch the application!
uv run main.py              # Desktop GUI
uv run Porn_Fetch_CLI.py    # Headless CLI
```

> **Headless / Termux note:** If you only need the CLI (e.g. on headless servers or in Android Termux), you don't need any Qt dependencies or the QtAsyncio patch. Just run `uv sync` (or `pip install -e .` on Termux) and execute `uv run Porn_Fetch_CLI.py`.

### 4. Compiling Standalone Binaries from Source
To produce distributable single binaries yourself:
- **CLI binary:**
  ```bash
  uv run pyinstaller --clean packaging/pyinstaller_cli.spec
  ```
- **GUI executable:**
  ```bash
  uv run pyside6-deploy -c packaging/pysidedeploy_linux.spec    # Linux
  uv run pyside6-deploy -c packaging/pysidedeploy_windows.spec  # Windows
  # macOS: scan QML imports and generate a spec that excludes unused plugins:
  uv run --no-sync python packaging/prepare_macos_deploy.py --output /tmp/pornfetch-macos.spec
  uv run pyside6-deploy -c /tmp/pornfetch-macos.spec
  # Repair and re-sign the macOS bundle after deployment:
  uv run --no-sync python packaging/repair_macos_bundle.py "Porn Fetch.app"
  ```

## Premium license

A valid entitlement enables these features:

- 1080+ downloads
- parallel downloads

In the GUI, use **Purchase / renew license**, then paste the signed key or use
**Import License File**. In the CLI, choose **License Management** and enter the
key, JSON envelope, or file path. Only commercial-policy test credentials work
with the current client; old beta credentials are not upgraded automatically.
See the [installation guide](docs/INSTALLATION.md).

## General Information

In the **Cross-Platform Build Pipeline → Run workflow** form, choose `build_target`:
`cli`, `gui`, or `both` (the default). CLI-only runs skip GUI compilation, installers,
and the macOS universal build; GUI-only runs skip all CLI builds. Update deployment
and GitHub Release publishing follow the selected target. Tag pushes build both.
All selections still run the shared validation suite.

> [!NOTE]
> **Targets in the current build workflow.** A target in the workflow does not
> mean its first beta artifact has passed manual testing.

| Platform                   | App              | Architectures                                   |
|----------------------------|------------------|-------------------------------------------------|
| **Windows**                | GUI              | x64                                             |
| **Windows**                | CLI              | x64, ARM64                                      |
| **Linux (X11 / Wayland)**  | GUI              | x64, ARM64                                      |
| **Linux (X11 / Wayland)**  | CLI              | x64, ARM64                                      |
| **macOS**                  | GUI              | x86_64, ARM64  (Universal build)                |
| **Android**                | CLI from source  | Termux; no beta APK in the desktop build workflow |

Linux 32-bit (x32 artifact) and riscv64 CLI builds are available as experimental workflow-dispatch targets. They use native target toolchains and must pass a CI build and smoke test before their artifacts are published. Linux s390x and ppc64le CLI builds are paused because `curl-cffi` does not support those architectures. Windows ARM64 GUI and Windows x86 CLI builds are paused after build and runtime failures in pipeline #43.

> [!NOTE]
> Porn Fetch is mainly developed and tested on Arch Linux with Hyprland and Gnome. 

> [!NOTE]
> The [experimental iOS port](docs/iOS.md) has been verified on a jailbroken
> iPhone 7, including downloads and automatic MP4 remuxing. See its
> [build instructions](docs/ios/BUILDING.md). Mobile GUI artifacts are not
> included in the current desktop build workflow.

## 🌐 Supported Websites
- [PornHub.com](https://github.com/Egsagon/PHUB)
- [xnxx.com](https://github.com/EchterAlsFake/xnxx_api)
- [Eporner.com](https://github.com/EchterAlsFake/eporner_api)
- [XVideos.com](https://github.com/EchterAlsFake/xvideos_api)
- [xhamster.com](https://github.com/EchterAlsFake/xhamster_api)
- [spankbang.com](https://spankbang.com)
- [youporn.com](https://youporn.com)
- [beeg.com](https://github.com/echteralsfake/beeg_api)
- [porntrex.com](https://github.com/echteralsfake/porntrex_api)
- [xfreehd.com](https://github.com/echteralsfake/xfreehd_api)
- [redtube.com](https://redtube.com)
- [thumbzilla.com](https://thumbzilla.com)
- [tube8.com](https://tube8.com)

> [!IMPORTANT] 
> Not all websites support every feature. 
> Some providers support only direct videos while others also support profiles or collections. Search is intentionally not available.

### You can find more information [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/WEBSITES.md)

### For Developers
If you want to develop on Porn Fetch and do local changes, contribute code or do whatever, please
have a look at the internal code documentation which explains the core structure of the project,
as well as the different concepts used here.

See: https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/FOR_DEVELOPERS.md



## 🌍 Translating

> [!CAUTION]
> Translations are still being brought up to date for 3.9. Please check with me
> before starting a large translation update.

Currently available in:
- German (3.0)
- English
- Chinese (3.0) `[*]` Thanks to: [Joshua-auhsoj](https://github.com/Joshua-auhsoj)
- French (3.0) `[*]` Thanks to: [Egsagon](https://github.com/Egsagon)
- Italian (3.8) Thanks to: [FatalPuppet](https://github.com/FatalPuppet)

<br>To contribute a translation, follow [this guide](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/TRANSLATING.md).

> If a language is marked with a `*` it means, you can contribute something, and it needs an update!


## 👏 Credits
- API: [PHUB](https://github.com/EchterAlsFake/PHUB)
- GUI: [Qt](https://qt.io) for Python
- Media processing: [PyAV / FFmpeg](https://pyav.org/) (license depends on the bundled FFmpeg build; see third-party notices)

### See [Credits](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/CREDITS.md) and [third-party notices](THIRD_PARTY_NOTICES.md)

## 📚 License
Current development snapshots marked with the [Porn Fetch Source-Available License 1.0](LICENSE) use that license for application-owned material. Earlier GPL-3.0-or-later copies retain their GPL rights; the historical license text is in [LICENSES](LICENSES/GPL-3.0-or-later.txt). Third-party components retain their own terms. See the [licensing guide](docs/LICENSING.md).
<br>Copyright (C) 2023–2026 Johannes Habel 

# Sponsoring / Donations
The payment deployment remains in sandbox mode as of 6 October 2026. The donation
links below are separate and optional; they are not needed to use the beta.

However, I kindly ask every one of you to donate a small amount of money. If you have Monero (crypto)
or PayPal, you can donate me here:

- Paypal: `https://paypal.me/EchterAlsFake` (Prefered)
- Monero: `42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR`
- Ko-Fi : `https://ko-fi.com/EchterAlsFake`

Even if it's just 10 cents, for me, it matters, because I do not work yet and it means a lot
to me :)
