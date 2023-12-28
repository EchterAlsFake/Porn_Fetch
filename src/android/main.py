# This Python file uses the following encoding: utf-8
import requests
import sys
import os
from frontend.ui_form import Ui_Porn_Fetch
from frontend.one_time_setup import Ui_Widget
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QLabel
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject
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


class Setup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        send_error_log(os.getcwd())
        self.threadpool = QThreadPool()
        self.ui.pushButton.clicked.connect(self.get_output_path)


    def get_output_path(self):
        if os.path.exists("/storage/emulated/0/Download"):
            send_error_log("Storage Download location exists!")

            with open("/storage/emulated/0/Download/test.txt", "w") as x:
                x.write("""Hello World""")
                send_error_log("Successfully wrote file")
                x.close()

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
        self.ui.button_output_path.clicked.connect(self.get_output_path)
        self.ui.button_download.clicked.connect(self.download_video)

    def update_progress(self, pos, total):
        self.ui.button_progressbar.setMaximum(total)
        self.ui.button_progressbar.setValue(pos)

    def download_video(self):
        url = self.ui.lineedit_url.text()
        quality = self.quality
        output_path = self.directory

        video = Client(language="en").get(url)

        try:
            self.thread = Download(video=video, quality=quality, output_path=output_path)
            self.thread.signals.progress.connect(self.update_progress)
            self.threadpool.start(self.thread)

        except Exception as e:
            send_error_log(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Setup()
    w.show()
    app.exec()