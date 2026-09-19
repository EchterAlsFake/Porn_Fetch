
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
- Fixed the build scripts for Windows and Linux | Thanks @omar-st [Pull Request #48](https://github.com/EchterAlsFake/Porn_Fetch/commit/2d9cc2885c1383369020a5c26e957fe5cdf0f886) [Related Issue #46](https://github.com/EchterAlsFake/Porn_Fetch/issues/46)