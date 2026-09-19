# v3.6

### New Features
- Re-added `spankbang` support.
- Windows ARM support (experimental)
- Native macOS (`.dmg`) support
- Native Android (x64, aarch64, armv7) support
- Added optional processing delay for each video
- Enabled direct video downloading without manual selection in the tree widget
- Added ability to ignore specific exceptions ([#74](https://github.com/EchterAlsFake/Porn_Fetch/issues/74))
- Added ability to double-click a thumbnail to view it separately.
- Added option to change font size.
- Added thumbnail preview support when navigating with arrow keys.
- Added kill switch feature for proxy users.
- Added option to use video IDs as filenames ([#76](https://github.com/EchterAlsFake/Porn_Fetch/issues/76)).
- (CLI) Added automatic model download for new videos ([#78](https://github.com/EchterAlsFake/Porn_Fetch/issues/78)).
- Finalized proxy support

### Bug Fixes
- Fixed XNXX progress reporting.
- Fixed JSON decode error for EPorner.
- Fixed issue where XNXX would not search on the first page.
- Fixed `missav.ws` 403 errors.
- Fixed `spankbang.com` 403 errors.
- Fixed `TypeError` for invalid markup types.
- Fixed `missav.ws` "too long path" issue for mutagen metadata editing.
- Fixed thumbnails for HQPorner.
- Fixed error handling in CLI ([#74](https://github.com/EchterAlsFake/Porn_Fetch/issues/74)).
- Fixed total progress calculation across the application.
- Fixed thumbnail rendering entirely.
- Fixed URL session export feature.
- Fixed tools section layout.
- Fixed update check changelog display.
- Completely reworked and fixed the error reporting system.
- Restored Porn Fetch functionality on Android:
  - Implemented Android-compatible layout.
  - Fixed threading issues.
  - Resolved UI flickering and loading problems.

### Graphical User Interface
- Total progress calculation now displays actual progress instead of a loading animation.
- Completely reworked progress bar system.
- Progress bars are now dynamically generated instead of hardcoded.
- Fixed tab navigation.
- Published translation strings on Crowdin.

### Other Improvements
- Updated license agreement to be GPLv3 compliant.
- Reintroduced error/feedback reporting system using a privacy-focused server.
- Changed update checking to use a custom server instead of GitHub.
- Completely reworked batch processing features.
- Added support for more parameters when starting Porn Fetch ([#77](https://github.com/EchterAlsFake/Porn_Fetch/issues/77)).

### Code Optimizations
- Fixed and improved overall session handling of each API
- Fixed latency issues when updating progress bars.
- Migrated application from `QWidget`-based to `QMainWindow` + `stackedWidget` architecture.
- Improved failed segment retrying.
- Completely reworked settings handling.
- Improved "download from file" implementation.
- Enhanced translation handling.
- Improved installation process.
- Upgraded Python version from 3.11 to 3.13.

### CLI
- Fully reworked CLI.
- Added better support for Termux on Android.
- Fixed progress reporting in CLI.


And even more that I forgot here...
