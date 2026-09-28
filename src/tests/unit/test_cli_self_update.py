"""Offline checks for signed CLI update publishing and local replacement."""

from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch

from tuf.ngclient import Updater

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
    def test_platform_names_and_versions(self):
        self.assertEqual(target_name("Linux", "riscv64"), "linux/riscv64.zip")
        self.assertEqual(target_name("Windows", "AMD64"), "windows/amd64.zip")
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

                    updater = Updater(
                        metadata_dir=str(base / "cache"),
                        metadata_base_url=url + "metadata/",
                        target_dir=str(base / "download"),
                        target_base_url=url + "targets/",
                        bootstrap=root_file.read_bytes(),
                    )
                    target = updater.get_targetinfo("linux/amd64.zip")
                    self.assertIsNotNone(target)
                    self.assertEqual(target.custom["version"], "3.9.1")
                    self.assertTrue(Path(updater.download_target(target)).is_file())

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
