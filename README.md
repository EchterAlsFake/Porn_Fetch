<div align = center>
<img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/master/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="350"/>
<br>
<h1 align="center">Porn Fetch - The Ultimate Open-Source Porn(Hub) Downloader</h1>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_all.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_all.yml/badge.svg" alt="Build Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/total?style=social&logo=github&logoColor=purple">

<br>


---

**[<kbd><strong>&nbsp;<br>&nbsp;Download (v3.7)&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.7)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Screenshots&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/SCREENSHOTS.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Supported Websites&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;FAQ&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/FAQ.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Changelog&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Development Status&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)** 

---
</div>

### #FreeHongKong

> [!WARNING]
> Porn Fetch is NOT associated with the websites. Porn Fetch is AGAINST the Terms of Services of EVERY website! Usage is on YOUR risk.

> [!IMPORTANT]
> Porn Fetch may get flagged by your antivirus software. See [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ANTIVIRUS_FLAGS.md) for an explanation why this is.
> For downloading and running Porn Fetch you NEED to disable Real-Time protection in Windows defender!


## 🚀 Quick Links
- [Features](#-features)
- [Installation](#installation)
- [Donations](#sponsoring--donations)
- [Supported Websites](#-supported-websites)
- [Building from Source](#-building-from-source)
  - [Linux](#for-ubuntu-windows-arch-linux-termux-fedora-opensuse)
  - [Termux](#for-termux)
  - [Windows](#for-windows-powershell-as-admin)
- [Android](#-android)
- [Translating](#-translating)
- [Credits](#-credits)
- [License](#-license)

## 🌟 Features
- Cross-platform
- Downloading Videos
- Downloading Playlists
- Downloading whole model / channel accounts
- Searching for videos (and downloading them directly)
- Multithreaded downloading
- Dark mode and CLI support
- No ads or mandatory logins
- Multiple supported websites 
- modern looking user interface
- Supports over 115 MB/s download speed thanks to well optimized HLS downloading
- Proxy support
- Model Batch download with database updating (CLI only)
- A lot of available settings
- In-App speed limit
- Installation AND portable mode selectable
- Automatic file tagging (metadata)
- Automatic conversion from MPEG-TS to mp4 (within seconds)
- 100% Open-Source, made with ❤️ in 🇩🇪

## Installation
> [!IMPORTANT]
> If you aren't tech savy, please read through this guide.

**A detailed installation guide for all platforms can be found** [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/INSTALLATION.md)

## General Information
> [!NOTE]
> **Supported platforms & architectures (based on current release files)**

| Platform                      | App              | Architectures                                   |
|-------------------------------|------------------|-------------------------------------------------|
| **Windows**                   | GUI              | x64, ARM                                        |
| **Windows**                   | CLI              | x64, x86 (x32)                                  |
| **Linux (X11 / Wayland)**     | GUI              | x64                                             |
| **Linux (X11 / Wayland)**     | CLI              | x64, x86 (x32)*                                 |
| **macOS**                     | GUI              | x86_64 (Intel)†                                 |
| **Android**                   | CLI (via Termux) | All                                             |
| **iOS** **(IN DEVELOPMENT!)** | CLI              | iOS 15.8+, rootless<br>Jailbroken with palera1n |


† Intel build; runs on Apple Silicon (M1/M2/M3) via Rosetta 2.

> [!NOTE]
> Porn Fetch is mainly developed and tested on Arch Linux with Hyprland and Gnome. 

## 🌐 Supported Websites
- [PornHub.com](https://github.com/Egsagon/PHUB)
- [HQPorner.com](https://github.com/EchterAlsFake/hqporner_api)
- [xnxx.com](https://github.com/EchterAlsFake/xnxx_api)
- [Eporner.com](https://github.com/EchterAlsFake/eporner_api)
- [XVideos.com](https://github.com/EchterAlsFake/xvideos_api)
- [missav.ws](https://github.com/EchterAlsFake/missav_api)
- [xhamster.com](https://github.com/EchterAlsFake/xhamster_api)
- [spankbang.com](https://spankbang.com)
- [youporn.com](https://youporn.com)

> [!IMPORTANT] 
> Not all websites support every feature. 
> Some might only support downloading, while others support searching

### You can find more information [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)

### For Developers
If you want to develop on Porn Fetch and do local changes, contribute code or do whatever, please
have a look at the internal code documentation which explains the core structure of the project,
as well as the different concepts used here.

See: https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/FOR_DEVELOPERS.md



## 🔨 Building from Source
Building will be done through a fully automated script, that lets you select the version / commit to 
build from and will install all dependencies automatically for you, including Python.

> [!NOTE]
> Building will be done using Python3.13.11 and [Nuitka](https://github.com/Nuitka/Nuitka) using Qt's `pyside6-deploy` tool.

Hardware requirements:
- ~3-5 GB of disk space (for macOS more like 10 GB) 
- ~2–3 GB of RAM
- A processor that can do some math

> Compilation takes around 20-60 minutes depending on your system and hardware.

### Linux / macOS
> [!NOTE]
> There is no official list of tested Linux distributions. I develop Porn Fetch only on Arch Linux. If you come across
> an issue, you can always report it and I will distro-hop to solve it.

> [!IMPORTANT]
> If using macOS, you need to install XCode developer tools and Homebrew.

```bash
curl "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install.sh" -o install.sh
bash install.sh
```

### Termux
> [!NOTE]
> You do **NOT** need a rooted Android device to compile and run Porn Fetch on Android

```bash
apt install wget -y && wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_termux.sh" | bash
```

### Windows (PowerShell as Admin)
> [!CAUTION]
> You absolutely **NEED** to disable Microsoft Defender (Realtime protection). Otherwise, Windows will just randomly delete
> files during build which makes it completely impossible to do anything.

You can read through the full rage letter [here](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/why_windows_sucks.md)

```
# Enable script execution
Set-ExecutionPolicy RemoteSigned 
Set-ExecutionPolicy Bypass -Scope Process
Invoke-Expression (Invoke-WebRequest -Uri https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_windows.ps1 -UseBasicParsing).Content
```


## 🌍 Translating

> [!CAUTION]
> Translating is currently broken and I need to find a different method and completely refactor this. DO NOT translate anything, everything is outdated and you will waste your time!

Currently available in:
- German (3.0)
- English
- Chinese (3.0) `[*]` Thanks to: [Joshua-auhsoj](https://github.com/Joshua-auhsoj)
- French (3.0) `[*]` Thanks to: [Egsagon](https://github.com/Egsagon)
- Italian (3.8) Thanks to: [FatalPuppet](https://github.com/FatalPuppet)

<br>To contribute a translation, follow [this guide](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/TRANSLATING.md).

> If a language is marked with a `*` it means, you can contribute something, and it needs an update!

If you are familiar with Crowdin, you can just use that for translating, here's the project link:
<br> -> https://crowdin.com/project/pornfetch


## 👏 Credits
- API: [PHUB](https://github.com/EchterAlsFake/PHUB)
- GUI: [Qt](https://qt.io) for Python
- FFmpeg: [FFmpeg](https://ffmpeg.org/) GPL

### See [Credits](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CREDITS.md)

## 📚 License
Licensed under [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
<br>Copyright (C) 2023–2025 Johannes Habel 

Porn Fetch uses [FFmpeg](https://ffmpeg.org/), which is licensed under the GPL license

# Sponsoring / Donations
Porn Fetch is developed entirely Open-Source and will always be free, because I like what
I am doing here. I will never ever charge money for this software.

However, I kindly ask every one of you to donate a small amount of money. If you have Monero (crypto)
or PayPal, you can donate me here:

- Paypal: `https://paypal.me/EchterAlsFake` (Prefered)
- Monero: `42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR`
- Ko-Fi : `https://ko-fi.com/EchterAlsFake`

Even if it's just 10 cents, for me, it matters, because I do not work yet and it means a lot
to me :)
