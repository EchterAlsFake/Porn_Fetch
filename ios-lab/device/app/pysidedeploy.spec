[app]
title = PornFetch
project_dir = /Users/asuna/ios-lab/device/app
input_file = main.py
exec_directory = .
project_file = 
icon = /Users/asuna/ios-lab/.venv/lib/python3.13/site-packages/PySide6/scripts/deploy_lib/pyside_icon.icns

[python]
packages = Nuitka==4.1.1
android_packages = buildozer==1.6.0,cython==0.29.33

[qt]
qml_files = src/frontend/UI/QualityComboBox.qml,src/frontend/UI/Theme.qml,src/frontend/UI/HelpButton.qml,src/frontend/UI/InfoPage.qml,src/frontend/UI/LicenseWidget.qml,src/frontend/UI/AndroidDownloadsPage.qml,src/frontend/UI/AndroidInfoPage.qml,src/frontend/UI/ProxyWindow.qml,src/frontend/UI/AccountLoginHelp.qml,src/frontend/UI/SplashScreen.qml,src/frontend/UI/ScrollableMessageDialog.qml,src/frontend/UI/SettingsPage.qml,src/frontend/UI/AndroidMain.qml,src/frontend/UI/LicenseWindow.qml,src/frontend/UI/SmoothScrollView.qml,src/frontend/UI/Main.qml,src/frontend/UI/AndroidSettingsPage.qml,src/frontend/UI/InstallDialog.qml,src/frontend/UI/ProcessingIndicator.qml,src/frontend/UI/AndroidMorePage.qml,src/frontend/UI/TorRouting.qml,src/frontend/UI/DownloadsPage.qml,src/frontend/UI/ActivityEdge.qml,src/frontend/UI/AppStrings.qml,src/frontend/UI/BetaDisclaimerDialog.qml,src/frontend/UI/ApplicationShutdown.qml,src/frontend/UI/AndroidAccountPage.qml,src/frontend/UI/ServiceTorFailureDialog.qml,src/frontend/UI/StatisticsPage.qml,src/frontend/UI/SmoothWheelHandler.qml,src/frontend/UI/MessageBox.qml,src/frontend/UI/AccountPage.qml
excluded_qml_plugins = QtCharts,QtQuick3D,QtSensors,QtTest,QtWebEngine
modules = Core,Gui,Qml,Quick,QuickControls2,Test
plugins = 

[android]
wheel_pyside = 
wheel_shiboken = 
plugins = 

[ios]
wheel_pyside = /Users/asuna/ios-lab/device/wheels/pyside6-6.12.0-6.12.0-cp315-cp315-ios_arm64.whl
wheel_shiboken = /Users/asuna/ios-lab/device/wheels/shiboken6-6.12.0-6.12.0-cp315-cp315-ios_arm64.whl
xcframework_path = /Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework
bundle_id = local.asuna.PornFetch
team_id = 
version = 1.0
deployment_target = 15.0
entitlements = 
signing_style = Automatic
header_search_paths = 

[nuitka]
macos.permissions = 
mode = standalone
extra_args = --quiet --noinclude-qt-translations

[buildozer]
mode = debug
recipe_dir = 
jars_dir = 
ndk_path = 
sdk_path = 
local_libs = 
arch = 

