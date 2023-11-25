import sys
from PySide6.QtWidgets import QApplication, QWidget

from src.frontend.ui_form import Ui_Porn_Fetch_Widget


class Porn_Fetch_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)

        self.setWindowTitle("Porn Fetch v3.0")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Porn_Fetch_Widget()
    widget.show()
    sys.exit(app.exec())
