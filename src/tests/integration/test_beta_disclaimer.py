from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PySide6.QtCore import QCoreApplication, QEvent, QObject, QSettings, Qt, QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QTest

from src.backend.beta_disclaimer import BetaDisclaimerBridge
from src.backend.config import SettingsManager
from src.tests.integration.settings_support import _app

UI_DIR = Path(__file__).resolve().parents[2] / "frontend" / "UI"


class BetaDisclaimerGuiTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.settings_path = str(Path(self.temporary.name) / "settings.ini")
        self.settings = SettingsManager(QSettings(self.settings_path, QSettings.Format.IniFormat))
        self.bridge = BetaDisclaimerBridge(self.settings)
        self.now = 100.0
        clock = patch("src.shared.beta_disclaimer.time", SimpleNamespace(monotonic=lambda: self.now))
        clock.start()
        self.addCleanup(clock.stop)

    def test_acceptance_requires_elapsed_time_and_survives_restart(self):
        self.assertFalse(self.settings.beta_disclaimer_accepted)
        self.assertFalse(self.bridge.accept())
        self.bridge.startReading()
        self.now = 129.999
        self.assertFalse(self.bridge.accept())
        self.now = 130.0
        self.assertTrue(self.bridge.accept())
        reloaded = SettingsManager(QSettings(self.settings_path, QSettings.Format.IniFormat))
        self.assertTrue(reloaded.beta_disclaimer_accepted)
        self.bridge.stopReading()

    def test_mobile_sized_dialog_blocks_enter_escape_and_early_ok(self):
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("testDisclaimer", self.bridge)
        engine.loadData(b"""
            import QtQuick
            import QtQuick.Controls
            ApplicationWindow {
                id: window
                width: 400
                height: 800
                visible: true
                property int confirmedCount: 0
                BetaDisclaimerDialog {
                    disclaimer: testDisclaimer
                    onConfirmed: window.confirmedCount += 1
                    Component.onCompleted: open()
                }
            }
        """, QUrl.fromLocalFile(str(UI_DIR / "BetaDisclaimerTest.qml")))
        self.assertTrue(engine.rootObjects())
        window = engine.rootObjects()[0]
        dialog = window.findChild(QObject, "betaDisclaimerDialog")
        button = window.findChild(QObject, "betaDisclaimerOkButton")
        self.assertIsNotNone(dialog)
        self.assertIsNotNone(button)
        QTest.qWait(250)
        self.assertFalse(button.property("enabled"))
        QTest.keyClick(window, Qt.Key.Key_Return)
        QTest.keyClick(window, Qt.Key.Key_Escape)
        button.clicked.emit()
        self.assertTrue(dialog.property("visible"))
        self.assertFalse(self.settings.beta_disclaimer_accepted)

        self.now = 130.0
        self.bridge._refresh_countdown()
        _app.processEvents()
        self.assertTrue(button.property("enabled"))
        button.clicked.emit()
        self.assertTrue(self.settings.beta_disclaimer_accepted)
        self.assertEqual(window.property("confirmedCount"), 1)
        window.close()
        engine.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        _app.processEvents()
