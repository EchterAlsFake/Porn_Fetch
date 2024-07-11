# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_desktop.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QProgressBar, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1210, 869)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Porn_Fetch_Widget.sizePolicy().hasHeightForWidth())
        Porn_Fetch_Widget.setSizePolicy(sizePolicy)
        Porn_Fetch_Widget.setMinimumSize(QSize(100, 50))
        self.gridLayout = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridlayout_main = QGridLayout()
        self.gridlayout_main.setObjectName(u"gridlayout_main")
        self.gridlayout_main.setContentsMargins(-1, -1, -1, 0)
        self.groupbox_top_bar = QGroupBox(Porn_Fetch_Widget)
        self.groupbox_top_bar.setObjectName(u"groupbox_top_bar")
        self.gridLayout_14 = QGridLayout(self.groupbox_top_bar)
        self.gridLayout_14.setSpacing(3)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(-1, -1, -1, 3)
        self.button_switch_settings = QPushButton(self.groupbox_top_bar)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_switch_settings.sizePolicy().hasHeightForWidth())
        self.button_switch_settings.setSizePolicy(sizePolicy1)
        self.button_switch_settings.setMinimumSize(QSize(50, 35))
        self.button_switch_settings.setMaximumSize(QSize(16777215, 35))
        self.button_switch_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"QPushButton {\n"
"    background-color: #800080;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 3px solid #dda0dd;\n"
"    padding: 8px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #9932cc;\n"
"    border: 3px solid #ba55d3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4b0082;\n"
"}\n"
"")
        self.button_switch_settings.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.button_switch_settings, 0, 3, 1, 1)

        self.button_switch_tools = QPushButton(self.groupbox_top_bar)
        self.button_switch_tools.setObjectName(u"button_switch_tools")
        sizePolicy1.setHeightForWidth(self.button_switch_tools.sizePolicy().hasHeightForWidth())
        self.button_switch_tools.setSizePolicy(sizePolicy1)
        self.button_switch_tools.setMinimumSize(QSize(50, 35))
        self.button_switch_tools.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        font.setPointSize(9)
        self.button_switch_tools.setFont(font)
        self.button_switch_tools.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_tools.setStyleSheet(u"QPushButton {\n"
"    background-color: #000000;\n"
"    color: #ffffff;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #ffffff;\n"
"    padding: 8px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #333333;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #666666;\n"
"}\n"
"")
        self.button_switch_tools.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.button_switch_tools, 0, 2, 1, 1)

        self.button_switch_home = QPushButton(self.groupbox_top_bar)
        self.button_switch_home.setObjectName(u"button_switch_home")
        sizePolicy1.setHeightForWidth(self.button_switch_home.sizePolicy().hasHeightForWidth())
        self.button_switch_home.setSizePolicy(sizePolicy1)
        self.button_switch_home.setMinimumSize(QSize(50, 35))
        self.button_switch_home.setMaximumSize(QSize(16777215, 35))
        self.button_switch_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"QPushButton {\n"
"    background-color: #4CAF50;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #0078d7;\n"
"    padding: 8px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #66BB6A;\n"
"    border: 2px solid #005bb5;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #388E3C;\n"
"}\n"
"")
        self.button_switch_home.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.button_switch_home, 0, 0, 1, 1)

        self.button_switch_credits = QPushButton(self.groupbox_top_bar)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        sizePolicy1.setHeightForWidth(self.button_switch_credits.sizePolicy().hasHeightForWidth())
        self.button_switch_credits.setSizePolicy(sizePolicy1)
        self.button_switch_credits.setMinimumSize(QSize(50, 35))
        self.button_switch_credits.setMaximumSize(QSize(16777215, 35))
        self.button_switch_credits.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"QPushButton {\n"
