"""Focused offline regression checks for build artifact handling."""
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.tests.unit.test_cli_self_update import load_script

merger = load_script("merge_macos_bundles")
repairer = load_script("repair_macos_bundle")
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MacBundleTests(unittest.TestCase):
    def test_repair_relinks_cocoa_and_transitive_framework_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "Porn Fetch.app"
            macos = bundle / "Contents" / "MacOS"
            cocoa = macos / "PySide6" / "qt-plugins" / "platforms" / "libqcocoa.dylib"
            gui = macos / "QtGui" / "QtGui"
            core = macos / "QtCore" / "QtCore"
            for binary in (cocoa, gui, core):
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_bytes(b"\xcf\xfa\xed\xfetest")
            # Universal otool output repeats dependencies for each slice.
            old_gui = "@rpath/QtGui.framework/Versions/A/QtGui"
            old_core = "@rpath/QtCore.framework/Versions/A/QtCore"
            outputs = {
                str(cocoa): f"{cocoa}:\n\t{old_gui} (compatibility version 6.0.0, current version 6.12.0)\n" * 2,
                str(gui): f"{gui}:\n\t{old_core} (compatibility version 6.0.0, current version 6.12.0)\n",
                str(core): f"{core}:\n\t{old_core} (compatibility version 6.0.0, current version 6.12.0)\n",
            }
            with patch.object(repairer.subprocess, "check_output", side_effect=lambda args, **_: outputs[args[-1]]), \
                 patch.object(repairer.subprocess, "run") as run:
                self.assertEqual(repairer.repair_bundle(bundle), 2)
            commands = [call.args[0] for call in run.call_args_list]
            self.assertIn(
                ["install_name_tool", "-change", old_gui, "@loader_path/../../../QtGui/QtGui", str(cocoa)],
                commands,
            )
            self.assertIn(
                ["install_name_tool", "-change", old_core, "@loader_path/../QtCore/QtCore", str(gui)],
                commands,
            )
            self.assertIn(["codesign", "--force", "--sign", "-", str(cocoa)], commands)
            self.assertIn(["codesign", "--force", "--sign", "-", str(gui)], commands)
            self.assertEqual(commands[-1], ["codesign", "--force", "--deep", "--sign", "-", str(bundle)])

    def test_repair_fails_before_modifying_bundle_when_framework_is_missing(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "broken.app"
            macos = bundle / "Contents" / "MacOS"
            macos.mkdir(parents=True)
            (macos / "libqcocoa.dylib").write_bytes(b"\xcf\xfa\xed\xfetest")
            with patch.object(repairer.subprocess, "check_output", return_value=(
                "plugin:\n\t@rpath/QtGui.framework/Versions/A/QtGui "
                "(compatibility version 6.0.0, current version 6.12.0)\n"
            )), patch.object(repairer.subprocess, "run") as run:
                with self.assertRaisesRegex(ValueError, "Missing bundled QtGui binary and source framework"):
                    repairer.repair_bundle(bundle, Path(temporary) / "missing-qt-libs")
                run.assert_not_called()

    def test_repair_copies_missing_stylekit_frameworks_and_their_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "Porn Fetch.app"
            macos = bundle / "Contents" / "MacOS"
            plugin = macos / "PySide6/qml/Qt/labs/StyleKit/impl/libstylekitimplplugin.dylib"
            gui = macos / "QtGui/QtGui"
            for binary in (plugin, gui):
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_bytes(b"\xcf\xfa\xed\xfetest")
            qt_lib_dir = root / "build environment" / "PySide6/Qt/lib"
            source_binaries = {}
            for name in ("QtLabsStyleKitImpl", "QtLabsStyleKit"):
                framework = qt_lib_dir / f"{name}.framework"
                source = framework / "Versions/A" / name
                source.parent.mkdir(parents=True)
                source.write_bytes(b"\xcf\xfa\xed\xfetest")
                resources = source.parent / "Resources"
                resources.mkdir()
                (resources / "Info.plist").write_text("framework metadata")
                (framework / "Versions/Current").symlink_to("A")
                (framework / name).symlink_to(f"Versions/Current/{name}")
                source_binaries[name] = source

            def otool_output(args, **_):
                path = Path(args[-1])
                dependency = {
                    plugin: "QtLabsStyleKitImpl",
                    source_binaries["QtLabsStyleKitImpl"]: "QtLabsStyleKit",
                    source_binaries["QtLabsStyleKit"]: "QtGui",
                }.get(path)
                return f"{path}:\n" + (
                    f"\t@rpath/{dependency}.framework/Versions/A/{dependency} "
                    "(compatibility version 6.0.0, current version 6.12.0)\n" if dependency else ""
                )

            with patch.object(repairer.subprocess, "check_output", side_effect=otool_output), \
                 patch.object(repairer.subprocess, "run") as run:
                self.assertEqual(repairer.repair_bundle(bundle, qt_lib_dir), 3)
            frameworks = bundle / "Contents/Frameworks"
            for name in source_binaries:
                framework = frameworks / f"{name}.framework"
                self.assertEqual((framework / name).read_bytes(), b"\xcf\xfa\xed\xfetest")
                self.assertEqual((framework / "Versions/Current").readlink(), Path("A"))
                self.assertTrue((framework / "Versions/A/Resources/Info.plist").is_file())
            commands = [call.args[0] for call in run.call_args_list]
            changes = [command for command in commands if command[0] == "install_name_tool"]
            targets = [frameworks / "QtLabsStyleKitImpl.framework/Versions/A/QtLabsStyleKitImpl",
                       frameworks / "QtLabsStyleKit.framework/Versions/A/QtLabsStyleKit", gui]
            for command, target in zip(changes, targets, strict=True):
                loader = Path(command[-1])
                self.assertEqual((loader.parent / command[3].removeprefix("@loader_path/")).resolve(),
                                 target.resolve())
            self.assertEqual(commands[-1], ["codesign", "--force", "--deep", "--sign", "-", str(bundle)])

    def test_repair_leaves_already_relinked_bundle_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "working.app"
            macos = bundle / "Contents" / "MacOS"
            macos.mkdir(parents=True)
            (macos / "libqcocoa.dylib").write_bytes(b"\xcf\xfa\xed\xfetest")
            with patch.object(repairer.subprocess, "check_output", return_value=(
                "plugin:\n\t@loader_path/QtGui "
                "(compatibility version 6.0.0, current version 6.12.0)\n"
            )), patch.object(repairer.subprocess, "run") as run:
                self.assertEqual(repairer.repair_bundle(bundle), 0)
                run.assert_not_called()

    def test_merge_extracts_slices_from_fat_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
            for bundle in (intel, arm):
                bundle.mkdir()
                (bundle / "main").write_bytes(b"Mach-O")
            (arm / "arm-resource.txt").write_text("resource")
            with patch.object(merger, "is_macho", side_effect=lambda path: path.name == "main"), \
                 patch.object(merger.subprocess, "check_output", return_value="x86_64 arm64"), \
                 patch.object(merger.subprocess, "run") as run:
                merger.merge_bundles(intel, arm, output)
            commands = [call.args[0] for call in run.call_args_list]
            self.assertEqual(sum("-thin" in command for command in commands), 2)
            create = next(command for command in commands if "-create" in command)
            self.assertNotIn(str(output / "main"), create[2:-2])
            self.assertEqual(commands[-1], ["lipo", str(output / "main"), "-verify_arch", "x86_64", "arm64"])
            self.assertEqual((output / "arm-resource.txt").read_text(), "resource")

    def test_unmatched_native_binary_is_verified(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
            intel.mkdir()
            arm.mkdir()
            (intel / "main").write_bytes(b"intel only")
            with patch.object(merger, "is_macho", return_value=True), \
                 patch.object(merger.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "lipo")):
                with self.assertRaises(subprocess.CalledProcessError):
                    merger.merge_bundles(intel, arm, output)


class DeploymentInputTests(unittest.TestCase):
    def test_cli_upload_contract_includes_only_repository_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            repository = base / "repository"
            (repository / "metadata").mkdir(parents=True)
            for role in ("root", "targets", "snapshot", "timestamp"):
                (repository / "metadata" / f"{role}.json").write_text("{}")
            (repository / "unrelated.pem").write_text("must not be uploaded")
            (base / "curl").write_text(
                '#!/bin/bash\n'
                'printf "%s\\n" "$@" > "$CAPTURE_ARGS"\n'
                'while [[ $# -gt 0 ]]; do\n'
                '  if [[ "$1" == --data-binary ]]; then cp "${2#@}" "$CAPTURE_TAR"; break; fi\n'
                '  shift\n'
                'done\n'
            )
            (base / "curl").chmod(0o755)
            for with_targets in (False, True):
                with self.subTest(with_targets=with_targets):
                    if with_targets:
                        (repository / "targets").mkdir()
                        (repository / "targets" / "bundle.zip").write_bytes(b"test bundle")
                    archive = base / "upload.tar.gz"
                    arguments = base / "curl-args.txt"
                    subprocess.run(
                        ["bash", str(PROJECT_ROOT / "scripts/deploy_cli_updates.sh"), str(repository)],
                        env={"PATH": f"{base}:/usr/bin:/bin", "CI_TOKEN": "disposable-token",
                             "CAPTURE_ARGS": str(arguments), "CAPTURE_TAR": str(archive)},
                        check=True, capture_output=True,
                    )
                    with tarfile.open(archive) as bundle:
                        self.assertEqual({name.split("/")[0] for name in bundle.getnames()},
                                         {"metadata", "targets"} if with_targets else {"metadata"})
                    args = arguments.read_text().splitlines()
                    self.assertIn("X-CI-TOKEN: disposable-token", args)
                    self.assertIn("https://api.pornfetch.to/ci/deploy/cli", args)
                    self.assertIn("POST", args)

    def test_raw_artifacts_cannot_be_uploaded_as_signed_repositories(self):
        with tempfile.TemporaryDirectory() as temporary:
            for script, arguments in (
                ("deploy_cli_updates.sh", [temporary]),
                ("deploy_ifw_repositories.sh", ["linux_amd64", temporary]),
            ):
                with self.subTest(script=script):
                    result = subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / script), *arguments],
                                            env={"CI_TOKEN": "test", "PATH": "/usr/bin:/bin"},
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn("signed", result.stderr)


class InstallerTests(unittest.TestCase):
    def test_piped_macos_installer_continues_after_homebrew_reads_stdin(self):
        script = (PROJECT_ROOT / "scripts/install.sh").read_text()
        # Exercise the macOS branch on an offline Linux test runner.
        script = script.replace('OS="$(detect_os)"', 'OS="darwin"')
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            commands = {
                "xcode-select": "exit 0\n",
                "brew": "cat >/dev/null\n",
                "uv": "echo 'mock uv'\n",
                # Stop before fetching or compiling; reaching this command proves
                # the build flow survived the dependency installer's stdin read.
                "git": "echo 'Reached project fetch'\nexit 42\n",
            }
            for name, body in commands.items():
                command = base / name
                command.write_text("#!/bin/bash\n" + body)
                command.chmod(0o755)
            result = subprocess.run(
                ["bash"], input=script, text=True, cwd=base,
                env={"PATH": f"{base}:/usr/bin:/bin"},
                capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 42, result.stdout + result.stderr)
            self.assertIn("macOS build deps installed", result.stdout)
            self.assertIn("Reached project fetch", result.stdout)


if __name__ == "__main__":
    unittest.main()
