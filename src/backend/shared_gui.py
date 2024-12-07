import logging
from PySide6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.exec()
