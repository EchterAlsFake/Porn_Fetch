# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1054, 829)
        font = QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-color: #262626;\n"
"color: white")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_26 = QGridLayout(self.centralwidget)
        self.gridLayout_26.setSpacing(0)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.main_horizontallayout_menu_buttons = QHBoxLayout()
        self.main_horizontallayout_menu_buttons.setSpacing(5)
        self.main_horizontallayout_menu_buttons.setObjectName(u"main_horizontallayout_menu_buttons")
        self.main_button_switch_home = QPushButton(self.centralwidget)
        self.main_button_switch_home.setObjectName(u"main_button_switch_home")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_button_switch_home.sizePolicy().hasHeightForWidth())
        self.main_button_switch_home.setSizePolicy(sizePolicy)
        self.main_button_switch_home.setMinimumSize(QSize(50, 35))
        self.main_button_switch_home.setMaximumSize(QSize(16777215, 35))
        self.main_button_switch_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_home.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #a9a9a9;\n"
"    border-radius: 8px;\n"
"    padding: 8px 10px;\n"
"}")
        self.main_button_switch_home.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_home)

        self.main_button_switch_account = QPushButton(self.centralwidget)
        self.main_button_switch_account.setObjectName(u"main_button_switch_account")
        sizePolicy.setHeightForWidth(self.main_button_switch_account.sizePolicy().hasHeightForWidth())
        self.main_button_switch_account.setSizePolicy(sizePolicy)
        self.main_button_switch_account.setMinimumSize(QSize(50, 35))
        self.main_button_switch_account.setMaximumSize(QSize(16777215, 35))
        self.main_button_switch_account.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_account.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    padding: 8px 10px;\n"
