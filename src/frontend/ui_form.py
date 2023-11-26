# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
    QHeaderView, QLabel, QLineEdit, QProgressBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1758, 829)
        Porn_Fetch_Widget.setStyleSheet(u"QWidget {\n"
"color: white;\n"
"background-color: rgb(60, 60, 60);\n"
"border: none;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #DDD;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid #5599FF;\n"
"}\n"
"\n"
"\n"
"QProgressBar {\n"
"	color: rgb(255, 153, 0);\n"
"    border: 2px solid #5a2a82;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background-color: rgb(74, 74, 74);\n"
"    color: #ffffff;  /* Adding text color for better visibility */\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 255, 224);\n"
"    width: 10px; /* Adjust this to change the width of the 'chunk' */\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: #dcdcdc; /* Light grey text */\n"
"    spacing: 5px; /* Space between the radio button and its label */\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border-radius: 7px; /* Circular indicator */\n"
""
                        "}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    background-color: #555; /* Dark background for unchecked state */\n"
"    border: 2px solid #777; /* Slightly lighter border */\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #7a7aff; /* Bright color for checked state */\n"
"    border: 2px solid #5a5aff; /* Border slightly darker than the background */\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover,\n"
"QRadioButton::indicator:unchecked:hover {\n"
"    border-color: #9a9aff; /* Change border color on hover */\n"
"}\n"
"\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #5a2a82;\n"
"    height: 8px;\n"
"    background: #e0e0e0;\n"
"    margin: 0px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #5a2a82;\n"
"    border: 1px solid #5a2a82;\n"
"    width: 18px;\n"
"    margin: -6px 0;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #e0e0e0;\n"
"}\n"
"\n"
"QSlider::sub-page"
                        ":horizontal {\n"
"    background: #5a2a82;\n"
"}\n"
"\n"
"QTreeWidget {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: white;\n"
"}\n"
"\n"
"QTreeWidget QHeaderView::section {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: black; \n"
"    border: 1px solid #5a2a82;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 1ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }\n"
"\n"
"QLabel {\n"
"    color: #DDD;\n"
"    padding: 2px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #555;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5599FF;\n"
"}\n"
"\n"
""
                        "QCheckBox {\n"
"    color: #dcdcdc; /* Light grey text */\n"
"    spacing: 5px; /* Space between the checkbox and its label */\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border: 2px solid #777; /* Border color */\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    background-color: #555; /* Dark background for unchecked state */\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #7a7aff; /* Bright color for checked state */\n"
"    /* Here you can add your custom icon */\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    border-color: #9a9aff; /* Change border color on hover */\n"
"}\n"
"\n"
"QCheckBox::indicator:checked:hover {\n"
"    background-color: #8a8aff; /* Slightly lighter background on hover */\n"
"}")
        self.gridLayout_8 = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.HEADER = QVBoxLayout()
        self.HEADER.setObjectName(u"HEADER")

        self.gridLayout_8.addLayout(self.HEADER, 0, 0, 1, 3)

        self.widget = QWidget(Porn_Fetch_Widget)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"background-color: rgb(34, 34, 34)")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_switch_credits = QPushButton(self.widget)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        self.button_switch_credits.setMinimumSize(QSize(50, 50))
        self.button_switch_credits.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.button_switch_credits, 3, 0, 1, 1)

        self.button_switch_search = QPushButton(self.widget)
        self.button_switch_search.setObjectName(u"button_switch_search")
        self.button_switch_search.setMinimumSize(QSize(50, 50))
        self.button_switch_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_search.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.button_switch_search, 1, 0, 1, 1)

        self.button_switch_settings = QPushButton(self.widget)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        self.button_switch_settings.setMinimumSize(QSize(50, 50))
        self.button_switch_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.button_switch_settings, 2, 0, 1, 1)

        self.button_switch_home = QPushButton(self.widget)
        self.button_switch_home.setObjectName(u"button_switch_home")
        self.button_switch_home.setMinimumSize(QSize(50, 50))
        self.button_switch_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.button_switch_home, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget, 1, 0, 2, 2)

        self.widget_status = QWidget(Porn_Fetch_Widget)
        self.widget_status.setObjectName(u"widget_status")
        self.widget_status.setStyleSheet(u"background-color: rgb(34, 34, 34);\n"
"border-radius: 5px;")
        self.gridLayout_5 = QGridLayout(self.widget_status)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_current_progress = QLabel(self.widget_status)
        self.label_current_progress.setObjectName(u"label_current_progress")

        self.gridLayout_2.addWidget(self.label_current_progress, 0, 0, 1, 1)

        self.progressbar_current = QProgressBar(self.widget_status)
        self.progressbar_current.setObjectName(u"progressbar_current")
        self.progressbar_current.setValue(0)

        self.gridLayout_2.addWidget(self.progressbar_current, 0, 1, 1, 1)

        self.label_total_progress = QLabel(self.widget_status)
        self.label_total_progress.setObjectName(u"label_total_progress")

        self.gridLayout_2.addWidget(self.label_total_progress, 1, 0, 1, 1)

        self.progressbar_total = QProgressBar(self.widget_status)
        self.progressbar_total.setObjectName(u"progressbar_total")
        self.progressbar_total.setValue(0)

        self.gridLayout_2.addWidget(self.progressbar_total, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.gridlayout_status = QGridLayout()
        self.gridlayout_status.setObjectName(u"gridlayout_status")
        self.label_total = QLabel(self.widget_status)
        self.label_total.setObjectName(u"label_total")

        self.gridlayout_status.addWidget(self.label_total, 0, 2, 1, 1)

        self.lineedit_error = QLineEdit(self.widget_status)
        self.lineedit_error.setObjectName(u"lineedit_error")
        self.lineedit_error.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_error, 1, 1, 1, 1)

        self.label_error = QLabel(self.widget_status)
        self.label_error.setObjectName(u"label_error")

        self.gridlayout_status.addWidget(self.label_error, 1, 0, 1, 1)

        self.label_debug = QLabel(self.widget_status)
        self.label_debug.setObjectName(u"label_debug")

        self.gridlayout_status.addWidget(self.label_debug, 1, 2, 1, 1)

        self.label_status = QLabel(self.widget_status)
        self.label_status.setObjectName(u"label_status")

        self.gridlayout_status.addWidget(self.label_status, 0, 0, 1, 1)

        self.lineedit_status = QLineEdit(self.widget_status)
        self.lineedit_status.setObjectName(u"lineedit_status")
        self.lineedit_status.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_status, 0, 1, 1, 1)

        self.lineedit_total = QLineEdit(self.widget_status)
        self.lineedit_total.setObjectName(u"lineedit_total")
        self.lineedit_total.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_total, 0, 3, 1, 1)

        self.lineedit_debug = QLineEdit(self.widget_status)
        self.lineedit_debug.setObjectName(u"lineedit_debug")
        self.lineedit_debug.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_debug, 1, 3, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_status, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget_status, 2, 2, 1, 1)

        self.stacked_widget_main = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_7 = QGridLayout(self.page_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.treeWidget = QTreeWidget(self.page_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.gridLayout_7.addWidget(self.treeWidget, 2, 0, 1, 1)

        self.stacked_widget_top = QStackedWidget(self.page_3)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        self.stacked_widget_top.setCursor(QCursor(Qt.ArrowCursor))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_6 = QGridLayout(self.page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_file = QLabel(self.page)
        self.label_file.setObjectName(u"label_file")

        self.gridLayout_3.addWidget(self.label_file, 3, 0, 1, 1)

        self.button_open_file = QPushButton(self.page)
        self.button_open_file.setObjectName(u"button_open_file")
        self.button_open_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_open_file.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.button_open_file, 3, 2, 1, 1)

        self.lineedit_url = QLineEdit(self.page)
        self.lineedit_url.setObjectName(u"lineedit_url")

        self.gridLayout_3.addWidget(self.lineedit_url, 0, 1, 1, 1)

        self.button_search_videos = QPushButton(self.page)
        self.button_search_videos.setObjectName(u"button_search_videos")
        self.button_search_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_search_videos.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.button_search_videos, 4, 2, 1, 1)

        self.lineedit_file = QLineEdit(self.page)
        self.lineedit_file.setObjectName(u"lineedit_file")

        self.gridLayout_3.addWidget(self.lineedit_file, 3, 1, 1, 1)

        self.lineedit_search_query = QLineEdit(self.page)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")

        self.gridLayout_3.addWidget(self.lineedit_search_query, 4, 1, 1, 1)

        self.label_model_url = QLabel(self.page)
        self.label_model_url.setObjectName(u"label_model_url")

        self.gridLayout_3.addWidget(self.label_model_url, 2, 0, 1, 1)

        self.butgton_download = QPushButton(self.page)
        self.butgton_download.setObjectName(u"butgton_download")
        self.butgton_download.setCursor(QCursor(Qt.PointingHandCursor))
        self.butgton_download.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.butgton_download, 0, 2, 1, 1)

        self.label_search_query = QLabel(self.page)
        self.label_search_query.setObjectName(u"label_search_query")

        self.gridLayout_3.addWidget(self.label_search_query, 4, 0, 1, 1)

        self.label_url = QLabel(self.page)
        self.label_url.setObjectName(u"label_url")

        self.gridLayout_3.addWidget(self.label_url, 0, 0, 1, 1)

        self.button_model = QPushButton(self.page)
        self.button_model.setObjectName(u"button_model")
        self.button_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_model.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.button_model, 2, 2, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")

        self.gridLayout_3.addWidget(self.lineedit_model_url, 2, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.button_get_recommended_videos = QPushButton(self.page)
        self.button_get_recommended_videos.setObjectName(u"button_get_recommended_videos")
        self.button_get_recommended_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_recommended_videos.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #78909C, stop:1 #90A4AE);\n"
"}")

        self.gridLayout_4.addWidget(self.button_get_recommended_videos, 3, 2, 1, 1)

        self.label_password = QLabel(self.page)
        self.label_password.setObjectName(u"label_password")

        self.gridLayout_4.addWidget(self.label_password, 1, 0, 1, 1)

        self.button_get_liked_videos = QPushButton(self.page)
        self.button_get_liked_videos.setObjectName(u"button_get_liked_videos")
        self.button_get_liked_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_liked_videos.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #78909C, stop:1 #90A4AE);\n"
