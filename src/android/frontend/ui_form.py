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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QWidget)

class Ui_Porn_Fetch(object):
    def setupUi(self, Porn_Fetch):
        if not Porn_Fetch.objectName():
            Porn_Fetch.setObjectName(u"Porn_Fetch")
        Porn_Fetch.resize(350, 414)
        self.gridLayout_2 = QGridLayout(Porn_Fetch)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineedit_url = QLineEdit(Porn_Fetch)
        self.lineedit_url.setObjectName(u"lineedit_url")

        self.gridLayout.addWidget(self.lineedit_url, 0, 1, 1, 1)

        self.button_download = QPushButton(Porn_Fetch)
        self.button_download.setObjectName(u"button_download")

        self.gridLayout.addWidget(self.button_download, 1, 0, 1, 1)

        self.label = QLabel(Porn_Fetch)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.button_progressbar = QProgressBar(Porn_Fetch)
        self.button_progressbar.setObjectName(u"button_progressbar")
        self.button_progressbar.setValue(24)

        self.gridLayout.addWidget(self.button_progressbar, 1, 1, 1, 2)

        self.button_paste_url = QPushButton(Porn_Fetch)
        self.button_paste_url.setObjectName(u"button_paste_url")

        self.gridLayout.addWidget(self.button_paste_url, 0, 2, 1, 1)

        self.button_output_path = QPushButton(Porn_Fetch)
        self.button_output_path.setObjectName(u"button_output_path")

        self.gridLayout.addWidget(self.button_output_path, 2, 0, 1, 1)

        self.lineedit_output_path = QLineEdit(Porn_Fetch)
        self.lineedit_output_path.setObjectName(u"lineedit_output_path")

        self.gridLayout.addWidget(self.lineedit_output_path, 2, 1, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Porn_Fetch)

        QMetaObject.connectSlotsByName(Porn_Fetch)
    # setupUi

    def retranslateUi(self, Porn_Fetch):
        Porn_Fetch.setWindowTitle(QCoreApplication.translate("Porn_Fetch", u"Porn_Fetch", None))
        self.button_download.setText(QCoreApplication.translate("Porn_Fetch", u"Download", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch", u"Enter / Paste URL", None))
        self.button_paste_url.setText(QCoreApplication.translate("Porn_Fetch", u"Paste URL", None))
        self.button_output_path.setText(QCoreApplication.translate("Porn_Fetch", u"Choose Output Path", None))
    # retranslateUi

