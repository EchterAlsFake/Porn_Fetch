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





