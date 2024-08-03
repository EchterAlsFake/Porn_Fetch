import os
import logging

from PySide6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    message_box = QMessageBox()
    message_box.setText(text)
    message_box.exec()


def get_output_path(path="/storage/emulated/0/Download"):
    """
    Checks if the application can write to a specified directory by attempting to create a test file.
    If the directory does not exist or the file cannot be created, returns False.
    """
    path = path if path.endswith("/") else f"{path}/"
    test_file_path = f"{path}test.txt"

    try:
        if not os.path.exists(path):
            return False

        if os.path.isfile(test_file_path):
            logger.debug("Android output path tests successful")
            return True

        with open(test_file_path, "w") as test_file:
            test_file.write("Test content for permission check.")
        return True

    except Exception as e:
        logger.error(e)
        return False