"    border: 2px solid #a9a9a9;\n"
"}\n"
"")
        self.main_button_switch_account.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_account)

        self.main_button_switch_tools = QPushButton(self.centralwidget)
        self.main_button_switch_tools.setObjectName(u"main_button_switch_tools")
        sizePolicy.setHeightForWidth(self.main_button_switch_tools.sizePolicy().hasHeightForWidth())
        self.main_button_switch_tools.setSizePolicy(sizePolicy)
        self.main_button_switch_tools.setMinimumSize(QSize(50, 35))
        self.main_button_switch_tools.setMaximumSize(QSize(16777215, 35))
        font1 = QFont()
        self.main_button_switch_tools.setFont(font1)
        self.main_button_switch_tools.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_tools.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.main_button_switch_tools.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_tools)

        self.main_button_switch_settings = QPushButton(self.centralwidget)
        self.main_button_switch_settings.setObjectName(u"main_button_switch_settings")
        sizePolicy.setHeightForWidth(self.main_button_switch_settings.sizePolicy().hasHeightForWidth())
        self.main_button_switch_settings.setSizePolicy(sizePolicy)
        self.main_button_switch_settings.setMinimumSize(QSize(50, 35))
        self.main_button_switch_settings.setMaximumSize(QSize(16777215, 35))
        self.main_button_switch_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_settings.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.main_button_switch_settings.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_settings)

        self.main_button_switch_credits = QPushButton(self.centralwidget)
        self.main_button_switch_credits.setObjectName(u"main_button_switch_credits")
        sizePolicy.setHeightForWidth(self.main_button_switch_credits.sizePolicy().hasHeightForWidth())
        self.main_button_switch_credits.setSizePolicy(sizePolicy)
        self.main_button_switch_credits.setMinimumSize(QSize(50, 35))
        self.main_button_switch_credits.setMaximumSize(QSize(16777215, 35))
        self.main_button_switch_credits.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_credits.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.main_button_switch_credits.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_credits)

        self.main_button_view_progress_bars = QPushButton(self.centralwidget)
        self.main_button_view_progress_bars.setObjectName(u"main_button_view_progress_bars")
        sizePolicy.setHeightForWidth(self.main_button_view_progress_bars.sizePolicy().hasHeightForWidth())
        self.main_button_view_progress_bars.setSizePolicy(sizePolicy)
        self.main_button_view_progress_bars.setMinimumSize(QSize(50, 35))
        self.main_button_view_progress_bars.setMaximumSize(QSize(16777215, 35))
        self.main_button_view_progress_bars.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_view_progress_bars.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}")
        self.main_button_view_progress_bars.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_view_progress_bars)

        self.main_button_switch_supported_websites = QPushButton(self.centralwidget)
        self.main_button_switch_supported_websites.setObjectName(u"main_button_switch_supported_websites")
        sizePolicy.setHeightForWidth(self.main_button_switch_supported_websites.sizePolicy().hasHeightForWidth())
        self.main_button_switch_supported_websites.setSizePolicy(sizePolicy)
        self.main_button_switch_supported_websites.setMinimumSize(QSize(50, 35))
        self.main_button_switch_supported_websites.setMaximumSize(QSize(16777215, 35))
        self.main_button_switch_supported_websites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_supported_websites.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}")
        self.main_button_switch_supported_websites.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_supported_websites)


        self.gridLayout_26.addLayout(self.main_horizontallayout_menu_buttons, 0, 0, 1, 1)

        self.CentralStackedWidget = QStackedWidget(self.centralwidget)
        self.CentralStackedWidget.setObjectName(u"CentralStackedWidget")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.page_main.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_9 = QGridLayout(self.page_main)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.main_verticallayout = QVBoxLayout()
        self.main_verticallayout.setSpacing(5)
        self.main_verticallayout.setObjectName(u"main_verticallayout")
        self.main_verticallayout.setContentsMargins(-1, 3, -1, -1)
        self.scroll_area_top_stacked = QScrollArea(self.page_main)
        self.scroll_area_top_stacked.setObjectName(u"scroll_area_top_stacked")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scroll_area_top_stacked.sizePolicy().hasHeightForWidth())
        self.scroll_area_top_stacked.setSizePolicy(sizePolicy1)
        self.scroll_area_top_stacked.setMinimumSize(QSize(0, 110))
        self.scroll_area_top_stacked.setMaximumSize(QSize(16777215, 240))
        self.scroll_area_top_stacked.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 580, 220))
        self.gridLayout_8 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.main_stacked_widget_top = QStackedWidget(self.scrollAreaWidgetContents)
        self.main_stacked_widget_top.setObjectName(u"main_stacked_widget_top")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.main_stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.main_stacked_widget_top.setSizePolicy(sizePolicy2)
        self.main_stacked_widget_top.setMinimumSize(QSize(0, 220))
        self.main_stacked_widget_top.setMaximumSize(QSize(16777215, 230))
        self.main_stacked_widget_top.setStyleSheet(u"b")
        self.main_stacked_widget_top.setLineWidth(1)
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.page_download.sizePolicy().hasHeightForWidth())
        self.page_download.setSizePolicy(sizePolicy3)
        self.page_download.setMinimumSize(QSize(0, 220))
        self.page_download.setMaximumSize(QSize(16777215, 220))
        self.gridLayout_5 = QGridLayout(self.page_download)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(6)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridlayout_downloading.setContentsMargins(-1, 0, -1, -1)
        self.download_radio_search_website_hqporner = QRadioButton(self.page_download)
        self.download_radio_search_website_hqporner.setObjectName(u"download_radio_search_website_hqporner")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.download_radio_search_website_hqporner.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_hqporner.setSizePolicy(sizePolicy4)
        self.download_radio_search_website_hqporner.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_hqporner, 8, 2, 1, 1)

        self.download_button_model = QPushButton(self.page_download)
        self.download_button_model.setObjectName(u"download_button_model")
        sizePolicy4.setHeightForWidth(self.download_button_model.sizePolicy().hasHeightForWidth())
        self.download_button_model.setSizePolicy(sizePolicy4)
        self.download_button_model.setMinimumSize(QSize(60, 30))
        self.download_button_model.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_model.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_model, 5, 5, 1, 1)

        self.download_lineedit_model_url = QLineEdit(self.page_download)
        self.download_lineedit_model_url.setObjectName(u"download_lineedit_model_url")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.download_lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_model_url.setSizePolicy(sizePolicy5)
        self.download_lineedit_model_url.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_model_url, 5, 1, 1, 4)

        self.download_lineedit_playlist_url = QLineEdit(self.page_download)
        self.download_lineedit_playlist_url.setObjectName(u"download_lineedit_playlist_url")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.download_lineedit_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_playlist_url.setSizePolicy(sizePolicy6)
        self.download_lineedit_playlist_url.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_playlist_url, 4, 1, 1, 4)

        self.button_search = QPushButton(self.page_download)
        self.button_search.setObjectName(u"button_search")
        sizePolicy4.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy4)
        self.button_search.setMinimumSize(QSize(0, 30))
        self.button_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search, 7, 5, 1, 1)

        self.download_label_file = QLabel(self.page_download)
        self.download_label_file.setObjectName(u"download_label_file")
        sizePolicy4.setHeightForWidth(self.download_label_file.sizePolicy().hasHeightForWidth())
        self.download_label_file.setSizePolicy(sizePolicy4)
        self.download_label_file.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.download_label_file, 6, 0, 1, 1)

        self.download_button_help_file = QPushButton(self.page_download)
        self.download_button_help_file.setObjectName(u"download_button_help_file")
        sizePolicy4.setHeightForWidth(self.download_button_help_file.sizePolicy().hasHeightForWidth())
        self.download_button_help_file.setSizePolicy(sizePolicy4)
        self.download_button_help_file.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_button_help_file, 6, 4, 1, 1)

        self.download_button_playlist_get_videos = QPushButton(self.page_download)
        self.download_button_playlist_get_videos.setObjectName(u"download_button_playlist_get_videos")
        sizePolicy4.setHeightForWidth(self.download_button_playlist_get_videos.sizePolicy().hasHeightForWidth())
        self.download_button_playlist_get_videos.setSizePolicy(sizePolicy4)
        self.download_button_playlist_get_videos.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_button_playlist_get_videos, 4, 5, 1, 1)

        self.download_lineedit_search_query = QLineEdit(self.page_download)
        self.download_lineedit_search_query.setObjectName(u"download_lineedit_search_query")
        sizePolicy5.setHeightForWidth(self.download_lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.download_lineedit_search_query.setSizePolicy(sizePolicy5)
        self.download_lineedit_search_query.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_search_query, 7, 1, 1, 4)

        self.download_label_search_website = QLabel(self.page_download)
        self.download_label_search_website.setObjectName(u"download_label_search_website")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.download_label_search_website.sizePolicy().hasHeightForWidth())
        self.download_label_search_website.setSizePolicy(sizePolicy7)
        self.download_label_search_website.setMinimumSize(QSize(0, 0))

        self.gridlayout_downloading.addWidget(self.download_label_search_website, 8, 0, 1, 1)

        self.download_label_playlist_url = QLabel(self.page_download)
        self.download_label_playlist_url.setObjectName(u"download_label_playlist_url")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.download_label_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_label_playlist_url.setSizePolicy(sizePolicy8)
        self.download_label_playlist_url.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_label_playlist_url, 4, 0, 1, 1)

        self.download_label_model_url = QLabel(self.page_download)
        self.download_label_model_url.setObjectName(u"download_label_model_url")
        sizePolicy4.setHeightForWidth(self.download_label_model_url.sizePolicy().hasHeightForWidth())
        self.download_label_model_url.setSizePolicy(sizePolicy4)
        self.download_label_model_url.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.download_label_model_url, 5, 0, 1, 1)

        self.download_radio_search_website_xnxx = QRadioButton(self.page_download)
        self.download_radio_search_website_xnxx.setObjectName(u"download_radio_search_website_xnxx")
        sizePolicy4.setHeightForWidth(self.download_radio_search_website_xnxx.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_xnxx.setSizePolicy(sizePolicy4)
        self.download_radio_search_website_xnxx.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_xnxx, 8, 5, 1, 1)

        self.download_button_download = QPushButton(self.page_download)
        self.download_button_download.setObjectName(u"download_button_download")
        sizePolicy4.setHeightForWidth(self.download_button_download.sizePolicy().hasHeightForWidth())
        self.download_button_download.setSizePolicy(sizePolicy4)
        self.download_button_download.setMinimumSize(QSize(60, 30))
        self.download_button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_download, 2, 5, 1, 1)

        self.download_lineedit_file = QLineEdit(self.page_download)
        self.download_lineedit_file.setObjectName(u"download_lineedit_file")
        sizePolicy5.setHeightForWidth(self.download_lineedit_file.sizePolicy().hasHeightForWidth())
        self.download_lineedit_file.setSizePolicy(sizePolicy5)
        self.download_lineedit_file.setMinimumSize(QSize(300, 30))
        self.download_lineedit_file.setReadOnly(True)

        self.gridlayout_downloading.addWidget(self.download_lineedit_file, 6, 1, 1, 3)

        self.download_radio_search_website_xvideos = QRadioButton(self.page_download)
        self.download_radio_search_website_xvideos.setObjectName(u"download_radio_search_website_xvideos")
        sizePolicy4.setHeightForWidth(self.download_radio_search_website_xvideos.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_xvideos.setSizePolicy(sizePolicy4)
        self.download_radio_search_website_xvideos.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_xvideos, 8, 3, 1, 1)

        self.download_label_search = QLabel(self.page_download)
        self.download_label_search.setObjectName(u"download_label_search")
        sizePolicy8.setHeightForWidth(self.download_label_search.sizePolicy().hasHeightForWidth())
        self.download_label_search.setSizePolicy(sizePolicy8)
        self.download_label_search.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_label_search, 7, 0, 1, 1)

        self.download_lineedit_url = QLineEdit(self.page_download)
        self.download_lineedit_url.setObjectName(u"download_lineedit_url")
        sizePolicy5.setHeightForWidth(self.download_lineedit_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_url.setSizePolicy(sizePolicy5)
        self.download_lineedit_url.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_url, 2, 1, 1, 4)

        self.download_radio_search_website_eporner = QRadioButton(self.page_download)
        self.download_radio_search_website_eporner.setObjectName(u"download_radio_search_website_eporner")
        sizePolicy4.setHeightForWidth(self.download_radio_search_website_eporner.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_eporner.setSizePolicy(sizePolicy4)
        self.download_radio_search_website_eporner.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_eporner, 8, 4, 1, 1)

        self.download_radio_search_website_pornhub = QRadioButton(self.page_download)
        self.download_radio_search_website_pornhub.setObjectName(u"download_radio_search_website_pornhub")
        sizePolicy4.setHeightForWidth(self.download_radio_search_website_pornhub.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_pornhub.setSizePolicy(sizePolicy4)
        self.download_radio_search_website_pornhub.setMinimumSize(QSize(0, 30))
        self.download_radio_search_website_pornhub.setChecked(True)

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_pornhub, 8, 1, 1, 1)

        self.download_label_url = QLabel(self.page_download)
        self.download_label_url.setObjectName(u"download_label_url")
        sizePolicy4.setHeightForWidth(self.download_label_url.sizePolicy().hasHeightForWidth())
        self.download_label_url.setSizePolicy(sizePolicy4)
        self.download_label_url.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.download_label_url, 2, 0, 1, 1)

        self.download_button_open_file = QPushButton(self.page_download)
        self.download_button_open_file.setObjectName(u"download_button_open_file")
        sizePolicy4.setHeightForWidth(self.download_button_open_file.sizePolicy().hasHeightForWidth())
        self.download_button_open_file.setSizePolicy(sizePolicy4)
        self.download_button_open_file.setMinimumSize(QSize(60, 30))
        self.download_button_open_file.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_open_file.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_open_file, 6, 5, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_downloading, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_download)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.page_login.setMinimumSize(QSize(0, 110))
        self.gridLayout_2 = QGridLayout(self.page_login)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.login_gridlayout_login_box = QGridLayout()
        self.login_gridlayout_login_box.setSpacing(6)
        self.login_gridlayout_login_box.setObjectName(u"login_gridlayout_login_box")
        self.login_gridlayout_login_box.setContentsMargins(-1, 0, -1, -1)
        self.login_button_get_liked_videos = QPushButton(self.page_login)
        self.login_button_get_liked_videos.setObjectName(u"login_button_get_liked_videos")
        self.login_button_get_liked_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_liked_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_liked_videos.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_get_liked_videos, 3, 0, 1, 1)

        self.login_button_get_recommended_videos = QPushButton(self.page_login)
        self.login_button_get_recommended_videos.setObjectName(u"login_button_get_recommended_videos")
        self.login_button_get_recommended_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_recommended_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_recommended_videos.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_get_recommended_videos, 3, 2, 1, 1)

        self.login_label_password = QLabel(self.page_login)
        self.login_label_password.setObjectName(u"login_label_password")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.login_label_password.sizePolicy().hasHeightForWidth())
        self.login_label_password.setSizePolicy(sizePolicy9)
        self.login_label_password.setMinimumSize(QSize(0, 30))

        self.login_gridlayout_login_box.addWidget(self.login_label_password, 1, 0, 1, 1)

        self.login_label_username = QLabel(self.page_login)
        self.login_label_username.setObjectName(u"login_label_username")
        sizePolicy9.setHeightForWidth(self.login_label_username.sizePolicy().hasHeightForWidth())
        self.login_label_username.setSizePolicy(sizePolicy9)
        self.login_label_username.setMinimumSize(QSize(0, 30))

        self.login_gridlayout_login_box.addWidget(self.login_label_username, 0, 0, 1, 1)

        self.login_button_login = QPushButton(self.page_login)
        self.login_button_login.setObjectName(u"login_button_login")
        self.login_button_login.setMinimumSize(QSize(0, 30))
        self.login_button_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_login.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_login, 2, 0, 1, 4)

        self.login_lineedit_password = QLineEdit(self.page_login)
        self.login_lineedit_password.setObjectName(u"login_lineedit_password")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.login_lineedit_password.sizePolicy().hasHeightForWidth())
        self.login_lineedit_password.setSizePolicy(sizePolicy10)
        self.login_lineedit_password.setMinimumSize(QSize(150, 30))
        self.login_lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_password, 1, 1, 1, 3)

        self.login_lineedit_username = QLineEdit(self.page_login)
        self.login_lineedit_username.setObjectName(u"login_lineedit_username")
        sizePolicy10.setHeightForWidth(self.login_lineedit_username.sizePolicy().hasHeightForWidth())
        self.login_lineedit_username.setSizePolicy(sizePolicy10)
        self.login_lineedit_username.setMinimumSize(QSize(150, 30))

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_username, 0, 1, 1, 3)

        self.login_button_get_watched_videos = QPushButton(self.page_login)
        self.login_button_get_watched_videos.setObjectName(u"login_button_get_watched_videos")
        self.login_button_get_watched_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_watched_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_watched_videos.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_get_watched_videos, 3, 1, 1, 1)

        self.login_spacer_main = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.login_gridlayout_login_box.addItem(self.login_spacer_main, 4, 1, 1, 1)


        self.gridLayout_2.addLayout(self.login_gridlayout_login_box, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_login)
        self.page_progressbars = QWidget()
        self.page_progressbars.setObjectName(u"page_progressbars")
        sizePolicy9.setHeightForWidth(self.page_progressbars.sizePolicy().hasHeightForWidth())
        self.page_progressbars.setSizePolicy(sizePolicy9)
        self.page_progressbars.setMinimumSize(QSize(20, 10))
        self.page_progressbars.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_6 = QGridLayout(self.page_progressbars)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_2 = QSpacerItem(248, 88, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.progress_gridlayout_progressbar = QGridLayout()
        self.progress_gridlayout_progressbar.setObjectName(u"progress_gridlayout_progressbar")
        self.progress_gridlayout_progressbar.setHorizontalSpacing(6)
        self.progress_gridlayout_progressbar.setContentsMargins(-1, -1, -1, 0)
        self.progress_label_info = QLabel(self.page_progressbars)
        self.progress_label_info.setObjectName(u"progress_label_info")
        self.progress_label_info.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_info, 1, 0, 1, 1)

        self.progress_lineedit_download_info = QLineEdit(self.page_progressbars)
        self.progress_lineedit_download_info.setObjectName(u"progress_lineedit_download_info")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.progress_lineedit_download_info.sizePolicy().hasHeightForWidth())
        self.progress_lineedit_download_info.setSizePolicy(sizePolicy11)
        self.progress_lineedit_download_info.setReadOnly(True)

        self.progress_gridlayout_progressbar.addWidget(self.progress_lineedit_download_info, 1, 1, 1, 1)


        self.gridLayout_6.addLayout(self.progress_gridlayout_progressbar, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_progressbars)
        self.page_tools = QWidget()
        self.page_tools.setObjectName(u"page_tools")
        sizePolicy3.setHeightForWidth(self.page_tools.sizePolicy().hasHeightForWidth())
        self.page_tools.setSizePolicy(sizePolicy3)
        self.page_tools.setMinimumSize(QSize(100, 30))
        self.gridLayout_17 = QGridLayout(self.page_tools)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.page_tools)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_15 = QGridLayout(self.groupBox)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tools_radio_top_porn_week = QRadioButton(self.groupBox)
        self.tools_radio_top_porn_week.setObjectName(u"tools_radio_top_porn_week")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.tools_radio_top_porn_week.sizePolicy().hasHeightForWidth())
        self.tools_radio_top_porn_week.setSizePolicy(sizePolicy12)
        self.tools_radio_top_porn_week.setMinimumSize(QSize(0, 0))
        self.tools_radio_top_porn_week.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tools_radio_top_porn_week.setChecked(True)

        self.gridLayout_3.addWidget(self.tools_radio_top_porn_week, 0, 1, 1, 1)

        self.tools_button_hqporner_category_get_videos = QPushButton(self.groupBox)
        self.tools_button_hqporner_category_get_videos.setObjectName(u"tools_button_hqporner_category_get_videos")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(2)
        sizePolicy13.setHeightForWidth(self.tools_button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_hqporner_category_get_videos.setSizePolicy(sizePolicy13)
        self.tools_button_hqporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_hqporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_hqporner_category_get_videos, 1, 2, 1, 1)

        self.tools_label_videos_by_category = QLabel(self.groupBox)
        self.tools_label_videos_by_category.setObjectName(u"tools_label_videos_by_category")
        sizePolicy9.setHeightForWidth(self.tools_label_videos_by_category.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category.setSizePolicy(sizePolicy9)
        self.tools_label_videos_by_category.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_videos_by_category, 1, 0, 1, 1)

        self.tools_label_get_top_porn = QLabel(self.groupBox)
        self.tools_label_get_top_porn.setObjectName(u"tools_label_get_top_porn")
        sizePolicy9.setHeightForWidth(self.tools_label_get_top_porn.sizePolicy().hasHeightForWidth())
        self.tools_label_get_top_porn.setSizePolicy(sizePolicy9)
        self.tools_label_get_top_porn.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_top_porn, 0, 0, 1, 1)

        self.tools_radio_top_porn_month = QRadioButton(self.groupBox)
        self.tools_radio_top_porn_month.setObjectName(u"tools_radio_top_porn_month")
        sizePolicy12.setHeightForWidth(self.tools_radio_top_porn_month.sizePolicy().hasHeightForWidth())
        self.tools_radio_top_porn_month.setSizePolicy(sizePolicy12)
        self.tools_radio_top_porn_month.setMinimumSize(QSize(0, 0))
        self.tools_radio_top_porn_month.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_radio_top_porn_month, 0, 2, 1, 1)

        self.tools_label_get_random_video = QLabel(self.groupBox)
        self.tools_label_get_random_video.setObjectName(u"tools_label_get_random_video")
        sizePolicy9.setHeightForWidth(self.tools_label_get_random_video.sizePolicy().hasHeightForWidth())
        self.tools_label_get_random_video.setSizePolicy(sizePolicy9)
        self.tools_label_get_random_video.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_random_video, 2, 0, 1, 1)

        self.tools_radio_top_porn_all_time = QRadioButton(self.groupBox)
        self.tools_radio_top_porn_all_time.setObjectName(u"tools_radio_top_porn_all_time")
        sizePolicy12.setHeightForWidth(self.tools_radio_top_porn_all_time.sizePolicy().hasHeightForWidth())
        self.tools_radio_top_porn_all_time.setSizePolicy(sizePolicy12)
        self.tools_radio_top_porn_all_time.setMinimumSize(QSize(0, 0))
        self.tools_radio_top_porn_all_time.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_radio_top_porn_all_time, 0, 3, 1, 1)

        self.tools_button_list_categories = QPushButton(self.groupBox)
        self.tools_button_list_categories.setObjectName(u"tools_button_list_categories")
        sizePolicy12.setHeightForWidth(self.tools_button_list_categories.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories.setSizePolicy(sizePolicy12)
        self.tools_button_list_categories.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_list_categories, 1, 3, 1, 1)

        self.tools_button_get_random_videos = QPushButton(self.groupBox)
        self.tools_button_get_random_videos.setObjectName(u"tools_button_get_random_videos")
        sizePolicy3.setHeightForWidth(self.tools_button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_random_videos.setSizePolicy(sizePolicy3)
        self.tools_button_get_random_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_random_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_get_random_videos, 2, 1, 1, 1)

        self.tools_lineedit_hqporner_category = QLineEdit(self.groupBox)
        self.tools_lineedit_hqporner_category.setObjectName(u"tools_lineedit_hqporner_category")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(4)
        sizePolicy14.setHeightForWidth(self.tools_lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_hqporner_category.setSizePolicy(sizePolicy14)
        self.tools_lineedit_hqporner_category.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.tools_lineedit_hqporner_category, 1, 1, 1, 1)

        self.tools_button_top_porn_get_videos = QPushButton(self.groupBox)
        self.tools_button_top_porn_get_videos.setObjectName(u"tools_button_top_porn_get_videos")
        sizePolicy12.setHeightForWidth(self.tools_button_top_porn_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_top_porn_get_videos.setSizePolicy(sizePolicy12)
        self.tools_button_top_porn_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_top_porn_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_top_porn_get_videos, 0, 4, 1, 1)

        self.tools_label_get_brazzers_videos = QLabel(self.groupBox)
        self.tools_label_get_brazzers_videos.setObjectName(u"tools_label_get_brazzers_videos")
        sizePolicy9.setHeightForWidth(self.tools_label_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.tools_label_get_brazzers_videos.setSizePolicy(sizePolicy9)
        self.tools_label_get_brazzers_videos.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_brazzers_videos, 3, 0, 1, 1)

        self.tools_button_get_brazzers_videos = QPushButton(self.groupBox)
        self.tools_button_get_brazzers_videos.setObjectName(u"tools_button_get_brazzers_videos")
        sizePolicy3.setHeightForWidth(self.tools_button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_brazzers_videos.setSizePolicy(sizePolicy3)
        self.tools_button_get_brazzers_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_brazzers_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_get_brazzers_videos, 3, 1, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.page_tools)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.gridLayout_16 = QGridLayout(self.groupBox_2)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.tools_gridlayout_tools = QGridLayout()
        self.tools_gridlayout_tools.setSpacing(6)
        self.tools_gridlayout_tools.setObjectName(u"tools_gridlayout_tools")
        self.tools_gridlayout_tools.setContentsMargins(-1, 0, -1, -1)
        self.tools_lineedit_videos_by_category_eporner = QLineEdit(self.groupBox_2)
        self.tools_lineedit_videos_by_category_eporner.setObjectName(u"tools_lineedit_videos_by_category_eporner")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(4)
        sizePolicy15.setHeightForWidth(self.tools_lineedit_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_videos_by_category_eporner.setSizePolicy(sizePolicy15)
        self.tools_lineedit_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_lineedit_videos_by_category_eporner, 4, 1, 1, 2)

        self.tools_button_eporner_category_get_videos = QPushButton(self.groupBox_2)
        self.tools_button_eporner_category_get_videos.setObjectName(u"tools_button_eporner_category_get_videos")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(2)
        sizePolicy16.setHeightForWidth(self.tools_button_eporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_eporner_category_get_videos.setSizePolicy(sizePolicy16)
        self.tools_button_eporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_eporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_eporner_category_get_videos, 4, 4, 1, 1)

        self.tools_button_list_categories_eporner = QPushButton(self.groupBox_2)
        self.tools_button_list_categories_eporner.setObjectName(u"tools_button_list_categories_eporner")
        sizePolicy12.setHeightForWidth(self.tools_button_list_categories_eporner.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories_eporner.setSizePolicy(sizePolicy12)
        self.tools_button_list_categories_eporner.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories_eporner.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_list_categories_eporner, 4, 3, 1, 1)

        self.tools_label_videos_by_category_eporner = QLabel(self.groupBox_2)
        self.tools_label_videos_by_category_eporner.setObjectName(u"tools_label_videos_by_category_eporner")
        sizePolicy3.setHeightForWidth(self.tools_label_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category_eporner.setSizePolicy(sizePolicy3)
        self.tools_label_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_label_videos_by_category_eporner, 4, 0, 1, 1)


        self.gridLayout_16.addLayout(self.tools_gridlayout_tools, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_2)


        self.gridLayout_17.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_tools)

        self.gridLayout_8.addWidget(self.main_stacked_widget_top, 0, 0, 1, 1)

        self.scroll_area_top_stacked.setWidget(self.scrollAreaWidgetContents)

        self.main_verticallayout.addWidget(self.scroll_area_top_stacked)

        self.main_scrollarea_treewidget = QScrollArea(self.page_main)
        self.main_scrollarea_treewidget.setObjectName(u"main_scrollarea_treewidget")
        self.main_scrollarea_treewidget.setWidgetResizable(True)
        self.main_scrollarea_treewidget_content = QWidget()
        self.main_scrollarea_treewidget_content.setObjectName(u"main_scrollarea_treewidget_content")
        self.main_scrollarea_treewidget_content.setGeometry(QRect(0, 0, 412, 207))
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.main_scrollarea_treewidget_content.sizePolicy().hasHeightForWidth())
        self.main_scrollarea_treewidget_content.setSizePolicy(sizePolicy17)
        self.gridLayout_4 = QGridLayout(self.main_scrollarea_treewidget_content)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.main_checkbox_tree_show_videos_reversed = QCheckBox(self.main_scrollarea_treewidget_content)
        self.main_checkbox_tree_show_videos_reversed.setObjectName(u"main_checkbox_tree_show_videos_reversed")
        self.main_checkbox_tree_show_videos_reversed.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_checkbox_tree_show_videos_reversed, 0, 0, 1, 1)

        self.main_checkbox_tree_do_not_clear_videos = QCheckBox(self.main_scrollarea_treewidget_content)
        self.main_checkbox_tree_do_not_clear_videos.setObjectName(u"main_checkbox_tree_do_not_clear_videos")

        self.gridLayout_13.addWidget(self.main_checkbox_tree_do_not_clear_videos, 0, 1, 1, 1)

        self.main_button_tree_automated_selection = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_automated_selection.setObjectName(u"main_button_tree_automated_selection")
        sizePolicy3.setHeightForWidth(self.main_button_tree_automated_selection.sizePolicy().hasHeightForWidth())
        self.main_button_tree_automated_selection.setSizePolicy(sizePolicy3)

        self.gridLayout_13.addWidget(self.main_button_tree_automated_selection, 1, 0, 1, 1)

        self.main_button_tree_keyboard_shortcuts = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_keyboard_shortcuts.setObjectName(u"main_button_tree_keyboard_shortcuts")

        self.gridLayout_13.addWidget(self.main_button_tree_keyboard_shortcuts, 1, 1, 1, 1)

        self.main_button_tree_stop = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_stop.setObjectName(u"main_button_tree_stop")
        sizePolicy.setHeightForWidth(self.main_button_tree_stop.sizePolicy().hasHeightForWidth())
        self.main_button_tree_stop.setSizePolicy(sizePolicy)
        self.main_button_tree_stop.setMinimumSize(QSize(0, 30))

        self.gridLayout_13.addWidget(self.main_button_tree_stop, 2, 0, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout_13)

        self.graphicsView = QGraphicsView(self.main_scrollarea_treewidget_content)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout_3.addWidget(self.graphicsView)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 2, 1, 1)

        self.main_button_tree_download = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_download.setObjectName(u"main_button_tree_download")
        sizePolicy.setHeightForWidth(self.main_button_tree_download.sizePolicy().hasHeightForWidth())
        self.main_button_tree_download.setSizePolicy(sizePolicy)
        self.main_button_tree_download.setMinimumSize(QSize(0, 30))
        self.main_button_tree_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_tree_download.setStyleSheet(u"")

        self.gridLayout.addWidget(self.main_button_tree_download, 1, 0, 1, 3)

        self.treeWidget = QTreeWidget(self.main_scrollarea_treewidget_content)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy18 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy18.setHorizontalStretch(0)
        sizePolicy18.setVerticalStretch(0)
        sizePolicy18.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy18)
        self.treeWidget.setMinimumSize(QSize(100, 10))

        self.gridLayout.addWidget(self.treeWidget, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.main_scrollarea_treewidget.setWidget(self.main_scrollarea_treewidget_content)

        self.main_verticallayout.addWidget(self.main_scrollarea_treewidget)


        self.gridLayout_9.addLayout(self.main_verticallayout, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_main)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.gridLayout_7 = QGridLayout(self.page_settings)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.settings_scrollarea = QScrollArea(self.page_settings)
        self.settings_scrollarea.setObjectName(u"settings_scrollarea")
        self.settings_scrollarea.setWidgetResizable(True)
        self.settings_scrollarea_widget_contents = QWidget()
        self.settings_scrollarea_widget_contents.setObjectName(u"settings_scrollarea_widget_contents")
        self.settings_scrollarea_widget_contents.setGeometry(QRect(0, 0, 739, 965))
        self.gridLayout_19 = QGridLayout(self.settings_scrollarea_widget_contents)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.settings_vertical_spacer_main = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_19.addItem(self.settings_vertical_spacer_main, 4, 0, 1, 2)

        self.settings_horizontallayout_apply = QHBoxLayout()
        self.settings_horizontallayout_apply.setObjectName(u"settings_horizontallayout_apply")
        self.settings_button_apply = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_apply.setObjectName(u"settings_button_apply")
        self.settings_button_apply.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_apply.addWidget(self.settings_button_apply)

        self.settings_button_reset = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_reset.setObjectName(u"settings_button_reset")
        self.settings_button_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_button_reset.setStyleSheet(u"QPushButton {\n"
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

        self.settings_horizontallayout_apply.addWidget(self.settings_button_reset)


        self.gridLayout_19.addLayout(self.settings_horizontallayout_apply, 2, 0, 2, 2)

        self.settings_scrollarea_gridlayout = QGridLayout()
        self.settings_scrollarea_gridlayout.setObjectName(u"settings_scrollarea_gridlayout")
        self.settings_horizontallayout_videos_post_processing = QHBoxLayout()
        self.settings_horizontallayout_videos_post_processing.setObjectName(u"settings_horizontallayout_videos_post_processing")
        self.settings_groupbox_videos = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_videos.setObjectName(u"settings_groupbox_videos")
        self.gridLayout_14 = QGridLayout(self.settings_groupbox_videos)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(6)
        self.gridLayout_14.setContentsMargins(6, 3, 6, 6)
        self.settings_gridlayout_videos = QGridLayout()
        self.settings_gridlayout_videos.setObjectName(u"settings_gridlayout_videos")
        self.settings_gridlayout_videos.setContentsMargins(6, 3, 6, 6)
        self.settings_radio_videos_quality_worst = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_videos_quality_worst.setObjectName(u"settings_radio_videos_quality_worst")
        self.settings_radio_videos_quality_worst.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_radio_videos_quality_worst, 0, 3, 1, 2)

        self.settings_radio_videos_quality_half = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_videos_quality_half.setObjectName(u"settings_radio_videos_quality_half")
        self.settings_radio_videos_quality_half.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_radio_videos_quality_half, 0, 2, 1, 1)

        self.settings_radio_videos_model_type_user_uploads = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_videos_model_type_user_uploads.setObjectName(u"settings_radio_videos_model_type_user_uploads")

        self.settings_gridlayout_videos.addWidget(self.settings_radio_videos_model_type_user_uploads, 5, 1, 1, 1)

        self.settings_lineedit_videos_output_path = QLineEdit(self.settings_groupbox_videos)
        self.settings_lineedit_videos_output_path.setObjectName(u"settings_lineedit_videos_output_path")
        sizePolicy12.setHeightForWidth(self.settings_lineedit_videos_output_path.sizePolicy().hasHeightForWidth())
        self.settings_lineedit_videos_output_path.setSizePolicy(sizePolicy12)

        self.settings_gridlayout_videos.addWidget(self.settings_lineedit_videos_output_path, 7, 1, 1, 2)

        self.settings_button_help_videos_model_videos_type = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_videos_model_videos_type.setObjectName(u"settings_button_help_videos_model_videos_type")

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_videos_model_videos_type, 5, 4, 1, 1)

        self.settings_button_help_videos_result_limit = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_videos_result_limit.setObjectName(u"settings_button_help_videos_result_limit")
        self.settings_button_help_videos_result_limit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_videos_result_limit, 6, 3, 1, 2)

        self.settings_spinbox_videos_result_limit = QSpinBox(self.settings_groupbox_videos)
        self.settings_spinbox_videos_result_limit.setObjectName(u"settings_spinbox_videos_result_limit")
        self.settings_spinbox_videos_result_limit.setMinimum(1)
        self.settings_spinbox_videos_result_limit.setMaximum(5000)

        self.settings_gridlayout_videos.addWidget(self.settings_spinbox_videos_result_limit, 6, 1, 1, 2)

        self.settings_button_videos_open_output_path = QPushButton(self.settings_groupbox_videos)
        self.settings_button_videos_open_output_path.setObjectName(u"settings_button_videos_open_output_path")
        self.settings_button_videos_open_output_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_button_videos_open_output_path, 7, 3, 1, 2)

        self.settings_button_help_videos_write_metadata = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_videos_write_metadata.setObjectName(u"settings_button_help_videos_write_metadata")

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_videos_write_metadata, 9, 1, 1, 1)

        self.settings_radio_videos_quality_best = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_videos_quality_best.setObjectName(u"settings_radio_videos_quality_best")
        self.settings_radio_videos_quality_best.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_radio_videos_quality_best, 0, 1, 1, 1)

        self.settings_label_videos_result_limit = QLabel(self.settings_groupbox_videos)
        self.settings_label_videos_result_limit.setObjectName(u"settings_label_videos_result_limit")

        self.settings_gridlayout_videos.addWidget(self.settings_label_videos_result_limit, 6, 0, 1, 1)

        self.settings_checkbox_videos_write_metadata = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_write_metadata.setObjectName(u"settings_checkbox_videos_write_metadata")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_write_metadata, 9, 0, 1, 1)

        self.settings_radio_videos_model_type_featured = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_videos_model_type_featured.setObjectName(u"settings_radio_videos_model_type_featured")

        self.settings_gridlayout_videos.addWidget(self.settings_radio_videos_model_type_featured, 5, 2, 1, 1)

        self.settings_label_videos_output_path = QLabel(self.settings_groupbox_videos)
        self.settings_label_videos_output_path.setObjectName(u"settings_label_videos_output_path")

        self.settings_gridlayout_videos.addWidget(self.settings_label_videos_output_path, 7, 0, 1, 1)

        self.settings_checkbox_videos_skip_existing_files = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_skip_existing_files.setObjectName(u"settings_checkbox_videos_skip_existing_files")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_skip_existing_files, 11, 0, 1, 1)

        self.settings_label_videos_quality = QLabel(self.settings_groupbox_videos)
        self.settings_label_videos_quality.setObjectName(u"settings_label_videos_quality")
        sizePolicy9.setHeightForWidth(self.settings_label_videos_quality.sizePolicy().hasHeightForWidth())
        self.settings_label_videos_quality.setSizePolicy(sizePolicy9)

        self.settings_gridlayout_videos.addWidget(self.settings_label_videos_quality, 0, 0, 1, 1)

        self.settings_button_help_videos_skip_existing_files = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_videos_skip_existing_files.setObjectName(u"settings_button_help_videos_skip_existing_files")

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_videos_skip_existing_files, 11, 1, 1, 1)

        self.settings_label_videos_model_vdeos_type = QLabel(self.settings_groupbox_videos)
        self.settings_label_videos_model_vdeos_type.setObjectName(u"settings_label_videos_model_vdeos_type")

        self.settings_gridlayout_videos.addWidget(self.settings_label_videos_model_vdeos_type, 5, 0, 1, 1)

        self.settings_radio_videos_model_type_both = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_videos_model_type_both.setObjectName(u"settings_radio_videos_model_type_both")

        self.settings_gridlayout_videos.addWidget(self.settings_radio_videos_model_type_both, 5, 3, 1, 1)

        self.settings_checkbox_videos_use_video_id_as_filename = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_use_video_id_as_filename.setObjectName(u"settings_checkbox_videos_use_video_id_as_filename")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_use_video_id_as_filename, 8, 0, 1, 2)

        self.settings_checkbox_videos_use_directory_system = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_use_directory_system.setObjectName(u"settings_checkbox_videos_use_directory_system")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_use_directory_system, 9, 2, 1, 1)

        self.settings_button_help_videos_use_directory_system = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_videos_use_directory_system.setObjectName(u"settings_button_help_videos_use_directory_system")
        self.settings_button_help_videos_use_directory_system.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_videos_use_directory_system, 9, 3, 1, 1)

        self.settings_checkbox_videos_direct_download = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_direct_download.setObjectName(u"settings_checkbox_videos_direct_download")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_direct_download, 11, 2, 1, 1)

        self.settings_button_help_videos_direct_download = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_videos_direct_download.setObjectName(u"settings_button_help_videos_direct_download")

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_videos_direct_download, 11, 3, 1, 1)


        self.gridLayout_14.addLayout(self.settings_gridlayout_videos, 6, 0, 1, 1)


        self.settings_horizontallayout_videos_post_processing.addWidget(self.settings_groupbox_videos)


        self.settings_scrollarea_gridlayout.addLayout(self.settings_horizontallayout_videos_post_processing, 2, 0, 1, 1)

        self.settings_groupbox_ui = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_ui.setObjectName(u"settings_groupbox_ui")
        self.gridLayout_12 = QGridLayout(self.settings_groupbox_ui)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.settings_gridlayout_graphical_userinterface = QGridLayout()
        self.settings_gridlayout_graphical_userinterface.setObjectName(u"settings_gridlayout_graphical_userinterface")
        self.settings_gridlayout_graphical_userinterface.setContentsMargins(6, 3, 6, 6)
        self.settings_radio_ui_language_system_default = QRadioButton(self.settings_groupbox_ui)
        self.settings_radio_ui_language_system_default.setObjectName(u"settings_radio_ui_language_system_default")
        self.settings_radio_ui_language_system_default.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_radio_ui_language_system_default, 0, 1, 1, 1)

        self.settings_label_ui_language = QLabel(self.settings_groupbox_ui)
        self.settings_label_ui_language.setObjectName(u"settings_label_ui_language")
        sizePolicy9.setHeightForWidth(self.settings_label_ui_language.sizePolicy().hasHeightForWidth())
        self.settings_label_ui_language.setSizePolicy(sizePolicy9)

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_label_ui_language, 0, 0, 1, 1)

        self.settings_radio_ui_language_english = QRadioButton(self.settings_groupbox_ui)
        self.settings_radio_ui_language_english.setObjectName(u"settings_radio_ui_language_english")
        self.settings_radio_ui_language_english.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_radio_ui_language_english, 0, 2, 1, 1)

        self.settings_radio_ui_language_french = QRadioButton(self.settings_groupbox_ui)
        self.settings_radio_ui_language_french.setObjectName(u"settings_radio_ui_language_french")
        self.settings_radio_ui_language_french.setEnabled(True)

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_radio_ui_language_french, 0, 5, 1, 1)

        self.settings_radio_ui_language_chinese_simplified = QRadioButton(self.settings_groupbox_ui)
        self.settings_radio_ui_language_chinese_simplified.setObjectName(u"settings_radio_ui_language_chinese_simplified")
        self.settings_radio_ui_language_chinese_simplified.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_radio_ui_language_chinese_simplified, 0, 4, 1, 1)

        self.settings_radio_ui_language_german = QRadioButton(self.settings_groupbox_ui)
        self.settings_radio_ui_language_german.setObjectName(u"settings_radio_ui_language_german")
        self.settings_radio_ui_language_german.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_radio_ui_language_german, 0, 3, 1, 1)

        self.settings_checkbox_ui_custom_font = QCheckBox(self.settings_groupbox_ui)
        self.settings_checkbox_ui_custom_font.setObjectName(u"settings_checkbox_ui_custom_font")

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_checkbox_ui_custom_font, 1, 0, 1, 1)

        self.settings_spinbox_ui_font_size = QSpinBox(self.settings_groupbox_ui)
        self.settings_spinbox_ui_font_size.setObjectName(u"settings_spinbox_ui_font_size")

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_spinbox_ui_font_size, 1, 2, 1, 1)

        self.settings_label_ui_font_size = QLabel(self.settings_groupbox_ui)
        self.settings_label_ui_font_size.setObjectName(u"settings_label_ui_font_size")

        self.settings_gridlayout_graphical_userinterface.addWidget(self.settings_label_ui_font_size, 1, 1, 1, 1)


        self.gridLayout_12.addLayout(self.settings_gridlayout_graphical_userinterface, 0, 0, 1, 1)


        self.settings_scrollarea_gridlayout.addWidget(self.settings_groupbox_ui, 4, 0, 1, 1)

        self.settings_groupbox_system_pornfetch = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_system_pornfetch.setObjectName(u"settings_groupbox_system_pornfetch")
        self.gridLayout_11 = QGridLayout(self.settings_groupbox_system_pornfetch)
        self.gridLayout_11.setSpacing(6)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(6, 6, 6, 6)
        self.settings_gridlayout_system_pornfetch = QGridLayout()
        self.settings_gridlayout_system_pornfetch.setObjectName(u"settings_gridlayout_system_pornfetch")
        self.settings_gridlayout_system_pornfetch.setContentsMargins(6, 3, 6, 6)
        self.settings_checkbox_system_enable_anonymous_mode = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_enable_anonymous_mode.setObjectName(u"settings_checkbox_system_enable_anonymous_mode")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_enable_anonymous_mode, 2, 1, 1, 1)

        self.settings_checkbox_system_enable_network_logging = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_enable_network_logging.setObjectName(u"settings_checkbox_system_enable_network_logging")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_enable_network_logging, 6, 0, 1, 1)

        self.settings_button_help_system_supress_errors = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_help_system_supress_errors.setObjectName(u"settings_button_help_system_supress_errors")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_help_system_supress_errors, 5, 1, 1, 1)

        self.settings_checkbox_system_supress_errors = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_supress_errors.setObjectName(u"settings_checkbox_system_supress_errors")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_supress_errors, 5, 0, 1, 1)

        self.settings_checkbox_system_internet_checks = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_internet_checks.setObjectName(u"settings_checkbox_system_internet_checks")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_internet_checks, 1, 2, 1, 1)

        self.settings_checkbox_system_activate_proxy = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_activate_proxy.setObjectName(u"settings_checkbox_system_activate_proxy")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_activate_proxy, 2, 2, 1, 1)

        self.settings_checkbox_system_update_checks = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_update_checks.setObjectName(u"settings_checkbox_system_update_checks")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_update_checks, 1, 1, 1, 1)

        self.settings_button_help_system_enable_network_logging = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_help_system_enable_network_logging.setObjectName(u"settings_button_help_system_enable_network_logging")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_help_system_enable_network_logging, 6, 1, 1, 1)

        self.settings_button_system_install_pornfetch = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_system_install_pornfetch.setObjectName(u"settings_button_system_install_pornfetch")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_system_install_pornfetch, 0, 0, 1, 3)

        self.settings_label_system_startup = QLabel(self.settings_groupbox_system_pornfetch)
        self.settings_label_system_startup.setObjectName(u"settings_label_system_startup")
        sizePolicy19 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy19.setHorizontalStretch(0)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.settings_label_system_startup.sizePolicy().hasHeightForWidth())
        self.settings_label_system_startup.setSizePolicy(sizePolicy19)

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_label_system_startup, 1, 0, 1, 1)

        self.settings_label_system_privacy = QLabel(self.settings_groupbox_system_pornfetch)
        self.settings_label_system_privacy.setObjectName(u"settings_label_system_privacy")
        sizePolicy19.setHeightForWidth(self.settings_label_system_privacy.sizePolicy().hasHeightForWidth())
        self.settings_label_system_privacy.setSizePolicy(sizePolicy19)

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_label_system_privacy, 2, 0, 1, 1)

        self.settings_checkbox_system_proxy_kill_switch = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_proxy_kill_switch.setObjectName(u"settings_checkbox_system_proxy_kill_switch")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_proxy_kill_switch, 3, 2, 1, 1)

        self.settings_button_help_system_anonymous_mode = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_help_system_anonymous_mode.setObjectName(u"settings_button_help_system_anonymous_mode")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_help_system_anonymous_mode, 3, 0, 1, 1)

        self.settings_button_help_system_proxy_kill_switch = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_help_system_proxy_kill_switch.setObjectName(u"settings_button_help_system_proxy_kill_switch")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_help_system_proxy_kill_switch, 3, 1, 1, 1)


        self.gridLayout_11.addLayout(self.settings_gridlayout_system_pornfetch, 2, 0, 1, 1)


        self.settings_scrollarea_gridlayout.addWidget(self.settings_groupbox_system_pornfetch, 3, 0, 1, 1)

        self.settings_groupbox_performance = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_performance.setObjectName(u"settings_groupbox_performance")
        self.gridLayout_10 = QGridLayout(self.settings_groupbox_performance)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.settings_horizontallayout_pornhub_delay = QHBoxLayout()
        self.settings_horizontallayout_pornhub_delay.setObjectName(u"settings_horizontallayout_pornhub_delay")
        self.settings_horizontallayout_pornhub_delay.setContentsMargins(6, 3, 6, 6)
        self.settings_label_performance_network_delay = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_network_delay.setObjectName(u"settings_label_performance_network_delay")

        self.settings_horizontallayout_pornhub_delay.addWidget(self.settings_label_performance_network_delay)

        self.settings_spinbox_performance_network_delay = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_performance_network_delay.setObjectName(u"settings_spinbox_performance_network_delay")
        self.settings_spinbox_performance_network_delay.setMinimum(0)
        self.settings_spinbox_performance_network_delay.setMaximum(5000)

        self.settings_horizontallayout_pornhub_delay.addWidget(self.settings_spinbox_performance_network_delay)

        self.settings_button_help_performance_network_delay = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_network_delay.setObjectName(u"settings_button_help_performance_network_delay")
        self.settings_button_help_performance_network_delay.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_pornhub_delay.addWidget(self.settings_button_help_performance_network_delay)


        self.gridLayout_10.addLayout(self.settings_horizontallayout_pornhub_delay, 3, 0, 1, 1)

        self.settings_horizontallayout_threading_mode = QHBoxLayout()
        self.settings_horizontallayout_threading_mode.setObjectName(u"settings_horizontallayout_threading_mode")
        self.settings_horizontallayout_threading_mode.setContentsMargins(6, 3, 6, 6)
        self.settings_label_performance_download_mode = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_download_mode.setObjectName(u"settings_label_performance_download_mode")
        sizePolicy9.setHeightForWidth(self.settings_label_performance_download_mode.sizePolicy().hasHeightForWidth())
        self.settings_label_performance_download_mode.setSizePolicy(sizePolicy9)

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_label_performance_download_mode)

        self.settings_radio_performance_download_mode_performance = QRadioButton(self.settings_groupbox_performance)
        self.settings_radio_performance_download_mode_performance.setObjectName(u"settings_radio_performance_download_mode_performance")
        self.settings_radio_performance_download_mode_performance.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_radio_performance_download_mode_performance)

        self.settings_radio_performance_download_mode_default = QRadioButton(self.settings_groupbox_performance)
        self.settings_radio_performance_download_mode_default.setObjectName(u"settings_radio_performance_download_mode_default")
        self.settings_radio_performance_download_mode_default.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_radio_performance_download_mode_default)

        self.settings_button_help_performance_download_mode = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_download_mode.setObjectName(u"settings_button_help_performance_download_mode")
        self.settings_button_help_performance_download_mode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_button_help_performance_download_mode)


        self.gridLayout_10.addLayout(self.settings_horizontallayout_threading_mode, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.settings_label_performance_speed_limit = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_speed_limit.setObjectName(u"settings_label_performance_speed_limit")

        self.horizontalLayout.addWidget(self.settings_label_performance_speed_limit)

        self.settings_doublespinbox_performance_speed_limit = QDoubleSpinBox(self.settings_groupbox_performance)
        self.settings_doublespinbox_performance_speed_limit.setObjectName(u"settings_doublespinbox_performance_speed_limit")

        self.horizontalLayout.addWidget(self.settings_doublespinbox_performance_speed_limit)

        self.settings_button_help_performance_speed_limit = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_speed_limit.setObjectName(u"settings_button_help_performance_speed_limit")

        self.horizontalLayout.addWidget(self.settings_button_help_performance_speed_limit)


        self.gridLayout_10.addLayout(self.horizontalLayout, 7, 0, 1, 1)

        self.settings_horizontallayout_maximal_timeout = QHBoxLayout()
        self.settings_horizontallayout_maximal_timeout.setObjectName(u"settings_horizontallayout_maximal_timeout")
        self.settings_horizontallayout_maximal_timeout.setContentsMargins(6, 3, 6, 6)
        self.settings_label_performance_maximal_timeout = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_maximal_timeout.setObjectName(u"settings_label_performance_maximal_timeout")

        self.settings_horizontallayout_maximal_timeout.addWidget(self.settings_label_performance_maximal_timeout)

        self.settings_spinbox_performance_maximal_timeout = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_performance_maximal_timeout.setObjectName(u"settings_spinbox_performance_maximal_timeout")
        self.settings_spinbox_performance_maximal_timeout.setMinimum(5)
        self.settings_spinbox_performance_maximal_timeout.setMaximum(5000)

        self.settings_horizontallayout_maximal_timeout.addWidget(self.settings_spinbox_performance_maximal_timeout)

        self.settings_button_help_performance_maximal_timeout = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_maximal_timeout.setObjectName(u"settings_button_help_performance_maximal_timeout")
        self.settings_button_help_performance_maximal_timeout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_button_help_performance_maximal_timeout.setStyleSheet(u"")

        self.settings_horizontallayout_maximal_timeout.addWidget(self.settings_button_help_performance_maximal_timeout)


        self.gridLayout_10.addLayout(self.settings_horizontallayout_maximal_timeout, 5, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.settings_label_performance_processing_delay = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_processing_delay.setObjectName(u"settings_label_performance_processing_delay")

        self.horizontalLayout_2.addWidget(self.settings_label_performance_processing_delay)

        self.settings_spinbox_performance_processing_delay = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_performance_processing_delay.setObjectName(u"settings_spinbox_performance_processing_delay")
        self.settings_spinbox_performance_processing_delay.setMinimum(0)
        self.settings_spinbox_performance_processing_delay.setMaximum(500)
        self.settings_spinbox_performance_processing_delay.setValue(0)

        self.horizontalLayout_2.addWidget(self.settings_spinbox_performance_processing_delay)

        self.settings_button_help_performance_processing_delay = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_processing_delay.setObjectName(u"settings_button_help_performance_processing_delay")
        self.settings_button_help_performance_processing_delay.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.settings_button_help_performance_processing_delay)


        self.gridLayout_10.addLayout(self.horizontalLayout_2, 8, 0, 1, 1)

        self.settings_horizontallayout_simultaneous_downloads = QHBoxLayout()
        self.settings_horizontallayout_simultaneous_downloads.setObjectName(u"settings_horizontallayout_simultaneous_downloads")
        self.settings_label_performance_simultaneous_download = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_simultaneous_download.setObjectName(u"settings_label_performance_simultaneous_download")

        self.settings_horizontallayout_simultaneous_downloads.addWidget(self.settings_label_performance_simultaneous_download)

        self.settings_spinbox_performance_simultaneous_downloads = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_performance_simultaneous_downloads.setObjectName(u"settings_spinbox_performance_simultaneous_downloads")
        self.settings_spinbox_performance_simultaneous_downloads.setMinimum(1)
        self.settings_spinbox_performance_simultaneous_downloads.setMaximum(5000)

        self.settings_horizontallayout_simultaneous_downloads.addWidget(self.settings_spinbox_performance_simultaneous_downloads)

        self.settings_button_help_performance_simultaneous_downloads = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_simultaneous_downloads.setObjectName(u"settings_button_help_performance_simultaneous_downloads")
        self.settings_button_help_performance_simultaneous_downloads.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_simultaneous_downloads.addWidget(self.settings_button_help_performance_simultaneous_downloads)


        self.gridLayout_10.addLayout(self.settings_horizontallayout_simultaneous_downloads, 2, 0, 1, 1)

        self.settings_horizontallayout_maximal_retries = QHBoxLayout()
        self.settings_horizontallayout_maximal_retries.setObjectName(u"settings_horizontallayout_maximal_retries")
        self.settings_horizontallayout_maximal_retries.setContentsMargins(6, 3, 6, 6)
        self.settings_label_performance_maximal_retries = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_maximal_retries.setObjectName(u"settings_label_performance_maximal_retries")

        self.settings_horizontallayout_maximal_retries.addWidget(self.settings_label_performance_maximal_retries)

        self.settings_spinbox_performance_maximal_retries = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_performance_maximal_retries.setObjectName(u"settings_spinbox_performance_maximal_retries")
        self.settings_spinbox_performance_maximal_retries.setMinimum(5)
        self.settings_spinbox_performance_maximal_retries.setMaximum(5000)

        self.settings_horizontallayout_maximal_retries.addWidget(self.settings_spinbox_performance_maximal_retries)

        self.settings_button_help_performance_maximal_retries = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_maximal_retries.setObjectName(u"settings_button_help_performance_maximal_retries")
        self.settings_button_help_performance_maximal_retries.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_maximal_retries.addWidget(self.settings_button_help_performance_maximal_retries)


        self.gridLayout_10.addLayout(self.settings_horizontallayout_maximal_retries, 6, 0, 1, 1)

        self.settings_horizontallayout_maximal_workers = QHBoxLayout()
        self.settings_horizontallayout_maximal_workers.setObjectName(u"settings_horizontallayout_maximal_workers")
        self.settings_horizontallayout_maximal_workers.setContentsMargins(6, 3, 6, 6)
        self.settings_label_performance_maximal_workers = QLabel(self.settings_groupbox_performance)
        self.settings_label_performance_maximal_workers.setObjectName(u"settings_label_performance_maximal_workers")

        self.settings_horizontallayout_maximal_workers.addWidget(self.settings_label_performance_maximal_workers)

        self.settings_spinbox_performance_maximal_workers = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_performance_maximal_workers.setObjectName(u"settings_spinbox_performance_maximal_workers")
        self.settings_spinbox_performance_maximal_workers.setMinimum(1)
        self.settings_spinbox_performance_maximal_workers.setMaximum(5000)

        self.settings_horizontallayout_maximal_workers.addWidget(self.settings_spinbox_performance_maximal_workers)

        self.settings_button_help_performance_maximal_workers = QPushButton(self.settings_groupbox_performance)
        self.settings_button_help_performance_maximal_workers.setObjectName(u"settings_button_help_performance_maximal_workers")
        self.settings_button_help_performance_maximal_workers.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_maximal_workers.addWidget(self.settings_button_help_performance_maximal_workers)


        self.gridLayout_10.addLayout(self.settings_horizontallayout_maximal_workers, 4, 0, 1, 1)


        self.settings_scrollarea_gridlayout.addWidget(self.settings_groupbox_performance, 0, 0, 1, 1)


        self.gridLayout_19.addLayout(self.settings_scrollarea_gridlayout, 0, 0, 1, 2)

        self.settings_scrollarea.setWidget(self.settings_scrollarea_widget_contents)

        self.gridLayout_7.addWidget(self.settings_scrollarea, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_settings)
        self.page_credits = QWidget()
        self.page_credits.setObjectName(u"page_credits")
        self.gridLayout_22 = QGridLayout(self.page_credits)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.scrollArea_2 = QScrollArea(self.page_credits)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 98, 70))
        self.gridLayout_21 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_21.setSpacing(0)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.main_textbrowser_credits = QTextBrowser(self.scrollAreaWidgetContents_3)
        self.main_textbrowser_credits.setObjectName(u"main_textbrowser_credits")

        self.gridLayout_21.addWidget(self.main_textbrowser_credits, 0, 0, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout_22.addWidget(self.scrollArea_2, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_credits)
        self.page_license = QWidget()
        self.page_license.setObjectName(u"page_license")
        self.gridLayout_24 = QGridLayout(self.page_license)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.scrollArea_3 = QScrollArea(self.page_license)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 226, 112))
        self.gridLayout_23 = QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_23.setSpacing(0)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setContentsMargins(0, 0, 0, 0)
        self.button_accept = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_accept.setObjectName(u"button_accept")
        self.button_accept.setStyleSheet(u"QPushButton {\n"
"    background-color: #28a745; /* Green */\n"
"    color: white;\n"
"    border: 2px solid #1e7e34;\n"
"    border-radius: 5px;\n"
"    padding: 8px 16px;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #218838; /* Darker green for hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1e7e34; /* Even darker green for active press */\n"
"}\n"
"")

        self.gridLayout_23.addWidget(self.button_accept, 1, 0, 1, 1)

        self.button_deny = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_deny.setObjectName(u"button_deny")
        self.button_deny.setStyleSheet(u"QPushButton {\n"
"    background-color: #dc3545; /* Red */\n"
"    color: white;\n"
"    border: 2px solid #c82333;\n"
"    border-radius: 5px;\n"
"    padding: 8px 16px;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #c82333; /* Darker red for hover */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #bd2130; /* Even darker red for active press */\n"
"}\n"
"")

        self.gridLayout_23.addWidget(self.button_deny, 1, 1, 1, 1)

        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents_4)
        self.textBrowser.setObjectName(u"textBrowser")
        font2 = QFont()
        font2.setFamilies([u"JetBrainsMono Nerd Font Propo"])
        font2.setPointSize(11)
        font2.setKerning(True)
        self.textBrowser.setFont(font2)
        self.textBrowser.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)
        self.textBrowser.setOpenExternalLinks(True)

        self.gridLayout_23.addWidget(self.textBrowser, 0, 0, 1, 2)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_4)

        self.gridLayout_24.addWidget(self.scrollArea_3, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_license)
        self.page_range_selector = QWidget()
        self.page_range_selector.setObjectName(u"page_range_selector")
        self.gridLayout_53 = QGridLayout(self.page_range_selector)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.scrollArea_4 = QScrollArea(self.page_range_selector)
        self.scrollArea_4.setObjectName(u"scrollArea_4")
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 318, 214))
        self.gridLayout_52 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_52.setSpacing(0)
        self.gridLayout_52.setObjectName(u"gridLayout_52")
        self.gridLayout_52.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.textbrowser_range = QTextBrowser(self.scrollAreaWidgetContents_5)
        self.textbrowser_range.setObjectName(u"textbrowser_range")

        self.gridLayout_25.addWidget(self.textbrowser_range, 0, 0, 1, 5)

        self.button_range_apply_time = QPushButton(self.scrollAreaWidgetContents_5)
        self.button_range_apply_time.setObjectName(u"button_range_apply_time")

        self.gridLayout_25.addWidget(self.button_range_apply_time, 5, 4, 1, 1)

        self.label_apply_by_time = QLabel(self.scrollAreaWidgetContents_5)
        self.label_apply_by_time.setObjectName(u"label_apply_by_time")

        self.gridLayout_25.addWidget(self.label_apply_by_time, 4, 0, 1, 4)

        self.lineedit_range_start = QLineEdit(self.scrollAreaWidgetContents_5)
        self.lineedit_range_start.setObjectName(u"lineedit_range_start")

        self.gridLayout_25.addWidget(self.lineedit_range_start, 5, 1, 1, 1)

        self.lineedit_range_author = QLineEdit(self.scrollAreaWidgetContents_5)
        self.lineedit_range_author.setObjectName(u"lineedit_range_author")

        self.gridLayout_25.addWidget(self.lineedit_range_author, 1, 1, 1, 1)

        self.spinbox_range_end = QSpinBox(self.scrollAreaWidgetContents_5)
        self.spinbox_range_end.setObjectName(u"spinbox_range_end")

        self.gridLayout_25.addWidget(self.spinbox_range_end, 9, 3, 1, 1)

        self.label_apply_by_index = QLabel(self.scrollAreaWidgetContents_5)
        self.label_apply_by_index.setObjectName(u"label_apply_by_index")

        self.gridLayout_25.addWidget(self.label_apply_by_index, 6, 0, 1, 4)

        self.label_range_end = QLabel(self.scrollAreaWidgetContents_5)
        self.label_range_end.setObjectName(u"label_range_end")

        self.gridLayout_25.addWidget(self.label_range_end, 9, 2, 1, 1)

        self.button_range_apply_index = QPushButton(self.scrollAreaWidgetContents_5)
        self.button_range_apply_index.setObjectName(u"button_range_apply_index")

        self.gridLayout_25.addWidget(self.button_range_apply_index, 9, 4, 1, 1)

        self.label_range_time_end = QLabel(self.scrollAreaWidgetContents_5)
        self.label_range_time_end.setObjectName(u"label_range_time_end")

        self.gridLayout_25.addWidget(self.label_range_time_end, 5, 2, 1, 1)

        self.label_range_start = QLabel(self.scrollAreaWidgetContents_5)
        self.label_range_start.setObjectName(u"label_range_start")

        self.gridLayout_25.addWidget(self.label_range_start, 9, 0, 1, 1)

        self.button_range_apply_author = QPushButton(self.scrollAreaWidgetContents_5)
        self.button_range_apply_author.setObjectName(u"button_range_apply_author")

        self.gridLayout_25.addWidget(self.button_range_apply_author, 1, 2, 1, 3)

        self.spinbox_range_start = QSpinBox(self.scrollAreaWidgetContents_5)
        self.spinbox_range_start.setObjectName(u"spinbox_range_start")

        self.gridLayout_25.addWidget(self.spinbox_range_start, 9, 1, 1, 1)

        self.lineedit_range_end = QLineEdit(self.scrollAreaWidgetContents_5)
        self.lineedit_range_end.setObjectName(u"lineedit_range_end")

        self.gridLayout_25.addWidget(self.lineedit_range_end, 5, 3, 1, 1)

        self.label_range_time_start = QLabel(self.scrollAreaWidgetContents_5)
        self.label_range_time_start.setObjectName(u"label_range_time_start")

        self.gridLayout_25.addWidget(self.label_range_time_start, 5, 0, 1, 1)

        self.label_range_by_author = QLabel(self.scrollAreaWidgetContents_5)
        self.label_range_by_author.setObjectName(u"label_range_by_author")

        self.gridLayout_25.addWidget(self.label_range_by_author, 1, 0, 1, 1)


        self.gridLayout_52.addLayout(self.gridLayout_25, 0, 0, 1, 1)

        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_5)

        self.gridLayout_53.addWidget(self.scrollArea_4, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_range_selector)
        self.page_keyboard_shortcuts = QWidget()
        self.page_keyboard_shortcuts.setObjectName(u"page_keyboard_shortcuts")
        self.gridLayout_55 = QGridLayout(self.page_keyboard_shortcuts)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.scrollArea_9 = QScrollArea(self.page_keyboard_shortcuts)
        self.scrollArea_9.setObjectName(u"scrollArea_9")
        self.scrollArea_9.setWidgetResizable(True)
        self.scrollAreaWidgetContents_11 = QWidget()
        self.scrollAreaWidgetContents_11.setObjectName(u"scrollAreaWidgetContents_11")
        self.scrollAreaWidgetContents_11.setGeometry(QRect(0, 0, 256, 192))
        self.gridLayout_54 = QGridLayout(self.scrollAreaWidgetContents_11)
        self.gridLayout_54.setSpacing(0)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.gridLayout_54.setContentsMargins(0, 0, 0, 0)
        self.text_browser_keyboard_shortcuts = QTextBrowser(self.scrollAreaWidgetContents_11)
        self.text_browser_keyboard_shortcuts.setObjectName(u"text_browser_keyboard_shortcuts")
        sizePolicy18.setHeightForWidth(self.text_browser_keyboard_shortcuts.sizePolicy().hasHeightForWidth())
        self.text_browser_keyboard_shortcuts.setSizePolicy(sizePolicy18)
        self.text_browser_keyboard_shortcuts.setMaximumSize(QSize(200000, 200000))

        self.gridLayout_54.addWidget(self.text_browser_keyboard_shortcuts, 0, 0, 1, 1)

        self.scrollArea_9.setWidget(self.scrollAreaWidgetContents_11)

        self.gridLayout_55.addWidget(self.scrollArea_9, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_keyboard_shortcuts)
        self.page_update_available = QWidget()
        self.page_update_available.setObjectName(u"page_update_available")
        self.gridLayout_28 = QGridLayout(self.page_update_available)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_27 = QGridLayout()
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.text_browser_update_available = QTextBrowser(self.page_update_available)
        self.text_browser_update_available.setObjectName(u"text_browser_update_available")

        self.gridLayout_27.addWidget(self.text_browser_update_available, 0, 0, 1, 1)

        self.button_update_acknowledged = QPushButton(self.page_update_available)
        self.button_update_acknowledged.setObjectName(u"button_update_acknowledged")

        self.gridLayout_27.addWidget(self.button_update_acknowledged, 1, 0, 1, 1)


        self.gridLayout_28.addLayout(self.gridLayout_27, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_update_available)
        self.page_install_dialog = QWidget()
        self.page_install_dialog.setObjectName(u"page_install_dialog")
        self.gridLayout_57 = QGridLayout(self.page_install_dialog)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.scrollArea_10 = QScrollArea(self.page_install_dialog)
        self.scrollArea_10.setObjectName(u"scrollArea_10")
        self.scrollArea_10.setWidgetResizable(True)
        self.scrollAreaWidgetContents_12 = QWidget()
        self.scrollAreaWidgetContents_12.setObjectName(u"scrollAreaWidgetContents_12")
        self.scrollAreaWidgetContents_12.setGeometry(QRect(0, 0, 170, 138))
        self.gridLayout_56 = QGridLayout(self.scrollAreaWidgetContents_12)
        self.gridLayout_56.setSpacing(0)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.gridLayout_56.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser_3 = QTextBrowser(self.scrollAreaWidgetContents_12)
        self.textBrowser_3.setObjectName(u"textBrowser_3")

        self.verticalLayout.addWidget(self.textBrowser_3)

        self.horizontallayout_app_name = QHBoxLayout()
        self.horizontallayout_app_name.setObjectName(u"horizontallayout_app_name")
        self.label_custom_app_name = QLabel(self.scrollAreaWidgetContents_12)
        self.label_custom_app_name.setObjectName(u"label_custom_app_name")

        self.horizontallayout_app_name.addWidget(self.label_custom_app_name)

        self.lineedit_custom_app_name = QLineEdit(self.scrollAreaWidgetContents_12)
        self.lineedit_custom_app_name.setObjectName(u"lineedit_custom_app_name")

        self.horizontallayout_app_name.addWidget(self.lineedit_custom_app_name)


        self.verticalLayout.addLayout(self.horizontallayout_app_name)

        self.horizontallayout_buttons = QHBoxLayout()
        self.horizontallayout_buttons.setObjectName(u"horizontallayout_buttons")
        self.button_install = QPushButton(self.scrollAreaWidgetContents_12)
        self.button_install.setObjectName(u"button_install")

        self.horizontallayout_buttons.addWidget(self.button_install)

        self.button_portable = QPushButton(self.scrollAreaWidgetContents_12)
        self.button_portable.setObjectName(u"button_portable")

        self.horizontallayout_buttons.addWidget(self.button_portable)


        self.verticalLayout.addLayout(self.horizontallayout_buttons)


        self.gridLayout_56.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.scrollArea_10.setWidget(self.scrollAreaWidgetContents_12)

        self.gridLayout_57.addWidget(self.scrollArea_10, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_install_dialog)
        self.page_supported_websites = QWidget()
        self.page_supported_websites.setObjectName(u"page_supported_websites")
        self.gridLayout_18 = QGridLayout(self.page_supported_websites)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.scrollArea = QScrollArea(self.page_supported_websites)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 98, 70))
        self.gridLayout_20 = QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_20.setSpacing(0)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.main_textbrowser_supported_websites = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.main_textbrowser_supported_websites.setObjectName(u"main_textbrowser_supported_websites")
        self.main_textbrowser_supported_websites.setOpenExternalLinks(True)

        self.gridLayout_20.addWidget(self.main_textbrowser_supported_websites, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.gridLayout_18.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_supported_websites)
        self.page_donation_nag = QWidget()
        self.page_donation_nag.setObjectName(u"page_donation_nag")
        self.gridLayout_60 = QGridLayout(self.page_donation_nag)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.scrollArea_11 = QScrollArea(self.page_donation_nag)
        self.scrollArea_11.setObjectName(u"scrollArea_11")
        self.scrollArea_11.setWidgetResizable(True)
        self.scrollAreaWidgetContents_13 = QWidget()
        self.scrollAreaWidgetContents_13.setObjectName(u"scrollAreaWidgetContents_13")
        self.scrollAreaWidgetContents_13.setGeometry(QRect(0, 0, 455, 101))
        self.gridLayout_59 = QGridLayout(self.scrollAreaWidgetContents_13)
        self.gridLayout_59.setObjectName(u"gridLayout_59")
        self.gridLayout_59.setHorizontalSpacing(0)
        self.gridLayout_59.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_58 = QGridLayout()
        self.gridLayout_58.setObjectName(u"gridLayout_58")
        self.button_donate_kofi = QPushButton(self.scrollAreaWidgetContents_13)
        self.button_donate_kofi.setObjectName(u"button_donate_kofi")
        self.button_donate_kofi.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_58.addWidget(self.button_donate_kofi, 1, 1, 1, 1)

        self.button_donate_already_donated = QPushButton(self.scrollAreaWidgetContents_13)
        self.button_donate_already_donated.setObjectName(u"button_donate_already_donated")
        self.button_donate_already_donated.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_58.addWidget(self.button_donate_already_donated, 1, 3, 1, 1)

        self.button_donate_paypal = QPushButton(self.scrollAreaWidgetContents_13)
        self.button_donate_paypal.setObjectName(u"button_donate_paypal")
        self.button_donate_paypal.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_58.addWidget(self.button_donate_paypal, 1, 0, 1, 1)

        self.button_donate_copy_xmr = QPushButton(self.scrollAreaWidgetContents_13)
        self.button_donate_copy_xmr.setObjectName(u"button_donate_copy_xmr")
        self.button_donate_copy_xmr.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_58.addWidget(self.button_donate_copy_xmr, 1, 2, 1, 1)

        self.button_donate_close = QPushButton(self.scrollAreaWidgetContents_13)
        self.button_donate_close.setObjectName(u"button_donate_close")
        self.button_donate_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_58.addWidget(self.button_donate_close, 1, 4, 1, 1)

        self.textBrowser_4 = QTextBrowser(self.scrollAreaWidgetContents_13)
        self.textBrowser_4.setObjectName(u"textBrowser_4")
        self.textBrowser_4.setStyleSheet(u"border-radius: 15px;")
        self.textBrowser_4.setOpenExternalLinks(True)

        self.gridLayout_58.addWidget(self.textBrowser_4, 0, 0, 1, 5)


        self.gridLayout_59.addLayout(self.gridLayout_58, 0, 0, 1, 1)

        self.scrollArea_11.setWidget(self.scrollAreaWidgetContents_13)

        self.gridLayout_60.addWidget(self.scrollArea_11, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_donation_nag)
        self.page_disclaimer = QWidget()
        self.page_disclaimer.setObjectName(u"page_disclaimer")
        self.gridLayout_62 = QGridLayout(self.page_disclaimer)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.scrollArea_12 = QScrollArea(self.page_disclaimer)
        self.scrollArea_12.setObjectName(u"scrollArea_12")
        self.scrollArea_12.setWidgetResizable(True)
        self.scrollAreaWidgetContents_14 = QWidget()
        self.scrollAreaWidgetContents_14.setObjectName(u"scrollAreaWidgetContents_14")
        self.scrollAreaWidgetContents_14.setGeometry(QRect(0, 0, 98, 119))
        self.gridLayout_61 = QGridLayout(self.scrollAreaWidgetContents_14)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.textBrowser_5 = QTextBrowser(self.scrollAreaWidgetContents_14)
        self.textBrowser_5.setObjectName(u"textBrowser_5")

        self.gridLayout_61.addWidget(self.textBrowser_5, 0, 0, 1, 1)

        self.button_disclaimer_accept = QPushButton(self.scrollAreaWidgetContents_14)
        self.button_disclaimer_accept.setObjectName(u"button_disclaimer_accept")

        self.gridLayout_61.addWidget(self.button_disclaimer_accept, 1, 0, 1, 1)

        self.scrollArea_12.setWidget(self.scrollAreaWidgetContents_14)

        self.gridLayout_62.addWidget(self.scrollArea_12, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_disclaimer)
        self.page_privacy_information = QWidget()
        self.page_privacy_information.setObjectName(u"page_privacy_information")
        self.gridLayout_30 = QGridLayout(self.page_privacy_information)
        self.gridLayout_30.setSpacing(0)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_29 = QGridLayout()
        self.gridLayout_29.setSpacing(0)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.textBrowser_2 = QTextBrowser(self.page_privacy_information)
        self.textBrowser_2.setObjectName(u"textBrowser_2")
        self.textBrowser_2.setLineWidth(1)
        self.textBrowser_2.setOpenExternalLinks(True)

        self.gridLayout_29.addWidget(self.textBrowser_2, 0, 0, 1, 2)

        self.button_server_enable_logging = QPushButton(self.page_privacy_information)
        self.button_server_enable_logging.setObjectName(u"button_server_enable_logging")

        self.gridLayout_29.addWidget(self.button_server_enable_logging, 1, 0, 1, 1)

        self.button_server_disable_logging = QPushButton(self.page_privacy_information)
        self.button_server_disable_logging.setObjectName(u"button_server_disable_logging")

        self.gridLayout_29.addWidget(self.button_server_disable_logging, 1, 1, 1, 1)


        self.gridLayout_30.addLayout(self.gridLayout_29, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_privacy_information)

        self.gridLayout_26.addWidget(self.CentralStackedWidget, 1, 0, 1, 1)

        self.formlayout_progressbar = QFormLayout()
        self.formlayout_progressbar.setObjectName(u"formlayout_progressbar")
        self.formlayout_progressbar.setHorizontalSpacing(0)
        self.formlayout_progressbar.setVerticalSpacing(0)
        self.main_label_progressbar_total = QLabel(self.centralwidget)
        self.main_label_progressbar_total.setObjectName(u"main_label_progressbar_total")

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_total)

        self.main_progressbar_total = QProgressBar(self.centralwidget)
        self.main_progressbar_total.setObjectName(u"main_progressbar_total")
        sizePolicy10.setHeightForWidth(self.main_progressbar_total.sizePolicy().hasHeightForWidth())
        self.main_progressbar_total.setSizePolicy(sizePolicy10)
        self.main_progressbar_total.setMinimumSize(QSize(300, 0))
        self.main_progressbar_total.setStyleSheet(u"text-align: center; /* Centered text */")
        self.main_progressbar_total.setValue(0)

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.FieldRole, self.main_progressbar_total)

        self.main_label_progressbar_converting = QLabel(self.centralwidget)
        self.main_label_progressbar_converting.setObjectName(u"main_label_progressbar_converting")

        self.formlayout_progressbar.setWidget(1, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_converting)

        self.main_progressbar_converting = QProgressBar(self.centralwidget)
        self.main_progressbar_converting.setObjectName(u"main_progressbar_converting")
        self.main_progressbar_converting.setStyleSheet(u"text-align: center; /* Centered text */")
        self.main_progressbar_converting.setValue(0)

        self.formlayout_progressbar.setWidget(1, QFormLayout.ItemRole.FieldRole, self.main_progressbar_converting)


        self.gridLayout_26.addLayout(self.formlayout_progressbar, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.main_button_switch_home, self.main_button_switch_account)
        QWidget.setTabOrder(self.main_button_switch_account, self.main_button_switch_tools)
        QWidget.setTabOrder(self.main_button_switch_tools, self.main_button_switch_settings)
        QWidget.setTabOrder(self.main_button_switch_settings, self.main_button_switch_credits)
        QWidget.setTabOrder(self.main_button_switch_credits, self.main_button_view_progress_bars)
        QWidget.setTabOrder(self.main_button_view_progress_bars, self.main_button_switch_supported_websites)
        QWidget.setTabOrder(self.main_button_switch_supported_websites, self.scroll_area_top_stacked)
        QWidget.setTabOrder(self.scroll_area_top_stacked, self.download_lineedit_url)
        QWidget.setTabOrder(self.download_lineedit_url, self.download_button_download)
        QWidget.setTabOrder(self.download_button_download, self.download_lineedit_playlist_url)
        QWidget.setTabOrder(self.download_lineedit_playlist_url, self.download_button_playlist_get_videos)
        QWidget.setTabOrder(self.download_button_playlist_get_videos, self.download_lineedit_model_url)
        QWidget.setTabOrder(self.download_lineedit_model_url, self.download_button_model)
        QWidget.setTabOrder(self.download_button_model, self.download_lineedit_file)
        QWidget.setTabOrder(self.download_lineedit_file, self.download_button_help_file)
        QWidget.setTabOrder(self.download_button_help_file, self.download_button_open_file)
        QWidget.setTabOrder(self.download_button_open_file, self.download_lineedit_search_query)
        QWidget.setTabOrder(self.download_lineedit_search_query, self.button_search)
        QWidget.setTabOrder(self.button_search, self.download_radio_search_website_pornhub)
        QWidget.setTabOrder(self.download_radio_search_website_pornhub, self.download_radio_search_website_hqporner)
        QWidget.setTabOrder(self.download_radio_search_website_hqporner, self.download_radio_search_website_xvideos)
        QWidget.setTabOrder(self.download_radio_search_website_xvideos, self.download_radio_search_website_eporner)
        QWidget.setTabOrder(self.download_radio_search_website_eporner, self.download_radio_search_website_xnxx)
        QWidget.setTabOrder(self.download_radio_search_website_xnxx, self.login_button_get_recommended_videos)
        QWidget.setTabOrder(self.login_button_get_recommended_videos, self.login_button_login)
        QWidget.setTabOrder(self.login_button_login, self.tools_button_list_categories_eporner)
        QWidget.setTabOrder(self.tools_button_list_categories_eporner, self.main_checkbox_tree_show_videos_reversed)
        QWidget.setTabOrder(self.main_checkbox_tree_show_videos_reversed, self.main_checkbox_tree_do_not_clear_videos)
        QWidget.setTabOrder(self.main_checkbox_tree_do_not_clear_videos, self.main_button_tree_automated_selection)
        QWidget.setTabOrder(self.main_button_tree_automated_selection, self.main_button_tree_keyboard_shortcuts)
        QWidget.setTabOrder(self.main_button_tree_keyboard_shortcuts, self.main_button_tree_stop)
        QWidget.setTabOrder(self.main_button_tree_stop, self.graphicsView)
        QWidget.setTabOrder(self.graphicsView, self.main_button_tree_download)
        QWidget.setTabOrder(self.main_button_tree_download, self.login_lineedit_username)
        QWidget.setTabOrder(self.login_lineedit_username, self.login_lineedit_password)
        QWidget.setTabOrder(self.login_lineedit_password, self.login_button_get_liked_videos)
        QWidget.setTabOrder(self.login_button_get_liked_videos, self.login_button_get_watched_videos)
        QWidget.setTabOrder(self.login_button_get_watched_videos, self.progress_lineedit_download_info)
        QWidget.setTabOrder(self.progress_lineedit_download_info, self.tools_radio_top_porn_week)
        QWidget.setTabOrder(self.tools_radio_top_porn_week, self.tools_radio_top_porn_month)
        QWidget.setTabOrder(self.tools_radio_top_porn_month, self.tools_radio_top_porn_all_time)
        QWidget.setTabOrder(self.tools_radio_top_porn_all_time, self.tools_button_top_porn_get_videos)
        QWidget.setTabOrder(self.tools_button_top_porn_get_videos, self.tools_lineedit_hqporner_category)
        QWidget.setTabOrder(self.tools_lineedit_hqporner_category, self.tools_button_hqporner_category_get_videos)
        QWidget.setTabOrder(self.tools_button_hqporner_category_get_videos, self.tools_button_list_categories)
        QWidget.setTabOrder(self.tools_button_list_categories, self.tools_button_get_random_videos)
        QWidget.setTabOrder(self.tools_button_get_random_videos, self.tools_button_get_brazzers_videos)
        QWidget.setTabOrder(self.tools_button_get_brazzers_videos, self.main_scrollarea_treewidget)
        QWidget.setTabOrder(self.main_scrollarea_treewidget, self.tools_lineedit_videos_by_category_eporner)
        QWidget.setTabOrder(self.tools_lineedit_videos_by_category_eporner, self.treeWidget)
        QWidget.setTabOrder(self.treeWidget, self.tools_button_eporner_category_get_videos)
        QWidget.setTabOrder(self.tools_button_eporner_category_get_videos, self.scrollArea_2)
        QWidget.setTabOrder(self.scrollArea_2, self.button_install)
        QWidget.setTabOrder(self.button_install, self.lineedit_custom_app_name)
        QWidget.setTabOrder(self.lineedit_custom_app_name, self.button_portable)
        QWidget.setTabOrder(self.button_portable, self.scrollArea_10)
        QWidget.setTabOrder(self.scrollArea_10, self.scrollArea_9)
        QWidget.setTabOrder(self.scrollArea_9, self.button_accept)
        QWidget.setTabOrder(self.button_accept, self.button_deny)
        QWidget.setTabOrder(self.button_deny, self.scrollArea_3)
        QWidget.setTabOrder(self.scrollArea_3, self.scrollArea_4)
        QWidget.setTabOrder(self.scrollArea_4, self.lineedit_range_author)
        QWidget.setTabOrder(self.lineedit_range_author, self.button_range_apply_author)
        QWidget.setTabOrder(self.button_range_apply_author, self.lineedit_range_start)
        QWidget.setTabOrder(self.lineedit_range_start, self.lineedit_range_end)
        QWidget.setTabOrder(self.lineedit_range_end, self.button_range_apply_time)
        QWidget.setTabOrder(self.button_range_apply_time, self.spinbox_range_start)
        QWidget.setTabOrder(self.spinbox_range_start, self.spinbox_range_end)
        QWidget.setTabOrder(self.spinbox_range_end, self.button_range_apply_index)
        QWidget.setTabOrder(self.button_range_apply_index, self.settings_radio_performance_download_mode_performance)
        QWidget.setTabOrder(self.settings_radio_performance_download_mode_performance, self.settings_radio_performance_download_mode_default)
        QWidget.setTabOrder(self.settings_radio_performance_download_mode_default, self.settings_button_help_performance_download_mode)
        QWidget.setTabOrder(self.settings_button_help_performance_download_mode, self.settings_spinbox_performance_simultaneous_downloads)
        QWidget.setTabOrder(self.settings_spinbox_performance_simultaneous_downloads, self.settings_button_help_performance_simultaneous_downloads)
        QWidget.setTabOrder(self.settings_button_help_performance_simultaneous_downloads, self.settings_spinbox_performance_network_delay)
        QWidget.setTabOrder(self.settings_spinbox_performance_network_delay, self.settings_button_help_performance_network_delay)
        QWidget.setTabOrder(self.settings_button_help_performance_network_delay, self.settings_spinbox_performance_maximal_workers)
        QWidget.setTabOrder(self.settings_spinbox_performance_maximal_workers, self.settings_button_help_performance_maximal_workers)
        QWidget.setTabOrder(self.settings_button_help_performance_maximal_workers, self.settings_spinbox_performance_maximal_timeout)
        QWidget.setTabOrder(self.settings_spinbox_performance_maximal_timeout, self.settings_spinbox_performance_maximal_retries)
        QWidget.setTabOrder(self.settings_spinbox_performance_maximal_retries, self.settings_button_help_performance_maximal_retries)
        QWidget.setTabOrder(self.settings_button_help_performance_maximal_retries, self.settings_button_help_performance_maximal_timeout)
        QWidget.setTabOrder(self.settings_button_help_performance_maximal_timeout, self.settings_doublespinbox_performance_speed_limit)
        QWidget.setTabOrder(self.settings_doublespinbox_performance_speed_limit, self.settings_button_help_performance_speed_limit)
        QWidget.setTabOrder(self.settings_button_help_performance_speed_limit, self.settings_radio_videos_quality_best)
        QWidget.setTabOrder(self.settings_radio_videos_quality_best, self.settings_radio_videos_quality_half)
        QWidget.setTabOrder(self.settings_radio_videos_quality_half, self.settings_radio_videos_quality_worst)
        QWidget.setTabOrder(self.settings_radio_videos_quality_worst, self.settings_radio_videos_model_type_user_uploads)
        QWidget.setTabOrder(self.settings_radio_videos_model_type_user_uploads, self.settings_radio_videos_model_type_featured)
        QWidget.setTabOrder(self.settings_radio_videos_model_type_featured, self.settings_radio_videos_model_type_both)
        QWidget.setTabOrder(self.settings_radio_videos_model_type_both, self.settings_button_help_videos_model_videos_type)
        QWidget.setTabOrder(self.settings_button_help_videos_model_videos_type, self.settings_spinbox_videos_result_limit)
        QWidget.setTabOrder(self.settings_spinbox_videos_result_limit, self.settings_button_help_videos_result_limit)
        QWidget.setTabOrder(self.settings_button_help_videos_result_limit, self.settings_lineedit_videos_output_path)
        QWidget.setTabOrder(self.settings_lineedit_videos_output_path, self.settings_button_videos_open_output_path)
        QWidget.setTabOrder(self.settings_button_videos_open_output_path, self.settings_checkbox_videos_use_video_id_as_filename)
        QWidget.setTabOrder(self.settings_checkbox_videos_use_video_id_as_filename, self.settings_checkbox_videos_write_metadata)
        QWidget.setTabOrder(self.settings_checkbox_videos_write_metadata, self.settings_button_help_videos_write_metadata)
        QWidget.setTabOrder(self.settings_button_help_videos_write_metadata, self.settings_checkbox_videos_skip_existing_files)
        QWidget.setTabOrder(self.settings_checkbox_videos_skip_existing_files, self.settings_button_help_videos_skip_existing_files)
        QWidget.setTabOrder(self.settings_button_help_videos_skip_existing_files, self.settings_button_system_install_pornfetch)
        QWidget.setTabOrder(self.settings_button_system_install_pornfetch, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.settings_button_reset)
        QWidget.setTabOrder(self.settings_button_reset, self.settings_button_help_system_anonymous_mode)
        QWidget.setTabOrder(self.settings_button_help_system_anonymous_mode, self.main_textbrowser_credits)
        QWidget.setTabOrder(self.main_textbrowser_credits, self.settings_checkbox_system_enable_anonymous_mode)
        QWidget.setTabOrder(self.settings_checkbox_system_enable_anonymous_mode, self.settings_checkbox_ui_custom_font)
        QWidget.setTabOrder(self.settings_checkbox_ui_custom_font, self.settings_spinbox_ui_font_size)
        QWidget.setTabOrder(self.settings_spinbox_ui_font_size, self.textBrowser)
        QWidget.setTabOrder(self.textBrowser, self.settings_checkbox_system_enable_network_logging)
        QWidget.setTabOrder(self.settings_checkbox_system_enable_network_logging, self.textbrowser_range)
        QWidget.setTabOrder(self.textbrowser_range, self.settings_checkbox_system_update_checks)
        QWidget.setTabOrder(self.settings_checkbox_system_update_checks, self.settings_checkbox_system_internet_checks)
        QWidget.setTabOrder(self.settings_checkbox_system_internet_checks, self.settings_button_help_system_supress_errors)
        QWidget.setTabOrder(self.settings_button_help_system_supress_errors, self.settings_button_help_system_proxy_kill_switch)
        QWidget.setTabOrder(self.settings_button_help_system_proxy_kill_switch, self.settings_checkbox_system_proxy_kill_switch)
        QWidget.setTabOrder(self.settings_checkbox_system_proxy_kill_switch, self.settings_checkbox_system_supress_errors)
        QWidget.setTabOrder(self.settings_checkbox_system_supress_errors, self.settings_button_help_system_enable_network_logging)
        QWidget.setTabOrder(self.settings_button_help_system_enable_network_logging, self.settings_checkbox_system_activate_proxy)
        QWidget.setTabOrder(self.settings_checkbox_system_activate_proxy, self.settings_radio_ui_language_german)
        QWidget.setTabOrder(self.settings_radio_ui_language_german, self.text_browser_keyboard_shortcuts)
        QWidget.setTabOrder(self.text_browser_keyboard_shortcuts, self.text_browser_update_available)
        QWidget.setTabOrder(self.text_browser_update_available, self.button_update_acknowledged)
        QWidget.setTabOrder(self.button_update_acknowledged, self.settings_radio_ui_language_chinese_simplified)
        QWidget.setTabOrder(self.settings_radio_ui_language_chinese_simplified, self.textBrowser_3)
        QWidget.setTabOrder(self.textBrowser_3, self.settings_radio_ui_language_english)
        QWidget.setTabOrder(self.settings_radio_ui_language_english, self.settings_radio_ui_language_system_default)
        QWidget.setTabOrder(self.settings_radio_ui_language_system_default, self.settings_radio_ui_language_french)
        QWidget.setTabOrder(self.settings_radio_ui_language_french, self.settings_button_apply)
        QWidget.setTabOrder(self.settings_button_apply, self.main_textbrowser_supported_websites)
        QWidget.setTabOrder(self.main_textbrowser_supported_websites, self.scrollArea_11)
        QWidget.setTabOrder(self.scrollArea_11, self.button_donate_kofi)
        QWidget.setTabOrder(self.button_donate_kofi, self.button_donate_already_donated)
        QWidget.setTabOrder(self.button_donate_already_donated, self.button_donate_paypal)
        QWidget.setTabOrder(self.button_donate_paypal, self.button_donate_copy_xmr)
        QWidget.setTabOrder(self.button_donate_copy_xmr, self.button_donate_close)
        QWidget.setTabOrder(self.button_donate_close, self.textBrowser_4)
        QWidget.setTabOrder(self.textBrowser_4, self.scrollArea_12)
        QWidget.setTabOrder(self.scrollArea_12, self.textBrowser_5)
        QWidget.setTabOrder(self.textBrowser_5, self.button_disclaimer_accept)

        self.retranslateUi(MainWindow)

        self.CentralStackedWidget.setCurrentIndex(11)
        self.main_stacked_widget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.main_button_switch_home.setText("")
        self.main_button_switch_account.setText("")
        self.main_button_switch_tools.setText("")
        self.main_button_switch_settings.setText("")
        self.main_button_switch_credits.setText("")
        self.main_button_view_progress_bars.setText("")
        self.main_button_switch_supported_websites.setText(QCoreApplication.translate("MainWindow", u"Supported websites", None))
        self.download_radio_search_website_hqporner.setText(QCoreApplication.translate("MainWindow", u"HQPorner", None))
        self.download_button_model.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
        self.download_lineedit_model_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Model / Channel / Actress URL", None))
        self.download_lineedit_playlist_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a PornHub Playlist URL", None))
        self.button_search.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.download_label_file.setText(QCoreApplication.translate("MainWindow", u"File:", None))
        self.download_button_help_file.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.download_button_playlist_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
        self.download_lineedit_search_query.setText("")
        self.download_lineedit_search_query.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search for Videos. Select Website below", None))
        self.download_label_search_website.setText(QCoreApplication.translate("MainWindow", u"Search Website", None))
        self.download_label_playlist_url.setText(QCoreApplication.translate("MainWindow", u"Playlist URL:", None))
        self.download_label_model_url.setText(QCoreApplication.translate("MainWindow", u"Model URL:", None))
        self.download_radio_search_website_xnxx.setText(QCoreApplication.translate("MainWindow", u"XNXX", None))
        self.download_button_download.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.download_lineedit_file.setText("")
        self.download_lineedit_file.setPlaceholderText(QCoreApplication.translate("MainWindow", u"URLs in the file must be separated with new lines!", None))
        self.download_radio_search_website_xvideos.setText(QCoreApplication.translate("MainWindow", u"XVideos", None))
        self.download_label_search.setText(QCoreApplication.translate("MainWindow", u"Search Query:", None))
        self.download_lineedit_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter video URL", None))
        self.download_radio_search_website_eporner.setText(QCoreApplication.translate("MainWindow", u"EPorner", None))
        self.download_radio_search_website_pornhub.setText(QCoreApplication.translate("MainWindow", u"PornHub", None))
        self.download_label_url.setText(QCoreApplication.translate("MainWindow", u"URL:", None))
        self.download_button_open_file.setText(QCoreApplication.translate("MainWindow", u"Open File", None))
        self.login_button_get_liked_videos.setText(QCoreApplication.translate("MainWindow", u"Get Liked videos", None))
        self.login_button_get_recommended_videos.setText(QCoreApplication.translate("MainWindow", u"Get recommended videos", None))
        self.login_label_password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.login_label_username.setText(QCoreApplication.translate("MainWindow", u"E-Mail:", None))
        self.login_button_login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.login_lineedit_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your PornHub Password", None))
        self.login_lineedit_username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your PornHub E-Mail address (not your username, pornhub changed it) ", None))
        self.login_button_get_watched_videos.setText(QCoreApplication.translate("MainWindow", u"Get watched videos", None))
        self.progress_label_info.setText(QCoreApplication.translate("MainWindow", u"Info:", None))
        self.progress_lineedit_download_info.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"HQPorner", None))
        self.tools_radio_top_porn_week.setText(QCoreApplication.translate("MainWindow", u"Week", None))
        self.tools_button_hqporner_category_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
        self.tools_label_videos_by_category.setText(QCoreApplication.translate("MainWindow", u"Get videos by category", None))
        self.tools_label_get_top_porn.setText(QCoreApplication.translate("MainWindow", u"Get Top Porn:", None))
        self.tools_radio_top_porn_month.setText(QCoreApplication.translate("MainWindow", u"Month", None))
        self.tools_label_get_random_video.setText(QCoreApplication.translate("MainWindow", u"Get random video", None))
        self.tools_radio_top_porn_all_time.setText(QCoreApplication.translate("MainWindow", u"All Time", None))
        self.tools_button_list_categories.setText(QCoreApplication.translate("MainWindow", u"List of all categories", None))
        self.tools_button_get_random_videos.setText(QCoreApplication.translate("MainWindow", u"Get Video", None))
        self.tools_button_top_porn_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
        self.tools_label_get_brazzers_videos.setText(QCoreApplication.translate("MainWindow", u"Get Brazzers videos", None))
        self.tools_button_get_brazzers_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"EPorner", None))
        self.tools_button_eporner_category_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
        self.tools_button_list_categories_eporner.setText(QCoreApplication.translate("MainWindow", u"List of all categories", None))
        self.tools_label_videos_by_category_eporner.setText(QCoreApplication.translate("MainWindow", u"Get videos by category", None))
        self.main_checkbox_tree_show_videos_reversed.setText(QCoreApplication.translate("MainWindow", u"Show videos in reverse", None))
        self.main_checkbox_tree_do_not_clear_videos.setText(QCoreApplication.translate("MainWindow", u"Do not clear videos", None))
        self.main_button_tree_automated_selection.setText(QCoreApplication.translate("MainWindow", u"Automated selection tool", None))
        self.main_button_tree_keyboard_shortcuts.setText(QCoreApplication.translate("MainWindow", u"Keyboard shortcuts", None))
