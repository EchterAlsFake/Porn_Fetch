<div align = center>
<img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/V3.0/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="350"/>
<br>
<h1 align="center">Porn Fetch - The Ultimate Open-Source Porn(Hub) Downloader</h1>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_all.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_all.yml/badge.svg" alt="Build GUI Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/total?style=social&logo=github&logoColor=purple">
<br>

---

**[<kbd><strong>&nbsp;<br>&nbsp;Download (v3.2)&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.2)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Screenshots&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/SCREENSHOTS.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Supported Websites&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;FAQ&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/FAQ.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Changelog&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Development Status&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)** 

---
</div>

> [!WARNING]
> Porn Fetch is NOT associated with the websites. Porn Fetch is AGAINST the Terms of Services of EVERY website! Usage is on YOUR risk.

> [!IMPORTANT]
> I need someone to help me with testing on macOS. I will highly appreciate any help. Please contact me on Discord: echteralsfake

## 🚀 Quick Links
- [Features](#-features)
- [Supported Platforms](#-supported-platforms)
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
- Metadata retrieval
- Optional account login
- Multi-threaded downloading
- Dark mode and CLI support
- No ads or mandatory logins
- Cross-platform compatibility
- Multiple supported websites
- Multiple user interface languages
- Native Android application
- modern looking user interface

## General Information
> [!NOTE]
> Supported Platforms:

- Windows (10 / 11)
- Linux   (X11 / Wayland)
- Android (aarch64)
- macOS   (Untested)

The Graphical User Interface is only for 64bit systems. The CLI supports 64 and 32bit systems.
<br>Porn Fetch is developed on Arch Linux (Hyprland) and cross-compiled using GitHub CI/CD

> Downloading on Windows is generally slower, because Windows doesn't have a good I/O network handling


## 🌐 Supported Websites
- [PornHub.com](https://github.com/Egsagon/PHUB)
- [HQPorner.com](https://github.com/EchterAlsFake/hqporner_api)
- [xnxx.com](https://github.com/EchterAlsFake/xnxx_api)
- [Eporner.com](https://github.com/EchterAlsFake/eporner_api)
- [XVideos.com](https://github.com/EchterAlsFake/xvideos_api)

> [!IMPORTANT] 
> Not all websites support every feature. 
> Some might only support downloading, while others support searching

### You can see more information [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)


## 🔨 Building from Source
Easy-to-use build scripts are available for various platforms. Run these in your terminal:

### For Ubuntu, Windows, Arch Linux, Termux, Fedora, OpenSUSE:
```bash
wget "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install.sh" -O install.sh
bash install.sh
```
### For Termux:
```bash
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_termux.sh" | bash
```
### For Windows (Powershell as Admin)
```
# Enable script execution
Set-ExecutionPolicy RemoteSigned 
Set-ExecutionPolicy Bypass -Scope Process
Invoke-Expression (Invoke-WebRequest -Uri https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_windows.ps1 -UseBasicParsing).Content
```

> Scripts aren't maintained very often. Please report errors immediately!

## 📱 Android
The Android app is the exact same as the desktop app. Thanks to Qt's Android developing Guide, you'll be able to simply
install the .apk file, and you have the full version of Porn Fetch on your device.

### Building for Android
Building the PySide6 application by yourself isn't possible through a simple script. If you really want
to do it, please refer to my [Pyside6-to-Android](https://github.com/EchterAlsFake/PySide6-to-Android) repository.

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
<br>Copyright (C) 2023–2024 Johannes Habel 

Porn Fetch uses [FFmpeg](https://ffmpeg.org/), which is licensed under the GPL license