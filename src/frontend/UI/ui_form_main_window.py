# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QMainWindow, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QStackedWidget,
    QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_PornFetch_UI(object):
    def setupUi(self, PornFetch_UI):
        if not PornFetch_UI.objectName():
            PornFetch_UI.setObjectName(u"PornFetch_UI")
        PornFetch_UI.resize(1138, 640)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PornFetch_UI.sizePolicy().hasHeightForWidth())
        PornFetch_UI.setSizePolicy(sizePolicy)
        PornFetch_UI.setStyleSheet(u"")
        self.main_CentralWidget = QWidget(PornFetch_UI)
        self.main_CentralWidget.setObjectName(u"main_CentralWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_CentralWidget.sizePolicy().hasHeightForWidth())
        self.main_CentralWidget.setSizePolicy(sizePolicy1)
        self.gridLayout_11 = QGridLayout(self.main_CentralWidget)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.formlayout_progressbar = QFormLayout()
        self.formlayout_progressbar.setObjectName(u"formlayout_progressbar")
        self.formlayout_progressbar.setHorizontalSpacing(0)
        self.formlayout_progressbar.setVerticalSpacing(5)
        self.main_label_progressbar_total = QLabel(self.main_CentralWidget)
        self.main_label_progressbar_total.setObjectName(u"main_label_progressbar_total")

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_total)

        self.main_progressbar_total = QProgressBar(self.main_CentralWidget)
        self.main_progressbar_total.setObjectName(u"main_progressbar_total")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.main_progressbar_total.sizePolicy().hasHeightForWidth())
        self.main_progressbar_total.setSizePolicy(sizePolicy2)
        self.main_progressbar_total.setMinimumSize(QSize(300, 0))
        self.main_progressbar_total.setStyleSheet(u"text-align: center; /* Centered text */")
        self.main_progressbar_total.setValue(0)

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.FieldRole, self.main_progressbar_total)


        self.gridLayout_11.addLayout(self.formlayout_progressbar, 2, 0, 1, 1)

        self.main_horizontallayout_menu_buttons = QHBoxLayout()
        self.main_horizontallayout_menu_buttons.setSpacing(5)
        self.main_horizontallayout_menu_buttons.setObjectName(u"main_horizontallayout_menu_buttons")
        self.main_button_switch_home = QPushButton(self.main_CentralWidget)
        self.main_button_switch_home.setObjectName(u"main_button_switch_home")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.main_button_switch_home.sizePolicy().hasHeightForWidth())
        self.main_button_switch_home.setSizePolicy(sizePolicy3)
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

        self.main_button_switch_account = QPushButton(self.main_CentralWidget)
        self.main_button_switch_account.setObjectName(u"main_button_switch_account")
        sizePolicy3.setHeightForWidth(self.main_button_switch_account.sizePolicy().hasHeightForWidth())
        self.main_button_switch_account.setSizePolicy(sizePolicy3)
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

        self.main_button_switch_tools = QPushButton(self.main_CentralWidget)
        self.main_button_switch_tools.setObjectName(u"main_button_switch_tools")
        sizePolicy3.setHeightForWidth(self.main_button_switch_tools.sizePolicy().hasHeightForWidth())
        self.main_button_switch_tools.setSizePolicy(sizePolicy3)
        self.main_button_switch_tools.setMinimumSize(QSize(50, 35))
        self.main_button_switch_tools.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        self.main_button_switch_tools.setFont(font)
        self.main_button_switch_tools.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_tools.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.main_button_switch_tools.setIconSize(QSize(32, 32))

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_tools)

        self.main_button_switch_settings = QPushButton(self.main_CentralWidget)
        self.main_button_switch_settings.setObjectName(u"main_button_switch_settings")
        sizePolicy3.setHeightForWidth(self.main_button_switch_settings.sizePolicy().hasHeightForWidth())
        self.main_button_switch_settings.setSizePolicy(sizePolicy3)
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

        self.main_button_switch_credits = QPushButton(self.main_CentralWidget)
        self.main_button_switch_credits.setObjectName(u"main_button_switch_credits")
        sizePolicy3.setHeightForWidth(self.main_button_switch_credits.sizePolicy().hasHeightForWidth())
        self.main_button_switch_credits.setSizePolicy(sizePolicy3)
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

        self.main_button_switch_supported_websites = QPushButton(self.main_CentralWidget)
        self.main_button_switch_supported_websites.setObjectName(u"main_button_switch_supported_websites")
        sizePolicy3.setHeightForWidth(self.main_button_switch_supported_websites.sizePolicy().hasHeightForWidth())
        self.main_button_switch_supported_websites.setSizePolicy(sizePolicy3)
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


        self.gridLayout_11.addLayout(self.main_horizontallayout_menu_buttons, 0, 0, 1, 1)

        self.main_CentralStackedWidget = QStackedWidget(self.main_CentralWidget)
        self.main_CentralStackedWidget.setObjectName(u"main_CentralStackedWidget")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.page_main.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_9 = QGridLayout(self.page_main)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.main_verticallayout = QVBoxLayout()
        self.main_verticallayout.setObjectName(u"main_verticallayout")
        self.main_stacked_widget_top = QStackedWidget(self.page_main)
        self.main_stacked_widget_top.setObjectName(u"main_stacked_widget_top")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.main_stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.main_stacked_widget_top.setSizePolicy(sizePolicy4)
        self.main_stacked_widget_top.setMinimumSize(QSize(0, 150))
        self.main_stacked_widget_top.setMaximumSize(QSize(16777215, 150))
        self.main_stacked_widget_top.setStyleSheet(u"")
        self.main_stacked_widget_top.setLineWidth(1)
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        sizePolicy1.setHeightForWidth(self.page_download.sizePolicy().hasHeightForWidth())
        self.page_download.setSizePolicy(sizePolicy1)
        self.page_download.setMinimumSize(QSize(0, 150))
        self.page_download.setMaximumSize(QSize(16777215, 180))
        self.gridLayout_5 = QGridLayout(self.page_download)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.download_gridlayout = QGridLayout()
        self.download_gridlayout.setSpacing(2)
        self.download_gridlayout.setObjectName(u"download_gridlayout")
        self.download_gridlayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.download_gridlayout.setContentsMargins(-1, 0, -1, -1)
        self.download_label_model_url = QLabel(self.page_download)
        self.download_label_model_url.setObjectName(u"download_label_model_url")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.download_label_model_url.sizePolicy().hasHeightForWidth())
        self.download_label_model_url.setSizePolicy(sizePolicy5)
        self.download_label_model_url.setMinimumSize(QSize(0, 30))
        font1 = QFont()
        font1.setBold(False)
        self.download_label_model_url.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_model_url, 5, 0, 1, 1)

        self.download_button_search = QPushButton(self.page_download)
        self.download_button_search.setObjectName(u"download_button_search")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.download_button_search.sizePolicy().hasHeightForWidth())
        self.download_button_search.setSizePolicy(sizePolicy6)
        self.download_button_search.setMinimumSize(QSize(0, 35))
        self.download_button_search.setFont(font1)
        self.download_button_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.download_gridlayout.addWidget(self.download_button_search, 6, 4, 1, 1)

        self.download_label_playlist_url = QLabel(self.page_download)
        self.download_label_playlist_url.setObjectName(u"download_label_playlist_url")
        sizePolicy5.setHeightForWidth(self.download_label_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_label_playlist_url.setSizePolicy(sizePolicy5)
        self.download_label_playlist_url.setMinimumSize(QSize(0, 30))
        self.download_label_playlist_url.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_playlist_url, 4, 0, 1, 1)

        self.download_button_model = QPushButton(self.page_download)
        self.download_button_model.setObjectName(u"download_button_model")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.download_button_model.sizePolicy().hasHeightForWidth())
        self.download_button_model.setSizePolicy(sizePolicy7)
        self.download_button_model.setMinimumSize(QSize(60, 30))
        self.download_button_model.setFont(font1)
        self.download_button_model.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_model.setStyleSheet(u"")

        self.download_gridlayout.addWidget(self.download_button_model, 5, 4, 1, 1)

        self.download_lineedit_playlist_url = QLineEdit(self.page_download)
        self.download_lineedit_playlist_url.setObjectName(u"download_lineedit_playlist_url")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.download_lineedit_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_playlist_url.setSizePolicy(sizePolicy8)
        self.download_lineedit_playlist_url.setMinimumSize(QSize(0, 30))
        font2 = QFont()
        font2.setBold(True)
        self.download_lineedit_playlist_url.setFont(font2)

        self.download_gridlayout.addWidget(self.download_lineedit_playlist_url, 4, 1, 1, 3)

        self.download_button_playlist_get_videos = QPushButton(self.page_download)
        self.download_button_playlist_get_videos.setObjectName(u"download_button_playlist_get_videos")
        sizePolicy7.setHeightForWidth(self.download_button_playlist_get_videos.sizePolicy().hasHeightForWidth())
        self.download_button_playlist_get_videos.setSizePolicy(sizePolicy7)
        self.download_button_playlist_get_videos.setMinimumSize(QSize(0, 30))
        self.download_button_playlist_get_videos.setFont(font1)
        self.download_button_playlist_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.download_gridlayout.addWidget(self.download_button_playlist_get_videos, 4, 4, 1, 1)

        self.download_lineedit_model_url = QLineEdit(self.page_download)
        self.download_lineedit_model_url.setObjectName(u"download_lineedit_model_url")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.download_lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_model_url.setSizePolicy(sizePolicy9)
        self.download_lineedit_model_url.setMinimumSize(QSize(300, 35))
        self.download_lineedit_model_url.setFont(font2)

        self.download_gridlayout.addWidget(self.download_lineedit_model_url, 5, 1, 1, 3)

        self.download_lineedit_search_query = QLineEdit(self.page_download)
        self.download_lineedit_search_query.setObjectName(u"download_lineedit_search_query")
        sizePolicy9.setHeightForWidth(self.download_lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.download_lineedit_search_query.setSizePolicy(sizePolicy9)
        self.download_lineedit_search_query.setMinimumSize(QSize(100, 35))
        self.download_lineedit_search_query.setFont(font2)

        self.download_gridlayout.addWidget(self.download_lineedit_search_query, 6, 1, 1, 1)

        self.download_label_search = QLabel(self.page_download)
        self.download_label_search.setObjectName(u"download_label_search")
        sizePolicy5.setHeightForWidth(self.download_label_search.sizePolicy().hasHeightForWidth())
        self.download_label_search.setSizePolicy(sizePolicy5)
        self.download_label_search.setMinimumSize(QSize(0, 30))
        self.download_label_search.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_search, 6, 0, 1, 1)

        self.download_button_download = QPushButton(self.page_download)
        self.download_button_download.setObjectName(u"download_button_download")
        sizePolicy7.setHeightForWidth(self.download_button_download.sizePolicy().hasHeightForWidth())
        self.download_button_download.setSizePolicy(sizePolicy7)
        self.download_button_download.setMinimumSize(QSize(60, 30))
        font3 = QFont()
        font3.setBold(False)
        font3.setUnderline(False)
        self.download_button_download.setFont(font3)
        self.download_button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_download.setStyleSheet(u"")

        self.download_gridlayout.addWidget(self.download_button_download, 2, 4, 1, 1)

        self.download_website_combobox = QComboBox(self.page_download)
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.addItem("")
        self.download_website_combobox.setObjectName(u"download_website_combobox")
        sizePolicy.setHeightForWidth(self.download_website_combobox.sizePolicy().hasHeightForWidth())
        self.download_website_combobox.setSizePolicy(sizePolicy)
        self.download_website_combobox.setMinimumSize(QSize(0, 35))
        self.download_website_combobox.setMaximumSize(QSize(16777215, 35))
        self.download_website_combobox.setFont(font1)
        self.download_website_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.download_gridlayout.addWidget(self.download_website_combobox, 6, 2, 1, 1)

        self.download_label_url = QLabel(self.page_download)
        self.download_label_url.setObjectName(u"download_label_url")
        sizePolicy5.setHeightForWidth(self.download_label_url.sizePolicy().hasHeightForWidth())
        self.download_label_url.setSizePolicy(sizePolicy5)
        self.download_label_url.setMinimumSize(QSize(0, 30))
        self.download_label_url.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_url, 2, 0, 1, 1)

        self.download_lineedit_url = QLineEdit(self.page_download)
        self.download_lineedit_url.setObjectName(u"download_lineedit_url")
        sizePolicy2.setHeightForWidth(self.download_lineedit_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_url.setSizePolicy(sizePolicy2)
        self.download_lineedit_url.setMinimumSize(QSize(300, 30))
        self.download_lineedit_url.setFont(font2)

        self.download_gridlayout.addWidget(self.download_lineedit_url, 2, 1, 1, 3)


        self.gridLayout_5.addLayout(self.download_gridlayout, 0, 0, 1, 1)

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
        self.login_horizontallayout_ph_account = QHBoxLayout()
        self.login_horizontallayout_ph_account.setObjectName(u"login_horizontallayout_ph_account")
        self.login_button_get_watched_videos = QPushButton(self.page_login)
        self.login_button_get_watched_videos.setObjectName(u"login_button_get_watched_videos")
        self.login_button_get_watched_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_watched_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_watched_videos.setStyleSheet(u"")

        self.login_horizontallayout_ph_account.addWidget(self.login_button_get_watched_videos)

        self.login_button_get_recommended_videos = QPushButton(self.page_login)
        self.login_button_get_recommended_videos.setObjectName(u"login_button_get_recommended_videos")
        self.login_button_get_recommended_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_recommended_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_recommended_videos.setStyleSheet(u"")

        self.login_horizontallayout_ph_account.addWidget(self.login_button_get_recommended_videos)

        self.login_button_get_liked_videos = QPushButton(self.page_login)
        self.login_button_get_liked_videos.setObjectName(u"login_button_get_liked_videos")
        self.login_button_get_liked_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_liked_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_liked_videos.setStyleSheet(u"")

        self.login_horizontallayout_ph_account.addWidget(self.login_button_get_liked_videos)


        self.login_gridlayout_login_box.addLayout(self.login_horizontallayout_ph_account, 3, 0, 1, 4)

        self.login_lineedit_password = QLineEdit(self.page_login)
        self.login_lineedit_password.setObjectName(u"login_lineedit_password")
        sizePolicy2.setHeightForWidth(self.login_lineedit_password.sizePolicy().hasHeightForWidth())
        self.login_lineedit_password.setSizePolicy(sizePolicy2)
        self.login_lineedit_password.setMinimumSize(QSize(0, 35))
        self.login_lineedit_password.setFont(font2)
        self.login_lineedit_password.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.login_lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_password, 1, 1, 1, 3)

        self.login_lineedit_username = QLineEdit(self.page_login)
        self.login_lineedit_username.setObjectName(u"login_lineedit_username")
        sizePolicy2.setHeightForWidth(self.login_lineedit_username.sizePolicy().hasHeightForWidth())
        self.login_lineedit_username.setSizePolicy(sizePolicy2)
        self.login_lineedit_username.setMinimumSize(QSize(150, 35))
        self.login_lineedit_username.setFont(font2)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_username, 0, 1, 1, 3)

        self.login_button_login = QPushButton(self.page_login)
        self.login_button_login.setObjectName(u"login_button_login")
        self.login_button_login.setMinimumSize(QSize(0, 30))
        self.login_button_login.setFont(font2)
        self.login_button_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_login.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_login, 2, 0, 1, 4)

        self.login_label_password = QLabel(self.page_login)
        self.login_label_password.setObjectName(u"login_label_password")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.login_label_password.sizePolicy().hasHeightForWidth())
        self.login_label_password.setSizePolicy(sizePolicy10)
        self.login_label_password.setMinimumSize(QSize(0, 30))
        self.login_label_password.setFont(font2)

        self.login_gridlayout_login_box.addWidget(self.login_label_password, 1, 0, 1, 1)

        self.login_label_username = QLabel(self.page_login)
        self.login_label_username.setObjectName(u"login_label_username")
        sizePolicy10.setHeightForWidth(self.login_label_username.sizePolicy().hasHeightForWidth())
        self.login_label_username.setSizePolicy(sizePolicy10)
        self.login_label_username.setMinimumSize(QSize(0, 30))
        self.login_label_username.setFont(font2)

        self.login_gridlayout_login_box.addWidget(self.login_label_username, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.login_gridlayout_login_box, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_login)
        self.page_tools = QWidget()
        self.page_tools.setObjectName(u"page_tools")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.page_tools.sizePolicy().hasHeightForWidth())
        self.page_tools.setSizePolicy(sizePolicy11)
        self.page_tools.setMinimumSize(QSize(100, 30))
        self.gridLayout_17 = QGridLayout(self.page_tools)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_tools = QScrollArea(self.page_tools)
        self.scrollarea_tools.setObjectName(u"scrollarea_tools")
        self.scrollarea_tools.setWidgetResizable(True)
        self.scrollarea_tools_widget_contents = QWidget()
        self.scrollarea_tools_widget_contents.setObjectName(u"scrollarea_tools_widget_contents")
        self.scrollarea_tools_widget_contents.setGeometry(QRect(0, 0, 466, 182))
        self.gridLayout_8 = QGridLayout(self.scrollarea_tools_widget_contents)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.tools_verticallayout = QVBoxLayout()
        self.tools_verticallayout.setObjectName(u"tools_verticallayout")
        self.tools_groupbox_hqporner = QGroupBox(self.scrollarea_tools_widget_contents)
        self.tools_groupbox_hqporner.setObjectName(u"tools_groupbox_hqporner")
        self.gridLayout_15 = QGridLayout(self.tools_groupbox_hqporner)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.tools_gridlayout_hqporner = QGridLayout()
        self.tools_gridlayout_hqporner.setObjectName(u"tools_gridlayout_hqporner")
        self.tools_button_get_random_videos = QPushButton(self.tools_groupbox_hqporner)
        self.tools_button_get_random_videos.setObjectName(u"tools_button_get_random_videos")
        sizePolicy11.setHeightForWidth(self.tools_button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_random_videos.setSizePolicy(sizePolicy11)
        self.tools_button_get_random_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_random_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_hqporner.addWidget(self.tools_button_get_random_videos, 3, 0, 1, 1)

        self.tools_button_hqporner_category_get_videos = QPushButton(self.tools_groupbox_hqporner)
        self.tools_button_hqporner_category_get_videos.setObjectName(u"tools_button_hqporner_category_get_videos")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(2)
        sizePolicy12.setHeightForWidth(self.tools_button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_hqporner_category_get_videos.setSizePolicy(sizePolicy12)
        self.tools_button_hqporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_hqporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tools_button_hqporner_category_get_videos.setAcceptDrops(False)

        self.tools_gridlayout_hqporner.addWidget(self.tools_button_hqporner_category_get_videos, 1, 2, 1, 1)

        self.tools_label_videos_by_category = QLabel(self.tools_groupbox_hqporner)
        self.tools_label_videos_by_category.setObjectName(u"tools_label_videos_by_category")
        sizePolicy10.setHeightForWidth(self.tools_label_videos_by_category.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category.setSizePolicy(sizePolicy10)
        self.tools_label_videos_by_category.setMinimumSize(QSize(0, 0))

        self.tools_gridlayout_hqporner.addWidget(self.tools_label_videos_by_category, 1, 0, 1, 1)

        self.tools_lineedit_hqporner_category = QLineEdit(self.tools_groupbox_hqporner)
        self.tools_lineedit_hqporner_category.setObjectName(u"tools_lineedit_hqporner_category")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(4)
        sizePolicy13.setHeightForWidth(self.tools_lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_hqporner_category.setSizePolicy(sizePolicy13)
        self.tools_lineedit_hqporner_category.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_hqporner.addWidget(self.tools_lineedit_hqporner_category, 1, 1, 1, 1)

        self.tools_label_get_top_porn = QLabel(self.tools_groupbox_hqporner)
        self.tools_label_get_top_porn.setObjectName(u"tools_label_get_top_porn")
        sizePolicy10.setHeightForWidth(self.tools_label_get_top_porn.sizePolicy().hasHeightForWidth())
        self.tools_label_get_top_porn.setSizePolicy(sizePolicy10)
        self.tools_label_get_top_porn.setMinimumSize(QSize(0, 0))

        self.tools_gridlayout_hqporner.addWidget(self.tools_label_get_top_porn, 0, 0, 1, 1)

        self.tools_button_get_brazzers_videos = QPushButton(self.tools_groupbox_hqporner)
        self.tools_button_get_brazzers_videos.setObjectName(u"tools_button_get_brazzers_videos")
        sizePolicy11.setHeightForWidth(self.tools_button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_brazzers_videos.setSizePolicy(sizePolicy11)
        self.tools_button_get_brazzers_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_brazzers_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_hqporner.addWidget(self.tools_button_get_brazzers_videos, 3, 1, 1, 1)

        self.tools_combobox_hqporner_top_porn = QComboBox(self.tools_groupbox_hqporner)
        self.tools_combobox_hqporner_top_porn.addItem("")
        self.tools_combobox_hqporner_top_porn.addItem("")
        self.tools_combobox_hqporner_top_porn.addItem("")
        self.tools_combobox_hqporner_top_porn.setObjectName(u"tools_combobox_hqporner_top_porn")
        self.tools_combobox_hqporner_top_porn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_hqporner.addWidget(self.tools_combobox_hqporner_top_porn, 0, 1, 1, 1)

        self.tools_button_top_porn_get_videos = QPushButton(self.tools_groupbox_hqporner)
        self.tools_button_top_porn_get_videos.setObjectName(u"tools_button_top_porn_get_videos")
        sizePolicy7.setHeightForWidth(self.tools_button_top_porn_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_top_porn_get_videos.setSizePolicy(sizePolicy7)
        self.tools_button_top_porn_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_top_porn_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_hqporner.addWidget(self.tools_button_top_porn_get_videos, 0, 2, 1, 1)

        self.tools_button_list_categories = QPushButton(self.tools_groupbox_hqporner)
        self.tools_button_list_categories.setObjectName(u"tools_button_list_categories")
        sizePolicy7.setHeightForWidth(self.tools_button_list_categories.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories.setSizePolicy(sizePolicy7)
        self.tools_button_list_categories.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_hqporner.addWidget(self.tools_button_list_categories, 3, 2, 1, 1)


        self.gridLayout_15.addLayout(self.tools_gridlayout_hqporner, 0, 0, 1, 1)


        self.tools_verticallayout.addWidget(self.tools_groupbox_hqporner)

        self.tools_groupbox_eporner = QGroupBox(self.scrollarea_tools_widget_contents)
        self.tools_groupbox_eporner.setObjectName(u"tools_groupbox_eporner")
        self.gridLayout_16 = QGridLayout(self.tools_groupbox_eporner)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.tools_gridlayout_tools = QGridLayout()
        self.tools_gridlayout_tools.setSpacing(6)
        self.tools_gridlayout_tools.setObjectName(u"tools_gridlayout_tools")
        self.tools_gridlayout_tools.setContentsMargins(-1, 0, -1, -1)
        self.tools_lineedit_videos_by_category_eporner = QLineEdit(self.tools_groupbox_eporner)
        self.tools_lineedit_videos_by_category_eporner.setObjectName(u"tools_lineedit_videos_by_category_eporner")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(4)
        sizePolicy14.setHeightForWidth(self.tools_lineedit_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_videos_by_category_eporner.setSizePolicy(sizePolicy14)
        self.tools_lineedit_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_lineedit_videos_by_category_eporner, 4, 1, 1, 2)

        self.tools_button_eporner_category_get_videos = QPushButton(self.tools_groupbox_eporner)
        self.tools_button_eporner_category_get_videos.setObjectName(u"tools_button_eporner_category_get_videos")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(2)
        sizePolicy15.setHeightForWidth(self.tools_button_eporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_eporner_category_get_videos.setSizePolicy(sizePolicy15)
        self.tools_button_eporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_eporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_eporner_category_get_videos, 4, 4, 1, 1)

        self.tools_button_list_categories_eporner = QPushButton(self.tools_groupbox_eporner)
        self.tools_button_list_categories_eporner.setObjectName(u"tools_button_list_categories_eporner")
        sizePolicy7.setHeightForWidth(self.tools_button_list_categories_eporner.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories_eporner.setSizePolicy(sizePolicy7)
        self.tools_button_list_categories_eporner.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories_eporner.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_list_categories_eporner, 4, 3, 1, 1)

        self.tools_label_videos_by_category_eporner = QLabel(self.tools_groupbox_eporner)
        self.tools_label_videos_by_category_eporner.setObjectName(u"tools_label_videos_by_category_eporner")
        sizePolicy11.setHeightForWidth(self.tools_label_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category_eporner.setSizePolicy(sizePolicy11)
        self.tools_label_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_label_videos_by_category_eporner, 4, 0, 1, 1)


        self.gridLayout_16.addLayout(self.tools_gridlayout_tools, 0, 0, 1, 1)


        self.tools_verticallayout.addWidget(self.tools_groupbox_eporner)


        self.gridLayout_8.addLayout(self.tools_verticallayout, 0, 0, 1, 1)

        self.scrollarea_tools.setWidget(self.scrollarea_tools_widget_contents)

        self.gridLayout_17.addWidget(self.scrollarea_tools, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_tools)
        self.page_progressbars = QWidget()
        self.page_progressbars.setObjectName(u"page_progressbars")
        sizePolicy10.setHeightForWidth(self.page_progressbars.sizePolicy().hasHeightForWidth())
        self.page_progressbars.setSizePolicy(sizePolicy10)
        self.page_progressbars.setMinimumSize(QSize(20, 10))
        self.page_progressbars.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.gridLayout_6 = QGridLayout(self.page_progressbars)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.main_stacked_widget_top.addWidget(self.page_progressbars)

        self.main_verticallayout.addWidget(self.main_stacked_widget_top)

        self.main_horizontallayout_tree_buttons = QHBoxLayout()
        self.main_horizontallayout_tree_buttons.setObjectName(u"main_horizontallayout_tree_buttons")
        self.treewidget_button_downloads = QPushButton(self.page_main)
        self.treewidget_button_downloads.setObjectName(u"treewidget_button_downloads")

        self.main_horizontallayout_tree_buttons.addWidget(self.treewidget_button_downloads)

        self.treewidget_button_advanced_configuration = QPushButton(self.page_main)
        self.treewidget_button_advanced_configuration.setObjectName(u"treewidget_button_advanced_configuration")

        self.main_horizontallayout_tree_buttons.addWidget(self.treewidget_button_advanced_configuration)

        self.treewidget_button_stop = QPushButton(self.page_main)
        self.treewidget_button_stop.setObjectName(u"treewidget_button_stop")
        sizePolicy.setHeightForWidth(self.treewidget_button_stop.sizePolicy().hasHeightForWidth())
        self.treewidget_button_stop.setSizePolicy(sizePolicy)
        self.treewidget_button_stop.setMinimumSize(QSize(0, 30))
        self.treewidget_button_stop.setFont(font1)
        self.treewidget_button_stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.main_horizontallayout_tree_buttons.addWidget(self.treewidget_button_stop)


        self.main_verticallayout.addLayout(self.main_horizontallayout_tree_buttons)

        self.main_stacked_widget_tree = QStackedWidget(self.page_main)
        self.main_stacked_widget_tree.setObjectName(u"main_stacked_widget_tree")
        self.page_downloads = QWidget()
        self.page_downloads.setObjectName(u"page_downloads")
        self.gridLayout = QGridLayout(self.page_downloads)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.main_scrollarea_treewidget = QScrollArea(self.page_downloads)
        self.main_scrollarea_treewidget.setObjectName(u"main_scrollarea_treewidget")
        self.main_scrollarea_treewidget.setWidgetResizable(True)
        self.main_scrollarea_treewidget_content = QWidget()
        self.main_scrollarea_treewidget_content.setObjectName(u"main_scrollarea_treewidget_content")
        self.main_scrollarea_treewidget_content.setGeometry(QRect(0, 0, 300, 16))
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.main_scrollarea_treewidget_content.sizePolicy().hasHeightForWidth())
        self.main_scrollarea_treewidget_content.setSizePolicy(sizePolicy16)
        self.gridLayout_4 = QGridLayout(self.main_scrollarea_treewidget_content)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.main_tree_widget = QTreeWidget(self.main_scrollarea_treewidget_content)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.main_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.main_tree_widget.setObjectName(u"main_tree_widget")
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.main_tree_widget.sizePolicy().hasHeightForWidth())
        self.main_tree_widget.setSizePolicy(sizePolicy17)
        self.main_tree_widget.setMinimumSize(QSize(300, 10))

        self.gridLayout_4.addWidget(self.main_tree_widget, 0, 0, 1, 1)

        self.main_scrollarea_treewidget.setWidget(self.main_scrollarea_treewidget_content)

        self.gridLayout.addWidget(self.main_scrollarea_treewidget, 0, 0, 1, 1)

        self.main_stacked_widget_tree.addWidget(self.page_downloads)
        self.page_advanced_configuration = QWidget()
        self.page_advanced_configuration.setObjectName(u"page_advanced_configuration")
        self.gridLayout_12 = QGridLayout(self.page_advanced_configuration)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.tree_advanced_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_12.addItem(self.tree_advanced_vertical_spacer, 3, 0, 1, 1)

        self.tree_avanced_gridlayout = QGridLayout()
        self.tree_avanced_gridlayout.setObjectName(u"tree_avanced_gridlayout")
        self.tree_advanced_hlayout_2 = QHBoxLayout()
        self.tree_advanced_hlayout_2.setObjectName(u"tree_advanced_hlayout_2")
        self.tree_advanced_label_index_end = QLabel(self.page_advanced_configuration)
        self.tree_advanced_label_index_end.setObjectName(u"tree_advanced_label_index_end")
        sizePolicy18 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy18.setHorizontalStretch(0)
        sizePolicy18.setVerticalStretch(0)
        sizePolicy18.setHeightForWidth(self.tree_advanced_label_index_end.sizePolicy().hasHeightForWidth())
        self.tree_advanced_label_index_end.setSizePolicy(sizePolicy18)

        self.tree_advanced_hlayout_2.addWidget(self.tree_advanced_label_index_end)

        self.tree_advanced_spinbox_index_fetching_end = QSpinBox(self.page_advanced_configuration)
        self.tree_advanced_spinbox_index_fetching_end.setObjectName(u"tree_advanced_spinbox_index_fetching_end")

        self.tree_advanced_hlayout_2.addWidget(self.tree_advanced_spinbox_index_fetching_end)


        self.tree_avanced_gridlayout.addLayout(self.tree_advanced_hlayout_2, 4, 1, 1, 1)

        self.tree_advanced_hlayout_3 = QHBoxLayout()
        self.tree_advanced_hlayout_3.setObjectName(u"tree_advanced_hlayout_3")
        self.tree_advanced_label_custom_title = QLabel(self.page_advanced_configuration)
        self.tree_advanced_label_custom_title.setObjectName(u"tree_advanced_label_custom_title")

        self.tree_advanced_hlayout_3.addWidget(self.tree_advanced_label_custom_title)

        self.tree_advanced_lineedit_custom_title = QLineEdit(self.page_advanced_configuration)
        self.tree_advanced_lineedit_custom_title.setObjectName(u"tree_advanced_lineedit_custom_title")

        self.tree_advanced_hlayout_3.addWidget(self.tree_advanced_lineedit_custom_title)

        self.tree_advanced_button_custom_title_options = QPushButton(self.page_advanced_configuration)
        self.tree_advanced_button_custom_title_options.setObjectName(u"tree_advanced_button_custom_title_options")

        self.tree_advanced_hlayout_3.addWidget(self.tree_advanced_button_custom_title_options)


        self.tree_avanced_gridlayout.addLayout(self.tree_advanced_hlayout_3, 5, 0, 1, 2)

        self.tree_advanced_checkbox_cleanup_on_stop = QCheckBox(self.page_advanced_configuration)
        self.tree_advanced_checkbox_cleanup_on_stop.setObjectName(u"tree_advanced_checkbox_cleanup_on_stop")

        self.tree_avanced_gridlayout.addWidget(self.tree_advanced_checkbox_cleanup_on_stop, 1, 1, 1, 1)

        self.tree_advanced_checkbox_do_not_clear_videos = QCheckBox(self.page_advanced_configuration)
        self.tree_advanced_checkbox_do_not_clear_videos.setObjectName(u"tree_advanced_checkbox_do_not_clear_videos")
        sizePolicy.setHeightForWidth(self.tree_advanced_checkbox_do_not_clear_videos.sizePolicy().hasHeightForWidth())
        self.tree_advanced_checkbox_do_not_clear_videos.setSizePolicy(sizePolicy)
        self.tree_advanced_checkbox_do_not_clear_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tree_avanced_gridlayout.addWidget(self.tree_advanced_checkbox_do_not_clear_videos, 1, 0, 1, 1)

        self.tree_advanced_hlayout_1 = QHBoxLayout()
        self.tree_advanced_hlayout_1.setObjectName(u"tree_advanced_hlayout_1")
        self.tree_advanced_label_tooltip_index_videos = QLabel(self.page_advanced_configuration)
        self.tree_advanced_label_tooltip_index_videos.setObjectName(u"tree_advanced_label_tooltip_index_videos")
        sizePolicy18.setHeightForWidth(self.tree_advanced_label_tooltip_index_videos.sizePolicy().hasHeightForWidth())
        self.tree_advanced_label_tooltip_index_videos.setSizePolicy(sizePolicy18)

        self.tree_advanced_hlayout_1.addWidget(self.tree_advanced_label_tooltip_index_videos)

        self.tree_advanced_label_index_start = QLabel(self.page_advanced_configuration)
        self.tree_advanced_label_index_start.setObjectName(u"tree_advanced_label_index_start")
        sizePolicy18.setHeightForWidth(self.tree_advanced_label_index_start.sizePolicy().hasHeightForWidth())
        self.tree_advanced_label_index_start.setSizePolicy(sizePolicy18)

        self.tree_advanced_hlayout_1.addWidget(self.tree_advanced_label_index_start)

        self.tree_advanced_spinbox_index_fetching_start = QSpinBox(self.page_advanced_configuration)
        self.tree_advanced_spinbox_index_fetching_start.setObjectName(u"tree_advanced_spinbox_index_fetching_start")

        self.tree_advanced_hlayout_1.addWidget(self.tree_advanced_spinbox_index_fetching_start)


        self.tree_avanced_gridlayout.addLayout(self.tree_advanced_hlayout_1, 4, 0, 1, 1)

        self.tree_advanced_button_keyboard_shortcuts = QPushButton(self.page_advanced_configuration)
        self.tree_advanced_button_keyboard_shortcuts.setObjectName(u"tree_advanced_button_keyboard_shortcuts")
        sizePolicy.setHeightForWidth(self.tree_advanced_button_keyboard_shortcuts.sizePolicy().hasHeightForWidth())
        self.tree_advanced_button_keyboard_shortcuts.setSizePolicy(sizePolicy)
        self.tree_advanced_button_keyboard_shortcuts.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tree_avanced_gridlayout.addWidget(self.tree_advanced_button_keyboard_shortcuts, 6, 0, 1, 2)


        self.gridLayout_12.addLayout(self.tree_avanced_gridlayout, 0, 0, 1, 1)

        self.main_stacked_widget_tree.addWidget(self.page_advanced_configuration)

        self.main_verticallayout.addWidget(self.main_stacked_widget_tree)


        self.gridLayout_9.addLayout(self.main_verticallayout, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_main)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        sizePolicy.setHeightForWidth(self.page_settings.sizePolicy().hasHeightForWidth())
        self.page_settings.setSizePolicy(sizePolicy)
        self.gridLayout_7 = QGridLayout(self.page_settings)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.settings_scrollarea = QScrollArea(self.page_settings)
        self.settings_scrollarea.setObjectName(u"settings_scrollarea")
        sizePolicy.setHeightForWidth(self.settings_scrollarea.sizePolicy().hasHeightForWidth())
        self.settings_scrollarea.setSizePolicy(sizePolicy)
        self.settings_scrollarea.setWidgetResizable(True)
        self.settings_scrollarea_widget_contents = QWidget()
        self.settings_scrollarea_widget_contents.setObjectName(u"settings_scrollarea_widget_contents")
        self.settings_scrollarea_widget_contents.setGeometry(QRect(0, 0, 555, 332))
        self.gridLayout_19 = QGridLayout(self.settings_scrollarea_widget_contents)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.settings_vlayout_1 = QVBoxLayout()
        self.settings_vlayout_1.setObjectName(u"settings_vlayout_1")
        self.serttings_vlayout_buttons = QHBoxLayout()
        self.serttings_vlayout_buttons.setObjectName(u"serttings_vlayout_buttons")
        self.settings_button_switch_video = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_video.setObjectName(u"settings_button_switch_video")
        self.settings_button_switch_video.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.serttings_vlayout_buttons.addWidget(self.settings_button_switch_video)

        self.settings_button_switch_performance = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_performance.setObjectName(u"settings_button_switch_performance")
        self.settings_button_switch_performance.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.serttings_vlayout_buttons.addWidget(self.settings_button_switch_performance)

        self.settings_button_switch_system = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_system.setObjectName(u"settings_button_switch_system")
        self.settings_button_switch_system.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.serttings_vlayout_buttons.addWidget(self.settings_button_switch_system)

        self.settings_button_switch_ui = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_ui.setObjectName(u"settings_button_switch_ui")
        self.settings_button_switch_ui.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.serttings_vlayout_buttons.addWidget(self.settings_button_switch_ui)


        self.settings_vlayout_1.addLayout(self.serttings_vlayout_buttons)

        self.settings_stacked_widget_main = QStackedWidget(self.settings_scrollarea_widget_contents)
        self.settings_stacked_widget_main.setObjectName(u"settings_stacked_widget_main")
        sizePolicy19 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy19.setHorizontalStretch(0)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.settings_stacked_widget_main.sizePolicy().hasHeightForWidth())
        self.settings_stacked_widget_main.setSizePolicy(sizePolicy19)
        self.page_video = QWidget()
        self.page_video.setObjectName(u"page_video")
        sizePolicy19.setHeightForWidth(self.page_video.sizePolicy().hasHeightForWidth())
        self.page_video.setSizePolicy(sizePolicy19)
        self.gridLayout_14 = QGridLayout(self.page_video)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.settings_gridlayout_video = QGridLayout()
        self.settings_gridlayout_video.setObjectName(u"settings_gridlayout_video")
        self.settings_video_combobox_quality = QComboBox(self.page_video)
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.addItem("")
        self.settings_video_combobox_quality.setObjectName(u"settings_video_combobox_quality")
        self.settings_video_combobox_quality.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_video_combobox_quality, 0, 2, 1, 4)

        self.settings_button_videos_open_output_path = QPushButton(self.page_video)
        self.settings_button_videos_open_output_path.setObjectName(u"settings_button_videos_open_output_path")
        self.settings_button_videos_open_output_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_button_videos_open_output_path, 3, 5, 1, 1)

        self.settings_video_combobox_model_videos = QComboBox(self.page_video)
        self.settings_video_combobox_model_videos.addItem("")
        self.settings_video_combobox_model_videos.addItem("")
        self.settings_video_combobox_model_videos.addItem("")
        self.settings_video_combobox_model_videos.setObjectName(u"settings_video_combobox_model_videos")
        self.settings_video_combobox_model_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_video_combobox_model_videos, 1, 2, 1, 4)

        self.settings_label_videos_quality = QLabel(self.page_video)
        self.settings_label_videos_quality.setObjectName(u"settings_label_videos_quality")
        sizePolicy10.setHeightForWidth(self.settings_label_videos_quality.sizePolicy().hasHeightForWidth())
        self.settings_label_videos_quality.setSizePolicy(sizePolicy10)

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_quality, 0, 1, 1, 1)

        self.label_tooltip_model_videos = QLabel(self.page_video)
        self.label_tooltip_model_videos.setObjectName(u"label_tooltip_model_videos")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_model_videos, 1, 0, 1, 1)

        self.label_tooltip_quality = QLabel(self.page_video)
        self.label_tooltip_quality.setObjectName(u"label_tooltip_quality")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_quality, 0, 0, 1, 1)

        self.label_tooltip_result_limit = QLabel(self.page_video)
        self.label_tooltip_result_limit.setObjectName(u"label_tooltip_result_limit")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_result_limit, 2, 0, 1, 1)

        self.settings_spinbox_videos_result_limit = QSpinBox(self.page_video)
        self.settings_spinbox_videos_result_limit.setObjectName(u"settings_spinbox_videos_result_limit")
        self.settings_spinbox_videos_result_limit.setMinimum(1)
        self.settings_spinbox_videos_result_limit.setMaximum(5000)

        self.settings_gridlayout_video.addWidget(self.settings_spinbox_videos_result_limit, 2, 2, 1, 4)

        self.settings_label_videos_model_vdeos_type = QLabel(self.page_video)
        self.settings_label_videos_model_vdeos_type.setObjectName(u"settings_label_videos_model_vdeos_type")

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_model_vdeos_type, 1, 1, 1, 1)

        self.settings_label_videos_result_limit = QLabel(self.page_video)
        self.settings_label_videos_result_limit.setObjectName(u"settings_label_videos_result_limit")

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_result_limit, 2, 1, 1, 1)

        self.label_tooltip_track_videos = QLabel(self.page_video)
        self.label_tooltip_track_videos.setObjectName(u"label_tooltip_track_videos")
        sizePolicy18.setHeightForWidth(self.label_tooltip_track_videos.sizePolicy().hasHeightForWidth())
        self.label_tooltip_track_videos.setSizePolicy(sizePolicy18)

        self.settings_gridlayout_video.addWidget(self.label_tooltip_track_videos, 5, 0, 1, 1)

        self.settings_checkbox_videos_track_downloaded_videos = QCheckBox(self.page_video)
        self.settings_checkbox_videos_track_downloaded_videos.setObjectName(u"settings_checkbox_videos_track_downloaded_videos")

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_track_downloaded_videos, 5, 1, 1, 1)

        self.settings_checkbox_videos_write_metadata = QCheckBox(self.page_video)
        self.settings_checkbox_videos_write_metadata.setObjectName(u"settings_checkbox_videos_write_metadata")
        self.settings_checkbox_videos_write_metadata.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_write_metadata, 4, 1, 1, 1)

        self.label_tooltip_write_metadata = QLabel(self.page_video)
        self.label_tooltip_write_metadata.setObjectName(u"label_tooltip_write_metadata")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_write_metadata, 4, 0, 1, 1)

        self.settings_label_videos_output_path = QLabel(self.page_video)
        self.settings_label_videos_output_path.setObjectName(u"settings_label_videos_output_path")

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_output_path, 3, 1, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_tooltip_use_directory_system = QLabel(self.page_video)
        self.label_tooltip_use_directory_system.setObjectName(u"label_tooltip_use_directory_system")

        self.horizontalLayout_6.addWidget(self.label_tooltip_use_directory_system)

        self.settings_checkbox_videos_use_directory_system = QCheckBox(self.page_video)
        self.settings_checkbox_videos_use_directory_system.setObjectName(u"settings_checkbox_videos_use_directory_system")
        self.settings_checkbox_videos_use_directory_system.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_6.addWidget(self.settings_checkbox_videos_use_directory_system)

        self.label_tooltip_skip_existing_files = QLabel(self.page_video)
        self.label_tooltip_skip_existing_files.setObjectName(u"label_tooltip_skip_existing_files")

        self.horizontalLayout_6.addWidget(self.label_tooltip_skip_existing_files)

        self.settings_checkbox_videos_skip_existing_files = QCheckBox(self.page_video)
        self.settings_checkbox_videos_skip_existing_files.setObjectName(u"settings_checkbox_videos_skip_existing_files")
        self.settings_checkbox_videos_skip_existing_files.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_6.addWidget(self.settings_checkbox_videos_skip_existing_files)


        self.settings_gridlayout_video.addLayout(self.horizontalLayout_6, 4, 2, 1, 4)

        self.settings_lineedit_videos_database_path = QLineEdit(self.page_video)
        self.settings_lineedit_videos_database_path.setObjectName(u"settings_lineedit_videos_database_path")

        self.settings_gridlayout_video.addWidget(self.settings_lineedit_videos_database_path, 5, 2, 1, 4)

        self.settings_lineedit_videos_output_path = QLineEdit(self.page_video)
        self.settings_lineedit_videos_output_path.setObjectName(u"settings_lineedit_videos_output_path")
        sizePolicy7.setHeightForWidth(self.settings_lineedit_videos_output_path.sizePolicy().hasHeightForWidth())
        self.settings_lineedit_videos_output_path.setSizePolicy(sizePolicy7)

        self.settings_gridlayout_video.addWidget(self.settings_lineedit_videos_output_path, 3, 2, 1, 3)


        self.gridLayout_14.addLayout(self.settings_gridlayout_video, 0, 0, 1, 1)

        self.settings_stacked_widget_main.addWidget(self.page_video)
        self.page_performance = QWidget()
        self.page_performance.setObjectName(u"page_performance")
        sizePolicy19.setHeightForWidth(self.page_performance.sizePolicy().hasHeightForWidth())
        self.page_performance.setSizePolicy(sizePolicy19)
        self.gridLayout_26 = QGridLayout(self.page_performance)
        self.gridLayout_26.setSpacing(0)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.settings_gridlayout_performance = QGridLayout()
        self.settings_gridlayout_performance.setObjectName(u"settings_gridlayout_performance")
        self.settings_label_performance_speed_limit = QLabel(self.page_performance)
        self.settings_label_performance_speed_limit.setObjectName(u"settings_label_performance_speed_limit")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_speed_limit, 7, 1, 1, 1)

        self.label_tooltip_maximum_timeout = QLabel(self.page_performance)
        self.label_tooltip_maximum_timeout.setObjectName(u"label_tooltip_maximum_timeout")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_maximum_timeout, 5, 0, 1, 1)

        self.label_tooltip_pages_concurrency = QLabel(self.page_performance)
        self.label_tooltip_pages_concurrency.setObjectName(u"label_tooltip_pages_concurrency")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_pages_concurrency, 8, 0, 1, 1)

        self.settings_label_performance_processing_delay = QLabel(self.page_performance)
        self.settings_label_performance_processing_delay.setObjectName(u"settings_label_performance_processing_delay")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_processing_delay, 5, 4, 1, 1)

        self.settings_label_performance_pages_concurrency = QLabel(self.page_performance)
        self.settings_label_performance_pages_concurrency.setObjectName(u"settings_label_performance_pages_concurrency")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_pages_concurrency, 8, 1, 1, 1)

        self.settings_spinbox_performance_simultaneous_downloads = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_simultaneous_downloads.setObjectName(u"settings_spinbox_performance_simultaneous_downloads")
        self.settings_spinbox_performance_simultaneous_downloads.setMinimum(1)
        self.settings_spinbox_performance_simultaneous_downloads.setMaximum(5000)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_simultaneous_downloads, 2, 2, 1, 1)

        self.settings_spinbox_performance_network_delay = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_network_delay.setObjectName(u"settings_spinbox_performance_network_delay")
        self.settings_spinbox_performance_network_delay.setMinimum(0)
        self.settings_spinbox_performance_network_delay.setMaximum(5000)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_network_delay, 0, 5, 1, 1)

        self.label_tooltip_simultaneous_downloads = QLabel(self.page_performance)
        self.label_tooltip_simultaneous_downloads.setObjectName(u"label_tooltip_simultaneous_downloads")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_simultaneous_downloads, 2, 0, 1, 1)

        self.settings_spinbox_performance_maximal_retries = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_maximal_retries.setObjectName(u"settings_spinbox_performance_maximal_retries")
        self.settings_spinbox_performance_maximal_retries.setMinimum(5)
        self.settings_spinbox_performance_maximal_retries.setMaximum(5000)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_maximal_retries, 2, 5, 1, 1)

        self.label_tooltip_speed_limit = QLabel(self.page_performance)
        self.label_tooltip_speed_limit.setObjectName(u"label_tooltip_speed_limit")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_speed_limit, 7, 0, 1, 1)

        self.settings_label_performance_maximal_retries = QLabel(self.page_performance)
        self.settings_label_performance_maximal_retries.setObjectName(u"settings_label_performance_maximal_retries")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_maximal_retries, 2, 4, 1, 1)

        self.settings_doublespinbox_performance_speed_limit = QDoubleSpinBox(self.page_performance)
        self.settings_doublespinbox_performance_speed_limit.setObjectName(u"settings_doublespinbox_performance_speed_limit")

        self.settings_gridlayout_performance.addWidget(self.settings_doublespinbox_performance_speed_limit, 7, 2, 1, 1)

        self.settings_spinbox_performance_videos_concurrency = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_videos_concurrency.setObjectName(u"settings_spinbox_performance_videos_concurrency")
        self.settings_spinbox_performance_videos_concurrency.setMinimum(1)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_videos_concurrency, 7, 5, 1, 1)

        self.label_tooltip_download_mode = QLabel(self.page_performance)
        self.label_tooltip_download_mode.setObjectName(u"label_tooltip_download_mode")
        sizePolicy18.setHeightForWidth(self.label_tooltip_download_mode.sizePolicy().hasHeightForWidth())
        self.label_tooltip_download_mode.setSizePolicy(sizePolicy18)

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_download_mode, 0, 0, 1, 1)

        self.settings_spinbox_performance_pages_concurrency = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_pages_concurrency.setObjectName(u"settings_spinbox_performance_pages_concurrency")
        self.settings_spinbox_performance_pages_concurrency.setMinimum(1)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_pages_concurrency, 8, 2, 1, 1)

        self.settings_spinbox_performance_processing_delay = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_processing_delay.setObjectName(u"settings_spinbox_performance_processing_delay")
        self.settings_spinbox_performance_processing_delay.setMinimum(1)
        self.settings_spinbox_performance_processing_delay.setMaximum(500)
        self.settings_spinbox_performance_processing_delay.setValue(1)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_processing_delay, 5, 5, 1, 1)

        self.settings_label_performance_simultaneous_download = QLabel(self.page_performance)
        self.settings_label_performance_simultaneous_download.setObjectName(u"settings_label_performance_simultaneous_download")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_simultaneous_download, 2, 1, 1, 1)

        self.settings_label_performance_maximal_timeout = QLabel(self.page_performance)
        self.settings_label_performance_maximal_timeout.setObjectName(u"settings_label_performance_maximal_timeout")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_maximal_timeout, 5, 1, 1, 1)

        self.settings_label_performance_videos_concurrency = QLabel(self.page_performance)
        self.settings_label_performance_videos_concurrency.setObjectName(u"settings_label_performance_videos_concurrency")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_videos_concurrency, 7, 4, 1, 1)

        self.settings_spinbox_performance_maximal_timeout = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_maximal_timeout.setObjectName(u"settings_spinbox_performance_maximal_timeout")
        self.settings_spinbox_performance_maximal_timeout.setMinimum(5)
        self.settings_spinbox_performance_maximal_timeout.setMaximum(5000)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_maximal_timeout, 5, 2, 1, 1)

        self.settings_label_performance_network_delay = QLabel(self.page_performance)
        self.settings_label_performance_network_delay.setObjectName(u"settings_label_performance_network_delay")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_network_delay, 0, 4, 1, 1)

        self.label_tooltip_network_delay = QLabel(self.page_performance)
        self.label_tooltip_network_delay.setObjectName(u"label_tooltip_network_delay")
        sizePolicy18.setHeightForWidth(self.label_tooltip_network_delay.sizePolicy().hasHeightForWidth())
        self.label_tooltip_network_delay.setSizePolicy(sizePolicy18)

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_network_delay, 0, 3, 1, 1)

        self.label_tooltip_processing_delay = QLabel(self.page_performance)
        self.label_tooltip_processing_delay.setObjectName(u"label_tooltip_processing_delay")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_processing_delay, 5, 3, 1, 1)

        self.label_tooltip_videos_concurrency = QLabel(self.page_performance)
        self.label_tooltip_videos_concurrency.setObjectName(u"label_tooltip_videos_concurrency")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_videos_concurrency, 7, 3, 1, 1)

        self.label_tooltip_download_workers = QLabel(self.page_performance)
        self.label_tooltip_download_workers.setObjectName(u"label_tooltip_download_workers")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_download_workers, 8, 3, 1, 1)

        self.label_tooltip_maximum_retries = QLabel(self.page_performance)
        self.label_tooltip_maximum_retries.setObjectName(u"label_tooltip_maximum_retries")

        self.settings_gridlayout_performance.addWidget(self.label_tooltip_maximum_retries, 2, 3, 1, 1)

        self.label_settings_performance_download_workers = QLabel(self.page_performance)
        self.label_settings_performance_download_workers.setObjectName(u"label_settings_performance_download_workers")

        self.settings_gridlayout_performance.addWidget(self.label_settings_performance_download_workers, 0, 1, 1, 1)

        self.settings_spinbox_performance_download_workers = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_download_workers.setObjectName(u"settings_spinbox_performance_download_workers")
        self.settings_spinbox_performance_download_workers.setMinimum(1)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_download_workers, 0, 2, 1, 1)


        self.gridLayout_26.addLayout(self.settings_gridlayout_performance, 0, 0, 1, 1)

        self.settings_stacked_widget_main.addWidget(self.page_performance)
        self.page_system = QWidget()
        self.page_system.setObjectName(u"page_system")
        sizePolicy19.setHeightForWidth(self.page_system.sizePolicy().hasHeightForWidth())
        self.page_system.setSizePolicy(sizePolicy19)
        self.gridLayout_33 = QGridLayout(self.page_system)
        self.gridLayout_33.setSpacing(0)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setContentsMargins(0, 0, 0, 0)
        self.settings_gridlayout_system = QGridLayout()
        self.settings_gridlayout_system.setSpacing(0)
        self.settings_gridlayout_system.setObjectName(u"settings_gridlayout_system")
        self.label_tooltip_anonymous_mode = QLabel(self.page_system)
        self.label_tooltip_anonymous_mode.setObjectName(u"label_tooltip_anonymous_mode")

        self.settings_gridlayout_system.addWidget(self.label_tooltip_anonymous_mode, 1, 0, 1, 1)

        self.label_tooltip_ssl_context = QLabel(self.page_system)
        self.label_tooltip_ssl_context.setObjectName(u"label_tooltip_ssl_context")
        sizePolicy18.setHeightForWidth(self.label_tooltip_ssl_context.sizePolicy().hasHeightForWidth())
        self.label_tooltip_ssl_context.setSizePolicy(sizePolicy18)

        self.settings_gridlayout_system.addWidget(self.label_tooltip_ssl_context, 3, 2, 1, 1)

        self.settings_checkbox_use_truststore = QCheckBox(self.page_system)
        self.settings_checkbox_use_truststore.setObjectName(u"settings_checkbox_use_truststore")
        sizePolicy.setHeightForWidth(self.settings_checkbox_use_truststore.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_use_truststore.setSizePolicy(sizePolicy)

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_use_truststore, 3, 3, 1, 1)

        self.settings_checkbox_system_enable_anonymous_mode = QCheckBox(self.page_system)
        self.settings_checkbox_system_enable_anonymous_mode.setObjectName(u"settings_checkbox_system_enable_anonymous_mode")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_enable_anonymous_mode.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_enable_anonymous_mode.setSizePolicy(sizePolicy)
        self.settings_checkbox_system_enable_anonymous_mode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_enable_anonymous_mode, 1, 1, 1, 1)

        self.label_tooltip_supress_errors = QLabel(self.page_system)
        self.label_tooltip_supress_errors.setObjectName(u"label_tooltip_supress_errors")

        self.settings_gridlayout_system.addWidget(self.label_tooltip_supress_errors, 2, 0, 1, 1)

        self.label_tooltip_update_checks = QLabel(self.page_system)
        self.label_tooltip_update_checks.setObjectName(u"label_tooltip_update_checks")
        sizePolicy18.setHeightForWidth(self.label_tooltip_update_checks.sizePolicy().hasHeightForWidth())
        self.label_tooltip_update_checks.setSizePolicy(sizePolicy18)

        self.settings_gridlayout_system.addWidget(self.label_tooltip_update_checks, 0, 0, 1, 1)

        self.label_tooltip_network_logging = QLabel(self.page_system)
        self.label_tooltip_network_logging.setObjectName(u"label_tooltip_network_logging")

        self.settings_gridlayout_system.addWidget(self.label_tooltip_network_logging, 3, 0, 1, 1)

        self.settings_checkbox_system_proxy_kill_switch = QCheckBox(self.page_system)
        self.settings_checkbox_system_proxy_kill_switch.setObjectName(u"settings_checkbox_system_proxy_kill_switch")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_proxy_kill_switch.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_proxy_kill_switch.setSizePolicy(sizePolicy)
        self.settings_checkbox_system_proxy_kill_switch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_proxy_kill_switch, 1, 2, 1, 2)

        self.settings_checkbox_system_enable_debug_mode = QCheckBox(self.page_system)
        self.settings_checkbox_system_enable_debug_mode.setObjectName(u"settings_checkbox_system_enable_debug_mode")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_enable_debug_mode.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_enable_debug_mode.setSizePolicy(sizePolicy)

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_enable_debug_mode, 2, 2, 1, 2)

        self.settings_checkbox_system_enable_network_logging = QCheckBox(self.page_system)
        self.settings_checkbox_system_enable_network_logging.setObjectName(u"settings_checkbox_system_enable_network_logging")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_enable_network_logging.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_enable_network_logging.setSizePolicy(sizePolicy)
        self.settings_checkbox_system_enable_network_logging.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_enable_network_logging, 3, 1, 1, 1)

        self.settings_checkbox_system_supress_errors = QCheckBox(self.page_system)
        self.settings_checkbox_system_supress_errors.setObjectName(u"settings_checkbox_system_supress_errors")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_supress_errors.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_supress_errors.setSizePolicy(sizePolicy)
        self.settings_checkbox_system_supress_errors.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_supress_errors, 2, 1, 1, 1)

        self.settings_checkbox_system_activate_proxy = QCheckBox(self.page_system)
        self.settings_checkbox_system_activate_proxy.setObjectName(u"settings_checkbox_system_activate_proxy")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_activate_proxy.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_activate_proxy.setSizePolicy(sizePolicy)
        self.settings_checkbox_system_activate_proxy.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_activate_proxy, 0, 2, 1, 2)

        self.settings_checkbox_system_update_checks = QCheckBox(self.page_system)
        self.settings_checkbox_system_update_checks.setObjectName(u"settings_checkbox_system_update_checks")
        sizePolicy.setHeightForWidth(self.settings_checkbox_system_update_checks.sizePolicy().hasHeightForWidth())
        self.settings_checkbox_system_update_checks.setSizePolicy(sizePolicy)
        self.settings_checkbox_system_update_checks.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_update_checks, 0, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settings_gridlayout_system.addItem(self.verticalSpacer_3, 4, 3, 1, 1)


        self.gridLayout_33.addLayout(self.settings_gridlayout_system, 0, 0, 1, 1)

        self.settings_stacked_widget_main.addWidget(self.page_system)
        self.page_ui = QWidget()
        self.page_ui.setObjectName(u"page_ui")
        sizePolicy19.setHeightForWidth(self.page_ui.sizePolicy().hasHeightForWidth())
        self.page_ui.setSizePolicy(sizePolicy19)
        self.gridLayout_34 = QGridLayout(self.page_ui)
        self.gridLayout_34.setSpacing(0)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridLayout_34.setContentsMargins(0, 0, 0, 0)
        self.settings_gridlayout_ui = QGridLayout()
        self.settings_gridlayout_ui.setObjectName(u"settings_gridlayout_ui")
        self.settings_spinbox_ui_font_size = QSpinBox(self.page_ui)
        self.settings_spinbox_ui_font_size.setObjectName(u"settings_spinbox_ui_font_size")
        sizePolicy.setHeightForWidth(self.settings_spinbox_ui_font_size.sizePolicy().hasHeightForWidth())
        self.settings_spinbox_ui_font_size.setSizePolicy(sizePolicy)

        self.settings_gridlayout_ui.addWidget(self.settings_spinbox_ui_font_size, 1, 1, 1, 1)

        self.settings_combobox_ui_theme = QComboBox(self.page_ui)
        self.settings_combobox_ui_theme.addItem("")
        self.settings_combobox_ui_theme.addItem("")
        self.settings_combobox_ui_theme.addItem("")
        self.settings_combobox_ui_theme.setObjectName(u"settings_combobox_ui_theme")
        sizePolicy.setHeightForWidth(self.settings_combobox_ui_theme.sizePolicy().hasHeightForWidth())
        self.settings_combobox_ui_theme.setSizePolicy(sizePolicy)

        self.settings_gridlayout_ui.addWidget(self.settings_combobox_ui_theme, 2, 1, 1, 1)

        self.settings_label_ui_language = QLabel(self.page_ui)
        self.settings_label_ui_language.setObjectName(u"settings_label_ui_language")
        sizePolicy5.setHeightForWidth(self.settings_label_ui_language.sizePolicy().hasHeightForWidth())
        self.settings_label_ui_language.setSizePolicy(sizePolicy5)

        self.settings_gridlayout_ui.addWidget(self.settings_label_ui_language, 0, 0, 1, 1)

        self.settings_ui_combobox_language = QComboBox(self.page_ui)
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.setObjectName(u"settings_ui_combobox_language")
        sizePolicy.setHeightForWidth(self.settings_ui_combobox_language.sizePolicy().hasHeightForWidth())
        self.settings_ui_combobox_language.setSizePolicy(sizePolicy)
        self.settings_ui_combobox_language.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_ui.addWidget(self.settings_ui_combobox_language, 0, 1, 1, 1)

        self.settings_label_ui_theme = QLabel(self.page_ui)
        self.settings_label_ui_theme.setObjectName(u"settings_label_ui_theme")

        self.settings_gridlayout_ui.addWidget(self.settings_label_ui_theme, 2, 0, 1, 1)

        self.settings_label_ui_font_size = QLabel(self.page_ui)
        self.settings_label_ui_font_size.setObjectName(u"settings_label_ui_font_size")

        self.settings_gridlayout_ui.addWidget(self.settings_label_ui_font_size, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settings_gridlayout_ui.addItem(self.verticalSpacer_2, 3, 1, 1, 1)


        self.gridLayout_34.addLayout(self.settings_gridlayout_ui, 0, 0, 1, 1)

        self.settings_stacked_widget_main.addWidget(self.page_ui)

        self.settings_vlayout_1.addWidget(self.settings_stacked_widget_main)

        self.settings_hlayout_license = QHBoxLayout()
        self.settings_hlayout_license.setObjectName(u"settings_hlayout_license")
        self.settings_button_buy_license = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_buy_license.setObjectName(u"settings_button_buy_license")
        self.settings_button_buy_license.setStyleSheet(u"")

        self.settings_hlayout_license.addWidget(self.settings_button_buy_license)

        self.settings_button_import_license = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_import_license.setObjectName(u"settings_button_import_license")
        self.settings_button_import_license.setStyleSheet(u"")

        self.settings_hlayout_license.addWidget(self.settings_button_import_license)


        self.settings_vlayout_1.addLayout(self.settings_hlayout_license)

        self.settings_hlayout_apply = QHBoxLayout()
        self.settings_hlayout_apply.setObjectName(u"settings_hlayout_apply")
        self.settings_button_apply = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_apply.setObjectName(u"settings_button_apply")
        self.settings_button_apply.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_hlayout_apply.addWidget(self.settings_button_apply)

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

        self.settings_hlayout_apply.addWidget(self.settings_button_reset)


        self.settings_vlayout_1.addLayout(self.settings_hlayout_apply)

        self.settings_hlayout_install = QHBoxLayout()
        self.settings_hlayout_install.setObjectName(u"settings_hlayout_install")
        self.settings_button_system_install_pornfetch = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_system_install_pornfetch.setObjectName(u"settings_button_system_install_pornfetch")

        self.settings_hlayout_install.addWidget(self.settings_button_system_install_pornfetch)

        self.settings_button_uninstall_porn_fetch = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_uninstall_porn_fetch.setObjectName(u"settings_button_uninstall_porn_fetch")

        self.settings_hlayout_install.addWidget(self.settings_button_uninstall_porn_fetch)

        self.button_settings_clear_temp = QPushButton(self.settings_scrollarea_widget_contents)
        self.button_settings_clear_temp.setObjectName(u"button_settings_clear_temp")

        self.settings_hlayout_install.addWidget(self.button_settings_clear_temp)


        self.settings_vlayout_1.addLayout(self.settings_hlayout_install)

        self.settings_vertical_spacer_main = QSpacerItem(108, 98, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settings_vlayout_1.addItem(self.settings_vertical_spacer_main)


        self.gridLayout_19.addLayout(self.settings_vlayout_1, 1, 0, 1, 1)

        self.settings_scrollarea.setWidget(self.settings_scrollarea_widget_contents)

        self.gridLayout_7.addWidget(self.settings_scrollarea, 0, 1, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_settings)
        self.page_credits = QWidget()
        self.page_credits.setObjectName(u"page_credits")
        self.gridLayout_22 = QGridLayout(self.page_credits)
        self.gridLayout_22.setSpacing(0)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_credits = QScrollArea(self.page_credits)
        self.scrollarea_credits.setObjectName(u"scrollarea_credits")
        self.scrollarea_credits.setWidgetResizable(True)
        self.scrollarea_credits_widget_contents = QWidget()
        self.scrollarea_credits_widget_contents.setObjectName(u"scrollarea_credits_widget_contents")
        self.scrollarea_credits_widget_contents.setGeometry(QRect(0, 0, 219, 104))
        self.gridLayout_21 = QGridLayout(self.scrollarea_credits_widget_contents)
        self.gridLayout_21.setSpacing(0)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_credits_vboxlayout = QVBoxLayout()
        self.scrollarea_credits_vboxlayout.setObjectName(u"scrollarea_credits_vboxlayout")
        self.credits_button_send_feedback = QPushButton(self.scrollarea_credits_widget_contents)
        self.credits_button_send_feedback.setObjectName(u"credits_button_send_feedback")

        self.scrollarea_credits_vboxlayout.addWidget(self.credits_button_send_feedback)

        self.credits_textbrowser = QTextBrowser(self.scrollarea_credits_widget_contents)
        self.credits_textbrowser.setObjectName(u"credits_textbrowser")

        self.scrollarea_credits_vboxlayout.addWidget(self.credits_textbrowser)


        self.gridLayout_21.addLayout(self.scrollarea_credits_vboxlayout, 0, 1, 1, 1)

        self.scrollarea_credits.setWidget(self.scrollarea_credits_widget_contents)

        self.gridLayout_22.addWidget(self.scrollarea_credits, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_credits)
        self.page_license = QWidget()
        self.page_license.setObjectName(u"page_license")
        self.gridLayout_24 = QGridLayout(self.page_license)
        self.gridLayout_24.setSpacing(0)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_license_page = QScrollArea(self.page_license)
        self.scrollarea_license_page.setObjectName(u"scrollarea_license_page")
        self.scrollarea_license_page.setWidgetResizable(True)
        self.scrollarea_license_page_widget_contents = QWidget()
        self.scrollarea_license_page_widget_contents.setObjectName(u"scrollarea_license_page_widget_contents")
        self.scrollarea_license_page_widget_contents.setGeometry(QRect(0, 0, 218, 110))
        self.gridLayout_23 = QGridLayout(self.scrollarea_license_page_widget_contents)
        self.gridLayout_23.setSpacing(0)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_23.setContentsMargins(0, 0, 0, 0)
        self.license_button_deny = QPushButton(self.scrollarea_license_page_widget_contents)
        self.license_button_deny.setObjectName(u"license_button_deny")
        self.license_button_deny.setStyleSheet(u"QPushButton {\n"
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

        self.gridLayout_23.addWidget(self.license_button_deny, 1, 1, 1, 1)

        self.license_button_accept = QPushButton(self.scrollarea_license_page_widget_contents)
        self.license_button_accept.setObjectName(u"license_button_accept")
        self.license_button_accept.setStyleSheet(u"QPushButton {\n"
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

        self.gridLayout_23.addWidget(self.license_button_accept, 1, 0, 1, 1)

        self.license_textbrowser = QTextBrowser(self.scrollarea_license_page_widget_contents)
        self.license_textbrowser.setObjectName(u"license_textbrowser")
        font4 = QFont()
        font4.setFamilies([u"JetBrainsMono Nerd Font Propo"])
        font4.setPointSize(11)
        font4.setKerning(True)
        self.license_textbrowser.setFont(font4)
        self.license_textbrowser.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)
        self.license_textbrowser.setOpenExternalLinks(True)

        self.gridLayout_23.addWidget(self.license_textbrowser, 0, 0, 1, 2)

        self.scrollarea_license_page.setWidget(self.scrollarea_license_page_widget_contents)

        self.gridLayout_24.addWidget(self.scrollarea_license_page, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_license)
        self.page_keyboard_shortcuts = QWidget()
        self.page_keyboard_shortcuts.setObjectName(u"page_keyboard_shortcuts")
        self.gridLayout_55 = QGridLayout(self.page_keyboard_shortcuts)
        self.gridLayout_55.setSpacing(0)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.gridLayout_55.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_keyboard_shortcuts = QScrollArea(self.page_keyboard_shortcuts)
        self.scrollarea_keyboard_shortcuts.setObjectName(u"scrollarea_keyboard_shortcuts")
        self.scrollarea_keyboard_shortcuts.setWidgetResizable(True)
        self.scrollarea_keyboard_shortcuts_widget_contents = QWidget()
        self.scrollarea_keyboard_shortcuts_widget_contents.setObjectName(u"scrollarea_keyboard_shortcuts_widget_contents")
        self.scrollarea_keyboard_shortcuts_widget_contents.setGeometry(QRect(0, 0, 256, 192))
        self.gridLayout_54 = QGridLayout(self.scrollarea_keyboard_shortcuts_widget_contents)
        self.gridLayout_54.setSpacing(0)
        self.gridLayout_54.setObjectName(u"gridLayout_54")
        self.gridLayout_54.setContentsMargins(0, 0, 0, 0)
        self.keyboard_shortcuts_text_browser = QTextBrowser(self.scrollarea_keyboard_shortcuts_widget_contents)
        self.keyboard_shortcuts_text_browser.setObjectName(u"keyboard_shortcuts_text_browser")
        sizePolicy17.setHeightForWidth(self.keyboard_shortcuts_text_browser.sizePolicy().hasHeightForWidth())
        self.keyboard_shortcuts_text_browser.setSizePolicy(sizePolicy17)
        self.keyboard_shortcuts_text_browser.setMaximumSize(QSize(200000, 200000))

        self.gridLayout_54.addWidget(self.keyboard_shortcuts_text_browser, 0, 0, 1, 1)

        self.scrollarea_keyboard_shortcuts.setWidget(self.scrollarea_keyboard_shortcuts_widget_contents)

        self.gridLayout_55.addWidget(self.scrollarea_keyboard_shortcuts, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_keyboard_shortcuts)
        self.page_install_dialog = QWidget()
        self.page_install_dialog.setObjectName(u"page_install_dialog")
        self.gridLayout_57 = QGridLayout(self.page_install_dialog)
        self.gridLayout_57.setSpacing(0)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.gridLayout_57.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_install_dialog = QScrollArea(self.page_install_dialog)
        self.scrollarea_install_dialog.setObjectName(u"scrollarea_install_dialog")
        self.scrollarea_install_dialog.setWidgetResizable(True)
        self.scrollarea_install_dialog_widget_contents = QWidget()
        self.scrollarea_install_dialog_widget_contents.setObjectName(u"scrollarea_install_dialog_widget_contents")
        self.scrollarea_install_dialog_widget_contents.setGeometry(QRect(0, 0, 170, 140))
        self.gridLayout_56 = QGridLayout(self.scrollarea_install_dialog_widget_contents)
        self.gridLayout_56.setSpacing(0)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.gridLayout_56.setContentsMargins(0, 0, 0, 0)
        self.install_dialog_vertical_layout = QVBoxLayout()
        self.install_dialog_vertical_layout.setObjectName(u"install_dialog_vertical_layout")
        self.install_dialog_text_browser = QTextBrowser(self.scrollarea_install_dialog_widget_contents)
        self.install_dialog_text_browser.setObjectName(u"install_dialog_text_browser")

        self.install_dialog_vertical_layout.addWidget(self.install_dialog_text_browser)

        self.install_dialog_horizontal_layout = QHBoxLayout()
        self.install_dialog_horizontal_layout.setObjectName(u"install_dialog_horizontal_layout")
        self.install_dialog_label_custom_app_name = QLabel(self.scrollarea_install_dialog_widget_contents)
        self.install_dialog_label_custom_app_name.setObjectName(u"install_dialog_label_custom_app_name")

        self.install_dialog_horizontal_layout.addWidget(self.install_dialog_label_custom_app_name)

        self.install_dialog_lineedit_custom_app_name = QLineEdit(self.scrollarea_install_dialog_widget_contents)
        self.install_dialog_lineedit_custom_app_name.setObjectName(u"install_dialog_lineedit_custom_app_name")

        self.install_dialog_horizontal_layout.addWidget(self.install_dialog_lineedit_custom_app_name)


        self.install_dialog_vertical_layout.addLayout(self.install_dialog_horizontal_layout)

        self.horizontallayout_buttons = QHBoxLayout()
        self.horizontallayout_buttons.setObjectName(u"horizontallayout_buttons")
        self.button_install = QPushButton(self.scrollarea_install_dialog_widget_contents)
        self.button_install.setObjectName(u"button_install")

        self.horizontallayout_buttons.addWidget(self.button_install)

        self.button_portable = QPushButton(self.scrollarea_install_dialog_widget_contents)
        self.button_portable.setObjectName(u"button_portable")

        self.horizontallayout_buttons.addWidget(self.button_portable)


        self.install_dialog_vertical_layout.addLayout(self.horizontallayout_buttons)


        self.gridLayout_56.addLayout(self.install_dialog_vertical_layout, 0, 0, 1, 1)

        self.scrollarea_install_dialog.setWidget(self.scrollarea_install_dialog_widget_contents)

        self.gridLayout_57.addWidget(self.scrollarea_install_dialog, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_install_dialog)
        self.page_supported_websites = QWidget()
        self.page_supported_websites.setObjectName(u"page_supported_websites")
        self.gridLayout_18 = QGridLayout(self.page_supported_websites)
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_supported_websites = QScrollArea(self.page_supported_websites)
        self.scrollarea_supported_websites.setObjectName(u"scrollarea_supported_websites")
        self.scrollarea_supported_websites.setWidgetResizable(True)
        self.scrollarea_supported_sites_widget_contents = QWidget()
        self.scrollarea_supported_sites_widget_contents.setObjectName(u"scrollarea_supported_sites_widget_contents")
        self.scrollarea_supported_sites_widget_contents.setGeometry(QRect(0, 0, 84, 70))
        self.gridLayout_20 = QGridLayout(self.scrollarea_supported_sites_widget_contents)
        self.gridLayout_20.setSpacing(0)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.gridLayout_20.setContentsMargins(0, 0, 0, 0)
        self.supported_sites_textbrowser = QTextBrowser(self.scrollarea_supported_sites_widget_contents)
        self.supported_sites_textbrowser.setObjectName(u"supported_sites_textbrowser")
        self.supported_sites_textbrowser.setOpenExternalLinks(True)

        self.gridLayout_20.addWidget(self.supported_sites_textbrowser, 0, 0, 1, 1)

        self.scrollarea_supported_websites.setWidget(self.scrollarea_supported_sites_widget_contents)

        self.gridLayout_18.addWidget(self.scrollarea_supported_websites, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_supported_websites)
        self.page_disclaimer = QWidget()
        self.page_disclaimer.setObjectName(u"page_disclaimer")
        self.gridLayout_62 = QGridLayout(self.page_disclaimer)
        self.gridLayout_62.setSpacing(0)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.gridLayout_62.setContentsMargins(0, 0, 0, 0)
        self.scrollarea_disclaimer = QScrollArea(self.page_disclaimer)
        self.scrollarea_disclaimer.setObjectName(u"scrollarea_disclaimer")
        self.scrollarea_disclaimer.setWidgetResizable(True)
        self.scrollarea_disclaimer_widget_contents = QWidget()
        self.scrollarea_disclaimer_widget_contents.setObjectName(u"scrollarea_disclaimer_widget_contents")
        self.scrollarea_disclaimer_widget_contents.setGeometry(QRect(0, 0, 98, 120))
        self.gridLayout_61 = QGridLayout(self.scrollarea_disclaimer_widget_contents)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.disclaimer_textbrowser = QTextBrowser(self.scrollarea_disclaimer_widget_contents)
        self.disclaimer_textbrowser.setObjectName(u"disclaimer_textbrowser")

        self.gridLayout_61.addWidget(self.disclaimer_textbrowser, 0, 0, 1, 1)

        self.disclaimer_button_accept = QPushButton(self.scrollarea_disclaimer_widget_contents)
        self.disclaimer_button_accept.setObjectName(u"disclaimer_button_accept")

        self.gridLayout_61.addWidget(self.disclaimer_button_accept, 1, 0, 1, 1)

        self.scrollarea_disclaimer.setWidget(self.scrollarea_disclaimer_widget_contents)

        self.gridLayout_62.addWidget(self.scrollarea_disclaimer, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_disclaimer)
        self.page_one_time_setup = QWidget()
        self.page_one_time_setup.setObjectName(u"page_one_time_setup")
        self.gridLayout_35 = QGridLayout(self.page_one_time_setup)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.vbox_info = QVBoxLayout()
        self.vbox_info.setObjectName(u"vbox_info")

        self.gridLayout_35.addLayout(self.vbox_info, 0, 0, 1, 1)

        self.one_time_setup_gridlayout = QGridLayout()
        self.one_time_setup_gridlayout.setObjectName(u"one_time_setup_gridlayout")
        self.one_time_setup_button_info_enable_all = QPushButton(self.page_one_time_setup)
        self.one_time_setup_button_info_enable_all.setObjectName(u"one_time_setup_button_info_enable_all")

        self.one_time_setup_gridlayout.addWidget(self.one_time_setup_button_info_enable_all, 0, 0, 1, 1)

        self.one_time_setup_button_info_enable_update = QPushButton(self.page_one_time_setup)
        self.one_time_setup_button_info_enable_update.setObjectName(u"one_time_setup_button_info_enable_update")

        self.one_time_setup_gridlayout.addWidget(self.one_time_setup_button_info_enable_update, 0, 1, 1, 1)

        self.one_time_setup_button_info_disable_all = QPushButton(self.page_one_time_setup)
        self.one_time_setup_button_info_disable_all.setObjectName(u"one_time_setup_button_info_disable_all")

        self.one_time_setup_gridlayout.addWidget(self.one_time_setup_button_info_disable_all, 0, 2, 1, 1)


        self.gridLayout_35.addLayout(self.one_time_setup_gridlayout, 1, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_one_time_setup)
        self.page_update_available = QWidget()
        self.page_update_available.setObjectName(u"page_update_available")
        self.gridLayout_28 = QGridLayout(self.page_update_available)
        self.gridLayout_28.setSpacing(0)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_28.setContentsMargins(0, 0, 0, 0)
        self.update_available_gridlayout = QGridLayout()
        self.update_available_gridlayout.setObjectName(u"update_available_gridlayout")
        self.text_browser_update_available = QTextBrowser(self.page_update_available)
        self.text_browser_update_available.setObjectName(u"text_browser_update_available")

        self.update_available_gridlayout.addWidget(self.text_browser_update_available, 0, 0, 1, 1)

        self.update_available_button_acknowledged = QPushButton(self.page_update_available)
        self.update_available_button_acknowledged.setObjectName(u"update_available_button_acknowledged")

        self.update_available_gridlayout.addWidget(self.update_available_button_acknowledged, 1, 0, 1, 1)


        self.gridLayout_28.addLayout(self.update_available_gridlayout, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_update_available)

        self.gridLayout_11.addWidget(self.main_CentralStackedWidget, 1, 0, 1, 1)

        PornFetch_UI.setCentralWidget(self.main_CentralWidget)
        QWidget.setTabOrder(self.main_button_switch_home, self.main_button_switch_account)
        QWidget.setTabOrder(self.main_button_switch_account, self.main_button_switch_tools)
        QWidget.setTabOrder(self.main_button_switch_tools, self.main_button_switch_settings)
        QWidget.setTabOrder(self.main_button_switch_settings, self.main_button_switch_credits)
        QWidget.setTabOrder(self.main_button_switch_credits, self.main_button_switch_supported_websites)
        QWidget.setTabOrder(self.main_button_switch_supported_websites, self.download_lineedit_url)
        QWidget.setTabOrder(self.download_lineedit_url, self.download_button_download)
        QWidget.setTabOrder(self.download_button_download, self.download_lineedit_playlist_url)
        QWidget.setTabOrder(self.download_lineedit_playlist_url, self.download_button_playlist_get_videos)
        QWidget.setTabOrder(self.download_button_playlist_get_videos, self.download_lineedit_model_url)
        QWidget.setTabOrder(self.download_lineedit_model_url, self.download_button_model)
        QWidget.setTabOrder(self.download_button_model, self.login_button_login)
        QWidget.setTabOrder(self.login_button_login, self.tools_button_list_categories_eporner)
        QWidget.setTabOrder(self.tools_button_list_categories_eporner, self.login_lineedit_username)
        QWidget.setTabOrder(self.login_lineedit_username, self.login_lineedit_password)
        QWidget.setTabOrder(self.login_lineedit_password, self.tools_lineedit_hqporner_category)
        QWidget.setTabOrder(self.tools_lineedit_hqporner_category, self.tools_button_hqporner_category_get_videos)
        QWidget.setTabOrder(self.tools_button_hqporner_category_get_videos, self.tools_button_get_brazzers_videos)
        QWidget.setTabOrder(self.tools_button_get_brazzers_videos, self.tools_lineedit_videos_by_category_eporner)
        QWidget.setTabOrder(self.tools_lineedit_videos_by_category_eporner, self.tools_button_eporner_category_get_videos)
        QWidget.setTabOrder(self.tools_button_eporner_category_get_videos, self.scrollarea_credits)
        QWidget.setTabOrder(self.scrollarea_credits, self.button_install)
        QWidget.setTabOrder(self.button_install, self.install_dialog_lineedit_custom_app_name)
        QWidget.setTabOrder(self.install_dialog_lineedit_custom_app_name, self.button_portable)
        QWidget.setTabOrder(self.button_portable, self.scrollarea_install_dialog)
        QWidget.setTabOrder(self.scrollarea_install_dialog, self.scrollarea_keyboard_shortcuts)
        QWidget.setTabOrder(self.scrollarea_keyboard_shortcuts, self.license_button_accept)
        QWidget.setTabOrder(self.license_button_accept, self.license_button_deny)
        QWidget.setTabOrder(self.license_button_deny, self.scrollarea_license_page)
        QWidget.setTabOrder(self.scrollarea_license_page, self.scrollarea_supported_websites)
        QWidget.setTabOrder(self.scrollarea_supported_websites, self.license_textbrowser)
        QWidget.setTabOrder(self.license_textbrowser, self.keyboard_shortcuts_text_browser)
        QWidget.setTabOrder(self.keyboard_shortcuts_text_browser, self.text_browser_update_available)
        QWidget.setTabOrder(self.text_browser_update_available, self.update_available_button_acknowledged)
        QWidget.setTabOrder(self.update_available_button_acknowledged, self.install_dialog_text_browser)
        QWidget.setTabOrder(self.install_dialog_text_browser, self.supported_sites_textbrowser)
        QWidget.setTabOrder(self.supported_sites_textbrowser, self.scrollarea_disclaimer)
        QWidget.setTabOrder(self.scrollarea_disclaimer, self.disclaimer_textbrowser)
        QWidget.setTabOrder(self.disclaimer_textbrowser, self.disclaimer_button_accept)

        self.retranslateUi(PornFetch_UI)

        self.main_CentralStackedWidget.setCurrentIndex(0)
        self.main_stacked_widget_top.setCurrentIndex(0)
        self.main_stacked_widget_tree.setCurrentIndex(1)
        self.settings_stacked_widget_main.setCurrentIndex(3)
        self.settings_video_combobox_quality.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PornFetch_UI)
    # setupUi

    def retranslateUi(self, PornFetch_UI):
        PornFetch_UI.setWindowTitle(QCoreApplication.translate("PornFetch_UI", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        PornFetch_UI.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        PornFetch_UI.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button Tools section", None))
#endif // QT_CONFIG(accessibility)
        self.main_label_progressbar_total.setText(QCoreApplication.translate("PornFetch_UI", u"Total (HLS):", None))
#if QT_CONFIG(accessibility)
        self.main_button_switch_home.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button home page", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_home.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_account.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button Login (PornHub)", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_account.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_tools.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button Tools section", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_tools.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_settings.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button view progressbars", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_settings.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_credits.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button Credits / Information", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_credits.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_supported_websites.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button: Supported websites", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_supported_websites.setText(QCoreApplication.translate("PornFetch_UI", u"Supported websites", None))
#if QT_CONFIG(accessibility)
        self.download_label_model_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label model url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_model_url.setText(QCoreApplication.translate("PornFetch_UI", u"Model URL:", None))
#if QT_CONFIG(accessibility)
        self.download_button_search.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start video search", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_search.setText(QCoreApplication.translate("PornFetch_UI", u"Search", None))
#if QT_CONFIG(accessibility)
        self.download_label_playlist_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label playlist url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_playlist_url.setText(QCoreApplication.translate("PornFetch_UI", u"Playlist URL:", None))
#if QT_CONFIG(accessibility)
        self.download_button_model.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start fetching videos from model, channel, actress or creator", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_model.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_playlist_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit playlist URL (PornHub, Xvideos)", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_playlist_url.setText("")
        self.download_lineedit_playlist_url.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter a PornHub / XVideos Playlist URL", None))
#if QT_CONFIG(accessibility)
        self.download_button_playlist_get_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start fetching videos of a playlist", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_playlist_get_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_model_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit model / channel, actress, creator URL", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_model_url.setText("")
        self.download_lineedit_model_url.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter a Model / Channel / Actress / Creator URL ", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_search_query.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit search query", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_search_query.setText("")
        self.download_lineedit_search_query.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Search for videos on a website", None))
#if QT_CONFIG(accessibility)
        self.download_label_search.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label search query", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_search.setText(QCoreApplication.translate("PornFetch_UI", u"Search Query:", None))
#if QT_CONFIG(accessibility)
        self.download_button_download.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start downloading a video", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_download.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
        self.download_website_combobox.setItemText(0, QCoreApplication.translate("PornFetch_UI", u"HQPorner", None))
        self.download_website_combobox.setItemText(1, QCoreApplication.translate("PornFetch_UI", u"PornHub", None))
        self.download_website_combobox.setItemText(2, QCoreApplication.translate("PornFetch_UI", u"EPorner", None))
        self.download_website_combobox.setItemText(3, QCoreApplication.translate("PornFetch_UI", u"XVideos", None))
        self.download_website_combobox.setItemText(4, QCoreApplication.translate("PornFetch_UI", u"XHamster", None))
        self.download_website_combobox.setItemText(5, QCoreApplication.translate("PornFetch_UI", u"XNXX", None))
        self.download_website_combobox.setItemText(6, QCoreApplication.translate("PornFetch_UI", u"Spankbang", None))
        self.download_website_combobox.setItemText(7, QCoreApplication.translate("PornFetch_UI", u"Missav", None))
        self.download_website_combobox.setItemText(8, QCoreApplication.translate("PornFetch_UI", u"YouPorn", None))
        self.download_website_combobox.setItemText(9, QCoreApplication.translate("PornFetch_UI", u"Porntrex", None))

#if QT_CONFIG(accessibility)
        self.download_website_combobox.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"combobox, select search website here", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.download_label_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label video url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_url.setText(QCoreApplication.translate("PornFetch_UI", u"Video URL:", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit video url", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_url.setText("")
        self.download_lineedit_url.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter a Video URL or an XHamster Short", None))
#if QT_CONFIG(accessibility)
        self.login_button_get_watched_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button get watched videos (requires login) ", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_get_watched_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get watched videos", None))
#if QT_CONFIG(accessibility)
        self.login_button_get_recommended_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button get recommended videos (requires login)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_get_recommended_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get recommended videos", None))
#if QT_CONFIG(accessibility)
        self.login_button_get_liked_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button get liked videos (requires login)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_get_liked_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Liked videos", None))
#if QT_CONFIG(accessibility)
        self.login_lineedit_password.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit password ", None))
#endif // QT_CONFIG(accessibility)
        self.login_lineedit_password.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter your PornHub Password (Your account data will never be saved nor shared) ", None))
#if QT_CONFIG(accessibility)
        self.login_lineedit_username.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit email", None))
#endif // QT_CONFIG(accessibility)
        self.login_lineedit_username.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter your PornHub E-Mail address", None))
#if QT_CONFIG(accessibility)
        self.login_button_login.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start login (enter credentials above)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_login.setText(QCoreApplication.translate("PornFetch_UI", u"Login", None))
#if QT_CONFIG(accessibility)
        self.login_label_password.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label password", None))
#endif // QT_CONFIG(accessibility)
        self.login_label_password.setText(QCoreApplication.translate("PornFetch_UI", u"Password:", None))
#if QT_CONFIG(accessibility)
        self.login_label_username.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label username", None))
#endif // QT_CONFIG(accessibility)
        self.login_label_username.setText(QCoreApplication.translate("PornFetch_UI", u"E-Mail:", None))
        self.tools_groupbox_hqporner.setTitle(QCoreApplication.translate("PornFetch_UI", u"HQPorner", None))
#if QT_CONFIG(accessibility)
        self.tools_button_get_random_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools button hqporner get random video", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_get_random_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get random Video", None))
#if QT_CONFIG(accessibility)
        self.tools_button_hqporner_category_get_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools button hqporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_hqporner_category_get_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.tools_label_videos_by_category.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label tools hqporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_label_videos_by_category.setText(QCoreApplication.translate("PornFetch_UI", u"Get videos by category", None))
#if QT_CONFIG(accessibility)
        self.tools_lineedit_hqporner_category.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools lineedit hqporner category (enter the category here)", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.tools_label_get_top_porn.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label tools hqporn get top porn", None))
