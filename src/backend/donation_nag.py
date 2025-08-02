import webbrowser

from src.backend.shared_gui import ui_popup
from PySide6.QtWidgets import QApplication, QWidget

from src.backend.config import shared_config
conf = shared_config

class DonationNag(QWidget):
    """
    This displays the Widget for the donation nag that asks the user kindly to donate a little bit
    of money to this project.
    """
    def __init__(self, ui, that_one_function):
        super().__init__()
        conf.read("config.ini")
        self.ui = ui
        self.was_shown_lol = that_one_function

    def check_donation_nag(self):
        if int(conf.get("Sponsoring", "downloaded_videos")) >= 25 and not conf.get("Sponsoring", "notice_shown") == "true":
            conf.set("Sponsoring", "notice_shown", "true")
            with open("config.ini", "w") as configfile:
                conf.write(configfile)

            self.button_connectors()
            return False

        else:
            return True

    def button_connectors(self):
        """Connects the buttons to their functions"""
        self.ui.button_donate_kofi.clicked.connect(self.open_kofi)
        self.ui.button_donate_paypal.clicked.connect(self.open_paypal)
        self.ui.button_donate_copy_xmr.clicked.connect(self.copy_xmr)
        self.ui.button_donate_already_donated.clicked.connect(self.already_donated)
        self.ui.button_donate_close.clicked.connect(self.button_close)

    @staticmethod
    def open_kofi():
        webbrowser.open("https://ko-fi.com/EchterAlsFake")

    @staticmethod
    def open_paypal():
        webbrowser.open("https://paypal.me/EchterAlsFake")

    @staticmethod
    def copy_xmr():
        """Copies the XMR address into the user's clipboard"""
        xmr_address = "42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR"
        QApplication.clipboard().setText(xmr_address)
        ui_popup("XMR address has been copied into your clipboard!")

    def already_donated(self):
        ui_popup("Thank you very much for your donation!")
        self.ui.CentralStackedWidget.setCurrentIndex(0)
        return True

    def button_close(self):
        self.ui.CentralStackedWidget.setCurrentIndex(0)
        return True

# EOF