#if QT_CONFIG(tooltip)
        self.main_button_tree_stop.setToolTip(QCoreApplication.translate("MainWindow", u"Does not stop downloading videos", None))
#endif // QT_CONFIG(tooltip)
        self.main_button_tree_stop.setText(QCoreApplication.translate("MainWindow", u"Stop loading videos", None))
        self.main_button_tree_download.setText(QCoreApplication.translate("MainWindow", u"Download Selected Videos", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Duration (minutes)", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Author", None));
        self.settings_button_apply.setText(QCoreApplication.translate("MainWindow", u"Apply  (needs restart)", None))
        self.settings_button_reset.setText(QCoreApplication.translate("MainWindow", u"Reset Porn Fetch to default settings", None))
        self.settings_groupbox_videos.setTitle(QCoreApplication.translate("MainWindow", u"Videos", None))
        self.settings_radio_videos_quality_worst.setText(QCoreApplication.translate("MainWindow", u"Worst", None))
        self.settings_radio_videos_quality_half.setText(QCoreApplication.translate("MainWindow", u"Half", None))
        self.settings_radio_videos_model_type_user_uploads.setText(QCoreApplication.translate("MainWindow", u"User uploads", None))
        self.settings_lineedit_videos_output_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter \"./\" for current directory", None))
        self.settings_button_help_videos_model_videos_type.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_button_help_videos_result_limit.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_button_videos_open_output_path.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.settings_button_help_videos_write_metadata.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_radio_videos_quality_best.setText(QCoreApplication.translate("MainWindow", u"Best", None))
        self.settings_label_videos_result_limit.setText(QCoreApplication.translate("MainWindow", u"Result Limit:", None))
        self.settings_checkbox_videos_write_metadata.setText(QCoreApplication.translate("MainWindow", u"Write metadata tags", None))
        self.settings_radio_videos_model_type_featured.setText(QCoreApplication.translate("MainWindow", u"Featured videos", None))
        self.settings_label_videos_output_path.setText(QCoreApplication.translate("MainWindow", u"Output path:", None))
        self.settings_checkbox_videos_skip_existing_files.setText(QCoreApplication.translate("MainWindow", u"Skip existing files", None))
        self.settings_label_videos_quality.setText(QCoreApplication.translate("MainWindow", u"Quality:", None))
        self.settings_button_help_videos_skip_existing_files.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_videos_model_vdeos_type.setText(QCoreApplication.translate("MainWindow", u"Model videos (PornHub)", None))
        self.settings_radio_videos_model_type_both.setText(QCoreApplication.translate("MainWindow", u"Both", None))
        self.settings_checkbox_videos_use_video_id_as_filename.setText(QCoreApplication.translate("MainWindow", u"Use Video ID as filename", None))
        self.settings_checkbox_videos_use_directory_system.setText(QCoreApplication.translate("MainWindow", u"Use directory system", None))
        self.settings_button_help_videos_use_directory_system.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_checkbox_videos_direct_download.setText(QCoreApplication.translate("MainWindow", u"Directly Download videos (bypass tree widget)", None))
        self.settings_button_help_videos_direct_download.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_groupbox_ui.setTitle(QCoreApplication.translate("MainWindow", u"Graphical User Interface", None))
        self.settings_radio_ui_language_system_default.setText(QCoreApplication.translate("MainWindow", u"System default", None))
        self.settings_label_ui_language.setText(QCoreApplication.translate("MainWindow", u"Graphical User Interface Language:", None))
        self.settings_radio_ui_language_english.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.settings_radio_ui_language_french.setText(QCoreApplication.translate("MainWindow", u"French", None))
        self.settings_radio_ui_language_chinese_simplified.setText(QCoreApplication.translate("MainWindow", u"Chinese (simplified)", None))
        self.settings_radio_ui_language_german.setText(QCoreApplication.translate("MainWindow", u"German", None))
        self.settings_checkbox_ui_custom_font.setText(QCoreApplication.translate("MainWindow", u"Enable custom font (Jetbrains Mono)", None))
        self.settings_label_ui_font_size.setText(QCoreApplication.translate("MainWindow", u"Font Size:", None))
        self.settings_groupbox_system_pornfetch.setTitle(QCoreApplication.translate("MainWindow", u"System / Porn Fetch", None))
        self.settings_checkbox_system_enable_anonymous_mode.setText(QCoreApplication.translate("MainWindow", u"Enable Anonymous mode", None))
        self.settings_checkbox_system_enable_network_logging.setText(QCoreApplication.translate("MainWindow", u"Enable Network Logging", None))
        self.settings_button_help_system_supress_errors.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_checkbox_system_supress_errors.setText(QCoreApplication.translate("MainWindow", u"Supress errors silently", None))
        self.settings_checkbox_system_internet_checks.setText(QCoreApplication.translate("MainWindow", u"Internet checks", None))
        self.settings_checkbox_system_activate_proxy.setText(QCoreApplication.translate("MainWindow", u"Activate Proxy", None))
        self.settings_checkbox_system_update_checks.setText(QCoreApplication.translate("MainWindow", u"Update checks", None))
        self.settings_button_help_system_enable_network_logging.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_button_system_install_pornfetch.setText(QCoreApplication.translate("MainWindow", u"Install Porn Fetch", None))
        self.settings_label_system_startup.setText(QCoreApplication.translate("MainWindow", u"Startup:", None))
        self.settings_label_system_privacy.setText(QCoreApplication.translate("MainWindow", u"Privacy:", None))
        self.settings_checkbox_system_proxy_kill_switch.setText(QCoreApplication.translate("MainWindow", u"Proxy Kill Switch", None))
        self.settings_button_help_system_anonymous_mode.setText(QCoreApplication.translate("MainWindow", u"Help (anonymous mode)", None))
        self.settings_button_help_system_proxy_kill_switch.setText(QCoreApplication.translate("MainWindow", u"Help / Explanation (Proxy Kill Switch) ", None))
        self.settings_groupbox_performance.setTitle(QCoreApplication.translate("MainWindow", u"Performance", None))
        self.settings_label_performance_network_delay.setText(QCoreApplication.translate("MainWindow", u"Network delay (per Request, in seconds):", None))
        self.settings_button_help_performance_network_delay.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_download_mode.setText(QCoreApplication.translate("MainWindow", u"Download Mode:", None))
        self.settings_radio_performance_download_mode_performance.setText(QCoreApplication.translate("MainWindow", u"High Performance", None))
        self.settings_radio_performance_download_mode_default.setText(QCoreApplication.translate("MainWindow", u"Default", None))
        self.settings_button_help_performance_download_mode.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_speed_limit.setText(QCoreApplication.translate("MainWindow", u"Speed Limit (MB/s):", None))
        self.settings_button_help_performance_speed_limit.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_maximal_timeout.setText(QCoreApplication.translate("MainWindow", u"Maximal timeout:", None))
        self.settings_button_help_performance_maximal_timeout.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_processing_delay.setText(QCoreApplication.translate("MainWindow", u"Processing Delay (each Video, in seconds):", None))
        self.settings_button_help_performance_processing_delay.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_simultaneous_download.setText(QCoreApplication.translate("MainWindow", u"Simultaneous downloads:", None))
        self.settings_button_help_performance_simultaneous_downloads.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_maximal_retries.setText(QCoreApplication.translate("MainWindow", u"Maximal retries:", None))
        self.settings_button_help_performance_maximal_retries.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.settings_label_performance_maximal_workers.setText(QCoreApplication.translate("MainWindow", u"Maximal workers:", None))
        self.settings_button_help_performance_maximal_workers.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.button_accept.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
        self.button_deny.setText(QCoreApplication.translate("MainWindow", u"Deny and Exit", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'JetBrainsMono Nerd Font Propo'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">GPL License Agreement for Porn Fetch</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program is free software: you may redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, eithe"
                        "r version 3 of the License or (at your option) any later version.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program is distributed in the hope that it will be useful, but it is provided <span style=\" font-weight:700;\">&quot;AS IS&quot; WITHOUT ANY WARRANTY</span>; without even the implied warranties of <span style=\" font-weight:700;\">MERCHANTABILITY</span> or <span style=\" font-weight:700;\">FITNESS FOR A PARTICULAR PURPOSE</span>. For more details, see the GNU General Public License.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You should have received a copy of the GNU General Public License along with this program. If not, visit <a href=\"https://www.gnu.org/licenses/\"><span style=\" text-decoration: underline; color:#007af4;\">https://www.gnu.org/licenses/</span></a>.</p>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-"
                        "bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Limitation of Liability</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Under no circumstances and under no legal theory\u2014whether in tort, contract, or otherwise\u2014shall the copyright holder or contributors be held liable for any direct, indirect, special, incidental, consequential, or exemplary damages of any kind. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This includes, but is not limited to:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Damages for loss of goodwill </li>\n"
"<li style=\" mar"
                        "gin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Work stoppage </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Computer failure or malfunction </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Loss of data </li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Any other commercial damages or losses </li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Even if such parties were informed of the possibility of such damages.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This limitation does not apply to liability for death or personal injury resulting f"
                        "rom the negligence of such parties, where applicable law prohibits such a limitation. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Note:</span> In some jurisdictions, the exclusion or limitation of incidental or consequential damages is not allowed. Therefore, these exclusions may not apply to you.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This Agreement constitutes the complete and exclusive understanding between the parties regarding the subject matter contained herein.</p>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Disclaimer</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent"
                        ":0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> violates the Terms of Service of all the websites it supports, including but not limited to: </p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://pornhub.com\"><span style=\" text-decoration: underline; color:#007af4;\">pornhub.com</span></a> </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://hqporner.com\"><span style=\" text-decoration: underline; color:#007af4;\">hqporner.com</span></a> </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://eporner.com\"><span style=\" text-decoration: underline; color:#007af4;\">eporner.com</span></a> </li>\n"
"<li sty"
                        "le=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://xnxx.com\"><span style=\" text-decoration: underline; color:#007af4;\">xnxx.com</span></a> </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://xvideos.com\"><span style=\" text-decoration: underline; color:#007af4;\">xvideos.com</span></a> </li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">spankbang.com</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline; color:#006fff;\">xhamster.com</span></li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">missav.ws</"
                        "li></ul>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Usage Warning</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Using <span style=\" font-weight:700;\">Porn Fetch</span> may result in <span style=\" font-weight:700;\">legal action</span> being taken against you. The creator of this software is not liable for any damages or legal consequences resulting from its use.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> was created solely for the purpose of enabling offline access to videos in scenarios where internet access is unavailable. </p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
""
                        "<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The redistribution of copyright-protected content obtained through Porn Fetch is <span style=\" font-weight:700;\">strictly forbidden</span>. </li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Any misuse of this software to steal and redistribute copyrighted material is against its intended purpose and is not endorsed by the creator. </li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-weight:700;\">batch processing feature</span> in Porn Fetch is intended to assist users without graphical user interfaces in downloading content for personal use, not for large-scale video theft or redistribution.</p>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-"
                        "block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Third-Party Software</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> utilizes the following third-party tools and resources:</p>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">FFmpeg</span> </li>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">Used for video processing and conversion. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">FFmpeg is free software licensed under the GPL. </p>\n"
"<p style=\" margi"
                        "n-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">For more information, visit <a href=\"https://ffmpeg.org\"><span style=\" text-decoration: underline; color:#007af4;\">https://ffmpeg.org</span></a>.</p>\n"
"<li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">JetBrains Mono Font</span> </li></ol>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">Copyright \u00a9 2019 JetBrains. All Rights Reserved. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">Licensed under the SIL Open Font License, Version 1.1. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">License details: <a href=\"https://scripts.sil.org/OFL\"><span style=\""
                        " text-decoration: underline; color:#007af4;\">https://scripts.sil.org/OFL</span></a>.</p>\n"
"<hr />\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Thank you for using <span style=\" font-weight:700;\">Porn Fetch</span> responsibly!</p></body></html>", None))
        self.textbrowser_range.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">Select the range of videos to be automatically selected.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; te"
                        "xt-indent:0px;\"><span style=\" font-family:'Segoe UI';\">For example, if you set the start to 5 and the end to 20, then all videos between 5-20 will be checked for downloading :)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">Or select by a range in time:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">For example if you want to download all videos in between 10 and 20 minutes do:</span></p>\n"
