# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_range_selector.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
    QPushButton, QSizePolicy, QSpinBox, QTextBrowser,
    QWidget)

class Ui_PornFetchRangeSelector(object):
    def setupUi(self, PornFetchRangeSelector):
        if not PornFetchRangeSelector.objectName():
            PornFetchRangeSelector.setObjectName(u"PornFetchRangeSelector")
        PornFetchRangeSelector.resize(729, 385)
        self.gridLayout_2 = QGridLayout(PornFetchRangeSelector)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.textbrowser_range = QTextBrowser(PornFetchRangeSelector)
        self.textbrowser_range.setObjectName(u"textbrowser_range")

        self.gridLayout.addWidget(self.textbrowser_range, 0, 0, 1, 5)

        self.button_range_apply_time = QPushButton(PornFetchRangeSelector)
        self.button_range_apply_time.setObjectName(u"button_range_apply_time")

        self.gridLayout.addWidget(self.button_range_apply_time, 5, 4, 1, 1)

        self.label_apply_by_time = QLabel(PornFetchRangeSelector)
        self.label_apply_by_time.setObjectName(u"label_apply_by_time")

        self.gridLayout.addWidget(self.label_apply_by_time, 4, 0, 1, 4)

        self.lineedit_range_start = QLineEdit(PornFetchRangeSelector)
        self.lineedit_range_start.setObjectName(u"lineedit_range_start")

        self.gridLayout.addWidget(self.lineedit_range_start, 5, 1, 1, 1)

        self.lineedit_range_author = QLineEdit(PornFetchRangeSelector)
        self.lineedit_range_author.setObjectName(u"lineedit_range_author")

        self.gridLayout.addWidget(self.lineedit_range_author, 1, 1, 1, 1)

        self.spinbox_range_end = QSpinBox(PornFetchRangeSelector)
        self.spinbox_range_end.setObjectName(u"spinbox_range_end")

        self.gridLayout.addWidget(self.spinbox_range_end, 9, 3, 1, 1)

        self.label_apply_by_index = QLabel(PornFetchRangeSelector)
        self.label_apply_by_index.setObjectName(u"label_apply_by_index")

        self.gridLayout.addWidget(self.label_apply_by_index, 6, 0, 1, 4)

        self.label_range_end = QLabel(PornFetchRangeSelector)
        self.label_range_end.setObjectName(u"label_range_end")

        self.gridLayout.addWidget(self.label_range_end, 9, 2, 1, 1)

        self.button_range_apply_index = QPushButton(PornFetchRangeSelector)
        self.button_range_apply_index.setObjectName(u"button_range_apply_index")

        self.gridLayout.addWidget(self.button_range_apply_index, 9, 4, 1, 1)

        self.label_range_time_end = QLabel(PornFetchRangeSelector)
        self.label_range_time_end.setObjectName(u"label_range_time_end")

        self.gridLayout.addWidget(self.label_range_time_end, 5, 2, 1, 1)

        self.label_range_start = QLabel(PornFetchRangeSelector)
        self.label_range_start.setObjectName(u"label_range_start")

        self.gridLayout.addWidget(self.label_range_start, 9, 0, 1, 1)

        self.button_range_apply_author = QPushButton(PornFetchRangeSelector)
        self.button_range_apply_author.setObjectName(u"button_range_apply_author")

        self.gridLayout.addWidget(self.button_range_apply_author, 1, 2, 1, 3)

        self.spinbox_range_start = QSpinBox(PornFetchRangeSelector)
        self.spinbox_range_start.setObjectName(u"spinbox_range_start")

        self.gridLayout.addWidget(self.spinbox_range_start, 9, 1, 1, 1)

        self.lineedit_range_end = QLineEdit(PornFetchRangeSelector)
        self.lineedit_range_end.setObjectName(u"lineedit_range_end")

        self.gridLayout.addWidget(self.lineedit_range_end, 5, 3, 1, 1)

        self.label_range_time_start = QLabel(PornFetchRangeSelector)
        self.label_range_time_start.setObjectName(u"label_range_time_start")

        self.gridLayout.addWidget(self.label_range_time_start, 5, 0, 1, 1)

        self.label_range_by_author = QLabel(PornFetchRangeSelector)
        self.label_range_by_author.setObjectName(u"label_range_by_author")

        self.gridLayout.addWidget(self.label_range_by_author, 1, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(PornFetchRangeSelector)

        QMetaObject.connectSlotsByName(PornFetchRangeSelector)
    # setupUi

    def retranslateUi(self, PornFetchRangeSelector):
        PornFetchRangeSelector.setWindowTitle(QCoreApplication.translate("PornFetchRangeSelector", u"Video selector...", None))
        self.textbrowser_range.setHtml(QCoreApplication.translate("PornFetchRangeSelector", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">Select the range of videos to be automatically selected.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; te"
                        "xt-indent:0px;\"><span style=\" font-family:'Segoe UI';\">For example, if you set the start to 5 and the end to 20, then all videos between 5-20 will be checked for downloading :)</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">Or select by a range in time:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">For example if you want to download all videos in between 10 and 20 minutes do:</span></p>\n"
""
                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">Start: 10</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">End: 20</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI';\">And click Apply.</span></p></body></html>", None))
        self.button_range_apply_time.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Apply", None))
        self.label_apply_by_time.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Apply by time:", None))
        self.lineedit_range_start.setText(QCoreApplication.translate("PornFetchRangeSelector", u"0", None))
        self.lineedit_range_author.setPlaceholderText(QCoreApplication.translate("PornFetchRangeSelector", u"Enter the author's name", None))
        self.label_apply_by_index.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Apply by Index:", None))
        self.label_range_end.setText(QCoreApplication.translate("PornFetchRangeSelector", u"End:", None))
        self.button_range_apply_index.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Apply", None))
        self.label_range_time_end.setText(QCoreApplication.translate("PornFetchRangeSelector", u"End:", None))
        self.label_range_start.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Start:", None))
        self.button_range_apply_author.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Apply", None))
        self.lineedit_range_end.setText(QCoreApplication.translate("PornFetchRangeSelector", u"0", None))
        self.label_range_time_start.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Start:", None))
        self.label_range_by_author.setText(QCoreApplication.translate("PornFetchRangeSelector", u"Apply by author:", None))
    # retranslateUi

