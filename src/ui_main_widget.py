# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_redesign.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QProgressBar, QPushButton, QRadioButton, QSizePolicy,
    QSlider, QStackedWidget, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1152, 518)
        Porn_Fetch_Widget.setStyleSheet(u"background-color: rgb(18,18,18);\n"
"color: white;")
        self.gridLayout_13 = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.groupBox = QGroupBox(Porn_Fetch_Widget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
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

        self.gridLayout.addWidget(self.progressbar_download, 4, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_url = QLabel(self.groupBox)
        self.label_url.setObjectName(u"label_url")

        self.horizontalLayout.addWidget(self.label_url)

        self.lineedit_url = QLineEdit(self.groupBox)
        self.lineedit_url.setObjectName(u"lineedit_url")
        self.lineedit_url.setCursor(QCursor(Qt.IBeamCursor))
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

        self.horizontalLayout.addWidget(self.lineedit_url)

        self.button_start = QPushButton(self.groupBox)
        self.button_start.setObjectName(u"button_start")
        self.button_start.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 20px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout.addWidget(self.button_start)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_user_channel = QLabel(self.groupBox)
        self.label_user_channel.setObjectName(u"label_user_channel")

        self.horizontalLayout_3.addWidget(self.label_user_channel)

        self.lineedit_user_channel = QLineEdit(self.groupBox)
        self.lineedit_user_channel.setObjectName(u"lineedit_user_channel")
        self.lineedit_user_channel.setStyleSheet(u"QLineEdit {\n"
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

        self.horizontalLayout_3.addWidget(self.lineedit_user_channel)

        self.button_start_user_channel = QPushButton(self.groupBox)
        self.button_start_user_channel.setObjectName(u"button_start_user_channel")
        self.button_start_user_channel.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start_user_channel.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 20px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_3.addWidget(self.button_start_user_channel)


        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_url_file = QLabel(self.groupBox)
        self.label_url_file.setObjectName(u"label_url_file")

        self.horizontalLayout_2.addWidget(self.label_url_file)

        self.lineedit_url_file = QLineEdit(self.groupBox)
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

        self.horizontalLayout_2.addWidget(self.lineedit_url_file)

        self.button_start_file = QPushButton(self.groupBox)
        self.button_start_file.setObjectName(u"button_start_file")
        self.button_start_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start_file.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 20px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_2.addWidget(self.button_start_file)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_output = QLabel(self.groupBox)
        self.label_output.setObjectName(u"label_output")

        self.horizontalLayout_20.addWidget(self.label_output)

        self.lineedit_output = QLineEdit(self.groupBox)
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

        self.horizontalLayout_20.addWidget(self.lineedit_output)


        self.gridLayout.addLayout(self.horizontalLayout_20, 3, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox, 0, 0, 1, 2)

        self.groupBox_3 = QGroupBox(Porn_Fetch_Widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.stackedWidget = QStackedWidget(self.groupBox_3)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_search = QWidget()
        self.page_search.setObjectName(u"page_search")
        self.gridLayout_4 = QGridLayout(self.page_search)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.button_download_search_query = QPushButton(self.page_search)
        self.button_download_search_query.setObjectName(u"button_download_search_query")
        self.button_download_search_query.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download_search_query.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_9.addWidget(self.button_download_search_query)

        self.button_search_fix = QPushButton(self.page_search)
        self.button_search_fix.setObjectName(u"button_search_fix")
        self.button_search_fix.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_search_fix.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_9.addWidget(self.button_search_fix)


        self.gridLayout_4.addLayout(self.horizontalLayout_9, 2, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_search_query = QLabel(self.page_search)
        self.label_search_query.setObjectName(u"label_search_query")

        self.horizontalLayout_8.addWidget(self.label_search_query)

        self.lineedit_search_query = QLineEdit(self.page_search)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        self.lineedit_search_query.setStyleSheet(u"QLineEdit {\n"
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

        self.horizontalLayout_8.addWidget(self.lineedit_search_query)

        self.button_start_search = QPushButton(self.page_search)
        self.button_start_search.setObjectName(u"button_start_search")
        self.button_start_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_start_search.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_8.addWidget(self.button_start_search)


        self.gridLayout_4.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)

        self.treeWidget = QTreeWidget(self.page_search)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"background-color: rgb(94, 94, 94);\n"
"color: white;")

        self.gridLayout_4.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_search)
        self.page_metadata = QWidget()
        self.page_metadata.setObjectName(u"page_metadata")
        self.gridLayout_10 = QGridLayout(self.page_metadata)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.groupBox_8 = QGroupBox(self.page_metadata)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_9 = QGridLayout(self.groupBox_8)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_title = QLabel(self.groupBox_8)
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

        self.lineedit_title = QLineEdit(self.groupBox_8)
        self.lineedit_title.setObjectName(u"lineedit_title")
        self.lineedit_title.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_title.setReadOnly(True)

        self.horizontalLayout_16.addWidget(self.lineedit_title)


        self.gridLayout_9.addLayout(self.horizontalLayout_16, 0, 0, 1, 1)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_image_url = QLabel(self.groupBox_8)
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

        self.lineedit_image_url = QLineEdit(self.groupBox_8)
        self.lineedit_image_url.setObjectName(u"lineedit_image_url")
        self.lineedit_image_url.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_image_url.setReadOnly(True)

        self.horizontalLayout_14.addWidget(self.lineedit_image_url)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_likes = QLabel(self.groupBox_8)
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

        self.lineedit_likes = QLineEdit(self.groupBox_8)
        self.lineedit_likes.setObjectName(u"lineedit_likes")
        self.lineedit_likes.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_likes.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.lineedit_likes)


        self.horizontalLayout_14.addLayout(self.horizontalLayout_15)


        self.gridLayout_9.addLayout(self.horizontalLayout_14, 2, 0, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_tags = QLabel(self.groupBox_8)
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

        self.lineedit_tags = QLineEdit(self.groupBox_8)
        self.lineedit_tags.setObjectName(u"lineedit_tags")
        self.lineedit_tags.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_tags.setReadOnly(True)

        self.horizontalLayout_13.addWidget(self.lineedit_tags)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_author = QLabel(self.groupBox_8)
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

        self.lineedit_author = QLineEdit(self.groupBox_8)
        self.lineedit_author.setObjectName(u"lineedit_author")
        self.lineedit_author.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_author.setReadOnly(True)

        self.horizontalLayout_12.addWidget(self.lineedit_author)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_12)


        self.gridLayout_9.addLayout(self.horizontalLayout_13, 3, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_views = QLabel(self.groupBox_8)
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

        self.lineedit_views = QLineEdit(self.groupBox_8)
        self.lineedit_views.setObjectName(u"lineedit_views")
        self.lineedit_views.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_views.setReadOnly(True)

        self.horizontalLayout_11.addWidget(self.lineedit_views)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_date = QLabel(self.groupBox_8)
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

        self.lineedit_date = QLineEdit(self.groupBox_8)
        self.lineedit_date.setObjectName(u"lineedit_date")
        self.lineedit_date.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_date.setReadOnly(True)

        self.horizontalLayout_10.addWidget(self.lineedit_date)


        self.horizontalLayout_11.addLayout(self.horizontalLayout_10)


        self.gridLayout_9.addLayout(self.horizontalLayout_11, 5, 0, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_duration = QLabel(self.groupBox_8)
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

        self.horizontalLayout_17.addWidget(self.label_duration)

        self.lineedit_duration = QLineEdit(self.groupBox_8)
        self.lineedit_duration.setObjectName(u"lineedit_duration")
        self.lineedit_duration.setAutoFillBackground(False)
        self.lineedit_duration.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_duration.setReadOnly(True)

        self.horizontalLayout_17.addWidget(self.lineedit_duration)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_hotspots = QLabel(self.groupBox_8)
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

        self.horizontalLayout_18.addWidget(self.label_hotspots)

        self.lineedit_hotspots = QLineEdit(self.groupBox_8)
        self.lineedit_hotspots.setObjectName(u"lineedit_hotspots")
        self.lineedit_hotspots.setAutoFillBackground(False)
        self.lineedit_hotspots.setStyleSheet(u"QLineEdit {\n"
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
        self.lineedit_hotspots.setReadOnly(True)

        self.horizontalLayout_18.addWidget(self.lineedit_hotspots)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_18)


        self.gridLayout_9.addLayout(self.horizontalLayout_17, 7, 0, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.button_get_metadata = QPushButton(self.groupBox_8)
        self.button_get_metadata.setObjectName(u"button_get_metadata")
        self.button_get_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_metadata.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_19.addWidget(self.button_get_metadata)

        self.button_download_thumbnail = QPushButton(self.groupBox_8)
        self.button_download_thumbnail.setObjectName(u"button_download_thumbnail")
        self.button_download_thumbnail.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download_thumbnail.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_19.addWidget(self.button_download_thumbnail)


        self.gridLayout_9.addLayout(self.horizontalLayout_19, 8, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_8, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_metadata)
        self.page_credits = QWidget()
        self.page_credits.setObjectName(u"page_credits")
        self.gridLayout_11 = QGridLayout(self.page_credits)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.textBrowser_2 = QTextBrowser(self.page_credits)
        self.textBrowser_2.setObjectName(u"textBrowser_2")

        self.gridLayout_11.addWidget(self.textBrowser_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_credits)

        self.gridLayout_3.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_3, 1, 0, 1, 2)

        self.groupBox_2 = QGroupBox(Porn_Fetch_Widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_8 = QGridLayout(self.groupBox_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridlayout_ui_language = QGridLayout()
        self.gridlayout_ui_language.setObjectName(u"gridlayout_ui_language")
        self.label_debug = QLabel(self.groupBox_2)
        self.label_debug.setObjectName(u"label_debug")

        self.gridlayout_ui_language.addWidget(self.label_debug, 1, 0, 1, 1)

        self.settings_checkbox_sentry = QCheckBox(self.groupBox_2)
        self.settings_checkbox_sentry.setObjectName(u"settings_checkbox_sentry")
        self.settings_checkbox_sentry.setCursor(QCursor(Qt.PointingHandCursor))
        self.settings_checkbox_sentry.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid white;\n"
"    background: white;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(graphics/checkmark.png);\n"
"}")

        self.gridlayout_ui_language.addWidget(self.settings_checkbox_sentry, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridlayout_ui_language.addWidget(self.label_2, 0, 0, 1, 1)

        self.settings_checkbox_logging = QCheckBox(self.groupBox_2)
        self.settings_checkbox_logging.setObjectName(u"settings_checkbox_logging")
        self.settings_checkbox_logging.setCursor(QCursor(Qt.PointingHandCursor))
        self.settings_checkbox_logging.setStyleSheet(u"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 1px solid white;\n"
"    background: white;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(graphics/checkmark.png);\n"
"}")

        self.gridlayout_ui_language.addWidget(self.settings_checkbox_logging, 1, 2, 1, 1)

        self.application_language_en = QRadioButton(self.groupBox_2)
        self.application_language_en.setObjectName(u"application_language_en")
        self.application_language_en.setCursor(QCursor(Qt.PointingHandCursor))
        self.application_language_en.setStyleSheet(u"QRadioButton {\n"
"	color: (255,255,255)}\n"
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
        self.application_language_en.setChecked(False)

        self.gridlayout_ui_language.addWidget(self.application_language_en, 0, 1, 1, 1)

        self.radio_threading_single_2 = QRadioButton(self.groupBox_2)
        self.radio_threading_single_2.setObjectName(u"radio_threading_single_2")
        self.radio_threading_single_2.setStyleSheet(u"QRadioButton {\n"
"	color: rgb(255, 238, 0)}\n"
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

        self.gridlayout_ui_language.addWidget(self.radio_threading_single_2, 2, 2, 1, 1)

        self.radio_threading_multiple_2 = QRadioButton(self.groupBox_2)
        self.radio_threading_multiple_2.setObjectName(u"radio_threading_multiple_2")
        self.radio_threading_multiple_2.setStyleSheet(u"QRadioButton {\n"
"	color: rgb(178, 0, 255)}\n"
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
        self.radio_threading_multiple_2.setChecked(True)

        self.gridlayout_ui_language.addWidget(self.radio_threading_multiple_2, 2, 1, 1, 1)

        self.label_threading_mode_2 = QLabel(self.groupBox_2)
        self.label_threading_mode_2.setObjectName(u"label_threading_mode_2")

        self.gridlayout_ui_language.addWidget(self.label_threading_mode_2, 2, 0, 1, 1)


        self.gridLayout_8.addLayout(self.gridlayout_ui_language, 1, 1, 1, 2)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_8.addWidget(self.label_3, 2, 0, 1, 1)

        self.horizontal_quality = QHBoxLayout()
        self.horizontal_quality.setObjectName(u"horizontal_quality")
        self.label_quality = QLabel(self.groupBox_2)
        self.label_quality.setObjectName(u"label_quality")

        self.horizontal_quality.addWidget(self.label_quality)

        self.radio_highest = QRadioButton(self.groupBox_2)
        self.radio_highest.setObjectName(u"radio_highest")
        self.radio_highest.setStyleSheet(u"QRadioButton {\n"
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
        self.radio_highest.setChecked(True)

        self.horizontal_quality.addWidget(self.radio_highest)

        self.radio_middle = QRadioButton(self.groupBox_2)
        self.radio_middle.setObjectName(u"radio_middle")
        self.radio_middle.setStyleSheet(u"QRadioButton {\n"
"	color: rgb(255, 162, 0)}\n"
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

        self.horizontal_quality.addWidget(self.radio_middle)

        self.radio_lowest = QRadioButton(self.groupBox_2)
        self.radio_lowest.setObjectName(u"radio_lowest")
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
"\n"
"")

        self.horizontal_quality.addWidget(self.radio_lowest)


        self.gridLayout_8.addLayout(self.horizontal_quality, 0, 0, 1, 3)

        self.gridlayout_api_language = QGridLayout()
        self.gridlayout_api_language.setObjectName(u"gridlayout_api_language")
        self.api_radio_fr = QRadioButton(self.groupBox_2)
        self.api_radio_fr.setObjectName(u"api_radio_fr")
        self.api_radio_fr.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_fr.setStyleSheet(u"QRadioButton {\n"
"	color: (255,255,255)}\n"
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

        self.gridlayout_api_language.addWidget(self.api_radio_fr, 2, 1, 1, 1)

        self.api_radio_de = QRadioButton(self.groupBox_2)
        self.api_radio_de.setObjectName(u"api_radio_de")
        self.api_radio_de.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_de.setStyleSheet(u"QRadioButton {\n"
"	color: (255,255,255)}\n"
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

        self.gridlayout_api_language.addWidget(self.api_radio_de, 2, 0, 1, 1)

        self.api_radio_ru = QRadioButton(self.groupBox_2)
        self.api_radio_ru.setObjectName(u"api_radio_ru")
        self.api_radio_ru.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_ru.setStyleSheet(u"QRadioButton {\n"
"	color: (255,255,255)}\n"
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

        self.gridlayout_api_language.addWidget(self.api_radio_ru, 3, 0, 1, 1)

        self.api_radio_es = QRadioButton(self.groupBox_2)
        self.api_radio_es.setObjectName(u"api_radio_es")
        self.api_radio_es.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_es.setStyleSheet(u"QRadioButton {\n"
"	color: (255,255,255)}\n"
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

        self.gridlayout_api_language.addWidget(self.api_radio_es, 1, 1, 1, 1)

        self.api_radio_en = QRadioButton(self.groupBox_2)
        self.api_radio_en.setObjectName(u"api_radio_en")
        self.api_radio_en.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_en.setStyleSheet(u"QRadioButton {\n"
"	color: (255,255,255)}\n"
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
        self.api_radio_en.setChecked(True)

        self.gridlayout_api_language.addWidget(self.api_radio_en, 1, 0, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridlayout_api_language.addWidget(self.label, 0, 0, 1, 2)


        self.gridLayout_8.addLayout(self.gridlayout_api_language, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.button_settings_apply = QPushButton(self.groupBox_2)
        self.button_settings_apply.setObjectName(u"button_settings_apply")
        self.button_settings_apply.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_settings_apply.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_7.addWidget(self.button_settings_apply)

        self.button_settings_help = QPushButton(self.groupBox_2)
        self.button_settings_help.setObjectName(u"button_settings_help")
        self.button_settings_help.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_settings_help.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.horizontalLayout_7.addWidget(self.button_settings_help)


        self.gridLayout_8.addLayout(self.horizontalLayout_7, 4, 0, 1, 3)

        self.horizontalSlider = QSlider(self.groupBox_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"        border: none;\n"
"        background: #3f1d4d; /* base groove color to match the button's disabled state */\n"
"        height: 8px; /* height of the groove */\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"    QSlider::handle:horizontal {\n"
"        background: #5a2a82; /* base handle color to match the button */\n"
"        width: 16px; /* width of the handle */\n"
"        height: 16px; /* height of the handle */\n"
"        border-radius: 8px; /* make it circular */\n"
"        margin: -4px 0; /* to center the handle vertically */\n"
"    }\n"
"\n"
"    QSlider::handle:horizontal:hover {\n"
"        background: #7b3ca3;\n"
"    }\n"
"\n"
"    QSlider::handle:horizontal:pressed {\n"
"        background: #481f61;\n"
"    }\n"
"\n"
"    QSlider::sub-page:horizontal {\n"
"        background-color: #5a2a82;\n"
"        border-radius: 4px;\n"
"    }")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setValue(0)
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)

        self.gridLayout_8.addWidget(self.horizontalSlider, 2, 1, 1, 2)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_8.addWidget(self.label_4, 3, 1, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_8.addWidget(self.label_5, 3, 2, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_2, 0, 2, 1, 1)

        self.groupBox_4 = QGroupBox(Porn_Fetch_Widget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_5 = QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.textBrowser = QTextBrowser(self.groupBox_4)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_5.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_4, 1, 2, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch v2.1", None))
        self.groupBox.setTitle("")
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u" URL: ", None))
        self.button_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_user_channel.setText(QCoreApplication.translate("Porn_Fetch_Widget", u" Model / Channel: ", None))
        self.button_start_user_channel.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_url_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u" File:  ", None))
        self.button_start_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_output.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Output path:         ", None))
        self.lineedit_output.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"./", None))
        self.groupBox_3.setTitle("")
        self.button_download_search_query.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.button_search_fix.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Automatically fixing issues (No 100% guarantee)", None))
        self.label_search_query.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.button_start_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.groupBox_8.setTitle("")
        self.label_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Title:", None))
        self.label_image_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Image URL", None))
        self.label_likes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Likes:", None))
        self.label_tags.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tags:", None))
        self.label_author.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Author: ", None))
        self.label_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Views:", None))
        self.label_date.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Date:", None))
        self.label_duration.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Duration:", None))
        self.label_hotspots.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hotspots:", None))
        self.button_get_metadata.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get metadata", None))
        self.button_download_thumbnail.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download thumbnail", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("Porn_Fetch_Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Porn Fetch is created and maintained by EchterAlsFake | Johannes Habel.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">EchterAlsFake is the internet pseudonym for Johannes Habel.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; ma"
                        "rgin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">The software is licensed under the GPL 3.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">The official Source code is available on GitHub:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" color:#ffffff;\">https://github.com/EchterAlsFake/Porn_Fetch</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">This software uses some external libraries that are out of my control.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">These are:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /><"
                        "/p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'JetBrains Mono','monospace'; color:#bcbec4; background-color:#1e1f22;\">phub</span><span style=\" font-family:'JetBrains Mono','monospace'; color:#bcbec4;\"><br />PySide6<br />colorama<br />bs4<br />tqdm<br />sentry-sdk<br />wget<br />requests<br />js2py</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Graphics:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; marg"
                        "in-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Download Icon : https://icons8.com/icon/104149/herunterladen</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Search Icon : https://icons8.com/icon/aROEUCBo74Il/suche</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Settings Icon : https://icons8.com/icon/52146/einstellungen</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">C Icon : https://icons8.com/icon/Uehg4gyVyrUo/copyright</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">M Icon By Unicons Font on Icon Sco"
                        "ut : https://iconscout.com/icons/medium : https://iconscout.com/contributors/unicons</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">: https://iconscout.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Checkmark Icon: </span><span style=\" font-family:'JetBrains Mono','monospace'; color:#6a8759;\">https://www.iconsdb.com/barbie-pink-icons/checkmark-icon.html</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">A special thanks to Egsagon for creating PHUB.</span></p>\n"
"<p style=\" mar"
                        "gin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">This project would not be possible without his great API and I have much respect for him!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">2.1 - 2023</span></p></body></html>", None))
        self.groupBox_2.setTitle("")
        self.label_debug.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Debug:", None))
        self.settings_checkbox_sentry.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Sentry", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Choose UI language", None))
        self.settings_checkbox_logging.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Logging", None))
        self.application_language_en.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"EN", None))
        self.radio_threading_single_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.radio_threading_multiple_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.label_threading_mode_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading:", None))
        self.label_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"UI Transparency:", None))
        self.label_quality.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Quality:", None))
        self.radio_highest.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Best", None))
        self.radio_middle.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Middle", None))
        self.radio_lowest.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Worst", None))
        self.api_radio_fr.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"FR", None))
        self.api_radio_de.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"DE", None))
        self.api_radio_ru.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"RU", None))
        self.api_radio_es.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"ES", None))
        self.api_radio_en.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"EN", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Choose API language", None))
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Apply", None))
        self.button_settings_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
#if QT_CONFIG(tooltip)
        self.horizontalSlider.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Set transparency for UI in %. Gives a better UX on DEs like Hyprland", None))
#endif // QT_CONFIG(tooltip)
        self.label_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"More", None))
        self.label_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"                                       Less", None))
        self.groupBox_4.setTitle("")
        self.textBrowser.setHtml(QCoreApplication.translate("Porn_Fetch_Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:20pt; font-weight:700; color:#ffffff;\">      Keyboard Shortcuts</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:20pt; font-weight:700; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bl"
                        "ock-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">1) CTRL + W	:  Exit		</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">2) CTRL + S	:  Search Tab</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">3) CTRL + M	:  Meatadata Tab	</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">4) CTRL + C	:  Show credits</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">5) CTRL + R	:  Reset config		</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" c"
                        "olor:#ffffff;\">6) CTRL + L	:  Set custom API language (exp.) </span></p></body></html>", None))
    # retranslateUi

