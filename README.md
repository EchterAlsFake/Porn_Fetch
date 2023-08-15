# Porn Fetch - A PornHub Downloader 4 Free & Everyone

![Build](https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/python-app.yml/badge.svg)

# Table of Contents

- [What is Porn Fetch?](#what-is-porn-fetch)<br>
- [Features](#features)
- [Installation](#installation)
- [Data collection and Privacy](#data-collection--privacy)
- [Supported platforms](#supported-platforms)
- [Building from source](#building-from-source)
- [Useful information](#useful-information)
- [Legal rights](#legal-rights)
- [Credits](#credits)
- [License](#license)

# What is Porn Fetch?

Porn Fetch is a program that can download, search and interact with videos from PornHub.<br>
The goal is to create a free and open-source downloader for everyone. <br>
#### There's no need to use shady websites or paid software in 2023.

# Features:

* Downloading directly from PornHub itself
* Downloading with selectable quality
* Fetching metadata from Videos
* Downloading multiple videos at once
* Downloading all videos from a whole Channel / User / Model account
* Search for videos and download them directly in the application
* You can log in with your Account (You don't need to!)
* Fetch all videos you've liked
* Fetch all videos you've ever watched
* Fetch recommended videos for your account
* Threaded downloads
* Native dark mode
* CLI for systems without a graphical user interface
* No ADs & restrictions
* No login / PornHub account needed
* No data tracking (See Data Collection / Privacy)
* Open-Source
* Cross-platform
* Actively maintained

# Installation

 
### * Files can be downloaded from [GitHub releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)
### * Source code can be found in the [GitHub releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)
##### * A backup download is available [here](https://drive.google.com/drive/folders/1sGvhAO_qQB87AOfyVDWPJZluVettBwaj?usp=drive_link)

# Data Collection / Privacy

- No data collection by default!

If you enable the option to allow Sentry to collect errors, then the following is collected

- Error messages (The full Python traceback)
- Variables and the values in it
- The lines of code, in which the error happened
- Your PC name (although I don't care about it, and I don't need it.)

> Sentry will NOT collect any user-specific information or system information!

Note: When using the Account login function, Sentry could eventually include your username <br>
and password in the error message.<br>
To prevent this, Sentry won't report any errors related to the Account function.
<br>If you get an error there, please report it using the "Issues" Tab from GitHub

# Supported Platforms

* Windows : Windows 7, 8, 8.1, 9, 10, 11
* Linux: X11 / Wayland - X64 (I am testing on Hyprland - Wayland)
* macOS: Needs to be built from source or run it natively with python
* Android can be run with a Linux emulator. (See Building from Source)
* iOS: Can be run with iSH (A script for it is in development) 
* ARM devices need to be natively run with Python
# Building from Source

This is an automatic build script. Just run the following in your terminal and select your system.

### Supported Platforms:

- Ubuntu
- Arch Linux
- Termux

```
wget "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/install.sh" && bash install.sh
```



## Useful Information


- [Porn Fetch Issues Documentation](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ISSUES.md)
- [How to contribute](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CONTRIBUTING.md)
- [Roadmap](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ROADMAP.md)
- [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)

# Legal Rights

> ! PornHub PROHIBITS downloading videos for unregistered users. <br>
> ! PornHub PROHIBITS scraping content on their website

So what do we learn from this?  This tool is probably NOT permitted by PornHub.
I am just the developer. Nobody will get you in jail because you downloaded a video from PornHub, but
consider using a VPN to be safe.

# Credits

### Project API : [PHUB](https://github.com/Egsagon/PHUB)
### GUI : PySide6 - [Qt](https://qt.io) for Python
### External libraries:
* [colorama](https://github.com/tartley/colorama)
* [tqdm](https://github.com/tqdm/tqdm)
* [phub](https://github.com/Egsagon/PHUB)
* [sentry sdk](https://github.com/getsentry/sentry-python) Used in 1.7+ 
* [requests](https://github.com/psf/requests)
* [pyside6](https://wiki.qt.io/Qt_for_Python)
* wget
* bs4 (Used by PHUB API)
* js2py (Used by PHUB API)
### Graphics:

* [Download Icon](https://icons8.com/icon/104149/herunterladen) *
* [Search Icon](https://icons8.com/icon/aROEUCBo74Il/suche) *
* [Settings Icon](https://icons8.com/icon/52146/einstellungen) * 
* [C Icon](https://icons8.com/icon/Uehg4gyVyrUo/copyright) * 
* [M Icon](https://iconscout.com/icons/medium) By [Unicons Font](https://iconscout.com/contributors/unicons) on [Icon Scout](https://iconscout.com) *
* [Checkmark](https://www.iconsdb.com/barbie-pink-icons/checkmark-icon.html)

*only used in older versions.

#### Contributors:

(Contribute to the project, to have your name listed here :D)

# License:

So and here we have a "little" problem. I started this project when I was 14 years old.
I licensed it under Creative Commons, but this is of course NOT the right license to be used for Open-Source Software development.
I did some research, and I realized that I need to use either LGPL or GPL license for an Open-Source development with Qt for Python.
I decided to use the LGPLv3 License. I don't know why, because it was a big mistake. The LGPLv3 License is used by libraries and not
by a full standalone Application. So I need to change my License to GPL. I talked to ChatGPT about it because I don't have
money for a Lawyer, and I guess ChatGPT is a bit smarter than some users on reddit. We figured out that the external libraries that I am using
within my Project are compatible with the GPL License. 

I am using the following external libraries:

* [tqdm](https://github.com/tqdm/tqdm)
* [colorama](https://github.com/tartley/colorama)
* [sentry_sdk](https://github.com/getsentry/sentry-python)
* [phub](https://github.com/Egsagon/PHUB/blob/master/LICENSE)
* [requests](https://github.com/psf/requests)
* wget - wget no longer has a repository

tqdm uses the MPL (Mozilla Public License) 2.0 and the MIT License <br>
colorama uses the BSD 3 license <br>
sentry sdk uses the MIT License <br>
phub uses the GPL license<br>

I can just say: Sorry. <br>
We all were young and foolish, but I don't delete my mistakes. I stay behind them, and I want to be transparent to everyone.


LICENSE: [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html)

