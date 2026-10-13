"""Exercise the targeted filter through Qt's actual logging callbacks."""

import io
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from PySide6.QtCore import QLoggingCategory, qCCritical, qCWarning, qInstallMessageHandler, qWarning

from src.backend import qt_logging

WARNING = (
    "virtual void QtWaylandClient::QWaylandTextInputv3::disableSurface(wl_surface*) "
    "Trying to disable 0x555c58a75f60 but 0x0 is focused"
)


class QtLoggingTests(unittest.TestCase):
    def setUp(self):
        previous = qInstallMessageHandler(None)
        state = patch.multiple(qt_logging, _installed=False, _previous_handler=None)
        state.start()
        self.addCleanup(state.stop)
        self.addCleanup(qInstallMessageHandler, previous)
        self.output = io.StringIO()
        platform = patch.object(qt_logging, "sys", SimpleNamespace(platform="linux", stderr=self.output))
        platform.start()
        self.addCleanup(platform.stop)
        self.category = QLoggingCategory("qt.qpa.wayland.textinput")

    def test_only_unfocused_disable_warning_is_hidden(self):
        qt_logging.install_wayland_message_filter()
        qCWarning(self.category, WARNING)
        self.assertEqual(self.output.getvalue(), "")

        different_focus = WARNING.replace("but 0x0", "but 0x1234")
        qCWarning(self.category, different_focus)
        qWarning("Unrelated QML warning")
        qCCritical(self.category, WARNING)
        other_category = QLoggingCategory("other.category")
        qCWarning(other_category, WARNING)

        output = self.output.getvalue()
        self.assertIn(different_focus, output)
        self.assertIn("Unrelated QML warning", output)
        self.assertIn("other.category: " + WARNING, output)
        self.assertEqual(output.count(WARNING), 2)

    def test_existing_handler_is_preserved_and_installation_is_idempotent(self):
        original = Mock()
        qInstallMessageHandler(original)
        qt_logging.install_wayland_message_filter()
        qt_logging.install_wayland_message_filter()

        qCWarning(self.category, WARNING)
        original.assert_not_called()
        qWarning("Forwarded warning")
        original.assert_called_once()
        self.assertEqual(original.call_args.args[2], "Forwarded warning")
