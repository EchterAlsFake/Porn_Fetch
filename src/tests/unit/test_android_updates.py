"""Verify Android update selection and prevent unsafe installer handoffs."""
import json
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from tuf.api.metadata import TargetFile

from src.shared import android_updates as service


class AndroidUpdatesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / "pornfetch-platform.json").write_text(json.dumps({"package": "to.pornfetch.app", "abi": "arm64-v8a"}))
        env = patch.dict(os.environ, {"ANDROID_PRIVATE": str(self.root)})
        env.start()
        self.addCleanup(env.stop)
        self.apk = self.root / "verified.apk"
        self.apk.write_bytes(b"synthetic APK")
        self.target = TargetFile.from_file("android/arm64-v8a.apk", str(self.apk))
        self.target.unrecognized_fields["custom"] = {"version": "3.9.77", "abi": "arm64-v8a",
                                                   "package": "to.pornfetch.app", "release_timestamp": 1792886400}
        self.client = MagicMock()
        self.client.get_targetinfo.return_value = self.target
        self.client.download_target.return_value = str(self.apk)

    def test_signed_identity_and_user_confirmed_install_command(self):
        with patch.object(service, "updater", return_value=self.client):
            update = service.check(None, "3.9.1")
            self.assertEqual(update["source"], "signed_android")
            self.assertEqual(update["download_size"], self.target.length)
            self.client.download_target.assert_not_called()
            service.download_and_request_install(None, "3.9.1")
        request = json.loads((self.root / "install-update.json").read_text())
        self.assertEqual(request, {"version": "3.9.77", "abi": "arm64-v8a"})
        self.assertEqual((self.root / "pornfetch-update.apk").read_bytes(), b"synthetic APK")

    def test_apk_progress_uses_signed_size_and_excludes_metadata_bytes(self):
        updates = []

        def make_updater(settings, on_chunk):
            def metadata(path):
                on_chunk(1000)
                return self.target

            def download(target):
                on_chunk(4)
                on_chunk(target.length - 4)
                return str(self.apk)

            self.client.get_targetinfo.side_effect = metadata
            self.client.download_target.side_effect = download
            return self.client

        with patch.object(service, "updater", side_effect=make_updater):
            service.download_and_request_install(None, "3.9.1", lambda current, total: updates.append((current, total)))
        self.assertEqual(updates, [(0, self.target.length), (4, self.target.length),
                                  (self.target.length, self.target.length)])

    def test_wrong_architecture_tampering_and_cancel_do_not_request_install(self):
        with patch.object(service, "updater", return_value=self.client):
            self.target.custom["abi"] = "x86"
            with self.assertRaises(ValueError):
                service.download_and_request_install(None, "3.9.1")
            self.target.custom["abi"] = "arm64-v8a"
            self.apk.write_bytes(b"tampered")
            with self.assertRaises(Exception):
                service.download_and_request_install(None, "3.9.1")
            event = threading.Event()
            event.set()
            with self.assertRaises(InterruptedError):
                service.download_and_request_install(None, "3.9.1", cancel=event)
        self.assertFalse((self.root / "install-update.json").exists())
