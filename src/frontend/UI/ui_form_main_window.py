# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
    QFormLayout, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QMainWindow, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(978, 655)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_12 = QGridLayout(self.centralwidget)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.main_horizontallayout_menu_buttons = QHBoxLayout()
        self.main_horizontallayout_menu_buttons.setSpacing(5)
        self.main_horizontallayout_menu_buttons.setObjectName(u"main_horizontallayout_menu_buttons")
        self.main_button_switch_home = QPushButton(self.centralwidget)
        self.main_button_switch_home.setObjectName(u"main_button_switch_home")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
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

        self.main_button_switch_account = QPushButton(self.centralwidget)
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

        self.main_button_switch_tools = QPushButton(self.centralwidget)
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

        self.main_button_switch_settings = QPushButton(self.centralwidget)
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

        self.main_button_switch_credits = QPushButton(self.centralwidget)
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

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_credits)

        self.main_button_view_progress_bars = QPushButton(self.centralwidget)
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

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_view_progress_bars)

        self.main_button_switch_supported_websites = QPushButton(self.centralwidget)
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

        self.main_horizontallayout_menu_buttons.addWidget(self.main_button_switch_supported_websites)


        self.gridLayout_12.addLayout(self.main_horizontallayout_menu_buttons, 0, 0, 1, 1)

        self.CentralStackedWidget = QStackedWidget(self.centralwidget)
        self.CentralStackedWidget.setObjectName(u"CentralStackedWidget")
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.page_main.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_9 = QGridLayout(self.page_main)
        self.gridLayout_9.setSpacing(0)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(0, 0, 0, 0)
        self.main_verticallayout = QVBoxLayout()
        self.main_verticallayout.setSpacing(0)
        self.main_verticallayout.setObjectName(u"main_verticallayout")
        self.main_verticallayout.setContentsMargins(-1, 0, -1, -1)
        self.main_stacked_widget_top = QStackedWidget(self.page_main)
        self.main_stacked_widget_top.setObjectName(u"main_stacked_widget_top")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.main_stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.main_stacked_widget_top.setSizePolicy(sizePolicy2)
        self.main_stacked_widget_top.setMinimumSize(QSize(0, 150))
        self.main_stacked_widget_top.setMaximumSize(QSize(16777215, 150))
        self.main_stacked_widget_top.setStyleSheet(u"")
        self.main_stacked_widget_top.setLineWidth(1)
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        sizePolicy.setHeightForWidth(self.page_download.sizePolicy().hasHeightForWidth())
        self.page_download.setSizePolicy(sizePolicy)
        self.page_download.setMinimumSize(QSize(0, 150))
        self.page_download.setMaximumSize(QSize(16777215, 180))
        self.gridLayout_5 = QGridLayout(self.page_download)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(2)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridlayout_downloading.setContentsMargins(-1, 0, -1, -1)
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
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.download_website_combobox.sizePolicy().hasHeightForWidth())
        self.download_website_combobox.setSizePolicy(sizePolicy3)
        self.download_website_combobox.setMinimumSize(QSize(0, 35))
        self.download_website_combobox.setMaximumSize(QSize(16777215, 35))
        font1 = QFont()
        font1.setBold(False)
        self.download_website_combobox.setFont(font1)
        self.download_website_combobox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.download_website_combobox, 6, 2, 1, 1)

        self.download_lineedit_url = QLineEdit(self.page_download)
        self.download_lineedit_url.setObjectName(u"download_lineedit_url")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.download_lineedit_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_url.setSizePolicy(sizePolicy4)
        self.download_lineedit_url.setMinimumSize(QSize(300, 30))
        font2 = QFont()
        font2.setBold(True)
        self.download_lineedit_url.setFont(font2)

        self.gridlayout_downloading.addWidget(self.download_lineedit_url, 2, 1, 1, 3)

        self.download_label_model_url = QLabel(self.page_download)
        self.download_label_model_url.setObjectName(u"download_label_model_url")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.download_label_model_url.sizePolicy().hasHeightForWidth())
        self.download_label_model_url.setSizePolicy(sizePolicy5)
        self.download_label_model_url.setMinimumSize(QSize(100, 30))
        self.download_label_model_url.setFont(font1)

        self.gridlayout_downloading.addWidget(self.download_label_model_url, 5, 0, 1, 1)

        self.download_lineedit_search_query = QLineEdit(self.page_download)
        self.download_lineedit_search_query.setObjectName(u"download_lineedit_search_query")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.download_lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.download_lineedit_search_query.setSizePolicy(sizePolicy6)
        self.download_lineedit_search_query.setMinimumSize(QSize(100, 35))
        self.download_lineedit_search_query.setFont(font2)

        self.gridlayout_downloading.addWidget(self.download_lineedit_search_query, 6, 1, 1, 1)

        self.download_button_model = QPushButton(self.page_download)
        self.download_button_model.setObjectName(u"download_button_model")
        sizePolicy5.setHeightForWidth(self.download_button_model.sizePolicy().hasHeightForWidth())
        self.download_button_model.setSizePolicy(sizePolicy5)
        self.download_button_model.setMinimumSize(QSize(60, 30))
        self.download_button_model.setFont(font1)
        self.download_button_model.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_model.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_model, 5, 4, 1, 1)

        self.download_label_search = QLabel(self.page_download)
        self.download_label_search.setObjectName(u"download_label_search")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.download_label_search.sizePolicy().hasHeightForWidth())
        self.download_label_search.setSizePolicy(sizePolicy7)
        self.download_label_search.setMinimumSize(QSize(0, 30))
        self.download_label_search.setFont(font1)

        self.gridlayout_downloading.addWidget(self.download_label_search, 6, 0, 1, 1)

        self.button_search = QPushButton(self.page_download)
        self.button_search.setObjectName(u"button_search")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy8)
        self.button_search.setMinimumSize(QSize(0, 35))
        self.button_search.setFont(font1)
        self.button_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search, 6, 4, 1, 1)

        self.download_lineedit_model_url = QLineEdit(self.page_download)
        self.download_lineedit_model_url.setObjectName(u"download_lineedit_model_url")
        sizePolicy6.setHeightForWidth(self.download_lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_model_url.setSizePolicy(sizePolicy6)
        self.download_lineedit_model_url.setMinimumSize(QSize(300, 35))
        self.download_lineedit_model_url.setFont(font2)

        self.gridlayout_downloading.addWidget(self.download_lineedit_model_url, 5, 1, 1, 3)

        self.download_label_playlist_url = QLabel(self.page_download)
        self.download_label_playlist_url.setObjectName(u"download_label_playlist_url")
        sizePolicy7.setHeightForWidth(self.download_label_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_label_playlist_url.setSizePolicy(sizePolicy7)
        self.download_label_playlist_url.setMinimumSize(QSize(0, 30))
        self.download_label_playlist_url.setFont(font1)

        self.gridlayout_downloading.addWidget(self.download_label_playlist_url, 4, 0, 1, 1)

        self.download_button_download = QPushButton(self.page_download)
        self.download_button_download.setObjectName(u"download_button_download")
        sizePolicy5.setHeightForWidth(self.download_button_download.sizePolicy().hasHeightForWidth())
        self.download_button_download.setSizePolicy(sizePolicy5)
        self.download_button_download.setMinimumSize(QSize(60, 30))
        font3 = QFont()
        font3.setBold(False)
        font3.setUnderline(False)
        self.download_button_download.setFont(font3)
        self.download_button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.download_button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.download_button_download, 2, 4, 1, 1)

        self.download_button_playlist_get_videos = QPushButton(self.page_download)
        self.download_button_playlist_get_videos.setObjectName(u"download_button_playlist_get_videos")
        sizePolicy5.setHeightForWidth(self.download_button_playlist_get_videos.sizePolicy().hasHeightForWidth())
        self.download_button_playlist_get_videos.setSizePolicy(sizePolicy5)
        self.download_button_playlist_get_videos.setMinimumSize(QSize(0, 30))
        self.download_button_playlist_get_videos.setFont(font1)
        self.download_button_playlist_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.download_button_playlist_get_videos, 4, 4, 1, 1)

        self.download_lineedit_playlist_url = QLineEdit(self.page_download)
        self.download_lineedit_playlist_url.setObjectName(u"download_lineedit_playlist_url")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.download_lineedit_playlist_url.sizePolicy().hasHeightForWidth())
        self.download_lineedit_playlist_url.setSizePolicy(sizePolicy9)
        self.download_lineedit_playlist_url.setMinimumSize(QSize(0, 30))
        self.download_lineedit_playlist_url.setFont(font2)

        self.gridlayout_downloading.addWidget(self.download_lineedit_playlist_url, 4, 1, 1, 3)

        self.download_label_url = QLabel(self.page_download)
        self.download_label_url.setObjectName(u"download_label_url")
        sizePolicy5.setHeightForWidth(self.download_label_url.sizePolicy().hasHeightForWidth())
        self.download_label_url.setSizePolicy(sizePolicy5)
        self.download_label_url.setMinimumSize(QSize(0, 30))
        self.download_label_url.setFont(font1)

        self.gridlayout_downloading.addWidget(self.download_label_url, 2, 0, 1, 1)


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
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.login_button_get_watched_videos = QPushButton(self.page_login)
        self.login_button_get_watched_videos.setObjectName(u"login_button_get_watched_videos")
        self.login_button_get_watched_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_watched_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_watched_videos.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.login_button_get_watched_videos)

        self.login_button_get_recommended_videos = QPushButton(self.page_login)
        self.login_button_get_recommended_videos.setObjectName(u"login_button_get_recommended_videos")
        self.login_button_get_recommended_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_recommended_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_recommended_videos.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.login_button_get_recommended_videos)

        self.login_button_get_liked_videos = QPushButton(self.page_login)
        self.login_button_get_liked_videos.setObjectName(u"login_button_get_liked_videos")
        self.login_button_get_liked_videos.setMinimumSize(QSize(0, 30))
        self.login_button_get_liked_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.login_button_get_liked_videos.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.login_button_get_liked_videos)


        self.login_gridlayout_login_box.addLayout(self.horizontalLayout_2, 3, 0, 1, 4)

        self.login_lineedit_password = QLineEdit(self.page_login)
        self.login_lineedit_password.setObjectName(u"login_lineedit_password")
        sizePolicy4.setHeightForWidth(self.login_lineedit_password.sizePolicy().hasHeightForWidth())
        self.login_lineedit_password.setSizePolicy(sizePolicy4)
        self.login_lineedit_password.setMinimumSize(QSize(0, 35))
        self.login_lineedit_password.setFont(font2)
        self.login_lineedit_password.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.login_lineedit_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_gridlayout_login_box.addWidget(self.login_lineedit_password, 1, 1, 1, 3)

        self.login_lineedit_username = QLineEdit(self.page_login)
        self.login_lineedit_username.setObjectName(u"login_lineedit_username")
        sizePolicy4.setHeightForWidth(self.login_lineedit_username.sizePolicy().hasHeightForWidth())
        self.login_lineedit_username.setSizePolicy(sizePolicy4)
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
        sizePolicy7.setHeightForWidth(self.page_tools.sizePolicy().hasHeightForWidth())
        self.page_tools.setSizePolicy(sizePolicy7)
        self.page_tools.setMinimumSize(QSize(100, 30))
        self.gridLayout_17 = QGridLayout(self.page_tools)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_5 = QScrollArea(self.page_tools)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 444, 182))
        self.gridLayout_8 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_15 = QGridLayout(self.groupBox)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tools_button_get_random_videos = QPushButton(self.groupBox)
        self.tools_button_get_random_videos.setObjectName(u"tools_button_get_random_videos")
        sizePolicy7.setHeightForWidth(self.tools_button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_random_videos.setSizePolicy(sizePolicy7)
        self.tools_button_get_random_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_random_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_get_random_videos, 3, 0, 1, 1)

        self.tools_button_hqporner_category_get_videos = QPushButton(self.groupBox)
        self.tools_button_hqporner_category_get_videos.setObjectName(u"tools_button_hqporner_category_get_videos")
        sizePolicy11 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(2)
        sizePolicy11.setHeightForWidth(self.tools_button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_hqporner_category_get_videos.setSizePolicy(sizePolicy11)
        self.tools_button_hqporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_hqporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.tools_button_hqporner_category_get_videos.setAcceptDrops(False)

        self.gridLayout_3.addWidget(self.tools_button_hqporner_category_get_videos, 1, 2, 1, 1)

        self.tools_label_videos_by_category = QLabel(self.groupBox)
        self.tools_label_videos_by_category.setObjectName(u"tools_label_videos_by_category")
        sizePolicy10.setHeightForWidth(self.tools_label_videos_by_category.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category.setSizePolicy(sizePolicy10)
        self.tools_label_videos_by_category.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_videos_by_category, 1, 0, 1, 1)

        self.tools_lineedit_hqporner_category = QLineEdit(self.groupBox)
        self.tools_lineedit_hqporner_category.setObjectName(u"tools_lineedit_hqporner_category")
        sizePolicy12 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(4)
        sizePolicy12.setHeightForWidth(self.tools_lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_hqporner_category.setSizePolicy(sizePolicy12)
        self.tools_lineedit_hqporner_category.setMinimumSize(QSize(100, 0))

        self.gridLayout_3.addWidget(self.tools_lineedit_hqporner_category, 1, 1, 1, 1)

        self.tools_label_get_top_porn = QLabel(self.groupBox)
        self.tools_label_get_top_porn.setObjectName(u"tools_label_get_top_porn")
        sizePolicy10.setHeightForWidth(self.tools_label_get_top_porn.sizePolicy().hasHeightForWidth())
        self.tools_label_get_top_porn.setSizePolicy(sizePolicy10)
        self.tools_label_get_top_porn.setMinimumSize(QSize(0, 0))

        self.gridLayout_3.addWidget(self.tools_label_get_top_porn, 0, 0, 1, 1)

        self.tools_button_get_brazzers_videos = QPushButton(self.groupBox)
        self.tools_button_get_brazzers_videos.setObjectName(u"tools_button_get_brazzers_videos")
        sizePolicy7.setHeightForWidth(self.tools_button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_get_brazzers_videos.setSizePolicy(sizePolicy7)
        self.tools_button_get_brazzers_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_get_brazzers_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_get_brazzers_videos, 3, 1, 1, 1)

        self.tools_combobox_hqporner_top_porn = QComboBox(self.groupBox)
        self.tools_combobox_hqporner_top_porn.addItem("")
        self.tools_combobox_hqporner_top_porn.addItem("")
        self.tools_combobox_hqporner_top_porn.addItem("")
        self.tools_combobox_hqporner_top_porn.setObjectName(u"tools_combobox_hqporner_top_porn")
        self.tools_combobox_hqporner_top_porn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_combobox_hqporner_top_porn, 0, 1, 1, 1)

        self.tools_button_top_porn_get_videos = QPushButton(self.groupBox)
        self.tools_button_top_porn_get_videos.setObjectName(u"tools_button_top_porn_get_videos")
        sizePolicy5.setHeightForWidth(self.tools_button_top_porn_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_top_porn_get_videos.setSizePolicy(sizePolicy5)
        self.tools_button_top_porn_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_top_porn_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_top_porn_get_videos, 0, 2, 1, 1)

        self.tools_button_list_categories = QPushButton(self.groupBox)
        self.tools_button_list_categories.setObjectName(u"tools_button_list_categories")
        sizePolicy5.setHeightForWidth(self.tools_button_list_categories.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories.setSizePolicy(sizePolicy5)
        self.tools_button_list_categories.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_3.addWidget(self.tools_button_list_categories, 3, 2, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
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
        sizePolicy13 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy13.setHorizontalStretch(0)
        sizePolicy13.setVerticalStretch(4)
        sizePolicy13.setHeightForWidth(self.tools_lineedit_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_lineedit_videos_by_category_eporner.setSizePolicy(sizePolicy13)
        self.tools_lineedit_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_lineedit_videos_by_category_eporner, 4, 1, 1, 2)

        self.tools_button_eporner_category_get_videos = QPushButton(self.groupBox_2)
        self.tools_button_eporner_category_get_videos.setObjectName(u"tools_button_eporner_category_get_videos")
        sizePolicy14 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy14.setHorizontalStretch(0)
        sizePolicy14.setVerticalStretch(2)
        sizePolicy14.setHeightForWidth(self.tools_button_eporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.tools_button_eporner_category_get_videos.setSizePolicy(sizePolicy14)
        self.tools_button_eporner_category_get_videos.setMinimumSize(QSize(0, 0))
        self.tools_button_eporner_category_get_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_eporner_category_get_videos, 4, 4, 1, 1)

        self.tools_button_list_categories_eporner = QPushButton(self.groupBox_2)
        self.tools_button_list_categories_eporner.setObjectName(u"tools_button_list_categories_eporner")
        sizePolicy5.setHeightForWidth(self.tools_button_list_categories_eporner.sizePolicy().hasHeightForWidth())
        self.tools_button_list_categories_eporner.setSizePolicy(sizePolicy5)
        self.tools_button_list_categories_eporner.setMinimumSize(QSize(0, 0))
        self.tools_button_list_categories_eporner.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.tools_gridlayout_tools.addWidget(self.tools_button_list_categories_eporner, 4, 3, 1, 1)

        self.tools_label_videos_by_category_eporner = QLabel(self.groupBox_2)
        self.tools_label_videos_by_category_eporner.setObjectName(u"tools_label_videos_by_category_eporner")
        sizePolicy7.setHeightForWidth(self.tools_label_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.tools_label_videos_by_category_eporner.setSizePolicy(sizePolicy7)
        self.tools_label_videos_by_category_eporner.setMinimumSize(QSize(100, 0))

        self.tools_gridlayout_tools.addWidget(self.tools_label_videos_by_category_eporner, 4, 0, 1, 1)


        self.gridLayout_16.addLayout(self.tools_gridlayout_tools, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_2)


        self.gridLayout_8.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_17.addWidget(self.scrollArea_5, 0, 0, 1, 1)

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
        self.scrollarea_progressbars = QScrollArea(self.page_progressbars)
        self.scrollarea_progressbars.setObjectName(u"scrollarea_progressbars")
        self.scrollarea_progressbars.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 308, 32))
        self.gridLayout_11 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(0, 0, 0, 0)
        self.progress_gridlayout_progressbar = QGridLayout()
        self.progress_gridlayout_progressbar.setObjectName(u"progress_gridlayout_progressbar")
        self.progress_gridlayout_progressbar.setHorizontalSpacing(6)
        self.progress_gridlayout_progressbar.setContentsMargins(-1, -1, -1, 0)
        self.progress_label_info = QLabel(self.scrollAreaWidgetContents_5)
        self.progress_label_info.setObjectName(u"progress_label_info")
        self.progress_label_info.setMinimumSize(QSize(0, 30))

        self.progress_gridlayout_progressbar.addWidget(self.progress_label_info, 1, 0, 1, 1)

        self.progress_lineedit_download_info = QLineEdit(self.scrollAreaWidgetContents_5)
        self.progress_lineedit_download_info.setObjectName(u"progress_lineedit_download_info")
        sizePolicy9.setHeightForWidth(self.progress_lineedit_download_info.sizePolicy().hasHeightForWidth())
        self.progress_lineedit_download_info.setSizePolicy(sizePolicy9)
        self.progress_lineedit_download_info.setReadOnly(True)

        self.progress_gridlayout_progressbar.addWidget(self.progress_lineedit_download_info, 1, 1, 1, 1)


        self.gridLayout_11.addLayout(self.progress_gridlayout_progressbar, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(308, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_11.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.scrollarea_progressbars.setWidget(self.scrollAreaWidgetContents_5)

        self.gridLayout_6.addWidget(self.scrollarea_progressbars, 1, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_progressbars)
        self.page_range = QWidget()
        self.page_range.setObjectName(u"page_range")
        self.gridLayout_10 = QGridLayout(self.page_range)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_25 = QGridLayout()
        self.gridLayout_25.setSpacing(0)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.button_range_apply_index = QPushButton(self.page_range)
        self.button_range_apply_index.setObjectName(u"button_range_apply_index")

        self.gridLayout_25.addWidget(self.button_range_apply_index, 8, 4, 1, 1)

        self.lineedit_range_start = QLineEdit(self.page_range)
        self.lineedit_range_start.setObjectName(u"lineedit_range_start")

        self.gridLayout_25.addWidget(self.lineedit_range_start, 4, 1, 1, 1)

        self.button_range_apply_author = QPushButton(self.page_range)
        self.button_range_apply_author.setObjectName(u"button_range_apply_author")

        self.gridLayout_25.addWidget(self.button_range_apply_author, 0, 2, 1, 3)

        self.spinbox_range_start = QSpinBox(self.page_range)
        self.spinbox_range_start.setObjectName(u"spinbox_range_start")

        self.gridLayout_25.addWidget(self.spinbox_range_start, 8, 1, 1, 1)

        self.lineedit_range_author = QLineEdit(self.page_range)
        self.lineedit_range_author.setObjectName(u"lineedit_range_author")

        self.gridLayout_25.addWidget(self.lineedit_range_author, 0, 1, 1, 1)

        self.spinbox_range_end = QSpinBox(self.page_range)
        self.spinbox_range_end.setObjectName(u"spinbox_range_end")

        self.gridLayout_25.addWidget(self.spinbox_range_end, 8, 3, 1, 1)

        self.label_range_start = QLabel(self.page_range)
        self.label_range_start.setObjectName(u"label_range_start")

        self.gridLayout_25.addWidget(self.label_range_start, 8, 0, 1, 1)

        self.button_range_apply_time = QPushButton(self.page_range)
        self.button_range_apply_time.setObjectName(u"button_range_apply_time")

        self.gridLayout_25.addWidget(self.button_range_apply_time, 4, 4, 1, 1)

        self.lineedit_range_end = QLineEdit(self.page_range)
        self.lineedit_range_end.setObjectName(u"lineedit_range_end")

        self.gridLayout_25.addWidget(self.lineedit_range_end, 4, 3, 1, 1)

        self.label_range_by_author = QLabel(self.page_range)
        self.label_range_by_author.setObjectName(u"label_range_by_author")

        self.gridLayout_25.addWidget(self.label_range_by_author, 0, 0, 1, 1)

        self.label_range_end = QLabel(self.page_range)
        self.label_range_end.setObjectName(u"label_range_end")

        self.gridLayout_25.addWidget(self.label_range_end, 8, 2, 1, 1)

        self.label_apply_by_time = QLabel(self.page_range)
        self.label_apply_by_time.setObjectName(u"label_apply_by_time")

        self.gridLayout_25.addWidget(self.label_apply_by_time, 3, 0, 1, 4)

        self.label_range_time_start = QLabel(self.page_range)
        self.label_range_time_start.setObjectName(u"label_range_time_start")

        self.gridLayout_25.addWidget(self.label_range_time_start, 4, 0, 1, 1)

        self.label_range_time_end = QLabel(self.page_range)
        self.label_range_time_end.setObjectName(u"label_range_time_end")

        self.gridLayout_25.addWidget(self.label_range_time_end, 4, 2, 1, 1)

        self.button_range_select_all = QPushButton(self.page_range)
        self.button_range_select_all.setObjectName(u"button_range_select_all")

        self.gridLayout_25.addWidget(self.button_range_select_all, 9, 0, 1, 2)

        self.button_range_unselect_all = QPushButton(self.page_range)
        self.button_range_unselect_all.setObjectName(u"button_range_unselect_all")

        self.gridLayout_25.addWidget(self.button_range_unselect_all, 9, 3, 1, 2)

        self.label_apply_by_index = QLabel(self.page_range)
        self.label_apply_by_index.setObjectName(u"label_apply_by_index")

        self.gridLayout_25.addWidget(self.label_apply_by_index, 5, 0, 1, 4)


        self.gridLayout_10.addLayout(self.gridLayout_25, 0, 0, 1, 1)

        self.main_stacked_widget_top.addWidget(self.page_range)

        self.main_verticallayout.addWidget(self.main_stacked_widget_top)

        self.main_scrollarea_treewidget = QScrollArea(self.page_main)
        self.main_scrollarea_treewidget.setObjectName(u"main_scrollarea_treewidget")
        self.main_scrollarea_treewidget.setWidgetResizable(True)
        self.main_scrollarea_treewidget_content = QWidget()
        self.main_scrollarea_treewidget_content.setObjectName(u"main_scrollarea_treewidget_content")
        self.main_scrollarea_treewidget_content.setGeometry(QRect(0, 0, 639, 384))
        sizePolicy15 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy15.setHorizontalStretch(0)
        sizePolicy15.setVerticalStretch(0)
        sizePolicy15.setHeightForWidth(self.main_scrollarea_treewidget_content.sizePolicy().hasHeightForWidth())
        self.main_scrollarea_treewidget_content.setSizePolicy(sizePolicy15)
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
        self.main_button_tree_download.setFont(font1)
        self.main_button_tree_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.main_button_tree_download.setStyleSheet(u"")

        self.gridLayout.addWidget(self.main_button_tree_download, 1, 0, 1, 3)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.main_button_tree_keyboard_shortcuts = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_keyboard_shortcuts.setObjectName(u"main_button_tree_keyboard_shortcuts")
        sizePolicy3.setHeightForWidth(self.main_button_tree_keyboard_shortcuts.sizePolicy().hasHeightForWidth())
        self.main_button_tree_keyboard_shortcuts.setSizePolicy(sizePolicy3)
        self.main_button_tree_keyboard_shortcuts.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_button_tree_keyboard_shortcuts, 3, 2, 1, 1)

        self.main_checkbox_direct_download = QCheckBox(self.main_scrollarea_treewidget_content)
        self.main_checkbox_direct_download.setObjectName(u"main_checkbox_direct_download")
        sizePolicy3.setHeightForWidth(self.main_checkbox_direct_download.sizePolicy().hasHeightForWidth())
        self.main_checkbox_direct_download.setSizePolicy(sizePolicy3)
        self.main_checkbox_direct_download.setFont(font1)
        self.main_checkbox_direct_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_checkbox_direct_download, 0, 0, 1, 2)

        self.main_button_tree_stop = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_stop.setObjectName(u"main_button_tree_stop")
        sizePolicy3.setHeightForWidth(self.main_button_tree_stop.sizePolicy().hasHeightForWidth())
        self.main_button_tree_stop.setSizePolicy(sizePolicy3)
        self.main_button_tree_stop.setMinimumSize(QSize(0, 30))
        self.main_button_tree_stop.setFont(font1)
        self.main_button_tree_stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_button_tree_stop, 4, 0, 1, 3)

        self.main_checkbox_tree_do_not_clear_videos = QCheckBox(self.main_scrollarea_treewidget_content)
        self.main_checkbox_tree_do_not_clear_videos.setObjectName(u"main_checkbox_tree_do_not_clear_videos")
        sizePolicy3.setHeightForWidth(self.main_checkbox_tree_do_not_clear_videos.sizePolicy().hasHeightForWidth())
        self.main_checkbox_tree_do_not_clear_videos.setSizePolicy(sizePolicy3)
        self.main_checkbox_tree_do_not_clear_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_checkbox_tree_do_not_clear_videos, 0, 2, 1, 1)

        self.main_button_tree_automated_selection = QPushButton(self.main_scrollarea_treewidget_content)
        self.main_button_tree_automated_selection.setObjectName(u"main_button_tree_automated_selection")
        sizePolicy3.setHeightForWidth(self.main_button_tree_automated_selection.sizePolicy().hasHeightForWidth())
        self.main_button_tree_automated_selection.setSizePolicy(sizePolicy3)
        self.main_button_tree_automated_selection.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridLayout_13.addWidget(self.main_button_tree_automated_selection, 3, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_tooltip_index_videos = QLabel(self.main_scrollarea_treewidget_content)
        self.label_tooltip_index_videos.setObjectName(u"label_tooltip_index_videos")
        sizePolicy16 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy16.setHorizontalStretch(0)
        sizePolicy16.setVerticalStretch(0)
        sizePolicy16.setHeightForWidth(self.label_tooltip_index_videos.sizePolicy().hasHeightForWidth())
        self.label_tooltip_index_videos.setSizePolicy(sizePolicy16)

        self.horizontalLayout_3.addWidget(self.label_tooltip_index_videos)

        self.label_index_start = QLabel(self.main_scrollarea_treewidget_content)
        self.label_index_start.setObjectName(u"label_index_start")
        sizePolicy16.setHeightForWidth(self.label_index_start.sizePolicy().hasHeightForWidth())
        self.label_index_start.setSizePolicy(sizePolicy16)

        self.horizontalLayout_3.addWidget(self.label_index_start)

        self.spinbox_index_fetching_start = QSpinBox(self.main_scrollarea_treewidget_content)
        self.spinbox_index_fetching_start.setObjectName(u"spinbox_index_fetching_start")

        self.horizontalLayout_3.addWidget(self.spinbox_index_fetching_start)

        self.label_index_end = QLabel(self.main_scrollarea_treewidget_content)
        self.label_index_end.setObjectName(u"label_index_end")
        sizePolicy16.setHeightForWidth(self.label_index_end.sizePolicy().hasHeightForWidth())
        self.label_index_end.setSizePolicy(sizePolicy16)

        self.horizontalLayout_3.addWidget(self.label_index_end)

        self.spinbox_index_fetching_end = QSpinBox(self.main_scrollarea_treewidget_content)
        self.spinbox_index_fetching_end.setObjectName(u"spinbox_index_fetching_end")

        self.horizontalLayout_3.addWidget(self.spinbox_index_fetching_end)


        self.gridLayout_13.addLayout(self.horizontalLayout_3, 1, 1, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout_13)

        self.graphicsView = QGraphicsView(self.main_scrollarea_treewidget_content)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy17 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy17.setHorizontalStretch(0)
        sizePolicy17.setVerticalStretch(0)
        sizePolicy17.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy17)

        self.verticalLayout_3.addWidget(self.graphicsView)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 2, 1, 1)

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
        self.treeWidget.setMinimumSize(QSize(300, 10))

        self.gridLayout.addWidget(self.treeWidget, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.main_scrollarea_treewidget.setWidget(self.main_scrollarea_treewidget_content)

        self.main_verticallayout.addWidget(self.main_scrollarea_treewidget)


        self.gridLayout_9.addLayout(self.main_verticallayout, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_main)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        sizePolicy3.setHeightForWidth(self.page_settings.sizePolicy().hasHeightForWidth())
        self.page_settings.setSizePolicy(sizePolicy3)
        self.gridLayout_7 = QGridLayout(self.page_settings)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.settings_scrollarea = QScrollArea(self.page_settings)
        self.settings_scrollarea.setObjectName(u"settings_scrollarea")
        sizePolicy3.setHeightForWidth(self.settings_scrollarea.sizePolicy().hasHeightForWidth())
        self.settings_scrollarea.setSizePolicy(sizePolicy3)
        self.settings_scrollarea.setWidgetResizable(True)
        self.settings_scrollarea_widget_contents = QWidget()
        self.settings_scrollarea_widget_contents.setObjectName(u"settings_scrollarea_widget_contents")
        self.settings_scrollarea_widget_contents.setGeometry(QRect(0, 0, 958, 532))
        self.gridLayout_19 = QGridLayout(self.settings_scrollarea_widget_contents)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.settings_button_switch_video = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_video.setObjectName(u"settings_button_switch_video")
        self.settings_button_switch_video.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.settings_button_switch_video)

        self.settings_button_switch_performance = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_performance.setObjectName(u"settings_button_switch_performance")
        self.settings_button_switch_performance.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.settings_button_switch_performance)

        self.settings_button_switch_system = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_system.setObjectName(u"settings_button_switch_system")
        self.settings_button_switch_system.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.settings_button_switch_system)

        self.settings_button_switch_ui = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_switch_ui.setObjectName(u"settings_button_switch_ui")
        self.settings_button_switch_ui.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.settings_button_switch_ui)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.settings_stacked_widget_main = QStackedWidget(self.settings_scrollarea_widget_contents)
        self.settings_stacked_widget_main.setObjectName(u"settings_stacked_widget_main")
        sizePolicy3.setHeightForWidth(self.settings_stacked_widget_main.sizePolicy().hasHeightForWidth())
        self.settings_stacked_widget_main.setSizePolicy(sizePolicy3)
        self.page_video = QWidget()
        self.page_video.setObjectName(u"page_video")
        sizePolicy19 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy19.setHorizontalStretch(0)
        sizePolicy19.setVerticalStretch(0)
        sizePolicy19.setHeightForWidth(self.page_video.sizePolicy().hasHeightForWidth())
        self.page_video.setSizePolicy(sizePolicy19)
        self.gridLayout_14 = QGridLayout(self.page_video)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.settings_gridlayout_video = QGridLayout()
        self.settings_gridlayout_video.setObjectName(u"settings_gridlayout_video")
        self.settings_label_videos_result_limit = QLabel(self.page_video)
        self.settings_label_videos_result_limit.setObjectName(u"settings_label_videos_result_limit")

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_result_limit, 2, 1, 1, 1)

        self.settings_checkbox_videos_use_directory_system = QCheckBox(self.page_video)
        self.settings_checkbox_videos_use_directory_system.setObjectName(u"settings_checkbox_videos_use_directory_system")
        self.settings_checkbox_videos_use_directory_system.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_use_directory_system, 5, 5, 1, 1)

        self.settings_checkbox_videos_track_downloaded_videos = QCheckBox(self.page_video)
        self.settings_checkbox_videos_track_downloaded_videos.setObjectName(u"settings_checkbox_videos_track_downloaded_videos")

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_track_downloaded_videos, 5, 1, 1, 1)

        self.settings_label_videos_quality = QLabel(self.page_video)
        self.settings_label_videos_quality.setObjectName(u"settings_label_videos_quality")
        sizePolicy10.setHeightForWidth(self.settings_label_videos_quality.sizePolicy().hasHeightForWidth())
        self.settings_label_videos_quality.setSizePolicy(sizePolicy10)

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_quality, 0, 1, 1, 1)

        self.label_tooltip_model_videos = QLabel(self.page_video)
        self.label_tooltip_model_videos.setObjectName(u"label_tooltip_model_videos")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_model_videos, 1, 0, 1, 1)

        self.settings_checkbox_videos_skip_existing_files = QCheckBox(self.page_video)
        self.settings_checkbox_videos_skip_existing_files.setObjectName(u"settings_checkbox_videos_skip_existing_files")
        self.settings_checkbox_videos_skip_existing_files.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_skip_existing_files, 4, 5, 1, 1)

        self.settings_label_videos_output_path = QLabel(self.page_video)
        self.settings_label_videos_output_path.setObjectName(u"settings_label_videos_output_path")

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_output_path, 3, 1, 1, 1)

        self.settings_checkbox_videos_write_metadata = QCheckBox(self.page_video)
        self.settings_checkbox_videos_write_metadata.setObjectName(u"settings_checkbox_videos_write_metadata")
        self.settings_checkbox_videos_write_metadata.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_write_metadata, 4, 3, 1, 1)

        self.label_tooltip_quality = QLabel(self.page_video)
        self.label_tooltip_quality.setObjectName(u"label_tooltip_quality")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_quality, 0, 0, 1, 1)

        self.settings_video_combobox_model_videos = QComboBox(self.page_video)
        self.settings_video_combobox_model_videos.addItem("")
        self.settings_video_combobox_model_videos.addItem("")
        self.settings_video_combobox_model_videos.addItem("")
        self.settings_video_combobox_model_videos.setObjectName(u"settings_video_combobox_model_videos")
        self.settings_video_combobox_model_videos.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_video_combobox_model_videos, 1, 2, 1, 4)

        self.label_tooltip_result_limit = QLabel(self.page_video)
        self.label_tooltip_result_limit.setObjectName(u"label_tooltip_result_limit")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_result_limit, 2, 0, 1, 1)

        self.label_tooltip_track_videos = QLabel(self.page_video)
        self.label_tooltip_track_videos.setObjectName(u"label_tooltip_track_videos")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_track_videos, 5, 0, 1, 1)

        self.settings_button_videos_open_output_path = QPushButton(self.page_video)
        self.settings_button_videos_open_output_path.setObjectName(u"settings_button_videos_open_output_path")
        self.settings_button_videos_open_output_path.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_button_videos_open_output_path, 3, 5, 1, 1)

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
        self.settings_video_combobox_quality.setObjectName(u"settings_video_combobox_quality")
        self.settings_video_combobox_quality.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_video.addWidget(self.settings_video_combobox_quality, 0, 2, 1, 4)

        self.settings_lineedit_videos_database_path = QLineEdit(self.page_video)
        self.settings_lineedit_videos_database_path.setObjectName(u"settings_lineedit_videos_database_path")

        self.settings_gridlayout_video.addWidget(self.settings_lineedit_videos_database_path, 5, 3, 1, 1)

        self.settings_spinbox_videos_result_limit = QSpinBox(self.page_video)
        self.settings_spinbox_videos_result_limit.setObjectName(u"settings_spinbox_videos_result_limit")
        self.settings_spinbox_videos_result_limit.setMinimum(1)
        self.settings_spinbox_videos_result_limit.setMaximum(5000)

        self.settings_gridlayout_video.addWidget(self.settings_spinbox_videos_result_limit, 2, 2, 1, 4)

        self.settings_checkbox_videos_use_video_id_as_filename = QCheckBox(self.page_video)
        self.settings_checkbox_videos_use_video_id_as_filename.setObjectName(u"settings_checkbox_videos_use_video_id_as_filename")

        self.settings_gridlayout_video.addWidget(self.settings_checkbox_videos_use_video_id_as_filename, 4, 1, 1, 1)

        self.label_tooltip_write_metadata = QLabel(self.page_video)
        self.label_tooltip_write_metadata.setObjectName(u"label_tooltip_write_metadata")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_write_metadata, 4, 2, 1, 1)

        self.settings_label_videos_model_vdeos_type = QLabel(self.page_video)
        self.settings_label_videos_model_vdeos_type.setObjectName(u"settings_label_videos_model_vdeos_type")

        self.settings_gridlayout_video.addWidget(self.settings_label_videos_model_vdeos_type, 1, 1, 1, 1)

        self.settings_lineedit_videos_output_path = QLineEdit(self.page_video)
        self.settings_lineedit_videos_output_path.setObjectName(u"settings_lineedit_videos_output_path")
        sizePolicy5.setHeightForWidth(self.settings_lineedit_videos_output_path.sizePolicy().hasHeightForWidth())
        self.settings_lineedit_videos_output_path.setSizePolicy(sizePolicy5)

        self.settings_gridlayout_video.addWidget(self.settings_lineedit_videos_output_path, 3, 2, 1, 2)

        self.label_tooltip_use_directory_system = QLabel(self.page_video)
        self.label_tooltip_use_directory_system.setObjectName(u"label_tooltip_use_directory_system")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_use_directory_system, 5, 4, 1, 1)

        self.label_tooltip_skip_existing_files = QLabel(self.page_video)
        self.label_tooltip_skip_existing_files.setObjectName(u"label_tooltip_skip_existing_files")

        self.settings_gridlayout_video.addWidget(self.label_tooltip_skip_existing_files, 4, 4, 1, 1)


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

        self.settings_label_performance_download_mode = QLabel(self.page_performance)
        self.settings_label_performance_download_mode.setObjectName(u"settings_label_performance_download_mode")
        sizePolicy10.setHeightForWidth(self.settings_label_performance_download_mode.sizePolicy().hasHeightForWidth())
        self.settings_label_performance_download_mode.setSizePolicy(sizePolicy10)

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_download_mode, 0, 1, 1, 1)

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

        self.settings_spinbox_performance_download_workers = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_download_workers.setObjectName(u"settings_spinbox_performance_download_workers")
        self.settings_spinbox_performance_download_workers.setMinimum(1)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_download_workers, 8, 5, 1, 1)

        self.settings_spinbox_performance_videos_concurrency = QSpinBox(self.page_performance)
        self.settings_spinbox_performance_videos_concurrency.setObjectName(u"settings_spinbox_performance_videos_concurrency")
        self.settings_spinbox_performance_videos_concurrency.setMinimum(1)

        self.settings_gridlayout_performance.addWidget(self.settings_spinbox_performance_videos_concurrency, 7, 5, 1, 1)

        self.label_tooltip_download_mode = QLabel(self.page_performance)
        self.label_tooltip_download_mode.setObjectName(u"label_tooltip_download_mode")
        sizePolicy16.setHeightForWidth(self.label_tooltip_download_mode.sizePolicy().hasHeightForWidth())
        self.label_tooltip_download_mode.setSizePolicy(sizePolicy16)

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

        self.settings_performance_combobox_download_mode = QComboBox(self.page_performance)
        self.settings_performance_combobox_download_mode.addItem("")
        self.settings_performance_combobox_download_mode.addItem("")
        self.settings_performance_combobox_download_mode.addItem("")
        self.settings_performance_combobox_download_mode.setObjectName(u"settings_performance_combobox_download_mode")
        self.settings_performance_combobox_download_mode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_performance.addWidget(self.settings_performance_combobox_download_mode, 0, 2, 1, 1)

        self.settings_label_performance_network_delay = QLabel(self.page_performance)
        self.settings_label_performance_network_delay.setObjectName(u"settings_label_performance_network_delay")

        self.settings_gridlayout_performance.addWidget(self.settings_label_performance_network_delay, 0, 4, 1, 1)

        self.label_settings_performance_download_workers = QLabel(self.page_performance)
        self.label_settings_performance_download_workers.setObjectName(u"label_settings_performance_download_workers")

        self.settings_gridlayout_performance.addWidget(self.label_settings_performance_download_workers, 8, 4, 1, 1)

        self.label_tooltip_network_delay = QLabel(self.page_performance)
        self.label_tooltip_network_delay.setObjectName(u"label_tooltip_network_delay")
        sizePolicy16.setHeightForWidth(self.label_tooltip_network_delay.sizePolicy().hasHeightForWidth())
        self.label_tooltip_network_delay.setSizePolicy(sizePolicy16)

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
        self.settings_checkbox_system_activate_proxy = QCheckBox(self.page_system)
        self.settings_checkbox_system_activate_proxy.setObjectName(u"settings_checkbox_system_activate_proxy")
        self.settings_checkbox_system_activate_proxy.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_activate_proxy, 2, 2, 1, 1)

        self.settings_checkbox_system_internet_checks = QCheckBox(self.page_system)
        self.settings_checkbox_system_internet_checks.setObjectName(u"settings_checkbox_system_internet_checks")
        self.settings_checkbox_system_internet_checks.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_internet_checks, 1, 2, 1, 1)

        self.settings_checkbox_system_enable_network_logging = QCheckBox(self.page_system)
        self.settings_checkbox_system_enable_network_logging.setObjectName(u"settings_checkbox_system_enable_network_logging")
        self.settings_checkbox_system_enable_network_logging.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_enable_network_logging, 4, 1, 1, 2)

        self.label_tooltip_network_logging = QLabel(self.page_system)
        self.label_tooltip_network_logging.setObjectName(u"label_tooltip_network_logging")

        self.settings_gridlayout_system.addWidget(self.label_tooltip_network_logging, 4, 0, 1, 1)

        self.settings_checkbox_system_supress_errors = QCheckBox(self.page_system)
        self.settings_checkbox_system_supress_errors.setObjectName(u"settings_checkbox_system_supress_errors")
        self.settings_checkbox_system_supress_errors.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_supress_errors, 3, 1, 1, 1)

        self.label_tooltip_update_checks = QLabel(self.page_system)
        self.label_tooltip_update_checks.setObjectName(u"label_tooltip_update_checks")
        sizePolicy16.setHeightForWidth(self.label_tooltip_update_checks.sizePolicy().hasHeightForWidth())
        self.label_tooltip_update_checks.setSizePolicy(sizePolicy16)

        self.settings_gridlayout_system.addWidget(self.label_tooltip_update_checks, 1, 0, 1, 1)

        self.label_tooltip_anonymous_mode = QLabel(self.page_system)
        self.label_tooltip_anonymous_mode.setObjectName(u"label_tooltip_anonymous_mode")

        self.settings_gridlayout_system.addWidget(self.label_tooltip_anonymous_mode, 2, 0, 1, 1)

        self.settings_checkbox_system_enable_anonymous_mode = QCheckBox(self.page_system)
        self.settings_checkbox_system_enable_anonymous_mode.setObjectName(u"settings_checkbox_system_enable_anonymous_mode")
        self.settings_checkbox_system_enable_anonymous_mode.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_enable_anonymous_mode, 2, 1, 1, 1)

        self.settings_checkbox_system_update_checks = QCheckBox(self.page_system)
        self.settings_checkbox_system_update_checks.setObjectName(u"settings_checkbox_system_update_checks")
        self.settings_checkbox_system_update_checks.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_update_checks, 1, 1, 1, 1)

        self.label_tooltip_supress_errors = QLabel(self.page_system)
        self.label_tooltip_supress_errors.setObjectName(u"label_tooltip_supress_errors")

        self.settings_gridlayout_system.addWidget(self.label_tooltip_supress_errors, 3, 0, 1, 1)

        self.settings_checkbox_system_proxy_kill_switch = QCheckBox(self.page_system)
        self.settings_checkbox_system_proxy_kill_switch.setObjectName(u"settings_checkbox_system_proxy_kill_switch")
        self.settings_checkbox_system_proxy_kill_switch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_system.addWidget(self.settings_checkbox_system_proxy_kill_switch, 3, 2, 1, 1)

        self.settings_button_system_install_pornfetch = QPushButton(self.page_system)
        self.settings_button_system_install_pornfetch.setObjectName(u"settings_button_system_install_pornfetch")

        self.settings_gridlayout_system.addWidget(self.settings_button_system_install_pornfetch, 0, 0, 1, 2)

        self.settings_lineedit_system_custom_app_name = QLineEdit(self.page_system)
        self.settings_lineedit_system_custom_app_name.setObjectName(u"settings_lineedit_system_custom_app_name")
        sizePolicy7.setHeightForWidth(self.settings_lineedit_system_custom_app_name.sizePolicy().hasHeightForWidth())
        self.settings_lineedit_system_custom_app_name.setSizePolicy(sizePolicy7)

        self.settings_gridlayout_system.addWidget(self.settings_lineedit_system_custom_app_name, 0, 2, 1, 1)


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
        self.settings_label_ui_theme = QLabel(self.page_ui)
        self.settings_label_ui_theme.setObjectName(u"settings_label_ui_theme")

        self.settings_gridlayout_ui.addWidget(self.settings_label_ui_theme, 2, 0, 1, 1)

        self.settings_label_ui_language = QLabel(self.page_ui)
        self.settings_label_ui_language.setObjectName(u"settings_label_ui_language")
        sizePolicy10.setHeightForWidth(self.settings_label_ui_language.sizePolicy().hasHeightForWidth())
        self.settings_label_ui_language.setSizePolicy(sizePolicy10)

        self.settings_gridlayout_ui.addWidget(self.settings_label_ui_language, 0, 0, 1, 1)

        self.settings_label_ui_font_size = QLabel(self.page_ui)
        self.settings_label_ui_font_size.setObjectName(u"settings_label_ui_font_size")

        self.settings_gridlayout_ui.addWidget(self.settings_label_ui_font_size, 1, 0, 1, 1)

        self.settings_combobox_ui_theme = QComboBox(self.page_ui)
        self.settings_combobox_ui_theme.addItem("")
        self.settings_combobox_ui_theme.addItem("")
        self.settings_combobox_ui_theme.addItem("")
        self.settings_combobox_ui_theme.setObjectName(u"settings_combobox_ui_theme")

        self.settings_gridlayout_ui.addWidget(self.settings_combobox_ui_theme, 2, 1, 1, 1)

        self.settings_spinbox_ui_font_size = QSpinBox(self.page_ui)
        self.settings_spinbox_ui_font_size.setObjectName(u"settings_spinbox_ui_font_size")

        self.settings_gridlayout_ui.addWidget(self.settings_spinbox_ui_font_size, 1, 1, 1, 1)

        self.settings_ui_combobox_language = QComboBox(self.page_ui)
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.addItem("")
        self.settings_ui_combobox_language.setObjectName(u"settings_ui_combobox_language")
        self.settings_ui_combobox_language.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.settings_gridlayout_ui.addWidget(self.settings_ui_combobox_language, 0, 1, 1, 1)


        self.gridLayout_34.addLayout(self.settings_gridlayout_ui, 0, 0, 1, 1)

        self.settings_stacked_widget_main.addWidget(self.page_ui)

        self.verticalLayout_4.addWidget(self.settings_stacked_widget_main)

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


        self.verticalLayout_4.addLayout(self.settings_horizontallayout_apply)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.settings_button_buy_license = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_buy_license.setObjectName(u"settings_button_buy_license")
        self.settings_button_buy_license.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.settings_button_buy_license)

        self.settings_button_import_license = QPushButton(self.settings_scrollarea_widget_contents)
        self.settings_button_import_license.setObjectName(u"settings_button_import_license")
        self.settings_button_import_license.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.settings_button_import_license)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.settings_vertical_spacer_main = QSpacerItem(108, 98, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.settings_vertical_spacer_main)


        self.gridLayout_19.addLayout(self.verticalLayout_4, 1, 0, 1, 1)

        self.settings_scrollarea.setWidget(self.settings_scrollarea_widget_contents)

        self.gridLayout_7.addWidget(self.settings_scrollarea, 0, 1, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_settings)
        self.page_credits = QWidget()
        self.page_credits.setObjectName(u"page_credits")
        self.gridLayout_22 = QGridLayout(self.page_credits)
        self.gridLayout_22.setSpacing(0)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.page_credits)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 202, 104))
        self.gridLayout_21 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_21.setSpacing(0)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.button_credits_send_feedback = QPushButton(self.scrollAreaWidgetContents_3)
        self.button_credits_send_feedback.setObjectName(u"button_credits_send_feedback")

        self.verticalLayout_5.addWidget(self.button_credits_send_feedback)

        self.main_textbrowser_credits = QTextBrowser(self.scrollAreaWidgetContents_3)
        self.main_textbrowser_credits.setObjectName(u"main_textbrowser_credits")

        self.verticalLayout_5.addWidget(self.main_textbrowser_credits)


        self.gridLayout_21.addLayout(self.verticalLayout_5, 0, 1, 1, 1)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout_22.addWidget(self.scrollArea_2, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_credits)
        self.page_license = QWidget()
        self.page_license.setObjectName(u"page_license")
        self.gridLayout_24 = QGridLayout(self.page_license)
        self.gridLayout_24.setSpacing(0)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(0, 0, 0, 0)
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
        font4 = QFont()
        font4.setFamilies([u"JetBrainsMono Nerd Font Propo"])
        font4.setPointSize(11)
        font4.setKerning(True)
        self.textBrowser.setFont(font4)
        self.textBrowser.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)
        self.textBrowser.setOpenExternalLinks(True)

        self.gridLayout_23.addWidget(self.textBrowser, 0, 0, 1, 2)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_4)

        self.gridLayout_24.addWidget(self.scrollArea_3, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_license)
        self.page_keyboard_shortcuts = QWidget()
        self.page_keyboard_shortcuts.setObjectName(u"page_keyboard_shortcuts")
        self.gridLayout_55 = QGridLayout(self.page_keyboard_shortcuts)
        self.gridLayout_55.setSpacing(0)
        self.gridLayout_55.setObjectName(u"gridLayout_55")
        self.gridLayout_55.setContentsMargins(0, 0, 0, 0)
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
        self.page_install_dialog = QWidget()
        self.page_install_dialog.setObjectName(u"page_install_dialog")
        self.gridLayout_57 = QGridLayout(self.page_install_dialog)
        self.gridLayout_57.setSpacing(0)
        self.gridLayout_57.setObjectName(u"gridLayout_57")
        self.gridLayout_57.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_10 = QScrollArea(self.page_install_dialog)
        self.scrollArea_10.setObjectName(u"scrollArea_10")
        self.scrollArea_10.setWidgetResizable(True)
        self.scrollAreaWidgetContents_12 = QWidget()
        self.scrollAreaWidgetContents_12.setObjectName(u"scrollAreaWidgetContents_12")
        self.scrollAreaWidgetContents_12.setGeometry(QRect(0, 0, 172, 140))
        self.gridLayout_56 = QGridLayout(self.scrollAreaWidgetContents_12)
        self.gridLayout_56.setSpacing(0)
        self.gridLayout_56.setObjectName(u"gridLayout_56")
        self.gridLayout_56.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textbrowser_install_dialog = QTextBrowser(self.scrollAreaWidgetContents_12)
        self.textbrowser_install_dialog.setObjectName(u"textbrowser_install_dialog")

        self.verticalLayout.addWidget(self.textbrowser_install_dialog)

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
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
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
        self.page_disclaimer = QWidget()
        self.page_disclaimer.setObjectName(u"page_disclaimer")
        self.gridLayout_62 = QGridLayout(self.page_disclaimer)
        self.gridLayout_62.setSpacing(0)
        self.gridLayout_62.setObjectName(u"gridLayout_62")
        self.gridLayout_62.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_12 = QScrollArea(self.page_disclaimer)
        self.scrollArea_12.setObjectName(u"scrollArea_12")
        self.scrollArea_12.setWidgetResizable(True)
        self.scrollAreaWidgetContents_14 = QWidget()
        self.scrollAreaWidgetContents_14.setObjectName(u"scrollAreaWidgetContents_14")
        self.scrollAreaWidgetContents_14.setGeometry(QRect(0, 0, 98, 120))
        self.gridLayout_61 = QGridLayout(self.scrollAreaWidgetContents_14)
        self.gridLayout_61.setObjectName(u"gridLayout_61")
        self.textbrowser_disclaimer = QTextBrowser(self.scrollAreaWidgetContents_14)
        self.textbrowser_disclaimer.setObjectName(u"textbrowser_disclaimer")

        self.gridLayout_61.addWidget(self.textbrowser_disclaimer, 0, 0, 1, 1)

        self.button_disclaimer_accept = QPushButton(self.scrollAreaWidgetContents_14)
        self.button_disclaimer_accept.setObjectName(u"button_disclaimer_accept")

        self.gridLayout_61.addWidget(self.button_disclaimer_accept, 1, 0, 1, 1)

        self.scrollArea_12.setWidget(self.scrollAreaWidgetContents_14)

        self.gridLayout_62.addWidget(self.scrollArea_12, 0, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_disclaimer)
        self.page_one_time_setup = QWidget()
        self.page_one_time_setup.setObjectName(u"page_one_time_setup")
        self.gridLayout_35 = QGridLayout(self.page_one_time_setup)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.vbox_info = QVBoxLayout()
        self.vbox_info.setObjectName(u"vbox_info")

        self.verticalLayout_6.addLayout(self.vbox_info)


        self.gridLayout_35.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.gridLayout_29 = QGridLayout()
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.button_info_enable_all = QPushButton(self.page_one_time_setup)
        self.button_info_enable_all.setObjectName(u"button_info_enable_all")

        self.gridLayout_29.addWidget(self.button_info_enable_all, 0, 0, 1, 1)

        self.button_info_enable_update = QPushButton(self.page_one_time_setup)
        self.button_info_enable_update.setObjectName(u"button_info_enable_update")

        self.gridLayout_29.addWidget(self.button_info_enable_update, 0, 1, 1, 1)

        self.button_info_disable_all = QPushButton(self.page_one_time_setup)
        self.button_info_disable_all.setObjectName(u"button_info_disable_all")

        self.gridLayout_29.addWidget(self.button_info_disable_all, 0, 2, 1, 1)


        self.gridLayout_35.addLayout(self.gridLayout_29, 1, 0, 1, 1)

        self.CentralStackedWidget.addWidget(self.page_one_time_setup)
        self.page_update_available = QWidget()
        self.page_update_available.setObjectName(u"page_update_available")
        self.gridLayout_28 = QGridLayout(self.page_update_available)
        self.gridLayout_28.setSpacing(0)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.gridLayout_28.setContentsMargins(0, 0, 0, 0)
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
        self.page_batch = QWidget()
        self.page_batch.setObjectName(u"page_batch")
        self.gridLayout_31 = QGridLayout(self.page_batch)
        self.gridLayout_31.setSpacing(0)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.gridLayout_31.setContentsMargins(0, 0, 0, 0)
        self.CentralStackedWidget.addWidget(self.page_batch)
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.gridLayout_30 = QGridLayout(self.widget)
        self.gridLayout_30.setSpacing(0)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.gridLayout_30.setContentsMargins(0, 0, 0, 0)
        self.CentralStackedWidget.addWidget(self.widget)
        self.widget_2 = QWidget()
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_60 = QGridLayout(self.widget_2)
        self.gridLayout_60.setSpacing(0)
        self.gridLayout_60.setObjectName(u"gridLayout_60")
        self.gridLayout_60.setContentsMargins(0, 0, 0, 0)
        self.CentralStackedWidget.addWidget(self.widget_2)
        self.widget_3 = QWidget()
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_53 = QGridLayout(self.widget_3)
        self.gridLayout_53.setSpacing(0)
        self.gridLayout_53.setObjectName(u"gridLayout_53")
        self.gridLayout_53.setContentsMargins(0, 0, 0, 0)
        self.CentralStackedWidget.addWidget(self.widget_3)

        self.gridLayout_12.addWidget(self.CentralStackedWidget, 1, 0, 1, 1)

        self.formlayout_progressbar = QFormLayout()
        self.formlayout_progressbar.setObjectName(u"formlayout_progressbar")
        self.formlayout_progressbar.setHorizontalSpacing(0)
        self.formlayout_progressbar.setVerticalSpacing(0)
        self.main_label_progressbar_total = QLabel(self.centralwidget)
        self.main_label_progressbar_total.setObjectName(u"main_label_progressbar_total")

        self.formlayout_progressbar.setWidget(0, QFormLayout.ItemRole.LabelRole, self.main_label_progressbar_total)

        self.main_progressbar_total = QProgressBar(self.centralwidget)
        self.main_progressbar_total.setObjectName(u"main_progressbar_total")
        sizePolicy4.setHeightForWidth(self.main_progressbar_total.sizePolicy().hasHeightForWidth())
        self.main_progressbar_total.setSizePolicy(sizePolicy4)
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


        self.gridLayout_12.addLayout(self.formlayout_progressbar, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.main_button_switch_home, self.main_button_switch_account)
        QWidget.setTabOrder(self.main_button_switch_account, self.main_button_switch_tools)
        QWidget.setTabOrder(self.main_button_switch_tools, self.main_button_switch_settings)
        QWidget.setTabOrder(self.main_button_switch_settings, self.main_button_switch_credits)
        QWidget.setTabOrder(self.main_button_switch_credits, self.main_button_view_progress_bars)
        QWidget.setTabOrder(self.main_button_view_progress_bars, self.main_button_switch_supported_websites)
        QWidget.setTabOrder(self.main_button_switch_supported_websites, self.download_lineedit_url)
        QWidget.setTabOrder(self.download_lineedit_url, self.download_button_download)
        QWidget.setTabOrder(self.download_button_download, self.download_lineedit_playlist_url)
        QWidget.setTabOrder(self.download_lineedit_playlist_url, self.download_button_playlist_get_videos)
        QWidget.setTabOrder(self.download_button_playlist_get_videos, self.download_lineedit_model_url)
        QWidget.setTabOrder(self.download_lineedit_model_url, self.download_button_model)
        QWidget.setTabOrder(self.download_button_model, self.login_button_login)
        QWidget.setTabOrder(self.login_button_login, self.tools_button_list_categories_eporner)
        QWidget.setTabOrder(self.tools_button_list_categories_eporner, self.main_checkbox_tree_do_not_clear_videos)
        QWidget.setTabOrder(self.main_checkbox_tree_do_not_clear_videos, self.main_button_tree_automated_selection)
        QWidget.setTabOrder(self.main_button_tree_automated_selection, self.main_button_tree_keyboard_shortcuts)
        QWidget.setTabOrder(self.main_button_tree_keyboard_shortcuts, self.main_button_tree_stop)
        QWidget.setTabOrder(self.main_button_tree_stop, self.graphicsView)
        QWidget.setTabOrder(self.graphicsView, self.main_button_tree_download)
        QWidget.setTabOrder(self.main_button_tree_download, self.login_lineedit_username)
        QWidget.setTabOrder(self.login_lineedit_username, self.login_lineedit_password)
        QWidget.setTabOrder(self.login_lineedit_password, self.progress_lineedit_download_info)
        QWidget.setTabOrder(self.progress_lineedit_download_info, self.tools_lineedit_hqporner_category)
        QWidget.setTabOrder(self.tools_lineedit_hqporner_category, self.tools_button_hqporner_category_get_videos)
        QWidget.setTabOrder(self.tools_button_hqporner_category_get_videos, self.tools_button_get_brazzers_videos)
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
        QWidget.setTabOrder(self.scrollArea_3, self.lineedit_range_author)
        QWidget.setTabOrder(self.lineedit_range_author, self.button_range_apply_author)
        QWidget.setTabOrder(self.button_range_apply_author, self.lineedit_range_start)
        QWidget.setTabOrder(self.lineedit_range_start, self.lineedit_range_end)
        QWidget.setTabOrder(self.lineedit_range_end, self.button_range_apply_time)
        QWidget.setTabOrder(self.button_range_apply_time, self.spinbox_range_start)
        QWidget.setTabOrder(self.spinbox_range_start, self.spinbox_range_end)
        QWidget.setTabOrder(self.spinbox_range_end, self.button_range_apply_index)
        QWidget.setTabOrder(self.button_range_apply_index, self.scrollArea)
        QWidget.setTabOrder(self.scrollArea, self.settings_button_reset)
        QWidget.setTabOrder(self.settings_button_reset, self.textBrowser)
        QWidget.setTabOrder(self.textBrowser, self.text_browser_keyboard_shortcuts)
        QWidget.setTabOrder(self.text_browser_keyboard_shortcuts, self.text_browser_update_available)
        QWidget.setTabOrder(self.text_browser_update_available, self.button_update_acknowledged)
        QWidget.setTabOrder(self.button_update_acknowledged, self.textbrowser_install_dialog)
        QWidget.setTabOrder(self.textbrowser_install_dialog, self.settings_button_apply)
        QWidget.setTabOrder(self.settings_button_apply, self.main_textbrowser_supported_websites)
        QWidget.setTabOrder(self.main_textbrowser_supported_websites, self.scrollArea_12)
        QWidget.setTabOrder(self.scrollArea_12, self.textbrowser_disclaimer)
        QWidget.setTabOrder(self.textbrowser_disclaimer, self.button_disclaimer_accept)

        self.retranslateUi(MainWindow)

        self.CentralStackedWidget.setCurrentIndex(1)
        self.main_stacked_widget_top.setCurrentIndex(4)
        self.settings_stacked_widget_main.setCurrentIndex(1)
        self.settings_video_combobox_quality.setCurrentIndex(6)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        MainWindow.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        MainWindow.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button Tools section", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.main_button_switch_home.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button home page", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_home.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_account.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button Login (PornHub)", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_account.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_tools.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button Tools section", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_tools.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_settings.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button view progressbars", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_settings.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_credits.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button Credits / Information", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_credits.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_view_progress_bars.setAccessibleName(QCoreApplication.translate("MainWindow", u"Button view progressbars", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_view_progress_bars.setText("")
#if QT_CONFIG(accessibility)
        self.main_button_switch_supported_websites.setAccessibleName(QCoreApplication.translate("MainWindow", u"button: Supported websites", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_switch_supported_websites.setText(QCoreApplication.translate("MainWindow", u"Supported websites", None))
        self.download_website_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"HQPorner", None))
        self.download_website_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"PornHub", None))
        self.download_website_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"EPorner", None))
        self.download_website_combobox.setItemText(3, QCoreApplication.translate("MainWindow", u"XVideos", None))
        self.download_website_combobox.setItemText(4, QCoreApplication.translate("MainWindow", u"XHamster", None))
        self.download_website_combobox.setItemText(5, QCoreApplication.translate("MainWindow", u"XNXX", None))
        self.download_website_combobox.setItemText(6, QCoreApplication.translate("MainWindow", u"Spankbang", None))
        self.download_website_combobox.setItemText(7, QCoreApplication.translate("MainWindow", u"Missav", None))
        self.download_website_combobox.setItemText(8, QCoreApplication.translate("MainWindow", u"YouPorn", None))
        self.download_website_combobox.setItemText(9, QCoreApplication.translate("MainWindow", u"Porntrex", None))

