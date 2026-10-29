from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication, QCursor


class SplashController:
    """
    Splashscreen is used to show the loading animation for Porn Fetch on startup.
    This is a DIFFERENT splashscreen from the Nuitka Splashscreen on Windows while unpacking.
    """
    def __init__(self, engine: QQmlApplicationEngine, qml_path: str):
        self.engine = engine
        self.engine.load(QUrl.fromLocalFile(qml_path))

        # Grab the newly created splash window
        self.splash_window = self.engine.rootObjects()[0]
        self.center_on_screen()

    def center_on_screen(self):
        current_cursor_pos = QCursor.pos()
        screen = QGuiApplication.screenAt(current_cursor_pos)
        if not screen:
            screen = QGuiApplication.primaryScreen()

        screen_geometry = screen.availableGeometry()
        window_width = self.splash_window.property("width")
        window_height = self.splash_window.property("height")

        x = screen_geometry.x() + (screen_geometry.width() - window_width) // 2
        y = screen_geometry.y() + (screen_geometry.height() - window_height) // 2

        self.splash_window.setX(x) # type: ignore
        self.splash_window.setY(y) # type: ignore

    def showMessage(self, message: str):
        self.splash_window.setProperty("message", message)
        QGuiApplication.processEvents()

    def finish(self):
        self.splash_window.close() # type: ignore
