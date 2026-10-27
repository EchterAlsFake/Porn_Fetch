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

These notes cover the current 3.9 development tree and changes since 3.8, updated through 28 October 2026. This remains a beta: implemented features, automated checks and verified platform builds are distinguished below.

The checkout remains a free sandbox simulation for this beta. These application changes do not enable real payments.

### Supported websites and URL handling

- Added RedTube, Thumbzilla and Tube8 video and profile integration.
- Added EMPFlix and TNAFlix video downloads, metadata and the profile/channel routes each provider exposes.
- The video-provider inventory now covers PornHub, XHamster, XNXX, XVideos, Eporner, SpankBang, YouPorn, Beeg, RedTube, Thumbzilla, Tube8, XFreeHD, Porntrex, EMPFlix and TNAFlix.
- Expanded model, pornstar, creator, user and channel URL handling according to each provider's actual capabilities.
- Added public playlist/collection routing for PornHub, XVideos, YouPorn and RedTube. Thumbzilla has a playlist route and parser, but live playlist verification still needs a usable public fixture.
- Added gallery handling for supported album links in the CLI, including XFreeHD and PornHub.
- Unified provider hostname and content-type routing between the GUI and CLI. Unsupported directories, resource types and tabs produce an actionable error instead of entering the wrong parser.
- Improved handling of localized video paths, profile aliases, explicit video tabs and supported mirror hosts. Relative listing links retain their provider origin.
- Preserve case-sensitive video IDs and distinguish the requested source URL from its redirected transport URL.
- Preserve pagination filters and replace existing page parameters instead of appending conflicting page numbers or nesting resource prefixes.
- Resolve profile identity before reading an AJAX video tab. Follow supported XVideos profile-to-channel redirects and XHamster user-to-creator links.
- Honor PornHub's uploaded/featured source selection when preparing a model or user list.
- Replaced the app's separately maintained Supported Websites page with a browser link to [pornfetch.to/#websites](https://pornfetch.to/#websites).

### Downloads, selection and queue controls

- Rebuilt the desktop download list around per-video quality, selection, status, progress, start, stop, resume and removal controls.
- Added automatic removal of completed desktop downloads from the visible list while retaining their history when tracking is enabled.
- Added manual removal of pending, queued and active entries. Active writers stop before their row is removed, and removing one job does not stop unrelated downloads.
- Fixed visible row numbering so entries no longer all display `1`. Numbers update when entries are removed or completed.
- Fixed column spacing so Stop / Resume and Progress do not overlap regardless of the available window width.
- Made selection, Download Selected and per-row actions use stable job identities as rows are inserted, removed and automatically cleared.
- Improved HLS stop/resume so retained segments and checkpoint progress are reused rather than requested again unnecessarily.
- Fixed RAW resume starting at byte zero after a partial download. The shared downloader now persists checkpoints and resumes with byte ranges when the server supports them.
- Direct-file downloads can use concurrent parts when supported by the server, with configurable bandwidth limits.
- Simplified the option label to **Cleanup on stop** and added adjacent help explaining that deleting partial segments and temporary files prevents later resumption from that progress.
- With cleanup disabled, stopping retains reusable partial data. With cleanup enabled, a later start performs a fresh transfer.
- Completion releases temporary segment/checkpoint data. Fixed cases where finished HLS downloads could retain substantial temporary data in memory.
- Treat native failed-download reports as failures that can be retried, rather than displaying a false successful completion.
- Cancel queued semaphore waits immediately, including jobs stopped before their coroutine first starts. Apply changed parallel limits when idle, deferring changes while active tasks drain.
- Improved HLS joining, progress reporting and handling of streams with unusual timestamps.
- Support YouPorn's direct-file fallback when an HLS stream is unavailable; tests record the transport actually selected.
- Corrected the displayed duration unit: prepared durations are normalized to minutes and displayed without converting them a second time.
- Added the missing 144p filter choice and retained per-video quality selection. The 4K filter corresponds to 2160p.
- Preserve quality entitlement checks in single and selected downloads; higher-quality and parallel-download features require an eligible license.

