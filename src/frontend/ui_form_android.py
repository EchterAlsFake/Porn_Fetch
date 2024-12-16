# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_android.ui'
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
    QLayout, QLineEdit, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_PornFetch_Android(object):
    def setupUi(self, PornFetch_Android):
        if not PornFetch_Android.objectName():
            PornFetch_Android.setObjectName(u"PornFetch_Android")
        PornFetch_Android.resize(720, 1280)
        PornFetch_Android.setStyleSheet(u"QWidget {background-color: rgb(59, 59, 59) }\n"
"QLabel {color: white}\n"
"QLineEdit {color: white} \n"
"QRadioButton {color: white}\n"
"QPushButton {color: white}")
        self.gridLayout = QGridLayout(PornFetch_Android)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridlayout_downloading = QGridLayout()
        self.gridlayout_downloading.setSpacing(6)
        self.gridlayout_downloading.setObjectName(u"gridlayout_downloading")
        self.gridlayout_downloading.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridlayout_downloading.setContentsMargins(-1, 14, -1, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_switch_home = QPushButton(PornFetch_Android)
        self.button_switch_home.setObjectName(u"button_switch_home")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_switch_home.sizePolicy().hasHeightForWidth())
        self.button_switch_home.setSizePolicy(sizePolicy)
        self.button_switch_home.setMinimumSize(QSize(50, 35))
        self.button_switch_home.setMaximumSize(QSize(16777215, 35))
        self.button_switch_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_home.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #a9a9a9;\n"
"    border-radius: 8px;\n"
"    padding: 8px 10px;\n"
"}")
        self.button_switch_home.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_home)

        self.button_switch_account = QPushButton(PornFetch_Android)
        self.button_switch_account.setObjectName(u"button_switch_account")
        sizePolicy.setHeightForWidth(self.button_switch_account.sizePolicy().hasHeightForWidth())
        self.button_switch_account.setSizePolicy(sizePolicy)
        self.button_switch_account.setMinimumSize(QSize(50, 35))
        self.button_switch_account.setMaximumSize(QSize(16777215, 35))
        self.button_switch_account.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_account.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    padding: 8px 10px;\n"
"    border: 2px solid #a9a9a9;\n"
"}\n"
"")
        self.button_switch_account.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_account)

        self.button_switch_tools = QPushButton(PornFetch_Android)
        self.button_switch_tools.setObjectName(u"button_switch_tools")
        sizePolicy.setHeightForWidth(self.button_switch_tools.sizePolicy().hasHeightForWidth())
        self.button_switch_tools.setSizePolicy(sizePolicy)
        self.button_switch_tools.setMinimumSize(QSize(50, 35))
        self.button_switch_tools.setMaximumSize(QSize(16777215, 35))
        font = QFont()
        self.button_switch_tools.setFont(font)
        self.button_switch_tools.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_tools.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.button_switch_tools.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_tools)

        self.button_switch_settings = QPushButton(PornFetch_Android)
        self.button_switch_settings.setObjectName(u"button_switch_settings")
        sizePolicy.setHeightForWidth(self.button_switch_settings.sizePolicy().hasHeightForWidth())
        self.button_switch_settings.setSizePolicy(sizePolicy)
        self.button_switch_settings.setMinimumSize(QSize(50, 35))
        self.button_switch_settings.setMaximumSize(QSize(16777215, 35))
        self.button_switch_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_settings.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.button_switch_settings.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_settings)

        self.button_switch_credits = QPushButton(PornFetch_Android)
        self.button_switch_credits.setObjectName(u"button_switch_credits")
        sizePolicy.setHeightForWidth(self.button_switch_credits.sizePolicy().hasHeightForWidth())
        self.button_switch_credits.setSizePolicy(sizePolicy)
        self.button_switch_credits.setMinimumSize(QSize(50, 35))
        self.button_switch_credits.setMaximumSize(QSize(16777215, 35))
        self.button_switch_credits.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_credits.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}\n"
