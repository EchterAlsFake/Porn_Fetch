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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QTreeWidget, QTreeWidgetItem,
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
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #DDD;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid #5599FF;\n"
"}\n"
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
"	border-radius: 6"
                        "px;\n"
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
"    background: #5a2a82;\n"
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
"        subcont"
                        "rol-position: top center;\n"
"        padding: 0 3px;\n"
"    }\n"
"\n"
"QLabel {\n"
"    color: #DDD;\n"
"    padding: 2px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: #333;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #555;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5599FF;\n"
"}")
        self.widget = QWidget(Porn_Fetch_Widget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 30, 122, 801))
        self.widget.setStyleSheet(u"background-color: rgb(34, 34, 34)")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setMinimumSize(QSize(50, 50))
        self.pushButton_5.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_5, 3, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setMinimumSize(QSize(50, 50))
        self.pushButton_3.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_3, 1, 0, 1, 1)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(50, 50))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(50, 50))
        self.pushButton_2.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet(u"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 white, stop:1 #abcdef); /* Anfang wei\u00df, Ende Farbe */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 0, 1, 1)

        self.widget_status = QWidget(Porn_Fetch_Widget)
        self.widget_status.setObjectName(u"widget_status")
        self.widget_status.setGeometry(QRect(120, 660, 1641, 171))
        self.widget_status.setStyleSheet(u"background-color: rgb(34, 34, 34);\n"
"border-radius: 5px;")
        self.gridLayout_5 = QGridLayout(self.widget_status)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.widget_status)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.progressBar = QProgressBar(self.widget_status)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout_2.addWidget(self.progressBar, 0, 1, 1, 1)

        self.label_2 = QLabel(self.widget_status)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.progressBar_2 = QProgressBar(self.widget_status)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(0)

        self.gridLayout_2.addWidget(self.progressBar_2, 1, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.gridlayout_status = QGridLayout()
        self.gridlayout_status.setObjectName(u"gridlayout_status")
        self.label_5 = QLabel(self.widget_status)
        self.label_5.setObjectName(u"label_5")

        self.gridlayout_status.addWidget(self.label_5, 0, 2, 1, 1)

        self.lineEdit_2 = QLineEdit(self.widget_status)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.label_4 = QLabel(self.widget_status)
        self.label_4.setObjectName(u"label_4")

        self.gridlayout_status.addWidget(self.label_4, 1, 0, 1, 1)

        self.label_6 = QLabel(self.widget_status)
        self.label_6.setObjectName(u"label_6")

        self.gridlayout_status.addWidget(self.label_6, 1, 2, 1, 1)

        self.label_3 = QLabel(self.widget_status)
        self.label_3.setObjectName(u"label_3")

        self.gridlayout_status.addWidget(self.label_3, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.widget_status)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(self.widget_status)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineEdit_3, 0, 3, 1, 1)

        self.lineEdit_4 = QLineEdit(self.widget_status)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setReadOnly(True)

        self.gridlayout_status.addWidget(self.lineEdit_4, 1, 3, 1, 1)


        self.gridLayout_5.addLayout(self.gridlayout_status, 0, 0, 1, 1)

        self.stacked_widget_main = QStackedWidget(Porn_Fetch_Widget)
        self.stacked_widget_main.setObjectName(u"stacked_widget_main")
        self.stacked_widget_main.setGeometry(QRect(130, 30, 1621, 631))
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_7 = QGridLayout(self.page_3)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.stacked_widget_top = QStackedWidget(self.page_3)
        self.stacked_widget_top.setObjectName(u"stacked_widget_top")
        self.stacked_widget_top.setCursor(QCursor(Qt.ArrowCursor))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_6 = QGridLayout(self.page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_9 = QLabel(self.page)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_3.addWidget(self.label_9, 3, 0, 1, 1)

        self.pushButton_8 = QPushButton(self.page)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_8, 3, 2, 1, 1)

        self.lineEdit_5 = QLineEdit(self.page)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.gridLayout_3.addWidget(self.lineEdit_5, 0, 1, 1, 1)

        self.pushButton_7 = QPushButton(self.page)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_7, 4, 2, 1, 1)

        self.lineEdit_7 = QLineEdit(self.page)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.gridLayout_3.addWidget(self.lineEdit_7, 3, 1, 1, 1)

        self.lineEdit_8 = QLineEdit(self.page)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.gridLayout_3.addWidget(self.lineEdit_8, 4, 1, 1, 1)

        self.label_8 = QLabel(self.page)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_3.addWidget(self.label_8, 2, 0, 1, 1)

        self.pushButton_4 = QPushButton(self.page)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_4, 0, 2, 1, 1)

        self.label_10 = QLabel(self.page)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 4, 0, 1, 1)

        self.label_7 = QLabel(self.page)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 0, 0, 1, 1)

        self.pushButton_6 = QPushButton(self.page)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_6.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_3.addWidget(self.pushButton_6, 2, 2, 1, 1)

        self.lineEdit_6 = QLineEdit(self.page)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.gridLayout_3.addWidget(self.lineEdit_6, 2, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pushButton_12 = QPushButton(self.page)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_12.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #78909C, stop:1 #90A4AE);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_12, 3, 2, 1, 1)

        self.label_11 = QLabel(self.page)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_4.addWidget(self.label_11, 1, 0, 1, 1)

        self.pushButton_9 = QPushButton(self.page)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #78909C, stop:1 #90A4AE);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_9, 3, 0, 1, 1)

        self.label_12 = QLabel(self.page)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)

        self.pushButton_11 = QPushButton(self.page)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_11.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #78909C, stop:1 #90A4AE);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_11, 3, 1, 1, 1)

        self.pushButton_10 = QPushButton(self.page)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton_10.setStyleSheet(u"QPushButton {\n"
"    border: 2px solid #444;\n"
"    border-radius: 8px;\n"
"    padding: 5px;\n"
"    color: #DDD;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #5555FF, stop:1 #AA55FF);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #6666FF, stop:1 #BB66FF);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,\n"
"                                stop:0 #4444DD, stop:1 #9944DD);\n"
"}")

        self.gridLayout_4.addWidget(self.pushButton_10, 2, 0, 1, 4)

        self.lineEdit_10 = QLineEdit(self.page)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setEchoMode(QLineEdit.Password)

        self.gridLayout_4.addWidget(self.lineEdit_10, 1, 1, 1, 3)

        self.lineEdit_9 = QLineEdit(self.page)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.gridLayout_4.addWidget(self.lineEdit_9, 0, 1, 1, 3)


        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_2, 1, 0, 1, 2)

        self.stacked_widget_top.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stacked_widget_top.addWidget(self.page_2)

        self.gridLayout_7.addWidget(self.stacked_widget_top, 0, 0, 1, 1)

        self.treeWidget = QTreeWidget(self.page_3)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.gridLayout_7.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.stacked_widget_main.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stacked_widget_main.addWidget(self.page_4)
        self.verticalLayoutWidget = QWidget(Porn_Fetch_Widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 1761, 31))
        self.HEADER = QVBoxLayout(self.verticalLayoutWidget)
        self.HEADER.setObjectName(u"HEADER")
        self.HEADER.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(Porn_Fetch_Widget)

        self.stacked_widget_main.setCurrentIndex(0)
        self.stacked_widget_top.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_Widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_Widget):
        Porn_Fetch_Widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_Widget", u"Porn_Fetch_Widget", None))
        self.pushButton_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Credits", None))
        self.pushButton_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search", None))
        self.pushButton.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Settings", None))
        self.pushButton_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Home", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Current Progress:", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_5.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Total:", None))
        self.label_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Error:", None))
        self.label_6.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Debug:", None))
        self.label_3.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Status:", None))
        self.label_9.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"File:", None))
        self.pushButton_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Open File", None))
        self.lineEdit_5.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub or HQPorner Video URL", None))
        self.pushButton_7.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineEdit_7.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Click Open File to select a file, or write the location here and click Open File.    URLs need to be separated with a new line. Supports HQPorner and PornHub", None))
        self.lineEdit_8.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter a Search Query for PornHub  You can define filters in the settings. The returned videos will be listed down below and you can select them.", None))
        self.label_8.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Model URL:", None))
        self.pushButton_4.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Download", None))
        self.label_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Search Query:", None))
        self.label_7.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"URL:", None))
        self.pushButton_6.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Videos", None))
        self.lineEdit_6.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter PornHub Model URL. This can be a Pornstar Account or a PornHub Channel. The videos will be listed down in the TreeWidget", None))
        self.pushButton_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get recommended videos", None))
        self.label_11.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Password:", None))
        self.pushButton_9.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get Liked videos", None))
        self.label_12.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Username:", None))
        self.pushButton_11.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Get watched videos", None))
        self.pushButton_10.setText(QCoreApplication.translate("Porn_Fetch_Widget", u"Login", None))
        self.lineEdit_10.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Password", None))
        self.lineEdit_9.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_Widget", u"Enter your PornHub Username", None))
    # retranslateUi