### Filters and custom output filenames

- Added title, author and tag regular expressions, minimum/maximum duration and quality, publication-date bounds, result limits and start/end source positions.
- Make Start/End inclusive original source positions, applied before filtering. Filenames retain those source indexes even when the visible list is renumbered.
- Apply combined filters together, with case-insensitive regular expressions. Tag expressions can match an individual tag.
- Treat publication-date limits as inclusive calendar dates.
- Validate invalid regexes, dates, reversed ranges and malformed filename templates before starting network preparation.
- Preserve original desktop list titles and author names for display and filtering. Sanitize metadata only when constructing filesystem paths.
- Handle foreign alphabets, emoji, combining Unicode, `/`, `\\`, `|`, reserved Windows filenames, trailing dots/spaces, control characters and very long filenames more safely.
- Prevent title/author metadata from introducing directories or escaping the intended filename component. Directory separators deliberately written in a custom template remain supported.
- Keep a video titled `~` from being interpreted as a request to use the home directory.
- Add the expected media extension when a title contains dots that are not a recognized video extension.
- Implemented the **Options** dialog for custom title formatting, documenting `$title`, `$author`, `$video_id`, `$index`, `$publish_date`, `$length`, `$output_path`, `${name}` syntax and `$$` for a literal dollar sign.
- Connected the keyboard-shortcuts dialog.

### Account login and account collections

- Added XHamster and XVideos account integration alongside PornHub, using the authentication methods each site exposes.
- Reorganized PornHub login so email/password and a full-width Login button come first, followed by one row of history, recommendation, subscription-feed and favorite actions. Username and browser-cookie import are grouped separately below.
- Replaced permanent login-page instructions with a **How to login** dialog explaining the site-specific flow, cookies and browser extraction.
- Import actual browser sessions through `browser_cookie3`; desktop testing includes Brave. Browser-cookie import is not offered as an Android OS feature.
- Verify imported sessions against the server's authenticated state. Cookie presence or constructing an Account object alone no longer establishes a successful login.
- Use PornHub's authenticated account menu to determine the username where needed.
- Fetch PornHub watch history, recommendations, subscription feed and favorites; XHamster liked videos/account playlists; and XVideos watch later, history and liked videos.
- Support XVideos session-token login. XVideos password/CAPTCHA login is not added by this release.
- Fixed XHamster liked-list extraction from embedded account JSON instead of accidentally reading recommendation thumbnails.
- Handle expired/rejected authentication, invalid collections, duplicate actions and cancellation without leaving the account page stuck in a loading state.
- Treat a missing later account-list page as the end of pagination while keeping first-page, authentication and video-metadata failures visible.
- Keep account secrets out of saved download-recovery snapshots and diagnostic result summaries.

### Desktop interface and settings

- Rebuilt the desktop interface in QML, covering downloads, accounts, settings, statistics, licensing and information.
- Added Material appearance, accent colors, dark mode and activity glow, with live updates where supported.
- Align switch controls to the left of their settings control column instead of centering them in the available space.
- Added attributed icons beside the Video, Performance, System, Privacy and UI settings categories.
- Made Tor routing labels and help more prominent.
- Fixed overlapping cards in the information/credits layout and improved resizing behavior.
- Added scrollable dialogs for longer help and notices, including title-formatting guidance and third-party notices.
- Apply logging, preparation delay, cache, retry, network, provider and idle download-concurrency settings to their actual runtime consumers.
- Persist settings to disk and reload them consistently. Language and Material appearance changes update the live QML interface; settings that need a restart still explain that requirement.
- Added a first-run beta disclaimer with a 30-second reading period in desktop, Android and CLI flows.
- Added an explicit first-run choice for optional error reporting, with privacy-sensitive details redacted from reports.
- Improved anonymous mode so sensitive video details and widgets are hidden when enabled.

### Download history and statistics