"    background-color: #008CBA;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: none;\n"
"    padding: 8px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #00A3CC;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #005F8C;\n"
"}\n"
"")
        self.button_switch_credits.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.button_switch_credits, 0, 4, 1, 1)

        self.button_switch_account = QPushButton(self.groupbox_top_bar)
        self.button_switch_account.setObjectName(u"button_switch_account")
        sizePolicy1.setHeightForWidth(self.button_switch_account.sizePolicy().hasHeightForWidth())
        self.button_switch_account.setSizePolicy(sizePolicy1)
        self.button_switch_account.setMinimumSize(QSize(50, 35))
        self.button_switch_account.setMaximumSize(QSize(16777215, 35))
        self.button_switch_account.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_account.setStyleSheet(u"QPushButton {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ff7f50, stop:1 #ff4500);\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: none;\n"
"    padding: 8px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #ffa07a, stop:1 #ff6347);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #cd5c5c, stop:1 #b22222);\n"
"}\n"
"")
        self.button_switch_account.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.button_switch_account, 0, 1, 1, 1)

        self.button_view_progress_bars = QPushButton(self.groupbox_top_bar)
        self.button_view_progress_bars.setObjectName(u"button_view_progress_bars")
        sizePolicy1.setHeightForWidth(self.button_view_progress_bars.sizePolicy().hasHeightForWidth())
        self.button_view_progress_bars.setSizePolicy(sizePolicy1)
        self.button_view_progress_bars.setMinimumSize(QSize(50, 35))
        self.button_view_progress_bars.setMaximumSize(QSize(16777215, 35))
        self.button_view_progress_bars.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_view_progress_bars.setStyleSheet(u"QPushButton {\n"
"    background-color: #808080;\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #a9a9a9;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #696969;\n"
"}\n"
"")
        self.button_view_progress_bars.setIconSize(QSize(32, 32))

        self.gridLayout_14.addWidget(self.button_view_progress_bars, 0, 5, 1, 1)


        self.gridlayout_main.addWidget(self.groupbox_top_bar, 0, 0, 1, 1)

        self.stacked_widget_main = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.stacked_widget_main.setLineWidth(1)
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.gridLayout_8 = QGridLayout(self.widget)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticallayout_treewidget = QVBoxLayout()
        self.verticallayout_treewidget.setObjectName(u"verticallayout_treewidget")
        self.stacked_widget_top = QStackedWidget(self.widget)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.stacked_widget_top.setSizePolicy(sizePolicy2)
        self.stacked_widget_top.setMinimumSize(QSize(650, 20))
        self.stacked_widget_top.setStyleSheet(u"b")
        self.stacked_widget_top.setLineWidth(1)
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        self.gridLayout_5 = QGridLayout(self.page_download)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SetMaximumSize)
        self.gridlayout_downloading.setHorizontalSpacing(0)
        self.gridlayout_downloading.setVerticalSpacing(6)
        self.button_search = QPushButton(self.page_download)
        self.button_search.setObjectName(u"button_search")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy3)
        self.button_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search, 7, 3, 1, 1)

        self.lineedit_url = QLineEdit(self.page_download)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy4)
        self.lineedit_url.setMinimumSize(QSize(300, 4))

        self.gridlayout_downloading.addWidget(self.lineedit_url, 2, 1, 1, 2)

        self.button_open_file = QPushButton(self.page_download)
        self.button_open_file.setObjectName(u"button_open_file")
        sizePolicy3.setHeightForWidth(self.button_open_file.sizePolicy().hasHeightForWidth())
        self.button_open_file.setSizePolicy(sizePolicy3)
        self.button_open_file.setMinimumSize(QSize(60, 2))
        self.button_open_file.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_open_file.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_open_file, 6, 3, 1, 1)

        self.label_search_website = QLabel(self.page_download)
        self.label_search_website.setObjectName(u"label_search_website")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_search_website.sizePolicy().hasHeightForWidth())
        self.label_search_website.setSizePolicy(sizePolicy5)

        self.gridlayout_downloading.addWidget(self.label_search_website, 9, 0, 1, 1)

        self.button_model = QPushButton(self.page_download)
        self.button_model.setObjectName(u"button_model")
        sizePolicy3.setHeightForWidth(self.button_model.sizePolicy().hasHeightForWidth())
        self.button_model.setSizePolicy(sizePolicy3)
        self.button_model.setMinimumSize(QSize(60, 2))
        self.button_model.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_model.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_model, 5, 3, 1, 1)

        self.button_download = QPushButton(self.page_download)
        self.button_download.setObjectName(u"button_download")
        sizePolicy3.setHeightForWidth(self.button_download.sizePolicy().hasHeightForWidth())
        self.button_download.setSizePolicy(sizePolicy3)
        self.button_download.setMinimumSize(QSize(60, 2))
        self.button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_download, 2, 3, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page_download)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")
        sizePolicy4.setHeightForWidth(self.lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.lineedit_model_url.setSizePolicy(sizePolicy4)
        self.lineedit_model_url.setMinimumSize(QSize(300, 2))

        self.gridlayout_downloading.addWidget(self.lineedit_model_url, 5, 1, 1, 2)

        self.horizontallayout_searching_websites = QHBoxLayout()
        self.horizontallayout_searching_websites.setSpacing(4)
        self.horizontallayout_searching_websites.setObjectName(u"horizontallayout_searching_websites")
        self.horizontallayout_searching_websites.setContentsMargins(-1, 5, 5, -1)
        self.radio_search_website_pornhub = QRadioButton(self.page_download)
        self.radio_search_website_pornhub.setObjectName(u"radio_search_website_pornhub")
        self.radio_search_website_pornhub.setChecked(True)

        self.horizontallayout_searching_websites.addWidget(self.radio_search_website_pornhub)

        self.radio_search_website_hqporner = QRadioButton(self.page_download)
        self.radio_search_website_hqporner.setObjectName(u"radio_search_website_hqporner")

        self.horizontallayout_searching_websites.addWidget(self.radio_search_website_hqporner)

        self.radio_search_website_xvideos = QRadioButton(self.page_download)
        self.radio_search_website_xvideos.setObjectName(u"radio_search_website_xvideos")

        self.horizontallayout_searching_websites.addWidget(self.radio_search_website_xvideos)

        self.radio_search_website_eporner = QRadioButton(self.page_download)
        self.radio_search_website_eporner.setObjectName(u"radio_search_website_eporner")

        self.horizontallayout_searching_websites.addWidget(self.radio_search_website_eporner)

        self.radio_search_website_xnxx = QRadioButton(self.page_download)
        self.radio_search_website_xnxx.setObjectName(u"radio_search_website_xnxx")

        self.horizontallayout_searching_websites.addWidget(self.radio_search_website_xnxx)

        self.horizontalspacer_search = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontallayout_searching_websites.addItem(self.horizontalspacer_search)

        self.button_switch_supported_websites = QPushButton(self.page_download)
        self.button_switch_supported_websites.setObjectName(u"button_switch_supported_websites")
        sizePolicy1.setHeightForWidth(self.button_switch_supported_websites.sizePolicy().hasHeightForWidth())
        self.button_switch_supported_websites.setSizePolicy(sizePolicy1)
        self.button_switch_supported_websites.setMinimumSize(QSize(0, 25))
        self.button_switch_supported_websites.setMaximumSize(QSize(16777215, 20))
        self.button_switch_supported_websites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_searching_websites.addWidget(self.button_switch_supported_websites)


        self.gridlayout_downloading.addLayout(self.horizontallayout_searching_websites, 9, 1, 1, 3)

        self.lineedit_file = QLineEdit(self.page_download)
        self.lineedit_file.setObjectName(u"lineedit_file")
        sizePolicy4.setHeightForWidth(self.lineedit_file.sizePolicy().hasHeightForWidth())
        self.lineedit_file.setSizePolicy(sizePolicy4)
        self.lineedit_file.setMinimumSize(QSize(300, 2))
        self.lineedit_file.setReadOnly(True)

        self.gridlayout_downloading.addWidget(self.lineedit_file, 6, 1, 1, 1)

        self.label_url = QLabel(self.page_download)
        self.label_url.setObjectName(u"label_url")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy6)
        self.label_url.setMinimumSize(QSize(100, 1))

        self.gridlayout_downloading.addWidget(self.label_url, 2, 0, 1, 1)

        self.lineedit_playlist_url = QLineEdit(self.page_download)
        self.lineedit_playlist_url.setObjectName(u"lineedit_playlist_url")

        self.gridlayout_downloading.addWidget(self.lineedit_playlist_url, 4, 1, 1, 2)

        self.labell_search = QLabel(self.page_download)
        self.labell_search.setObjectName(u"labell_search")

        self.gridlayout_downloading.addWidget(self.labell_search, 7, 0, 1, 1)

        self.label_playlist_url = QLabel(self.page_download)
        self.label_playlist_url.setObjectName(u"label_playlist_url")

        self.gridlayout_downloading.addWidget(self.label_playlist_url, 4, 0, 1, 1)

        self.label_model_url = QLabel(self.page_download)
        self.label_model_url.setObjectName(u"label_model_url")
        sizePolicy6.setHeightForWidth(self.label_model_url.sizePolicy().hasHeightForWidth())
        self.label_model_url.setSizePolicy(sizePolicy6)
        self.label_model_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_model_url, 5, 0, 1, 1)

        self.button_playlist_get_videos = QPushButton(self.page_download)
        self.button_playlist_get_videos.setObjectName(u"button_playlist_get_videos")

        self.gridlayout_downloading.addWidget(self.button_playlist_get_videos, 4, 3, 1, 1)

        self.lineedit_search_query = QLineEdit(self.page_download)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        sizePolicy4.setHeightForWidth(self.lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.lineedit_search_query.setSizePolicy(sizePolicy4)
        self.lineedit_search_query.setMinimumSize(QSize(300, 0))

        self.gridlayout_downloading.addWidget(self.lineedit_search_query, 7, 1, 1, 2)

        self.label_file = QLabel(self.page_download)
        self.label_file.setObjectName(u"label_file")
        sizePolicy6.setHeightForWidth(self.label_file.sizePolicy().hasHeightForWidth())
        self.label_file.setSizePolicy(sizePolicy6)
        self.label_file.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_file, 6, 0, 1, 1)

        self.button_help_file = QPushButton(self.page_download)
        self.button_help_file.setObjectName(u"button_help_file")

        self.gridlayout_downloading.addWidget(self.button_help_file, 6, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_downloading, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_download)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.gridLayout_2 = QGridLayout(self.page_login)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridlayout_login_box = QGridLayout()
        self.gridlayout_login_box.setSpacing(0)
        self.gridlayout_login_box.setObjectName(u"gridlayout_login_box")
        self.button_get_liked_videos = QPushButton(self.page_login)
        self.button_get_liked_videos.setObjectName(u"button_get_liked_videos")
        self.button_get_liked_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_get_liked_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_liked_videos, 3, 0, 1, 1)

        self.button_get_watched_videos = QPushButton(self.page_login)
        self.button_get_watched_videos.setObjectName(u"button_get_watched_videos")
        self.button_get_watched_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_get_watched_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_watched_videos, 3, 1, 1, 1)

        self.label_username = QLabel(self.page_login)
        self.label_username.setObjectName(u"label_username")
        sizePolicy5.setHeightForWidth(self.label_username.sizePolicy().hasHeightForWidth())
        self.label_username.setSizePolicy(sizePolicy5)

        self.gridlayout_login_box.addWidget(self.label_username, 0, 0, 1, 1)

        self.button_login = QPushButton(self.page_login)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setMinimumSize(QSize(0, 0))
        self.button_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_login.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_login, 2, 0, 1, 4)

        self.lineedit_username = QLineEdit(self.page_login)
        self.lineedit_username.setObjectName(u"lineedit_username")
        sizePolicy4.setHeightForWidth(self.lineedit_username.sizePolicy().hasHeightForWidth())
        self.lineedit_username.setSizePolicy(sizePolicy4)
        self.lineedit_username.setMinimumSize(QSize(150, 0))

        self.gridlayout_login_box.addWidget(self.lineedit_username, 0, 1, 1, 3)

        self.button_get_recommended_videos = QPushButton(self.page_login)
        self.button_get_recommended_videos.setObjectName(u"button_get_recommended_videos")
        self.button_get_recommended_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_get_recommended_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_recommended_videos, 3, 2, 1, 1)

        self.label_password = QLabel(self.page_login)
        self.label_password.setObjectName(u"label_password")
        sizePolicy5.setHeightForWidth(self.label_password.sizePolicy().hasHeightForWidth())
        self.label_password.setSizePolicy(sizePolicy5)

        self.gridlayout_login_box.addWidget(self.label_password, 1, 0, 1, 1)

        self.lineedit_password = QLineEdit(self.page_login)
        self.lineedit_password.setObjectName(u"lineedit_password")
        sizePolicy4.setHeightForWidth(self.lineedit_password.sizePolicy().hasHeightForWidth())
        self.lineedit_password.setSizePolicy(sizePolicy4)
        self.lineedit_password.setMinimumSize(QSize(150, 0))
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.gridlayout_login_box.addWidget(self.lineedit_password, 1, 1, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridlayout_login_box.addItem(self.verticalSpacer, 4, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridlayout_login_box, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_login)
        self.page_progressbars = QWidget()
        self.page_progressbars.setObjectName(u"page_progressbars")
        self.gridLayout_6 = QGridLayout(self.page_progressbars)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.page_progressbars)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 387, 206))
        self.gridLayout_18 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridlayout_progressbar = QGridLayout()
        self.gridlayout_progressbar.setObjectName(u"gridlayout_progressbar")
        self.progressbar_xvideos = QProgressBar(self.scrollAreaWidgetContents)
        self.progressbar_xvideos.setObjectName(u"progressbar_xvideos")
        self.progressbar_xvideos.setValue(0)

        self.gridlayout_progressbar.addWidget(self.progressbar_xvideos, 4, 1, 1, 1)

        self.label_progress_pornhub = QLabel(self.scrollAreaWidgetContents)
        self.label_progress_pornhub.setObjectName(u"label_progress_pornhub")
        sizePolicy5.setHeightForWidth(self.label_progress_pornhub.sizePolicy().hasHeightForWidth())
        self.label_progress_pornhub.setSizePolicy(sizePolicy5)

        self.gridlayout_progressbar.addWidget(self.label_progress_pornhub, 0, 0, 1, 1)

        self.label_progress_xvideos = QLabel(self.scrollAreaWidgetContents)
        self.label_progress_xvideos.setObjectName(u"label_progress_xvideos")

        self.gridlayout_progressbar.addWidget(self.label_progress_xvideos, 4, 0, 1, 1)

        self.label_progress_xnxx = QLabel(self.scrollAreaWidgetContents)
        self.label_progress_xnxx.setObjectName(u"label_progress_xnxx")

        self.gridlayout_progressbar.addWidget(self.label_progress_xnxx, 3, 0, 1, 1)

        self.progressbar_xnxx = QProgressBar(self.scrollAreaWidgetContents)
        self.progressbar_xnxx.setObjectName(u"progressbar_xnxx")
        self.progressbar_xnxx.setValue(0)

        self.gridlayout_progressbar.addWidget(self.progressbar_xnxx, 3, 1, 1, 1)

        self.label_progress_hqporner = QLabel(self.scrollAreaWidgetContents)
        self.label_progress_hqporner.setObjectName(u"label_progress_hqporner")
        sizePolicy5.setHeightForWidth(self.label_progress_hqporner.sizePolicy().hasHeightForWidth())
        self.label_progress_hqporner.setSizePolicy(sizePolicy5)

        self.gridlayout_progressbar.addWidget(self.label_progress_hqporner, 1, 0, 1, 1)

        self.progressbar_hqporner = QProgressBar(self.scrollAreaWidgetContents)
        self.progressbar_hqporner.setObjectName(u"progressbar_hqporner")
        sizePolicy4.setHeightForWidth(self.progressbar_hqporner.sizePolicy().hasHeightForWidth())
        self.progressbar_hqporner.setSizePolicy(sizePolicy4)
        self.progressbar_hqporner.setMinimumSize(QSize(300, 0))
        self.progressbar_hqporner.setValue(0)

        self.gridlayout_progressbar.addWidget(self.progressbar_hqporner, 1, 1, 1, 1)

        self.progressbar_pornhub = QProgressBar(self.scrollAreaWidgetContents)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        sizePolicy4.setHeightForWidth(self.progressbar_pornhub.sizePolicy().hasHeightForWidth())
        self.progressbar_pornhub.setSizePolicy(sizePolicy4)
        self.progressbar_pornhub.setMinimumSize(QSize(300, 0))
        self.progressbar_pornhub.setValue(0)

        self.gridlayout_progressbar.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.verticalspacer_progress_bars = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridlayout_progressbar.addItem(self.verticalspacer_progress_bars, 6, 1, 1, 1)

        self.progressbar_eporner = QProgressBar(self.scrollAreaWidgetContents)
        self.progressbar_eporner.setObjectName(u"progressbar_eporner")
        self.progressbar_eporner.setValue(0)

        self.gridlayout_progressbar.addWidget(self.progressbar_eporner, 2, 1, 1, 1)

        self.label_progress_eporner = QLabel(self.scrollAreaWidgetContents)
        self.label_progress_eporner.setObjectName(u"label_progress_eporner")

        self.gridlayout_progressbar.addWidget(self.label_progress_eporner, 2, 0, 1, 1)

        self.label_info = QLabel(self.scrollAreaWidgetContents)
        self.label_info.setObjectName(u"label_info")

        self.gridlayout_progressbar.addWidget(self.label_info, 5, 0, 1, 1)

        self.lineedit_download_info = QLineEdit(self.scrollAreaWidgetContents)
        self.lineedit_download_info.setObjectName(u"lineedit_download_info")
        self.lineedit_download_info.setReadOnly(True)

        self.gridlayout_progressbar.addWidget(self.lineedit_download_info, 5, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridlayout_progressbar, 1, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_6.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_progressbars)
        self.page_tools = QWidget()
        self.page_tools.setObjectName(u"page_tools")
        self.gridLayout_29 = QGridLayout(self.page_tools)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.groupBox_2 = QGroupBox(self.page_tools)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_15 = QGridLayout(self.groupBox_2)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_videos_by_category_eporner = QLabel(self.groupBox_2)
        self.label_videos_by_category_eporner.setObjectName(u"label_videos_by_category_eporner")
        self.label_videos_by_category_eporner.setMinimumSize(QSize(0, 4))

        self.horizontalLayout.addWidget(self.label_videos_by_category_eporner)

        self.lineedit_videos_by_category_eporner = QLineEdit(self.groupBox_2)
        self.lineedit_videos_by_category_eporner.setObjectName(u"lineedit_videos_by_category_eporner")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(4)
        sizePolicy7.setHeightForWidth(self.lineedit_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.lineedit_videos_by_category_eporner.setSizePolicy(sizePolicy7)
        self.lineedit_videos_by_category_eporner.setMinimumSize(QSize(100, 4))

        self.horizontalLayout.addWidget(self.lineedit_videos_by_category_eporner)

        self.button_eporner_category_get_videos = QPushButton(self.groupBox_2)
        self.button_eporner_category_get_videos.setObjectName(u"button_eporner_category_get_videos")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(2)
        sizePolicy8.setHeightForWidth(self.button_eporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.button_eporner_category_get_videos.setSizePolicy(sizePolicy8)
        self.button_eporner_category_get_videos.setMinimumSize(QSize(0, 2))
        self.button_eporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.button_eporner_category_get_videos)

        self.button_list_categories_eporner = QPushButton(self.groupBox_2)
        self.button_list_categories_eporner.setObjectName(u"button_list_categories_eporner")
        sizePolicy3.setHeightForWidth(self.button_list_categories_eporner.sizePolicy().hasHeightForWidth())
        self.button_list_categories_eporner.setSizePolicy(sizePolicy3)
        self.button_list_categories_eporner.setMinimumSize(QSize(0, 2))
        self.button_list_categories_eporner.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.button_list_categories_eporner)


        self.gridLayout_15.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox_2, 1, 1, 1, 1)

        self.groupbox_tools = QGroupBox(self.page_tools)
        self.groupbox_tools.setObjectName(u"groupbox_tools")
        self.gridLayout_7 = QGridLayout(self.groupbox_tools)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridlayout_tools_hqporner = QGridLayout()
        self.gridlayout_tools_hqporner.setObjectName(u"gridlayout_tools_hqporner")
        self.radio_top_porn_month = QRadioButton(self.groupbox_tools)
        self.radio_top_porn_month.setObjectName(u"radio_top_porn_month")
        self.radio_top_porn_month.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_month.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.radio_top_porn_month, 0, 2, 1, 1)

        self.button_top_porn_get_videos = QPushButton(self.groupbox_tools)
        self.button_top_porn_get_videos.setObjectName(u"button_top_porn_get_videos")
        self.button_top_porn_get_videos.setMinimumSize(QSize(0, 10))
        self.button_top_porn_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.button_top_porn_get_videos, 0, 4, 1, 1)

        self.label_get_brazzers_videos = QLabel(self.groupbox_tools)
        self.label_get_brazzers_videos.setObjectName(u"label_get_brazzers_videos")
        self.label_get_brazzers_videos.setMinimumSize(QSize(0, 4))

        self.gridlayout_tools_hqporner.addWidget(self.label_get_brazzers_videos, 3, 0, 1, 4)

        self.radio_top_porn_week = QRadioButton(self.groupbox_tools)
        self.radio_top_porn_week.setObjectName(u"radio_top_porn_week")
        self.radio_top_porn_week.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_week.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.radio_top_porn_week.setChecked(True)

        self.gridlayout_tools_hqporner.addWidget(self.radio_top_porn_week, 0, 1, 1, 1)

        self.button_list_categories = QPushButton(self.groupbox_tools)
        self.button_list_categories.setObjectName(u"button_list_categories")
        sizePolicy3.setHeightForWidth(self.button_list_categories.sizePolicy().hasHeightForWidth())
        self.button_list_categories.setSizePolicy(sizePolicy3)
        self.button_list_categories.setMinimumSize(QSize(0, 2))
        self.button_list_categories.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.button_list_categories, 1, 4, 1, 1)

        self.lineedit_hqporner_category = QLineEdit(self.groupbox_tools)
        self.lineedit_hqporner_category.setObjectName(u"lineedit_hqporner_category")
        sizePolicy7.setHeightForWidth(self.lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.lineedit_hqporner_category.setSizePolicy(sizePolicy7)
        self.lineedit_hqporner_category.setMinimumSize(QSize(100, 4))

        self.gridlayout_tools_hqporner.addWidget(self.lineedit_hqporner_category, 1, 1, 1, 2)

        self.label_get_top_porn = QLabel(self.groupbox_tools)
        self.label_get_top_porn.setObjectName(u"label_get_top_porn")

        self.gridlayout_tools_hqporner.addWidget(self.label_get_top_porn, 0, 0, 1, 1)

        self.radio_top_porn_all_time = QRadioButton(self.groupbox_tools)
        self.radio_top_porn_all_time.setObjectName(u"radio_top_porn_all_time")
        self.radio_top_porn_all_time.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_all_time.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.radio_top_porn_all_time, 0, 3, 1, 1)

        self.button_hqporner_category_get_videos = QPushButton(self.groupbox_tools)
        self.button_hqporner_category_get_videos.setObjectName(u"button_hqporner_category_get_videos")
        sizePolicy8.setHeightForWidth(self.button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.button_hqporner_category_get_videos.setSizePolicy(sizePolicy8)
        self.button_hqporner_category_get_videos.setMinimumSize(QSize(0, 2))
        self.button_hqporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.button_hqporner_category_get_videos, 1, 3, 1, 1)

        self.button_get_random_videos = QPushButton(self.groupbox_tools)
        self.button_get_random_videos.setObjectName(u"button_get_random_videos")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.button_get_random_videos.setSizePolicy(sizePolicy9)
        self.button_get_random_videos.setMinimumSize(QSize(0, 10))
        self.button_get_random_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.button_get_random_videos, 2, 4, 1, 1)

        self.button_get_brazzers_videos = QPushButton(self.groupbox_tools)
        self.button_get_brazzers_videos.setObjectName(u"button_get_brazzers_videos")
        sizePolicy9.setHeightForWidth(self.button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.button_get_brazzers_videos.setSizePolicy(sizePolicy9)
        self.button_get_brazzers_videos.setMinimumSize(QSize(0, 10))
        self.button_get_brazzers_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tools_hqporner.addWidget(self.button_get_brazzers_videos, 3, 4, 1, 1)

        self.labe_get_random_video = QLabel(self.groupbox_tools)
        self.labe_get_random_video.setObjectName(u"labe_get_random_video")
        self.labe_get_random_video.setMinimumSize(QSize(0, 4))

        self.gridlayout_tools_hqporner.addWidget(self.labe_get_random_video, 2, 0, 1, 4)

        self.label_videos_by_category = QLabel(self.groupbox_tools)
        self.label_videos_by_category.setObjectName(u"label_videos_by_category")
        self.label_videos_by_category.setMinimumSize(QSize(0, 4))

        self.gridlayout_tools_hqporner.addWidget(self.label_videos_by_category, 1, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridlayout_tools_hqporner, 0, 0, 1, 1)


        self.gridLayout_29.addWidget(self.groupbox_tools, 0, 1, 1, 1)

        self.stacked_widget_top.addWidget(self.page_tools)

        self.verticallayout_treewidget.addWidget(self.stacked_widget_top)

        self.scrollarea_treewidget = QScrollArea(self.widget)
        self.scrollarea_treewidget.setObjectName(u"scrollarea_treewidget")
        self.scrollarea_treewidget.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 478, 289))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticallayout_treewidget_settings = QVBoxLayout()
        self.verticallayout_treewidget_settings.setObjectName(u"verticallayout_treewidget_settings")
        self.treeWidget = QTreeWidget(self.scrollAreaWidgetContents_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy10)
        self.treeWidget.setMinimumSize(QSize(100, 200))

        self.verticallayout_treewidget_settings.addWidget(self.treeWidget)


        self.gridLayout_4.addLayout(self.verticallayout_treewidget_settings, 2, 0, 1, 1)

        self.gridlayout_tree_settings = QGridLayout()
        self.gridlayout_tree_settings.setObjectName(u"gridlayout_tree_settings")
        self.radio_tree_show_all = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radio_tree_show_all.setObjectName(u"radio_tree_show_all")
        sizePolicy5.setHeightForWidth(self.radio_tree_show_all.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_all.setSizePolicy(sizePolicy5)
        self.radio_tree_show_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.radio_tree_show_all.setStyleSheet(u"")
        self.radio_tree_show_all.setCheckable(True)
        self.radio_tree_show_all.setChecked(False)

        self.gridlayout_tree_settings.addWidget(self.radio_tree_show_all, 0, 1, 1, 1)

        self.horizontalspacer_tree_1 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridlayout_tree_settings.addItem(self.horizontalspacer_tree_1, 0, 3, 1, 1)

        self.horizontalspacer_tree_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridlayout_tree_settings.addItem(self.horizontalspacer_tree_2, 1, 3, 1, 1)

        self.radio_tree_show_title = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radio_tree_show_title.setObjectName(u"radio_tree_show_title")
        sizePolicy5.setHeightForWidth(self.radio_tree_show_title.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_title.setSizePolicy(sizePolicy5)
        self.radio_tree_show_title.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.radio_tree_show_title.setChecked(True)

        self.gridlayout_tree_settings.addWidget(self.radio_tree_show_title, 0, 0, 1, 1)

        self.checkbox_tree_do_not_clear_videos = QCheckBox(self.scrollAreaWidgetContents_3)
        self.checkbox_tree_do_not_clear_videos.setObjectName(u"checkbox_tree_do_not_clear_videos")

        self.gridlayout_tree_settings.addWidget(self.checkbox_tree_do_not_clear_videos, 1, 0, 1, 1)

        self.checkbox_tree_show_videos_reversed = QCheckBox(self.scrollAreaWidgetContents_3)
        self.checkbox_tree_show_videos_reversed.setObjectName(u"checkbox_tree_show_videos_reversed")
        self.checkbox_tree_show_videos_reversed.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_tree_settings.addWidget(self.checkbox_tree_show_videos_reversed, 1, 1, 1, 1)

        self.button_tree_export_video_urls = QPushButton(self.scrollAreaWidgetContents_3)
        self.button_tree_export_video_urls.setObjectName(u"button_tree_export_video_urls")

        self.gridlayout_tree_settings.addWidget(self.button_tree_export_video_urls, 1, 2, 1, 1)

        self.button_tree_stop = QPushButton(self.scrollAreaWidgetContents_3)
        self.button_tree_stop.setObjectName(u"button_tree_stop")
        sizePolicy1.setHeightForWidth(self.button_tree_stop.sizePolicy().hasHeightForWidth())
        self.button_tree_stop.setSizePolicy(sizePolicy1)
        self.button_tree_stop.setMinimumSize(QSize(0, 30))

        self.gridlayout_tree_settings.addWidget(self.button_tree_stop, 0, 2, 1, 1)


        self.gridLayout_4.addLayout(self.gridlayout_tree_settings, 1, 0, 1, 1)

        self.scrollarea_treewidget.setWidget(self.scrollAreaWidgetContents_3)

        self.verticallayout_treewidget.addWidget(self.scrollarea_treewidget)

        self.gridlayout_tree_buttons = QGridLayout()
        self.gridlayout_tree_buttons.setObjectName(u"gridlayout_tree_buttons")
        self.button_tree_select_range = QPushButton(self.widget)
        self.button_tree_select_range.setObjectName(u"button_tree_select_range")
        sizePolicy1.setHeightForWidth(self.button_tree_select_range.sizePolicy().hasHeightForWidth())
        self.button_tree_select_range.setSizePolicy(sizePolicy1)
        self.button_tree_select_range.setMinimumSize(QSize(0, 30))
        self.button_tree_select_range.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_tree_select_range.setStyleSheet(u"")

        self.gridlayout_tree_buttons.addWidget(self.button_tree_select_range, 2, 1, 1, 1)

        self.button_range_apply_everything = QPushButton(self.widget)
        self.button_range_apply_everything.setObjectName(u"button_range_apply_everything")

        self.gridlayout_tree_buttons.addWidget(self.button_range_apply_everything, 2, 0, 1, 1)

        self.button_tree_download = QPushButton(self.widget)
        self.button_tree_download.setObjectName(u"button_tree_download")
        sizePolicy1.setHeightForWidth(self.button_tree_download.sizePolicy().hasHeightForWidth())
        self.button_tree_download.setSizePolicy(sizePolicy1)
        self.button_tree_download.setMinimumSize(QSize(0, 30))
        self.button_tree_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_tree_download.setStyleSheet(u"")

        self.gridlayout_tree_buttons.addWidget(self.button_tree_download, 1, 0, 1, 3)

        self.button_tree_unselect_all = QPushButton(self.widget)
        self.button_tree_unselect_all.setObjectName(u"button_tree_unselect_all")
        sizePolicy1.setHeightForWidth(self.button_tree_unselect_all.sizePolicy().hasHeightForWidth())
        self.button_tree_unselect_all.setSizePolicy(sizePolicy1)
        self.button_tree_unselect_all.setMinimumSize(QSize(0, 30))
        self.button_tree_unselect_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_tree_unselect_all.setStyleSheet(u"")

        self.gridlayout_tree_buttons.addWidget(self.button_tree_unselect_all, 2, 2, 1, 1)


        self.verticallayout_treewidget.addLayout(self.gridlayout_tree_buttons)


        self.gridLayout_8.addLayout(self.verticallayout_treewidget, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.widget)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.gridLayout_25 = QGridLayout(self.page_settings)
        self.gridLayout_25.setSpacing(0)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_settings = QScrollArea(self.page_settings)
        self.scrollarea_settings.setObjectName(u"scrollarea_settings")
        self.scrollarea_settings.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 1188, 693))
        self.gridLayout_19 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.button_download_ffmpeg = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_download_ffmpeg.setObjectName(u"button_download_ffmpeg")

        self.gridLayout_19.addWidget(self.button_download_ffmpeg, 0, 0, 1, 1)

        self.gridlayout_settings = QGridLayout()
        self.gridlayout_settings.setObjectName(u"gridlayout_settings")
        self.groupbox_performance = QGroupBox(self.scrollAreaWidgetContents_6)
        self.groupbox_performance.setObjectName(u"groupbox_performance")
        self.gridLayout_9 = QGridLayout(self.groupbox_performance)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontallayout_simultaneous_downloads = QHBoxLayout()
        self.horizontallayout_simultaneous_downloads.setObjectName(u"horizontallayout_simultaneous_downloads")
        self.label_semaphore = QLabel(self.groupbox_performance)
        self.label_semaphore.setObjectName(u"label_semaphore")

        self.horizontallayout_simultaneous_downloads.addWidget(self.label_semaphore)

        self.spinbox_semaphore = QSpinBox(self.groupbox_performance)
        self.spinbox_semaphore.setObjectName(u"spinbox_semaphore")
        self.spinbox_semaphore.setMinimum(1)
        self.spinbox_semaphore.setMaximum(5000)

        self.horizontallayout_simultaneous_downloads.addWidget(self.spinbox_semaphore)

        self.button_semaphore_help = QPushButton(self.groupbox_performance)
        self.button_semaphore_help.setObjectName(u"button_semaphore_help")
        self.button_semaphore_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_simultaneous_downloads.addWidget(self.button_semaphore_help)


        self.gridLayout_9.addLayout(self.horizontallayout_simultaneous_downloads, 2, 0, 1, 1)

        self.horizontallayout_maximal_workers = QHBoxLayout()
        self.horizontallayout_maximal_workers.setObjectName(u"horizontallayout_maximal_workers")
        self.label_maximal_workers = QLabel(self.groupbox_performance)
        self.label_maximal_workers.setObjectName(u"label_maximal_workers")

        self.horizontallayout_maximal_workers.addWidget(self.label_maximal_workers)

        self.spinbox_maximal_workers = QSpinBox(self.groupbox_performance)
        self.spinbox_maximal_workers.setObjectName(u"spinbox_maximal_workers")
        self.spinbox_maximal_workers.setMinimum(1)
        self.spinbox_maximal_workers.setMaximum(5000)

        self.horizontallayout_maximal_workers.addWidget(self.spinbox_maximal_workers)

        self.button_workers_help = QPushButton(self.groupbox_performance)
        self.button_workers_help.setObjectName(u"button_workers_help")
        self.button_workers_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_maximal_workers.addWidget(self.button_workers_help)


        self.gridLayout_9.addLayout(self.horizontallayout_maximal_workers, 4, 0, 1, 1)

        self.horizontallayout_pornhub_delay = QHBoxLayout()
        self.horizontallayout_pornhub_delay.setObjectName(u"horizontallayout_pornhub_delay")
        self.label_pornhub_delay = QLabel(self.groupbox_performance)
        self.label_pornhub_delay.setObjectName(u"label_pornhub_delay")

        self.horizontallayout_pornhub_delay.addWidget(self.label_pornhub_delay)

        self.spinbox_pornhub_delay = QSpinBox(self.groupbox_performance)
        self.spinbox_pornhub_delay.setObjectName(u"spinbox_pornhub_delay")
        self.spinbox_pornhub_delay.setMinimum(0)
        self.spinbox_pornhub_delay.setMaximum(5000)

        self.horizontallayout_pornhub_delay.addWidget(self.spinbox_pornhub_delay)

        self.button_pornhub_delay_help = QPushButton(self.groupbox_performance)
        self.button_pornhub_delay_help.setObjectName(u"button_pornhub_delay_help")
        self.button_pornhub_delay_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_pornhub_delay.addWidget(self.button_pornhub_delay_help)


        self.gridLayout_9.addLayout(self.horizontallayout_pornhub_delay, 3, 0, 1, 1)

        self.horizontallayout_threading_mode = QHBoxLayout()
        self.horizontallayout_threading_mode.setObjectName(u"horizontallayout_threading_mode")
        self.label_threading_mode = QLabel(self.groupbox_performance)
        self.label_threading_mode.setObjectName(u"label_threading_mode")
        sizePolicy5.setHeightForWidth(self.label_threading_mode.sizePolicy().hasHeightForWidth())
        self.label_threading_mode.setSizePolicy(sizePolicy5)

        self.horizontallayout_threading_mode.addWidget(self.label_threading_mode)

        self.radio_threading_mode_high_performance = QRadioButton(self.groupbox_performance)
        self.radio_threading_mode_high_performance.setObjectName(u"radio_threading_mode_high_performance")
        self.radio_threading_mode_high_performance.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.radio_threading_mode_high_performance)

        self.radio_threading_mode_ffmpeg = QRadioButton(self.groupbox_performance)
        self.radio_threading_mode_ffmpeg.setObjectName(u"radio_threading_mode_ffmpeg")
        self.radio_threading_mode_ffmpeg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.radio_threading_mode_ffmpeg)

        self.radio_threading_mode_default = QRadioButton(self.groupbox_performance)
        self.radio_threading_mode_default.setObjectName(u"radio_threading_mode_default")
        self.radio_threading_mode_default.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.radio_threading_mode_default)

        self.button_threading_mode_help = QPushButton(self.groupbox_performance)
        self.button_threading_mode_help.setObjectName(u"button_threading_mode_help")
        self.button_threading_mode_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.button_threading_mode_help)


        self.gridLayout_9.addLayout(self.horizontallayout_threading_mode, 1, 0, 1, 1)

        self.horizontallayout_maximal_timeout = QHBoxLayout()
        self.horizontallayout_maximal_timeout.setObjectName(u"horizontallayout_maximal_timeout")
        self.label_maximal_timeout = QLabel(self.groupbox_performance)
        self.label_maximal_timeout.setObjectName(u"label_maximal_timeout")

        self.horizontallayout_maximal_timeout.addWidget(self.label_maximal_timeout)

        self.spinbox_maximal_timeout = QSpinBox(self.groupbox_performance)
        self.spinbox_maximal_timeout.setObjectName(u"spinbox_maximal_timeout")
        self.spinbox_maximal_timeout.setMinimum(5)
        self.spinbox_maximal_timeout.setMaximum(5000)

        self.horizontallayout_maximal_timeout.addWidget(self.spinbox_maximal_timeout)

        self.button_timeout_help = QPushButton(self.groupbox_performance)
        self.button_timeout_help.setObjectName(u"button_timeout_help")
        self.button_timeout_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_maximal_timeout.addWidget(self.button_timeout_help)


        self.gridLayout_9.addLayout(self.horizontallayout_maximal_timeout, 5, 0, 1, 1)

        self.horizontallayout_maximal_retries = QHBoxLayout()
        self.horizontallayout_maximal_retries.setObjectName(u"horizontallayout_maximal_retries")
        self.label_maximal_retries = QLabel(self.groupbox_performance)
        self.label_maximal_retries.setObjectName(u"label_maximal_retries")

        self.horizontallayout_maximal_retries.addWidget(self.label_maximal_retries)

        self.spinbox_maximal_retries = QSpinBox(self.groupbox_performance)
        self.spinbox_maximal_retries.setObjectName(u"spinbox_maximal_retries")
        self.spinbox_maximal_retries.setMinimum(5)
        self.spinbox_maximal_retries.setMaximum(5000)

        self.horizontallayout_maximal_retries.addWidget(self.spinbox_maximal_retries)

        self.button_timeout_maximal_retries_help = QPushButton(self.groupbox_performance)
        self.button_timeout_maximal_retries_help.setObjectName(u"button_timeout_maximal_retries_help")
        self.button_timeout_maximal_retries_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_maximal_retries.addWidget(self.button_timeout_maximal_retries_help)


        self.gridLayout_9.addLayout(self.horizontallayout_maximal_retries, 6, 0, 1, 1)


        self.gridlayout_settings.addWidget(self.groupbox_performance, 0, 0, 1, 1)


        self.gridLayout_19.addLayout(self.gridlayout_settings, 1, 0, 1, 1)

        self.groupbox_videos = QGroupBox(self.scrollAreaWidgetContents_6)
        self.groupbox_videos.setObjectName(u"groupbox_videos")
        self.gridLayout_10 = QGridLayout(self.groupbox_videos)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.horizontallayout_output_path = QHBoxLayout()
        self.horizontallayout_output_path.setObjectName(u"horizontallayout_output_path")
        self.label_output_path = QLabel(self.groupbox_videos)
        self.label_output_path.setObjectName(u"label_output_path")

        self.horizontallayout_output_path.addWidget(self.label_output_path)

        self.lineedit_output_path = QLineEdit(self.groupbox_videos)
        self.lineedit_output_path.setObjectName(u"lineedit_output_path")

        self.horizontallayout_output_path.addWidget(self.lineedit_output_path)

        self.button_output_path_select = QPushButton(self.groupbox_videos)
        self.button_output_path_select.setObjectName(u"button_output_path_select")
        self.button_output_path_select.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_output_path.addWidget(self.button_output_path_select)


        self.gridLayout_10.addLayout(self.horizontallayout_output_path, 1, 0, 1, 1)

        self.horizontallayout_result_limit = QHBoxLayout()
        self.horizontallayout_result_limit.setObjectName(u"horizontallayout_result_limit")
        self.label_searching_limit = QLabel(self.groupbox_videos)
        self.label_searching_limit.setObjectName(u"label_searching_limit")

        self.horizontallayout_result_limit.addWidget(self.label_searching_limit)

        self.spinbox_treewidget_limit = QSpinBox(self.groupbox_videos)
        self.spinbox_treewidget_limit.setObjectName(u"spinbox_treewidget_limit")
        self.spinbox_treewidget_limit.setMinimum(1)
        self.spinbox_treewidget_limit.setMaximum(5000)

        self.horizontallayout_result_limit.addWidget(self.spinbox_treewidget_limit)

        self.button_result_limit_help = QPushButton(self.groupbox_videos)
        self.button_result_limit_help.setObjectName(u"button_result_limit_help")
        self.button_result_limit_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_result_limit.addWidget(self.button_result_limit_help)


        self.gridLayout_10.addLayout(self.horizontallayout_result_limit, 3, 0, 1, 1)

        self.horizontallayout_quality = QHBoxLayout()
        self.horizontallayout_quality.setObjectName(u"horizontallayout_quality")
        self.label_quality = QLabel(self.groupbox_videos)
        self.label_quality.setObjectName(u"label_quality")
        sizePolicy5.setHeightForWidth(self.label_quality.sizePolicy().hasHeightForWidth())
        self.label_quality.setSizePolicy(sizePolicy5)

        self.horizontallayout_quality.addWidget(self.label_quality)

        self.radio_quality_best = QRadioButton(self.groupbox_videos)
        self.radio_quality_best.setObjectName(u"radio_quality_best")
        self.radio_quality_best.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_quality.addWidget(self.radio_quality_best)

        self.radio_quality_half = QRadioButton(self.groupbox_videos)
        self.radio_quality_half.setObjectName(u"radio_quality_half")
        self.radio_quality_half.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_quality.addWidget(self.radio_quality_half)

        self.radio_quality_worst = QRadioButton(self.groupbox_videos)
        self.radio_quality_worst.setObjectName(u"radio_quality_worst")
        self.radio_quality_worst.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_quality.addWidget(self.radio_quality_worst)


        self.gridLayout_10.addLayout(self.horizontallayout_quality, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_skip_existing_files = QLabel(self.groupbox_videos)
        self.label_skip_existing_files.setObjectName(u"label_skip_existing_files")

        self.horizontalLayout_2.addWidget(self.label_skip_existing_files)

        self.radio_skip_existing_files_yes = QRadioButton(self.groupbox_videos)
        self.radio_skip_existing_files_yes.setObjectName(u"radio_skip_existing_files_yes")

        self.horizontalLayout_2.addWidget(self.radio_skip_existing_files_yes)

        self.radio_skip_existing_files_no = QRadioButton(self.groupbox_videos)
        self.radio_skip_existing_files_no.setObjectName(u"radio_skip_existing_files_no")

        self.horizontalLayout_2.addWidget(self.radio_skip_existing_files_no)

        self.button_help_skip_existing_files = QPushButton(self.groupbox_videos)
        self.button_help_skip_existing_files.setObjectName(u"button_help_skip_existing_files")

        self.horizontalLayout_2.addWidget(self.button_help_skip_existing_files)


        self.gridLayout_10.addLayout(self.horizontalLayout_2, 4, 0, 1, 1)

        self.horizontallayout_directory_system = QHBoxLayout()
        self.horizontallayout_directory_system.setObjectName(u"horizontallayout_directory_system")
        self.label_directory_system = QLabel(self.groupbox_videos)
        self.label_directory_system.setObjectName(u"label_directory_system")

        self.horizontallayout_directory_system.addWidget(self.label_directory_system)

        self.radio_directory_system_yes = QRadioButton(self.groupbox_videos)
        self.radio_directory_system_yes.setObjectName(u"radio_directory_system_yes")
        self.radio_directory_system_yes.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_directory_system.addWidget(self.radio_directory_system_yes)

        self.radio_directory_system_no = QRadioButton(self.groupbox_videos)
        self.radio_directory_system_no.setObjectName(u"radio_directory_system_no")
        self.radio_directory_system_no.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_directory_system.addWidget(self.radio_directory_system_no)

        self.button_directory_system_help = QPushButton(self.groupbox_videos)
        self.button_directory_system_help.setObjectName(u"button_directory_system_help")
        self.button_directory_system_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_directory_system.addWidget(self.button_directory_system_help)


        self.gridLayout_10.addLayout(self.horizontallayout_directory_system, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.labe_settings_videos_model = QLabel(self.groupbox_videos)
        self.labe_settings_videos_model.setObjectName(u"labe_settings_videos_model")

        self.horizontalLayout_3.addWidget(self.labe_settings_videos_model)

        self.radio_model_uploads = QRadioButton(self.groupbox_videos)
        self.radio_model_uploads.setObjectName(u"radio_model_uploads")

        self.horizontalLayout_3.addWidget(self.radio_model_uploads)

        self.radio_model_featured = QRadioButton(self.groupbox_videos)
        self.radio_model_featured.setObjectName(u"radio_model_featured")

        self.horizontalLayout_3.addWidget(self.radio_model_featured)

        self.radio_model_both = QRadioButton(self.groupbox_videos)
        self.radio_model_both.setObjectName(u"radio_model_both")

        self.horizontalLayout_3.addWidget(self.radio_model_both)

        self.button_help_model_videos = QPushButton(self.groupbox_videos)
        self.button_help_model_videos.setObjectName(u"button_help_model_videos")

        self.horizontalLayout_3.addWidget(self.button_help_model_videos)


        self.gridLayout_10.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)


        self.gridLayout_19.addWidget(self.groupbox_videos, 2, 0, 1, 1)

        self.goroupbox_gui = QGroupBox(self.scrollAreaWidgetContents_6)
        self.goroupbox_gui.setObjectName(u"goroupbox_gui")
        self.gridLayout_12 = QGridLayout(self.goroupbox_gui)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridlayout_gui_settings = QGridLayout()
        self.gridlayout_gui_settings.setObjectName(u"gridlayout_gui_settings")
        self.radio_ui_language_german = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_german.setObjectName(u"radio_ui_language_german")
        self.radio_ui_language_german.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_german, 1, 3, 1, 1)

        self.radio_ui_language_chinese_simplified = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_chinese_simplified.setObjectName(u"radio_ui_language_chinese_simplified")
        self.radio_ui_language_chinese_simplified.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_chinese_simplified, 1, 4, 1, 1)

        self.radio_ui_language_english = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_english.setObjectName(u"radio_ui_language_english")
        self.radio_ui_language_english.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_english, 1, 2, 1, 1)

        self.radio_ui_language_system_default = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_system_default.setObjectName(u"radio_ui_language_system_default")
        self.radio_ui_language_system_default.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_system_default, 1, 1, 1, 1)

        self.label_ui_language = QLabel(self.goroupbox_gui)
        self.label_ui_language.setObjectName(u"label_ui_language")
        sizePolicy5.setHeightForWidth(self.label_ui_language.sizePolicy().hasHeightForWidth())
        self.label_ui_language.setSizePolicy(sizePolicy5)

        self.gridlayout_gui_settings.addWidget(self.label_ui_language, 1, 0, 1, 1)

        self.radio_ui_language_french = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_french.setObjectName(u"radio_ui_language_french")
        self.radio_ui_language_french.setEnabled(True)

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_french, 1, 5, 1, 1)


        self.gridLayout_12.addLayout(self.gridlayout_gui_settings, 0, 0, 1, 1)


        self.gridLayout_19.addWidget(self.goroupbox_gui, 3, 0, 1, 2)

        self.horizontallayout_settings_apply = QHBoxLayout()
        self.horizontallayout_settings_apply.setObjectName(u"horizontallayout_settings_apply")
        self.button_settings_apply = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_settings_apply.setObjectName(u"button_settings_apply")
        self.button_settings_apply.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontallayout_settings_apply.addWidget(self.button_settings_apply)

        self.button_settings_reset = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_settings_reset.setObjectName(u"button_settings_reset")
        self.button_settings_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_settings_reset.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(85, 0, 0)/* Green */\n"