#if QT_CONFIG(accessibility)
        self.download_website_combobox.setAccessibleName(QCoreApplication.translate("MainWindow", u"combobox, select search website here", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.download_lineedit_url.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit video url", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_url.setText("")
        self.download_lineedit_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a Video URL or an XHamster Short", None))
#if QT_CONFIG(accessibility)
        self.download_label_model_url.setAccessibleName(QCoreApplication.translate("MainWindow", u"label model url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_model_url.setText(QCoreApplication.translate("MainWindow", u"Model URL:", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_search_query.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit search query", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_search_query.setText("")
        self.download_lineedit_search_query.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search for videos on a website", None))
#if QT_CONFIG(accessibility)
        self.download_button_model.setAccessibleName(QCoreApplication.translate("MainWindow", u"button start fetching videos from model, channel, actress or creator", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_model.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_label_search.setAccessibleName(QCoreApplication.translate("MainWindow", u"label search query", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_search.setText(QCoreApplication.translate("MainWindow", u"Search Query:", None))
#if QT_CONFIG(accessibility)
        self.button_search.setAccessibleName(QCoreApplication.translate("MainWindow", u"button start video search", None))
#endif // QT_CONFIG(accessibility)
        self.button_search.setText(QCoreApplication.translate("MainWindow", u"Search", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_model_url.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit model / channel, actress, creator URL", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_model_url.setText("")
        self.download_lineedit_model_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a Model / Channel / Actress / Creator URL ", None))
#if QT_CONFIG(accessibility)
        self.download_label_playlist_url.setAccessibleName(QCoreApplication.translate("MainWindow", u"label playlist url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_playlist_url.setText(QCoreApplication.translate("MainWindow", u"Playlist URL:", None))
#if QT_CONFIG(accessibility)
        self.download_button_download.setAccessibleName(QCoreApplication.translate("MainWindow", u"button start downloading a video", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_download.setText(QCoreApplication.translate("MainWindow", u"Download", None))
#if QT_CONFIG(accessibility)
        self.download_button_playlist_get_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"button start fetching videos of a playlist", None))
#endif // QT_CONFIG(accessibility)
        self.download_button_playlist_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.download_lineedit_playlist_url.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit playlist URL (PornHub, Xvideos)", None))
#endif // QT_CONFIG(accessibility)
        self.download_lineedit_playlist_url.setText("")
        self.download_lineedit_playlist_url.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter a PornHub / XVideos Playlist URL", None))
#if QT_CONFIG(accessibility)
        self.download_label_url.setAccessibleName(QCoreApplication.translate("MainWindow", u"label video url", None))
#endif // QT_CONFIG(accessibility)
        self.download_label_url.setText(QCoreApplication.translate("MainWindow", u"Video URL:", None))
#if QT_CONFIG(accessibility)
        self.login_button_get_watched_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"button get watched videos (requires login) ", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_get_watched_videos.setText(QCoreApplication.translate("MainWindow", u"Get watched videos", None))
#if QT_CONFIG(accessibility)
        self.login_button_get_recommended_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"button get recommended videos (requires login)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_get_recommended_videos.setText(QCoreApplication.translate("MainWindow", u"Get recommended videos", None))
#if QT_CONFIG(accessibility)
        self.login_button_get_liked_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"button get liked videos (requires login)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_get_liked_videos.setText(QCoreApplication.translate("MainWindow", u"Get Liked videos", None))
#if QT_CONFIG(accessibility)
        self.login_lineedit_password.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit password ", None))
#endif // QT_CONFIG(accessibility)
        self.login_lineedit_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your PornHub Password (Your account data will never be saved nor shared) ", None))
#if QT_CONFIG(accessibility)
        self.login_lineedit_username.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit email", None))
#endif // QT_CONFIG(accessibility)
        self.login_lineedit_username.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your PornHub E-Mail address", None))
#if QT_CONFIG(accessibility)
        self.login_button_login.setAccessibleName(QCoreApplication.translate("MainWindow", u"button start login (enter credentials above)", None))
#endif // QT_CONFIG(accessibility)
        self.login_button_login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
#if QT_CONFIG(accessibility)
        self.login_label_password.setAccessibleName(QCoreApplication.translate("MainWindow", u"label password", None))
#endif // QT_CONFIG(accessibility)
        self.login_label_password.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
#if QT_CONFIG(accessibility)
        self.login_label_username.setAccessibleName(QCoreApplication.translate("MainWindow", u"label username", None))
#endif // QT_CONFIG(accessibility)
        self.login_label_username.setText(QCoreApplication.translate("MainWindow", u"E-Mail:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"HQPorner", None))
#if QT_CONFIG(accessibility)
        self.tools_button_get_random_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools button hqporner get random video", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_get_random_videos.setText(QCoreApplication.translate("MainWindow", u"Get random Video", None))
#if QT_CONFIG(accessibility)
        self.tools_button_hqporner_category_get_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools button hqporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_hqporner_category_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.tools_label_videos_by_category.setAccessibleName(QCoreApplication.translate("MainWindow", u"label tools hqporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_label_videos_by_category.setText(QCoreApplication.translate("MainWindow", u"Get videos by category", None))
#if QT_CONFIG(accessibility)
        self.tools_lineedit_hqporner_category.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools lineedit hqporner category (enter the category here)", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.tools_label_get_top_porn.setAccessibleName(QCoreApplication.translate("MainWindow", u"label tools hqporn get top porn", None))
#endif // QT_CONFIG(accessibility)
        self.tools_label_get_top_porn.setText(QCoreApplication.translate("MainWindow", u"Get Top Porn:", None))
#if QT_CONFIG(accessibility)
        self.tools_button_get_brazzers_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools buttonn get brazzers videos", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_get_brazzers_videos.setText(QCoreApplication.translate("MainWindow", u"Get Brazzers videos", None))
        self.tools_combobox_hqporner_top_porn.setItemText(0, QCoreApplication.translate("MainWindow", u"Week", None))
        self.tools_combobox_hqporner_top_porn.setItemText(1, QCoreApplication.translate("MainWindow", u"Month", None))
        self.tools_combobox_hqporner_top_porn.setItemText(2, QCoreApplication.translate("MainWindow", u"All time", None))

#if QT_CONFIG(accessibility)
        self.tools_combobox_hqporner_top_porn.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools combobox hqporner top porn selection", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.tools_button_top_porn_get_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools button hqporner get videos by top porn", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_top_porn_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.tools_button_list_categories.setAccessibleName(QCoreApplication.translate("MainWindow", u"tools button hqporner list all categories", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_list_categories.setText(QCoreApplication.translate("MainWindow", u"List of all categories", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"EPorner", None))
#if QT_CONFIG(accessibility)
        self.tools_lineedit_videos_by_category_eporner.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit tools eporner enter category here", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.tools_button_eporner_category_get_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"button tools eporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_eporner_category_get_videos.setText(QCoreApplication.translate("MainWindow", u"Get Videos", None))
#if QT_CONFIG(accessibility)
        self.tools_button_list_categories_eporner.setAccessibleName(QCoreApplication.translate("MainWindow", u"button tools eporner list all categories", None))
#endif // QT_CONFIG(accessibility)
        self.tools_button_list_categories_eporner.setText(QCoreApplication.translate("MainWindow", u"List of all categories", None))
#if QT_CONFIG(accessibility)
        self.tools_label_videos_by_category_eporner.setAccessibleName(QCoreApplication.translate("MainWindow", u"label tools eporner get videos by category", None))
#endif // QT_CONFIG(accessibility)
        self.tools_label_videos_by_category_eporner.setText(QCoreApplication.translate("MainWindow", u"Get videos by category", None))
#if QT_CONFIG(accessibility)
        self.progress_label_info.setAccessibleName(QCoreApplication.translate("MainWindow", u"label information (this shows how many videos have been downloaded)", None))
#endif // QT_CONFIG(accessibility)
        self.progress_label_info.setText(QCoreApplication.translate("MainWindow", u"Info:", None))
#if QT_CONFIG(accessibility)
        self.progress_lineedit_download_info.setAccessibleName(QCoreApplication.translate("MainWindow", u"information (the actual value) ", None))
#endif // QT_CONFIG(accessibility)
        self.progress_lineedit_download_info.setText("")
#if QT_CONFIG(accessibility)
        self.button_range_apply_index.setAccessibleName(QCoreApplication.translate("MainWindow", u"button apply automated selection by index", None))
#endif // QT_CONFIG(accessibility)
        self.button_range_apply_index.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
#if QT_CONFIG(accessibility)
        self.lineedit_range_start.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox apply by time range start", None))
#endif // QT_CONFIG(accessibility)
        self.lineedit_range_start.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(accessibility)
        self.button_range_apply_author.setAccessibleName(QCoreApplication.translate("MainWindow", u"button apply automated video selection by author", None))
#endif // QT_CONFIG(accessibility)
        self.button_range_apply_author.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
#if QT_CONFIG(accessibility)
        self.spinbox_range_start.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox apply by index start", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.lineedit_range_author.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit author name ", None))
#endif // QT_CONFIG(accessibility)
        self.lineedit_range_author.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the author's name", None))
#if QT_CONFIG(accessibility)
        self.spinbox_range_end.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox apply by index end", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.label_range_start.setAccessibleName(QCoreApplication.translate("MainWindow", u"label index range start", None))
#endif // QT_CONFIG(accessibility)
        self.label_range_start.setText(QCoreApplication.translate("MainWindow", u"Start:", None))
#if QT_CONFIG(accessibility)
        self.button_range_apply_time.setAccessibleName(QCoreApplication.translate("MainWindow", u"button apply automated selection by time", None))
#endif // QT_CONFIG(accessibility)
        self.button_range_apply_time.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
#if QT_CONFIG(accessibility)
        self.lineedit_range_end.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox apply by time range end", None))
#endif // QT_CONFIG(accessibility)
        self.lineedit_range_end.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(accessibility)
        self.label_range_by_author.setAccessibleName(QCoreApplication.translate("MainWindow", u"label apply by author", None))
#endif // QT_CONFIG(accessibility)
        self.label_range_by_author.setText(QCoreApplication.translate("MainWindow", u"Apply by author:", None))
#if QT_CONFIG(accessibility)
        self.label_range_end.setAccessibleName(QCoreApplication.translate("MainWindow", u"label index range end", None))
#endif // QT_CONFIG(accessibility)
        self.label_range_end.setText(QCoreApplication.translate("MainWindow", u"End:", None))
#if QT_CONFIG(accessibility)
        self.label_apply_by_time.setAccessibleName(QCoreApplication.translate("MainWindow", u"label apply by time", None))
#endif // QT_CONFIG(accessibility)
        self.label_apply_by_time.setText(QCoreApplication.translate("MainWindow", u"Apply by time:", None))
#if QT_CONFIG(accessibility)
        self.label_range_time_start.setAccessibleName(QCoreApplication.translate("MainWindow", u"label apply by time start", None))
#endif // QT_CONFIG(accessibility)
        self.label_range_time_start.setText(QCoreApplication.translate("MainWindow", u"Start:", None))
#if QT_CONFIG(accessibility)
        self.label_range_time_end.setAccessibleName(QCoreApplication.translate("MainWindow", u"label apply by time end", None))
#endif // QT_CONFIG(accessibility)
        self.label_range_time_end.setText(QCoreApplication.translate("MainWindow", u"End:", None))
#if QT_CONFIG(accessibility)
        self.button_range_select_all.setAccessibleName(QCoreApplication.translate("MainWindow", u"button automated selection select all videos", None))
#endif // QT_CONFIG(accessibility)
        self.button_range_select_all.setText(QCoreApplication.translate("MainWindow", u"Select all videos", None))
#if QT_CONFIG(accessibility)
        self.button_range_unselect_all.setAccessibleName(QCoreApplication.translate("MainWindow", u"button automated selection unselect all videos", None))
#endif // QT_CONFIG(accessibility)
        self.button_range_unselect_all.setText(QCoreApplication.translate("MainWindow", u"Unselect all videos", None))
#if QT_CONFIG(accessibility)
        self.label_apply_by_index.setAccessibleName(QCoreApplication.translate("MainWindow", u"label apply by index", None))
#endif // QT_CONFIG(accessibility)
        self.label_apply_by_index.setText(QCoreApplication.translate("MainWindow", u"Apply by Index:", None))
        self.main_button_tree_download.setText(QCoreApplication.translate("MainWindow", u"Download Selected Videos", None))
#if QT_CONFIG(accessibility)
        self.main_button_tree_keyboard_shortcuts.setAccessibleName(QCoreApplication.translate("MainWindow", u"button keyboard shortcuts", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_tree_keyboard_shortcuts.setText(QCoreApplication.translate("MainWindow", u"Keyboard shortcuts", None))
#if QT_CONFIG(accessibility)
        self.main_checkbox_direct_download.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox directly download videos", None))
#endif // QT_CONFIG(accessibility)
        self.main_checkbox_direct_download.setText(QCoreApplication.translate("MainWindow", u"Download videos \n"
"directly ", None))
#if QT_CONFIG(tooltip)
        self.main_button_tree_stop.setToolTip(QCoreApplication.translate("MainWindow", u"Does not stop downloading videos", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.main_button_tree_stop.setAccessibleName(QCoreApplication.translate("MainWindow", u"button stop loading videos", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_tree_stop.setText(QCoreApplication.translate("MainWindow", u"Stop loading videos", None))
#if QT_CONFIG(accessibility)
        self.main_checkbox_tree_do_not_clear_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox do not clear videos", None))
#endif // QT_CONFIG(accessibility)
        self.main_checkbox_tree_do_not_clear_videos.setText(QCoreApplication.translate("MainWindow", u"Do not clear videos", None))
#if QT_CONFIG(accessibility)
        self.main_button_tree_automated_selection.setAccessibleName(QCoreApplication.translate("MainWindow", u"button automated selection tool", None))
#endif // QT_CONFIG(accessibility)
        self.main_button_tree_automated_selection.setText(QCoreApplication.translate("MainWindow", u"Automated selection tool", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_index_videos.setToolTip(QCoreApplication.translate("MainWindow", u"This feature allows you to only fetch a specific range of videos when\n"
"searching, loading models / channels or fetching a playlist.\n"
"\n"
"For example if you use 20 for the start and 30 for the end value, the first\n"
"20 videos will be completely ignored and not loaded into the tree widget.\n"
"This can save a lot of time in certain scenarios.\n"
"", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_index_videos.setText("")
        self.label_index_start.setText(QCoreApplication.translate("MainWindow", u"Start:", None))
        self.label_index_end.setText(QCoreApplication.translate("MainWindow", u"End:", None))
#if QT_CONFIG(accessibility)
        self.graphicsView.setAccessibleName(QCoreApplication.translate("MainWindow", u"thumbnail display", None))
#endif // QT_CONFIG(accessibility)
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Duration (minutes)", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Author", None));
#if QT_CONFIG(accessibility)
        self.settings_button_switch_video.setAccessibleName(QCoreApplication.translate("MainWindow", u"Video page (settings)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_video.setText(QCoreApplication.translate("MainWindow", u"Video", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_performance.setAccessibleName(QCoreApplication.translate("MainWindow", u"Performance page (Settings)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_performance.setText(QCoreApplication.translate("MainWindow", u"Performance", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_system.setAccessibleName(QCoreApplication.translate("MainWindow", u"System page (settings)", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_button_switch_system.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_system.setText(QCoreApplication.translate("MainWindow", u"System", None))
#if QT_CONFIG(accessibility)
        self.settings_button_switch_ui.setAccessibleName(QCoreApplication.translate("MainWindow", u"button: Supported websites", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_switch_ui.setText(QCoreApplication.translate("MainWindow", u"UI", None))
#if QT_CONFIG(tooltip)
        self.settings_label_videos_result_limit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_videos_result_limit.setAccessibleName(QCoreApplication.translate("MainWindow", u"label result limit", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_result_limit.setText(QCoreApplication.translate("MainWindow", u"Result Limit:", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_use_directory_system.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_directory_system.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox use directory system", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_directory_system.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"The directory system will automatically create folders for each author of videos", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_directory_system.setText(QCoreApplication.translate("MainWindow", u"Use directory system", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_track_downloaded_videos.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_track_downloaded_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox track downloaded videos", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_track_downloaded_videos.setText(QCoreApplication.translate("MainWindow", u"Track downloaded videos", None))
#if QT_CONFIG(tooltip)
        self.settings_label_videos_quality.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_videos_quality.setAccessibleName(QCoreApplication.translate("MainWindow", u"label video quality", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_quality.setText(QCoreApplication.translate("MainWindow", u"Quality:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_model_videos.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_model_videos.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_skip_existing_files.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_skip_existing_files.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox skip existing files", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_skip_existing_files.setText(QCoreApplication.translate("MainWindow", u"Skip existing files", None))
#if QT_CONFIG(accessibility)
        self.settings_label_videos_output_path.setAccessibleName(QCoreApplication.translate("MainWindow", u"label output path", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_output_path.setText(QCoreApplication.translate("MainWindow", u"Output path:", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_videos_write_metadata.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_write_metadata.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox write metadata tags", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_write_metadata.setText(QCoreApplication.translate("MainWindow", u"Write metadata tags", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_quality.setToolTip(QCoreApplication.translate("MainWindow", u"By default, Porn Fetch will select the best available video quality. You can also decide between half and worst above.\n"
"If you instead use the custom integer values (1080p, 720p etc.) then Porn Fetch will try to use these, if available,\n"
"but if they are not available the next best quality will be chosen. Please note that this is experimental and has not\n"
"been that tested very well. (Be honest, why would you not choose the best quality lol)", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_quality.setText("")
        self.settings_video_combobox_model_videos.setItemText(0, QCoreApplication.translate("MainWindow", u"Both (recommended)", None))
        self.settings_video_combobox_model_videos.setItemText(1, QCoreApplication.translate("MainWindow", u"Uploaded", None))
        self.settings_video_combobox_model_videos.setItemText(2, QCoreApplication.translate("MainWindow", u"Featured", None))

#if QT_CONFIG(accessibility)
        self.settings_video_combobox_model_videos.setAccessibleName(QCoreApplication.translate("MainWindow", u"combobox model videos type", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_video_combobox_model_videos.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"This decides whether you want to fetch model uploads or featured videos or both of them", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.label_tooltip_result_limit.setToolTip(QCoreApplication.translate("MainWindow", u"The result limit defines how many videos will be returned when performing a search or doing other operations which\n"
"involves loading multiple videos. This also affects models / channels and your liked videos. The result limit is\n"
"basically the number of videos which can be loaded into the tree widget (this thing where videos are displayed).", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_result_limit.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_track_videos.setToolTip(QCoreApplication.translate("MainWindow", u"Videos will be tracked in a SQL database which will save the URL and the metadata. ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_track_videos.setText("")
#if QT_CONFIG(accessibility)
        self.settings_button_videos_open_output_path.setAccessibleName(QCoreApplication.translate("MainWindow", u"settings open output path", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_videos_open_output_path.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.settings_video_combobox_quality.setItemText(0, QCoreApplication.translate("MainWindow", u"BEST (auto)", None))
        self.settings_video_combobox_quality.setItemText(1, QCoreApplication.translate("MainWindow", u"HALF (auto)", None))
        self.settings_video_combobox_quality.setItemText(2, QCoreApplication.translate("MainWindow", u"WORST (auto)", None))
        self.settings_video_combobox_quality.setItemText(3, QCoreApplication.translate("MainWindow", u"2160p", None))
        self.settings_video_combobox_quality.setItemText(4, QCoreApplication.translate("MainWindow", u"1440p", None))
        self.settings_video_combobox_quality.setItemText(5, QCoreApplication.translate("MainWindow", u"1080p", None))
        self.settings_video_combobox_quality.setItemText(6, QCoreApplication.translate("MainWindow", u"720p", None))
        self.settings_video_combobox_quality.setItemText(7, QCoreApplication.translate("MainWindow", u"540p", None))
        self.settings_video_combobox_quality.setItemText(8, QCoreApplication.translate("MainWindow", u"360p", None))
        self.settings_video_combobox_quality.setItemText(9, QCoreApplication.translate("MainWindow", u"240p", None))
        self.settings_video_combobox_quality.setItemText(10, QCoreApplication.translate("MainWindow", u"144p", None))

#if QT_CONFIG(accessibility)
        self.settings_video_combobox_quality.setAccessibleName(QCoreApplication.translate("MainWindow", u"combobox settings quality", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_video_combobox_quality.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"Porn Fetch will by default download the best video quality", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_lineedit_videos_database_path.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit output path of the database", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_lineedit_videos_database_path.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"the database tracks all downloaded videos in Porn Fetch, optional", None))
#endif // QT_CONFIG(accessibility)
        self.settings_lineedit_videos_database_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter the path of the database file here", None))
#if QT_CONFIG(accessibility)
        self.settings_spinbox_videos_result_limit.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox resutl limit", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_spinbox_videos_result_limit.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"The result limit limits how many videos will be fetched", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_video_id_as_filename.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox use video id as filename", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_videos_use_video_id_as_filename.setText(QCoreApplication.translate("MainWindow", u"Use Video ID as filename", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_write_metadata.setToolTip(QCoreApplication.translate("MainWindow", u"Metadata tags are saved inside of the file itself. These are tags that video players can read from and provide you information.\n"
"Some folder viewers also give you the ability to search files by specific metadata tags. Those tags can help organize and structure files.\n"
"Porn Fetch will by default save those tags inside of your video files. ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_write_metadata.setText("")
#if QT_CONFIG(tooltip)
        self.settings_label_videos_model_vdeos_type.setToolTip(QCoreApplication.translate("MainWindow", u"User uploads and featured videos are two different things. User uploads are the videos which were really uploaded\n"
"by the model and the featured videos are videos the model is part or featured in.\n"
"\n"
"For example the model Nancy Ace has like 10 self uploaded which she made by herself, but she is part in like thousands\n"
"of videos from other studios.\n"
"\n"
"If you choose \"User Uploads\", only self uploaded videos will be fetched, and the other way around :)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_videos_model_vdeos_type.setAccessibleName(QCoreApplication.translate("MainWindow", u"label model videos type (pornhub)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_videos_model_vdeos_type.setText(QCoreApplication.translate("MainWindow", u"Model videos (PH)", None))
#if QT_CONFIG(accessibility)
        self.settings_lineedit_videos_output_path.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit video output path", None))
#endif // QT_CONFIG(accessibility)
        self.settings_lineedit_videos_output_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter \"./\" for current directory", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_use_directory_system.setToolTip(QCoreApplication.translate("MainWindow", u"The directory system will save videos in an intelligent way. If you download 3 videos form one Pornstar and 5 videos \n"
"from another, Porn Fetch will automatically make folders for it and move the 3 videos into that one folder and the other\n"
"5 into the other. (This will still apply with your selected output path)\n"
"\n"
"This can be helpful for organizing stuff, but is a more advanced feature, so the majority of users won't use it probably", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_use_directory_system.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_skip_existing_files.setToolTip(QCoreApplication.translate("MainWindow", u"If you fetch a video and the exact same filename already exists, usually Porn Fetch would just skip this file.\n"
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
        self.settings_label_performance_speed_limit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_speed_limit.setAccessibleName(QCoreApplication.translate("MainWindow", u"Speed Limit (MB/s)", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_speed_limit.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"Pages concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_speed_limit.setText(QCoreApplication.translate("MainWindow", u"Speed Limit (MB/s):", None))
#if QT_CONFIG(accessibility)
        self.settings_label_performance_download_mode.setAccessibleName(QCoreApplication.translate("MainWindow", u"Download Mode", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_download_mode.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_download_mode.setText(QCoreApplication.translate("MainWindow", u"Download Mode:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_maximum_timeout.setToolTip(QCoreApplication.translate("MainWindow", u"The timeout handles the timeout for retrieving segments when using the threaded download mode. If you have a poor \n"
"internet connection you can set this higher than 10. But this isn't required for most users!", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_maximum_timeout.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_pages_concurrency.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The pages concurrency defines how many pages will be scraped at the same time,</p><p>when searching for videos or fetching models. Lower values are generally recommended,</p><p>to avoid getting blocked. Keep it between 1-3.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_pages_concurrency.setText("")
#if QT_CONFIG(tooltip)
        self.settings_label_performance_processing_delay.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_processing_delay.setAccessibleName(QCoreApplication.translate("MainWindow", u"Videos Concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_processing_delay.setText(QCoreApplication.translate("MainWindow", u"Processing Delay (videos/sec):", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_pages_concurrency.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_pages_concurrency.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"Pages concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_pages_concurrency.setText(QCoreApplication.translate("MainWindow", u"Pages concurrency:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_simultaneous_downloads.setToolTip(QCoreApplication.translate("MainWindow", u"The Semaphore is a tool to limit the number of simultaneous actions / downloads. For example: If the semaphore is set to 1, only 1 video will be downloaded at the same time.\\nIf the semaphore is set to 4, 4 videos will be downloaded at the same time. Changing this is only useful, if you have a really good internet connection and a good system.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_simultaneous_downloads.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_speed_limit.setToolTip(QCoreApplication.translate("MainWindow", u"The speed limit sets the maximum allowed network speed in megabyte per seconds. However, this doesn't work perfectly.\n"
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
        self.settings_label_performance_maximal_retries.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"Maximum retries", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_retries.setText(QCoreApplication.translate("MainWindow", u"Maximum retries:", None))
#if QT_CONFIG(accessibility)
        self.settings_doublespinbox_performance_speed_limit.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox speed limit", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.label_tooltip_download_mode.setToolTip(QCoreApplication.translate("MainWindow", u"1) High Performance:  Uses a class of workers to download multiple video segments at a time. Can be really fast if you\n"
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
        self.settings_spinbox_performance_pages_concurrency.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox pages concurrency", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_spinbox_performance_pages_concurrency.setAccessibleDescription(QCoreApplication.translate("MainWindow", u"This decides how many pages will be scraped at the same time. Lower values between 1-3 are recommended", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(tooltip)
        self.settings_label_performance_simultaneous_download.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_simultaneous_download.setAccessibleName(QCoreApplication.translate("MainWindow", u"Simultaneous downloads", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_simultaneous_download.setText(QCoreApplication.translate("MainWindow", u"Simultaneous downloads:", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_maximal_timeout.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_timeout.setAccessibleName(QCoreApplication.translate("MainWindow", u"Maximum timeout", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_maximal_timeout.setText(QCoreApplication.translate("MainWindow", u"Maximum timeout:", None))
#if QT_CONFIG(tooltip)
        self.settings_label_performance_videos_concurrency.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_videos_concurrency.setAccessibleName(QCoreApplication.translate("MainWindow", u"Videos Concurrency", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_videos_concurrency.setText(QCoreApplication.translate("MainWindow", u"Videos Concurrency:", None))
        self.settings_performance_combobox_download_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"High Performance", None))
        self.settings_performance_combobox_download_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"FFMPEG", None))
        self.settings_performance_combobox_download_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"Default", None))

#if QT_CONFIG(tooltip)
        self.settings_performance_combobox_download_mode.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.settings_label_performance_network_delay.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_label_performance_network_delay.setAccessibleName(QCoreApplication.translate("MainWindow", u"Network delay (requests/sec)", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_performance_network_delay.setText(QCoreApplication.translate("MainWindow", u"Network delay (requests/sec):", None))
#if QT_CONFIG(tooltip)
        self.label_settings_performance_download_workers.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.label_settings_performance_download_workers.setAccessibleName(QCoreApplication.translate("MainWindow", u"Download workers:", None))
#endif // QT_CONFIG(accessibility)
        self.label_settings_performance_download_workers.setText(QCoreApplication.translate("MainWindow", u"Download workers:", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_network_delay.setToolTip(QCoreApplication.translate("MainWindow", u"You can set a delay between requests from you and a site. If you are downloading a lot of videos or experiencing \n"
"errors, you should enable a delay. By default the delay is turned off with the value 0\n"
"\n"
"A good starting point is between 0.5 - 1.5\n"
"\n"
"The longer the delay is, the longer it will take to download videos, load videos and generally do stuff. This does not\n"
"really affect the high performance download mode.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_network_delay.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_processing_delay.setToolTip(QCoreApplication.translate("MainWindow", u"The processing delay sets a delay before every video gets downloaded.\n"
"Let's assume you set a delay of 30 (30 seconds), then it will take 30 seconds between each video downloads.\n"
"This does not apply if you have a value of simultaneous downloads greater than 1.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_processing_delay.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_videos_concurrency.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The videos concurrency defines how many videos are fetched at the same time when searching or fetching models etc.</p><p>For example, let's say you search for something. Then the first page of the results will be scraped for video URLs. This takes</p><p>usually around 1 second. If you set this value to 20, then from all those URLs Porn Fetch will attempt to load 20 videos at</p><p>the same time. This can improve speed A LOT, but can also get you blocked from the site. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_videos_concurrency.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_download_workers.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>The download worker setting defines, how many workers / threads will be used at the same time</p><p>to fetch video segments at the same time. Usually you don't need to go over 20, unless you have a higher</p><p>internet connection than 1gbit/s. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_download_workers.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_maximum_retries.setToolTip(QCoreApplication.translate("MainWindow", u"The maximal retries defines how much attempts will be used for a network request. For example if an API calls\n"
"a URL for a website there will be <AMOUNT> of attempts until an error is thrown.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_maximum_retries.setText("")
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_activate_proxy.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox activate a proxy", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_activate_proxy.setText(QCoreApplication.translate("MainWindow", u"Activate Proxy", None))
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_internet_checks.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox enable internet checks", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_internet_checks.setText(QCoreApplication.translate("MainWindow", u"Internet checks", None))
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_enable_network_logging.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_network_logging.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox enable network logging", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_network_logging.setText(QCoreApplication.translate("MainWindow", u"Enable Network Logging", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_network_logging.setToolTip(QCoreApplication.translate("MainWindow", u"I have created my own server that runs 24/7 in my home. Porn Fetch (ONLY if you enable it) logs specific types of errors,\n"
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
        self.settings_checkbox_system_supress_errors.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_supress_errors.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox supress errors silently", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_supress_errors.setText(QCoreApplication.translate("MainWindow", u"Supress errors silently", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_update_checks.setToolTip(QCoreApplication.translate("MainWindow", u"Porn Fetch will check for updates each time it starts, using my own server. This will require a working IPv6 connection. No personal data nor any other data is sent during this process.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_update_checks.setText("")
#if QT_CONFIG(tooltip)
        self.label_tooltip_anonymous_mode.setToolTip(QCoreApplication.translate("MainWindow", u"The anonymous mode renames all of Porn Fetch's elements to look NOT like a Porn downloader.\n"
"This makes it useful for downloading Porn content if you are in public, or multiple people use your PC / Phone.\n"
"\n"
"This also disables thumbnail preview. All titles will be replaced with: [redacted] as well as all authors.", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_anonymous_mode.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_enable_anonymous_mode.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_anonymous_mode.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox enable anonymous mode", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_enable_anonymous_mode.setText(QCoreApplication.translate("MainWindow", u"Enable Anonymous mode", None))
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_update_checks.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox enable update checks", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_update_checks.setText(QCoreApplication.translate("MainWindow", u"Update checks", None))
#if QT_CONFIG(tooltip)
        self.label_tooltip_supress_errors.setToolTip(QCoreApplication.translate("MainWindow", u"If you enable this function, all errors will be suppressed. This does not mean that they will be completely ignored, but\n"
"you won't get a big notification for it. \n"
"\n"
"If you have activated Network Logging, they will still be reported. If an error happens while iterating through videos,\n"
"the current video will be skipped and Porn Fetch will continue with the next one.  ", None))
#endif // QT_CONFIG(tooltip)
        self.label_tooltip_supress_errors.setText("")
#if QT_CONFIG(tooltip)
        self.settings_checkbox_system_proxy_kill_switch.setToolTip(QCoreApplication.translate("MainWindow", u"The proxy kill switch is an additional security layer if you use proxies. It will check your IP each time before making\n"
"a request and if it's leaked it will immediately exit everything.\n"
"\n"
"My priority on developing this is low. Please do not report errors. Thank you <3", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(accessibility)
        self.settings_checkbox_system_proxy_kill_switch.setAccessibleName(QCoreApplication.translate("MainWindow", u"checkbox enable proxy kill switch", None))
#endif // QT_CONFIG(accessibility)
        self.settings_checkbox_system_proxy_kill_switch.setText(QCoreApplication.translate("MainWindow", u"Proxy Kill Switch", None))
#if QT_CONFIG(accessibility)
        self.settings_button_system_install_pornfetch.setAccessibleName(QCoreApplication.translate("MainWindow", u"button install porn fetch (This is optional) ", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_system_install_pornfetch.setText(QCoreApplication.translate("MainWindow", u"Install Porn Fetch", None))
        self.settings_lineedit_system_custom_app_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Write a custom app name here", None))
#if QT_CONFIG(accessibility)
        self.settings_label_ui_theme.setAccessibleName(QCoreApplication.translate("MainWindow", u"label porn fetch theme ", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_ui_theme.setText(QCoreApplication.translate("MainWindow", u"Theme:", None))
#if QT_CONFIG(accessibility)
        self.settings_label_ui_language.setAccessibleName(QCoreApplication.translate("MainWindow", u"label graphical user interface language", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_ui_language.setText(QCoreApplication.translate("MainWindow", u"Graphical User Interface Language:", None))
#if QT_CONFIG(accessibility)
        self.settings_label_ui_font_size.setAccessibleName(QCoreApplication.translate("MainWindow", u"label font size", None))
#endif // QT_CONFIG(accessibility)
        self.settings_label_ui_font_size.setText(QCoreApplication.translate("MainWindow", u"Font Size:", None))
        self.settings_combobox_ui_theme.setItemText(0, QCoreApplication.translate("MainWindow", u"Dark", None))
        self.settings_combobox_ui_theme.setItemText(1, QCoreApplication.translate("MainWindow", u"Light (why would you pick light theme)", None))
        self.settings_combobox_ui_theme.setItemText(2, QCoreApplication.translate("MainWindow", u"LSD (don't activate while you are high) ", None))

#if QT_CONFIG(accessibility)
        self.settings_combobox_ui_theme.setAccessibleName(QCoreApplication.translate("MainWindow", u"combobox porn fetch theme", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_spinbox_ui_font_size.setAccessibleName(QCoreApplication.translate("MainWindow", u"spinbox font size", None))
#endif // QT_CONFIG(accessibility)
        self.settings_ui_combobox_language.setItemText(0, QCoreApplication.translate("MainWindow", u"System", None))
        self.settings_ui_combobox_language.setItemText(1, QCoreApplication.translate("MainWindow", u"English", None))
        self.settings_ui_combobox_language.setItemText(2, QCoreApplication.translate("MainWindow", u"German", None))
        self.settings_ui_combobox_language.setItemText(3, QCoreApplication.translate("MainWindow", u"Chinese simplified (outdated)", None))
        self.settings_ui_combobox_language.setItemText(4, QCoreApplication.translate("MainWindow", u"French (outdated)", None))
        self.settings_ui_combobox_language.setItemText(5, QCoreApplication.translate("MainWindow", u"Italian", None))

#if QT_CONFIG(accessibility)
        self.settings_ui_combobox_language.setAccessibleName(QCoreApplication.translate("MainWindow", u"combobox porn fetch language", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.settings_button_apply.setAccessibleName(QCoreApplication.translate("MainWindow", u"button apply the settings", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_apply.setText(QCoreApplication.translate("MainWindow", u"Apply  (needs restart)", None))
#if QT_CONFIG(accessibility)
        self.settings_button_reset.setAccessibleName(QCoreApplication.translate("MainWindow", u"button reset porn fetch to default settings", None))
#endif // QT_CONFIG(accessibility)
        self.settings_button_reset.setText(QCoreApplication.translate("MainWindow", u"Reset Porn Fetch to default settings", None))
        self.settings_button_buy_license.setText(QCoreApplication.translate("MainWindow", u"Buy License (5\u20ac)", None))
        self.settings_button_import_license.setText(QCoreApplication.translate("MainWindow", u"Import License File", None))
        self.button_credits_send_feedback.setText(QCoreApplication.translate("MainWindow", u"Send Feedback (Anonymously)", None))
#if QT_CONFIG(accessibility)
        self.main_textbrowser_credits.setAccessibleName(QCoreApplication.translate("MainWindow", u"Textbrowser for credits / information", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.button_accept.setAccessibleName(QCoreApplication.translate("MainWindow", u"button accept license", None))
#endif // QT_CONFIG(accessibility)
        self.button_accept.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
#if QT_CONFIG(accessibility)
        self.button_deny.setAccessibleName(QCoreApplication.translate("MainWindow", u"button deny license", None))
#endif // QT_CONFIG(accessibility)
        self.button_deny.setText(QCoreApplication.translate("MainWindow", u"Deny and Exit", None))
#if QT_CONFIG(accessibility)
        self.textBrowser.setAccessibleName(QCoreApplication.translate("MainWindow", u"textbrowser license", None))
#endif // QT_CONFIG(accessibility)
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
#if QT_CONFIG(accessibility)
        self.text_browser_keyboard_shortcuts.setAccessibleName(QCoreApplication.translate("MainWindow", u"textbrowser keyboard shortcuts", None))
#endif // QT_CONFIG(accessibility)
        self.text_browser_keyboard_shortcuts.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:14pt; font-weight:700;\">Keyboard Shortcuts</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:14pt; font-weight:700;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0"
                        "px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + Q     Closes the application</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + E      Exports all current video URLs from the tree widget into a .txt file </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + T      Downloads all videos in the tree widget (same as clicking the button)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + A     Quickly enables the anonymous mode (temporarily)</span></p>\n"
"<p style=\" margin-top:0px; margin-bott"
                        "om:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + S     Saves Porn Fetch settings</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + X     Selects all items in the tree widget as checked</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">CTRL + Z     Unchecks all items in the tree widget</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0"
                        "; text-indent:0px; font-family:'Sans Serif'; font-size:16pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:16pt;\">   </span></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.textbrowser_install_dialog.setAccessibleName(QCoreApplication.translate("MainWindow", u"textbrowser install dialog", None))
#endif // QT_CONFIG(accessibility)
        self.textbrowser_install_dialog.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:24pt; font-weight:700;\">Installation Mode</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#0000ff;\">1) Inst</span><span style=\" font-family:'Segoe UI'; font-size:14pt; text-decor"
                        "ation: underline; color:#0000ff;\">all</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This will install Porn Fetch into your system, meaning that you can run it directly from your Start Menu. e.g, press Windows key, type Porn Fetch and directly start it and on Linux it will be the same.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Porn Fetch will be installed into the following path(s):</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0"
                        "; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Windows: C:\\Users\\&lt;user&gt;\\AppData\\Local\\pornfetch\\</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Linux: ~/.local/share/pornfetch</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#00ff00;\">2) Portable</span></p>\n"
"<p style=\" margin-to"
                        "p:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This means, that Porn Fetch will not be installed and in order to use and start Porn Fetch you always need to double click on the file you have downloaded. This has some benefits as the uninstallation is easier and you have more control over it, but for the average user I do not recommend this.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; font-weight:700; color:#a100ff;\">Custom App name</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0"
                        "px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\">Down below you can enter  a custom name for Porn Fetch. You can then search with this name for Porn Fetch and Porn Fetch will not be found anymore when someone enters &quot;Porn Fetch&quot; on your PC. This can be useful if multiple persons use your PC and you don't want them to know you are using this application. It can also help if you are in public and people stare at your PC. Porn Fetch has also an option to fully hide, that it's a PornHub downloader.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:12pt; color:#ffffff;\">If you leave it empty, Porn Fetch will remain as &quot;Porn "
                        "Fetch&quot; in your short menu.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Sans Serif'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:14pt; text-decoration: underline; color:#aa0000;\">NOTE:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Installation was implemented in this release and might still be experimental. If you run into any issues, please report it on my GitHub. Thank you :</span><span style=\" font-family:'Segoe UI'; font-size:9pt;\">) </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                        "text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.label_custom_app_name.setAccessibleName(QCoreApplication.translate("MainWindow", u"label custom app name", None))
#endif // QT_CONFIG(accessibility)
        self.label_custom_app_name.setText(QCoreApplication.translate("MainWindow", u"Custom App Name:", None))
#if QT_CONFIG(accessibility)
        self.lineedit_custom_app_name.setAccessibleName(QCoreApplication.translate("MainWindow", u"lineedit custom app name (enter the custom name here) ", None))
#endif // QT_CONFIG(accessibility)
        self.lineedit_custom_app_name.setText("")
        self.lineedit_custom_app_name.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter your custom App Name here. Leave it empty to keep \"Porn Fetch\"", None))
#if QT_CONFIG(accessibility)
        self.button_install.setAccessibleName(QCoreApplication.translate("MainWindow", u"buttom instal porn fetch", None))
#endif // QT_CONFIG(accessibility)
        self.button_install.setText(QCoreApplication.translate("MainWindow", u"Install", None))
#if QT_CONFIG(accessibility)
        self.button_portable.setAccessibleName(QCoreApplication.translate("MainWindow", u"button portable mode", None))
#endif // QT_CONFIG(accessibility)
        self.button_portable.setText(QCoreApplication.translate("MainWindow", u"Portable", None))
#if QT_CONFIG(accessibility)
        self.main_textbrowser_supported_websites.setAccessibleName(QCoreApplication.translate("MainWindow", u"textbrowser supported websites", None))
#endif // QT_CONFIG(accessibility)
        self.main_textbrowser_supported_websites.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\"><thead>\n"
"<tr>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt; font-weight:700;\">Category</span></p></td>\n"
"<td>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bloc"
                        "k-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt; font-weight:700;\">Websites</span></p></td></tr></thead>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Videos</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang, YouPorn</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Searching</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-inden"
                        "t:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">PornHub, HQporner, Eporner, xnxx, xvideos, missav, Xhamster, Spankbang</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Models</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">PornHub, HQporner, xnxx</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Pornstars</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwa"
                        "ita Sans'; font-size:11pt;\">PornHub, Eporner, xvideos, Xhamster, Spankbang</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Channels</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">PornHub, Xhamster, Spankbang</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Creator / Users</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Xhamster (Creator), Spa"
                        "nkbang (Creator), xnxx (Users)</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Playlists</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">PornHub, xvideos</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Downloading</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">xvideos</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; marg"
                        "in-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Shorts</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Xhamster</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Account Login</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">PornHub</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family"
                        ":'Adwaita Sans'; font-size:11pt;\">Videos by Category</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">HQporner, Eporner</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Random</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">HQporner</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Brazzers only</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top"
                        ":0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">HQporner</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">Top Porn</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Adwaita Sans'; font-size:11pt;\">HQporner</span></p></td></tr></table></body></html>", None))
#if QT_CONFIG(accessibility)
        self.textbrowser_disclaimer.setAccessibleName(QCoreApplication.translate("MainWindow", u"textbrowser disclaimer message", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.textbrowser_disclaimer.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.textbrowser_disclaimer.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">DISCLAIMER</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">Porn Fetch</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> is free software licensed un"
                        "der the GNU General Public License v3.0. You are free to use, modify, and redistribute this software under the terms of that license.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Please be aware that </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">Porn Fetch may interact with websites in ways that violate their Terms of Service.</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> Additionally, downloading copyright-protected content without proper authorization may be illegal in many jurisdictions, including under the DMCA (Digital Millennium Copyright Act).</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">While some countries or regions may allow downloading content for "
                        "strictly </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">personal, non-commercial use</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\">, I </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">strongly discourage</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> using Porn Fetch to download, share, or redistribute content without appropriate rights or permissions. Always ensure you comply with your local laws and the terms of any website you access.</span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">IMPORTANT NOTE</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">I </span><span style=\" font-family:'Sans Serif'; fon"
                        "t-size:9pt; font-weight:700;\">strongly recommend</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> that you do </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">not</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> use this software for:</span></p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" font-family:'Sans Serif'; font-size:9pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Unauthorized redistribution of content</li>\n"
"<li style=\" font-family:'Sans Serif'; font-size:9pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Commercial use of downloaded materials</li>\n"
"<li style=\" font-family:'Sans Serif'; font-size:9pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-i"
                        "ndent:0; text-indent:0px;\">Any activity that could result in legal liability for yourself or others</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt;\">Although the GPL license grants you broad rights, </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">continued misuse</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> may jeopardize the development and availability of this project. Please respect the intent behind this tool and use it responsibly.</span></p>\n"
"<h3 style=\" margin-top:14px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">LIABILITY DISCLAIMER</span></h3>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span sty"
                        "le=\" font-family:'Sans Serif'; font-size:9pt;\">This software is provided </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">without any warranty</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> as described in the GPLv3. I am </span><span style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:700;\">not liable</span><span style=\" font-family:'Sans Serif'; font-size:9pt;\"> for any damages, legal consequences, or misuse resulting from your use of this software.<br />You are solely responsible for ensuring your actions are lawful and ethical. </span></p></body></html>", None))
#if QT_CONFIG(accessibility)
        self.button_disclaimer_accept.setAccessibleName(QCoreApplication.translate("MainWindow", u"button accept disclaimer message", None))
#endif // QT_CONFIG(accessibility)
        self.button_disclaimer_accept.setText(QCoreApplication.translate("MainWindow", u"Accept", None))
        self.button_info_enable_all.setText(QCoreApplication.translate("MainWindow", u"Enable Update + Error reports (100% anonymous)", None))
        self.button_info_enable_update.setText(QCoreApplication.translate("MainWindow", u"Enable Update checking only", None))
        self.button_info_disable_all.setText(QCoreApplication.translate("MainWindow", u"Disable everything", None))
#if QT_CONFIG(accessibility)
        self.text_browser_update_available.setAccessibleName(QCoreApplication.translate("MainWindow", u"textbrowser update changelog notification", None))
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.button_update_acknowledged.setAccessibleName(QCoreApplication.translate("MainWindow", u"button acknowledge that a new version is out", None))
#endif // QT_CONFIG(accessibility)
        self.button_update_acknowledged.setText(QCoreApplication.translate("MainWindow", u"OK", None))
        self.main_label_progressbar_total.setText(QCoreApplication.translate("MainWindow", u"Total:", None))
        self.main_label_progressbar_converting.setText(QCoreApplication.translate("MainWindow", u"Converting:", None))
    # retranslateUi