- Rebuilt desktop tracking with a local PocketBase service and added a statistics dashboard. The CLI can discover or install PocketBase; legacy SQLite records can be imported.
- Track prepared videos, completion, stopped/failed transfers, retries and their originating profile or playlist.
- Update an existing history entry when a job resumes or retries instead of creating duplicate completion records.
- Preserve the source name and URL so statistics can group downloads by model, channel or collection.
- Make Statistics Refresh reload the database cache asynchronously instead of only repainting old values.
- Keep history after a video is removed from the download list, and retain it across normal application restarts.
- Honor disabled tracking and anonymous presentation. Android does not start a download-history database.
- Share database signal wiring between normal startup and diagnostic workflows so initialization failures and busy state are handled consistently.
- Fixed generated PocketBase passwords beginning with `-` being parsed as command-line options.

### Desktop shutdown and paused-job recovery

- Added coordinated teardown for normal window closing: stop active downloads cooperatively, cancel queued work, save the queue, flush history and close provider sessions and PocketBase.
- Restore unfinished desktop rows as **paused** after reopening. Transfers resume only when the user explicitly clicks Resume.
- Restore job identity, output paths, chosen quality and retained progress without making provider requests during startup.
- Obtain a fresh native provider object when Resume is clicked, rather than serializing live sessions or provider objects.
- Discard incompatible HLS state if the selected or permitted quality has changed.
- Store queue snapshots and native HLS state in a writable application cache directory instead of depending on the current working directory.
- Write recovery metadata atomically and exclude cookies, passwords and native objects from it.
- Flush pending history before moving its database directory during shutdown.
- These changes concern normal close/reopen behavior; forced-kill and power-loss recovery are outside the implemented test scope.

### Networking and privacy

- Moved the provider network layer to asynchronous `curl-cffi` through `eaf_base_api`, with browser impersonation, HTTP-version selection, retries, caching and shared proxy handling.
- Added HTTP, HTTPS and SOCKS proxy configuration with a desktop connection test.
- Added configurable DNS over HTTPS, primary/fallback resolvers, Encrypted Client Hello, network-interface binding and browser-style TLS fingerprints. Optional desktop SNI obfuscation modes remain available.
- Apply provider-session changes without requiring a restart, then close replaced sessions and their background tasks.
- Honor the configured fallback DNS-over-HTTPS resolver after primary-resolution failure.
- Added managed Tor routing choices: Off, updates/licensing only, or all app traffic including provider requests and media downloads.
- Start an app-owned Tor client on demand, show bootstrap progress, and stop routed requests on failure rather than falling back to a direct connection.
- In all-traffic mode, use remote SOCKS hostname resolution, keep PocketBase loopback requests local, and prevent custom proxies, interface settings, environment bypasses or QUIC from silently changing the selected route.
- Require acknowledgment before routing bandwidth-heavy video downloads through Tor. External browser links and other applications are outside Porn Fetch's route.
- Added clearer service-failure notices distinguishing Tor startup problems, an unreachable service and temporary server errors, with repeated notifications grouped.
- Refreshed dependencies and the lockfile, including the shared downloader fixes now present in published releases.

### Automatic updates

#### Desktop GUI

- Added automatic update handoff for installations managed by Qt Installer Framework. The old macOS Sparkle updater has been removed.
- Check signed release metadata and download/hash-verify the repository metadata and payloads into local staging before launching the Qt Maintenance Tool.
- Reject external payload substitutions and do not offer automatic installation from unauthenticated fallback update information.
- Close PocketBase and provider sessions before the updater handoff to reduce locked-file failures, particularly on Windows.
- Display the current release notes as Markdown in the update dialog, verifying the downloaded notes against the signed release metadata.
- Check update eligibility against the release timestamp. Portable/source installations retain their appropriate manual update method.

#### Standalone CLI

- Added `self-update --check`, interactive `self-update`, and `self-update --yes` for supported standalone binaries.
- Verify signed updates through The Update Framework (TUF), then replace the executable and bundled PocketBase with a separate update helper.
- Keep previous files and a staging result for recovery and diagnosis if installation fails.
- Fixed standalone certificate-bundle discovery and added visible update download progress.
- Leave source checkouts and package-manager installations to their original update method.

#### Android