"    font: bold 14px;\n"
"    min-width: 5em;\n"
"    padding: 3px;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color:  rgb(222, 0, 41)/* Lighter green */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(108, 0, 52) /* Dark green */\n"
"}\n"
"")

        self.horizontallayout_settings_apply.addWidget(self.button_settings_reset)


        self.gridLayout_19.addLayout(self.horizontallayout_settings_apply, 4, 0, 1, 1)

        self.scrollarea_settings.setWidget(self.scrollAreaWidgetContents_6)

        self.gridLayout_25.addWidget(self.scrollarea_settings, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_settings)
        self.page_credits = QWidget()
        self.page_credits.setObjectName(u"page_credits")
        self.gridLayout_26 = QGridLayout(self.page_credits)
        self.gridLayout_26.setSpacing(0)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.gridlayout_textbrowser = QGridLayout()
        self.gridlayout_textbrowser.setObjectName(u"gridlayout_textbrowser")
        self.textBrowser = QTextBrowser(self.page_credits)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridlayout_textbrowser.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout_26.addLayout(self.gridlayout_textbrowser, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_credits)
        self.page_supported_websites = QWidget()
        self.page_supported_websites.setObjectName(u"page_supported_websites")
        self.gridLayout_11 = QGridLayout(self.page_supported_websites)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.textbrowser_websites = QTextBrowser(self.page_supported_websites)
        self.textbrowser_websites.setObjectName(u"textbrowser_websites")

        self.gridLayout_11.addWidget(self.textbrowser_websites, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_supported_websites)

        self.gridlayout_main.addWidget(self.stacked_widget_main, 2, 0, 1, 1)

        self.gridlayout_status = QGridLayout()
        self.gridlayout_status.setSpacing(0)
        self.gridlayout_status.setObjectName(u"gridlayout_status")
        self.label_total_progress = QLabel(Porn_Fetch_Widget)
        self.label_total_progress.setObjectName(u"label_total_progress")
        sizePolicy5.setHeightForWidth(self.label_total_progress.sizePolicy().hasHeightForWidth())
        self.label_total_progress.setSizePolicy(sizePolicy5)

        self.gridlayout_status.addWidget(self.label_total_progress, 2, 0, 1, 1)

        self.progressbar_converting = QProgressBar(Porn_Fetch_Widget)
        self.progressbar_converting.setObjectName(u"progressbar_converting")
        self.progressbar_converting.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_converting, 3, 1, 1, 1)

        self.label_progress_converting = QLabel(Porn_Fetch_Widget)
        self.label_progress_converting.setObjectName(u"label_progress_converting")

        self.gridlayout_status.addWidget(self.label_progress_converting, 3, 0, 1, 1)

        self.label_progress_information = QLabel(Porn_Fetch_Widget)
        self.label_progress_information.setObjectName(u"label_progress_information")
        sizePolicy5.setHeightForWidth(self.label_progress_information.sizePolicy().hasHeightForWidth())
        self.label_progress_information.setSizePolicy(sizePolicy5)

        self.gridlayout_status.addWidget(self.label_progress_information, 4, 1, 1, 1)

        self.progressbar_total = QProgressBar(Porn_Fetch_Widget)
        self.progressbar_total.setObjectName(u"progressbar_total")
        sizePolicy4.setHeightForWidth(self.progressbar_total.sizePolicy().hasHeightForWidth())
        self.progressbar_total.setSizePolicy(sizePolicy4)
        self.progressbar_total.setMinimumSize(QSize(300, 0))
        self.progressbar_total.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_total, 2, 1, 1, 1)


        self.gridlayout_main.addLayout(self.gridlayout_status, 3, 0, 1, 1)


        self.gridLayout.addLayout(self.gridlayout_main, 0, 0, 1, 1)

        QWidget.setTabOrder(self.lineedit_url, self.button_download)
        QWidget.setTabOrder(self.button_download, self.lineedit_playlist_url)
        QWidget.setTabOrder(self.lineedit_playlist_url, self.button_playlist_get_videos)
        QWidget.setTabOrder(self.button_playlist_get_videos, self.lineedit_model_url)
        QWidget.setTabOrder(self.lineedit_model_url, self.button_model)
        QWidget.setTabOrder(self.button_model, self.lineedit_file)
        QWidget.setTabOrder(self.lineedit_file, self.button_help_file)
        QWidget.setTabOrder(self.button_help_file, self.button_open_file)
        QWidget.setTabOrder(self.button_open_file, self.lineedit_search_query)
        QWidget.setTabOrder(self.lineedit_search_query, self.button_search)
        QWidget.setTabOrder(self.button_search, self.radio_search_website_pornhub)
        QWidget.setTabOrder(self.radio_search_website_pornhub, self.radio_search_website_hqporner)
        QWidget.setTabOrder(self.radio_search_website_hqporner, self.radio_search_website_xvideos)
        QWidget.setTabOrder(self.radio_search_website_xvideos, self.radio_search_website_eporner)
        QWidget.setTabOrder(self.radio_search_website_eporner, self.radio_search_website_xnxx)
        QWidget.setTabOrder(self.radio_search_website_xnxx, self.treeWidget)
        QWidget.setTabOrder(self.treeWidget, self.scrollarea_treewidget)
        QWidget.setTabOrder(self.scrollarea_treewidget, self.lineedit_username)
        QWidget.setTabOrder(self.lineedit_username, self.lineedit_password)
        QWidget.setTabOrder(self.lineedit_password, self.button_login)
        QWidget.setTabOrder(self.button_login, self.button_get_liked_videos)
        QWidget.setTabOrder(self.button_get_liked_videos, self.button_get_watched_videos)
        QWidget.setTabOrder(self.button_get_watched_videos, self.button_get_recommended_videos)
        QWidget.setTabOrder(self.button_get_recommended_videos, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.radio_top_porn_week)
        QWidget.setTabOrder(self.radio_top_porn_week, self.radio_top_porn_month)
        QWidget.setTabOrder(self.radio_top_porn_month, self.radio_top_porn_all_time)
        QWidget.setTabOrder(self.radio_top_porn_all_time, self.button_top_porn_get_videos)
        QWidget.setTabOrder(self.button_top_porn_get_videos, self.lineedit_hqporner_category)
        QWidget.setTabOrder(self.lineedit_hqporner_category, self.button_hqporner_category_get_videos)
        QWidget.setTabOrder(self.button_hqporner_category_get_videos, self.button_list_categories)
        QWidget.setTabOrder(self.button_list_categories, self.button_get_random_videos)
        QWidget.setTabOrder(self.button_get_random_videos, self.button_get_brazzers_videos)
        QWidget.setTabOrder(self.button_get_brazzers_videos, self.lineedit_videos_by_category_eporner)
        QWidget.setTabOrder(self.lineedit_videos_by_category_eporner, self.button_eporner_category_get_videos)
        QWidget.setTabOrder(self.button_eporner_category_get_videos, self.button_list_categories_eporner)
        QWidget.setTabOrder(self.button_list_categories_eporner, self.scrollarea_settings)
        QWidget.setTabOrder(self.scrollarea_settings, self.button_download_ffmpeg)
        QWidget.setTabOrder(self.button_download_ffmpeg, self.radio_threading_mode_high_performance)
        QWidget.setTabOrder(self.radio_threading_mode_high_performance, self.radio_threading_mode_ffmpeg)
        QWidget.setTabOrder(self.radio_threading_mode_ffmpeg, self.radio_threading_mode_default)
        QWidget.setTabOrder(self.radio_threading_mode_default, self.button_threading_mode_help)
        QWidget.setTabOrder(self.button_threading_mode_help, self.spinbox_semaphore)
        QWidget.setTabOrder(self.spinbox_semaphore, self.button_semaphore_help)
        QWidget.setTabOrder(self.button_semaphore_help, self.spinbox_pornhub_delay)
        QWidget.setTabOrder(self.spinbox_pornhub_delay, self.button_pornhub_delay_help)
        QWidget.setTabOrder(self.button_pornhub_delay_help, self.spinbox_maximal_workers)
        QWidget.setTabOrder(self.spinbox_maximal_workers, self.button_workers_help)
        QWidget.setTabOrder(self.button_workers_help, self.spinbox_maximal_timeout)
        QWidget.setTabOrder(self.spinbox_maximal_timeout, self.button_timeout_help)
        QWidget.setTabOrder(self.button_timeout_help, self.spinbox_maximal_retries)
        QWidget.setTabOrder(self.spinbox_maximal_retries, self.button_timeout_maximal_retries_help)
        QWidget.setTabOrder(self.button_timeout_maximal_retries_help, self.radio_quality_best)
        QWidget.setTabOrder(self.radio_quality_best, self.radio_quality_half)
        QWidget.setTabOrder(self.radio_quality_half, self.radio_quality_worst)
        QWidget.setTabOrder(self.radio_quality_worst, self.lineedit_output_path)
        QWidget.setTabOrder(self.lineedit_output_path, self.button_output_path_select)
        QWidget.setTabOrder(self.button_output_path_select, self.radio_directory_system_yes)
        QWidget.setTabOrder(self.radio_directory_system_yes, self.radio_directory_system_no)
        QWidget.setTabOrder(self.radio_directory_system_no, self.button_directory_system_help)
        QWidget.setTabOrder(self.button_directory_system_help, self.spinbox_treewidget_limit)
        QWidget.setTabOrder(self.spinbox_treewidget_limit, self.button_result_limit_help)
        QWidget.setTabOrder(self.button_result_limit_help, self.radio_ui_language_system_default)
        QWidget.setTabOrder(self.radio_ui_language_system_default, self.radio_ui_language_english)
        QWidget.setTabOrder(self.radio_ui_language_english, self.radio_ui_language_german)
        QWidget.setTabOrder(self.radio_ui_language_german, self.radio_ui_language_chinese_simplified)
        QWidget.setTabOrder(self.radio_ui_language_chinese_simplified, self.radio_ui_language_french)
        QWidget.setTabOrder(self.radio_ui_language_french, self.button_settings_apply)
        QWidget.setTabOrder(self.button_settings_apply, self.button_settings_reset)
        QWidget.setTabOrder(self.button_settings_reset, self.textBrowser)
        QWidget.setTabOrder(self.textBrowser, self.textbrowser_websites)

        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(1)
        self.stacked_widget_top.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch V3.4 (C) Johannes Habel GPL 3", None))
        self.groupbox_top_bar.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch Menu", None))
        self.button_switch_settings.setText("")
        self.button_switch_tools.setText("")
        self.button_switch_home.setText("")
        self.button_switch_credits.setText("")
        self.button_switch_account.setText("")
        self.button_view_progress_bars.setText("")
        self.stacked_widget_main.setStyleSheet("")
        self.button_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter video URL", None))
        self.button_open_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.label_search_website.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Website", None))
        self.button_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter Model / Channel / Actress URL", None))
        self.radio_search_website_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub", None))
        self.radio_search_website_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner", None))
        self.radio_search_website_xvideos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XVideos", None))
        self.radio_search_website_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"EPorner", None))
        self.radio_search_website_xnxx.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XNXX", None))
        self.button_switch_supported_websites.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"See Supported Websites", None))
        self.lineedit_file.setText("")
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"URLs in the file must be separated with new lines!", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.lineedit_playlist_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter a PornHub Playlist URL", None))
        self.labell_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.label_playlist_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Playlist URL:", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.button_playlist_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_search_query.setText("")
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search for Videos. Select Website below", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.button_help_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.button_get_liked_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.button_get_watched_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
        self.button_get_recommended_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.label_progress_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub:", None))
        self.label_progress_xvideos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XVideos", None))
        self.label_progress_xnxx.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XNXX", None))
        self.label_progress_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner:", None))
        self.label_progress_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Eporner", None))
        self.label_info.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Info:", None))
        self.lineedit_download_info.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"EPorner", None))
        self.label_videos_by_category_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get videos by category", None))
        self.button_eporner_category_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.button_list_categories_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"List of all categories", None))
        self.groupbox_tools.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner", None))
        self.radio_top_porn_month.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Month", None))
        self.button_top_porn_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.label_get_brazzers_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Brazzers videos", None))
        self.radio_top_porn_week.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Week", None))
        self.button_list_categories.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"List of all categories", None))
        self.label_get_top_porn.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Top Porn:", None))
        self.radio_top_porn_all_time.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"All Time", None))
        self.button_hqporner_category_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.button_get_random_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Video", None))
        self.button_get_brazzers_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.labe_get_random_video.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get random video", None))
        self.label_videos_by_category.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get videos by category", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Porn_Fetch_Widget", u"Duration (minutes)", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Porn_Fetch_Widget", u"Author", None));
