# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_batch.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Batch(object):
    def setupUi(self, Batch):
        if not Batch.objectName():
            Batch.setObjectName(u"Batch")
        Batch.resize(1151, 600)
        self.gridLayout = QGridLayout(Batch)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_batch_disclaimer_1 = QLabel(Batch)
        self.label_batch_disclaimer_1.setObjectName(u"label_batch_disclaimer_1")

        self.verticalLayout_5.addWidget(self.label_batch_disclaimer_1)

        self.batch_button_help = QPushButton(Batch)
        self.batch_button_help.setObjectName(u"batch_button_help")

        self.verticalLayout_5.addWidget(self.batch_button_help)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.batch_lineedit_model_url = QLineEdit(Batch)
        self.batch_lineedit_model_url.setObjectName(u"batch_lineedit_model_url")

        self.gridLayout_12.addWidget(self.batch_lineedit_model_url, 1, 1, 1, 1)

        self.batch_label_model_url = QLabel(Batch)
        self.batch_label_model_url.setObjectName(u"batch_label_model_url")

        self.gridLayout_12.addWidget(self.batch_label_model_url, 1, 0, 1, 1)

        self.batch_button_add_model_url = QPushButton(Batch)
        self.batch_button_add_model_url.setObjectName(u"batch_button_add_model_url")

        self.gridLayout_12.addWidget(self.batch_button_add_model_url, 1, 2, 1, 1)

        self.batch_button_add_playlist_url = QPushButton(Batch)
        self.batch_button_add_playlist_url.setObjectName(u"batch_button_add_playlist_url")

        self.gridLayout_12.addWidget(self.batch_button_add_playlist_url, 2, 2, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.batch_button_update = QPushButton(Batch)
        self.batch_button_update.setObjectName(u"batch_button_update")

        self.horizontalLayout_4.addWidget(self.batch_button_update)

        self.batch_button_download = QPushButton(Batch)
        self.batch_button_download.setObjectName(u"batch_button_download")

        self.horizontalLayout_4.addWidget(self.batch_button_download)

        self.batch_button_retry_failed = QPushButton(Batch)
        self.batch_button_retry_failed.setObjectName(u"batch_button_retry_failed")

        self.horizontalLayout_4.addWidget(self.batch_button_retry_failed)


        self.gridLayout_12.addLayout(self.horizontalLayout_4, 3, 0, 1, 3)

        self.batch_label_playlist_url = QLabel(Batch)
        self.batch_label_playlist_url.setObjectName(u"batch_label_playlist_url")

        self.gridLayout_12.addWidget(self.batch_label_playlist_url, 2, 0, 1, 1)

        self.batch_lineedit_playlist_url = QLineEdit(Batch)
        self.batch_lineedit_playlist_url.setObjectName(u"batch_lineedit_playlist_url")

        self.gridLayout_12.addWidget(self.batch_lineedit_playlist_url, 2, 1, 1, 1)

        self.batch_checkbox_custom_path = QCheckBox(Batch)
        self.batch_checkbox_custom_path.setObjectName(u"batch_checkbox_custom_path")

        self.gridLayout_12.addWidget(self.batch_checkbox_custom_path, 0, 0, 1, 2)

        self.batch_treewidget = QTreeWidget(Batch)
        self.batch_treewidget.setObjectName(u"batch_treewidget")

        self.gridLayout_12.addWidget(self.batch_treewidget, 4, 0, 1, 3)


        self.verticalLayout_5.addLayout(self.gridLayout_12)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.batch_label_downloaded_playlists = QLabel(Batch)
        self.batch_label_downloaded_playlists.setObjectName(u"batch_label_downloaded_playlists")

        self.gridLayout_11.addWidget(self.batch_label_downloaded_playlists, 0, 3, 1, 1)

        self.batch_lineedit_database_status = QLineEdit(Batch)
        self.batch_lineedit_database_status.setObjectName(u"batch_lineedit_database_status")
        self.batch_lineedit_database_status.setReadOnly(True)

        self.gridLayout_11.addWidget(self.batch_lineedit_database_status, 0, 1, 1, 2)

        self.batch_lineedit_downloaded_playlists = QLineEdit(Batch)
        self.batch_lineedit_downloaded_playlists.setObjectName(u"batch_lineedit_downloaded_playlists")
        self.batch_lineedit_downloaded_playlists.setReadOnly(True)

        self.gridLayout_11.addWidget(self.batch_lineedit_downloaded_playlists, 0, 4, 1, 1)

        self.batch_label_downloaded_models = QLabel(Batch)
        self.batch_label_downloaded_models.setObjectName(u"batch_label_downloaded_models")

        self.gridLayout_11.addWidget(self.batch_label_downloaded_models, 1, 3, 1, 1)

        self.batch_label_database_status = QLabel(Batch)
        self.batch_label_database_status.setObjectName(u"batch_label_database_status")

        self.gridLayout_11.addWidget(self.batch_label_database_status, 0, 0, 1, 1)

        self.batch_lineedit_downloaded_models = QLineEdit(Batch)
        self.batch_lineedit_downloaded_models.setObjectName(u"batch_lineedit_downloaded_models")
        self.batch_lineedit_downloaded_models.setReadOnly(True)

        self.gridLayout_11.addWidget(self.batch_lineedit_downloaded_models, 1, 4, 1, 1)

        self.batch_lineedit_downloaded_videos = QLineEdit(Batch)
        self.batch_lineedit_downloaded_videos.setObjectName(u"batch_lineedit_downloaded_videos")
        self.batch_lineedit_downloaded_videos.setReadOnly(True)

        self.gridLayout_11.addWidget(self.batch_lineedit_downloaded_videos, 1, 1, 1, 2)

        self.batch_label_downloaded_videos = QLabel(Batch)
        self.batch_label_downloaded_videos.setObjectName(u"batch_label_downloaded_videos")

        self.gridLayout_11.addWidget(self.batch_label_downloaded_videos, 1, 0, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout_11)


        self.gridLayout.addLayout(self.verticalLayout_6, 0, 0, 1, 1)


        self.retranslateUi(Batch)

        QMetaObject.connectSlotsByName(Batch)
    # setupUi

    def retranslateUi(self, Batch):
        Batch.setWindowTitle(QCoreApplication.translate("Batch", u"Batch", None))
        self.label_batch_disclaimer_1.setText(QCoreApplication.translate("Batch", u"DO NOT DOWNLOAD OTHER VIDEOS WHILE USING THIS FEATURE!", None))
        self.batch_button_help.setText(QCoreApplication.translate("Batch", u"Eplanation how this works (please read this)", None))
        self.batch_label_model_url.setText(QCoreApplication.translate("Batch", u"Model URL:", None))
        self.batch_button_add_model_url.setText(QCoreApplication.translate("Batch", u"Add", None))
        self.batch_button_add_playlist_url.setText(QCoreApplication.translate("Batch", u"Add", None))
        self.batch_button_update.setText(QCoreApplication.translate("Batch", u"Update", None))
        self.batch_button_download.setText(QCoreApplication.translate("Batch", u"Download", None))
        self.batch_button_retry_failed.setText(QCoreApplication.translate("Batch", u"Retry failed", None))
        self.batch_label_playlist_url.setText(QCoreApplication.translate("Batch", u"Playlist URL:", None))
        self.batch_checkbox_custom_path.setText(QCoreApplication.translate("Batch", u"Use a custom output path for evey playlist URL / Model URL independent of the output path you defined in settings (you'll be asked to enter one each time)", None))
        ___qtreewidgetitem = self.batch_treewidget.headerItem()
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("Batch", u"Progress", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("Batch", u"Remove", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Batch", u"Failed", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Batch", u"Downloaded", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Batch", u"Video count", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Batch", u"URL", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Batch", u"Type", None));
        self.batch_label_downloaded_playlists.setText(QCoreApplication.translate("Batch", u"Downloaded Playlists:", None))
        self.batch_label_downloaded_models.setText(QCoreApplication.translate("Batch", u"Downloaded Models:", None))
        self.batch_label_database_status.setText(QCoreApplication.translate("Batch", u"Database Status:", None))
        self.batch_label_downloaded_videos.setText(QCoreApplication.translate("Batch", u"Downloaded Videos:", None))
    # retranslateUi

