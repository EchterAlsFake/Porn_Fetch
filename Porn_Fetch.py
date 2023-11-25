import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QPoint

# Your existing UI form import
from src.frontend.ui_form import Ui_Porn_Fetch_Widget

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel("Porn Fetch v3.0")
        self.layout.addWidget(self.title)

        self.minimizeButton = QPushButton("_")
        self.minimizeButton.clicked.connect(self.window().showMinimized)
        self.layout.addWidget(self.minimizeButton)

        self.maximizeButton = QPushButton("□")
        self.maximizeButton.clicked.connect(self.toggleMaximizeRestore)
        self.layout.addWidget(self.maximizeButton)

        self.closeButton = QPushButton("X")
        self.closeButton.clicked.connect(self.window().close)
        self.layout.addWidget(self.closeButton)

        # Style omitted for brevity

    def toggleMaximizeRestore(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.maximizeButton.setText("□")  # Or update with an icon for the maximize state
        else:
            self.window().showMaximized()
            self.maximizeButton.setText("❐")  # Or update with an icon for the restore state

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().clickPosition = event.globalPosition().toPoint()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.parent().clickPosition:
            delta = QPoint(event.globalPosition().toPoint() - self.parent().clickPosition)
            self.window().move(self.window().pos() + delta)
            self.parent().clickPosition = event.globalPosition().toPoint()
            event.accept()
        else:
            super().mouseMoveEvent(event)

class Porn_Fetch_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("Porn Fetch v3.0")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.titleBar = CustomTitleBar(self)

        self.ui.HEADER.insertWidget(0, self.titleBar)
        self.clickPosition = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Porn_Fetch_Widget()
    widget.show()
    sys.exit(app.exec())
