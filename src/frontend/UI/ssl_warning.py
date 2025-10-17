from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt


class SSLWarningDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SSL Verification Warning")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        warning_text = (
            "<b>Your proxy does not support proper SSL verification.</b><br><br>"
            "The only way to bypass this is to <b>disable SSL certificate verification</b> completely.<br><br>"
            "<b>⚠ This is a serious security risk.</b><br>"
            "Disabling SSL verification may expose your connection to man-in-the-middle (MITM) attacks, "
            "data interception, or spoofed websites.<br><br>"
            "Do you want to proceed and disable SSL verification?"
        )

        label = QLabel(warning_text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(label)

        # Button layout
        button_layout = QHBoxLayout()
        self.accept_btn = QPushButton("Accept (Disable SSL Verification)")
        self.cancel_btn = QPushButton("Cancel")
        button_layout.addStretch()
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        self.accept_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)