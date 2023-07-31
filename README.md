# Porn Fetch - A PornHub Downloader 4 Free & Everyone

### The only free and Open-Source GUI Downloader without restrictions or ADs

# Important:

I can not seed the .torrent files, until next week Saturday evening. 
<br>I am on vacation and the WiFi here is at 200 KB/s speed lmao.
<br> So please use the Google Drive files until Saturday, Thanks :) 

# Features:

* Downloading directly from PornHub itself
* Downloading with Max. quality
* Fetching Metadata from Videos
* Downloading multiple videos at once
* Downloading all videos from a whole Channel / User account
* Search for Videos and download them directly in the APP
* Native Dark mode
* CLI for systems without a Graphical User Interface
* No ADs & restrictions
* No Login / PornHub Account needed
* No Data tracking
* Open-Source
* Cross Platform
* Actively maintained

## Windows (X86_64)

* [Porn Fetch 1.6.exe](https://drive.google.com/uc?export=download&id=1Ok4iHIBOFlTa0hXifLql0TRy-8JwC39D) -|- Torrent: [1.6.torrent](https://drive.google.com/uc?export=download&id=1BPjfmqEiqmEdAXmsRV2KUktS6GOc8_DK)
* [LICENSE](https://drive.google.com/uc?export=download&id=1V5pgayZB9_cv7nlon55r80-hMKiAwWC2) 

Source code can be found in the [GitHub Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)
<br>Older versions: See [Downloads](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/DOWNLOADS.md)

## Linux (AppImage)

* [Porn Fetch 1.6](https://drive.google.com/uc?export=download&id=1JMqEIhdLwHtB2c34qZpVDUv1fkIsGE3l) -|- Torrent: [1.6.torrent](https://drive.google.com/uc?export=download&id=1_taHgEy74raRPxKNpNLcm9h4nAtEKDSn)
* [LICENSE](https://drive.google.com/uc?export=download&id=1V5pgayZB9_cv7nlon55r80-hMKiAwWC2)

<br>Older versions: See [Downloads](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/DOWNLOADS.md)<br>
Source code can be found in the [GitHub Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)

# Data Collection / Privacy

Porn Fetch doesn't collect ANY data by default. <br>

However, you can support the development by allowing Sentry to automatically collect <br>
error messages and display them to me, So that I can fix the issues immediately. <br>
Sentry ONLY collects the full Python Traceback and the Values of variables.<br>
Sentry doesn't collect any System information or anything user specific, which would identify you!

# Supported Platforms

* Windows : Native Support for Windows 10 / 11 for X64 / X86 Systems
* Linux   : Native Support on all X11 / Wayland systems with Qt Support. Just run the AppImage
* macOS   : Needs to either be built from source, or run it natively with Python3 from source code
* Android : Can be run with either VNC for the GUI or within a terminal emulator with Python
* iOS     : Same as Android.  You can install iSH from the App Store and install Python3 on it. 
* ARM devices: For all arm devices, the compiled versions won't work. You need to either run it natively or compile it by yourself.

# Building from Source

Note, this is for advanced users and is NOT needed for the average guy out there...

Make sure you are using a Linux Environment and have the following dependencies installed: git python3 python3-pip
<br>Ubuntu Users also need to have:  python3-venv   installed.


This Process does NOT require root access!
```
mkdir build output && cd build && git clone https://github.com/EchterAlsFake/Porn_Fetch && cd Porn_Fetch && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pyinstaller -F widget.py && cd dist && mv widget Porn_Fetch && chmod +x Porn_Fetch && mv Porn_Fetch ../../../output/ && echo "Porn Fetch is now in the output directory!" 

````
# Current Issues
Please refer to [Porn Fetch Issues Documentation](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ISSUES.md)

# Contribution
Please refer to [How to contribute](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CONTRIBUTING.md)

# ROADMAP
Please refer to [Roadmap](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ROADMAP.md)

# Security
Please refer to [Security](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/SECURITY.md)

# Changelog
Please refer to [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)

# Legal Rights

PornHub prohibits downloading videos for unregistered users. <br>
PornHub prohibits scraping content on their website

So what do we learn from this?  This tool is probably NOT permitted by PornHub.
<br>I am just the developer. Nobody will get you in jail, because you downloaded a video from PornHub, but
consider using a VPN to be safe.

# Credits


####  A BIG thanks to [Egasgon](https://github.com/Egsagon), who created the [PHUB](https://github.com/Egsagon/PHUB) API, which is the API I am using. Without his project, I would not be able to make this program.
####  Thanks to ChatGPT for helping me with the Threading, Signal and Slots stuff.
####  Thanks to the Qt Company for giving people like me the opportunity to use some really nice developing Tools like Qt Creator / Designer for free Open-Source developing.
####  <br>I really appreciate that!

#### And of course the external libraries, that I used within my code:
* [colorama](https://github.com/tartley/colorama)
* [tqdm](https://github.com/tqdm/tqdm)
* [sentry sdk](https://github.com/getsentry/sentry-python) Used in 1.7+ 


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

