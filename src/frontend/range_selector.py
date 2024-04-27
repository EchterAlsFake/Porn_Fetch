# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'range_selector.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpinBox, QTextBrowser, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(421, 157)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.spinbox_range_end = QSpinBox(Form)
        self.spinbox_range_end.setObjectName(u"spinbox_range_end")

        self.gridLayout.addWidget(self.spinbox_range_end, 1, 3, 1, 1)

        self.textbrowser_range = QTextBrowser(Form)
        self.textbrowser_range.setObjectName(u"textbrowser_range")

        self.gridLayout.addWidget(self.textbrowser_range, 0, 0, 1, 4)

        self.label_range_start = QLabel(Form)
        self.label_range_start.setObjectName(u"label_range_start")

        self.gridLayout.addWidget(self.label_range_start, 1, 0, 1, 1)

        self.label_range_end = QLabel(Form)
        self.label_range_end.setObjectName(u"label_range_end")

        self.gridLayout.addWidget(self.label_range_end, 1, 2, 1, 1)

        self.spinbox_range_start = QSpinBox(Form)
        self.spinbox_range_start.setObjectName(u"spinbox_range_start")

        self.gridLayout.addWidget(self.spinbox_range_start, 1, 1, 1, 1)

        self.button_range_apply_everything = QPushButton(Form)
        self.button_range_apply_everything.setObjectName(u"button_range_apply_everything")

        self.gridLayout.addWidget(self.button_range_apply_everything, 2, 2, 1, 2)

        self.button_range_apply = QPushButton(Form)
        self.button_range_apply.setObjectName(u"button_range_apply")

        self.gridLayout.addWidget(self.button_range_apply, 2, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Video selector...", None))
        self.textbrowser_range.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">Select the range of videos to be automatically selected.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:9pt;\">For example, if you set the start to 5 and the end to 20, then"
                        " all videos between 5-20 will be checked for downloading :)</span></p></body></html>", None))
        self.label_range_start.setText(QCoreApplication.translate("Form", u"Start:", None))
        self.label_range_end.setText(QCoreApplication.translate("Form", u"End:", None))
        self.button_range_apply_everything.setText(QCoreApplication.translate("Form", u"Select everything", None))
        self.button_range_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
    # retranslateUi

