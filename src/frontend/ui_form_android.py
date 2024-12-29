# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_android.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_PornFetch_Android(object):
    def setupUi(self, PornFetch_Android):
        if not PornFetch_Android.objectName():
            PornFetch_Android.setObjectName(u"PornFetch_Android")
        PornFetch_Android.resize(720, 1280)
        PornFetch_Android.setStyleSheet(u"")
        self.gridLayout = QGridLayout(PornFetch_Android)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(6)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridlayout_downloading.setContentsMargins(-1, 14, -1, -1)
        self.button_clipboard = QPushButton(PornFetch_Android)
        self.button_clipboard.setObjectName(u"button_clipboard")

        self.gridlayout_downloading.addWidget(self.button_clipboard, 5, 2, 1, 2)

        self.radioButton_2 = QRadioButton(PornFetch_Android)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridlayout_downloading.addWidget(self.radioButton_2, 3, 1, 1, 1)

        self.radioButton_3 = QRadioButton(PornFetch_Android)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridlayout_downloading.addWidget(self.radioButton_3, 3, 2, 1, 4)

        self.pushButton = QPushButton(PornFetch_Android)
        self.pushButton.setObjectName(u"pushButton")

        self.gridlayout_downloading.addWidget(self.pushButton, 5, 4, 1, 2)

        self.lineedit_url = QLineEdit(PornFetch_Android)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy)
        self.lineedit_url.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.lineedit_url, 2, 1, 1, 5)

        self.button_download = QPushButton(PornFetch_Android)
        self.button_download.setObjectName(u"button_download")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.button_download.sizePolicy().hasHeightForWidth())
        self.button_download.setSizePolicy(sizePolicy1)
        self.button_download.setMinimumSize(QSize(60, 30))
        self.button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.gridlayout_downloading.addWidget(self.button_download, 5, 0, 1, 2)

        self.label_url = QLabel(PornFetch_Android)
        self.label_url.setObjectName(u"label_url")
        sizePolicy1.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy1)
        self.label_url.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.label_url, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.gridlayout_downloading.addLayout(self.horizontalLayout, 9, 0, 1, 6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridlayout_downloading.addItem(self.verticalSpacer, 6, 2, 1, 1)

        self.radioButton = QRadioButton(PornFetch_Android)
        self.radioButton.setObjectName(u"radioButton")

        self.gridlayout_downloading.addWidget(self.radioButton, 4, 4, 1, 1)

        self.lineEdit = QLineEdit(PornFetch_Android)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridlayout_downloading.addWidget(self.lineEdit, 4, 1, 1, 3)


        self.verticalLayout.addLayout(self.gridlayout_downloading)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(PornFetch_Android)

        QMetaObject.connectSlotsByName(PornFetch_Android)
    # setupUi

    def retranslateUi(self, PornFetch_Android):
        PornFetch_Android.setWindowTitle(QCoreApplication.translate("PornFetch_Android", u"UI_android", None))
        self.button_clipboard.setText(QCoreApplication.translate("PornFetch_Android", u"Copy clipbaord", None))
        self.radioButton_2.setText(QCoreApplication.translate("PornFetch_Android", u"Playlist", None))
        self.radioButton_3.setText(QCoreApplication.translate("PornFetch_Android", u"Model URL", None))
        self.pushButton.setText(QCoreApplication.translate("PornFetch_Android", u"Reset URL", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter video URL", None))
        self.button_download.setText(QCoreApplication.translate("PornFetch_Android", u"Download", None))
        self.label_url.setText(QCoreApplication.translate("PornFetch_Android", u"URL:", None))
        self.radioButton.setText(QCoreApplication.translate("PornFetch_Android", u"Video", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"This line will show you debug messages, please read it (only on Android)", None))
    # retranslateUi

