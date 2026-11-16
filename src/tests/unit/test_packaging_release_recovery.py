"""Publication retries must preserve payload identity and authenticate expired feeds."""
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from securesystemslib.signer import Signer
from tuf.api.exceptions import LengthOrHashMismatchError
from tuf.api.metadata import Metadata, Root

from src.tests.unit.test_cli_self_update import keys_script, publisher
from src.tests.unit.test_deployment_verification import serve_repository


class ReleaseRecoveryTests(unittest.TestCase):
    def test_cli_retry_accepts_identical_bytes_and_rejects_changed_binary(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / 'root.json'
            keys_script.initialize(base / 'keys', root)
            artifact = base / 'artifacts/PornFetch_linux_CLI_x64'
            artifact.mkdir(parents=True)
            binary = artifact / artifact.name
            binary.write_bytes(b'original executable')
            public = base / 'public'
            with patch.object(publisher, 'previous_metadata', return_value=None):
                publisher.publish(artifact.parent, 'unused', public, base / 'keys/online.pem', '3.9.123', root_file=root)
            previous = tuple(Metadata.from_file(str(public / f'metadata/{role}.json'))
                             for role in ('targets', 'snapshot', 'timestamp'))
            with patch.object(publisher, 'previous_metadata', return_value=previous):
                publisher.publish(artifact.parent, 'unused', base / 'retry', base / 'keys/online.pem', '3.9.123', root_file=root)
                binary.write_bytes(b'different executable')
                with self.assertRaisesRegex(ValueError, 'different bytes'):
                    publisher.publish(artifact.parent, 'unused', base / 'bad', base / 'keys/online.pem', '3.9.123', root_file=root)

    def test_expired_feed_recovery_checks_signatures_and_metadata_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root_file = base / 'root.json'
            keys_script.initialize(base / 'keys', root_file)
            artifact = base / 'artifacts/PornFetch_linux_CLI_x64'
            artifact.mkdir(parents=True)
            (artifact / artifact.name).write_bytes(b'executable')
            public = base / 'public'
            with patch.object(publisher, 'previous_metadata', return_value=None):
                publisher.publish(artifact.parent, 'unused', public, base / 'keys/online.pem', '3.9.123', root_file=root_file)
            root = Metadata[Root].from_file(str(root_file))
            signer = Signer.from_priv_key_uri(f'file2:{base / "keys/online.pem"}', root.signed.keys[root.signed.roles['targets'].keyids[0]])
            timestamp = Metadata.from_file(str(public / 'metadata/timestamp.json'))
            timestamp.signed.expires = datetime.now(timezone.utc) - timedelta(days=1)
            timestamp.sign(signer)
            timestamp.to_file(str(public / 'metadata/timestamp.json'))
            with serve_repository(public) as url:
                recovered = publisher.previous_metadata(url, root_file.read_bytes(), base / 'cache')
                self.assertEqual(recovered[0].signed.targets['linux/amd64.zip'].custom['version'], '3.9.123')
                snapshot = Metadata.from_file(str(public / 'metadata/snapshot.json'))
                snapshot.signed.version += 1
                snapshot.sign(signer)
                snapshot.to_file(str(public / 'metadata/snapshot.json'))
                with self.assertRaises(LengthOrHashMismatchError):
                    publisher.previous_metadata(url, root_file.read_bytes(), base / 'bad-cache')


class GitHubReleaseRecoveryTests(unittest.TestCase):
    def test_retry_verifies_existing_assets_before_publishing(self):
        from types import SimpleNamespace

        from src.tests.unit.test_cli_self_update import load_script
        github = load_script('publish_github_release')
        with tempfile.TemporaryDirectory() as temporary:
            assets = Path(temporary)
            (assets / 'app.zip').write_bytes(b'original signed package')
            release = {'prerelease': True, 'assets': [{'name': 'app.zip'}]}

            def api(arguments, **kwargs):
                payload = release if '/releases/tags/' in arguments[-1] else {'sha': 'commit'}
                return SimpleNamespace(returncode=0, stdout=json.dumps(payload), stderr='')

            def gh(*arguments):
                if arguments[:2] == ('release', 'download'):
                    (Path(arguments[-1]) / 'app.zip').write_bytes(b'original signed package')
                return 'commit\n'

            with patch.dict('os.environ', {'GITHUB_REPOSITORY': 'owner/repo'}), \
                    patch.object(github.subprocess, 'run', side_effect=api), \
                    patch.object(github, 'gh', side_effect=gh) as commands:
                github.publish(assets, '3.9.123', 'commit', 'beta', assets / 'notes.md')
                self.assertIn(unittest.mock.call('release', 'edit', 'v3.9.123', '--draft=false'), commands.call_args_list)
                (assets / 'app.zip').write_bytes(b'different signed package')
                commands.reset_mock()
                with self.assertRaisesRegex(ValueError, 'asset differs'):
                    github.publish(assets, '3.9.123', 'commit', 'beta', assets / 'notes.md')
                self.assertNotIn(unittest.mock.call('release', 'edit', 'v3.9.123', '--draft=false'), commands.call_args_list)
