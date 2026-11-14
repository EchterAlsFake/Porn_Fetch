"""Exercise first-run choices against real QML and persistent, isolated settings."""
import hashlib
from pathlib import Path

from PySide6.QtCore import QMetaObject, QObject, QPointF, QSettings, Qt, QUrl
from PySide6.QtTest import QTest

from src.backend.config import SettingsManager
from src.shared.error_reporting import ERROR_REPORT_DISCLOSURE
from src.tests.integration import test_mobile_onboarding as mobile

UI = mobile.UI


class FirstRunSetupTests(mobile.MobileOnboardingTests):
    # The parent supplies isolated Qt/settings infrastructure, not extra test cases.
    test_mobile_message_fills_window_in_both_orientations = None
    test_folder_setup_survives_cancellation_and_saves_selection = None

    def open_setup(self, android=False, keyboard_navigation=True):
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
                    keyboardNavigation: {str(keyboard_navigation).lower()}
                }}
                Component.onCompleted: dialog.begin()
            }}
        '''.encode(),
            QUrl.fromLocalFile(str(UI / 'FirstRunFixture.qml')))
        self.assertTrue(self.engine.rootObjects(), self.warnings)
        QTest.qWait(250)
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

    def test_touch_setup_has_no_forced_focus_but_keyboard_still_works(self):
        dialog = self.open_setup(android=True, keyboard_navigation=False)
        self.assertFalse(self.control('setupTextReader').property('activeFocus'))
        rings = dialog.findChildren(QObject, 'setupFocusRing')
        self.assertTrue(rings)
        self.assertFalse(any(ring.property('visible') for ring in rings))
        accept = self.control('setupAcceptLicenseCheckBox')
        position = accept.mapToScene(QPointF(accept.width() / 2, accept.height() / 2)).toPoint()
        QTest.mouseClick(self.window, Qt.LeftButton, pos=position)
        self.assertTrue(accept.property('checked'))
        self.assertFalse(any(ring.property('visible') for ring in rings))
        self.advance()
        self.assertEqual(dialog.property('step'), 'offer')
        self.assertFalse(self.control('setupTextReader').property('activeFocus'))
        self.assertFalse(any(ring.property('visible') for ring in rings))
        self.key(Qt.Key_Right, 'setupBuyLicenseButton')
        self.assertTrue(any(ring.property('visible') for ring in rings))
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

    def key(self, key, focus=None, modifiers=Qt.NoModifier):
        QTest.keyClick(self.window, key, modifiers)
        QTest.qWait(30)
        if focus:
            self.assertTrue(self.control(focus).property('activeFocus'),
                            f'{focus}: actual focus is {self.window.activeFocusItem().objectName()}')

    def test_dpad_completes_all_five_steps_with_explicit_choices(self):
        dialog = self.open_setup(android=True)
        self.window.resize(960, 540)
        QTest.qWait(50)
        self.assertTrue(self.control('setupPageScroll').property('activeFocus'))
        flick = self.control('setupPageScroll').property('contentItem')
        self.key(Qt.Key_Down, 'setupPageScroll')
        self.assertGreater(flick.property('contentY'), 0)
        self.key(Qt.Key_Up, 'setupPageScroll')
        self.assertEqual(flick.property('contentY'), 0)
        # Right leaves the text reader without forcing a full license scroll.
        self.key(Qt.Key_Right, 'setupAcceptLicenseCheckBox')
        self.assertFalse(self.settings.license_accepted)
        self.key(Qt.Key_Enter)
        self.assertTrue(self.control('setupAcceptLicenseCheckBox').property('checked'))
        self.assertFalse(self.settings.license_accepted)
        self.key(Qt.Key_Down, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupContinueButton')
        self.key(Qt.Key_Enter, 'setupPageScroll')
        self.assertEqual(dialog.property('step'), 'offer')
        self.key(Qt.Key_Right, 'setupBuyLicenseButton')
        # Focused actions inside the reader must be scrolled into view.
        button = self.control('setupBuyLicenseButton')
        self.assertGreater(flick.property('contentY'), 0)
        self.assertGreaterEqual(button.mapToItem(flick, 0, 0).y(), -1)
        self.assertLessEqual(button.mapToItem(flick, 0, button.height()).y(), flick.height() + 1)
        self.key(Qt.Key_Right, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupContinueButton')
        self.key(Qt.Key_Enter, 'setupPageScroll')
        self.assertEqual(dialog.property('step'), 'reporting')
        self.key(Qt.Key_Right, 'setupReportsOff')
        self.key(Qt.Key_Down, 'setupReportsBasic')
        self.key(Qt.Key_Down, 'setupReportsFull')
        self.assertEqual(dialog.property('reportingChoice'), -1)
        self.assertFalse(self.control('setupContinueButton').property('enabled'))
        self.key(Qt.Key_Up, 'setupReportsBasic')
        self.key(Qt.Key_Enter)
        self.assertEqual(dialog.property('reportingChoice'), 1)
        self.key(Qt.Key_Down, 'setupReportsFull')
        self.key(Qt.Key_Down, 'setupDisclosureToggle')
        self.key(Qt.Key_Enter)
        self.assertTrue(self.control('setupDisclosureToggle').property('checked'))
        self.key(Qt.Key_Down, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupContinueButton')
        self.key(Qt.Key_Enter, 'setupPageScroll')
        self.assertEqual(dialog.property('step'), 'ukraine')
        self.key(Qt.Key_Up, 'ukraineDiscoveryButton')
        self.key(Qt.Key_Down, 'setupPageScroll')
        self.key(Qt.Key_Right, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupContinueButton')
        self.key(Qt.Key_Enter, 'setupPageScroll')
        self.assertEqual(dialog.property('step'), 'folder')
        self.key(Qt.Key_Right, 'setupChooseFolderButton')
        self.key(Qt.Key_Enter)
        picker = self.control('setupFolderPicker')
        self.assertTrue(picker.property('visible'))
        # Native picker interaction/permissions require Android. Exercise its
        # cancellation and accepted-result boundary with disposable storage.
        QMetaObject.invokeMethod(picker, 'reject')
        self.window.requestActivate()  # The offscreen platform has no window manager.
        QTest.qWait(50)
        self.assertTrue(self.control('setupChooseFolderButton').property('activeFocus'))
        self.key(Qt.Key_Right, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupPageScroll')  # Finish stays unavailable.
        self.assertFalse(self.settings.setup_completed)
        self.key(Qt.Key_Right, 'setupChooseFolderButton')
        self.key(Qt.Key_Enter)
        folder = QUrl.fromLocalFile(self.temporary.name)
        picker.setProperty('selectedFolder', folder)
        QMetaObject.invokeMethod(picker, 'accept')
        self.window.requestActivate()
        QTest.qWait(50)
        self.assertTrue(self.control('setupChooseFolderButton').property('activeFocus'))
        self.key(Qt.Key_Right, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupContinueButton')
        self.key(Qt.Key_Enter)
        self.assertTrue(self.settings.setup_completed)
        self.assertTrue(self.settings.enable_logging)
        self.assertFalse(self.settings.error_reporting_full_traceback)
        self.assertEqual(self.warnings, [])

    def test_keyboard_tab_activation_and_remote_back(self):
        dialog = self.open_setup(android=True)
        self.key(Qt.Key_Tab, 'setupAcceptLicenseCheckBox')
        self.key(Qt.Key_Return)
        self.key(Qt.Key_Tab, 'setupBackButton')
        self.key(Qt.Key_Tab, 'setupContinueButton')
        self.key(Qt.Key_Return, 'setupPageScroll')
        self.assertEqual(dialog.property('step'), 'offer')
        self.key(Qt.Key_Back, 'setupPageScroll')
        self.assertEqual(dialog.property('step'), 'license')
        self.assertEqual(self.control('setupPageScroll').property('contentItem').property('contentY'), 0)
        self.key(Qt.Key_Back, 'setupBackButton')
        self.assertTrue(dialog.property('visible'))
        self.key(Qt.Key_Tab, 'setupContinueButton')
        self.key(Qt.Key_Tab, 'setupPageScroll')
        self.key(Qt.Key_Backtab, 'setupContinueButton')
        self.key(Qt.Key_Tab, 'setupBackButton', Qt.ShiftModifier)
        self.key(Qt.Key_Escape, 'setupBackButton')
        self.assertFalse(self.settings.setup_completed)
        self.assertEqual(self.warnings, [])

    def test_dpad_shared_downloads_completes_setup_without_opening_picker(self):
        self.backend.shared_downloads = True
        # Resume at the storage choice to exercise the native-picker-free path.
        self.settings.accept_application_license(Path('LICENSE').read_text())
        self.settings.mark_license_offer_seen()
        self.settings.set_error_reporting_options(False, False)
        self.settings.mark_ukraine_message_seen()
        dialog = self.open_setup(android=True)
        self.assertEqual(dialog.property('step'), 'folder')
        self.assertFalse(self.control('setupContinueButton').property('enabled'))
        self.key(Qt.Key_Right, 'setupChooseFolderButton')
        self.key(Qt.Key_Down, 'setupSharedDownloadsButton')
        self.key(Qt.Key_Enter)
        self.assertEqual(self.settings.android_output_folder, 'mediastore:Download/Porn Fetch')
        self.assertFalse(self.control('setupFolderPicker').property('visible'))
        self.key(Qt.Key_Down, 'setupBackButton')
        self.key(Qt.Key_Right, 'setupContinueButton')
        self.key(Qt.Key_Enter)
        self.assertTrue(self.settings.setup_completed)
        self.assertEqual(self.warnings, [])
