# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_license.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QScrollArea,
    QSizePolicy, QTextBrowser, QWidget)

class Ui_SetupLicense(object):
    def setupUi(self, SetupLicense):
        if not SetupLicense.objectName():
            SetupLicense.setObjectName(u"SetupLicense")
        SetupLicense.resize(1120, 556)
        SetupLicense.setStyleSheet(u"background-color: rgb(68, 68, 68);\n"
"color: white;")
        self.gridLayout_2 = QGridLayout(SetupLicense)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.scrollArea = QScrollArea(SetupLicense)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1116, 552))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.button_accept = QPushButton(self.scrollAreaWidgetContents)
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

        self.gridLayout_3.addWidget(self.button_accept, 1, 0, 1, 1)

        self.button_deny = QPushButton(self.scrollAreaWidgetContents)
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

        self.gridLayout_3.addWidget(self.button_deny, 1, 1, 1, 1)

        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_3.addWidget(self.textBrowser, 0, 0, 1, 2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(SetupLicense)

        QMetaObject.connectSlotsByName(SetupLicense)
    # setupUi

    def retranslateUi(self, SetupLicense):
        SetupLicense.setWindowTitle(QCoreApplication.translate("SetupLicense", u"Porn Fetch License Agreement (GPLv3)", None))
        self.button_accept.setText(QCoreApplication.translate("SetupLicense", u"Accept", None))
        self.button_deny.setText(QCoreApplication.translate("SetupLicense", u"Deny and Exit", None))
        self.textBrowser.setHtml(QCoreApplication.translate("SetupLicense", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">GPL License Agreement for Porn Fetch</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program is free software: you may redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, ei"
                        "ther version 3 of the License or (at your option) any later version.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This program is distributed in the hope that it will be useful, but it is provided <span style=\" font-weight:700;\">&quot;AS IS&quot; WITHOUT ANY WARRANTY</span>; without even the implied warranties of <span style=\" font-weight:700;\">MERCHANTABILITY</span> or <span style=\" font-weight:700;\">FITNESS FOR A PARTICULAR PURPOSE</span>. For more details, see the GNU General Public License.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You should have received a copy of the GNU General Public License along with this program. If not, visit <a href=\"https://www.gnu.org/licenses/\"><span style=\" text-decoration: underline; color:#0000ff;\">https://www.gnu.org/licenses/</span></a>.</p>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; marg"
                        "in-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Limitation of Liability</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Under no circumstances and under no legal theory\u2014whether in tort, contract, or otherwise\u2014shall the copyright holder or contributors be held liable for any direct, indirect, special, incidental, consequential, or exemplary damages of any kind. This includes, but is not limited to: damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data, or any other commercial damages or losses, even if such parties were informed of the possibility of such damages.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This limitation does not apply to liability for death or personal injury resulting from the"
                        " negligence of such parties, where applicable law prohibits such a limitation. In some jurisdictions, the exclusion or limitation of incidental or consequential damages is not allowed. Therefore, these exclusions may not apply to you.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This Agreement constitutes the complete and exclusive understanding between the parties regarding the subject matter contained herein.</p>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Disclaimer</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Porn Fetch violates the Terms of Service of all the websites it supports, including but not limited to:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px;"
                        " margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">spankbang.com</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">pornhub.com</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">hqporner.com</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">eporner.com</li>\n"
"<li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">xnxx.com</li>\n"
"<li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">xvideos.com</li></ul>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-inde"
                        "nt:0px;\"><span style=\" font-weight:700;\">Usage Warning:</span> Using Porn Fetch may result in legal action being taken against you. The creator of this software is not liable for any damages or legal consequences resulting from its use.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Porn Fetch was created solely for the purpose of enabling offline access to videos in scenarios where internet access is unavailable. <span style=\" font-weight:700;\">The redistribution of copyright-protected content obtained through Porn Fetch is strictly forbidden.</span> Any misuse of this software to steal and redistribute copyrighted material is against its intended purpose and is not endorsed by the creator.</p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The batch processing feature in Porn Fetch is intended to assist users without graphical user interfaces"
                        " in downloading content for personal use, not for large-scale video theft or redistribution.</p>\n"
"<hr />\n"
"<h2 style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Third-Party Software</span></h2>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Porn Fetch utilizes FFmpeg for video processing and conversion. FFmpeg is free software licensed under the GPL. For more information about FFmpeg, visit <a href=\"https://ffmpeg.org\"><span style=\" text-decoration: underline; color:#0000ff;\">https://ffmpeg.org</span></a>.</p></body></html>", None))
    # retranslateUi

