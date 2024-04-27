[app]
# title of your application
title = main
# project directory. the general assumption is that project_dir is the parent directory
# of input_file
project_dir = .
# source file path
input_file = /home/asuna/PycharmProjects/Porn_Fetch/main.py
# directory where exec is stored
exec_directory = .
# path to .pyproject project file
project_file = 
# application icon
icon = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/android_app_icon.png

[python]
# python path
python_path = /home/asuna/venvab/bin/python3.11
# python packages to install
# ordered-set = increase compile time performance of nuitka packaging
# zstandard = provides final executable size optimization
packages = Nuitka==2.1
# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]
# comma separated path to qml files required
# normally all the qml files required by the project are added automatically
qml_files = 
# excluded qml plugin binaries
excluded_qml_plugins = 
# qt modules used. comma separated
modules = Gui,Widgets,Core
# qt plugins used by the application
plugins = egldeviceintegrations,iconengines,platforms/darwin,xcbglintegrations,imageformats,platforms,platformthemes,styles,platforminputcontexts,accessiblebridge,generic

[android]
# path to pyside wheel
wheel_pyside = /home/asuna/build_wheels/PySide6-6.7.0-6.7.0-no-py-ver-impl-available-no-abi-tag-info-available-android_armv7a.whl
# path to shiboken wheel
wheel_shiboken = /home/asuna/build_wheels/shiboken6-6.7.0-6.7.0-no-py-ver-impl-available-no-abi-tag-info-available-android_armv7a.whl
# plugins to be copied to libs folder of the packaged application. comma separated
plugins = imageformats_qjpeg,iconengines_qsvgicon,imageformats_qico,imageformats_qgif,styles_qandroidstyle,imageformats_qsvg,platforms_qtforandroid

[nuitka]
# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 
# (str) specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]
# build mode
# possible options = [release, debug]
# release creates an aab, while debug creates an apk
mode = debug
# contrains path to pyside6 and shiboken6 recipe dir
recipe_dir = /home/asuna/PycharmProjects/Porn_Fetch/deployment/recipes
# path to extra qt android jars to be loaded by the application
jars_dir = /home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar
# if empty uses default ndk path downloaded by buildozer
ndk_path = /home/asuna/Android/Sdk/ndk
# if empty uses default sdk path downloaded by buildozer
sdk_path = /home/asuna/Android/Sdk
# other libraries to be loaded. comma separated.
# loaded at app startup
local_libs = plugins_platforms_qtforandroid
# architecture of deployed platform
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
arch = armv7a

