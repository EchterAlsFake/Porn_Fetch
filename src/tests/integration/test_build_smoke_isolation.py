"""The builder's GUI startup check must not consume the user's first-use state."""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class BuildSmokeIsolationTests(unittest.TestCase):
    def test_desktop_and_mobile_smoke_leave_real_settings_and_download_cache_untouched(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            settings = state / 'config/EchterAlsFake/Porn Fetch.conf'
            checkpoint = state / 'cache/PornFetch/states/download.json'
            settings.parent.mkdir(parents=True)
            checkpoint.parent.mkdir(parents=True)
            settings.write_text('[Onboarding]\nlicense_offer_seen=false\nukraine_message_seen=false\n')
            checkpoint.write_text('{"sentinel": "existing download"}')
            originals = {file: file.read_bytes() for file in (settings, checkpoint)}
            launch_directory = state / 'readonly'
            launch_directory.mkdir(mode=0o555)
            env = {**os.environ, 'QT_QPA_PLATFORM': 'offscreen', 'XDG_CONFIG_HOME': str(state / 'config'),
                   'XDG_CACHE_HOME': str(state / 'cache'), 'XDG_DATA_HOME': str(state / 'data'),
                   'PYTHONPATH': str(root), 'PORN_FETCH_LOG_DIR': str(state / 'logs')}
            direct = """
import os, sys
os.environ.pop('PORN_FETCH_TEST_ENV', None)
sys.argv = ['main.py', '--smoke-test']
from src.backend.application import main
from src.backend.config import app_settings
main()
assert not app_settings.license_offer_seen
assert not app_settings.license_accepted
assert not app_settings.setup_completed
"""
            commands = ([str(root / 'main.py'), '--smoke-test'],
                        [str(root / 'main.py'), '--smoke-test', '--android'], ['-c', direct])
            for command in commands:
                with self.subTest(command=command[:2]):
                    result = subprocess.run([sys.executable, *command],
                                            cwd=launch_directory, env=env, capture_output=True, text=True, timeout=30)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('GUI smoke test passed', result.stdout)
                    for file, original in originals.items():
                        self.assertEqual(file.read_bytes(), original)
                    self.assertEqual(list((state / 'config').rglob('*.conf')), [settings])
                    self.assertEqual(list(launch_directory.iterdir()), [])
                    if command[0] != '-c':
                        self.assertFalse((state / 'logs').exists(), 'Smoke logs escaped their disposable directory')