- Added a separate signed Android TUF feed with APK architecture, package, version, release timestamp and hash metadata.
- Verify the downloaded APK, update entitlement and signing identity before handing it to Android's installer through a read-only content URI.
- Let Android request installation permission and final confirmation; updates are not installed silently.
- Preserve the installed application if an update is cancelled or verification/download fails.
- Android update and installation flows still require validation on real devices and built APKs.

### CLI workflows

- Rebuilt the terminal app around separate flows for videos, profiles/playlists, account access, settings, licensing, tracked sources, history and statistics.
- Keep CLI and shared services free of Qt dependencies so they can run on headless systems, including Termux.
- Accept multiple supported source URLs in batch mode, with quality/output overrides and optional continuation past failed entries.
- Track model/profile pages, scan for new videos and manage a pending download queue.
- Added pause, resume and cancel controls, including saved paused jobs that can continue in a later CLI session.
- Improved progress display, optional MP4 metadata writing, unavailable-video reporting and normalization of provider quality APIs.
- Added explicit offline/provider/download diagnostics and a shared interactive test selector.

### Provider-library fixes used by Porn Fetch

These are the provider versions required by the current application manifest. The summaries cover changes used by Porn Fetch's own video, account, profile, collection, gallery or download paths.

#### [PornHub 5.4.6](https://github.com/EchterAlsFake/unofficial-api-for-pornhub/blob/master/CHANGELOG.md)

- Corrected regular-user upload routes and made profile listing extraction more resilient.
- Improved normalization of embedded and relative video links and extraction of localized profile statistics.
- Improved author handling for the video/short types consumed by the app, including channel authors.
- The live-test guard now lets recognized PornHub math challenges reach the existing native `eaf_base_api` handler. It previously stopped the response before that handler could run.
- Corrected pagination-test identities to retain PornHub's public `viewkey`; stripping every query parameter had made different videos appear identical.

#### [XHamster 2.6.5](https://github.com/EchterAlsFake/unofficial-api-for-xhamster/blob/main/CHANGELOG.md)

- Restored shorts/moments extraction from current page data and DOM layouts, preserving regional hosts and the correct profile listing route.
- Read hydrated listing metadata so later cards retain their thumbnails and durations.
- Improved Full HD/UHD recognition and handling of missing short metadata.
- Includes the earlier account-JSON extraction fix used for liked videos, and reports rejected credentials as a failed login.
- Updated the app's pagination test to allow a real overlapping page prefix while still requiring a new later-page video; a fully repeated page still fails.

#### [XNXX 2.4.4](https://github.com/EchterAlsFake/unofficial-api-for-xnxx/blob/master/CHANGELOG.md)

- Read video metadata from JSON-LD arrays and graph objects.
- Handle empty profiles without division-by-zero errors and close profile scrapers when iteration stops early.
- Preserve canonical video identity when listing click links contain a separate tracking token.

#### [XVideos 2.5.3](https://github.com/EchterAlsFake/unofficial-api-for-xvideos/blob/master/CHANGELOG.md)

- Return actual listing thumbnails and decoded titles, decode HTML entities in profile JSON, and exclude cards that are not videos.
- Handle empty channels and model/profile aliases more consistently.
- Expose uploader names from video-page metadata. Porn Fetch uses those names instead of making a separate author/statistics request for every prepared row, retaining the native lookup when the name is unavailable.
- Close the inner profile scraper when iteration ends early, preventing leftover prefetches from racing later requests.
- Support the author-helper calling conventions consumed by shared metadata preparation.

#### [Eporner 2.5.3](https://github.com/EchterAlsFake/unofficial-api-for-eporner/blob/master/CHANGELOG.md)

- Correct listing IDs, embed links, keywords, thumbnails and duration types.
- Select download qualities for the requested codec and handle absolute media URLs correctly.
- Tolerate additional JSON-LD shapes and optional metadata.
- Recognize localized video paths, German/French profile statistics and missing channels that incorrectly return HTTP 200.
- The app now reads Eporner's real quality method instead of requesting a nonexistent `video_qualities` dataclass field.

