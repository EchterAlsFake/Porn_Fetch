
"""
IMPORTANT INFORMATION

THIS PROJECT IS LICENSED UNDER THE LGPLv3 License
You should have received a copy of the license along with this program.

The Source code of this program can be found here: https://github.com/EchterAlsFake/Porn_Fetch

API by Egsagon: https://github.com/Egsagon/PHUB



Author: EchterAlsFake - Johannes Habel

2023
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtWidgets import QMessageBox
from ui_form import Ui_Widget
from phub import Client, Quality
import os
import wget
from configparser import ConfigParser
from colorama import *

def character_stripping(title):
    disallowed_characters = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]
    for char in disallowed_characters:
        title = title.replace(char, "")

    title = str(title).lower()
    return title.encode("utf-8")


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

    def get_quality(self):

        if self.ui.radio_highest.isChecked():
            return Quality.BEST

        elif self.ui.radio_middle.isChecked():
            return Quality.MIDDLE

        elif self.ui.radio_lowest.isChecked():
            return Quality.MIDDLE

        else:
            qmsg_box = QMessageBox()
            qmsg_box.setText("No Quality selected..  Using best automatically ")
            qmsg_box.exec()
            return Quality.BEST

    def callback(self, pos, total):
        self.ui.progressbar_download.setMaximum(total)
        self.ui.progressbar_download.setValue(pos)

    def start(self):

        url = self.ui.lineedit_url.text()
        self.download(url)

    def download(self, url):

        if not self.test_video(url):
            return
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
            self._extracted_from_download_17(output, quality)

    def _extracted_from_download_17(self, output, quality):
        title = self.video.title
        self.ui.lineedit_status.setText(f"Downloading: {title}")
        title = character_stripping(title=title)
        final_output = str(output) + str(title) + ".mp4"
        print(f"""
[DEBUG] {Fore.LIGHTCYAN_EX}
{Fore.LIGHTGREEN_EX}Downloading: {title}
{Fore.LIGHTYELLOW_EX}Location: {final_output}
{Fore.LIGHTMAGENTA_EX}Quality: {quality}""")

        self.video.download(quality=quality, path=final_output, callback=self.callback)
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
                self._extracted_from_url_testing_13(f)

    def _extracted_from_url_testing_13(self, f):
        content = f.read().splitlines()
        self.ui.lineedit_status.setText("ATTENTION: Testing URLs before downloading...")
        valid_urls = []
        invalid_urls = []
        counter = 0

        for url in content:
            length = len(content)
            if self.test_video(url):
                counter += 1
                text = f"Testing {counter} of {length} URLs....  Please wait "
                self.ui.lineedit_status.setText(str(text))
                valid_urls.append(url)

            else:
                invalid_urls.append(url)
        text = f"Valid URLs: {len(valid_urls)} : Invalid URLs: {len(invalid_urls)}"
        self.ui.lineedit_status.setText(str(text))

        for url in valid_urls:
            self.download(url)

    def test_video(self, url):

        try:

            self.video = self.client.get(url=str(url))
            return True

        except Exception as e:
            qmsg = QMessageBox()
            qmsg.setText(f"The URL you entered is not valid. ERROR: {str(e)}")
            qmsg.exec()
            return "WW"

    def get_metadata(self):

        url = self.ui.lineedit_url.text()
        if self.test_video(url):

            self._extracted_from_get_metadata_6()
        elif self.test_video(url) != "WW":
            qmsg_box = QMessageBox()
            qmsg_box.setText("Unknown Error.  Please still report it and give me the URL you used. Thansk :) ")
            qmsg_box.exec()

    def _extracted_from_get_metadata_6(self):
        self.ui.lineedit_status.setText("Getting metadata...")
        title = self.video.title
        duration = self.video.duration
        hotspots = self.video.hotspots
        date = self.video.date
        author = self.video.author

        duration = duration / 60
        str(duration).strip(":")
        str(duration).strip("0")

        self.ui.lineedit_title.setText(str(title))
        self.ui.lineedit_duration.setText(f"{str(duration)} minutes")
        self.ui.lineedit_date.setText(str(date))
        self.ui.lineedit_author.setText(str(author))
        self.ui.lineedit_hotspots.setText(str(hotspots))
        self.ui.lineedit_status.setText("Successfully got metadata")

    def get_thumbnail(self):

        title = self.video.title
        url = self.video.image_url
        output = self.ui.lineedit_output.text()
        final_output = output + title + ".jpg"

        try:
            self.ui.lineedit_status.setText("Downloading thumbnail...")
            wget.download(url, out=final_output)

            if os.path.exists(final_output):
                print("Downloaded Thumbnail :)")
                self.ui.lineedit_status.setText("Downloaded Thumbnail")

            else:

                qmsg_box = QMessageBox()
                qmsg_box.setText(
"""There was an error. Maybe the thumbnail downloaded successfully, but the title is weird, and program can't find it. 
Just search for it :)""")
                qmsg_box.exec()

        except Exception as e:

            qmsg_box = QMessageBox()
            qmsg_box.setText(f"Unhandled Error: {str(e)}")
            qmsg_box.exec()

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

    app = QApplication(sys.argv)
    widget = Widget()
    Themes(widget).set_native_theme()
    widget.show()
    sys.exit(app.exec())
