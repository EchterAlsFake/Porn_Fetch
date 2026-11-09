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
- Added release progress tracking, now maintained in the [server checklist](https://pornfetch.to/checklist).
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



# 3.9
### Website Support

- Added RedTube video downloads, public playlists, and pornstar, channel and amateur pages.
- Added Thumbzilla video downloads and pornstar, channel and amateur pages.
- Added Tube8 video downloads and pornstar, channel and amateur pages.
- Added EMPFlix video downloads and profile/pornstar pages.
- Added TNAFlix video downloads and profile, pornstar and channel pages.
- Added Eporner channel downloads. Pornstar downloads were already supported.
- Added PornHub Shorts downloads.
- Added support for XHamster `/users/` links that lead to a creator's video page.
- Added support for XVideos `/models/`, `/profiles/` and `/amateur-channels/` links, including profiles that redirect to channels. XVideos model and channel downloads were already supported in 3.8.
- Added support for `xhamster.desi`, XNXX's `xnxx.es`, `xnxx-ru.com`, `xnxx-arabic.com` and `xnxx-india.com`, and Tube8's `tube8.fr` and `tube8.es` domains.
- [CLI] Added photo-album downloads for PornHub and XFreeHD.
- [CLI] Added profile/channel downloads for XHamster, SpankBang, YouPorn and Porntrex, alongside the five newly supported websites.
- [CLI] Added XVideos playlists and YouPorn collections alongside the existing PornHub playlist support.

### Website Fixes

- [PornHub] Fixed loading uploaded videos from regular user pages. Links ending in `/videos` or `/videos/upload` now select the correct video list.
- [PornHub] Fixed model links that redirect to pornstar pages, and video links copied from embedded players.
- [XHamster] Fixed Shorts/Moments downloads after changes to the website. Fixed missing durations on later videos in a profile list and incorrect Full HD/4K detection.
- [XVideos] Fixed loading profile video lists and their later pages. Fixed broken video links taken from profile lists and titles displaying HTML codes such as `&amp;`.
- [XVideos] Loading video details now uses the uploader name from the video page when available, avoiding an extra profile request for each video.
- [XNXX] Fixed broken video links taken from profile lists, loading video details from newer page layouts, and crashes on empty profiles.
- [Eporner] Fixed German video links using `/porno-video/` and pornstar links using `/pornostar/`. Fixed missing quality choices and selecting a download link for the wrong video codec.
- [YouPorn] Downloads can now use a direct MP4 file when no segmented stream is available. Fixed loading collections with missing details and collection links containing the website address twice.
- [Beeg] Fixed downloads after changes to Beeg's video API. Fixed links copied from tag pages and video IDs ending in zero.
- [Porntrex] Fixed downloads whose MP4 links contain access tokens. Fixed loading later pages of model and channel videos.
- [XFreeHD] Fixed missing quality choices and crashes when videos have missing duration/rating details or are private.
- Fixed loading video-tab links on PornHub, XNXX and XVideos, such as links ending in `/videos/best/0`, without treating them as a separate profile.
- Fixed later-page links losing sort/filter settings or adding a second page number on PornHub, XHamster, XNXX, XVideos, Eporner, SpankBang, YouPorn and Porntrex. Video links loaded from lists on these sites also keep the source domain, including localized and mirror domains.
- Unsupported search pages, profile directories and photo/GIF tabs now show a clear error instead of being opened as video links.

### Downloads

- [Desktop] Rebuilt the download list with quality, status, progress and Start/Stop/Resume controls for each video.
- [Desktop] You can now remove waiting, queued and active downloads from the list. Removing an active download stops it first and leaves other downloads running.
- [Desktop] Added an option to remove completed downloads from the list automatically. Their download history is kept if tracking is enabled.
- [Desktop] Fixed selection and Download Selected acting on the wrong video after rows were added or removed.
- Improved Stop/Resume so downloaded parts are reused. Direct-file downloads no longer restart at byte zero when the server supports resuming.
- Renamed the temporary-file option to **Cleanup on stop** and added help beside it. Leave it off to keep partial downloads for Resume; turn it on to delete them and start fresh next time.
- Direct-file downloads can now download several parts at once when the server supports it. The download speed limit also applies to these transfers.
- Fixed completed downloads keeping large amounts of temporary data in memory. Temporary download parts are released after completion.
- Failed transfers now show as failed and can be retried, instead of sometimes being marked complete.
- Stopping a queued download now removes it from the queue immediately. Repeated Start clicks no longer queue the same download several times.
- Changes to the number of parallel downloads take effect when the current downloads finish.
- Improved joining downloaded video parts, conversion progress and handling of streams with unusual timestamps.
- [Windows] Fixed MP4 conversion and metadata writing failing when the app was opened from Explorer or the Start Menu. FFmpeg no longer opens an extra console window.
- Fixed video lengths being converted twice and displayed with the wrong duration.
- [Desktop] Closing the app now saves unfinished downloads. They return as paused when you reopen it; click Resume to continue. The output path, selected quality and reusable progress are kept.

### Filters and Filenames

- [GUI] Added filters for title, author and tags using regular expressions, plus minimum/maximum length, highest available quality and publication dates. You can combine the filters.
- [GUI] Text filters ignore upper/lower case. A tag filter can match any one tag, and date ranges include both selected days.
- [GUI] Added Start/End positions to choose a section of a profile or playlist before filtering. For example, 10 to 20 includes both videos 10 and 20.
- [GUI] Added 144p to the quality filter and fixed the 4K filter to mean 2160p.
- Invalid filters, dates, ranges and filename templates now show an error before loading videos.
- Improved custom filenames. The **Options** dialog explains `$title`, `$author`, `$video_id`, `$index`, `$publish_date`, `$length`, `$output_path` and `$$` for a dollar sign.
- `$index` keeps the video's original position in the source list, even when other videos are filtered out or removed.
- Fixed filenames containing foreign alphabets, emoji, slashes, Windows-reserved names, trailing dots/spaces or very long titles. Titles and author names can no longer accidentally create folders; folders deliberately written into your template still work.
- Titles and author names are now shown as written on the website. Only the saved filename has characters replaced when needed.
- Fixed missing `.mp4` extensions when a title contains dots, and a video titled `~` being saved to the home folder.

### Account Login

- Added XHamster login with username/password or an imported desktop browser session. You can load liked videos and account playlists.
- Added XVideos login with session tokens or an imported desktop browser session. You can load Watch Later, history and liked videos. XVideos password/CAPTCHA login is not supported.
- Added desktop browser-session import for PornHub, including automatic username detection. Existing email/password login, watch history and recommendations remain available.
- Added PornHub subscription-feed and favorites actions.
- Browser-session import now checks that the website actually recognizes you as logged in. Expired cookies no longer produce a false successful login.
- Fixed XHamster liked videos showing recommendations instead of your liked list.
- Added a **How to login** dialog for each supported account website.
- Fixed account pages staying busy after a failed login, cancelled request or invalid playlist. Reaching the end of an account list no longer reports a missing later page as an error.

### User Interface and Settings

- Rebuilt the desktop interface in QML with a Material design, accent colors and light/dark themes. Appearance changes can be applied while the app is open.
- Added high-contrast light and dark themes.
- Added an optional glow around the window while the app is busy.
- Added **Recent activity** for messages and errors, plus optional system notifications. System notifications are off by default.
- Added detailed download errors with a **Copy text** button, making it easier to report a problem. You can read these without enabling online error reporting.
- Improved resizing, download-column spacing, settings alignment and scrolling with high-resolution mouse wheels. Fixed overlapping cards on the information page.
- Added scrollable help dialogs and connected the keyboard-shortcuts dialog.
- Improved app icons on Windows, Linux, macOS, Android and iOS.
- Fixed settings that were saved but not used, including logging, request retries, cache sizes, preparation delays and network options. Settings that need a restart say so.
- Added a first-run setup for the application license and optional error reporting. Completed steps are remembered across updates and preference resets.
- Replaced the in-app Supported Websites page with a link to [pornfetch.to/#websites](https://pornfetch.to/#websites).

### Download History and Statistics

- Rebuilt desktop download history using a local PocketBase database and added a statistics dashboard. Download history and statistics are now also available in the CLI.
- History now records completed, stopped and failed downloads, retries, and the model/channel/playlist they came from.
- Resuming or retrying updates the existing history entry instead of creating another completion record.
- History stays available after removing a video from the download list or restarting the app. **Refresh** now loads new database records.
- Fixed history being lost while moving the database folder during shutdown, and database startup failing with some automatically generated passwords.

### Networking and Privacy

- Rebuilt the entire network backend with asynchronous requests, allowing network work to run without blocking the interface.
- Added a desktop proxy setup/test dialog for HTTP, HTTPS and SOCKS proxies.
- Added encrypted DNS (DNS over HTTPS) with a backup resolver, Encrypted Client Hello where supported, and settings for browser fingerprints, HTTP versions and network interfaces.
- Added optional desktop SNI obfuscation modes to help with some network blocks. Strict mode requires administrator/root access and is available on supported Windows x64 and Linux systems.
- Added managed Tor routing: Off, updates/licensing only, or all app traffic including video downloads. The app starts Tor when needed and shows connection progress.
- If the selected Tor route fails, requests stop instead of silently using a direct connection. Links opened in your browser are outside the app's Tor route.
- Network setting changes can now be applied without restarting. Old connections are closed after replacement.
- Improved Anonymous Mode to hide sensitive video details and detailed error dialogs.
- Error reporting is optional. Basic reports leave out URLs, local paths and full error details; Full reports include detailed debugging information. Reporting stays off until you enable it.

### Automatic Updates

- Automatic updates are free on desktop, Android and CLI. No premium license is required.
- [Desktop] Installer-based copies now update through the Qt Maintenance Tool on Windows, Linux and macOS. This replaces the old macOS Sparkle updater.
- [Desktop] Added update download progress, release notes and an option to stop showing startup update dialogs. Manual update checks remain available.
- [Desktop] Updates now use the normal shutdown process to save the queue and close the history database before installation, reducing locked-file errors on Windows.
- [Desktop] The maintenance tool and app can update together in one run.
- [CLI] Added **Check for Updates** to the menu and `self-update --check`, `self-update` and `self-update --yes` for standalone binaries.
- [CLI] Update failures keep the previous files and recovery information. Fixed certificate errors in standalone update checks.
- [Android] Added APK update downloads with signature, file and package checks. Android still asks for installation permission and confirmation.
- Updates now check signed update information and downloaded files before installation. Interrupted update-file downloads can resume.
- Portable, source and package-manager installations still use their appropriate manual update method.

### CLI

- Rebuilt the terminal menus for downloads, profiles/playlists, accounts, settings, licenses, tracked models, history and statistics.
- The CLI now runs without Qt, including on headless systems and in Termux.
- Batch downloads accept multiple supported source URLs, with quality/output options and an option to continue after a failed entry.
- Added pause, resume and cancel controls, including paused downloads that can continue in a later CLI session.
- Reworked tracked-model scanning and the pending-download queue around the same website handling used by ordinary downloads.
- Added automatic discovery/installation of PocketBase for download history and statistics.
- Improved progress displays and errors for unavailable videos. Added offline checks and optional website/download diagnostics to help investigate problems.

### Android and iOS

- Replaced the old Kotlin Android app with a new QML interface for Android 9+, with phone/tablet navigation and download cards. Android remains experimental.
- Android asks you to choose a shared output folder. Completed videos are copied there automatically so other apps can open them, and the folder choice is remembered.
- Added Android APK builds for ARM64, ARMv7, x86_64 and x86, with signed release APKs.
- Added an iOS app for iOS 15+. The IPA needs re-signing for sideloading. License activation, downloading, MP4 conversion and playback have been checked on a non-jailbroken iPhone 7.
- Download history/statistics and desktop browser-cookie import are unavailable on Android. System notifications do not enable background downloads.

### Licensing

- Replaced the beta licensing system. Old beta keys no longer work; you can now paste a license key or import a license file in both GUI and CLI.
- Free use supports up to 720p, one active download, and the first five videos of a public model, channel or playlist. Account lists are exempt from the five-video limit.
- Premium unlocks higher qualities, parallel downloads and bulk downloads beyond that preview.
- Permanent Premium costs €29.99 once for up to ten active installations and includes all future versions, with no subscription or paid renewal. Activation and periodic validation remain required. After successful online validation, offline use is available for up to seven days.
- Changed the application license to the Porn Fetch Source-Available License 1.0. Copies of 3.8 released under the GPL keep their original license.

### Other

- Updated the desktop/CLI build environment to Python 3.15, Qt to 6.12 and Nuitka to 4.3.3, and updated the website libraries and shared downloader.
- Improved the Windows build script to install missing Git, C++ build tools and FFmpeg build dependencies automatically. Build errors stay visible and are saved to a log.
- Fixed macOS app-bundle packaging and Windows ARM64 build issues. Build scripts now show full compiler output and progress where available.
- Moved the website, update and application-service links to `pornfetch.to`.

### Removals and Known Issues

- Removed in-app keyword search, thumbnails and the Eporner tools screen.
- Removed support for HQPorner, MissAV and Porngo, and removed the old proxy kill-switch option.
- The interface is currently English-only. Translations and language selection are unfinished.
- Old filename templates using nested fields or format codes, such as `${author.name}` or `${publish_date:%Y}`, need updating to the placeholders listed under **Filters and Filenames**.
- Download history saved by 3.8 is not imported into the new database. The current importer only supports history from earlier 3.9 betas.
- The old `xhopen` domain is no longer accepted. Use an `xhamster.com` or `xhamster.desi` link.
- Windows x86 and Linux s390x/ppc64le builds are paused.
- SpankBang desktop downloads still need manual checking. Thumbzilla playlists have not been verified with a working public playlist.
- Public video lists from RedTube and Tube8 User pages are not confirmed working. Use their supported pornstar, channel or amateur pages.
- XFreeHD desktop downloads still need a follow-up check that Resume reuses the downloaded bytes correctly.
- Android device behavior, Android updates, packaged desktop/CLI updates, and Tor/Strict SNI behavior still need checks on their respective devices or networks. Desktop queue recovery covers normal close/reopen; recovery after a forced kill or power loss has not been tested.
