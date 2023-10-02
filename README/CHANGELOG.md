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