""
                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">Start: 10</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">End: 20</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">And click Apply.</span></p></body></html>", None))
        self.button_range_apply_time.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_apply_by_time.setText(QCoreApplication.translate("MainWindow", u"Apply by time:", None))
        self.lineedit_range_start.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lineedit_range_author.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the author's name", None))
        self.label_apply_by_index.setText(QCoreApplication.translate("MainWindow", u"Apply by Index:", None))
        self.label_range_end.setText(QCoreApplication.translate("MainWindow", u"End:", None))
        self.button_range_apply_index.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.label_range_time_end.setText(QCoreApplication.translate("MainWindow", u"End:", None))
        self.label_range_start.setText(QCoreApplication.translate("MainWindow", u"Start:", None))
        self.button_range_apply_author.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.lineedit_range_end.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_range_time_start.setText(QCoreApplication.translate("MainWindow", u"Start:", None))
        self.label_range_by_author.setText(QCoreApplication.translate("MainWindow", u"Apply by author:", None))
        self.text_browser_keyboard_shortcuts.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:700;\">Keyboard Shortcuts</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:700;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-"
                        "indent:0px;\"><span style=\" font-size:16pt;\">CTRL + Q     Closes the application</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + E      Exports all current video URLs from the tree widget into a .txt file </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + T      Downloads all videos in the tree widget (same as clicking the button)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + A     Quickly enables the anonymous mode (temporarily)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + S     Saves Porn Fetch settin"
                        "gs</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + X     Selects all items in the tree widget as checked</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + Z     Unchecks all items in the tree widget</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">   </span></p></body></html>", None))
        self.button_update_acknowledged.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.textBrowser_3.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:24pt; font-weight:700;\">Installation Mode</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#0000ff;\">1) Inst</span><span style=\" font-family:'Segoe UI'; font-size:14pt; text-"
                        "decoration: underline; color:#0000ff;\">all</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This will install Porn Fetch into your system, meaning that you can run it directly from your Start Menu. e.g, press Windows key, type Porn Fetch and directly start it and on Linux it will be the same.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Porn Fetch will be installed into the following path(s):</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-ind"
                        "ent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Windows: C:\\Users\\&lt;user&gt;\\AppData\\Local\\pornfetch\\</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Linux: ~/.local/share/pornfetch</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#00ff00;\">2) Portable</span></p>\n"
