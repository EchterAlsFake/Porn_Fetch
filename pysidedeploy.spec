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

[python]
# python path
python_path = /home/asuna/venv/bin/python
# python packages to install
# ordered-set = increase compile time performance of nuitka packaging
# zstandard = provides final executable size optimization
packages = nuitka==1.5.4,ordered_set,zstandard
# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]
# comma separated path to qml files required
# normally all the qml files are added automatically
qml_files = 
# excluded qml plugin binaries
excluded_qml_plugins = 
# path to pyside wheel
wheel_pyside = /home/asuna/PycharmProjects/Porn_Fetch/src/backend/PySide6_6.6.1_aarch64.whl
# path to shiboken wheel
wheel_shiboken = /home/asuna/PycharmProjects/Porn_Fetch/src/backend/shiboken6_6.6.1_aarch64.whl
# plugins to be copied to libs folder of the packaged application. comma separated
plugins = platforms_qtforandroid,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,platforminputcontexts_qtvirtualkeyboardplugin,generic_qinsighttracker,iconengines_qsvgicon,imageformats_qgif,imageformats_qicns,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,imageformats_qtga,imageformats_qtiff,imageformats_qwbmp,imageformats_qwebp,styles_qandroidstyle,platforms_qtforandroid,platforminputcontexts_qtvirtualkeyboardplugin,generic_qinsighttracker,iconengines_qsvgicon,imageformats_qgif,imageformats_qicns,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,imageformats_qtga,imageformats_qtiff,imageformats_qwbmp,imageformats_qwebp,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle,platforms_qtforandroid,iconengines_qsvgicon,imageformats_qgif,imageformats_qico,imageformats_qjpeg,imageformats_qsvg,styles_qandroidstyle

[nuitka]
# (str) specify any extra nuitka arguments
# eg = extra_args = --show-modules --follow-stdlib
extra_args = --quiet --noinclude-qt-translations=True

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
ndk_path = /home/asuna/Android/Sdk/ndk/25c
# if empty uses default sdk path downloaded by buildozer
sdk_path = /home/asuna/Android/Sdk
# modules used. comma separated
modules = Core,Gui,Widgets
# other libraries to be loaded. comma separated.
# loaded at app startup
local_libs = plugins_platforms_qtforandroid
# architecture of deployed platform
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
arch = aarch64

