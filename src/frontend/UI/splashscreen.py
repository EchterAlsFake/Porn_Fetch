from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPalette, QCursor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication


class ModernSplashScreen(QWidget):
    def __init__(self, pixmap: QPixmap):
        super().__init__()

        # 1. Window Flags
        # REMOVED: Qt.WindowType.WindowStaysOnTopHint (Fixes "Always visible" issue)
        self.setWindowFlags(
            Qt.WindowType.SplashScreen |
            Qt.WindowType.FramelessWindowHint
        )

        # 2. Appearance (Dark Theme)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
        self.setPalette(palette)

        # 3. Layout (Vertical, Centered)
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.setContentsMargins(20, 20, 20, 20)
        self._layout.setSpacing(15)

        # 4. Logo Widget
        self._logo_label = QLabel()
        self._logo_label.setPixmap(pixmap)
        self._logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._logo_label)

        # 5. Text Widget (Status)
        self._text_label = QLabel("Initializing...")
        self._text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self._text_label.font()
        font.setPointSize(10)
        self._text_label.setFont(font)
        self._layout.addWidget(self._text_label)

        self.setWindowTitle("PornFetch-Splash")

        # 6. Critical Fix: Size and Center
        # We set the size first, then move it.
        self.resize(600, 400)
        self.center_on_screen()

    def center_on_screen(self):
        """
        Centers the window on the screen where the cursor currently is.
        """
        # PySide6 Fix: Use QCursor.pos() to find the mouse position
        current_cursor_pos = QCursor.pos()

        # Get the screen where the mouse is
        screen = QApplication.screenAt(current_cursor_pos)

        # Fallback to primary screen if something goes wrong
        if not screen:
            screen = QApplication.primaryScreen()

        # Get available geometry (excludes taskbar)
        screen_geometry = screen.availableGeometry()

        # Calculate center
        center_point = screen_geometry.center()

        # Move the window's geometry to that center
        frame_geometry = self.frameGeometry()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def showMessage(self, message):
        """Mimics QSplashScreen.showMessage"""
        self._text_label.setText(message)
        QApplication.processEvents()

    def finish(self, window):
        """Closes splash when main window is ready"""
        self.close()