"<p style=\" margin-top:0px; mar"
                        "gin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This means, that Porn Fetch will not be installed and in order to use and start Porn Fetch you always need to double click on the file you have downloaded. This has some benefits as the uninstallation is easier and you have more control over it, but for the average user I do not recommend this.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; font-weight:700; color:#a100ff;\">Custom App name</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\">Down below you can enter  a custom name for Porn Fetch. You can then search with this name for Porn Fetch and Porn Fetch will not be found anymore when someone enters &quot;Porn Fetch&quot; on your PC. This can be useful if multiple persons use your PC and you don't want them to know you are using this application. It can also help if you are in public and people stare at your PC. Porn Fetch has also an option to fully hide, that it's a PornHub downloader.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ffffff;\">If you leave it empty, Porn Fetch will remain as &quot;Porn Fetch&quot; in your short menu.</spa"
                        "n></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:14pt; text-decoration: underline; color:#aa0000;\">NOTE:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Installation was implemented in this release and might still be experimental. If you run into any issues, please report it on my GitHub. Thank you :</span><span style=\" font-family:'Segoe UI';\">) </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p></body></html>", None))
        self.label_custom_app_name.setText(QCoreApplication.translate("MainWindow", u"Custom App Name:", None))
        self.lineedit_custom_app_name.setText("")
        self.lineedit_custom_app_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your custom App Name here. Leave it empty to keep \"Porn Fetch\"", None))
        self.button_install.setText(QCoreApplication.translate("MainWindow", u"Install", None))
        self.button_portable.setText(QCoreApplication.translate("MainWindow", u"Portable", None))
        self.main_textbrowser_supported_websites.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#0019ff;\">Supported Websites:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-"
                        "size:16pt; color:#00ff08;\">Downloading:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- PornHub.com (supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- HQPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- Eporner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- XNXX.com (supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- XVideos.com (supports total pro"
                        "gress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- Missav.ws (and all of it's subsites, supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- Xhamster.com (supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- Spankbang.com (supports total progress)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#ee00ff;\">Model / Channel Dow"
                        "nloads</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- PornHub.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- HQPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- EPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- XNXX.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- XVideos.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; m"
                        "argin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; color:#ff8800;\">Searching:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- PornHub.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- HQPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- Xvideos.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- Eporner.com</span></p>\n"