"}")

        self.gridLayout_4.addWidget(self.button_get_liked_videos, 3, 0, 1, 1)

        self.label_username = QLabel(self.page)
        self.label_username.setObjectName(u"label_username")

        self.gridLayout_4.addWidget(self.label_username, 0, 0, 1, 1)

        self.button_get_watched_videos = QPushButton(self.page)
        self.button_get_watched_videos.setObjectName(u"button_get_watched_videos")
        self.button_get_watched_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_watched_videos.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #78909C, stop:1 #90A4AE);\n"
"}")

        self.gridLayout_4.addWidget(self.button_get_watched_videos, 3, 1, 1, 1)

        self.button_login = QPushButton(self.page)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_login.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 8px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_4.addWidget(self.button_login, 2, 0, 1, 4)

        self.lineedit_password = QLineEdit(self.page)
        self.lineedit_password.setObjectName(u"lineedit_password")
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.gridLayout_4.addWidget(self.lineedit_password, 1, 1, 1, 3)

        self.lineedit_username = QLineEdit(self.page)
        self.lineedit_username.setObjectName(u"lineedit_username")

        self.gridLayout_4.addWidget(self.lineedit_username, 0, 1, 1, 3)


        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_2, 1, 0, 1, 2)

        self.stacked_widget_top.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayoutWidget = QWidget(self.page_2)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 791, 113))
        self.gridLayout_9 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout_9.addWidget(self.pushButton_2, 1, 2, 1, 1)

        self.lineEdit = QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_9.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout_9.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_9.addWidget(self.label_2, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_9.addWidget(self.pushButton, 0, 2, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_9.addWidget(self.label, 1, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_9.addWidget(self.label_3, 2, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_9.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.pushButton_3 = QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout_9.addWidget(self.pushButton_3, 2, 2, 1, 1)

        self.button_filter_videos = QPushButton(self.gridLayoutWidget)
        self.button_filter_videos.setObjectName(u"button_filter_videos")

        self.gridLayout_9.addWidget(self.button_filter_videos, 0, 3, 1, 1)

        self.button_filter_users = QPushButton(self.gridLayoutWidget)
        self.button_filter_users.setObjectName(u"button_filter_users")

        self.gridLayout_9.addWidget(self.button_filter_users, 1, 3, 1, 1)

        self.groupBox = QGroupBox(self.page_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(800, 0, 821, 131))
        self.gridLayout_12 = QGridLayout(self.groupBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_10.addWidget(self.radioButton_2, 2, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"padding-left: 40px;")

        self.gridLayout_10.addWidget(self.label_4, 1, 0, 1, 3)

        self.radioButton_4 = QRadioButton(self.groupBox)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.gridLayout_10.addWidget(self.radioButton_4, 2, 1, 1, 1)

        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout_10.addWidget(self.radioButton, 2, 0, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.checkBox_6 = QCheckBox(self.groupBox)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.gridLayout_11.addWidget(self.checkBox_6, 2, 2, 1, 1)

        self.checkBox_4 = QCheckBox(self.groupBox)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.gridLayout_11.addWidget(self.checkBox_4, 2, 3, 1, 1)

        self.checkBox_11 = QCheckBox(self.groupBox)
        self.checkBox_11.setObjectName(u"checkBox_11")

        self.gridLayout_11.addWidget(self.checkBox_11, 4, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"padding-left: 180px;")

        self.gridLayout_11.addWidget(self.label_5, 1, 0, 1, 4)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout_11.addWidget(self.checkBox, 2, 0, 1, 1)

        self.checkBox_8 = QCheckBox(self.groupBox)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.gridLayout_11.addWidget(self.checkBox_8, 2, 1, 1, 1)

        self.checkBox_9 = QCheckBox(self.groupBox)
        self.checkBox_9.setObjectName(u"checkBox_9")

        self.gridLayout_11.addWidget(self.checkBox_9, 3, 0, 1, 1)

        self.checkBox_3 = QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.gridLayout_11.addWidget(self.checkBox_3, 3, 3, 1, 1)

        self.checkBox_12 = QCheckBox(self.groupBox)
        self.checkBox_12.setObjectName(u"checkBox_12")

        self.gridLayout_11.addWidget(self.checkBox_12, 3, 1, 1, 1)

        self.checkBox_10 = QCheckBox(self.groupBox)
        self.checkBox_10.setObjectName(u"checkBox_10")

        self.gridLayout_11.addWidget(self.checkBox_10, 3, 2, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_11, 0, 1, 1, 1)

        self.gridLayoutWidget_4 = QWidget(self.page_2)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 130, 301, 80))
        self.gridLayout_13 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.radioButton_9 = QRadioButton(self.gridLayoutWidget_4)
        self.radioButton_9.setObjectName(u"radioButton_9")

        self.gridLayout_13.addWidget(self.radioButton_9, 1, 1, 1, 1)

        self.radioButton_7 = QRadioButton(self.gridLayoutWidget_4)
        self.radioButton_7.setObjectName(u"radioButton_7")

        self.gridLayout_13.addWidget(self.radioButton_7, 1, 0, 1, 1)

        self.radioButton_8 = QRadioButton(self.gridLayoutWidget_4)
        self.radioButton_8.setObjectName(u"radioButton_8")

        self.gridLayout_13.addWidget(self.radioButton_8, 1, 2, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_13.addWidget(self.label_6, 0, 0, 1, 3)

        self.gridLayoutWidget_5 = QWidget(self.page_2)
        self.gridLayoutWidget_5.setObjectName(u"gridLayoutWidget_5")
        self.gridLayoutWidget_5.setGeometry(QRect(10, 220, 297, 80))
        self.gridLayout_14 = QGridLayout(self.gridLayoutWidget_5)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.radioButton_15 = QRadioButton(self.gridLayoutWidget_5)
        self.radioButton_15.setObjectName(u"radioButton_15")

        self.gridLayout_14.addWidget(self.radioButton_15, 1, 2, 1, 1)

        self.radioButton_14 = QRadioButton(self.gridLayoutWidget_5)
        self.radioButton_14.setObjectName(u"radioButton_14")

        self.gridLayout_14.addWidget(self.radioButton_14, 1, 1, 1, 1)

        self.radioButton_11 = QRadioButton(self.gridLayoutWidget_5)
        self.radioButton_11.setObjectName(u"radioButton_11")

        self.gridLayout_14.addWidget(self.radioButton_11, 1, 0, 1, 1)

        self.radioButton_12 = QRadioButton(self.gridLayoutWidget_5)
        self.radioButton_12.setObjectName(u"radioButton_12")

        self.gridLayout_14.addWidget(self.radioButton_12, 2, 0, 1, 1)

        self.radioButton_10 = QRadioButton(self.gridLayoutWidget_5)
        self.radioButton_10.setObjectName(u"radioButton_10")

        self.gridLayout_14.addWidget(self.radioButton_10, 2, 1, 1, 1)

        self.radioButton_13 = QRadioButton(self.gridLayoutWidget_5)
        self.radioButton_13.setObjectName(u"radioButton_13")

        self.gridLayout_14.addWidget(self.radioButton_13, 2, 2, 1, 1)

        self.label_7 = QLabel(self.gridLayoutWidget_5)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_14.addWidget(self.label_7, 0, 0, 1, 3)

        self.gridLayoutWidget_6 = QWidget(self.page_2)
        self.gridLayoutWidget_6.setObjectName(u"gridLayoutWidget_6")
        self.gridLayoutWidget_6.setGeometry(QRect(350, 220, 323, 80))
        self.gridLayout_15 = QGridLayout(self.gridLayoutWidget_6)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.radioButton_17 = QRadioButton(self.gridLayoutWidget_6)
        self.radioButton_17.setObjectName(u"radioButton_17")

        self.gridLayout_15.addWidget(self.radioButton_17, 1, 0, 1, 1)

        self.radioButton_16 = QRadioButton(self.gridLayoutWidget_6)
        self.radioButton_16.setObjectName(u"radioButton_16")

        self.gridLayout_15.addWidget(self.radioButton_16, 1, 1, 1, 1)

        self.radioButton_18 = QRadioButton(self.gridLayoutWidget_6)
        self.radioButton_18.setObjectName(u"radioButton_18")

        self.gridLayout_15.addWidget(self.radioButton_18, 1, 2, 1, 1)

        self.label_8 = QLabel(self.gridLayoutWidget_6)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_15.addWidget(self.label_8, 0, 0, 1, 3)

        self.gridLayoutWidget_7 = QWidget(self.page_2)
        self.gridLayoutWidget_7.setObjectName(u"gridLayoutWidget_7")
        self.gridLayoutWidget_7.setGeometry(QRect(730, 210, 389, 80))
        self.gridLayout_16 = QGridLayout(self.gridLayoutWidget_7)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.gridLayoutWidget_7)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_16.addWidget(self.label_12, 0, 1, 1, 1)

        self.radioButton_22 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_22.setObjectName(u"radioButton_22")

        self.gridLayout_16.addWidget(self.radioButton_22, 1, 0, 1, 1)

        self.radioButton_26 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_26.setObjectName(u"radioButton_26")

        self.gridLayout_16.addWidget(self.radioButton_26, 1, 1, 1, 1)

        self.radioButton_21 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_21.setObjectName(u"radioButton_21")

        self.gridLayout_16.addWidget(self.radioButton_21, 1, 3, 1, 1)

        self.radioButton_25 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_25.setObjectName(u"radioButton_25")

        self.gridLayout_16.addWidget(self.radioButton_25, 1, 2, 1, 1)

        self.radioButton_20 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_20.setObjectName(u"radioButton_20")

        self.gridLayout_16.addWidget(self.radioButton_20, 2, 0, 1, 1)

        self.radioButton_19 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_19.setObjectName(u"radioButton_19")

        self.gridLayout_16.addWidget(self.radioButton_19, 2, 1, 1, 1)

        self.radioButton_24 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_24.setObjectName(u"radioButton_24")

        self.gridLayout_16.addWidget(self.radioButton_24, 2, 2, 1, 1)

        self.radioButton_23 = QRadioButton(self.gridLayoutWidget_7)
        self.radioButton_23.setObjectName(u"radioButton_23")

        self.gridLayout_16.addWidget(self.radioButton_23, 2, 3, 1, 1)

        self.gridLayoutWidget_8 = QWidget(self.page_2)
        self.gridLayoutWidget_8.setObjectName(u"gridLayoutWidget_8")
        self.gridLayoutWidget_8.setGeometry(QRect(1160, 180, 212, 80))
        self.gridLayout_17 = QGridLayout(self.gridLayoutWidget_8)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.radioButton_27 = QRadioButton(self.gridLayoutWidget_8)
        self.radioButton_27.setObjectName(u"radioButton_27")

        self.gridLayout_17.addWidget(self.radioButton_27, 1, 0, 1, 1)

        self.label_11 = QLabel(self.gridLayoutWidget_8)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_17.addWidget(self.label_11, 0, 0, 1, 1)

        self.radioButton_30 = QRadioButton(self.gridLayoutWidget_8)
        self.radioButton_30.setObjectName(u"radioButton_30")

        self.gridLayout_17.addWidget(self.radioButton_30, 1, 1, 1, 1)

        self.radioButton_29 = QRadioButton(self.gridLayoutWidget_8)
        self.radioButton_29.setObjectName(u"radioButton_29")

        self.gridLayout_17.addWidget(self.radioButton_29, 2, 0, 1, 1)

        self.radioButton_28 = QRadioButton(self.gridLayoutWidget_8)
        self.radioButton_28.setObjectName(u"radioButton_28")

        self.gridLayout_17.addWidget(self.radioButton_28, 2, 1, 1, 1)

        self.gridLayoutWidget_9 = QWidget(self.page_2)
        self.gridLayoutWidget_9.setObjectName(u"gridLayoutWidget_9")
        self.gridLayoutWidget_9.setGeometry(QRect(1410, 190, 205, 80))
        self.gridLayout_18 = QGridLayout(self.gridLayoutWidget_9)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.radioButton_32 = QRadioButton(self.gridLayoutWidget_9)
        self.radioButton_32.setObjectName(u"radioButton_32")

        self.gridLayout_18.addWidget(self.radioButton_32, 1, 0, 1, 1)

        self.radioButton_31 = QRadioButton(self.gridLayoutWidget_9)
        self.radioButton_31.setObjectName(u"radioButton_31")

        self.gridLayout_18.addWidget(self.radioButton_31, 1, 1, 1, 1)

        self.label_10 = QLabel(self.gridLayoutWidget_9)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_18.addWidget(self.label_10, 0, 0, 1, 2)

        self.stacked_widget_top.addWidget(self.page_2)

        self.gridLayout_7.addWidget(self.stacked_widget_top, 1, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stacked_widget_main.addWidget(self.page_4)

        self.gridLayout_8.addWidget(self.stacked_widget_main, 1, 2, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(0)
        self.stacked_widget_top.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn_Fetch_Widget", None))
        self.button_switch_credits.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Credits", None))
        self.button_switch_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.button_switch_settings.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Settings", None))
        self.button_switch_home.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home", None))
        self.label_current_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Current Progress:", None))
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_total.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_error.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Error:", None))
        self.label_debug.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Debug:", None))
        self.label_status.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Status:", None))
        self.treeWidget.setStyleSheet(QCoreApplication.translate("Porn_Fetch_Widget", u"QWidget {\n"
"color: white;\n"
"background-color: rgb(60, 60, 60);\n"
"border: none;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #DDD;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid #5599FF;\n"
"}\n"
"\n"
"\n"
"QProgressBar {\n"
"	color: rgb(255, 153, 0);\n"
"    border: 2px solid #5a2a82;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background-color: rgb(74, 74, 74);\n"
"    color: #ffffff;  /* Adding text color for better visibility */\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 255, 224);\n"
"    width: 10px; /* Adjust this to change the width of the 'chunk' */\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: #dcdcdc; /* Light grey text */\n"
"    spacing: 5px; /* Space between the radio button and its label */\n"
"}\n"
"\n"
"QRadioButton::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"    border-radius: 7px; /* Circular indicator */\n"
""
                        "}\n"
"\n"
"QRadioButton::indicator:unchecked {\n"
"    background-color: #555; /* Dark background for unchecked state */\n"
"    border: 2px solid #777; /* Slightly lighter border */\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: #7a7aff; /* Bright color for checked state */\n"
"    border: 2px solid #5a5aff; /* Border slightly darker than the background */\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover,\n"
"QRadioButton::indicator:unchecked:hover {\n"
"    border-color: #9a9aff; /* Change border color on hover */\n"
"}\n"
"\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #5a2a82;\n"
"    height: 8px;\n"
"    background: #e0e0e0;\n"
"    margin: 0px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #5a2a82;\n"
"    border: 1px solid #5a2a82;\n"
"    width: 18px;\n"
"    margin: -6px 0;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #e0e0e0;\n"
"}\n"
"\n"
"QSlider::sub-page"
                        ":horizontal {\n"
"    background: #5a2a82;\n"
"}\n"
"\n"
"QTreeWidget {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: white;\n"
"}\n"
"\n"
"QTreeWidget QHeaderView::section {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: black; \n"
"    border: 1px solid #5a2a82;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 1ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }\n"
"\n"
"QLabel {\n"
"    color: #DDD;\n"
"    padding: 2px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #555;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5599FF;\n"
"}", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.button_open_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub or HQPorner Video URL", None))
        self.button_search_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Click Open File to select a file, or write the location here and click Open File.    URLs need to be separated with a new line. Supports HQPorner and PornHub", None))
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter a Search Query for PornHub  You can define filters in the settings. The returned videos will be listed down below and you can select them.", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.butgton_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.label_search_query.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.button_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub Model URL. This can be a Pornstar Account or a PornHub Channel. The videos will be listed down in the TreeWidget", None))
        self.button_get_recommended_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.button_get_liked_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.button_get_watched_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
        self.pushButton_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Videos", None))
        self.pushButton.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Users", None))
        self.label_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Pornstars", None))
        self.pushButton_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.button_filter_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Category Filter", None))
        self.button_filter_users.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Filters", None))
        self.groupBox.setTitle("")
        self.radioButton_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"None", None))
        self.label_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Production Filters (for Videos)", None))
        self.radioButton_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Professional", None))
        self.radioButton.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.checkBox_6.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Weekly", None))
        self.checkBox_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yearly", None))
        self.checkBox_11.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Recent", None))
        self.label_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Sorting filters (for Videos)", None))
        self.checkBox.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HD", None))
        self.checkBox_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Daily", None))
        self.checkBox_9.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"All Time", None))
        self.checkBox_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Longest", None))
        self.checkBox_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Top rated", None))
        self.checkBox_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Views", None))
        self.radioButton_9.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_7.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.label_6.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Member Type", None))
        self.radioButton_15.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_14.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_11.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_13.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.label_7.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Member content", None))
        self.radioButton_17.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_16.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_18.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.label_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Member relationship", None))
        self.label_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Member Gender", None))
        self.radioButton_22.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_26.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_21.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_25.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_20.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_19.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_24.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_23.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_27.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.label_11.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Member interests", None))
        self.radioButton_30.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_29.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_28.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_32.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.radioButton_31.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Homemade", None))
        self.label_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Other filters", None))
    # retranslateUi

