# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_android.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QProgressBar,
    QPushButton, QRadioButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1076, 802)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Porn_Fetch_Widget.sizePolicy().hasHeightForWidth())
        Porn_Fetch_Widget.setSizePolicy(sizePolicy)
        self.gridLayout_17 = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_switch_home = QPushButton(Porn_Fetch_Widget)
        self.button_switch_home.setObjectName(u"button_switch_home")
        self.button_switch_home.setMinimumSize(QSize(50, 50))
        self.button_switch_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"border: none")
        self.button_switch_home.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_home)

        self.button_switch_account = QPushButton(Porn_Fetch_Widget)
        self.button_switch_account.setObjectName(u"button_switch_account")
        self.button_switch_account.setMinimumSize(QSize(50, 50))
        self.button_switch_account.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_account.setStyleSheet(u"border: none;")
        self.button_switch_account.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_account)

        self.button_switch_search = QPushButton(Porn_Fetch_Widget)
        self.button_switch_search.setObjectName(u"button_switch_search")
        self.button_switch_search.setMinimumSize(QSize(50, 50))
        self.button_switch_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_search.setStyleSheet(u"border: none;")
        self.button_switch_search.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_search)

        self.button_switch_settings = QPushButton(Porn_Fetch_Widget)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        self.button_switch_settings.setMinimumSize(QSize(50, 50))
        self.button_switch_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"border: none;")
        self.button_switch_settings.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_settings)

        self.button_switch_metadata = QPushButton(Porn_Fetch_Widget)
        self.button_switch_metadata.setObjectName(u"button_switch_metadata")
        self.button_switch_metadata.setMinimumSize(QSize(50, 50))
        self.button_switch_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_metadata.setStyleSheet(u"border: none;")
        self.button_switch_metadata.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_metadata)

        self.button_switch_credits = QPushButton(Porn_Fetch_Widget)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        self.button_switch_credits.setMinimumSize(QSize(50, 50))
        self.button_switch_credits.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"border: none;")
        self.button_switch_credits.setIconSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.button_switch_credits)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_15.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.widget = QWidget(Porn_Fetch_Widget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.progressbar_total = QProgressBar(self.widget)
        self.progressbar_total.setObjectName(u"progressbar_total")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.progressbar_total.sizePolicy().hasHeightForWidth())
        self.progressbar_total.setSizePolicy(sizePolicy1)
        self.progressbar_total.setMinimumSize(QSize(600, 0))
        self.progressbar_total.setValue(0)

        self.gridLayout_3.addWidget(self.progressbar_total, 2, 1, 1, 1)

        self.progressbar_pornhub = QProgressBar(self.widget)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        sizePolicy1.setHeightForWidth(self.progressbar_pornhub.sizePolicy().hasHeightForWidth())
        self.progressbar_pornhub.setSizePolicy(sizePolicy1)
        self.progressbar_pornhub.setMinimumSize(QSize(600, 0))
        self.progressbar_pornhub.setValue(0)

        self.gridLayout_3.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.label_progress_pornhub = QLabel(self.widget)
        self.label_progress_pornhub.setObjectName(u"label_progress_pornhub")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_progress_pornhub.sizePolicy().hasHeightForWidth())
        self.label_progress_pornhub.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.label_progress_pornhub, 0, 0, 1, 1)

        self.label_progress_hqporner = QLabel(self.widget)
        self.label_progress_hqporner.setObjectName(u"label_progress_hqporner")
        sizePolicy2.setHeightForWidth(self.label_progress_hqporner.sizePolicy().hasHeightForWidth())
        self.label_progress_hqporner.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.label_progress_hqporner, 1, 0, 1, 1)

        self.progressbar_hqporner = QProgressBar(self.widget)
        self.progressbar_hqporner.setObjectName(u"progressbar_hqporner")
        sizePolicy1.setHeightForWidth(self.progressbar_hqporner.sizePolicy().hasHeightForWidth())
        self.progressbar_hqporner.setSizePolicy(sizePolicy1)
        self.progressbar_hqporner.setMinimumSize(QSize(600, 0))
        self.progressbar_hqporner.setValue(0)

        self.gridLayout_3.addWidget(self.progressbar_hqporner, 1, 1, 1, 1)

        self.label_total_progress = QLabel(self.widget)
        self.label_total_progress.setObjectName(u"label_total_progress")
        sizePolicy2.setHeightForWidth(self.label_total_progress.sizePolicy().hasHeightForWidth())
        self.label_total_progress.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.label_total_progress, 2, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 1, 0, 1, 1)

        self.stacked_widget_main = QStackedWidget(self.widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_5 = QGridLayout(self.page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.stacked_widget_top = QStackedWidget(self.page)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout = QGridLayout(self.page_3)
        self.gridLayout.setObjectName(u"gridLayout")
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
        sizePolicy2.setHeightForWidth(self.label_search_query.sizePolicy().hasHeightForWidth())
        self.label_search_query.setSizePolicy(sizePolicy2)
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
        sizePolicy2.setHeightForWidth(self.label_file.sizePolicy().hasHeightForWidth())
        self.label_file.setSizePolicy(sizePolicy2)
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
        self.button_open_file.setEnabled(False)
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
        sizePolicy2.setHeightForWidth(self.label_model_url.sizePolicy().hasHeightForWidth())
        self.label_model_url.setSizePolicy(sizePolicy2)
        self.label_model_url.setMinimumSize(QSize(100, 0))

        self.gridlayout_start_download_box_2.addWidget(self.label_model_url, 2, 0, 1, 1)

        self.label_url = QLabel(self.page_3)
        self.label_url.setObjectName(u"label_url")
        sizePolicy2.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy2)
        self.label_url.setMinimumSize(QSize(100, 0))

        self.gridlayout_start_download_box_2.addWidget(self.label_url, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridlayout_start_download_box_2, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_4 = QGridLayout(self.page_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridlayout_login_box_2 = QGridLayout()
        self.gridlayout_login_box_2.setObjectName(u"gridlayout_login_box_2")
        self.label_password = QLabel(self.page_4)
        self.label_password.setObjectName(u"label_password")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_password.sizePolicy().hasHeightForWidth())
        self.label_password.setSizePolicy(sizePolicy3)

        self.gridlayout_login_box_2.addWidget(self.label_password, 1, 0, 1, 1)

        self.lineedit_password = QLineEdit(self.page_4)
        self.lineedit_password.setObjectName(u"lineedit_password")
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.gridlayout_login_box_2.addWidget(self.lineedit_password, 1, 1, 1, 2)

        self.label_username = QLabel(self.page_4)
        self.label_username.setObjectName(u"label_username")
        sizePolicy3.setHeightForWidth(self.label_username.sizePolicy().hasHeightForWidth())
        self.label_username.setSizePolicy(sizePolicy3)

        self.gridlayout_login_box_2.addWidget(self.label_username, 0, 0, 1, 1)

        self.lineedit_username = QLineEdit(self.page_4)
        self.lineedit_username.setObjectName(u"lineedit_username")

        self.gridlayout_login_box_2.addWidget(self.lineedit_username, 0, 1, 1, 2)

        self.button_login = QPushButton(self.page_4)
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

        self.gridlayout_login_box_2.addWidget(self.button_login, 2, 0, 1, 3)

        self.button_get_watched_videos = QPushButton(self.page_4)
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

        self.gridlayout_login_box_2.addWidget(self.button_get_watched_videos, 3, 0, 1, 1)

        self.button_get_liked_videos = QPushButton(self.page_4)
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

        self.gridlayout_login_box_2.addWidget(self.button_get_liked_videos, 3, 1, 1, 1)

        self.button_get_recommended_videos = QPushButton(self.page_4)
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


        self.gridLayout_4.addLayout(self.gridlayout_login_box_2, 0, 1, 1, 1)

        self.stacked_widget_top.addWidget(self.page_4)

        self.verticalLayout_6.addWidget(self.stacked_widget_top)

        self.scrollArea_4 = QScrollArea(self.page)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        sizePolicy.setHeightForWidth(self.scrollArea_4.sizePolicy().hasHeightForWidth())
        self.scrollArea_4.setSizePolicy(sizePolicy)
        self.scrollArea_4.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea_4.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea_4.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 944, 551))
        self.gridLayout_16 = QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radio_tree_show_title = QRadioButton(self.scrollAreaWidgetContents_4)
        self.radio_tree_show_title.setObjectName(u"radio_tree_show_title")
        sizePolicy2.setHeightForWidth(self.radio_tree_show_title.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_title.setSizePolicy(sizePolicy2)

        self.horizontalLayout_2.addWidget(self.radio_tree_show_title)

        self.radio_tree_show_all = QRadioButton(self.scrollAreaWidgetContents_4)
        self.radio_tree_show_all.setObjectName(u"radio_tree_show_all")
        sizePolicy.setHeightForWidth(self.radio_tree_show_all.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_all.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.radio_tree_show_all)


        self.gridLayout_7.addLayout(self.horizontalLayout_2, 0, 2, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.treeWidget = QTreeWidget(self.scrollAreaWidgetContents_4)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy4)
        self.treeWidget.setMinimumSize(QSize(300, 500))

        self.gridLayout_16.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)

        self.verticalLayout_6.addWidget(self.scrollArea_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_tree_download = QPushButton(self.page)
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

        self.horizontalLayout.addWidget(self.button_tree_download)

        self.button_tree_select_all = QPushButton(self.page)
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

        self.horizontalLayout.addWidget(self.button_tree_select_all)

        self.button_tree_unselect_all = QPushButton(self.page)
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

        self.horizontalLayout.addWidget(self.button_tree_unselect_all)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.gridLayout_5.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_4, 1, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_11 = QGridLayout(self.page_2)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.page_2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 958, 647))
        self.gridLayout_9 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.radio_directory_system_yes = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_directory_system_yes.setObjectName(u"radio_directory_system_yes")

        self.gridLayout_6.addWidget(self.radio_directory_system_yes, 8, 1, 1, 1)

        self.label_searching_limit = QLabel(self.scrollAreaWidgetContents)
        self.label_searching_limit.setObjectName(u"label_searching_limit")

        self.gridLayout_6.addWidget(self.label_searching_limit, 9, 0, 1, 1)

        self.radio_threading_yes = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_threading_yes.setObjectName(u"radio_threading_yes")

        self.gridLayout_6.addWidget(self.radio_threading_yes, 0, 1, 1, 2)

        self.radio_threading_mode_high_performance = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_threading_mode_high_performance.setObjectName(u"radio_threading_mode_high_performance")

        self.gridLayout_6.addWidget(self.radio_threading_mode_high_performance, 1, 1, 1, 1)

        self.radio_threading_mode_default = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_threading_mode_default.setObjectName(u"radio_threading_mode_default")

        self.gridLayout_6.addWidget(self.radio_threading_mode_default, 1, 3, 1, 1)

        self.radio_api_language_german = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_api_language_german.setObjectName(u"radio_api_language_german")

        self.gridLayout_6.addWidget(self.radio_api_language_german, 4, 2, 1, 1)

        self.button_settings_apply = QPushButton(self.scrollAreaWidgetContents)
        self.button_settings_apply.setObjectName(u"button_settings_apply")

        self.gridLayout_6.addWidget(self.button_settings_apply, 12, 0, 1, 5)

        self.radio_quality_best = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_quality_best.setObjectName(u"radio_quality_best")

        self.gridLayout_6.addWidget(self.radio_quality_best, 3, 1, 1, 1)

        self.radio_quality_worst = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_quality_worst.setObjectName(u"radio_quality_worst")

        self.gridLayout_6.addWidget(self.radio_quality_worst, 3, 3, 1, 2)

        self.button_threading_mode_help = QPushButton(self.scrollAreaWidgetContents)
        self.button_threading_mode_help.setObjectName(u"button_threading_mode_help")

        self.gridLayout_6.addWidget(self.button_threading_mode_help, 1, 4, 1, 1)

        self.label_output_path = QLabel(self.scrollAreaWidgetContents)
        self.label_output_path.setObjectName(u"label_output_path")

        self.gridLayout_6.addWidget(self.label_output_path, 6, 0, 1, 1)

        self.radio_threading_no = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_threading_no.setObjectName(u"radio_threading_no")

        self.gridLayout_6.addWidget(self.radio_threading_no, 0, 3, 1, 2)

        self.radio_ui_language_english = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_ui_language_english.setObjectName(u"radio_ui_language_english")

        self.gridLayout_6.addWidget(self.radio_ui_language_english, 11, 1, 1, 1)

        self.label_3 = QLabel(self.scrollAreaWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 4, 0, 1, 1)

        self.radio_api_language_chinese = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_api_language_chinese.setObjectName(u"radio_api_language_chinese")

        self.gridLayout_6.addWidget(self.radio_api_language_chinese, 4, 4, 1, 1)

        self.label_semaphore = QLabel(self.scrollAreaWidgetContents)
        self.label_semaphore.setObjectName(u"label_semaphore")

        self.gridLayout_6.addWidget(self.label_semaphore, 2, 0, 1, 1)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_6.addWidget(self.label_5, 11, 0, 1, 1)

        self.label_directory_system = QLabel(self.scrollAreaWidgetContents)
        self.label_directory_system.setObjectName(u"label_directory_system")

        self.gridLayout_6.addWidget(self.label_directory_system, 8, 0, 1, 1)

        self.button_directory_system_help = QPushButton(self.scrollAreaWidgetContents)
        self.button_directory_system_help.setObjectName(u"button_directory_system_help")

        self.gridLayout_6.addWidget(self.button_directory_system_help, 8, 3, 1, 2)

        self.radio_ui_language_german = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_ui_language_german.setObjectName(u"radio_ui_language_german")

        self.gridLayout_6.addWidget(self.radio_ui_language_german, 11, 2, 1, 1)

        self.spinbox_semaphore = QSpinBox(self.scrollAreaWidgetContents)
        self.spinbox_semaphore.setObjectName(u"spinbox_semaphore")
        self.spinbox_semaphore.setMinimum(1)
        self.spinbox_semaphore.setMaximum(10)

        self.gridLayout_6.addWidget(self.spinbox_semaphore, 2, 1, 1, 2)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_6.addWidget(self.label_2, 1, 0, 1, 1)

        self.radio_quality_half = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_quality_half.setObjectName(u"radio_quality_half")

        self.gridLayout_6.addWidget(self.radio_quality_half, 3, 2, 1, 1)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)

        self.radio_threading_mode_ffmpeg = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_threading_mode_ffmpeg.setObjectName(u"radio_threading_mode_ffmpeg")
        self.radio_threading_mode_ffmpeg.setCheckable(False)

        self.gridLayout_6.addWidget(self.radio_threading_mode_ffmpeg, 1, 2, 1, 1)

        self.button_semaphore_help = QPushButton(self.scrollAreaWidgetContents)
        self.button_semaphore_help.setObjectName(u"button_semaphore_help")

        self.gridLayout_6.addWidget(self.button_semaphore_help, 2, 3, 1, 2)

        self.lineedit_output_path = QLineEdit(self.scrollAreaWidgetContents)
        self.lineedit_output_path.setObjectName(u"lineedit_output_path")

        self.gridLayout_6.addWidget(self.lineedit_output_path, 6, 3, 1, 2)

        self.label_semaphore_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_semaphore_2.setObjectName(u"label_semaphore_2")

        self.gridLayout_6.addWidget(self.label_semaphore_2, 3, 0, 1, 1)

        self.radio_directory_system_no = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_directory_system_no.setObjectName(u"radio_directory_system_no")

        self.gridLayout_6.addWidget(self.radio_directory_system_no, 8, 2, 1, 1)

        self.radio_ui_language_french = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_ui_language_french.setObjectName(u"radio_ui_language_french")
        self.radio_ui_language_french.setEnabled(False)

        self.gridLayout_6.addWidget(self.radio_ui_language_french, 11, 3, 1, 2)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 6, 1, 1, 2)

        self.spinbox_searching = QSpinBox(self.scrollAreaWidgetContents)
        self.spinbox_searching.setObjectName(u"spinbox_searching")
        self.spinbox_searching.setMinimum(1)
        self.spinbox_searching.setMaximum(200)

        self.gridLayout_6.addWidget(self.spinbox_searching, 9, 1, 1, 4)

        self.radio_api_language_english = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_api_language_english.setObjectName(u"radio_api_language_english")

        self.gridLayout_6.addWidget(self.radio_api_language_english, 4, 1, 1, 1)

        self.radio_api_language_french = QRadioButton(self.scrollAreaWidgetContents)
        self.radio_api_language_french.setObjectName(u"radio_api_language_french")

        self.gridLayout_6.addWidget(self.radio_api_language_french, 4, 3, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_3, 13, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.gridLayout_11.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_2)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_12 = QGridLayout(self.page_7)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea_2 = QScrollArea(self.page_7)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 958, 647))
        self.gridLayout_8 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_8.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_3.addWidget(self.scrollArea_2)


        self.gridLayout_12.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_7)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout_13 = QGridLayout(self.page_8)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.scrollArea_3 = QScrollArea(self.page_8)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 944, 662))
        self.gridLayout_10 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.button_metadata_user_start = QPushButton(self.scrollAreaWidgetContents_3)
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

        self.label_metadata_video_url = QLabel(self.scrollAreaWidgetContents_3)
        self.label_metadata_video_url.setObjectName(u"label_metadata_video_url")

        self.gridLayout_27.addWidget(self.label_metadata_video_url, 0, 0, 1, 1)

        self.lineedit_metadata_video_url = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_metadata_video_url.setObjectName(u"lineedit_metadata_video_url")

        self.gridLayout_27.addWidget(self.lineedit_metadata_video_url, 0, 1, 1, 1)

        self.label_metadata_user_url = QLabel(self.scrollAreaWidgetContents_3)
        self.label_metadata_user_url.setObjectName(u"label_metadata_user_url")

        self.gridLayout_27.addWidget(self.label_metadata_user_url, 1, 0, 1, 1)

        self.button_metadata_video_start = QPushButton(self.scrollAreaWidgetContents_3)
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

        self.lineedit_metadata_user_url = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_metadata_user_url.setObjectName(u"lineedit_metadata_user_url")

        self.gridLayout_27.addWidget(self.lineedit_metadata_user_url, 1, 1, 1, 1)

        self.gridLayout_30 = QGridLayout()
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.lineedit_user_tattoos = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_tattoos.setObjectName(u"lineedit_user_tattoos")

        self.gridLayout_30.addWidget(self.lineedit_user_tattoos, 8, 3, 1, 1)

        self.lineedit_user_birth_place = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_birth_place.setObjectName(u"lineedit_user_birth_place")

        self.gridLayout_30.addWidget(self.lineedit_user_birth_place, 8, 1, 1, 1)

        self.label_video_views = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_views.setObjectName(u"label_video_views")

        self.gridLayout_30.addWidget(self.label_video_views, 4, 2, 1, 1)

        self.lineedit_user_videos_watched = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_videos_watched.setObjectName(u"lineedit_user_videos_watched")

        self.gridLayout_30.addWidget(self.lineedit_user_videos_watched, 6, 3, 1, 1)

        self.lineedit_user_interests_hobbies = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_interests_hobbies.setObjectName(u"lineedit_user_interests_hobbies")

        self.gridLayout_30.addWidget(self.lineedit_user_interests_hobbies, 7, 1, 1, 1)

        self.lineedit_user_gender = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_gender.setObjectName(u"lineedit_user_gender")

        self.gridLayout_30.addWidget(self.lineedit_user_gender, 2, 1, 1, 1)

        self.label_relationship = QLabel(self.scrollAreaWidgetContents_3)
        self.label_relationship.setObjectName(u"label_relationship")

        self.gridLayout_30.addWidget(self.label_relationship, 0, 0, 1, 1)

        self.lineedit_user_hair_color = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_hair_color.setObjectName(u"lineedit_user_hair_color")

        self.gridLayout_30.addWidget(self.lineedit_user_hair_color, 6, 1, 1, 1)

        self.lineedit_user_relationship = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_relationship.setObjectName(u"lineedit_user_relationship")

        self.gridLayout_30.addWidget(self.lineedit_user_relationship, 0, 1, 1, 1)

        self.label_hair_color = QLabel(self.scrollAreaWidgetContents_3)
        self.label_hair_color.setObjectName(u"label_hair_color")

        self.gridLayout_30.addWidget(self.label_hair_color, 6, 0, 1, 1)

        self.label_widght = QLabel(self.scrollAreaWidgetContents_3)
        self.label_widght.setObjectName(u"label_widght")

        self.gridLayout_30.addWidget(self.label_widght, 4, 0, 1, 1)

        self.label_piercings = QLabel(self.scrollAreaWidgetContents_3)
        self.label_piercings.setObjectName(u"label_piercings")

        self.gridLayout_30.addWidget(self.label_piercings, 0, 2, 1, 1)

        self.label_interested_in = QLabel(self.scrollAreaWidgetContents_3)
        self.label_interested_in.setObjectName(u"label_interested_in")

        self.gridLayout_30.addWidget(self.label_interested_in, 1, 0, 1, 1)

        self.lineedit_user_ethnicity = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_ethnicity.setObjectName(u"lineedit_user_ethnicity")

        self.gridLayout_30.addWidget(self.lineedit_user_ethnicity, 5, 1, 1, 1)

        self.lineedit_user_profile_views = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_profile_views.setObjectName(u"lineedit_user_profile_views")

        self.gridLayout_30.addWidget(self.lineedit_user_profile_views, 5, 3, 1, 1)

        self.lineedit_user_turn_ons = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_turn_ons.setObjectName(u"lineedit_user_turn_ons")

        self.gridLayout_30.addWidget(self.lineedit_user_turn_ons, 2, 3, 1, 1)

        self.label_ethnicity = QLabel(self.scrollAreaWidgetContents_3)
        self.label_ethnicity.setObjectName(u"label_ethnicity")

        self.gridLayout_30.addWidget(self.label_ethnicity, 5, 0, 1, 1)

        self.label_turn_ons = QLabel(self.scrollAreaWidgetContents_3)
        self.label_turn_ons.setObjectName(u"label_turn_ons")

        self.gridLayout_30.addWidget(self.label_turn_ons, 2, 2, 1, 1)

        self.label_gender = QLabel(self.scrollAreaWidgetContents_3)
        self.label_gender.setObjectName(u"label_gender")

        self.gridLayout_30.addWidget(self.label_gender, 2, 0, 1, 1)

        self.lineedit_user_piercings = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_piercings.setObjectName(u"lineedit_user_piercings")

        self.gridLayout_30.addWidget(self.lineedit_user_piercings, 0, 3, 1, 1)

        self.lineedit_user_height = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_height.setObjectName(u"lineedit_user_height")

        self.gridLayout_30.addWidget(self.lineedit_user_height, 3, 1, 1, 1)

        self.label_profile_views = QLabel(self.scrollAreaWidgetContents_3)
        self.label_profile_views.setObjectName(u"label_profile_views")

        self.gridLayout_30.addWidget(self.label_profile_views, 5, 2, 1, 1)

        self.label_city_country = QLabel(self.scrollAreaWidgetContents_3)
        self.label_city_country.setObjectName(u"label_city_country")

        self.gridLayout_30.addWidget(self.label_city_country, 7, 2, 1, 1)

        self.label_fake_boobs = QLabel(self.scrollAreaWidgetContents_3)
        self.label_fake_boobs.setObjectName(u"label_fake_boobs")

        self.gridLayout_30.addWidget(self.label_fake_boobs, 1, 2, 1, 1)

        self.label_birth_place = QLabel(self.scrollAreaWidgetContents_3)
        self.label_birth_place.setObjectName(u"label_birth_place")

        self.gridLayout_30.addWidget(self.label_birth_place, 8, 0, 1, 1)

        self.label_interests_hobbies = QLabel(self.scrollAreaWidgetContents_3)
        self.label_interests_hobbies.setObjectName(u"label_interests_hobbies")

        self.gridLayout_30.addWidget(self.label_interests_hobbies, 7, 0, 1, 1)

        self.lineedit_user_city_country = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_city_country.setObjectName(u"lineedit_user_city_country")

        self.gridLayout_30.addWidget(self.lineedit_user_city_country, 7, 3, 1, 1)

        self.lineedit_user_weight = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_weight.setObjectName(u"lineedit_user_weight")

        self.gridLayout_30.addWidget(self.lineedit_user_weight, 4, 1, 1, 1)

        self.lineedit_user_interested_in = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_interested_in.setObjectName(u"lineedit_user_interested_in")

        self.gridLayout_30.addWidget(self.lineedit_user_interested_in, 1, 1, 1, 1)

        self.label_turn_offs = QLabel(self.scrollAreaWidgetContents_3)
        self.label_turn_offs.setObjectName(u"label_turn_offs")

        self.gridLayout_30.addWidget(self.label_turn_offs, 3, 2, 1, 1)

        self.label_height = QLabel(self.scrollAreaWidgetContents_3)
        self.label_height.setObjectName(u"label_height")

        self.gridLayout_30.addWidget(self.label_height, 3, 0, 1, 1)

        self.lineedit_user_fake_boobs = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_fake_boobs.setObjectName(u"lineedit_user_fake_boobs")

        self.gridLayout_30.addWidget(self.lineedit_user_fake_boobs, 1, 3, 1, 1)

        self.lineedit_user_video_views = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_video_views.setObjectName(u"lineedit_user_video_views")

        self.gridLayout_30.addWidget(self.lineedit_user_video_views, 4, 3, 1, 1)

        self.lineedit_user_turn_offs = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_turn_offs.setObjectName(u"lineedit_user_turn_offs")

        self.gridLayout_30.addWidget(self.lineedit_user_turn_offs, 3, 3, 1, 1)

        self.label_videos_watched = QLabel(self.scrollAreaWidgetContents_3)
        self.label_videos_watched.setObjectName(u"label_videos_watched")

        self.gridLayout_30.addWidget(self.label_videos_watched, 6, 2, 1, 1)

        self.label_tattoos = QLabel(self.scrollAreaWidgetContents_3)
        self.label_tattoos.setObjectName(u"label_tattoos")

        self.gridLayout_30.addWidget(self.label_tattoos, 8, 2, 1, 1)

        self.label_home_town = QLabel(self.scrollAreaWidgetContents_3)
        self.label_home_town.setObjectName(u"label_home_town")

        self.gridLayout_30.addWidget(self.label_home_town, 9, 0, 1, 1)

        self.lineedit_user_home_town = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_home_town.setObjectName(u"lineedit_user_home_town")

        self.gridLayout_30.addWidget(self.lineedit_user_home_town, 9, 1, 1, 1)

        self.gridLayout_39 = QGridLayout()
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.lineedit_user_type = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_type.setObjectName(u"lineedit_user_type")

        self.gridLayout_39.addWidget(self.lineedit_user_type, 2, 1, 1, 1)

        self.button_user_get_bio = QPushButton(self.scrollAreaWidgetContents_3)
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

        self.gridLayout_39.addWidget(self.button_user_get_bio, 3, 1, 1, 1)

        self.button_user_download_avatar = QPushButton(self.scrollAreaWidgetContents_3)
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

        self.gridLayout_39.addWidget(self.button_user_download_avatar, 3, 0, 1, 1)

        self.lineedit_user_name = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_user_name.setObjectName(u"lineedit_user_name")

        self.gridLayout_39.addWidget(self.lineedit_user_name, 1, 1, 1, 1)

        self.label_13 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_39.addWidget(self.label_13, 2, 0, 1, 1)

        self.label_12 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_39.addWidget(self.label_12, 1, 0, 1, 1)

        self.gridLayout_37 = QGridLayout()
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.lineedit_video_pornstars = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_pornstars.setObjectName(u"lineedit_video_pornstars")

        self.gridLayout_37.addWidget(self.lineedit_video_pornstars, 4, 1, 1, 1)

        self.lineedit_video_title = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_title.setObjectName(u"lineedit_video_title")

        self.gridLayout_37.addWidget(self.lineedit_video_title, 0, 1, 1, 1)

        self.label_video_tags = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_tags.setObjectName(u"label_video_tags")

        self.gridLayout_37.addWidget(self.label_video_tags, 1, 2, 1, 1)

        self.label_video_orientation = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_orientation.setObjectName(u"label_video_orientation")

        self.gridLayout_37.addWidget(self.label_video_orientation, 4, 2, 1, 1)

        self.lineedit_video_rating = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_rating.setObjectName(u"lineedit_video_rating")

        self.gridLayout_37.addWidget(self.lineedit_video_rating, 2, 3, 1, 1)

        self.lineedit_video_orientation = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_orientation.setObjectName(u"lineedit_video_orientation")

        self.gridLayout_37.addWidget(self.lineedit_video_orientation, 4, 3, 1, 1)

        self.lineedit_video_hotspots = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_hotspots.setObjectName(u"lineedit_video_hotspots")

        self.gridLayout_37.addWidget(self.lineedit_video_hotspots, 0, 3, 1, 1)

        self.lineedit_video_duration = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_duration.setObjectName(u"lineedit_video_duration")

        self.gridLayout_37.addWidget(self.lineedit_video_duration, 2, 1, 1, 1)

        self.label_video_hotspots = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_hotspots.setObjectName(u"label_video_hotspots")

        self.gridLayout_37.addWidget(self.label_video_hotspots, 0, 2, 1, 1)

        self.label_video_title = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_title.setObjectName(u"label_video_title")

        self.gridLayout_37.addWidget(self.label_video_title, 0, 0, 1, 1)

        self.label_video_pornstars = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_pornstars.setObjectName(u"label_video_pornstars")

        self.gridLayout_37.addWidget(self.label_video_pornstars, 4, 0, 1, 1)

        self.lineedit_video_views = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_views.setObjectName(u"lineedit_video_views")

        self.gridLayout_37.addWidget(self.lineedit_video_views, 1, 1, 1, 1)

        self.lineedit_video_tags = QLineEdit(self.scrollAreaWidgetContents_3)
        self.lineedit_video_tags.setObjectName(u"lineedit_video_tags")

        self.gridLayout_37.addWidget(self.lineedit_video_tags, 1, 3, 1, 1)

        self.label_video_duration = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_duration.setObjectName(u"label_video_duration")

        self.gridLayout_37.addWidget(self.label_video_duration, 2, 0, 1, 1)

        self.label_video_rating = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_rating.setObjectName(u"label_video_rating")

        self.gridLayout_37.addWidget(self.label_video_rating, 2, 2, 1, 1)

        self.label_video_views_2 = QLabel(self.scrollAreaWidgetContents_3)
        self.label_video_views_2.setObjectName(u"label_video_views_2")

        self.gridLayout_37.addWidget(self.label_video_views_2, 1, 0, 1, 1)

        self.button_video_thumbnail_download = QPushButton(self.scrollAreaWidgetContents_3)
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

        self.gridLayout_37.addWidget(self.button_video_thumbnail_download, 5, 0, 1, 4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_37.addItem(self.verticalSpacer_2, 6, 0, 1, 1)


        self.gridLayout_39.addLayout(self.gridLayout_37, 4, 0, 1, 2)


        self.gridLayout_30.addLayout(self.gridLayout_39, 10, 0, 1, 4)


        self.gridLayout_27.addLayout(self.gridLayout_30, 2, 0, 1, 3)


        self.gridLayout_10.addLayout(self.gridLayout_27, 0, 0, 1, 1)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_4.addWidget(self.scrollArea_3)


        self.gridLayout_13.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_8)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_20 = QGridLayout(self.page_5)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.lineedit_seach_pornhub_filters = QLineEdit(self.page_5)
        self.lineedit_seach_pornhub_filters.setObjectName(u"lineedit_seach_pornhub_filters")
        sizePolicy1.setHeightForWidth(self.lineedit_seach_pornhub_filters.sizePolicy().hasHeightForWidth())
        self.lineedit_seach_pornhub_filters.setSizePolicy(sizePolicy1)
        self.lineedit_seach_pornhub_filters.setMinimumSize(QSize(100, 0))

        self.gridLayout_14.addWidget(self.lineedit_seach_pornhub_filters, 2, 1, 1, 1)

        self.lineedit_search_hqporner = QLineEdit(self.page_5)
        self.lineedit_search_hqporner.setObjectName(u"lineedit_search_hqporner")
        sizePolicy1.setHeightForWidth(self.lineedit_search_hqporner.sizePolicy().hasHeightForWidth())
        self.lineedit_search_hqporner.setSizePolicy(sizePolicy1)
        self.lineedit_search_hqporner.setMinimumSize(QSize(100, 0))

        self.gridLayout_14.addWidget(self.lineedit_search_hqporner, 1, 1, 1, 1)

        self.label_query_1 = QLabel(self.page_5)
        self.label_query_1.setObjectName(u"label_query_1")

        self.gridLayout_14.addWidget(self.label_query_1, 1, 0, 1, 1)

        self.label_query_3 = QLabel(self.page_5)
        self.label_query_3.setObjectName(u"label_query_3")

        self.gridLayout_14.addWidget(self.label_query_3, 3, 0, 1, 1)

        self.button_search_hqporner = QPushButton(self.page_5)
        self.button_search_hqporner.setObjectName(u"button_search_hqporner")

        self.gridLayout_14.addWidget(self.button_search_hqporner, 1, 2, 1, 1)

        self.label_query_2 = QLabel(self.page_5)
        self.label_query_2.setObjectName(u"label_query_2")

        self.gridLayout_14.addWidget(self.label_query_2, 2, 0, 1, 1)

        self.button_search_pornhub_filters = QPushButton(self.page_5)
        self.button_search_pornhub_filters.setObjectName(u"button_search_pornhub_filters")

        self.gridLayout_14.addWidget(self.button_search_pornhub_filters, 2, 2, 1, 1)

        self.lineedit_search_users = QLineEdit(self.page_5)
        self.lineedit_search_users.setObjectName(u"lineedit_search_users")
        sizePolicy1.setHeightForWidth(self.lineedit_search_users.sizePolicy().hasHeightForWidth())
        self.lineedit_search_users.setSizePolicy(sizePolicy1)
        self.lineedit_search_users.setMinimumSize(QSize(100, 0))

        self.gridLayout_14.addWidget(self.lineedit_search_users, 3, 1, 1, 1)

        self.button_search_users = QPushButton(self.page_5)
        self.button_search_users.setObjectName(u"button_search_users")

        self.gridLayout_14.addWidget(self.button_search_users, 3, 2, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_14, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.scroll_area_search_filters_ = QScrollArea(self.page_5)
        self.scroll_area_search_filters_.setObjectName(u"scroll_area_search_filters_")
        sizePolicy4.setHeightForWidth(self.scroll_area_search_filters_.sizePolicy().hasHeightForWidth())
        self.scroll_area_search_filters_.setSizePolicy(sizePolicy4)
        self.scroll_area_search_filters_.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 475, 552))
        self.gridLayout_19 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridlayout_search_filter = QGridLayout()
        self.gridlayout_search_filter.setObjectName(u"gridlayout_search_filter")

        self.gridLayout_19.addLayout(self.gridlayout_search_filter, 0, 0, 1, 1)

        self.scroll_area_search_filters_.setWidget(self.scrollAreaWidgetContents_6)

        self.horizontalLayout_3.addWidget(self.scroll_area_search_filters_)

        self.scroll_area_search_filters = QScrollArea(self.page_5)
        self.scroll_area_search_filters.setObjectName(u"scroll_area_search_filters")
        sizePolicy4.setHeightForWidth(self.scroll_area_search_filters.sizePolicy().hasHeightForWidth())
        self.scroll_area_search_filters.setSizePolicy(sizePolicy4)
        self.scroll_area_search_filters.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 475, 552))
        self.gridLayout_18 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridlayout_user_filter = QGridLayout()
        self.gridlayout_user_filter.setObjectName(u"gridlayout_user_filter")

        self.gridLayout_18.addLayout(self.gridlayout_user_filter, 0, 0, 1, 1)

        self.scroll_area_search_filters.setWidget(self.scrollAreaWidgetContents_5)

        self.horizontalLayout_3.addWidget(self.scroll_area_search_filters)


        self.gridLayout_20.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.stacked_widget_main.addWidget(self.page_5)

        self.gridLayout_2.addWidget(self.stacked_widget_main, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.widget, 0, 1, 1, 1)


        self.gridLayout_17.addLayout(self.gridLayout_15, 0, 0, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(4)
        self.stacked_widget_top.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch V3 (C) Johannes Habel GPL 3", None))
        self.button_switch_home.setText("")
        self.button_switch_account.setText("")
        self.button_switch_search.setText("")
        self.button_switch_settings.setText("")
        self.button_switch_metadata.setText("")
        self.button_switch_credits.setText("")
        self.label_progress_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub:", None))
        self.label_progress_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner:", None))
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"This feature does not work on Android, because there's a Bug in the QFileDialog, which I can't fix!", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub Model / Channel URL or a HQPorner Actresss name (e.g Anissa Kate or anissa-kate)", None))
        self.button_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub or HQPorner Video URL", None))
        self.label_search_query.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter a Search query for PornHub. For Advanced searching use the search tab on the left", None))
        self.button_open_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.button_search_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.button_get_watched_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.button_get_liked_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.button_get_recommended_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.radio_tree_show_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Only Title (a lot faster)", None))
        self.radio_tree_show_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Title, Author, Duration", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Porn_Fetch_Widget", u"Duration", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Porn_Fetch_Widget", u"Author", None));
        self.button_tree_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Selected Videos", None))
        self.button_tree_select_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select all", None))
        self.button_tree_unselect_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselect all", None))
        self.radio_directory_system_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.label_searching_limit.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Limit:", None))
        self.radio_threading_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_threading_mode_high_performance.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"High Performance", None))
        self.radio_threading_mode_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Default", None))
        self.radio_api_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Apply / Reload", None))
        self.radio_quality_best.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Best", None))
        self.radio_quality_worst.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Worst", None))
        self.button_threading_mode_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_output_path.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Output path:", None))
        self.radio_threading_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.radio_ui_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.label_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"API Language", None))
        self.radio_api_language_chinese.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese", None))
        self.label_semaphore.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Semaphore:", None))
        self.label_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Language:", None))
        self.label_directory_system.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Use Directory system? ", None))
        self.button_directory_system_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.radio_ui_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading Mode:", None))
        self.radio_quality_half.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Half", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading:", None))
        self.radio_threading_mode_ffmpeg.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"FFMPEG", None))
        self.button_semaphore_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.lineedit_output_path.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter \"./\" for current directory", None))
        self.label_semaphore_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Quality:", None))
        self.radio_directory_system_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.radio_ui_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.label_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"DO NOT CHANGE UNLESS YOU KNOW WHAT YOU DO", None))
        self.radio_api_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_api_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.button_metadata_user_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_metadata_video_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Video URL:", None))
        self.label_metadata_user_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User URL:", None))
        self.button_metadata_video_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_video_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Video Views:", None))
        self.label_relationship.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Relationship:", None))
        self.label_hair_color.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hair Color:", None))
        self.label_widght.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Weight:", None))
        self.label_piercings.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Piercings:", None))
        self.label_interested_in.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Interested in:", None))
        self.label_ethnicity.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Ethnicity:", None))
        self.label_turn_ons.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Turn Ons:", None))
        self.label_gender.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Gender:", None))
        self.label_profile_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Profile Views:", None))
        self.label_city_country.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"City / Country:", None))
        self.label_fake_boobs.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Fake Boobs:", None))
        self.label_birth_place.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Birth Place:", None))
        self.label_interests_hobbies.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Interests / Hobbies:", None))
        self.label_turn_offs.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Turn Offs:", None))
        self.label_height.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Height:", None))
        self.label_videos_watched.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Videos Watched:", None))
        self.label_tattoos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tattoos:", None))
        self.label_home_town.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home Town", None))
        self.button_user_get_bio.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get User's Bio", None))
        self.button_user_download_avatar.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download User Avatar", None))
        self.label_13.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User Type:", None))
        self.label_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Name:", None))
        self.label_video_tags.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tags:", None))
        self.label_video_orientation.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Orientation:", None))
        self.label_video_hotspots.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hotspots:", None))
        self.label_video_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Title:", None))
        self.label_video_pornstars.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Pornstars:", None))
        self.label_video_duration.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Duration:", None))
        self.label_video_rating.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Rating:", None))
        self.label_video_views_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Views:", None))
        self.button_video_thumbnail_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Thumbnail", None))
        self.lineedit_seach_pornhub_filters.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search on PornHub (with filters defined below)", None))
        self.lineedit_search_hqporner.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search for videos on HQPorner.com", None))
        self.label_query_1.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Query:", None))
        self.label_query_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Query:", None))
        self.button_search_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_query_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Query:", None))
        self.button_search_pornhub_filters.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.lineedit_search_users.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search for Users (with filters defined below)", None))
        self.button_search_users.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
    # retranslateUi

