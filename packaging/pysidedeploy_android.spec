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
# CI installs the pinned upstream Buildozer with Cython 3 support; preserve it.
android_packages = buildozer,cython==3.3.0

[qt]
qml_files = src/frontend/UI/FirstRunSetup.qml,src/frontend/UI/LicenseOfferContent.qml,src/frontend/UI/UkraineMessageContent.qml,src/frontend/UI/NotificationPanel.qml,src/frontend/UI/LicenseOfferDialog.qml,src/frontend/UI/UkraineMessageDialog.qml,src/frontend/UI/AndroidOutputSetupDialog.qml,src/frontend/UI/AndroidMain.qml,src/frontend/UI/AndroidDownloadsPage.qml,src/frontend/UI/AndroidAccountPage.qml,src/frontend/UI/AndroidSettingsPage.qml,src/frontend/UI/AndroidMorePage.qml,src/frontend/UI/AndroidInfoPage.qml,src/frontend/UI/LicenseWidget.qml,src/frontend/UI/ProxyWindow.qml,src/frontend/UI/HelpButton.qml,src/frontend/UI/AccountLoginHelp.qml,src/frontend/UI/ScrollableMessageDialog.qml,src/frontend/UI/TorRouting.qml,src/frontend/UI/QualityComboBox.qml,src/frontend/UI/SmoothScrollView.qml,src/frontend/UI/SmoothWheelHandler.qml,src/frontend/UI/AppStrings.qml,src/frontend/UI/Theme.qml,src/frontend/UI/AppButton.qml,src/frontend/UI/AppTextField.qml,src/frontend/UI/AppComboBox.qml,src/frontend/UI/AppSpinBox.qml,src/frontend/UI/ContrastOutline.qml,src/frontend/UI/ContentLanguageComboBox.qml,src/frontend/UI/ContrastPopupBackground.qml
excluded_qml_plugins =
# SVG images and icons need QtSvg even though Python never imports it directly.
modules = Core,Gui,Qml,Quick,QuickControls2,QuickLayouts,Network,Widgets,Svg
plugins =

[android]
wheel_pyside =
wheel_shiboken =
# Copy these into APK/lib as well as the wheel's private Python bundle.
plugins = platforms_qtforandroid,imageformats_qsvg,iconengines_qsvgicon

[nuitka]
extra_args =

[buildozer]
mode = release
recipe_dir =
jars_dir =
ndk_path =
sdk_path =
local_libs =
arch = aarch64
