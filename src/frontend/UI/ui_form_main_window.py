# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

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
        self.gridLayout_8 = QGridLayout(self.main_CentralWidget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.main_horizontallayout_menu_buttons = QHBoxLayout()
        self.main_horizontallayout_menu_buttons.setSpacing(5)
        self.main_horizontallayout_menu_buttons.setObjectName(u"main_horizontallayout_menu_buttons")
        self.main_button_switch_home = QPushButton(self.main_CentralWidget)
        self.main_button_switch_home.setObjectName(u"main_button_switch_home")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.main_button_switch_home.sizePolicy().hasHeightForWidth())
        self.main_button_switch_home.setSizePolicy(sizePolicy2)
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
        sizePolicy2.setHeightForWidth(self.main_button_switch_account.sizePolicy().hasHeightForWidth())
        self.main_button_switch_account.setSizePolicy(sizePolicy2)
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

        self.main_button_switch_settings = QPushButton(self.main_CentralWidget)
        self.main_button_switch_settings.setObjectName(u"main_button_switch_settings")
        sizePolicy2.setHeightForWidth(self.main_button_switch_settings.sizePolicy().hasHeightForWidth())
        self.main_button_switch_settings.setSizePolicy(sizePolicy2)
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
        sizePolicy2.setHeightForWidth(self.main_button_switch_credits.sizePolicy().hasHeightForWidth())
        self.main_button_switch_credits.setSizePolicy(sizePolicy2)
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
        sizePolicy2.setHeightForWidth(self.main_button_switch_supported_websites.sizePolicy().hasHeightForWidth())
        self.main_button_switch_supported_websites.setSizePolicy(sizePolicy2)
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


        self.gridLayout_8.addLayout(self.main_horizontallayout_menu_buttons, 0, 0, 1, 1)

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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.main_stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.main_stacked_widget_top.setSizePolicy(sizePolicy3)
        self.main_stacked_widget_top.setMinimumSize(QSize(0, 120))
        self.main_stacked_widget_top.setMaximumSize(QSize(16777215, 120))
        self.main_stacked_widget_top.setStyleSheet(u"")
        self.main_stacked_widget_top.setLineWidth(1)
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        sizePolicy1.setHeightForWidth(self.page_download.sizePolicy().hasHeightForWidth())
        self.page_download.setSizePolicy(sizePolicy1)
        self.page_download.setMinimumSize(QSize(0, 120))
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
        self.download_lineedit_model_url = QLineEdit(self.page_download)
        self.download_lineedit_model_url.setObjectName(u"download_lineedit_model_url")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.download_lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_model_url.setSizePolicy(sizePolicy4)
        self.download_lineedit_model_url.setMinimumSize(QSize(300, 35))
        font = QFont()
        font.setBold(True)
        self.download_lineedit_model_url.setFont(font)

        self.download_gridlayout.addWidget(self.download_lineedit_model_url, 5, 1, 1, 2)

        self.download_button_playlist_get_videos = QPushButton(self.page_download)
        self.download_button_playlist_get_videos.setObjectName(u"download_button_playlist_get_videos")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.download_button_playlist_get_videos.sizePolicy().hasHeightForWidth())
        self.download_button_playlist_get_videos.setSizePolicy(sizePolicy5)
        self.download_button_playlist_get_videos.setMinimumSize(QSize(0, 30))
        font1 = QFont()
        font1.setBold(False)
        self.download_button_playlist_get_videos.setFont(font1)
        self.download_button_playlist_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.download_gridlayout.addWidget(self.download_button_playlist_get_videos, 4, 3, 1, 1)

        self.download_button_download = QPushButton(self.page_download)
        self.download_button_download.setObjectName(u"download_button_download")
        sizePolicy5.setHeightForWidth(self.download_button_download.sizePolicy().hasHeightForWidth())
        self.download_button_download.setSizePolicy(sizePolicy5)
        self.download_button_download.setMinimumSize(QSize(60, 30))
        font2 = QFont()
        font2.setBold(False)
        font2.setUnderline(False)
        self.download_button_download.setFont(font2)
        self.download_button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_download.setStyleSheet(u"")

        self.download_gridlayout.addWidget(self.download_button_download, 2, 3, 1, 1)

        self.download_lineedit_playlist_url = QLineEdit(self.page_download)
        self.download_lineedit_playlist_url.setObjectName(u"download_lineedit_playlist_url")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.download_lineedit_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_playlist_url.setSizePolicy(sizePolicy6)
        self.download_lineedit_playlist_url.setMinimumSize(QSize(0, 30))
        self.download_lineedit_playlist_url.setFont(font)

        self.download_gridlayout.addWidget(self.download_lineedit_playlist_url, 4, 1, 1, 2)

        self.download_label_playlist_url = QLabel(self.page_download)
        self.download_label_playlist_url.setObjectName(u"download_label_playlist_url")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.download_label_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_label_playlist_url.setSizePolicy(sizePolicy7)
        self.download_label_playlist_url.setMinimumSize(QSize(0, 30))
        self.download_label_playlist_url.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_playlist_url, 4, 0, 1, 1)

        self.download_lineedit_url = QLineEdit(self.page_download)
        self.download_lineedit_url.setObjectName(u"download_lineedit_url")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.download_lineedit_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_url.setSizePolicy(sizePolicy8)
        self.download_lineedit_url.setMinimumSize(QSize(300, 30))
        self.download_lineedit_url.setFont(font)

        self.download_gridlayout.addWidget(self.download_lineedit_url, 2, 1, 1, 2)

        self.download_label_model_url = QLabel(self.page_download)
        self.download_label_model_url.setObjectName(u"download_label_model_url")
        sizePolicy7.setHeightForWidth(self.download_label_model_url.sizePolicy().hasHeightForWidth())
        self.download_label_model_url.setSizePolicy(sizePolicy7)
        self.download_label_model_url.setMinimumSize(QSize(0, 30))
        self.download_label_model_url.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_model_url, 5, 0, 1, 1)

        self.download_button_model = QPushButton(self.page_download)
        self.download_button_model.setObjectName(u"download_button_model")
        sizePolicy5.setHeightForWidth(self.download_button_model.sizePolicy().hasHeightForWidth())
        self.download_button_model.setSizePolicy(sizePolicy5)
        self.download_button_model.setMinimumSize(QSize(60, 30))
        self.download_button_model.setFont(font1)
        self.download_button_model.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_model.setStyleSheet(u"")

        self.download_gridlayout.addWidget(self.download_button_model, 5, 3, 1, 1)

        self.download_label_url = QLabel(self.page_download)
        self.download_label_url.setObjectName(u"download_label_url")
        sizePolicy7.setHeightForWidth(self.download_label_url.sizePolicy().hasHeightForWidth())
        self.download_label_url.setSizePolicy(sizePolicy7)
        self.download_label_url.setMinimumSize(QSize(0, 30))
        self.download_label_url.setFont(font1)

        self.download_gridlayout.addWidget(self.download_label_url, 2, 0, 1, 1)


        self.gridLayout_5.addLayout(self.download_gridlayout, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_download)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.page_login.setMinimumSize(QSize(0, 110))
        self.gridLayout_2 = QGridLayout(self.page_login)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.login_button_switch_pornhub = QPushButton(self.page_login)
        self.login_button_switch_pornhub.setObjectName(u"login_button_switch_pornhub")

        self.horizontalLayout.addWidget(self.login_button_switch_pornhub)

        self.login_button_switch_xvideos = QPushButton(self.page_login)
        self.login_button_switch_xvideos.setObjectName(u"login_button_switch_xvideos")

        self.horizontalLayout.addWidget(self.login_button_switch_xvideos)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.login_stacked_widget = QStackedWidget(self.page_login)
        self.login_stacked_widget.setObjectName(u"login_stacked_widget")
        self.page_pornhub = QWidget()
        self.page_pornhub.setObjectName(u"page_pornhub")
        self.gridLayout_3 = QGridLayout(self.page_pornhub)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.login_gridlayout_login_box = QGridLayout()
        self.login_gridlayout_login_box.setSpacing(6)
        self.login_gridlayout_login_box.setObjectName(u"login_gridlayout_login_box")
        self.login_gridlayout_login_box.setContentsMargins(3, 6, 3, 3)
        self.login_lineedit_username = QLineEdit(self.page_pornhub)
        self.login_lineedit_username.setObjectName(u"login_lineedit_username")
        sizePolicy8.setHeightForWidth(self.login_lineedit_username.sizePolicy().hasHeightForWidth())
        self.login_lineedit_username.setSizePolicy(sizePolicy8)
        self.login_lineedit_username.setMinimumSize(QSize(150, 35))
        self.login_lineedit_username.setFont(font)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_username, 0, 1, 1, 2)

        self.login_horizontallayout_ph_account = QHBoxLayout()
        self.login_horizontallayout_ph_account.setObjectName(u"login_horizontallayout_ph_account")
        self.login_button_get_watched_videos = QPushButton(self.page_pornhub)
        self.login_button_get_watched_videos.setObjectName(u"login_button_get_watched_videos")
        self.login_button_get_watched_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_watched_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_watched_videos.setStyleSheet(u"")

        self.login_horizontallayout_ph_account.addWidget(self.login_button_get_watched_videos)

        self.login_button_get_recommended_videos = QPushButton(self.page_pornhub)
        self.login_button_get_recommended_videos.setObjectName(u"login_button_get_recommended_videos")
        self.login_button_get_recommended_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_recommended_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_recommended_videos.setStyleSheet(u"")

        self.login_horizontallayout_ph_account.addWidget(self.login_button_get_recommended_videos)

        self.login_button_get_liked_videos = QPushButton(self.page_pornhub)
        self.login_button_get_liked_videos.setObjectName(u"login_button_get_liked_videos")
        self.login_button_get_liked_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_liked_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_liked_videos.setStyleSheet(u"")

        self.login_horizontallayout_ph_account.addWidget(self.login_button_get_liked_videos)


        self.login_gridlayout_login_box.addLayout(self.login_horizontallayout_ph_account, 2, 0, 1, 3)

        self.login_label_password = QLabel(self.page_pornhub)
        self.login_label_password.setObjectName(u"login_label_password")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.login_label_password.sizePolicy().hasHeightForWidth())
        self.login_label_password.setSizePolicy(sizePolicy9)
        self.login_label_password.setMinimumSize(QSize(0, 30))
        self.login_label_password.setFont(font)

        self.login_gridlayout_login_box.addWidget(self.login_label_password, 1, 0, 1, 1)

        self.login_lineedit_password = QLineEdit(self.page_pornhub)
        self.login_lineedit_password.setObjectName(u"login_lineedit_password")
        sizePolicy8.setHeightForWidth(self.login_lineedit_password.sizePolicy().hasHeightForWidth())
        self.login_lineedit_password.setSizePolicy(sizePolicy8)
        self.login_lineedit_password.setMinimumSize(QSize(0, 35))
        self.login_lineedit_password.setFont(font)
        self.login_lineedit_password.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.login_lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_password, 1, 1, 1, 2)

        self.login_button_login = QPushButton(self.page_pornhub)
        self.login_button_login.setObjectName(u"login_button_login")
        self.login_button_login.setMinimumSize(QSize(0, 30))
        self.login_button_login.setFont(font)
        self.login_button_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_login.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_login, 3, 0, 1, 3)

        self.login_label_username = QLabel(self.page_pornhub)
        self.login_label_username.setObjectName(u"login_label_username")
        sizePolicy9.setHeightForWidth(self.login_label_username.sizePolicy().hasHeightForWidth())
        self.login_label_username.setSizePolicy(sizePolicy9)
        self.login_label_username.setMinimumSize(QSize(0, 30))
        self.login_label_username.setFont(font)

        self.login_gridlayout_login_box.addWidget(self.login_label_username, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.login_gridlayout_login_box, 1, 0, 1, 1)

        self.login_stacked_widget.addWidget(self.page_pornhub)
        self.page_xvideos = QWidget()
        self.page_xvideos.setObjectName(u"page_xvideos")
        self.gridLayout_11 = QGridLayout(self.page_xvideos)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.login_xvideos_label_session_auth_token = QLabel(self.page_xvideos)
        self.login_xvideos_label_session_auth_token.setObjectName(u"login_xvideos_label_session_auth_token")

        self.gridLayout_10.addWidget(self.login_xvideos_label_session_auth_token, 1, 1, 1, 1)

        self.login_xvideos_button_login = QPushButton(self.page_xvideos)
        self.login_xvideos_button_login.setObjectName(u"login_xvideos_button_login")

        self.gridLayout_10.addWidget(self.login_xvideos_button_login, 2, 2, 1, 1)

        self.login_xvideos_label_session_token = QLabel(self.page_xvideos)
        self.login_xvideos_label_session_token.setObjectName(u"login_xvideos_label_session_token")

        self.gridLayout_10.addWidget(self.login_xvideos_label_session_token, 0, 1, 1, 1)

        self.login_xvideos_button_get_recommended = QPushButton(self.page_xvideos)
        self.login_xvideos_button_get_recommended.setObjectName(u"login_xvideos_button_get_recommended")

        self.gridLayout_10.addWidget(self.login_xvideos_button_get_recommended, 1, 3, 1, 1)

        self.login_xvideos_button_get_liked = QPushButton(self.page_xvideos)
        self.login_xvideos_button_get_liked.setObjectName(u"login_xvideos_button_get_liked")

        self.gridLayout_10.addWidget(self.login_xvideos_button_get_liked, 0, 3, 1, 1)

        self.login_xvideos_lineedit_session_auth_token = QLineEdit(self.page_xvideos)
        self.login_xvideos_lineedit_session_auth_token.setObjectName(u"login_xvideos_lineedit_session_auth_token")

        self.gridLayout_10.addWidget(self.login_xvideos_lineedit_session_auth_token, 1, 2, 1, 1)

        self.login_xvideos_button_help = QPushButton(self.page_xvideos)
        self.login_xvideos_button_help.setObjectName(u"login_xvideos_button_help")

        self.gridLayout_10.addWidget(self.login_xvideos_button_help, 2, 1, 1, 1)

        self.login_xvideos_button_get_watch_later = QPushButton(self.page_xvideos)
        self.login_xvideos_button_get_watch_later.setObjectName(u"login_xvideos_button_get_watch_later")

        self.gridLayout_10.addWidget(self.login_xvideos_button_get_watch_later, 2, 3, 1, 1)

        self.login_xvideos_lineedit_session_token = QLineEdit(self.page_xvideos)
        self.login_xvideos_lineedit_session_token.setObjectName(u"login_xvideos_lineedit_session_token")

        self.gridLayout_10.addWidget(self.login_xvideos_lineedit_session_token, 0, 2, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.login_stacked_widget.addWidget(self.page_xvideos)

        self.verticalLayout_2.addWidget(self.login_stacked_widget)


        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_login)
        self.page_tools = QWidget()
        self.page_tools.setObjectName(u"page_tools")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.page_tools.sizePolicy().hasHeightForWidth())
        self.page_tools.setSizePolicy(sizePolicy10)
        self.page_tools.setMinimumSize(QSize(100, 30))
        self.gridLayout_17 = QGridLayout(self.page_tools)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.main_stacked_widget_top.addWidget(self.page_tools)
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
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.main_scrollarea_treewidget_content.sizePolicy().hasHeightForWidth())
        self.main_scrollarea_treewidget_content.setSizePolicy(sizePolicy11)
        self.gridLayout_4 = QGridLayout(self.main_scrollarea_treewidget_content)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.main_tree_widget = QTreeWidget(self.main_scrollarea_treewidget_content)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title")
        self.main_tree_widget.setHeaderItem(__qtreewidgetitem)
        self.main_tree_widget.setObjectName(u"main_tree_widget")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.main_tree_widget.sizePolicy().hasHeightForWidth())
        self.main_tree_widget.setSizePolicy(sizePolicy12)
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
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(0)
        sizePolicy13.setHeightForWidth(self.tree_advanced_label_index_end.sizePolicy().hasHeightForWidth())
        self.tree_advanced_label_index_end.setSizePolicy(sizePolicy13)

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
        self.tree_advanced_checkbox_cleanup_on_stop.setChecked(False)

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
        sizePolicy13.setHeightForWidth(self.tree_advanced_label_tooltip_index_videos.sizePolicy().hasHeightForWidth())
        self.tree_advanced_label_tooltip_index_videos.setSizePolicy(sizePolicy13)

        self.tree_advanced_hlayout_1.addWidget(self.tree_advanced_label_tooltip_index_videos)

        self.tree_advanced_label_index_start = QLabel(self.page_advanced_configuration)
        self.tree_advanced_label_index_start.setObjectName(u"tree_advanced_label_index_start")
        sizePolicy13.setHeightForWidth(self.tree_advanced_label_index_start.sizePolicy().hasHeightForWidth())
        self.tree_advanced_label_index_start.setSizePolicy(sizePolicy13)

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
        self.settings_scrollarea_widget_contents.setGeometry(QRect(0, 0, 1118, 544))
        self.gridLayout_19 = QGridLayout(self.settings_scrollarea_widget_contents)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.settings_vlayout_1 = QVBoxLayout()
        self.settings_vlayout_1.setObjectName(u"settings_vlayout_1")
        self.serttings_vlayout_buttons = QHBoxLayout()
        self.serttings_vlayout_buttons.setObjectName(u"serttings_vlayout_buttons")

        self.settings_vlayout_1.addLayout(self.serttings_vlayout_buttons)


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
        self.scrollarea_credits_widget_contents.setGeometry(QRect(0, 0, 188, 103))
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
        self.scrollarea_license_page_widget_contents.setGeometry(QRect(0, 0, 226, 112))
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
        font3 = QFont()
        font3.setFamilies([u"JetBrainsMono Nerd Font Propo"])
        font3.setPointSize(11)
        font3.setKerning(True)
        self.license_textbrowser.setFont(font3)
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
        sizePolicy12.setHeightForWidth(self.keyboard_shortcuts_text_browser.sizePolicy().hasHeightForWidth())
        self.keyboard_shortcuts_text_browser.setSizePolicy(sizePolicy12)
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
        self.scrollarea_install_dialog_widget_contents.setGeometry(QRect(0, 0, 170, 138))
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
        self.scrollarea_disclaimer_widget_contents.setGeometry(QRect(0, 0, 98, 119))
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

        self.update_available_hlayout_buttons = QHBoxLayout()
        self.update_available_hlayout_buttons.setObjectName(u"update_available_hlayout_buttons")
        self.update_available_button_acknowledged = QPushButton(self.page_update_available)
        self.update_available_button_acknowledged.setObjectName(u"update_available_button_acknowledged")

        self.update_available_hlayout_buttons.addWidget(self.update_available_button_acknowledged)

        self.update_available_button_automatic_update = QPushButton(self.page_update_available)
        self.update_available_button_automatic_update.setObjectName(u"update_available_button_automatic_update")

        self.update_available_hlayout_buttons.addWidget(self.update_available_button_automatic_update)


        self.update_available_gridlayout.addLayout(self.update_available_hlayout_buttons, 1, 0, 1, 1)


        self.gridLayout_28.addLayout(self.update_available_gridlayout, 0, 0, 1, 1)

        self.main_CentralStackedWidget.addWidget(self.page_update_available)

        self.gridLayout_8.addWidget(self.main_CentralStackedWidget, 1, 0, 1, 1)

        self.formlayout_progressbar = QFormLayout()
        self.formlayout_progressbar.setObjectName(u"formlayout_progressbar")
        self.formlayout_progressbar.setHorizontalSpacing(0)
        self.formlayout_progressbar.setVerticalSpacing(5)
        self.main_label_progressbar_total = QLabel(self.main_CentralWidget)
        self.main_label_progressbar_total.setObjectName(u"main_label_progressbar_total")

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_total)

        self.main_progressbar_total = QProgressBar(self.main_CentralWidget)
        self.main_progressbar_total.setObjectName(u"main_progressbar_total")
        sizePolicy8.setHeightForWidth(self.main_progressbar_total.sizePolicy().hasHeightForWidth())
        self.main_progressbar_total.setSizePolicy(sizePolicy8)
        self.main_progressbar_total.setMinimumSize(QSize(300, 0))
        self.main_progressbar_total.setStyleSheet(u"text-align: center; /* Centered text */")
        self.main_progressbar_total.setValue(0)

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.FieldRole, self.main_progressbar_total)


        self.gridLayout_8.addLayout(self.formlayout_progressbar, 2, 0, 1, 1)

        PornFetch_UI.setCentralWidget(self.main_CentralWidget)
        QWidget.setTabOrder(self.main_button_switch_home, self.main_button_switch_account)
        QWidget.setTabOrder(self.main_button_switch_account, self.main_button_switch_settings)
        QWidget.setTabOrder(self.main_button_switch_settings, self.main_button_switch_credits)
        QWidget.setTabOrder(self.main_button_switch_credits, self.main_button_switch_supported_websites)
        QWidget.setTabOrder(self.main_button_switch_supported_websites, self.download_lineedit_url)
        QWidget.setTabOrder(self.download_lineedit_url, self.download_button_download)
        QWidget.setTabOrder(self.download_button_download, self.download_lineedit_playlist_url)
        QWidget.setTabOrder(self.download_lineedit_playlist_url, self.download_button_playlist_get_videos)
        QWidget.setTabOrder(self.download_button_playlist_get_videos, self.download_lineedit_model_url)
        QWidget.setTabOrder(self.download_lineedit_model_url, self.download_button_model)
        QWidget.setTabOrder(self.download_button_model, self.login_lineedit_username)
        QWidget.setTabOrder(self.login_lineedit_username, self.login_lineedit_password)
        QWidget.setTabOrder(self.login_lineedit_password, self.scrollarea_credits)
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
        QWidget.setTabOrder(self.text_browser_update_available, self.install_dialog_text_browser)
        QWidget.setTabOrder(self.install_dialog_text_browser, self.supported_sites_textbrowser)
        QWidget.setTabOrder(self.supported_sites_textbrowser, self.scrollarea_disclaimer)
        QWidget.setTabOrder(self.scrollarea_disclaimer, self.disclaimer_textbrowser)
        QWidget.setTabOrder(self.disclaimer_textbrowser, self.disclaimer_button_accept)

        self.retranslateUi(PornFetch_UI)

        self.main_CentralStackedWidget.setCurrentIndex(1)
        self.main_stacked_widget_top.setCurrentIndex(1)
        self.login_stacked_widget.setCurrentIndex(0)
        self.main_stacked_widget_tree.setCurrentIndex(1)


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
#if QT_CONFIG(accessibility)
        self.main_button_switch_home.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button home page", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_home.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_account.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"Button Login (PornHub)", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_account.setText("")
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
        self.download_lineedit_model_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit model / channel, actress, creator URL", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_model_url.setText("")
        self.download_lineedit_model_url.setPlaceholderText("")