#### [SpankBang 2.4.4](https://github.com/EchterAlsFake/unofficial-api-for-spankbang/blob/master/CHANGELOG.md)

- Use more conservative listing concurrency and standard navigation headers.
- Improve regional profile paths/statistics and thumbnail, duration and stream-data parsing across page layouts.
- Retain earlier quality-detection improvements, including 4K stream identification.
- Desktop workflows remain marked manual until separately verified; a parser update alone does not establish working browser/CDN playback.

#### [YouPorn 1.8.3](https://github.com/EchterAlsFake/unofficial-api-for-youporn/blob/main/CHANGELOG.md)

- Handle empty listings, partial collections and users without public collections safely.
- Resolve absolute collection links without duplicating the provider hostname.
- Avoid loading unrelated title/name fields just to log helper operations used during metadata/collection handling.
- Correct duration normalization so minute values are not multiplied into incorrect validation expectations.
- Retain direct-MP4 fallback handling alongside HLS downloads.

#### [Beeg 1.7.4](https://github.com/EchterAlsFake/unofficial-api-for-beeg/blob/main/CHANGELOG.md)

- Preserve video keys in links copied from tag pages and retain significant trailing zeros.
- Expose author, tags, thumbnails and publication dates for consumers such as CLI metadata preparation.
- Return a useful unavailable-video error for missing/malformed API metadata instead of an indexing exception.

#### [RedTube 1.4.4](https://github.com/EchterAlsFake/unofficial-api-for-redtube/blob/main/CHANGELOG.md)

- Recognize playlist video containers as well as profile grids, rather than extracting zero videos from a populated playlist.
- Normalize supported profile routes and improve localized statistics and playlist counts.
- Return actual thumbnail URLs instead of lazy-loading placeholders or unprocessed `srcset` strings.
- Load optional uploader/performer data more safely and remove duplicate performer entries.

#### [Thumbzilla 1.4.3](https://github.com/EchterAlsFake/unofficial-api-for-thumbzilla/blob/main/CHANGELOG.md)

- Handle missing optional playlist metadata and short statistics layouts without crashing.
- Added parser regression coverage for playlist metadata; live playlist support remains unverified without a usable public fixture.

#### [Tube8 1.3.3](https://github.com/EchterAlsFake/unofficial-api-for-tube8/blob/main/CHANGELOG.md)

- Stop interpreting subscriber totals as video counts, including on French channel pages.
- Reject empty User pages instead of accepting generic session data as a valid profile identity.
- Keep public User-feed verification separate from working video, channel, pornstar and amateur routes.

#### [XFreeHD 1.7.4](https://github.com/EchterAlsFake/unofficial-api-for-xfreehd/blob/main/CHANGELOG.md)

- Normalize relative and embedded video/album links, return qualities consistently and accept numeric quality aliases.
- Tolerate optional ratings/duration metadata and expose private-video status without a metadata parser crash.
- Handle empty albums and invalid image-page numbers safely.
- The app reads the native quality method rather than a nonexistent lazy dataclass field.

#### [Porntrex 1.8.3](https://github.com/EchterAlsFake/unofficial-api-for-porntrex/blob/main/CHANGELOG.md)

- Recognize MP4 media URLs with signed query strings or fragments while preserving the tokens required to download them.
- Retain the corrected profile pagination and provider-origin handling used by model/channel preparation.

#### [EMPFlix 1.0.1](https://github.com/EchterAlsFake/unofficial-api-for-empflix/blob/main/CHANGELOG.md)

- Resolve short and embedded video links to a full watch page when metadata is missing.
- Return the appropriate profile/channel/pornstar identity for supported author links.
- Keep channel authors out of category/tag lists and parse abbreviated rating counts safely.
- Added parser fixtures for the supported page layouts.

#### [TNAFlix 1.0.1](https://github.com/EchterAlsFake/unofficial-api-for-tnaflix/blob/main/CHANGELOG.md)

- Follow canonical watch links when short/embed pages omit required video details.
- Normalize video/profile/channel/pornstar identities and support the author helpers used by metadata preparation.
- Keep channel authors out of tags/categories and tolerate missing source-size attributes and abbreviated rating counts.
- Added parser fixtures for the supported page layouts.

