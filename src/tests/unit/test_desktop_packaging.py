"""Unit tests validating desktop deployment specifications and build scripts."""
import configparser
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class DesktopPackagingSpecTests(unittest.TestCase):
    def test_project_root_survives_relocating_desktop_specs(self):
        import PySide6

        # PySide's command wrappers add this directory for project_lib imports.
        scripts_dir = str(Path(PySide6.__file__).parent / "scripts")
        with patch.object(sys, "path", [scripts_dir, *sys.path]):
            from PySide6.scripts.deploy_lib.config import Config

        with tempfile.TemporaryDirectory() as temporary:
            for platform in ("linux", "windows", "macos"):
                with self.subTest(platform=platform):
                    source = PROJECT_ROOT / "packaging" / f"pysidedeploy_{platform}.spec"
                    relocated = Path(temporary) / source.name
                    shutil.copy2(source, relocated)
                    with patch.object(Config, "_find_qml_files", return_value=[]), \
                         patch.object(Config, "_find_excluded_qml_plugins", return_value=[]):
                        config = Config(relocated, PROJECT_ROOT / "main.py", Path("python"),
                                        dry_run=True, existing_config_file=True)
                    self.assertEqual(config.project_dir, PROJECT_ROOT)

    def test_linux_spec_configuration(self):
        spec_path = PROJECT_ROOT / "packaging" / "pysidedeploy_linux.spec"
        self.assertTrue(spec_path.is_file(), f"Spec missing: {spec_path}")
        parser = configparser.ConfigParser()
        parser.read(spec_path, encoding="utf-8")

        self.assertEqual(parser.get("app", "input_file"), "main.py")
        self.assertTrue(parser.get("app", "icon").endswith(".png"))

        modules = set(parser.get("qt", "modules").split(","))
        required = {"Core", "Gui", "Widgets", "Qml", "Quick", "QuickControls2", "Network", "OpenGL"}
        self.assertTrue(required.issubset(modules), f"Missing Qt modules: {required - modules}")

        plugins = set(parser.get("qt", "plugins").split(","))
        self.assertIn("qml", plugins)
        self.assertNotIn("platforms/darwin", plugins)

        self.assertEqual(parser.get("nuitka", "mode"), "onefile")
        extra_args = parser.get("nuitka", "extra_args")
        self.assertIn("--include-data-files=src/frontend/UI/*.qml=src/frontend/UI/", extra_args)

    def test_windows_spec_configuration(self):
        spec_path = PROJECT_ROOT / "packaging" / "pysidedeploy_windows.spec"
        self.assertTrue(spec_path.is_file(), f"Spec missing: {spec_path}")
        parser = configparser.ConfigParser()
        parser.read(spec_path, encoding="utf-8")

        self.assertEqual(parser.get("app", "input_file"), "main.py")
        self.assertTrue(parser.get("app", "icon").endswith(".ico"))

        modules = set(parser.get("qt", "modules").split(","))
        required = {"Core", "Gui", "Widgets", "Qml", "Quick", "QuickControls2", "Network", "OpenGL"}
        self.assertTrue(required.issubset(modules), f"Missing Qt modules: {required - modules}")

        plugins = set(parser.get("qt", "plugins").split(","))
        self.assertIn("qml", plugins)
        self.assertNotIn("platforms/darwin", plugins)
        self.assertNotIn("xcbglintegrations", plugins)

        self.assertEqual(parser.get("nuitka", "mode"), "onefile")
        extra_args = parser.get("nuitka", "extra_args")
        self.assertIn("--windows-console-mode=disable", extra_args)
        self.assertNotIn("--windows-disable-console", extra_args)

    def test_macos_spec_configuration(self):
        spec_path = PROJECT_ROOT / "packaging" / "pysidedeploy_macos.spec"
        self.assertTrue(spec_path.is_file(), f"Spec missing: {spec_path}")
        parser = configparser.ConfigParser()
        parser.read(spec_path, encoding="utf-8")

        self.assertEqual(parser.get("app", "input_file"), "main.py")
        self.assertTrue(parser.get("app", "icon").endswith(".icns"))

        modules = set(parser.get("qt", "modules").split(","))
        required = {"Core", "Gui", "Widgets", "Qml", "Quick", "QuickControls2", "Network", "OpenGL"}
        self.assertTrue(required.issubset(modules), f"Missing Qt modules: {required - modules}")
        self.assertNotIn("DBus", modules)

        plugins = set(parser.get("qt", "plugins").split(","))
        self.assertIn("qml", plugins)
        self.assertNotIn("xcbglintegrations", plugins)

        self.assertEqual(parser.get("nuitka", "mode"), "standalone")
        extra_args = parser.get("nuitka", "extra_args")
        self.assertNotIn("windows-console-mode", extra_args)
        self.assertNotIn("windows-disable-console", extra_args)

    def test_install_windows_script_spec_path_and_flags(self):
        script_path = PROJECT_ROOT / "scripts" / "install_windows.ps1"
        content = script_path.read_text(encoding="utf-8")
        self.assertIn(r"packaging\pysidedeploy_windows.spec", content)
        self.assertNotIn(r"src\build\pysidedeploy_windows.spec", content)
        self.assertIn("--keep-deployment-files", content)

    def test_install_sh_script_flags(self):
        script_path = PROJECT_ROOT / "scripts" / "install.sh"
        content = script_path.read_text(encoding="utf-8")
        self.assertIn("--keep-deployment-files", content)
        self.assertIn("read -rp \"Enter choice (0-${max_choice}) [${default_choice}]: \" choice </dev/tty", content)
        self.assertIn("Non-interactive shell detected", content)

    def test_ci_workflow_deploy_flags(self):
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "build_all.yml"
        content = workflow_path.read_text(encoding="utf-8")
        self.assertIn("pyside6-deploy -c \"$SPEC_FILE\" -f -v --keep-deployment-files", content)