#endif // QT_CONFIG(accessibility)
        self.tools_label_get_top_porn.setText(QCoreApplication.translate("PornFetch_UI", u"Get Top Porn:", None))
#if QT_CONFIG(accessibility)
        self.tools_button_get_brazzers_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools buttonn get brazzers videos", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_get_brazzers_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Brazzers videos", None))
        self.tools_combobox_hqporner_top_porn.setItemText(0, QCoreApplication.translate("PornFetch_UI", u"Week", None))
        self.tools_combobox_hqporner_top_porn.setItemText(1, QCoreApplication.translate("PornFetch_UI", u"Month", None))
        self.tools_combobox_hqporner_top_porn.setItemText(2, QCoreApplication.translate("PornFetch_UI", u"All time", None))

#if QT_CONFIG(accessibility)
        self.tools_combobox_hqporner_top_porn.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools combobox hqporner top porn selection", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.tools_button_top_porn_get_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools button hqporner get videos by top porn", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_top_porn_get_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.tools_button_list_categories.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"tools button hqporner list all categories", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_list_categories.setText(QCoreApplication.translate("PornFetch_UI", u"List of all categories", None))
        self.tools_groupbox_eporner.setTitle(QCoreApplication.translate("PornFetch_UI", u"EPorner", None))
