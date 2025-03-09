# 3.5

## Bug fixes
- [x] Fix the progress reporting on the file-read function
- [x] Optimize the CLI and fix some of its errors (#61) (#62)
- [x] Fixed output path issue in CLI
- [x] Fixed HQporner / Eporner progress issue stopping at 99%
- [x] Fixed get random video (HQPorner)
- [] Fix [#53](https://github.com/EchterAlsFake/Porn_Fetch/issues/53)
  - [] ~~Fix remote connection closed without response~~
  - [x] Fix logging
  - [x] Fix image URLs from PornHub
  - [x] Improving installation instructions
    - [x] Add instruction which file to pick from the releases
    - [x] Tell about the .sig and gpg verification
    - [x] Tell about the .config file and why it's important
    - [x] Tell how to make Porn Fetch executable on Linux systems
- [x] Fix an index issue in the tree widget:
 When a video was loaded in index 1 and a user checked the box for not clearing videos, the next loaded
 Video would have an index of 11, although it should have an index of 2

## New Features
- [x] Make Porn Fetch fully installable and runable from the start menu on Windows and Linux
- [x] Re-implement the internet and status checks, but in a better way
- [x] Porn Fetch CLI now supports batch processing through arguments
- [x] Porn Fetch CLI is now completely thread-safe and uses rich progressbar
- [x] Porn Fetch CLI now also tracks the total progress with a separate bar
- [x] Display thumbnails when searching (optionally)
- [x] Allow for optional tag writing
- [x] Allow for different format converting e.g, mov and mkv
- [x] When downloading a new video / loading in and videos are already downloading, the total progress should be appended
  by that instead of calculating the new total progress. This will require a rework of the progress system, but is a huge QOL update.
- [x] Make an "evasion" mode to hide Porn Fetch from your PC / Android device
- [] ~~Full support for spankbang~~ 
- [] Support for macOS
  - [x] Add build script
  - [x] Improve UI
  - [] Add it to `INSTALLATION.md`
  - [] Add it to `SCREENSHOTS.md`

## Code improvements and design updates
- [x] Fix the Porn Fetch layout
- [x] Rename **ALL** UI elements to be more consistent and easier to handle within code
- [x] Code refactoring
 - [x] Remove useless code
 - [x] Improve code comments

- [x] Make Porn Fetch's codebase more structured. In Germany, we say "Roter faden"
- [x] Improving and hardening the tag writing function (with exceptions)
- [x] Generalizing the backend Porn APIs to work more equally to optimize Porn Fetch to write lesser lines of code
- [x] Improve code for the part when a video finished downloading
- [x] Make a threading class for every function that could take more time than ~350 ms to prevent UI delays
- [x] Rework Porn Fetch buttons and some UI design
- [x] Show a status for how many of the total downloads already succeeded (probably at the bottom of Porn Fetch)
- [] ~~Rework the entire progress reporting system (probably the hardest thing to do)~~
- [] ~~searching for ways to improve Android display reaction time for UI elements~~ (There is no way)
- [x] Update translations
- [] ~~Make a first-use tutorial~~ Nah, people can use their brain


### Testing (Really don't want to do that)

- [x] Verify that every single setting in Porn Fetch works and has an effect
- [x] Test how much simultaneous downloads Porn Fetch is capable of
- [] ~~Test how robust the code is against user errors and improve traceback~~
- [] ~~Get Porn Fetch back on Android~~
  - [] Enabling the QFile picker (currently has a crash bug)
  - [] Fixing threading and segment downloading in general
  - [] Make a separate layout for Porn Fetch on Android
  <br>**DEPENDS ON QT, NOT MY FAULT IF IT DOESN'T WORK, SERIOUSLY**

- [] Testing installation on Windows
- [] Testing installation on Linux
- [] Testing macOS

# v3.6
- [] ~~Geo block bypass~~
- [x] Allow for custom proxy lists to help people in censored countries


### Important things
- [] Entirely rework and fix the error reporting system
- [] Bring Porn Fetch back on Android
  - [] Make an Android compatible Layout
  - [] Fix threading
  - [] Fix UI flickering and loading issues

  
- [] Support Thumbnail when navigating with Arrow keys
- [] Fix XNXX progress reporting
- [] Improve failed segment retrying
- [] Improve download from file implementation
- [] Change Icons
- [] Fix TypeError: Incoming markup is of an invalid type: None. Markup must be a string, a bytestring, or an open filehandle.
- [] Finalize proxy support
- [] Improving installation
- [] Fix and improve the CLI
- [] Implement transition animations for the Stacked Widget
- [] Splash screen loading animation? (maybe idk yet)