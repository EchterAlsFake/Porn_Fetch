"""Render the real desktop UI while switching contrast and color schemes."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ContrastThemeTests(unittest.TestCase):
    def test_live_contrast_schemes_buttons_fields_and_flag_images(self):
        script = r'''
import os
import sys
from pathlib import Path
from PySide6.QtCore import QSettings
QSettings.setDefaultFormat(QSettings.IniFormat)
for scope in (QSettings.UserScope, QSettings.SystemScope):
    QSettings.setPath(QSettings.IniFormat, scope, os.environ['XDG_CONFIG_HOME'])
from src.backend.config import app_settings
app_settings.core_style = sys.argv[1]
app_settings.update_checks = False
app_settings.track_videos = False
app_settings.mark_license_offer_seen()
app_settings.mark_ukraine_message_seen()
app_settings.set_error_reporting_consent(False)
sys.argv = ['main.py', '--smoke-test']
from src.backend import application
from PySide6.QtCore import QMetaObject, QObject, QTimer
from PySide6.QtGui import QImage, QPalette
from PySide6.QtQml import QQmlExpression, QQmlProperty
from unittest.mock import patch

errors = []
cases = iter(((True, True), (False, True), (False, False), (True, False)))
state = {}
single_shot = QTimer.singleShot
def checked(callback):
    def run():
        try:
            callback()
        except Exception as error:
            errors.append(repr(error))
            application.app.quit()
    return run

def next_case():
    try:
        dark, contrast = next(cases)
    except StopIteration:
        verify_flags()
        return
    state.update(dark=dark, contrast=contrast)
    app_settings.dark_mode = dark
    app_settings.high_contrast = contrast
    single_shot(350, checked(verify_case))

def verify_case():
    window = application.engine.rootObjects()[-1]
    dark, contrast = state['dark'], state['contrast']
    button = window.findChild(QObject, 'downloadListButton')
    background = button.findChild(QObject, 'contrastButtonBackground')
    assert background.property('visible') == contrast
    if contrast:
        base, ink, accent, selected = ('#000000', '#ffffff', '#ffff00', '#000000') if dark else (
            '#ffffff', '#000000', '#000080', '#ffffff')
        assert window.property('background').property('color').name() == base
        assert background.property('color').name() == accent
        assert button.property('contentItem').property('color').name() == selected
        ordinary = window.findChild(QObject, 'downloadAdvancedButton')
        assert ordinary.property('contentItem').property('color').name() == ink
        field = window.findChild(QObject, 'videoUrlInput')
        outline = field.findChild(QObject, 'contrastControlOutline')
        assert outline.property('visible') and QQmlProperty.read(outline, 'border.width') >= 2
        stats = window.findChild(QObject, 'statisticsPage')
        assert stats.property('cardColor').name() == base
        assert stats.property('foregroundColor').name() == ink
        assert application.app.palette().color(QPalette.Window).name() == base
        assert application.app.palette().color(QPalette.HighlightedText).name() == selected
    single_shot(30, checked(next_case))

def verify_flags():
    window = application.engine.rootObjects()[-1]
    app_settings.dark_mode = False
    app_settings.high_contrast = True
    combo = window.findChild(QObject, 'contentLanguageComboBox')
    assert combo.property('count') == 14
    assert combo.property('currentText') == 'English'
    assert combo.property('currentValue') == 'en-US'
    image = combo.findChild(QObject, 'selectedContentLanguageFlag')
    assert image.property('source').toString().endswith('/flags/us.svg')
    for code in ('cz', 'de', 'us', 'es', 'ph', 'fr', 'it', 'nl', 'jp', 'pl', 'pt', 'ru', 'ua', 'cn'):
        assert not QImage(':/images/graphics/flags/' + code + '.svg').isNull(), code
    window.findChild(QObject, 'mainNavigation').setProperty('currentIndex', 3)
    expression = QQmlExpression(application.engine.rootContext(), combo, 'popup.open()')
    expression.evaluate()
    assert not expression.hasError(), expression.error().toString()
    single_shot(350, checked(finish))

def finish():
    window = application.engine.rootObjects()[-1]
    combo = window.findChild(QObject, 'contentLanguageComboBox')
    surface = combo.findChild(QObject, 'contrastPopupSurface')
    assert surface.property('visible') and surface.property('color').name() == '#ffffff'
    print('Contrast schemes and flag images verified', flush=True)
    application.app.quit()

single_shot(150, checked(next_case))
def delay_smoke_exit(delay, *args):
    return single_shot(10000 if delay == 250 else delay, *args)
with patch.object(QTimer, 'singleShot', side_effect=delay_smoke_exit):
    application.main()
assert not errors, errors
'''
        root = Path(__file__).resolve().parents[3]
        for style in ("Material", "Fusion"):
            with self.subTest(style=style), tempfile.TemporaryDirectory(prefix="contrast-theme-") as directory:
                env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software",
                           QML_DISABLE_DISK_CACHE="1", XDG_CONFIG_HOME=directory + "/config",
                           XDG_DATA_HOME=directory + "/data", XDG_CACHE_HOME=directory + "/cache")
                env.pop("PORN_FETCH_TEST_ENV", None)
                result = subprocess.run([sys.executable, "-c", script, style], cwd=root, env=env,
                                        capture_output=True, text=True, timeout=25)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Contrast schemes and flag images verified", result.stdout)
                self.assertNotIn("TypeError:", result.stderr)
                self.assertNotIn("ReferenceError:", result.stderr)