#if QT_CONFIG(accessibility)
        self.download_button_playlist_get_videos.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start fetching videos of a playlist", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_playlist_get_videos.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_button_download.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start downloading a video", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_download.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_playlist_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit playlist URL (PornHub, Xvideos)", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_playlist_url.setText("")
        self.download_lineedit_playlist_url.setPlaceholderText("")
#if QT_CONFIG(accessibility)
        self.download_label_playlist_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label playlist url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_playlist_url.setText(QCoreApplication.translate("PornFetch_UI", u"Playlist URL:", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit video url", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_url.setText("")
        self.download_lineedit_url.setPlaceholderText("")
#if QT_CONFIG(accessibility)
        self.download_label_model_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label model url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_model_url.setText(QCoreApplication.translate("PornFetch_UI", u"Model URL:", None))
#if QT_CONFIG(accessibility)
        self.download_button_model.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start fetching videos from model, channel, actress or creator", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_model.setText(QCoreApplication.translate("PornFetch_UI", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_label_url.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label video url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_url.setText(QCoreApplication.translate("PornFetch_UI", u"Video URL:", None))
        self.login_button_switch_pornhub.setText(QCoreApplication.translate("PornFetch_UI", u"PornHub", None))
        self.login_button_switch_xvideos.setText(QCoreApplication.translate("PornFetch_UI", u"Xvideos", None))
#if QT_CONFIG(accessibility)
        self.login_lineedit_username.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit email", None))
#endif // QT_CONFIG(accessibility)
        self.login_lineedit_username.setPlaceholderText("")
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
        self.login_label_password.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label password", None))
#endif // QT_CONFIG(accessibility)
        self.login_label_password.setText(QCoreApplication.translate("PornFetch_UI", u"Password:", None))
#if QT_CONFIG(accessibility)
        self.login_lineedit_password.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"lineedit password ", None))
