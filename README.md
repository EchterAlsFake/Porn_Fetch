<p align="center">
  <img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/V3.0/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="200"/>
</p>


<h1 align="center">Porn Fetch - The Ultimate Open-Source PornHub Downloader</h1>

<p align="center">
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/python-app.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/python-app.yml/badge.svg" alt="Build Status"/></a>
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/android.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/android.yml/badge.svg" alt="Android Build"/></a>
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
  <img alt="GitHub release (by tag)" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/2.9/total">

</p>

<p align="center">
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/beta-3.0"><strong>Download Version 3.0 (BETA)</strong></a> ·
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.9"><strong>Download Version 2.9</strong></a> ·
  <a href="https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md"><strong>Development Update V3.0</strong></a>
</p>

![Alt text](https://github.com/EchterAlsFake/Porn_Fetch/blob/9c634446b097f35d17fcf06e735e184ccd358c60/screenshot.png?raw=true "Optional Title")

## 🚀 Quick Links
- [Features](#-features)
- [Supported Platforms](#-supported-platforms)
- [How to Build](#-building-from-source)
- [Android Version](#-android)
- [iOS Instructions](#-ios)
- [Translation](#-translating)
- [Useful Resources](#-useful-information)
- [Legal Disclaimer](#-legal-rights)
- [Acknowledgements](#-credits)
- [License Details](#-license)

## 🌟 Features
- Direct downloads from PornHub
- Selectable video quality
- Metadata retrieval
- Full channel/user/model download capabilities
- In-app search and download features
- Optional account login
- Download history management
- Multi-threaded downloading
- Dark mode and CLI support
- No ads or mandatory logins
- Cross-platform compatibility

## 🖥️ Supported Platforms
- Windows 10, 11 (backward compatibility untested)
- Linux (X11 / Wayland)
- macOS (via source build or Python)
- Android (recommended .apk)
- iOS (via iSH)
- ARM (native Python run)

## 🌐 Supported Websites
- [PornHub.com](https://github.com/Egsagon/PHUB)
- [HQPorner.com](https://github.com/EchterAlsFake/hqporner_api)

## 🔨 Building from Source
Easy-to-use build scripts are available for various platforms. Run these in your terminal:

### For Ubuntu, Windows, Arch Linux, Termux, iSH, Fedora, OpenSUSE:
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
I am currently working very hard to convert Porn Fetch from PySide6 version 3 to Android. 
<br>I am actively on it. As long as I am working you can use the Kivy version entirely made by ChatGPT :)
<br>For the latest Kivy build, download from [here](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.9).

Note: The Android version is tested and developed on Android 13!

### Building for Android
Use [this script](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/src/scripts/build_android.sh) to build on Ubuntu 22.04.3.

## 🍏 iOS
### iSH
Run the CLI version of Porn Fetch via the 'iSH' app on iOS.

### Building for iOS
Kivy-based apps can be converted for iOS, but I need community assistance for testing and compiling. Contact me on Discord (echteralsfake | EchterAlsFake#7164) if you can help.
<br>I have no interest in developing Porn Fetch for iOS by myself. I don't have an iOS device and I won't ever have one.
## 🌍 Translating
Currently available in:
- German (3.0)
- English

To contribute a translation, follow [this guide](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/TRANSLATING.md).

## 🛠️ Useful Information
- [Roadmap](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ROADMAP.md)
- [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)
- [Development Status](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)

## ⚖️ Legal Rights
Important: Usage of Porn Fetch may not be in compliance with PornHub's terms of service. It is recommended to use a VPN for privacy.

## 👏 Credits
- API: [PHUB](https://github.com/Egsagon/PHUB)
- GUI: [Qt](https://qt.io) for Python
### See [Credits](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CREDITS.md)

## 📚 License
Licensed under [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
 
