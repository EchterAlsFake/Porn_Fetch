# Porn Fetch - A Free & Open-Source PornHub Downloader 

![Build](https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/python-app.yml/badge.svg)
### [Download Current Version 2.7](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.7)
### [Development Status V2.8](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)
## Table of Contents

- [What is Porn Fetch?](#what-is-porn-fetch)
- [Features](#features)
- [Supported Platforms](#supported-platforms)
- [Supported Websites](#supported-websites)
- [Building from Source](#building-from-source)
- [Android](#android)
- [iOS](#ios)
- [Useful Information](#useful-information)
- [Legal Rights](#legal-rights)
- [Credits](#credits)
- [License](#license)

## What is Porn Fetch?

Porn Fetch allows users to download, search, and interact with videos from PornHub, aiming to provide a free and open-source downloader for everyone. 

#### Avoid shady websites or paid software in 2023.

## Features:

- Downloading directly from PornHub
- Selectable quality for downloads
- Fetching metadata from videos / Users
- Downloading all videos from a whole Channel / User / Model account
- In-app video search and download
- Account login
- Fetch all liked, watched, and recommended videos for your account
- Threaded downloads
- Native dark mode
- CLI for systems without a graphical user interface
- No ads & restrictions
- No mandatory login / PornHub account
- Cross-platform compatibility


## Supported Platforms

- Windows: 10, 11 (lower versions may be compatible)
- Linux: X11 / Wayland - X64 (Testing on Hyprland - Wayland)
- macOS: Requires building from source or native run with Python
- Android: Native run with an .apk recommended; CLI available in Termux
- iOS: Can be run with iSH ([See Building from Source](#building-from-source))
- ARM devices: Native run with Python required

## Supported Websites

- PornHub.com [PHUB](https://github.com/Egsagon/PHUB)
- HQPorner.com (Supported Since v2.8) [hqporner_api](https://github.com/EchterAlsFake/hqporner_api)

## Building from Source

Automatic build script is available. Run the following in your terminal and select your system.

### Supported Platforms:

- Ubuntu
- Windows 10 / 11
- Arch Linux
- Termux
- iSH (iOS / Alpine)  (Enter iSH on the App Store, and you'll find it) 
- Fedora
- OpenSUSE

```
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/install.sh" | bash
```
#### Termux:
```
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/install_termux.sh" | bash
```
#### Windows:
```
# Enable powershell script execution:

# Run Powershell ad Administrator and run the following command:
$ Set-ExecutionPolicy RemoteSigned 
$ Set-ExecutionPolicy Bypass -Scope Process
$ Invoke-Expression (Invoke-WebRequest -Uri https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/install_windows.ps1 -UseBasicParsing).Content

This will automatically install Python3 (if not installed) and build the project
```

# Android

#### Read carefully to prevent errors!

The development for Android has a separate branch named "android".
<br>Kivy is a whole new framework for me, so I will need my time to make it look good!

### DOWNLOAD: [0.1](https://github.com/EchterAlsFake/Porn_Fetch/releases)

Minimum needed API: 21

**Requirements:**
- Internet, Read and write to External storage (your internal /emulated/0/ drive)

**Error reporting:**
- You can report errors, but please include your Android version, a detailed description of what you did and if your device is rooted, because if it is, we can get additional logs :)

**Manual Building:**
- A guide/script is in development

# iOS

It's possible to convert the Kivy created APP for Android easily into an iOS application, but I don't have an Apple device, so I cannot compile or even test it. You can do it by yourself and if you think you got a successful stable build, contact me via Discord: echteralsfake | EchterAlsFake#7164 and we can merge your build into the releases!

(Your changes need to be documented in a FORK of my project. A recommendation would be a secondary iOS branch.)

## Useful Information
- [Roadmap](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ROADMAP.md)
- [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)
- [Development Status](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)
# Legal Rights

> ! PornHub PROHIBITS downloading videos for unregistered users. <br>
> ! PornHub PROHIBITS scraping content on their website or usage of any automation tools in general

So what do we learn from this? This tool is probably NOT permitted by PornHub.
I am just the developer. Nobody will get you in jail because you downloaded a video from PornHub, but consider using a VPN to be safe.

# Credits

##### Project API : [PHUB](https://github.com/Egsagon/PHUB)
##### GUI : PySide6 - [Qt](https://qt.io) for Python
##### Android : Kivy, KivyMD
### External libraries:
- [colorama](https://github.com/tartley/colorama)
- [tqdm](https://github.com/tqdm/tqdm)
- [phub](https://github.com/Egsagon/PHUB)
- [sentry sdk](https://github.com/getsentry/sentry-python) Used in 1.7 - 2.7
- [requests](https://github.com/psf/requests)
- [hqporner_api](https://github.com/EchterAlsFake/hqporner_api)
- [pyside6](https://wiki.qt.io/Qt_for_Python)
- wget

### Android Specific:
- Kivy MD
- Kivy
- Buildozer
- Cython

### Graphics:
- [Download Icon](https://icons8.com/icon/104149/herunterladen) *
- [Search Icon](https://icons8.com/icon/aROEUCBo74Il/suche) *
- [Settings Icon](https://icons8.com/icon/52146/einstellungen) *
- [C Icon](https://icons8.com/icon/Uehg4gyVyrUo/copyright) * 
- [M Icon](https://iconscout.com/icons/medium) By [Unicons Font](https://iconscout.com/contributors/unicons) on [Icon Scout](https://iconscout.com) *
- [Checkmark](https://www.iconsdb.com/barbie-pink-icons/checkmark-icon.html)
- [Download Icon v2](https://iconscout.com/free-icon/download-1754130) by [Kmg Design](https://iconscout.com/contributors/kmgdesignid) on [Icon Scout](https://iconscout.com)
- [Settings Icon v2](https://iconscout.com/free-icon/settings-2856913) by [Haca Studio](https://iconscout.com/contributors/boosticon) on [Icon Scout](https://iconscout.com)
- [Account Icon](https://iconscout.com/free-icon/account-6495099) by [Alex Martynov](https://iconscout.com/contributors/rengised) on [Icon Scout](https://iconscout.com)

*Only used in older versions.

## Contributors:
- [Egsagon](https://github.com/Egsagon)

# License:
LICENSE: [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html)
<br>Copyright (C) 2023 Johannes Habel | EchterAlsFake

