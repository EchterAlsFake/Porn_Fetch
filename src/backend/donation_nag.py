import webbrowser

from src.backend.shared_gui import ui_popup
from PySide6.QtWidgets import QApplication, QWidget


class DonationNag(QWidget):
    """
    This displays the Widget for the donation nag that asks the user kindly to donate a little bit
    of money to this project.
    """
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.button_connectors()

    def button_connectors(self):
        """Connects the buttons to their functions"""
        self.ui.button_donate_kofi.clicked.connect(self.open_kofi)
        self.ui.button_donate_paypal.clicked.connect(self.open_paypal)
        self.ui.button_donate_copy_xmr.clicked.connect(self.copy_xmr)
        self.ui.button_donate_already_donated.clicked.connect(self.already_donated)

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

    @staticmethod
    def already_donated():
        ui_popup("Thank you very much for your donation!")

# EOF
