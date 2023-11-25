# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QGroupBox, QLabel, QLayout, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_Porn_Fetch_Widget(object):
    def setupUi(self, Porn_Fetch_Widget):
        if not Porn_Fetch_Widget.objectName():
            Porn_Fetch_Widget.setObjectName(u"Porn_Fetch_Widget")
        Porn_Fetch_Widget.resize(1758, 829)
        Porn_Fetch_Widget.setStyleSheet(u"QWidget {\n"
"color: white;\n"
"background-color: rgb(60, 60, 60);\n"
"border: none;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100); \n"
"    color: #FFFFFF; \n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  \n"
"    color: #aaaaaa; \n"
"    border-color: #aaaaaa;\n"
"}\n"
"\n"
"QPushButton {\n"
"        background-color: #5a2a82;\n"
"        color: #ffffff; \n"
"        border: none;\n"
"        border-radius: 10px;\n"
"        padding: 5px 20px; \n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; \n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; \n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; \n"
"        color"
                        ": #8a7b9a; \n"
"    }\n"
"\n"
"\n"
"QProgressBar {\n"
"	color: rgb(255, 153, 0);\n"
"    border: 2px solid #5a2a82;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background-color: rgb(74, 74, 74);\n"
"    color: #ffffff;  /* Adding text color for better visibility */\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(0, 255, 224);\n"
"    width: 10px; /* Adjust this to change the width of the 'chunk' */\n"
"}\n"
"\n"
"QRadioButton {\n"
"	color: rgb(255,255,255)}\n"
"\n"
"QRadioButton::indicator::unchecked {\n"
"	border: 1px solid white;\n"
"	border-radius: 5px;\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    border : 4px solid;\n"
"	border-color: black;\n"
"	border-radius: 6px;\n"
"	background-color: rgb(0, 255, 183);\n"
"\n"
"}\n"
"\n"
"QSlider::groove:horizontal {\n"
"    border: 1px solid #5a2a82;\n"
"    height: 8px;\n"
"    background: #e0e0e0;\n"
"    margin: 0px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"    background: #5"
                        "a2a82;\n"
"    border: 1px solid #5a2a82;\n"
"    width: 18px;\n"
"    margin: -6px 0;\n"
"    border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"    background: #e0e0e0;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"    background: #5a2a82;\n"
"}\n"
"\n"
"QTreeWidget {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: white;\n"
"}\n"
"\n"
"QTreeWidget QHeaderView::section {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: black; \n"
"    border: 1px solid #5a2a82;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 1ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.widget = QWidget(Porn_Fetch_Widget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 122, 831))
        self.widget.setStyleSheet(u"background-color: rgb(34, 34, 34)")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(50, 50))
        self.pushButton_2.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(50, 50))
        self.pushButton_3.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(50, 50))
        self.pushButton_4.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(50, 50))
        self.pushButton.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(50, 50))
        self.pushButton_5.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.verticalLayout.addWidget(self.pushButton_5)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)

        self.widget_2 = QWidget(Porn_Fetch_Widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(120, 670, 1641, 161))
        self.widget_2.setStyleSheet(u"background-color: rgb(34, 34, 34);\n"
"border-radius: 5px;")
        self.groupBox = QGroupBox(self.widget_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 70, 1641, 91))
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.progressBar = QProgressBar(self.groupBox)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.progressBar)

        self.progressBar_2 = QProgressBar(self.groupBox)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(0)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.progressBar_2)


        self.gridLayout_2.addLayout(self.formLayout_2, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.widget_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 0, 1641, 81))
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 0, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(self.groupBox_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_4.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_4.addWidget(self.label_6, 1, 2, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_4.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.gridLayout_4.addWidget(self.lineEdit_3, 0, 3, 1, 1)

        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.gridLayout_4.addWidget(self.lineEdit_4, 1, 3, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 1, 1, 1)

        self.stacked_widget_main = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.stacked_widget_main.setGeometry(QRect(120, 0, 1641, 471))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget_top = QStackedWidget(self.page)
        self.stackedWidget_top.setObjectName(u"stackedWidget_top")
        self.stackedWidget_top.setGeometry(QRect(0, 0, 1641, 241))
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.label_7 = QLabel(self.page_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 10, 24, 16))
        self.lineEdit_6 = QLineEdit(self.page_5)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setGeometry(QRect(89, 43, 143, 24))
        self.label_8 = QLabel(self.page_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 42, 37, 16))
        self.pushButton_7 = QPushButton(self.page_5)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(238, 42, 64, 26))
        self.lineEdit_8 = QLineEdit(self.page_5)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setGeometry(QRect(89, 107, 143, 24))
        self.lineEdit_7 = QLineEdit(self.page_5)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setGeometry(QRect(89, 75, 143, 24))
        self.pushButton_6 = QPushButton(self.page_5)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(238, 10, 64, 26))
        self.pushButton_9 = QPushButton(self.page_5)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(238, 106, 64, 26))
        self.lineEdit_5 = QLineEdit(self.page_5)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setGeometry(QRect(89, 11, 143, 24))
        self.label_10 = QLabel(self.page_5)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 74, 21, 16))
        self.label_9 = QLabel(self.page_5)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 106, 73, 16))
        self.pushButton_8 = QPushButton(self.page_5)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(238, 74, 64, 26))
        self.stackedWidget_top.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.groupBox_3 = QGroupBox(self.page_6)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(9, 9, 1611, 151))
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_11)

        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_12)

        self.lineEdit_9 = QLineEdit(self.groupBox_3)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.lineEdit_9)

        self.lineEdit_10 = QLineEdit(self.groupBox_3)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.lineEdit_10)

        self.pushButton_10 = QPushButton(self.groupBox_3)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.formLayout_3.setWidget(2, QFormLayout.SpanningRole, self.pushButton_10)


        self.gridLayout_5.addLayout(self.formLayout_3, 0, 0, 1, 1)

        self.stackedWidget_top.addWidget(self.page_6)
        self.groupBox_4 = QGroupBox(self.page)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(180, 430, 274, 213))
        self.gridLayout_6 = QGridLayout(self.groupBox_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stacked_widget_main.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stacked_widget_main.addWidget(self.page_2)
        self.stacked_widget_tree = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_tree.setObjectName(u"stacked_widget_tree")
        self.stacked_widget_tree.setGeometry(QRect(120, 470, 1641, 191))
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.stacked_widget_tree.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stacked_widget_tree.addWidget(self.page_4)

        self.retranslateUi(Porn_Fetch_Widget)

        self.stackedWidget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn_Fetch_Widget", None))
        self.pushButton_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home", None))
        self.pushButton_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.pushButton_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Account", None))
        self.pushButton.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Settings", None))
        self.pushButton_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Credits", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Current Progress:", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.groupBox_2.setTitle("")
        self.label_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Error:", None))
        self.label_6.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Debug:", None))
        self.label_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Status:", None))
        self.label_7.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.label_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model:", None))
        self.pushButton_7.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.pushButton_6.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.pushButton_9.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.label_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.label_9.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.pushButton_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Start", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Account", None))
        self.label_11.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.label_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.pushButton_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"PushButton", None))
        self.groupBox_4.setTitle("")
    # retranslateUi

