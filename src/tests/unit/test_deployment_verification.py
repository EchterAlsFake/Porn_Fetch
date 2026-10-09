"""Deployment checks use disposable keys and localhost payloads without production requests."""
from __future__ import annotations

import tempfile
import unittest
from contextlib import contextmanager
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch
from urllib.parse import urlsplit

from src.tests.unit.test_cli_self_update import QuietHandler, keys_script, load_script, publisher

verifier = load_script("verify_deployment")
desktop_signer = load_script("sign_desktop_release")


@contextmanager
def serve_repository(repository: Path):
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(repository)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


class RepositoryClient:
    def __init__(self, repository: Path):
        self.repository = repository
        self.requested = []
        self.corrupt_payload = False

    async def fetch_bytes(self, url, **kwargs):
        self.requested.append(url)
        path = self.repository / urlsplit(url).path.lstrip("/")
        if self.corrupt_payload and path.suffix in (".zip", ".7z"):
            return b"corrupted download"
        return path.read_bytes()


class DeploymentVerificationTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "root.json"
        keys_script.initialize(self.base / "keys", self.root)
        self.repository = self.base / "public"
        self.client = RepositoryClient(self.repository)

    def publish_cli(self):
        artifacts = self.base / "artifacts"
        for name, extension in (("PornFetch_linux_CLI_x64", ""), ("PornFetch_windows_CLI_x64", ".exe")):
            artifact = artifacts / name
            artifact.mkdir(parents=True)
            (artifact / (name + extension)).write_bytes(b"compiled CLI")
        with patch.object(publisher, "ROOT_FILE", self.root), patch.object(publisher, "previous_metadata", return_value=None):
            publisher.publish(artifacts, "https://updates.example/", self.repository,
                              self.base / "keys/online.pem", "3.9.123")

    async def test_cli_checks_consistent_metadata_and_each_platform_sample(self):
        self.publish_cli()
        with serve_repository(self.repository) as url, patch.object(
                verifier.Updater, "download_target", autospec=True,
                side_effect=verifier.Updater.download_target) as download:
            await verifier.verify_cli(self.client, self.repository, url, self.root)
        self.assertEqual({call.args[1].path for call in download.call_args_list},
                         {"linux/amd64.zip", "windows/amd64.zip"})

    async def test_cli_rejects_corrupted_public_payload(self):
        self.publish_cli()
        next((self.repository / "targets").rglob("*.zip")).write_bytes(b"corrupted download")
        with serve_repository(self.repository) as url, self.assertRaises(Exception):
            await verifier.verify_cli(self.client, self.repository, url, self.root)

    async def test_cli_rejects_stale_public_metadata(self):
        self.publish_cli()
        self.client.repository = self.base / "stale"
        with patch.object(publisher, "ROOT_FILE", self.root), patch.object(publisher, "previous_metadata", return_value=None):
            publisher.publish(self.base / "artifacts", "https://updates.example/", self.client.repository,
                              self.base / "keys/online.pem", "3.9.122")
        with serve_repository(self.client.repository) as url, self.assertRaisesRegex(
                ValueError, "does not match this deployment"):
            await verifier.verify_cli(self.client, self.repository, url, self.root)

    async def test_metadata_only_refresh_retains_and_verifies_existing_targets(self):
        self.publish_cli()
        refreshed = self.base / "refreshed"
        with serve_repository(self.repository) as url:
            publisher.publish(None, url, refreshed, self.base / "keys/online.pem", None, root_file=self.root)
            self.assertFalse((refreshed / "targets").exists())
            for path in (refreshed / "metadata").iterdir():
                (self.repository / "metadata" / path.name).write_bytes(path.read_bytes())
            await verifier.verify_cli(self.client, refreshed, url, self.root)

    async def test_merged_artifacts_cannot_silently_refresh_an_existing_repository(self):
        self.publish_cli()
        merged = self.base / "merged"
        merged.mkdir()
        (merged / "PornFetch_linux_CLI_x64").write_bytes(b"compiled CLI")
        with serve_repository(self.repository) as url, self.assertRaisesRegex(
                ValueError, "No recognized CLI artifact directories"):
            publisher.publish(merged, url, self.base / "output", self.base / "keys/online.pem", "3.9.124",
                              root_file=self.root)

    async def test_desktop_checks_signed_manifest_xml_and_application_archive(self):
        self.repository.mkdir()
        (self.repository / "Updates.xml").write_text(
            "<Updates><PackageUpdate><Version>3.9.123</Version>"
            "<ReleaseDate>2026-10-06</ReleaseDate></PackageUpdate></Updates>"
        )
        (self.repository / "payload.7z").write_bytes(b"application payload")
        desktop_signer.sign_repository(self.repository, "linux_amd64", "3.9.123",
                                       self.base / "keys/online.pem", self.root)
        await verifier.verify_desktop(self.client, self.repository, "https://updates.example", "linux_amd64", self.root)
        self.assertIn("https://updates.example/Updates.xml", self.client.requested)
        self.client.corrupt_payload = True
        with self.assertRaises(Exception):
            await verifier.verify_desktop(self.client, self.repository, "https://updates.example", "linux_amd64", self.root)


if __name__ == "__main__":
    unittest.main()
