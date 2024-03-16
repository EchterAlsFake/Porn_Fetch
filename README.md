<p align="center">
  <img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/V3.0/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="600"/>
</p>


<h1 align="center">Porn Fetch - The Ultimate Open-Source Porn(Hub) Downloader</h1>

<p align="center">
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui.yml/badge.svg" alt="Build GUI Status"/></a>
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli.yml/badge.svg" alt="Build CLI Status"/></a>
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/total?style=for-the-badge&logoColor=grey&labelColor=%2300CCCC&color=purple">

</p>


## 🚀 Quick Links
- [Legal Rights](#-legal-rights)
- [Features](#-features)
- [Supported Platforms](#-supported-platforms)
- [Supported Websites](#-supported-websites)
- [Building from Source](#-building-from-source)
  - [Linux](#for-ubuntu-windows-arch-linux-termux-fedora-opensuse)
  - [Termux](#for-termux)
  - [Windows](#for-windows-powershell-as-admin)
- [Android](#-android)
- [Translating](#-translating)
- [Useful Information](#-useful-information)
- [Credits](#-credits)
- [License](#-license)
## ⚖️ Legal Rights
Warning: Porn Fetch is in fact against the ToS of every website. Usage is on your own risk!

## 🌟 Features
- Direct downloads from PornHub and other sites
- PornHub playlist downloads
- Selectable video quality
- Metadata retrieval
- Full channel/user/model download capabilities
- In-app search and download features for multiple sites
- Optional account login
- Multi-threaded downloading
- Dark mode and CLI support
- No ads or mandatory logins
- Cross-platform compatibility
- Multiple supported websites
- Multiple languages
- Native Android application
- modern looking user interface

## 🖥️ Supported Platforms
- Windows 10, 11 (backward compatibility untested)
- Linux (X11 / Wayland)
- macOS (via source build or Python)
- Android (arm64-v8a)
- ARM (native Python run)

> iOS is NOT supported. Don't even try!

## 🌐 Supported Websites
#### Important:

Not all websites support every feature. 
<br>Some might only support downloading, while others support searching

### You can see more information [HERE](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)


- [PornHub.com](https://github.com/Egsagon/PHUB)
- [HQPorner.com](https://github.com/EchterAlsFake/hqporner_api)
- [xnxx.com](https://github.com/EchterAlsFake/xnxx_api)
- [Eporner.com](https://github.com/EchterAlsFake/eporner_api)
- [XVideos.com](https://github.com/EchterAlsFake/xvideos_api)

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


## 🛠️ Useful Information
- [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)
- [Development Status](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)

## 👏 Credits
- API: [PHUB](https://github.com/EchterAlsFake/PHUB)
- GUI: [Qt](https://qt.io) for Python
### See [Credits](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CREDITS.md)

## 📚 License
Licensed under [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
<br>Copyright (C) 2023–2024 Johannes Habel 
