# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_android.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QProgressBar, QPushButton,
    QRadioButton, QScrollArea, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_PornFetch_Android(object):
    def setupUi(self, PornFetch_Android):
        if not PornFetch_Android.objectName():
            PornFetch_Android.setObjectName(u"PornFetch_Android")
        PornFetch_Android.resize(723, 1062)
        PornFetch_Android.setStyleSheet(u"")
        self.gridLayout_21 = QGridLayout(PornFetch_Android)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.verticallayout_main = QVBoxLayout()
        self.verticallayout_main.setSpacing(0)
        self.verticallayout_main.setObjectName(u"verticallayout_main")
        self.lineEdit = QLineEdit(PornFetch_Android)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticallayout_main.addWidget(self.lineEdit)

        self.main_stacked_widget_main = QStackedWidget(PornFetch_Android)
        self.main_stacked_widget_main.setObjectName(u"main_stacked_widget_main")
        self.main_stacked_widget_main.setLineWidth(1)
        self.main_widget = QWidget()
        self.main_widget.setObjectName(u"main_widget")
        self.gridLayout_8 = QGridLayout(self.main_widget)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.main_verticallayout = QVBoxLayout()
        self.main_verticallayout.setSpacing(5)
        self.main_verticallayout.setObjectName(u"main_verticallayout")
        self.main_verticallayout.setContentsMargins(-1, 3, -1, -1)
        self.main_verticallayout_treewidget = QVBoxLayout()
        self.main_verticallayout_treewidget.setObjectName(u"main_verticallayout_treewidget")
        self.scrollArea = QScrollArea(self.main_widget)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 697, 248))
        self.gridLayout_20 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.main_stacked_widget_top = QStackedWidget(self.scrollAreaWidgetContents)
        self.main_stacked_widget_top.setObjectName(u"main_stacked_widget_top")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.main_stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.main_stacked_widget_top.setSizePolicy(sizePolicy1)
        self.main_stacked_widget_top.setMinimumSize(QSize(650, 220))
        self.main_stacked_widget_top.setMaximumSize(QSize(16777215, 230))
        self.main_stacked_widget_top.setStyleSheet(u"b")
        self.main_stacked_widget_top.setLineWidth(1)
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.page_download.sizePolicy().hasHeightForWidth())
        self.page_download.setSizePolicy(sizePolicy2)
        self.page_download.setMinimumSize(QSize(0, 0))
        self.gridLayout_5 = QGridLayout(self.page_download)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(6)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridlayout_downloading.setContentsMargins(-1, 3, -1, -1)
        self.download_button_download = QPushButton(self.page_download)
        self.download_button_download.setObjectName(u"download_button_download")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.download_button_download.sizePolicy().hasHeightForWidth())
        self.download_button_download.setSizePolicy(sizePolicy3)
        self.download_button_download.setMinimumSize(QSize(60, 30))
        self.download_button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_download, 2, 5, 1, 1)

        self.download_radio_search_website_pornhub = QRadioButton(self.page_download)
        self.download_radio_search_website_pornhub.setObjectName(u"download_radio_search_website_pornhub")
        sizePolicy3.setHeightForWidth(self.download_radio_search_website_pornhub.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_pornhub.setSizePolicy(sizePolicy3)
        self.download_radio_search_website_pornhub.setMinimumSize(QSize(0, 30))
        self.download_radio_search_website_pornhub.setChecked(True)

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_pornhub, 8, 1, 1, 1)

        self.download_lineedit_search_query = QLineEdit(self.page_download)
        self.download_lineedit_search_query.setObjectName(u"download_lineedit_search_query")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.download_lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.download_lineedit_search_query.setSizePolicy(sizePolicy4)
        self.download_lineedit_search_query.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_search_query, 7, 1, 1, 4)

        self.download_label_playlist_url = QLabel(self.page_download)
        self.download_label_playlist_url.setObjectName(u"download_label_playlist_url")
        sizePolicy2.setHeightForWidth(self.download_label_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_label_playlist_url.setSizePolicy(sizePolicy2)
        self.download_label_playlist_url.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_label_playlist_url, 4, 0, 1, 1)

        self.download_label_search_website = QLabel(self.page_download)
        self.download_label_search_website.setObjectName(u"download_label_search_website")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.download_label_search_website.sizePolicy().hasHeightForWidth())
        self.download_label_search_website.setSizePolicy(sizePolicy5)
        self.download_label_search_website.setMinimumSize(QSize(0, 0))

        self.gridlayout_downloading.addWidget(self.download_label_search_website, 8, 0, 1, 1)

        self.download_label_file = QLabel(self.page_download)
        self.download_label_file.setObjectName(u"download_label_file")
        sizePolicy3.setHeightForWidth(self.download_label_file.sizePolicy().hasHeightForWidth())
        self.download_label_file.setSizePolicy(sizePolicy3)
        self.download_label_file.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.download_label_file, 6, 0, 1, 1)

        self.download_label_model_url = QLabel(self.page_download)
        self.download_label_model_url.setObjectName(u"download_label_model_url")
        sizePolicy3.setHeightForWidth(self.download_label_model_url.sizePolicy().hasHeightForWidth())
        self.download_label_model_url.setSizePolicy(sizePolicy3)
        self.download_label_model_url.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.download_label_model_url, 5, 0, 1, 1)

        self.button_search = QPushButton(self.page_download)
        self.button_search.setObjectName(u"button_search")
        sizePolicy3.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy3)
        self.button_search.setMinimumSize(QSize(0, 30))
        self.button_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search, 7, 5, 1, 1)

        self.download_radio_search_website_hqporner = QRadioButton(self.page_download)
        self.download_radio_search_website_hqporner.setObjectName(u"download_radio_search_website_hqporner")
        sizePolicy3.setHeightForWidth(self.download_radio_search_website_hqporner.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_hqporner.setSizePolicy(sizePolicy3)
        self.download_radio_search_website_hqporner.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_hqporner, 8, 2, 1, 1)

        self.download_label_url = QLabel(self.page_download)
        self.download_label_url.setObjectName(u"download_label_url")
        sizePolicy3.setHeightForWidth(self.download_label_url.sizePolicy().hasHeightForWidth())
        self.download_label_url.setSizePolicy(sizePolicy3)
        self.download_label_url.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.download_label_url, 2, 0, 1, 1)

        self.download_lineedit_file = QLineEdit(self.page_download)
        self.download_lineedit_file.setObjectName(u"download_lineedit_file")
        sizePolicy4.setHeightForWidth(self.download_lineedit_file.sizePolicy().hasHeightForWidth())
        self.download_lineedit_file.setSizePolicy(sizePolicy4)
        self.download_lineedit_file.setMinimumSize(QSize(300, 30))
        self.download_lineedit_file.setReadOnly(True)

        self.gridlayout_downloading.addWidget(self.download_lineedit_file, 6, 1, 1, 3)

        self.download_radio_search_website_xvideos = QRadioButton(self.page_download)
        self.download_radio_search_website_xvideos.setObjectName(u"download_radio_search_website_xvideos")
        sizePolicy3.setHeightForWidth(self.download_radio_search_website_xvideos.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_xvideos.setSizePolicy(sizePolicy3)
        self.download_radio_search_website_xvideos.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_xvideos, 8, 3, 1, 1)

        self.download_button_model = QPushButton(self.page_download)
        self.download_button_model.setObjectName(u"download_button_model")
        sizePolicy3.setHeightForWidth(self.download_button_model.sizePolicy().hasHeightForWidth())
        self.download_button_model.setSizePolicy(sizePolicy3)
        self.download_button_model.setMinimumSize(QSize(60, 30))
        self.download_button_model.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_model.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_model, 5, 5, 1, 1)

        self.download_lineedit_playlist_url = QLineEdit(self.page_download)
        self.download_lineedit_playlist_url.setObjectName(u"download_lineedit_playlist_url")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.download_lineedit_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_playlist_url.setSizePolicy(sizePolicy6)
        self.download_lineedit_playlist_url.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_playlist_url, 4, 1, 1, 4)

        self.download_button_help_file = QPushButton(self.page_download)
        self.download_button_help_file.setObjectName(u"download_button_help_file")
        sizePolicy3.setHeightForWidth(self.download_button_help_file.sizePolicy().hasHeightForWidth())
        self.download_button_help_file.setSizePolicy(sizePolicy3)
        self.download_button_help_file.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_button_help_file, 6, 4, 1, 1)

        self.download_radio_search_website_xnxx = QRadioButton(self.page_download)
        self.download_radio_search_website_xnxx.setObjectName(u"download_radio_search_website_xnxx")
        sizePolicy3.setHeightForWidth(self.download_radio_search_website_xnxx.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_xnxx.setSizePolicy(sizePolicy3)
        self.download_radio_search_website_xnxx.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_xnxx, 8, 5, 1, 1)

        self.download_lineedit_url = QLineEdit(self.page_download)
        self.download_lineedit_url.setObjectName(u"download_lineedit_url")
        sizePolicy4.setHeightForWidth(self.download_lineedit_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_url.setSizePolicy(sizePolicy4)
        self.download_lineedit_url.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_url, 2, 1, 1, 4)

        self.download_lineedit_model_url = QLineEdit(self.page_download)
        self.download_lineedit_model_url.setObjectName(u"download_lineedit_model_url")
        sizePolicy4.setHeightForWidth(self.download_lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_model_url.setSizePolicy(sizePolicy4)
        self.download_lineedit_model_url.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.download_lineedit_model_url, 5, 1, 1, 4)

        self.download_label_search = QLabel(self.page_download)
        self.download_label_search.setObjectName(u"download_label_search")
        sizePolicy2.setHeightForWidth(self.download_label_search.sizePolicy().hasHeightForWidth())
        self.download_label_search.setSizePolicy(sizePolicy2)
        self.download_label_search.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_label_search, 7, 0, 1, 1)

        self.download_button_open_file = QPushButton(self.page_download)
        self.download_button_open_file.setObjectName(u"download_button_open_file")
        sizePolicy3.setHeightForWidth(self.download_button_open_file.sizePolicy().hasHeightForWidth())
        self.download_button_open_file.setSizePolicy(sizePolicy3)
        self.download_button_open_file.setMinimumSize(QSize(60, 30))
        self.download_button_open_file.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_open_file.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_open_file, 6, 5, 1, 1)

        self.download_radio_search_website_eporner = QRadioButton(self.page_download)
        self.download_radio_search_website_eporner.setObjectName(u"download_radio_search_website_eporner")
        sizePolicy3.setHeightForWidth(self.download_radio_search_website_eporner.sizePolicy().hasHeightForWidth())
        self.download_radio_search_website_eporner.setSizePolicy(sizePolicy3)
        self.download_radio_search_website_eporner.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_radio_search_website_eporner, 8, 4, 1, 1)

        self.download_button_playlist_get_videos = QPushButton(self.page_download)
        self.download_button_playlist_get_videos.setObjectName(u"download_button_playlist_get_videos")
        sizePolicy3.setHeightForWidth(self.download_button_playlist_get_videos.sizePolicy().hasHeightForWidth())
        self.download_button_playlist_get_videos.setSizePolicy(sizePolicy3)
        self.download_button_playlist_get_videos.setMinimumSize(QSize(0, 30))

        self.gridlayout_downloading.addWidget(self.download_button_playlist_get_videos, 4, 5, 1, 1)

        self.download_spacer_main = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridlayout_downloading.addItem(self.download_spacer_main, 9, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_downloading, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_download)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.page_login.setMinimumSize(QSize(0, 30))
        self.gridLayout_2 = QGridLayout(self.page_login)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.login_gridlayout_login_box = QGridLayout()
        self.login_gridlayout_login_box.setSpacing(6)
        self.login_gridlayout_login_box.setObjectName(u"login_gridlayout_login_box")
        self.login_gridlayout_login_box.setContentsMargins(-1, 0, -1, -1)
        self.login_label_password = QLabel(self.page_login)
        self.login_label_password.setObjectName(u"login_label_password")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.login_label_password.sizePolicy().hasHeightForWidth())
        self.login_label_password.setSizePolicy(sizePolicy7)
        self.login_label_password.setMinimumSize(QSize(0, 30))

        self.login_gridlayout_login_box.addWidget(self.login_label_password, 1, 0, 1, 1)

        self.login_label_username = QLabel(self.page_login)
        self.login_label_username.setObjectName(u"login_label_username")
        sizePolicy7.setHeightForWidth(self.login_label_username.sizePolicy().hasHeightForWidth())
        self.login_label_username.setSizePolicy(sizePolicy7)
        self.login_label_username.setMinimumSize(QSize(0, 30))

        self.login_gridlayout_login_box.addWidget(self.login_label_username, 0, 0, 1, 1)

        self.login_button_login = QPushButton(self.page_login)
        self.login_button_login.setObjectName(u"login_button_login")
        self.login_button_login.setMinimumSize(QSize(0, 30))
        self.login_button_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_login.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_login, 2, 0, 1, 4)

        self.login_lineedit_username = QLineEdit(self.page_login)
        self.login_lineedit_username.setObjectName(u"login_lineedit_username")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.login_lineedit_username.sizePolicy().hasHeightForWidth())
        self.login_lineedit_username.setSizePolicy(sizePolicy8)
        self.login_lineedit_username.setMinimumSize(QSize(150, 30))

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_username, 0, 1, 1, 3)

        self.login_button_get_watched_videos = QPushButton(self.page_login)
        self.login_button_get_watched_videos.setObjectName(u"login_button_get_watched_videos")
        self.login_button_get_watched_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_watched_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_watched_videos.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_get_watched_videos, 3, 1, 1, 1)

        self.login_lineedit_password = QLineEdit(self.page_login)
        self.login_lineedit_password.setObjectName(u"login_lineedit_password")
        sizePolicy8.setHeightForWidth(self.login_lineedit_password.sizePolicy().hasHeightForWidth())
        self.login_lineedit_password.setSizePolicy(sizePolicy8)
        self.login_lineedit_password.setMinimumSize(QSize(150, 30))
        self.login_lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_password, 1, 1, 1, 3)

        self.login_button_get_recommended_videos = QPushButton(self.page_login)
        self.login_button_get_recommended_videos.setObjectName(u"login_button_get_recommended_videos")
        self.login_button_get_recommended_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_recommended_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_recommended_videos.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_get_recommended_videos, 3, 2, 1, 1)

        self.login_button_get_liked_videos = QPushButton(self.page_login)
        self.login_button_get_liked_videos.setObjectName(u"login_button_get_liked_videos")
        self.login_button_get_liked_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_liked_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_liked_videos.setStyleSheet(u"")

        self.login_gridlayout_login_box.addWidget(self.login_button_get_liked_videos, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.login_gridlayout_login_box.addItem(self.verticalSpacer, 4, 2, 1, 1)


        self.gridLayout_2.addLayout(self.login_gridlayout_login_box, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_login)
        self.page_progressbars = QWidget()
        self.page_progressbars.setObjectName(u"page_progressbars")
        self.gridLayout_6 = QGridLayout(self.page_progressbars)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.progress_scrollarea = QScrollArea(self.page_progressbars)
        self.progress_scrollarea.setObjectName(u"progress_scrollarea")
        self.progress_scrollarea.setWidgetResizable(True)
        self.progress_scrollarea_widgedcontents = QWidget()
        self.progress_scrollarea_widgedcontents.setObjectName(u"progress_scrollarea_widgedcontents")
        self.progress_scrollarea_widgedcontents.setGeometry(QRect(0, 0, 634, 300))
        self.gridLayout_18 = QGridLayout(self.progress_scrollarea_widgedcontents)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.progress_gridlayout_progressbar = QGridLayout()
        self.progress_gridlayout_progressbar.setObjectName(u"progress_gridlayout_progressbar")
        self.progress_gridlayout_progressbar.setHorizontalSpacing(6)
        self.progressbar_xnxx = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_xnxx.setObjectName(u"progressbar_xnxx")
        self.progressbar_xnxx.setMinimumSize(QSize(0, 30))
        self.progressbar_xnxx.setStyleSheet(u"text-align: center; /* Centered text */")
        self.progressbar_xnxx.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_xnxx, 3, 1, 1, 1)

        self.progress_label_pornhub = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_pornhub.setObjectName(u"progress_label_pornhub")
        sizePolicy7.setHeightForWidth(self.progress_label_pornhub.sizePolicy().hasHeightForWidth())
        self.progress_label_pornhub.setSizePolicy(sizePolicy7)
        self.progress_label_pornhub.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_pornhub, 0, 0, 1, 1)

        self.progress_label_xvideos = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_xvideos.setObjectName(u"progress_label_xvideos")
        self.progress_label_xvideos.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_xvideos, 4, 0, 1, 1)

        self.progress_label_eporner = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_eporner.setObjectName(u"progress_label_eporner")
        self.progress_label_eporner.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_eporner, 2, 0, 1, 1)

        self.progress_vertical_spacer_main = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.progress_gridlayout_progressbar.addItem(self.progress_vertical_spacer_main, 8, 1, 1, 1)

        self.progressbar_eporner = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_eporner.setObjectName(u"progressbar_eporner")
        self.progressbar_eporner.setMinimumSize(QSize(0, 30))
        self.progressbar_eporner.setStyleSheet(u"text-align: center; /* Centered text */")
        self.progressbar_eporner.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_eporner, 2, 1, 1, 1)

        self.progress_label_info = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_info.setObjectName(u"progress_label_info")
        self.progress_label_info.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_info, 7, 0, 1, 1)

        self.progressbar_hqporner = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_hqporner.setObjectName(u"progressbar_hqporner")
        sizePolicy8.setHeightForWidth(self.progressbar_hqporner.sizePolicy().hasHeightForWidth())
        self.progressbar_hqporner.setSizePolicy(sizePolicy8)
        self.progressbar_hqporner.setMinimumSize(QSize(300, 30))
        self.progressbar_hqporner.setStyleSheet(u"text-align: center; /* Centered text */")
        self.progressbar_hqporner.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_hqporner, 1, 1, 1, 1)

        self.progressbar_pornhub = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        sizePolicy8.setHeightForWidth(self.progressbar_pornhub.sizePolicy().hasHeightForWidth())
        self.progressbar_pornhub.setSizePolicy(sizePolicy8)
        self.progressbar_pornhub.setMinimumSize(QSize(300, 30))
        self.progressbar_pornhub.setStyleSheet(u"text-align: center; /* Centered text */")
        self.progressbar_pornhub.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.progress_label_hqporner = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_hqporner.setObjectName(u"progress_label_hqporner")
        sizePolicy7.setHeightForWidth(self.progress_label_hqporner.sizePolicy().hasHeightForWidth())
        self.progress_label_hqporner.setSizePolicy(sizePolicy7)
        self.progress_label_hqporner.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_hqporner, 1, 0, 1, 1)

        self.progress_label_missav = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_missav.setObjectName(u"progress_label_missav")

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_missav, 5, 0, 1, 1)

        self.progressbar_xvideos = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_xvideos.setObjectName(u"progressbar_xvideos")
        self.progressbar_xvideos.setMinimumSize(QSize(0, 30))
        self.progressbar_xvideos.setStyleSheet(u"text-align: center; /* Centered text */")
        self.progressbar_xvideos.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_xvideos, 4, 1, 1, 1)

        self.progress_lineedit_download_info = QLineEdit(self.progress_scrollarea_widgedcontents)
        self.progress_lineedit_download_info.setObjectName(u"progress_lineedit_download_info")
        self.progress_lineedit_download_info.setReadOnly(True)

        self.progress_gridlayout_progressbar.addWidget(self.progress_lineedit_download_info, 7, 1, 1, 1)

        self.progress_label_xnxx = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_xnxx.setObjectName(u"progress_label_xnxx")
        self.progress_label_xnxx.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_xnxx, 3, 0, 1, 1)

        self.progress_label_xhamster = QLabel(self.progress_scrollarea_widgedcontents)
        self.progress_label_xhamster.setObjectName(u"progress_label_xhamster")

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_xhamster, 6, 0, 1, 1)

        self.progressbar_missav = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_missav.setObjectName(u"progressbar_missav")
        self.progressbar_missav.setStyleSheet(u"")
        self.progressbar_missav.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_missav, 5, 1, 1, 1)

        self.progressbar_xhamster = QProgressBar(self.progress_scrollarea_widgedcontents)
        self.progressbar_xhamster.setObjectName(u"progressbar_xhamster")
        self.progressbar_xhamster.setValue(0)

        self.progress_gridlayout_progressbar.addWidget(self.progressbar_xhamster, 6, 1, 1, 1)


        self.gridLayout_18.addLayout(self.progress_gridlayout_progressbar, 1, 0, 1, 1)

        self.progress_scrollarea.setWidget(self.progress_scrollarea_widgedcontents)

        self.gridLayout_6.addWidget(self.progress_scrollarea, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_progressbars)
        self.page_tools = QWidget()
        self.page_tools.setObjectName(u"page_tools")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.page_tools.sizePolicy().hasHeightForWidth())
        self.page_tools.setSizePolicy(sizePolicy9)
        self.page_tools.setMinimumSize(QSize(100, 30))
        self.gridLayout_17 = QGridLayout(self.page_tools)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.page_tools)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_15 = QGridLayout(self.groupBox)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tools_radio_top_porn_all_time = QRadioButton(self.groupBox)
        self.tools_radio_top_porn_all_time.setObjectName(u"tools_radio_top_porn_all_time")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.tools_radio_top_porn_all_time.sizePolicy().hasHeightForWidth())
        self.tools_radio_top_porn_all_time.setSizePolicy(sizePolicy10)
        self.tools_radio_top_porn_all_time.setMinimumSize(QSize(0, 0))
        self.tools_radio_top_porn_all_time.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_radio_top_porn_all_time, 0, 3, 1, 1)

        self.tools_lineedit_hqporner_category = QLineEdit(self.groupBox)
        self.tools_lineedit_hqporner_category.setObjectName(u"tools_lineedit_hqporner_category")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(4)
        sizePolicy11.setHeightForWidth(self.tools_lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_hqporner_category.setSizePolicy(sizePolicy11)
        self.tools_lineedit_hqporner_category.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.tools_lineedit_hqporner_category, 1, 1, 1, 1)

        self.tools_label_get_brazzers_videos = QLabel(self.groupBox)
        self.tools_label_get_brazzers_videos.setObjectName(u"tools_label_get_brazzers_videos")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.tools_label_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.tools_label_get_brazzers_videos.setSizePolicy(sizePolicy12)
        self.tools_label_get_brazzers_videos.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_brazzers_videos, 3, 0, 1, 1)

        self.tools_button_hqporner_category_get_videos = QPushButton(self.groupBox)
        self.tools_button_hqporner_category_get_videos.setObjectName(u"tools_button_hqporner_category_get_videos")
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(2)
        sizePolicy13.setHeightForWidth(self.tools_button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_hqporner_category_get_videos.setSizePolicy(sizePolicy13)
        self.tools_button_hqporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_hqporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_hqporner_category_get_videos, 1, 2, 1, 1)

        self.tools_label_videos_by_category = QLabel(self.groupBox)
        self.tools_label_videos_by_category.setObjectName(u"tools_label_videos_by_category")
        sizePolicy12.setHeightForWidth(self.tools_label_videos_by_category.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category.setSizePolicy(sizePolicy12)
        self.tools_label_videos_by_category.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_videos_by_category, 1, 0, 1, 1)

        self.tools_button_list_categories = QPushButton(self.groupBox)
        self.tools_button_list_categories.setObjectName(u"tools_button_list_categories")
        sizePolicy10.setHeightForWidth(self.tools_button_list_categories.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories.setSizePolicy(sizePolicy10)
        self.tools_button_list_categories.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_list_categories, 1, 3, 1, 1)

        self.tools_label_get_top_porn = QLabel(self.groupBox)
        self.tools_label_get_top_porn.setObjectName(u"tools_label_get_top_porn")
        sizePolicy12.setHeightForWidth(self.tools_label_get_top_porn.sizePolicy().hasHeightForWidth())
        self.tools_label_get_top_porn.setSizePolicy(sizePolicy12)
        self.tools_label_get_top_porn.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_top_porn, 0, 0, 1, 1)

        self.tools_button_get_brazzers_videos = QPushButton(self.groupBox)
        self.tools_button_get_brazzers_videos.setObjectName(u"tools_button_get_brazzers_videos")
        sizePolicy12.setHeightForWidth(self.tools_button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_brazzers_videos.setSizePolicy(sizePolicy12)
        self.tools_button_get_brazzers_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_brazzers_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_get_brazzers_videos, 3, 1, 1, 1)

        self.tools_button_top_porn_get_videos = QPushButton(self.groupBox)
        self.tools_button_top_porn_get_videos.setObjectName(u"tools_button_top_porn_get_videos")
        sizePolicy10.setHeightForWidth(self.tools_button_top_porn_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_top_porn_get_videos.setSizePolicy(sizePolicy10)
        self.tools_button_top_porn_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_top_porn_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_top_porn_get_videos, 0, 4, 1, 1)

        self.tools_label_get_random_video = QLabel(self.groupBox)
        self.tools_label_get_random_video.setObjectName(u"tools_label_get_random_video")
        sizePolicy12.setHeightForWidth(self.tools_label_get_random_video.sizePolicy().hasHeightForWidth())
        self.tools_label_get_random_video.setSizePolicy(sizePolicy12)
        self.tools_label_get_random_video.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_random_video, 2, 0, 1, 1)

        self.tools_radio_top_porn_week = QRadioButton(self.groupBox)
        self.tools_radio_top_porn_week.setObjectName(u"tools_radio_top_porn_week")
        sizePolicy10.setHeightForWidth(self.tools_radio_top_porn_week.sizePolicy().hasHeightForWidth())
        self.tools_radio_top_porn_week.setSizePolicy(sizePolicy10)
        self.tools_radio_top_porn_week.setMinimumSize(QSize(0, 0))
        self.tools_radio_top_porn_week.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tools_radio_top_porn_week.setChecked(True)

        self.gridLayout_3.addWidget(self.tools_radio_top_porn_week, 0, 1, 1, 1)

        self.tools_button_get_random_videos = QPushButton(self.groupBox)
        self.tools_button_get_random_videos.setObjectName(u"tools_button_get_random_videos")
        sizePolicy12.setHeightForWidth(self.tools_button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_random_videos.setSizePolicy(sizePolicy12)
        self.tools_button_get_random_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_random_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_get_random_videos, 2, 1, 1, 1)

        self.tools_radio_top_porn_month = QRadioButton(self.groupBox)
        self.tools_radio_top_porn_month.setObjectName(u"tools_radio_top_porn_month")
        sizePolicy10.setHeightForWidth(self.tools_radio_top_porn_month.sizePolicy().hasHeightForWidth())
        self.tools_radio_top_porn_month.setSizePolicy(sizePolicy10)
        self.tools_radio_top_porn_month.setMinimumSize(QSize(0, 0))
        self.tools_radio_top_porn_month.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_radio_top_porn_month, 0, 2, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox)

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
        sizePolicy11.setHeightForWidth(self.tools_lineedit_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_videos_by_category_eporner.setSizePolicy(sizePolicy11)
        self.tools_lineedit_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_lineedit_videos_by_category_eporner, 4, 1, 1, 2)

        self.tools_button_eporner_category_get_videos = QPushButton(self.groupBox_2)
        self.tools_button_eporner_category_get_videos.setObjectName(u"tools_button_eporner_category_get_videos")
        sizePolicy13.setHeightForWidth(self.tools_button_eporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_eporner_category_get_videos.setSizePolicy(sizePolicy13)
        self.tools_button_eporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_eporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_eporner_category_get_videos, 4, 4, 1, 1)

        self.tools_label_videos_by_category_eporner = QLabel(self.groupBox_2)
        self.tools_label_videos_by_category_eporner.setObjectName(u"tools_label_videos_by_category_eporner")
        sizePolicy12.setHeightForWidth(self.tools_label_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category_eporner.setSizePolicy(sizePolicy12)
        self.tools_label_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_label_videos_by_category_eporner, 4, 0, 1, 1)

        self.tools_button_list_categories_eporner = QPushButton(self.groupBox_2)
        self.tools_button_list_categories_eporner.setObjectName(u"tools_button_list_categories_eporner")
        sizePolicy10.setHeightForWidth(self.tools_button_list_categories_eporner.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories_eporner.setSizePolicy(sizePolicy10)
        self.tools_button_list_categories_eporner.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories_eporner.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_list_categories_eporner, 4, 3, 1, 1)


        self.gridLayout_16.addLayout(self.tools_gridlayout_tools, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_2)


        self.gridLayout_17.addLayout(self.verticalLayout_3, 0, 1, 1, 1)

        self.tools_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_17.addItem(self.tools_vertical_spacer, 1, 1, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_tools)

        self.gridLayout_20.addWidget(self.main_stacked_widget_top, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.main_verticallayout_treewidget.addWidget(self.scrollArea)

        self.main_scrollarea_treewidget = QScrollArea(self.main_widget)
        self.main_scrollarea_treewidget.setObjectName(u"main_scrollarea_treewidget")
        self.main_scrollarea_treewidget.setWidgetResizable(True)
        self.main_scrollarea_treewidget_content = QWidget()
        self.main_scrollarea_treewidget_content.setObjectName(u"main_scrollarea_treewidget_content")
        self.main_scrollarea_treewidget_content.setGeometry(QRect(0, 0, 697, 585))
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(0)
        sizePolicy14.setHeightForWidth(self.main_scrollarea_treewidget_content.sizePolicy().hasHeightForWidth())
        self.main_scrollarea_treewidget_content.setSizePolicy(sizePolicy14)
        self.gridLayout_4 = QGridLayout(self.main_scrollarea_treewidget_content)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_button_tree_download = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_download.setObjectName(u"main_button_tree_download")
        sizePolicy1.setHeightForWidth(self.main_button_tree_download.sizePolicy().hasHeightForWidth())
        self.main_button_tree_download.setSizePolicy(sizePolicy1)
        self.main_button_tree_download.setMinimumSize(QSize(0, 30))
        self.main_button_tree_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_tree_download.setStyleSheet(u"")

        self.gridLayout.addWidget(self.main_button_tree_download, 2, 0, 1, 3)

        self.treeWidget = QTreeWidget(self.main_scrollarea_treewidget_content)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy15)
        self.treeWidget.setMinimumSize(QSize(100, 200))

        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 3)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.main_checkbox_tree_do_not_clear_videos = QCheckBox(self.main_scrollarea_treewidget_content)
        self.main_checkbox_tree_do_not_clear_videos.setObjectName(u"main_checkbox_tree_do_not_clear_videos")

        self.gridLayout_13.addWidget(self.main_checkbox_tree_do_not_clear_videos, 0, 1, 1, 1)

        self.main_button_tree_automated_selection = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_automated_selection.setObjectName(u"main_button_tree_automated_selection")
        sizePolicy9.setHeightForWidth(self.main_button_tree_automated_selection.sizePolicy().hasHeightForWidth())
        self.main_button_tree_automated_selection.setSizePolicy(sizePolicy9)

        self.gridLayout_13.addWidget(self.main_button_tree_automated_selection, 1, 0, 1, 1)

        self.main_checkbox_tree_show_videos_reversed = QCheckBox(self.main_scrollarea_treewidget_content)
        self.main_checkbox_tree_show_videos_reversed.setObjectName(u"main_checkbox_tree_show_videos_reversed")
        self.main_checkbox_tree_show_videos_reversed.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_checkbox_tree_show_videos_reversed, 0, 0, 1, 1)

        self.main_button_tree_keyboard_shortcuts = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_keyboard_shortcuts.setObjectName(u"main_button_tree_keyboard_shortcuts")

        self.gridLayout_13.addWidget(self.main_button_tree_keyboard_shortcuts, 1, 1, 1, 1)

        self.main_button_tree_stop = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_stop.setObjectName(u"main_button_tree_stop")
        sizePolicy1.setHeightForWidth(self.main_button_tree_stop.sizePolicy().hasHeightForWidth())
        self.main_button_tree_stop.setSizePolicy(sizePolicy1)
        self.main_button_tree_stop.setMinimumSize(QSize(0, 30))

        self.gridLayout_13.addWidget(self.main_button_tree_stop, 2, 0, 1, 2)


        self.gridLayout.addLayout(self.gridLayout_13, 1, 0, 1, 3)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.main_scrollarea_treewidget.setWidget(self.main_scrollarea_treewidget_content)

        self.main_verticallayout_treewidget.addWidget(self.main_scrollarea_treewidget)


        self.main_verticallayout.addLayout(self.main_verticallayout_treewidget)


        self.gridLayout_8.addLayout(self.main_verticallayout, 0, 0, 1, 1)

        self.main_stacked_widget_main.addWidget(self.main_widget)
        self.main_page_settings = QWidget()
        self.main_page_settings.setObjectName(u"main_page_settings")
        self.gridLayout_25 = QGridLayout(self.main_page_settings)
        self.gridLayout_25.setSpacing(0)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.gridLayout_25.setContentsMargins(0, 0, 0, 0)
        self.settings_verticallayout = QVBoxLayout()
        self.settings_verticallayout.setSpacing(0)
        self.settings_verticallayout.setObjectName(u"settings_verticallayout")
        self.settings_scrollarea = QScrollArea(self.main_page_settings)
        self.settings_scrollarea.setObjectName(u"settings_scrollarea")
        self.settings_scrollarea.setWidgetResizable(True)
        self.settings_scrollarea_widget_contents = QWidget()
        self.settings_scrollarea_widget_contents.setObjectName(u"settings_scrollarea_widget_contents")
        self.settings_scrollarea_widget_contents.setGeometry(QRect(0, 0, 844, 927))
        self.gridLayout_19 = QGridLayout(self.settings_scrollarea_widget_contents)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.settings_scrollarea_gridlayout = QGridLayout()
        self.settings_scrollarea_gridlayout.setObjectName(u"settings_scrollarea_gridlayout")
        self.settings_groupbox_performance = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_performance.setObjectName(u"settings_groupbox_performance")
        self.gridLayout_9 = QGridLayout(self.settings_groupbox_performance)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.settings_horizontallayout_simultaneous_downloads = QHBoxLayout()
        self.settings_horizontallayout_simultaneous_downloads.setObjectName(u"settings_horizontallayout_simultaneous_downloads")
        self.settings_label_semaphore = QLabel(self.settings_groupbox_performance)
        self.settings_label_semaphore.setObjectName(u"settings_label_semaphore")

        self.settings_horizontallayout_simultaneous_downloads.addWidget(self.settings_label_semaphore)

        self.settings_spinbox_semaphore = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_semaphore.setObjectName(u"settings_spinbox_semaphore")
        self.settings_spinbox_semaphore.setMinimum(1)
        self.settings_spinbox_semaphore.setMaximum(5000)

        self.settings_horizontallayout_simultaneous_downloads.addWidget(self.settings_spinbox_semaphore)

        self.settings_button_semaphore_help = QPushButton(self.settings_groupbox_performance)
        self.settings_button_semaphore_help.setObjectName(u"settings_button_semaphore_help")
        self.settings_button_semaphore_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_simultaneous_downloads.addWidget(self.settings_button_semaphore_help)


        self.gridLayout_9.addLayout(self.settings_horizontallayout_simultaneous_downloads, 2, 0, 1, 1)

        self.settings_horizontallayout_maximal_workers = QHBoxLayout()
        self.settings_horizontallayout_maximal_workers.setObjectName(u"settings_horizontallayout_maximal_workers")
        self.settings_horizontallayout_maximal_workers.setContentsMargins(6, 3, 6, 6)
        self.settings_label_maximal_workers = QLabel(self.settings_groupbox_performance)
        self.settings_label_maximal_workers.setObjectName(u"settings_label_maximal_workers")

        self.settings_horizontallayout_maximal_workers.addWidget(self.settings_label_maximal_workers)

        self.settings_spinbox_maximal_workers = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_maximal_workers.setObjectName(u"settings_spinbox_maximal_workers")
        self.settings_spinbox_maximal_workers.setMinimum(1)
        self.settings_spinbox_maximal_workers.setMaximum(5000)

        self.settings_horizontallayout_maximal_workers.addWidget(self.settings_spinbox_maximal_workers)

        self.settings_button_workers_help = QPushButton(self.settings_groupbox_performance)
        self.settings_button_workers_help.setObjectName(u"settings_button_workers_help")
        self.settings_button_workers_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_maximal_workers.addWidget(self.settings_button_workers_help)


        self.gridLayout_9.addLayout(self.settings_horizontallayout_maximal_workers, 4, 0, 1, 1)

        self.settings_horizontallayout_maximal_timeout = QHBoxLayout()
        self.settings_horizontallayout_maximal_timeout.setObjectName(u"settings_horizontallayout_maximal_timeout")
        self.settings_horizontallayout_maximal_timeout.setContentsMargins(6, 3, 6, 6)
        self.settings_label_maximal_timeout = QLabel(self.settings_groupbox_performance)
        self.settings_label_maximal_timeout.setObjectName(u"settings_label_maximal_timeout")

        self.settings_horizontallayout_maximal_timeout.addWidget(self.settings_label_maximal_timeout)

        self.settings_spinbox_maximal_timeout = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_maximal_timeout.setObjectName(u"settings_spinbox_maximal_timeout")
        self.settings_spinbox_maximal_timeout.setMinimum(5)
        self.settings_spinbox_maximal_timeout.setMaximum(5000)

        self.settings_horizontallayout_maximal_timeout.addWidget(self.settings_spinbox_maximal_timeout)

        self.settings_button_timeout_help = QPushButton(self.settings_groupbox_performance)
        self.settings_button_timeout_help.setObjectName(u"settings_button_timeout_help")
        self.settings_button_timeout_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.settings_button_timeout_help.setStyleSheet(u"")

        self.settings_horizontallayout_maximal_timeout.addWidget(self.settings_button_timeout_help)


        self.gridLayout_9.addLayout(self.settings_horizontallayout_maximal_timeout, 5, 0, 1, 1)

        self.settings_horizontallayout_maximal_retries = QHBoxLayout()
        self.settings_horizontallayout_maximal_retries.setObjectName(u"settings_horizontallayout_maximal_retries")
        self.settings_horizontallayout_maximal_retries.setContentsMargins(6, 3, 6, 6)
        self.settings_label_maximal_retries = QLabel(self.settings_groupbox_performance)
        self.settings_label_maximal_retries.setObjectName(u"settings_label_maximal_retries")

        self.settings_horizontallayout_maximal_retries.addWidget(self.settings_label_maximal_retries)

        self.settings_spinbox_maximal_retries = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_maximal_retries.setObjectName(u"settings_spinbox_maximal_retries")
        self.settings_spinbox_maximal_retries.setMinimum(5)
        self.settings_spinbox_maximal_retries.setMaximum(5000)

        self.settings_horizontallayout_maximal_retries.addWidget(self.settings_spinbox_maximal_retries)

        self.settings_button_timeout_maximal_retries_help = QPushButton(self.settings_groupbox_performance)
        self.settings_button_timeout_maximal_retries_help.setObjectName(u"settings_button_timeout_maximal_retries_help")
        self.settings_button_timeout_maximal_retries_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_maximal_retries.addWidget(self.settings_button_timeout_maximal_retries_help)


        self.gridLayout_9.addLayout(self.settings_horizontallayout_maximal_retries, 6, 0, 1, 1)

        self.settings_horizontallayout_pornhub_delay = QHBoxLayout()
        self.settings_horizontallayout_pornhub_delay.setObjectName(u"settings_horizontallayout_pornhub_delay")
        self.settings_horizontallayout_pornhub_delay.setContentsMargins(6, 3, 6, 6)
        self.settings_label_pornhub_delay = QLabel(self.settings_groupbox_performance)
        self.settings_label_pornhub_delay.setObjectName(u"settings_label_pornhub_delay")

        self.settings_horizontallayout_pornhub_delay.addWidget(self.settings_label_pornhub_delay)

        self.settings_spinbox_pornhub_delay = QSpinBox(self.settings_groupbox_performance)
        self.settings_spinbox_pornhub_delay.setObjectName(u"settings_spinbox_pornhub_delay")
        self.settings_spinbox_pornhub_delay.setMinimum(0)
        self.settings_spinbox_pornhub_delay.setMaximum(5000)

        self.settings_horizontallayout_pornhub_delay.addWidget(self.settings_spinbox_pornhub_delay)

        self.settings_button_pornhub_delay_help = QPushButton(self.settings_groupbox_performance)
        self.settings_button_pornhub_delay_help.setObjectName(u"settings_button_pornhub_delay_help")
        self.settings_button_pornhub_delay_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_pornhub_delay.addWidget(self.settings_button_pornhub_delay_help)


        self.gridLayout_9.addLayout(self.settings_horizontallayout_pornhub_delay, 3, 0, 1, 1)

        self.settings_horizontallayout_threading_mode = QHBoxLayout()
        self.settings_horizontallayout_threading_mode.setObjectName(u"settings_horizontallayout_threading_mode")
        self.settings_horizontallayout_threading_mode.setContentsMargins(6, 3, 6, 6)
        self.settings_label_threading_mode = QLabel(self.settings_groupbox_performance)
        self.settings_label_threading_mode.setObjectName(u"settings_label_threading_mode")
        sizePolicy7.setHeightForWidth(self.settings_label_threading_mode.sizePolicy().hasHeightForWidth())
        self.settings_label_threading_mode.setSizePolicy(sizePolicy7)

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_label_threading_mode)

        self.settings_radio_threading_mode_high_performance = QRadioButton(self.settings_groupbox_performance)
        self.settings_radio_threading_mode_high_performance.setObjectName(u"settings_radio_threading_mode_high_performance")
        self.settings_radio_threading_mode_high_performance.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_radio_threading_mode_high_performance)

        self.settings_radio_threading_mode_ffmpeg = QRadioButton(self.settings_groupbox_performance)
        self.settings_radio_threading_mode_ffmpeg.setObjectName(u"settings_radio_threading_mode_ffmpeg")
        self.settings_radio_threading_mode_ffmpeg.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_radio_threading_mode_ffmpeg)

        self.settings_radio_threading_mode_default = QRadioButton(self.settings_groupbox_performance)
        self.settings_radio_threading_mode_default.setObjectName(u"settings_radio_threading_mode_default")
        self.settings_radio_threading_mode_default.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_radio_threading_mode_default)

        self.settings_button_threading_mode_help = QPushButton(self.settings_groupbox_performance)
        self.settings_button_threading_mode_help.setObjectName(u"settings_button_threading_mode_help")
        self.settings_button_threading_mode_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_horizontallayout_threading_mode.addWidget(self.settings_button_threading_mode_help)


        self.gridLayout_9.addLayout(self.settings_horizontallayout_threading_mode, 1, 0, 1, 1)


        self.settings_scrollarea_gridlayout.addWidget(self.settings_groupbox_performance, 0, 0, 1, 1)

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
        sizePolicy7.setHeightForWidth(self.settings_label_ui_language.sizePolicy().hasHeightForWidth())
        self.settings_label_ui_language.setSizePolicy(sizePolicy7)

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


        self.gridLayout_12.addLayout(self.settings_gridlayout_graphical_userinterface, 0, 0, 1, 1)


        self.settings_scrollarea_gridlayout.addWidget(self.settings_groupbox_ui, 3, 0, 1, 1)

        self.settings_groupbox_system_pornfetch = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_system_pornfetch.setObjectName(u"settings_groupbox_system_pornfetch")
        self.gridLayout_7 = QGridLayout(self.settings_groupbox_system_pornfetch)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.settings_gridlayout_system_pornfetch = QGridLayout()
        self.settings_gridlayout_system_pornfetch.setObjectName(u"settings_gridlayout_system_pornfetch")
        self.settings_gridlayout_system_pornfetch.setContentsMargins(6, 3, 6, 6)
        self.settings_button_help_tor = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_help_tor.setObjectName(u"settings_button_help_tor")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_help_tor, 4, 1, 1, 1)

        self.settings_label_startup = QLabel(self.settings_groupbox_system_pornfetch)
        self.settings_label_startup.setObjectName(u"settings_label_startup")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.settings_label_startup.sizePolicy().hasHeightForWidth())
        self.settings_label_startup.setSizePolicy(sizePolicy16)

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_label_startup, 2, 0, 1, 1)

        self.settings_button_download_ffmpeg = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_download_ffmpeg.setObjectName(u"settings_button_download_ffmpeg")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_download_ffmpeg, 0, 0, 1, 3)

        self.settings_button_help_anonymous_mode = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_help_anonymous_mode.setObjectName(u"settings_button_help_anonymous_mode")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_help_anonymous_mode, 4, 2, 1, 1)

        self.settings_checkbox_internet_checks = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_internet_checks.setObjectName(u"settings_checkbox_internet_checks")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_internet_checks, 2, 2, 1, 1)

        self.settings_checkbox_system_update_checks = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_update_checks.setObjectName(u"settings_checkbox_system_update_checks")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_update_checks, 2, 1, 1, 1)

        self.settings_button_install_pornfetch = QPushButton(self.settings_groupbox_system_pornfetch)
        self.settings_button_install_pornfetch.setObjectName(u"settings_button_install_pornfetch")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_button_install_pornfetch, 1, 0, 1, 3)

        self.settings_label_system_privacy = QLabel(self.settings_groupbox_system_pornfetch)
        self.settings_label_system_privacy.setObjectName(u"settings_label_system_privacy")
        sizePolicy16.setHeightForWidth(self.settings_label_system_privacy.sizePolicy().hasHeightForWidth())
        self.settings_label_system_privacy.setSizePolicy(sizePolicy16)

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_label_system_privacy, 3, 0, 1, 1)

        self.settings_checkbox_system_anonymous_mode = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_anonymous_mode.setObjectName(u"settings_checkbox_system_anonymous_mode")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_anonymous_mode, 3, 1, 1, 1)

        self.settings_checkbox_system_activate_proxy = QCheckBox(self.settings_groupbox_system_pornfetch)
        self.settings_checkbox_system_activate_proxy.setObjectName(u"settings_checkbox_system_activate_proxy")

        self.settings_gridlayout_system_pornfetch.addWidget(self.settings_checkbox_system_activate_proxy, 3, 2, 1, 1)


        self.gridLayout_7.addLayout(self.settings_gridlayout_system_pornfetch, 2, 0, 1, 1)


        self.settings_scrollarea_gridlayout.addWidget(self.settings_groupbox_system_pornfetch, 2, 0, 1, 1)

        self.settings_horizontallayout_videos_post_processing = QHBoxLayout()
        self.settings_horizontallayout_videos_post_processing.setObjectName(u"settings_horizontallayout_videos_post_processing")
        self.settings_groupbox_videos = QGroupBox(self.settings_scrollarea_widget_contents)
        self.settings_groupbox_videos.setObjectName(u"settings_groupbox_videos")
        self.gridLayout_10 = QGridLayout(self.settings_groupbox_videos)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setHorizontalSpacing(6)
        self.gridLayout_10.setContentsMargins(6, 3, 6, 6)
        self.settings_gridlayout_videos = QGridLayout()
        self.settings_gridlayout_videos.setObjectName(u"settings_gridlayout_videos")
        self.settings_gridlayout_videos.setContentsMargins(6, 3, 6, 6)
        self.settings_radio_quality_worst = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_quality_worst.setObjectName(u"settings_radio_quality_worst")
        self.settings_radio_quality_worst.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_radio_quality_worst, 0, 3, 1, 2)

        self.settings_radio_quality_best = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_quality_best.setObjectName(u"settings_radio_quality_best")
        self.settings_radio_quality_best.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_radio_quality_best, 0, 1, 1, 1)

        self.settings_button_directory_system_help = QPushButton(self.settings_groupbox_videos)
        self.settings_button_directory_system_help.setObjectName(u"settings_button_directory_system_help")
        self.settings_button_directory_system_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_button_directory_system_help, 10, 1, 1, 1)

        self.settings_checkbox_videos_use_directory_system = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_use_directory_system.setObjectName(u"settings_checkbox_videos_use_directory_system")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_use_directory_system, 10, 0, 1, 1)

        self.button_help_write_metadata_tags = QPushButton(self.settings_groupbox_videos)
        self.button_help_write_metadata_tags.setObjectName(u"button_help_write_metadata_tags")

        self.settings_gridlayout_videos.addWidget(self.button_help_write_metadata_tags, 9, 1, 1, 1)

        self.settings_label_output_path = QLabel(self.settings_groupbox_videos)
        self.settings_label_output_path.setObjectName(u"settings_label_output_path")

        self.settings_gridlayout_videos.addWidget(self.settings_label_output_path, 7, 0, 1, 1)

        self.radio_settings_post_processing_do_not_convert = QRadioButton(self.settings_groupbox_videos)
        self.radio_settings_post_processing_do_not_convert.setObjectName(u"radio_settings_post_processing_do_not_convert")

        self.settings_gridlayout_videos.addWidget(self.radio_settings_post_processing_do_not_convert, 8, 0, 1, 1)

        self.checkbox_settings_post_processing_write_metadata_tags = QCheckBox(self.settings_groupbox_videos)
        self.checkbox_settings_post_processing_write_metadata_tags.setObjectName(u"checkbox_settings_post_processing_write_metadata_tags")

        self.settings_gridlayout_videos.addWidget(self.checkbox_settings_post_processing_write_metadata_tags, 9, 0, 1, 1)

        self.settings_label_settings_videos_model = QLabel(self.settings_groupbox_videos)
        self.settings_label_settings_videos_model.setObjectName(u"settings_label_settings_videos_model")

        self.settings_gridlayout_videos.addWidget(self.settings_label_settings_videos_model, 5, 0, 1, 1)

        self.settings_button_output_path_select = QPushButton(self.settings_groupbox_videos)
        self.settings_button_output_path_select.setObjectName(u"settings_button_output_path_select")
        self.settings_button_output_path_select.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_button_output_path_select, 7, 3, 1, 2)

        self.settings_label_searching_limit = QLabel(self.settings_groupbox_videos)
        self.settings_label_searching_limit.setObjectName(u"settings_label_searching_limit")

        self.settings_gridlayout_videos.addWidget(self.settings_label_searching_limit, 6, 0, 1, 1)

        self.settings_button_result_limit_help = QPushButton(self.settings_groupbox_videos)
        self.settings_button_result_limit_help.setObjectName(u"settings_button_result_limit_help")
        self.settings_button_result_limit_help.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_button_result_limit_help, 6, 3, 1, 2)

        self.radio_settings_post_processing_use_custom_format = QRadioButton(self.settings_groupbox_videos)
        self.radio_settings_post_processing_use_custom_format.setObjectName(u"radio_settings_post_processing_use_custom_format")

        self.settings_gridlayout_videos.addWidget(self.radio_settings_post_processing_use_custom_format, 8, 1, 1, 1)

        self.settings_label_quality = QLabel(self.settings_groupbox_videos)
        self.settings_label_quality.setObjectName(u"settings_label_quality")
        sizePolicy7.setHeightForWidth(self.settings_label_quality.sizePolicy().hasHeightForWidth())
        self.settings_label_quality.setSizePolicy(sizePolicy7)

        self.settings_gridlayout_videos.addWidget(self.settings_label_quality, 0, 0, 1, 1)

        self.settings_radio_model_both = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_model_both.setObjectName(u"settings_radio_model_both")

        self.settings_gridlayout_videos.addWidget(self.settings_radio_model_both, 5, 3, 1, 1)

        self.settings_radio_model_featured = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_model_featured.setObjectName(u"settings_radio_model_featured")

        self.settings_gridlayout_videos.addWidget(self.settings_radio_model_featured, 5, 2, 1, 1)

        self.settings_spinbox_treewidget_limit = QSpinBox(self.settings_groupbox_videos)
        self.settings_spinbox_treewidget_limit.setObjectName(u"settings_spinbox_treewidget_limit")
        self.settings_spinbox_treewidget_limit.setMinimum(1)
        self.settings_spinbox_treewidget_limit.setMaximum(5000)

        self.settings_gridlayout_videos.addWidget(self.settings_spinbox_treewidget_limit, 6, 1, 1, 2)

        self.settings_lineedit_output_path = QLineEdit(self.settings_groupbox_videos)
        self.settings_lineedit_output_path.setObjectName(u"settings_lineedit_output_path")
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.settings_lineedit_output_path.sizePolicy().hasHeightForWidth())
        self.settings_lineedit_output_path.setSizePolicy(sizePolicy17)

        self.settings_gridlayout_videos.addWidget(self.settings_lineedit_output_path, 7, 1, 1, 2)

        self.settings_button_help_model_videos = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_model_videos.setObjectName(u"settings_button_help_model_videos")

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_model_videos, 5, 4, 1, 1)

        self.settings_radio_quality_half = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_quality_half.setObjectName(u"settings_radio_quality_half")
        self.settings_radio_quality_half.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_videos.addWidget(self.settings_radio_quality_half, 0, 2, 1, 1)

        self.lineedit_settings_post_processing_use_custom_format = QLineEdit(self.settings_groupbox_videos)
        self.lineedit_settings_post_processing_use_custom_format.setObjectName(u"lineedit_settings_post_processing_use_custom_format")

        self.settings_gridlayout_videos.addWidget(self.lineedit_settings_post_processing_use_custom_format, 8, 2, 1, 2)

        self.settings_radio_model_uploads = QRadioButton(self.settings_groupbox_videos)
        self.settings_radio_model_uploads.setObjectName(u"settings_radio_model_uploads")

        self.settings_gridlayout_videos.addWidget(self.settings_radio_model_uploads, 5, 1, 1, 1)

        self.settings_checkbox_videos_skip_existing_files = QCheckBox(self.settings_groupbox_videos)
        self.settings_checkbox_videos_skip_existing_files.setObjectName(u"settings_checkbox_videos_skip_existing_files")

        self.settings_gridlayout_videos.addWidget(self.settings_checkbox_videos_skip_existing_files, 11, 0, 1, 1)

        self.settings_button_help_skip_existing_files = QPushButton(self.settings_groupbox_videos)
        self.settings_button_help_skip_existing_files.setObjectName(u"settings_button_help_skip_existing_files")

        self.settings_gridlayout_videos.addWidget(self.settings_button_help_skip_existing_files, 11, 1, 1, 1)


        self.gridLayout_10.addLayout(self.settings_gridlayout_videos, 6, 0, 1, 1)


        self.settings_horizontallayout_videos_post_processing.addWidget(self.settings_groupbox_videos)


        self.settings_scrollarea_gridlayout.addLayout(self.settings_horizontallayout_videos_post_processing, 1, 0, 1, 1)


        self.gridLayout_19.addLayout(self.settings_scrollarea_gridlayout, 0, 0, 1, 2)

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

        self.settings_scrollarea.setWidget(self.settings_scrollarea_widget_contents)

        self.settings_verticallayout.addWidget(self.settings_scrollarea)


        self.gridLayout_25.addLayout(self.settings_verticallayout, 0, 0, 1, 1)

        self.main_stacked_widget_main.addWidget(self.main_page_settings)
        self.main_page_credits = QWidget()
        self.main_page_credits.setObjectName(u"main_page_credits")
        self.gridLayout_26 = QGridLayout(self.main_page_credits)
        self.gridLayout_26.setSpacing(0)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridLayout_26.setContentsMargins(0, 0, 0, 0)
        self.main_gridlayout_textbrowser = QGridLayout()
        self.main_gridlayout_textbrowser.setObjectName(u"main_gridlayout_textbrowser")
        self.main_textbrowser_credits = QTextBrowser(self.main_page_credits)
        self.main_textbrowser_credits.setObjectName(u"main_textbrowser_credits")

        self.main_gridlayout_textbrowser.addWidget(self.main_textbrowser_credits, 0, 0, 1, 1)


        self.gridLayout_26.addLayout(self.main_gridlayout_textbrowser, 0, 0, 1, 1)

        self.main_stacked_widget_main.addWidget(self.main_page_credits)
        self.main_page_supported_websites = QWidget()
        self.main_page_supported_websites.setObjectName(u"main_page_supported_websites")
        self.gridLayout_11 = QGridLayout(self.main_page_supported_websites)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.main_textbrowser_supported_websites = QTextBrowser(self.main_page_supported_websites)
        self.main_textbrowser_supported_websites.setObjectName(u"main_textbrowser_supported_websites")

        self.gridLayout_11.addWidget(self.main_textbrowser_supported_websites, 0, 0, 1, 1)

        self.main_stacked_widget_main.addWidget(self.main_page_supported_websites)

        self.verticallayout_main.addWidget(self.main_stacked_widget_main)

        self.groupBox_3 = QGroupBox(PornFetch_Android)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_14 = QGridLayout(self.groupBox_3)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setHorizontalSpacing(0)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.main_horizontallayout_menu_buttons = QHBoxLayout()
        self.main_horizontallayout_menu_buttons.setSpacing(5)
        self.main_horizontallayout_menu_buttons.setObjectName(u"main_horizontallayout_menu_buttons")
        self.main_button_switch_home = QPushButton(self.groupBox_3)
        self.main_button_switch_home.setObjectName(u"main_button_switch_home")
        sizePolicy1.setHeightForWidth(self.main_button_switch_home.sizePolicy().hasHeightForWidth())
        self.main_button_switch_home.setSizePolicy(sizePolicy1)
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

        self.main_button_switch_account = QPushButton(self.groupBox_3)
        self.main_button_switch_account.setObjectName(u"main_button_switch_account")
        sizePolicy1.setHeightForWidth(self.main_button_switch_account.sizePolicy().hasHeightForWidth())
        self.main_button_switch_account.setSizePolicy(sizePolicy1)
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

        self.main_button_switch_tools = QPushButton(self.groupBox_3)
        self.main_button_switch_tools.setObjectName(u"main_button_switch_tools")
        sizePolicy1.setHeightForWidth(self.main_button_switch_tools.sizePolicy().hasHeightForWidth())
        self.main_button_switch_tools.setSizePolicy(sizePolicy1)
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

        self.main_button_switch_settings = QPushButton(self.groupBox_3)
        self.main_button_switch_settings.setObjectName(u"main_button_switch_settings")
        sizePolicy1.setHeightForWidth(self.main_button_switch_settings.sizePolicy().hasHeightForWidth())
        self.main_button_switch_settings.setSizePolicy(sizePolicy1)
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


        self.gridLayout_14.addLayout(self.main_horizontallayout_menu_buttons, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.main_button_switch_credits = QPushButton(self.groupBox_3)
        self.main_button_switch_credits.setObjectName(u"main_button_switch_credits")
        sizePolicy1.setHeightForWidth(self.main_button_switch_credits.sizePolicy().hasHeightForWidth())
        self.main_button_switch_credits.setSizePolicy(sizePolicy1)
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

        self.horizontalLayout.addWidget(self.main_button_switch_credits)

        self.main_button_view_progress_bars = QPushButton(self.groupBox_3)
        self.main_button_view_progress_bars.setObjectName(u"main_button_view_progress_bars")
        sizePolicy1.setHeightForWidth(self.main_button_view_progress_bars.sizePolicy().hasHeightForWidth())
        self.main_button_view_progress_bars.setSizePolicy(sizePolicy1)
        self.main_button_view_progress_bars.setMinimumSize(QSize(50, 35))
        self.main_button_view_progress_bars.setMaximumSize(QSize(16777215, 35))
        self.main_button_view_progress_bars.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_view_progress_bars.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}")
        self.main_button_view_progress_bars.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.main_button_view_progress_bars)

        self.main_button_switch_supported_websites = QPushButton(self.groupBox_3)
        self.main_button_switch_supported_websites.setObjectName(u"main_button_switch_supported_websites")
        sizePolicy1.setHeightForWidth(self.main_button_switch_supported_websites.sizePolicy().hasHeightForWidth())
        self.main_button_switch_supported_websites.setSizePolicy(sizePolicy1)
        self.main_button_switch_supported_websites.setMinimumSize(QSize(50, 35))
        self.main_button_switch_supported_websites.setMaximumSize(QSize(16777215, 35))
        self.main_button_switch_supported_websites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_switch_supported_websites.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}")
        self.main_button_switch_supported_websites.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.main_button_switch_supported_websites)


        self.gridLayout_14.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.formlayout_progressbar = QFormLayout()
        self.formlayout_progressbar.setObjectName(u"formlayout_progressbar")
        self.formlayout_progressbar.setHorizontalSpacing(0)
        self.formlayout_progressbar.setVerticalSpacing(0)
        self.main_label_progressbar_total = QLabel(self.groupBox_3)
        self.main_label_progressbar_total.setObjectName(u"main_label_progressbar_total")

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_total)

        self.main_progressbar_total = QProgressBar(self.groupBox_3)
        self.main_progressbar_total.setObjectName(u"main_progressbar_total")
        sizePolicy8.setHeightForWidth(self.main_progressbar_total.sizePolicy().hasHeightForWidth())
        self.main_progressbar_total.setSizePolicy(sizePolicy8)
        self.main_progressbar_total.setMinimumSize(QSize(300, 0))
        self.main_progressbar_total.setStyleSheet(u"text-align: center; /* Centered text */")
        self.main_progressbar_total.setValue(0)

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.FieldRole, self.main_progressbar_total)

        self.main_label_progressbar_converting = QLabel(self.groupBox_3)
        self.main_label_progressbar_converting.setObjectName(u"main_label_progressbar_converting")

        self.formlayout_progressbar.setWidget(1, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_converting)

        self.main_progressbar_converting = QProgressBar(self.groupBox_3)
        self.main_progressbar_converting.setObjectName(u"main_progressbar_converting")
        self.main_progressbar_converting.setStyleSheet(u"text-align: center; /* Centered text */")
        self.main_progressbar_converting.setValue(0)

        self.formlayout_progressbar.setWidget(1, QFormLayout.ItemRole.FieldRole, self.main_progressbar_converting)


        self.gridLayout_14.addLayout(self.formlayout_progressbar, 2, 0, 1, 1)


        self.verticallayout_main.addWidget(self.groupBox_3)


        self.gridLayout_21.addLayout(self.verticallayout_main, 0, 0, 1, 1)


        self.retranslateUi(PornFetch_Android)

        self.main_stacked_widget_main.setCurrentIndex(0)
        self.main_stacked_widget_top.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(PornFetch_Android)
    # setupUi

    def retranslateUi(self, PornFetch_Android):
        PornFetch_Android.setWindowTitle(QCoreApplication.translate("PornFetch_Android", u"UI_android", None))
        self.lineEdit.setText(QCoreApplication.translate("PornFetch_Android", u"Current Status: ", None))
        self.main_stacked_widget_main.setStyleSheet("")
        self.download_button_download.setText(QCoreApplication.translate("PornFetch_Android", u"Download", None))
        self.download_radio_search_website_pornhub.setText(QCoreApplication.translate("PornFetch_Android", u"PornHub", None))
        self.download_lineedit_search_query.setText("")
        self.download_lineedit_search_query.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Search for Videos. Select Website below", None))
        self.download_label_playlist_url.setText(QCoreApplication.translate("PornFetch_Android", u"Playlist URL:", None))
        self.download_label_search_website.setText(QCoreApplication.translate("PornFetch_Android", u"Search Website", None))
        self.download_label_file.setText(QCoreApplication.translate("PornFetch_Android", u"File:", None))
        self.download_label_model_url.setText(QCoreApplication.translate("PornFetch_Android", u"Model URL:", None))
        self.button_search.setText(QCoreApplication.translate("PornFetch_Android", u"Start", None))
        self.download_radio_search_website_hqporner.setText(QCoreApplication.translate("PornFetch_Android", u"HQPorner", None))
        self.download_label_url.setText(QCoreApplication.translate("PornFetch_Android", u"URL:", None))
        self.download_lineedit_file.setText("")
        self.download_lineedit_file.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"URLs in the file must be separated with new lines!", None))
        self.download_radio_search_website_xvideos.setText(QCoreApplication.translate("PornFetch_Android", u"XVideos", None))
        self.download_button_model.setText(QCoreApplication.translate("PornFetch_Android", u"Get Videos", None))
        self.download_lineedit_playlist_url.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter a PornHub Playlist URL", None))
        self.download_button_help_file.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.download_radio_search_website_xnxx.setText(QCoreApplication.translate("PornFetch_Android", u"XNXX", None))
        self.download_lineedit_url.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter video URL", None))
        self.download_lineedit_model_url.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter Model / Channel / Actress URL", None))
        self.download_label_search.setText(QCoreApplication.translate("PornFetch_Android", u"Search Query:", None))
        self.download_button_open_file.setText(QCoreApplication.translate("PornFetch_Android", u"Open File", None))
        self.download_radio_search_website_eporner.setText(QCoreApplication.translate("PornFetch_Android", u"EPorner", None))
        self.download_button_playlist_get_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Videos", None))
        self.login_label_password.setText(QCoreApplication.translate("PornFetch_Android", u"Password:", None))
        self.login_label_username.setText(QCoreApplication.translate("PornFetch_Android", u"E-Mail:", None))
        self.login_button_login.setText(QCoreApplication.translate("PornFetch_Android", u"Login", None))
        self.login_lineedit_username.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter your PornHub E-Mail address (not your username, pornhub changed it) ", None))
        self.login_button_get_watched_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get watched videos", None))
        self.login_lineedit_password.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter your PornHub Password", None))
        self.login_button_get_recommended_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get recommended videos", None))
        self.login_button_get_liked_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Liked videos", None))
        self.progress_label_pornhub.setText(QCoreApplication.translate("PornFetch_Android", u"PornHub:", None))
        self.progress_label_xvideos.setText(QCoreApplication.translate("PornFetch_Android", u"XVideos:", None))
        self.progress_label_eporner.setText(QCoreApplication.translate("PornFetch_Android", u"Eporner:", None))
        self.progress_label_info.setText(QCoreApplication.translate("PornFetch_Android", u"Info:", None))
        self.progress_label_hqporner.setText(QCoreApplication.translate("PornFetch_Android", u"HQPorner:", None))
        self.progress_label_missav.setText(QCoreApplication.translate("PornFetch_Android", u"MissAV", None))
        self.progress_lineedit_download_info.setText("")
        self.progress_label_xnxx.setText(QCoreApplication.translate("PornFetch_Android", u"XNXX:", None))
        self.progress_label_xhamster.setText(QCoreApplication.translate("PornFetch_Android", u"XHamster", None))
        self.groupBox.setTitle(QCoreApplication.translate("PornFetch_Android", u"HQPorner", None))
        self.tools_radio_top_porn_all_time.setText(QCoreApplication.translate("PornFetch_Android", u"All Time", None))
        self.tools_label_get_brazzers_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Brazzers videos", None))
        self.tools_button_hqporner_category_get_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Videos", None))
        self.tools_label_videos_by_category.setText(QCoreApplication.translate("PornFetch_Android", u"Get videos by category", None))
        self.tools_button_list_categories.setText(QCoreApplication.translate("PornFetch_Android", u"List of all categories", None))
        self.tools_label_get_top_porn.setText(QCoreApplication.translate("PornFetch_Android", u"Get Top Porn:", None))
        self.tools_button_get_brazzers_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Videos", None))
        self.tools_button_top_porn_get_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Videos", None))
        self.tools_label_get_random_video.setText(QCoreApplication.translate("PornFetch_Android", u"Get random video", None))
        self.tools_radio_top_porn_week.setText(QCoreApplication.translate("PornFetch_Android", u"Week", None))
        self.tools_button_get_random_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Video", None))
        self.tools_radio_top_porn_month.setText(QCoreApplication.translate("PornFetch_Android", u"Month", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("PornFetch_Android", u"EPorner", None))
        self.tools_button_eporner_category_get_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Get Videos", None))
        self.tools_label_videos_by_category_eporner.setText(QCoreApplication.translate("PornFetch_Android", u"Get videos by category", None))
        self.tools_button_list_categories_eporner.setText(QCoreApplication.translate("PornFetch_Android", u"List of all categories", None))
        self.main_button_tree_download.setText(QCoreApplication.translate("PornFetch_Android", u"Download Selected Videos", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("PornFetch_Android", u"Duration (minutes)", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("PornFetch_Android", u"Author", None));
        self.main_checkbox_tree_do_not_clear_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Do not clear videos", None))
        self.main_button_tree_automated_selection.setText(QCoreApplication.translate("PornFetch_Android", u"Automated selection tool", None))
        self.main_checkbox_tree_show_videos_reversed.setText(QCoreApplication.translate("PornFetch_Android", u"Show videos in reverse", None))
        self.main_button_tree_keyboard_shortcuts.setText(QCoreApplication.translate("PornFetch_Android", u"Keyboard shortcuts", None))
#if QT_CONFIG(tooltip)
        self.main_button_tree_stop.setToolTip(QCoreApplication.translate("PornFetch_Android", u"Does not stop downloading videos", None))
#endif // QT_CONFIG(tooltip)
        self.main_button_tree_stop.setText(QCoreApplication.translate("PornFetch_Android", u"Stop loading videos", None))
        self.settings_groupbox_performance.setTitle(QCoreApplication.translate("PornFetch_Android", u"Performance", None))
        self.settings_label_semaphore.setText(QCoreApplication.translate("PornFetch_Android", u"Simultaneous downloads:", None))
        self.settings_button_semaphore_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_maximal_workers.setText(QCoreApplication.translate("PornFetch_Android", u"Maximal workers:", None))
        self.settings_button_workers_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_maximal_timeout.setText(QCoreApplication.translate("PornFetch_Android", u"Maximal timeout:", None))
        self.settings_button_timeout_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_maximal_retries.setText(QCoreApplication.translate("PornFetch_Android", u"Maximal retries:", None))
        self.settings_button_timeout_maximal_retries_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_pornhub_delay.setText(QCoreApplication.translate("PornFetch_Android", u"Network delay (per Request, in seconds):", None))
        self.settings_button_pornhub_delay_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_threading_mode.setText(QCoreApplication.translate("PornFetch_Android", u"Download Mode:", None))
        self.settings_radio_threading_mode_high_performance.setText(QCoreApplication.translate("PornFetch_Android", u"High Performance", None))
        self.settings_radio_threading_mode_ffmpeg.setText(QCoreApplication.translate("PornFetch_Android", u"FFMPEG", None))
        self.settings_radio_threading_mode_default.setText(QCoreApplication.translate("PornFetch_Android", u"Default", None))
        self.settings_button_threading_mode_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_groupbox_ui.setTitle(QCoreApplication.translate("PornFetch_Android", u"Graphical User Interface", None))
        self.settings_radio_ui_language_system_default.setText(QCoreApplication.translate("PornFetch_Android", u"System default", None))
        self.settings_label_ui_language.setText(QCoreApplication.translate("PornFetch_Android", u"Graphical User Interface Language:", None))
        self.settings_radio_ui_language_english.setText(QCoreApplication.translate("PornFetch_Android", u"English", None))
        self.settings_radio_ui_language_french.setText(QCoreApplication.translate("PornFetch_Android", u"French", None))
        self.settings_radio_ui_language_chinese_simplified.setText(QCoreApplication.translate("PornFetch_Android", u"Chinese (simplified)", None))
        self.settings_radio_ui_language_german.setText(QCoreApplication.translate("PornFetch_Android", u"German", None))
        self.settings_checkbox_ui_custom_font.setText(QCoreApplication.translate("PornFetch_Android", u"Enable custom font (Jetbrains Mono)", None))
        self.settings_groupbox_system_pornfetch.setTitle(QCoreApplication.translate("PornFetch_Android", u"System / Porn Fetch", None))
        self.settings_button_help_tor.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_startup.setText(QCoreApplication.translate("PornFetch_Android", u"Startup:", None))
        self.settings_button_download_ffmpeg.setText(QCoreApplication.translate("PornFetch_Android", u"Download and Setup FFmpeg", None))
        self.settings_button_help_anonymous_mode.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_checkbox_internet_checks.setText(QCoreApplication.translate("PornFetch_Android", u"Internet checks", None))
        self.settings_checkbox_system_update_checks.setText(QCoreApplication.translate("PornFetch_Android", u"Update checks", None))
        self.settings_button_install_pornfetch.setText(QCoreApplication.translate("PornFetch_Android", u"Install Porn Fetch", None))
        self.settings_label_system_privacy.setText(QCoreApplication.translate("PornFetch_Android", u"Privacy:", None))
        self.settings_checkbox_system_anonymous_mode.setText(QCoreApplication.translate("PornFetch_Android", u"Enable Anonymous mode", None))
        self.settings_checkbox_system_activate_proxy.setText(QCoreApplication.translate("PornFetch_Android", u"Activate Proxy", None))
        self.settings_groupbox_videos.setTitle(QCoreApplication.translate("PornFetch_Android", u"Videos", None))
        self.settings_radio_quality_worst.setText(QCoreApplication.translate("PornFetch_Android", u"Worst", None))
        self.settings_radio_quality_best.setText(QCoreApplication.translate("PornFetch_Android", u"Best", None))
        self.settings_button_directory_system_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_checkbox_videos_use_directory_system.setText(QCoreApplication.translate("PornFetch_Android", u"Use directory system", None))
        self.button_help_write_metadata_tags.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_label_output_path.setText(QCoreApplication.translate("PornFetch_Android", u"Output path:", None))
        self.radio_settings_post_processing_do_not_convert.setText(QCoreApplication.translate("PornFetch_Android", u"Do not convert", None))
        self.checkbox_settings_post_processing_write_metadata_tags.setText(QCoreApplication.translate("PornFetch_Android", u"Write metadata tags", None))
        self.settings_label_settings_videos_model.setText(QCoreApplication.translate("PornFetch_Android", u"Model videos (PornHub)", None))
        self.settings_button_output_path_select.setText(QCoreApplication.translate("PornFetch_Android", u"Open", None))
        self.settings_label_searching_limit.setText(QCoreApplication.translate("PornFetch_Android", u"Result Limit:", None))
        self.settings_button_result_limit_help.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.radio_settings_post_processing_use_custom_format.setText(QCoreApplication.translate("PornFetch_Android", u"Use custom format:", None))
        self.settings_label_quality.setText(QCoreApplication.translate("PornFetch_Android", u"Quality:", None))
        self.settings_radio_model_both.setText(QCoreApplication.translate("PornFetch_Android", u"Both", None))
        self.settings_radio_model_featured.setText(QCoreApplication.translate("PornFetch_Android", u"Featured videos", None))
        self.settings_lineedit_output_path.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter \"./\" for current directory", None))
        self.settings_button_help_model_videos.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_radio_quality_half.setText(QCoreApplication.translate("PornFetch_Android", u"Half", None))
        self.lineedit_settings_post_processing_use_custom_format.setText(QCoreApplication.translate("PornFetch_Android", u"mp4", None))
        self.settings_radio_model_uploads.setText(QCoreApplication.translate("PornFetch_Android", u"User uploads", None))
        self.settings_checkbox_videos_skip_existing_files.setText(QCoreApplication.translate("PornFetch_Android", u"Skip existing files", None))
        self.settings_button_help_skip_existing_files.setText(QCoreApplication.translate("PornFetch_Android", u"Help", None))
        self.settings_button_apply.setText(QCoreApplication.translate("PornFetch_Android", u"Apply  (needs restart)", None))
        self.settings_button_reset.setText(QCoreApplication.translate("PornFetch_Android", u"Reset Porn Fetch to default settings", None))
        self.main_textbrowser_supported_websites.setHtml(QCoreApplication.translate("PornFetch_Android", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Supported Websites:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-"
                        "indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Downloading:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- PornHub.com (supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- HQPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- Eporner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-r"
                        "ight:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- XNXX.com (supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- XVideos.com (supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- Missav.ws (and all of it's subsites, supports total progress)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- Xhamster.com<br /></span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif"
                        "'; font-size:9pt;\">All sites support *threaded* downloads and selectable quality!</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">* hqporner and eporner running in QThreads, but they don't fetch segments. The video is directly</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">downloaded, therefore threading in a segment isn't needed.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9"
                        "pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Model / Channel Downloads</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- PornHub.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- HQPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; fon"
                        "t-size:9pt;\">- EPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- XNXX.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- XVideos.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Searching:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans "
                        "Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- PornHub.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- HQPorner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- Xvideos.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">- Eporner.com</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'San"
                        "s Serif'; font-size:9pt;\">- XNXX.com</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">I am constantly working to support more websites.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">If you want a specific site to be supported, just ask:<br /><br />Discord: echteralsfake</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">GitHub.com/echteralsfake/Porn_Fetch/issues</span></p>\n"
"<p sty"
                        "le=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\"-qt-paragr"
                        "aph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p></body></html>", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("PornFetch_Android", u"GroupBox", None))
        self.main_button_switch_home.setText("")
        self.main_button_switch_account.setText("")
        self.main_button_switch_tools.setText("")
        self.main_button_switch_settings.setText("")
        self.main_button_switch_credits.setText("")
        self.main_button_view_progress_bars.setText("")
        self.main_button_switch_supported_websites.setText(QCoreApplication.translate("PornFetch_Android", u"Supported websites", None))
        self.main_label_progressbar_total.setText(QCoreApplication.translate("PornFetch_Android", u"Total:", None))
        self.main_label_progressbar_converting.setText(QCoreApplication.translate("PornFetch_Android", u"Converting:", None))
    # retranslateUi

