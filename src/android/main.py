# This Python file uses the following encoding: utf-8
import requests
import sys
import os
from frontend.ui_form import Ui_Porn_Fetch
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QTreeWidgetItem
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Qt, QSemaphore
from phub import Quality, Client


def send_error_log(message):
    url = "http://192.168.2.103:8000/error-log/"
    data = {"message": message}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Error log sent successfully")
        else:
            print(f"Failed to send error log: {response.content}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def get_output_path():
    if os.path.exists("/storage/emulated/0/Download"):
        send_error_log("Storage Download location exists!")

        with open("/storage/emulated/0/Download/test.txt", "w") as x:
            x.write("""Hello World""")
            send_error_log("Successfully wrote file")
            x.close()
            return True

    else:
        send_error_log("Location doesn't exist... (FUCK)")


class Signals(QObject):
    finished = Signal()
    progress = Signal(int, int)


class Download(QRunnable):
    def __init__(self, video, output_path, quality):
        super(Download, self).__init__()
        self.signals = Signals()
        self.video = video
        self.output_path = output_path
        self.quality = quality

    def callback(self, pos, total):
        self.signals.progress.emit(pos, total)

    def run(self):
        try:
            self.video.download(self.output_path, quality=self.quality, display=self.callback)
            self.signals.finished.emit()
        except Exception as e:
            send_error_log(str(e))


class Porn_Fetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.directory = None
        self.ui = Ui_Porn_Fetch()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
        self.quality = Quality.BEST
        self.output_path = "/storage/emulated/0/Download"
        self.client = Client()

        self.ui.button_download_tree_widget.clicked.connect(self.download_tree_widget)
        self.ui.button_select_all.clicked.connect(self.select_all_items)
        self.ui.button_unselect_all.clicked.connect(self.unselect_all_items)
        self.ui.button_get_model_videos.clicked.connect(self.get_model_videos)
        self.ui.button_download.clicked.connect(self.download_single_video)

    def update_progress(self, pos, total):
        self.ui.button_progressbar.setMaximum(total)
        self.ui.button_progressbar.setValue(pos)

    def unselect_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Unchecked)

    def select_all_items(self):
        root = self.ui.treeWidget.invisibleRootItem()
        item_count = root.childCount()
        for i in range(item_count):
            item = root.child(i)
            item.setCheckState(0, Qt.Checked)

    def get_model_videos(self):
        url = self.ui.lineedit_model_url.text()
        videos = self.client.get_user(url)
        self.add_to_tree_widget(iterator=videos.videos)

    def download_single_video(self):
        iterator = []
        url = self.ui.lineedit_video_url.text()
        iterator.append(self.client.get(url))
        self.add_to_tree_widget(iterator=iterator)

    def add_to_tree_widget(self, iterator):
        for idx, video in enumerate(iterator):
            title = video.title
            item = QTreeWidgetItem(self.ui.treeWidget)
            item.setText(0, f"{idx}) {title}")
            item.setData(0, Qt.UserRole, video)
            item.setCheckState(0, Qt.Unchecked)

    def finished_download(self):
        ""

    def download_tree_widget(self):
        video_objects = []
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            item = self.ui.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                video_objects.append(item.data(0, Qt.UserRole))

        for video in video_objects:
            self.thread = Download(video=video, quality=Quality.BEST, output_path=self.output_path)
            self.thread.signals.progress.connect(self.update_progress)
            self.thread.signals.finished.connect(self.finished_download)
            self.threadpool.start(self.thread)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if get_output_path():
        w = Porn_Fetch()
        w.show()


    else:
        label = QLabel("Porn Fetch doesn't work on your Android Version.")
        label.show()

    app.exec()