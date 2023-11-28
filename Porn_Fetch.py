import os.path
import sys
import requests

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QCheckBox, QPushButton,
                               QScrollArea, QGroupBox, QApplication, QMessageBox, QInputDialog, QFileDialog)

from PySide6.QtCore import QFile, QTextStream, Signal
from PySide6.QtGui import QIcon
from configparser import ConfigParser

from src.frontend.ui_form import Ui_Porn_Fetch_Widget
from src.frontend.License import Ui_License
from src.frontend import ressources_rc  # This is needed for the Stylesheet and Icons
from phub import Quality, Client, locals, errors

categories = [attr for attr in dir(locals.Category) if
              not callable(getattr(locals.Category, attr)) and not attr.startswith("__")]


def ui_popup(text):
    """ A simple UI popup that will be used for small messages to the user."""
    qmsg_box = QMessageBox()
    qmsg_box.setText(text)
    qmsg_box.exec()

def show_get_text_dialog(self, title, text):
    name, ok = QInputDialog.getText(self, f'{title}', f'{text}:')
    if ok:
        return name


class License(QWidget):
    """ License class to display the GPL 3 License to the user."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_widget = None
        self.conf = ConfigParser()
        self.conf.read("config.ini")

        self.ui = Ui_License()
        self.ui.setupUi(self)
        self.ui.button_accept.clicked.connect(self.accept)
        self.ui.button_deny.clicked.connect(self.denied)

    def check_license_and_proceed(self):
        if self.conf["License"]["accept"] == "true":
            self.show_main_window()

        else:
            self.show()  # Show the license widget

    def accept(self):
        self.conf.set("License", "accept", "true")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()

        self.show_main_window()

    def denied(self):
        self.conf.set("License", "accept", "false")
        with open("config.ini", "w") as config_file:
            self.conf.write(config_file)
            config_file.close()
            self.close()
            sys.exit(0)

    def show_main_window(self):
        """ If license was accepted, the License widget is closed and the main widget will be shown."""
        self.close()
        self.main_widget = PornFetch()
        self.main_widget.show()


class CategoryFilterWindow(QWidget):
    data_selected = Signal((str, list))

    def __init__(self, categories):
        super().__init__()
        self.excluded_categories = None
        self.selected_category = None
        self.radio_buttons = {}
        self.checkboxes = {}
        self.categories = categories

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        left_group = QGroupBox("Select Category")

        for category in self.categories:
            radio_button = QRadioButton(category)
            left_layout.addWidget(radio_button)
            self.radio_buttons[category] = radio_button

        left_group.setLayout(left_layout)

        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setWidget(left_group)

        right_layout = QVBoxLayout()
        right_group = QGroupBox("Exclude Categories")

        for category in self.categories:
            checkbox = QCheckBox(category)
            right_layout.addWidget(checkbox)
            self.checkboxes[category] = checkbox

        right_group.setLayout(right_layout)

        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_scroll.setWidget(right_group)

        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.on_apply)

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

        self.selected_category = selected_category
        self.excluded_categories = excluded_categories
        self.data_selected.emit(self.selected_category, self.excluded_categories)
        self.close()


class PornFetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Variable initialization:

        self.selected_category = None
        self.excluded_categories_filter = None
        self.client = None
        self.api_language = None
        self.delay = None
        self.search_limit = None
        self.semaphore_limit = None
        self.quality = None
        self.output_path = None
        self.threading_mode = None
        self.threading = None

        # UI relevant initialization:
        self.ui = Ui_Porn_Fetch_Widget()
        self.ui.setupUi(self)
        self.button_connectors()
        self.load_icons()

    def load_icons(self):
        """a simple function to load the icons for the buttons"""
        self.ui.button_switch_search.setIcon(QIcon(":/images/graphics/search.svg"))
        self.ui.button_switch_home.setIcon(QIcon(":/images/graphics/download.svg"))
        self.ui.button_switch_settings.setIcon(QIcon(":/images/graphics/settings.svg"))
        self.ui.button_switch_credits.setIcon(QIcon(":/images/graphics/information.svg"))
        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))

    def button_connectors(self):
        """a function to link the buttons to their functions"""

        # Menu Bar Switch Button Connections
        self.ui.button_switch_home.clicked.connect(self.switch_to_home)
        self.ui.button_switch_search.clicked.connect(self.switch_to_search)
        self.ui.button_switch_settings.clicked.connect(self.switch_to_settings)
        self.ui.button_switch_credits.clicked.connect(self.switch_to_credits)
        self.ui.button_login.clicked.connect(self.select_output_path)

        # Video Download Button Connections

    def switch_to_home(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(0)

    def switch_to_search(self):
        self.ui.stacked_widget_main.setCurrentIndex(0)
        self.ui.stacked_widget_top.setCurrentIndex(1)

    def switch_to_settings(self):
        self.ui.stacked_widget_main.setCurrentIndex(1)

    def switch_to_credits(self):
        self.ui.stacked_widget_main.setCurrentIndex(2)

    """
    The following are functions used by different other functions to handle data over different classes / threads.
    Mostly by using signals and slot connectors. I don't recommend anyone to change stuff here!
    (It's already complicated enough, even with the Documentation)
    """

    def handle_selected_data(self, selected_category, excluded_categories):
        """
        Receives the selected and excluded categories from the Category class. Needed for video searching.
        """
        self.selected_category = selected_category
        self.excluded_categories_filter = excluded_categories

    def search_videos(self):
        """I don't know how this function even works. Ask ChatGPT about it. No joke, I don't understand it."""
        include_filters = []
        exclude_filters = []

        filter_objects = {
            'include': [self.selected_category],
            'exclude': [self.excluded_categories_filter]
        }

        for action, filters in filter_objects.items():
            for filter_object in filters:
                if isinstance(filter_object, locals.Param):
                    if action == 'include':
                        include_filters.append(filter_object)
                    elif action == 'exclude':
                        exclude_filters.append(filter_object)
                else:
                    print(f"Invalid filter")

        if include_filters:
            combined_include_filter = include_filters[0]
            for filter_object in include_filters[1:]:
                combined_include_filter |= filter_object
        else:
            combined_include_filter = None

        if exclude_filters:
            combined_exclude_filter = exclude_filters[0]
            for filter_object in exclude_filters[1:]:
                combined_exclude_filter -= filter_object
        else:
            combined_exclude_filter = None

        query = self.ui.lineedit_search_query.text()

        if combined_include_filter and combined_exclude_filter:
            final_filter = combined_include_filter - combined_exclude_filter
            query_object = self.client.search(query, final_filter)
        elif combined_include_filter:
            query_object = self.client.search(query, combined_include_filter)
        elif combined_exclude_filter:
            query_object = self.client.search(query, -combined_exclude_filter)
        else:
            query_object = self.client.search(query)

    def get_quality(self):
        """Returns the quality selected by the user"""
        if self.ui.radio_quality_best.isChecked():
            self.quality = Quality.BEST

        elif self.ui.radio_quality_half.isChecked():
            self.quality = Quality.HALF

        elif self.ui.radio_quality_worst.isChecked():
            self.quality = Quality.WORST

    def get_api_language(self):
        """Returns the API Language. Will be used by the API to return correct video titles etc..."""
        if self.ui.radio_api_language_custom.isChecked():
            language = show_get_text_dialog(title="API Language", text="""
            Please enter the language code for your language.  Example: en, de, fr, ru --=>:""")
            self.api_language = language

        elif self.ui.radio_api_language_chinese.isChecked():
            self.api_language = "zh"

        elif self.ui.radio_api_language_english.isChecked():
            self.api_language = "en"

        elif self.ui.radio_api_language_french.isChecked():
            self.api_language = "fr"

        elif self.ui.radio_api_language_german.isChecked():
            self.api_language = "de"

        elif self.ui.radio_api_language_russian.isChecked():
            self.api_language = "ru"

    def get_output_path(self):
        output_path = self.ui.lineedit_output_path.text()
        if not os.path.exists(output_path):
            ui_popup("The specified output path doesn't exist. If you think, this is an error, please report it!")

        else:
            self.output_path = output_path

    def select_output_path(self):
        directory = QFileDialog.getExistingDirectory()
        if os.path.exists(directory):  # Should always be the case hopefully
            self.ui.lineedit_output_path.setText(directory)
            self.output_path = directory

    def get_semaphore_limit(self):
        value = self.ui.spinbox_semaphore.value()
        if value >= 1:
            self.semaphore_limit = value

    def get_threading_mode(self):
        if self.ui.radio_threading_mode_default.isChecked():
            self.threading_mode = 0

        elif self.ui.radio_threading_mode_ffmpeg.isChecked():
            self.threading_mode = 1

        elif self.ui.radio_threading_mode_high_performance.isChecked():
            self.threading_mode = 2

    def get_threading(self):
        if self.ui.radio_threading_yes.isChecked():
            self.threading = True

        elif self.ui.radio_threading_no.isChecked():
            self.threading = False

    def get_search_limit(self):
        search_limit = self.ui.spinbox_searching.value() if self.ui.spinbox_searching.value() >= 1 else 50
        self.search_limit = search_limit

    def update_settings(self):
        self.get_threading()
        self.get_search_limit()
        self.get_threading_mode()
        self.get_quality()
        self.get_api_language()
        self.get_output_path()
        self.get_semaphore_limit()

    def load_user_settings(self):
        """Loads the user settings from the configuration file and applies them"""















def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        """
        I had many problems with coding in general where something didn't work but the translations are the hardest
        thing I've ever done. Now where I've understand it it makes sense but the Qt documentation is a piece of shit...
        """

        """# Obtain the system's locale
        locale = QLocale.system()
        # Get the language code (e.g., "de" for German)
        language_code = locale.name().split('_')[0]
        # Construct the path to the translation file
        path = f":/translations/translations/{language_code}.qm"

        translator = QTranslator(app)
        if translator.load(path):
            logging(f"{language_code} translation loaded")
            app.installTranslator(translator)
        else:
            logging(f"Failed to load {language_code} translation")
        """
        file = QFile(":/style/stylesheet.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

        widget = License()  # Starts License widget and checks if license was accepted.
        widget.check_license_and_proceed()

    except PermissionError:
        ui_popup("Insufficient Permissions to access something. Please run Porn Fetch as root / admin")

    except ConnectionResetError:
        ui_popup("Connection was reset. Are you connected to a public wifi or a university's wifi? ")
    except ConnectionError:
        ui_popup("Connection Error, please make sure you have a stable internet connection")

    except KeyboardInterrupt:
        sys.exit(0)

    except requests.exceptions.SSLError:
        ui_popup("SSLError: Your connection is blocked by your ISP / IT administrator (Firewall). If you are in a "
                 "University or at school, please connect to a VPN / Proxy")

    except TypeError:
        pass

    except OSError as e:
        ui_popup(f"This error shouldn't happen. If you still see it it's REALLY important that you report the "
                 f"following: {e}")

    except ZeroDivisionError:
        pass

    sys.exit(app.exec())


if __name__ == "__main__":
    main()