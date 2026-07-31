"""
Contains the theme for Porn Fetch's main UI using qt-material.
"""
import qt_material

from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtWidgets import (QApplication, QComboBox, QListView, QFrame, QWidget, QLineEdit, QTextEdit, QSpinBox,
                               QDoubleSpinBox, QAbstractButton, QPlainTextEdit)

# All available qt-material themes
MATERIAL_THEMES = qt_material.list_themes()


def get_theme_display_name(xml_filename: str) -> str:
    """Converts a theme XML filename like 'dark_blue.xml' or 'light_pink_500.xml' into a readable display name."""
    name = xml_filename.replace(".xml", "")
    parts = name.split("_")
    return " ".join([p.capitalize() for p in parts])


THEME_DISPLAY_NAMES = [get_theme_display_name(t) for t in MATERIAL_THEMES]


def get_theme_filename(theme_spec) -> str:
    """Resolves a theme specification (integer index, XML filename, or display name) to an XML theme filename."""
    if isinstance(theme_spec, int):
        if 0 <= theme_spec < len(MATERIAL_THEMES):
            return MATERIAL_THEMES[theme_spec]
        return MATERIAL_THEMES[0]
    if isinstance(theme_spec, str):
        if theme_spec in MATERIAL_THEMES:
            return theme_spec
        if theme_spec.isdigit():
            idx = int(theme_spec)
            if 0 <= idx < len(MATERIAL_THEMES):
                return MATERIAL_THEMES[idx]
        for t in MATERIAL_THEMES:
            if get_theme_display_name(t).lower() == theme_spec.lower():
                return t
    return MATERIAL_THEMES[0]


def get_theme_colors(theme_spec) -> dict:
    """
    Returns a dictionary of colors and metadata for the specified theme.
    Used by QML Material UI to synchronize accent, primary, background, and foreground colors.
    """
    theme_file = get_theme_filename(theme_spec)
    theme_dict = qt_material.get_theme(theme_file)
    is_dark = theme_file.startswith("dark")

    primary = theme_dict.get("primaryColor", "#448aff")
    secondary = theme_dict.get("secondaryColor", "#232629" if is_dark else "#f5f5f5")
    primary_text = theme_dict.get("primaryTextColor", "#ffffff" if is_dark else "#111827")
    secondary_text = theme_dict.get("secondaryTextColor", "#a0a0a0" if is_dark else "#555555")

    return {
        "theme_file": theme_file,
        "is_dark": is_dark,
        "primary": primary,
        "background": secondary,
        "foreground": primary_text,
        "secondary_text": secondary_text
    }


def apply_theme(app: QApplication, theme_spec=0, extra=""):
    """
    Applies the chosen qt-material theme to the QApplication.
    `theme_spec` can be an integer index (0..25), XML filename, or display name.
    """
    theme_file = get_theme_filename(theme_spec)
    qt_material.apply_stylesheet(app, theme=theme_file, extra=extra)


def apply_theme_light(app: QApplication):
    """Convenience helper to apply a light theme."""
    apply_theme(app, "light_blue.xml")


def mark(w, *, intent=None, size=None, flat=False, seg=False, role=None):
    if intent: w.setProperty("intent", intent)
    if size: w.setProperty("size", size)
    if flat: w.setProperty("appearance", "flat")
    if seg: w.setProperty("seg", "1")
    if role: w.setProperty("role", role)
    w.style().unpolish(w); w.style().polish(w)


def pretty_combo(combo: QComboBox):
    view = QListView()
    view.setSpacing(6)
    view.setFrameShape(QFrame.Shape.NoFrame)
    combo.setView(view)


def outline(widget, mode="accent"):
    widget.setProperty("highlight", mode)
    widget.style().unpolish(widget); widget.style().polish(widget)


class FocusOutlineFilter(QObject):
    def eventFilter(self, obj: QObject, ev: QEvent) -> bool:
        et = ev.type()
        keyboard_reasons = {Qt.FocusReason.TabFocusReason, Qt.FocusReason.BacktabFocusReason,
                            Qt.FocusReason.ShortcutFocusReason}
        if et == QEvent.Type.FocusIn:
            try:
                reason = ev.reason()
            except Exception:
                reason = Qt.FocusReason.OtherFocusReason
            obj.setProperty("kbd", "1" if reason in keyboard_reasons else "0")
            _repolish(obj)
        elif et == QEvent.Type.FocusOut:
            obj.setProperty("kbd", "0")
            _repolish(obj)
        return False


def _repolish(w: QObject):
    if isinstance(w, QWidget):
        w.setStyleSheet(w.styleSheet())
        w.style().unpolish(w)
        w.style().polish(w)
        w.update()


def install_focus_outline(root: QWidget):
    """Attach to all interactive widgets now (call again after dynamic UI changes)."""
    filter = FocusOutlineFilter(root)
    root._focus_outline_filter = filter
    classes = [QLineEdit, QComboBox, QTextEdit, QPlainTextEdit,
               QSpinBox, QDoubleSpinBox, QAbstractButton]
    for cls in classes:
        for w in root.findChildren(cls):
            w.installEventFilter(filter)