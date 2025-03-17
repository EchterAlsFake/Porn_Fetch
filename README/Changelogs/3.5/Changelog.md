# 3.5

## New Features
- Support for missav.ws
- Support for xhamster.com (finally)
- macOS is now fully supported and functional (hopefully functional)
- You can now install Porn Fetch into your system (Windows, Linux)
- Proxy Support (very experimental!!!)
- Display thumbnails when searching
- High Performance download mode is now async and allows for much higher speeds while reducing CPU power (only XNXX, XVideos, xhamster, missav.ws)
- Re-implemented the internet and status checks, but in a better way
- Porn Fetch CLI now supports batch processing through arguments
- Porn Fetch CLI is now completely thread-safe and uses rich progressbar
- Porn Fetch CLI now also tracks the total progress with a separate bar
- Allow for optional tag writing
- Allow for different format converting e.g, mov and mkv
- When downloading a new video / loading in and videos are already downloading, the total progress will now be accounted for that
- Make an "evasion" / anonymous mode to hide Porn Fetch from your PC / Android device (Renames elements, so that people can't see you are using it)

## Bug fixes
- Fixed logging encoding error on Windows
- Fixed ffmpeg downloads
- Fixed the progress reporting on the file-read function
- Optimized the CLI and fix some of its errors (#61) (#62)
- Fixed issues with video length parsing
- Fixed output path issue in CLI
- Fixed HQporner / Eporner progress issue stopping at 99%
- Fixed get random video (HQPorner)
- Fixed image URLs for PornHub and improved logging
- Fixed an index issue in the tree widget:
 When a video was loaded in index 1 and a user checked the box for not clearing videos, the next loaded
 Video would have an index of 11, although it should have an index of 2
- Generally stabilized and improved Porn Fetch a lot


## Code improvements and design updates
- Fixed the Porn Fetch layout (this time really, I swear)
- Rename **ALL** UI elements to be more consistent and easier to handle within code
- Huge code refactoring
- improved the tag writing function (with exceptions)
- Generalized the backend Porn APIs to work more equally to optimize Porn Fetch to write lesser lines of code
- Improved code for the part when a video finished downloading
- Made a threading class for every function that could take more time than ~350 ms to prevent UI delays
- Reworked Porn Fetch buttons and some UI design

## Deprecations
- Removed support for Spankbang because the site blocks all requests with a 403 status code
