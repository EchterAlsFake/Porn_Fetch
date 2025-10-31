import sys
import datetime as dt

from PySide6.QtCore import Qt
from typing import Optional, Dict
from src.backend.config import __version__
from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QTextEdit, QDialogButtonBox


class FeedbackDialog(QDialog):
    """Modal dialog to collect user feedback text."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Send Feedback")
        self.setWindowModality(Qt.ApplicationModal)
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        prompt = QLabel("Please describe what happened or share your feedback:")
        prompt.setWordWrap(True)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Type your feedback here...")
        self.text_edit.textChanged.connect(self._sync_ok_enabled)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        self.ok_btn = buttons.button(QDialogButtonBox.Ok)
        self.ok_btn.setText("Submit")
        self.ok_btn.setEnabled(False)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)

        layout.addWidget(prompt)
        layout.addWidget(self.text_edit)
        layout.addWidget(buttons)

        self._sync_ok_enabled()

    def _sync_ok_enabled(self) -> None:
        self.ok_btn.setEnabled(bool(self.text_edit.toPlainText().strip()))

    def feedback_text(self) -> str:
        return self.text_edit.toPlainText().strip()


def ask_for_feedback_and_report(
    *,
    version: Optional[str] = None,
    report_url: str = "https://echteralsfake.duckdns.org:443/report",
    timeout: int = 20,
    parent=None,
) -> Optional[Dict[str, str]]:
    """
    Shows a modal dialog to collect feedback. If the user cancels or closes the dialog,
    returns None and does not send anything. If they submit text, builds the message
    exactly per your structure, posts it to `report_url`, and returns the payload dict.

    Parameters
    ----------
    version : str | None
        App version string to include in the message; falls back to global __version__.
    report_url : str
        Endpoint to POST the payload to.
    timeout : int
        httpx timeout in seconds.
    parent :
        Optional Qt parent widget.

    Returns
    -------
    dict | None
        The payload dict if submitted; None if the dialog was cancelled.
    """
    app = QApplication.instance()
    created_app = False
    if app is None:
        app = QApplication(sys.argv)
        created_app = True

    dlg = FeedbackDialog(parent)
    if dlg.exec() != QDialog.Accepted:
        # User cancelled or closed the dialog: do nothing.
        return None

    error_message = dlg.feedback_text()
    ver = version if version is not None else __version__

    message = f"""
[Feedback Report]
Time: {dt.datetime.now()}
Version: {ver}
System: {sys.platform}
Feedback: {error_message}
""".strip()

    payload = {"message": message}

    return payload