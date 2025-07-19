import httpx
import datetime
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


def handle_error_gracefully(self, error_message: str, needs_network_log: bool= False):
    self.logger.error(error_message)

    if not self.supress_errors:
        self.signals.error_signal.emit(error_message)

    if needs_network_log:
        if self.activate_logging:
            self.logger.info(f"Logging Error: {error_message} to network server...")
            message = f"""
            An error occurred in Porn Fetch - [AddToTreeWidget]
            Time: {datetime.datetime.now()}
            Version: {__version__}
            System: {sys.platform}
            Error message: {error_message}
            """

            payload = {"message": message}
            try:
                response = httpx.post(
                url="https://echteralsfake.duckdns.org:443/report",
                json=payload,
                timeout=6)

                if response.status_code == 200:
                    self.logger.info("Successfully reported the Error!")

            except Exception as e:
                self.logger.error(f"Couldn't report the error. Maybe you don't have an IPv6 connection: {e}")