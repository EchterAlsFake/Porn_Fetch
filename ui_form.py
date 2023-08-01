# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
    QHeaderView, QLabel, QLineEdit, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QStackedWidget,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(970, 528)
        Widget.setStyleSheet(u"background-color: rgb(0, 0, 0)")
        self.gridLayout_12 = QGridLayout(Widget)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupbox_urls = QGroupBox(self.page)
        self.groupbox_urls.setObjectName(u"groupbox_urls")
        self.groupbox_urls.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.groupbox_urls)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_url_file = QLabel(self.groupbox_urls)
        self.label_url_file.setObjectName(u"label_url_file")
        self.label_url_file.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 4px;\n"
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
"}")

        self.horizontalLayout.addWidget(self.label_url_file)

        self.lineedit_url_file = QLineEdit(self.groupbox_urls)
        self.lineedit_url_file.setObjectName(u"lineedit_url_file")
        self.lineedit_url_file.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
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
"    border-radius: 12px;\n"
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


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_user_channel = QLabel(self.groupbox_urls)
        self.label_user_channel.setObjectName(u"label_user_channel")
        self.label_user_channel.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 0.5px;\n"
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
"    border-radius: 12px;\n"
"	margin-right: 1px;\n"
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
"    border-radius: 12px;\n"
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


        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_url = QLabel(self.groupbox_urls)
        self.label_url.setObjectName(u"label_url")
        self.label_url.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 5px;\n"
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
"    border-radius: 12px;\n"
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
"    border-radius: 12px;\n"
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


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupbox_urls)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"color: white;\n"
"font-size: 14px;\n"
"border-width: 10px;")
        self.gridLayout_9 = QGridLayout(self.groupBox_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"color: white;")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.radio_highest = QRadioButton(self.groupBox_3)
        self.radio_highest.setObjectName(u"radio_highest")
        self.radio_highest.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_highest.setStyleSheet(u"QRadioButton {\n"
"	color: rgb(0, 255, 136)\n"
"}\n"
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
        self.radio_highest.setChecked(True)

        self.gridLayout_4.addWidget(self.radio_highest, 0, 0, 1, 1)

        self.radio_middle = QRadioButton(self.groupBox_3)
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

        self.gridLayout_4.addWidget(self.radio_middle, 1, 0, 1, 1)

        self.radio_lowest = QRadioButton(self.groupBox_3)
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

        self.gridLayout_4.addWidget(self.radio_lowest, 2, 0, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_3, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"color: white;\n"
"font-size: 14px;")
        self.gridLayout_8 = QGridLayout(self.groupBox_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.radio_threading_multiple = QRadioButton(self.groupBox_4)
        self.radio_threading_multiple.setObjectName(u"radio_threading_multiple")
        self.radio_threading_multiple.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_threading_multiple.setStyleSheet(u"QRadioButton {\n"
"	color: rgb(0, 255, 110);}\n"
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
        self.radio_threading_multiple.setChecked(True)

        self.gridLayout_8.addWidget(self.radio_threading_multiple, 0, 0, 1, 1)

        self.radio_threading_single = QRadioButton(self.groupBox_4)
        self.radio_threading_single.setObjectName(u"radio_threading_single")
        self.radio_threading_single.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_threading_single.setStyleSheet(u"QRadioButton {\n"
"	color: rgb(246, 0, 255);}\n"
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
        self.radio_threading_single.setChecked(False)

        self.gridLayout_8.addWidget(self.radio_threading_single, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_4, 0, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_output = QLabel(self.groupBox_2)
        self.label_output.setObjectName(u"label_output")
        self.label_output.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font-size: 14px;")

        self.horizontalLayout_7.addWidget(self.label_output)

        self.lineedit_output = QLineEdit(self.groupBox_2)
        self.lineedit_output.setObjectName(u"lineedit_output")
        self.lineedit_output.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
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

        self.horizontalLayout_7.addWidget(self.lineedit_output)


        self.gridLayout_9.addLayout(self.horizontalLayout_7, 1, 0, 1, 2)


        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupbox_urls, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupbox_metadata = QGroupBox(self.page_2)
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
"    border-radius: 12px;\n"
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


        self.gridLayout_3.addWidget(self.groupbox_metadata, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_6 = QGridLayout(self.page_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.credits_text = QTextBrowser(self.page_3)
        self.credits_text.setObjectName(u"credits_text")
        self.credits_text.setStyleSheet(u"background-color: rgb(0, 0, 0)")

        self.gridLayout_6.addWidget(self.credits_text, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_11 = QGridLayout(self.page_4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.button_download_search_query = QPushButton(self.page_4)
        self.button_download_search_query.setObjectName(u"button_download_search_query")
        self.button_download_search_query.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download_search_query.setStyleSheet(u"QPushButton {\n"
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

        self.gridLayout_11.addWidget(self.button_download_search_query, 1, 0, 1, 1)

        self.groupBox_5 = QGroupBox(self.page_4)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_10 = QGridLayout(self.groupBox_5)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color: white;\n"
"font-size: 17px;")

        self.gridLayout_10.addWidget(self.label_2, 3, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_total_videos = QLabel(self.groupBox_5)
        self.label_total_videos.setObjectName(u"label_total_videos")
        self.label_total_videos.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 11px;\n"
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

        self.horizontalLayout_3.addWidget(self.label_total_videos)

        self.lineedit_total_videos = QLineEdit(self.groupBox_5)
        self.lineedit_total_videos.setObjectName(u"lineedit_total_videos")
        self.lineedit_total_videos.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_total_videos.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.lineedit_total_videos)


        self.gridLayout_10.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_search_query = QLabel(self.groupBox_5)
        self.label_search_query.setObjectName(u"label_search_query")
        self.label_search_query.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 1px;\n"
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

        self.horizontalLayout_5.addWidget(self.label_search_query)

        self.lineedit_search_query = QLineEdit(self.groupBox_5)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        self.lineedit_search_query.setStyleSheet(u"QLineEdit {\n"
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

        self.horizontalLayout_5.addWidget(self.lineedit_search_query)

        self.button_start_search = QPushButton(self.groupBox_5)
        self.button_start_search.setObjectName(u"button_start_search")
        self.button_start_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start_search.setStyleSheet(u"QPushButton {\n"
"    background-color: #5468ff;\n"
"	border-width: 2px;\n"
"	border-color: rgb(98, 255, 182);\n"
"	border-style: double;\n"
"    border-radius: 12px;\n"
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

        self.horizontalLayout_5.addWidget(self.button_start_search)


        self.gridLayout_10.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"color: white;\n"
"font-size: 17px;")

        self.gridLayout_10.addWidget(self.label, 2, 0, 1, 1)

        self.treeWidget = QTreeWidget(self.groupBox_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"color: white;\n"
"background-color: rgb(109, 109, 109)")

        self.gridLayout_10.addWidget(self.treeWidget, 4, 0, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_4)

        self.gridLayout_12.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.progressbar_download = QProgressBar(self.groupBox)
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
"	border-radius: 12px;\n"
"}\n"
"")
        self.progressbar_download.setValue(0)

        self.gridLayout_7.addWidget(self.progressbar_download, 0, 0, 1, 1)

        self.label_search_query_progress = QLabel(self.groupBox)
        self.label_search_query_progress.setObjectName(u"label_search_query_progress")
        self.label_search_query_progress.setStyleSheet(u"color: white")

        self.gridLayout_7.addWidget(self.label_search_query_progress, 1, 0, 1, 1)


        self.gridLayout_12.addWidget(self.groupBox, 1, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.button_download_tab = QPushButton(Widget)
        self.button_download_tab.setObjectName(u"button_download_tab")
        self.button_download_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(0, 255, 234);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(255, 0, 136); \n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")

        self.horizontalLayout_6.addWidget(self.button_download_tab)

        self.button_metadata_tab = QPushButton(Widget)
        self.button_metadata_tab.setObjectName(u"button_metadata_tab")
        self.button_metadata_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(132, 255, 0);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(255, 0, 136); \n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")

        self.horizontalLayout_6.addWidget(self.button_metadata_tab)

        self.button_credits_tab = QPushButton(Widget)
        self.button_credits_tab.setObjectName(u"button_credits_tab")
        self.button_credits_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(255, 0, 136); \n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")

        self.horizontalLayout_6.addWidget(self.button_credits_tab)

        self.button_search_tab = QPushButton(Widget)
        self.button_search_tab.setObjectName(u"button_search_tab")
        self.button_search_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(119, 0, 255);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(255, 0, 136); \n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")

        self.horizontalLayout_6.addWidget(self.button_search_tab)


        self.gridLayout_12.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)


        self.retranslateUi(Widget)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Porn Fetch 1.6 (LGPLv3) : https://github.com/EchterAlsFake/Porn_Fetch", None))
        self.groupbox_urls.setTitle("")
        self.label_url_file.setText(QCoreApplication.translate("Widget", u"File with URLs:", None))
        self.button_start_file.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label_user_channel.setText(QCoreApplication.translate("Widget", u"User / Channel:", None))
        self.button_start_user_channel.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label_url.setText(QCoreApplication.translate("Widget", u"URL:", None))
        self.button_start.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Widget", u"Settings", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Widget", u"Quality:", None))
        self.radio_highest.setText(QCoreApplication.translate("Widget", u"Highest", None))
        self.radio_middle.setText(QCoreApplication.translate("Widget", u"Middle", None))
        self.radio_lowest.setText(QCoreApplication.translate("Widget", u"Lowest", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Widget", u"Threading:", None))
        self.radio_threading_multiple.setText(QCoreApplication.translate("Widget", u"Multiple", None))
        self.radio_threading_single.setText(QCoreApplication.translate("Widget", u"Single", None))
        self.label_output.setText(QCoreApplication.translate("Widget", u"Output Path:", None))
        self.lineedit_output.setText(QCoreApplication.translate("Widget", u"./", None))
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
        self.credits_text.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Credits:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bl"
                        "ock-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">API: PHUB by Egsagon.  This project would not be possible without it.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Author: EchterAlsFake</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">License: LGPLv3</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; "
                        "font-size:11pt; color:#ffffff;\">Plugins: Tabnine, Material Theme Icons</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Libraries: colorama, tqdm, PySide6, PHUB</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Graphical User Interface was created with Qt - PySide6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Version: 1.5<"
                        "/span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p></body></html>", None))
        self.button_download_search_query.setText(QCoreApplication.translate("Widget", u"Download", None))
        self.groupBox_5.setTitle("")
        self.label_2.setText(QCoreApplication.translate("Widget", u"Just click on it, and select all videos you want to download!", None))
        self.label_total_videos.setText(QCoreApplication.translate("Widget", u"Total Videos:", None))
        self.label_search_query.setText(QCoreApplication.translate("Widget", u"Search Query:", None))
        self.button_start_search.setText(QCoreApplication.translate("Widget", u"Search", None))
        self.label.setText(QCoreApplication.translate("Widget", u"On the left side, there are check boxes. They only appear if you select them.", None))
        self.groupBox.setTitle("")
        self.label_search_query_progress.setText(QCoreApplication.translate("Widget", u"Downloaded: / of / Videos", None))
        self.button_download_tab.setText(QCoreApplication.translate("Widget", u"Download Tab", None))
        self.button_metadata_tab.setText(QCoreApplication.translate("Widget", u"Metadata Tab", None))
        self.button_credits_tab.setText(QCoreApplication.translate("Widget", u"Credits", None))
        self.button_search_tab.setText(QCoreApplication.translate("Widget", u"Search Videos ", None))
    # retranslateUi

