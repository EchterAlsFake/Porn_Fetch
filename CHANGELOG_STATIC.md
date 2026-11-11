# 3.9 (in development)

This version is still in beta. See the [development checklist](https://pornfetch.to/checklist) for release progress.

### Website Support

- Added YouJizz videos, public collections, pornstar directory links and public user uploads. General keyword search and other provider methods remain unavailable.

- Added Porn.com video downloads, collections, channels and pornstar pages on verified language hosts. External referral cards are excluded from download lists.

- Added Pornhat video downloads and model/channel pages, including verified language hosts and the `.one` alias.

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
- Lifetime Premium costs €29.99 once for up to ten active installations. Every future Porn Fetch update and feature I release is included, without release cutoffs or renewal purchases. Future development has no guaranteed duration. Activation and periodic validation remain required, with up to seven days offline after a successful check. If I permanently close the licensing service, I will provide an offline unlock before closure.
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
