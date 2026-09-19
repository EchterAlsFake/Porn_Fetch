# iOS support before GTA6? 
Maybe...

# CLI
The CLI of Porn Fetch is able to run on iOS. I have just managed to get it working.
I bought an old iPhone 7 and jailbroken it rootless using [palera1n](https://github.com/palera1n/palera1n).
The way was hard but it works. After installing Python3.12.5 from kitty-xz's repositories.
This way I was able to clone the repository, install the requirements and run Porn Fetch.
The base CLI worked, downloading did not. However, downloading with the pure PHUB module did
work and produced a .mp4 file. 

This proves: **IT CAN BE DONE**

Over the next weeks I will search for ways and try all possible ways to get that working.
In version 3.8, maybe we have iOS support for the CLI. Maybe even a native binary you can 
just run without the Python stuff. We'll see.

Okay Edit:
I don't know what I changed, but yeah downloading works just fine now :) 

# GUI
While the above process produces the CLI, but only works on jailbroken iPhones, the GUI
could maybe even by half of 2026 be running officially on iOS with native support using
the official Apple way.

This depends on two things:

1) Code signing (big Apple L moment)
2) PySide6 for iOS

Qt has stated in their PySide6 6.10.0 blogpost, that they have started initial support
for iOS with their core Qt modules. This means, that the base of Qt works.
They need to get the graphical stuff working and enable full UI rendering, and then we
can build full PySide6 apps for iOS. Yes, really.

The problem is: **Signing.**

I don't own an Apple developer account nor will I pay for one. So, maybe you can install
the app through some unofficial methods if you live in the EU, I don't know, we will see.
But there's always a way. I will find it. 


If all this works, Porn Fetch would be running on all major platforms. 
This would be a huge milestone, not only for me, but actually to show the
true power of Python. Sure Python isn't Java where you can say: 

"Compile once, run everywhere"
<br>or like Fireship likes to say: 
<br>"Compile once, debug everywhere" xD

But it's possible with enough time.



# Installation (Jailbreak)
#### Supported iPhones (theoretical)
- iPhone 6s
- iPhone 6s Plus
- iPhone SE
- iPhone 7
- iPhone 7 Plus
- iPhone 8
- iPhone 8 Plus
- iPhone X

You can maybe also run on iPad, iPod or Apple TV,
however, I can't test it and I can't provide any guide on how
to do it. You are absolutely on your own, but feel free to do it.

> [!IMPORTANT]
> If you haven't already, jailbreak your iPhone using: [Paler1n](https://palera.in/). This can destroy your
> device, some apps may stop working, you (probably) lose Apple's warranty, and Apple may even sue you for breaking
> into their system. Usage is on your risk. I can't help you if something goes wrong!

# Installation Tutorial
#### Jailbreaking your device

> [!IMPORTANT]
> Use a USB-A to Lightning Cable. The USB-C variants usually don't work well. 

1) Run: `sudo palera1n -l -V -vvv` to jailbreak your device

If you get this error: `UaF race: heuristic strategy failed, setup packet was not accepted`
<br>Use an Intel CPU based system (yes seriously)

If you get stuck in the Pongo OS screen and nothing happens,
disconnect and reconnect cable and it will boot fine. 

If your iPhone breaks, buy a Google Pixel instead 🔥

2) Open Sileo and Install the CyPwn repository
3) Install Python 3.12.5-1 by kitty-xz (or compile yourself if you have no life LMAO)
4) Install some terminal e.g., NewTerm

Now everything wors as usual on Linux

5) Clone the repository, cd into the project, create a virtual environment, install the CLI requirements 

You need to install all the requirements and every API manually. Do NOT try
to install from pyproject.toml, that won't work. Just run the CLI and install each missing package
until it works.









