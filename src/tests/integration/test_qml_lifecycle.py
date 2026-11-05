"""QML objects must be destroyed before their Python context providers."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from PySide6.QtCore import QSettings, QUrl
from PySide6.QtQml import QQmlApplicationEngine
from shiboken6 import isValid

from src.backend.config import SettingsManager
from src.backend.qml_lifecycle import destroy_qml_engine
from src.tests.integration.settings_support import _app

ROOT = Path(__file__).resolve().parents[3]


class QmlLifecycleTests(unittest.TestCase):
    def test_retained_engine_destroys_windows_before_context_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            engine = QQmlApplicationEngine()
            # Both external providers and engine-owned adapters exist in production.
            settings = SettingsManager(QSettings(directory + "/settings.ini", QSettings.IniFormat))
            adapter = SettingsManager(QSettings(directory + "/adapter.ini", QSettings.IniFormat))
            adapter.setParent(engine)
            engine.rootContext().setContextProperty("appSettings", settings)
            engine.rootContext().setContextProperty("adapter", adapter)
            engine.retained_adapter = SimpleNamespace(engine=engine)
            warnings = []
            engine.warnings.connect(lambda errors: warnings.extend(e.toString() for e in errors))
            for _ in range(2):
                engine.loadData(b"""
                    import QtQuick
                    import QtQuick.Controls
                    ApplicationWindow {
                        width: 400; height: 300; visible: true
                        Label { text: appSettings.font_size + " / " + adapter.font_size }
                    }
                """, QUrl())
            roots = engine.rootObjects()
            self.assertEqual(len(roots), 2)
            provider_alive = []
            for root in roots:
                root.destroyed.connect(lambda: provider_alive.append(isValid(adapter)))
            _app.processEvents()
            destroy_qml_engine(engine)
            self.assertEqual(provider_alive, [True, True])
            self.assertFalse(isValid(engine))
            self.assertFalse(any(isValid(root) for root in roots))
            self.assertTrue(isValid(settings))
            self.assertEqual(warnings, [])
            # Another owner may still hold the wrapper after cleanup.
            destroy_qml_engine(engine)

    def test_real_app_close_and_smoke_exit_have_no_null_context_errors(self):
        script = """
import gc
import sys
from PySide6.QtCore import QTimer
from src.backend.config import app_settings
app_settings.update_checks = False
app_settings.track_videos = False
app_settings.mark_ukraine_message_seen()
app_settings.set_error_reporting_consent(False)
mode, layout = sys.argv[1:]
sys.argv = ['main.py'] + (['--smoke-test'] if mode == 'smoke' else []) + (['--android'] if layout == 'mobile' else [])
from src.backend import application
# Import after the application: importing unittest disables its production GUI setup.
from unittest.mock import patch
from base_api import BaseCore
from curl_cffi.requests import AsyncSession
if mode == 'close':
    QTimer.singleShot(500, lambda: application.engine.rootObjects()[-1].close())
    QTimer.singleShot(15000, application.app.quit)
with patch.object(BaseCore, 'request', side_effect=AssertionError('Unexpected HTTP')) as core_request, \\
     patch.object(AsyncSession, 'request', side_effect=AssertionError('Unexpected HTTP')) as session_request:
    application.main()
    core_request.assert_not_called()
    session_request.assert_not_called()
assert application.engine is None
assert application.splash is None
gc.collect()
print('Clean application exit')
"""
        for mode in ("smoke", "close"):
            for layout in ("desktop", "mobile"):
                with self.subTest(mode=mode, layout=layout), tempfile.TemporaryDirectory() as directory:
                    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software",
                               XDG_CONFIG_HOME=directory + "/config", XDG_DATA_HOME=directory + "/data",
                               XDG_CACHE_HOME=directory + "/cache")
                    env.pop("PORN_FETCH_TEST_ENV", None)
                    result = subprocess.run([sys.executable, "-c", script, mode, layout], cwd=ROOT,
                                            env=env, capture_output=True, text=True, timeout=30)
                    output = result.stdout + result.stderr
                    self.assertEqual(result.returncode, 0, output)
                    self.assertIn("Clean application exit", result.stdout)
                    self.assertNotIn("TypeError:", output)
                    self.assertNotIn("ReferenceError:", output)
                    if mode == "close":
                        self.assertEqual(output.count("Application teardown finished."), 1)
