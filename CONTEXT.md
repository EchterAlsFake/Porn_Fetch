This file is reserved for AI agents and shall not be used by other developers!


# Project 
- Name: Porn Fetch
- Status: Source Available (Development v3.9)
- Repository: https://github.com/EchterAlFake/Porn_Fetch
- Maintainer: EchterAlsFake (Johannes Habel)
- Description: A legaly compliant privacy respecting application to download adult media


# Tech Stack
- Language: Python 3.14
- Framework: Qt 6.11+ 
- Frontend: QML 
- Networking: curl-cffi (async)

# Target Platforms
- Windows (x64, ARM64)
- Linux (x64, ARM64)
- macOS (x64, Universal2)
- Android: (aarch64, x86_64, armv7a, i686)
- Possible iOS support not yet started

# Important Notice
- Entire Project is asynchronous
- Entire project is legally developed under German Law
- PySide6 has custom patches applied


# Project Structure

# The Root
- .python-version -> defines Python 3.14 for UV Project management
- BACKEND.md -> Explains the eaf_base_api library
- CONTEXT.md -> This file
- CONTRIBUTING.md -> Contribute guide and reference
- main.py -> Entry Point
- Porn_Fetch_CLI.py -> The CLI of Porn Fetch (not relevant during development unless explicitly told)
- pyproject.toml -> Defines dependencies for UV
- SECURITY.md -> Document to follow European Security laws for software
- uv.lock -> Locks dependencies with UV

# Frontend
Path: src/frontend/UI/

- Main.qml -> Entry Point for the app
- AccountPage.qml -> Related to account specific actions
- AppStrings.qml -> Translation strings for e.g., settings page
- DownloadsPage.qml -> The main download page where users can download videos
- HelpButton.qml -> Custom QML button to show help messages
- InfoPage.qml -> Shwos credits and about for the application
- InstallDialog.qml -> Dialog where a user can initiate the installation and enter a custom app name
- LicenseManager.qml > Used for managing and importing the license to unlock premium features
- LicenseWidget.qml -> Widget for LicenseManager.qml
- LicenseWindow.qml -> Window
- MessageBox.qml -> a simple Message Box to show the user an information
- ProxyWindow.qml -> custom window to apply proxies to all clients
- qmldir -> Defines the singleton instances e.g., AppStrings.qml
- QualityComboBox.qml -> Custom Combobox with licensing logic applied
- SettingsPage.qml -> Settings page to configure Porn Fetch settings. Options: System. Privacy, UI, Video, Performance
- SplashScreen.qml -> Splash Screen for startup
- StatisticsPage.qml -> Uses an internal database to show download statistics
- SupportedWebsitesPage.qml -> A page dedicated to show which websites are supported
- Theme.qml -> Handles theming across the application e.g., Material UI vs. Native, Dark and Light mode

Path:
src/frontend/

- resources.qrc -> Holds all translations, Markdown files and graphics
- update.ps1 -> Script for Windows to automatically update the frontend
- update.sh -> Does the same but for Linux and macOS

Path: src/frontend/graphics
- Description: Holds .png and .svg files that are used during runtime

Path: src/frontend/translations
- Description: Holds the translation files for different languages

Path: src/frontend/screenshots
- Description: Shows screenshots of the app for GitHub

# The Backend (important)
Path: src/backend/
- Description: Holds a lot of files that do the underlying work

- check_license.py -> Validates the imported license against a cryptographic asymetric public key
- clients.py -> Holds helper functions and the clients which Porn Fetch uses to fetch data and interact with the websites
- config.py -> Holds the global settings instance using QSettings, connected to the SettingsPage.qml using Signals
- database.py -> Logic for setting up the database for the statistics part
- download_manager.py -> Connects the backend which adds the videos into the download manager class which is connected to the QML frontend. 
- errors.py -> Custom App errors to be raised inside the app
- handle_ssl.py -> Legacy file for implementing SSL support per system using truststore (not needed anymore)
- helper_functions.py -> Some legacy functions
- installation.py -> class responsible for installing Porn Fetch on Windows and Linux
- license_bridge.py -> Connects the frontend QML Licensing logic to the backend
- login_manager.py -> Handles login to the different supported sites
- macos_setup.py -> Custom logic for macOS startup that tells users to move the app into /Applications
- proxy_tester.py -> Tests the proxy the user entered during the proxy setup and shows statistics about the proxy
- shared_functions -> contains functions used by the CLI and the GUI
- shared_gui -> useless file that needs to be abandoned
- sni_fragment_proxy_lite.py -> Please see: SNI_PROXY_AGENT_HANDOFF.md
- sni_fragment_proxy_strict.py -> Please see: SNI_PROXY_AGENT_HANDOFF.md
- sni_proxy_manager.py -> Connects both SNI proxies and manages them e.g., startup and shutdown
- splashscreen.py -> Starts the actual splashscreen
- tests.py -> Runs a fully automatic test suite that uses real network requests
- theme_manager.py -> manages Porn Fetch's theme e.g., dark vs. light
- tls_client_hello.py -> See SNI_PROXY_AGENT_HANDOFF.md
- uninstallation.py -> Handles the uninstallation of Porn Fetch
- update_service.py -> Handles automatic update checking using the Sparkle Framework on macOS and my own website for all other system. Fetches update information and changelogs and can also automatically update Porn Fetch

The sparkle folder contains the entire Sparkle Framework as well as a custom bridge in Objective-C which
makes the sparkle framework usable in Python.

### The Networking Backend
All network traffic is fundamentally routed through the eaf_base_api library / the BaseCore class.
It creates a curl-cffi async session and allows the user to heavily configure it through the SettingsPage.qml. 

The clients.py file reloads all these clients and applies the full configuration each time. A RuntimeConfig class is used for this.
The BaseCore class has different methods e.g., an iterator which allows to asynchronously fetch websites using a special consumer
producer pattern. This can also be configured. 

For a full reference read BACKEND.md

# Building
Path: src/build/

Building is done through the official pyside6-deploy tool.
The scripts are based on their platform. 

The nuitka package config file additionally imports AV and Sparkle.

Android building is done through pyside6-android-deploy with custom patches to the tool to build successfuly
and custom recipes for the C components.


# Scripts and Custom Patches 
Path: src/scripts/

- install.sh -> Installs Porn Fetch from source on Linux
- install_termux.sh -> Installs the CLI on Termux
- install_windows.ps1 -> Installs Porn Fetch on Windows
- patch_macos_bundle.py -> Injects sparkle to Info.plist
- patch_qtasyncio.py -> Patches the QtAsyncio library to add support for specific curl_cffi functions

# Testing
/testing
- Description: Contains automated scripts for testing. Not relevant for development.


# Commercial Aspect
The Project is freemium and a License is needed to unlock all features. 
The entire application is still source available though.
