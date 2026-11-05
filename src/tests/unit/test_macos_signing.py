"""Offline signing order, credential handling and notarization failure contracts."""

import base64
import contextlib
import io
import json
import os
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from src.tests.unit.test_cli_self_update import load_script

signing = load_script("sign_macos")
repository = load_script("generate_repository")
TEAM = "ABCDE12345"
IDENTITY = "A" * 40


def native(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes.fromhex("cffaedfe") + b"synthetic Mach-O fixture")
    return path


class MacOSSigningTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        environment = {
            "RUNNER_TEMP": str(self.root),
            "PORN_FETCH_MACOS_SIGN_IDENTITY": IDENTITY,
            "PORN_FETCH_MACOS_KEYCHAIN": str(self.root / "signing.keychain-db"),
            "PORN_FETCH_MACOS_TEAM_ID": TEAM,
        }
        self.environ = patch.dict(os.environ, environment)
        self.environ.start()
        self.addCleanup(self.environ.stop)

    def test_verification_uses_inline_requirement_for_developer_id_and_team(self):
        for name in ("helper", "Example.app"):
            with self.subTest(name=name):
                path = self.root / name
                result = subprocess.CompletedProcess([], 0, stdout="", stderr="")
                with patch.object(signing.subprocess, "run", return_value=result) as execute:
                    signing.verify(path)
                command = execute.call_args.args[0]
                self.assertEqual(command[:6], [
                    "/usr/bin/codesign", "--verify", "--all-architectures", "--strict", "--verbose=2", "-R",
                ])
                self.assertEqual(command[6],
                                 '=anchor apple generic and certificate leaf[field.1.2.840.113635.100.6.1.13] exists '
                                 f'and certificate leaf[subject.OU] = "{TEAM}"')
                self.assertEqual(command[-1], str(path))
                self.assertEqual("--deep" in command, path.suffix == ".app")

    def test_signs_nested_code_inside_out_without_entitling_libraries(self):
        app = self.root / "Example.app"
        main = native(app / "Contents/MacOS/Example")
        library = native(app / "Contents/MacOS/package/native.so")
        framework = app / "Contents/Frameworks/QtCore.framework"
        framework_binary = native(framework / "Versions/A/QtCore")
        (framework / "Versions/Current").symlink_to("A", target_is_directory=True)
        (framework / "QtCore").symlink_to("Versions/Current/QtCore")
        with (app / "Contents/Info.plist").open("wb") as output:
            plistlib.dump({"CFBundleExecutable": "Example"}, output)
        commands = []
        with patch.object(signing, "run", side_effect=lambda command, **kwargs: commands.append(command)):
            signing.sign(app, "python")
        signed = [command for command in commands if "--sign" in command]
        paths = [Path(command[-1]) for command in signed]
        self.assertEqual(paths[-1], app)
        self.assertLess(paths.index(framework_binary), paths.index(framework))
        self.assertLess(paths.index(framework), paths.index(app))
        self.assertIn(library, paths)
        self.assertNotIn(main, paths)
        self.assertNotIn(framework / "QtCore", paths)
        for command in signed:
            self.assertNotIn("--deep", command)
            self.assertIn("--timestamp", command)
            if Path(command[-1]) in {app, main}:
                self.assertIn("--entitlements", command)
            else:
                self.assertNotIn("--entitlements", command)

    def test_bundle_data_moves_to_resources_and_remains_readable_at_runtime_paths(self):
        app = self.root / "Example.app"
        macos = app / "Contents/MacOS"
        main = native(macos / "Example")
        library = native(macos / "package/native.so")
        data = ("LICENSES/Monero-CC-BY-SA-4.0.txt", "src/frontend/resources.rcc", "package/data.json")
        for name in data:
            path = macos / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(name)
        with (app / "Contents/Info.plist").open("wb") as output:
            plistlib.dump({"CFBundleExecutable": "Example"}, output)
        with patch.object(signing, "run"):
            signing.sign(app, "python")
            signing.sign(app, "python")  # Re-signing staged IFW bundles must be safe.
        for name in data:
            path = macos / name
            self.assertTrue(path.is_symlink())
            self.assertEqual(path.read_text(), name)
            self.assertEqual(path.resolve(), (app / "Contents/Resources/runtime" / name).resolve())
            self.assertFalse(path.readlink().is_absolute())
        self.assertFalse(main.is_symlink())
        self.assertFalse(library.is_symlink())

    def test_notarization_failure_never_staples_or_passes_gatekeeper(self):
        commands = []

        def invoke(command, **kwargs):
            commands.append(command)
            result = {"id": "test-submission", "status": "Invalid"} if command[2] in {"submit", "wait"} else {}
            return SimpleNamespace(returncode=0, stdout=json.dumps(result), stderr="")

        with patch.object(signing, "run", side_effect=invoke):
            with self.assertRaisesRegex(RuntimeError, "not accepted"):
                signing.notarize(self.root / "Example.app")
        self.assertFalse(any("stapler" in command or "spctl" in command for command in commands))
        self.assertTrue((self.root / "porn-fetch-build-logs/notarization/test-submission.json").is_file())

    def test_accepted_app_is_stapled_validated_and_assessed(self):
        commands = []

        def invoke(command, **kwargs):
            commands.append(command)
            return SimpleNamespace(
                returncode=0, stdout=json.dumps({"id": "accepted-submission", "status": "Accepted"}), stderr=""
            )

        with patch.object(signing, "run", side_effect=invoke):
            signing.notarize(self.root / "Example.app")
        submit = next(command for command in commands if "submit" in command)
        self.assertIn("--keychain-profile", submit)
        self.assertNotIn("--password", submit)
        self.assertTrue(any("staple" in command for command in commands))
        self.assertTrue(any("validate" in command for command in commands))
        self.assertTrue(any(command[0] == "spctl" for command in commands))

    def test_wait_timeout_checks_existing_submission_without_uploading_again(self):
        commands = []

        def invoke(command, **kwargs):
            commands.append(command)
            if "wait" in command:
                return SimpleNamespace(returncode=9, stdout="", stderr="Timeout reached")
            status = "Accepted" if "info" in command else "In Progress"
            return SimpleNamespace(returncode=0, stdout=json.dumps({"id": "delayed", "status": status}), stderr="")

        with patch.object(signing, "run", side_effect=invoke):
            signing.submit(self.root / "payload.zip")
        self.assertEqual(sum("submit" in command for command in commands), 1)
        upload = next(command for command in commands if "submit" in command)
        self.assertIn("--no-wait", upload)
        wait = next(command for command in commands if "wait" in command)
        self.assertEqual(wait[wait.index("--timeout") + 1], "60m")
        reports = self.root / "porn-fetch-build-logs/notarization"
        self.assertEqual(json.loads((reports / "delayed.json").read_text())["status"], "Accepted")
        self.assertEqual(next(reports.glob("submission-*/wait.stderr.txt")).read_text(), "Timeout reached")

    def test_pending_notarization_reports_id_and_never_staples(self):
        commands = []

        def invoke(command, **kwargs):
            commands.append(command)
            if "wait" in command:
                return SimpleNamespace(returncode=9, stdout="", stderr="Timeout reached")
            return SimpleNamespace(returncode=0, stdout=json.dumps({"id": "pending", "status": "In Progress"}),
                                   stderr="")

        with patch.object(signing, "run", side_effect=invoke):
            with self.assertRaisesRegex(RuntimeError, "still In Progress.*submission pending"):
                signing.notarize(self.root / "Example.app")
        self.assertFalse(any("stapler" in command or "spctl" in command or "log" in command for command in commands))
        report = self.root / "porn-fetch-build-logs/notarization/pending.json"
        self.assertEqual(json.loads(report.read_text())["status"], "In Progress")

    def test_import_uses_temporary_keychain_and_cleanup_restores_search_list(self):
        github_env = self.root / "github-env"
        password = "synthetic-password$(not-a-command)"
        environment = {
            "MACOS_CERT_P12_BASE64": base64.b64encode(b"synthetic certificate").decode(),
            "MACOS_CERT_PASSWORD": password,
            "APPLE_ID": "example@example.invalid",
            "APPLE_APP_PASSWORD": "synthetic-app-password",
            "APPLE_TEAM_ID": TEAM,
            "GITHUB_ENV": str(github_env),
        }
        commands = []

        def invoke(command, **kwargs):
            commands.append(list(map(str, command)))
            if "find-identity" in command:
                stdout = f'1) {IDENTITY} "Developer ID Application: Example ({TEAM})"'
            elif "list-keychains" in command and "-s" not in command:
                stdout = '"/Users/runner/Library/Keychains/login.keychain-db"'
            else:
                stdout = ""
            if "import" in command:
                path = Path(command[2])
                self.assertEqual(path.read_bytes(), b"synthetic certificate")
                self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

        output = io.StringIO()
        with (
            patch.dict(os.environ, environment),
            patch.object(signing, "run", side_effect=invoke),
            contextlib.redirect_stdout(output),
        ):
            signing.setup()
            self.assertFalse((signing.signing_directory() / "certificate.p12").exists())
            self.assertIn("PORN_FETCH_MACOS_SIGN_IDENTITY=" + IDENTITY, github_env.read_text())
            self.assertNotIn(password, github_env.read_text() + output.getvalue())
            signing.cleanup()
        self.assertIn(
            ["security", "list-keychains", "-d", "user", "-s", "/Users/runner/Library/Keychains/login.keychain-db"],
            commands,
        )
        self.assertFalse(signing.signing_directory().exists())

    def test_sensitive_subprocess_failure_does_not_expose_its_arguments_or_output(self):
        failure = subprocess.CompletedProcess([], 1, stdout="secret", stderr="secret")
        with patch.object(signing.subprocess, "run", return_value=failure) as execute:
            with self.assertRaises(RuntimeError) as error:
                signing.run(["security", "import", "secret"], sensitive=True)
        self.assertNotIn("secret", str(error.exception))
        self.assertNotIn("shell", execute.call_args.kwargs)

    def test_public_subprocess_failure_includes_stapler_stdout_diagnostics(self):
        failure = subprocess.CompletedProcess([], 68, stdout="CloudKit connection was lost", stderr="")
        with patch.object(signing.subprocess, "run", return_value=failure):
            with self.assertRaisesRegex(RuntimeError, "CloudKit connection was lost"):
                signing.run(["xcrun", "stapler", "staple", self.root / "Example.app"])

    def test_macos_repository_preserves_framework_links_and_uses_signed_maintenance(self):
        dist = self.root / "dist"
        app = dist / "Porn Fetch.app/Contents/MacOS"
        native(app / "Porn Fetch")
        native(app / "third_party/pocketbase")
        native(app / "third_party/ffmpeg")
        (app / "third_party/ffmpeg.sha256").write_text("fixture checksum")
        signing.relocate_resources(dist / "Porn Fetch.app")
        (app / "alias").symlink_to("Porn Fetch")
        pb, ff = native(self.root / "pocketbase"), native(self.root / "ffmpeg")
        config, packages = repository.prepare_staging_directory(
            self.root / "staging", dist, pb, "darwin", "arm64", "3.9.123", ff, macos_signed=True
        )
        core = packages / "to.pornfetch.echteralsfake"
        self.assertTrue((core / "data/Porn Fetch.app/Contents/MacOS/alias").is_symlink())
        self.assertFalse((core / "data/Porn Fetch.app/Contents/MacOS/third_party/ffmpeg").exists())
        self.assertEqual(list((core / "data").rglob("ffmpeg.sha256")), [])
        self.assertEqual(ET.parse(config).findtext("MaintenanceToolName"), "maintenancetool")
        self.assertEqual(
            ET.parse(core / "meta/package.xml").findtext("Dependencies"), "to.pornfetch.echteralsfake.maintenance"
        )
        script = packages / "to.pornfetch.echteralsfake.maintenance/meta/installscript.qs"
        self.assertIn("tmpMaintenanceToolApp/maintenancetool.app", script.read_text())
        self.assertIn('component.addOperation("Extract"', script.read_text())


