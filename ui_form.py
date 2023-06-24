# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QProgressBar, QPushButton,
    QRadioButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1496, 487)
        self.gridLayout_7 = QGridLayout(Widget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.groupbox_urls = QGroupBox(Widget)
        self.groupbox_urls.setObjectName(u"groupbox_urls")
        self.gridLayout_5 = QGridLayout(self.groupbox_urls)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_url = QLabel(self.groupbox_urls)
        self.label_url.setObjectName(u"label_url")
        self.horizontalLayout_2.addWidget(self.label_url)
        self.lineedit_url = QLineEdit(self.groupbox_urls)
        self.lineedit_url.setObjectName(u"lineedit_url")
        self.horizontalLayout_2.addWidget(self.lineedit_url)
        self.button_start = QPushButton(self.groupbox_urls)
        self.button_start.setObjectName(u"button_start")
        self.horizontalLayout_2.addWidget(self.button_start)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_url_file = QLabel(self.groupbox_urls)
        self.label_url_file.setObjectName(u"label_url_file")
        self.horizontalLayout.addWidget(self.label_url_file)
        self.lineedit_url_file = QLineEdit(self.groupbox_urls)
        self.lineedit_url_file.setObjectName(u"lineedit_url_file")
        self.horizontalLayout.addWidget(self.lineedit_url_file)
        self.button_start_file = QPushButton(self.groupbox_urls)
        self.button_start_file.setObjectName(u"button_start_file")
        self.horizontalLayout.addWidget(self.button_start_file)
        self.gridLayout_5.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupbox_urls, 0, 0, 1, 1)
        self.groupbox_settings = QGroupBox(Widget)
        self.groupbox_settings.setObjectName(u"groupbox_settings")
        self.gridLayout_4 = QGridLayout(self.groupbox_settings)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupbox_useless = QGroupBox(self.groupbox_settings)
        self.groupbox_useless.setObjectName(u"groupbox_useless")
        self.gridLayout_2 = QGridLayout(self.groupbox_useless)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupbox_quality = QGroupBox(self.groupbox_useless)
        self.groupbox_quality.setObjectName(u"groupbox_quality")
        self.gridLayout_3 = QGridLayout(self.groupbox_quality)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.radio_highest = QRadioButton(self.groupbox_quality)
        self.radio_highest.setObjectName(u"radio_highest")
        self.gridLayout_3.addWidget(self.radio_highest, 0, 0, 1, 1)
        self.radio_middle = QRadioButton(self.groupbox_quality)
        self.radio_middle.setObjectName(u"radio_middle")
        self.gridLayout_3.addWidget(self.radio_middle, 1, 0, 1, 1)
        self.radio_lowest = QRadioButton(self.groupbox_quality)
        self.radio_lowest.setObjectName(u"radio_lowest")
        self.gridLayout_3.addWidget(self.radio_lowest, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupbox_quality, 0, 0, 2, 1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_output = QLabel(self.groupbox_useless)
        self.label_output.setObjectName(u"label_output")
        self.horizontalLayout_3.addWidget(self.label_output)
        self.lineedit_output = QLineEdit(self.groupbox_useless)
        self.lineedit_output.setObjectName(u"lineedit_output")
        self.horizontalLayout_3.addWidget(self.lineedit_output)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupbox_useless, 0, 1, 1, 1)
        self.groupbox_settings_ui = QGroupBox(self.groupbox_settings)
        self.groupbox_settings_ui.setObjectName(u"groupbox_settings_ui")
        self.gridLayout = QGridLayout(self.groupbox_settings_ui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radio_native = QRadioButton(self.groupbox_settings_ui)
        self.radio_native.setObjectName(u"radio_native")

        self.gridLayout.addWidget(self.radio_native, 0, 0, 1, 1)
        self.radio_dark = QRadioButton(self.groupbox_settings_ui)
        self.radio_dark.setObjectName(u"radio_dark")

        self.gridLayout.addWidget(self.radio_dark, 1, 0, 1, 1)
        self.radio_white = QRadioButton(self.groupbox_settings_ui)
        self.radio_white.setObjectName(u"radio_white")
        self.gridLayout.addWidget(self.radio_white, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupbox_settings_ui, 0, 3, 1, 1)
        self.progressbar_download = QProgressBar(self.groupbox_settings)
        self.progressbar_download.setObjectName(u"progressbar_download")
        self.progressbar_download.setValue(0)
        self.gridLayout_4.addWidget(self.progressbar_download, 1, 1, 1, 3)
        self.gridLayout_7.addWidget(self.groupbox_settings, 0, 1, 2, 1)
        self.groupbox_metadata = QGroupBox(Widget)
        self.groupbox_metadata.setObjectName(u"groupbox_metadata")
        self.gridLayout_6 = QGridLayout(self.groupbox_metadata)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_duration = QLabel(self.groupbox_metadata)
        self.label_duration.setObjectName(u"label_duration")
        self.gridLayout_6.addWidget(self.label_duration, 4, 0, 1, 1)
        self.label_author = QLabel(self.groupbox_metadata)
        self.label_author.setObjectName(u"label_author")
        self.gridLayout_6.addWidget(self.label_author, 1, 0, 1, 1)
        self.lineedit_author = QLineEdit(self.groupbox_metadata)
        self.lineedit_author.setObjectName(u"lineedit_author")
        self.lineedit_author.setReadOnly(True)
        self.gridLayout_6.addWidget(self.lineedit_author, 1, 1, 1, 1)
        self.lineedit_duration = QLineEdit(self.groupbox_metadata)
        self.lineedit_duration.setObjectName(u"lineedit_duration")
        self.lineedit_duration.setAutoFillBackground(False)
        self.lineedit_duration.setReadOnly(True)
        self.gridLayout_6.addWidget(self.lineedit_duration, 4, 1, 1, 1)
        self.lineedit_title = QLineEdit(self.groupbox_metadata)
        self.lineedit_title.setObjectName(u"lineedit_title")
        self.lineedit_title.setReadOnly(True)
        self.gridLayout_6.addWidget(self.lineedit_title, 0, 1, 1, 1)
        self.lineedit_hotspots = QLineEdit(self.groupbox_metadata)
        self.lineedit_hotspots.setObjectName(u"lineedit_hotspots")
        self.lineedit_hotspots.setAutoFillBackground(False)
        self.lineedit_hotspots.setReadOnly(True)
        self.gridLayout_6.addWidget(self.lineedit_hotspots, 5, 1, 1, 1)
        self.label_hotspots = QLabel(self.groupbox_metadata)
        self.label_hotspots.setObjectName(u"label_hotspots")
        self.gridLayout_6.addWidget(self.label_hotspots, 5, 0, 1, 1)
        self.label_date = QLabel(self.groupbox_metadata)
        self.label_date.setObjectName(u"label_date")
        self.gridLayout_6.addWidget(self.label_date, 3, 0, 1, 1)
        self.label_title = QLabel(self.groupbox_metadata)
        self.label_title.setObjectName(u"label_title")
        self.gridLayout_6.addWidget(self.label_title, 0, 0, 1, 1)
        self.lineedit_views = QLineEdit(self.groupbox_metadata)
        self.lineedit_views.setObjectName(u"lineedit_views")
        self.lineedit_views.setReadOnly(True)
        self.gridLayout_6.addWidget(self.lineedit_views, 2, 1, 1, 1)
        self.lineedit_date = QLineEdit(self.groupbox_metadata)
        self.lineedit_date.setObjectName(u"lineedit_date")
        self.lineedit_date.setReadOnly(True)
        self.gridLayout_6.addWidget(self.lineedit_date, 3, 1, 1, 1)
        self.label_views = QLabel(self.groupbox_metadata)
        self.label_views.setObjectName(u"label_views")
        self.gridLayout_6.addWidget(self.label_views, 2, 0, 1, 1)
        self.button_get_metadata = QPushButton(self.groupbox_metadata)
        self.button_get_metadata.setObjectName(u"button_get_metadata")
        self.gridLayout_6.addWidget(self.button_get_metadata, 6, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupbox_metadata, 1, 0, 2, 1)
        self.credits_text = QTextBrowser(Widget)
        self.credits_text.setObjectName(u"credits_text")
        self.gridLayout_7.addWidget(self.credits_text, 2, 1, 1, 1)
        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Porn Fetch 1.0 (CC)", None))
        self.groupbox_urls.setTitle(QCoreApplication.translate("Widget", u"Download", None))
        self.label_url.setText(QCoreApplication.translate("Widget", u"URL:", None))
        self.button_start.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.label_url_file.setText(QCoreApplication.translate("Widget", u"File with URLs:", None))
        self.button_start_file.setText(QCoreApplication.translate("Widget", u"Start", None))
        self.groupbox_settings.setTitle("")
        self.groupbox_useless.setTitle("")
        self.groupbox_quality.setTitle(QCoreApplication.translate("Widget", u"Quality", None))
        self.radio_highest.setText(QCoreApplication.translate("Widget", u"Highest", None))
        self.radio_middle.setText(QCoreApplication.translate("Widget", u"Middle", None))
        self.radio_lowest.setText(QCoreApplication.translate("Widget", u"Lowest", None))
        self.label_output.setText(QCoreApplication.translate("Widget", u"Output Path:", None))
        self.groupbox_settings_ui.setTitle(QCoreApplication.translate("Widget", u"UI", None))
        self.radio_native.setText(QCoreApplication.translate("Widget", u"Native", None))
        self.radio_dark.setText(QCoreApplication.translate("Widget", u"Dark mode", None))
        self.radio_white.setText(QCoreApplication.translate("Widget", u"White mode", None))
        self.groupbox_metadata.setTitle(QCoreApplication.translate("Widget", u"Metadata", None))
        self.label_duration.setText(QCoreApplication.translate("Widget", u"Duration:", None))
        self.label_author.setText(QCoreApplication.translate("Widget", u"Author: ", None))
        self.label_hotspots.setText(QCoreApplication.translate("Widget", u"Hotspots:", None))
        self.label_date.setText(QCoreApplication.translate("Widget", u"Date:", None))
        self.label_title.setText(QCoreApplication.translate("Widget", u"Title:", None))
        self.label_views.setText(QCoreApplication.translate("Widget", u"Views:", None))
        self.button_get_metadata.setText(QCoreApplication.translate("Widget", u"Get metadata", None))
        self.credits_text.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Credits:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">API: PHUB by Egsa"
                        "gon.  This project would not be possible without it.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Author: EchterAlsFake</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">License: Creative Commons</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Plugins: Tabnine, Material Theme Icons</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Libraries: colorama, tqdm, PySide6</s"
                        "pan></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Graphical User Interface was created with Qt - PySide6</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">Version: 1.0</span></p></body></html>", None))
    # retranslateUi

