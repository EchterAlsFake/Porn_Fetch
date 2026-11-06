"""Offline notification delivery, privacy and actual QML keyboard contracts."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ["QML_DISABLE_DISK_CACHE"] = "1"

from PySide6.QtCore import QEvent, QMetaObject, QObject, QSettings, Qt, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow  # noqa: F401
from PySide6.QtTest import QTest

from src.backend.config import SettingsManager
from src.backend.notifications import NotificationCenter
from src.backend.shared_gui import set_notice_handler, ui_popup
from src.backend.system_notifications import SystemNotifications


class NotificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QGuiApplication.instance() or QGuiApplication([])
        cls.app.setQuitOnLastWindowClosed(False)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.settings = SettingsManager(QSettings(str(Path(self.temporary.name) / "settings.ini"), QSettings.IniFormat))
        self.center = NotificationCenter(self.settings)

    def tearDown(self):
        set_notice_handler(None)

    def test_feedback_is_nonblocking_and_frontend_routed_on_ios(self):
        set_notice_handler(self.center.publish)
        with (
            patch("sys.platform", "ios"),
            patch(
                "src.backend.shared_gui.QGuiApplication.instance",
                side_effect=AssertionError("Presenter must own delivery"),
            ),
        ):
            ui_popup("Finished", severity="success", key="task")
        self.assertEqual(self.center.latest["severity"], "success")
        self.assertEqual(self.center.latest["message"], "Finished")

    def test_suppression_preserves_failure_and_success_does_not_hide_error(self):
        self.center.download_failed("support-1")
        first = self.center.latest["id"]
        self.center.download_completed()
        self.assertEqual(self.center.latest["id"], first)
        self.settings.supress_errors = True
        self.center.dismiss()
        self.center.download_failed("support-2")
        self.assertFalse(self.center.latest)
        failure = next(e for e in self.center.entries if e["key"] == "download-failed")
        self.assertEqual(failure["count"], 2)
        self.assertIn("support-2", failure["details"])

    def test_private_text_is_scrubbed_before_display_copy_and_after_mode_change(self):
        self.center.publish(
            "Could not read https://example.test/private?token=secret\nDebug for GitHub\nTraceback", severity="error"
        )
        self.center.copy(self.center.latest["id"])
        copied = self.app.clipboard().text()
        self.assertNotIn("example.test", copied)
        self.assertNotIn("Traceback", copied)
        self.center.publish("Example media title", "Creator name")
        self.settings.anonymous_mode = True
        self.center.copy(self.center.entries[0]["id"])
        self.assertNotIn("Example media title", str(self.center.entries))
        self.assertNotIn("Creator name", self.app.clipboard().text())

    def test_session_is_bounded_and_restart_survives_message_dismissal(self):
        for index in range(60):
            self.center.publish(str(index))
        self.assertEqual(len(self.center.entries), 50)
        self.center.require_restart()
        self.center.clear()
        self.assertTrue(self.center.restartRequired)
        self.assertFalse(self.center.entries)

    def test_decisions_are_queued_and_cancellation_does_not_accept_an_action(self):
        accepted = []
        self.center.decisionAccepted.connect(accepted.append)
        self.center.request_decision("first", "First action", "Confirm first")
        self.center.request_decision("second", "Second action", "Confirm second")
        self.center.resolve_decision("first", False)
        self.assertEqual(accepted, [])
        self.assertEqual(self.center.pendingDecision["action"], "second")
        self.center.resolve_decision("second", True)
        self.assertEqual(accepted, ["second"])
        self.assertFalse(self.center.pendingDecision)

    def test_activity_escape_restores_focus_and_privacy_closes_history(self):
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("appSettings", self.settings)
        engine.rootContext().setContextProperty("noticeCenter", self.center)
        warnings = []
        engine.warnings.connect(lambda messages: warnings.extend(str(e) for e in messages))
        ui = Path(__file__).resolve().parents[2] / "frontend/UI/NotificationFixture.qml"
        engine.loadData(
            b"""import QtQuick
import QtQuick.Controls
ApplicationWindow {
    visible: true; width: 400; height: 700
    NotificationPanel { anchors.left: parent.left; anchors.right: parent.right }
}""",
            QUrl.fromLocalFile(str(ui)),
        )
        self.assertTrue(engine.rootObjects(), warnings)
        window = engine.rootObjects()[0]
        window.requestActivate()
        self.addCleanup(engine.deleteLater)
        self.addCleanup(window.close)
        self.center.publish("A recoverable error", severity="error")
        QTest.qWait(30)
        button = window.findChild(QObject, "recentActivityButton")
        QMetaObject.invokeMethod(button, "forceActiveFocus")
        button.clicked.emit()
        dialog = window.findChild(QObject, "recentActivityDialog")
        QTest.qWait(250)
        self.assertTrue(dialog.property("visible"))
        QTest.keyClick(window, Qt.Key_Escape)
        QTest.qWait(250)
        self.assertFalse(dialog.property("visible"))
        self.assertEqual(window.activeFocusItem(), button)
        self.assertTrue(
            button.property("visualFocus"),
            f"active={button.property('activeFocus')}, reason={button.property('focusReason')}, window={window.isActive()}",
        )
        button.clicked.emit()
        self.settings.anonymous_mode = True
        QTest.qWait(250)
        self.assertFalse(dialog.property("visible"))
        self.assertIsNone(window.findChild(QObject, "notificationBanner"))
        self.settings.anonymous_mode = False
        self.center.publish("No update available.", "App updates", direct=True)
        QTest.qWait(250)
        feedback = window.findChild(QObject, "directFeedbackDialog")
        self.assertTrue(feedback.property("visible"))
        self.assertEqual(feedback.property("message"), "No update available.")
        self.assertFalse(dialog.property("visible"))
        feedback.setProperty("visible", False)
        self.center.require_restart()
        QTest.qWait(250)
        self.assertTrue(feedback.property("visible"))
        self.assertIn("Restart Porn Fetch", feedback.property("message"))
        self.assertEqual(warnings, [])
        self.app.sendPostedEvents(None, QEvent.DeferredDelete)

    def test_mobile_system_bridge_is_opt_in_and_uses_generic_payload(self):
        with (
            patch("src.backend.system_notifications.sys.platform", "android"),
            patch.dict(os.environ, {"ANDROID_PRIVATE": self.temporary.name}),
        ):
            notifier = SystemNotifications(self.settings)
        self.addCleanup(notifier.close)
        self.settings.system_notifications = True
        self.settings.sync()
        self.assertTrue(
            SettingsManager(
                QSettings(str(Path(self.temporary.name) / "settings.ini"), QSettings.IniFormat)
            ).system_notifications
        )
        request = Path(self.temporary.name) / "notifications-request.json"
        self.assertEqual(json.loads(request.read_text())["action"], "enable")
        # Exercise actual timer delivery without invoking an OS service.
        inactive_app = SimpleNamespace(applicationState=lambda: Qt.ApplicationInactive)
        with patch("src.backend.system_notifications.QGuiApplication.instance", return_value=inactive_app):
            notifier.request("failed")
            notifier._deliver()
        value = json.loads(request.read_text())
        self.assertEqual(value["action"], "notify")
        self.assertNotIn("http", value["message"])
        self.assertIn("attention", value["message"])
        self.settings.system_notifications = False
        self.assertEqual(json.loads(request.read_text())["action"], "disable")


if __name__ == "__main__":
    unittest.main()
