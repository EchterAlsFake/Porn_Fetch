[app]
icon.adaptive_background.filename = src/frontend/graphics/icon_background.png
icon.adaptive_foreground.filename = src/frontend/graphics/icon_foreground.png
p4a.hook = scripts/android_storage_hook.py
title = Porn Fetch
package.name = app
package.domain = to.pornfetch
source.dir = .
source.include_exts = py,png,jpg,qml,js,json,txt,rcc
version = 3.9
requirements = python3==3.15.2,hostpython3==3.15.2,shiboken6,PySide6,certifi,cffi==2.1.1,charset-normalizer,chompjs,openssl==3.5.9,cryptography==50.0.2,curl_cffi==0.17.0,eaf_base_api,filelock,idna,m3u8,markdown-it-py,python-dateutil,selectolax,unofficial-api-for-beeg,unofficial-api-for-eporner,unofficial-api-for-pornhub,unofficial-api-for-porntrex,unofficial-api-for-redtube,unofficial-api-for-spankbang,unofficial-api-for-thumbzilla,unofficial-api-for-tube8,unofficial-api-for-xfreehd,unofficial-api-for-xhamster,unofficial-api-for-xnxx,unofficial-api-for-xvideos,unofficial-api-for-youporn,cachetools,tenacity,json5,six,platformdirs,tuf,securesystemslib,urllib3,unofficial-api-for-empflix,unofficial-api-for-tnaflix
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.allow_backup = True
presplash.filename = src/frontend/graphics/logo_square.png
android.ndk_path =
android.ndk = 28c
android.release_artifact = apk
android.sdk_path =
android.api = 36
android.minapi = 28
android.ndk_api = 28
android.no-byte-compile-python = True
p4a.bootstrap = qt
p4a.local_recipes = deployment/recipes
p4a.branch = develop
p4a.commit = HEAD
android.permissions = android.permission.INTERNET, android.permission.ACCESS_NETWORK_STATE, android.permission.WRITE_EXTERNAL_STORAGE
p4a.extra_args = --qt-libs=Core,Network,Gui,OpenGL,Widgets,Qml,Quick,QuickControls2,Test --load-local-libs=plugins_platforms_qtforandroid --init-classes=
icon.filename = src/frontend/graphics/logo_square.png

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = .

