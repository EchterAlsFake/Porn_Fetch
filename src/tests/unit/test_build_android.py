"""Unit tests for the Android build automation script (scripts/build_android.py)."""
from __future__ import annotations

import configparser
import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts.build_android import (
    PATTERN_CAN_READ,
    build_single_arch,
    detect_arch_from_filename,
    find_wheels_for_arch,
    main,
    normalize_arch,
    patch_pyside_wheel_if_needed,
    update_buildozer_spec,
    update_pysidedeploy_spec,
)


class TestAndroidBuildAutomation(unittest.TestCase):
    def test_normalize_arch(self) -> None:
        """Architecture normalization should map aliases to canonical names."""
        self.assertEqual(normalize_arch("aarch64"), "aarch64")
        self.assertEqual(normalize_arch("arm64-v8a"), "aarch64")
        self.assertEqual(normalize_arch("arm64"), "aarch64")
        self.assertEqual(normalize_arch("ARM64-V8A"), "aarch64")

        self.assertEqual(normalize_arch("armv7a"), "armv7a")
        self.assertEqual(normalize_arch("armeabi-v7a"), "armv7a")
        self.assertEqual(normalize_arch("armeabi"), "armv7a")

        self.assertEqual(normalize_arch("x86_64"), "x86_64")
        self.assertEqual(normalize_arch("amd64"), "x86_64")

        self.assertEqual(normalize_arch("i686"), "i686")
        self.assertEqual(normalize_arch("x86"), "i686")

        self.assertEqual(normalize_arch("all"), "all")

        with self.assertRaises(ValueError):
            normalize_arch("mips")

    def test_detect_arch_from_filename(self) -> None:
        """Wheel filename inspection should identify canonical architectures."""
        self.assertEqual(
            detect_arch_from_filename("pyside6-6.11.2-cp314-cp314-android_aarch64.whl"),
            "aarch64",
        )
        self.assertEqual(
            detect_arch_from_filename("pyside6-6.11.2-cp314-cp314-android_armv7a.whl"),
            "armv7a",
        )
        self.assertEqual(
            detect_arch_from_filename("pyside6-6.11.2-cp314-cp314-android_x86_64.whl"),
            "x86_64",
        )
        self.assertEqual(
            detect_arch_from_filename("pyside6-6.11.2-cp314-cp314-android_i686.whl"),
            "i686",
        )
        self.assertIsNone(detect_arch_from_filename("unknown_package.whl"))

    def test_x86_wheel_search_does_not_select_x86_64(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            for package in ("pyside6", "shiboken6"):
                (directory / f"{package}-6.11.2-cp314-cp314-android_x86_64.whl").touch()
            self.assertEqual(find_wheels_for_arch("i686", [directory], None, None), (None, None))

    def test_dry_run_does_not_patch_host(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            args = ["build_android.py", "--dry-run", "--venv", str(directory),
                    "--sdk-path", str(directory), "--ndk-path", str(directory)]
            with patch.object(sys, "argv", args), patch("scripts.build_android.ensure_host_patches") as host:
                with patch("scripts.build_android.find_wheels_for_arch", return_value=(directory, directory)):
                    self.assertEqual(main(), 0)
            host.assert_not_called()

    def test_update_buildozer_spec(self) -> None:
        """update_buildozer_spec should update target arch and file paths."""
        initial_spec = """[app]
title = Porn Fetch
android.archs = arm64-v8a
android.sdk_path = /old/sdk
android.ndk_path = /old/ndk
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = Path(tmpdir) / "buildozer.spec"
            spec_path.write_text(initial_spec, encoding="utf-8")

            update_buildozer_spec(
                spec_path=spec_path,
                buildozer_arch="armeabi-v7a",
                sdk_path=Path("/new/sdk"),
                ndk_path=Path("/new/ndk"),
                project_root=Path("/project"),
            )

            result = spec_path.read_text(encoding="utf-8")
            self.assertIn("android.archs = armeabi-v7a", result)
            self.assertIn("android.sdk_path = /new/sdk", result)
            self.assertIn("android.ndk_path = /new/ndk", result)

    def test_update_pysidedeploy_spec(self) -> None:
        """update_pysidedeploy_spec should update wheel paths and mode."""
        initial_spec = """[android]
wheel_pyside = /old/pyside.whl
wheel_shiboken = /old/shiboken.whl
[buildozer]
mode = debug
arch = aarch64
[nuitka]
mode = onefile
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = Path(tmpdir) / "pysidedeploy.spec"
            spec_path.write_text(initial_spec, encoding="utf-8")

            new_pyside = Path(tmpdir) / "new_pyside.whl"
            new_shiboken = Path(tmpdir) / "new_shiboken.whl"
            new_pyside.touch()
            new_shiboken.touch()

            update_pysidedeploy_spec(
                spec_path=spec_path,
                wheel_pyside=new_pyside,
                wheel_shiboken=new_shiboken,
                sdk_path=Path("/new/sdk"),
                ndk_path=Path("/new/ndk"),
                project_root=Path("/project"),
                mode="release",
            )

            result = spec_path.read_text(encoding="utf-8")
            self.assertIn(f"wheel_pyside = {new_pyside.resolve()}", result)
            self.assertIn(f"wheel_shiboken = {new_shiboken.resolve()}", result)
            self.assertIn("mode = release", result)
            config = configparser.ConfigParser()
            config.read(spec_path)
            self.assertEqual(config["nuitka"]["mode"], "onefile")
            self.assertNotIn("arch", config["buildozer"])
            self.assertEqual(config["app"]["icon"], "/project/src/frontend/graphics/logo_transparent.png")
            self.assertEqual(config["android"]["extra_recipes_dir"], "/project/p4a-recipes")

    def test_release_build_returns_new_aab_instead_of_old_apk(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "old-arm64-v8a-debug.apk").write_bytes(b"old")
            output = root / "app-arm64-v8a-release.aab"

            def deploy(*args, **kwargs):
                output.write_bytes(b"new")
                return type("Result", (), {"returncode": 0})()

            with patch("scripts.build_android.patch_pyside_wheel_if_needed"), \
                 patch("scripts.build_android.update_buildozer_spec"), \
                 patch("scripts.build_android.update_pysidedeploy_spec"), \
                 patch("scripts.build_android.inject_android_templates"), \
                 patch("scripts.build_android.subprocess.run", side_effect=deploy):
                result = build_single_arch("aarch64", root / "pyside.whl", root / "shiboken.whl",
                                           root, root / "venv", root / "sdk", root / "ndk",
                                           build_mode="release", output_dir=root / "output")
            self.assertIsNotNone(result)
            self.assertEqual(result.suffix, ".aab")
            self.assertEqual(result.read_bytes(), b"new")

    def test_patch_pyside_wheel_if_needed(self) -> None:
        """Mock wheel containing unpatched assets should be patched and verified."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = Path(tmpdir)
            whl_path = tmp_root / "test-1.0-cp314-android_aarch64.whl"

            # Create inner jar with unpatched pattern
            inner_jar_buf = io.BytesIO()
            with zipfile.ZipFile(inner_jar_buf, "w") as jz:
                jz.writestr(
                    "org/qtproject/qt/android/QtContentFileEngine.class",
                    b"header" + PATTERN_CAN_READ + b"footer",
                )
            inner_jar_bytes = inner_jar_buf.getvalue()

            # Create mock wheel
            with zipfile.ZipFile(whl_path, "w") as wz:
                wz.writestr("PySide6/QtAsyncio/events.py", "unpatched events code\n")
                wz.writestr("PySide6/jar/Qt6Android.jar", inner_jar_bytes)
                wz.writestr(
                    "test-1.0.dist-info/RECORD",
                    "PySide6/QtAsyncio/events.py,,\nPySide6/jar/Qt6Android.jar,,\n",
                )

            # Create mock host venv with patched QtAsyncio
            venv_asyncio = tmp_root / "venv" / "lib" / "python3.14" / "site-packages" / "PySide6" / "QtAsyncio"
            venv_asyncio.mkdir(parents=True, exist_ok=True)
            (venv_asyncio / "events.py").write_text("# qtasyncio-compat-v2\nclass Ev: pass\n")
            (venv_asyncio / "futures.py").write_text("# futures\n")
            (venv_asyncio / "tasks.py").write_text("# tasks\n")

            patched = patch_pyside_wheel_if_needed(whl_path, tmp_root / "venv")
            self.assertTrue(patched)

            # Verify contents
            with zipfile.ZipFile(whl_path, "r") as rz:
                events_code = rz.read("PySide6/QtAsyncio/events.py").decode("utf-8")
                self.assertIn("qtasyncio-compat-v2", events_code)

                jar_data = rz.read("PySide6/jar/Qt6Android.jar")
                with zipfile.ZipFile(io.BytesIO(jar_data), "r") as jrz:
                    cls_bytes = jrz.read("org/qtproject/qt/android/QtContentFileEngine.class")
                    self.assertNotIn(PATTERN_CAN_READ, cls_bytes)
                    self.assertIn(bytes([0x04, 0xac]), cls_bytes)

            # Second run should detect already patched
            patched_again = patch_pyside_wheel_if_needed(whl_path, tmp_root / "venv")
            self.assertFalse(patched_again)


if __name__ == "__main__":
    unittest.main()
