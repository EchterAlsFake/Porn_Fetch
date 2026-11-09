[app]
android.add_jars = /home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6Android.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidBindings.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidMultimedia.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidNetwork.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidNetworkInformationBackend.jar,/home/asuna/PycharmProjects/Porn_Fetch/deployment/jar/PySide6/jar/Qt6AndroidQuick.jar
icon.adaptive_background.filename = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/icon_background.png
icon.adaptive_foreground.filename = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/icon_foreground.png
p4a.hook = /home/asuna/PycharmProjects/Porn_Fetch/scripts/android_storage_hook.py
title = Porn Fetch
package.name = app
package.domain = to.pornfetch
source.dir = /home/asuna/PycharmProjects/Porn_Fetch
source.include_exts = py,png,jpg,qml,js,json,txt,rcc
version = 3.9.0
requirements = python3==3.15.2,hostpython3==3.15.2,shiboken6,PySide6,certifi,cffi==2.1.1,charset-normalizer,chompjs,openssl==3.5.9,cryptography==50.0.2,curl_cffi==0.17.0,eaf_base_api,filelock,idna,m3u8,markdown-it-py,python-dateutil,selectolax,unofficial-api-for-beeg,unofficial-api-for-eporner,unofficial-api-for-porndoe,unofficial-api-for-pornhub,unofficial-api-for-porntrex,unofficial-api-for-redtube,unofficial-api-for-spankbang,unofficial-api-for-thumbzilla,unofficial-api-for-tube8,unofficial-api-for-xfreehd,unofficial-api-for-xhamster,unofficial-api-for-xnxx,unofficial-api-for-xvideos,unofficial-api-for-youporn,cachetools,tenacity,json5,six,platformdirs,tuf,securesystemslib,urllib3,unofficial-api-for-empflix,unofficial-api-for-tnaflix,PyJWT
orientation = portrait
fullscreen = 0
android.archs = x86_64
android.allow_backup = True
presplash.filename = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_square.png
android.ndk_path = /home/asuna/.pyside6_android_deploy/android-ndk/android-ndk-r28c
android.ndk = 28c
android.release_artifact = apk
android.sdk_path = /home/asuna/.pyside6_android_deploy/android-sdk
android.api = 36
android.minapi = 28
android.ndk_api = 28
android.no-byte-compile-python = True
p4a.bootstrap = qt
p4a.local_recipes = /home/asuna/PycharmProjects/Porn_Fetch/deployment/recipes
p4a.branch = develop
p4a.commit = HEAD
android.permissions = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE, android.permission.WRITE_EXTERNAL_STORAGE
p4a.extra_args = --qt-libs=Core,Network,Gui,OpenGL,Widgets,Qml,Quick,QuickControls2,Test --load-local-libs=plugins_platforms_qtforandroid --init-classes=
icon.filename = /home/asuna/PycharmProjects/Porn_Fetch/src/frontend/graphics/logo_square.png
source.exclude_dirs = src/tests,src/frontend/screenshots,src/frontend/translations/ts,scripts,packaging,demos,p4a-recipes
android.ant_path = /usr/share/ant

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = /home/asuna/PycharmProjects/Porn_Fetch

