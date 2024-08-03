# 3.3

## New Features
- Porn Fetch supports discord rich presence (although it's optional and disabled by default)
- Porn Fetch now checks connection to all sites and lets you know if there was an error
- Untested support for macOS
- Added model support for xvideos
- You can now select a range of videos
- Added sorting to the tree widget
- Added searching support for files

## Bug fixes
- Fixed application tabbing
- Fixed the total progressbar showing no percent value after it is finished

## Other
- Huge code refactoring
- Added CI/CD build actions for all platforms
- Switched to Qt 6.7.0
- Improved terminal debug messages
- Reduced file size by over 70% on Windows and Linux
- Improved the tree widget
- Switched building to pyside6-deploy (nuitka)
- Improved visual appearance and startup time

## Deprecations
- removed all metadata functionality from Porn Fetch, because it's useless and hard to maintain.
