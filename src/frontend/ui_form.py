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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

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
"	color: rgb(255,255,255)}\n"
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
"	border-radius: 6"
                        "px;\n"
"	background-color: rgb(0, 255, 183);\n"
"\n"
"}\n"
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
"QSlider::sub-page:horizontal {\n"
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
"        subcont"
                        "rol-position: top center;\n"
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

        self.stacked_widget_main = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_7 = QGridLayout(self.page_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
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
        self.stacked_widget_top.addWidget(self.page_2)

        self.gridLayout_7.addWidget(self.stacked_widget_top, 0, 0, 1, 1)

        self.treeWidget = QTreeWidget(self.page_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.gridLayout_7.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stacked_widget_main.addWidget(self.page_4)

        self.gridLayout_8.addWidget(self.stacked_widget_main, 1, 2, 1, 1)

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


        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(0)
        self.stacked_widget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn_Fetch_Widget", None))
        self.button_switch_credits.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Credits", None))
        self.button_switch_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.button_switch_settings.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Settings", None))
        self.button_switch_home.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home", None))
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
        self.label_current_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Current Progress:", None))
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_total.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_error.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Error:", None))
        self.label_debug.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Debug:", None))
        self.label_status.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Status:", None))
    # retranslateUi

