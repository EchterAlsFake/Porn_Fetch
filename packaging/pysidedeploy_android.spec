[app]
title = Porn Fetch
project_dir = .
input_file = main.py
exec_directory = .
project_file = pyproject.toml
icon = src/frontend/graphics/logo.png

[python]
python_path =
packages =
android_packages = buildozer,cython

[qt]
qml_files = src/frontend/UI/AndroidMain.qml,src/frontend/UI/AndroidDownloadsPage.qml,src/frontend/UI/AndroidAccountPage.qml,src/frontend/UI/AndroidSettingsPage.qml,src/frontend/UI/AndroidMorePage.qml,src/frontend/UI/AndroidInfoPage.qml,src/frontend/UI/AndroidSupportedWebsitesPage.qml,src/frontend/UI/WebsiteSupportData.qml,src/frontend/UI/WebsiteSupportContent.qml,src/frontend/UI/LicenseWidget.qml,src/frontend/UI/ProxyWindow.qml,src/frontend/UI/HelpButton.qml,src/frontend/UI/QualityComboBox.qml,src/frontend/UI/SmoothScrollView.qml,src/frontend/UI/SmoothWheelHandler.qml,src/frontend/UI/AppStrings.qml,src/frontend/UI/Theme.qml
excluded_qml_plugins =
modules = Core,Gui,Qml,Quick,QuickControls2,QuickLayouts,Network,Widgets
plugins =

[android]
wheel_pyside =
wheel_shiboken =
plugins =

[nuitka]
extra_args =

[buildozer]
mode = debug
recipe_dir =
jars_dir =
ndk_path =
sdk_path =
local_libs =
arch = aarch64
