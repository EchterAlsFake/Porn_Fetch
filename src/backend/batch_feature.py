"""
Disclaimer:

This feature is for personal backup purposes and not to mass-redistribute videos (even if free) from other
sites. I am not liable for any damages caused by this. You, the user, have been informed to NOT misuse this.

You are responsible for your actions.
"""

from src.frontend.UI.ui_form_batch import Ui_Batch
from PySide6.QtWidgets import QWidget

class Batch(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Batch()
        self.ui.setupUi(self)
        self.show()


