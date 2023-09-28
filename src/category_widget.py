from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QRadioButton,
    QCheckBox, QPushButton, QScrollArea, QGroupBox)
from phub import locals


categories = [attr for attr in dir(locals.Category) if
              not callable(getattr(locals.Category, attr)) and not attr.startswith("__")]


class CategoryFilterWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Left Side
        self.radio_buttons = {}
        left_layout = QVBoxLayout()
        left_group = QGroupBox("Select Category")
        for category in categories:
            radio_button = QRadioButton(category)
            left_layout.addWidget(radio_button)
            self.radio_buttons[category] = radio_button
        left_group.setLayout(left_layout)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(left_group)

        # Right Side
        self.checkboxes = {}
        right_layout = QVBoxLayout()
        right_group = QGroupBox("Exclude Categories")
        for category in categories:
            checkbox = QCheckBox(category)
            right_layout.addWidget(checkbox)
            self.checkboxes[category] = checkbox
        right_group.setLayout(right_layout)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(right_group)

        # Apply Button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.on_apply)

        # Main Layout
        hlayout = QHBoxLayout()
        hlayout.addWidget(left_scroll)
        hlayout.addWidget(right_scroll)

        layout.addLayout(hlayout)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def on_apply(self):
        selected_category = None
        excluded_categories = []

        for category, radio_button in self.radio_buttons.items():
            if radio_button.isChecked():
                selected_category = category

        for category, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                excluded_categories.append(category)

        



        # Here you can return or use the selected and excluded categories as needed


# Create the Qt Application
app = QApplication([])

# Create and show the window
window = CategoryFilterWindow()
window.show()

# Run the main Qt loop
app.exec()