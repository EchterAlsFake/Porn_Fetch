# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_install_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_SetupInstallDialog(object):
    def setupUi(self, SetupInstallDialog):
        if not SetupInstallDialog.objectName():
            SetupInstallDialog.setObjectName(u"SetupInstallDialog")
        SetupInstallDialog.resize(936, 682)
        SetupInstallDialog.setStyleSheet(u"background-color: rgb(42, 42, 42);\n"
"color: rgb(255, 255, 255)")
        self.gridLayout = QGridLayout(SetupInstallDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(SetupInstallDialog)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)

        self.horizontallayout_app_name = QHBoxLayout()
        self.horizontallayout_app_name.setObjectName(u"horizontallayout_app_name")
        self.label_custom_app_name = QLabel(SetupInstallDialog)
        self.label_custom_app_name.setObjectName(u"label_custom_app_name")

        self.horizontallayout_app_name.addWidget(self.label_custom_app_name)

        self.lineedit_custom_app_name = QLineEdit(SetupInstallDialog)
        self.lineedit_custom_app_name.setObjectName(u"lineedit_custom_app_name")

        self.horizontallayout_app_name.addWidget(self.lineedit_custom_app_name)


        self.verticalLayout.addLayout(self.horizontallayout_app_name)

        self.horizontallayout_buttons = QHBoxLayout()
        self.horizontallayout_buttons.setObjectName(u"horizontallayout_buttons")
        self.button_install = QPushButton(SetupInstallDialog)
        self.button_install.setObjectName(u"button_install")

        self.horizontallayout_buttons.addWidget(self.button_install)

        self.button_portable = QPushButton(SetupInstallDialog)
        self.button_portable.setObjectName(u"button_portable")

        self.horizontallayout_buttons.addWidget(self.button_portable)


        self.verticalLayout.addLayout(self.horizontallayout_buttons)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(SetupInstallDialog)

        QMetaObject.connectSlotsByName(SetupInstallDialog)
    # setupUi

    def retranslateUi(self, SetupInstallDialog):
        SetupInstallDialog.setWindowTitle(QCoreApplication.translate("SetupInstallDialog", u"Widget", None))
        self.textBrowser.setHtml(QCoreApplication.translate("SetupInstallDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:24pt; font-weight:700;\">Installation Mode</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#0000ff;\">1) Inst</span><span style=\" font-family:'Segoe UI'; font-size:14pt; text-"
                        "decoration: underline; color:#0000ff;\">all</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This will install Porn Fetch into your system, meaning that you can run it directly from your Start Menu. e.g, press Windows key, type Porn Fetch and directly start it and on Linux it will be the same.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Porn Fetch will be installed into the following path(s):</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-ind"
                        "ent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Windows: C:\\Users\\&lt;user&gt;\\AppData\\Local\\pornfetch\\</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Linux: ~/.local/share/pornfetch</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; text-decoration: underline; color:#00ff00;\">2) Portable</span></p>\n"
"<p style=\" margin-top:0px; mar"
                        "gin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">This means, that Porn Fetch will not be installed and in order to use and start Porn Fetch you always need to double click on the file you have downloaded. This has some benefits as the uninstallation is easier and you have more control over it, but for the average user I do not recommend this.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:16pt; font-weight:700; color:#a100ff;\">Custom App name</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\">Down below you can enter  a custom name for Porn Fetch. You can then search with this name for Porn Fetch and Porn Fetch will not be found anymore when someone enters &quot;Porn Fetch&quot; on your PC. This can be useful if multiple persons use your PC and you don't want them to know you are using this application. It can also help if you are in public and people stare at your PC. Porn Fetch has also an option to fully hide, that it's a PornHub downloader.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI'; font-size:12pt; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ffffff;\">If you leave it empty, Porn Fetch will remain as &quot;Porn Fetch&quot; in your short menu.</spa"
                        "n></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:14pt; text-decoration: underline; color:#aa0000;\">NOTE:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI'; font-size:12pt;\">Installation was implemented in this release and might still be experimental. If you run into any issues, please report it on my GitHub. Thank you :</span><span style=\" font-family:'Segoe UI';\">) </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI';\"><br /></p></body></html>", None))
        self.label_custom_app_name.setText(QCoreApplication.translate("SetupInstallDialog", u"Custom App Name:", None))
        self.lineedit_custom_app_name.setText("")
        self.lineedit_custom_app_name.setPlaceholderText(QCoreApplication.translate("SetupInstallDialog", u"Enter your custom App Name here. Leave it empty to keep \"Porn Fetch\"", None))
        self.button_install.setText(QCoreApplication.translate("SetupInstallDialog", u"Install", None))
        self.button_portable.setText(QCoreApplication.translate("SetupInstallDialog", u"Portable", None))
    # retranslateUi

