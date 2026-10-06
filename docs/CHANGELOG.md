# 1.0
Initial Release

# 1.1
- Code refactoring
- Added Support for downloading a whole channel / user
- Fixed an Issue with the progress bar
- Fixed typo issues
- Fixed the output path issue
- Changed License to LGPLv3 (The reason for this is, that I am stupid and I used the wrong license. Creative Commons is not valid to be used for developing with Qt. I didn't know that, I am sorry...)

# 1.2
- Added additional stuff to the metadata function (Likes, Image URL, Tags)
- Added border colours for input fields

# 1.3
- Added Threading Modes
- Single: Downloads will be executed within the main thread, and the GUI won't respond to your actions if the download isn't finished.
- Multiple: Download(s) will be executed with separate Threads (QThreads). This is mostly intended for single downloads. You can use that function also for multiple downloads, but that will ruin the progress bar, because it will jump between the different videos.

# 1.4
- Changed UI (stackedWidget)

# 1.5
- Added CI 
- Made Readme.md and Build process simpler to understand

# 1.6
- Fixed 7 Bugs
- CLI is more stable
- Code refactoring
- Handling API timeout in Search function
- Created Security.md
- Created ROADMAP.md
- Created ISSUES.md
- Compiled Versions now compiled with Python 3.11.4


# 1.7
- Implemented an automated fix for the IndexError exception
- Improved overall code quality
- Split the code into multiple files, to be better readable 
- A lot of grammar fixes
- Added native support for Termux (See building from source : Android)
- Changed Qt Version from 6.5.1 to 6.5.2
- Changed Python version from 3.11.3 to 3.11.4
- Added automatic error reporting with Sentry.io
- Changed License to GPL 3
- Added CI/CD Actions for build and security checks
- Made the Readme.md A LOT more readable and more professionally
- Added license agreement script (implemented in 1.8)


# 1.8
- Implemented final License agreement
- Persistent settings (untested)
- Added Ubuntu to Install script
- Added installation script
- Added arch linux to install script
- Typo and grammar fixes
- Added Icons and images
- UI redesign
- Added some basic exceptions

# 1.9
- Fixed OS Error issue
- Added function to strip out special symbols in title, to prevent path issues

# 2.0
This release exists, but I don't remember the changes anymore.

# 2.1
- A complete new UI design
- UI is more fluent / flexible
- API updated to v3.1
- Thanks to Egsagons Update, most errors are fixed now
- Fixed Connection Error
- You can change the API language 
- You can change the UI language (only english supported now, see contribution for more)
- Added Keyboard shortcuts
- UI is much smaller now
- removed icons
- added more dependencies
- little bit code refactoring
- removed borders
- better windows support
- better automatic error handling
- included sentry reporting to more sections of the code
- added more filters, to prevent OS Error

# 2.2
- You can now log in with your PornHub Account
- You can now fetch your watched, liked, and recommended videos for your PornHub Account
- updated the CLI a little bit (not finished. It's my priority for the next release)
- API updated to v3.1-1
- a lot of typo fixes
- removed Security.md, because it was useless, and I don't really remember why I even added it
- added all files to the release page (thanks to Egsagon for telling me that I should do that :)

# 2.3
- fixed some issues...


# 2.4
- If you use the file / model - user - channel functionality, then the TreeWidget will be used
  to let you select the videos that you want to download instead of downloading everything
- fixed an issue in the termux build script
- API updated to v3.1-4
- You can now select if you want to have a delay or not (enabling it is recommended!)
- OS error is fixed (FOR REAL!)
- Sentry strips out sensitive information and now only the exception, lines of code, server name is reported
  (Although I need to still test that.)

The next update will focus more on features / compatibility to other systems.
I hope that most issues are now fixed.

# 2.5
- Added search filters
- Move settings to a new page of stacked Widget
- Added keyboard shortcut and some buttons for it
- API Updated to v3.2
- Added function for downloading the thumbnail
- Fixed an error with the metadata function
- Removed file logging
- Recoded CLI

# 2.6
- API Updated to v3.2.1
- Redesign of the settings widget
- removed some things from the roadmap
- added a connection error exception

# 2.7
- API Updated to v4
- Huge stability and performance boost
- fixed setting Delay not working issue
- fixed #4 connection error / model error

# Version 2.8 Update Notes

### New Features:
- Added support for HQPorner.com.
- Introduced dynamic colors for CLI.
- Created STATUS.md for tracking upcoming releases.
- Implemented help buttons for threading and "high speed" (previously known as Delay).
- Added user metadata and info functionality.
- Included a new logo.

#### Interface & Design:
- Rolled out the final app design.
- Integrated qt resource file for better icon handling.
- Improved stylesheet logic in the GUI (reduces code by approx. 1500 lines).
- Unified to a single tree widget for all functionalities.

#### Performance & Efficiency:
- Removed 'get_graphics' function, enhancing UI start speed and eliminating setup requirement.
- Adjusted "Delay" to "High Speed" for clearer understanding.
- Defaulting to maximum api requests possible for faster downloads
- API updated to v4.1

#### CLI Updates:
- Updated CLI to version 4.1.
- Entirely refactored CLI.
- Fixed issues with Termux CLI build.

#### Build & Integration:
- Improved dependency handling in the build script.
- Added support for iSH in the build script.
- Integrated kivy build with CI/CD.

#### Removals & Deprecations:
- Eliminated Sentry from the project.
- Deleted unnecessary files: DOWNLOADS.md, ISSUES.md.
- Discontinued transparency support.
- Modified several minor elements in various files.

#### Miscellaneous:
- Updated thumbnail download to align with PHUB v4.
- Note: This Readme has been crafted with assistance from ChatGPT for professionalism.

#### Android:
- API Update to PHUB v4.1 from py-3.9 branch using custom fork
- You can now just paste the URL from the clipboard
- You can now choose the output folder without needing to enter it in to the input line
- improved visual look and progressbar

# 2.9
- API updated to 4.1.3
- Added Enhancement request from #11 (Skips already downloaded videos...)
- huge Performance increase when downloading (thanks to Egsagon's threaded preset) 
- Added a Semaphore (only 4 threads at once -- less overload and less CPU burning)
- Added Avatar downloading 

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


# 3.1

# Features / Improvements
- Added playlist support #20
- Added model for EPorner
- Error handling if wrong URL was entered
- Added Disclaimer to the License agreement
- Added more ui popups into the translations
- Updated **ALL** Stylesheets. The GUI now looks a LOT better
- implemented logic, so that user can't log in to PornHub without entering actual credentials
- Added searching support for EPorner
- Implemented update mechanism
- Implemented a factory reset for the settings
- Reimplemented back the client delay (optional)
- Redesigned settings widget
- Added get_by_category for EPorner
- Added a setting for specifying the workers and timeout in the threaded preset


# Bug Fixes / Issues
- Fixed an issue, where the settings were displayed, instead of the download tab
- Fixed total progress callback for processed videos in file mode
- Fixed the issue that the downloaded ffmpeg .zip wasn't deleted on windows
- Fixed callback progress for HQPorner
- Fixed the total progress for FFMPEG
- Fixed the FFMPEG type error #21
- Fixed individual progress for FFMPEG
- Fixed searching (result) limit
- Fixed total progress for loading objects and stuff
- Handling `Client.call failed after 4 attempts`
- Fixed an issue that video reversing is not working
- Fixed overflow error
- Progress now gets only updated all 0.5 seconds
- Some issues in the CLI

# Code related
- Renamed UI widgets so that they make more sense
- Improved the load style function
- Added code comments
- Code refactoring (refactored all Signals)

# Android
- [x] Fixed the threaded presets for Android (may or may not work...)


# 3.2

## New Features
- Disabled limits in the settings e.g., the search limit
- You can now apply your own values for the timeout, max workers, delay and other network settings
- You can now export Video URLs from the tree widget directly into a file
- You can now stop loading video objects by clicking the button
- Porn Fetch is now able to install ffmpeg automatically for you. Go to the settings to do this.
- Added Searching support for xnxx
- Added Model support for xnxx
- Porn Fetch will now automatically write some metadata to the files and convert the .ts files into a valid .mp4 header file.
  (This requires FFmpeg. If it is not installed, it will be skipped.)

## Bug Fixes
- Fixed the Overflow Error
- Fixed logger debug / error connections (only relevant for local development with Android)
- Fixed several typo issues, e.g., #34
- Fixed some PHUB errors related to #33 #30 #27 #12 #4


## Other
- Rewrite of the README
- Rewrite of the CLI of Porn Fetch
- A lot of code optimizations

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

# 3.4

## New Features
- Added support for spankbang
- You can now choose between user uploads, featured videos or both of them when downloading from a PornHub model account
- You can now decide if already existing files will be skipped, or if the title will be slightly changed to download both of them
- Thumbnail of videos will be written into the mp4 file
- You can now automatically select all videos from an author by a certain name

## Design
- switched the sidebar to a top bar (looks better)
- removed the progressbars at the bottom, but added a second widget for it (more space)
- added a new button into the menu which can switch to the previous mentioned widget
- fixed the whole layout for the desktop application. 
- Video titles will now be shown in the progress report in the CLI

## Deprecations
- removed internet checks, because it triggers AV
- removed status bar at the top, because it's useless
- removed discord rich presence. I don't even remember why I added it :skull:

## Bug fixes
- Fixed a bug where you couldn't search on xvideos
- Porn Fetch now handles 2002 errors from PornHub (when a video is blocked in your region) Thanks #44 @WatsonSola
- Fixed several issues in the tag writing function (The thing that converts the video with ffmpeg)
- All APIs will now use infinite paging, so that always all videos until the defined search limit will be fetched
- Fixed playlist downloading
- Fixed file progress
- Fixed an issue where the semaphore wouldn't release in the CLI which makes downloading almost impossible, because
the thread is permanently locked
- Fixed the build scripts for Windows and Linux | Thanks @omar-st [Pull Request #48](https://github.com/EchterAlsFake/Porn_Fetch/commit/2d9cc2885c1383369020a5c26e957fe5cdf0f886) [Related Issue #46](https://github.com/EchterAlsFake/Porn_Fetch/issues/46)>

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


# 3.7

### New Features
- Added Video downloading support for YouPorn.com
- Support for XHamster shorts (moments)
- Added Pornstar, Channel, Searching support for YouPorn.com
- Added Playlist support for YouPorn.com
- Added Searching support for missav.ws
- Added Searching support for Spankbang.com
- Added Playlist support for xvideos.com
- Added Channel, Creator and Pornstar support for xvideos, spankbang and xhamster
- You can now track videos in a SQL database
- You can now change font size (actually)
- Screen reader support (in theory)
- You can now switch UI themes (experimental, still needs work)
- Increased scraping speed for all non-PornHub requests A LOT (seriously)
- You can now control how many pages and videos are fetched at the same time
- Http2 support 
- Brotli compression support

### Bug fixes
- Fixed CLI being stuck when file already exists
- Fixed AV1 decoding for XHamster
- Fixed m3u8 URL for XHamster 
- Fixed thumbnail display
- Fixed range selector widget
- Fixed 429 and 403 errors (mostly)
- Fixed PornHub pagination
- Fixed URL export function

### User Interface
- Completely new design (finally good)
- You can now select quality per video
- Font sizes scale correctly now, thanks to point size
  instead of pixels
- Redesigned the settings widget (compact now)
- Replaced radio buttons with QComboBoxes (much better)
- Improved QCheckbox visibility

### Internal code
- Massive rewrite of the network backend
- Much more consistent network requests and retrying
- automatic 429 bypass
- Improved proxy support
- SSL certificate will now be taken from the OS instead of certifi
- AND SO MUCH MORE!

### Deprecations
- Android support (it's just not good enough)
- File processing (I don't see the benefit) 

### Final words
This release comes with a lot of features, new supported websites,
a new UI design and a refactored backend.

But there are still problems. The CLI is almost untested,
The progressbar system is still inconsistent and the error reporting
too. The translations are also completely out of date and need
to be refactored. 



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



# V 3.9 (in development)

These notes cover the changes since 3.8. The current 3.9 source is still being worked on and is not yet fully functional; the latest published download is 3.8. Some new builds and features have not yet been tested on every platform.

### New Features
- Added RedTube, Thumbzilla and Tube8. You can give Porn Fetch a video or profile URL from these sites; RedTube and Thumbzilla also have playlist support.
- The supported sites now cover more kinds of links, including XFreeHD albums and model, channel and collection pages where the site provides them. Available features still vary by website.
- Added account access for XHamster and XVideos alongside PornHub. You can use site credentials, session tokens where required, or cookies from a supported browser, then fetch collections such as liked videos, favorites and watch history where available.
- Added filters for profile and playlist fetching: duration, title, author, tags, quality and publication date. You can also limit the number of results.
- Downloads now have more reliable stop and resume controls. Unfinished downloads can keep their partial data, including HLS segments, so you can continue them later. You can choose to clean up the partial files when stopping.
- Direct MP4 downloads can use several parts at once when the server supports byte ranges. A working speed limit is available too.
- Added HTTP, HTTPS and SOCKS proxy options, with a connection test in the desktop app. Changes to network settings refresh the site connections without restarting the app.
- Added settings for DNS over HTTPS (Mullvad by default), Encrypted Client Hello, binding to a network interface, and browser style TLS fingerprints. Desktop users can also try the optional SNI obfuscation modes.
- Rebuilt the local download history and added a statistics dashboard. On desktop, tracking uses PocketBase and can import records from the old SQLite database. The CLI can find or install PocketBase for you. Tracking can be turned off.
- The new beta license screen can import and check license files in both the desktop app and CLI. The planned first beta uses a test checkout with no real payment; 1080p and higher quality and parallel downloads require a test license.

### Bug Fixes
- Fixed a case where a finished download could leave gigabytes of temporary data in memory.
- Fixed several cases of blocked or failed website requests by updating browser impersonation, request handling and TLS settings.
- Fixed pagination and page ordering problems when fetching large profiles or collections.
- Fixed HLS downloads sometimes failing while stopping, resuming or joining segments. Progress updates and videos with unusual timestamps are handled more reliably.
- YouPorn videos with a direct file instead of an HLS stream can use the direct download path.
- Fixed quality detection and selection on several sites, including PornHub's incorrect resolution calculation and SpankBang's 4K options.
- Updated site parsers after layout changes. Video, profile and playlist pages now have better fallbacks when a field is missing or a website changes its markup.
- More sites now return useful details such as the author, tags, publication date and available qualities, which helps with filters, filenames and metadata.
- Removed Eporner and XFreeHD videos now give a clearer unavailable-video error. Invalid XHamster credentials are reported as a failed login instead of a successful one.
- Improved custom filename formatting and tightened download paths so a video title cannot write outside the chosen download folder.
- Improved cleanup of replaced network sessions and background tasks when settings change or the app closes.

### User Interface
- Rebuilt the desktop app in QML, including the downloads, account, settings, statistics, license and information pages.
- Added Material style, accent colors and theme changes while the app is running. Most settings now apply immediately; the app still tells you when a restart is needed.
- The download list shows each video's status, progress and quality, with controls to select videos, download them, stop them and resume them.
- Added a dedicated proxy window that checks the address and tests the connection before it is used.
- Added a first-run choice for error reporting. Reports are optional and redact common private details before sending; you can change the choice later in Settings.
- Improved anonymous mode so the desktop app hides video details and sensitive widgets when it is enabled.
- Started a new QML Android layout with phone and tablet navigation, download cards and a folder picker for completed files. Android history uses a local SQLite file. This is development work: there is no 3.9 APK in the current desktop build workflow.

### CLI
- Rebuilt the terminal app around an interactive menu with separate screens for single links, profiles and playlists, account access, settings, licenses and download history. It runs without Qt, including on headless systems such as Termux.
- Batch mode accepts multiple video, profile and playlist URLs, with quality and output overrides, automatic processing and an option to continue past failed items.
- You can track model and profile pages, scan them for new videos and download the pending queue. The CLI also shows download history, failed downloads and statistics when tracking is enabled.
- Added pause, resume and cancel controls, including saved paused jobs that can be resumed in a later CLI session.
- Reworked download progress and optional MP4 metadata writing. Added an opt-in self-test command for checking providers and downloads.
- Standalone CLI builds can check for and install signed updates with `self-update`. Source checkouts and package manager installs continue to use their own update method.

### Code Optimizations
- All of the site APIs used by Porn Fetch are asynchronous now. The app can fetch pages and video details concurrently without tying up the interface.
- Rebuilt the shared API library around `curl-cffi`, with HTTP/2 and HTTP/3 options, browser impersonation, retries, caching and shared proxy handling.
- Site APIs now load only the video details they need and use smaller data models. The shared scraper can process pages concurrently, preserve the original order when needed and clean up unfinished tasks.
- Shared download and request errors now carry clearer context across the site APIs, making failed links easier to diagnose.
- Moved the GUI, CLI, database and licensing code into separate modules. The CLI and shared services no longer need PySide6 to start.
- Updated the development source to Python 3.14 and added offline tests and build checks for the rewritten code.

### Other
- Desktop installer work has moved to Qt Installer Framework; the old macOS Sparkle updater has been removed. Installed desktop builds use the Qt maintenance tool for updates.
- Reworked the build and release workflows, including packaging for PocketBase, third-party license notices and signed CLI update files. Experimental build targets are only published after their build and smoke checks pass.
- The 3.9 application source uses the Porn Fetch Source-Available License 1.0. The site APIs and shared API library have moved to AGPL; the already published 3.8 GPL release keeps its existing license.
- Moved the project's update and service links from `EchterAlsFake.me` to `pornfetch.to`.

### Deprecations
- Removed in-app search, thumbnail display and the Eporner tools screen as part of the project's legal changes. You can still use direct links to supported content.
- Removed HQPorner, MissAV and Porngo from Porn Fetch's supported sites.
- Removed the kill switch feature.
- Removed the old Kotlin Android app while the new QML Android version is being developed.
- Paused some older experimental build targets, including Linux s390x and ppc64le, because required networking dependencies are unavailable for them.
