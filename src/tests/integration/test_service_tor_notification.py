"""Offline GUI regression: service Tor failures are visible and independently switchable."""
import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtCore import SIGNAL, QCoreApplication, QEvent, QObject, QSettings, QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QSignalSpy

from src.backend.config import SettingsManager
from src.backend.tor_status import TorStatus
from src.shared import service_transport
from src.shared.tor_runtime import runtime
from src.tests.integration.settings_support import _app

UI_DIR = Path(__file__).resolve().parents[2] / "frontend/UI"


class ServiceTorNotificationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.settings = SettingsManager(QSettings(str(Path(self.temporary.name) / "settings.ini"), QSettings.Format.IniFormat))
        self.settings.service_transport = "tor"
        self.settings.proxy = "socks5h://127.0.0.1:9999"
        self.previous_progress = runtime.progress
        self.previous_listener = service_transport.failure_listener
        self.adapter = TorStatus()
        self.addCleanup(self.restore_callbacks)

    def restore_callbacks(self):
        service_transport.failure_listener = self.previous_listener
        runtime.progress = self.previous_progress

    def close_engine(self, engine):
        for window in engine.rootObjects():
            window.close()
        engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        _app.processEvents()

    def test_mobile_dialog_opens_from_worker_and_disables_only_service_tor(self):
        engine = QQmlApplicationEngine()
        self.addCleanup(self.close_engine, engine)
        engine.rootContext().setContextProperty("torStatus", self.adapter)
        engine.rootContext().setContextProperty("appSettings", self.settings)
        engine.loadData(b"""
            import QtQuick
            import QtQuick.Controls
            ApplicationWindow {
                width: 375; height: 667; visible: true
                ServiceTorFailureDialog {}
            }
        """, QUrl.fromLocalFile(str(UI_DIR / "ServiceTorNoticeTest.qml")))
        self.assertTrue(engine.rootObjects())
        window = engine.rootObjects()[0]
        dialog = window.findChild(QObject, "serviceTorFailureDialog")
        button = window.findChild(QObject, "disableServiceTorButton")
        opened = QSignalSpy(dialog, SIGNAL("opened()"))
        closed = QSignalSpy(dialog, SIGNAL("closed()"))
        self.assertFalse(dialog.property("visible"))
        message = service_transport.service_failure_message("connection")
        asyncio.run(asyncio.to_thread(self.adapter.failureReceived.emit, message))
        self.assertTrue(opened.count() or opened.wait(2000), "Tor failure dialog did not finish opening")
        self.assertTrue(dialog.property("visible"))
        self.assertIn("third-party websites", dialog.property("message"))
        self.assertLessEqual(dialog.property("width"), 375 - 32)
        self.assertLessEqual(dialog.property("height"), 667 - 32)
        with patch.object(runtime, "stop"):
            button.clicked.emit()
        self.assertTrue(closed.count() or closed.wait(2000), "Tor failure dialog did not finish closing")
        self.assertEqual(self.settings.service_transport, "direct")
        self.assertEqual(self.settings.proxy, "socks5h://127.0.0.1:9999")
        self.assertFalse(dialog.property("visible"))
        self.adapter.failureReceived.emit(message)
        _app.processEvents()
        self.assertFalse(dialog.property("visible"))

    def test_retries_do_not_stack_identical_notices(self):
        messages = []
        self.adapter.failure.connect(messages.append)
        with patch("src.backend.tor_status.time.monotonic", return_value=10):
            self.adapter.failureReceived.emit("service unreachable")
            self.adapter.failureReceived.emit("service unreachable")
        self.assertEqual(messages, ["service unreachable"])
        with patch("src.backend.tor_status.time.monotonic", return_value=71):
            self.adapter.failureReceived.emit("service unreachable")
        self.assertEqual(len(messages), 2)
