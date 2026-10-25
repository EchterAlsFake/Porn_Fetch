"""Offline checks for signed CLI update publishing and local replacement."""

from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import call, patch

from rich.console import Console
from rich.progress import Progress
from tuf.api.exceptions import DownloadError, LengthOrHashMismatchError, UnsignedMetadataError
from tuf.ngclient import Updater

from src.cli import self_update
from src.cli.self_update import _apply_update, _stage_bundle, target_name, version_parts


def load_script(name: str):
    path = Path(__file__).resolve().parents[3] / "packaging" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


keys_script = load_script("init_cli_updates")
publisher = load_script("publish_cli_updates")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        pass


class CliUpdateTests(unittest.TestCase):
    def test_frozen_update_check_configures_ca_without_overriding_user_settings(self):
        for configured in ({}, {"SSL_CERT_FILE": "/custom/ca.pem"}, {"SSL_CERT_DIR": "/custom/certs"}):
            with self.subTest(configured=configured), tempfile.TemporaryDirectory() as temporary:
                build = Path(temporary) / "build.json"
                build.write_text(json.dumps({"version": "3.9.1", "target": "linux/amd64.zip"}))
                with patch.dict(os.environ, configured, clear=True), \
                        patch.object(self_update.sys, "frozen", True, create=True), \
                        patch.object(self_update, "BUILD_FILE", build), \
                        patch.object(self_update, "user_cache_dir", return_value=temporary), \
                        patch.object(self_update, "Updater") as updater, redirect_stdout(io.StringIO()) as output:
                    updater.return_value.get_targetinfo.return_value.custom = {"version": "3.9.1"}
                    self.assertEqual(self_update.run_self_update(check_only=False, assume_yes=False), 0)
                    if configured:
                        for key, value in configured.items():
                            self.assertEqual(os.environ[key], value)
                        if "SSL_CERT_FILE" not in configured:
                            self.assertNotIn("SSL_CERT_FILE", os.environ)
                    else:
                        self.assertEqual(os.environ["SSL_CERT_FILE"], self_update.certifi.where())
                        self.assertTrue(Path(os.environ["SSL_CERT_FILE"]).is_file())
                    self.assertIn("up to date (3.9.1)", output.getvalue())

    def test_download_failure_reports_the_underlying_cause(self):
        error = DownloadError("Failed to download metadata")
        error.__cause__ = OSError("certificate verify failed")
        with tempfile.TemporaryDirectory() as temporary, \
                patch.object(self_update, "user_cache_dir", return_value=temporary), \
                patch.object(self_update, "Updater", side_effect=error), redirect_stderr(io.StringIO()) as output:
            self.assertEqual(self_update.run_self_update(check_only=True, assume_yes=False), 1)
        self.assertIn("Cause: certificate verify failed", output.getvalue())

    def test_metadata_download_recovers_from_transport_errors(self):
        metadata = object()
        with tempfile.TemporaryDirectory() as temporary, \
                patch.object(publisher, "fetch_previous_metadata", side_effect=[
                    urllib.error.URLError(TimeoutError("TLS handshake")), DownloadError("connection lost"), metadata,
                ]) as fetch, patch.object(publisher.time, "sleep") as sleep:
            self.assertIs(publisher.previous_metadata("https://example.invalid/", b"root", Path(temporary)), metadata)
            self.assertEqual(fetch.call_count, 3)
            self.assertEqual(sleep.call_args_list, [call(5), call(10)])

    def test_metadata_download_failure_never_bootstraps_a_new_repository(self):
        with tempfile.TemporaryDirectory() as temporary, \
                patch.object(publisher, "fetch_previous_metadata", side_effect=urllib.error.URLError("DNS failure")), \
                patch.object(publisher.time, "sleep"):
            with self.assertRaises(urllib.error.URLError):
                publisher.previous_metadata("https://example.invalid/", b"root", Path(temporary))

    def test_invalid_metadata_is_not_retried(self):
        with tempfile.TemporaryDirectory() as temporary, \
                patch.object(publisher, "fetch_previous_metadata", side_effect=UnsignedMetadataError("bad signature")) as fetch, \
                patch.object(publisher.time, "sleep") as sleep:
            with self.assertRaises(UnsignedMetadataError):
                publisher.previous_metadata("https://example.invalid/", b"root", Path(temporary))
            fetch.assert_called_once()
            sleep.assert_not_called()

    def test_platform_names_and_versions(self):
        self.assertEqual(target_name("Linux", "riscv64"), "linux/riscv64.zip")
        self.assertEqual(target_name("Windows", "AMD64"), "windows/amd64.zip")
        self.assertEqual(target_name("Windows", "x86"), "windows/x86.zip")
        self.assertEqual(target_name("Darwin", "aarch64"), "darwin/arm64.zip")
        self.assertGreater(version_parts("3.9.42"), version_parts("3.9.41"))

    def test_stage_and_replace_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            artifact = base / "PornFetch_linux_CLI_x64"
            artifact.mkdir()
            (artifact / artifact.name).write_text("new cli", encoding="utf-8")
            (artifact / "pocketbase").write_text("new pocketbase", encoding="utf-8")
            archive = base / "bundle.zip"
            publisher.create_bundle(artifact, "linux/amd64.zip", "3.9.2", archive)
            executable = base / "installed-cli"
            executable.write_text("old cli", encoding="utf-8")
            stage = base / ".pornfetch-update-test"
            stage.mkdir()
            _stage_bundle(archive, stage, "linux/amd64.zip", "3.9.2", executable)
            self.assertEqual(_apply_update(stage, executable), 0)
            self.assertEqual(executable.read_text(encoding="utf-8"), "new cli")
            self.assertEqual((base / "pocketbase").read_text(encoding="utf-8"), "new pocketbase")
            self.assertEqual((stage / "previous" / "installed-cli").read_text(encoding="utf-8"), "old cli")

    def test_signed_repository_round_trip(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            private_dir = base / "private"
            root_file = base / "root.json"
            keys_script.initialize(private_dir, root_file)
            artifact_dir = base / "artifacts"
            artifact = artifact_dir / "PornFetch_linux_CLI_x64"
            artifact.mkdir(parents=True)
            (artifact / artifact.name).write_bytes(b"version one")
            public = base / "public"
            public.mkdir()
            server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(public)))
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                url = f"http://127.0.0.1:{server.server_port}/"
                with patch.object(publisher, "ROOT_FILE", root_file):
                    first = base / "first"
                    publisher.publish(artifact_dir, url, first, private_dir / "online.pem", "3.9.1")
                    shutil.copytree(first, public, dirs_exist_ok=True)

                    fetcher = self_update._ProgressFetcher(chunk_size=64)
                    updater = Updater(
                        metadata_dir=str(base / "cache"),
                        metadata_base_url=url + "metadata/",
                        target_dir=str(base / "download"),
                        target_base_url=url + "targets/",
                        bootstrap=root_file.read_bytes(),
                        fetcher=fetcher,
                    )
                    target = updater.get_targetinfo("linux/amd64.zip")
                    self.assertIsNotNone(target)
                    self.assertEqual(target.custom["version"], "3.9.1")
                    rendered = io.StringIO()
                    progress = Progress(console=Console(file=rendered, width=160), auto_refresh=False)
                    with patch.object(self_update, "Progress", return_value=progress), \
                            patch.object(progress, "advance", wraps=progress.advance) as advance:
                        archive = self_update._download_update(updater, target, fetcher)
                    self.assertTrue(archive.is_file())
                    self.assertGreater(advance.call_count, 1)
                    self.assertEqual(progress.tasks[0].completed, target.length)
                    self.assertIn("100%", rendered.getvalue())
                    self.assertIsNone(fetcher.on_chunk)

                    # A missing 2.root.json is normal before the first key rotation.
                    # The CLI must still verify the repository and report its current version.
                    self.assertFalse((public / "metadata" / "2.root.json").exists())
                    build = base / "build.json"
                    build.write_text(json.dumps({"version": "3.9.1", "target": "linux/amd64.zip"}))
                    with patch.object(self_update, "BUILD_FILE", build), \
                            patch.object(self_update, "ROOT_FILE", root_file), \
                            patch.object(self_update, "REPOSITORY_URL", url), \
                            patch.object(self_update, "user_cache_dir", return_value=str(base / "cli-cache")), \
                            patch.object(self_update, "_license_status") as license_status, \
                            patch("src.shared.service_transport.ServiceFetcher", lambda settings: self_update._ProgressFetcher()), \
                            redirect_stdout(io.StringIO()) as output:
                        self.assertEqual(self_update.run_self_update(check_only=False, assume_yes=False), 0)
                    self.assertIn("up to date (3.9.1)", output.getvalue())
                    license_status.assert_not_called()

                    # Progress reporting must not bypass TUF's payload verification.
                    remote_bundle = next((public / "targets").rglob("*.zip"))
                    content = remote_bundle.read_bytes()
                    remote_bundle.write_bytes(bytes([content[0] ^ 1]) + content[1:])
                    with redirect_stderr(io.StringIO()), self.assertRaises(LengthOrHashMismatchError):
                        self_update._download_update(updater, target, fetcher)
                    self.assertIsNone(fetcher.on_chunk)

                    (artifact / artifact.name).write_bytes(b"version two")
                    second = base / "second"
                    publisher.publish(artifact_dir, url, second, private_dir / "online.pem", "3.9.2")
                    shutil.copytree(second, public, dirs_exist_ok=True)
                    self.assertEqual(json.loads((public / "metadata" / "timestamp.json").read_text())["signed"]["version"], 2)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
