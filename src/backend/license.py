import sys

from io import TextIOWrapper
from PySide6.QtWidgets import QWidget
from src.backend.shared_gui import ui_popup
from src.backend.config import shared_config
conf = shared_config


class License(QWidget):
    def __init__(self, ui, this_one_function):
        super().__init__(parent=None)
        conf.read("config.ini")
        self.ui = ui
        self.license_accepted_trigger = this_one_function

    def check_license(self):
        if not conf.get("Setup", "license_accepted") == "true":
            self.button_connections()
            return False

        else:
            return True

    def button_connections(self):
        self.ui.button_accept.clicked.connect(self.license_accepted)
        self.ui.button_deny.clicked.connect(self.license_denied)

    def license_accepted(self):
        conf.set("Setup", "license_accepted", "true")
        with open("config.ini", "w") as config_file:
            conf.write(config_file)

        self.ui.CentralStackedWidget.setCurrentIndex(0)
        self.license_accepted_trigger()

    def license_denied(self):
        conf.set("Setup", "license_accepted", "false")
        with open("config.ini", "w") as config_file: #type: TextIOWrapper
            conf.write(config_file)

        ui_popup("License was not accepted. Exiting...")
        sys.exit(0)


class Disclaimer(QWidget):
    def __init__(self, ui, this_one_function_lol):
        super().__init__(parent=None)
        conf.read("config.ini")
        self.ui = ui
        self.disclaimer_accepted_trigger = this_one_function_lol

    def check_disclaimer(self):
        if not conf.get("Setup", "disclaimer_shown") == "true":
            self.button_connections()
            return False

        else:
            return True

    def button_connections(self):
        self.ui.button_disclaimer_accept.clicked.connect(self.disclaimer_accepted)

    def disclaimer_accepted(self):
        conf.set("Setup", "disclaimer_shown", "true")
        with open("config.ini", "w") as config_file:
            conf.write(config_file)

        self.ui.CentralStackedWidget.setCurrentIndex(0)
        self.disclaimer_accepted_trigger()
