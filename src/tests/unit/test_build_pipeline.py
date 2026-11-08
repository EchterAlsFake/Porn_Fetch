"""Focused offline regression checks for build artifact handling."""
import configparser
import fnmatch
import hashlib
import io
import json
import os
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

from packaging.requirements import Requirement

from src.tests.unit.test_cli_self_update import load_script

merger = load_script("merge_macos_bundles")
repairer = load_script("repair_macos_bundle")
preparer = load_script("prepare_macos_deploy")
desktop_preparer = load_script("prepare_deploy")
ffmpeg_builder = load_script("build_ffmpeg")
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class WindowsBuildDependencyTests(unittest.TestCase):
    def test_ifw_workflow_passes_optional_arguments_without_empty_array_expansion(self):
        workflow = (PROJECT_ROOT / ".github/workflows/build_all.yml").read_text()
        step = workflow.split("      - name: Build IFW installer and repository\n", 1)[1].split(
            "      - name:", 1)[0]
        script = textwrap.dedent(step.split("        run: |\n", 1)[1])
        for target in ("macos", "windows"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                (root / "Porn Fetch.app").mkdir()
                (root / "Porn Fetch.dist").mkdir()
                (root / "Porn Fetch.dist/main.exe").touch()
                (root / f"PornFetch_{target}_GUI_x64_LEGAL.zip").touch()
                uv = root / "uv"
                uv.write_text(f"#!{sys.executable}\n" + textwrap.dedent('''\
                    import json, os, sys
                    from pathlib import Path
                    if sys.argv[4] == "-c":
                        print("3.9.123")
                    else:
                        Path(os.environ["CAPTURE"]).write_text(json.dumps(sys.argv[5:]))
                    '''))
                uv.chmod(0o755)
                command = script.replace("${{ matrix.platform }}", target).replace(
                    "${{ matrix.arch }}", "x64").replace("${{ inputs.benchmark_compression }}", "false")
                capture = root / "arguments.json"
                subprocess.run(["bash", "-eu", "-o", "pipefail", "-c", command], cwd=root, check=True,
                               env={**os.environ, "PATH": f"{root}{os.pathsep}{os.environ['PATH']}",
                                    "CAPTURE": str(capture), "RUNNER_TEMP": str(root / "runner temp"),
                                    "GITHUB_ENV": str(root / "github-env")})
                arguments = json.loads(capture.read_text())
                self.assertEqual(arguments[arguments.index("--platform") + 1],
                                 "darwin" if target == "macos" else "windows")
                self.assertNotIn("--benchmark-compression", arguments)
                if target == "windows":
                    self.assertEqual(arguments[arguments.index("--maintenance-tool") + 1],
                                     str(root / "runner temp/pornfetch-maintenance/installerbase.exe"))
                else:
                    self.assertNotIn("--maintenance-tool", arguments)

    def test_workflow_assembles_normal_and_long_command_windows_distributions(self):
        workflow = (PROJECT_ROOT / ".github/workflows/build_all.yml").read_text()
        assembly = workflow.split('# Standalone Layout & Assembly', 1)[1].split(
            'if [ "${{ matrix.platform }}" = "windows" ]; then', 1)[1].split(
            '            mkdir -p "Porn Fetch.dist/third_party"', 1)[0]
        for long_command in (False, True):
            with self.subTest(long_command=long_command), tempfile.TemporaryDirectory() as temporary:
                project = Path(temporary)
                bundle = project / ("deployment/deploy_main.dist" if long_command else "Porn Fetch.dist")
                bundle.mkdir(parents=True)
                (bundle / ("deploy_main.exe" if long_command else "main.exe")).write_bytes(b"application")
                (bundle / "Qt6Core.dll").write_bytes(b"dependency")
                subprocess.run(["bash", "-eu", "-c", assembly], cwd=project, check=True)
                self.assertEqual((project / "Porn Fetch.dist/Porn Fetch.exe").read_bytes(), b"application")
                self.assertEqual((project / "Porn Fetch.dist/Qt6Core.dll").read_bytes(), b"dependency")

    def test_pydivert_is_installed_only_for_supported_windows_architecture(self):
        project = tomllib.loads((PROJECT_ROOT / "pyproject.toml").read_text())
        dependency = next(Requirement(value) for value in project["project"]["optional-dependencies"]["gui"]
                          if value.startswith("pydivert"))
        for system, machine, expected in (("win32", "ARM64", False), ("win32", "AMD64", True),
                                          ("win32", "x86_64", True), ("linux", "aarch64", True)):
            with self.subTest(system=system, machine=machine):
                self.assertEqual(dependency.marker.evaluate({"sys_platform": system, "platform_machine": machine}),
                                 expected)

    def test_windows_ffmpeg_uses_explicit_msys2_tools_instead_of_wsl(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "MSYS2 installation"
            tools = root / "usr/bin"
            tools.mkdir(parents=True)
            for name in ("bash.exe", "make.exe"):
                (tools / name).touch()
            with patch.dict(os.environ, {"PATH": "WSL launchers"}):
                for arch, compiler in (("x64", "clang64"), ("arm64", "clangarm64")):
                    with self.subTest(arch=arch):
                        bash, make, environment = ffmpeg_builder.build_tools("windows", arch, root)
                        self.assertEqual(Path(bash), tools / "bash.exe")
                        self.assertEqual(Path(make), tools / "make.exe")
                        self.assertEqual(environment["PATH"].split(os.pathsep)[:2],
                                         [str(root / compiler / "bin"), str(tools)])

    def test_windows_ffmpeg_collects_notices_without_msys2_on_parent_path(self):
        for arch, compiler in (("x64", "clang64"), ("arm64", "clangarm64")):
            with self.subTest(arch=arch), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                msys = root / "MSYS2 installation"
                tools = msys / "usr/bin"
                tools.mkdir(parents=True)
                for name in ("bash.exe", "make.exe"):
                    (tools / name).touch()
                include = msys / compiler / "include"
                include.mkdir(parents=True)
                (include / "zlib.h").write_text("zlib license fixture")
                archive = root / "source.tar.xz"
                with tarfile.open(archive, "w:xz") as bundle:
                    for name in ("configure", "COPYING.LGPLv2.1", "LICENSE.md"):
                        data = b"source fixture"
                        entry = tarfile.TarInfo(f"ffmpeg-{ffmpeg_builder.VERSION}/{name}")
                        entry.size = len(data)
                        bundle.addfile(entry, io.BytesIO(data))

                def compile_fixture(command, *, label, cwd, env):
                    if label == "Configure FFmpeg":
                        (cwd / "config.h").write_text("\n".join(
                            f"#define CONFIG_{option} 0" for option in ("GPL", "VERSION3", "NONFREE")))
                        (cwd / "config_components.h").write_text("#define CONFIG_AAC_ENCODER 0\n")
                    else:
                        (cwd / "ffmpeg.exe").write_bytes(b"compiled executable")

                def windows_output(command, **kwargs):
                    # CreateProcess resolves bare names using the parent's PATH,
                    # regardless of the PATH passed in the child's environment.
                    if not Path(command[0]).is_absolute():
                        raise FileNotFoundError(2, "Windows cannot locate this executable", command[0])
                    self.assertTrue(Path(command[0]).is_file())
                    return "GNU Lesser General Public License version 2.1" if "-L" in command else "FFmpeg version fixture"

                with patch.object(ffmpeg_builder.sys, "platform", "win32"), \
                        patch.object(ffmpeg_builder.platform, "machine", return_value=arch), \
                        patch.object(ffmpeg_builder, "SOURCE_SHA256", hashlib.sha256(archive.read_bytes()).hexdigest()), \
                        patch.object(ffmpeg_builder.build_output, "run", side_effect=compile_fixture), \
                        patch.object(ffmpeg_builder.subprocess, "check_output", side_effect=windows_output), \
                        patch.dict(os.environ, {"PATH": "plain PowerShell PATH without MSYS2"}):
                    result = ffmpeg_builder.build("windows", arch, root / "output", root / "work", archive,
                                                  msys2_root=msys)
                self.assertEqual(result.read_bytes(), b"compiled executable")
                legal = result.parent / "ffmpeg-legal"
                self.assertEqual((legal / "zlib.h").read_text(), "zlib license fixture")
                self.assertIn("FFmpeg version fixture", (legal / "version.txt").read_text())
                manifest = json.loads((legal / "build.json").read_text())
                self.assertEqual(manifest["arch"], arch)


class FFmpegCacheTests(unittest.TestCase):
    def payload(self, root):
        legal = root / "ffmpeg-legal"
        legal.mkdir()
        source = b"pinned source archive fixture"
        executable = root / "ffmpeg.exe"
        executable.write_bytes(b"unsigned native executable")
        (legal / f"ffmpeg-{ffmpeg_builder.VERSION}.tar.xz").write_bytes(source)
        for name in ("COPYING.LGPLv2.1", "LICENSE.md", "configuration.txt", "version.txt", "zlib.h"):
            (legal / name).write_text("legal fixture")
        (legal / "config.h").write_text("\n".join(
            f"#define CONFIG_{option} 0" for option in ("GPL", "VERSION3", "NONFREE")))
        (legal / "config_components.h").write_text("#define CONFIG_AAC_ENCODER 0\n")
        digest = hashlib.sha256(source).hexdigest()
        (legal / "build.json").write_text(json.dumps({
            "version": ffmpeg_builder.VERSION, "platform": "windows", "arch": "arm64",
            "source_sha256": digest, "binary_sha256": hashlib.sha256(executable.read_bytes()).hexdigest(),
        }))
        return executable, digest

    def test_restored_payload_verifies_source_configuration_and_native_license(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable, digest = self.payload(root)
            with patch.object(ffmpeg_builder, "SOURCE_SHA256", digest), \
                    patch.object(ffmpeg_builder.subprocess, "check_output",
                                 return_value="GNU Lesser General Public License version 2.1") as command:
                self.assertEqual(ffmpeg_builder.verify_existing(root, "windows", "ARM64"), executable)
            command.assert_called_once_with([str(executable), "-hide_banner", "-L"],
                                            stderr=subprocess.STDOUT, text=True)

    def test_changed_cached_executable_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable, digest = self.payload(root)
            executable.write_bytes(b"unexpected executable")
            with patch.object(ffmpeg_builder, "SOURCE_SHA256", digest), \
                    patch.object(ffmpeg_builder.subprocess, "check_output") as command:
                with self.assertRaisesRegex(ValueError, "recorded SHA-256"):
                    ffmpeg_builder.verify_existing(root, "windows", "arm64")
            command.assert_not_called()


class FFmpegSourceDownloadTests(unittest.IsolatedAsyncioTestCase):
    async def test_dns_failure_uses_alternate_host_with_the_same_pinned_hash(self):
        from base_api.modules.errors import NetworkRequestError

        data = b"source archive fixture"
        request = AsyncMock(side_effect=[NetworkRequestError("DNS failure"),
                                        SimpleNamespace(content=data, raise_for_status=Mock())])
        with tempfile.TemporaryDirectory() as temporary, patch("base_api.BaseCore") as client, \
                patch.object(ffmpeg_builder, "SOURCE_SHA256", hashlib.sha256(data).hexdigest()):
            client.return_value.__aenter__.return_value = SimpleNamespace(request=request)
            destination = Path(temporary) / "source.tar.xz"
            await ffmpeg_builder.download_source(destination)
            self.assertEqual(destination.read_bytes(), data)
            self.assertEqual([call.kwargs["url"] for call in request.await_args_list],
                             list(ffmpeg_builder.SOURCE_URLS))

    async def test_corrupt_download_is_not_saved_or_accepted(self):
        request = AsyncMock(return_value=SimpleNamespace(content=b"corrupt", raise_for_status=Mock()))
        with tempfile.TemporaryDirectory() as temporary, patch("base_api.BaseCore") as client:
            client.return_value.__aenter__.return_value = SimpleNamespace(request=request)
            destination = Path(temporary) / "source.tar.xz"
            with self.assertRaisesRegex(ValueError, "pinned SHA-256"):
                await ffmpeg_builder.download_source(destination)
            self.assertFalse(destination.exists())


class QmlPackagingTests(unittest.TestCase):
    def test_cache_compiler_uses_active_environment_before_unrelated_path_tool(self):
        from scripts.compile_qml import find_qmlcachegen

        with tempfile.TemporaryDirectory() as directory:
            prefix = Path(directory)
            expected = prefix / "bin/pyside6-qmlcachegen"
            expected.parent.mkdir()
            expected.touch()
            with patch("scripts.compile_qml.sys.prefix", str(prefix)), \
                    patch("scripts.compile_qml.shutil.which", return_value="/usr/bin/qmlcachegen"):
                self.assertEqual(find_qmlcachegen(), expected)

    def test_windows_wheel_layout_is_used_for_scan_and_exclusions(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            ui = project / "src/frontend/UI"
            ui.mkdir(parents=True)
            (ui / "Main.qml").write_text("import QtQuick.Controls\nApplicationWindow {}\n")
            pyside = Path(temporary) / "PySide6"
            qml = pyside / "qml"
            required = ("QtQml", "QtQuick", "QtQuick/Controls", "QtQuick/Controls/Basic")
            for module in (*required, "QtWebEngine"):
                directory = qml / module
                directory.mkdir(parents=True, exist_ok=True)
                (directory / "qmldir").write_text("module " + module.replace("/", "."))
            scanner = pyside / "qmlimportscanner.exe"
            scanner.write_bytes(b"scanner")
            scanner.chmod(0o755)

            def scan(arguments, **kwargs):
                self.assertEqual(arguments[0], str(scanner))
                self.assertEqual(arguments[arguments.index("-importPath") + 1], str(qml))
                self.assertIn("import QtQuick.Controls.Basic", Path(arguments[-1]).read_text())
                return json.dumps([{"type": "module", "path": str(qml / module)} for module in required])

            output = project / "windows.spec"
            with patch.object(desktop_preparer.subprocess, "check_output", side_effect=scan), \
                    patch.object(desktop_preparer.sys, "platform", "win32"), \
                    patch.object(desktop_preparer.platform, "machine", return_value="ARM64"), \
                    patch.object(desktop_preparer, "patch_installed_nuitka") as patch_nuitka:
                desktop_preparer.prepare_spec(PROJECT_ROOT / "packaging/pysidedeploy_windows.spec",
                                             output, project, pyside)
            patch_nuitka.assert_called_once_with()
            config = configparser.ConfigParser()
            config.read(output)
            arguments = shlex.split(config.get("nuitka", "extra_args"))
            self.assertIn("--lto=no", arguments)
            self.assertNotIn("--lto=yes", arguments)
            self.assertIn("--noinclude-dlls=*/qml/QtWebEngine/*", arguments)
            self.assertIn("--noinclude-data-files=PySide6/qml/QtWebEngine/**", arguments)
            self.assertNotIn("--noinclude-dlls=*/qml/QtQuick/*", arguments)

    def test_exclusions_preserve_imported_children_without_keeping_unused_siblings(self):
        with tempfile.TemporaryDirectory() as temporary:
            qml = Path(temporary)
            for module in ("QtQuick", "QtQuick/Layouts", "QtQuick/Scene3D", "QtQuick/Controls",
                           "QtQuick/Controls/Basic", "QtQuick/Controls/StyleKit", "QtSensors"):
                directory = qml / module
                directory.mkdir(parents=True, exist_ok=True)
                (directory / "qmldir").write_text("module " + module.replace("/", "."))
            required = {Path("QtQuick"), Path("QtQuick/Layouts"), Path("QtQuick/Controls/Basic")}
            self.assertEqual(set(preparer.excluded_qml_modules(qml, required)),
                             {Path("QtQuick/Scene3D"), Path("QtQuick/Controls/StyleKit"), Path("QtSensors")})

    def test_real_qml_scan_excludes_unrelated_plugins_and_keeps_ui_imports(self):
        import PySide6

        pyside = Path(PySide6.__file__).resolve().parent
        with tempfile.TemporaryDirectory() as temporary:
            spec = Path(temporary) / "macos.spec"
            preparer.prepare_spec(PROJECT_ROOT / "packaging/pysidedeploy_macos.spec", spec, PROJECT_ROOT, pyside)
            config = configparser.ConfigParser()
            config.read(spec)
            arguments = shlex.split(config.get("nuitka", "extra_args"))
            dll_exclusions = [arg.split("=", 1)[1] for arg in arguments if arg.startswith("--noinclude-dlls=")]
            data_exclusions = [arg.split("=", 1)[1] for arg in arguments
                               if arg.startswith("--noinclude-data-files=")]
            for module in ("QtMultimedia", "QtSensors", "QtWebEngine", "QtQuick3D", "Qt/labs/StyleKit",
                           "Qt5Compat/GraphicalEffects"):
                with self.subTest(excluded=module):
                    self.assertTrue(any(fnmatch.fnmatch(f"{pyside}/Qt/qml/{module}/libplugin.dylib", pattern)
                                        for pattern in dll_exclusions))
                    self.assertTrue(any(fnmatch.fnmatch(f"PySide6/qml/{module}/qmldir", pattern)
                                        for pattern in data_exclusions))
            for module in ("QtQuick/Layouts", "QtQuick/Dialogs", "QtQuick/Controls/Material"):
                with self.subTest(retained=module):
                    self.assertFalse(any(fnmatch.fnmatch(f"{pyside}/Qt/qml/{module}/libplugin.dylib", pattern)
                                         for pattern in dll_exclusions))
                    self.assertFalse(any(fnmatch.fnmatch(f"PySide6/qml/{module}/qmldir", pattern)
                                         for pattern in data_exclusions))
            self.assertTrue(any(fnmatch.fnmatch("PornFetch_old.app/Contents/MacOS/main", pattern)
                                for pattern in data_exclusions))
            self.assertTrue(any(fnmatch.fnmatch(
                "src/frontend/graphics/ios/Assets.xcassets/AppIcon.appiconset/Contents.json", pattern)
                for pattern in data_exclusions))
            self.assertEqual(config.get("app", "input_file"), str(PROJECT_ROOT / "main.py"))
            self.assertTrue(all(path.startswith("src/frontend/UI/")
                                for path in config.get("qt", "qml_files").split(",")))


class MacBundleTests(unittest.TestCase):
    def test_single_arch_bundle_relinks_homebrew_openssl_and_keeps_python_copy_separate(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "Porn Fetch.app"
            macos = bundle / "Contents/MacOS"
            rust = macos / "cryptography/hazmat/bindings/_rust.so"
            crypto = macos / "libcrypto.dylib"
            ssl = macos / "libssl.dylib"
            python_crypto = macos / "libcrypto.3.dylib"
            for binary in (rust, crypto, ssl, python_crypto):
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_bytes(b"\xcf\xfa\xed\xfetest")
            python_crypto.write_bytes(b"\xcf\xfa\xed\xfePython OpenSSL build")
            old_crypto = "/usr/local/opt/openssl@3/lib/libcrypto.3.dylib"
            old_ssl = "/usr/local/opt/openssl@3/lib/libssl.3.dylib"
            ids = {crypto: old_crypto, ssl: old_ssl}
            dependencies = {rust: [old_crypto, old_ssl], crypto: [old_crypto], ssl: [old_ssl, old_crypto]}

            def otool(command, **_):
                binary = Path(command[-1])
                if command[1] == "-D":
                    return f"{binary}:\n" + ids.get(binary, "") + "\n"
                return f"{binary}:\n" + "".join(
                    f"\t{dependency} (compatibility version 3.0.0, current version 3.0.0)\n"
                    for dependency in dependencies.get(binary, [])
                )

            def execute(command, **_):
                if command[0] == "install_name_tool":
                    replacements = dict(zip(command[2:-1:3], command[3:-1:3], strict=True))
                    binary = Path(command[-1])
                    dependencies[binary] = [replacements.get(dep, dep) for dep in dependencies[binary]]

            with patch.object(repairer.subprocess, "check_output", side_effect=otool), \
                 patch.object(repairer.subprocess, "run", side_effect=execute) as run:
                self.assertEqual(repairer.repair_bundle(bundle), 2)
            self.assertEqual(dependencies[rust], ["@loader_path/../../../libcrypto.dylib",
                                                  "@loader_path/../../../libssl.dylib"])
            self.assertEqual(dependencies[ssl], [old_ssl, "@loader_path/libcrypto.dylib"])
            self.assertEqual(python_crypto.read_bytes(), b"\xcf\xfa\xed\xfePython OpenSSL build")
            self.assertEqual(run.call_args_list[-1].args[0],
                             ["codesign", "--force", "--deep", "--sign", "-", str(bundle)])

    def test_bundle_repair_rejects_remaining_build_machine_library_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            bundle = Path(temporary) / "Porn Fetch.app"
            binary = bundle / "Contents/MacOS/package/native.so"
            binary.parent.mkdir(parents=True)
            binary.write_bytes(b"\xcf\xfa\xed\xfetest")
            external = "/usr/local/opt/example/lib/libexample.dylib"

            def otool(command, **_):
                return f"{binary}:\n" + (
                    f"\t{external} (compatibility version 1.0.0, current version 1.0.0)\n"
                    if command[1] == "-L" else ""
                )

            with patch.object(repairer.subprocess, "check_output", side_effect=otool), \
                 patch.object(repairer.subprocess, "run"):
                with self.assertRaisesRegex(ValueError, "External library dependency.*libexample"):
                    repairer.verify_bundle_dependencies(bundle)

    def test_bundle_repair_copies_missing_lz4_and_relinks_its_extensions(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bundle = root / "Porn Fetch.app"
            extension = bundle / "Contents/MacOS/lz4/block/_block.so"
            source = root / "build host/liblz4.1.dylib"
            for binary in (extension, source):
                binary.parent.mkdir(parents=True)
                binary.write_bytes(b"\xcf\xfa\xed\xfetest")
            target = bundle / "Contents/Frameworks/liblz4.1.dylib"
            linked = {extension: str(source), source: str(source), target: str(source)}

            def otool(command, **_):
                binary = Path(command[-1])
                if command[1] == "-D":
                    return f"{binary}:\n" + (str(source) if binary != extension else "") + "\n"
                return f"{binary}:\n\t{linked[binary]} (compatibility version 1.0.0, current version 1.10.0)\n"

            def execute(command, **_):
                if command[0] == "install_name_tool":
                    linked[Path(command[-1])] = command[3]

            with patch.object(repairer.subprocess, "check_output", side_effect=otool), \
                 patch.object(repairer.subprocess, "run", side_effect=execute):
                self.assertEqual(repairer.repair_bundle(bundle), 1)
            self.assertEqual(target.read_bytes(), source.read_bytes())
            self.assertEqual(linked[extension], "@loader_path/../../../Frameworks/liblz4.1.dylib")

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

    def test_merge_preserves_optional_intel_crypto_accelerators(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
            intel.mkdir()
            arm.mkdir()
            accelerators = (
                Path("Contents/MacOS/Cryptodome/Cipher/_raw_aesni.so"),
                Path("Contents/MacOS/Cryptodome/Hash/_ghash_clmul.so"),
            )
            for relative in accelerators:
                source = intel / relative
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_bytes(b"intel accelerator")
            with patch.object(merger, "is_macho", return_value=True), \
                 patch.object(merger.subprocess, "check_output", return_value=""), \
                 patch.object(merger.subprocess, "run") as run:
                merger.merge_bundles(intel, arm, output)
            commands = [call.args[0] for call in run.call_args_list]
            self.assertEqual(commands, [
                ["lipo", str(output / relative), "-verify_arch", "x86_64"]
                for relative in accelerators
            ])
            for relative in accelerators:
                self.assertEqual((output / relative).read_bytes(), b"intel accelerator")

    def test_merge_uses_versioned_arm_library_for_intel_openssl_alias(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
            relative = Path("Contents/MacOS/libcrypto.dylib")
            for bundle in (intel, arm):
                (bundle / relative.parent).mkdir(parents=True)
                (bundle / relative.with_name("libcrypto.3.dylib")).write_bytes(bundle.name.encode())
            (intel / relative).write_bytes(b"Homebrew Intel")
            merged_inputs = {}

            def check_output(command, **_):
                if command[0] == "lipo":
                    return "x86_64" if Path(command[-1]).is_relative_to(intel) else "arm64"
                return f"{command[-1]}:\n/usr/local/opt/openssl@3/lib/libcrypto.3.dylib\n"

            def run(command, **_):
                if "-create" in command:
                    merged_inputs[Path(command[-1])] = [Path(path).read_bytes() for path in command[2:4]]

            with patch.object(merger, "is_macho", return_value=True), \
                 patch.object(merger.subprocess, "check_output", side_effect=check_output), \
                 patch.object(merger.subprocess, "run", side_effect=run), \
                 patch.object(merger, "repair_openssl_references"):
                merger.merge_bundles(intel, arm, output)
            self.assertEqual(merged_inputs[output / relative], [b"Homebrew Intel", b"arm"])
            self.assertEqual(merged_inputs[output / relative.with_name("libcrypto.3.dylib")], [b"intel", b"arm"])

    def test_merge_relinks_homebrew_openssl_to_separate_bundled_libraries(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            macos = output / "Contents/MacOS"
            rust = macos / "cryptography/hazmat/bindings/_rust.so"
            rust.parent.mkdir(parents=True)
            rust.touch()
            for name in ("libcrypto.dylib", "libssl.dylib"):
                (macos / name).touch()
            crypto = "/usr/local/Cellar/openssl@3/3.6.3/lib/libcrypto.3.dylib"
            ssl = "/usr/local/opt/openssl@3/lib/libssl.3.dylib"
            dependencies = "\n".join(
                f"\t{path} (compatibility version 3.0.0, current version 3.0.0)"
                for path in (crypto, ssl, "/usr/lib/libSystem.B.dylib")
            )
            with patch.object(merger.subprocess, "check_output", return_value=dependencies), \
                 patch.object(merger.subprocess, "run") as run:
                self.assertTrue(merger.repair_openssl_references(rust, output))
            self.assertEqual(run.call_args_list[0].args[0], [
                "install_name_tool", "-change", crypto, "@loader_path/../../../libcrypto.dylib",
                "-change", ssl, "@loader_path/../../../libssl.dylib", str(rust),
            ])
            self.assertEqual(run.call_args_list[1].args[0], ["codesign", "--force", "--sign", "-", str(rust)])

    def test_unmatched_native_binary_is_verified(self):
        for relative in (Path("main"), Path("Contents/MacOS/Cryptodome/Cipher/_raw_aes.so")):
            with self.subTest(binary=relative), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                intel, arm, output = (root / name for name in ("intel", "arm", "universal"))
                intel.mkdir()
                arm.mkdir()
                binary = intel / relative
                binary.parent.mkdir(parents=True, exist_ok=True)
                binary.write_bytes(b"intel only")
                with patch.object(merger, "is_macho", return_value=True), \
                     patch.object(merger.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "lipo")) as run:
                    with self.assertRaises(subprocess.CalledProcessError):
                        merger.merge_bundles(intel, arm, output)
                run.assert_called_once_with(
                    ["lipo", str(output / relative), "-verify_arch", "x86_64", "arm64"], check=True,
                )


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
    def test_macos_installer_selects_stable_python_and_refreshes_old_uv_catalog(self):
        script = (PROJECT_ROOT / "scripts/install.sh").read_text().replace('OS="$(detect_os)"', 'OS="darwin"')
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            (base / "scripts").mkdir()
            (base / "scripts/build_desktop.py").touch()
            (base / "pyproject.toml").touch()
            for name in ("xcode-select", "brew"):
                command = base / name
                command.write_text(f"#!{shutil.which('bash')}\nexit 0\n")
                command.chmod(0o755)
            uv = base / "uv"
            uv.write_text(f"#!{sys.executable}\n" + textwrap.dedent('''\
                import json, os, sys
                from pathlib import Path
                root = Path(os.environ["CAPTURE"])
                with (root / "uv-arguments.jsonl").open("a") as output:
                    output.write(json.dumps(sys.argv[1:]) + "\\n")
                if sys.argv[1:3] == ["python", "install"] and not (root / "updated").exists():
                    print("No download found in old uv catalog", file=sys.stderr)
                    sys.exit(2)
                if sys.argv[1:3] == ["self", "update"]:
                    (root / "updated").touch()
                if "scripts/build_desktop.py" in sys.argv:
                    sys.exit(42)
                '''))
            uv.chmod(0o755)
            result = subprocess.run(
                ["bash"], input=script, text=True, cwd=base, capture_output=True, timeout=10,
                env={**os.environ, "PATH": f"{base}:{os.environ['PATH']}", "CAPTURE": str(base)},
            )
            self.assertEqual(result.returncode, 42, result.stdout + result.stderr)
            commands = [json.loads(line) for line in (base / "uv-arguments.jsonl").read_text().splitlines()]
            self.assertEqual(commands.count(["python", "install", "3.15.2"]), 2)
            self.assertIn(["self", "update"], commands)
            sync = next(command for command in commands if command[0] == "sync")
            self.assertEqual(sync[sync.index("--python") + 1], "3.15.2")

    def test_arch_installs_only_build_dependencies_without_system_upgrade(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            commands = {
                "sudo": 'if [[ "$1" == -v ]]; then exit 0; fi\nexec "$@"\n',
                "pacman": 'printf "%s\\n" "$@" > "$CAPTURE"\n'
                          'echo "Package installation output"\necho "Package diagnostics" >&2\nexit 37\n',
            }
            for name, body in commands.items():
                command = base / name
                command.write_text(f"#!{shutil.which('bash')}\n" + body)
                command.chmod(0o755)
            capture = base / "arguments.txt"
            result = subprocess.run(
                ["bash", str(PROJECT_ROOT / "scripts/install.sh")], cwd=base,
                env={**os.environ, "PATH": f"{base}:{os.environ['PATH']}", "CAPTURE": str(capture),
                     "PORN_FETCH_BUILD_VERBOSE": "0"},
                capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 37, result.stdout + result.stderr)
            arguments = capture.read_text().splitlines()
            self.assertEqual(arguments[:3], ["-S", "--noconfirm", "--needed"])
            self.assertIn("base-devel", arguments)
            self.assertIn("Package installation output", result.stdout)
            self.assertIn("Package diagnostics", result.stdout)

    def test_piped_macos_installer_continues_after_homebrew_reads_stdin(self):
        script = (PROJECT_ROOT / "scripts/install.sh").read_text()
        # Exercise the macOS branch on an offline Linux test runner.
        script = script.replace('OS="$(detect_os)"', 'OS="darwin"')
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            commands = {
                "xcode-select": "exit 0\n",
                "brew": '[[ "$1" == install && "${HOMEBREW_NO_AUTO_UPDATE:-}" == 1 '
                        '&& "${HOMEBREW_NO_INSTALL_UPGRADE:-}" == 1 ]] || exit 19\ncat >/dev/null\n',
                "uv": "echo 'mock uv'\n",
                # Stop before fetching or compiling; reaching this command proves
                # the build flow survived the dependency installer's stdin read.
                "git": "echo 'Reached project fetch'\nexit 42\n",
            }
            for name, body in commands.items():
                command = base / name
                command.write_text(f"#!{shutil.which('bash')}\n" + body)
                command.chmod(0o755)
            result = subprocess.run(
                ["bash"], input=script, text=True, cwd=base,
                env={**os.environ, "PATH": f"{base}:{os.environ['PATH']}"},
                capture_output=True, timeout=10,
            )
            self.assertEqual(result.returncode, 42, result.stdout + result.stderr)
            self.assertIn("macOS build deps installed", result.stdout)
            self.assertIn("Reached project fetch", result.stdout)


if __name__ == "__main__":
    unittest.main()
