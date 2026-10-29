from PySide6.QtCore import QObject, Property, Signal, Slot, Qt
from PySide6.QtGui import QGuiApplication, QPalette, QColor
from PySide6.QtQuickControls2 import QQuickStyle
from src.backend.config import app_settings

class ThemeManager(QObject):
    """Manages the UI theme, exposing properties to QML."""

    themeModeChanged = Signal()
    accentColorChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_mode = "Dark" if app_settings.dark_mode else "Light"
        self._accent_color = app_settings.accent_color

        app_settings.darkModeChanged.connect(self._on_settings_mode_changed)
        app_settings.accentColorChanged.connect(self._on_settings_color_changed)
        
        self._update_color_scheme(self._theme_mode == "Dark")

    def _update_color_scheme(self, is_dark: bool):
        app = QGuiApplication.instance()
        if not app:
            return

        try:
            app.styleHints().setColorScheme(Qt.ColorScheme.Dark if is_dark else Qt.ColorScheme.Light)
        except AttributeError:
            pass

        if app_settings.core_style == "Fusion":
            # Explicitly apply QPalette to override platform theme bugs (e.g. xdgdesktopportal ignoring color scheme)
            palette = QPalette()
            if is_dark:
                palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
                palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
                palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
                palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
                palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
                palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
                palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
                palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
                palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
                palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
                palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
                palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
            else:
                palette.setColor(QPalette.ColorRole.Window, QColor(239, 239, 239))
                palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
                palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
                palette.setColor(QPalette.ColorRole.AlternateBase, QColor(247, 247, 247))
                palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
                palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
                palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
                palette.setColor(QPalette.ColorRole.Button, QColor(239, 239, 239))
                palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
                palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
                palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
                palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
                palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
            
            app.setPalette(palette)


    @Slot(bool)
    def _on_settings_mode_changed(self, is_dark: bool):
        self.themeMode = "Dark" if is_dark else "Light"

    @Slot(str)
    def _on_settings_color_changed(self, color: str):
        self.accentColor = color

    # --- Properties exposed to QML ---

    # noinspection PyPropertyDefinition
    @Property(str, notify=themeModeChanged)
    def themeMode(self):
        return self._theme_mode

    @themeMode.setter
    def themeMode(self, mode):
        if self._theme_mode != mode:
            self._theme_mode = mode
            self.themeModeChanged.emit()
            app_settings.dark_mode = (mode == "Dark")
            self._update_color_scheme(mode == "Dark")

    # noinspection PyPropertyDefinition
    @Property(str, notify=accentColorChanged)
    def accentColor(self):
        return self._accent_color

    @accentColor.setter
    def accentColor(self, color):
        if self._accent_color != color:
            self._accent_color = color
            self.accentColorChanged.emit()
            app_settings.accent_color = color

    # noinspection PyPropertyDefinition
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
        app_settings.core_style = style_name