#if QT_CONFIG(accessibility)
        self.tools_lineedit_videos_by_category_eporner.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit tools eporner enter category here", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.tools_button_eporner_category_get_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button tools eporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_eporner_category_get_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.tools_button_list_categories_eporner.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button tools eporner list all categories", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_list_categories_eporner.setText(QCoreApplication.translate("PornFetch_UI", u"List of all categories", None))
#if QT_CONFIG(accessibility)
        self.tools_label_videos_by_category_eporner.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label tools eporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_label_videos_by_category_eporner.setText(QCoreApplication.translate("PornFetch_UI", u"Get videos by category", None))
        self.treewidget_button_downloads.setText(QCoreApplication.translate("PornFetch_UI", u"Downloads", None))
        self.treewidget_button_advanced_configuration.setText(QCoreApplication.translate("PornFetch_UI", u"Advanced Configuration", None))
#if QT_CONFIG(tooltip)
        self.treewidget_button_stop.setToolTip(QCoreApplication.translate("PornFetch_UI", u"Does not stop downloading videos", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.treewidget_button_stop.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button stop loading videos", None))
#endif // QT_CONFIG(accessibility)
        self.treewidget_button_stop.setText(QCoreApplication.translate("PornFetch_UI", u"Stop loading videos", None))
        ___qtreewidgetitem = self.main_tree_widget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("PornFetch_UI", u"Duration (minutes)", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("PornFetch_UI", u"Author", None));
        self.tree_advanced_label_index_end.setText(QCoreApplication.translate("PornFetch_UI", u"End:", None))
        self.tree_advanced_label_custom_title.setText(QCoreApplication.translate("PornFetch_UI", u"Custom Title formatting:", None))
        self.tree_advanced_lineedit_custom_title.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"$title", None))
        self.tree_advanced_button_custom_title_options.setText(QCoreApplication.translate("PornFetch_UI", u"Options", None))
        self.tree_advanced_checkbox_cleanup_on_stop.setText(QCoreApplication.translate("PornFetch_UI", u"Cleanup on stop (disables resume feature for HLS) ", None))