"<p style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- XNXX.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ff0000;\">I am constantly working to support more websites.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ff0000;\">If you want a specific site to be supported, just ask:<br /><br />Discord: echteralsfake</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ff0000;\">Git"
                        "Hub: https://github.com/EchterAlsFake/Porn_Fetch/issues</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; color:#ff0000;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:"
                        "0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.button_donate_kofi.setText(QCoreApplication.translate("MainWindow", u"Ko-Fi", None))
        self.button_donate_already_donated.setText(QCoreApplication.translate("MainWindow", u"Already Donated", None))
        self.button_donate_paypal.setText(QCoreApplication.translate("MainWindow", u"PayPal", None))
        self.button_donate_copy_xmr.setText(QCoreApplication.translate("MainWindow", u"Copy XMR", None))
        self.button_donate_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.textBrowser_4.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:36pt; color:#ffc800;\">y</span><span style=\" font-size:36pt; color:#cc00ff;\">o</span><span style=\" font-size:36pt; color:#ffffff;\"> </span><span style=\" font-size:36pt; color:#37ff00;\">w</span><span style=\" font-size:36pt; color:#ff00bb;\">a</span><span style=\" font-size:36pt; color:#ff0000;\">s</span><span style=\" font-size:36pt; color:#0000ff;\""
                        ">s</span><span style=\" font-size:36pt; color:#00fff7;\">u</span><span style=\" font-size:36pt; color:#ff55ff;\">p</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; text-decoration: underline; color:#ffffff;\">If you have a moment to read this, I'd appreciate it a lot...</span><span style=\" font-size:14px; color:#ffffff;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#ffffff;\">I have started developing Porn Fetch ~2 years ago as a fun project for learning graphical user interfaces. Over the years Porn Fetch became more professional, as my programming skills increased and more people started using it. That I reach even 1000 downloads on this was something I'd never thought was possible and now we are over 20.000 xD</span></p>\n"
