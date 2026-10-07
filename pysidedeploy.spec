[app]

# title of your application
title = Porn Fetch

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = main.py

# directory where the executable output is generated
exec_directory = .

# path to the project file relative to project_dir
project_file = 

# application icon
icon = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_transparent.png

[python]

# python path
python_path = /home/asuna/PycharmProjects/Porn_Fetch/.venv/bin/python

# python packages to install
packages = Nuitka==4.1.1

# buildozer = for deploying Android application
android_packages = buildozer==1.6.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
# normally all the qml files required by the project are added automatically
# design studio projects include the qml files using qt resources
qml_files = src/frontend/UI/AccountPage.qml,src/frontend/UI/AndroidAccountPage.qml,src/frontend/UI/AndroidDownloadsPage.qml,src/frontend/UI/AndroidInfoPage.qml,src/frontend/UI/AndroidMain.qml,src/frontend/UI/AndroidMorePage.qml,src/frontend/UI/AndroidSettingsPage.qml,src/frontend/UI/AndroidStatisticsPage.qml,src/frontend/UI/AndroidSupportedWebsitesPage.qml,src/frontend/UI/AppStrings.qml,src/frontend/UI/DownloadsPage.qml,src/frontend/UI/HelpButton.qml,src/frontend/UI/InfoPage.qml,src/frontend/UI/InstallDialog.qml,src/frontend/UI/LicenseWidget.qml,src/frontend/UI/LicenseWindow.qml,src/frontend/UI/Main.qml,src/frontend/UI/MessageBox.qml,src/frontend/UI/ProxyWindow.qml,src/frontend/UI/QualityComboBox.qml,src/frontend/UI/SettingsPage.qml,src/frontend/UI/SmoothScrollView.qml,src/frontend/UI/SmoothWheelHandler.qml,src/frontend/UI/SplashScreen.qml,src/frontend/UI/StatisticsPage.qml,src/frontend/UI/SupportedWebsitesPage.qml,src/frontend/UI/Theme.qml

# excluded qml plugin binaries
excluded_qml_plugins = QtCharts,QtQuick3D,QtSensors,QtTest,QtWebEngine

# qt modules used. comma separated
modules = Widgets,Network,QuickControls2,Quick,OpenGL,Core,Qml,Test,Gui

# qt plugins used by the application. only relevant for desktop deployment
# for qt plugins used in android application see [android][plugins]
plugins = 

[android]

# path to pyside wheel
wheel_pyside = /home/asuna/PycharmProjects/Porn_Fetch/pyside6-6.11.2-6.11.2-cp314-cp314-android_aarch64.whl

# path to shiboken wheel
wheel_shiboken = /home/asuna/PycharmProjects/Porn_Fetch/shiboken6-6.11.2-6.11.2-cp314-cp314-android_aarch64.whl

# package identity and version
package_name = app
package_domain = to.pornfetch
version = 3.9
presplash = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_transparent.png

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = platforms_qtforandroid
requirements = asyncstdlib,certifi,cffi,charset-normalizer,chompjs,colorama,coverage,cryptography,curl_cffi,eaf_base_api,filelock,idna,m3u8,markdown-it-py,pkginfo,python-dateutil,requests,selectolax,tqdm,unofficial-api-for-beeg,unofficial-api-for-eporner,unofficial-api-for-pornhub,unofficial-api-for-porntrex,unofficial-api-for-redtube,unofficial-api-for-spankbang,unofficial-api-for-thumbzilla,unofficial-api-for-tube8,unofficial-api-for-xfreehd,unofficial-api-for-xhamster,unofficial-api-for-xnxx,unofficial-api-for-xvideos,unofficial-api-for-youporn,cachetools,tenacity,json5,six,platformdirs,tuf,securesystemslib,urllib3
extra_recipes_dir = /home/asuna/PycharmProjects/Porn_Fetch/p4a-recipes

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle. comma separated
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default = onefile
mode = onefile

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
# release creates a .aab, while debug creates a .apk
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir = /home/asuna/PycharmProjects/Porn_Fetch/deployment/recipes

# path to extra qt android .jar files to be loaded by the application
jars_dir = /home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar

# if empty, uses default ndk path downloaded by buildozer
ndk_path = /home/asuna/.pyside6_android_deploy/android-ndk/android-ndk-r27c

# if empty, uses default sdk path downloaded by buildozer
sdk_path = /home/asuna/.pyside6_android_deploy/android-sdk

# other libraries to be loaded at app startup. comma separated.
local_libs = plugins_platforms_qtforandroid

# architecture of deployed platform
arch = aarch64

