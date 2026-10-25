"""Verify CI specs keep app settings while replacing developer-local paths."""

import configparser
import runpy
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.build_android import update_buildozer_spec, update_pysidedeploy_spec

ROOT = Path(__file__).resolve().parents[3]
prepare = runpy.run_path(str(ROOT / "packaging/prepare_android_ci.py"))["prepare"]


class AndroidCIPreparationTests(unittest.TestCase):
    def test_ci_specs_preserve_runtime_settings_and_select_requested_build(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            (project / "packaging").mkdir()
            shutil.copyfile(ROOT / "packaging/pysidedeploy_android.spec",
                            project / "packaging/pysidedeploy_android.spec")
            shutil.copyfile(ROOT / "buildozer.spec", project / "buildozer.spec")
            original = configparser.ConfigParser(interpolation=None)
            original.read(project / "buildozer.spec")
            venv = project.parent / "external-venv"
            prepare(project, venv, "3.9.77")
            update_buildozer_spec(project / "buildozer.spec", "x86", project / "sdk", project / "ndk", project)
            update_pysidedeploy_spec(project / "pysidedeploy.spec", project / "pyside.whl",
                                    project / "shiboken.whl", project / "sdk", project / "ndk", project)
            build = configparser.ConfigParser(interpolation=None)
            build.read(project / "buildozer.spec")
            deploy = configparser.ConfigParser(interpolation=None)
            deploy.read(project / "pysidedeploy.spec")
            for key in ("package.name", "package.domain", "requirements", "android.permissions", "android.minapi"):
                self.assertEqual(build["app"][key], original["app"][key])
            self.assertEqual(build["app"]["version"], "3.9.77")
            self.assertEqual(build["app"]["android.archs"], "x86")
            self.assertEqual(build["app"]["android.api"], "36")
            self.assertNotIn("android.add_jars", build["app"])
            self.assertEqual(build["buildozer"]["bin_dir"], str(project))
            self.assertNotIn("/home/asuna/", str(dict(build["app"])))
            self.assertEqual(deploy["android"]["version"], "3.9.77")
            self.assertEqual(deploy["python"]["python_path"], str(venv / "bin/python"))
            self.assertEqual(deploy["app"]["project_file"], "")
            self.assertNotIn("arch", deploy["buildozer"])


if __name__ == "__main__":
    unittest.main()
