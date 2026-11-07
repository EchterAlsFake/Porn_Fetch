from PySide6.QtCore import Property, QObject, Qt, Signal, Slot
from PySide6.QtGui import QColor, QGuiApplication, QPalette
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
        app_settings.accessibilityChanged.connect(self._refresh_palette)
        app_settings.lightThemeBrightnessChanged.connect(self._refresh_palette)
        
        self._update_color_scheme(self._theme_mode == "Dark")

    def _update_color_scheme(self, is_dark: bool):
        app = QGuiApplication.instance()
        if not app:
            return

        try:
            app.styleHints().setColorScheme(Qt.ColorScheme.Dark if is_dark else Qt.ColorScheme.Light)
        except AttributeError:
            pass

        palette = QPalette()
        if app_settings.high_contrast:
            background, foreground = ("#000000", "#ffffff") if is_dark else ("#ffffff", "#000000")
            accent, selected_text = ("#ffff00", "#000000") if is_dark else ("#000080", "#ffffff")
            colors = {
                "Window": background, "WindowText": foreground,
                "Base": background, "AlternateBase": background,
                "ToolTipBase": background, "ToolTipText": foreground,
                "Text": foreground, "Button": background, "ButtonText": foreground,
                "BrightText": foreground, "Link": accent, "LinkVisited": accent,
                "Highlight": accent, "HighlightedText": selected_text,
                "PlaceholderText": foreground,
                "Light": background, "Midlight": background,
                "Mid": foreground, "Dark": foreground, "Shadow": foreground,
            }
        else:
            light_level = round(255 * app_settings.light_theme_brightness / 100)
            light_background = QColor(light_level, light_level, light_level)
            background, foreground = ("#353535", "#ffffff") if is_dark else (light_background, "#000000")
            colors = {
                "Window": background, "WindowText": foreground,
                "Base": "#191919" if is_dark else light_background,
                "AlternateBase": background,
                "ToolTipBase": background, "ToolTipText": foreground,
                "Text": foreground, "Button": background, "ButtonText": foreground,
                "BrightText": "#ff0000", "Link": app_settings.accent_color,
                "Highlight": app_settings.accent_color, "HighlightedText": "#ffffff",
            }
        for role, color in colors.items():
            palette.setColor(getattr(QPalette.ColorRole, role), QColor(color))
        if app_settings.high_contrast:
            disabled = QColor("#b3b3b3" if is_dark else "#555555")
            for role in (QPalette.ColorRole.Text, QPalette.ColorRole.ButtonText, QPalette.ColorRole.WindowText):
                palette.setColor(QPalette.ColorGroup.Disabled, role, disabled)
        app.setPalette(palette)

    @Slot()
    def _refresh_palette(self):
        self._update_color_scheme(app_settings.dark_mode)


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
            self._refresh_palette()

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
