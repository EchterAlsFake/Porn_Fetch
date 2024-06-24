# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_android.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QStackedWidget, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(462, 721)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Porn_Fetch_Widget.sizePolicy().hasHeightForWidth())
        Porn_Fetch_Widget.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(Porn_Fetch_Widget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.stacked_widget_main = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stacked_widget_top = QStackedWidget(self.page)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout = QGridLayout(self.page_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.label_model_url = QLabel(self.page_3)
        self.label_model_url.setObjectName(u"label_model_url")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_model_url.sizePolicy().hasHeightForWidth())
        self.label_model_url.setSizePolicy(sizePolicy1)
        self.label_model_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_model_url, 2, 0, 1, 1)

        self.lineedit_url = QLineEdit(self.page_3)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy2)
        self.lineedit_url.setMinimumSize(QSize(300, 4))

        self.gridlayout_downloading.addWidget(self.lineedit_url, 0, 1, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page_3)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")
        sizePolicy2.setHeightForWidth(self.lineedit_model_url.sizePolicy().hasHeightForWidth())
        self.lineedit_model_url.setSizePolicy(sizePolicy2)
        self.lineedit_model_url.setMinimumSize(QSize(300, 2))

        self.gridlayout_downloading.addWidget(self.lineedit_model_url, 2, 1, 1, 1)

        self.lineedit_search_query = QLineEdit(self.page_3)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        sizePolicy2.setHeightForWidth(self.lineedit_search_query.sizePolicy().hasHeightForWidth())
        self.lineedit_search_query.setSizePolicy(sizePolicy2)
        self.lineedit_search_query.setMinimumSize(QSize(300, 0))

        self.gridlayout_downloading.addWidget(self.lineedit_search_query, 4, 1, 1, 1)

        self.labell_search = QLabel(self.page_3)
        self.labell_search.setObjectName(u"labell_search")

        self.gridlayout_downloading.addWidget(self.labell_search, 4, 0, 1, 1)

        self.label_playlist_url = QLabel(self.page_3)
        self.label_playlist_url.setObjectName(u"label_playlist_url")

        self.gridlayout_downloading.addWidget(self.label_playlist_url, 1, 0, 1, 1)

        self.lineedit_playlist_url = QLineEdit(self.page_3)
        self.lineedit_playlist_url.setObjectName(u"lineedit_playlist_url")

        self.gridlayout_downloading.addWidget(self.lineedit_playlist_url, 1, 1, 1, 1)

        self.label_file = QLabel(self.page_3)
        self.label_file.setObjectName(u"label_file")
        sizePolicy1.setHeightForWidth(self.label_file.sizePolicy().hasHeightForWidth())
        self.label_file.setSizePolicy(sizePolicy1)
        self.label_file.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_file, 3, 0, 1, 1)

        self.lineedit_file = QLineEdit(self.page_3)
        self.lineedit_file.setObjectName(u"lineedit_file")
        sizePolicy2.setHeightForWidth(self.lineedit_file.sizePolicy().hasHeightForWidth())
        self.lineedit_file.setSizePolicy(sizePolicy2)
        self.lineedit_file.setMinimumSize(QSize(300, 2))
        self.lineedit_file.setReadOnly(True)

        self.gridlayout_downloading.addWidget(self.lineedit_file, 3, 1, 1, 1)

        self.label_url = QLabel(self.page_3)
        self.label_url.setObjectName(u"label_url")
        sizePolicy1.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy1)
        self.label_url.setMinimumSize(QSize(100, 2))

        self.gridlayout_downloading.addWidget(self.label_url, 0, 0, 1, 1)

        self.b = QPushButton(self.page_3)
        self.b.setObjectName(u"b")

        self.gridlayout_downloading.addWidget(self.b, 5, 0, 1, 2)


        self.gridLayout.addLayout(self.gridlayout_downloading, 0, 0, 1, 1)

        self.stacked_widget_top.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stacked_widget_top.addWidget(self.page_4)

        self.gridLayout_2.addWidget(self.stacked_widget_top, 0, 0, 1, 1)

        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.button_tree_settings = QPushButton(self.page)
        self.button_tree_settings.setObjectName(u"button_tree_settings")

        self.gridLayout_17.addWidget(self.button_tree_settings, 2, 2, 1, 2)

        self.button_tree_stop = QPushButton(self.page)
        self.button_tree_stop.setObjectName(u"button_tree_stop")

        self.gridLayout_17.addWidget(self.button_tree_stop, 3, 2, 1, 2)

        self.button_tree_download = QPushButton(self.page)
        self.button_tree_download.setObjectName(u"button_tree_download")
        self.button_tree_download.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_tree_download.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.button_tree_download, 2, 0, 1, 2)

        self.treeWidget = QTreeWidget(self.page)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"Title");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy3)
        self.treeWidget.setMinimumSize(QSize(100, 200))

        self.gridLayout_17.addWidget(self.treeWidget, 1, 0, 1, 4)

        self.button_tree_select_range = QPushButton(self.page)
        self.button_tree_select_range.setObjectName(u"button_tree_select_range")
        self.button_tree_select_range.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_tree_select_range.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.button_tree_select_range, 3, 0, 1, 1)

        self.button_tree_unselect_all = QPushButton(self.page)
        self.button_tree_unselect_all.setObjectName(u"button_tree_unselect_all")
        self.button_tree_unselect_all.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_tree_unselect_all.setStyleSheet(u"")

        self.gridLayout_17.addWidget(self.button_tree_unselect_all, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_17, 1, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stacked_widget_main.addWidget(self.page_2)

        self.gridLayout_3.addWidget(self.stacked_widget_main, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_switch_home = QPushButton(Porn_Fetch_Widget)
        self.button_switch_home.setObjectName(u"button_switch_home")
        sizePolicy.setHeightForWidth(self.button_switch_home.sizePolicy().hasHeightForWidth())
        self.button_switch_home.setSizePolicy(sizePolicy)
        self.button_switch_home.setMinimumSize(QSize(50, 50))
        self.button_switch_home.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"border: none")
        self.button_switch_home.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_home)

        self.button_switch_account = QPushButton(Porn_Fetch_Widget)
        self.button_switch_account.setObjectName(u"button_switch_account")
        sizePolicy.setHeightForWidth(self.button_switch_account.sizePolicy().hasHeightForWidth())
        self.button_switch_account.setSizePolicy(sizePolicy)
        self.button_switch_account.setMinimumSize(QSize(50, 50))
        self.button_switch_account.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_account.setStyleSheet(u"border: none")
        self.button_switch_account.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_account)

        self.button_switch_tools = QPushButton(Porn_Fetch_Widget)
        self.button_switch_tools.setObjectName(u"button_switch_tools")
        sizePolicy.setHeightForWidth(self.button_switch_tools.sizePolicy().hasHeightForWidth())
        self.button_switch_tools.setSizePolicy(sizePolicy)
        self.button_switch_tools.setMinimumSize(QSize(50, 50))
        font = QFont()
        font.setPointSize(9)
        self.button_switch_tools.setFont(font)
        self.button_switch_tools.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_tools.setStyleSheet(u"border: none")
        self.button_switch_tools.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_tools)

        self.button_switch_settings = QPushButton(Porn_Fetch_Widget)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        sizePolicy.setHeightForWidth(self.button_switch_settings.sizePolicy().hasHeightForWidth())
        self.button_switch_settings.setSizePolicy(sizePolicy)
        self.button_switch_settings.setMinimumSize(QSize(50, 50))
        self.button_switch_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"border: none;")
        self.button_switch_settings.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_settings)

        self.button_switch_credits = QPushButton(Porn_Fetch_Widget)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        sizePolicy.setHeightForWidth(self.button_switch_credits.sizePolicy().hasHeightForWidth())
        self.button_switch_credits.setSizePolicy(sizePolicy)
        self.button_switch_credits.setMinimumSize(QSize(50, 50))
        self.button_switch_credits.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"border: none;")
        self.button_switch_credits.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_credits)

        self.pushButton = QPushButton(Porn_Fetch_Widget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton)


        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)


        self.retranslateUi(Porn_Fetch_Widget)

        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Form", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter video URL", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter Model / Channel / Actress URL", None))
        self.lineedit_search_query.setText("")
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search for Videos. Select Website below", None))
        self.labell_search.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.label_playlist_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Playlist URL:", None))
        self.lineedit_playlist_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter a PornHub Playlist URL", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.lineedit_file.setText("")
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"See GitHub for formatting instructions", None))
        self.label_url.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.b.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.button_tree_settings.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.button_tree_stop.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Does not stop downloading videos", None))
#endif // QT_CONFIG(tooltip)
        self.button_tree_stop.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Stop loading videos", None))
        self.button_tree_download.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download Selected Videos", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Porn_Fetch_Widget", u"Duration", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Porn_Fetch_Widget", u"Author", None));
#if QT_CONFIG(tooltip)
        self.button_tree_select_range.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Automatically checks a range of videos", None))
#endif // QT_CONFIG(tooltip)
        self.button_tree_select_range.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Select a range of videos", None))
#if QT_CONFIG(tooltip)
        self.button_tree_unselect_all.setToolTip(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselects all videos in the tree widget", None))
#endif // QT_CONFIG(tooltip)
        self.button_tree_unselect_all.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Unselect all", None))
        self.button_switch_home.setText("")
        self.button_switch_account.setText("")
        self.button_switch_tools.setText("")
        self.button_switch_settings.setText("")
        self.button_switch_credits.setText("")
        self.pushButton.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Progress", None))
    # retranslateUi

