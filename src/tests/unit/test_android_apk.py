"""Guard the Android 13 native-library extraction failure before publication."""
import tempfile
import unittest
import zipfile
from pathlib import Path

from src.tests.unit.test_cli_self_update import load_script

checker = load_script("check_android_apk")


class AndroidApkTests(unittest.TestCase):
    def test_native_preloads_are_present_and_extractable(self):
        for abi in ("arm64-v8a", "armeabi-v7a", "x86", "x86_64"):
            with self.subTest(abi=abi), tempfile.TemporaryDirectory() as directory:
                apk = Path(directory) / "app.apk"
                with zipfile.ZipFile(apk, "w") as archive:
                    for name in ("libQtCore.abi3.so", "libpyside6.abi3.so", "libshiboken6.abi3.so",
                                 "libpython3.15.so", "libTor.so", f"libQt6Svg_{abi}.so",
                                 f"libplugins_imageformats_qsvg_{abi}.so",
                                 f"libplugins_iconengines_qsvgicon_{abi}.so"):
                        archive.writestr(f"lib/{abi}/{name}", b"native library")
                checker.check_apk(apk, abi)
                with zipfile.ZipFile(apk, "a") as archive:
                    archive.writestr(f"lib/{abi}/QtCore.abi3.so", b"not extracted on Android 13")
                with self.assertRaisesRegex(ValueError, "Invalid native libraries"):
                    checker.check_apk(apk, abi)

    def test_svg_plugins_are_required_before_publication(self):
        abi = "arm64-v8a"
        with tempfile.TemporaryDirectory() as directory:
            apk = Path(directory) / "app.apk"
            with zipfile.ZipFile(apk, "w") as archive:
                for name in ("libQtCore.abi3.so", "libpyside6.abi3.so", "libshiboken6.abi3.so",
                             "libpython3.15.so", "libTor.so", f"libQt6Svg_{abi}.so"):
                    archive.writestr(f"lib/{abi}/{name}", b"native library")
            with self.assertRaisesRegex(ValueError, "libplugins_imageformats_qsvg"):
                checker.check_apk(apk, abi)