#endif // QT_CONFIG(accessibility)
        self.login_lineedit_password.setPlaceholderText("")
#if QT_CONFIG(accessibility)
        self.login_button_login.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"button start login (enter credentials above)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_login.setText(QCoreApplication.translate("PornFetch_UI", u"Login", None))
#if QT_CONFIG(accessibility)
        self.login_label_username.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"label username", None))
#endif // QT_CONFIG(accessibility)
        self.login_label_username.setText(QCoreApplication.translate("PornFetch_UI", u"E-Mail:", None))
        self.login_xvideos_label_session_auth_token.setText(QCoreApplication.translate("PornFetch_UI", u"Session Token Auth:", None))
        self.login_xvideos_button_login.setText(QCoreApplication.translate("PornFetch_UI", u"Login", None))
        self.login_xvideos_label_session_token.setText(QCoreApplication.translate("PornFetch_UI", u"Session Token:", None))
        self.login_xvideos_button_get_recommended.setText(QCoreApplication.translate("PornFetch_UI", u"Get recommended videos", None))
        self.login_xvideos_button_get_liked.setText(QCoreApplication.translate("PornFetch_UI", u"Get Liked videos", None))
        self.login_xvideos_button_help.setText(QCoreApplication.translate("PornFetch_UI", u"Help", None))
        self.login_xvideos_button_get_watch_later.setText(QCoreApplication.translate("PornFetch_UI", u"Get watch later videos", None))
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
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("PornFetch_UI", u"Duration (minutes)", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("PornFetch_UI", u"Author", None))
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
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline; color:#0055ff;\">spankbang.com</span></li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" text-decoration: underline; color:#006fff;\">xhamster.com</span></li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; ma"
                        "rgin-right:0px; -qt-block-indent:0; text-indent:0px;\">missav.ws</li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">beeg.com</li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">porngo.com</li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">xfreehd.com</li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">porntrex.com</li>\n"
