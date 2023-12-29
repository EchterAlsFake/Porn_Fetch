# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1776, 927)
        self.gridLayout_9 = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(Porn_Fetch_Widget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_switch_home = QPushButton(self.widget)
        self.button_switch_home.setObjectName(u"button_switch_home")
        self.button_switch_home.setMinimumSize(QSize(50, 50))
        self.button_switch_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"border: none")
        self.button_switch_home.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_home)

        self.button_switch_search = QPushButton(self.widget)
        self.button_switch_search.setObjectName(u"button_switch_search")
        self.button_switch_search.setMinimumSize(QSize(50, 50))
        self.button_switch_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_search.setStyleSheet(u"border: none;")
        self.button_switch_search.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_search)

        self.button_switch_settings = QPushButton(self.widget)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        self.button_switch_settings.setMinimumSize(QSize(50, 50))
        self.button_switch_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"border: none;")
        self.button_switch_settings.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_settings)

        self.button_switch_metadata = QPushButton(self.widget)
        self.button_switch_metadata.setObjectName(u"button_switch_metadata")
        self.button_switch_metadata.setMinimumSize(QSize(50, 50))
        self.button_switch_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_metadata.setStyleSheet(u"border: none;")
        self.button_switch_metadata.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_metadata)

        self.button_switch_credits = QPushButton(self.widget)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        self.button_switch_credits.setMinimumSize(QSize(50, 50))
        self.button_switch_credits.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"border: none;")
        self.button_switch_credits.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_credits)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.stacked_widget_main = QStackedWidget(self.widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_8 = QGridLayout(self.page)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.widget_status = QWidget(self.page)
        self.widget_status.setObjectName(u"widget_status")
        self.widget_status.setStyleSheet(u"")
        self.gridLayout_5 = QGridLayout(self.widget_status)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_progress_information = QLabel(self.widget_status)
        self.label_progress_information.setObjectName(u"label_progress_information")

        self.gridLayout_5.addWidget(self.label_progress_information, 2, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_total_progress = QLabel(self.widget_status)
        self.label_total_progress.setObjectName(u"label_total_progress")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_total_progress.sizePolicy().hasHeightForWidth())
        self.label_total_progress.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.label_total_progress, 2, 0, 1, 1)

        self.progressbar_pornhub = QProgressBar(self.widget_status)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressbar_pornhub.sizePolicy().hasHeightForWidth())
        self.progressbar_pornhub.setSizePolicy(sizePolicy1)
        self.progressbar_pornhub.setMinimumSize(QSize(600, 0))
        self.progressbar_pornhub.setValue(0)

        self.gridLayout_3.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.label_progress_pornhub = QLabel(self.widget_status)
        self.label_progress_pornhub.setObjectName(u"label_progress_pornhub")
        sizePolicy.setHeightForWidth(self.label_progress_pornhub.sizePolicy().hasHeightForWidth())
        self.label_progress_pornhub.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.label_progress_pornhub, 0, 0, 1, 1)

        self.progressbar_total = QProgressBar(self.widget_status)
        self.progressbar_total.setObjectName(u"progressbar_total")
        sizePolicy1.setHeightForWidth(self.progressbar_total.sizePolicy().hasHeightForWidth())
        self.progressbar_total.setSizePolicy(sizePolicy1)
        self.progressbar_total.setMinimumSize(QSize(600, 0))
        self.progressbar_total.setValue(0)

        self.gridLayout_3.addWidget(self.progressbar_total, 2, 1, 1, 1)

        self.label_progress_hqporner = QLabel(self.widget_status)
        self.label_progress_hqporner.setObjectName(u"label_progress_hqporner")
        sizePolicy.setHeightForWidth(self.label_progress_hqporner.sizePolicy().hasHeightForWidth())
        self.label_progress_hqporner.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.label_progress_hqporner, 1, 0, 1, 1)

        self.progressbar_hqporner = QProgressBar(self.widget_status)
        self.progressbar_hqporner.setObjectName(u"progressbar_hqporner")
        sizePolicy1.setHeightForWidth(self.progressbar_hqporner.sizePolicy().hasHeightForWidth())
        self.progressbar_hqporner.setSizePolicy(sizePolicy1)
        self.progressbar_hqporner.setMinimumSize(QSize(600, 0))
        self.progressbar_hqporner.setValue(0)

        self.gridLayout_3.addWidget(self.progressbar_hqporner, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.gridlayout_status = QGridLayout()
        self.gridlayout_status.setObjectName(u"gridlayout_status")
        self.lineedit_status = QLineEdit(self.widget_status)
        self.lineedit_status.setObjectName(u"lineedit_status")
        sizePolicy1.setHeightForWidth(self.lineedit_status.sizePolicy().hasHeightForWidth())
        self.lineedit_status.setSizePolicy(sizePolicy1)
        self.lineedit_status.setMinimumSize(QSize(200, 0))
        self.lineedit_status.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_status, 0, 1, 1, 1)

        self.lineedit_debug = QLineEdit(self.widget_status)
        self.lineedit_debug.setObjectName(u"lineedit_debug")
        sizePolicy1.setHeightForWidth(self.lineedit_debug.sizePolicy().hasHeightForWidth())
        self.lineedit_debug.setSizePolicy(sizePolicy1)
        self.lineedit_debug.setMinimumSize(QSize(200, 0))
        self.lineedit_debug.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_debug, 1, 3, 1, 1)

        self.label_error = QLabel(self.widget_status)
        self.label_error.setObjectName(u"label_error")
        sizePolicy.setHeightForWidth(self.label_error.sizePolicy().hasHeightForWidth())
        self.label_error.setSizePolicy(sizePolicy)

        self.gridlayout_status.addWidget(self.label_error, 1, 0, 1, 1)

        self.lineedit_error = QLineEdit(self.widget_status)
        self.lineedit_error.setObjectName(u"lineedit_error")
        sizePolicy1.setHeightForWidth(self.lineedit_error.sizePolicy().hasHeightForWidth())
        self.lineedit_error.setSizePolicy(sizePolicy1)
        self.lineedit_error.setMinimumSize(QSize(200, 0))
        self.lineedit_error.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_error, 1, 1, 1, 1)

        self.lineedit_total = QLineEdit(self.widget_status)
        self.lineedit_total.setObjectName(u"lineedit_total")
        sizePolicy1.setHeightForWidth(self.lineedit_total.sizePolicy().hasHeightForWidth())
        self.lineedit_total.setSizePolicy(sizePolicy1)
        self.lineedit_total.setMinimumSize(QSize(200, 0))
        self.lineedit_total.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineedit_total, 0, 3, 1, 1)

        self.label_status = QLabel(self.widget_status)
        self.label_status.setObjectName(u"label_status")
        sizePolicy.setHeightForWidth(self.label_status.sizePolicy().hasHeightForWidth())
        self.label_status.setSizePolicy(sizePolicy)

        self.gridlayout_status.addWidget(self.label_status, 0, 0, 1, 1)

        self.label_debug = QLabel(self.widget_status)
        self.label_debug.setObjectName(u"label_debug")
        sizePolicy.setHeightForWidth(self.label_debug.sizePolicy().hasHeightForWidth())
        self.label_debug.setSizePolicy(sizePolicy)

        self.gridlayout_status.addWidget(self.label_debug, 1, 2, 1, 1)

        self.label_total = QLabel(self.widget_status)
        self.label_total.setObjectName(u"label_total")
        sizePolicy.setHeightForWidth(self.label_total.sizePolicy().hasHeightForWidth())
        self.label_total.setSizePolicy(sizePolicy)

        self.gridlayout_status.addWidget(self.label_total, 0, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_status, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.widget_status, 1, 0, 1, 1)

        self.stacked_widget_top = QStackedWidget(self.page)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_4 = QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.radio_tree_show_title = QRadioButton(self.page_3)
        self.radio_tree_show_title.setObjectName(u"radio_tree_show_title")
        sizePolicy.setHeightForWidth(self.radio_tree_show_title.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_title.setSizePolicy(sizePolicy)

        self.gridLayout_7.addWidget(self.radio_tree_show_title, 0, 0, 1, 4)

        self.groupBox_4 = QGroupBox(self.page_3)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_34 = QGridLayout(self.groupBox_4)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.button_tree_unselect_all = QPushButton(self.groupBox_4)
        self.button_tree_unselect_all.setObjectName(u"button_tree_unselect_all")
        self.button_tree_unselect_all.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: rgb(0, 208, 255); /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_34.addWidget(self.button_tree_unselect_all, 0, 2, 1, 1)

        self.button_tree_select_all = QPushButton(self.groupBox_4)
        self.button_tree_select_all.setObjectName(u"button_tree_select_all")
        self.button_tree_select_all.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: rgba(255, 162, 0, 170); /* Purple background */\n"
"	color: rgb(255, 162, 0);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_34.addWidget(self.button_tree_select_all, 0, 1, 1, 1)

        self.button_tree_download = QPushButton(self.groupBox_4)
        self.button_tree_download.setObjectName(u"button_tree_download")
        self.button_tree_download.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_34.addWidget(self.button_tree_download, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_4, 2, 0, 1, 7)

        self.treeWidget = QTreeWidget(self.page_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy2)
        self.treeWidget.setMinimumSize(QSize(1620, 100))

        self.gridLayout_7.addWidget(self.treeWidget, 1, 0, 1, 7)

        self.radio_tree_show_all = QRadioButton(self.page_3)
        self.radio_tree_show_all.setObjectName(u"radio_tree_show_all")
        sizePolicy.setHeightForWidth(self.radio_tree_show_all.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_all.setSizePolicy(sizePolicy)

        self.gridLayout_7.addWidget(self.radio_tree_show_all, 0, 4, 1, 3)


        self.gridLayout_4.addLayout(self.gridLayout_7, 1, 0, 1, 2)

        self.gridlayout_login_box_2 = QGridLayout()
        self.gridlayout_login_box_2.setObjectName(u"gridlayout_login_box_2")
        self.lineedit_username = QLineEdit(self.page_3)
        self.lineedit_username.setObjectName(u"lineedit_username")

        self.gridlayout_login_box_2.addWidget(self.lineedit_username, 0, 1, 1, 3)

        self.button_get_liked_videos = QPushButton(self.page_3)
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

        self.gridlayout_login_box_2.addWidget(self.button_get_liked_videos, 3, 0, 1, 1)

        self.button_get_watched_videos = QPushButton(self.page_3)
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

        self.gridlayout_login_box_2.addWidget(self.button_get_watched_videos, 3, 1, 1, 1)

        self.label_password = QLabel(self.page_3)
        self.label_password.setObjectName(u"label_password")

        self.gridlayout_login_box_2.addWidget(self.label_password, 1, 0, 1, 1)

        self.button_login = QPushButton(self.page_3)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_login.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #4CAF50; /* Green background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: #4CAF50;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #66BB6A;\n"
"    border-color: #66BB6A;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #388E3C;\n"
"    border-color: #388E3C;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}")

        self.gridlayout_login_box_2.addWidget(self.button_login, 2, 0, 1, 4)

        self.button_get_recommended_videos = QPushButton(self.page_3)
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

        self.gridlayout_login_box_2.addWidget(self.button_get_recommended_videos, 3, 2, 1, 1)

        self.label_username = QLabel(self.page_3)
        self.label_username.setObjectName(u"label_username")

        self.gridlayout_login_box_2.addWidget(self.label_username, 0, 0, 1, 1)

        self.lineedit_password = QLineEdit(self.page_3)
        self.lineedit_password.setObjectName(u"lineedit_password")
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.gridlayout_login_box_2.addWidget(self.lineedit_password, 1, 1, 1, 3)


        self.gridLayout_4.addLayout(self.gridlayout_login_box_2, 0, 1, 1, 1)

        self.gridlayout_start_download_box_2 = QGridLayout()
        self.gridlayout_start_download_box_2.setObjectName(u"gridlayout_start_download_box_2")
        self.lineedit_file = QLineEdit(self.page_3)
        self.lineedit_file.setObjectName(u"lineedit_file")
        sizePolicy1.setHeightForWidth(self.lineedit_file.sizePolicy().hasHeightForWidth())
        self.lineedit_file.setSizePolicy(sizePolicy1)
        self.lineedit_file.setMinimumSize(QSize(300, 0))

        self.gridlayout_start_download_box_2.addWidget(self.lineedit_file, 3, 1, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page_3)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")
        sizePolicy1.setHeightForWidth(self.lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.lineedit_model_url.setSizePolicy(sizePolicy1)
        self.lineedit_model_url.setMinimumSize(QSize(300, 0))

        self.gridlayout_start_download_box_2.addWidget(self.lineedit_model_url, 2, 1, 1, 1)

        self.button_model = QPushButton(self.page_3)
        self.button_model.setObjectName(u"button_model")
        self.button_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_model.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}")

        self.gridlayout_start_download_box_2.addWidget(self.button_model, 2, 2, 1, 1)

        self.lineedit_url = QLineEdit(self.page_3)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy1.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy1)
        self.lineedit_url.setMinimumSize(QSize(300, 0))

        self.gridlayout_start_download_box_2.addWidget(self.lineedit_url, 0, 1, 1, 1)

        self.label_search_query = QLabel(self.page_3)
        self.label_search_query.setObjectName(u"label_search_query")
        sizePolicy.setHeightForWidth(self.label_search_query.sizePolicy().hasHeightForWidth())
        self.label_search_query.setSizePolicy(sizePolicy)
        self.label_search_query.setMinimumSize(QSize(100, 0))

        self.gridlayout_start_download_box_2.addWidget(self.label_search_query, 4, 0, 1, 1)

        self.button_download = QPushButton(self.page_3)
        self.button_download.setObjectName(u"button_download")
        self.button_download.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}")

        self.gridlayout_start_download_box_2.addWidget(self.button_download, 0, 2, 1, 1)

        self.label_file = QLabel(self.page_3)
        self.label_file.setObjectName(u"label_file")
        sizePolicy.setHeightForWidth(self.label_file.sizePolicy().hasHeightForWidth())
        self.label_file.setSizePolicy(sizePolicy)
        self.label_file.setMinimumSize(QSize(100, 0))

        self.gridlayout_start_download_box_2.addWidget(self.label_file, 3, 0, 1, 1)

        self.lineedit_search_query = QLineEdit(self.page_3)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        sizePolicy1.setHeightForWidth(self.lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.lineedit_search_query.setSizePolicy(sizePolicy1)
        self.lineedit_search_query.setMinimumSize(QSize(300, 0))

        self.gridlayout_start_download_box_2.addWidget(self.lineedit_search_query, 4, 1, 1, 1)

        self.button_open_file = QPushButton(self.page_3)
        self.button_open_file.setObjectName(u"button_open_file")
        self.button_open_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_open_file.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}")

        self.gridlayout_start_download_box_2.addWidget(self.button_open_file, 3, 2, 1, 1)

        self.button_search_videos = QPushButton(self.page_3)
        self.button_search_videos.setObjectName(u"button_search_videos")
        self.button_search_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_search_videos.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}")

        self.gridlayout_start_download_box_2.addWidget(self.button_search_videos, 4, 2, 1, 1)

        self.label_model_url = QLabel(self.page_3)
        self.label_model_url.setObjectName(u"label_model_url")
        sizePolicy.setHeightForWidth(self.label_model_url.sizePolicy().hasHeightForWidth())
        self.label_model_url.setSizePolicy(sizePolicy)
        self.label_model_url.setMinimumSize(QSize(100, 0))

        self.gridlayout_start_download_box_2.addWidget(self.label_model_url, 2, 0, 1, 1)

        self.label_url = QLabel(self.page_3)
        self.label_url.setObjectName(u"label_url")
        sizePolicy.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy)
        self.label_url.setMinimumSize(QSize(100, 0))

        self.gridlayout_start_download_box_2.addWidget(self.label_url, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridlayout_start_download_box_2, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stacked_widget_top.addWidget(self.page_4)

        self.gridLayout_8.addWidget(self.stacked_widget_top, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_25 = QGridLayout(self.page_2)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.groupBox = QGroupBox(self.page_2)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_11 = QGridLayout(self.groupBox)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.groupbox_performance_threading = QGroupBox(self.groupBox)
        self.groupbox_performance_threading.setObjectName(u"groupbox_performance_threading")
        self.gridLayout_20 = QGridLayout(self.groupbox_performance_threading)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.radio_threading_no = QRadioButton(self.groupbox_performance_threading)
        self.radio_threading_no.setObjectName(u"radio_threading_no")

        self.gridLayout_20.addWidget(self.radio_threading_no, 0, 1, 1, 1)

        self.radio_threading_yes = QRadioButton(self.groupbox_performance_threading)
        self.radio_threading_yes.setObjectName(u"radio_threading_yes")

        self.gridLayout_20.addWidget(self.radio_threading_yes, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.groupbox_performance_threading, 0, 0, 1, 2)

        self.groupbox_performance_threading_mode = QGroupBox(self.groupBox)
        self.groupbox_performance_threading_mode.setObjectName(u"groupbox_performance_threading_mode")
        self.gridLayout_19 = QGridLayout(self.groupbox_performance_threading_mode)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.radio_threading_mode_high_performance = QRadioButton(self.groupbox_performance_threading_mode)
        self.radio_threading_mode_high_performance.setObjectName(u"radio_threading_mode_high_performance")

        self.gridLayout_19.addWidget(self.radio_threading_mode_high_performance, 0, 0, 1, 1)

        self.radio_threading_mode_default = QRadioButton(self.groupbox_performance_threading_mode)
        self.radio_threading_mode_default.setObjectName(u"radio_threading_mode_default")

        self.gridLayout_19.addWidget(self.radio_threading_mode_default, 0, 2, 1, 1)

        self.radio_threading_mode_ffmpeg = QRadioButton(self.groupbox_performance_threading_mode)
        self.radio_threading_mode_ffmpeg.setObjectName(u"radio_threading_mode_ffmpeg")

        self.gridLayout_19.addWidget(self.radio_threading_mode_ffmpeg, 0, 1, 1, 1)

        self.button_threading_mode_help = QPushButton(self.groupbox_performance_threading_mode)
        self.button_threading_mode_help.setObjectName(u"button_threading_mode_help")

        self.gridLayout_19.addWidget(self.button_threading_mode_help, 0, 3, 1, 1)


        self.gridLayout_11.addWidget(self.groupbox_performance_threading_mode, 1, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_12 = QGridLayout(self.groupBox_2)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.groupbox_video_quality = QGroupBox(self.groupBox_2)
        self.groupbox_video_quality.setObjectName(u"groupbox_video_quality")
        self.gridLayout_18 = QGridLayout(self.groupbox_video_quality)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.radio_quality_half = QRadioButton(self.groupbox_video_quality)
        self.radio_quality_half.setObjectName(u"radio_quality_half")

        self.gridLayout_18.addWidget(self.radio_quality_half, 0, 1, 1, 1)

        self.radio_quality_best = QRadioButton(self.groupbox_video_quality)
        self.radio_quality_best.setObjectName(u"radio_quality_best")

        self.gridLayout_18.addWidget(self.radio_quality_best, 0, 0, 1, 1)

        self.radio_quality_worst = QRadioButton(self.groupbox_video_quality)
        self.radio_quality_worst.setObjectName(u"radio_quality_worst")

        self.gridLayout_18.addWidget(self.radio_quality_worst, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.groupbox_video_quality, 0, 0, 1, 1)

        self.groupbox_video_output = QGroupBox(self.groupBox_2)
        self.groupbox_video_output.setObjectName(u"groupbox_video_output")
        self.gridLayout_21 = QGridLayout(self.groupbox_video_output)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.label_directory_system = QLabel(self.groupbox_video_output)
        self.label_directory_system.setObjectName(u"label_directory_system")

        self.gridLayout_21.addWidget(self.label_directory_system, 1, 0, 1, 1)

        self.radio_directory_system_yes = QRadioButton(self.groupbox_video_output)
        self.radio_directory_system_yes.setObjectName(u"radio_directory_system_yes")

        self.gridLayout_21.addWidget(self.radio_directory_system_yes, 1, 1, 1, 1)

        self.radio_directory_system_no = QRadioButton(self.groupbox_video_output)
        self.radio_directory_system_no.setObjectName(u"radio_directory_system_no")

        self.gridLayout_21.addWidget(self.radio_directory_system_no, 1, 2, 1, 1)

        self.lineedit_output_path = QLineEdit(self.groupbox_video_output)
        self.lineedit_output_path.setObjectName(u"lineedit_output_path")

        self.gridLayout_21.addWidget(self.lineedit_output_path, 0, 1, 1, 3)

        self.label_output_path = QLabel(self.groupbox_video_output)
        self.label_output_path.setObjectName(u"label_output_path")

        self.gridLayout_21.addWidget(self.label_output_path, 0, 0, 1, 1)

        self.button_output_path_select = QPushButton(self.groupbox_video_output)
        self.button_output_path_select.setObjectName(u"button_output_path_select")

        self.gridLayout_21.addWidget(self.button_output_path_select, 0, 4, 1, 1)

        self.button_directory_system_help = QPushButton(self.groupbox_video_output)
        self.button_directory_system_help.setObjectName(u"button_directory_system_help")

        self.gridLayout_21.addWidget(self.button_directory_system_help, 1, 4, 1, 1)


        self.gridLayout_12.addWidget(self.groupbox_video_output, 1, 0, 1, 1)

        self.groupbox_video_language = QGroupBox(self.groupBox_2)
        self.groupbox_video_language.setObjectName(u"groupbox_video_language")
        self.gridLayout_24 = QGridLayout(self.groupbox_video_language)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.radio_api_language_german = QRadioButton(self.groupbox_video_language)
        self.radio_api_language_german.setObjectName(u"radio_api_language_german")

        self.gridLayout_24.addWidget(self.radio_api_language_german, 1, 0, 1, 1)

        self.radio_api_language_french = QRadioButton(self.groupbox_video_language)
        self.radio_api_language_french.setObjectName(u"radio_api_language_french")

        self.gridLayout_24.addWidget(self.radio_api_language_french, 2, 0, 1, 1)

        self.radio_api_language_english = QRadioButton(self.groupbox_video_language)
        self.radio_api_language_english.setObjectName(u"radio_api_language_english")

        self.gridLayout_24.addWidget(self.radio_api_language_english, 0, 0, 1, 1)

        self.radio_api_language_chinese = QRadioButton(self.groupbox_video_language)
        self.radio_api_language_chinese.setObjectName(u"radio_api_language_chinese")

        self.gridLayout_24.addWidget(self.radio_api_language_chinese, 0, 1, 1, 1)

        self.radio_api_language_russian = QRadioButton(self.groupbox_video_language)
        self.radio_api_language_russian.setObjectName(u"radio_api_language_russian")

        self.gridLayout_24.addWidget(self.radio_api_language_russian, 1, 1, 1, 1)

        self.radio_api_language_custom = QRadioButton(self.groupbox_video_language)
        self.radio_api_language_custom.setObjectName(u"radio_api_language_custom")

        self.gridLayout_24.addWidget(self.radio_api_language_custom, 2, 1, 1, 1)


        self.gridLayout_12.addWidget(self.groupbox_video_language, 0, 1, 1, 1)

        self.groupbox_searching = QGroupBox(self.groupBox_2)
        self.groupbox_searching.setObjectName(u"groupbox_searching")
        self.gridLayout_23 = QGridLayout(self.groupbox_searching)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.label_searching_limit = QLabel(self.groupbox_searching)
        self.label_searching_limit.setObjectName(u"label_searching_limit")

        self.gridLayout_23.addWidget(self.label_searching_limit, 0, 0, 1, 1)

        self.spinbox_searching = QSpinBox(self.groupbox_searching)
        self.spinbox_searching.setObjectName(u"spinbox_searching")
        self.spinbox_searching.setMinimum(1)
        self.spinbox_searching.setMaximum(200)

        self.gridLayout_23.addWidget(self.spinbox_searching, 0, 1, 1, 1)


        self.gridLayout_12.addWidget(self.groupbox_searching, 1, 1, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_2, 2, 0, 1, 2)

        self.groupbox_performance_semaphore = QGroupBox(self.groupBox)
        self.groupbox_performance_semaphore.setObjectName(u"groupbox_performance_semaphore")
        self.gridLayout_22 = QGridLayout(self.groupbox_performance_semaphore)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.label_semaphore = QLabel(self.groupbox_performance_semaphore)
        self.label_semaphore.setObjectName(u"label_semaphore")

        self.gridLayout_22.addWidget(self.label_semaphore, 0, 0, 1, 1)

        self.button_semaphore_help = QPushButton(self.groupbox_performance_semaphore)
        self.button_semaphore_help.setObjectName(u"button_semaphore_help")

        self.gridLayout_22.addWidget(self.button_semaphore_help, 1, 0, 1, 2)

        self.spinbox_semaphore = QSpinBox(self.groupbox_performance_semaphore)
        self.spinbox_semaphore.setObjectName(u"spinbox_semaphore")
        self.spinbox_semaphore.setMinimum(1)
        self.spinbox_semaphore.setMaximum(10)

        self.gridLayout_22.addWidget(self.spinbox_semaphore, 0, 1, 1, 1)


        self.gridLayout_11.addWidget(self.groupbox_performance_semaphore, 1, 0, 1, 1)

        self.groupBox_6 = QGroupBox(self.groupBox)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_13 = QGridLayout(self.groupBox_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.groupbox_GUI_language = QGroupBox(self.groupBox_6)
        self.groupbox_GUI_language.setObjectName(u"groupbox_GUI_language")
        self.gridLayout_29 = QGridLayout(self.groupbox_GUI_language)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.radio_ui_language_english = QRadioButton(self.groupbox_GUI_language)
        self.radio_ui_language_english.setObjectName(u"radio_ui_language_english")

        self.gridLayout_29.addWidget(self.radio_ui_language_english, 0, 0, 1, 1)

        self.radio_ui_language_german = QRadioButton(self.groupbox_GUI_language)
        self.radio_ui_language_german.setObjectName(u"radio_ui_language_german")

        self.gridLayout_29.addWidget(self.radio_ui_language_german, 0, 1, 1, 1)

        self.radio_ui_language_french = QRadioButton(self.groupbox_GUI_language)
        self.radio_ui_language_french.setObjectName(u"radio_ui_language_french")
        self.radio_ui_language_french.setEnabled(False)

        self.gridLayout_29.addWidget(self.radio_ui_language_french, 0, 2, 1, 1)


        self.gridLayout_13.addWidget(self.groupbox_GUI_language, 0, 0, 1, 1)


        self.gridLayout_11.addWidget(self.groupBox_6, 3, 0, 1, 2)

        self.button_settings_apply = QPushButton(self.groupBox)
        self.button_settings_apply.setObjectName(u"button_settings_apply")

        self.gridLayout_11.addWidget(self.button_settings_apply, 4, 0, 1, 2)


        self.gridLayout_15.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_25.addLayout(self.gridLayout_15, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_2)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_26 = QGridLayout(self.page_7)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_31 = QGridLayout()
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.textBrowser = QTextBrowser(self.page_7)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_31.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout_26.addLayout(self.gridLayout_31, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_7)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout_40 = QGridLayout(self.page_8)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.groupbox_advanced_user_information = QGroupBox(self.page_8)
        self.groupbox_advanced_user_information.setObjectName(u"groupbox_advanced_user_information")
        self.gridLayout_28 = QGridLayout(self.groupbox_advanced_user_information)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_30 = QGridLayout()
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.lineedit_user_fake_boobs = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_fake_boobs.setObjectName(u"lineedit_user_fake_boobs")

        self.gridLayout_30.addWidget(self.lineedit_user_fake_boobs, 1, 3, 1, 1)

        self.lineedit_user_piercings = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_piercings.setObjectName(u"lineedit_user_piercings")

        self.gridLayout_30.addWidget(self.lineedit_user_piercings, 0, 3, 1, 1)

        self.label_height = QLabel(self.groupbox_advanced_user_information)
        self.label_height.setObjectName(u"label_height")

        self.gridLayout_30.addWidget(self.label_height, 3, 0, 1, 1)

        self.lineedit_user_interests_hobbies = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_interests_hobbies.setObjectName(u"lineedit_user_interests_hobbies")

        self.gridLayout_30.addWidget(self.lineedit_user_interests_hobbies, 7, 1, 1, 1)

        self.lineedit_user_weight = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_weight.setObjectName(u"lineedit_user_weight")

        self.gridLayout_30.addWidget(self.lineedit_user_weight, 4, 1, 1, 1)

        self.label_tattoos = QLabel(self.groupbox_advanced_user_information)
        self.label_tattoos.setObjectName(u"label_tattoos")

        self.gridLayout_30.addWidget(self.label_tattoos, 8, 2, 1, 1)

        self.lineedit_user_tattoos = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_tattoos.setObjectName(u"lineedit_user_tattoos")

        self.gridLayout_30.addWidget(self.lineedit_user_tattoos, 8, 3, 1, 1)

        self.lineedit_user_hair_color = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_hair_color.setObjectName(u"lineedit_user_hair_color")

        self.gridLayout_30.addWidget(self.lineedit_user_hair_color, 6, 1, 1, 1)

        self.lineedit_user_city_country = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_city_country.setObjectName(u"lineedit_user_city_country")

        self.gridLayout_30.addWidget(self.lineedit_user_city_country, 7, 3, 1, 1)

        self.lineedit_user_relationship = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_relationship.setObjectName(u"lineedit_user_relationship")

        self.gridLayout_30.addWidget(self.lineedit_user_relationship, 0, 1, 1, 1)

        self.label_relationship = QLabel(self.groupbox_advanced_user_information)
        self.label_relationship.setObjectName(u"label_relationship")

        self.gridLayout_30.addWidget(self.label_relationship, 0, 0, 1, 1)

        self.lineedit_user_turn_ons = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_turn_ons.setObjectName(u"lineedit_user_turn_ons")

        self.gridLayout_30.addWidget(self.lineedit_user_turn_ons, 2, 3, 1, 1)

        self.lineedit_user_interested_in = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_interested_in.setObjectName(u"lineedit_user_interested_in")

        self.gridLayout_30.addWidget(self.lineedit_user_interested_in, 1, 1, 1, 1)

        self.label_turn_ons = QLabel(self.groupbox_advanced_user_information)
        self.label_turn_ons.setObjectName(u"label_turn_ons")

        self.gridLayout_30.addWidget(self.label_turn_ons, 2, 2, 1, 1)

        self.lineedit_user_video_views = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_video_views.setObjectName(u"lineedit_user_video_views")

        self.gridLayout_30.addWidget(self.lineedit_user_video_views, 4, 3, 1, 1)

        self.lineedit_user_turn_offs = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_turn_offs.setObjectName(u"lineedit_user_turn_offs")

        self.gridLayout_30.addWidget(self.lineedit_user_turn_offs, 3, 3, 1, 1)

        self.label_widght = QLabel(self.groupbox_advanced_user_information)
        self.label_widght.setObjectName(u"label_widght")

        self.gridLayout_30.addWidget(self.label_widght, 4, 0, 1, 1)

        self.label_piercings = QLabel(self.groupbox_advanced_user_information)
        self.label_piercings.setObjectName(u"label_piercings")

        self.gridLayout_30.addWidget(self.label_piercings, 0, 2, 1, 1)

        self.label_fake_boobs = QLabel(self.groupbox_advanced_user_information)
        self.label_fake_boobs.setObjectName(u"label_fake_boobs")

        self.gridLayout_30.addWidget(self.label_fake_boobs, 1, 2, 1, 1)

        self.label_videos_watched = QLabel(self.groupbox_advanced_user_information)
        self.label_videos_watched.setObjectName(u"label_videos_watched")

        self.gridLayout_30.addWidget(self.label_videos_watched, 6, 2, 1, 1)

        self.label_ethnicity = QLabel(self.groupbox_advanced_user_information)
        self.label_ethnicity.setObjectName(u"label_ethnicity")

        self.gridLayout_30.addWidget(self.label_ethnicity, 5, 0, 1, 1)

        self.lineedit_user_height = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_height.setObjectName(u"lineedit_user_height")

        self.gridLayout_30.addWidget(self.lineedit_user_height, 3, 1, 1, 1)

        self.label_video_views = QLabel(self.groupbox_advanced_user_information)
        self.label_video_views.setObjectName(u"label_video_views")

        self.gridLayout_30.addWidget(self.label_video_views, 4, 2, 1, 1)

        self.label_interests_hobbies = QLabel(self.groupbox_advanced_user_information)
        self.label_interests_hobbies.setObjectName(u"label_interests_hobbies")

        self.gridLayout_30.addWidget(self.label_interests_hobbies, 7, 0, 1, 1)

        self.lineedit_user_birth_place = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_birth_place.setObjectName(u"lineedit_user_birth_place")

        self.gridLayout_30.addWidget(self.lineedit_user_birth_place, 8, 1, 1, 1)

        self.lineedit_user_videos_watched = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_videos_watched.setObjectName(u"lineedit_user_videos_watched")

        self.gridLayout_30.addWidget(self.lineedit_user_videos_watched, 6, 3, 1, 1)

        self.label_turn_offs = QLabel(self.groupbox_advanced_user_information)
        self.label_turn_offs.setObjectName(u"label_turn_offs")

        self.gridLayout_30.addWidget(self.label_turn_offs, 3, 2, 1, 1)

        self.label_gender = QLabel(self.groupbox_advanced_user_information)
        self.label_gender.setObjectName(u"label_gender")

        self.gridLayout_30.addWidget(self.label_gender, 2, 0, 1, 1)

        self.lineedit_user_profile_views = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_profile_views.setObjectName(u"lineedit_user_profile_views")

        self.gridLayout_30.addWidget(self.lineedit_user_profile_views, 5, 3, 1, 1)

        self.label_hair_color = QLabel(self.groupbox_advanced_user_information)
        self.label_hair_color.setObjectName(u"label_hair_color")

        self.gridLayout_30.addWidget(self.label_hair_color, 6, 0, 1, 1)

        self.label_profile_views = QLabel(self.groupbox_advanced_user_information)
        self.label_profile_views.setObjectName(u"label_profile_views")

        self.gridLayout_30.addWidget(self.label_profile_views, 5, 2, 1, 1)

        self.label_city_country = QLabel(self.groupbox_advanced_user_information)
        self.label_city_country.setObjectName(u"label_city_country")

        self.gridLayout_30.addWidget(self.label_city_country, 7, 2, 1, 1)

        self.label_interested_in = QLabel(self.groupbox_advanced_user_information)
        self.label_interested_in.setObjectName(u"label_interested_in")

        self.gridLayout_30.addWidget(self.label_interested_in, 1, 0, 1, 1)

        self.label_birth_place = QLabel(self.groupbox_advanced_user_information)
        self.label_birth_place.setObjectName(u"label_birth_place")

        self.gridLayout_30.addWidget(self.label_birth_place, 8, 0, 1, 1)

        self.lineedit_user_gender = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_gender.setObjectName(u"lineedit_user_gender")

        self.gridLayout_30.addWidget(self.lineedit_user_gender, 2, 1, 1, 1)

        self.lineedit_user_ethnicity = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_ethnicity.setObjectName(u"lineedit_user_ethnicity")

        self.gridLayout_30.addWidget(self.lineedit_user_ethnicity, 5, 1, 1, 1)

        self.label_home_town = QLabel(self.groupbox_advanced_user_information)
        self.label_home_town.setObjectName(u"label_home_town")

        self.gridLayout_30.addWidget(self.label_home_town, 9, 0, 1, 1)

        self.lineedit_user_home_town = QLineEdit(self.groupbox_advanced_user_information)
        self.lineedit_user_home_town.setObjectName(u"lineedit_user_home_town")

        self.gridLayout_30.addWidget(self.lineedit_user_home_town, 9, 1, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_30, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupbox_advanced_user_information, 1, 0, 1, 2)

        self.groupBox_8 = QGroupBox(self.page_8)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_38 = QGridLayout(self.groupBox_8)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.gridLayout_39 = QGridLayout()
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.lineedit_user_name = QLineEdit(self.groupBox_8)
        self.lineedit_user_name.setObjectName(u"lineedit_user_name")

        self.gridLayout_39.addWidget(self.lineedit_user_name, 0, 1, 1, 1)

        self.lineedit_user_type = QLineEdit(self.groupBox_8)
        self.lineedit_user_type.setObjectName(u"lineedit_user_type")

        self.gridLayout_39.addWidget(self.lineedit_user_type, 1, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_8)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_39.addWidget(self.label_12, 0, 0, 1, 1)

        self.button_user_download_avatar = QPushButton(self.groupBox_8)
        self.button_user_download_avatar.setObjectName(u"button_user_download_avatar")
        self.button_user_download_avatar.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_39.addWidget(self.button_user_download_avatar, 2, 0, 1, 1)

        self.label_13 = QLabel(self.groupBox_8)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_39.addWidget(self.label_13, 1, 0, 1, 1)

        self.button_user_get_bio = QPushButton(self.groupBox_8)
        self.button_user_get_bio.setObjectName(u"button_user_get_bio")
        self.button_user_get_bio.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_39.addWidget(self.button_user_get_bio, 2, 1, 1, 1)


        self.gridLayout_38.addLayout(self.gridLayout_39, 0, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_8, 2, 0, 1, 1)

        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.label_metadata_video_url = QLabel(self.page_8)
        self.label_metadata_video_url.setObjectName(u"label_metadata_video_url")

        self.gridLayout_27.addWidget(self.label_metadata_video_url, 0, 0, 1, 1)

        self.button_metadata_user_start = QPushButton(self.page_8)
        self.button_metadata_user_start.setObjectName(u"button_metadata_user_start")
        self.button_metadata_user_start.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_27.addWidget(self.button_metadata_user_start, 1, 2, 1, 1)

        self.lineedit_metadata_video_url = QLineEdit(self.page_8)
        self.lineedit_metadata_video_url.setObjectName(u"lineedit_metadata_video_url")

        self.gridLayout_27.addWidget(self.lineedit_metadata_video_url, 0, 1, 1, 1)

        self.lineedit_metadata_user_url = QLineEdit(self.page_8)
        self.lineedit_metadata_user_url.setObjectName(u"lineedit_metadata_user_url")

        self.gridLayout_27.addWidget(self.lineedit_metadata_user_url, 1, 1, 1, 1)

        self.button_metadata_video_start = QPushButton(self.page_8)
        self.button_metadata_video_start.setObjectName(u"button_metadata_video_start")
        self.button_metadata_video_start.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_27.addWidget(self.button_metadata_video_start, 0, 2, 1, 1)

        self.label_metadata_user_url = QLabel(self.page_8)
        self.label_metadata_user_url.setObjectName(u"label_metadata_user_url")

        self.gridLayout_27.addWidget(self.label_metadata_user_url, 1, 0, 1, 1)


        self.gridLayout_40.addLayout(self.gridLayout_27, 0, 0, 1, 2)

        self.groupBox_7 = QGroupBox(self.page_8)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_36 = QGridLayout(self.groupBox_7)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.gridLayout_37 = QGridLayout()
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.label_video_hotspots = QLabel(self.groupBox_7)
        self.label_video_hotspots.setObjectName(u"label_video_hotspots")

        self.gridLayout_37.addWidget(self.label_video_hotspots, 0, 2, 1, 1)

        self.label_video_pornstars = QLabel(self.groupBox_7)
        self.label_video_pornstars.setObjectName(u"label_video_pornstars")

        self.gridLayout_37.addWidget(self.label_video_pornstars, 3, 0, 1, 1)

        self.label_video_title = QLabel(self.groupBox_7)
        self.label_video_title.setObjectName(u"label_video_title")

        self.gridLayout_37.addWidget(self.label_video_title, 0, 0, 1, 1)

        self.lineedit_video_duration = QLineEdit(self.groupBox_7)
        self.lineedit_video_duration.setObjectName(u"lineedit_video_duration")

        self.gridLayout_37.addWidget(self.lineedit_video_duration, 2, 1, 1, 1)

        self.label_video_duration = QLabel(self.groupBox_7)
        self.label_video_duration.setObjectName(u"label_video_duration")

        self.gridLayout_37.addWidget(self.label_video_duration, 2, 0, 1, 1)

        self.label_video_views_2 = QLabel(self.groupBox_7)
        self.label_video_views_2.setObjectName(u"label_video_views_2")

        self.gridLayout_37.addWidget(self.label_video_views_2, 1, 0, 1, 1)

        self.label_video_rating = QLabel(self.groupBox_7)
        self.label_video_rating.setObjectName(u"label_video_rating")

        self.gridLayout_37.addWidget(self.label_video_rating, 2, 2, 1, 1)

        self.lineedit_video_title = QLineEdit(self.groupBox_7)
        self.lineedit_video_title.setObjectName(u"lineedit_video_title")

        self.gridLayout_37.addWidget(self.lineedit_video_title, 0, 1, 1, 1)

        self.label_video_tags = QLabel(self.groupBox_7)
        self.label_video_tags.setObjectName(u"label_video_tags")

        self.gridLayout_37.addWidget(self.label_video_tags, 1, 2, 1, 1)

        self.lineedit_video_pornstars = QLineEdit(self.groupBox_7)
        self.lineedit_video_pornstars.setObjectName(u"lineedit_video_pornstars")

        self.gridLayout_37.addWidget(self.lineedit_video_pornstars, 3, 1, 1, 1)

        self.lineedit_video_views = QLineEdit(self.groupBox_7)
        self.lineedit_video_views.setObjectName(u"lineedit_video_views")

        self.gridLayout_37.addWidget(self.lineedit_video_views, 1, 1, 1, 1)

        self.lineedit_video_hotspots = QLineEdit(self.groupBox_7)
        self.lineedit_video_hotspots.setObjectName(u"lineedit_video_hotspots")

        self.gridLayout_37.addWidget(self.lineedit_video_hotspots, 0, 3, 1, 1)

        self.lineedit_video_tags = QLineEdit(self.groupBox_7)
        self.lineedit_video_tags.setObjectName(u"lineedit_video_tags")

        self.gridLayout_37.addWidget(self.lineedit_video_tags, 1, 3, 1, 1)

        self.lineedit_video_rating = QLineEdit(self.groupBox_7)
        self.lineedit_video_rating.setObjectName(u"lineedit_video_rating")

        self.gridLayout_37.addWidget(self.lineedit_video_rating, 2, 3, 1, 1)

        self.lineedit_video_orientation = QLineEdit(self.groupBox_7)
        self.lineedit_video_orientation.setObjectName(u"lineedit_video_orientation")

        self.gridLayout_37.addWidget(self.lineedit_video_orientation, 3, 3, 1, 1)

        self.label_video_orientation = QLabel(self.groupBox_7)
        self.label_video_orientation.setObjectName(u"label_video_orientation")

        self.gridLayout_37.addWidget(self.label_video_orientation, 3, 2, 1, 1)


        self.gridLayout_36.addLayout(self.gridLayout_37, 0, 0, 1, 1)

        self.button_video_thumbnail_download = QPushButton(self.groupBox_7)
        self.button_video_thumbnail_download.setObjectName(u"button_video_thumbnail_download")
        self.button_video_thumbnail_download.setStyleSheet(u"QPushButton {\n"
"    /* Base style */\n"
"    background-color: #7B1FA2; /* Purple background */\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 8px; /* Slightly smaller radius for a smaller look */\n"
"    border-color: #7B1FA2;\n"
"    font: bold 12px; /* Smaller font size */\n"
"    min-width: 8em; /* Smaller width */\n"
"    padding: 4px; /* Less padding for a more compact look */\n"
"    color: white; /* White text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    /* Hover effect */\n"
"    background-color: #9575CD; /* Lighter violet for hover */\n"
"    border-color: #9575CD;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    /* Pressed effect */\n"
"    background-color: #303F9F; /* Dark blue when pressed */\n"
"    border-color: #303F9F;\n"
"    border-style: inset; /* Changes the style to look \"pressed\" */\n"
"}\n"
"")

        self.gridLayout_36.addWidget(self.button_video_thumbnail_download, 1, 0, 1, 1)


        self.gridLayout_40.addWidget(self.groupBox_7, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_40.addItem(self.verticalSpacer_2, 3, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_8)

        self.gridLayout_2.addWidget(self.stacked_widget_main, 0, 1, 1, 1)


        self.horizontalLayout.addWidget(self.widget)


        self.gridLayout_9.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(1)
        self.stacked_widget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch V3 (C) Johannes Habel GPL 3", None))
        self.button_switch_home.setText("")
        self.button_switch_search.setText("")
        self.button_switch_settings.setText("")
        self.button_switch_metadata.setText("")
        self.button_switch_credits.setText("")
        self.label_progress_information.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Information: The total progressbar only counts the total progress of all PornHub videos being downloaded. I can't add it for HQPorner due to some differences in how the progress is being handled across the different websites!", None))
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_progress_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub:", None))
        self.label_progress_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner:", None))
        self.label_error.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Error:", None))
        self.label_status.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Status:", None))
        self.label_debug.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Debug:", None))
        self.label_total.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.radio_tree_show_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Only Title (a lot faster)", None))
        self.groupBox_4.setTitle("")
        self.button_tree_unselect_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselect all", None))
        self.button_tree_select_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select all", None))
        self.button_tree_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Selected Videos", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Porn_Fetch_Widget", u"Duration", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Porn_Fetch_Widget", u"Author", None));
        self.radio_tree_show_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Title, Author, Duration", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
        self.button_get_liked_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.button_get_watched_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.button_get_recommended_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Click Open File to select a file, or write the location here and click Open File.    URLs need to be separated with a new line. Supports HQPorner and PornHub", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub Model URL. This can be a Pornstar Account or a PornHub Channel. The videos will be listed down in the TreeWidget", None))
        self.button_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub or HQPorner Video URL", None))
        self.label_search_query.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter a Search Query for PornHub  You can define filters in the settings. The returned videos will be listed down below and you can select them.", None))
        self.button_open_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.button_search_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.groupBox.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Performance Settings", None))
        self.groupbox_performance_threading.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading?", None))
        self.radio_threading_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.radio_threading_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.groupbox_performance_threading_mode.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading Mode", None))
        self.radio_threading_mode_high_performance.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"High Performance", None))
        self.radio_threading_mode_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Default", None))
        self.radio_threading_mode_ffmpeg.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"FFMPEG", None))
        self.button_threading_mode_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Video Settings", None))
        self.groupbox_video_quality.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Quality", None))
        self.radio_quality_half.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Half", None))
        self.radio_quality_best.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Best", None))
        self.radio_quality_worst.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Worst", None))
        self.groupbox_video_output.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Output", None))
        self.label_directory_system.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Use Directory system? ", None))
        self.radio_directory_system_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_directory_system_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.lineedit_output_path.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter \"./\" for current directory", None))
        self.label_output_path.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Output path:", None))
        self.button_output_path_select.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select", None))
        self.button_directory_system_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.groupbox_video_language.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"API Language", None))
        self.radio_api_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.radio_api_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.radio_api_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_api_language_chinese.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese", None))
        self.radio_api_language_russian.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Russian", None))
        self.radio_api_language_custom.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Custom", None))
        self.groupbox_searching.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Searching", None))
        self.label_searching_limit.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Limit:", None))
        self.groupbox_performance_semaphore.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Semaphore", None))
        self.label_semaphore.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Semaphore:", None))
        self.button_semaphore_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface Settings", None))
        self.groupbox_GUI_language.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface Language (Neeeds restart)", None))
        self.radio_ui_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_ui_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.radio_ui_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Apply / Reload", None))
        self.groupbox_advanced_user_information.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Advanced User Information", None))
        self.label_height.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Height:", None))
        self.label_tattoos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tattoos:", None))
        self.label_relationship.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Relationship:", None))
        self.label_turn_ons.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Turn Ons:", None))
        self.label_widght.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Weight:", None))
        self.label_piercings.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Piercings:", None))
        self.label_fake_boobs.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Fake Boobs:", None))
        self.label_videos_watched.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Videos Watched:", None))
        self.label_ethnicity.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Ethnicity:", None))
        self.label_video_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Video Views:", None))
        self.label_interests_hobbies.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Interests / Hobbies:", None))
        self.label_turn_offs.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Turn Offs:", None))
        self.label_gender.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Gender:", None))
        self.label_hair_color.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hair Color:", None))
        self.label_profile_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Profile Views:", None))
        self.label_city_country.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"City / Country:", None))
        self.label_interested_in.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Interested in:", None))
        self.label_birth_place.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Birth Place:", None))
        self.label_home_town.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home Town", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Basic User Information", None))
        self.label_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Name:", None))
        self.button_user_download_avatar.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download User Avatar", None))
        self.label_13.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User Type:", None))
        self.button_user_get_bio.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get User's Bio", None))
        self.label_metadata_video_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Video URL:", None))
        self.button_metadata_user_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.button_metadata_video_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_metadata_user_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User URL:", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Video Information:", None))
        self.label_video_hotspots.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hotspots:", None))
        self.label_video_pornstars.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Pornstars:", None))
        self.label_video_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Title:", None))
        self.label_video_duration.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Duration:", None))
        self.label_video_views_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Views:", None))
        self.label_video_rating.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Rating:", None))
        self.label_video_tags.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tags:", None))
        self.label_video_orientation.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Orientation:", None))
        self.button_video_thumbnail_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Thumbnail", None))
    # retranslateUi

