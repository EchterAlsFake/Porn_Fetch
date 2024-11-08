# 3.5

## Bug fixes
- [x] Fix the progress reporting on the file-read function
- [] Optimize the CLI and fix some of its errors
- [x] Fix HQporner / Eporner progress issue stopping at 99%
- [] Fix [#53](https://github.com/EchterAlsFake/Porn_Fetch/issues/53)
  - [] Fix remote connection closed without response
  - [] Fix logging
  - [] Fix image URLs from PornHub
  - [x] Improving installation instructions
    - [x] Add instruction which file to pick from the releases
    - [x] Tell about the .sig and gpg verification
    - [x] Tell about the .config file and why it's important
    - [x] Tell how to make Porn Fetch executable on Linux systems
- [] Fix an index issue in the tree widget:
 When a video was loaded in index 1 and a user checked the box for not clearing videos, the next loaded
 Video would have an index of 11, although it should have an index of 2

## New Features
- [x] Make Porn Fetch fully installable and runable from the start menu on Windows and Linux
- [x] Re-implement the internet and status checks, but in a better way
- [] Display thumbnails when searching (optionally)
- [] Support for system's native UI design
- [] Geo block bypass
- [] Allow for custom proxy lists to help people in censored countries
- [] Full support for spankbang
- [] Allow for different format converting e.g, mov and mkv
- [] Allow for optional tag writing
- [] When downloading a new video / loading in and videos are already downloading, the total progress should be appended
by that instead of calculating the new total progress. This will require a rework of the progress system, but is a huge QOL update.
- [] Make an "evasion" mode, to hide Porn Fetch from your PC / Android device

## Code improvements and design updates
- [x] Fix the Porn Fetch layout
- [] Improving and hardening the tag writing function (with exceptions)
- [] Generalizing the backend Porn APIs to work more equally to optimize Porn Fetch to write lesser lines of code
- [] Rework the entire progress reporting system (probably the hardest thing to do)
- [] searching for ways to improve Android display reaction time for UI elements
- [] Improve code for the part when a video finished downloading
- [] Make a threading class for every function that could take more time than ~350 ms to prevent UI delays
- [] Make a first-use tutorial
- [] Rework Porn Fetch buttons and some UI design
- [] Show a status for how many of the total downloads already succeeded (probably at the bottom of Porn Fetch)


### Testing (Really don't want to do that)

- [] Verify that every single setting in Porn Fetch works and has an effect
- [] Test how much simultaneous downloads Porn Fetch is capable of
- [] Test how robust the code is against user errors and improve traceback
- [] Get Porn Fetch back on Android
  - [] Enabling the QFile picker (currently has a crash bug)
  - [] Fixing threading and segment downloading in general
  - [] Make a separate layout for Porn Fetch on Android
  <br>**DEPENDS ON QT, NOT MY FAULT IF IT DOESN'T WORK, SERIOUSLY**