### Shared API/download engine

- Require [eaf_base_api 4.2.5](https://github.com/EchterAlsFake/eaf_base_api/blob/master/CHANGELOG.md), including resumable RAW downloader changes previously available only in the source checkout.
- Preserve resumable byte offsets/checkpoints and validate ranged responses instead of silently treating a restarted RAW transfer as resumed progress.
- Sanitize automatic download filenames and provide a safe fallback when no title is available.
- Fixed contextual logging failures for URLs containing percent escapes.
- Load metadata through explicit sources/fields, retaining clear errors for unresolved or unavailable values instead of relying on legacy `.load()` behavior.
- Keep request/download error context consistent across providers, with bounded retries and explicit unavailable-resource handling.
- Bound asynchronous page/item work, preserve original order where requested, and clean up unfinished scraper tasks.
- Keep the native PornHub math handler, retry budget and cooldown behavior in the shared library; the app's test guard does not implement a second solver.

### Test coverage and diagnostics

Added substantial offline and opt-in live coverage around the production GUI, CLI, provider libraries, filesystem and local database. Positive live paths use actual requests and media; protocol/error contracts and unusual-title fixtures are explicitly separate.

| Area | Implemented checks |
| --- | --- |
| Offline and Qt integration | URL routing, provider adapters, input validation, persistence, real QML bindings, settings consumers, error/cancellation recovery, update verification and application startup |
| Provider/profile metadata | All 15 video providers, supported shorts/galleries, and a 76-case profile URL/alias/localization inventory feeding actual GUI models |
| CLI download lifecycle | 30 pause/resume and cleanup/restart workflows across 15 providers, using the native HLS/RAW transport selected by each provider |
| Desktop download controls | 42 automated workflows across 14 providers: real controls, progress, quality, stop/resume, cleanup, removal and completion clearing; SpankBang is a separate manual exception |
| Queue/concurrency | Three multi-video workflows using real HLS/RAW transfers, limits 1/2, duplicate starts, queued cancellation and isolation when active jobs are stopped/removed |
| Desktop settings | Persistence checks for 55 settings, independent disk reads/reloads, active provider configuration and observable effects; optional Tor/Strict SNI effects require their own environment |
| Statistics/history | Eleven workflows covering actual PocketBase records, aggregates/source groups, retry/resume updates, privacy, refresh, restart persistence and disabled/error states |
| Advanced controls | Eleven groups using real video metadata, regex/range/date/quality filters, templates and a real formatted download, plus 25 explicit synthetic unusual-title fixtures |
| Normal teardown/recovery | Eight workflows in 16 independent GUI processes, covering preparation, pending database writes, database moves and retained/cleaned HLS/RAW transfers |
| Public model/playlist workflow | 16 automated source workflows from input through limits/filters/ranges, cancellation, native later-page rows, selected media and source history/statistics; SpankBang is manual and Thumbzilla playlists remain unverified |
| Account controls | Default 36-check desktop/mobile-QML action inventory, real browser-cookie sessions and account lists, list metadata, tokens, help, busy state, cancellation and errors; optional private-playlist verification and separate local password checks |

- Added `uv run src/tests/helper.py` selections for the live suites, with explicit network, media-download and browser-session confirmations as appropriate.
- Live download checks observe actual HTTP range/segment reuse and use FFmpeg to verify a readable output video stream and plausible duration. They do not substitute fake successful transfers.
- Isolate settings, outputs, queue snapshots and PocketBase data from personal application state. Save JSON reports, stages, library versions and diagnostic logs for follow-up.
- Keep live suites out of ordinary unit/integration discovery and CI. Ordinary integration tests include offline GUI contracts that reject network calls.
- Handle HTTP 429 with a minimum 30-second cooldown, longer `Retry-After` values when supplied, and at least five seconds between requests after rate limiting; retries of safe reads are bounded.
- Stop on explicit access denials, CAPTCHA pages and unsupported scripts. Let only recognized HTTP-200 PornHub math payloads on HTTPS PornHub hosts reach the existing native handler, recording delegations without cookies/tokens.
- Detect genuinely repeated pagination while permitting real overlapping entries at page boundaries. Retain public IDs such as PornHub `viewkey` in hashed video comparisons.
- Require actual authenticated server state for account success and explicit anonymous-denial evidence before claiming a private playlist is authorized correctly.
- Add line/branch reporting through `coverage`, including an HTML report when requested. Workflow/checklist counts are not a claim of 100% Python line or branch coverage.
- Treat failed, blocked, skipped, manual and unverified cases as distinct outcomes. External website changes, unavailable fixtures and expired sessions remain visible instead of being counted as passes.
- The focused PornHub model and playlist rerun passed after the guard/identity corrections; the latest integration run completed 165 tests with one existing skip. These are verification snapshots, not a blanket all-platform or all-suite success claim.

### Android, packaging and release workflows

- Replaced the old Kotlin Android app with an experimental QML layout featuring phone/tablet navigation, download cards, safe-area/layout work and file export through Android's picker.
- Added GitHub Actions APK jobs for arm64-v8a, armeabi-v7a, x86_64 and x86. Android-only workflow selection is available alongside desktop GUI, CLI and combined builds.
- Updated the Android build path for Python 3.14 and matching PySide6/Shiboken wheels, with checksum verification before deployment patches.
- Fixed native dependency recipes, target-ABI cryptography builds, Android command-line-tool discovery and clean-build registration of the Qt activity JARs.
- Preserve maintained native recipes outside deployment cleanup, and keep build failures visible through shell pipelines and per-ABI diagnostic artifacts.
- Added APK signing with a persistent signing identity, signature verification and checksum sidecars. Publishing requires signed APKs; unsigned build artifacts are explicitly diagnostic.
- Added website release publication and the signed Android update feed, including publication-only retries from existing successful build artifacts without recompiling them.
- Stamp one release version and original workflow timestamp into the binaries, update metadata and release assets; workflow reruns retain that timestamp.
- Allow separate GUI/CLI builds, and include only successful target artifacts in signed update repositories.
- Add offline CI gates, compiled GUI/CLI smoke checks, platform bundle checks, and post-upload signature/hash/download verification before release publication.
- Improved macOS runtime/plugin packaging and Intel/ARM64 bundle checks, and fixed installer archive handling for paths containing spaces.
- Package PocketBase, optional installer components, third-party notices and managed Tor runtimes where supported. Keep Android/device and platform-specific runtime verification separate from workflow lint.
- Refresh signed update metadata between releases and support retrying website publication using retained artifacts.
- The current source uses the Porn Fetch Source-Available License 1.0. Provider/shared API libraries use AGPL; the existing GPL 3.8 release retains its original license.
- Moved application service, update and website links to `pornfetch.to`.

### Removals and remaining limits

- Removed in-app keyword search, thumbnail display and the Eporner tools screen. Upstream library capabilities do not automatically become app features.
- Removed HQPorner, MissAV and Porngo from the application's supported-site list, and removed the kill-switch feature.
- Removed the old macOS Sparkle update path and the former Kotlin Android application.
- Linux s390x/ppc64le and Windows x86 builds remain paused where required networking binaries are unavailable or fail their build/runtime checks. Experimental targets are published only after their own checks succeed.
- SpankBang desktop workflows remain manual; Thumbzilla public playlists need a fixture; a working Tube8 public User feed is not claimed from generic profile/session markup.
- Recent live diagnostics still require follow-up for the XFreeHD desktop RAW-resume reuse assertion and a Tube8 User fixture. XVideos cookie checks depend on a currently authenticated browser session. These outstanding checks are not described as fixed by the other API updates.
- Tor/Strict SNI live effects, Android device behavior and packaged CLI/GUI installation/update behavior need their respective environment/build verification. Desktop-rendered mobile QML checks do not establish Android OS/device coverage.
- Licensing lifecycle retesting and forced-kill/power-loss recovery were not added to the new live matrix. Android device testing remains deferred while that platform is experimental.
