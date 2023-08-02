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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QStackedWidget, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1221, 528)
        Widget.setStyleSheet(u"background-color: rgb(0, 0, 0)")
        self.stackedWidget = QStackedWidget(Widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(140, 10, 1081, 441))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupbox_urls = QGroupBox(self.page)
        self.groupbox_urls.setObjectName(u"groupbox_urls")
        self.groupbox_urls.setStyleSheet(u"border: none;")
        self.gridLayout = QGridLayout(self.groupbox_urls)
        self.gridLayout.setObjectName(u"gridLayout")
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

        self.groupBox_2 = QGroupBox(self.groupbox_urls)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"color: white;\n"
"font-size: 14px;\n"
"border: none;")
        self.gridLayout_9 = QGridLayout(self.groupBox_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
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

        self.gridLayout_8.addWidget(self.radio_threading_multiple, 1, 0, 1, 1)

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

        self.gridLayout_8.addWidget(self.radio_threading_single, 2, 0, 1, 1)

        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_8.addWidget(self.label_4, 0, 0, 1, 1)


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

        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"color: white;\n"
"border: none;")
        self.gridLayout_4 = QGridLayout(self.groupBox_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
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

        self.gridLayout_4.addWidget(self.radio_lowest, 3, 0, 1, 1)

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

        self.gridLayout_4.addWidget(self.radio_highest, 1, 0, 1, 1)

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

        self.gridLayout_4.addWidget(self.radio_middle, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)

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


        self.gridLayout_2.addWidget(self.groupbox_urls, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_3 = QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.groupbox_metadata = QGroupBox(self.page_2)
        self.groupbox_metadata.setObjectName(u"groupbox_metadata")
        self.groupbox_metadata.setStyleSheet(u"color: rgb(255, 255, 255)")
        self.horizontalLayoutWidget = QWidget(self.groupbox_metadata)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 380, 1051, 41))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.button_get_metadata = QPushButton(self.horizontalLayoutWidget)
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

        self.horizontalLayout_6.addWidget(self.button_get_metadata)

        self.button_metadata_refresh = QPushButton(self.horizontalLayoutWidget)
        self.button_metadata_refresh.setObjectName(u"button_metadata_refresh")
        self.button_metadata_refresh.setStyleSheet(u"QPushButton {\n"
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
"}")

        self.horizontalLayout_6.addWidget(self.button_metadata_refresh)

        self.groupBox_7 = QGroupBox(self.groupbox_metadata)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(0, 0, 1061, 381))
        self.gridLayout_5 = QGridLayout(self.groupBox_7)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_title = QLabel(self.groupBox_7)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 55px;\n"
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

        self.horizontalLayout_16.addWidget(self.label_title)

        self.lineedit_title = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_16.addWidget(self.lineedit_title)


        self.gridLayout_5.addLayout(self.horizontalLayout_16, 0, 0, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_likes = QLabel(self.groupBox_7)
        self.label_likes.setObjectName(u"label_likes")
        self.label_likes.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 49px;\n"
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

        self.horizontalLayout_15.addWidget(self.label_likes)

        self.lineedit_likes = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_15.addWidget(self.lineedit_likes)


        self.gridLayout_5.addLayout(self.horizontalLayout_15, 1, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_image_url = QLabel(self.groupBox_7)
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

        self.horizontalLayout_14.addWidget(self.label_image_url)

        self.lineedit_image_url = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_14.addWidget(self.lineedit_image_url)


        self.gridLayout_5.addLayout(self.horizontalLayout_14, 2, 0, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_tags = QLabel(self.groupBox_7)
        self.label_tags.setObjectName(u"label_tags")
        self.label_tags.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 53px;\n"
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

        self.horizontalLayout_13.addWidget(self.label_tags)

        self.lineedit_tags = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_13.addWidget(self.lineedit_tags)


        self.gridLayout_5.addLayout(self.horizontalLayout_13, 3, 0, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_author = QLabel(self.groupBox_7)
        self.label_author.setObjectName(u"label_author")
        self.label_author.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 35px;\n"
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

        self.horizontalLayout_12.addWidget(self.label_author)

        self.lineedit_author = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_12.addWidget(self.lineedit_author)


        self.gridLayout_5.addLayout(self.horizontalLayout_12, 4, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_views = QLabel(self.groupBox_7)
        self.label_views.setObjectName(u"label_views")
        self.label_views.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 44px;\n"
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

        self.horizontalLayout_11.addWidget(self.label_views)

        self.lineedit_views = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_11.addWidget(self.lineedit_views)


        self.gridLayout_5.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_date = QLabel(self.groupBox_7)
        self.label_date.setObjectName(u"label_date")
        self.label_date.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 53px;\n"
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

        self.horizontalLayout_10.addWidget(self.label_date)

        self.lineedit_date = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_10.addWidget(self.lineedit_date)


        self.gridLayout_5.addLayout(self.horizontalLayout_10, 6, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_duration = QLabel(self.groupBox_7)
        self.label_duration.setObjectName(u"label_duration")
        self.label_duration.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 25px;\n"
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

        self.horizontalLayout_9.addWidget(self.label_duration)

        self.lineedit_duration = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_9.addWidget(self.lineedit_duration)


        self.gridLayout_5.addLayout(self.horizontalLayout_9, 7, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_hotspots = QLabel(self.groupBox_7)
        self.label_hotspots.setObjectName(u"label_hotspots")
        self.label_hotspots.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 23px;\n"
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

        self.horizontalLayout_8.addWidget(self.label_hotspots)

        self.lineedit_hotspots = QLineEdit(self.groupBox_7)
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

        self.horizontalLayout_8.addWidget(self.lineedit_hotspots)


        self.gridLayout_5.addLayout(self.horizontalLayout_8, 8, 0, 1, 1)


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

        self.treeWidget = QTreeWidget(self.groupBox_5)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"color: white;\n"
"background-color: rgb(109, 109, 109)")

        self.gridLayout_10.addWidget(self.treeWidget, 3, 0, 1, 1)

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
        self.label.setStyleSheet(u"color: white;")

        self.gridLayout_10.addWidget(self.label, 2, 0, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.stackedWidget.addWidget(self.page_5)
        self.groupBox = QGroupBox(Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 450, 1211, 71))
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

        self.groupBox_6 = QGroupBox(Widget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(10, 10, 131, 431))
        self.formLayout = QFormLayout(self.groupBox_6)
        self.formLayout.setObjectName(u"formLayout")
        self.button_download_tab = QPushButton(self.groupBox_6)
        self.button_download_tab.setObjectName(u"button_download_tab")
        self.button_download_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(0, 255, 234);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(0, 234, 255);\n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")
        icon = QIcon()
        icon.addFile(u"graphics/download.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.button_download_tab.setIcon(icon)
        self.button_download_tab.setIconSize(QSize(32, 32))

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.button_download_tab)

        self.button_search_tab = QPushButton(self.groupBox_6)
        self.button_search_tab.setObjectName(u"button_search_tab")
        self.button_search_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(119, 0, 255);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(255, 179, 0);\n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"graphics/search.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.button_search_tab.setIcon(icon1)
        self.button_search_tab.setIconSize(QSize(32, 32))

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.button_search_tab)

        self.button_credits_tab = QPushButton(self.groupBox_6)
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
        icon2 = QIcon()
        icon2.addFile(u"graphics/c.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.button_credits_tab.setIcon(icon2)
        self.button_credits_tab.setIconSize(QSize(32, 32))

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.button_credits_tab)

        self.button_settings_tab = QPushButton(self.groupBox_6)
        self.button_settings_tab.setObjectName(u"button_settings_tab")
        self.button_settings_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(255, 255, 255);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(178, 0, 255);\n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u"graphics/settings-colorful.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.button_settings_tab.setIcon(icon3)
        self.button_settings_tab.setIconSize(QSize(32, 32))

        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.button_settings_tab)

        self.button_metadata_tab = QPushButton(self.groupBox_6)
        self.button_metadata_tab.setObjectName(u"button_metadata_tab")
        self.button_metadata_tab.setStyleSheet(u"QPushButton {\n"
"color: rgb(119, 0, 255);\n"
"border-width: 2px;\n"
"border-style: double;\n"
"border-color: rgb(0, 255, 81);\n"
"padding: 10px, 10px, 10px, 10px;\n"
"border-radius: 12px;\n"
"}\n"
"\n"
"QPushButton::hover {\n"
"border-width: 2px;\n"
"border-style: dotted;\n"
"border-color: rgb(255, 162, 0)\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u"graphics/medium.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.button_metadata_tab.setIcon(icon4)
        self.button_settings_tab.setIconSize(QSize(32, 32))

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.button_metadata_tab)


        self.retranslateUi(Widget)

        self.stackedWidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Porn Fetch 1.6 (LGPLv3) : https://github.com/EchterAlsFake/Porn_Fetch", None))
        self.groupbox_urls.setTitle("")
        self.label_user_channel.setText(QCoreApplication.translate("Widget", u"User / Channel:", None))
        self.button_start_user_channel.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.groupBox_2.setTitle("")
        self.groupBox_4.setTitle("")
        self.radio_threading_multiple.setText(QCoreApplication.translate("Widget", u"Multiple", None))
        self.radio_threading_single.setText(QCoreApplication.translate("Widget", u"Single", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Select Download mode (Threading)", None))
        self.label_output.setText(QCoreApplication.translate("Widget", u"Output Path:", None))
        self.lineedit_output.setText(QCoreApplication.translate("Widget", u"./", None))
        self.groupBox_3.setTitle("")
        self.radio_lowest.setText(QCoreApplication.translate("Widget", u"Lowest", None))
        self.radio_highest.setText(QCoreApplication.translate("Widget", u"Highest", None))
        self.radio_middle.setText(QCoreApplication.translate("Widget", u"Middle", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Select Quality:", None))
        self.label_url_file.setText(QCoreApplication.translate("Widget", u"File with URLs:", None))
        self.button_start_file.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label_url.setText(QCoreApplication.translate("Widget", u"URL:", None))
        self.button_start.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.groupbox_metadata.setTitle("")
        self.button_get_metadata.setText(QCoreApplication.translate("Widget", u"Get metadata", None))
        self.button_metadata_refresh.setText(QCoreApplication.translate("Widget", u"Refresh", None))
        self.groupBox_7.setTitle("")
        self.label_title.setText(QCoreApplication.translate("Widget", u"Title:", None))
        self.label_likes.setText(QCoreApplication.translate("Widget", u"Likes:", None))
        self.label_image_url.setText(QCoreApplication.translate("Widget", u"Image URL", None))
        self.label_tags.setText(QCoreApplication.translate("Widget", u"Tags:", None))
        self.label_author.setText(QCoreApplication.translate("Widget", u"Author: ", None))
        self.label_views.setText(QCoreApplication.translate("Widget", u"Views:", None))
        self.label_date.setText(QCoreApplication.translate("Widget", u"Date:", None))
        self.label_duration.setText(QCoreApplication.translate("Widget", u"Duration:", None))
        self.label_hotspots.setText(QCoreApplication.translate("Widget", u"Hotspots:", None))
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Author: EchterAlsFake | Johannes Habel</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">License: GPL 3</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-fami"
                        "ly:'Cantarell'; font-size:11pt; color:#ffffff;\">Plugins: Tabnine, Material Theme Icons, Sourcery</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Libraries: colorama, tqdm, PySide6, PHUB, Sentry SDK</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-size:11pt; color:#ffffff;\">Graphical User Interface was created with Qt - PySide6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Cantarell'; font-siz"
                        "e:11pt; color:#ffffff;\">Version: 1.7</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Cantarell'; font-size:11pt; color:#ffffff;\"><br /></p></body></html>", None))
        self.button_download_search_query.setText(QCoreApplication.translate("Widget", u"Download", None))
        self.groupBox_5.setTitle("")
        self.label_total_videos.setText(QCoreApplication.translate("Widget", u"Total Videos:", None))
        self.label_search_query.setText(QCoreApplication.translate("Widget", u"Search Query:", None))
        self.button_start_search.setText(QCoreApplication.translate("Widget", u"Search", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Do not use this feature too much, because you can get blocked by PornHub for a few minutes!", None))
        self.groupBox.setTitle("")
        self.label_search_query_progress.setText(QCoreApplication.translate("Widget", u"Downloaded: / of / Videos", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Widget", u"GroupBox", None))
        self.button_download_tab.setText("")
        self.button_search_tab.setText("")
        self.button_credits_tab.setText("")
        self.button_settings_tab.setText("")
        self.button_metadata_tab.setText(QCoreApplication.translate("Widget", u"etadata", None))
    # retranslateUi

