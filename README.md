# Porn Fetch - A PornHub Downloader 4 Free & Everyone

## The *only free and Open-Source Downloader without restrictions or ADs


# Features:

* Downloading directly from PornHub itself
* Downloading with Max. quality
* Fetching Metadata from Videos
* Downloading multiple videos at once
* Downloading all videos from a whole Channel / User account
* Native Dark mode
* No ADs & restrictions
* No Login / PornHub Account needed

## Windows (X86_64)

 * [Porn Fetch 1.4.exe](https://drive.google.com/uc?export=download&id=1sur_U5h_j7jjwF_Cj3IaLzz1mRg1YqK6) <===========> Torrent: [1.4.torrent](https://drive.google.com/uc?export=download&id=1o2zgg40REu4V6hUKYAOHPtNF09OIjMZV) 
 * [Porn Fetch 1.3.exe](https://drive.google.com/uc?export=download&id=15pUQDXyqVGOXVMbSIcihYsuu7z6dKRan) <===========> Torrent: [1.3.torrent](https://drive.google.com/uc?export=download&id=1_G63Q_SMg-p1tXXlPP8l7wu1R4v92lQM)
 * [Porn Fetch 1.2.exe](https://drive.google.com/uc?export=download&id=156z1RNcSQSXUPSkO8sXG6U-r_wdmrB2d) <===========> Torrent: [1.2.torrent](https://drive.google.com/uc?export=download&id=1MYBZ6uzYO4pvphCa6P4iAmfUXFnGE-g_)
 * [Porn Fetch 1.1.exe](https://drive.google.com/uc?export=download&id=1Tt-siUB9siSMx4etcNvkZ0e4srbiVlr9) <===========> Torrent: [1.1.torrent](https://drive.google.com/uc?export=download&id=1wbztz8LQUj83qbUwL-0VqEql3TYzlag7)
 * [Porn Fetch 1.0.exe](https://drive.google.com/uc?export=download&id=19EUh8DgiMnZTa2lQPldIWhuOR6Y3XMiZ)  <===========> Torrent: [1.0.torrent](https://drive.google.com/uc?export=download&id=1CgZqfA6WZWFUB5LO3EnkpPVV6z8vQ6bW)
 * [LICENSE](https://drive.google.com/uc?export=download&id=1V5pgayZB9_cv7nlon55r80-hMKiAwWC2) 
    
Source code can be found in the [GitHub Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)

## Linux (AppImage)

* [Porn Fetch 1.4](https://drive.google.com/uc?export=download&id=1GkF0vuwxLn1jDaPQoqHdaokqSLjJIXIp) <===========> Torrent: [1.4.torrent](https://drive.google.com/uc?export=download&id=1nm2_NLIUuzBTlzXj6Z63Kdlr3AS9nroi)
* [Porn Fetch 1.3](https://drive.google.com/uc?export=download&id=1fmKO3HZbddhx1NtKRw2Pexro0jy5t7HP) <===========> Torrent: [1.3.torrent](https://drive.google.com/uc?export=download&id=1jLfg-XPZpkI3SLXUd3hRGJpraDb9KZKT)
* [Porn Fetch 1.2](https://drive.google.com/uc?export=download&id=1Z_S1F74y8lF9crM1aWus3MiO8Yqt92YQ) <===========> Torrent: [1.2.torrent](https://drive.google.com/uc?export=download&id=1zWLKmbiLocv7UOWHJEWf1Y4-RdJljI1J)
* [Porn Fetch 1.1](https://drive.google.com/uc?export=download&id=1-fghgnBv1tfkW5z5qY491KvXfWtyj0TP) <===========> Torrent: [1.1.torrent](https://drive.google.com/uc?export=download&id=1yTkyoDPr7soLT_wQ6u7D_fa92FL9tGFT)
* [Porn Fetch 1.0](https://drive.google.com/uc?export=download&id=1l3SMGTdt01yjqFOOwpgiKt029087SWwy) <===========> Torrent: [1.0.torrent](https://drive.google.com/uc?export=download&id=1664ZZa21seGlCq5lgpwZybF_wpsuLPgR)
* [LICENSE](https://drive.google.com/uc?export=download&id=1V5pgayZB9_cv7nlon55r80-hMKiAwWC2)

Source code can be found in the [GitHub Releases](https://github.com/EchterAlsFake/Porn_Fetch/releases)

# Supported Platforms

* Windows (Compiled versions available) (Tested on 11)
* Linux (Compiled versions available) (Tested on Arch, Kali, Ubuntu)
* macOS (Needs to be built from source -- I can't compile it, because I don't have a macOS device -- )
* Android (Can be built from source, but it's tricky.  -- Working on it -- )
* iOS (Would be possible in theory, but practical No.  You would need to Set up a Linux Distro via iSH and connect to a GUI via VNC, then setup X Window System and launch the GUI with Python, without compiling it.)

# Building from Source

Note, this is for advanced users and is NOT needed for the average guy out there...

Make sure you are using a Linux Environment and have the following dependencies installed: git python3 python3-pip
<br>Ubuntu Users also need to have:  python3-venv   installed.


This Process does NOT require root access!
```
mkdir build output && cd build && git clone https://github.com/EchterAlsFake/Porn_Fetch && cd Porn_Fetch && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && pyinstaller -F widget.py && cd dist && mv widget Porn_Fetch && chmod +x Porn_Fetch && mv Porn_Fetch ../../../output/ && echo "Porn Fetch is now in the output directory!" 

````
# Common Issues

* Unhandled Error: Index out of range
   <br> This is an error caused by the API. Restarting the application usually fixes this.
   <br>
* Request connection error:
  <br>You only see this if running in a terminal. This is caused again by the API. This happens when using the Search feature. Some videos won't be listed but in general
<br>this error can be ignored. Also, I am not able to fix this. This is a problem with PornHub itself!
* Nothing happens, when I click a button
 <br> I am aware of that. Restarting the Application will fix the error for now, but I am trying to implement a "refresh" feature which would resolve this.

# Legal Rights

I don't know about the Law in the U.S.
<br>I am not a Lawyer and I can not say much to it. Probably nothing happens, when you use this program, but if you really want to be safe, then use a VPN.
<br>For me in Germany, you need to be at least 18 years old to watch & have porn. (I know I am not 18, but let's put that away ^^)
<br>Also, You are downloading copyright protected content, so it's a risky thing. It's like when you download music from YouTube.  It's a gray zone.
<br>But in the end, I am not liable for it. Don't ask me if you got in trouble.

# Support / Contribution

You can always make Pull Requests, Submit Issues and give new ideas in the discussion section :)
<br>I would really need your help, when it comes to design. I can develop software, but I am terrible in designing something.
<br>So, If you have ideas, tell me.

External Support:
<br> If you want, you can [donate](paypal.me/EchterAlsFake) me something on PayPal, but please mark the Payment as "for friends and family"

# Credits

####  A BIG thanks to [Egasgon](https://github.com/Egsagon), who created the [PHUB](https://github.com/Egsagon/PHUB) API, which is the API I am using. Without his project, I would not be able to make this program.
####  Thanks to ChatGPT for helping me with the Threading, Signal and Slots stuff.
####  Thanks to the Qt Company for giving people like me the opportunity to use some really nice developing Tools like Qt Creator / Designer for free Open-Source developing.
####  <br>I really appreciate that!

#### And of course the external libraries, that I used within my code:
* [colorama](https://github.com/tartley/colorama)


# License:

[LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.en.html)

*of course not the only, but you get the point, what I mean