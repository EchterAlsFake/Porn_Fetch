# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Porn_Fetch_v3.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QStackedWidget, QTextBrowser,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_Porn_Fetch_widget(object):
    def setupUi(self, Porn_Fetch_widget):
        if not Porn_Fetch_widget.objectName():
            Porn_Fetch_widget.setObjectName(u"Porn_Fetch_widget")
        Porn_Fetch_widget.resize(1418, 595)
        Porn_Fetch_widget.setStyleSheet(u"QWidget {\n"
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
"QProgressBar {\n"
"    border: 2px solid #5a2a82;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #5a2a82;\n"
"    width: 10px; /* You can adjust this to change the width of the 'chunk' */\n"
"}\n"
"QRadioButton {\n"
"	color: (255,255,255)}\n"
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
"    background: #5a2a82;\n"
"    border: 1px solid #5a2a82;\n"
"    width: 18px;\n"
"    margin: -6px 0;\n"
"    border-radius: 9px;\n"
"}\n"
""
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
"QTreeWidget::header {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: black; /* Set color to black or any other color that you prefer for the header text */\n"
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
        self.gridLayout_8 = QGridLayout(Porn_Fetch_widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.stackedWidget_3 = QStackedWidget(Porn_Fetch_widget)
        self.stackedWidget_3.setObjectName(u"stackedWidget_3")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_6 = QGridLayout(self.page_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stackedWidget_2 = QStackedWidget(self.page_5)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.stackedWidget_2.setStyleSheet(u"border: none;")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_4 = QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.groupBox_2 = QGroupBox(self.page_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.treeWidget = QTreeWidget(self.groupBox_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setStyleSheet(u"")

        self.gridLayout_3.addWidget(self.treeWidget, 0, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.button_download_tree_widget = QPushButton(self.page_3)
        self.button_download_tree_widget.setObjectName(u"button_download_tree_widget")
        self.button_download_tree_widget.setStyleSheet(u"QPushButton {\n"
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
"        color: #8a7b9a; \n"
"    }")

        self.horizontalLayout_8.addWidget(self.button_download_tree_widget)

        self.button_select_all = QPushButton(self.page_3)
        self.button_select_all.setObjectName(u"button_select_all")

        self.horizontalLayout_8.addWidget(self.button_select_all)

        self.button_unselect_all = QPushButton(self.page_3)
        self.button_unselect_all.setObjectName(u"button_unselect_all")

        self.horizontalLayout_8.addWidget(self.button_unselect_all)


        self.gridLayout_4.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.stackedWidget_2.addWidget(self.page_4)

        self.gridLayout_6.addWidget(self.stackedWidget_2, 1, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self.page_5)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_9 = QGridLayout(self.page)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_model_url = QLabel(self.page)
        self.label_model_url.setObjectName(u"label_model_url")

        self.gridLayout.addWidget(self.label_model_url, 1, 0, 1, 1)

        self.lineedit_search_query = QLineEdit(self.page)
        self.lineedit_search_query.setObjectName(u"lineedit_search_query")
        self.lineedit_search_query.setStyleSheet(u"")

        self.gridLayout.addWidget(self.lineedit_search_query, 3, 1, 1, 1)

        self.button_file_start = QPushButton(self.page)
        self.button_file_start.setObjectName(u"button_file_start")
        self.button_file_start.setStyleSheet(u"")

        self.gridLayout.addWidget(self.button_file_start, 2, 2, 1, 1)

        self.label_search_query = QLabel(self.page)
        self.label_search_query.setObjectName(u"label_search_query")

        self.gridLayout.addWidget(self.label_search_query, 3, 0, 1, 1)

        self.button_search_start = QPushButton(self.page)
        self.button_search_start.setObjectName(u"button_search_start")
        self.button_search_start.setStyleSheet(u"")

        self.gridLayout.addWidget(self.button_search_start, 3, 2, 1, 1)

        self.lineedit_model_url = QLineEdit(self.page)
        self.lineedit_model_url.setObjectName(u"lineedit_model_url")
        self.lineedit_model_url.setStyleSheet(u"")

        self.gridLayout.addWidget(self.lineedit_model_url, 1, 1, 1, 1)

        self.button_video_url_start = QPushButton(self.page)
        self.button_video_url_start.setObjectName(u"button_video_url_start")
        self.button_video_url_start.setStyleSheet(u"")

        self.gridLayout.addWidget(self.button_video_url_start, 0, 2, 1, 1)

        self.label_file = QLabel(self.page)
        self.label_file.setObjectName(u"label_file")

        self.gridLayout.addWidget(self.label_file, 2, 0, 1, 1)

        self.button_model_url_start = QPushButton(self.page)
        self.button_model_url_start.setObjectName(u"button_model_url_start")
        self.button_model_url_start.setStyleSheet(u"")

        self.gridLayout.addWidget(self.button_model_url_start, 1, 2, 1, 1)

        self.lineedit_video_url = QLineEdit(self.page)
        self.lineedit_video_url.setObjectName(u"lineedit_video_url")
        self.lineedit_video_url.setStyleSheet(u"")

        self.gridLayout.addWidget(self.lineedit_video_url, 0, 1, 1, 1)

        self.lineedit_file = QLineEdit(self.page)
        self.lineedit_file.setObjectName(u"lineedit_file")
        self.lineedit_file.setStyleSheet(u"")

        self.gridLayout.addWidget(self.lineedit_file, 2, 1, 1, 1)

        self.label_video_url = QLabel(self.page)
        self.label_video_url.setObjectName(u"label_video_url")

        self.gridLayout.addWidget(self.label_video_url, 0, 0, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_7 = QGridLayout(self.page_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.groupBox_3 = QGroupBox(self.page_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.button_get_liked = QPushButton(self.groupBox_3)
        self.button_get_liked.setObjectName(u"button_get_liked")
        self.button_get_liked.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.button_get_liked)

        self.button_get_watched = QPushButton(self.groupBox_3)
        self.button_get_watched.setObjectName(u"button_get_watched")
        self.button_get_watched.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.button_get_watched)

        self.button_get_recommended = QPushButton(self.groupBox_3)
        self.button_get_recommended.setObjectName(u"button_get_recommended")
        self.button_get_recommended.setStyleSheet(u"")

        self.horizontalLayout_4.addWidget(self.button_get_recommended)


        self.gridLayout_5.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_disclaimer = QLabel(self.page_2)
        self.label_disclaimer.setObjectName(u"label_disclaimer")

        self.horizontalLayout_3.addWidget(self.label_disclaimer)


        self.gridLayout_7.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_username = QLabel(self.page_2)
        self.label_username.setObjectName(u"label_username")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_username)

        self.lineedit_username = QLineEdit(self.page_2)
        self.lineedit_username.setObjectName(u"lineedit_username")
        self.lineedit_username.setStyleSheet(u"")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineedit_username)

        self.label_password = QLabel(self.page_2)
        self.label_password.setObjectName(u"label_password")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_password)

        self.lineedit_password = QLineEdit(self.page_2)
        self.lineedit_password.setObjectName(u"lineedit_password")
        self.lineedit_password.setStyleSheet(u"")
        self.lineedit_password.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineedit_password)

        self.button_login = QPushButton(self.page_2)
        self.button_login.setObjectName(u"button_login")
        self.button_login.setStyleSheet(u"")

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.button_login)


        self.gridLayout_7.addLayout(self.formLayout, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_6.addWidget(self.stackedWidget, 0, 0, 1, 1)

        self.stackedWidget_3.addWidget(self.page_5)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6.setStyleSheet(u"QProgressBar {\n"
"    border: 2px solid #5a2a82;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #5a2a82;\n"
"    width: 10px; /* You can adjust this to change the width of the 'chunk' */\n"
"}\n"
"")
        self.gridLayout_13 = QGridLayout(self.page_6)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.groupBox_4 = QGroupBox(self.page_6)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_12 = QGridLayout(self.groupBox_4)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridlayout_api_language = QGridLayout()
        self.gridlayout_api_language.setObjectName(u"gridlayout_api_language")
        self.api_radio_fr = QRadioButton(self.groupBox_4)
        self.api_radio_fr.setObjectName(u"api_radio_fr")
        self.api_radio_fr.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_fr.setStyleSheet(u"")

        self.gridlayout_api_language.addWidget(self.api_radio_fr, 2, 1, 1, 1)

        self.api_radio_de = QRadioButton(self.groupBox_4)
        self.api_radio_de.setObjectName(u"api_radio_de")
        self.api_radio_de.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_de.setStyleSheet(u"")

        self.gridlayout_api_language.addWidget(self.api_radio_de, 2, 0, 1, 1)

        self.api_radio_ru = QRadioButton(self.groupBox_4)
        self.api_radio_ru.setObjectName(u"api_radio_ru")
        self.api_radio_ru.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_ru.setStyleSheet(u"")

        self.gridlayout_api_language.addWidget(self.api_radio_ru, 3, 0, 1, 1)

        self.api_radio_es = QRadioButton(self.groupBox_4)
        self.api_radio_es.setObjectName(u"api_radio_es")
        self.api_radio_es.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_es.setStyleSheet(u"")

        self.gridlayout_api_language.addWidget(self.api_radio_es, 1, 1, 1, 1)

        self.api_radio_en = QRadioButton(self.groupBox_4)
        self.api_radio_en.setObjectName(u"api_radio_en")
        self.api_radio_en.setCursor(QCursor(Qt.PointingHandCursor))
        self.api_radio_en.setStyleSheet(u"")
        self.api_radio_en.setChecked(False)

        self.gridlayout_api_language.addWidget(self.api_radio_en, 1, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")

        self.gridlayout_api_language.addWidget(self.label_11, 0, 0, 1, 2)

        self.radio_api_custom = QRadioButton(self.groupBox_4)
        self.radio_api_custom.setObjectName(u"radio_api_custom")
        self.radio_api_custom.setChecked(True)

        self.gridlayout_api_language.addWidget(self.radio_api_custom, 3, 1, 1, 1)


        self.gridLayout_12.addLayout(self.gridlayout_api_language, 1, 0, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.radio_speed_high = QRadioButton(self.groupBox_4)
        self.radio_speed_high.setObjectName(u"radio_speed_high")
        self.radio_speed_high.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_speed_high, 2, 1, 1, 1)

        self.label_threading = QLabel(self.groupBox_4)
        self.label_threading.setObjectName(u"label_threading")

        self.gridLayout_10.addWidget(self.label_threading, 1, 0, 1, 1)

        self.radio_threading_no = QRadioButton(self.groupBox_4)
        self.radio_threading_no.setObjectName(u"radio_threading_no")
        self.radio_threading_no.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_threading_no, 1, 2, 1, 1)

        self.button_threading_help = QPushButton(self.groupBox_4)
        self.button_threading_help.setObjectName(u"button_threading_help")
        self.button_threading_help.setStyleSheet(u"QPushButton {\n"
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
"        color: #8a7b9a; \n"
"    }")

        self.gridLayout_10.addWidget(self.button_threading_help, 1, 3, 1, 1)

        self.radio_quality_middle = QRadioButton(self.groupBox_4)
        self.radio_quality_middle.setObjectName(u"radio_quality_middle")
        self.radio_quality_middle.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_quality_middle, 0, 2, 1, 1)

        self.radio_quality_worst = QRadioButton(self.groupBox_4)
        self.radio_quality_worst.setObjectName(u"radio_quality_worst")
        self.radio_quality_worst.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_quality_worst, 0, 3, 1, 1)

        self.label_quality = QLabel(self.groupBox_4)
        self.label_quality.setObjectName(u"label_quality")

        self.gridLayout_10.addWidget(self.label_quality, 0, 0, 1, 1)

        self.radio_threading_yes = QRadioButton(self.groupBox_4)
        self.radio_threading_yes.setObjectName(u"radio_threading_yes")
        self.radio_threading_yes.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_threading_yes, 1, 1, 1, 1)

        self.label_speed = QLabel(self.groupBox_4)
        self.label_speed.setObjectName(u"label_speed")

        self.gridLayout_10.addWidget(self.label_speed, 2, 0, 1, 1)

        self.radio_speed_usual = QRadioButton(self.groupBox_4)
        self.radio_speed_usual.setObjectName(u"radio_speed_usual")
        self.radio_speed_usual.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_speed_usual, 2, 2, 1, 1)

        self.radio_quality_best = QRadioButton(self.groupBox_4)
        self.radio_quality_best.setObjectName(u"radio_quality_best")
        self.radio_quality_best.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.radio_quality_best, 0, 1, 1, 1)

        self.label_note_speed = QLabel(self.groupBox_4)
        self.label_note_speed.setObjectName(u"label_note_speed")

        self.gridLayout_10.addWidget(self.label_note_speed, 3, 0, 1, 4)

        self.button_speed_help = QPushButton(self.groupBox_4)
        self.button_speed_help.setObjectName(u"button_speed_help")
        self.button_speed_help.setStyleSheet(u"QPushButton {\n"
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
"        color: #8a7b9a; \n"
"    }")

        self.gridLayout_10.addWidget(self.button_speed_help, 2, 3, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.frame = QFrame(self.groupBox_4)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_19 = QGridLayout(self.frame)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.label_output_path = QLabel(self.frame)
        self.label_output_path.setObjectName(u"label_output_path")

        self.gridLayout_19.addWidget(self.label_output_path, 1, 0, 1, 1)

        self.lineedit_default_output_path = QLineEdit(self.frame)
        self.lineedit_default_output_path.setObjectName(u"lineedit_default_output_path")
        self.lineedit_default_output_path.setStyleSheet(u"")

        self.gridLayout_19.addWidget(self.lineedit_default_output_path, 1, 1, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_19.addWidget(self.label_2, 2, 0, 1, 1)

        self.label_current_value_slider = QLabel(self.frame)
        self.label_current_value_slider.setObjectName(u"label_current_value_slider")

        self.gridLayout_19.addWidget(self.label_current_value_slider, 3, 1, 1, 1)

        self.button_search_limit_help = QPushButton(self.frame)
        self.button_search_limit_help.setObjectName(u"button_search_limit_help")
        self.button_search_limit_help.setStyleSheet(u"")

        self.gridLayout_19.addWidget(self.button_search_limit_help, 2, 2, 1, 1)

        self.horizontalSlider = QSlider(self.frame)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setStyleSheet(u"")
        self.horizontalSlider.setMaximum(200)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.gridLayout_19.addWidget(self.horizontalSlider, 2, 1, 1, 1)

        self.label_custom_api = QLabel(self.frame)
        self.label_custom_api.setObjectName(u"label_custom_api")

        self.gridLayout_19.addWidget(self.label_custom_api, 0, 0, 1, 1)

        self.lineedit_custom_api_language = QLineEdit(self.frame)
        self.lineedit_custom_api_language.setObjectName(u"lineedit_custom_api_language")

        self.gridLayout_19.addWidget(self.lineedit_custom_api_language, 0, 1, 1, 1)

        self.button_custom_api = QPushButton(self.frame)
        self.button_custom_api.setObjectName(u"button_custom_api")

        self.gridLayout_19.addWidget(self.button_custom_api, 0, 2, 1, 1)


        self.gridLayout_12.addWidget(self.frame, 2, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_4, 0, 0, 1, 1)

        self.groupBox_10 = QGroupBox(self.page_6)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.groupBox_10.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_16 = QGridLayout(self.groupBox_10)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.groupBox_13 = QGroupBox(self.groupBox_10)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.groupBox_13.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_14 = QGridLayout(self.groupBox_13)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.radio_day = QRadioButton(self.groupBox_13)
        self.radio_day.setObjectName(u"radio_day")
        self.radio_day.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.radio_day, 0, 0, 1, 1)

        self.radio_month = QRadioButton(self.groupBox_13)
        self.radio_month.setObjectName(u"radio_month")
        self.radio_month.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.radio_month, 2, 0, 1, 1)

        self.radio_time_sort_ignore = QRadioButton(self.groupBox_13)
        self.radio_time_sort_ignore.setObjectName(u"radio_time_sort_ignore")
        self.radio_time_sort_ignore.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.radio_time_sort_ignore, 4, 0, 1, 1)

        self.radio_week = QRadioButton(self.groupBox_13)
        self.radio_week.setObjectName(u"radio_week")
        self.radio_week.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.radio_week, 1, 0, 1, 1)

        self.radio_year = QRadioButton(self.groupBox_13)
        self.radio_year.setObjectName(u"radio_year")
        self.radio_year.setStyleSheet(u"")

        self.gridLayout_14.addWidget(self.radio_year, 3, 0, 1, 1)


        self.gridLayout_16.addWidget(self.groupBox_13, 1, 0, 1, 1)

        self.groupBox_12 = QGroupBox(self.groupBox_10)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.groupBox_12.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_11 = QGridLayout(self.groupBox_12)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.radio_longest = QRadioButton(self.groupBox_12)
        self.radio_longest.setObjectName(u"radio_longest")
        self.radio_longest.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.radio_longest, 2, 0, 1, 1)

        self.radio_top_rated = QRadioButton(self.groupBox_12)
        self.radio_top_rated.setObjectName(u"radio_top_rated")
        self.radio_top_rated.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.radio_top_rated, 4, 0, 1, 1)

        self.radio_most_viewed = QRadioButton(self.groupBox_12)
        self.radio_most_viewed.setObjectName(u"radio_most_viewed")
        self.radio_most_viewed.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.radio_most_viewed, 1, 0, 1, 1)

        self.radio_most_relevant = QRadioButton(self.groupBox_12)
        self.radio_most_relevant.setObjectName(u"radio_most_relevant")
        self.radio_most_relevant.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.radio_most_relevant, 0, 0, 1, 1)

        self.radio_most_recent = QRadioButton(self.groupBox_12)
        self.radio_most_recent.setObjectName(u"radio_most_recent")
        self.radio_most_recent.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.radio_most_recent, 3, 0, 1, 1)

        self.radio_sort_ignore = QRadioButton(self.groupBox_12)
        self.radio_sort_ignore.setObjectName(u"radio_sort_ignore")
        self.radio_sort_ignore.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.radio_sort_ignore, 5, 0, 1, 1)


        self.gridLayout_16.addWidget(self.groupBox_12, 1, 1, 1, 1)

        self.groupBox_15 = QGroupBox(self.groupBox_10)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.groupBox_15.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_15 = QGridLayout(self.groupBox_15)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.radio_professional = QRadioButton(self.groupBox_15)
        self.radio_professional.setObjectName(u"radio_professional")
        self.radio_professional.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.radio_professional, 0, 0, 1, 1)

        self.radio_homemade = QRadioButton(self.groupBox_15)
        self.radio_homemade.setObjectName(u"radio_homemade")
        self.radio_homemade.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.radio_homemade, 1, 0, 1, 1)

        self.radio_production_ignore = QRadioButton(self.groupBox_15)
        self.radio_production_ignore.setObjectName(u"radio_production_ignore")
        self.radio_production_ignore.setStyleSheet(u"")

        self.gridLayout_15.addWidget(self.radio_production_ignore, 2, 0, 1, 1)


        self.gridLayout_16.addWidget(self.groupBox_15, 0, 1, 1, 1)

        self.groupBox = QGroupBox(self.groupBox_10)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"        border: 0px;\n"
