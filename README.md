<div align = center>
<img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/master/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="350"/>
<br>
<h1 align="center">Porn Fetch - The Ultimate Open-Source Porn(Hub) Downloader</h1>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_windows.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_windows.yml/badge.svg" alt="Build GUI Windows Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_linux.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_linux.yml/badge.svg" alt="Build GUI Linux Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_windows.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_windows.yml/badge.svg" alt="Build CLI Windows Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_linux.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_linux.yml/badge.svg" alt="Build GUI CLI Linux Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/total?style=social&logo=github&logoColor=purple">

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D21C103Z)

<br>


---

**[<kbd><strong>&nbsp;<br>&nbsp;Download (v3.5)&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.5)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Screenshots&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/SCREENSHOTS.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Supported Websites&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;FAQ&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/FAQ.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Changelog&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Development Status&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)** 

---
</div>

> [!NOTE]
> I will completely rewrite Porn Fetch in QML using Qt's `Qt Design Studio`. This will make the UI much more smooth and fully working on Android. It will be a huge
> learning curve for me and take some time, but it's absolutely worth it. Please remember, Porn Fetch is only a LEARNING project for me to learn GUI development.
> So it can often be the case that I randomly try new stuff because "i feel like it" although it might not be necessary. 

> [!WARNING]
> Porn Fetch is NOT associated with the websites. Porn Fetch is AGAINST the Terms of Services of EVERY website! Usage is on YOUR risk.

> [!IMPORTANT]
> Porn Fetch may get flagged by your antivirus software. See [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ANTIVIRUS_FLAGS.md) for an explanation why this is.

## 🚀 Quick Links
- [Features](#-features)
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
- Downloading Videos
- Downloading Playlists
- Downloading whole model / channel accounts
- Searching for videos (and downloading them directly)
- Downloading from a file
- Optional account login
- Multithreaded downloading
- Dark mode and CLI support
- No ads or mandatory logins
- Cross-platform compatibility
- Multiple supported websites
- Multiple user interface languages
- Native Android application (Not on >=v3.3)
- modern looking user interface
- Supports over 115 MB/s download speed thanks to well optimized HLS downloading
- Proxy support (Experimental)
- Native macOS support (Experimental)

## Installation
A detailed installation guide for all platforms can be found [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/INSTALLATION.md)

## General Information
> [!NOTE]
> Supported Platforms:

- Windows (10 / 11)
- Linux (X11 / Wayland)
- macoS

> [!NOTE]
> Porn Fetch is mainly developed and tested on Arch Linux with Hyprland and Gnome. 

> [!CAUTION]
> macOS is compiled on x64 AMD hardware. Apple has a translation layer, but I can't test that. If you have an Apple Silicon
> chip, and you are willing to help, please get in touch with me.


## 🌐 Supported Websites
- [PornHub.com](https://github.com/Egsagon/PHUB)
- [HQPorner.com](https://github.com/EchterAlsFake/hqporner_api)
- [xnxx.com](https://github.com/EchterAlsFake/xnxx_api)
- [Eporner.com](https://github.com/EchterAlsFake/eporner_api)
- [XVideos.com](https://github.com/EchterAlsFake/xvideos_api)
- [missav.ws](https://github.com/EchterAlsFake/missav_api)
- [xhamster.com](https://github.com/EchterAlsFake/xhamster_api)

> [!IMPORTANT] 
> Not all websites support every feature. 
> Some might only support downloading, while others support searching

### You can find more information [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)


## Batch processing
Porn Fetch allows you to use batch / automatic processing of videos, models and search queries

Here's a short documentation on how to use it:

> [!NOTE]
> This feature is currently being reworked. New changes will apply in version 3.6

Here's a quick example on how to use it. It should explain anything by itself:

```text
Inside the File:

url # The url of some video you want to download. Just in raw format, like when you would download it.
model#pornhub.com/pornstar/whatever # First enter "model#" after the # follows the model URL
search#query#website  # First enter search# then the query and then after another hashtag the website you want to search on.


Porn Fetch supports all URLs, Models and search terms like it would if you use the basic GUI for downloading.
```

> [!IMPORTANT]
> When using the search function, make sure the website is the exact same name like in the URL between www. and .com
> e., for "https://www.pornhub.com" it would be just "pornhub" or for "https://xvideos.com" it would be just "xvideos"

If you still need a real example file, [here you go](https://github.com/EchterAlsFake/Porn_Fetch/blob/eac6fa2ccf644e4b30816a7bd2fa0257b2a03e36/src/backend/urls.txt)

## 🔨 Building from Source
Easy-to-use build scripts are available for various platforms.

> [!NOTE]
> Building will be done using Python3.12 and [Nuitka](https://github.com/Nuitka/Nuitka) using Qt's `pyside6-deploy` tool.

Hardware requirements:
- ~1.5 GB of hard disk space
- ~2–3 GB of RAM
- A processor that can do some math

> Compilation takes around 5–20 minutes depending on your system and hardware.

### Linux (Ubuntu, Arch-based, Debian-based, OpenSUSE)
> [!NOTE]
> There is no official list of tested Linux distributions. I develop Porn Fetch only on Arch Linux. If you come across
> an issue, you can always report it and I will distro-hop to solve it.

```bash
wget "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install.sh" -O install.sh
bash install.sh
```

### Termux
> [!NOTE]
> You do **NOT** need a rooted Android device to compile and run Porn Fetch on Android


```bash
apt install wget -y && wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_termux.sh" | bash
```

### Windows (PowerShell as Admin)
```
# Enable script execution
Set-ExecutionPolicy RemoteSigned 
Set-ExecutionPolicy Bypass -Scope Process
Invoke-Expression (Invoke-WebRequest -Uri https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_windows.ps1 -UseBasicParsing).Content
```

### macOS
> [!NOTE]
> You need to have the Apple Developer command line tools installed. You can install them by going into your terminal
> and run `xcode-select --install`


```bash
curl "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_macos.sh" -o install.sh
bash install.sh
```

**Please Read:**
<br>The created file will be a `.app` file. You cannot usually run it as you would, because it doesn't work for some reason...
Instead, you need to go inside the `.app` package using a Terminal and run the main file in it.

You can do that with something like `./<the_app_package.app/Contents/MacOS/main`


## 📱 Android
> [!IMPORTANT]
> Building for Android is a hard and complex topic. If you need help feel free to ask me on Discord. However, I absolutely
> **DO NOT** recommend you doing that now. Please wait until things get easier in the next months...

**Make sure your host system has the following dependencies installed**
- jdk17-openjdk
- llvm
- openssl
- python3.11
- zip
- libtool
- libssl-dev
- openssl

```bash
curl "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/build_android.sh" -o build_android.sh
bash build_android.sh
```

## 🌍 Translating
Currently available in:
- German (3.0)
- English
- Chinese (3.0) `[*]` Thanks to: [Joshua-auhsoj](https://github.com/Joshua-auhsoj)
- French (3.0) `[*]` Thanks to: [Egsagon](https://github.com/Egsagon)

<br>To contribute a translation, follow [this guide](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/TRANSLATING.md).

> If a language is marked with a `*` it means, you can contribute something, and it needs an update!


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

- Paypal: `https://paypal.me/EchterAlsFake`
- Monero: `42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR`
- Ko-Fi : `https://ko-fi.com/EchterAlsFake`

Even if it's just 10 cents, for me, it matters, because I do not work yet and it means a lot
to me :)