"<p style=\""
                        " margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#ffffff;\">Although I absolutely love what I am doing here, and unless I receive a Cease and Desist letter, will never stop it, I haven't earned much from this project except for the few people that donated me something (Thank you so much btw).</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#ffffff;\">If you have a few cents left on your pocket, I'd absolutely appreciate it. I know it might not seem much but it's a thank you and it keeps me motivated. Also since I still go to school small amounts of money are much more in relation to me than it is for someone who already has a job.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-s"
                        "ize:11pt; color:#ffffff;\">But even if you don't donate, please don't feel bad. I don't expect it from you. I just kindly ask, but it's absolutely okay if you don't want to.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#0000ff;\">Donation options</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://paypal.me/EchterAlsFake\"><span style=\" font-size:14pt; text-decoration: underline; color:#27bf73;\">1) PayPal (https://paypal.me/EchterAlsFake)</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://paypal.me/EchterAlsFake\"><span style=\" font-size:14pt; text-decoration: underline; color:#aa00ff;\">2) K</span></a><a href=\"https://ko-fi.com/EchterAlsFake\"><span style=\" font-size:"
                        "14pt; text-decoration: underline; color:#aa00ff;\">o-Fi (https://ko-fi.com/EchterAlsFake)</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">3) Crypto (XMR / Monero) : </span><span style=\" font-family:'ui-monospace','SFMono-Regular','SF Mono','Menlo','Consolas','Liberation Mono','monospace'; font-size:14px; color:#ff7700; background-color:rgba(101,108,118,0.2);\">42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#00ffb3;\">[This message won't be shown again, except if you update to a new version]</span></p></body></html>", None))
        self.textBrowser_5.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">DISCLAIMER</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> is free software licensed under the GNU General Public License v3.0. You are free to use, modify, and redistribute this software under the terms o"
                        "f that license.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please be aware that <span style=\" font-weight:700;\">Porn Fetch may interact with websites in ways that violate their Terms of Service.</span> Additionally, downloading copyright-protected content without proper authorization may be illegal in many jurisdictions, including under the DMCA (Digital Millennium Copyright Act).</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">While some countries or regions may allow downloading content for strictly <span style=\" font-weight:700;\">personal, non-commercial use</span>, I <span style=\" font-weight:700;\">strongly discourage</span> using Porn Fetch to download, share, or redistribute content without appropriate rights or permissions. Always ensure you comply with your local laws and the terms of any website you access.</p>\n"
