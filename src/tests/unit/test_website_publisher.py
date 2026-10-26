"""Website packaging checks use synthetic artifacts and no publishing credentials."""

import importlib.util
import json
import os
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

PUBLISHER = Path(__file__).resolve().parents[3] / "packaging/publish_website_release.py"


@unittest.skipUnless(PUBLISHER.exists(), "Sibling app checkout is not available")
class WebsitePublisherTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("website_publisher", PUBLISHER)
        cls.publisher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.publisher)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.artifacts = self.root / "artifacts"
        self.artifacts.mkdir()
        self.output = self.root / "website"

    def artifact(self, name, files):
        directory = self.artifacts / name
        directory.mkdir()
        for filename, value in files.items():
            (directory / filename).write_bytes(value)
        return directory

    def test_gui_apk_cli_helpers_notices_and_installer_classification(self):
        self.artifact(
            "PornFetch_linux_GUI_arm64",
            {
                "PornFetch_linux_GUI_arm64.zip": b"gui",
                "PornFetch_linux_GUI_arm64_LEGAL.zip": b"notices",
                "ffmpeg": b"bundled upstream",
            },
        )
        self.artifact(
            "PornFetch_windows_CLI_x64",
            {
                "PornFetch_windows_CLI_x64.exe": b"cli",
                "pocketbase.exe": b"helper",
                "PornFetch_windows_CLI_x64_LEGAL.zip": b"legal",
            },
        )
        self.artifact("PornFetch_android_GUI_armeabi-v7a", {"PornFetch_android_GUI_armeabi-v7a.apk": b"apk"})
        self.artifact("PornFetch_macos_GUI_arm64_Setup.dmg", {"PornFetch_macos_GUI_arm64_Setup.dmg": b"setup"})
        self.artifact("PornFetch_macos_GUI_arm64_Setup.dmg.sha256", {"checksum.sha256": b"sidecar ignored"})
        manifest = self.publisher.prepare(self.artifacts, self.output, "3.9.66", "beta", 1792833600, "a" * 40, "notes")
        kinds = {item["kind"] for item in manifest["artifacts"]}
        self.assertEqual(kinds, {"gui", "cli", "apk", "installer", "notices"})
        apk = next(item for item in manifest["artifacts"] if item["kind"] == "apk")
        self.assertEqual(apk["arch"], "armv7")
        setup = next(item for item in manifest["artifacts"] if item["kind"] == "installer")
        self.assertTrue(setup["experimental"])
        with zipfile.ZipFile(self.output / "PornFetch_windows_CLI_x64.zip") as archive:
            self.assertIn("pocketbase.exe", archive.namelist())
            self.assertIn("PornFetch_windows_CLI_x64.exe", archive.namelist())
        self.assertEqual(json.loads((self.output / "manifest.json").read_text()), manifest)

    def test_all_android_abis_are_published_with_matching_notices(self):
        for abi in ("arm64-v8a", "armeabi-v7a", "x86_64", "x86"):
            name = f"PornFetch_android_GUI_{abi}"
            self.artifact(name, {name + ".apk": b"apk", name + "_LEGAL.zip": b"notices"})
        manifest = self.publisher.prepare(self.artifacts, self.output, "3.9.66", "beta", 1792833600, "a" * 40, "notes")
        for kind in ("apk", "notices"):
            self.assertEqual({a["arch"] for a in manifest["artifacts"] if a["kind"] == kind},
                             {"arm64", "armv7", "x64", "x86"})

    def test_unix_cli_bundle_restores_executable_permissions(self):
        self.artifact("PornFetch_linux_CLI_x64", {"PornFetch_linux_CLI_x64": b"cli", "pocketbase": b"helper"})
        self.publisher.prepare(self.artifacts, self.output, "3.9.66", "beta", 1792833600, "a" * 40, "notes")
        with zipfile.ZipFile(self.output / "PornFetch_linux_CLI_x64.zip") as archive:
            for name in ("PornFetch_linux_CLI_x64", "pocketbase"):
                self.assertTrue((archive.getinfo(name).external_attr >> 16) & 0o111)

    def test_source_archive_uses_tracked_files_and_stamped_version_only(self):
        source = self.root / "source"
        (source / "src/shared").mkdir(parents=True)
        version = source / "src/shared/version.py"
        version.write_text('__version__ = "3.9"\n')
        subprocess.run(["git", "init", "-q", str(source)], check=True)
        subprocess.run(["git", "-C", str(source), "add", "src/shared/version.py"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(source),
                "-c",
                "commit.gpgsign=false",
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.com",
                "commit",
                "-qm",
                "fixture",
            ],
            check=True,
        )
        version.write_text('__version__ = "3.9.66"\n')
        (source / "private-secret.txt").write_text("must not be published")
        self.output.mkdir()
        archive = self.publisher.source_bundle(source, self.output, "3.9.66", 1792833600)
        with tarfile.open(archive) as contents:
            names = contents.getnames()
            self.assertFalse(any("private-secret" in name for name in names))
            self.assertIn(b"3.9.66", contents.extractfile("porn-fetch-3.9.66/src/shared/version.py").read())

    def test_dry_preparation_does_not_make_network_requests(self):
        self.artifact("PornFetch_linux_GUI_x64", {"PornFetch_linux_GUI_x64.zip": b"gui"})
        with patch.object(self.publisher.http.client, "HTTPSConnection", side_effect=AssertionError("no network")):
            self.publisher.prepare(self.artifacts, self.output, "3.9.66", "beta", 1792833600, "a" * 40, "notes")
        self.assertTrue((self.output / "manifest.json").is_file())

    def test_unknown_targets_and_duplicate_packages_fail_before_publishing(self):
        self.artifact("unexpected-target", {"unknown.bin": b"unknown"})
        with self.assertRaisesRegex(ValueError, "No recognized"):
            self.publisher.prepare(self.artifacts, self.output, "3.9.66", "beta", 1792833600, "a" * 40, "notes")

    def test_cli_packages_are_reproducible_when_download_timestamps_change(self):
        folder = self.artifact("PornFetch_linux_CLI_x64", {"PornFetch_linux_CLI_x64": b"cli", "pocketbase": b"helper"})
        first = self.publisher.prepare(self.artifacts, self.output, "3.9.66", "beta", 1792833600, "a" * 40, "notes")
        for path in folder.iterdir():
            os.utime(path, (1792833800, 1792833800))
        second = self.publisher.prepare(
            self.artifacts, self.root / "second", "3.9.66", "beta", 1792833600, "a" * 40, "notes"
        )
        self.assertEqual(first, second)

    def test_upload_reports_early_http_rejection_and_closes_connection(self):
        payload = self.root / "build.apk"
        payload.write_bytes(b"apk")
        connection = Mock()
        connection.send.side_effect = BrokenPipeError()
        connection.getresponse.return_value.status = 413
        with patch.object(self.publisher.http.client, "HTTPSConnection", return_value=connection):
            with self.assertRaisesRegex(RuntimeError, r"PUT /ci/files/build.apk: upload rejected \(HTTP 413\)"):
                self.publisher.send("https://example.com", "PUT", "/ci/files/build.apk", "private-token", payload)
        connection.getresponse.assert_called_once()
        connection.close.assert_called_once()

    def test_upload_identifies_file_when_server_disconnects_without_response(self):
        payload = self.root / "build.apk"
        payload.write_bytes(b"apk")
        connection = Mock()
        connection.send.side_effect = BrokenPipeError()
        connection.getresponse.side_effect = self.publisher.http.client.RemoteDisconnected()
        with patch.object(self.publisher.http.client, "HTTPSConnection", return_value=connection):
            with self.assertRaisesRegex(RuntimeError, "PUT /ci/files/build.apk: connection closed during upload"):
                self.publisher.send("https://example.com", "PUT", "/ci/files/build.apk", "private-token", payload)
        connection.close.assert_called_once()
