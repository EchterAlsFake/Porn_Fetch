# DO NOT USE THIS PROJECT RIGHT NOW, WAIT UNTIL MONDAY PLEASE!!!!!!!!!!! (seriously) 


<img width="4096" height="1844" alt="IMG_20261003_222305" src="https://github.com/user-attachments/assets/17540384-d0bd-4f82-b6b5-11ebbea65edb" />

# If I don't remove this image tomorrow, you know I died because of a heart attack

Edit: 23:47 (I am still alive and going to touch some grass now cuz I am out of quota for Gemini and Codex, need to wait 2 hours) 

Edit: 2:27 I am 60% done. I go to sleep now and hopefully in ~13-15 hours this is all working again xD 

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

**The first 3.9 beta uses the real license import and validation flow with a
sandbox checkout.** Go to [pornfetch.to](https://pornfetch.to/), press
the sandbox purchase button, and import the license file you receive in the
app. **This is not a real transaction. No money is processed, and you do not
need to send cryptocurrency.** The checkout is there to test how a license
reaches the app. Please tell me if any step is confusing or fails.

### #FreeHongKong

> [!WARNING]
> Porn Fetch is NOT associated with the websites. Porn Fetch is AGAINST the Terms of Services of EVERY website! Usage is on YOUR risk.

> [!IMPORTANT]
> Porn Fetch may get flagged by your antivirus software. See [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/ANTIVIRUS_FLAGS.md) for an explanation why this is.
> If your antivirus flags a beta build, check the download source and report the
> detection before making changes to your security settings.

## 🚀 Quick Links
- [Features](#-features)
- [Installation](#installation)
- [Donations](#sponsoring--donations)
- [Supported Websites](#-supported-websites)
- [Building from Source](#-building-from-source)
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

## Installation
Standalone 3.9 CLI builds can check for signed updates with `self-update --check`
and install one with `self-update`. The desktop installers use Qt Installer
Framework instead. See the [CLI update guide](docs/CLI_UPDATES.md) for
supported builds and publishing details.

> [!IMPORTANT]
> Please read the 3.9 guide before installing a beta. It does not describe the
> older 3.8 download.

**A detailed installation guide for all platforms can be found** [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/docs/INSTALLATION.md)

## Beta license

The beta still checks licenses for these features:

- 1080+ downloads
- parallel downloads

The sandbox checkout described above provides a test license. There is no beta
price and no real purchase. In the GUI, use **Get beta test license**, then
**Import License File**. In the CLI, choose **License Management** and import
the file there. The [installation guide](docs/INSTALLATION.md) has the steps.

## General Information
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
> Older Android and iOS information is in the project history. I have not
> included mobile GUI artifacts in the current desktop build workflow.

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


## 🔨 Building from Source
The source tree targets Python 3.14 and uses `uv`. From a checkout of the
current branch:

```bash
uv sync --extra gui --group dev
uv run python scripts/patch_qtasyncio.py .venv
uv run Porn_Fetch_CLI.py
uv run main.py
```

The GUI uses the repository's QtAsyncio patch. The packaging workflow runs it
before building. For build details, start with
[FOR_DEVELOPERS.md](docs/FOR_DEVELOPERS.md) and
[the build workflow](.github/workflows/build_all.yml). A source run is useful
for development; it is not proof that a packaged beta works on your platform.


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
The beta license checkout is a sandbox and does not take payment. The donation
links below are separate and optional; they are not needed to use the beta.

However, I kindly ask every one of you to donate a small amount of money. If you have Monero (crypto)
or PayPal, you can donate me here:

- Paypal: `https://paypal.me/EchterAlsFake` (Prefered)
- Monero: `42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR`
- Ko-Fi : `https://ko-fi.com/EchterAlsFake`

Even if it's just 10 cents, for me, it matters, because I do not work yet and it means a lot
to me :)
