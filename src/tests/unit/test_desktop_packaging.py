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
                        config = Config(relocated, PROJECT_ROOT / "main.py",
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
        required = {"Core", "Gui", "Qml", "Quick", "QuickControls2", "Network", "OpenGL"}
        self.assertTrue(required.issubset(modules), f"Missing Qt modules: {required - modules}")
        self.assertNotIn("Widgets", modules)

        plugins = set(parser.get("qt", "plugins").split(","))
        self.assertIn("qml", plugins)
        self.assertNotIn("platforms/darwin", plugins)

        self.assertEqual(parser.get("nuitka", "mode"), "standalone")
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
        required = {"Core", "Gui", "Qml", "Quick", "QuickControls2", "Network", "OpenGL"}
        self.assertTrue(required.issubset(modules), f"Missing Qt modules: {required - modules}")
        self.assertNotIn("Widgets", modules)

        plugins = set(parser.get("qt", "plugins").split(","))
        self.assertIn("qml", plugins)
        self.assertNotIn("platforms/darwin", plugins)
        self.assertNotIn("xcbglintegrations", plugins)

        self.assertEqual(parser.get("nuitka", "mode"), "standalone")
        extra_args = parser.get("nuitka", "extra_args")
        self.assertIn("--windows-console-mode=attach", extra_args)
        exclusions = parser.get("qt", "excluded_qml_plugins").split(",")
        self.assertNotIn("QtTest", exclusions)
        self.assertNotEqual(exclusions, [""], "Automatic exclusions remove QtTest")
        self.assertNotIn("--windows-disable-console", extra_args)

    def test_macos_spec_configuration(self):
        spec_path = PROJECT_ROOT / "packaging" / "pysidedeploy_macos.spec"
        self.assertTrue(spec_path.is_file(), f"Spec missing: {spec_path}")
        parser = configparser.ConfigParser()
        parser.read(spec_path, encoding="utf-8")

        self.assertEqual(parser.get("app", "input_file"), "main.py")
        self.assertTrue(parser.get("app", "icon").endswith(".icns"))

        modules = set(parser.get("qt", "modules").split(","))
        required = {"Core", "Gui", "Qml", "Quick", "QuickControls2", "Network", "OpenGL"}
        self.assertTrue(required.issubset(modules), f"Missing Qt modules: {required - modules}")
        self.assertNotIn("Widgets", modules)
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
    def test_optional_tools_are_excluded_from_core_on_desktop_platforms(self):
        import importlib.util
        import xml.etree.ElementTree as ET

        spec = importlib.util.spec_from_file_location(
            "generate_repo_mod", PROJECT_ROOT / "packaging" / "generate_repository.py"
        )
        assert spec and spec.loader
        gen_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gen_mod)
        core = "to.pornfetch.echteralsfake"

        for platform in ("linux", "windows", "darwin"):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as directory:
                tmp = Path(directory)
                dist = tmp / "dist"
                app_dir = dist / "Porn Fetch.app/Contents/MacOS" if platform == "darwin" else dist
                app_dir.mkdir(parents=True)
                suffix = ".exe" if platform == "windows" else ""
                executable = "main.bin" if platform == "linux" else f"Porn Fetch{suffix}"
                (app_dir / executable).write_bytes(b"application")
                tools = app_dir / "third_party"
                tools.mkdir()
                for tool in ("pocketbase", "ffmpeg"):
                    name = tool + suffix
                    (tmp / name).write_bytes(tool.encode())
                    # Portable builds can already contain duplicate tool copies and sidecars.
                    for parent in (app_dir, tools):
                        (parent / name).write_bytes(tool.encode())
                        (parent / f"{name}.sha256").write_text("checksum")
                config, packages = gen_mod.prepare_staging_directory(
                    tmp / "staging", dist, tmp / f"pocketbase{suffix}",
                    platform, "amd64", "3.9.123", tmp / f"ffmpeg{suffix}",
                )
                settings = ET.parse(config)
                self.assertEqual(settings.findtext("WizardStyle"), "Modern")
                self.assertTrue((config.parent / settings.findtext("StyleSheet")).is_file())
                self.assertEqual(settings.findtext("RemoteRepositories/Repository/Url"),
                                 f"https://api.pornfetch.to/repo/{platform}_amd64")
                data = packages / core / "data"
                relative_app = app_dir.relative_to(dist) / f"Porn Fetch{suffix}"
                self.assertEqual((data / relative_app).read_bytes(), b"application")
                if platform == "linux":
                    self.assertEqual((data / relative_app).stat().st_mode & 0o777, 0o755)
                self.assertFalse(any(p.name.startswith(("pocketbase", "ffmpeg")) for p in data.rglob("*")
                                     if p.is_file()))
                self.assertTrue((tools / f"pocketbase{suffix}").is_file(), "Source bundle was modified")
                metadata = ET.parse(packages / core / "meta/package.xml")
                self.assertEqual(metadata.findtext("ForcedInstallation"), "true")
                for tool in ("pocketbase", "ffmpeg"):
                    component = packages / f"{core}.{tool}"
                    metadata = ET.parse(component / "meta/package.xml")
                    self.assertEqual(metadata.findtext("Default"), "false")
                    self.assertEqual(metadata.findtext("Dependencies"), core)
                    self.assertEqual(metadata.findtext("Version"), "3.9.123")
                    binary = component / "data/third_party" / (tool + suffix)
                    self.assertEqual(binary.read_bytes(), tool.encode())
                    if platform != "windows":
                        self.assertEqual(binary.stat().st_mode & 0o777, 0o755)

    def test_macos_optional_tools_are_found_beside_app(self):
        from src.database.service import PocketBaseService
        from src.shared.ffmpeg import find_ffmpeg

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            executable = target / "Porn Fetch.app/Contents/MacOS/Porn Fetch"
            tools = target / "third_party"
            tools.mkdir()
            for tool in ("pocketbase", "ffmpeg"):
                (tools / tool).write_bytes(b"tool")
                (tools / tool).chmod(0o755)
            with patch("src.shared.ffmpeg._find_original_executable", return_value=executable):
                self.assertEqual(find_ffmpeg(), (tools / "ffmpeg").resolve())
            with patch("src.database.service._find_original_executable", return_value=executable):
                self.assertEqual(PocketBaseService(target / "data").find_binary(), (tools / "pocketbase").resolve())


if __name__ == "__main__":
    unittest.main()
