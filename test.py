import os
import src.frontend.UI.resources # This may not seem to be used, but it needs to be imported!.
import sys
from pathlib import Path
from src.backend.config import app_settings
from src.backend.theme_manager import ThemeManager

from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtGui import QGuiApplication

from PySide6.QtQml import QQmlApplicationEngine

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Dark"

class Backend(QObject):
    """Dummy backend class to satisfy the required property in QML."""

    def __init__(self):
        super().__init__()

    @Slot(str)
    def test_func(self, msg: str):
        print(f"Backend received: {msg}")


def main():
    app = QGuiApplication(sys.argv)
    app.setOrganizationName("EchterAlsFake")
    app.setApplicationName("Porn Fetch")

    core_style = app_settings.core_style
    is_dark = app_settings.dark_mode
    accent_color = app_settings.accent_color

    # --- 2. Inject Environment Variables for Styles ---
    # QML will read these automatically. No attached properties needed in QML!
    if core_style == "Material":
        os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Dark" if is_dark else "Light"
        os.environ["QT_QUICK_CONTROLS_MATERIAL_ACCENT"] = accent_color
        os.environ["QT_QUICK_CONTROLS_MATERIAL_PRIMARY"] = accent_color
    elif core_style == "Universal":
        os.environ["QT_QUICK_CONTROLS_UNIVERSAL_THEME"] = "Dark" if is_dark else "Light"
        os.environ["QT_QUICK_CONTROLS_UNIVERSAL_ACCENT"] = accent_color

    engine = QQmlApplicationEngine()


    saved_style = app_settings.core_style
    QQuickStyle.setStyle(saved_style)

    # 1. Instantiate backend object
    backend_instance = Backend()

    # 2. Pass backend to QML to satisfy `required property var backend`
    engine.setInitialProperties({"backend": backend_instance})

    theme_manager = ThemeManager()
    # 3. Resolve path to Main.qml relative to this script
    qml_file = Path(__file__).resolve().parent / "src" / "frontend" / "UI"/ "Main.qml"
    engine.rootContext().setContextProperty("themeManager", theme_manager)
    engine.rootContext().setContextProperty("appSettings", app_settings)
    engine.load(QUrl.fromLocalFile(str(qml_file)))

    # 4. Check if QML loaded successfully
    if not engine.rootObjects():
        print("Failed to load QML file.")
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()