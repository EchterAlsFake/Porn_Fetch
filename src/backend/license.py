import sys

from io import TextIOWrapper
from configparser import ConfigParser
from PySide6.QtWidgets import QWidget
from src.backend.shared_gui import ui_popup


class License(QWidget):
    def __init__(self, ui):
        super().__init__(parent=None)
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.ui = ui


    def check_license(self):
        if not self.conf.get("Setup", "license_accepted") == "true":
            self.button_connections()
            return False


        else:
            return True


    def button_connections(self):
        self.ui.button_accept.clicked.connect(self.license_accepted)
        self.ui.button_deny.clicked.connect(self.license_denied)

    def license_accepted(self):
        self.conf.set("Setup", "license_accepted", "true")
        with open("config.ini", "w") as config_file: #type: TextIOWrapper
            self.conf.write(config_file)

        self.ui.CentralStackedWidget.setCurrentIndex(0)

    def license_denied(self):
        self.conf.set("Setup", "license_denied", "false")
        with open("config.ini", "w") as config_file: #type: TextIOWrapper
            self.conf.write(config_file)


        ui_popup("License was not accepted. Exiting...")
        sys.exit(0)


