"""Shared window and tray artwork with native small and high-DPI sizes."""

from PySide6.QtGui import QIcon


def application_icon() -> QIcon:
    icon = QIcon(":/images/graphics/logo_transparent.ico")
    icon.addFile(":/images/graphics/logo.png")
    return icon
