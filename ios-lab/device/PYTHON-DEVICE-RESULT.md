# Embedded Python on the physical iPhone

On 2026-10-28, `PythonNative.app` launched on the iPhone 7 running iOS 15.8.8 / palera1n rootless. Its embedded CPython executed Python code before starting the UIKit event loop. The app remained running and wrote a JSON result in its own Documents directory.

Recorded output: `../build/python-native-device-result.json`.

- Python: 3.15.0rc2, official python.org iOS framework distributed for Qt for Python.
- Platform reported by Python: `ios`.
- Calculation: `sum(i*i for i in range(100)) == 328350`, assertion passed.
- Native executable: arm64, minimum iOS 15.0. Python framework minimum iOS 13.0.
- Bundle identifier: `local.asuna.PythonNative`.
- Installed path: `/var/jb/Applications/PythonNative.app`.
- Data container: `/private/var/mobile/Containers/Data/Application/1FD2BE24-8542-4488-B02C-7D9A6F01D7C2`.

Source: `python-native/main.m`; rebuild: `build-python-native.sh`. Both the executable and embedded Python framework were signed with the same upstream Procursus ldid used for HelloNative. Transfer used an uncompressed tar over SSH; registration used `uicache -p`; launch used `uiopen --bundleid`.

This test establishes CPython execution on this phone. Qt, PySide, native third party modules, and the full Porn Fetch app still need separate device validation.
