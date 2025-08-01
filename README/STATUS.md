# v3.6


# Bug fixes
- [x] Fix XNXX progress reporting
- [x] Fixed total progress in general
- [x] Fixed thumbnails entirely
- [x] Fix tools section layout
- [] Fix check for updates changelog displaying
- [] Entirely rework and fix the error reporting system
- [x] Fix thumbnails for HQPorner
- [] Bring Porn Fetch back on Android
  - [] Make an Android compatible Layout
  - [] Fix threading
  - [] Fix UI flickering and loading issues

# Graphical User Interace
- [x] Entirely reworked progressbar system
- [x] Progressbars are now dynamically generated instead of hardcoded
- [x] You can now double-click a thumbnail to view it separately
- [x] Upgrade Python version from 3.11 -> 3.13
- [x] Allow for font size change
- [] Allow for direct video downloading instead of manually selecting in the tree widget
- [] Support Thumbnail when navigating with Arrow keys
- [] Change Icons
- [] Fix TypeError: Incoming markup is of an invalid type: None. Markup must be a string, a bytestring, or an open filehandle.
- [] Fix and improve the CLI
- [] ~~Implement transition animations for the Stacked Widget~~
- [] Improve tree widget range selection and make it finally intuitive lol
- [] Splash screen loading animation? (maybe idk yet)
- [] Publish translation strings on Crowdin 
- [] Optional processing delay for every video
- [] Fix tabbing
- [] Fix keyboard shortcuts

# Other stuff
- [x] Add spankbang back into the project
- [] Automatic model download of new videos [#78](https://github.com/EchterAlsFake/Porn_Fetch/issues/78)
- [] Allow for more parameters when starting Porn Fetch [#77](https://github.com/EchterAlsFake/Porn_Fetch/issues/77)
- [] Allow for Video IDs as the filename [#76](https://github.com/EchterAlsFake/Porn_Fetch/issues/76)
- [] Allow ignoring specific errors [#74](https://github.com/EchterAlsFake/Porn_Fetch/issues/74)
- [] Rework the Batch processing features entirely (lol)
- [] Re-add an error / feedback reporting system using my own privacy focussed server
- [] Switch update checking to my own server instead of GitHub (more flexibility)
- [] Rewrite License Agreement to be GPLv3 compliant
- [] Add a kill switch feature for Proxy users

# Code optimizations
- [x] Fixed latency issues when updating progressbar
- [x] Switch the whole application from QWidget-based to QMainWindow + stackedWidget (long story)
- [x] Improve failed segment retrying
- [] Allow ignoring specific exceptions (#74)
- [] Entirely rework how settings are handled within Porn Fetch
- [] Generally improve how translations are handled
- [] Improve download from file implementation
- [] Finalize proxy support
- [] Improving installation
  - [] Letting user know if Porn Fetch is already there
  - [] Better exception handling
  - [] Maybe auto updating Porn Fetch in the future? (Would be great lmao)

# Android
(This will be ignored for now, cuz we're switching to QML in the future, so these problems should automatically resolve lol)
- [] Fix I/O error for Qt stylesheets and icons
- [] Layout changes, so that the app fits the screen (probably with QScrollBar)
- [] Fix path issues
- [] Make an Android Intent event, so that Android immediately recognizes downloaded fies (long story)

# CLI
- [] Entire rework of the CLI
- [] Specific better support for Termux
- [] Auto installation for Termux on Android to also handle storage permissions etc...
- [] Fix progress reporting


# 3.7 - I don't know
- [] Entire rewrite in QML
- [] Dedicated Android layout in QML
- 