"<h3 style=\""
                        " margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">IMPORTANT NOTE</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">I <span style=\" font-weight:700;\">strongly recommend</span> that you do <span style=\" font-weight:700;\">not</span> use this software for:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Unauthorized redistribution of content</li>\n"
"<li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Commercial use of downloaded materials</li>\n"
"<li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent"
                        ":0; text-indent:0px;\">Any activity that could result in legal liability for yourself or others</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Although the GPL license grants you broad rights, <span style=\" font-weight:700;\">continued misuse</span> may jeopardize the development and availability of this project. Please respect the intent behind this tool and use it responsibly.</p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">LIABILITY DISCLAIMER</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This software is provided <span style=\" font-weight:700;\">without any warranty</span> as described in the GPLv3. I am <span style=\" font-weight:700;\">not liable</span> for any damages, legal consequences, "
                        "or misuse resulting from your use of this software.<br />You are solely responsible for ensuring your actions are lawful and ethical. </p></body></html>", None))
        self.button_disclaimer_accept.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
        self.textBrowser_2.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Data Collection &amp; Privacy Information</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">This application now uses my own server for update checking and error reporting, instead of relying on GitHub. This gives me greater"
                        " control over the process and the data transmitted. However, my server is </span><span style=\" font-size:12pt; font-weight:700;\">IPv6-only</span><span style=\" font-size:12pt;\">. This means that only about 50% of internet users will be able to connect. </span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">About the Server</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The server is a small, older Acer Swift 3 laptop running 24/7 in my room. The full source code for the server is publicly available here:<br /></span><a href=\"https://github.com/EchterAlsFake/Server\"><span style=\" font-size:12pt; text-decoration: underline; color:#f700ff;\">https://github.com/EchterAlsFake/Server</span></a><span style=\" font-size:12pt;\"> </span></p>\n"
"<h3 style=\""
                        " margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:700;\">Data Collected via Error Reports</span></h3>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The version of Porn Fetch you are using</span></li>\n"
"<li style=\" font-size:12pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Your operating system (e.g., Windows, Linux, or macOS)</li>\n"
"<li style=\" font-size:12pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The current date and time</li>\n"
"<li style=\" font-size:12pt;\" style=\" margin-top:0px; margin-bottom:12px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The error details (full Python traceback)</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:700;\">Important:</span><span style=\" font-size:12pt;\"> The Python traceback may, in some cases, include incidental personal information \u2014 for example, your system username if it appears in a file path. No other personal data is intentionally collected. </span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Data Storage &amp; Security</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Error reports are stored in plain text on my server. The server\u2019s storage device is encr"
                        "ypted with LUKS and secured with a strong password (40+ characters). </span><span style=\" font-size:12pt; color:#ff0000;\">Your </span><span style=\" font-size:12pt; font-weight:700; color:#ff0000;\">IP address is never logged, stored, or displayed</span><span style=\" font-size:12pt; color:#ff0000;\">. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Optional Participation</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Whether you enable error reporting or not will have no impact on the application's functionality. It simply helps me identify and fix issues faster. You can also manually check for updates on GitHub, although most users do not do this. </span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:700;\">IPv6 Connectivity Check</span></h3>\n"
"<p style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">To see if you have IPv6 connectivity, visit:</span><span style=\" font-size:14pt;\"><br /></span><a href=\"https://echteralsfake.duckdns.org/ping\"><span style=\" font-size:14pt; text-decoration: underline; color:#1aff00;\">https://echteralsfake.duckdns.org/ping</span></a><br /><span style=\" font-size:12pt;\">If you see a white page with </span><span style=\" font-size:12pt; font-weight:700;\">Success</span><span style=\" font-size:12pt;\">, you have IPv6. If not, you do not. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">You can also verify your IP addresses by visiting: </span><a href=\"https://ipleak.n"
                        "et\"><span style=\" font-size:12pt; text-decoration: underline; color:#ffff00;\">https://ipleak.net</span></a><span style=\" font-size:12pt;\"><br />Example formats:<br />IPv4: </span><span style=\" font-family:'monospace'; font-size:12pt;\">135.215.32.64</span><span style=\" font-size:12pt;\"><br />IPv6: </span><span style=\" font-family:'monospace'; font-size:12pt;\">2a02:810a:186:b400::5c51</span><span style=\" font-size:12pt;\"> </span></p></body></html>", None))
        self.button_server_enable_logging.setText(QCoreApplication.translate("MainWindow", u"I have IPv6 :) (and want to enable it)", None))
        self.button_server_disable_logging.setText(QCoreApplication.translate("MainWindow", u"I don't have IPv6 / I don't want to enable this feature", None))
        self.main_label_progressbar_total.setText(QCoreApplication.translate("MainWindow", u"Total:", None))
        self.main_label_progressbar_converting.setText(QCoreApplication.translate("MainWindow", u"Converting:", None))
    # retranslateUi

