[app]
title = Porn Fetch
package.name = app
package.domain = to.pornfetch
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,qml,qmlc,js
source.exclude_dirs = tests, scripts, packaging, docs, .github, demos, dist, build, .venv, .git, .idea, .ruff_cache, p4a-recipes, deployment
version = 3.9
requirements = python3,shiboken6,PySide6,certifi,cffi,charset-normalizer,chompjs,cryptography,curl_cffi,eaf_base_api,filelock,idna,m3u8,markdown-it-py,python-dateutil,selectolax,unofficial-api-for-beeg,unofficial-api-for-eporner,unofficial-api-for-pornhub,unofficial-api-for-porntrex,unofficial-api-for-redtube,unofficial-api-for-spankbang,unofficial-api-for-thumbzilla,unofficial-api-for-tube8,unofficial-api-for-xfreehd,unofficial-api-for-xhamster,unofficial-api-for-xnxx,unofficial-api-for-xvideos,unofficial-api-for-youporn,cachetools,tenacity,json5,six,platformdirs,tuf,securesystemslib,urllib3
orientation = portrait
osx.kivy_version = 2.2.0
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.12.2
ios.codesign.allowed = false
presplash.filename = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_transparent.png
android.ndk_path = /home/asuna/.pyside6_android_deploy/android-ndk/android-ndk-r27c
android.sdk_path = /home/asuna/.pyside6_android_deploy/android-sdk
android.api = 35
android.minapi = 28
android.ndk_api = 28
android.no-byte-compile-python = False
p4a.bootstrap = qt
p4a.local_recipes = /home/asuna/PycharmProjects/Porn_Fetch/deployment/recipes
p4a.branch = develop
p4a.commit = HEAD
android.permissions = android.permission.ACCESS_NETWORK_STATE, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.INTERNET
android.add_jars = /home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6Android.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidNetwork.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidNetworkInformationBackend.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidQuick.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidBindings.jar
p4a.extra_args = --qt-libs=Core,Network,Gui,OpenGL,Qml,Quick,QuickControls2 --load-local-libs=plugins_platforms_qtforandroid --init-classes=
icon.filename = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_transparent.png

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = /home/asuna/PycharmProjects/Porn_Fetch

