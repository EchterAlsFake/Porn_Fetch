"""Check portable iOS staging without invoking Apple's toolchain."""

import configparser
import json
import os
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]


class IOSPreparationTests(unittest.TestCase):
    def test_staging_uses_published_device_pair_runtime_and_release_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            device = root / "lab/device"
            source = root / "source"
            ui = source / "src/frontend/UI"
            ui.mkdir(parents=True)
            (ui / "Main.qml").write_text("import QtQuick\nItem {}\n")
            vendor = root / "lab/pornfetch/vendor"
            vendor.mkdir(parents=True)
            (vendor / "dependency.py").write_text("value = 1\n")
            native = device / "native/packages"
            native.mkdir(parents=True)
            (native / "_ios_ffmpeg.cpython-315-iphoneos.so").write_bytes(b"device extension")
            template = device / "python-qt-hello/pysidedeploy.spec"
            template.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "ios-lab/device/python-qt-hello/pysidedeploy.spec", template)
            script = device / "prepare-application.py"
            shutil.copyfile(ROOT / "ios-lab/device/prepare-application.py", script)
            wheels = device / "wheels"
            wheels.mkdir()
            for package in ("pyside6", "shiboken6"):
                (wheels / f"{package}-6.12.0-6.12.0-cp315-cp315-ios_arm64.whl").touch()
            # Another ABI must never be selected, even when it sorts first.
            (wheels / "pyside6-0-cp314-cp314-ios_arm64_simulator.whl").touch()
            project = device / "app/deployment/ios_arm64/PornFetch.xcodeproj/project.pbxproj"

            def deploy(command, **kwargs):
                if Path(command[0]).name == "pyside6-ios-deploy":
                    project.parent.mkdir(parents=True)
                    project.write_text('/* Copy Python Packages */ = { shellScript = "original"; };')

            environment = {
                "PORN_FETCH_SOURCE": str(source), "IOS_DEPLOY_VENV": str(root / "venv"),
                "IOS_PYTHON_XCFRAMEWORK": str(root / "runtime/Python.xcframework"),
                "IOS_APP_VERSION": "3.9.77", "DEVELOPER_DIR": "/Applications/Xcode.app/Contents/Developer",
            }
            with patch.dict(os.environ, environment), patch("subprocess.run", side_effect=deploy), \
                    patch("subprocess.check_output", return_value=environment["DEVELOPER_DIR"]), \
                    patch("sys.argv", [str(script)]):
                runpy.run_path(str(script), run_name="__main__")

            config = configparser.ConfigParser()
            config.read(device / "app/pysidedeploy.spec")
            self.assertEqual(config["ios"]["version"], "3.9.77")
            self.assertEqual(config["ios"]["xcframework_path"], environment["IOS_PYTHON_XCFRAMEWORK"])
            self.assertEqual(config["ios"]["wheel_pyside"],
                             str(wheels / "pyside6-6.12.0-6.12.0-cp315-cp315-ios_arm64.whl"))
            self.assertEqual(config["app"]["icon"], "")
            self.assertEqual((device / "vendor/_ios_ffmpeg.cpython-315-iphoneos.so").read_bytes(),
                             b"device extension")
            self.assertTrue((device / "app/src/frontend/UI/Main.qml").is_file())
            self.assertIn(json.dumps(str(device / "bundle-vendor.sh"))[1:-1], project.read_text())


if __name__ == "__main__":
    unittest.main()
