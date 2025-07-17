from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMessageBox


def ui_popup(text, title="Notice"):
    """A styled UI popup for small messages to the user."""
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setFont(QFont("Segoe UI", 10))

    # Apply custom style sheet
    message_box.setStyleSheet("""
        QMessageBox {
            background-color: #2e2e2e;
            color: white;
            border: 2px solid #4CAF50;
            border-radius: 10px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 6px 12px;
            font-size: 10pt;
            min-width: 80px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QPushButton:pressed {
            background-color: #3e8e41;
        }
    """)

    message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    message_box.exec()