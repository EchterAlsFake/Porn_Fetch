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