"")
        self.button_switch_credits.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_credits)

        self.button_view_progress_bars = QPushButton(PornFetch_Android)
        self.button_view_progress_bars.setObjectName(u"button_view_progress_bars")
        sizePolicy.setHeightForWidth(self.button_view_progress_bars.sizePolicy().hasHeightForWidth())
        self.button_view_progress_bars.setSizePolicy(sizePolicy)
        self.button_view_progress_bars.setMinimumSize(QSize(50, 35))
        self.button_view_progress_bars.setMaximumSize(QSize(16777215, 35))
        self.button_view_progress_bars.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_view_progress_bars.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}")
        self.button_view_progress_bars.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_view_progress_bars)

        self.button_switch_supported_websites = QPushButton(PornFetch_Android)
        self.button_switch_supported_websites.setObjectName(u"button_switch_supported_websites")
        sizePolicy.setHeightForWidth(self.button_switch_supported_websites.sizePolicy().hasHeightForWidth())
        self.button_switch_supported_websites.setSizePolicy(sizePolicy)
        self.button_switch_supported_websites.setMinimumSize(QSize(50, 35))
        self.button_switch_supported_websites.setMaximumSize(QSize(16777215, 35))
        self.button_switch_supported_websites.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_switch_supported_websites.setStyleSheet(u"QPushButton {\n"
"    border-radius: 8px;\n"
"    border: 2px solid #a9a9a9;\n"
"    padding: 8px 10px;\n"
"}")
        self.button_switch_supported_websites.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.button_switch_supported_websites)


        self.gridlayout_downloading.addLayout(self.horizontalLayout, 7, 0, 1, 6)

        self.label_url = QLabel(PornFetch_Android)
        self.label_url.setObjectName(u"label_url")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_url.sizePolicy().hasHeightForWidth())
        self.label_url.setSizePolicy(sizePolicy1)
        self.label_url.setMinimumSize(QSize(100, 30))

        self.gridlayout_downloading.addWidget(self.label_url, 2, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridlayout_downloading.addItem(self.verticalSpacer_4, 8, 2, 1, 1)

        self.lineEdit = QLineEdit(PornFetch_Android)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridlayout_downloading.addWidget(self.lineEdit, 0, 0, 1, 6)

        self.radioButton_2 = QRadioButton(PornFetch_Android)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridlayout_downloading.addWidget(self.radioButton_2, 3, 1, 1, 1)

        self.radioButton_3 = QRadioButton(PornFetch_Android)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.gridlayout_downloading.addWidget(self.radioButton_3, 3, 2, 1, 4)

        self.pushButton = QPushButton(PornFetch_Android)
        self.pushButton.setObjectName(u"pushButton")

        self.gridlayout_downloading.addWidget(self.pushButton, 4, 4, 1, 2)

        self.lineedit_url = QLineEdit(PornFetch_Android)
        self.lineedit_url.setObjectName(u"lineedit_url")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineedit_url.sizePolicy().hasHeightForWidth())
        self.lineedit_url.setSizePolicy(sizePolicy2)
        self.lineedit_url.setMinimumSize(QSize(300, 30))

        self.gridlayout_downloading.addWidget(self.lineedit_url, 2, 1, 1, 5)

        self.button_clipboard = QPushButton(PornFetch_Android)
        self.button_clipboard.setObjectName(u"button_clipboard")

        self.gridlayout_downloading.addWidget(self.button_clipboard, 4, 2, 1, 2)

        self.button_download = QPushButton(PornFetch_Android)
        self.button_download.setObjectName(u"button_download")
        sizePolicy1.setHeightForWidth(self.button_download.sizePolicy().hasHeightForWidth())
        self.button_download.setSizePolicy(sizePolicy1)
        self.button_download.setMinimumSize(QSize(60, 30))
        self.button_download.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.button_download.setStyleSheet(u"")

        self.gridlayout_downloading.addWidget(self.button_download, 4, 0, 1, 2)

        self.radioButton = QRadioButton(PornFetch_Android)
        self.radioButton.setObjectName(u"radioButton")

        self.gridlayout_downloading.addWidget(self.radioButton, 3, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridlayout_downloading)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(PornFetch_Android)

        QMetaObject.connectSlotsByName(PornFetch_Android)
    # setupUi

    def retranslateUi(self, PornFetch_Android):
        PornFetch_Android.setWindowTitle(QCoreApplication.translate("PornFetch_Android", u"UI_android", None))
        self.button_switch_home.setText("")
        self.button_switch_account.setText("")
        self.button_switch_tools.setText("")
        self.button_switch_settings.setText("")
        self.button_switch_credits.setText("")
        self.button_view_progress_bars.setText("")
        self.button_switch_supported_websites.setText(QCoreApplication.translate("PornFetch_Android", u"Supported websites", None))
        self.label_url.setText(QCoreApplication.translate("PornFetch_Android", u"URL:", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"This line will show you debug messages, please read it (only on Android)", None))
        self.radioButton_2.setText(QCoreApplication.translate("PornFetch_Android", u"Playlist", None))
        self.radioButton_3.setText(QCoreApplication.translate("PornFetch_Android", u"Model URL", None))
        self.pushButton.setText(QCoreApplication.translate("PornFetch_Android", u"Reset URL", None))
        self.lineedit_url.setPlaceholderText(QCoreApplication.translate("PornFetch_Android", u"Enter video URL", None))
        self.button_clipboard.setText(QCoreApplication.translate("PornFetch_Android", u"Copy clipbaord", None))
        self.button_download.setText(QCoreApplication.translate("PornFetch_Android", u"Download", None))
        self.radioButton.setText(QCoreApplication.translate("PornFetch_Android", u"Video", None))
    # retranslateUi

