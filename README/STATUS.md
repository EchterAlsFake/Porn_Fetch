# 3.0
 

## TODO:

- [] Update Web application
- [x] Updating CLI
- [] Fixing the script for iOS (will take its time)
- [] Searching for Pornstars
- [] Searching for Users
- [] Filters for both (Users, Pornstars)
- [] Updating both translations
- [] Supporting feed objects
- [] OLED night black instead of grey
- [x] Different threading modes, for different use cases
- [x] A new and better layout (some in 1920x1080) See explanation down below
- [x] Better way of getting metadata
- [x] Directory structure system
- [x] Better way of checking if file exists
- [] A lot better exception handling
- [x] More features for hqporner.com
- [] Including French translations (will need an update on the .ts)
- [x] Dark mode for license widget
- [x] Working on the translations
- [x] Support for macOS in Build Script (untested)
- [x] Fixing the way of handling threading / semaphores
- [x] Fixing the counter of how many videos are already downloaded
- [x] Code refactoring / better logical operations
- [x] More and detailed debugging, error logging and error handling
- [x] Encoding titles always in utf-8 to eliminate the OS Error issue on Windows
- [x] Better way of downloading for HQPorner.com

# Android:

I'll try to compile PySide6 to Android. If I get that working, I could make a lot
of progress for it. It would be so easy for me and I wouldn't need to learn Kivy.


- [] PySide6 to Android (will probably fail ;) 
- [] Download from file
- [] Download from Model
- [] Search Query support
- [] Persistent settings
- [] Title stripping
- [] Debugging / Logging





# Layout:


99% of developers are completely bad at design. Porn Fetch is also not the greatest and 
most intuitive app, but I'll change that and I got some nice ideas:

The goal is to make the app bigger, but more intuitive by using 3 widgets.

1)  :

The main widget will include the basic Downloading process, progressbars,
status reports, error logs, explanations and is some kind of "homepage"

2)  :

The account widget will include the account, the feed, information about users, filters, 
regexes, user search and pornstar search

3) : The third widget will be about the settings and credits for the project.



I know it maybe sounds weird, but you'll see when it's done :) 

