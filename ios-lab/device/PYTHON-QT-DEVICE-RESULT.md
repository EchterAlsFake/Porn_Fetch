# Embedded Python and custom PySide on the physical iPhone

On 2026-10-28, `PythonQtPhoneHello.app` launched on the physical iPhone 7 / iOS 15.8.8 using embedded CPython 3.15.0rc2 and custom-built Qt/PySide 6.12.0 targeting arm64/iOS 15.0. It imports the real static Core/Gui bindings, creates a QGuiApplication and QWindow, and paints text with QPainter/QBackingStore repeatedly.

Result copied from the phone: `../build/python-qt-device-result.json`. It records Python, PySide and Qt versions, `platform: ios`, an exposed/active window and a growing frame count. The process remains running and no new crash report appeared. The user visually confirmed the actual phone displays **“Hello Python + Qt! Python 3.15 / Qt 6.12.0 on your real iPhone 7”**. Thus real on-screen Python/PySide/Qt execution is established on this device.

The earlier C++ widget probe required explicit GPU driver entitlements: without `com.apple.security.iokit-user-client-class`, both Metal and GLES device/context creation failed and the user saw black. With `qt-app.entitlements.plist`, the app reports Apple A10 GPU and GLES 3 availability, and Qt logs successful Metal swapchain composition/presentation. No global jailbreak or sandbox settings were changed.

The first verified device wheels contained Core, Gui and Network; copies are retained in `artifacts/proven-core-wheels`. The full Qml/Quick/Controls/OpenGL/Svg bindings were subsequently built and used by the real Porn Fetch app. Source and commands are in `python-qt-hello`, `prepare-python-qt-hello.py`, `build-python-qt-hello.sh`, `pyside-ios15-toolchain.cmake` and `build-pyside.sh`.

Bundle identifier: `local.asuna.PythonQtPhoneHello`. Executable: `PythonQtPhoneHello_bin`. Installed path: `/var/jb/Applications/PythonQtPhoneHello.app`. Data container at this run: `/private/var/mobile/Containers/Data/Application/1CE20CE9-BE53-4420-8F01-0F6EED8E5AFE`.

The finalizer signs each embedded framework and the main executable with upstream Procursus ldid; the main executable additionally receives the GPU-only entitlement. It also supplies explicit iOS scene metadata and strips the stdlib test suite/desktop tools on subsequent builds.
