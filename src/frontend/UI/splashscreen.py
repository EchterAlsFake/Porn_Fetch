from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication


class ModernSplashScreen(QWidget):
    def __init__(self, pixmap: QPixmap):
        super().__init__()

        # 1. Window Flags
        # 'SplashScreen' hint tells the OS this is a splash window.
        # 'Frameless' removes the title bar.
        # 'StaysOnTop' keeps it visible.
        self.setWindowFlags(
            Qt.WindowType.SplashScreen |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
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
        # Make text slightly larger/bolder
        font = self._text_label.font()
        font.setPointSize(10)
        self._text_label.setFont(font)
        self._layout.addWidget(self._text_label)

        # Optional: Add a simple progress bar if you want
        # self._progress = QProgressBar()
        # self._progress.setFixedHeight(2)
        # self._progress.setTextVisible(False)
        # self._layout.addWidget(self._progress)

        # Set a fixed size initially (Hyprland might override this, but it's good practice)
        self.resize(600, 400)

        # Set a specific Title for Hyprland Rules
        self.setWindowTitle("PornFetch-Splash")

    def showMessage(self, message, alignment=Qt.AlignmentFlag.AlignBottom, color=Qt.GlobalColor.white):
        """Mimics QSplashScreen.showMessage"""
        self._text_label.setText(message)
        # We process events immediately to ensure text updates on screen
        QApplication.processEvents()

    def finish(self, window):
        """Closes splash when main window is ready"""
        self.close()