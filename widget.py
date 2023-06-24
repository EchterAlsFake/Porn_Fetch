import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from ui_form import Ui_Widget
from phub import Client, Quality
import os
import wget
from configparser import ConfigParser
from colorama import *

data = """
[ui]
mode = native
"""


def config_file():
    if not os.path.isfile("config.ini"):
        with open("config.ini", "w") as f:
            f.write(data)


def character_stripping(title):
    disallowed_characters = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]
    for char in disallowed_characters:
        title = title.replace(char, "")

    title = str(title).lower()
    title = str(title).encode("utf-8")
    return title


def ui_popup():
    qmsg_box = QMessageBox()
    qmsg_box.setText("Successfully applied :) ")
    qmsg_box.exec()


class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.video = None
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.conf = ConfigParser()
        self.conf.read("config.ini")
        self.client = Client(language="en")

        self.ui.button_start.clicked.connect(self.start)
        self.ui.button_start_file.clicked.connect(self.url_testing)
        self.ui.button_get_metadata.clicked.connect(self.get_metadata)
        self.ui.radio_dark.clicked.connect(self.set_dark)
        self.ui.radio_white.clicked.connect(self.set_white)
        self.ui.radio_native.clicked.connect(self.set_native)

    def reset_ui(self):
        self.ui.progressbar_download.setValue(0)
        self.ui.lineedit_url.clear()
        self.ui.lineedit_url_file.clear()
        self.ui.lineedit_title.clear()
        self.ui.lineedit_author.clear()
        self.ui.lineedit_date.clear()
        self.ui.lineedit_duration.clear()
        self.ui.lineedit_hotspots.clear()
        self.ui.lineedit_views.clear()

    def set_dark(self):

        self.conf.set("ui", "mode", "dark")
        with open("config.ini", "w") as config:
            self.conf.write(config)
            ui_popup()
            config.close()

    def set_white(self):

        self.conf.set("ui", "mode", "white")
        with open("config.ini", "w") as config:
            self.conf.write(config)
            ui_popup()
            config.close()

    def set_native(self):

        self.conf.set("ui", "mode", "native")
        with open("config.ini", "w") as config:
            self.conf.write(config)
            ui_popup()
            config.close()

    def get_quality(self):

        if self.ui.radio_highest.isChecked():
            quality = Quality.BEST

        elif self.ui.radio_middle.isChecked():
            quality = Quality.MIDDLE

        elif self.ui.radio_lowest.isChecked():
            quality = Quality.WORST

        else:
            qmsg_box = QMessageBox()
            qmsg_box.setText("No Quality selected..  Using best automatically ")
            qmsg_box.exec()
            quality = Quality.BEST

        return quality

    def callback(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def start(self):

        url = self.ui.lineedit_url.text()
        self.download(url)

    def download(self, url):

        if self.test_video(url):

            quality = self.get_quality()
            output = self.ui.lineedit_output.text()

            if not os.path.exists(output):
                qmsg_box = QMessageBox()
                string = """The output path you entered is not valid! Please note, that you also need to include slashes
                         For an example:  A valid path would be:  /home/USERNAME/videos/, but not /home/USERNAME/videos  
                         as there is missing the slash. Thanks :)."""
                qmsg_box.setText(string)
                qmsg_box.exec()

            else:
                title = self.video.title
                title = character_stripping(title=title)
                final_output = str(output) + str(title) + ".mp4"
                print(f"""
[DEBUG] {Fore.LIGHTCYAN_EX}
{Fore.LIGHTGREEN_EX}Downloading: {title}
{Fore.LIGHTYELLOW_EX}Location: {final_output}
{Fore.LIGHTMAGENTA_EX}Quality: {quality}""")

                self.video.download(quality=quality, path=final_output, quiet=True, callback=self.callback)
                if os.path.exists(final_output):
                    print(f"""
{Fore.LIGHTCYAN_EX} Successfully downloaded""")

    def url_testing(self):

        url_file = self.ui.lineedit_url_file.text()
        if not os.path.isfile(url_file):

            qmsg_box = QMessageBox()
            qmsg_box.setText(f"Could not find: {url_file}.  Please try again....")
            qmsg_box.exec()

        else:

            with open(url_file, "r") as f:
                content = f.read().splitlines()
                qmsg_box = QMessageBox()
                qmsg_box.exec()
                current = 0
                valid_urls = []
                invalid_urls = []
                for url in content:
                    current += 1
                    length = len(content)
                    text = f"Testing {current} of {length} URLs....  Please wait "

                    if self.test_video(url):
                        qmsg_box.exec().setText(str(text))
                        valid_urls.append(url)

                    else:
                        print(f"Error with: {url}")
                        invalid_urls.append(url)

                qmsg_box.close()
                qmsg_box = QMessageBox()
                qmsg_box.setText(f"Valid URLs: {len(valid_urls)} : Invalid URLs: {len(invalid_urls)}")
                qmsg_box.exec()

                for url in valid_urls:
                    self.download(url)

    def test_video(self, url):

        try:

            self.video = self.client.get(url=str(url))
            return True

        except Exception as e:
            qmsg = QMessageBox()
            qmsg.setText("The URL you entered is not valid. ERROR: " + str(e))
            qmsg.exec()
            x = "WW"  # Just don't ask ;)
            return x

    def get_metadata(self):

        url = self.ui.lineedit_url.text()
        if self.test_video(url):

            title = self.video.title
            duration = self.video.duration
            hotspots = self.video.hotspots
            date = self.video.date
            author = self.video.author

            duration = duration / 60
            str(duration).strip(":")
            str(duration).strip("0")

            self.ui.lineedit_title.setText(str(title))
            self.ui.lineedit_duration.setText(str(duration) + str(" minutes"))
            self.ui.lineedit_date.setText(str(date))
            self.ui.lineedit_author.setText(str(author))
            self.ui.lineedit_hotspots.setText(str(hotspots))

        elif self.test_video(url) == "WW":
            pass

        else:
            qmsg_box = QMessageBox()
            qmsg_box.setText("Unknown Error.  Please still report it and give me the URL you used. Thansk :) ")
            qmsg_box.exec()

    def get_thumbnail(self):

        title = self.video.title
        url = self.video.image_url
        output = self.ui.lineedit_output.text()
        final_output = output + title + ".jpg"

        try:
            wget.download(url, out=final_output)

            if os.path.exists(final_output):
                print("Downloaded Thumbnail :)")
                qmsg_box = QMessageBox()
                qmsg_box.setText("Thumbnail downloaded successfully :)")
                qmsg_box.exec()

            else:

                qmsg_box = QMessageBox()
                qmsg_box.setText(
                            """There was an error. Maybe the thumbnail downloaded successfully, but the title is weird, 
                            and program can't find it. Just search for it :)""")
                qmsg_box.exec()

        except Exception as e:

            qmsg_box = QMessageBox()
            qmsg_box.setText("Unhandled Error: " + str(e))
            qmsg_box.exec()


def set_dark_theme():
    palette = QPalette()

    # Set colors for different roles
    palette.setColor(palette.Window, QColor(53, 53, 53))
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, QColor(25, 25, 25))
    palette.setColor(palette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ToolTipBase, Qt.white)
    palette.setColor(palette.ToolTipText, Qt.white)
    palette.setColor(palette.Text, Qt.white)
    palette.setColor(palette.Button, QColor(53, 53, 53))
    palette.setColor(palette.ButtonText, Qt.white)
    palette.setColor(palette.BrightText, Qt.red)
    palette.setColor(palette.Link, QColor(42, 130, 218))
    palette.setColor(palette.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.HighlightedText, Qt.black)

    # Apply the palette to the application
    app.setPalette(palette)