#if QT_CONFIG(tooltip)
        self.radio_tree_show_all.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.radio_tree_show_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Title, Author, Duration", None))
        self.radio_tree_show_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Only Title (a lot faster)", None))
        self.checkbox_tree_do_not_clear_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Do not clear videos", None))
        self.checkbox_tree_show_videos_reversed.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Show videos in reverse", None))
        self.button_tree_export_video_urls.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Export video URLs", None))
#if QT_CONFIG(tooltip)
        self.button_tree_stop.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Does not stop downloading videos", None))
#endif // QT_CONFIG(tooltip)
        self.button_tree_stop.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Stop loading videos", None))
#if QT_CONFIG(tooltip)
        self.button_tree_select_range.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Automatically checks a range of videos", None))
#endif // QT_CONFIG(tooltip)
        self.button_tree_select_range.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select a range of videos", None))
        self.button_range_apply_everything.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select everything", None))
        self.button_tree_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Selected Videos", None))
#if QT_CONFIG(tooltip)
        self.button_tree_unselect_all.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselects all videos in the tree widget", None))
#endif // QT_CONFIG(tooltip)
        self.button_tree_unselect_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselect all", None))
        self.button_download_ffmpeg.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download and Setup FFmpeg", None))
        self.groupbox_performance.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Performance", None))
        self.label_semaphore.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Simultaneous downloads:", None))
        self.button_semaphore_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_maximal_workers.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Maximal workers:", None))
        self.button_workers_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_pornhub_delay.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub Delay (0 = Disabled) in seconds:", None))
        self.button_pornhub_delay_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_threading_mode.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading Mode:", None))
        self.radio_threading_mode_high_performance.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"High Performance", None))
        self.radio_threading_mode_ffmpeg.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"FFMPEG", None))
        self.radio_threading_mode_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Default", None))
        self.button_threading_mode_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_maximal_timeout.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Maximal timeout:", None))
        self.button_timeout_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_maximal_retries.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Maximal retries:", None))
        self.button_timeout_maximal_retries_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.groupbox_videos.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Videos", None))
        self.label_output_path.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Output path:", None))
        self.lineedit_output_path.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter \"./\" for current directory", None))
        self.button_output_path_select.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open", None))
        self.label_searching_limit.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Result Limit:", None))
        self.button_result_limit_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_quality.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Quality:", None))
        self.radio_quality_best.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Best", None))
        self.radio_quality_half.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Half", None))
        self.radio_quality_worst.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Worst", None))
        self.label_skip_existing_files.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Skip existing files:", None))
        self.radio_skip_existing_files_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_skip_existing_files_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.button_help_skip_existing_files.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_directory_system.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Use Directory system? ", None))
        self.radio_directory_system_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_directory_system_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.button_directory_system_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.labe_settings_videos_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model videos (PornHub)", None))
        self.radio_model_uploads.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User uploads", None))
        self.radio_model_featured.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Featured videos", None))
        self.radio_model_both.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Both", None))
        self.button_help_model_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.goroupbox_gui.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface", None))
        self.radio_ui_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.radio_ui_language_chinese_simplified.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese (simplified)", None))
        self.radio_ui_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_ui_language_system_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"System default", None))
        self.label_ui_language.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface Language:", None))
        self.radio_ui_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Apply  (needs restart)", None))
        self.button_settings_reset.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Reset Porn Fetch to default settings", None))
        self.textbrowser_websites.setHtml(QCoreApplication.translate("Porn_Fetch_Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Supported Websites:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Downloading:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-righ"
                        "t:0px; -qt-block-indent:0; text-indent:0px;\">- PornHub.com (supports total progress)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- HQPorner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Eporner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- XNXX.com (supports total progress)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- XVideos.com (supports total progress)</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All sites support *threaded"
                        "* downloads and selectable quality!</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">* hqporner and eporner running in QThreads, but they don't fetch segments. The video is directly</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">downloaded, therefore threading in a segment isn't needed.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Model / Channel Downloads</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; m"
                        "argin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- PornHub.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- HQPorner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- EPorner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- XNXX.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- XVideos.com</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\">Searching:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- PornHub.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- HQPorner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Xvideos.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Eporner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- XNXX.com</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; ma"
                        "rgin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">I am constantly working to support more websites.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-"
                        "indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_progress_converting.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Converting:", None))
        self.label_progress_information.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Information: The total progressbar does not count for Eporner and HQPorner, because they are using different mechanisms for downloading.", None))
    # retranslateUi