#if QT_CONFIG(accessibility)
        self.tree_advanced_checkbox_do_not_clear_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox do not clear videos", None))
#endif // QT_CONFIG(accessibility)
        self.tree_advanced_checkbox_do_not_clear_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Do not clear videos", None))
#if QT_CONFIG(tooltip)
        self.tree_advanced_label_tooltip_index_videos.setToolTip(QCoreApplication.translate("PornFetch_UI", u"This feature allows you to only fetch a specific range of videos when\n"
"searching, loading models / channels or fetching a playlist.\n"
"\n"
"For example if you use 20 for the start and 30 for the end value, the first\n"
"20 videos will be completely ignored and not loaded into the tree widget.\n"
"This can save a lot of time in certain scenarios.\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.tree_advanced_label_tooltip_index_videos.setText("")
        self.tree_advanced_label_index_start.setText(QCoreApplication.translate("PornFetch_UI", u"Start:", None))
#if QT_CONFIG(accessibility)
        self.tree_advanced_button_keyboard_shortcuts.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button keyboard shortcuts", None))
#endif // QT_CONFIG(accessibility)
        self.tree_advanced_button_keyboard_shortcuts.setText(QCoreApplication.translate("PornFetch_UI", u"Keyboard shortcuts", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_video.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Video page (settings)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_video.setText(QCoreApplication.translate("PornFetch_UI", u"Video", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_performance.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Performance page (Settings)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_performance.setText(QCoreApplication.translate("PornFetch_UI", u"Performance", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_system.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"System page (settings)", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_button_switch_system.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_system.setText(QCoreApplication.translate("PornFetch_UI", u"System", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_ui.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button: Supported websites", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_ui.setText(QCoreApplication.translate("PornFetch_UI", u"UI", None))
        self.settings_video_combobox_quality.setItemText(0, QCoreApplication.translate("PornFetch_UI", u"BEST (auto)", None))
        self.settings_video_combobox_quality.setItemText(1, QCoreApplication.translate("PornFetch_UI", u"HALF (auto)", None))
        self.settings_video_combobox_quality.setItemText(2, QCoreApplication.translate("PornFetch_UI", u"WORST (auto)", None))
        self.settings_video_combobox_quality.setItemText(3, QCoreApplication.translate("PornFetch_UI", u"2160p", None))
        self.settings_video_combobox_quality.setItemText(4, QCoreApplication.translate("PornFetch_UI", u"1440p", None))
        self.settings_video_combobox_quality.setItemText(5, QCoreApplication.translate("PornFetch_UI", u"1080p", None))
        self.settings_video_combobox_quality.setItemText(6, QCoreApplication.translate("PornFetch_UI", u"720p", None))
        self.settings_video_combobox_quality.setItemText(7, QCoreApplication.translate("PornFetch_UI", u"540p", None))
        self.settings_video_combobox_quality.setItemText(8, QCoreApplication.translate("PornFetch_UI", u"480p", None))
        self.settings_video_combobox_quality.setItemText(9, QCoreApplication.translate("PornFetch_UI", u"360p", None))
        self.settings_video_combobox_quality.setItemText(10, QCoreApplication.translate("PornFetch_UI", u"240p", None))
        self.settings_video_combobox_quality.setItemText(11, QCoreApplication.translate("PornFetch_UI", u"144p", None))

#if QT_CONFIG(accessibility)
        self.settings_video_combobox_quality.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"combobox settings quality", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_video_combobox_quality.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"Porn Fetch will by default download the best video quality", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_button_videos_open_output_path.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"settings open output path", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_videos_open_output_path.setText(QCoreApplication.translate("PornFetch_UI", u"Open", None))
        self.settings_video_combobox_model_videos.setItemText(0, QCoreApplication.translate("PornFetch_UI", u"Both (recommended)", None))
        self.settings_video_combobox_model_videos.setItemText(1, QCoreApplication.translate("PornFetch_UI", u"Uploaded", None))
        self.settings_video_combobox_model_videos.setItemText(2, QCoreApplication.translate("PornFetch_UI", u"Featured", None))

#if QT_CONFIG(accessibility)
        self.settings_video_combobox_model_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"combobox model videos type", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_video_combobox_model_videos.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"This decides whether you want to fetch model uploads or featured videos or both of them", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.settings_label_videos_quality.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_videos_quality.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label video quality", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_quality.setText(QCoreApplication.translate("PornFetch_UI", u"Quality:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_model_videos.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_model_videos.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_quality.setToolTip(QCoreApplication.translate("PornFetch_UI", u"By default, Porn Fetch will select the best available video quality. You can also decide between half and worst above.\n"
"If you instead use the custom integer values (1080p, 720p etc.) then Porn Fetch will try to use these, if available,\n"
"but if they are not available the next best quality will be chosen. Please note that this is experimental and has not\n"
"been that tested very well. (Be honest, why would you not choose the best quality lol)", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_quality.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_result_limit.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The result limit defines how many videos will be returned when performing a search or doing other operations which\n"
"involves loading multiple videos. This also affects models / channels and your liked videos. The result limit is\n"
"basically the number of videos which can be loaded into the tree widget (this thing where videos are displayed).", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_result_limit.setText("")
#if QT_CONFIG(accessibility)
        self.settings_spinbox_videos_result_limit.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"spinbox resutl limit", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_spinbox_videos_result_limit.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"The result limit limits how many videos will be fetched", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.settings_label_videos_model_vdeos_type.setToolTip(QCoreApplication.translate("PornFetch_UI", u"User uploads and featured videos are two different things. User uploads are the videos which were really uploaded\n"
"by the model and the featured videos are videos the model is part or featured in.\n"
"\n"
"For example the model Nancy Ace has like 10 self uploaded which she made by herself, but she is part in like thousands\n"
"of videos from other studios.\n"
"\n"
"If you choose \"User Uploads\", only self uploaded videos will be fetched, and the other way around :)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_videos_model_vdeos_type.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label model videos type (pornhub)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_model_vdeos_type.setText(QCoreApplication.translate("PornFetch_UI", u"Model videos (PH)", None))
#if QT_CONFIG(tooltip)
        self.settings_label_videos_result_limit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_videos_result_limit.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label result limit", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_result_limit.setText(QCoreApplication.translate("PornFetch_UI", u"Result Limit:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_track_videos.setToolTip(QCoreApplication.translate("PornFetch_UI", u"Videos will be tracked in a SQL database which will save the URL and the metadata. ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_track_videos.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_track_downloaded_videos.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_track_downloaded_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox track downloaded videos", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_track_downloaded_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Track downloaded videos", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_write_metadata.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_write_metadata.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox write metadata tags", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_write_metadata.setText(QCoreApplication.translate("PornFetch_UI", u"Write metadata tags", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_write_metadata.setToolTip(QCoreApplication.translate("PornFetch_UI", u"Metadata tags are saved inside of the file itself. These are tags that video players can read from and provide you information.\n"
"Some folder viewers also give you the ability to search files by specific metadata tags. Those tags can help organize and structure files.\n"
"Porn Fetch will by default save those tags inside of your video files. ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_write_metadata.setText("")
#if QT_CONFIG(accessibility)
        self.settings_label_videos_output_path.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label output path", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_output_path.setText(QCoreApplication.translate("PornFetch_UI", u"Output path:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_use_directory_system.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos \n"
"from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other\n"
"5 into the other. (This will still apply with your selected output path)\n"
"\n"
"This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_use_directory_system.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_use_directory_system.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_directory_system.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox use directory system", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_directory_system.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"The directory system will automatically create folders for each author of videos", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_directory_system.setText(QCoreApplication.translate("PornFetch_UI", u"Use directory system", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_skip_existing_files.setToolTip(QCoreApplication.translate("PornFetch_UI", u"If you fetch a video and the exact same filename already exists, usually Porn Fetch would just skip this file.\n"
"If you set this option to No, then Porn Fetch instead download the video and append a random number to it.\n"
"\n"
"For example you have downloaded a video called:\n"
"\n"
"Spain_didnt_win_against_Germany.mp4\n"
"\n"
"and you download a video with the same title, then it would append a random number to it:\n"
"\n"
"Spain_didnt_win_against_Germany_118251.mp4", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_skip_existing_files.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_skip_existing_files.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_skip_existing_files.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox skip existing files", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_skip_existing_files.setText(QCoreApplication.translate("PornFetch_UI", u"Skip existing files", None))
#if QT_CONFIG(accessibility)
        self.settings_lineedit_videos_database_path.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit output path of the database", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_lineedit_videos_database_path.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"the database tracks all downloaded videos in Porn Fetch, optional", None))
#endif // QT_CONFIG(accessibility)
        self.settings_lineedit_videos_database_path.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter the path of the database file here", None))
#if QT_CONFIG(accessibility)
        self.settings_lineedit_videos_output_path.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit video output path", None))
#endif // QT_CONFIG(accessibility)
        self.settings_lineedit_videos_output_path.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter \"./\" for current directory", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_speed_limit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_speed_limit.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Speed Limit (MB/s)", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_speed_limit.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"Pages concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_speed_limit.setText(QCoreApplication.translate("PornFetch_UI", u"Speed Limit (MB/s):", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_maximum_timeout.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The timeout handles the timeout for retrieving segments when using the threaded download mode. If you have a poor \n"
"internet connection you can set this higher than 10. But this isn't required for most users!", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_maximum_timeout.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_pages_concurrency.setToolTip(QCoreApplication.translate("PornFetch_UI", u"<html><head/><body><p>The pages concurrency defines how many pages will be scraped at the same time,</p><p>when searching for videos or fetching models. Lower values are generally recommended,</p><p>to avoid getting blocked. Keep it between 1-3.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_pages_concurrency.setText("")
#if QT_CONFIG(tooltip)
        self.settings_label_performance_processing_delay.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_processing_delay.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Videos Concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_processing_delay.setText(QCoreApplication.translate("PornFetch_UI", u"Processing Delay (videos/sec):", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_pages_concurrency.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_pages_concurrency.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"Pages concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_pages_concurrency.setText(QCoreApplication.translate("PornFetch_UI", u"Pages concurrency:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_simultaneous_downloads.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The Semaphore is a tool to limit the number of simultaneous actions / downloads. For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.\\nIf the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if you have a really good internet connection and a good system.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_simultaneous_downloads.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_speed_limit.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The speed limit sets the maximum allowed network speed in megabyte per seconds. However, this doesn't work perfectly.\n"
"The speed limit also only works for the default download mode, because it wouldn't make sense downloading multiple\n"
"segments at the same time with a speed limit being in place.\n"
"\n"
"If you need something more 'exact / precise', use applications like NetLimiter 4 or something similar.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_speed_limit.setText("")
#if QT_CONFIG(tooltip)
        self.settings_label_performance_maximal_retries.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_retries.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"Maximum retries", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_retries.setText(QCoreApplication.translate("PornFetch_UI", u"Maximum retries:", None))
#if QT_CONFIG(accessibility)
        self.settings_doublespinbox_performance_speed_limit.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"spinbox speed limit", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.label_tooltip_download_mode.setToolTip(QCoreApplication.translate("PornFetch_UI", u"1) High Performance:  Uses a class of workers to download multiple video segments at a time. Can be really fast if you\n"
"have a very strong internet connection. Maybe not great for low end systems.\n"
"\n"
"2) FFMPEG:\n"
"FFmpeg is a specialized tool for video encoding and decoding. It is also able to fetch videos based on their m3u8 URL, which contains the segments. FFmpeg is slower compared to high performance and not well tested. Please only use if you have to.\n"
"\n"
"3) Default:  The default download mode will just download one video segment after the next one. If you get a lot of \n"
"timeouts this can really slow down the process, as we need to wait the Porn sites to return the video segments.\n"
"With the High Performance method, we can just download other segments while waiting which makes it so fast.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_download_mode.setText("")
#if QT_CONFIG(accessibility)
        self.settings_spinbox_performance_pages_concurrency.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"spinbox pages concurrency", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_spinbox_performance_pages_concurrency.setAccessibleDescription(QCoreApplication.translate("PornFetch_UI", u"This decides how many pages will be scraped at the same time. Lower values between 1-3 are recommended", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.settings_label_performance_simultaneous_download.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_simultaneous_download.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Simultaneous downloads", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_simultaneous_download.setText(QCoreApplication.translate("PornFetch_UI", u"Simultaneous downloads:", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_maximal_timeout.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_timeout.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Maximum timeout", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_timeout.setText(QCoreApplication.translate("PornFetch_UI", u"Maximum timeout:", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_videos_concurrency.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_videos_concurrency.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Videos Concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_videos_concurrency.setText(QCoreApplication.translate("PornFetch_UI", u"Videos Concurrency:", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_network_delay.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_network_delay.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Network delay (requests/sec)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_network_delay.setText(QCoreApplication.translate("PornFetch_UI", u"Network delay (requests/sec):", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_network_delay.setToolTip(QCoreApplication.translate("PornFetch_UI", u"You can set a delay between requests from you and a site. If you are downloading a lot of videos or experiencing \n"
"errors, you should enable a delay. By default the delay is turned off with the value 0\n"
"\n"
"A good starting point is between 0.5 - 1.5\n"
"\n"
"The longer the delay is, the longer it will take to download videos, load videos and generally do stuff. This does not\n"
"really affect the high performance download mode.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_network_delay.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_processing_delay.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The processing delay sets a delay before every video gets downloaded.\n"
"Let's assume you set a delay of 30 (30 seconds), then it will take 30 seconds between each video downloads.\n"
"This does not apply if you have a value of simultaneous downloads greater than 1.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_processing_delay.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_videos_concurrency.setToolTip(QCoreApplication.translate("PornFetch_UI", u"<html><head/><body><p>The videos concurrency defines how many videos are fetched at the same time when searching or fetching models etc.</p><p>For example, let's say you search for something. Then the first page of the results will be scraped for video URLs. This takes</p><p>usually around 1 second. If you set this value to 20, then from all those URLs Porn Fetch will attempt to load 20 videos at</p><p>the same time. This can improve speed A LOT, but can also get you blocked from the site. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_videos_concurrency.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_download_workers.setToolTip(QCoreApplication.translate("PornFetch_UI", u"<html><head/><body><p>The download worker setting defines, how many workers / threads will be used at the same time</p><p>to fetch video segments at the same time. Usually you don't need to go over 20, unless you have a higher</p><p>internet connection than 1gbit/s. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_download_workers.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_maximum_retries.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The maximal retries defines how much attempts will be used for a network request. For example if an API calls\n"
"a URL for a website there will be <AMOUNT> of attempts until an error is thrown.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_maximum_retries.setText("")
#if QT_CONFIG(tooltip)
        self.label_settings_performance_download_workers.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.label_settings_performance_download_workers.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Download workers:", None))
#endif // QT_CONFIG(accessibility)
        self.label_settings_performance_download_workers.setText(QCoreApplication.translate("PornFetch_UI", u"Download workers:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_anonymous_mode.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The anonymous mode renames all of Porn Fetch's elements to look NOT like a Porn downloader.\n"
"This makes it useful for downloading Porn content if you are in public, or multiple people use your PC / Phone.\n"
"\n"
"This also disables thumbnail preview. All titles will be replaced with: [redacted] as well as all authors.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_anonymous_mode.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_ssl_context.setToolTip(QCoreApplication.translate("PornFetch_UI", u"<html><head/><body><p>If you use truststore as your SSL context, your system's OS will validate whether the HTTPS (SSL)) certificate of the website is valid or not. On newer systems, truststore is the recommended and default way, because again, your system manages everything and makes sure it's up to date.</p><p>However, if your system is too old, e.g., some old legacy WIndows XP build, then you might want to use the pre-shipped CA which is the one that comes with certifi. </p><p><br/></p><p>This is a complex topic, just leave the default options and you'll be good to go. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_ssl_context.setText("")
        self.settings_checkbox_use_truststore.setText(QCoreApplication.translate("PornFetch_UI", u"Use Truststore", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_enable_anonymous_mode.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_anonymous_mode.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox enable anonymous mode", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_anonymous_mode.setText(QCoreApplication.translate("PornFetch_UI", u"Enable Anonymous mode", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_supress_errors.setToolTip(QCoreApplication.translate("PornFetch_UI", u"If you enable this function, all errors will be suppressed. This does not mean that they will be completely ignored, but\n"
"you won't get a big notification for it. \n"
"\n"
"If you have activated Network Logging, they will still be reported. If an error happens while iterating through videos,\n"
"the current video will be skipped and Porn Fetch will continue with the next one.  ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_supress_errors.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_update_checks.setToolTip(QCoreApplication.translate("PornFetch_UI", u"Porn Fetch will check for updates each time it starts, using my own server. This will require a working IPv6 connection. No personal data nor any other data is sent during this process.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_update_checks.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_network_logging.setToolTip(QCoreApplication.translate("PornFetch_UI", u"I have created my own server that runs 24/7 in my home. Porn Fetch (ONLY if you enable it) logs specific types of errors,\n"
"that I don't know of, or that I need your help to fix them, to my server using a simple JSON post request.\n"
"\n"
"You can see the Code of the server publicly here -->: https://github.com/EchterAlsFake/Server\n"
"Porn Fetch also does its update checking mechanism through that server.\n"
"\n"
"IMPORTANT:\n"
"The server is IPv6 only. If your ISP has not given you a working IPv6 IP address, then you can't reach me.\n"
"You can check for yourself on 'https://ipleak.net'. It should be something like this: '2a02:810a:186:b400::5c51'\n"
"\n"
"My server does NOT save any of your personal information. No IP addresses, no PC information, no other identifiable information.\n"
"The only things being stored is the literal Python exception that's being caught, the version you are running on, and your system.\n"
"Like literally only if you use Windows, Linux or Mac. Nothing else.\n"
"\n"
"You can see"
                        " that yourself, as mentioned before on the source code.\n"
"You'd help me a lot by enabling network logging :) ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_network_logging.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_proxy_kill_switch.setToolTip(QCoreApplication.translate("PornFetch_UI", u"The proxy kill switch is an additional security layer if you use proxies. It will check your IP each time before making\n"
"a request and if it's leaked it will immediately exit everything.\n"
"\n"
"My priority on developing this is low. Please do not report errors. Thank you <3", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_proxy_kill_switch.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox enable proxy kill switch", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_proxy_kill_switch.setText(QCoreApplication.translate("PornFetch_UI", u"Proxy Kill Switch", None))
        self.settings_checkbox_system_enable_debug_mode.setText(QCoreApplication.translate("PornFetch_UI", u"Enable Debug Mode (Not recommended) ", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_enable_network_logging.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_network_logging.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox enable network logging", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_network_logging.setText(QCoreApplication.translate("PornFetch_UI", u"Enable Network Logging", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_supress_errors.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_supress_errors.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox supress errors silently", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_supress_errors.setText(QCoreApplication.translate("PornFetch_UI", u"Supress errors silently", None))
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_activate_proxy.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox activate a proxy", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_activate_proxy.setText(QCoreApplication.translate("PornFetch_UI", u"Activate Proxy", None))
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_update_checks.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"checkbox enable update checks", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_update_checks.setText(QCoreApplication.translate("PornFetch_UI", u"Update checks", None))
#if QT_CONFIG(accessibility)
        self.settings_spinbox_ui_font_size.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"spinbox font size", None))
#endif // QT_CONFIG(accessibility)
        self.settings_combobox_ui_theme.setItemText(0, QCoreApplication.translate("PornFetch_UI", u"Dark", None))
        self.settings_combobox_ui_theme.setItemText(1, QCoreApplication.translate("PornFetch_UI", u"Light (why would you pick light theme)", None))
        self.settings_combobox_ui_theme.setItemText(2, QCoreApplication.translate("PornFetch_UI", u"LSD (don't activate while you are high) ", None))

#if QT_CONFIG(accessibility)
        self.settings_combobox_ui_theme.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"combobox porn fetch theme", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_label_ui_language.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label graphical user interface language", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_ui_language.setText(QCoreApplication.translate("PornFetch_UI", u"Graphical User Interface Language:", None))
        self.settings_ui_combobox_language.setItemText(0, QCoreApplication.translate("PornFetch_UI", u"System", None))
        self.settings_ui_combobox_language.setItemText(1, QCoreApplication.translate("PornFetch_UI", u"English", None))
        self.settings_ui_combobox_language.setItemText(2, QCoreApplication.translate("PornFetch_UI", u"German", None))
        self.settings_ui_combobox_language.setItemText(3, QCoreApplication.translate("PornFetch_UI", u"Chinese simplified (outdated)", None))
        self.settings_ui_combobox_language.setItemText(4, QCoreApplication.translate("PornFetch_UI", u"French (outdated)", None))
        self.settings_ui_combobox_language.setItemText(5, QCoreApplication.translate("PornFetch_UI", u"Italian", None))

#if QT_CONFIG(accessibility)
        self.settings_ui_combobox_language.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"combobox porn fetch language", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_label_ui_theme.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label porn fetch theme ", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_ui_theme.setText(QCoreApplication.translate("PornFetch_UI", u"Theme:", None))
#if QT_CONFIG(accessibility)
        self.settings_label_ui_font_size.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label font size", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_ui_font_size.setText(QCoreApplication.translate("PornFetch_UI", u"Font Size:", None))
        self.settings_button_buy_license.setText(QCoreApplication.translate("PornFetch_UI", u"Buy License (5\u20ac)", None))
        self.settings_button_import_license.setText(QCoreApplication.translate("PornFetch_UI", u"Import License File", None))
#if QT_CONFIG(accessibility)
        self.settings_button_apply.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button apply the settings", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_apply.setText(QCoreApplication.translate("PornFetch_UI", u"Apply  (needs restart)", None))
#if QT_CONFIG(accessibility)
        self.settings_button_reset.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button reset porn fetch to default settings", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_reset.setText(QCoreApplication.translate("PornFetch_UI", u"Reset Porn Fetch to default settings", None))
#if QT_CONFIG(accessibility)
        self.settings_button_system_install_pornfetch.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button install porn fetch (This is optional) ", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_system_install_pornfetch.setText(QCoreApplication.translate("PornFetch_UI", u"Install Porn Fetch", None))
        self.settings_button_uninstall_porn_fetch.setText(QCoreApplication.translate("PornFetch_UI", u"Uninstall Porn Fetch", None))
        self.button_settings_clear_temp.setText(QCoreApplication.translate("PornFetch_UI", u"Clear Temporary Files", None))
        self.credits_button_send_feedback.setText(QCoreApplication.translate("PornFetch_UI", u"Send Feedback (Anonymously)", None))
#if QT_CONFIG(accessibility)
        self.credits_textbrowser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Textbrowser for credits / information", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.license_button_deny.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button deny license", None))
#endif // QT_CONFIG(accessibility)
        self.license_button_deny.setText(QCoreApplication.translate("PornFetch_UI", u"Deny and Exit", None))
#if QT_CONFIG(accessibility)
        self.license_button_accept.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button accept license", None))
#endif // QT_CONFIG(accessibility)
        self.license_button_accept.setText(QCoreApplication.translate("PornFetch_UI", u"Accept", None))
#if QT_CONFIG(accessibility)
        self.license_textbrowser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser license", None))
#endif // QT_CONFIG(accessibility)
        self.license_textbrowser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
                        "<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The redistribution of copyright-protected content obtained through Porn Fetch is <span style=\" font-weight:700;\">strictly discouraged</span>. </li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Any misuse of this software to steal and redistribute copyrighted material is against its intended purpose and is not endorsed by the creator. </li></ul>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Third-Party Software</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> utilizes the following third-party tools and resources:</p>\n"
"<ol"
                        " style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">FFmpeg</span> </li></ol>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">Used for video processing and conversion. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">FFmpeg is free software licensed under the GPL. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">For more information, visit <a href=\"https://ffmpeg.org\"><span style=\" text-decoration: underline; color:#007af4;\">https://ffmpeg.org</span></a>.</p>\n"
"<hr />\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt"
                        "-block-indent:0; text-indent:0px;\">Thank you for using <span style=\" font-weight:700;\">Porn Fetch</span> responsibly!</p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.keyboard_shortcuts_text_browser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser keyboard shortcuts", None))
#endif // QT_CONFIG(accessibility)
        self.keyboard_shortcuts_text_browser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:14pt; font-weight:700;\">Keyboard Shortcuts</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:14pt; font-weight:700;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-l"
                        "eft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + Q     Closes the application</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + E      Exports all current video URLs from the tree widget into a .txt file </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + T      Downloads all videos in the tree widget (same as clicking the button)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + A     Quickly enables the anonymous mode (temporarily)</span></p>\n"
"<p style=\" margin-top:0px; margin"
                        "-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + S     Saves Porn Fetch settings</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + X     Selects all items in the tree widget as checked</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + Z     Unchecks all items in the tree widget</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-ind"
                        "ent:0; text-indent:0px; font-family:'Sans Serif'; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">   </span></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.install_dialog_text_browser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser install dialog", None))
#endif // QT_CONFIG(accessibility)
        self.install_dialog_text_browser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
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
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#00ff00;\">2) Portable</span></p>\n"
"<p style=\" marg"
                        "in-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This means, that Porn Fetch will not be installed and in order to use and start Porn Fetch you always need to double click on the file you have downloaded. This has some benefits as the uninstallation is easier and you have more control over it, but for the average user I do not recommend this.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; font-weight:700; color:#a100ff;\">Custom App name</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                        "ent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\">Down below you can enter  a custom name for Porn Fetch. You can then search with this name for Porn Fetch and Porn Fetch will not be found anymore when someone enters &quot;Porn Fetch&quot; on your PC. This can be useful if multiple persons use your PC and you don't want them to know you are using this application. It can also help if you are in public and people stare at your PC. Porn Fetch has also an option to fully hide, that it's a PornHub downloader.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:12pt; color:#ffffff;\">If you leave it empty, Porn Fetch will remain as &quot;"
                        "Porn Fetch&quot; in your short menu.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:14pt; text-decoration: underline; color:#aa0000;\">NOTE:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Installation was implemented in this release and might still be experimental. If you run into any issues, please report it on my GitHub. Thank you :</span><span style=\" font-family:'Segoe UI'; font-size:9pt;\">) </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-inden"
                        "t:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.install_dialog_label_custom_app_name.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label custom app name", None))
#endif // QT_CONFIG(accessibility)
        self.install_dialog_label_custom_app_name.setText(QCoreApplication.translate("PornFetch_UI", u"Custom App Name:", None))
#if QT_CONFIG(accessibility)
        self.install_dialog_lineedit_custom_app_name.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit custom app name (enter the custom name here) ", None))
#endif // QT_CONFIG(accessibility)
        self.install_dialog_lineedit_custom_app_name.setText("")
        self.install_dialog_lineedit_custom_app_name.setPlaceholderText(QCoreApplication.translate("PornFetch_UI", u"Enter your custom App Name here. Leave it empty to keep \"Porn Fetch\"", None))
#if QT_CONFIG(accessibility)
        self.button_install.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"buttom instal porn fetch", None))
#endif // QT_CONFIG(accessibility)
        self.button_install.setText(QCoreApplication.translate("PornFetch_UI", u"Install", None))
#if QT_CONFIG(accessibility)
        self.button_portable.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button portable mode", None))
#endif // QT_CONFIG(accessibility)
        self.button_portable.setText(QCoreApplication.translate("PornFetch_UI", u"Portable", None))
#if QT_CONFIG(accessibility)
        self.supported_sites_textbrowser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser supported websites", None))
#endif // QT_CONFIG(accessibility)
        self.supported_sites_textbrowser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\"><thead>\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-weight:700;\">Category</span></p></td>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                        " text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-weight:700;\">Websites</span></p></td></tr></thead>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Videos</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang, YouPorn</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Searching</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub, HQporner, Ep"
                        "orner, xnxx, xvideos, missav, Xhamster, Spankbang</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Models</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub, HQporner, xnxx</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Pornstars</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub, Eporner, xvideos, Xhamster, Spankbang</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-b"
                        "ottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Channels</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub, Xhamster, Spankbang</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Creator / Users</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Xhamster (Creator), Spankbang (Creator), xnxx (Users)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-fami"
                        "ly:'Adwaita Sans';\">Playlists</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub, xvideos</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Downloading</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">xvideos</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Shorts</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent"
                        ":0px;\"><span style=\" font-family:'Adwaita Sans';\">Xhamster</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Account Login</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">PornHub</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Videos by Category</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">HQporner, Eporner</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin"
                        "-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Random</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">HQporner</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Brazzers only</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">HQporner</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">Top Porn</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px;"
                        " margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans';\">HQporner</span></p></td></tr></table></body></html>", None))
#if QT_CONFIG(accessibility)
        self.disclaimer_textbrowser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser disclaimer message", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.disclaimer_textbrowser.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.disclaimer_textbrowser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">DISCLAIMER</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">Porn Fetch</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> is free software licens"
                        "ed under the GNU General Public License v3.0. You are free to use, modify, and redistribute this software under the terms of that license.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Please be aware that </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">Porn Fetch may interact with websites in ways that violate their Terms of Service.</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> Additionally, downloading copyright-protected content without proper authorization may be illegal in many jurisdictions, including under the DMCA (Digital Millennium Copyright Act).</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">While some countries or regions may allow downloading content"
                        " for strictly </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">personal, non-commercial use</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\">, I </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">strongly discourage</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> using Porn Fetch to download, share, or redistribute content without appropriate rights or permissions. Always ensure you comply with your local laws and the terms of any website you access.</span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">IMPORTANT NOTE</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">I </span><span style=\" font-family:'Sans Serif'"
                        "; font-size:9pt; font-weight:700;\">strongly recommend</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> that you do </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">not</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> use this software for:</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" font-family:'Sans Serif'; font-size:9pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Unauthorized redistribution of content</li>\n"
"<li style=\" font-family:'Sans Serif'; font-size:9pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Commercial use of downloaded materials</li>\n"
"<li style=\" font-family:'Sans Serif'; font-size:9pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-bl"
                        "ock-indent:0; text-indent:0px;\">Any activity that could result in legal liability for yourself or others</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Although the GPL license grants you broad rights, </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">continued misuse</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> may jeopardize the development and availability of this project. Please respect the intent behind this tool and use it responsibly.</span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">LIABILITY DISCLAIMER</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" font-family:'Sans Serif'; font-size:9pt;\">This software is provided </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">without any warranty</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> as described in the GPLv3. I am </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">not liable</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> for any damages, legal consequences, or misuse resulting from your use of this software.<br />You are solely responsible for ensuring your actions are lawful and ethical. </span></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.disclaimer_button_accept.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button accept disclaimer message", None))
#endif // QT_CONFIG(accessibility)
        self.disclaimer_button_accept.setText(QCoreApplication.translate("PornFetch_UI", u"Accept", None))
        self.one_time_setup_button_info_enable_all.setText(QCoreApplication.translate("PornFetch_UI", u"Enable Update + Error reports (100% anonymous)", None))
        self.one_time_setup_button_info_enable_update.setText(QCoreApplication.translate("PornFetch_UI", u"Enable Update checking only", None))
        self.one_time_setup_button_info_disable_all.setText(QCoreApplication.translate("PornFetch_UI", u"Disable everything", None))
#if QT_CONFIG(accessibility)
        self.text_browser_update_available.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser update changelog notification", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.update_available_button_acknowledged.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button acknowledge that a new version is out", None))
#endif // QT_CONFIG(accessibility)
        self.update_available_button_acknowledged.setText(QCoreApplication.translate("PornFetch_UI", u"OK", None))
    # retranslateUi