def set_light_theme():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(239, 240, 241))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.black)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(239, 240, 241))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))


class Themes:

    def __init__(self, fenster):
        self.widget = fenster

    def set_native_theme(self):
        self.widget.setStyleSheet(u"background-color: rgb(0, 0, 0)")
        self.widget.ui.label_url.setStyleSheet(u"QLabel {\n"
                                               "    color: white;\n"
                                               "    font-size: 16px;\n"
                                               "	margin-right: 28px;\n"
                                               "}\n"
                                               "\n"
                                               "QLabel#Title {\n"
                                               "    color: #212121;\n"
                                               "    font-size: 24px;\n"
                                               "    font-weight: bold;\n"
                                               "}\n"
                                               "\n"
                                               "QLabel#Subtitle {\n"
                                               "    color: #757575;\n"
                                               "    font-size: 20px;\n"
                                               "}\n"
                                               "")
        self.widget.ui.lineedit_url.setStyleSheet(u"QLineEdit {\n"
                                                  "    border: 2px solid #757575;\n"
                                                  "    border-radius: 5px;\n"
                                                  "    padding: 0 8px;\n"
                                                  "    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf "
                                                  "Schwarz */\n"
                                                  "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                  "    font-size: 16px;\n"
                                                  "    height: 20px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QLineEdit:focus {\n"
                                                  "    border-color: #4a90d9;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QLineEdit:disabled {\n"
                                                  "    background: #444444;  /* setzt den Hintergrund auf ein dunkles "
                                                  "Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                  "    color: #aaaaaa; \n"
                                                  "    border-color: #aaaaaa;\n"
                                                  "}")
        self.widget.ui.button_start.setStyleSheet(u"QPushButton {\n"
                                                  "    background-color: #5468ff;\n"
                                                  "    border: none;\n"
                                                  "    border-radius: 6px;\n"
                                                  "    color: #fff;\n"
                                                  "    font-family: \"JetBrains Mono\", monospace;\n"
                                                  "    font-size: 15px;\n"
                                                  "    padding: 0px 16px 0px 16px;\n"
                                                  "    height: 24px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:hover {\n"
                                                  "    background-color: #3c4fe0;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color: #3c4fe0;\n"
                                                  "}\n"
                                                  "")
        self.widget.ui.label_url_file.setStyleSheet(u"QLabel {\n"
                                                    "    color: white;\n"
                                                    "    font-size: 16px;\n"
                                                    "	margin-right: 28px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLabel#Title {\n"
                                                    "    color: #212121;\n"
                                                    "    font-size: 24px;\n"
                                                    "    font-weight: bold;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLabel#Subtitle {\n"
                                                    "    color: #757575;\n"
                                                    "    font-size: 20px;\n"
                                                    "}\n"
                                                    "")
        self.widget.ui.lineedit_url_file.setStyleSheet(u"QLineEdit {\n"
                                                       "    border: 2px solid #757575;\n"
                                                       "    border-radius: 5px;\n"
                                                       "    padding: 0 8px;\n"
                                                       "    background: rgb(94, 92, 100);  /* setzt den Hintergrund "
                                                       "auf Schwarz */\n"
                                                       "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                       "    font-size: 16px;\n"
                                                       "    height: 20px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QLineEdit:focus {\n"
                                                       "    border-color: #4a90d9;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QLineEdit:disabled {\n"
                                                       "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                       "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                       "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles "
                                                       "Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                       "    border-color: #aaaaaa;\n"
                                                       "}")
        self.widget.ui.button_start_file.setStyleSheet(u"QPushButton {\n"
                                                       "    background-color: #5468ff;\n"
                                                       "    border: none;\n"
                                                       "    border-radius: 6px;\n"
                                                       "    color: #fff;\n"
                                                       "    font-family: \"JetBrains Mono\", monospace;\n"
                                                       "    font-size: 15px;\n"
                                                       "    padding: 0px 16px 0px 16px;\n"
                                                       "    height: 24px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:hover {\n"
                                                       "    background-color: #3c4fe0;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QPushButton:pressed {\n"
                                                       "    background-color: #3c4fe0;\n"
                                                       "}\n"
                                                       "")
        self.widget.ui.radio_highest.setStyleSheet(u"QRadioButton {\n"
                                                   "	color: rgb(0, 255, 152)}\n"
                                                   "\n"
                                                   "\n"
                                                   "QRadioButton::indicator::unchecked {\n"
                                                   "	border: 1px solid white;\n"
                                                   "	border-radius: 5px;\n"
                                                   "}\n"
                                                   "\n"
                                                   "\n"
                                                   "QRadioButton::indicator:checked {\n"
                                                   "    border : 4px solid;\n"
                                                   "	border-color: black;\n"
                                                   "	border-radius: 6px;\n"
                                                   "	background-color: rgb(0, 255, 183);\n"
                                                   "\n"
                                                   "}\n"
                                                   "")
        self.widget.ui.radio_middle.setStyleSheet(u"QRadioButton {\n"
                                                  "	color: rgb(255, 171, 0)}\n"
                                                  "\n"
                                                  "\n"
                                                  "QRadioButton::indicator::unchecked {\n"
                                                  "	border: 1px solid white;\n"
                                                  "	border-radius: 5px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "\n"
                                                  "QRadioButton::indicator:checked {\n"
                                                  "    border : 4px solid;\n"
                                                  "	border-color: black;\n"
                                                  "	border-radius: 6px;\n"
                                                  "	background-color: rgb(0, 255, 183);\n"
                                                  "\n"
                                                  "}\n"
                                                  "\n"
                                                  "")
        self.widget.ui.radio_lowest.setStyleSheet(u"QRadioButton {\n"
                                                  "	color: rgb(255, 0, 0)}\n"
                                                  "\n"
                                                  "\n"
                                                  "QRadioButton::indicator::unchecked {\n"
                                                  "	border: 1px solid white;\n"
                                                  "	border-radius: 5px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "\n"
                                                  "QRadioButton::indicator:checked {\n"
                                                  "    border : 4px solid;\n"
                                                  "	border-color: black;\n"
                                                  "	border-radius: 6px;\n"
                                                  "	background-color: rgb(0, 255, 183);\n"
                                                  "\n"
                                                  "}\n"
                                                  "")
        self.widget.ui.groupbox_quality.setStyleSheet(u"color: rgb(122, 0, 255)")
        self.widget.ui.label_output.setStyleSheet(u"color: rgb(255, 255, 255)")
        self.widget.ui.lineedit_output.setStyleSheet(u"QLineEdit {\n"
                                                     "    border: 2px solid #757575;\n"
                                                     "    border-radius: 5px;\n"
                                                     "    padding: 0 8px;\n"
                                                     "    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf "
                                                     "Schwarz */\n"
                                                     "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                     "    font-size: 16px;\n"
                                                     "    height: 20px;\n"
                                                     "}\n"
                                                     "\n"
                                                     "QLineEdit:focus {\n"
                                                     "    border-color: #4a90d9;\n"
                                                     "}\n"
                                                     "\n"
                                                     "QLineEdit:disabled {\n"
                                                     "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                     "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                     "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles "
                                                     "Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                     "    border-color: #aaaaaa;\n"
                                                     "}")
        self.widget.ui.groupbox_settings_ui.setStyleSheet(u"color: rgb(255, 176, 0)")
        self.widget.ui.radio_native.setStyleSheet(u"QRadioButton {\n"
                                                  "	color: rgb(0, 255, 250) }\n"
                                                  "\n"
                                                  "\n"
                                                  "QRadioButton::indicator::unchecked {\n"
                                                  "	border: 1px solid white;\n"
                                                  "	border-radius: 5px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "\n"
                                                  "QRadioButton::indicator:checked {\n"
                                                  "    border : 4px solid;\n"
                                                  "	border-color: black;\n"
                                                  "	border-radius: 6px;\n"
                                                  "	background-color: rgb(0, 255, 183);\n"
                                                  "\n"
                                                  "}\n"
                                                  "")
        self.widget.ui.radio_dark.setStyleSheet(u"QRadioButton {\n"
                                                "	color: rgb(81, 0, 255)}\n"
                                                "\n"
                                                "\n"
                                                "QRadioButton::indicator::unchecked {\n"
                                                "	border: 1px solid white;\n"
                                                "	border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "QRadioButton::indicator:checked {\n"
                                                "    border : 4px solid;\n"
                                                "	border-color: black;\n"
                                                "	border-radius: 6px;\n"
                                                "	background-color: rgb(0, 255, 183);\n"
                                                "\n"
                                                "}\n"
                                                "")
        self.widget.ui.radio_white.setStyleSheet(u"QRadioButton {\n"
                                                 "	color: rgb(255, 255, 255)}\n"
                                                 "\n"
                                                 "\n"
                                                 "QRadioButton::indicator::unchecked {\n"
                                                 "	border: 1px solid white;\n"
                                                 "	border-radius: 5px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "\n"
                                                 "QRadioButton::indicator:checked {\n"
                                                 "    border : 4px solid;\n"
                                                 "	border-color: black;\n"
                                                 "	border-radius: 6px;\n"
                                                 "	background-color: rgb(0, 255, 183);\n"
                                                 "\n"
                                                 "}\n"
                                                 "")
        self.widget.ui.progressbar_download.setStyleSheet(u"QProgressBar {\n"
                                                          "    background-color: #F0F0F0; /* Hellgrauer Hintergrund "
                                                          "*/\n"
                                                          "	text-align: center;\n"
                                                          "	color: rgb(230, 97, 0);\n"
                                                          "	border: color grey;\n"
                                                          "	border-width: 6;\n"
                                                          "	border-radius: 12px;\n"
                                                          "	color: black;\n"
                                                          "	\n"
                                                          "}\n"
                                                          "\n"
                                                          "QProgressBar::chunk {\n"
                                                          "    background-color: rgb(26, 95, 180); /* Gr\u00fcn als "
                                                          "Vordergrundfarbe */\n"
                                                          "}cc")
        self.widget.ui.groupbox_metadata.setStyleSheet(u"color: rgb(255, 255, 255)")
        self.widget.ui.label_duration.setStyleSheet(u"QLabel {\n"
                                                    "    color: white;\n"
                                                    "    font-size: 16px;\n"
                                                    "	margin-right: 28px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLabel#Title {\n"
                                                    "    color: #212121;\n"
                                                    "    font-size: 24px;\n"
                                                    "    font-weight: bold;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLabel#Subtitle {\n"
                                                    "    color: #757575;\n"
                                                    "    font-size: 20px;\n"
                                                    "}\n"
                                                    "")
        self.widget.ui.label_author.setStyleSheet(u"QLabel {\n"
                                                  "    color: white;\n"
                                                  "    font-size: 16px;\n"
                                                  "	margin-right: 28px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QLabel#Title {\n"
                                                  "    color: #212121;\n"
                                                  "    font-size: 24px;\n"
                                                  "    font-weight: bold;\n"
                                                  "}\n"
                                                  "\n"
                                                  "QLabel#Subtitle {\n"
                                                  "    color: #757575;\n"
                                                  "    font-size: 20px;\n"
                                                  "}\n"
                                                  "")
        self.widget.ui.lineedit_author.setStyleSheet(u"QLineEdit {\n"
                                                     "    border: 2px solid #757575;\n"
                                                     "    border-radius: 5px;\n"
                                                     "    padding: 0 8px;\n"
                                                     "    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf "
                                                     "Schwarz */\n"
                                                     "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                     "    font-size: 16px;\n"
                                                     "    height: 20px;\n"
                                                     "}\n"
                                                     "\n"
                                                     "QLineEdit:focus {\n"
                                                     "    border-color: #4a90d9;\n"
                                                     "}\n"
                                                     "\n"
                                                     "QLineEdit:disabled {\n"
                                                     "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                     "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                     "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles "
                                                     "Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                     "    border-color: #aaaaaa;\n"
                                                     "}")
        self.widget.ui.lineedit_duration.setStyleSheet(u"QLineEdit {\n"
                                                       "    border: 2px solid #757575;\n"
                                                       "    border-radius: 5px;\n"
                                                       "    padding: 0 8px;\n"
                                                       "    background: rgb(94, 92, 100);  /* setzt den Hintergrund "
                                                       "auf Schwarz */\n"
                                                       "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                       "    font-size: 16px;\n"
                                                       "    height: 20px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QLineEdit:focus {\n"
                                                       "    border-color: #4a90d9;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QLineEdit:disabled {\n"
                                                       "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                       "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                       "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles "
                                                       "Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                       "    border-color: #aaaaaa;\n"
                                                       "}")
        self.widget.ui.lineedit_title.setStyleSheet(u"QLineEdit {\n"
                                                    "    border: 2px solid #757575;\n"
                                                    "    border-radius: 5px;\n"
                                                    "    padding: 0 8px;\n"
                                                    "    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf "
                                                    "Schwarz */\n"
                                                    "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                    "    font-size: 16px;\n"
                                                    "    height: 20px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLineEdit:focus {\n"
                                                    "    border-color: #4a90d9;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLineEdit:disabled {\n"
                                                    "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                    "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                    "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, "
                                                    "wenn das QLineEdit deaktiviert ist */\n"
                                                    "    border-color: #aaaaaa;\n"
                                                    "}")
        self.widget.ui.lineedit_hotspots.setStyleSheet(u"QLineEdit {\n"
                                                       "    border: 2px solid #757575;\n"
                                                       "    border-radius: 5px;\n"
                                                       "    padding: 0 8px;\n"
                                                       "    background: rgb(94, 92, 100);  /* setzt den Hintergrund "
                                                       "auf Schwarz */\n"
                                                       "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                       "    font-size: 16px;\n"
                                                       "    height: 20px;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QLineEdit:focus {\n"
                                                       "    border-color: #4a90d9;\n"
                                                       "}\n"
                                                       "\n"
                                                       "QLineEdit:disabled {\n"
                                                       "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                       "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                       "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles "
                                                       "Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                       "    border-color: #aaaaaa;\n"
                                                       "}")
        self.widget.ui.label_hotspots.setStyleSheet(u"QLabel {\n"
                                                    "    color: white;\n"
                                                    "    font-size: 16px;\n"
                                                    "	margin-right: 28px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLabel#Title {\n"
                                                    "    color: #212121;\n"
                                                    "    font-size: 24px;\n"
                                                    "    font-weight: bold;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLabel#Subtitle {\n"
                                                    "    color: #757575;\n"
                                                    "    font-size: 20px;\n"
                                                    "}\n"
                                                    "")
        self.widget.ui.label_date.setStyleSheet(u"QLabel {\n"
                                                "    color: white;\n"
                                                "    font-size: 16px;\n"
                                                "	margin-right: 28px;\n"
                                                "}\n"
                                                "\n"
                                                "QLabel#Title {\n"
                                                "    color: #212121;\n"
                                                "    font-size: 24px;\n"
                                                "    font-weight: bold;\n"
                                                "}\n"
                                                "\n"
                                                "QLabel#Subtitle {\n"
                                                "    color: #757575;\n"
                                                "    font-size: 20px;\n"
                                                "}\n"
                                                "")
        self.widget.ui.label_title.setStyleSheet(u"QLabel {\n"
                                                 "    color: white;\n"
                                                 "    font-size: 16px;\n"
                                                 "	margin-right: 28px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QLabel#Title {\n"
                                                 "    color: #212121;\n"
                                                 "    font-size: 24px;\n"
                                                 "    font-weight: bold;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QLabel#Subtitle {\n"
                                                 "    color: #757575;\n"
                                                 "    font-size: 20px;\n"
                                                 "}\n"
                                                 "")
        self.widget.ui.lineedit_views.setStyleSheet(u"QLineEdit {\n"
                                                    "    border: 2px solid #757575;\n"
                                                    "    border-radius: 5px;\n"
                                                    "    padding: 0 8px;\n"
                                                    "    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf "
                                                    "Schwarz */\n"
                                                    "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                    "    font-size: 16px;\n"
                                                    "    height: 20px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLineEdit:focus {\n"
                                                    "    border-color: #4a90d9;\n"
                                                    "}\n"
                                                    "\n"
                                                    "QLineEdit:disabled {\n"
                                                    "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                    "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                    "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, "
                                                    "wenn das QLineEdit deaktiviert ist */\n"
                                                    "    border-color: #aaaaaa;\n"
                                                    "}")
        self.widget.ui.lineedit_date.setStyleSheet(u"QLineEdit {\n"
                                                   "    border: 2px solid #757575;\n"
                                                   "    border-radius: 5px;\n"
                                                   "    padding: 0 8px;\n"
                                                   "    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf "
                                                   "Schwarz */\n"
                                                   "    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
                                                   "    font-size: 16px;\n"
                                                   "    height: 20px;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QLineEdit:focus {\n"
                                                   "    border-color: #4a90d9;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QLineEdit:disabled {\n"
                                                   "    background: #444444;  /* setzt den Hintergrund auf ein "
                                                   "dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
                                                   "    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, "
                                                   "wenn das QLineEdit deaktiviert ist */\n"
                                                   "    border-color: #aaaaaa;\n"
                                                   "}")
        self.widget.ui.label_views.setStyleSheet(u"QLabel {\n"
                                                 "    color: white;\n"
                                                 "    font-size: 16px;\n"
                                                 "	margin-right: 28px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QLabel#Title {\n"
                                                 "    color: #212121;\n"
                                                 "    font-size: 24px;\n"
                                                 "    font-weight: bold;\n"
                                                 "}\n"
                                                 "\n"
                                                 "QLabel#Subtitle {\n"
                                                 "    color: #757575;\n"
                                                 "    font-size: 20px;\n"
                                                 "}\n"
                                                 "")
        self.widget.ui.button_get_metadata.setStyleSheet(u"QPushButton {\n"
                                                         "    background-color: #5468ff;\n"
                                                         "    border: none;\n"
                                                         "    border-radius: 6px;\n"
                                                         "    color: #fff;\n"
                                                         "    font-family: \"JetBrains Mono\", monospace;\n"
                                                         "    font-size: 15px;\n"
                                                         "    padding: 0px 16px 0px 16px;\n"
                                                         "    height: 24px;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QPushButton:hover {\n"
                                                         "    background-color: #3c4fe0;\n"
                                                         "}\n"
                                                         "\n"
                                                         "QPushButton:pressed {\n"
                                                         "    background-color: #3c4fe0;\n"
                                                         "}\n"
                                                         "")
        self.widget.ui.credits_text.setStyleSheet(u"background-color: rgb(0, 0, 0)")


if __name__ == "__main__":
    config_file()
    conf = ConfigParser()
    conf.read("config.ini")

    app = QApplication(sys.argv)
    widget = Widget()

    if conf["ui"]["mode"] == "dark":
        app.setStyleSheet("fusion")

    elif conf["ui"]["mode"] == "native":
        Themes(widget).set_native_theme()

    elif conf["ui"]["mode"] == "white":
        print("WHITE MODE USER DETECTED.   - 10 Social credit!!!")
        set_light_theme()

    widget.show()
    sys.exit(app.exec())
