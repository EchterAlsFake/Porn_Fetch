"""Unit tests for the Android build automation script (scripts/build_android.py)."""
from __future__ import annotations

import configparser
import io
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts.build_android import (
    ANDROID_NDK_REVISION,
    PATTERN_CAN_READ,
    build_single_arch,
    detect_arch_from_filename,
    ensure_host_patches,
    extract_qt_jars,
    find_android_ndk,
    find_wheels_for_arch,
    main,
    normalize_arch,
    patch_pyside_wheel_if_needed,
    sign_apk,
    update_buildozer_spec,
    update_pysidedeploy_spec,
)
from scripts.patch_android_deploy import (
    patch_android_config_source,
    patch_android_utilities_source,
    patch_buildozer_source,
    patched_source,
    verify_android_config,
    verify_android_deploy,
    verify_android_utilities,
    verify_buildozer,
)


class TestApkSigning(unittest.TestCase):
    def test_align_sign_verify_and_publish(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            apk = root / "unsigned.apk"
            apk.write_bytes(b"unsigned")
            commands = []

            def run(command, **kwargs):
                commands.append(command)
                self.assertEqual(kwargs, {"check": True})  # Password prompts inherit stdin.
                if command[0] == "zipalign":
                    Path(command[-1]).write_bytes(b"aligned")
                elif command[1] == "sign":
                    output = Path(command[command.index("--out") + 1])
                    output.write_bytes(b"signed")
                    Path(str(output) + ".idsig").write_bytes(b"signature")
                return subprocess.CompletedProcess(command, 0)

            with patch("scripts.build_android.subprocess.run", side_effect=run):
                result = sign_apk(apk, root, root / "key.jks", "alias")
            self.assertEqual(result, root / "app-signed.apk")
            self.assertEqual(result.read_bytes(), b"signed")
            self.assertEqual((root / "app-aligned.apk").read_bytes(), b"aligned")
            self.assertTrue(Path(str(result) + ".idsig").exists())
            self.assertEqual(commands[0][:6], ["zipalign", "-p", "-f", "-v", "4", str(apk)])
            self.assertEqual(commands[1][1:6], ["sign", "--ks", str(root / "key.jks"), "--ks-key-alias", "alias"])
            self.assertEqual(commands[2][:3], ["apksigner", "verify", "--verbose"])

    def test_failed_signing_preserves_previous_signed_apk(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            previous = root / "app-signed-aarch64.apk"
            previous.write_bytes(b"previous release")
            with patch("scripts.build_android.subprocess.run",
                       side_effect=subprocess.CalledProcessError(1, "apksigner")):
                with self.assertRaises(subprocess.CalledProcessError):
                    sign_apk(root / "unsigned.apk", root, root / "key.jks", "alias", "aarch64")
            self.assertEqual(previous.read_bytes(), b"previous release")


class TestAndroidDeployToolchain(unittest.TestCase):
    def test_ndk_download_version_and_checksums_are_patched_together(self):
        source = '''ANDROID_NDK_VERSION = "27c"
_NDK_SHA1: dict[str, str] = {
    "linux": "old-linux-checksum",
    "darwin": "old-mac-checksum",
}
'''
        patched = patch_android_utilities_source(source)
        verify_android_utilities(patched)
        self.assertEqual(patch_android_utilities_source(patched), patched)
        namespace = {}
        exec(compile(patched, "android_utilities.py", "exec"), namespace)
        self.assertEqual(namespace["ANDROID_NDK_VERSION"], "28c")
        self.assertEqual(namespace["_NDK_SHA1"]["linux"], "a7b54a5de87fecd125a17d54f73c446199e72a64")

    def test_buildozer_cache_survives_deploy_cleanup_and_failure(self):
        source = '''# porn-fetch-buildozer-file-v1
import logging
import shutil
import traceback

def _cleanup_with_custom_spec(config, preserve_spec: bool) -> None:
    cleanup(config=config, is_android=not preserve_spec)
    if preserve_spec:
        build_dir = config.project_dir / ".buildozer"
        if build_dir.exists():
            shutil.rmtree(build_dir)

def main(config, fail=False, keep_deployment_files=False):
    dry_run = config.dry_run
    preserve_spec = True
    _cleanup_with_custom_spec(config, preserve_spec)
    try:
        config.generated_files_path.mkdir()
        (config.generated_files_path / "generated.jar").touch()
        if fail:
            raise RuntimeError("compiler failed")
        # move buildozer build files to {generated_files_path}
        if not dry_run:
            buildozer_build_dir = config.project_dir / ".buildozer"
            if not buildozer_build_dir.exists():
                logging.info(f"[DEPLOY] Unable to copy {buildozer_build_dir} to "
                             f"{config.generated_files_path}. {buildozer_build_dir} does not exist")
            logging.info(f"[DEPLOY] copy {buildozer_build_dir} to {config.generated_files_path}")
            shutil.move(buildozer_build_dir, config.generated_files_path)

    except Exception:
        print(f"Exception occurred: {traceback.format_exc()}")
    finally:
        if not keep_deployment_files:
            _cleanup_with_custom_spec(config, preserve_spec)
'''
        patched = patched_source(source)
        verify_android_deploy(patched)
        self.assertEqual(patched_source(patched), patched)
        with tempfile.TemporaryDirectory() as temporary:
            import shutil
            from types import SimpleNamespace

            root = Path(temporary)
            generated = root / "deployment"
            previous_cache = generated / ".buildozer"
            previous_cache.mkdir(parents=True)
            (previous_cache / "hostpython").write_bytes(b"compiled python")
            spec = root / "buildozer.spec"
            spec.write_text("[app]\n")
            config = SimpleNamespace(project_dir=root, generated_files_path=generated, dry_run=False)

            def cleanup(config, is_android):
                self.assertFalse(is_android)
                if generated.exists():
                    shutil.rmtree(generated)

            namespace = {"cleanup": cleanup}
            exec(compile(patched, "android_deploy.py", "exec"), namespace)
            # Upgrade an archived cache, then exercise consecutive builds and a failure.
            for keep in (True, False):
                namespace["main"](config, keep_deployment_files=keep)
                self.assertEqual(generated.exists(), keep)
                self.assertEqual((root / ".buildozer" / "hostpython").read_bytes(), b"compiled python")
                self.assertTrue(spec.exists())
            with patch("builtins.print"), self.assertRaisesRegex(RuntimeError, "compiler failed"):
                namespace["main"](config, fail=True)
            self.assertFalse(generated.exists())
            self.assertTrue((root / ".buildozer" / "hostpython").is_file())

    def test_android_config_detects_and_maps_local_32bit_wheels(self):
        source = '''# porn-fetch-custom-recipes-v1
import shutil


class AndroidConfig(Config):
    def _find_arch(self):
        arch = get_wheel_android_arch(wheel=self.wheel_pyside)
        if not arch:
            raise RuntimeError("PySide wheel corrupted")
        return arch
'''
        with self.assertRaisesRegex(ValueError, "32-bit Android"):
            verify_android_config(source)
        patched = patch_android_config_source(source)
        verify_android_config(patched)
        self.assertEqual(patch_android_config_source(patched), patched)
        namespace = {
            "Config": object,
            "platform_map": {"aarch64": "arm64-v8a", "x86_64": "x86_64",
                             "arm64-v8a": "arm64-v8a"},
            "get_wheel_android_arch": lambda wheel: next(
                (arch for arch in ("aarch64", "x86_64") if arch in wheel.stem), None),
        }
        exec(compile(patched, "android_config.py", "exec"), namespace)
        config = namespace["AndroidConfig"]()
        for arch, abi in (("armv7a", "armeabi-v7a"), ("i686", "x86"),
                          ("aarch64", "arm64-v8a"), ("x86_64", "x86_64")):
            with self.subTest(arch=arch):
                config.wheel_pyside = Path(f"pyside6-6.12.0-cp314-cp314-android_{arch}.whl")
                detected = config._find_arch()
                self.assertEqual(detected, arch)
                self.assertEqual(namespace["platform_map"][detected], abi)

    def test_deployment_failure_propagates_after_cleanup(self):
        source = '''# porn-fetch-buildozer-file-v1
# porn-fetch-buildozer-cache-v1
import traceback

def main():
    try:
        raise RuntimeError("compiler failed")
    except Exception:
        print(f"Exception occurred: {traceback.format_exc()}")
    finally:
        cleanup()
'''
        with self.assertRaisesRegex(ValueError, "failure propagation"):
            verify_android_deploy(source)
        patched = patched_source(source)
        verify_android_deploy(patched)
        self.assertEqual(patched_source(patched), patched)
        cleaned = []
        namespace = {"cleanup": lambda: cleaned.append(True)}
        exec(compile(patched, "android_deploy.py", "exec"), namespace)
        with patch("builtins.print"), self.assertRaisesRegex(RuntimeError, "compiler failed"):
            namespace["main"]()
        self.assertEqual(cleaned, [True])

    def test_pyside_612_release_pin_is_replaced_with_develop_head(self):
        source = '''P4A_BRANCH = "master"
P4A_COMMIT = "58d21141f17c889bf8585f5665921d72028f8831"

class BuildozerConfig:
    def configure(self):
        pkg_domain = "to.pornfetch"
        extra_reqs = pysidedeploy_config
        qt_priority = {}
        # android platform specific
        self.set_value("app", "p4a.branch", P4A_BRANCH)
        self.set_value("app", "p4a.commit", P4A_COMMIT)
'''
        with self.assertRaisesRegex(ValueError, "develop/HEAD"):
            verify_buildozer(source)
        patched = patch_buildozer_source(source)
        verify_buildozer(patched)
        self.assertEqual(patch_buildozer_source(patched), patched)
        namespace = {}
        exec(compile(patched, "buildozer.py", "exec"), namespace)
        settings = {}
        config = namespace["BuildozerConfig"]()
        config.set_value = lambda section, key, value: settings.update({key: value})
        namespace["pysidedeploy_config"] = object()
        config.configure()
        self.assertEqual(settings, {"p4a.branch": "develop", "p4a.commit": "HEAD",
                                    "android.ndk": "28c", "android.release_artifact": "apk"})

    def test_pyside_611_keeps_develop_branch(self):
        source = '''class BuildozerConfig:
    def configure(self):
        pkg_domain = "to.pornfetch"
        extra_reqs = pysidedeploy_config
        qt_priority = {}
        # android platform specific
        self.set_value("app", "p4a.branch", "develop")
'''
        patched = patch_buildozer_source(source)
        self.assertEqual(patch_buildozer_source(patched), patched)
        verify_buildozer(patched)


class TestAndroidBuildAutomation(unittest.TestCase):
    def test_custom_native_recipes_survive_deployment_cleanup(self):
        import logging
        import shutil

        source = '''# porn-fetch-32bit-android-arch-v1
import shutil

class AndroidConfig:
    def find_recipe_dir(self):
        recipe_dir = None
        if not self.dry_run:
            recipe_dir = ((self.generated_files_path
                           / "recipes").resolve())

        return recipe_dir
'''
        namespace = {"Path": Path, "logging": logging}
        exec(compile(patch_android_config_source(source), "android_config.py", "exec"), namespace)
        project = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            shutil.copytree(project / "p4a-recipes", root / "p4a-recipes")
            generated = root / "deployment"
            generated.mkdir()
            shutil.rmtree(generated)  # PySide's cleanup happens before find_recipe_dir.
            config = namespace["AndroidConfig"]()
            config.recipe_dir = generated / "recipes"
            config.generated_files_path = generated
            config.source_file = root / "main.py"
            config.project_dir = root
            config.dry_run = False
            config.get_value = lambda *args, **kwargs: str(root / "p4a-recipes")
            destination = config.find_recipe_dir()
            for name in ("cryptography", "curl_cffi", "libcurl_impersonate"):
                self.assertEqual((destination / name / "__init__.py").read_bytes(),
                                 (project / "p4a-recipes" / name / "__init__.py").read_bytes())

    def test_clean_build_extracts_and_registers_qt_activity_jars(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            wheel = root / "pyside.whl"
            bindings = io.BytesIO()
            with zipfile.ZipFile(bindings, "w") as jar:
                jar.writestr("org/qtproject/qt/android/bindings/QtActivity.class", b"activity")
            with zipfile.ZipFile(wheel, "w") as bundle:
                bundle.writestr("PySide6/jar/Qt6AndroidBindings.jar", bindings.getvalue())
                bundle.writestr("PySide6/jar/Qt6Android.jar", b"qt")
            spec = root / "buildozer.spec"
            spec.write_text("[app]\ntitle = Porn Fetch\n")
            extract_qt_jars(wheel, root)
            update_buildozer_spec(spec, "arm64-v8a", root / "sdk", root / "ndk", root)
            config = configparser.ConfigParser()
            config.read(spec)
            jars = config["app"]["android.add_jars"].split(",")
            self.assertEqual({Path(name).name for name in jars}, {"Qt6Android.jar", "Qt6AndroidBindings.jar"})
            for name in jars:
                self.assertTrue(Path(name).is_file())

    def test_ndk_discovery_requires_r28c_even_with_stale_environment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            ndk = root / ".pyside6_android_deploy/android-ndk/android-ndk-r28c"
            old_ndk = root / "android-ndk-r27c"
            for directory, revision in ((ndk, ANDROID_NDK_REVISION), (old_ndk, "27.2.12479018")):
                directory.mkdir(parents=True)
                (directory / "source.properties").write_text(f"Pkg.Revision = {revision}\n")
            with patch("scripts.build_android.Path.home", return_value=root), \
                 patch.dict("os.environ", {"ANDROID_NDK_HOME": str(old_ndk),
                                            "ANDROID_NDK_ROOT": str(old_ndk), "ANDROIDNDK": str(old_ndk)}):
                self.assertEqual(find_android_ndk(), ndk)
                with self.assertRaisesRegex(ValueError, "r28c"):
                    find_android_ndk(old_ndk)

    def test_host_qtasyncio_patch_failure_stops_build(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            patcher = root / "scripts" / "patch_qtasyncio.py"
            patcher.touch()
            with patch("scripts.build_android.subprocess.run") as run:
                ensure_host_patches(root, root / "venv")
                self.assertEqual(run.call_count, 2)
                self.assertEqual(run.call_args.args[0][-1], "--verify")
                self.assertTrue(all(call.kwargs["check"] for call in run.call_args_list))
            import subprocess
            with patch("scripts.build_android.subprocess.run",
                       side_effect=subprocess.CalledProcessError(2, "patch_qtasyncio.py")):
                with self.assertRaises(subprocess.CalledProcessError):
                    ensure_host_patches(root, root / "venv")

    def test_missing_host_qtasyncio_patcher_stops_build(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(FileNotFoundError):
                ensure_host_patches(Path(temporary), Path(temporary) / "venv")

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
            (directory / "source.properties").write_text(f"Pkg.Revision = {ANDROID_NDK_REVISION}\n")
            args = ["build_android.py", "--dry-run", "--venv", str(directory),
                    "--sdk-path", str(directory), "--ndk-path", str(directory)]
            with patch.object(sys, "argv", args), patch("scripts.build_android.ensure_host_patches") as host:
                with patch("scripts.build_android.find_wheels_for_arch", return_value=(directory, directory)), \
                     patch("scripts.build_android.build_single_arch", wraps=build_single_arch) as build:
                    self.assertEqual(main(), 0)
                    self.assertEqual(build.call_args.kwargs["build_mode"], "release")
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
            config = configparser.ConfigParser()
            config.read(spec_path)
            self.assertEqual(config["app"]["android.ndk"], "28c")
            self.assertEqual(config["app"]["android.release_artifact"], "apk")

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

    def test_regenerated_buildozer_spec_recovers_application_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            spec = root / "buildozer.spec"
            spec.write_text(
                "[app]\ntitle = Porn Fetch\npackage.name = Porn Fetch\n"
                "package.domain = org.Porn Fetch\nversion = 0.1\n"
                "requirements = python3,shiboken6,PySide6\n"
                "p4a.branch = master\np4a.commit = release-commit\n"
                "[buildozer]\nlog_level = 2\n",
                encoding="utf-8",
            )
            (root / "pysidedeploy.spec").write_text(
                "[android]\npackage_name = app\npackage_domain = to.pornfetch\n"
                "version = 3.9\nrequirements = certifi,cffi,curl_cffi\n",
                encoding="utf-8",
            )

            update_buildozer_spec(spec, "arm64-v8a", root / "sdk", root / "ndk", root)

            config = configparser.ConfigParser()
            config.read(spec)
            self.assertEqual(config["app"]["title"], "Porn Fetch")
            self.assertEqual(config["app"]["package.name"], "app")
            self.assertEqual(config["app"]["package.domain"], "to.pornfetch")
            self.assertEqual(config["app"]["version"], "3.9")
            self.assertEqual(config["app"]["requirements"],
                             "python3,shiboken6,PySide6,certifi,cffi,curl_cffi")
            self.assertEqual(config["app"]["p4a.branch"], "develop")
            self.assertEqual(config["app"]["p4a.commit"], "HEAD")
            self.assertEqual(config["buildozer"]["log_level"], "2")

    def test_release_build_returns_apk_and_ignores_aab_and_debug_apk(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "old-arm64-v8a-debug.apk").write_bytes(b"old")
            output = root / "app-arm64-v8a-release-unsigned.apk"

            def deploy(*args, **kwargs):
                output.write_bytes(b"new")
                (root / "app-arm64-v8a-release.aab").write_bytes(b"bundle")
                (root / "app-arm64-v8a-debug.apk").write_bytes(b"debug")
                for variable in ("ANDROIDNDK", "ANDROID_NDK_HOME", "ANDROID_NDK_ROOT"):
                    self.assertEqual(kwargs["env"][variable], str(root / "ndk"))
                return type("Result", (), {"returncode": 0})()

            with patch("scripts.build_android.patch_pyside_wheel_if_needed"), \
                 patch("scripts.build_android.extract_qt_jars"), \
                 patch("scripts.build_android.update_buildozer_spec"), \
                 patch("scripts.build_android.update_pysidedeploy_spec"), \
                 patch("scripts.build_android.inject_android_templates"), \
                 patch("scripts.build_android.subprocess.run", side_effect=deploy):
                result = build_single_arch("aarch64", root / "pyside.whl", root / "shiboken.whl",
                                           root, root / "venv", root / "sdk", root / "ndk",
                                           build_mode="release", output_dir=root / "output")
            self.assertIsNotNone(result)
            self.assertEqual(result.suffix, ".apk")
            self.assertEqual(result.read_bytes(), b"new")

    def test_ndk_upgrade_rebuilds_once_and_clean_keeps_downloads_and_other_archs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archived = root / "deployment" / ".buildozer"
            downloads = Path("android/platform/build-arm64-v8a/packages/hostpython3/Python.tar.gz")
            selected = Path("android/platform/build-arm64-v8a/build/other_builds/hostpython3/hostpython")
            distribution = Path("android/platform/build-arm64-v8a/dists/app/dist_info.json")
            other = Path("android/platform/build-armeabi-v7a/build/other_builds/hostpython3/hostpython")
            for relative in (downloads, selected, distribution, other):
                path = archived / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"cached")

            def deploy(*args, **kwargs):
                cache = root / ".buildozer"
                self.assertFalse(archived.exists())
                self.assertEqual((cache / selected).exists(), iteration == 1)
                self.assertEqual((cache / distribution).exists(), iteration == 1)
                self.assertEqual((cache / downloads).read_bytes(), b"cached")
                self.assertEqual((cache / other).read_bytes(), b"cached")
                for relative in (selected, distribution):
                    path = cache / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(b"rebuilt")
                (root / "app-arm64-v8a-release.apk").write_bytes(b"new")
                return type("Result", (), {"returncode": 0})()

            with patch("scripts.build_android.patch_pyside_wheel_if_needed"), \
                 patch("scripts.build_android.extract_qt_jars"), \
                 patch("scripts.build_android.update_buildozer_spec"), \
                 patch("scripts.build_android.update_pysidedeploy_spec"), \
                 patch("scripts.build_android.inject_android_templates"), \
                 patch("scripts.build_android.subprocess.run", side_effect=deploy):
                for iteration, clean in enumerate((False, False, True)):
                    build_single_arch("aarch64", root / "pyside.whl", root / "shiboken.whl",
                                      root, root / "venv", root / "sdk", root / "ndk", clean=clean)

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
