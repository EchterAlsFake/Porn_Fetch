# 3.0
#### Entire rewrite of Porn Fetch, the CLI, the Android App and the HQPorner API.


## GUI
- Entire rewrite of the Porn Fetch GUI (Graphical User Interface)
- The GUI is now fully resizeable and works on all screen sizes
- The GUI now supports translations in German, Chinese and French
- The GUI now has a sidebar which is simpler than v2.9
- There's a third progressbar which tracks the total progress of all PornHub videos being downloaded
- The Tree Widget can now provide more information over the videos. Author, title and duration
- The Progressbars now have a dark design
- The License widget has now a dark design too
- The header of the QTreeWidget now supports Dark Mode.
- Updated to new improved icons.
- Global usage of the tree Widget.


## Performance
- There are three threading modes for different use cases
- The semaphore has been fixed, and you can now decide how many videos can be downloaded simultaneously (1-6)
- Implemented a Threading class for listing model videos.
- Transitioned all Metadata methods to use threading.
- Optimized the 'check_if_video_exists' function for greater efficiency.
- Strengthened the robustness of the config file integrity checking logic.
- Porn Fetch is now built with Python 3.12 (Android still 3.10)

## GitHub Repository
- A lot better project structure
- The Readme now has a translation guide
- Optimized all readmes

## Code Optimization
- Removed unnecessary signals and completed slots
- Improved threading classes
- Refactored the user settings functions
- Enhanced structure of the Q Resource file.
- Stylesheets have been reorganized and divided into multiple sections for better management.
- Changed the strip title function to allow non UTF-8 characters to support other language alphabets
- Comprehensive rewrite of the Command Line Interface (CLI).

## Translations
- Added German
- Added French
- Added Chinese

## Scripts
- Removed iOS build script (Porn Fetch isn't working on iOS sadly)
- Added support for macOS in the build script
- Added support for Windows (separate build script)

## Issues / Bug Fixes
- Fixed an issue with the config file location creation

# Deprecations
- Threading is now ALWAYS on. You can't disable it, because I see no reason for it.
- Removed Searching Filters

## Features
- Added support for Eporner.com
- Added support for xnxx.com
- Added support for xvideos.com
- New directory system to organize videos by model in separate folders.
- Videos can now be shown in reverse order [#17](https://github.com/EchterAlsFake/Porn_Fetch/issues/17)
- You can now also download by model on HQPorner
- You can now download by category on HQPorner
- You can now download by Top Porn on HQPorner
- You can now download a random video on HQPorner
- You can now search for videos on HQPorner
- FFMPEG will now be automatically downloaded and installed if checked as threading mode

# Android
- The Android App is now exactly the same as Porn Fetch desktop
- The Android app is now based on PySide6
- The Android app now supports all* features as the Desktop App

* except the QFileDialog, but this is an Issue from Qt itself.

## Contributors

- [Egsagon](https://github.com/Egsagon) French translations
- [Joshua-auhsoj](https://github.com/Joshua-auhsoj) Chinese translations & Enhancement [#17](https://github.com/EchterAlsFake/Porn_Fetch/issues/17)

# IMPORTANT FOR ANDROID USERS

Since Android changed a lot on their storage permission system, apps must nowadays ask for read / write permissions
at runtime. 
<br>I can't do this for some [reason](). You can ONLY use Porn Fetch on Android if you have the shared Download folder. It would be in
<br> `/storage/emulated/0/Download` Porn Fetch will automatically check this and notify you if it doesn't work. 

This is also the reason why Porn Fetch uses an older Android SDK, because with a lower SDK level I can get around the 
<br> Permission system, but there's no guarantee that this works.

I tested it on Android 12 & 13 on two devices.

