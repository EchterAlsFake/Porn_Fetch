from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtQuickControls2 import QQuickStyle


class ThemeManager(QObject):
    """Manages the UI theme, exposing properties to QML."""

    # Signals to notify QML when a property changes
    themeModeChanged = Signal()
    accentColorChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_mode = "Dark"  # "Dark" or "Light"
        self._accent_color = "#448aff"  # Default blue

    # --- Properties exposed to QML ---

    @Property(str, notify=themeModeChanged)
    def themeMode(self):
        return self._theme_mode

    @themeMode.setter
    def themeMode(self, mode):
        if self._theme_mode != mode:
            self._theme_mode = mode
            self.themeModeChanged.emit()

    @Property(str, notify=accentColorChanged)
    def accentColor(self):
        return self._accent_color

    @accentColor.setter
    def accentColor(self, color):
        if self._accent_color != color:
            self._accent_color = color
            self.accentColorChanged.emit()

    @Property(list, constant=True)
    def availableStyles(self):
        """Returns built-in Qt Quick Controls styles (Basic, Fusion, Material, etc.)"""
        return QQuickStyle.availableStyles()

    # --- Callable Slots ---

    @Slot(str)
    def saveStylePreference(self, style_name):
        """
        Since core styles (Material vs Fusion) must be set before the QML engine starts,
        save the user's choice here (e.g., via QSettings or a JSON file) and apply it
        on the next application launch.
        """
        print(f"Style '{style_name}' saved! Please restart the app to apply.")
        # TODO: Implement your saving logic here