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
        Porn_Fetch_Widget.resize(1044, 611)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Porn_Fetch_Widget.sizePolicy().hasHeightForWidth())
        Porn_Fetch_Widget.setSizePolicy(sizePolicy)
        Porn_Fetch_Widget.setMinimumSize(QSize(100, 50))
        self.gridLayout_16 = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
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

        self.button_switch_tools = QPushButton(Porn_Fetch_Widget)
        self.button_switch_tools.setObjectName(u"button_switch_tools")
        self.button_switch_tools.setMinimumSize(QSize(50, 50))
        font = QFont()
        font.setPointSize(9)
        self.button_switch_tools.setFont(font)
        self.button_switch_tools.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_tools.setStyleSheet(u"border: none")
        self.button_switch_tools.setIconSize(QSize(32, 32))

        self.verticallayout_sidebar.addWidget(self.button_switch_tools)

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
        self.scrollarea_status = QScrollArea(self.main_widget)
        self.scrollarea_status.setObjectName(u"scrollarea_status")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollarea_status.sizePolicy().hasHeightForWidth())
        self.scrollarea_status.setSizePolicy(sizePolicy1)
        self.scrollarea_status.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 956, 202))
        self.gridLayout_33 = QGridLayout(self.scrollAreaWidgetContents_5)
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridlayout_status = QGridLayout()
        self.gridlayout_status.setObjectName(u"gridlayout_status")
        self.label_total_progress = QLabel(self.scrollAreaWidgetContents_5)
        self.label_total_progress.setObjectName(u"label_total_progress")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_total_progress.sizePolicy().hasHeightForWidth())
        self.label_total_progress.setSizePolicy(sizePolicy2)

        self.gridlayout_status.addWidget(self.label_total_progress, 5, 0, 1, 1)

        self.label_progress_pornhub = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_pornhub.setObjectName(u"label_progress_pornhub")
        sizePolicy2.setHeightForWidth(self.label_progress_pornhub.sizePolicy().hasHeightForWidth())
        self.label_progress_pornhub.setSizePolicy(sizePolicy2)

        self.gridlayout_status.addWidget(self.label_progress_pornhub, 0, 0, 1, 1)

        self.label_progress_xnxx = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_xnxx.setObjectName(u"label_progress_xnxx")

        self.gridlayout_status.addWidget(self.label_progress_xnxx, 3, 0, 1, 1)

        self.progressbar_hqporner = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_hqporner.setObjectName(u"progressbar_hqporner")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.progressbar_hqporner.sizePolicy().hasHeightForWidth())
        self.progressbar_hqporner.setSizePolicy(sizePolicy3)
        self.progressbar_hqporner.setMinimumSize(QSize(300, 0))
        self.progressbar_hqporner.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_hqporner, 1, 1, 1, 1)

        self.label_progress_information = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_information.setObjectName(u"label_progress_information")
        sizePolicy2.setHeightForWidth(self.label_progress_information.sizePolicy().hasHeightForWidth())
        self.label_progress_information.setSizePolicy(sizePolicy2)

        self.gridlayout_status.addWidget(self.label_progress_information, 6, 0, 1, 2)

        self.progressbar_xnxx = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_xnxx.setObjectName(u"progressbar_xnxx")
        self.progressbar_xnxx.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_xnxx, 3, 1, 1, 1)

        self.progressbar_eporner = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_eporner.setObjectName(u"progressbar_eporner")
        self.progressbar_eporner.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_eporner, 2, 1, 1, 1)

        self.label_progress_eporner = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_eporner.setObjectName(u"label_progress_eporner")

        self.gridlayout_status.addWidget(self.label_progress_eporner, 2, 0, 1, 1)

        self.label_progress_hqporner = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_hqporner.setObjectName(u"label_progress_hqporner")
        sizePolicy2.setHeightForWidth(self.label_progress_hqporner.sizePolicy().hasHeightForWidth())
        self.label_progress_hqporner.setSizePolicy(sizePolicy2)

        self.gridlayout_status.addWidget(self.label_progress_hqporner, 1, 0, 1, 1)

        self.progressbar_total = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_total.setObjectName(u"progressbar_total")
        sizePolicy3.setHeightForWidth(self.progressbar_total.sizePolicy().hasHeightForWidth())
        self.progressbar_total.setSizePolicy(sizePolicy3)
        self.progressbar_total.setMinimumSize(QSize(300, 0))
        self.progressbar_total.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_total, 5, 1, 1, 1)

        self.progressbar_pornhub = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        sizePolicy3.setHeightForWidth(self.progressbar_pornhub.sizePolicy().hasHeightForWidth())
        self.progressbar_pornhub.setSizePolicy(sizePolicy3)
        self.progressbar_pornhub.setMinimumSize(QSize(300, 0))
        self.progressbar_pornhub.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.label_progress_xvideos = QLabel(self.scrollAreaWidgetContents_5)
        self.label_progress_xvideos.setObjectName(u"label_progress_xvideos")

        self.gridlayout_status.addWidget(self.label_progress_xvideos, 4, 0, 1, 1)

        self.progressbar_xvideos = QProgressBar(self.scrollAreaWidgetContents_5)
        self.progressbar_xvideos.setObjectName(u"progressbar_xvideos")
        self.progressbar_xvideos.setValue(0)

        self.gridlayout_status.addWidget(self.progressbar_xvideos, 4, 1, 1, 1)


        self.gridLayout_33.addLayout(self.gridlayout_status, 1, 0, 1, 1)

        self.scrollarea_status.setWidget(self.scrollAreaWidgetContents_5)

        self.gridLayout_13.addWidget(self.scrollarea_status, 2, 0, 1, 1)

        self.stacked_widget_main = QStackedWidget(self.main_widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.widget = QWidget()
        self.widget.setObjectName(u"widget")
        self.gridLayout_8 = QGridLayout(self.widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticallayout_treewidget = QVBoxLayout()
        self.verticallayout_treewidget.setObjectName(u"verticallayout_treewidget")
        self.scrollarea_treewidget = QScrollArea(self.widget)
        self.scrollarea_treewidget.setObjectName(u"scrollarea_treewidget")
        self.scrollarea_treewidget.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 936, 282))
        self.gridLayout_4 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticallayout_treewidget_settings = QVBoxLayout()
        self.verticallayout_treewidget_settings.setObjectName(u"verticallayout_treewidget_settings")
        self.horizontallayout_treewidget_settings = QHBoxLayout()
        self.horizontallayout_treewidget_settings.setObjectName(u"horizontallayout_treewidget_settings")
        self.radio_tree_show_title = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radio_tree_show_title.setObjectName(u"radio_tree_show_title")
        sizePolicy2.setHeightForWidth(self.radio_tree_show_title.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_title.setSizePolicy(sizePolicy2)
        self.radio_tree_show_title.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_tree_show_title.setChecked(False)

        self.horizontallayout_treewidget_settings.addWidget(self.radio_tree_show_title)

        self.radio_tree_show_all = QRadioButton(self.scrollAreaWidgetContents_3)
        self.radio_tree_show_all.setObjectName(u"radio_tree_show_all")
        sizePolicy2.setHeightForWidth(self.radio_tree_show_all.sizePolicy().hasHeightForWidth())
        self.radio_tree_show_all.setSizePolicy(sizePolicy2)
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
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy4)
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

        self.scrollarea_stacked_top = QScrollArea(self.widget)
        self.scrollarea_stacked_top.setObjectName(u"scrollarea_stacked_top")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.scrollarea_stacked_top.sizePolicy().hasHeightForWidth())
        self.scrollarea_stacked_top.setSizePolicy(sizePolicy5)
        self.scrollarea_stacked_top.setWidgetResizable(True)
        self.scrollAreaWidgetContents_7 = QWidget()
        self.scrollAreaWidgetContents_7.setObjectName(u"scrollAreaWidgetContents_7")
        self.scrollAreaWidgetContents_7.setGeometry(QRect(0, -7, 938, 318))
        self.gridLayout_14 = QGridLayout(self.scrollAreaWidgetContents_7)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.stacked_widget_top = QStackedWidget(self.scrollAreaWidgetContents_7)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        sizePolicy4.setHeightForWidth(self.stacked_widget_top.sizePolicy().hasHeightForWidth())
        self.stacked_widget_top.setSizePolicy(sizePolicy4)
        self.stacked_widget_top.setMinimumSize(QSize(600, 300))
        self.stacked_widget_top.setStyleSheet(u"b")
        self.page_download = QWidget()
        self.page_download.setObjectName(u"page_download")
        self.gridLayout_5 = QGridLayout(self.page_download)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(0)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SetMaximumSize)
        self.label_file = QLabel(self.page_download)
        self.label_file.setObjectName(u"label_file")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_file.sizePolicy().hasHeightForWidth())
        self.label_file.setSizePolicy(sizePolicy6)
        self.label_file.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_file, 4, 0, 1, 1)

        self.lineedit_search_query = QLineEdit(self.page_download)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        sizePolicy3.setHeightForWidth(self.lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.lineedit_search_query.setSizePolicy(sizePolicy3)
        self.lineedit_search_query.setMinimumSize(QSize(300, 0))

        self.gridlayout_downloading.addWidget(self.lineedit_search_query, 5, 1, 1, 1)

        self.button_download = QPushButton(self.page_download)
        self.button_download.setObjectName(u"button_download")
        sizePolicy7 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.button_download.sizePolicy().hasHeightForWidth())
        self.button_download.setSizePolicy(sizePolicy7)
        self.button_download.setMinimumSize(QSize(60, 2))
        self.button_download.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_download, 1, 2, 1, 1)

        self.label_search_website = QLabel(self.page_download)
        self.label_search_website.setObjectName(u"label_search_website")

        self.gridlayout_downloading.addWidget(self.label_search_website, 7, 0, 1, 1)

        self.button_search = QPushButton(self.page_download)
        self.button_search.setObjectName(u"button_search")
        sizePolicy7.setHeightForWidth(self.button_search.sizePolicy().hasHeightForWidth())
        self.button_search.setSizePolicy(sizePolicy7)
        self.button_search.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_search, 5, 2, 1, 1)

        self.button_model = QPushButton(self.page_download)
        self.button_model.setObjectName(u"button_model")
        sizePolicy7.setHeightForWidth(self.button_model.sizePolicy().hasHeightForWidth())
        self.button_model.setSizePolicy(sizePolicy7)
        self.button_model.setMinimumSize(QSize(60, 2))
        self.button_model.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_model.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_model, 3, 2, 1, 1)

        self.lineedit_file = QLineEdit(self.page_download)
        self.lineedit_file.setObjectName(u"lineedit_file")
        sizePolicy3.setHeightForWidth(self.lineedit_file.sizePolicy().hasHeightForWidth())
        self.lineedit_file.setSizePolicy(sizePolicy3)
        self.lineedit_file.setMinimumSize(QSize(300, 2))
        self.lineedit_file.setReadOnly(True)

        self.gridlayout_downloading.addWidget(self.lineedit_file, 4, 1, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page_download)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")
        sizePolicy3.setHeightForWidth(self.lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.lineedit_model_url.setSizePolicy(sizePolicy3)
        self.lineedit_model_url.setMinimumSize(QSize(300, 2))

        self.gridlayout_downloading.addWidget(self.lineedit_model_url, 3, 1, 1, 1)

        self.labell_search = QLabel(self.page_download)
        self.labell_search.setObjectName(u"labell_search")

        self.gridlayout_downloading.addWidget(self.labell_search, 5, 0, 1, 1)

        self.label_url = QLabel(self.page_download)
        self.label_url.setObjectName(u"label_url")
        sizePolicy6.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy6)
        self.label_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_url, 1, 0, 1, 1)

        self.horizontallayout_searching_websites = QHBoxLayout()
        self.horizontallayout_searching_websites.setSpacing(0)
        self.horizontallayout_searching_websites.setObjectName(u"horizontallayout_searching_websites")
        self.horizontallayout_searching_websites.setContentsMargins(-1, 5, -1, -1)
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

        self.horizontal_spacer_searching = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontallayout_searching_websites.addItem(self.horizontal_spacer_searching)


        self.gridlayout_downloading.addLayout(self.horizontallayout_searching_websites, 7, 1, 1, 2)

        self.lineedit_url = QLineEdit(self.page_download)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy3.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy3)
        self.lineedit_url.setMinimumSize(QSize(300, 4))

        self.gridlayout_downloading.addWidget(self.lineedit_url, 1, 1, 1, 1)

        self.button_open_file = QPushButton(self.page_download)
        self.button_open_file.setObjectName(u"button_open_file")
        sizePolicy7.setHeightForWidth(self.button_open_file.sizePolicy().hasHeightForWidth())
        self.button_open_file.setSizePolicy(sizePolicy7)
        self.button_open_file.setMinimumSize(QSize(60, 2))
        self.button_open_file.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_open_file.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_open_file, 4, 2, 1, 1)

        self.label_model_url = QLabel(self.page_download)
        self.label_model_url.setObjectName(u"label_model_url")
        sizePolicy6.setHeightForWidth(self.label_model_url.sizePolicy().hasHeightForWidth())
        self.label_model_url.setSizePolicy(sizePolicy6)
        self.label_model_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_model_url, 3, 0, 1, 1)

        self.button_switch_supported_websites = QPushButton(self.page_download)
        self.button_switch_supported_websites.setObjectName(u"button_switch_supported_websites")
        self.button_switch_supported_websites.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_switch_supported_websites, 0, 0, 1, 3)


        self.gridLayout_5.addLayout(self.gridlayout_downloading, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_download)
        self.page_login = QWidget()
        self.page_login.setObjectName(u"page_login")
        self.gridLayout_2 = QGridLayout(self.page_login)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridlayout_login_box = QGridLayout()
        self.gridlayout_login_box.setSpacing(0)
        self.gridlayout_login_box.setObjectName(u"gridlayout_login_box")
        self.lineedit_username = QLineEdit(self.page_login)
        self.lineedit_username.setObjectName(u"lineedit_username")
        sizePolicy3.setHeightForWidth(self.lineedit_username.sizePolicy().hasHeightForWidth())
        self.lineedit_username.setSizePolicy(sizePolicy3)
        self.lineedit_username.setMinimumSize(QSize(150, 0))

        self.gridlayout_login_box.addWidget(self.lineedit_username, 0, 1, 1, 3)

        self.button_get_liked_videos = QPushButton(self.page_login)
        self.button_get_liked_videos.setObjectName(u"button_get_liked_videos")
        self.button_get_liked_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_liked_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_liked_videos, 3, 0, 1, 1)

        self.button_get_watched_videos = QPushButton(self.page_login)
        self.button_get_watched_videos.setObjectName(u"button_get_watched_videos")
        self.button_get_watched_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_watched_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_watched_videos, 3, 1, 1, 1)

        self.label_password = QLabel(self.page_login)
        self.label_password.setObjectName(u"label_password")
        sizePolicy2.setHeightForWidth(self.label_password.sizePolicy().hasHeightForWidth())
        self.label_password.setSizePolicy(sizePolicy2)

        self.gridlayout_login_box.addWidget(self.label_password, 1, 0, 1, 1)

        self.button_login = QPushButton(self.page_login)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setMinimumSize(QSize(0, 0))
        self.button_login.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_login.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_login, 2, 0, 1, 4)

        self.label_username = QLabel(self.page_login)
        self.label_username.setObjectName(u"label_username")
        sizePolicy2.setHeightForWidth(self.label_username.sizePolicy().hasHeightForWidth())
        self.label_username.setSizePolicy(sizePolicy2)

        self.gridlayout_login_box.addWidget(self.label_username, 0, 0, 1, 1)

        self.lineedit_password = QLineEdit(self.page_login)
        self.lineedit_password.setObjectName(u"lineedit_password")
        sizePolicy3.setHeightForWidth(self.lineedit_password.sizePolicy().hasHeightForWidth())
        self.lineedit_password.setSizePolicy(sizePolicy3)
        self.lineedit_password.setMinimumSize(QSize(150, 0))
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.gridlayout_login_box.addWidget(self.lineedit_password, 1, 1, 1, 3)

        self.button_get_recommended_videos = QPushButton(self.page_login)
        self.button_get_recommended_videos.setObjectName(u"button_get_recommended_videos")
        self.button_get_recommended_videos.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_recommended_videos.setStyleSheet(u"")

        self.gridlayout_login_box.addWidget(self.button_get_recommended_videos, 3, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridlayout_login_box, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_login)
        self.page_nothing_2 = QWidget()
        self.page_nothing_2.setObjectName(u"page_nothing_2")
        self.gridLayout_6 = QGridLayout(self.page_nothing_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stacked_widget_top.addWidget(self.page_nothing_2)
        self.page_hqporner = QWidget()
        self.page_hqporner.setObjectName(u"page_hqporner")
        self.gridLayout_29 = QGridLayout(self.page_hqporner)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.groupBox = QGroupBox(self.page_hqporner)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_7 = QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.radio_top_porn_month = QRadioButton(self.groupBox)
        self.radio_top_porn_month.setObjectName(u"radio_top_porn_month")
        self.radio_top_porn_month.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_month.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.radio_top_porn_month, 0, 2, 1, 1)

        self.button_top_porn_get_videos = QPushButton(self.groupBox)
        self.button_top_porn_get_videos.setObjectName(u"button_top_porn_get_videos")
        self.button_top_porn_get_videos.setMinimumSize(QSize(0, 10))
        self.button_top_porn_get_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.button_top_porn_get_videos, 0, 4, 1, 1)

        self.label_get_brazzers_videos = QLabel(self.groupBox)
        self.label_get_brazzers_videos.setObjectName(u"label_get_brazzers_videos")
        self.label_get_brazzers_videos.setMinimumSize(QSize(0, 4))

        self.gridLayout.addWidget(self.label_get_brazzers_videos, 3, 0, 1, 4)

        self.radio_top_porn_week = QRadioButton(self.groupBox)
        self.radio_top_porn_week.setObjectName(u"radio_top_porn_week")
        self.radio_top_porn_week.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_week.setCursor(QCursor(Qt.PointingHandCursor))
        self.radio_top_porn_week.setChecked(True)

        self.gridLayout.addWidget(self.radio_top_porn_week, 0, 1, 1, 1)

        self.button_list_categories = QPushButton(self.groupBox)
        self.button_list_categories.setObjectName(u"button_list_categories")
        sizePolicy7.setHeightForWidth(self.button_list_categories.sizePolicy().hasHeightForWidth())
        self.button_list_categories.setSizePolicy(sizePolicy7)
        self.button_list_categories.setMinimumSize(QSize(0, 2))
        self.button_list_categories.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.button_list_categories, 1, 4, 1, 1)

        self.lineedit_hqporner_category = QLineEdit(self.groupBox)
        self.lineedit_hqporner_category.setObjectName(u"lineedit_hqporner_category")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(4)
        sizePolicy8.setHeightForWidth(self.lineedit_hqporner_category.sizePolicy().hasHeightForWidth())
        self.lineedit_hqporner_category.setSizePolicy(sizePolicy8)
        self.lineedit_hqporner_category.setMinimumSize(QSize(100, 4))

        self.gridLayout.addWidget(self.lineedit_hqporner_category, 1, 1, 1, 2)

        self.label_get_top_porn = QLabel(self.groupBox)
        self.label_get_top_porn.setObjectName(u"label_get_top_porn")

        self.gridLayout.addWidget(self.label_get_top_porn, 0, 0, 1, 1)

        self.radio_top_porn_all_time = QRadioButton(self.groupBox)
        self.radio_top_porn_all_time.setObjectName(u"radio_top_porn_all_time")
        self.radio_top_porn_all_time.setMinimumSize(QSize(0, 10))
        self.radio_top_porn_all_time.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.radio_top_porn_all_time, 0, 3, 1, 1)

        self.button_hqporner_category_get_videos = QPushButton(self.groupBox)
        self.button_hqporner_category_get_videos.setObjectName(u"button_hqporner_category_get_videos")
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(2)
        sizePolicy9.setHeightForWidth(self.button_hqporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.button_hqporner_category_get_videos.setSizePolicy(sizePolicy9)
        self.button_hqporner_category_get_videos.setMinimumSize(QSize(0, 2))
        self.button_hqporner_category_get_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.button_hqporner_category_get_videos, 1, 3, 1, 1)

        self.button_get_random_videos = QPushButton(self.groupBox)
        self.button_get_random_videos.setObjectName(u"button_get_random_videos")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.button_get_random_videos.sizePolicy().hasHeightForWidth())
        self.button_get_random_videos.setSizePolicy(sizePolicy10)
        self.button_get_random_videos.setMinimumSize(QSize(0, 10))
        self.button_get_random_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.button_get_random_videos, 2, 4, 1, 1)

        self.button_get_brazzers_videos = QPushButton(self.groupBox)
        self.button_get_brazzers_videos.setObjectName(u"button_get_brazzers_videos")
        sizePolicy10.setHeightForWidth(self.button_get_brazzers_videos.sizePolicy().hasHeightForWidth())
        self.button_get_brazzers_videos.setSizePolicy(sizePolicy10)
        self.button_get_brazzers_videos.setMinimumSize(QSize(0, 10))
        self.button_get_brazzers_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridLayout.addWidget(self.button_get_brazzers_videos, 3, 4, 1, 1)

        self.labe_get_random_video = QLabel(self.groupBox)
        self.labe_get_random_video.setObjectName(u"labe_get_random_video")
        self.labe_get_random_video.setMinimumSize(QSize(0, 4))

        self.gridLayout.addWidget(self.labe_get_random_video, 2, 0, 1, 4)

        self.label_videos_by_category = QLabel(self.groupBox)
        self.label_videos_by_category.setObjectName(u"label_videos_by_category")
        self.label_videos_by_category.setMinimumSize(QSize(0, 4))

        self.gridLayout.addWidget(self.label_videos_by_category, 1, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.page_hqporner)
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
        sizePolicy8.setHeightForWidth(self.lineedit_videos_by_category_eporner.sizePolicy().hasHeightForWidth())
        self.lineedit_videos_by_category_eporner.setSizePolicy(sizePolicy8)
        self.lineedit_videos_by_category_eporner.setMinimumSize(QSize(100, 4))

        self.horizontalLayout.addWidget(self.lineedit_videos_by_category_eporner)

        self.button_eporner_category_get_videos = QPushButton(self.groupBox_2)
        self.button_eporner_category_get_videos.setObjectName(u"button_eporner_category_get_videos")
        sizePolicy9.setHeightForWidth(self.button_eporner_category_get_videos.sizePolicy().hasHeightForWidth())
        self.button_eporner_category_get_videos.setSizePolicy(sizePolicy9)
        self.button_eporner_category_get_videos.setMinimumSize(QSize(0, 2))
        self.button_eporner_category_get_videos.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.button_eporner_category_get_videos)

        self.button_list_categories_eporner = QPushButton(self.groupBox_2)
        self.button_list_categories_eporner.setObjectName(u"button_list_categories_eporner")
        sizePolicy7.setHeightForWidth(self.button_list_categories_eporner.sizePolicy().hasHeightForWidth())
        self.button_list_categories_eporner.setSizePolicy(sizePolicy7)
        self.button_list_categories_eporner.setMinimumSize(QSize(0, 2))
        self.button_list_categories_eporner.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout.addWidget(self.button_list_categories_eporner)


        self.gridLayout_15.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout_29.addWidget(self.groupBox_2, 1, 1, 1, 1)

        self.stacked_widget_top.addWidget(self.page_hqporner)

        self.gridLayout_14.addWidget(self.stacked_widget_top, 0, 0, 1, 1)

        self.scrollarea_stacked_top.setWidget(self.scrollAreaWidgetContents_7)

        self.gridLayout_8.addWidget(self.scrollarea_stacked_top, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.widget)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.gridLayout_25 = QGridLayout(self.page_settings)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.scrollarea_settings = QScrollArea(self.page_settings)
        self.scrollarea_settings.setObjectName(u"scrollarea_settings")
        self.scrollarea_settings.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 686, 568))
        self.gridLayout_34 = QGridLayout(self.scrollAreaWidgetContents_6)
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.goroupbox_gui = QGroupBox(self.scrollAreaWidgetContents_6)
        self.goroupbox_gui.setObjectName(u"goroupbox_gui")
        self.gridLayout_12 = QGridLayout(self.goroupbox_gui)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridlayout_gui_settings = QGridLayout()
        self.gridlayout_gui_settings.setObjectName(u"gridlayout_gui_settings")
        self.radio_ui_language_english = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_english.setObjectName(u"radio_ui_language_english")
        self.radio_ui_language_english.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_english, 0, 2, 1, 1)

        self.radio_ui_language_system_default = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_system_default.setObjectName(u"radio_ui_language_system_default")
        self.radio_ui_language_system_default.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_system_default, 0, 1, 1, 1)

        self.radio_ui_language_french = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_french.setObjectName(u"radio_ui_language_french")
        self.radio_ui_language_french.setEnabled(True)

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_french, 0, 5, 1, 1)

        self.radio_ui_language_german = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_german.setObjectName(u"radio_ui_language_german")
        self.radio_ui_language_german.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_german, 0, 3, 1, 1)

        self.label_ui_language = QLabel(self.goroupbox_gui)
        self.label_ui_language.setObjectName(u"label_ui_language")
        sizePolicy2.setHeightForWidth(self.label_ui_language.sizePolicy().hasHeightForWidth())
        self.label_ui_language.setSizePolicy(sizePolicy2)

        self.gridlayout_gui_settings.addWidget(self.label_ui_language, 0, 0, 1, 1)

        self.radio_ui_language_chinese_simplified = QRadioButton(self.goroupbox_gui)
        self.radio_ui_language_chinese_simplified.setObjectName(u"radio_ui_language_chinese_simplified")
        self.radio_ui_language_chinese_simplified.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_gui_settings.addWidget(self.radio_ui_language_chinese_simplified, 0, 4, 1, 1)


        self.gridLayout_12.addLayout(self.gridlayout_gui_settings, 0, 0, 1, 1)


        self.gridLayout_34.addWidget(self.goroupbox_gui, 2, 0, 1, 1)

        self.groupbox_videos = QGroupBox(self.scrollAreaWidgetContents_6)
        self.groupbox_videos.setObjectName(u"groupbox_videos")
        self.gridLayout_10 = QGridLayout(self.groupbox_videos)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_searching_limit = QLabel(self.groupbox_videos)
        self.label_searching_limit.setObjectName(u"label_searching_limit")

        self.horizontalLayout_9.addWidget(self.label_searching_limit)

        self.spinbox_treewidget_limit = QSpinBox(self.groupbox_videos)
        self.spinbox_treewidget_limit.setObjectName(u"spinbox_treewidget_limit")
        self.spinbox_treewidget_limit.setMinimum(1)
        self.spinbox_treewidget_limit.setMaximum(200)

        self.horizontalLayout_9.addWidget(self.spinbox_treewidget_limit)

        self.button_result_limit_help = QPushButton(self.groupbox_videos)
        self.button_result_limit_help.setObjectName(u"button_result_limit_help")
        self.button_result_limit_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontalLayout_9.addWidget(self.button_result_limit_help)


        self.gridLayout_10.addLayout(self.horizontalLayout_9, 3, 0, 1, 1)

        self.horizontallayout_directory_system = QHBoxLayout()
        self.horizontallayout_directory_system.setObjectName(u"horizontallayout_directory_system")
        self.label_directory_system = QLabel(self.groupbox_videos)
        self.label_directory_system.setObjectName(u"label_directory_system")

        self.horizontallayout_directory_system.addWidget(self.label_directory_system)

        self.radio_directory_system_yes = QRadioButton(self.groupbox_videos)
        self.radio_directory_system_yes.setObjectName(u"radio_directory_system_yes")
        self.radio_directory_system_yes.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_directory_system.addWidget(self.radio_directory_system_yes)

        self.radio_directory_system_no = QRadioButton(self.groupbox_videos)
        self.radio_directory_system_no.setObjectName(u"radio_directory_system_no")
        self.radio_directory_system_no.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_directory_system.addWidget(self.radio_directory_system_no)

        self.button_directory_system_help = QPushButton(self.groupbox_videos)
        self.button_directory_system_help.setObjectName(u"button_directory_system_help")
        self.button_directory_system_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_directory_system.addWidget(self.button_directory_system_help)


        self.gridLayout_10.addLayout(self.horizontallayout_directory_system, 2, 0, 1, 1)

        self.horizontallayout_quality = QHBoxLayout()
        self.horizontallayout_quality.setObjectName(u"horizontallayout_quality")
        self.label_quality = QLabel(self.groupbox_videos)
        self.label_quality.setObjectName(u"label_quality")
        sizePolicy2.setHeightForWidth(self.label_quality.sizePolicy().hasHeightForWidth())
        self.label_quality.setSizePolicy(sizePolicy2)

        self.horizontallayout_quality.addWidget(self.label_quality)

        self.radio_quality_best = QRadioButton(self.groupbox_videos)
        self.radio_quality_best.setObjectName(u"radio_quality_best")
        self.radio_quality_best.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_quality.addWidget(self.radio_quality_best)

        self.radio_quality_half = QRadioButton(self.groupbox_videos)
        self.radio_quality_half.setObjectName(u"radio_quality_half")
        self.radio_quality_half.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_quality.addWidget(self.radio_quality_half)

        self.radio_quality_worst = QRadioButton(self.groupbox_videos)
        self.radio_quality_worst.setObjectName(u"radio_quality_worst")
        self.radio_quality_worst.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_quality.addWidget(self.radio_quality_worst)


        self.gridLayout_10.addLayout(self.horizontallayout_quality, 0, 0, 1, 1)

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
        self.button_output_path_select.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_output_path.addWidget(self.button_output_path_select)


        self.gridLayout_10.addLayout(self.horizontallayout_output_path, 1, 0, 1, 1)

        self.gridlayout_api_language = QGridLayout()
        self.gridlayout_api_language.setObjectName(u"gridlayout_api_language")
        self.radio_api_language_chinese = QRadioButton(self.groupbox_videos)
        self.radio_api_language_chinese.setObjectName(u"radio_api_language_chinese")
        self.radio_api_language_chinese.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_chinese, 2, 1, 1, 1)

        self.horizontalspacer_api_language_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_api_language.addItem(self.horizontalspacer_api_language_3, 3, 4, 1, 1)

        self.radio_api_language_french = QRadioButton(self.groupbox_videos)
        self.radio_api_language_french.setObjectName(u"radio_api_language_french")
        self.radio_api_language_french.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_french, 4, 0, 1, 1)

        self.horizontalspacer_api_language_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_api_language.addItem(self.horizontalspacer_api_language_2, 2, 4, 1, 1)

        self.radio_api_language_english = QRadioButton(self.groupbox_videos)
        self.radio_api_language_english.setObjectName(u"radio_api_language_english")
        self.radio_api_language_english.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_english, 2, 0, 1, 1)

        self.radio_api_language_spanish = QRadioButton(self.groupbox_videos)
        self.radio_api_language_spanish.setObjectName(u"radio_api_language_spanish")

        self.gridlayout_api_language.addWidget(self.radio_api_language_spanish, 2, 2, 1, 1)

        self.radio_api_language_portuguese = QRadioButton(self.groupbox_videos)
        self.radio_api_language_portuguese.setObjectName(u"radio_api_language_portuguese")

        self.gridlayout_api_language.addWidget(self.radio_api_language_portuguese, 4, 2, 1, 1)

        self.radio_api_language_japanese = QRadioButton(self.groupbox_videos)
        self.radio_api_language_japanese.setObjectName(u"radio_api_language_japanese")

        self.gridlayout_api_language.addWidget(self.radio_api_language_japanese, 3, 3, 1, 1)

        self.horizontalspacer_api_language = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridlayout_api_language.addItem(self.horizontalspacer_api_language, 4, 4, 1, 1)

        self.radio_api_language_italian = QRadioButton(self.groupbox_videos)
        self.radio_api_language_italian.setObjectName(u"radio_api_language_italian")

        self.gridlayout_api_language.addWidget(self.radio_api_language_italian, 3, 2, 1, 1)

        self.radio_api_language_czech = QRadioButton(self.groupbox_videos)
        self.radio_api_language_czech.setObjectName(u"radio_api_language_czech")

        self.gridlayout_api_language.addWidget(self.radio_api_language_czech, 2, 3, 1, 1)

        self.radio_api_language_german = QRadioButton(self.groupbox_videos)
        self.radio_api_language_german.setObjectName(u"radio_api_language_german")
        self.radio_api_language_german.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_german, 3, 0, 1, 1)

        self.radio_api_language_dutch = QRadioButton(self.groupbox_videos)
        self.radio_api_language_dutch.setObjectName(u"radio_api_language_dutch")

        self.gridlayout_api_language.addWidget(self.radio_api_language_dutch, 4, 1, 1, 1)

        self.radio_api_language_russian = QRadioButton(self.groupbox_videos)
        self.radio_api_language_russian.setObjectName(u"radio_api_language_russian")
        self.radio_api_language_russian.setCursor(QCursor(Qt.PointingHandCursor))

        self.gridlayout_api_language.addWidget(self.radio_api_language_russian, 3, 1, 1, 1)

        self.label_api_language = QLabel(self.groupbox_videos)
        self.label_api_language.setObjectName(u"label_api_language")
        sizePolicy2.setHeightForWidth(self.label_api_language.sizePolicy().hasHeightForWidth())
        self.label_api_language.setSizePolicy(sizePolicy2)

        self.gridlayout_api_language.addWidget(self.label_api_language, 1, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridlayout_api_language, 4, 0, 1, 1)


        self.gridLayout_34.addWidget(self.groupbox_videos, 1, 0, 1, 1)

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
        self.spinbox_semaphore.setMaximum(10)

        self.horizontallayout_simultaneous_downloads.addWidget(self.spinbox_semaphore)

        self.button_semaphore_help = QPushButton(self.groupbox_performance)
        self.button_semaphore_help.setObjectName(u"button_semaphore_help")
        self.button_semaphore_help.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.spinbox_maximal_workers.setMaximum(50)

        self.horizontallayout_maximal_workers.addWidget(self.spinbox_maximal_workers)

        self.button_workers_help = QPushButton(self.groupbox_performance)
        self.button_workers_help.setObjectName(u"button_workers_help")
        self.button_workers_help.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.spinbox_pornhub_delay.setMaximum(10)

        self.horizontallayout_pornhub_delay.addWidget(self.spinbox_pornhub_delay)

        self.button_pornhub_delay_help = QPushButton(self.groupbox_performance)
        self.button_pornhub_delay_help.setObjectName(u"button_pornhub_delay_help")
        self.button_pornhub_delay_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_pornhub_delay.addWidget(self.button_pornhub_delay_help)


        self.gridLayout_9.addLayout(self.horizontallayout_pornhub_delay, 3, 0, 1, 1)

        self.horizontallayout_threading_mode = QHBoxLayout()
        self.horizontallayout_threading_mode.setObjectName(u"horizontallayout_threading_mode")
        self.label_threading_mode = QLabel(self.groupbox_performance)
        self.label_threading_mode.setObjectName(u"label_threading_mode")
        sizePolicy2.setHeightForWidth(self.label_threading_mode.sizePolicy().hasHeightForWidth())
        self.label_threading_mode.setSizePolicy(sizePolicy2)

        self.horizontallayout_threading_mode.addWidget(self.label_threading_mode)

        self.radio_threading_mode_high_performance = QRadioButton(self.groupbox_performance)
        self.radio_threading_mode_high_performance.setObjectName(u"radio_threading_mode_high_performance")
        self.radio_threading_mode_high_performance.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.radio_threading_mode_high_performance)

        self.radio_threading_mode_ffmpeg = QRadioButton(self.groupbox_performance)
        self.radio_threading_mode_ffmpeg.setObjectName(u"radio_threading_mode_ffmpeg")
        self.radio_threading_mode_ffmpeg.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.radio_threading_mode_ffmpeg)

        self.radio_threading_mode_default = QRadioButton(self.groupbox_performance)
        self.radio_threading_mode_default.setObjectName(u"radio_threading_mode_default")
        self.radio_threading_mode_default.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_threading_mode.addWidget(self.radio_threading_mode_default)

        self.button_threading_mode_help = QPushButton(self.groupbox_performance)
        self.button_threading_mode_help.setObjectName(u"button_threading_mode_help")
        self.button_threading_mode_help.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.spinbox_maximal_timeout.setMaximum(30)

        self.horizontallayout_maximal_timeout.addWidget(self.spinbox_maximal_timeout)

        self.button_timeout_help = QPushButton(self.groupbox_performance)
        self.button_timeout_help.setObjectName(u"button_timeout_help")
        self.button_timeout_help.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_maximal_timeout.addWidget(self.button_timeout_help)


        self.gridLayout_9.addLayout(self.horizontallayout_maximal_timeout, 5, 0, 1, 1)


        self.gridlayout_settings.addWidget(self.groupbox_performance, 0, 0, 1, 1)


        self.gridLayout_34.addLayout(self.gridlayout_settings, 0, 0, 1, 1)

        self.horizontallayout_settings_apply = QHBoxLayout()
        self.horizontallayout_settings_apply.setObjectName(u"horizontallayout_settings_apply")
        self.button_settings_apply = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_settings_apply.setObjectName(u"button_settings_apply")
        self.button_settings_apply.setCursor(QCursor(Qt.PointingHandCursor))

        self.horizontallayout_settings_apply.addWidget(self.button_settings_apply)

        self.button_settings_reset = QPushButton(self.scrollAreaWidgetContents_6)
        self.button_settings_reset.setObjectName(u"button_settings_reset")
        self.button_settings_reset.setCursor(QCursor(Qt.PointingHandCursor))
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


        self.gridLayout_34.addLayout(self.horizontallayout_settings_apply, 3, 0, 1, 1)

        self.scrollarea_settings.setWidget(self.scrollAreaWidgetContents_6)

        self.gridLayout_25.addWidget(self.scrollarea_settings, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_settings)
        self.page_credits = QWidget()
        self.page_credits.setObjectName(u"page_credits")
        self.gridLayout_26 = QGridLayout(self.page_credits)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.gridlayout_textbrowser = QGridLayout()
        self.gridlayout_textbrowser.setObjectName(u"gridlayout_textbrowser")
        self.textBrowser = QTextBrowser(self.page_credits)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridlayout_textbrowser.addWidget(self.textBrowser, 0, 0, 1, 1)


        self.gridLayout_26.addLayout(self.gridlayout_textbrowser, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_credits)
        self.page_metadata = QWidget()
        self.page_metadata.setObjectName(u"page_metadata")
        self.gridLayout_32 = QGridLayout(self.page_metadata)
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.verticallayout_metadata = QVBoxLayout()
        self.verticallayout_metadata.setObjectName(u"verticallayout_metadata")
        self.scrollarea_metadata = QScrollArea(self.page_metadata)
        self.scrollarea_metadata.setObjectName(u"scrollarea_metadata")
        self.scrollarea_metadata.setWidgetResizable(True)
        self.scrollAreaWidgetContents_4 = QWidget()
        self.scrollAreaWidgetContents_4.setObjectName(u"scrollAreaWidgetContents_4")
        self.scrollAreaWidgetContents_4.setGeometry(QRect(0, 0, 232, 978))
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
        self.lineedit_user_interests_hobbies.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_interests_hobbies, 18, 1, 1, 1)

        self.lineedit_user_birth_place = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_birth_place.setObjectName(u"lineedit_user_birth_place")
        self.lineedit_user_birth_place.setReadOnly(True)

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
        self.lineedit_user_video_views.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_video_views, 10, 1, 1, 1)

        self.label_piercings = QLabel(self.scrollAreaWidgetContents_4)
        self.label_piercings.setObjectName(u"label_piercings")

        self.gridlayout_user_metadata.addWidget(self.label_piercings, 1, 0, 1, 1)

        self.lineedit_user_tattoos = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_tattoos.setObjectName(u"lineedit_user_tattoos")
        self.lineedit_user_tattoos.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_tattoos, 22, 1, 1, 1)

        self.label_ethnicity = QLabel(self.scrollAreaWidgetContents_4)
        self.label_ethnicity.setObjectName(u"label_ethnicity")

        self.gridlayout_user_metadata.addWidget(self.label_ethnicity, 14, 0, 1, 1)

        self.lineedit_user_turn_ons = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_turn_ons.setObjectName(u"lineedit_user_turn_ons")
        self.lineedit_user_turn_ons.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_turn_ons, 5, 1, 1, 1)

        self.lineedit_user_fake_boobs = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_fake_boobs.setObjectName(u"lineedit_user_fake_boobs")
        self.lineedit_user_fake_boobs.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_fake_boobs, 3, 1, 1, 1)

        self.lineedit_user_profile_views = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_profile_views.setObjectName(u"lineedit_user_profile_views")
        self.lineedit_user_profile_views.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_profile_views, 15, 1, 1, 1)

        self.lineedit_user_gender = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_gender.setObjectName(u"lineedit_user_gender")
        self.lineedit_user_gender.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_gender, 4, 1, 1, 1)

        self.lineedit_user_ethnicity = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_ethnicity.setObjectName(u"lineedit_user_ethnicity")
        self.lineedit_user_ethnicity.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_ethnicity, 14, 1, 1, 1)

        self.lineedit_user_interested_in = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_interested_in.setObjectName(u"lineedit_user_interested_in")
        self.lineedit_user_interested_in.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_interested_in, 2, 1, 1, 1)

        self.lineedit_user_videos_watched = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_videos_watched.setObjectName(u"lineedit_user_videos_watched")
        self.lineedit_user_videos_watched.setReadOnly(True)

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
        self.lineedit_user_name.setReadOnly(True)

        self.gridlayout_vieo_metadata.addWidget(self.lineedit_user_name, 1, 1, 1, 1)

        self.label_user_type = QLabel(self.scrollAreaWidgetContents_4)
        self.label_user_type.setObjectName(u"label_user_type")

        self.gridlayout_vieo_metadata.addWidget(self.label_user_type, 2, 0, 1, 1)

        self.label_name = QLabel(self.scrollAreaWidgetContents_4)
        self.label_name.setObjectName(u"label_name")

        self.gridlayout_vieo_metadata.addWidget(self.label_name, 1, 0, 1, 1)

        self.lineedit_user_type = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_type.setObjectName(u"lineedit_user_type")
        self.lineedit_user_type.setReadOnly(True)

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
        self.lineedit_video_title.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_title, 0, 1, 1, 1)

        self.lineedit_video_views = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_views.setObjectName(u"lineedit_video_views")
        self.lineedit_video_views.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_views, 2, 1, 1, 1)

        self.label_video_rating = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_rating.setObjectName(u"label_video_rating")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_rating, 5, 0, 1, 1)

        self.label_video_duration = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_duration.setObjectName(u"label_video_duration")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_duration, 4, 0, 1, 1)

        self.lineedit_video_tags = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_tags.setObjectName(u"lineedit_video_tags")
        self.lineedit_video_tags.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_tags, 3, 1, 1, 1)

        self.label_video_views_2 = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_views_2.setObjectName(u"label_video_views_2")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_views_2, 2, 0, 1, 1)

        self.lineedit_video_hotspots = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_hotspots.setObjectName(u"lineedit_video_hotspots")
        self.lineedit_video_hotspots.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_hotspots, 1, 1, 1, 1)

        self.lineedit_video_duration = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_duration.setObjectName(u"lineedit_video_duration")
        self.lineedit_video_duration.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_duration, 4, 1, 1, 1)

        self.label_video_pornstars = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_pornstars.setObjectName(u"label_video_pornstars")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_pornstars, 6, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.girdlayout_pure_video_metadata.addItem(self.verticalSpacer_3, 9, 0, 1, 1)

        self.lineedit_video_rating = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_rating.setObjectName(u"lineedit_video_rating")
        self.lineedit_video_rating.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_rating, 5, 1, 1, 1)

        self.label_video_hotspots = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_hotspots.setObjectName(u"label_video_hotspots")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_hotspots, 1, 0, 1, 1)

        self.lineedit_video_pornstars = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_pornstars.setObjectName(u"lineedit_video_pornstars")
        self.lineedit_video_pornstars.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_pornstars, 6, 1, 1, 1)

        self.label_video_orientation = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_orientation.setObjectName(u"label_video_orientation")

        self.girdlayout_pure_video_metadata.addWidget(self.label_video_orientation, 7, 0, 1, 1)

        self.lineedit_video_orientation = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_video_orientation.setObjectName(u"lineedit_video_orientation")
        self.lineedit_video_orientation.setReadOnly(True)

        self.girdlayout_pure_video_metadata.addWidget(self.lineedit_video_orientation, 7, 1, 1, 1)


        self.gridlayout_vieo_metadata.addLayout(self.girdlayout_pure_video_metadata, 6, 0, 1, 2)


        self.gridlayout_user_metadata.addLayout(self.gridlayout_vieo_metadata, 23, 0, 1, 4)

        self.label_widght = QLabel(self.scrollAreaWidgetContents_4)
        self.label_widght.setObjectName(u"label_widght")

        self.gridlayout_user_metadata.addWidget(self.label_widght, 9, 0, 1, 1)

        self.lineedit_user_relationship = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_relationship.setObjectName(u"lineedit_user_relationship")
        self.lineedit_user_relationship.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_relationship, 0, 1, 1, 1)

        self.label_relationship = QLabel(self.scrollAreaWidgetContents_4)
        self.label_relationship.setObjectName(u"label_relationship")

        self.gridlayout_user_metadata.addWidget(self.label_relationship, 0, 0, 1, 1)

        self.lineedit_user_piercings = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_piercings.setObjectName(u"lineedit_user_piercings")
        self.lineedit_user_piercings.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_piercings, 1, 1, 1, 1)

        self.lineedit_user_weight = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_weight.setObjectName(u"lineedit_user_weight")
        self.lineedit_user_weight.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_weight, 9, 1, 1, 1)

        self.lineedit_user_home_town = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_home_town.setObjectName(u"lineedit_user_home_town")
        self.lineedit_user_home_town.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_home_town, 21, 1, 1, 1)

        self.lineedit_user_city_country = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_city_country.setObjectName(u"lineedit_user_city_country")
        self.lineedit_user_city_country.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_city_country, 19, 1, 1, 1)

        self.lineedit_user_height = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_height.setObjectName(u"lineedit_user_height")
        self.lineedit_user_height.setReadOnly(True)

        self.gridlayout_user_metadata.addWidget(self.lineedit_user_height, 7, 1, 1, 1)

        self.label_video_views = QLabel(self.scrollAreaWidgetContents_4)
        self.label_video_views.setObjectName(u"label_video_views")

        self.gridlayout_user_metadata.addWidget(self.label_video_views, 10, 0, 1, 1)

        self.lineedit_user_turn_offs = QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineedit_user_turn_offs.setObjectName(u"lineedit_user_turn_offs")
        self.lineedit_user_turn_offs.setReadOnly(True)

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
        self.lineedit_user_hair_color.setReadOnly(True)

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

        self.stacked_widget_main.addWidget(self.page_metadata)
        self.page_supported_websites = QWidget()
        self.page_supported_websites.setObjectName(u"page_supported_websites")
        self.gridLayout_11 = QGridLayout(self.page_supported_websites)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.stackedWidget = QStackedWidget(self.page_supported_websites)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_i_dont_know = QWidget()
        self.page_i_dont_know.setObjectName(u"page_i_dont_know")
        self.gridLayout_3 = QGridLayout(self.page_i_dont_know)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textbrowser_websites = QTextBrowser(self.page_i_dont_know)
        self.textbrowser_websites.setObjectName(u"textbrowser_websites")

        self.verticalLayout.addWidget(self.textbrowser_websites)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_i_dont_know)
        self.page_nothing_3 = QWidget()
        self.page_nothing_3.setObjectName(u"page_nothing_3")
        self.stackedWidget.addWidget(self.page_nothing_3)

        self.gridLayout_11.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_supported_websites)

        self.gridLayout_13.addWidget(self.stacked_widget_main, 1, 0, 1, 1)


        self.main_gridlayout.addWidget(self.main_widget, 0, 1, 1, 1)


        self.gridLayout_16.addLayout(self.main_gridlayout, 0, 0, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(0)
        self.stacked_widget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn Fetch V3.1 (C) Johannes Habel GPL 3", None))
        self.button_switch_home.setText("")
        self.button_switch_account.setText("")
        self.button_switch_tools.setText("")
        self.button_switch_settings.setText("")
        self.button_switch_metadata.setText("")
        self.button_switch_credits.setText("")
        self.label_total_progress.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_progress_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub:", None))
        self.label_progress_xnxx.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XNXX", None))
        self.label_progress_information.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Information: The total progressbar only counts the total progress of all PornHub videos being downloaded.", None))
        self.label_progress_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Eporner", None))
        self.label_progress_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner:", None))
        self.label_progress_xvideos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XVideos", None))
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
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.lineedit_search_query.setText("")
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search for Videos. Select Website below", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.label_search_website.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Website", None))
        self.button_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.button_model.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineedit_file.setText("")
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"URLs in the file must be separated with new lines!", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter Model / Channel / Actress name", None))
        self.labell_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.radio_search_website_pornhub.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub", None))
        self.radio_search_website_hqporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner", None))
        self.radio_search_website_xvideos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"XVideos", None))
        self.radio_search_website_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"EPorner", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter video URL", None))
        self.button_open_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.button_switch_supported_websites.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"See Supported Websites", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
        self.button_get_liked_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.button_get_watched_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.button_get_recommended_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.groupBox.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"HQPorner", None))
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
        self.groupBox_2.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"EPorner", None))
        self.label_videos_by_category_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get videos by category", None))
        self.button_eporner_category_get_videos.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.button_list_categories_eporner.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"List of all categories", None))
        self.goroupbox_gui.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface", None))
        self.radio_ui_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_ui_language_system_default.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"System default", None))
        self.radio_ui_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.radio_ui_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.label_ui_language.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Graphical User Interface Language:", None))
        self.radio_ui_language_chinese_simplified.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese (simplified)", None))
        self.groupbox_videos.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Videos", None))
        self.label_searching_limit.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Result Limit:", None))
        self.button_result_limit_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_directory_system.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Use Directory system? ", None))
        self.radio_directory_system_yes.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Yes", None))
        self.radio_directory_system_no.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"No", None))
        self.button_directory_system_help.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Help", None))
        self.label_quality.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Quality:", None))
        self.radio_quality_best.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Best", None))
        self.radio_quality_half.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Half", None))
        self.radio_quality_worst.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Worst", None))
        self.label_output_path.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Output path:", None))
        self.lineedit_output_path.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter \"./\" for current directory", None))
        self.button_output_path_select.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open", None))
        self.radio_api_language_chinese.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Chinese", None))
        self.radio_api_language_french.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"French", None))
        self.radio_api_language_english.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"English", None))
        self.radio_api_language_spanish.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Spanish", None))
        self.radio_api_language_portuguese.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Portuguese", None))
        self.radio_api_language_japanese.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Japanese", None))
        self.radio_api_language_italian.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Italian", None))
        self.radio_api_language_czech.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Czech", None))
        self.radio_api_language_german.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"German", None))
        self.radio_api_language_dutch.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Dutch", None))
        self.radio_api_language_russian.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Russian", None))
        self.label_api_language.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PornHub Language (affects video titles)", None))
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
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Apply  (needs restart)", None))
        self.button_settings_reset.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Reset Porn Fetch to default settings", None))
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
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All sites support threaded "
                        "downloads and selectable quality!</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Model / Channel Downloads</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- PornHub.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- HQPorner.com</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left"
                        ":0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Searching:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- PornHub.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- HQPorner.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Xvideos.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- Eporner.com</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:"
                        "0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">I am constantly working to support more websites.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; "
                        "margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

