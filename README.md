> [!WARNING] 
> I currently investigate an issue where Porn Fetch executables are flagged as a virus on VirusTotal (36+ vendors).
> I of course have NOT modified the executables and I will be absolutely transparent to ANYONE in the build process. 
> <br>
> <br>
> Please see this issue for updates: [Porn Fetch trojan report](https://github.com/EchterAlsFake/Porn_Fetch/issues/40)

> [!IMPORTANT]
> DO NOT DOWNLOAD PORN FETCH UNTIL THIS ISSUE HAS BEEN RESOLVED!


> [!NOTE] 
> My account didn't get hacked and I always used code signing (in most of the cases). I am pretty sure there haven't been
> any modifications by a third party, but I will do anything to find out what did go wrong.



If you want to use Porn Fetch now, please ONLY use it from the source code but NOT from the releases.


Thank you all, I'll let you know when it's fixed. For updates, please refer to the issue mentioned above. Thanks.





<div align = center>
<img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/V3.0/src/frontend/graphics/logo_transparent.png" alt="Porn Fetch Logo" width="350"/>
<br>
<h1 align="center">Porn Fetch - The Ultimate Open-Source Porn(Hub) Downloader</h1>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_windows.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_windows.yml/badge.svg" alt="Build GUI Windows Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_linux.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_linux.yml/badge.svg" alt="Build GUI Linux Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_macos.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_gui_macos.yml/badge.svg" alt="Build GUI MacOS Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_windows.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_windows.yml/badge.svg" alt="Build CLI Windows Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_linux.yml"><img src="https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/build_cli_linux.yml/badge.svg" alt="Build GUI CLI Linux Status"/></a>
<a href="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL"><img src="https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg" alt="CodeQL Analysis"/></a>
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/EchterAlsFake/Porn_Fetch/total?style=social&logo=github&logoColor=purple">
<br>

2 parents 684a0ae + 6399217
commit b34f733

---

**[<kbd><strong>&nbsp;<br>&nbsp;Download (v3.3)&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/3.3)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Screenshots&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/SCREENSHOTS.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Supported Websites&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/WEBSITES.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;FAQ&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/FAQ.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Changelog&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)** 
**[<kbd><strong>&nbsp;<br>&nbsp;Development Status&nbsp;<br>&nbsp;</strong></kbd>](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)** 

---
</div>

> [!NOTE]
> I am not active on GitHub for the next weeks. Errors won't be fixed now, but later, when I feel better.

> [!WARNING]
> Porn Fetch is NOT associated with the websites. Porn Fetch is AGAINST the Terms of Services of EVERY website! Usage is on YOUR risk.

> [!IMPORTANT]
> I need someone to help me with testing on macOS. I will highly appreciate any help. Please contact me on Discord: echteralsfake

## 🚀 Quick Links
- [Features](#-features)
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
- Native Android application
- modern looking user interface

## General Information
> [!NOTE]
> Supported Platforms:

- Windows (10 / 11)
- Linux   (X11 / Wayland)
- Android
- macOS (Untested)

The Graphical User Interface is only for 64bit systems. The CLI supports 64 and 32bit systems.
<br>Porn Fetch is developed on Arch Linux (Hyprland) and cross-compiled using GitHub CI/CD

> Downloading on Windows is generally slower because Windows doesn't have a good I/O network handling


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


## Working with Files
Porn Fetch allows you to use a URL or kind of batch file to programmatically download all videos, models, and search
terms listed in there.

Here's a short documentation on how to use it:

> [!NOTE]
> The format ending of the file doesn't matter.

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