"<li style=\" text-decoration: underline; color:#006fff;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-inde"
                        "nt:0px;\">youporn.com</li></ul>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px; text-decoration: underline; color:#006fff;\"><br /></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Usage Warning</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Using <span style=\" font-weight:700;\">Porn Fetch</span> may result in <span style=\" font-weight:700;\">legal action</span> being taken against you. The creator of this software is not liable for any damages or legal consequences resulting from its use.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> was created solely"
                        " for the purpose of enabling offline access to videos in scenarios where internet access is unavailable. </p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The redistribution of copyright-protected content obtained through Porn Fetch is <span style=\" font-weight:700;\">strictly discouraged</span>. </li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Any misuse of this software to steal and redistribute copyrighted material is against its intended purpose and is not endorsed by the creator. </li></ul>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Third-Party Software</span></h2>\n"
"<p style=\" mar"
                        "gin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Porn Fetch</span> utilizes the following third-party tools and resources:</p>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">FFmpeg</span> </li></ol>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">Used for video processing and conversion. </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">FFmpeg is free software licensed under the GPL. </p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:1; text-indent:0px;\">For more information, visit <"
                        "a href=\"https://ffmpeg.org\"><span style=\" text-decoration: underline; color:#007af4;\">https://ffmpeg.org</span></a>.</p>\n"
"<hr />\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Thank you for using <span style=\" font-weight:700;\">Porn Fetch</span> responsibly!</p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.keyboard_shortcuts_text_browser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser keyboard shortcuts", None))
#endif // QT_CONFIG(accessibility)
        self.keyboard_shortcuts_text_browser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + A     Quickly enables the anonymous mode (temporarily)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">CTRL + S     Saves Porn Fetch settings</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margi"
                        "n-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">   </span></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.install_dialog_text_browser.setAccessibleName(QCoreApplication.translate("PornFetch_UI", u"textbrowser install dialog", None))
#endif // QT_CONFIG(accessibility)
        self.install_dialog_text_browser.setHtml(QCoreApplication.translate("PornFetch_UI", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
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
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
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
        self.update_available_button_acknowledged.setText(QCoreApplication.translate("PornFetch_UI", u"OK (Update manually)", None))
        self.update_available_button_automatic_update.setText(QCoreApplication.translate("PornFetch_UI", u"Automatic Update", None))
        self.main_label_progressbar_total.setText(QCoreApplication.translate("PornFetch_UI", u"Total (HLS):", None))
    # retranslateUi