class QtIFWStagingTests(unittest.TestCase):
    def test_prepare_staging_directory_linux_amd64(self):
        import importlib.util
        import tempfile

        spec = importlib.util.spec_from_file_location(
            "generate_repo_mod", PROJECT_ROOT / "packaging" / "generate_repository.py"
        )
        assert spec and spec.loader
        gen_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen_mod)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            dist_dir = tmp / "dist"
            dist_dir.mkdir()
            (dist_dir / "Porn Fetch").write_text("#!/bin/sh\necho hi\n")
            (dist_dir / "logo_transparent.png").write_bytes(b"fakepng")

            pb_file = tmp / "pocketbase"
            pb_file.write_text("#!/bin/sh\necho pb\n")

            staging_dir = tmp / "staging"
            config_xml, pkg_dir = gen_mod.prepare_staging_directory(
                staging_dir=staging_dir,
                dist_dir=dist_dir,
                pocketbase_binary=pb_file,
                target_platform="linux",
                target_arch="amd64",
                version="3.9.123",
            )

            self.assertTrue(config_xml.is_file())
            config_content = config_xml.read_text(encoding="utf-8")
            self.assertIn("<Url>https://api.pornfetch.to/repo/linux_amd64</Url>", config_content)
            self.assertIn("<Version>3.9.123</Version>", config_content)

            package_xml = pkg_dir / "com.echteralsfake.pornfetch" / "meta" / "package.xml"
            self.assertTrue(package_xml.is_file())
            package_content = package_xml.read_text(encoding="utf-8")
            self.assertIn("<Version>3.9.123</Version>", package_content)

            data_dir = pkg_dir / "com.echteralsfake.pornfetch" / "data"
            self.assertTrue((data_dir / "Porn Fetch").is_file())
            self.assertTrue((data_dir / "logo_transparent.png").is_file())
            self.assertTrue((data_dir / "pocketbase").is_file())

    def test_prepare_staging_directory_windows_amd64(self):
        import importlib.util
        import tempfile

        spec = importlib.util.spec_from_file_location(
            "generate_repo_mod", PROJECT_ROOT / "packaging" / "generate_repository.py"
        )
        assert spec and spec.loader
        gen_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen_mod)

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp = Path(tmp_dir)
            dist_dir = tmp / "dist"
            dist_dir.mkdir()
            (dist_dir / "Porn Fetch.exe").write_bytes(b"fakeexe")

            pb_file = tmp / "pocketbase.exe"
            pb_file.write_bytes(b"fakepbexe")

            staging_dir = tmp / "staging"
            config_xml, pkg_dir = gen_mod.prepare_staging_directory(
                staging_dir=staging_dir,
                dist_dir=dist_dir,
                pocketbase_binary=pb_file,
                target_platform="windows",
                target_arch="amd64",
                version="3.9.456",
            )

            self.assertTrue(config_xml.is_file())
            config_content = config_xml.read_text(encoding="utf-8")
            self.assertIn("<Url>https://api.pornfetch.to/repo/windows_amd64</Url>", config_content)
            self.assertIn("<Version>3.9.456</Version>", config_content)

            data_dir = pkg_dir / "com.echteralsfake.pornfetch" / "data"
            self.assertTrue((data_dir / "Porn Fetch.exe").is_file())
            self.assertTrue((data_dir / "pocketbase.exe").is_file())


if __name__ == "__main__":
    unittest.main()
