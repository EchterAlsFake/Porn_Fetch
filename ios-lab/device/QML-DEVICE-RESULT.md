# Qt Quick / Material on the physical iPhone

On 2026-10-28, the source-built Qt 6.12.0 / iOS 15.0 ARM64 kit rendered the real `QtQuickPhoneHello` QML application on the iPhone 7 running iOS 15.8.8.

The result retrieved from the phone (`../build/qt-quick-phone-result.json`) reports Metal, a visible QML window, and a saved 750×1294 image read back from the rendered window. The image (`../build/qt-quick-phone.png`) was inspected and shows the expected Material-style title, text and button.

The user confirmed that the screen and button work. After their taps, the phone's result file recorded `taps: 5`, verifying physical touch events reached the QML handler and updated its live property.

No VM OpenGL/software-renderer overrides are used. The GPU entitlement and explicit scene metadata are applied by `finalize-qt-app.py`. The app links the same source-built Qt modules being packaged for Porn Fetch.

Source: `qt-quick-hello`. Rebuild: `sh build-qt-quick-hello.sh`. Install/launch: `sh deploy-app.sh QtQuickPhoneHello`. Bundle ID: `local.asuna.QtQuickPhoneHello`. Data container for this run: `/private/var/mobile/Containers/Data/Application/5AD63890-B1E7-456E-B96D-DDD75216860C`.
