# Porn Fetch installation guide

You can find the download files in the GitHub releases.
-->: https://github.com/EchterAlsFake/Porn_Fetch/releases/


> [!NOTE]
> Everyone needs to read the following 3 sections:

- [Versions of Porn Fetch](#versions-of-porn-fetch)
- [The actual installation](#the-actual-installation-of-porn-fetch)
- [Updating Porn Fetch](#updating-porn-fetch)


After that you can continue selecting your system from the 3 (+1):

- [Windows](#downloading-and-installing-on-windows)
- [Linux](#downloading-and-installing-on-linux)
- [macOS](#downloading-and-installing-on-macos)
- [Android](#downloading-and-installing-on-android)

Additionally, you may also be interested in:

- [Verifying Porn Fetch integrity](#verifying-porn-fetch-integrity)
- [Torrent version of Porn Fetch](#torrent-version-of-porn-fetch)

# Versions of Porn Fetch
Porn Fetch has two versions. The `GUI` (Graphical User Interface) and the `CLI` (Command Line Interface). The Graphical
User interface is the full app that you probably want to use. The Terminal version as it says, runs purely in a terminal
and is intended to be used by advanced users or in cases, where you don't have a graphical environment, e.g., iSH or Termux.

Porn Fetch runs on different processor architectures:
- `x64` -> For all new desktop processors
- `x32` -> For 32bit versions of Windows / Linux and very old processors

If you don't know the difference, pick `x64`



> [!IMPORTANT]
> ### macOS USERS MUST READ THIS:
As you might know, Apple uses their own M1, M2, M3 (so-called Apple Silicon) chips. These processors run differently than
most others. I do not have a MacBook myself. Porn Fetch on macOS is tested thanks to a virtualized environment. That means
that when I compile Porn Fetch, I do so on an x86_64 AMD processor.

However, Apple has a translation layer that makes it in theory possible for you to run these application, but I have no
way of testing that. If it doesn't work for you, but you have the time, please get in touch with me.


# The actual installation of Porn Fetch
As soon as you have downloaded the file for your operating system, and you started Porn Fetch, you'll
be prompted for an installation mode.

Porn Fetch itself only consists of two files. The `config.ini` and the main `.exe` / `.bin` file. However, to make
Porn Fetch easily accessible on your system, you can install it. You can give it a custom App name, and then you can use
this name to search for Porn Fetch on your PC. 

For example on Windows you would press Windows key, and then you can search inside of this window. There you can
search for the App name you have given Porn Fetch during the installation. If you left it empty, simply search 
for "Porn Fetch". 

However, you **DO NOT NEED** to install Porn Fetch. You can also select the portable mode. That means that Porn 
Fetch will stay where you have downloaded it to and you just simply always click the downloaded executable file. 
This gives you more control over it. 


# Updating Porn Fetch
Porn Fetch searches for updates everytime you start it. If a new version is out it will let you know and give
you the download link.

When you download the new file, and you install Porn Fetch into your system it will overwrite the old configuration and 
executable file. That means that all your configuration will be lost and Porn Fetch basically resets itself to default settings.


# Downloading and Installing on Windows
You need to download the file: `PornFetch_Windows_GUI_x64.exe` from the GitHub releases. After downloading it,
simply click the .exe file and select your installation mode.

That's it! Now you can additionally install FFmpeg from the settings menu to correctly convert videos.

Have fun! 


# Downloading and Installing on Linux

> [!NOTE]
> Porn Fetch is made with Qt. Depending on your distro, you **may** (maybe not) need to additionally install some Qt related packages.
> Please ask ChatGPT for more information.

You need to download the file: `PornFetch_Linux_GUI_x64.bin` from the GitHub releases. After downloading it, you
can try double-clicking the `.bin` file. If nothing happens you may need to set executable permissions. 

You can do that by opening a Terminal in the current location and paste: `chmod +x PornFetch_Linux_GUI_x64.bin`.
After that, try to open it again by double-clicking it.

If still nothing happens go into a Terminal once again and type: `./PornFetch_Linux_GUI_x64.bin`. This will "execute"
the Porn Fetch executable. If you see some output, but it seems to have crashed, create an Issue on GitHub and paste
the output along with your Linux system information.

After that select the installation mode and that's it! If you haven't already installed ffmpeg on your Linux distribution
you can do so with the package manager e.g., Debian based: `sudo apt install ffmpeg` or you can install it automatically
through Porn Fetch's settings menu.

Have fun! 


# Downloading and Installing on macOS
So, macOS is currently not that easy to actually run....

Because of some problems with Nuitka and pyside6-deploy you can not just install Porn Fetch on macOS like you would
do with other packages, however you can still use it!

Download the file: `PornFetch_macOS_GUI_x86_64.zip` and extract the zip. You will be given a directory named "Porn Fetch.app".
This is where all Porn Fetch assets are stored. You need to go into a terminal and execute the `main` file inside the .app package.

You can do so by typing: `cd Porn Fetch.app/Contents/MacOS && ./main`

You need to always execute it via the terminal. There's unfortunately no other way...

### Here's a video tutorial
https://youtu.be/VvFJLEFECXg


> [!IMPORTANT]
> You really need to change the output path of videos in the settings of Porn Fetch. Set it to something like your desktop
> or similar. Otherwise, videos will be saved into the .app package directory -_- 


# Downloading and Installing on Android
> [!CRITICAL]
> Android is at the moment not supported due to UI rendering issues. This will be fixed in version 3.6 but is a 
> lot of work.


Experienced users can use Termux on Android to emulate the CLI. There will be an in depth guide when version 3.6
is out, because I need to change some things...



# Verifying Porn Fetch integrity
If you live in a censored country or you are a high value target for your government / law enforcment
it might be critical for you to verify that your Porn Fetch downloaded executable hasn't been modified by a
third party.

You can verify that using the .sig files from the GitHub release assets. Every file from Porn Fetch also has the same
file with a `.sig` ending. 

E.g.,:
- `PornFetch_Windows_GUI_x64.exe` and `PornFetch_Windows_GUI_x64.exe.sig`

The .sig file is a cryptographic proof with my gpg key that your downloaded Porn Fetch executable is 100% from me
and is unmodified.

> [!NOTE]
> You need to have `gpg` installed on your system

For example, for the Linux GUI version you would do something like:

`gpg --verify PornFetch_Linux_GUI_x64.bin.sig PornFetch_Linux_GUI_x64.bin `

It should show something like this:
![img.png](../src/backend/img.png)

It may tell you that it can't really verify that the signature is from me. In that case you need to import my public gpg
key and trust it. 

You can download it from here: https://github.com/EchterAlsFake/EchterAlsFake/blob/main/public_key.asc


# Torrent version of Porn Fetch
A torrent is a file for the P2P network. Shortly explained, it's a decentralized network of people who have certain files 
and others who want to have files.

If you for whatever reason want to download Porn Fetch through this Network, you can download a torrent client
such as `qBittorrent` and paste the `.torrent` file or the Magnet Link in there.

You then need to wait to find seeds (the term for people who have 100% of the file/s). I will seed almost every day for
at least 6 hours. But if you are lucky you might also find other seeds.

> [!CRITICAL]
> I am seeding with a VPN! (Yes, all the time...)

















