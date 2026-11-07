"""Offline update presentation; opt in to the native renderer with a display."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class UpdateDialogTests(unittest.TestCase):
    def test_startup_opt_out_and_activity_review_with_long_notes(self):
        script = r'''
import sys
from pathlib import Path
from src.backend.config import app_settings, SettingsManager
app_settings.update_checks = False
app_settings.track_videos = False
app_settings.mark_license_offer_seen()
app_settings.mark_ukraine_message_seen()
app_settings.set_error_reporting_consent(False)
mobile = '--android' in sys.argv
sys.argv = ['main.py', '--smoke-test']
if mobile:
    sys.argv.append('--android')
from src.backend import application
from PySide6.QtCore import QMetaObject, QObject, QSettings, QTimer
from PySide6.QtGui import QFont
from PySide6.QtQuick import QQuickTextDocument
from unittest.mock import patch

errors = []
state = {}
def checked(callback):
    def run():
        try:
            callback()
        except Exception as error:
            errors.append(repr(error))
            application.app.quit()
    return run

def offer():
    window = application.engine.rootObjects()[-1]
    backend = application.engine.rootContext().contextProperty('backend')
    details = dict(version='999.0.0', automatic=True, install_allowed=True,
                   changelog=Path('CHANGELOG_STATIC.md').read_text(), changelog_format='markdown')
    state.update(window=window, backend=backend, details=details,
                 dialog=window.findChild(QObject, 'updateDialog'))
    backend._available_update = details
    backend.updateAvailable.emit(details)
    QTimer.singleShot(600, checked(suppress))

def suppress():
    dialog = state['dialog']
    assert dialog.property('visible'), 'Startup update dialog did not open'
    notes = dialog.findChild(QObject, 'updateChangelogText')
    assert len(notes.property('text')) > 2000
    assert notes.property('readOnly') and notes.property('selectByMouse')
    quick_document = notes.property('textDocument')
    document = quick_document.textDocument()
    assert document.firstBlock().blockFormat().headingLevel() == 1, 'Markdown heading was lost'
    assert document.find('Added RedTube').block().textList(), 'Markdown list was lost'
    assert document.find('Cleanup on stop').charFormat().fontWeight() >= QFont.Bold, 'Markdown bold was lost'
    link = document.find('development checklist').charFormat()
    assert link.isAnchor() and link.anchorHref() == 'https://pornfetch.to/checklist', 'Markdown link was lost'
    if not mobile:
        assert dialog.findChild(QObject, 'installUpdateButton').property('text') == 'Update now'
    assert not dialog.findChild(QObject, 'updateReleasesButton')
    app_settings.update_prompts = False
    restored = SettingsManager(QSettings(app_settings._settings.fileName(), QSettings.IniFormat))
    assert not restored.update_prompts, 'Opt-out did not persist'
    assert dialog.findChild(QObject, 'hideUpdatePromptsCheckBox').property('checked')
    QMetaObject.invokeMethod(dialog, 'close')
    QTimer.singleShot(500, checked(offer_again))

def offer_again():
    state['backend'].updateAvailable.emit(state['details'])
    QTimer.singleShot(500, checked(open_activity))

def open_activity():
    assert not state['dialog'].property('visible'), 'Suppressed startup dialog reopened'
    if mobile:
        state['backend'].review_update()
        QTimer.singleShot(600, checked(verify_review))
        return
    state['backend'].notifications.publish('Version 999.0.0 is available.', action='updates')
    state['window'].findChild(QObject, 'recentActivityButton').clicked.emit()
    QTimer.singleShot(500, checked(review))

def review():
    activity = state['window'].findChild(QObject, 'recentActivityDialog')
    assert activity.property('visible')
    def walk(item):
        yield item
        for child in item.childItems():
            yield from walk(child)
    content = activity.findChild(QObject, 'recentActivityList').property('contentItem')
    buttons = [item for item in walk(content)
               if item.property('text') == 'Review update' and hasattr(item, 'clicked')]
    assert len(buttons) == 1, 'Missing activity review action'
    buttons[0].clicked.emit()
    QTimer.singleShot(600, checked(verify_review))

def verify_review():
    assert state['dialog'].property('visible'), 'Manual review must ignore the startup opt-out'
    if not mobile:
        assert not state['window'].findChild(QObject, 'recentActivityDialog').property('visible')
    state['backend'].updateAvailable.emit(dict(state['details'], automatic=False, changelog_format='html',
        changelog='<h2>Legacy notes</h2><ul><li><b>Fixed updates</b></li></ul>'))
    QTimer.singleShot(600, checked(verify_html))

def verify_html():
    notes = state['dialog'].findChild(QObject, 'updateChangelogText')
    quick_document = notes.property('textDocument')
    document = quick_document.textDocument()
    assert document.firstBlock().blockFormat().headingLevel() == 2, 'HTML heading was lost'
    fixed = document.find('Fixed updates')
    assert fixed.block().textList() and fixed.charFormat().fontWeight() >= QFont.Bold
    print('Update dialog verified', flush=True)
    application.app.quit()

single_shot = QTimer.singleShot
single_shot(100, checked(offer))
def delay_smoke_exit(delay, *args):
    return single_shot(10000 if delay == 250 else delay, *args)
with patch.object(QTimer, 'singleShot', side_effect=delay_smoke_exit):
    application.main()
assert not errors, errors
'''
        root = Path(__file__).resolve().parents[3]
        for layout in ('desktop', 'mobile'):
            with self.subTest(layout=layout), tempfile.TemporaryDirectory(prefix="update-dialog-") as directory:
                self.run_dialog(script, root, directory, layout)

    def run_dialog(self, script, root, directory, layout):
        env = dict(os.environ, XDG_CONFIG_HOME=directory + "/config",
                   XDG_DATA_HOME=directory + "/data", XDG_CACHE_HOME=directory + "/cache")
        env.pop("PORN_FETCH_TEST_ENV", None)
        env["QML_DISABLE_DISK_CACHE"] = "1"
        if os.environ.get("PORNFETCH_NATIVE_UPDATE_TEST") == "1":
            env.pop("QT_QPA_PLATFORM", None)
            env.pop("QT_QUICK_BACKEND", None)
        else:
            env.update(QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software")
        command = [sys.executable, "-X", "faulthandler", "-c", script]
        if layout == 'mobile':
            command.append('--android')
        result = subprocess.run(command,
                                cwd=root, env=env, capture_output=True, text=True, timeout=25)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Update dialog verified", result.stdout)
        self.assertNotIn("TypeError:", result.stderr)
        self.assertNotIn("ReferenceError:", result.stderr)