"        margin-top: 2ex; /* Adjust as needed */\n"
"    }\n"
"    QGroupBox::title {\n"
"        subcontrol-origin: margin;\n"
"        subcontrol-position: top center;\n"
"        padding: 0 3px;\n"
"    }")
        self.gridLayout_18 = QGridLayout(self.groupBox)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.button_category_filters = QPushButton(self.groupBox)
        self.button_category_filters.setObjectName(u"button_category_filters")
        self.button_category_filters.setStyleSheet(u"QPushButton {\n"
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
"        color: #8a7b9a; \n"
"    }")

        self.gridLayout_18.addWidget(self.button_category_filters, 0, 0, 1, 1)


        self.gridLayout_16.addWidget(self.groupBox, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.groupBox_10, 0, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.button_settings_apply = QPushButton(self.page_6)
        self.button_settings_apply.setObjectName(u"button_settings_apply")
        self.button_settings_apply.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_settings_apply.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.button_settings_apply)


        self.gridLayout_13.addLayout(self.horizontalLayout_5, 1, 0, 1, 2)

        self.stackedWidget_3.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_26 = QGridLayout(self.page_7)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.stacked_widget_metadata = QStackedWidget(self.page_7)
        self.stacked_widget_metadata.setObjectName(u"stacked_widget_metadata")
        self.stacked_widget_metadata.setStyleSheet(u"QPushButton {\n"
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
"        color: #8a7b9a; \n"
"    }")
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.gridLayout_22 = QGridLayout(self.page_9)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.groupBox_5 = QGroupBox(self.page_9)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_21 = QGridLayout(self.groupBox_5)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.lineedit_tags = QLineEdit(self.groupBox_5)
        self.lineedit_tags.setObjectName(u"lineedit_tags")
        self.lineedit_tags.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_tags.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_tags, 4, 1, 1, 1)

        self.lineedit_title = QLineEdit(self.groupBox_5)
        self.lineedit_title.setObjectName(u"lineedit_title")
        self.lineedit_title.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_title.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_title, 1, 1, 1, 1)

        self.label_author = QLabel(self.groupBox_5)
        self.label_author.setObjectName(u"label_author")
        self.label_author.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 35px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_author, 0, 2, 1, 1)

        self.label_likes = QLabel(self.groupBox_5)
        self.label_likes.setObjectName(u"label_likes")
        self.label_likes.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 49px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_likes, 3, 0, 1, 1)

        self.lineedit_likes = QLineEdit(self.groupBox_5)
        self.lineedit_likes.setObjectName(u"lineedit_likes")
        self.lineedit_likes.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_likes.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_likes, 3, 1, 1, 1)

        self.label_title = QLabel(self.groupBox_5)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 55px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_title, 1, 0, 1, 1)

        self.label_image_url = QLabel(self.groupBox_5)
        self.label_image_url.setObjectName(u"label_image_url")
        self.label_image_url.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 10px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_image_url, 2, 0, 1, 1)

        self.lineedit_metadata_url = QLineEdit(self.groupBox_5)
        self.lineedit_metadata_url.setObjectName(u"lineedit_metadata_url")
        self.lineedit_metadata_url.setStyleSheet(u"QLineEdit {\n"
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
"}")

        self.gridLayout_17.addWidget(self.lineedit_metadata_url, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName(u"label")

        self.gridLayout_17.addWidget(self.label, 5, 0, 1, 1)

        self.lineedit_actress = QLineEdit(self.groupBox_5)
        self.lineedit_actress.setObjectName(u"lineedit_actress")
        self.lineedit_actress.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_actress.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_actress, 5, 1, 1, 1)

        self.label_video_metadata_url = QLabel(self.groupBox_5)
        self.label_video_metadata_url.setObjectName(u"label_video_metadata_url")

        self.gridLayout_17.addWidget(self.label_video_metadata_url, 0, 0, 1, 1)

        self.label_tags = QLabel(self.groupBox_5)
        self.label_tags.setObjectName(u"label_tags")
        self.label_tags.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 53px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_tags, 4, 0, 1, 1)

        self.lineedit_image_url = QLineEdit(self.groupBox_5)
        self.lineedit_image_url.setObjectName(u"lineedit_image_url")
        self.lineedit_image_url.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_image_url.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_image_url, 2, 1, 1, 1)

        self.lineedit_author = QLineEdit(self.groupBox_5)
        self.lineedit_author.setObjectName(u"lineedit_author")
        self.lineedit_author.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_author.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_author, 0, 3, 1, 1)

        self.label_views = QLabel(self.groupBox_5)
        self.label_views.setObjectName(u"label_views")
        self.label_views.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 44px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_views, 1, 2, 1, 1)

        self.lineedit_views = QLineEdit(self.groupBox_5)
        self.lineedit_views.setObjectName(u"lineedit_views")
        self.lineedit_views.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_views.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_views, 1, 3, 1, 1)

        self.label_date = QLabel(self.groupBox_5)
        self.label_date.setObjectName(u"label_date")
        self.label_date.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 53px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_date, 2, 2, 1, 1)

        self.lineedit_date = QLineEdit(self.groupBox_5)
        self.lineedit_date.setObjectName(u"lineedit_date")
        self.lineedit_date.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_date.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_date, 2, 3, 1, 1)

        self.label_duration = QLabel(self.groupBox_5)
        self.label_duration.setObjectName(u"label_duration")
        self.label_duration.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 16px;\n"
