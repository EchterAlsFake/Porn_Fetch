[app]
title = Porn Fetch
project_dir = .
input_file = main.py
exec_directory = .
project_file = 
icon = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_transparent.png

[python]
python_path = /home/asuna/PycharmProjects/Porn_Fetch/.venv/bin/python
packages = Nuitka==4.1.1
android_packages = buildozer==1.6.0,cython==0.29.33

[qt]
qml_files = src/frontend/UI/BetaDisclaimerDialog.qml,src/frontend/UI/AccountPage.qml,src/frontend/UI/AndroidAccountPage.qml,src/frontend/UI/AndroidDownloadsPage.qml,src/frontend/UI/AndroidInfoPage.qml,src/frontend/UI/AndroidMain.qml,src/frontend/UI/AndroidMorePage.qml,src/frontend/UI/AndroidSettingsPage.qml,src/frontend/UI/AndroidSupportedWebsitesPage.qml,src/frontend/UI/WebsiteSupportData.qml,src/frontend/UI/WebsiteSupportContent.qml,src/frontend/UI/AppStrings.qml,src/frontend/UI/DownloadsPage.qml,src/frontend/UI/HelpButton.qml,src/frontend/UI/InfoPage.qml,src/frontend/UI/InstallDialog.qml,src/frontend/UI/LicenseWidget.qml,src/frontend/UI/LicenseWindow.qml,src/frontend/UI/Main.qml,src/frontend/UI/MessageBox.qml,src/frontend/UI/ProxyWindow.qml,src/frontend/UI/QualityComboBox.qml,src/frontend/UI/SettingsPage.qml,src/frontend/UI/SmoothScrollView.qml,src/frontend/UI/SmoothWheelHandler.qml,src/frontend/UI/SplashScreen.qml,src/frontend/UI/StatisticsPage.qml,src/frontend/UI/SupportedWebsitesPage.qml,src/frontend/UI/Theme.qml
excluded_qml_plugins = QtCharts,QtQuick3D,QtSensors,QtTest,QtWebEngine
modules = Core,Network,Qml,Test,QuickControls2,Gui,Widgets,OpenGL,Quick
plugins = 

[android]
wheel_pyside = /home/asuna/PycharmProjects/Porn_Fetch/pyside6-6.12.0-6.12.0-cp314-cp314-android_aarch64.whl
wheel_shiboken = /home/asuna/PycharmProjects/Porn_Fetch/shiboken6-6.12.0-6.12.0-cp314-cp314-android_aarch64.whl
package_name = app
package_domain = to.pornfetch
version = 3.9
presplash = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_transparent.png
plugins = platforms_qtforandroid
requirements = certifi,cffi,charset-normalizer,chompjs,cryptography,curl_cffi,eaf_base_api,filelock,idna,m3u8,markdown-it-py,python-dateutil,selectolax,unofficial-api-for-beeg,unofficial-api-for-eporner,unofficial-api-for-pornhub,unofficial-api-for-porntrex,unofficial-api-for-redtube,unofficial-api-for-spankbang,unofficial-api-for-thumbzilla,unofficial-api-for-tube8,unofficial-api-for-xfreehd,unofficial-api-for-xhamster,unofficial-api-for-xnxx,unofficial-api-for-xvideos,unofficial-api-for-youporn,cachetools,tenacity,json5,six,platformdirs,tuf,securesystemslib,urllib3
extra_recipes_dir = /home/asuna/PycharmProjects/Porn_Fetch/p4a-recipes

[nuitka]
macos.permissions = 
mode = standalone
extra_args = --quiet --noinclude-qt-translations

[buildozer]
mode = release
recipe_dir = /home/asuna/PycharmProjects/Porn_Fetch/deployment/recipes
jars_dir = /home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar
ndk_path = /home/asuna/.pyside6_android_deploy/android-ndk/android-ndk-r28c
sdk_path = /home/asuna/.pyside6_android_deploy/android-sdk
local_libs = plugins_platforms_qtforandroid
arch = aarch64

