# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_donation.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QPushButton, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_SponsoringDialog(object):
    def setupUi(self, SponsoringDialog):
        if not SponsoringDialog.objectName():
            SponsoringDialog.setObjectName(u"SponsoringDialog")
        SponsoringDialog.resize(800, 600)
        SponsoringDialog.setStyleSheet(u"QWidget {\n"
"    background-color: rgb(35, 35, 35);\n"
"    color: #f8f8f2;\n"
"    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QTextBrowser {\n"
"    background-color: rgb(47, 47, 47)\n"
"    color: #e0e0e0;\n"
"    border: 1px solid #3a3a4a;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3a3f5c;\n"
"    color: #ffffff;\n"
"    border: none;\n"
"    padding: 8px 16px;\n"
"    border-radius: 8px;\n"
"    font-weight: bold;\n"
"    transition: all 0.2s ease-in-out;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #5a5f7a;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2a2f4a;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #444;\n"
"    color: #999;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #cfcfcf;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QStackedWidget {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* Hyperlink style inside QTextBrowser */\n"
"QText"
                        "Browser QTextBrowser {\n"
"    color: #8be9fd;\n"
"}\n"
"\n"
"QTextBrowser a {\n"
"    color: #8be9fd;\n"
"    text-decoration: none;\n"
"}\n"
"\n"
"QTextBrowser a:hover {\n"
"    text-decoration: underline;\n"
"}")
        self.gridLayout_2 = QGridLayout(SponsoringDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.button_donate_kofi = QPushButton(SponsoringDialog)
        self.button_donate_kofi.setObjectName(u"button_donate_kofi")

        self.gridLayout.addWidget(self.button_donate_kofi, 1, 1, 1, 1)

        self.button_donate_already_donated = QPushButton(SponsoringDialog)
        self.button_donate_already_donated.setObjectName(u"button_donate_already_donated")

        self.gridLayout.addWidget(self.button_donate_already_donated, 1, 3, 1, 1)

        self.button_donate_paypal = QPushButton(SponsoringDialog)
        self.button_donate_paypal.setObjectName(u"button_donate_paypal")

        self.gridLayout.addWidget(self.button_donate_paypal, 1, 0, 1, 1)

        self.button_donate_copy_xmr = QPushButton(SponsoringDialog)
        self.button_donate_copy_xmr.setObjectName(u"button_donate_copy_xmr")

        self.gridLayout.addWidget(self.button_donate_copy_xmr, 1, 2, 1, 1)

        self.button_donate_close = QPushButton(SponsoringDialog)
        self.button_donate_close.setObjectName(u"button_donate_close")

        self.gridLayout.addWidget(self.button_donate_close, 1, 4, 1, 1)

        self.textBrowser = QTextBrowser(SponsoringDialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setStyleSheet(u"border-radius: 15px;")
        self.textBrowser.setOpenExternalLinks(True)

        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 5)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(SponsoringDialog)

        QMetaObject.connectSlotsByName(SponsoringDialog)
    # setupUi

    def retranslateUi(self, SponsoringDialog):
        SponsoringDialog.setWindowTitle(QCoreApplication.translate("SponsoringDialog", u"SponsoringDialog", None))
        self.button_donate_kofi.setText(QCoreApplication.translate("SponsoringDialog", u"Ko-Fi", None))
        self.button_donate_already_donated.setText(QCoreApplication.translate("SponsoringDialog", u"Already Donated", None))
        self.button_donate_paypal.setText(QCoreApplication.translate("SponsoringDialog", u"PayPal", None))
        self.button_donate_copy_xmr.setText(QCoreApplication.translate("SponsoringDialog", u"Copy XMR", None))
        self.button_donate_close.setText(QCoreApplication.translate("SponsoringDialog", u"Close", None))
        self.textBrowser.setHtml(QCoreApplication.translate("SponsoringDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI','Helvetica Neue','sans-serif'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#ffc800;\">y</span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#cc00ff;\">o</span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#ffffff;\"> </span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#37ff00;\">w</span><span style=\" font-family"
                        ":'Sans Serif'; font-size:36pt; color:#ff00bb;\">a</span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#ff0000;\">s</span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#0000ff;\">s</span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#00fff7;\">u</span><span style=\" font-family:'Sans Serif'; font-size:36pt; color:#ff55ff;\">p</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:14pt; text-decoration: underline; color:#ffffff;\">If you have a moment to read this, I'd appreciate it a lot...</span><span style=\" font-family:'Sans Serif'; font-size:9pt; color:#ffffff;\"><br /></span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:11pt; color:#ffffff;\">I have started developing Porn"
                        " Fetch ~2 years ago as a fun project for learning graphical user interfaces. Over the years Porn Fetch became more professional, as my programming skills increased and more people started using it. That I reach even 1000 downloads on this was something I'd never thought was possible and now we are over 20.000 xD</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:11pt; color:#ffffff;\">Although I absolutely love what I am doing here, and unless I receive a Cease and Desist letter, will never stop it, I haven't earned much from this project except for the few people that donated me something (Thank you so much btw).</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:11pt; color:#ffffff;\">If you have a few cents left on your pocket, I'd abso"
                        "lutely appreciate it. I know it might not seem much but it's a thank you and it keeps me motivated. Also since I still go to school small amounts of money are much more in relation to me than it is for someone who already has a job.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:11pt; color:#ffffff;\">But even if you don't donate, please don't feel bad. I don't expect it from you. I just kindly ask, but it's absolutely okay if you don't want to.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:14pt; color:#0000ff;\">Donation options</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://paypal.me/EchterAlsFake\"><span style=\" font-fa"
                        "mily:'Sans Serif'; font-size:14pt; text-decoration: underline; color:#27bf73;\">1) PayPal (https://paypal.me/EchterAlsFake)</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://paypal.me/EchterAlsFake\"><span style=\" font-family:'Sans Serif'; font-size:14pt; text-decoration: underline; color:#aa00ff;\">2) K</span></a><a href=\"https://ko-fi.com/EchterAlsFake\"><span style=\" font-family:'Sans Serif'; font-size:14pt; text-decoration: underline; color:#aa00ff;\">o-Fi (https://ko-fi.com/EchterAlsFake)</span></a></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:14pt;\">3) Crypto (XMR / Monero) : </span><span style=\" font-family:'ui-monospace','SFMono-Regular','SF Mono','Menlo','Consolas','Liberation Mono','monospace'; font-size:9pt; color:#ff7700; background-color:rgba(101,108"
                        ",118,0.2);\">42XwGZYbSxpMvhn9eeP4DwMwZV91tQgAm3UQr6Zwb2wzBf5HcuZCHrsVxa4aV2jhP4gLHsWWELxSoNjfnkt4rMfDDwXy9jR</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif'; font-size:12pt; color:#00ffb3;\">[This message won't be shown again, except if you update to a new version]</span></p></body></html>", None))
    # retranslateUi

