# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1496, 569)
        Widget.setStyleSheet(u"background-color: rgb(0, 0, 0)")
        self.gridLayout_7 = QGridLayout(Widget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.groupbox_urls = QGroupBox(Widget)
        self.groupbox_urls.setObjectName(u"groupbox_urls")
        self.gridLayout = QGridLayout(self.groupbox_urls)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_url = QLabel(self.groupbox_urls)
        self.label_url.setObjectName(u"label_url")
        self.label_url.setStyleSheet(u"QLabel {\n"
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

        self.horizontalLayout_2.addWidget(self.label_url)

        self.lineedit_url = QLineEdit(self.groupbox_urls)
        self.lineedit_url.setObjectName(u"lineedit_url")
        self.lineedit_url.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")

        self.horizontalLayout_2.addWidget(self.lineedit_url)

        self.button_start = QPushButton(self.groupbox_urls)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start.setStyleSheet(u"QPushButton {\n"
"    background-color: #5468ff;\n"
"	border-width: 2px;\n"
"	border-color: rgb(98, 255, 182);\n"
"	border-style: double;\n"
"    border-radius: 6px;\n"
"	text-align: center;\n"
"    color: #fff;\n"
"    font-family: \"JetBrains Mono\", monospace;\n"
"    font-size: 15px;\n"
"    padding: 0px 16px 0px 16px;\n"
"    height: 24px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3c4fe0;\n"
"	border-color: rgb(179, 0, 255)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3c4fe0;\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.button_start)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_url_file = QLabel(self.groupbox_urls)
        self.label_url_file.setObjectName(u"label_url_file")
        self.label_url_file.setStyleSheet(u"QLabel {\n"
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

        self.horizontalLayout.addWidget(self.label_url_file)

        self.lineedit_url_file = QLineEdit(self.groupbox_urls)
        self.lineedit_url_file.setObjectName(u"lineedit_url_file")
        self.lineedit_url_file.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")

        self.horizontalLayout.addWidget(self.lineedit_url_file)

        self.button_start_file = QPushButton(self.groupbox_urls)
        self.button_start_file.setObjectName(u"button_start_file")
        self.button_start_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start_file.setStyleSheet(u"QPushButton {\n"
"    background-color: #5468ff;\n"
"	border-width: 2px;\n"
"	border-color: rgb(98, 255, 182);\n"
"	border-style: double;\n"
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
"	border-color: rgb(179, 0, 255)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3c4fe0;\n"
"}\n"
"")

        self.horizontalLayout.addWidget(self.button_start_file)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.label = QLabel(self.groupbox_urls)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: white;\n"
"font-size: 12px;")

        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_user_channel = QLabel(self.groupbox_urls)
        self.label_user_channel.setObjectName(u"label_user_channel")
        self.label_user_channel.setStyleSheet(u"QLabel {\n"
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

        self.horizontalLayout_4.addWidget(self.label_user_channel)

        self.lineedit_user_channel = QLineEdit(self.groupbox_urls)
        self.lineedit_user_channel.setObjectName(u"lineedit_user_channel")
        self.lineedit_user_channel.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")

        self.horizontalLayout_4.addWidget(self.lineedit_user_channel)

        self.button_start_user_channel = QPushButton(self.groupbox_urls)
        self.button_start_user_channel.setObjectName(u"button_start_user_channel")
        self.button_start_user_channel.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start_user_channel.setStyleSheet(u"QPushButton {\n"
"    background-color: #5468ff;\n"
"	border-width: 2px;\n"
"	border-color: rgb(98, 255, 182);\n"
"	border-style: double;\n"
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
"	border-color: rgb(179, 0, 255)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3c4fe0;\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.button_start_user_channel)


        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupbox_urls, 0, 0, 2, 1)

        self.credits_text = QTextBrowser(Widget)
        self.credits_text.setObjectName(u"credits_text")
        self.credits_text.setStyleSheet(u"background-color: rgb(0, 0, 0)")

        self.gridLayout_7.addWidget(self.credits_text, 2, 1, 1, 1)

        self.groupbox_metadata = QGroupBox(Widget)
        self.groupbox_metadata.setObjectName(u"groupbox_metadata")
        self.groupbox_metadata.setStyleSheet(u"color: rgb(255, 255, 255)")
        self.gridLayout_5 = QGridLayout(self.groupbox_metadata)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_title = QLabel(self.groupbox_metadata)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_title, 0, 0, 1, 1)

        self.lineedit_title = QLineEdit(self.groupbox_metadata)
        self.lineedit_title.setObjectName(u"lineedit_title")
        self.lineedit_title.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_title.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_title, 0, 1, 1, 1)

        self.label_likes = QLabel(self.groupbox_metadata)
        self.label_likes.setObjectName(u"label_likes")
        self.label_likes.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_likes, 1, 0, 1, 1)

        self.lineedit_likes = QLineEdit(self.groupbox_metadata)
        self.lineedit_likes.setObjectName(u"lineedit_likes")
        self.lineedit_likes.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_likes.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_likes, 1, 1, 1, 1)

        self.label_image_url = QLabel(self.groupbox_metadata)
        self.label_image_url.setObjectName(u"label_image_url")
        self.label_image_url.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 10px;\n"
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

        self.gridLayout_5.addWidget(self.label_image_url, 2, 0, 1, 1)

        self.lineedit_image_url = QLineEdit(self.groupbox_metadata)
        self.lineedit_image_url.setObjectName(u"lineedit_image_url")
        self.lineedit_image_url.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_image_url.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_image_url, 2, 1, 1, 1)

        self.label_tags = QLabel(self.groupbox_metadata)
        self.label_tags.setObjectName(u"label_tags")
        self.label_tags.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 10px;\n"
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

        self.gridLayout_5.addWidget(self.label_tags, 3, 0, 1, 1)

        self.lineedit_tags = QLineEdit(self.groupbox_metadata)
        self.lineedit_tags.setObjectName(u"lineedit_tags")
        self.lineedit_tags.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_tags.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_tags, 3, 1, 1, 1)

        self.label_author = QLabel(self.groupbox_metadata)
        self.label_author.setObjectName(u"label_author")
        self.label_author.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_author, 4, 0, 1, 1)

        self.lineedit_author = QLineEdit(self.groupbox_metadata)
        self.lineedit_author.setObjectName(u"lineedit_author")
        self.lineedit_author.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_author.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_author, 4, 1, 1, 1)

        self.label_views = QLabel(self.groupbox_metadata)
        self.label_views.setObjectName(u"label_views")
        self.label_views.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_views, 5, 0, 1, 1)

        self.lineedit_views = QLineEdit(self.groupbox_metadata)
        self.lineedit_views.setObjectName(u"lineedit_views")
        self.lineedit_views.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_views.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_views, 5, 1, 1, 1)

        self.label_date = QLabel(self.groupbox_metadata)
        self.label_date.setObjectName(u"label_date")
        self.label_date.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_date, 6, 0, 1, 1)

        self.lineedit_date = QLineEdit(self.groupbox_metadata)
        self.lineedit_date.setObjectName(u"lineedit_date")
        self.lineedit_date.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_date.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_date, 6, 1, 1, 1)

        self.label_duration = QLabel(self.groupbox_metadata)
        self.label_duration.setObjectName(u"label_duration")
        self.label_duration.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_duration, 7, 0, 1, 1)

        self.lineedit_duration = QLineEdit(self.groupbox_metadata)
        self.lineedit_duration.setObjectName(u"lineedit_duration")
        self.lineedit_duration.setAutoFillBackground(False)
        self.lineedit_duration.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_duration.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_duration, 7, 1, 1, 1)

        self.label_hotspots = QLabel(self.groupbox_metadata)
        self.label_hotspots.setObjectName(u"label_hotspots")
        self.label_hotspots.setStyleSheet(u"QLabel {\n"
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

        self.gridLayout_5.addWidget(self.label_hotspots, 8, 0, 1, 1)

        self.lineedit_hotspots = QLineEdit(self.groupbox_metadata)
        self.lineedit_hotspots.setObjectName(u"lineedit_hotspots")
        self.lineedit_hotspots.setAutoFillBackground(False)
        self.lineedit_hotspots.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_hotspots.setReadOnly(True)

        self.gridLayout_5.addWidget(self.lineedit_hotspots, 8, 1, 1, 1)

        self.button_get_metadata = QPushButton(self.groupbox_metadata)
        self.button_get_metadata.setObjectName(u"button_get_metadata")
        self.button_get_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_metadata.setStyleSheet(u"QPushButton {\n"
"    background-color: #5468ff;\n"
"	text-align: center;\n"
"	border-width: 2px;\n"
"    border-radius: 6px;\n"
"	border-style: double;\n"
"    color: #fff;\n"
"    font-family: \"JetBrains Mono\", monospace;\n"
"    font-size: 15px;\n"
"    padding: 0px 16px 0px 16px;\n"
"    height: 24px;\n"
"	border-color: rgb(73, 255, 167)\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3c4fe0;\n"
"	border-color: rgb(179, 0, 255)\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3c4fe0;\n"
"}\n"
"")

        self.gridLayout_5.addWidget(self.button_get_metadata, 9, 1, 1, 1)


        self.gridLayout_7.addWidget(self.groupbox_metadata, 2, 0, 1, 1)

        self.groupbox_settings = QGroupBox(Widget)
        self.groupbox_settings.setObjectName(u"groupbox_settings")
        self.gridLayout_4 = QGridLayout(self.groupbox_settings)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupbox_useless = QGroupBox(self.groupbox_settings)
        self.groupbox_useless.setObjectName(u"groupbox_useless")
        self.gridLayout_2 = QGridLayout(self.groupbox_useless)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_status = QLabel(self.groupbox_useless)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setStyleSheet(u"color: white;")

        self.gridLayout_2.addWidget(self.label_status, 0, 1, 1, 1)

        self.groupbox_quality = QGroupBox(self.groupbox_useless)
        self.groupbox_quality.setObjectName(u"groupbox_quality")
        self.groupbox_quality.setStyleSheet(u"color: rgb(122, 0, 255)")
        self.gridLayout_3 = QGridLayout(self.groupbox_quality)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.radio_highest = QRadioButton(self.groupbox_quality)
        self.radio_highest.setObjectName(u"radio_highest")
        self.radio_highest.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_highest.setStyleSheet(u"QRadioButton {\n"
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

        self.gridLayout_3.addWidget(self.radio_highest, 0, 0, 1, 1)

        self.radio_middle = QRadioButton(self.groupbox_quality)
        self.radio_middle.setObjectName(u"radio_middle")
        self.radio_middle.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_middle.setStyleSheet(u"QRadioButton {\n"
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

        self.gridLayout_3.addWidget(self.radio_middle, 1, 0, 1, 1)

        self.radio_lowest = QRadioButton(self.groupbox_quality)
        self.radio_lowest.setObjectName(u"radio_lowest")
        self.radio_lowest.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_lowest.setStyleSheet(u"QRadioButton {\n"
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

        self.gridLayout_3.addWidget(self.radio_lowest, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupbox_quality, 0, 0, 2, 1)

        self.lineedit_status = QLineEdit(self.groupbox_useless)
        self.lineedit_status.setObjectName(u"lineedit_status")
        self.lineedit_status.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_status.setReadOnly(True)

        self.gridLayout_2.addWidget(self.lineedit_status, 0, 2, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_output = QLabel(self.groupbox_useless)
        self.label_output.setObjectName(u"label_output")
        self.label_output.setStyleSheet(u"color: rgb(255, 255, 255)")

        self.horizontalLayout_3.addWidget(self.label_output)

        self.lineedit_output = QLineEdit(self.groupbox_useless)
        self.lineedit_output.setObjectName(u"lineedit_output")
        self.lineedit_output.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 5px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")

        self.horizontalLayout_3.addWidget(self.lineedit_output)


        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 2)


        self.gridLayout_4.addWidget(self.groupbox_useless, 0, 1, 1, 1)

        self.progressbar_download = QProgressBar(self.groupbox_settings)
        self.progressbar_download.setObjectName(u"progressbar_download")
        self.progressbar_download.setStyleSheet(u"QProgressBar {\n"
"    background-color: #F0F0F0; /* Hellgrauer Hintergrund */\n"
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
"    background-color: rgb(26, 95, 180); /* Gr\u00fcn als Vordergrundfarbe */\n"
"}cc")
        self.progressbar_download.setValue(0)

        self.gridLayout_4.addWidget(self.progressbar_download, 1, 1, 1, 3)


        self.gridLayout_7.addWidget(self.groupbox_settings, 0, 1, 2, 1)


        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Porn Fetch 1.2 (LGPLv3) : https://github.com/EchterAlsFake/Porn_Fetch", None))
        self.groupbox_urls.setTitle(QCoreApplication.translate("Widget", u"Download", None))
        self.label_url.setText(QCoreApplication.translate("Widget", u"URL:", None))
        self.button_start.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label_url_file.setText(QCoreApplication.translate("Widget", u"File with URLs:", None))
        self.button_start_file.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Must be a URL.  Example: https://de.pornhub.com/model/luna-roulette", None))
        self.label_user_channel.setText(QCoreApplication.translate("Widget", u"User / Channel:", None))
        self.button_start_user_channel.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.credits_text.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Credits:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">API: PHUB by Egsagon.  This project would not be possible without it.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-inden"
                        "t:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Author: EchterAlsFake</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">License: LGPLv3</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Plugins: Tabnine, Material Theme Icons</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Libraries: colorama, tqdm, PySide6</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><"
                        "br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Graphical User Interface was created with Qt - PySide6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Version: 1.2</span></p></body></html>", None))
        self.groupbox_metadata.setTitle(QCoreApplication.translate("Widget", u"Metadata", None))
        self.label_title.setText(QCoreApplication.translate("Widget", u"Title:", None))
        self.label_likes.setText(QCoreApplication.translate("Widget", u"Likes:", None))
        self.label_image_url.setText(QCoreApplication.translate("Widget", u"Image URL", None))
        self.label_tags.setText(QCoreApplication.translate("Widget", u"Tags:", None))
        self.label_author.setText(QCoreApplication.translate("Widget", u"Author: ", None))
        self.label_views.setText(QCoreApplication.translate("Widget", u"Views:", None))
        self.label_date.setText(QCoreApplication.translate("Widget", u"Date:", None))
        self.label_duration.setText(QCoreApplication.translate("Widget", u"Duration:", None))
        self.label_hotspots.setText(QCoreApplication.translate("Widget", u"Hotspots:", None))
        self.button_get_metadata.setText(QCoreApplication.translate("Widget", u"Get metadata", None))
        self.groupbox_settings.setTitle("")
        self.groupbox_useless.setTitle("")
        self.label_status.setText(QCoreApplication.translate("Widget", u"Status:", None))
        self.groupbox_quality.setTitle(QCoreApplication.translate("Widget", u"Quality", None))
        self.radio_highest.setText(QCoreApplication.translate("Widget", u"Highest", None))
        self.radio_middle.setText(QCoreApplication.translate("Widget", u"Middle", None))
        self.radio_lowest.setText(QCoreApplication.translate("Widget", u"Lowest", None))
        self.label_output.setText(QCoreApplication.translate("Widget", u"Output Path:", None))
    # retranslateUi

