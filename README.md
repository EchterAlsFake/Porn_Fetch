# Porn Fetch - A PornHub Downloader 4 Free & Everyone

# Table of Contents

- [What is Porn Fetch?](#what-is-porn-fetch)<br>
- [Features](#features)
- [Installation](#installation)
- [Data collection and Privacy](#data-collection--privacy)
- [Supported platforms](#supported-platforms)
- [Building from source](#building-from-source)
- [Useful information](#useful-information)
- [Legal rights](#lgeal-rights)
- [Credits](#credits)
- [License](#license)

# What is Porn Fetch?

Porn Fetch is a program, that can download, search and interact with videos from PornHub.
The goal is to create a free and open-source downloader for everyone. 
There's no need to use shady websites or paid software in 2023.

# Features:

* Downloading directly from PornHub itself
* Downloading with selectable quality
* Fetching metadata from Videos
* Downloading multiple videos at once
* Downloading all videos from a whole Channel / User / Model account
* Search for videos and download them directly in the application
* Native dark mode
* CLI for systems without a graphical user interface
* No ADs & restrictions
* No login / PornHub account needed
* No data tracking
* Open-Source
* Cross-platform
* Actively maintained

# Installation

Source code can be found in the [GitHub releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)
<br>Older versions: See [Downloads](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/DOWNLOADS.md)


### Windows:


* [Porn Fetch 1.6.exe](https://drive.google.com/uc?export=download&id=1Ok4iHIBOFlTa0hXifLql0TRy-8JwC39D) -|- Torrent: [1.6.torrent](https://drive.google.com/uc?export=download&id=1BPjfmqEiqmEdAXmsRV2KUktS6GOc8_DK)
* [LICENSE](https://drive.google.com/uc?export=download&id=1V5pgayZB9_cv7nlon55r80-hMKiAwWC2) 

### Linux (AppImage)

* [Porn Fetch 1.6](https://drive.google.com/uc?export=download&id=1JMqEIhdLwHtB2c34qZpVDUv1fkIsGE3l) -|- Torrent: [1.6.torrent](https://drive.google.com/uc?export=download&id=1_taHgEy74raRPxKNpNLcm9h4nAtEKDSn)
* [LICENSE](https://drive.google.com/uc?export=download&id=1V5pgayZB9_cv7nlon55r80-hMKiAwWC2)

# Data Collection / Privacy

- No data collection by default!

If you enable the option to allow Sentry to collect errors, then the following is collected

- Error messages (The full Python traceback)
- Variables and the values in it
- The lines of code, in which the error happened

> Sentry will NOT collect any user specific information or system information!


# Supported Platforms

* Windows : Windows 7, 8, 8.1, 9, 10, 11
* Linux   : X11 / Wayland - X64 
* macOS   : Needs to be built from source or run it natively with python
* Android : Can be run with a Linux emulator. (A script for it is in development)
* iOS     : Can be run with iSH  (A script for it is in development) 
* ARM devices: Need to be natively run with Python
# Building from Source

### Arch Linux:

``` 
sudo pacman -S python-virtualenv
```
```
mkdir build
```
```
cd build && git clone https://github.com/EchterAlsFake/Porn_Fetch && cd Porn_Fetch
```
```
python3 -m venv venv && source venv/bin/activate
```
```
pip install -r requirements.txt
```
```
pyinstaller -F widget.py && cd dist && mv widget Porn_Fetch && chmod +x Porn_Fetch && sudo mv Porn_Fetch /usr/bin/
```
```
$ Porn_Fetch
```



## Useful Information


- [Porn Fetch Issues Documentation](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ISSUES.md)
- [How to contribute](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CONTRIBUTING.md)
- [Roadmap](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ROADMAP.md)
- [Security](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/SECURITY.md)
- [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)

# Legal Rights

> ! PornHub PROHIBITS downloading videos for unregistered users. <br>
> ! PornHub PROHIBITS scraping content on their website

So what do we learn from this?  This tool is probably NOT permitted by PornHub.
I am just the developer. Nobody will get you in jail, because you downloaded a video from PornHub, but
consider using a VPN to be safe.

# Credits

### Project API : [PHUB](https://github.com/Egsagon/PHUB)
### GUI : PySide6 - [Qt](https://qt.io) for Python
### External libraries:
* [colorama](https://github.com/tartley/colorama)
* [tqdm](https://github.com/tqdm/tqdm)
* [phub](https://github.com/Egsagon/PHUB)
* [sentry sdk](https://github.com/getsentry/sentry-python) Used in 1.7+ 

#### Contributors:

(Contribute to the project, to have your name listed here :D)

# License:

So and here we have a "little" problem. I started this project, when I was 14 years old.
I licensed it under Creative Commons, but this is of course NOT the right license to be used for Open-Source Software development.
I did some research and I realized that I need to use either LGPL or GPL license for an Open-Source development with Qt for Python.
I decided to use the LGPLv3 License. I don't know why, because it was a big mistake. The LGPLv3 License is used by libraries and not
by a full standalone Application. So I need to change my License to GPL. I talked to ChatGPT about it, because I don't have
money for a Lawyer and I guess ChatGPT is a bit smarter than some users on reddit. We figured out, that the external libraries that I am using
within my Project are compatible with the GPL License. 

I am using the following external libraries:

* [tqdm](https://github.com/tqdm/tqdm)
* [colorama](https://github.com/tartley/colorama)
* [sentry_sdk](https://github.com/getsentry/sentry-python)
* [phub](https://github.com/Egsagon/PHUB/blob/master/LICENSE)

tqdm uses the  MPL (Mozilla Public License) 2.0 and the MIT License <br>
colorama uses the BSD 3 license <br>
sentry sdk uses the MIT License <br>
phub uses the GPL license<br>

I can just say: Sorry. <br>
We all were young and dumb, but I don't delete my mistakes. I stay behind them, and I want to be transparent to everyone.


LICENSE: [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html)

