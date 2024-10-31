# 3.5

- [] Support for system's native UI design
- [] Geo block bypass
- [] Allow for custom proxy lists to help people in censored countries
- [] Full support for spankbang
- [] Harden the tag writing function
- [] Allow for different format converting e.g, mov and mkv
- [x] Fix the progress reporting on the file-read function
- [] Optimize the CLI and fix some of its errors
- [] Rework the entire progress reporting system (probably the hardest thing to do)
- [] Re-implement the internet and status checks, but in a better way
- [] Display thumbnails when searching (optionally)
- [] Fix [#53](https://github.com/EchterAlsFake/Porn_Fetch/issues/53)
  - [] Fix remote connection closed without response
  - [] Fix logging
  - [] Fix image URLs from PornHub
  - [x] Improving installation instructions
    - [x] Add instruction which file to pick from the releases
    - [x] Tell about the .sig and gpg verification
    - [x] Tell about the .config file and why it's important
    - [x] Tell how to make Porn Fetch executable on Linux systems

- [] Make a first-use tutorial
- [x] Fix the Porn Fetch layout
- [] Rework Porn Fetch buttons and some UI design
- [] Make Porn Fetch fully installable and runable from context menu on Windows and Linux
- [] Make an "evasion" mode, to hide Porn Fetch from your PC / Android device

### I don't want to do this, but I have to.

- [] Verify that every single setting in Porn Fetch works and has an effect
- [] Test how much simultaneous downloads Porn Fetch is capable of
- [] Test how robust the code is against user errors and improve traceback
- [] Get Porn Fetch back on Android
  - [] Enabling the QFile picker (currently has a crash bug)
  - [] Fixing threading and segment downloading in general
  - [] Make a separate layout for Porn Fetch on Android
  <br>**DEPENDS ON QT, NOT MY FAULT IF IT DOESN'T WORK, SERIOUSLY**