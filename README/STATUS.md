# v3.6


# Bug fixes
- [] Fix check for updates changelog displaying
- [] Entirely rework and fix the error reporting system
- [] Fix thumbnails for HQPorner
- [] Bring Porn Fetch back on Android
  - [] Make an Android compatible Layout
  - [] Fix threading
  - [] Fix UI flickering and loading issues

# Graphical User Interace
- [] Allow for direct video downloading instead of manually selecting in the tree widget
- [] Support Thumbnail when navigating with Arrow keys
- [] Fix XNXX progress reporting
- [] Change Icons
- [] Fix TypeError: Incoming markup is of an invalid type: None. Markup must be a string, a bytestring, or an open filehandle.
- [] Fix and improve the CLI
- [] Implement transition animations for the Stacked Widget
- [] Improve tree widget range selection and make it finally intuitive lol
- [] Splash screen loading animation? (maybe idk yet)
- [] Publish translation strings on Crowdin 
- [] Allow for font size change
- [] Optional processing delay for every video
- [] Upgrade Python version from 3.11 -> 3.13
- [] Fix tools section layout

# Code optimizations
- [] Allow ignoring specific exceptions (#74)
- [] Entirely rework how settings are handled within Porn Fetch
- [] Switch the whole application from QWidget-based to QMainWindow + stackedWidget (long story)
- [] Generally improve how translations are handled
- [] Improve failed segment retrying
- [] Improve download from file implementation
- [] Finalize proxy support
- [] Improving installation
  - [] Letting user know if Porn Fetch is already there
  - [] Better exception handling
  - [] Maybe auto updating Porn Fetch in the future? (Would be great lmao)

# Android
- [] Fix I/O error for Qt stylesheets and icons
- [] Layout changes, so that the app fits the screen (probably with QScrollBar)
- [] Fix path issues
- [] Make an Android Intent event, so that Android immediately recognizes downloaded fies (long story)

# CLI
- [] Entire rework of the CLI
- [] Specific better support for Termux
- [] Auto installation for Termux on Android to also handle storage permissions etc...
- [] Fix progress reporting
