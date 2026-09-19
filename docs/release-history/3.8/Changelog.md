# 3.8
### New Features
- [GUI] Support for Linux arm64
- [CLI] Support for macOS x64, macOS arm64, Linux riscv64, Linux s390x, Linux ppc64le
- [GUI] Support for Android (native Kotlin App)
- Added support for xhamster's alternative "xhopen" domain
- Added Video support for beeg.com
- Added Video support for porntrex.com
- Added Video support for xfreehd.com
- Added Model / Channel support for porntrex.com
- Added Searching support for porntrex.com
- Your configuration values are now saved after an update
- Added automatic updating for macOS (natively, yes really 🔥)
- Added fully automatic auto updating for future builds
- You can now apply a custom template for the filename
- You can now resume downloads
- You can now actually stop downloads lol
- You can now choose quality for each download separately
- You can now choose between system's CA for SSL or Certifi's CA 
- Added a splashscreen for Windows devices
- Added loading screen

### Bug Fixes
- Fixed Windows Arm64 builds
- Fixed 403 missav error
- Fixed PornHub download issue
- Fixed PornHub thumbnail issue
- Fixed non utf-8 video titles to cause a crash on Windows CLI

### User Interface
- Added Italian translations (Thanks: @FatalPuppet)
- Added clear tooltips for most settings option to help understand
- You can also set a custom app name when installing Porn Fetch from the settings
- Infinite loading animation works better now
- Added 480p to quality selection (#98)
- Added an information dialog for the first run basically telling about all useful aspects of Porn Fetch
- QCombobox items have a correct size and the text isn't hidden anymore
- Changed UI to be smoother and more modern friendly
- Thumbnails are now fetched in a separate thread

### Code Optimizations
- Refactored `check_video` function to be faster and less redundant
- Switched (mostly) from configparser to QSettings for faster and native settings handling
- When installing Porn Fetch on Linux, the logo will not be downloaded and is embedded in the app
- Improved installation by using standardized paths, instead of hardcoded ones

### Other
- Fixed build scripts
- Improved building speed thanks to uv
- You can now select which tag / commit to build
- Unified macOS / Linux build into one file
- Updated build to Python 3.13.11 (All systems)
- Updated Qt to 6.10.2
- Updated Nuitka to 2.8.9
- Porn Fetch server supports IPv4 now and has an actual SSL certificate

### Deprecations
- Removed automated selection of videos
- Removed Internet checks entirely
- Removed default and ffmpeg download mode

