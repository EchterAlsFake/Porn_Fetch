"""Exercise first-run choices against real QML and persistent, isolated settings."""
import hashlib
from pathlib import Path

from PySide6.QtCore import QMetaObject, QObject, QSettings, Qt, QUrl
from PySide6.QtTest import QTest

from src.backend.config import SettingsManager
from src.shared.error_reporting import ERROR_REPORT_DISCLOSURE
from src.tests.integration import test_mobile_onboarding as mobile

UI = mobile.UI


class FirstRunSetupTests(mobile.MobileOnboardingTests):
    # The parent supplies isolated Qt/settings infrastructure, not extra test cases.
    test_mobile_message_fills_window_in_both_orientations = None
    test_folder_setup_survives_cancellation_and_saves_selection = None

    def open_setup(self, android=False):
        self.license = Path('LICENSE').read_text()
        self.engine.rootContext().setContextProperty('applicationLicenseText', self.license)
        self.engine.loadData(f'''
            import QtQuick
            import QtQuick.Controls
            ApplicationWindow {{
                width: {360 if android else 1100}; height: {640 if android else 800}; visible: true
                FirstRunSetup {{
                    id: dialog; settings: appSettings
                    licenseText: applicationLicenseText; reportDisclosure: disclosureText
                    fullScreen: {str(android).lower()}; requireOutputFolder: {str(android).lower()}
                }}
                Component.onCompleted: dialog.begin()
            }}
        '''.encode(),
            QUrl.fromLocalFile(str(UI / 'FirstRunFixture.qml')))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        QTest.qWait(100)
        self.window = self.engine.rootObjects()[0]
        self.dialog = self.window.findChild(QObject, 'firstRunSetup')
        return self.dialog

    def setUp(self):
        super().setUp()
        self.engine.rootContext().setContextProperty('disclosureText', ERROR_REPORT_DISCLOSURE)

    def control(self, name):
        result = self.window.findChild(QObject, name)
        self.assertIsNotNone(result, name)
        return result

    def advance(self):
        self.assertTrue(self.control('setupContinueButton').property('enabled'))
        self.control('setupContinueButton').clicked.emit()
        QTest.qWait(30)

    def accept(self):
        self.control('setupAcceptLicenseCheckBox').forceActiveFocus()
        QTest.keyClick(self.window, Qt.Key_Space)
        self.assertTrue(self.control('setupAcceptLicenseCheckBox').property('checked'))
        self.advance()

    def test_explicit_choices_complete_once_and_survive_reset(self):
        dialog = self.open_setup()
        self.assertEqual(dialog.property('step'), 'license')
        self.assertFalse(self.control('setupContinueButton').property('enabled'))
        self.assertEqual(self.control('setupLicenseText').property('text'), self.license)
        self.assertFalse(self.settings.license_accepted)
        self.accept()
        self.assertTrue(self.settings.license_accepted)
        self.assertEqual(self.settings.get_str('Onboarding/license_accepted_sha256'),
                         hashlib.sha256(self.license.encode()).hexdigest())
        self.assertEqual(self.settings.get_str('Onboarding/license_accepted_text'), self.license)
        self.assertTrue(self.settings.get_str('Onboarding/license_accepted_at'))
        self.assertEqual(dialog.property('step'), 'offer')
        self.assertFalse(self.settings.license_offer_seen)  # Opening never consumes it.
        self.advance()
        self.assertTrue(self.settings.license_offer_seen)
        self.assertEqual(dialog.property('step'), 'reporting')
        self.assertFalse(self.control('setupContinueButton').property('enabled'))
        self.control('setupReportsBasic').clicked.emit()
        self.advance()
        self.assertTrue(self.settings.enable_logging)
        self.assertFalse(self.settings.error_reporting_full_traceback)
        self.assertEqual(dialog.property('step'), 'ukraine')
        self.assertFalse(self.settings.ukraine_message_seen)
        self.assertFalse(self.settings.setup_completed)
        self.advance()
        self.assertTrue(self.settings.setup_completed)
        for _ in range(30):
            if not dialog.property('visible'):
                break
            QTest.qWait(50)
        self.assertFalse(dialog.property('visible'))
        self.settings.reset()
        saved = SettingsManager(QSettings(self.path, QSettings.IniFormat))
        self.assertTrue(saved.setup_completed)
        self.assertTrue(saved.enable_logging)
        self.assertFalse(saved.error_reporting_full_traceback)
        QMetaObject.invokeMethod(dialog, 'begin')
        self.assertFalse(dialog.property('visible'))
        self.assertEqual(self.warnings, [])

    def test_interrupted_setup_resumes_without_consuming_offer(self):
        dialog = self.open_setup()
        self.accept()
        QMetaObject.invokeMethod(dialog, 'close')
        self.assertFalse(self.settings.license_offer_seen)
        self.assertFalse(self.settings.setup_completed)
        QMetaObject.invokeMethod(dialog, 'begin')
        QTest.qWait(30)
        self.assertEqual(dialog.property('step'), 'offer')
        self.assertTrue(dialog.property('visible'))
        self.assertEqual(self.warnings, [])

    def test_android_requires_accessible_folder_and_fits_both_orientations(self):
        dialog = self.open_setup(android=True)
        self.assertEqual(self.control('setupStepCounter').property('text'), 'Setup 1 of 5')
        for width, height in ((360, 640), (640, 360)):
            self.window.resize(width, height)
            QTest.qWait(50)
            self.assertEqual(dialog.property('width'), width)
            self.assertEqual(dialog.property('height'), height)
            self.assertGreater(dialog.property('contentItem').property('height'), 0)
            self.assertGreater(dialog.property('footer').property('height'), 0)
        self.accept()
        self.advance()  # Offer
        self.control('setupReportsFull').clicked.emit()
        self.advance()
        self.assertTrue(self.settings.enable_logging)
        self.assertTrue(self.settings.error_reporting_full_traceback)
        self.advance()  # Ukraine acknowledgement
        self.assertEqual(dialog.property('step'), 'folder')
        self.assertFalse(self.control('setupContinueButton').property('enabled'))
        self.assertFalse(self.settings.finish_setup(True))
        picker = self.control('setupFolderPicker')
        QMetaObject.invokeMethod(picker, 'open')
        QTest.qWait(50)
        QMetaObject.invokeMethod(picker, 'reject')
        self.assertTrue(dialog.property('visible'))
        self.assertFalse(self.settings.setup_completed)
        folder = QUrl.fromLocalFile(self.temporary.name)
        QMetaObject.invokeMethod(picker, 'open')
        QTest.qWait(50)
        picker.setProperty('currentFolder', folder)
        picker.setProperty('selectedFolder', folder)
        picker.accepted.emit()
        QMetaObject.invokeMethod(picker, 'close')
        QTest.qWait(50)
        self.advance()
        self.assertTrue(self.settings.setup_completed)
        self.assertEqual(QUrl(self.settings.android_output_folder), folder)
        self.assertEqual(self.warnings, [])
