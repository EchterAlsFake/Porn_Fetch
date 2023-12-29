# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStackedWidget, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Porn_Fetch(object):
    def setupUi(self, Porn_Fetch):
        if not Porn_Fetch.objectName():
            Porn_Fetch.setObjectName(u"Porn_Fetch")
        Porn_Fetch.resize(1628, 663)
        self.gridLayout_3 = QGridLayout(Porn_Fetch)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget = QWidget(Porn_Fetch)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_home = QPushButton(self.widget)
        self.button_home.setObjectName(u"button_home")
        self.button_home.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_home)

        self.button_account = QPushButton(self.widget)
        self.button_account.setObjectName(u"button_account")
        self.button_account.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_account)

        self.button_metadata = QPushButton(self.widget)
        self.button_metadata.setObjectName(u"button_metadata")
        self.button_metadata.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_metadata)

        self.button_credits = QPushButton(self.widget)
        self.button_credits.setObjectName(u"button_credits")
        self.button_credits.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.button_credits)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 2, 1)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_3 = QLabel(Porn_Fetch)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(Porn_Fetch)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 1)

        self.progressbar_pornhub = QProgressBar(Porn_Fetch)
        self.progressbar_pornhub.setObjectName(u"progressbar_pornhub")
        self.progressbar_pornhub.setValue(0)

        self.gridLayout_6.addWidget(self.progressbar_pornhub, 0, 1, 1, 1)

        self.progressbar_total = QProgressBar(Porn_Fetch)
        self.progressbar_total.setObjectName(u"progressbar_total")
        self.progressbar_total.setValue(0)

        self.gridLayout_6.addWidget(self.progressbar_total, 1, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_6, 1, 1, 1, 1)

        self.stackedWidget = QStackedWidget(Porn_Fetch)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_7 = QGridLayout(self.page)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.button_download = QPushButton(self.page)
        self.button_download.setObjectName(u"button_download")

        self.gridLayout_2.addWidget(self.button_download, 0, 2, 1, 1)

        self.lineedit_video_url = QLineEdit(self.page)
        self.lineedit_video_url.setObjectName(u"lineedit_video_url")

        self.gridLayout_2.addWidget(self.lineedit_video_url, 0, 1, 1, 1)

        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")

        self.gridLayout_2.addWidget(self.lineedit_model_url, 1, 1, 1, 1)

        self.button_get_model_videos = QPushButton(self.page)
        self.button_get_model_videos.setObjectName(u"button_get_model_videos")

        self.gridLayout_2.addWidget(self.button_get_model_videos, 1, 2, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.button_unselect_all = QPushButton(self.page)
        self.button_unselect_all.setObjectName(u"button_unselect_all")

        self.gridLayout_4.addWidget(self.button_unselect_all, 1, 2, 1, 1)

        self.button_download_tree_widget = QPushButton(self.page)
        self.button_download_tree_widget.setObjectName(u"button_download_tree_widget")

        self.gridLayout_4.addWidget(self.button_download_tree_widget, 1, 0, 1, 1)

        self.button_select_all = QPushButton(self.page)
        self.button_select_all.setObjectName(u"button_select_all")

        self.gridLayout_4.addWidget(self.button_select_all, 1, 1, 1, 1)

        self.scrollArea = QScrollArea(self.page)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1482, 464))
        self.gridLayout_5 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.treeWidget = QTreeWidget(self.scrollAreaWidgetContents)
        self.treeWidget.setObjectName(u"treeWidget")

        self.gridLayout_5.addWidget(self.treeWidget, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 3)


        self.gridLayout_7.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_3.addWidget(self.stackedWidget, 0, 1, 1, 1)


        self.retranslateUi(Porn_Fetch)

        QMetaObject.connectSlotsByName(Porn_Fetch)
    # setupUi

    def retranslateUi(self, Porn_Fetch):
        Porn_Fetch.setWindowTitle(QCoreApplication.translate("Porn_Fetch", u"Porn_Fetch", None))
        self.button_home.setText("")
        self.button_account.setText(QCoreApplication.translate("Porn_Fetch", u"D", None))
        self.button_metadata.setText(QCoreApplication.translate("Porn_Fetch", u"PushButton", None))
        self.button_credits.setText(QCoreApplication.translate("Porn_Fetch", u"PushButton", None))
        self.label_3.setText(QCoreApplication.translate("Porn_Fetch", u"Total:", None))
        self.label_4.setText(QCoreApplication.translate("Porn_Fetch", u"PornHub:", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch", u"Video URL:", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch", u"Start", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch", u"Model URL:", None))
        self.button_get_model_videos.setText(QCoreApplication.translate("Porn_Fetch", u"Get videos", None))
        self.button_unselect_all.setText(QCoreApplication.translate("Porn_Fetch", u"Unselect all", None))
        self.button_download_tree_widget.setText(QCoreApplication.translate("Porn_Fetch", u"Download", None))
        self.button_select_all.setText(QCoreApplication.translate("Porn_Fetch", u"Select all", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Porn_Fetch", u"Title", None));
    # retranslateUi

