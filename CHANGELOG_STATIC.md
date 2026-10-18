# Porn Fetch 3.9 beta

These notes describe the current 3.9 beta and the changes since 3.8. This beta is incomplete and still being tested; features and platform support may change.

The crypto checkout is a free sandbox simulation: no real transaction takes place and no money or credit card is required.

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
- Added a first-run beta disclaimer with a 30-second reading period on desktop, Android and CLI.
- The desktop update notification shows current release notes and links to GitHub releases.
- Rebuilt the desktop app in QML, including the downloads, account, settings, statistics, license and information pages.
- Added Material style, accent colors and theme changes while the app is running. Most settings now apply immediately; the app still tells you when a restart is needed.
- The download list shows each video's status, progress and quality, with controls to select videos, download them, stop them and resume them.
- Added a dedicated proxy window that checks the address and tests the connection before it is used.
- Added a first-run choice for error reporting. Reports are optional and redact common private details before sending; you can change the choice later in Settings.
- Improved anonymous mode so the desktop app hides video details and sensitive widgets when it is enabled.
- Started a new QML Android layout with phone and tablet navigation, download cards and a folder picker for completed files. Download history and statistics are desktop-only; Android does not run a tracking database. This is development work: there is no 3.9 APK in the current desktop build workflow.

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
