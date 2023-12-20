# Dev Information:

I have currently not the time to maintain this. School in Germnay is really hard in October - December.
I'll make a big update. You can expect it at late December. Thanks everyone for supporting this project!

Update:

Something negative happened in my life (my fault), and my brain is some kind of shocked. I don't know
when I'll be back. Maybe tomorrow I feel great again, or it takes a month.

# Porn Fetch - A Free & Open-Source PornHub Downloader 

![Build](https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/python-app.yml/badge.svg)
![Build](https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/android.yml/badge.svg)
### [Download Current Version 2.9](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.9)
### [Development Status V3.0](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)
## Table of Contents

- [What is Porn Fetch?](#what-is-porn-fetch)
- [Features](#features)
- [Supported Platforms](#supported-platforms)
- [Supported Websites](#supported-websites)
- [Building from Source](#building-from-source)
- [Android](#android)
- [iOS](#ios)
- [Translating](#translating)
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
- iSH (iOS / Alpine) (Enter iSH on the App Store, and you'll find it) 
- Fedora
- OpenSUSE

```
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install.sh" | bash
```
#### Termux:
```
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_termux.sh" | bash
```
#### Windows:
```
# Enable powershell script execution:

# Run Powershell ad Administrator and run the following command:
$ Set-ExecutionPolicy RemoteSigned 
$ Set-ExecutionPolicy Bypass -Scope Process
$ Invoke-Expression (Invoke-WebRequest -Uri https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_windows.ps1 -UseBasicParsing).Content

This will automatically install Python3 (if not installed) and build the project
```

# Android

#### PySide6 to Android:

I will try to compile my PySide6 application for Android. The Qt Company already works hard on making this possible.
<br>See their blog post [here](https://www.qt.io/blog/qt-for-python-6.6) It's currently still unstable and not very well explained,
but they said, they try to make it better with Qt 6.7, so I'll wait for that and see what I can do.

If I get that working I could port Porn Fetch to Android with all features (and translations) without using Kivy which would
speed up this process a lot.

#### Read carefully to prevent errors!

The development for Android has a separate branch named "android."
<br>Kivy is a whole new framework for me, so I will need my time to make it look good!

### DOWNLOAD: [0.2](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.9)

#### Supported are Android 5-13 (in theory)

If you like to build it by yourself, use [this script](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/src/scripts/build_android.sh) 

It will install all dependencies and use the buildozer.spec from my repo.
<br> YOU NEED UBUNTU 22.04.3 FOR BUILDING AND NOTHING ELSE!!!


# iOS
### iSH
You can use the CLI (Terminal version) of Porn Fetch via the App 'iSH.'
iSH is a terminal emulator for iOS that launches an Alpine Linux.
You can use the build script to automatically install everything. It's not 
the best solution, but it works at least :) 

### Building
It's possible to convert the Kivy created APP for Android easily into an iOS application, but I don't have an Apple device, so I cannot compile or even test it. You can do it by yourself, and if you think you got a successful stable build, contact me via Discord: echteralsfake | EchterAlsFake#7164, and we can merge your build into the releases!

(Your changes need to be documented in a FORK of my project. A recommendation would be a secondary iOS branch.)

# Translating

### Supported Languages:

* German (3.0)
* English

If you want to port Porn Fetch into your language, see [this Guide](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/TRANSLATING.md)
> I appreciate it a lot, and you'll be credited in further releases and in the Readme!


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
##### GUI : [Qt](https://qt.io) for Python
##### Android : Kivy, KivyMD
### External libraries:
- [colorama](https://github.com/tartley/colorama)
- [tqdm](https://github.com/tqdm/tqdm)
- [phub](https://github.com/Egsagon/PHUB)
- [sentry sdk](https://github.com/getsentry/sentry-python) Used in 1.7–2.7
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

> I consider enhancement requests also as a contribution!

- [Egsagon](https://github.com/Egsagon)
- [RSDCFGVHBJNKML](https://github.com/RSDCFGVHBJNKML) : Enhancement #11

# License:
LICENSE: [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html)
<br>Copyright (C) 2023 Johannes Habel | EchterAlsFake

