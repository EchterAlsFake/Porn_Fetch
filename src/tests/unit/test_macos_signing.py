"""Offline signing order, credential handling and notarization failure contracts."""

import base64
import contextlib
import io
import json
import os
import plistlib
import subprocess
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
        self.assertNotIn(framework / "QtCore", paths)
        for command in signed:
            self.assertNotIn("--deep", command)
            self.assertIn("--timestamp", command)
            if Path(command[-1]) in {app, main}:
                self.assertIn("--entitlements", command)
            else:
                self.assertNotIn("--entitlements", command)

    def test_notarization_failure_never_staples_or_passes_gatekeeper(self):
        commands = []

        def invoke(command, **kwargs):
            commands.append(command)
            result = {"id": "test-submission", "status": "Invalid"} if "submit" in command else {}
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

    def test_macos_repository_preserves_framework_links_and_uses_signed_maintenance(self):
        dist = self.root / "dist"
        app = dist / "Porn Fetch.app/Contents/MacOS"
        native(app / "Porn Fetch")
        native(app / "third_party/pocketbase")
        native(app / "third_party/ffmpeg")
        (app / "alias").symlink_to("Porn Fetch")
        pb, ff = native(self.root / "pocketbase"), native(self.root / "ffmpeg")
        config, packages = repository.prepare_staging_directory(
            self.root / "staging", dist, pb, "darwin", "arm64", "3.9.123", ff, macos_signed=True
        )
        core = packages / "to.pornfetch.echteralsfake"
        self.assertTrue((core / "data/Porn Fetch.app/Contents/MacOS/alias").is_symlink())
        self.assertFalse((core / "data/Porn Fetch.app/Contents/MacOS/third_party/ffmpeg").exists())
        self.assertEqual(ET.parse(config).findtext("MaintenanceToolName"), "maintenancetool")
        self.assertEqual(
            ET.parse(core / "meta/package.xml").findtext("Dependencies"), "to.pornfetch.echteralsfake.maintenance"
        )
        script = packages / "to.pornfetch.echteralsfake.maintenance/meta/installscript.qs"
        self.assertIn("tmpMaintenanceToolApp/maintenancetool.app", script.read_text())
        self.assertIn('component.addOperation("Extract"', script.read_text())


if __name__ == "__main__":
    unittest.main()
