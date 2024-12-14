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
        font = QFont()
        font.setFamilies([u"JetBrainsMono Nerd Font Propo"])
        font.setPointSize(11)
        font.setKerning(True)
        self.textBrowser.setFont(font)

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
"</style></head><body style=\" font-family:'JetBrainsMono Nerd Font Propo'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:22pt;\">GPL License Agreement for Porn Fetch</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">This program is free software: you may redistribute it and/or mod"
                        "ify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License or (at your option) any later version.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">This program is distributed in the hope that it will be useful, but it is provided &quot;AS IS&quot; WITHOUT ANY WARRANTY; without even the implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. For more details, see the GNU General Public License.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">You should have received a copy of the GNU General Public License along with this program. If not, visit https://www.gnu.org/licenses/.</span></p>\n"
"<p style=\" mar"
                        "gin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt; color:#a51d2d;\">Limitation of Liability</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt; text-decoration: underline;\">Under no circumstances and under no legal theory\u2014whether in tort, contract, or otherwise\u2014shall the copyright holder or contributors be held liable for any direct, indirect, special, incidental, consequential, or exemplary damages of any kind. This includes, but is not limited to: damages for loss of goodwill, work stoppage, computer failure or malfunction, loss of data, or any other commercial damages or losses, even if such parties were informed of the possibility of such damages.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left"
                        ":0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">This limitation does not apply to liability for death or personal injury resulting from the negligence of such parties, where applicable law prohibits such a limitation. In some jurisdictions, the exclusion or limitation of incidental or consequential damages is not allowed. Therefore, these exclusions may not apply to you.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">This Agreement constitutes the complete and exclusive understanding between the parties regarding the subject matter contained herein.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; m"
                        "argin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">Disclaimer</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">Porn Fetch violates the Terms of Service of all the websites it supports, including but not limited to:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">spankbang.com</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">pornhub.com</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">hqporner.com</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">eporner.com</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">xnxx.com</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">xvideos.com</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">Usage Warning: <br /></span><span st"
                        "yle=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt; text-decoration: underline;\">Using Porn Fetch may result in legal action being taken against you. The creator of this software is not liable for any damages or legal consequences resulting from its use.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt; text-decoration: underline;\">Porn Fetch was created solely for the purpose of enabling offline access to videos in scenarios where internet access is unavailable. The redistribution of copyright-protected content obtained through Porn Fetch is strictly forbidden. Any misuse of this software to steal and redistribute copyrighted material is against its intended purpose and is not endorsed by the creator.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span sty"
                        "le=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt; text-decoration: underline;\">The batch processing feature in Porn Fetch is intended to assist users without graphical user interfaces in downloading content for personal use, not for large-scale video theft or redistribution.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:14pt;\">Third-Party Software</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">Porn Fetch utilizes FFmpeg for video processing and conversion. FFmpeg is free software license"
                        "d under the GPL. For more information about FFmpeg, visit https://ffmpeg.org.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Droid Naskh Shift Alt'; font-size:12pt;\">The JetBrains Mono font is used in this application. Copyright \u00a9 2019 JetBrains. All Rights Reserved. Licensed under the SIL Open Font License, Version 1.1. You can find a copy of the license at: https://scripts.sil.org/OFL</span></p></body></html>", None))
    # retranslateUi

