"""
The functions and classes in this file are only used once in the GUI and I'll probably never ever need
to touch them again, which is why I am outsourcing them here, so that the project just gets smaller and my CPU
needs less Monster Energy to process the code.
"""

import logging

from src.frontend.UI import resources
from src.backend.shared_gui import ui_popup
from eporner_api import Category as ep_Category
from src.backend.shared_functions import setup_config_file, setup_logger
from PySide6.QtCore import QFile, QCoreApplication, QTextStream


logger = setup_logger("Porn Fetch - [one_time_functions.py]", log_file="PornFetch.log", level=logging.DEBUG, http_ip=None, http_port=None)
logger.setLevel(logging.DEBUG)



def load_stylesheet(path):
    """Load stylesheet from a given path with explicit open and close."""
    file = QFile(path)
    if not file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
        logger.error(f"Failed to open stylesheet.qss: {file.errorString()}")
        return ""
    stylesheet = QTextStream(file).readAll()
    file.close()
    return stylesheet


def reset_pornfetch():
    setup_config_file(force=True)
    ui_popup(QCoreApplication.translate("main", "Done! Please restart.", None))

def switch_login_button_state(self):
    """If the user is logged in, I'll change the stylesheets of the buttons"""
    file = ":/style/stylesheets/stylesheet_switch_buttons_login_state.qss"
    stylesheet = load_stylesheet(file)

    self.ui.login_button_get_liked_videos.setStyleSheet(stylesheet)
    self.ui.login_button_get_watched_videos.setStyleSheet(stylesheet)
    self.ui.login_button_get_recommended_videos.setStyleSheet(stylesheet)
