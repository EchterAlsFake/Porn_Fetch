# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_desktop.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QProgressBar, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QTextBrowser, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1098, 668)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Porn_Fetch_Widget.sizePolicy().hasHeightForWidth())
        Porn_Fetch_Widget.setSizePolicy(sizePolicy)
        Porn_Fetch_Widget.setMinimumSize(QSize(100, 50))
        self.gridLayout = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_gridlayout = QGridLayout()
        self.main_gridlayout.setSpacing(0)
        self.main_gridlayout.setObjectName(u"main_gridlayout")
        self.verticallayout_sidebar = QVBoxLayout()
        self.verticallayout_sidebar.setObjectName(u"verticallayout_sidebar")
        self.button_switch_home = QPushButton(Porn_Fetch_Widget)
        self.button_switch_home.setObjectName(u"button_switch_home")
        self.button_switch_home.setMinimumSize(QSize(50, 50))
        self.button_switch_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"border: none")
        self.button_switch_home.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_home)

        self.button_switch_account = QPushButton(Porn_Fetch_Widget)
        self.button_switch_account.setObjectName(u"button_switch_account")
        self.button_switch_account.setMinimumSize(QSize(50, 50))
        self.button_switch_account.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_account.setStyleSheet(u"border: none")
        self.button_switch_account.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_account)

        self.button_switch_hqporner = QPushButton(Porn_Fetch_Widget)
        self.button_switch_hqporner.setObjectName(u"button_switch_hqporner")
        self.button_switch_hqporner.setMinimumSize(QSize(50, 50))
        font = QFont()
        font.setPointSize(25)
        self.button_switch_hqporner.setFont(font)
        self.button_switch_hqporner.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_hqporner.setStyleSheet(u"border: none;\n"
"color: #ff8397")
        self.button_switch_hqporner.setIconSize(QSize(64, 64))

        self.verticallayout_sidebar.addWidget(self.button_switch_hqporner)

        self.button_switch_search = QPushButton(Porn_Fetch_Widget)
        self.button_switch_search.setObjectName(u"button_switch_search")
        self.button_switch_search.setMinimumSize(QSize(50, 50))
        self.button_switch_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_search.setStyleSheet(u"border: none;")
        self.button_switch_search.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_search)

        self.button_switch_settings = QPushButton(Porn_Fetch_Widget)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        self.button_switch_settings.setMinimumSize(QSize(50, 50))
        self.button_switch_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"border: none;")
        self.button_switch_settings.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_settings)

        self.button_switch_metadata = QPushButton(Porn_Fetch_Widget)
        self.button_switch_metadata.setObjectName(u"button_switch_metadata")
        self.button_switch_metadata.setMinimumSize(QSize(50, 50))
        self.button_switch_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_metadata.setStyleSheet(u"border: none;")
        self.button_switch_metadata.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_metadata)

        self.button_switch_credits = QPushButton(Porn_Fetch_Widget)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        self.button_switch_credits.setMinimumSize(QSize(50, 50))
        self.button_switch_credits.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"border: none;")
        self.button_switch_credits.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_credits)

        self.vertical_spacer_sidebar = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticallayout_sidebar.addItem(self.vertical_spacer_sidebar)


        self.main_gridlayout.addLayout(self.verticallayout_sidebar, 0, 0, 1, 1)

        self.main_widget = QWidget(Porn_Fetch_Widget)
        self.main_widget.setObjectName(u"main_widget")
        self.gridLayout_13 = QGridLayout(self.main_widget)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.stacked_widget_main = QStackedWidget(self.main_widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_8 = QGridLayout(self.page)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticallayout_treewidget = QVBoxLayout()
        self.verticallayout_treewidget.setObjectName(u"verticallayout_treewidget")
        self.scrollarea_treewidget = QScrollArea(self.page)
        self.scrollarea_treewidget.setObjectName(u"scrollarea_treewidget")
        self.scrollarea_treewidget.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 1004, 289))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticallayout_treewidget_settings = QVBoxLayout()
        self.verticallayout_treewidget_settings.setObjectName(u"verticallayout_treewidget_settings")
        self.horizontallayout_treewidget_settings = QHBoxLayout()
        self.horizontallayout_treewidget_settings.setObjectName(u"horizontallayout_treewidget_settings")
        self.radio_tree_show_title = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radio_tree_show_title.setObjectName(u"radio_tree_show_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.radio_tree_show_title.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_title.setSizePolicy(sizePolicy1)
        self.radio_tree_show_title.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_tree_show_title.setChecked(False)

        self.horizontallayout_treewidget_settings.addWidget(self.radio_tree_show_title)

        self.radio_tree_show_all = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radio_tree_show_all.setObjectName(u"radio_tree_show_all")
        sizePolicy1.setHeightForWidth(self.radio_tree_show_all.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_all.setSizePolicy(sizePolicy1)
        self.radio_tree_show_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_tree_show_all.setStyleSheet(u"")
        self.radio_tree_show_all.setChecked(True)

        self.horizontallayout_treewidget_settings.addWidget(self.radio_tree_show_all)

        self.checkbox_show_videos_reversed = QCheckBox(self.scrollAreaWidgetContents_3)
        self.checkbox_show_videos_reversed.setObjectName(u"checkbox_show_videos_reversed")
        self.checkbox_show_videos_reversed.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_treewidget_settings.addWidget(self.checkbox_show_videos_reversed)


        self.verticallayout_treewidget_settings.addLayout(self.horizontallayout_treewidget_settings)

        self.treeWidget = QTreeWidget(self.scrollAreaWidgetContents_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy2)
        self.treeWidget.setMinimumSize(QSize(100, 200))

        self.verticallayout_treewidget_settings.addWidget(self.treeWidget)


        self.gridLayout_4.addLayout(self.verticallayout_treewidget_settings, 0, 0, 1, 1)

        self.horizontallayout_treewidget_buttons = QHBoxLayout()
        self.horizontallayout_treewidget_buttons.setObjectName(u"horizontallayout_treewidget_buttons")
        self.button_tree_download = QPushButton(self.scrollAreaWidgetContents_3)
        self.button_tree_download.setObjectName(u"button_tree_download")
        self.button_tree_download.setCursor(QCursor(Qt.PointingHandCursor))
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

        self.horizontallayout_treewidget_buttons.addWidget(self.button_tree_download)

        self.button_tree_select_all = QPushButton(self.scrollAreaWidgetContents_3)
        self.button_tree_select_all.setObjectName(u"button_tree_select_all")
        self.button_tree_select_all.setCursor(QCursor(Qt.PointingHandCursor))
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

        self.horizontallayout_treewidget_buttons.addWidget(self.button_tree_select_all)

        self.button_tree_unselect_all = QPushButton(self.scrollAreaWidgetContents_3)
        self.button_tree_unselect_all.setObjectName(u"button_tree_unselect_all")
        self.button_tree_unselect_all.setCursor(QCursor(Qt.PointingHandCursor))
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

        self.horizontallayout_treewidget_buttons.addWidget(self.button_tree_unselect_all)


        self.gridLayout_4.addLayout(self.horizontallayout_treewidget_buttons, 1, 0, 1, 1)

        self.scrollarea_treewidget.setWidget(self.scrollAreaWidgetContents_3)

        self.verticallayout_treewidget.addWidget(self.scrollarea_treewidget)


        self.gridLayout_8.addLayout(self.verticallayout_treewidget, 1, 0, 1, 1)

        self.scrollarea_stacked_top = QScrollArea(self.page)
        self.scrollarea_stacked_top.setObjectName(u"scrollarea_stacked_top")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.scrollarea_stacked_top.sizePolicy().hasHeightForWidth())
        self.scrollarea_stacked_top.setSizePolicy(sizePolicy3)
        self.scrollarea_stacked_top.setWidgetResizable(True)
        self.scrollAreaWidgetContents_7 = QWidget()
        self.scrollAreaWidgetContents_7.setObjectName(u"scrollAreaWidgetContents_7")
        self.scrollAreaWidgetContents_7.setGeometry(QRect(0, 0, 1006, 197))
        self.gridLayout_14 = QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.stacked_widget_top = QStackedWidget(self.scrollAreaWidgetContents_7)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        sizePolicy2.setHeightForWidth(self.stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.stacked_widget_top.setSizePolicy(sizePolicy2)
        self.stacked_widget_top.setMinimumSize(QSize(600, 150))
        self.stacked_widget_top.setStyleSheet(u"b")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_5 = QGridLayout(self.page_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(0)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SetMaximumSize)
        self.label_url = QLabel(self.page_3)
        self.label_url.setObjectName(u"label_url")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy4)
        self.label_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_url, 0, 0, 1, 1)

        self.button_search_hqporner = QPushButton(self.page_3)
        self.button_search_hqporner.setObjectName(u"button_search_hqporner")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.button_search_hqporner.sizePolicy().hasHeightForWidth())
        self.button_search_hqporner.setSizePolicy(sizePolicy5)
        self.button_search_hqporner.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search_hqporner, 3, 2, 1, 1)

        self.lineedit_file = QLineEdit(self.page_3)
        self.lineedit_file.setObjectName(u"lineedit_file")
        sizePolicy6 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.lineedit_file.sizePolicy().hasHeightForWidth())
        self.lineedit_file.setSizePolicy(sizePolicy6)
        self.lineedit_file.setMinimumSize(QSize(300, 2))
        self.lineedit_file.setReadOnly(True)

        self.gridlayout_downloading.addWidget(self.lineedit_file, 2, 1, 1, 1)

        self.label_file = QLabel(self.page_3)
        self.label_file.setObjectName(u"label_file")
        sizePolicy4.setHeightForWidth(self.label_file.sizePolicy().hasHeightForWidth())
        self.label_file.setSizePolicy(sizePolicy4)
        self.label_file.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_file, 2, 0, 1, 1)

        self.lineedit_search_hqporner = QLineEdit(self.page_3)
        self.lineedit_search_hqporner.setObjectName(u"lineedit_search_hqporner")
        sizePolicy6.setHeightForWidth(self.lineedit_search_hqporner.sizePolicy().hasHeightForWidth())
        self.lineedit_search_hqporner.setSizePolicy(sizePolicy6)
        self.lineedit_search_hqporner.setMinimumSize(QSize(300, 0))

        self.gridlayout_downloading.addWidget(self.lineedit_search_hqporner, 3, 1, 1, 1)

        self.lineedit_url = QLineEdit(self.page_3)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy6.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy6)
        self.lineedit_url.setMinimumSize(QSize(300, 4))

        self.gridlayout_downloading.addWidget(self.lineedit_url, 0, 1, 1, 1)

        self.label_model_url = QLabel(self.page_3)
        self.label_model_url.setObjectName(u"label_model_url")
        sizePolicy4.setHeightForWidth(self.label_model_url.sizePolicy().hasHeightForWidth())
        self.label_model_url.setSizePolicy(sizePolicy4)
        self.label_model_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_model_url, 1, 0, 1, 1)

        self.button_model = QPushButton(self.page_3)
        self.button_model.setObjectName(u"button_model")
        sizePolicy5.setHeightForWidth(self.button_model.sizePolicy().hasHeightForWidth())
        self.button_model.setSizePolicy(sizePolicy5)
        self.button_model.setMinimumSize(QSize(60, 2))
        self.button_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_model.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_model, 1, 2, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page_3)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")
        sizePolicy6.setHeightForWidth(self.lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.lineedit_model_url.setSizePolicy(sizePolicy6)
        self.lineedit_model_url.setMinimumSize(QSize(300, 2))

        self.gridlayout_downloading.addWidget(self.lineedit_model_url, 1, 1, 1, 1)

        self.button_download = QPushButton(self.page_3)
        self.button_download.setObjectName(u"button_download")
        sizePolicy5.setHeightForWidth(self.button_download.sizePolicy().hasHeightForWidth())
        self.button_download.setSizePolicy(sizePolicy5)
        self.button_download.setMinimumSize(QSize(60, 2))
        self.button_download.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_download, 0, 2, 1, 1)

        self.button_open_file = QPushButton(self.page_3)
        self.button_open_file.setObjectName(u"button_open_file")
        sizePolicy5.setHeightForWidth(self.button_open_file.sizePolicy().hasHeightForWidth())
        self.button_open_file.setSizePolicy(sizePolicy5)
        self.button_open_file.setMinimumSize(QSize(60, 2))
        self.button_open_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_open_file.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_open_file, 2, 2, 1, 1)

        self.label_search_query_hqporner = QLabel(self.page_3)
        self.label_search_query_hqporner.setObjectName(u"label_search_query_hqporner")

        self.gridlayout_downloading.addWidget(self.label_search_query_hqporner, 3, 0, 1, 1)

        self.label_search_query_pornhub = QLabel(self.page_3)
        self.label_search_query_pornhub.setObjectName(u"label_search_query_pornhub")

        self.gridlayout_downloading.addWidget(self.label_search_query_pornhub, 4, 0, 1, 1)

        self.lineedit_seach_pornhub = QLineEdit(self.page_3)
        self.lineedit_seach_pornhub.setObjectName(u"lineedit_seach_pornhub")
        sizePolicy6.setHeightForWidth(self.lineedit_seach_pornhub.sizePolicy().hasHeightForWidth())
        self.lineedit_seach_pornhub.setSizePolicy(sizePolicy6)
        self.lineedit_seach_pornhub.setMinimumSize(QSize(300, 0))

        self.gridlayout_downloading.addWidget(self.lineedit_seach_pornhub, 4, 1, 1, 1)

        self.button_search_pornhub = QPushButton(self.page_3)
        self.button_search_pornhub.setObjectName(u"button_search_pornhub")
        sizePolicy5.setHeightForWidth(self.button_search_pornhub.sizePolicy().hasHeightForWidth())
        self.button_search_pornhub.setSizePolicy(sizePolicy5)
        self.button_search_pornhub.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search_pornhub, 4, 2, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_downloading, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_3)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_2 = QGridLayout(self.page_5)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridlayout_login_box = QGridLayout()
        self.gridlayout_login_box.setSpacing(0)
        self.gridlayout_login_box.setObjectName(u"gridlayout_login_box")
        self.lineedit_username = QLineEdit(self.page_5)
        self.lineedit_username.setObjectName(u"lineedit_username")
        sizePolicy6.setHeightForWidth(self.lineedit_username.sizePolicy().hasHeightForWidth())
        self.lineedit_username.setSizePolicy(sizePolicy6)
        self.lineedit_username.setMinimumSize(QSize(150, 0))

        self.gridlayout_login_box.addWidget(self.lineedit_username, 0, 1, 1, 3)

        self.button_get_liked_videos = QPushButton(self.page_5)
        self.button_get_liked_videos.setObjectName(u"button_get_liked_videos")
        self.button_get_liked_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_liked_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_liked_videos, 3, 0, 1, 1)

        self.button_get_watched_videos = QPushButton(self.page_5)
        self.button_get_watched_videos.setObjectName(u"button_get_watched_videos")
        self.button_get_watched_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_watched_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_watched_videos, 3, 1, 1, 1)

        self.label_password = QLabel(self.page_5)
        self.label_password.setObjectName(u"label_password")
        sizePolicy1.setHeightForWidth(self.label_password.sizePolicy().hasHeightForWidth())
        self.label_password.setSizePolicy(sizePolicy1)

        self.gridlayout_login_box.addWidget(self.label_password, 1, 0, 1, 1)

        self.button_login = QPushButton(self.page_5)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setMinimumSize(QSize(0, 0))
        self.button_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_login.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_login, 2, 0, 1, 4)

        self.label_username = QLabel(self.page_5)
        self.label_username.setObjectName(u"label_username")
        sizePolicy1.setHeightForWidth(self.label_username.sizePolicy().hasHeightForWidth())
        self.label_username.setSizePolicy(sizePolicy1)

        self.gridlayout_login_box.addWidget(self.label_username, 0, 0, 1, 1)

        self.lineedit_password = QLineEdit(self.page_5)
        self.lineedit_password.setObjectName(u"lineedit_password")
        sizePolicy6.setHeightForWidth(self.lineedit_password.sizePolicy().hasHeightForWidth())
        self.lineedit_password.setSizePolicy(sizePolicy6)
        self.lineedit_password.setMinimumSize(QSize(150, 0))
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.gridlayout_login_box.addWidget(self.lineedit_password, 1, 1, 1, 3)

        self.button_get_recommended_videos = QPushButton(self.page_5)
        self.button_get_recommended_videos.setObjectName(u"button_get_recommended_videos")
        self.button_get_recommended_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_recommended_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_recommended_videos, 3, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridlayout_login_box, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_5)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_6 = QGridLayout(self.page_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stacked_widget_top.addWidget(self.page_4)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.gridLayout_29 = QGridLayout(self.page_6)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.gridlayout_hqporner = QGridLayout()
        self.gridlayout_hqporner.setObjectName(u"gridlayout_hqporner")
        self.horizontallayout_category = QHBoxLayout()
        self.horizontallayout_category.setObjectName(u"horizontallayout_category")
        self.label_videos_by_category = QLabel(self.page_6)
        self.label_videos_by_category.setObjectName(u"label_videos_by_category")
        self.label_videos_by_category.setMinimumSize(QSize(0, 4))

        self.horizontallayout_category.addWidget(self.label_videos_by_category)

        self.lineedit_hqporner_category = QLineEdit(self.page_6)
        self.lineedit_hqporner_category.setObjectName(u"lineedit_hqporner_category")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(4)
        sizePolicy7.setHeightForWidth(self.lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.lineedit_hqporner_category.setSizePolicy(sizePolicy7)
        self.lineedit_hqporner_category.setMinimumSize(QSize(100, 4))

        self.horizontallayout_category.addWidget(self.lineedit_hqporner_category)

        self.button_hqporner_category_get_videos = QPushButton(self.page_6)
        self.button_hqporner_category_get_videos.setObjectName(u"button_hqporner_category_get_videos")
        sizePolicy5.setHeightForWidth(self.button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.button_hqporner_category_get_videos.setSizePolicy(sizePolicy5)
        self.button_hqporner_category_get_videos.setMinimumSize(QSize(0, 10))
        self.button_hqporner_category_get_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_category.addWidget(self.button_hqporner_category_get_videos)

        self.button_list_categories = QPushButton(self.page_6)
        self.button_list_categories.setObjectName(u"button_list_categories")
        sizePolicy5.setHeightForWidth(self.button_list_categories.sizePolicy().hasHeightForWidth())
        self.button_list_categories.setSizePolicy(sizePolicy5)
        self.button_list_categories.setMinimumSize(QSize(0, 10))
        self.button_list_categories.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_category.addWidget(self.button_list_categories)

        self.horizontalspacer_categories = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontallayout_category.addItem(self.horizontalspacer_categories)


        self.gridlayout_hqporner.addLayout(self.horizontallayout_category, 1, 0, 1, 1)

        self.horizontallayout_top = QHBoxLayout()
        self.horizontallayout_top.setObjectName(u"horizontallayout_top")
        self.label_get_top_porn = QLabel(self.page_6)
        self.label_get_top_porn.setObjectName(u"label_get_top_porn")

        self.horizontallayout_top.addWidget(self.label_get_top_porn)

        self.radio_top_porn_week = QRadioButton(self.page_6)
        self.radio_top_porn_week.setObjectName(u"radio_top_porn_week")
        self.radio_top_porn_week.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_week.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_top_porn_week.setChecked(True)

        self.horizontallayout_top.addWidget(self.radio_top_porn_week)

        self.radio_top_porn_month = QRadioButton(self.page_6)
        self.radio_top_porn_month.setObjectName(u"radio_top_porn_month")
        self.radio_top_porn_month.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_month.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_top.addWidget(self.radio_top_porn_month)

        self.radio_top_porn_all_time = QRadioButton(self.page_6)
        self.radio_top_porn_all_time.setObjectName(u"radio_top_porn_all_time")
        self.radio_top_porn_all_time.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_all_time.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_top.addWidget(self.radio_top_porn_all_time)

        self.button_top_porn_get_videos = QPushButton(self.page_6)
        self.button_top_porn_get_videos.setObjectName(u"button_top_porn_get_videos")
        self.button_top_porn_get_videos.setMinimumSize(QSize(0, 10))
        self.button_top_porn_get_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_top.addWidget(self.button_top_porn_get_videos)

        self.horizontalspacer_top_porn = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontallayout_top.addItem(self.horizontalspacer_top_porn)


        self.gridlayout_hqporner.addLayout(self.horizontallayout_top, 0, 0, 1, 1)

        self.horizontallayout_pages = QHBoxLayout()
        self.horizontallayout_pages.setObjectName(u"horizontallayout_pages")
        self.label_pages = QLabel(self.page_6)
        self.label_pages.setObjectName(u"label_pages")

        self.horizontallayout_pages.addWidget(self.label_pages)

        self.spinbox_pages = QSpinBox(self.page_6)
        self.spinbox_pages.setObjectName(u"spinbox_pages")
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.spinbox_pages.sizePolicy().hasHeightForWidth())
        self.spinbox_pages.setSizePolicy(sizePolicy8)
        self.spinbox_pages.setMinimumSize(QSize(0, 4))
        self.spinbox_pages.setValue(2)

        self.horizontallayout_pages.addWidget(self.spinbox_pages)

        self.button_help_pages = QPushButton(self.page_6)
        self.button_help_pages.setObjectName(u"button_help_pages")
        sizePolicy8.setHeightForWidth(self.button_help_pages.sizePolicy().hasHeightForWidth())
        self.button_help_pages.setSizePolicy(sizePolicy8)
        self.button_help_pages.setMinimumSize(QSize(0, 4))
        self.button_help_pages.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_pages.addWidget(self.button_help_pages)

        self.horizontalspacer_pages = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontallayout_pages.addItem(self.horizontalspacer_pages)


        self.gridlayout_hqporner.addLayout(self.horizontallayout_pages, 3, 0, 1, 1)

        self.horizontallayout_brazzers_random = QHBoxLayout()
        self.horizontallayout_brazzers_random.setSpacing(0)
        self.horizontallayout_brazzers_random.setObjectName(u"horizontallayout_brazzers_random")
        self.horizontallayout_brazzers_random.setContentsMargins(-1, 0, -1, -1)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labe_get_random_video = QLabel(self.page_6)
        self.labe_get_random_video.setObjectName(u"labe_get_random_video")
        self.labe_get_random_video.setMinimumSize(QSize(0, 4))

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labe_get_random_video)

        self.button_get_random_videos = QPushButton(self.page_6)
        self.button_get_random_videos.setObjectName(u"button_get_random_videos")
        sizePolicy9 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.button_get_random_videos.setSizePolicy(sizePolicy9)
        self.button_get_random_videos.setMinimumSize(QSize(0, 10))
        self.button_get_random_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.button_get_random_videos)

        self.label_get_brazzers_videos = QLabel(self.page_6)
        self.label_get_brazzers_videos.setObjectName(u"label_get_brazzers_videos")
        self.label_get_brazzers_videos.setMinimumSize(QSize(0, 4))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_get_brazzers_videos)

        self.button_get_brazzers_videos = QPushButton(self.page_6)
        self.button_get_brazzers_videos.setObjectName(u"button_get_brazzers_videos")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.button_get_brazzers_videos.setSizePolicy(sizePolicy10)
        self.button_get_brazzers_videos.setMinimumSize(QSize(0, 10))
        self.button_get_brazzers_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.button_get_brazzers_videos)


        self.horizontallayout_brazzers_random.addLayout(self.formLayout)


        self.gridlayout_hqporner.addLayout(self.horizontallayout_brazzers_random, 2, 0, 1, 1)


        self.gridLayout_29.addLayout(self.gridlayout_hqporner, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_6)

        self.gridLayout_14.addWidget(self.stacked_widget_top, 0, 0, 1, 1)

        self.scrollarea_stacked_top.setWidget(self.scrollAreaWidgetContents_7)

        self.gridLayout_8.addWidget(self.scrollarea_stacked_top, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_25 = QGridLayout(self.page_2)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.scrollarea_settings = QScrollArea(self.page_2)
        self.scrollarea_settings.setObjectName(u"scrollarea_settings")
        self.scrollarea_settings.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 680, 444))
        self.gridLayout_34 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.gridlayout_settings = QGridLayout()
        self.gridlayout_settings.setObjectName(u"gridlayout_settings")
        self.gridlayout_threading_mode = QGridLayout()
        self.gridlayout_threading_mode.setObjectName(u"gridlayout_threading_mode")
        self.label_threading_mode = QLabel(self.scrollAreaWidgetContents_6)
        self.label_threading_mode.setObjectName(u"label_threading_mode")
        sizePolicy1.setHeightForWidth(self.label_threading_mode.sizePolicy().hasHeightForWidth())
        self.label_threading_mode.setSizePolicy(sizePolicy1)

        self.gridlayout_threading_mode.addWidget(self.label_threading_mode, 0, 0, 1, 1)

        self.radio_threading_mode_ffmpeg = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_threading_mode_ffmpeg.setObjectName(u"radio_threading_mode_ffmpeg")
        self.radio_threading_mode_ffmpeg.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_threading_mode.addWidget(self.radio_threading_mode_ffmpeg, 0, 2, 1, 1)

        self.radio_threading_mode_high_performance = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_threading_mode_high_performance.setObjectName(u"radio_threading_mode_high_performance")
        self.radio_threading_mode_high_performance.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_threading_mode.addWidget(self.radio_threading_mode_high_performance, 0, 1, 1, 1)

        self.radio_threading_mode_default = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_threading_mode_default.setObjectName(u"radio_threading_mode_default")
        self.radio_threading_mode_default.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_threading_mode.addWidget(self.radio_threading_mode_default, 0, 3, 1, 1)

        self.button_threading_mode_help = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_threading_mode_help.setObjectName(u"button_threading_mode_help")
        self.button_threading_mode_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_threading_mode.addWidget(self.button_threading_mode_help, 0, 4, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_threading_mode.addItem(self.horizontalSpacer_7, 0, 5, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_threading_mode, 2, 0, 1, 1)

        self.gridlayout_semaphore = QGridLayout()
        self.gridlayout_semaphore.setObjectName(u"gridlayout_semaphore")
        self.label_semaphore = QLabel(self.scrollAreaWidgetContents_6)
        self.label_semaphore.setObjectName(u"label_semaphore")

        self.gridlayout_semaphore.addWidget(self.label_semaphore, 0, 0, 1, 1)

        self.spinbox_semaphore = QSpinBox(self.scrollAreaWidgetContents_6)
        self.spinbox_semaphore.setObjectName(u"spinbox_semaphore")
        self.spinbox_semaphore.setMinimum(1)
        self.spinbox_semaphore.setMaximum(10)

        self.gridlayout_semaphore.addWidget(self.spinbox_semaphore, 0, 1, 1, 1)

        self.button_semaphore_help = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_semaphore_help.setObjectName(u"button_semaphore_help")
        self.button_semaphore_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_semaphore.addWidget(self.button_semaphore_help, 1, 0, 1, 2)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_semaphore.addItem(self.horizontalSpacer_8, 0, 2, 1, 1)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_semaphore.addItem(self.horizontalSpacer_16, 1, 2, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_semaphore, 1, 0, 1, 1)

        self.gridlayout_quality = QGridLayout()
        self.gridlayout_quality.setObjectName(u"gridlayout_quality")
        self.radio_quality_worst = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_quality_worst.setObjectName(u"radio_quality_worst")
        self.radio_quality_worst.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_quality.addWidget(self.radio_quality_worst, 0, 3, 1, 1)

        self.label_quality = QLabel(self.scrollAreaWidgetContents_6)
        self.label_quality.setObjectName(u"label_quality")
        sizePolicy1.setHeightForWidth(self.label_quality.sizePolicy().hasHeightForWidth())
        self.label_quality.setSizePolicy(sizePolicy1)

        self.gridlayout_quality.addWidget(self.label_quality, 0, 0, 1, 1)

        self.radio_quality_best = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_quality_best.setObjectName(u"radio_quality_best")
        self.radio_quality_best.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_quality.addWidget(self.radio_quality_best, 0, 1, 1, 1)

        self.radio_quality_half = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_quality_half.setObjectName(u"radio_quality_half")
        self.radio_quality_half.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_quality.addWidget(self.radio_quality_half, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_quality.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_quality, 3, 0, 1, 1)

        self.gridlayout_threading = QGridLayout()
        self.gridlayout_threading.setObjectName(u"gridlayout_threading")
        self.label_threading = QLabel(self.scrollAreaWidgetContents_6)
        self.label_threading.setObjectName(u"label_threading")
        sizePolicy1.setHeightForWidth(self.label_threading.sizePolicy().hasHeightForWidth())
        self.label_threading.setSizePolicy(sizePolicy1)

        self.gridlayout_threading.addWidget(self.label_threading, 0, 0, 1, 1)

        self.radio_threading_no = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_threading_no.setObjectName(u"radio_threading_no")
        self.radio_threading_no.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_threading.addWidget(self.radio_threading_no, 0, 2, 1, 1)

        self.radio_threading_yes = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_threading_yes.setObjectName(u"radio_threading_yes")
        self.radio_threading_yes.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_threading.addWidget(self.radio_threading_yes, 0, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_threading.addItem(self.horizontalSpacer_9, 0, 3, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_threading, 0, 0, 1, 1)

        self.gridlayout_gui_settings = QGridLayout()
        self.gridlayout_gui_settings.setObjectName(u"gridlayout_gui_settings")
        self.radio_ui_language_french = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_ui_language_french.setObjectName(u"radio_ui_language_french")
        self.radio_ui_language_french.setEnabled(False)

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_french, 0, 5, 1, 1)

        self.radio_ui_language_german = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_ui_language_german.setObjectName(u"radio_ui_language_german")
        self.radio_ui_language_german.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_german, 0, 3, 1, 1)

        self.radio_ui_language_english = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_ui_language_english.setObjectName(u"radio_ui_language_english")
        self.radio_ui_language_english.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_english, 0, 2, 1, 1)

        self.label_ui_language = QLabel(self.scrollAreaWidgetContents_6)
        self.label_ui_language.setObjectName(u"label_ui_language")
        sizePolicy1.setHeightForWidth(self.label_ui_language.sizePolicy().hasHeightForWidth())
        self.label_ui_language.setSizePolicy(sizePolicy1)

        self.gridlayout_gui_settings.addWidget(self.label_ui_language, 0, 0, 1, 1)

        self.radio_ui_language_system_default = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_ui_language_system_default.setObjectName(u"radio_ui_language_system_default")
        self.radio_ui_language_system_default.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_system_default, 0, 1, 1, 1)

        self.radio_ui_language_chinese_simplified = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_ui_language_chinese_simplified.setObjectName(u"radio_ui_language_chinese_simplified")
        self.radio_ui_language_chinese_simplified.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_chinese_simplified, 0, 4, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_gui_settings.addItem(self.horizontalSpacer_11, 0, 6, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_gui_settings, 6, 0, 1, 1)

        self.gridlayout_api_language = QGridLayout()
        self.gridlayout_api_language.setObjectName(u"gridlayout_api_language")
        self.radio_api_language_russian = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_api_language_russian.setObjectName(u"radio_api_language_russian")
        self.radio_api_language_russian.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_russian, 2, 1, 1, 1)

        self.radio_api_language_custom = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_api_language_custom.setObjectName(u"radio_api_language_custom")
        self.radio_api_language_custom.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_custom, 3, 1, 1, 1)

        self.radio_api_language_english = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_api_language_english.setObjectName(u"radio_api_language_english")
        self.radio_api_language_english.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_english, 1, 0, 1, 1)

        self.radio_api_language_german = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_api_language_german.setObjectName(u"radio_api_language_german")
        self.radio_api_language_german.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_german, 2, 0, 1, 1)

        self.radio_api_language_french = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_api_language_french.setObjectName(u"radio_api_language_french")
        self.radio_api_language_french.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_french, 3, 0, 1, 1)

        self.radio_api_language_chinese = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_api_language_chinese.setObjectName(u"radio_api_language_chinese")
        self.radio_api_language_chinese.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_chinese, 1, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_api_language.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.label_api_language = QLabel(self.scrollAreaWidgetContents_6)
        self.label_api_language.setObjectName(u"label_api_language")
        sizePolicy1.setHeightForWidth(self.label_api_language.sizePolicy().hasHeightForWidth())
        self.label_api_language.setSizePolicy(sizePolicy1)

        self.gridlayout_api_language.addWidget(self.label_api_language, 0, 0, 1, 3)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_api_language.addItem(self.horizontalSpacer_12, 3, 2, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_api_language.addItem(self.horizontalSpacer_13, 2, 2, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_api_language, 4, 0, 1, 1)

        self.gridlayout_output_limit = QGridLayout()
        self.gridlayout_output_limit.setObjectName(u"gridlayout_output_limit")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_output_limit.addItem(self.horizontalSpacer_14, 1, 4, 1, 1)

        self.spinbox_treewidget_limit = QSpinBox(self.scrollAreaWidgetContents_6)
        self.spinbox_treewidget_limit.setObjectName(u"spinbox_treewidget_limit")
        self.spinbox_treewidget_limit.setMinimum(1)
        self.spinbox_treewidget_limit.setMaximum(200)

        self.gridlayout_output_limit.addWidget(self.spinbox_treewidget_limit, 2, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_output_limit.addItem(self.horizontalSpacer_10, 0, 4, 1, 1)

        self.lineedit_output_path = QLineEdit(self.scrollAreaWidgetContents_6)
        self.lineedit_output_path.setObjectName(u"lineedit_output_path")

        self.gridlayout_output_limit.addWidget(self.lineedit_output_path, 0, 1, 1, 2)

        self.label_output_path = QLabel(self.scrollAreaWidgetContents_6)
        self.label_output_path.setObjectName(u"label_output_path")

        self.gridlayout_output_limit.addWidget(self.label_output_path, 0, 0, 1, 1)

        self.button_directory_system_help = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_directory_system_help.setObjectName(u"button_directory_system_help")
        self.button_directory_system_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_output_limit.addWidget(self.button_directory_system_help, 1, 3, 1, 1)

        self.label_directory_system = QLabel(self.scrollAreaWidgetContents_6)
        self.label_directory_system.setObjectName(u"label_directory_system")

        self.gridlayout_output_limit.addWidget(self.label_directory_system, 1, 0, 1, 1)

        self.button_output_path_select = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_output_path_select.setObjectName(u"button_output_path_select")
        self.button_output_path_select.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_output_limit.addWidget(self.button_output_path_select, 0, 3, 1, 1)

        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.label_searching_limit = QLabel(self.scrollAreaWidgetContents_6)
        self.label_searching_limit.setObjectName(u"label_searching_limit")

        self.gridLayout_21.addWidget(self.label_searching_limit, 0, 0, 1, 1)


        self.gridlayout_output_limit.addLayout(self.gridLayout_21, 2, 0, 1, 1)

        self.radio_directory_system_yes = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_directory_system_yes.setObjectName(u"radio_directory_system_yes")
        self.radio_directory_system_yes.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_output_limit.addWidget(self.radio_directory_system_yes, 1, 1, 1, 1)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_output_limit.addItem(self.horizontalSpacer_15, 2, 2, 1, 3)

        self.radio_directory_system_no = QRadioButton(self.scrollAreaWidgetContents_6)
        self.radio_directory_system_no.setObjectName(u"radio_directory_system_no")
        self.radio_directory_system_no.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_output_limit.addWidget(self.radio_directory_system_no, 1, 2, 1, 1)


        self.gridlayout_settings.addLayout(self.gridlayout_output_limit, 5, 0, 1, 1)

        self.button_settings_apply = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_settings_apply.setObjectName(u"button_settings_apply")
        self.button_settings_apply.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_settings.addWidget(self.button_settings_apply, 7, 0, 1, 1)


        self.gridLayout_34.addLayout(self.gridlayout_settings, 0, 0, 1, 1)

        self.scrollarea_settings.setWidget(self.scrollAreaWidgetContents_6)

        self.gridLayout_25.addWidget(self.scrollarea_settings, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_2)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_26 = QGridLayout(self.page_7)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridlayout_textbrowser = QGridLayout()
        self.gridlayout_textbrowser.setObjectName(u"gridlayout_textbrowser")
        self.textBrowser = QTextBrowser(self.page_7)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridlayout_textbrowser.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout_26.addLayout(self.gridlayout_textbrowser, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_7)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout_32 = QGridLayout(self.page_8)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.verticallayout_metadata = QVBoxLayout()
        self.verticallayout_metadata.setObjectName(u"verticallayout_metadata")
        self.scrollarea_metadata = QScrollArea(self.page_8)
        self.scrollarea_metadata.setObjectName(u"scrollarea_metadata")
        self.scrollarea_metadata.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 234, 1080))
        self.gridLayout_27 = QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.gridlayout_metadata_ = QGridLayout()
        self.gridlayout_metadata_.setObjectName(u"gridlayout_metadata_")
        self.lineedit_metadata_video_url = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_metadata_video_url.setObjectName(u"lineedit_metadata_video_url")

        self.gridlayout_metadata_.addWidget(self.lineedit_metadata_video_url, 0, 1, 1, 1)

        self.lineedit_metadata_user_url = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_metadata_user_url.setObjectName(u"lineedit_metadata_user_url")

        self.gridlayout_metadata_.addWidget(self.lineedit_metadata_user_url, 1, 1, 1, 1)

        self.button_metadata_video_start = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_metadata_video_start.setObjectName(u"button_metadata_video_start")
        self.button_metadata_video_start.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_metadata_video_start.setStyleSheet(u"")

        self.gridlayout_metadata_.addWidget(self.button_metadata_video_start, 0, 2, 1, 1)

        self.label_metadata_video_url = QLabel(self.scrollAreaWidgetContents_4)
        self.label_metadata_video_url.setObjectName(u"label_metadata_video_url")

        self.gridlayout_metadata_.addWidget(self.label_metadata_video_url, 0, 0, 1, 1)

        self.button_metadata_user_start = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_metadata_user_start.setObjectName(u"button_metadata_user_start")
        self.button_metadata_user_start.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_metadata_user_start.setStyleSheet(u"")

        self.gridlayout_metadata_.addWidget(self.button_metadata_user_start, 1, 2, 1, 1)

        self.label_metadata_user_url = QLabel(self.scrollAreaWidgetContents_4)
        self.label_metadata_user_url.setObjectName(u"label_metadata_user_url")

        self.gridlayout_metadata_.addWidget(self.label_metadata_user_url, 1, 0, 1, 1)

        self.gridlayout_user_metadata = QGridLayout()
        self.gridlayout_user_metadata.setObjectName(u"gridlayout_user_metadata")
        self.lineedit_user_interests_hobbies = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_interests_hobbies.setObjectName(u"lineedit_user_interests_hobbies")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_interests_hobbies, 18, 1, 1, 1)

        self.lineedit_user_birth_place = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_birth_place.setObjectName(u"lineedit_user_birth_place")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_birth_place, 20, 1, 1, 1)

        self.label_height = QLabel(self.scrollAreaWidgetContents_4)
        self.label_height.setObjectName(u"label_height")

        self.gridlayout_user_metadata.addWidget(self.label_height, 7, 0, 1, 1)

        self.label_birth_place = QLabel(self.scrollAreaWidgetContents_4)
        self.label_birth_place.setObjectName(u"label_birth_place")

        self.gridlayout_user_metadata.addWidget(self.label_birth_place, 20, 0, 1, 1)

        self.label_turn_ons = QLabel(self.scrollAreaWidgetContents_4)
        self.label_turn_ons.setObjectName(u"label_turn_ons")

        self.gridlayout_user_metadata.addWidget(self.label_turn_ons, 5, 0, 1, 1)

        self.label_interests_hobbies = QLabel(self.scrollAreaWidgetContents_4)
        self.label_interests_hobbies.setObjectName(u"label_interests_hobbies")

        self.gridlayout_user_metadata.addWidget(self.label_interests_hobbies, 18, 0, 1, 1)

        self.lineedit_user_video_views = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_video_views.setObjectName(u"lineedit_user_video_views")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_video_views, 10, 1, 1, 1)

        self.label_piercings = QLabel(self.scrollAreaWidgetContents_4)
        self.label_piercings.setObjectName(u"label_piercings")

        self.gridlayout_user_metadata.addWidget(self.label_piercings, 1, 0, 1, 1)

        self.lineedit_user_tattoos = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_tattoos.setObjectName(u"lineedit_user_tattoos")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_tattoos, 22, 1, 1, 1)

        self.label_ethnicity = QLabel(self.scrollAreaWidgetContents_4)
        self.label_ethnicity.setObjectName(u"label_ethnicity")

        self.gridlayout_user_metadata.addWidget(self.label_ethnicity, 14, 0, 1, 1)

        self.lineedit_user_turn_ons = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_turn_ons.setObjectName(u"lineedit_user_turn_ons")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_turn_ons, 5, 1, 1, 1)

        self.lineedit_user_fake_boobs = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_fake_boobs.setObjectName(u"lineedit_user_fake_boobs")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_fake_boobs, 3, 1, 1, 1)

        self.lineedit_user_profile_views = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_profile_views.setObjectName(u"lineedit_user_profile_views")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_profile_views, 15, 1, 1, 1)

        self.lineedit_user_gender = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_gender.setObjectName(u"lineedit_user_gender")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_gender, 4, 1, 1, 1)

        self.lineedit_user_ethnicity = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_ethnicity.setObjectName(u"lineedit_user_ethnicity")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_ethnicity, 14, 1, 1, 1)

        self.lineedit_user_interested_in = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_interested_in.setObjectName(u"lineedit_user_interested_in")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_interested_in, 2, 1, 1, 1)

        self.lineedit_user_videos_watched = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_videos_watched.setObjectName(u"lineedit_user_videos_watched")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_videos_watched, 16, 1, 1, 1)

        self.label_turn_offs = QLabel(self.scrollAreaWidgetContents_4)
        self.label_turn_offs.setObjectName(u"label_turn_offs")

        self.gridlayout_user_metadata.addWidget(self.label_turn_offs, 8, 0, 1, 1)

        self.label_videos_watched = QLabel(self.scrollAreaWidgetContents_4)
        self.label_videos_watched.setObjectName(u"label_videos_watched")

        self.gridlayout_user_metadata.addWidget(self.label_videos_watched, 16, 0, 1, 1)

        self.label_fake_boobs = QLabel(self.scrollAreaWidgetContents_4)
        self.label_fake_boobs.setObjectName(u"label_fake_boobs")

        self.gridlayout_user_metadata.addWidget(self.label_fake_boobs, 3, 0, 1, 1)

        self.label_interested_in = QLabel(self.scrollAreaWidgetContents_4)
        self.label_interested_in.setObjectName(u"label_interested_in")

        self.gridlayout_user_metadata.addWidget(self.label_interested_in, 2, 0, 1, 1)

        self.label_gender = QLabel(self.scrollAreaWidgetContents_4)
        self.label_gender.setObjectName(u"label_gender")

        self.gridlayout_user_metadata.addWidget(self.label_gender, 4, 0, 1, 1)

        self.gridlayout_vieo_metadata = QGridLayout()
        self.gridlayout_vieo_metadata.setObjectName(u"gridlayout_vieo_metadata")
        self.lineedit_user_name = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_name.setObjectName(u"lineedit_user_name")

        self.gridlayout_vieo_metadata.addWidget(self.lineedit_user_name, 1, 1, 1, 1)

        self.label_user_type = QLabel(self.scrollAreaWidgetContents_4)
        self.label_user_type.setObjectName(u"label_user_type")

        self.gridlayout_vieo_metadata.addWidget(self.label_user_type, 2, 0, 1, 1)

        self.label_name = QLabel(self.scrollAreaWidgetContents_4)
        self.label_name.setObjectName(u"label_name")

        self.gridlayout_vieo_metadata.addWidget(self.label_name, 1, 0, 1, 1)

        self.lineedit_user_type = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_type.setObjectName(u"lineedit_user_type")

        self.gridlayout_vieo_metadata.addWidget(self.lineedit_user_type, 2, 1, 1, 1)

        self.girdlayout_pure_video_metadata = QGridLayout()
        self.girdlayout_pure_video_metadata.setObjectName(u"girdlayout_pure_video_metadata")
        self.label_video_title = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_title.setObjectName(u"label_video_title")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_title, 0, 0, 1, 1)

        self.label_video_tags = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_tags.setObjectName(u"label_video_tags")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_tags, 3, 0, 1, 1)

        self.lineedit_video_title = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_title.setObjectName(u"lineedit_video_title")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_title, 0, 1, 1, 1)

        self.lineedit_video_views = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_views.setObjectName(u"lineedit_video_views")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_views, 2, 1, 1, 1)

        self.label_video_rating = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_rating.setObjectName(u"label_video_rating")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_rating, 5, 0, 1, 1)

        self.label_video_duration = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_duration.setObjectName(u"label_video_duration")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_duration, 4, 0, 1, 1)

        self.lineedit_video_tags = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_tags.setObjectName(u"lineedit_video_tags")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_tags, 3, 1, 1, 1)

        self.label_video_views_2 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_views_2.setObjectName(u"label_video_views_2")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_views_2, 2, 0, 1, 1)

        self.lineedit_video_hotspots = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_hotspots.setObjectName(u"lineedit_video_hotspots")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_hotspots, 1, 1, 1, 1)

        self.lineedit_video_duration = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_duration.setObjectName(u"lineedit_video_duration")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_duration, 4, 1, 1, 1)

        self.label_video_pornstars = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_pornstars.setObjectName(u"label_video_pornstars")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_pornstars, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.girdlayout_pure_video_metadata.addItem(self.verticalSpacer_3, 9, 0, 1, 1)

        self.lineedit_video_rating = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_rating.setObjectName(u"lineedit_video_rating")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_rating, 5, 1, 1, 1)

        self.label_video_hotspots = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_hotspots.setObjectName(u"label_video_hotspots")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_hotspots, 1, 0, 1, 1)

        self.lineedit_video_pornstars = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_pornstars.setObjectName(u"lineedit_video_pornstars")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_pornstars, 6, 1, 1, 1)

        self.label_video_orientation = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_orientation.setObjectName(u"label_video_orientation")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_orientation, 7, 0, 1, 1)

        self.lineedit_video_orientation = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_orientation.setObjectName(u"lineedit_video_orientation")

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_orientation, 7, 1, 1, 1)


        self.gridlayout_vieo_metadata.addLayout(self.girdlayout_pure_video_metadata, 6, 0, 1, 2)


        self.gridlayout_user_metadata.addLayout(self.gridlayout_vieo_metadata, 23, 0, 1, 4)

        self.label_widght = QLabel(self.scrollAreaWidgetContents_4)
        self.label_widght.setObjectName(u"label_widght")

        self.gridlayout_user_metadata.addWidget(self.label_widght, 9, 0, 1, 1)

        self.lineedit_user_relationship = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_relationship.setObjectName(u"lineedit_user_relationship")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_relationship, 0, 1, 1, 1)

        self.label_relationship = QLabel(self.scrollAreaWidgetContents_4)
        self.label_relationship.setObjectName(u"label_relationship")

        self.gridlayout_user_metadata.addWidget(self.label_relationship, 0, 0, 1, 1)

        self.lineedit_user_piercings = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_piercings.setObjectName(u"lineedit_user_piercings")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_piercings, 1, 1, 1, 1)

        self.lineedit_user_weight = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_weight.setObjectName(u"lineedit_user_weight")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_weight, 9, 1, 1, 1)

        self.lineedit_user_home_town = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_home_town.setObjectName(u"lineedit_user_home_town")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_home_town, 21, 1, 1, 1)

        self.lineedit_user_city_country = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_city_country.setObjectName(u"lineedit_user_city_country")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_city_country, 19, 1, 1, 1)

        self.lineedit_user_height = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_height.setObjectName(u"lineedit_user_height")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_height, 7, 1, 1, 1)

        self.label_video_views = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_views.setObjectName(u"label_video_views")

        self.gridlayout_user_metadata.addWidget(self.label_video_views, 10, 0, 1, 1)

        self.lineedit_user_turn_offs = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_turn_offs.setObjectName(u"lineedit_user_turn_offs")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_turn_offs, 8, 1, 1, 1)

        self.label_profile_views = QLabel(self.scrollAreaWidgetContents_4)
        self.label_profile_views.setObjectName(u"label_profile_views")

        self.gridlayout_user_metadata.addWidget(self.label_profile_views, 15, 0, 1, 1)

        self.label_city_country = QLabel(self.scrollAreaWidgetContents_4)
        self.label_city_country.setObjectName(u"label_city_country")

        self.gridlayout_user_metadata.addWidget(self.label_city_country, 19, 0, 1, 1)

        self.label_tattoos = QLabel(self.scrollAreaWidgetContents_4)
        self.label_tattoos.setObjectName(u"label_tattoos")

        self.gridlayout_user_metadata.addWidget(self.label_tattoos, 22, 0, 1, 1)

        self.label_home_town = QLabel(self.scrollAreaWidgetContents_4)
        self.label_home_town.setObjectName(u"label_home_town")

        self.gridlayout_user_metadata.addWidget(self.label_home_town, 21, 0, 1, 1)

        self.lineedit_user_hair_color = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_hair_color.setObjectName(u"lineedit_user_hair_color")

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_hair_color, 17, 1, 1, 1)

        self.label_hair_color = QLabel(self.scrollAreaWidgetContents_4)
        self.label_hair_color.setObjectName(u"label_hair_color")

        self.gridlayout_user_metadata.addWidget(self.label_hair_color, 17, 0, 1, 1)


        self.gridlayout_metadata_.addLayout(self.gridlayout_user_metadata, 5, 0, 1, 3)

        self.button_user_get_bio = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_user_get_bio.setObjectName(u"button_user_get_bio")
        self.button_user_get_bio.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_user_get_bio.setStyleSheet(u"")

        self.gridlayout_metadata_.addWidget(self.button_user_get_bio, 2, 0, 1, 2)

        self.button_user_download_avatar = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_user_download_avatar.setObjectName(u"button_user_download_avatar")
        self.button_user_download_avatar.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_user_download_avatar.setStyleSheet(u"")

        self.gridlayout_metadata_.addWidget(self.button_user_download_avatar, 4, 0, 1, 2)

        self.button_video_thumbnail_download = QPushButton(self.scrollAreaWidgetContents_4)
        self.button_video_thumbnail_download.setObjectName(u"button_video_thumbnail_download")
        self.button_video_thumbnail_download.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_video_thumbnail_download.setStyleSheet(u"")

        self.gridlayout_metadata_.addWidget(self.button_video_thumbnail_download, 3, 0, 1, 2)


        self.gridLayout_27.addLayout(self.gridlayout_metadata_, 0, 0, 1, 1)

        self.scrollarea_metadata.setWidget(self.scrollAreaWidgetContents_4)

        self.verticallayout_metadata.addWidget(self.scrollarea_metadata)


        self.gridLayout_32.addLayout(self.verticallayout_metadata, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_8)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.gridLayout_11 = QGridLayout(self.page_9)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.stacked_widget_main.addWidget(self.page_9)

        self.gridLayout_13.addWidget(self.stacked_widget_main, 0, 0, 1, 1)

        self.scrollarea_status = QScrollArea(self.main_widget)
        self.scrollarea_status.setObjectName(u"scrollarea_status")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.scrollarea_status.sizePolicy().hasHeightForWidth())
        self.scrollarea_status.setSizePolicy(sizePolicy11)
        self.scrollarea_status.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 1024, 130))
        self.gridLayout_33 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridlayout_status = QGridLayout()
        self.gridlayout_status.setObjectName(u"gridlayout_status")
        self.progressbar_pornhub = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        sizePolicy6.setHeightForWidth(self.progressbar_pornhub.sizePolicy().hasHeightForWidth())
        self.progressbar_pornhub.setSizePolicy(sizePolicy6)
        self.progressbar_pornhub.setMinimumSize(QSize(300, 0))
        self.progressbar_pornhub.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.label_total_progress = QLabel(self.scrollAreaWidgetContents_5)
        self.label_total_progress.setObjectName(u"label_total_progress")
        sizePolicy1.setHeightForWidth(self.label_total_progress.sizePolicy().hasHeightForWidth())
        self.label_total_progress.setSizePolicy(sizePolicy1)

        self.gridlayout_status.addWidget(self.label_total_progress, 2, 0, 1, 1)

        self.label_progress_information = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_information.setObjectName(u"label_progress_information")
        sizePolicy1.setHeightForWidth(self.label_progress_information.sizePolicy().hasHeightForWidth())
        self.label_progress_information.setSizePolicy(sizePolicy1)

        self.gridlayout_status.addWidget(self.label_progress_information, 3, 0, 1, 2)

        self.progressbar_hqporner = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_hqporner.setObjectName(u"progressbar_hqporner")
        sizePolicy6.setHeightForWidth(self.progressbar_hqporner.sizePolicy().hasHeightForWidth())
        self.progressbar_hqporner.setSizePolicy(sizePolicy6)
        self.progressbar_hqporner.setMinimumSize(QSize(300, 0))
        self.progressbar_hqporner.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_hqporner, 1, 1, 1, 1)

        self.label_progress_pornhub = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_pornhub.setObjectName(u"label_progress_pornhub")
        sizePolicy1.setHeightForWidth(self.label_progress_pornhub.sizePolicy().hasHeightForWidth())
        self.label_progress_pornhub.setSizePolicy(sizePolicy1)

        self.gridlayout_status.addWidget(self.label_progress_pornhub, 0, 0, 1, 1)

        self.label_progress_hqporner = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_hqporner.setObjectName(u"label_progress_hqporner")
        sizePolicy1.setHeightForWidth(self.label_progress_hqporner.sizePolicy().hasHeightForWidth())
        self.label_progress_hqporner.setSizePolicy(sizePolicy1)

        self.gridlayout_status.addWidget(self.label_progress_hqporner, 1, 0, 1, 1)

        self.progressbar_total = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_total.setObjectName(u"progressbar_total")
        sizePolicy6.setHeightForWidth(self.progressbar_total.sizePolicy().hasHeightForWidth())
        self.progressbar_total.setSizePolicy(sizePolicy6)
        self.progressbar_total.setMinimumSize(QSize(300, 0))
        self.progressbar_total.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_total, 2, 1, 1, 1)


        self.gridLayout_33.addLayout(self.gridlayout_status, 0, 0, 1, 1)

        self.scrollarea_status.setWidget(self.scrollAreaWidgetContents_5)

        self.gridLayout_13.addWidget(self.scrollarea_status, 1, 0, 1, 1)


        self.main_gridlayout.addWidget(self.main_widget, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.main_gridlayout, 0, 0, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(0)
        self.stacked_widget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch V3 (C) Johannes Habel GPL 3", None))
        self.button_switch_home.setText("")
        self.button_switch_account.setText("")
        self.button_switch_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQ", None))
        self.button_switch_search.setText("")
        self.button_switch_settings.setText("")
        self.button_switch_metadata.setText("")
        self.button_switch_credits.setText("")
        self.stacked_widget_main.setStyleSheet("")
        self.radio_tree_show_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Only Title (a lot faster)", None))
        self.radio_tree_show_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Title, Author, Duration", None))
        self.checkbox_show_videos_reversed.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Show videos in reverse", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Porn_Fetch_Widget", u"Duration", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Porn_Fetch_Widget", u"Author", None));
        self.button_tree_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Selected Videos", None))
        self.button_tree_select_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select all", None))
        self.button_tree_unselect_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselect all", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.button_search_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.lineedit_file.setText("")
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"URLs in the file must be separated with new lines!", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.lineedit_search_hqporner.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search videos on HQPorner", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub or HQPorner Video URL", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.button_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub Model / Channel URL or a HQPorner Actresss name (e.g Anissa Kate or anissa-kate)", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.button_open_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.label_search_query_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.label_search_query_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.lineedit_seach_pornhub.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search videos on PornHub", None))
        self.button_search_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
        self.button_get_liked_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.button_get_watched_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.button_get_recommended_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.label_videos_by_category.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get videos by category", None))
        self.button_hqporner_category_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.button_list_categories.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"List of all categories", None))
        self.label_get_top_porn.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Top Porn:", None))
        self.radio_top_porn_week.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Week", None))
        self.radio_top_porn_month.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Month", None))
        self.radio_top_porn_all_time.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"All Time", None))
        self.button_top_porn_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.label_pages.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Pages:", None))
        self.button_help_pages.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.labe_get_random_video.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get random video", None))
        self.button_get_random_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Video", None))
        self.label_get_brazzers_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Brazzers videos", None))
        self.button_get_brazzers_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.label_threading_mode.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading Mode:", None))
        self.radio_threading_mode_ffmpeg.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"FFMPEG", None))
        self.radio_threading_mode_high_performance.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"High Performance", None))
        self.radio_threading_mode_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Default", None))
        self.button_threading_mode_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_semaphore.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Semaphore:", None))
        self.button_semaphore_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.radio_quality_worst.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Worst", None))
        self.label_quality.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Quality:", None))
        self.radio_quality_best.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Best", None))
        self.radio_quality_half.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Half", None))
        self.label_threading.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Threading: ", None))
        self.radio_threading_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.radio_threading_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_ui_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.radio_ui_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.radio_ui_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.label_ui_language.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface Language:", None))
        self.radio_ui_language_system_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"System default", None))
        self.radio_ui_language_chinese_simplified.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese (simplified)", None))
        self.radio_api_language_russian.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Russian", None))
        self.radio_api_language_custom.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Custom", None))
        self.radio_api_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_api_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.radio_api_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.radio_api_language_chinese.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese", None))
        self.label_api_language.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"API Language", None))
        self.lineedit_output_path.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter \"./\" for current directory", None))
        self.label_output_path.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Output path:", None))
        self.button_directory_system_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_directory_system.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Use Directory system? ", None))
        self.button_output_path_select.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open", None))
        self.label_searching_limit.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Result Limit:", None))
        self.radio_directory_system_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_directory_system_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Apply / Reload", None))
        self.button_metadata_video_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_metadata_video_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Video URL:", None))
        self.button_metadata_user_start.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_metadata_user_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User URL:", None))
        self.label_height.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Height:", None))
        self.label_birth_place.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Birth Place:", None))
        self.label_turn_ons.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Turn Ons:", None))
        self.label_interests_hobbies.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Interests / Hobbies:", None))
        self.label_piercings.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Piercings:", None))
        self.label_ethnicity.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Ethnicity:", None))
        self.label_turn_offs.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Turn Offs:", None))
        self.label_videos_watched.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Videos Watched:", None))
        self.label_fake_boobs.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Fake Boobs:", None))
        self.label_interested_in.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Interested in:", None))
        self.label_gender.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Gender:", None))
        self.label_user_type.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"User Type:", None))
        self.label_name.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Name:", None))
        self.label_video_title.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Title:", None))
        self.label_video_tags.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tags:", None))
        self.label_video_rating.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Rating:", None))
        self.label_video_duration.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Duration:", None))
        self.label_video_views_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Views:", None))
        self.label_video_pornstars.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Pornstars:", None))
        self.label_video_hotspots.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hotspots:", None))
        self.label_video_orientation.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Orientation:", None))
        self.label_widght.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Weight:", None))
        self.label_relationship.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Relationship:", None))
        self.label_video_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Video Views:", None))
        self.label_profile_views.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Profile Views:", None))
        self.label_city_country.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"City / Country:", None))
        self.label_tattoos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Tattoos:", None))
        self.label_home_town.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home Town", None))
        self.label_hair_color.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Hair Color:", None))
        self.button_user_get_bio.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get User's Bio", None))
        self.button_user_download_avatar.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download User Avatar", None))
        self.button_video_thumbnail_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Thumbnail", None))
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_progress_information.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Information: The total progressbar only counts the total progress of all PornHub videos being downloaded.", None))
        self.label_progress_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub:", None))
        self.label_progress_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner:", None))
    # retranslateUi