@unittest.skipUnless(sys.platform == "darwin" and os.environ.get("PORN_FETCH_MACOS_SIGNING") == "1",
                     "requires the macOS CI signing identity")
class NativeMacOSSigningTests(unittest.TestCase):
    def test_signs_app_with_runtime_data_before_compilation(self):
        with tempfile.TemporaryDirectory() as temporary:
            app = Path(temporary) / "SigningProbe.app"
            macos = app / "Contents/MacOS"
            macos.mkdir(parents=True)
            # System file flags cannot be copied by an unprivileged CI user.
            shutil.copy("/usr/bin/true", macos / "SigningProbe")
            (macos / "LICENSES").mkdir()
            (macos / "LICENSES/notice.txt").write_text("Signing probe license")
            (macos / "package").mkdir()
            shutil.copy("/usr/bin/true", macos / "package/helper")
            (macos / "package/data.json").write_text("{}")
            with (app / "Contents/Info.plist").open("wb") as output:
                plistlib.dump({"CFBundleExecutable": "SigningProbe", "CFBundleIdentifier": "to.pornfetch.signingprobe",
                               "CFBundlePackageType": "APPL", "CFBundleVersion": "1.0"}, output)
            signing.sign(app, "python")
            self.assertEqual((macos / "LICENSES/notice.txt").read_text(), "Signing probe license")


if __name__ == "__main__":
    unittest.main()
