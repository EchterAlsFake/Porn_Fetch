"""Android publication uses the existing trust root and retains stable targets."""
import hashlib
import unittest
from datetime import datetime, timedelta, timezone

from securesystemslib.signer import CryptoSigner
from tuf.api.metadata import Metadata, Root

from src.tests.unit.test_cli_self_update import load_script

publisher = load_script("publish_android_updates")


class AndroidPublisherTests(unittest.TestCase):
    def test_stable_selection_and_signed_metadata_relationships(self):
        artifact = {"filename": "PornFetch_android_GUI_arm64-v8a.apk", "size": 3,
                    "sha256": hashlib.sha256(b"apk").hexdigest(), "platform": "android",
                    "kind": "apk", "arch": "arm64"}
        releases = [{"version": version, "channel": channel, "published_at": "2026-10-25T00:00:00+00:00",
                     "notes": "notes", "artifacts": [artifact]} for version, channel in (("3.9.78", "beta"), ("3.9.77", "stable"))]
        targets = publisher.select_targets(releases)
        self.assertEqual(targets["android/arm64-v8a.apk"].custom["version"], "3.9.77")
        offline, online = CryptoSigner.generate_ed25519(), CryptoSigner.generate_ed25519()
        root = Metadata(Root(expires=datetime.now(timezone.utc) + timedelta(days=365)))
        root.signed.add_key(offline.public_key, "root")
        for role in ("targets", "snapshot", "timestamp"):
            root.signed.add_key(online.public_key, role)
        root.sign(offline)
        files = publisher.signed_files(root.to_bytes(), targets, online)
        parsed = {name: Metadata.from_bytes(value) for name, value in files.items()}
        for role in ("targets", "snapshot", "timestamp"):
            item = parsed[role + ".json"]
            root.signed.verify_delegate(role, item.signed_bytes, item.signatures)
        parsed["timestamp.json"].signed.snapshot_meta.verify_length_and_hashes(files["snapshot.json"])
        parsed["snapshot.json"].signed.meta["targets.json"].verify_length_and_hashes(files["targets.json"])
        second = publisher.signed_files(root.to_bytes(), targets, online,
                                        tuple(parsed[r + ".json"] for r in ("targets", "snapshot", "timestamp")))
        self.assertEqual(Metadata.from_bytes(second["timestamp.json"]).signed.version, 2)