"	margin-right: 25px;\n"
"}\n"
"\n"
"QLabel#Title {\n"
"    color: #212121;\n"
"    font-size: 24px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#Subtitle {\n"
"    color: #757575;\n"
"    font-size: 20px;\n"
"}\n"
"")

        self.gridLayout_17.addWidget(self.label_duration, 3, 2, 1, 1)

        self.lineedit_duration = QLineEdit(self.groupBox_5)
        self.lineedit_duration.setObjectName(u"lineedit_duration")
        self.lineedit_duration.setAutoFillBackground(False)
        self.lineedit_duration.setStyleSheet(u"QLineEdit {\n"
"    border: 2px solid #757575;\n"
"    border-radius: 12px;\n"
"    padding: 0 8px;\n"
"    background: rgb(94, 92, 100);  /* setzt den Hintergrund auf Schwarz */\n"
"    color: #FFFFFF;  /* setzt die Textfarbe auf Wei\u00df */\n"
"    font-size: 16px;\n"
"    height: 20px;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border-color: rgb(107, 0, 255)\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background: #444444;  /* setzt den Hintergrund auf ein dunkles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    color: #aaaaaa;  /* setzt die Textfarbe auf ein helles Grau, wenn das QLineEdit deaktiviert ist */\n"
"    border-color: #aaaaaa;\n"
"}")
        self.lineedit_duration.setReadOnly(True)

        self.gridLayout_17.addWidget(self.lineedit_duration, 3, 3, 1, 1)


        self.gridLayout_21.addLayout(self.gridLayout_17, 0, 0, 1, 2)

        self.button_download_thumbnail = QPushButton(self.groupBox_5)
        self.button_download_thumbnail.setObjectName(u"button_download_thumbnail")
        self.button_download_thumbnail.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download_thumbnail.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.gridLayout_21.addWidget(self.button_download_thumbnail, 1, 0, 1, 1)

        self.button_get_metadata = QPushButton(self.groupBox_5)
        self.button_get_metadata.setObjectName(u"button_get_metadata")
        self.button_get_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_get_metadata.setStyleSheet(u"QPushButton {\n"
"        background-color: #5a2a82; /* base violet color */\n"
"        color: #ffffff; /* white text */\n"
"        border: none;\n"
"        border-radius: 10px; /* reduced rounded corner radius */\n"
"        padding: 5px 10px; /* reduced button padding */\n"
"        font-size: 12px;\n"
"        outline: none;\n"
"    }\n"
"    \n"
"    QPushButton:hover {\n"
"        background-color: #7b3ca3; /* slightly lighter violet when hovered */\n"
"    }\n"
"\n"
"    QPushButton:pressed {\n"
"        background-color: #481f61; /* darker violet when pressed */\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #3f1d4d; /* even darker shade when button is disabled */\n"
"        color: #8a7b9a; /* greyish text */\n"
"    }")

        self.gridLayout_21.addWidget(self.button_get_metadata, 1, 1, 1, 1)


        self.gridLayout_22.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.stacked_widget_metadata.addWidget(self.page_9)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.gridLayout_23 = QGridLayout(self.page_10)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.groupBox_6 = QGroupBox(self.page_10)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setStyleSheet(u"QLineEdit {\n"
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
"}")
        self.gridLayout_25 = QGridLayout(self.groupBox_6)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.button_user_information = QPushButton(self.groupBox_6)
        self.button_user_information.setObjectName(u"button_user_information")
        self.button_user_information.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_user_information.setStyleSheet(u"")

        self.horizontalLayout_7.addWidget(self.button_user_information)

        self.button_download_avatar = QPushButton(self.groupBox_6)
        self.button_download_avatar.setObjectName(u"button_download_avatar")
        self.button_download_avatar.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_download_avatar.setStyleSheet(u"")

        self.horizontalLayout_7.addWidget(self.button_download_avatar)

        self.button_user_biography = QPushButton(self.groupBox_6)
        self.button_user_biography.setObjectName(u"button_user_biography")
        self.button_user_biography.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_user_biography.setStyleSheet(u"")

        self.horizontalLayout_7.addWidget(self.button_user_biography)


        self.gridLayout_25.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.label_user_avatar = QLabel(self.groupBox_6)
        self.label_user_avatar.setObjectName(u"label_user_avatar")

        self.gridLayout_24.addWidget(self.label_user_avatar, 1, 0, 1, 1)

        self.label_user_relationship = QLabel(self.groupBox_6)
        self.label_user_relationship.setObjectName(u"label_user_relationship")

        self.gridLayout_24.addWidget(self.label_user_relationship, 2, 0, 1, 1)

        self.lineedit_user_fake_breasts = QLineEdit(self.groupBox_6)
        self.lineedit_user_fake_breasts.setObjectName(u"lineedit_user_fake_breasts")

        self.gridLayout_24.addWidget(self.lineedit_user_fake_breasts, 7, 1, 1, 1)

        self.label_user_ethnicity = QLabel(self.groupBox_6)
        self.label_user_ethnicity.setObjectName(u"label_user_ethnicity")

        self.gridLayout_24.addWidget(self.label_user_ethnicity, 6, 0, 1, 1)

        self.lineedit_user_gender = QLineEdit(self.groupBox_6)
        self.lineedit_user_gender.setObjectName(u"lineedit_user_gender")

        self.gridLayout_24.addWidget(self.lineedit_user_gender, 4, 1, 1, 1)

        self.label_user_name = QLabel(self.groupBox_6)
        self.label_user_name.setObjectName(u"label_user_name")

        self.gridLayout_24.addWidget(self.label_user_name, 0, 0, 1, 1)

        self.label_user_video_views = QLabel(self.groupBox_6)
        self.label_user_video_views.setObjectName(u"label_user_video_views")

        self.gridLayout_24.addWidget(self.label_user_video_views, 4, 2, 1, 1)

        self.label_user_hair_color = QLabel(self.groupBox_6)
        self.label_user_hair_color.setObjectName(u"label_user_hair_color")

        self.gridLayout_24.addWidget(self.label_user_hair_color, 1, 2, 1, 1)

        self.label_user_videos_watched = QLabel(self.groupBox_6)
        self.label_user_videos_watched.setObjectName(u"label_user_videos_watched")

        self.gridLayout_24.addWidget(self.label_user_videos_watched, 7, 2, 1, 1)

        self.label_user_profile_views = QLabel(self.groupBox_6)
        self.label_user_profile_views.setObjectName(u"label_user_profile_views")

        self.gridLayout_24.addWidget(self.label_user_profile_views, 5, 2, 1, 1)

        self.label_user_hobbies = QLabel(self.groupBox_6)
        self.label_user_hobbies.setObjectName(u"label_user_hobbies")

        self.gridLayout_24.addWidget(self.label_user_hobbies, 3, 2, 1, 1)

        self.label_user_interested_in = QLabel(self.groupBox_6)
        self.label_user_interested_in.setObjectName(u"label_user_interested_in")

        self.gridLayout_24.addWidget(self.label_user_interested_in, 3, 0, 1, 1)

        self.label_user_height = QLabel(self.groupBox_6)
        self.label_user_height.setObjectName(u"label_user_height")

        self.gridLayout_24.addWidget(self.label_user_height, 5, 0, 1, 1)

        self.lineedit_user_name = QLineEdit(self.groupBox_6)
        self.lineedit_user_name.setObjectName(u"lineedit_user_name")

        self.gridLayout_24.addWidget(self.lineedit_user_name, 0, 1, 1, 1)

        self.label_user_piercings = QLabel(self.groupBox_6)
        self.label_user_piercings.setObjectName(u"label_user_piercings")

        self.gridLayout_24.addWidget(self.label_user_piercings, 0, 2, 1, 1)

        self.lineedit_user_ethnicity = QLineEdit(self.groupBox_6)
        self.lineedit_user_ethnicity.setObjectName(u"lineedit_user_ethnicity")

        self.gridLayout_24.addWidget(self.lineedit_user_ethnicity, 6, 1, 1, 1)

        self.label_user_fake_breasts = QLabel(self.groupBox_6)
        self.label_user_fake_breasts.setObjectName(u"label_user_fake_breasts")

        self.gridLayout_24.addWidget(self.label_user_fake_breasts, 7, 0, 1, 1)

        self.lineedit_user_interested = QLineEdit(self.groupBox_6)
        self.lineedit_user_interested.setObjectName(u"lineedit_user_interested")

        self.gridLayout_24.addWidget(self.lineedit_user_interested, 3, 1, 1, 1)

        self.label_user_gender = QLabel(self.groupBox_6)
        self.label_user_gender.setObjectName(u"label_user_gender")

        self.gridLayout_24.addWidget(self.label_user_gender, 4, 0, 1, 1)

        self.lineedit_user_relationship = QLineEdit(self.groupBox_6)
        self.lineedit_user_relationship.setObjectName(u"lineedit_user_relationship")

        self.gridLayout_24.addWidget(self.lineedit_user_relationship, 2, 1, 1, 1)

        self.label_user_tattoos = QLabel(self.groupBox_6)
        self.label_user_tattoos.setObjectName(u"label_user_tattoos")

        self.gridLayout_24.addWidget(self.label_user_tattoos, 2, 2, 1, 1)

        self.label_user_turn_ons = QLabel(self.groupBox_6)
        self.label_user_turn_ons.setObjectName(u"label_user_turn_ons")

        self.gridLayout_24.addWidget(self.label_user_turn_ons, 6, 2, 1, 1)

        self.lineedit_user_avatar = QLineEdit(self.groupBox_6)
        self.lineedit_user_avatar.setObjectName(u"lineedit_user_avatar")

        self.gridLayout_24.addWidget(self.lineedit_user_avatar, 1, 1, 1, 1)

        self.lineedit_user_height = QLineEdit(self.groupBox_6)
        self.lineedit_user_height.setObjectName(u"lineedit_user_height")

        self.gridLayout_24.addWidget(self.lineedit_user_height, 5, 1, 1, 1)

        self.lineedit_user_piercings = QLineEdit(self.groupBox_6)
        self.lineedit_user_piercings.setObjectName(u"lineedit_user_piercings")

        self.gridLayout_24.addWidget(self.lineedit_user_piercings, 0, 3, 1, 1)

        self.lineedit_user_hair_color = QLineEdit(self.groupBox_6)
        self.lineedit_user_hair_color.setObjectName(u"lineedit_user_hair_color")

        self.gridLayout_24.addWidget(self.lineedit_user_hair_color, 1, 3, 1, 1)

        self.lineedit_user_tattoos = QLineEdit(self.groupBox_6)
        self.lineedit_user_tattoos.setObjectName(u"lineedit_user_tattoos")

        self.gridLayout_24.addWidget(self.lineedit_user_tattoos, 2, 3, 1, 1)

        self.lineedit_user_hobbies = QLineEdit(self.groupBox_6)
        self.lineedit_user_hobbies.setObjectName(u"lineedit_user_hobbies")

        self.gridLayout_24.addWidget(self.lineedit_user_hobbies, 3, 3, 1, 1)

        self.lineedit_user_video_views = QLineEdit(self.groupBox_6)
        self.lineedit_user_video_views.setObjectName(u"lineedit_user_video_views")

        self.gridLayout_24.addWidget(self.lineedit_user_video_views, 4, 3, 1, 1)

        self.lineedit_user_profile_views = QLineEdit(self.groupBox_6)
        self.lineedit_user_profile_views.setObjectName(u"lineedit_user_profile_views")

        self.gridLayout_24.addWidget(self.lineedit_user_profile_views, 5, 3, 1, 1)

        self.lineedit_user_turn_ons = QLineEdit(self.groupBox_6)
        self.lineedit_user_turn_ons.setObjectName(u"lineedit_user_turn_ons")

        self.gridLayout_24.addWidget(self.lineedit_user_turn_ons, 6, 3, 1, 1)

        self.lineedit_user_videos_watched = QLineEdit(self.groupBox_6)
        self.lineedit_user_videos_watched.setObjectName(u"lineedit_user_videos_watched")

        self.gridLayout_24.addWidget(self.lineedit_user_videos_watched, 7, 3, 1, 1)


        self.gridLayout_25.addLayout(self.gridLayout_24, 2, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_user_url = QLabel(self.groupBox_6)
        self.label_user_url.setObjectName(u"label_user_url")

        self.horizontalLayout_6.addWidget(self.label_user_url)

        self.lineedit_user_url = QLineEdit(self.groupBox_6)
        self.lineedit_user_url.setObjectName(u"lineedit_user_url")

        self.horizontalLayout_6.addWidget(self.lineedit_user_url)


        self.gridLayout_25.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)


        self.gridLayout_23.addWidget(self.groupBox_6, 0, 0, 1, 1)

        self.stacked_widget_metadata.addWidget(self.page_10)

        self.gridLayout_26.addWidget(self.stacked_widget_metadata, 0, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.button_switch_video_metadata = QPushButton(self.page_7)
        self.button_switch_video_metadata.setObjectName(u"button_switch_video_metadata")
        self.button_switch_video_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_video_metadata.setStyleSheet(u"")

        self.horizontalLayout_9.addWidget(self.button_switch_video_metadata)

        self.button_switch_user_metadata = QPushButton(self.page_7)
        self.button_switch_user_metadata.setObjectName(u"button_switch_user_metadata")
        self.button_switch_user_metadata.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_switch_user_metadata.setStyleSheet(u"")

        self.horizontalLayout_9.addWidget(self.button_switch_user_metadata)


        self.gridLayout_26.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)

        self.stackedWidget_3.addWidget(self.page_7)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout_20 = QGridLayout(self.page_8)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.textBrowser = QTextBrowser(self.page_8)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout_20.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.stackedWidget_3.addWidget(self.page_8)

        self.gridLayout_8.addWidget(self.stackedWidget_3, 0, 0, 1, 1)

        self.group_status = QGroupBox(Porn_Fetch_widget)
        self.group_status.setObjectName(u"group_status")
        self.gridLayout_2 = QGridLayout(self.group_status)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.button_video = QPushButton(self.group_status)
        self.button_video.setObjectName(u"button_video")
        self.button_video.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_video.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.button_video)

        self.button_account = QPushButton(self.group_status)
        self.button_account.setObjectName(u"button_account")
        self.button_account.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_account.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.button_account)

        self.button_settings = QPushButton(self.group_status)
        self.button_settings.setObjectName(u"button_settings")
        self.button_settings.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_settings.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.button_settings)

        self.button_miscellaneus = QPushButton(self.group_status)
        self.button_miscellaneus.setObjectName(u"button_miscellaneus")
        self.button_miscellaneus.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_miscellaneus.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.button_miscellaneus)

        self.button_credits = QPushButton(self.group_status)
        self.button_credits.setObjectName(u"button_credits")
        self.button_credits.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_credits.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.button_credits)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_status = QLabel(self.group_status)
        self.label_status.setObjectName(u"label_status")

        self.horizontalLayout_2.addWidget(self.label_status)

        self.lineedit_status = QLineEdit(self.group_status)
        self.lineedit_status.setObjectName(u"lineedit_status")
        self.lineedit_status.setStyleSheet(u"")
        self.lineedit_status.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineedit_status)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lineedit_toal = QLineEdit(self.group_status)
        self.lineedit_toal.setObjectName(u"lineedit_toal")

        self.verticalLayout_2.addWidget(self.lineedit_toal)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.progressbar_download = QProgressBar(self.group_status)
        self.progressbar_download.setObjectName(u"progressbar_download")
        self.progressbar_download.setStyleSheet(u"")
        self.progressbar_download.setValue(0)

        self.verticalLayout.addWidget(self.progressbar_download)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout_8.addWidget(self.group_status, 2, 0, 1, 1)


        self.retranslateUi(Porn_Fetch_widget)

        self.stackedWidget_3.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(0)
        self.stackedWidget.setCurrentIndex(0)
        self.stacked_widget_metadata.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Porn_Fetch_widget)
    # setupUi

    def retranslateUi(self, Porn_Fetch_widget):
        Porn_Fetch_widget.setWindowTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Porn Fetch v2.8     GPLv3", None))
        self.stackedWidget_3.setStyleSheet(QCoreApplication.translate("Porn_Fetch_widget", u"QTreeWidget {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: white;\n"
"}\n"
"\n"
"QTreeWidget::header {\n"
"    background-color: rgb(94, 94, 94);\n"
"    color: black; /* Set color to black or any other color that you prefer for the header text */\n"
"}\n"
"", None))
        self.groupBox_2.setTitle("")
        self.button_download_tree_widget.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Download selected videos", None))
        self.button_select_all.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Select all", None))
        self.button_unselect_all.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Unselect all", None))
        self.label_model_url.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Model URL: ", None))
        self.lineedit_search_query.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter Search Query for PornHub.com", None))
        self.button_file_start.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Start", None))
        self.label_search_query.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Search Query:", None))
        self.button_search_start.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Start", None))
        self.lineedit_model_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter PornHub Model / Channel / User URL. You can select the videos at the bottom", None))
        self.button_video_url_start.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Start", None))
        self.label_file.setText(QCoreApplication.translate("Porn_Fetch_widget", u"File: ", None))
        self.button_model_url_start.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Start", None))
        self.lineedit_video_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter PornHub or HQPorner URL", None))
        self.lineedit_file.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter File with URL's from PornHub or HQPorner. The URL's must be separated with new lines in the file!", None))
        self.label_video_url.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Video URL:", None))
        self.groupBox_3.setTitle("")
        self.button_get_liked.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Get liked videos", None))
        self.button_get_watched.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Get watched videos", None))
        self.button_get_recommended.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Get recommended videos", None))
        self.label_disclaimer.setText(QCoreApplication.translate("Porn_Fetch_widget", u"IMPORTANT:  Porn Fetch is against the Terms of Services from PornHub.com and HQPorner.com. Logging in with your account can lead to a ban from PornHub.com!", None))
        self.label_username.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Username:", None))
        self.lineedit_username.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter your PornHub Username", None))
        self.label_password.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Password:", None))
        self.lineedit_password.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter your PornHub Password  (Account data won't be saved, and the Session will be terminated, when you leave Porn Fetch)", None))
        self.button_login.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Login", None))
        self.groupBox_4.setTitle("")
        self.api_radio_fr.setText(QCoreApplication.translate("Porn_Fetch_widget", u"FR", None))
        self.api_radio_de.setText(QCoreApplication.translate("Porn_Fetch_widget", u"DE", None))
        self.api_radio_ru.setText(QCoreApplication.translate("Porn_Fetch_widget", u"RU", None))
        self.api_radio_es.setText(QCoreApplication.translate("Porn_Fetch_widget", u"ES", None))
        self.api_radio_en.setText(QCoreApplication.translate("Porn_Fetch_widget", u"EN", None))
        self.label_11.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Choose API language", None))
        self.radio_api_custom.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Custom", None))
        self.radio_speed_high.setText(QCoreApplication.translate("Porn_Fetch_widget", u"High", None))
        self.label_threading.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Threading:", None))
        self.radio_threading_no.setText(QCoreApplication.translate("Porn_Fetch_widget", u"No", None))
        self.button_threading_help.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Help", None))
        self.radio_quality_middle.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Middle", None))
        self.radio_quality_worst.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Worst", None))
        self.label_quality.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Quality: ", None))
        self.radio_threading_yes.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Yes", None))
        self.label_speed.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Speed:", None))
        self.radio_speed_usual.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Usual", None))
        self.radio_quality_best.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Best", None))
        self.label_note_speed.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Note: Changing the speed from Usual, can lead to errors!", None))
        self.button_speed_help.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Help", None))
        self.label_output_path.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Output Path: ", None))
        self.label_2.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Search Limit:", None))
        self.label_current_value_slider.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Current Limit: ", None))
        self.button_search_limit_help.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Help", None))
        self.label_custom_api.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Custom API Language:", None))
        self.lineedit_custom_api_language.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter language code e.g.,  zh = Chinese or fi = finnish", None))
        self.button_custom_api.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Apply", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Search filters", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Time sort filters", None))
        self.radio_day.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Day", None))
        self.radio_month.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Month", None))
        self.radio_time_sort_ignore.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Ignore filter", None))
        self.radio_week.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Week", None))
        self.radio_year.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Year", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Sorting for Search function", None))
        self.radio_longest.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Longest", None))
        self.radio_top_rated.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Top rated", None))
        self.radio_most_viewed.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Most viewed", None))
        self.radio_most_relevant.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Most relevant", None))
        self.radio_most_recent.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Most recent", None))
        self.radio_sort_ignore.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Ignore filter", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Production:", None))
        self.radio_professional.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Professional", None))
        self.radio_homemade.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Homemade", None))
        self.radio_production_ignore.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Ignore filter", None))
        self.groupBox.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Category", None))
        self.button_category_filters.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Category Filters", None))
        self.button_settings_apply.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Apply", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"Video metadata", None))
        self.lineedit_tags.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Tags == Categories", None))
        self.label_author.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Author: ", None))
        self.label_likes.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Rating:", None))
        self.label_title.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Title:", None))
        self.label_image_url.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Image URL", None))
        self.lineedit_metadata_url.setText("")
        self.lineedit_metadata_url.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Enter PornHub or HQPorner Video URL", None))
        self.label.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Actress:", None))
        self.lineedit_actress.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"For HQPorner.com only", None))
        self.label_video_metadata_url.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Video URL:", None))
        self.label_tags.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Tags:", None))
        self.label_views.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Views:", None))
        self.label_date.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Date:", None))
        self.label_duration.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Duration:", None))
        self.button_download_thumbnail.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Download thumbnail", None))
        self.button_get_metadata.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Get metadata", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Porn_Fetch_widget", u"User Metadata", None))
        self.button_user_information.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Get Information", None))
        self.button_download_avatar.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Not implemented", None))
        self.button_user_biography.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Get User's Biography", None))
        self.label_user_avatar.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Avatar:", None))
        self.label_user_relationship.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Relationship: ", None))
        self.label_user_ethnicity.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Ethnicity: ", None))
        self.label_user_name.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Name: ", None))
        self.label_user_video_views.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Video views:", None))
        self.label_user_hair_color.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Hair color: ", None))
        self.label_user_videos_watched.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Videos watched;", None))
        self.label_user_profile_views.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Profile views: ", None))
        self.label_user_hobbies.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Hobbies:", None))
        self.label_user_interested_in.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Interested in: ", None))
        self.label_user_height.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Height: ", None))
        self.label_user_piercings.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Piercings:", None))
        self.label_user_fake_breasts.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Fake breasts:", None))
        self.label_user_gender.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Gender:", None))
        self.label_user_tattoos.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Tattoos:", None))
        self.label_user_turn_ons.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Turn ons:", None))
        self.lineedit_user_avatar.setPlaceholderText(QCoreApplication.translate("Porn_Fetch_widget", u"Not implemented yet", None))
        self.label_user_url.setText(QCoreApplication.translate("Porn_Fetch_widget", u"User URL: ", None))
        self.button_switch_video_metadata.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Video", None))
        self.button_switch_user_metadata.setText(QCoreApplication.translate("Porn_Fetch_widget", u"User", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Porn_Fetch_widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Cantarell'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Project API: PHUB v4</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">See https://github.com/Egsagon/PHUB</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top"
                        ":0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please like his project!</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Graphical User Interface was written in PySide6, which is maintained, by the Qt company:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margi"
                        "n-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">https://qt.io</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Source of this Project:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">https://github.com/EchterAlsFake/Porn_Fetch</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Exte"
                        "rnal libraries:<br /><br />1) tqdm</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2) PySide6</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3) BeautifulSoup</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4) PHUB</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5) wget</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6) requests</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                        ">Copyright (C) 2023 EchterAlsFake | Johannes Habel</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Graphics:<br /><br />Download Icon: by https://iconscout.com/contributors/kmgdesignid on Iconscout.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Account Icon: by https://iconscout.com/contributors/rengised on Iconscout.com</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Settings Icon: by https://iconscout.com/contributors/boosticon on Iconscout.com</p></body></html>", None))
        self.group_status.setTitle("")
        self.button_video.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Video", None))
        self.button_account.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Account", None))
        self.button_settings.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Settings", None))
        self.button_miscellaneus.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Miscellaneous", None))
        self.button_credits.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Credits", None))
        self.label_status.setText(QCoreApplication.translate("Porn_Fetch_widget", u"Status:", None))
    # retranslateUi

