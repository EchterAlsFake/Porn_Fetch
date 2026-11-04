"""First-launch license offer: order, persistence and purchase link."""
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import QObject, QSettings, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtTest import QSignalSpy

from src.backend.config import SettingsManager
from src.backend.qml_lifecycle import destroy_qml_engine
from src.tests.integration.test_ukraine_message import UrlCapture

UI = Path(__file__).resolve().parents[2] / "frontend/UI"


class LicenseOfferTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.path = str(Path(self.temporary.name) / "settings.ini")
        self.settings = SettingsManager(QSettings(self.path, QSettings.IniFormat))
        self.engines = []
        self.addCleanup(self.cleanup_engines)

    def cleanup_engines(self):
        for engine in self.engines:
            destroy_qml_engine(engine)
        self.engines.clear()

    def load(self, width=900, height=950):
        engine = QQmlApplicationEngine()
        self.engines.append(engine)
        engine.rootContext().setContextProperty("appSettings", self.settings)
        warnings = []
        engine.warnings.connect(lambda errors: warnings.extend(e.toString() for e in errors))
        engine.loadData(f"""
            import QtQuick
            import QtQuick.Controls
            ApplicationWindow {{
                width: {width}; height: {height}; visible: true
                LicenseOfferDialog {{
                    id: offer
                    settings: appSettings
                    onDismissed: ukraine.presentOnce()
                }}
                UkraineMessageDialog {{ id: ukraine; settings: appSettings }}
                Component.onCompleted: {{
                    if (!offer.presentOnce()) ukraine.presentOnce()
                }}
            }}
        """.encode(), QUrl.fromLocalFile(str(UI / "OfferFixture.qml")))
        self.assertTrue(engine.rootObjects(), warnings)
        window = engine.rootObjects()[0]
        offer = window.findChild(QObject, "licenseOfferDialog")
        if offer.property("visible") and not offer.property("opened"):
            self.assertTrue(QSignalSpy(offer.opened).wait(3000))
        self.assertFalse(warnings, warnings)
        return window, offer

    def test_offer_precedes_ukraine_and_is_remembered_after_reset_and_restart(self):
        window, offer = self.load()
        ukraine = window.findChild(QObject, "ukraineMessageDialog")
        self.assertTrue(offer.property("visible"))
        self.assertFalse(ukraine.property("visible"))
        self.assertTrue(self.settings.license_offer_seen)
        window.findChild(QObject, "licenseOfferContinueButton").clicked.emit()
        if not ukraine.property("opened"):
            self.assertTrue(QSignalSpy(ukraine.opened).wait(3000))
        self.assertFalse(offer.property("visible"))
        self.assertTrue(self.settings.ukraine_message_seen)
        self.cleanup_engines()
        self.settings.reset()
        self.settings = SettingsManager(QSettings(self.path, QSettings.IniFormat))
        window, offer = self.load()
        self.assertFalse(offer.property("visible"))
        self.assertFalse(window.findChild(QObject, "ukraineMessageDialog").property("visible"))

    def test_mobile_purchase_button_opens_website_without_closing_offer(self):
        capture = UrlCapture()
        QDesktopServices.setUrlHandler("https", capture, "capture")
        self.addCleanup(lambda: QDesktopServices.unsetUrlHandler("https"))
        window, offer = self.load(360, 640)
        self.assertEqual(window.findChild(QObject, "licenseOfferPrice").property("text"), "19.99 €")
        self.assertLessEqual(offer.property("height"), 616)
        self.assertEqual(capture.urls, [])
        window.findChild(QObject, "licenseOfferBuyButton").clicked.emit()
        self.assertEqual(capture.urls, ["https://pornfetch.to"])
        self.assertTrue(offer.property("visible"))
