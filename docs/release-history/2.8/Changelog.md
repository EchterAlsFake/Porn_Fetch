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
