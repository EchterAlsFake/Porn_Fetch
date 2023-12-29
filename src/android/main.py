# This Python file uses the following encoding: utf-8
import requests
import sys
import os

from frontend.ui_form import Ui_Porn_Fetch
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QTreeWidgetItem, QMessageBox
from PySide6.QtCore import QRunnable, QThreadPool, Signal, QObject, Qt, QSemaphore, QFile, QTextStream
from PySide6.QtGui import QIcon
from phub import Quality, Client, Video, errors

total_segments = 0
downloaded_segments = 0

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


try:
    import frontend.resources
    send_error_log("Successfully imported resources")

except Exception as e:
    send_error_log(f"{e}")


def get_output_path():
    if os.path.exists("/storage/emulated/0/Download"):
        if os.path.isfile("/storage/emulated/0/Download/test.txt"):
            send_error_log("Text.txt already exists")
            return True

        else:
            send_error_log("Storage Download location exists!")
            with open("/storage/emulated/0/Download/test.txt", "w") as x:
                x.write("""Hello World""")
                send_error_log("Successfully wrote file")
                x.close()
                return True

    else:
        send_error_log("Location doesn't exist... (FUCK)")


class QTreeWidgetSignal(QObject):
    """Signals needed across the QTreeWidget"""
    progress = Signal(Video)
    get_total = Signal(str, Quality)
    start_undefined_range = Signal()
    stop_undefined_range = Signal()


class Signals(QObject):
    finished = Signal()
    progress = Signal(int, int)
    total_progress = Signal(int, int)


class Download(QRunnable):
    def __init__(self, video, output_path, quality):
        super(Download, self).__init__()
        self.signals = Signals()
        self.video = video
        self.output_path = output_path
        self.quality = quality

    def callback(self, pos, total):
        self.signals.progress.emit(pos, total)

        global downloaded_segments
        downloaded_segments += 1  # Assuming each call represents one segment
        self.signals.total_progress.emit(downloaded_segments, total_segments)

    def run(self):
        try:
            self.video.download(self.output_path, quality=self.quality, display=self.callback)
            self.signals.finished.emit()
        except Exception as e:
            send_error_log(str(e))


class DownloadTreeWidget(QRunnable):
    def __init__(self, treeWidget, semaphore, quality):
        super(DownloadTreeWidget, self).__init__()
        self.treeWidget = treeWidget
        self.semaphore = semaphore
        self.quality = quality
        self.signals = QTreeWidgetSignal()

    def run(self):
        self.signals.start_undefined_range.emit()

        video_objects = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            checkState = item.checkState(0)
            if checkState == Qt.Checked:
                video_objects.append(item.data(0, Qt.UserRole))

        global total_segments, downloaded_segments
        total_segments = sum(
            [len(list(video.get_segments(quality=self.quality))) for video in video_objects])

        downloaded_segments = 0

        self.signals.stop_undefined_range.emit()
        for video in video_objects:
            self.signals.progress.emit(video)


class Porn_Fetch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.directory = None
        self.ui = Ui_Porn_Fetch()
        self.ui.setupUi(self)
        self.threadpool = QThreadPool()
        self.quality = Quality.BEST
        self.output_path = "/storage/emulated/0/Download/"
        self.client = Client()
        self.semaphore = QSemaphore(2)
        self.load_style()

        self.ui.button_download_tree_widget.clicked.connect(self.download_tree_widget)
        self.ui.button_select_all.clicked.connect(self.select_all_items)
        self.ui.button_unselect_all.clicked.connect(self.unselect_all_items)
        self.ui.button_get_model_videos.clicked.connect(self.get_model_videos)
        self.ui.button_download.clicked.connect(self.download_single_video)
        self.ui.button_home.clicked.connect(self.switch_home)
        self.ui.button_account.clicked.connect(self.switch_account)
        self.ui.button_login.clicked.connect(self.login)
        self.ui.button_get_liked_videos.clicked.connect(self.get_liked_videos)
        self.ui.button_get_watched_videos.clicked.connect(self.get_watched_videos)
        self.ui.button_get_recommended_videos.clicked.connect(self.get_recommended_videos)

    def load_style(self):
        """a simple function to load the icons for the buttons"""
        self.setWindowIcon(QIcon(":/images/graphics/logo_transparent.ico"))

        file_progress_pornhub = QFile(":/style/stylesheets/progressbar_pornhub.qss")
        file_progress_pornhub.open(QFile.ReadOnly | QFile.Text)
        stream_progress_pornhub = QTextStream(file_progress_pornhub)

        file_progressbar_total = QFile(":/style/stylesheets/progressbar_total.qss")
        file_progressbar_total.open(QFile.ReadOnly | QFile.Text)
        stream_progress_total = QTextStream(file_progressbar_total)

        file_stylesheet_button_blue = QFile(":/style/stylesheets/stylesheet_button_blue.qss")
        file_stylesheet_button_orange = QFile(":/style/stylesheets/stylesheet_button_orange.qss")
        file_stylesheet_button_purple = QFile(":/style/stylesheets/stylesheet_button_purple.qss")
        file_stylesheet_button_login = QFile(":/style/stylesheets/stylesheet_button_login.qss")
        file_stylesheet_button_logins = QFile(":/style/stylesheets/stylesheet_buttons_login.qss")

        file_stylesheet_button_blue.open(QFile.ReadOnly | QFile.Text)
        stream_button_blue = QTextStream(file_stylesheet_button_blue)
        file_stylesheet_button_logins.open(QFile.ReadOnly | QFile.Text)
        stream_button_logins = QTextStream(file_stylesheet_button_logins)
        file_stylesheet_button_login.open(QFile.ReadOnly | QFile.Text)
        stream_button_login = QTextStream(file_stylesheet_button_login)
        file_stylesheet_button_orange.open(QFile.ReadOnly | QFile.Text)
        stream_button_orange = QTextStream(file_stylesheet_button_orange)
        file_stylesheet_button_purple.open(QFile.ReadOnly | QFile.Text)
        stream_button_purple = QTextStream(file_stylesheet_button_purple)

        blue = stream_button_blue.readAll()
        orange = stream_button_orange.readAll()
        purple = stream_button_purple.readAll()
        login = stream_button_login.readAll()
        logins = stream_button_logins.readAll()


        self.ui.button_home.setStyleSheet(purple)
        self.ui.button_account.setStyleSheet(purple)
        self.ui.button_login.setStyleSheet(login)
        self.ui.button_get_watched_videos.setStyleSheet(logins)
        self.ui.button_get_liked_videos.setStyleSheet(logins)
        self.ui.button_get_recommended_videos.setStyleSheet(logins)
        self.ui.button_download.setStyleSheet(purple)
        self.ui.button_get_model_videos.setStyleSheet(purple)
        self.ui.button_download_tree_widget.setStyleSheet(purple)
        self.ui.button_select_all.setStyleSheet(orange)
        self.ui.button_unselect_all.setStyleSheet(blue)

        self.ui.progressbar_pornhub.setStyleSheet(stream_progress_pornhub.readAll())
        self.ui.progressbar_total.setStyleSheet(stream_progress_total.readAll())

    def switch_account(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def switch_home(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def update_progress(self, pos, total):
        self.ui.progressbar_pornhub.setMaximum(total)
        self.ui.progressbar_pornhub.setValue(pos)

    def update_total_progress(self, downloaded_segments, total_segments):
        self.ui.progressbar_total.setMaximum(total_segments)
        self.ui.progressbar_total.setValue(downloaded_segments)

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
        self.semaphore.release()

    def tree_widget_completed(self, video):
        self.thread = Download(video=video, quality=Quality.BEST, output_path=self.output_path)
        self.thread.signals.progress.connect(self.update_progress)
        self.thread.signals.total_progress.connect(self.update_total_progress)
        self.thread.signals.finished.connect(self.finished_download)
        self.threadpool.start(self.thread)

    def start_undefined_range(self):
        self.ui.progressbar_total.setRange(0, 0)

    def stop_undefined_range(self):
        self.ui.progressbar_total.setRange(0, 1)

    def download_tree_widget(self):
        semaphore = self.semaphore
        treeWidget = self.ui.treeWidget
        quality = self.quality
        download_tree_thread = DownloadTreeWidget(treeWidget=treeWidget, semaphore=semaphore, quality=quality)
        download_tree_thread.signals.progress.connect(self.tree_widget_completed)
        download_tree_thread.signals.start_undefined_range.connect(self.start_undefined_range)
        download_tree_thread.signals.stop_undefined_range.connect(self.stop_undefined_range)
        self.threadpool.start(download_tree_thread)

    def login(self):
        username = self.ui.lineedit_username.text()
        password = self.ui.lineedit_password.text()
        try:
            self.client = Client(username, password, language="en")
            self.switch_login_button_state()
            qmessage_box = QMessageBox()
            qmessage_box.setText("Login Successful")
            qmessage_box.exec()

        except errors.LoginFailed:
            qmessage_box = QMessageBox()
            qmessage_box.setText("Login failed!")
            qmessage_box.exec()

    def switch_login_button_state(self):
        file = QFile(":/style/stylesheets/stylesheet_switch_buttons_login_state.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        stylesheet = stream.readAll()

        self.ui.button_get_liked_videos.setStyleSheet(stylesheet)
        self.ui.button_get_watched_videos.setStyleSheet(stylesheet)
        self.ui.button_get_recommended_videos.setStyleSheet(stylesheet)

    def get_watched_videos(self):
        self.add_to_tree_widget(self.client.account.watched)
        self.switch_home()

    def get_liked_videos(self):
        self.add_to_tree_widget(self.client.account.liked)
        self.switch_home()

    def get_recommended_videos(self):
        self.add_to_tree_widget(self.client.account.recommended)
        self.switch_home()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        file = QFile(":/style/stylesheets/stylesheet.qss")
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())

    except Exception as e:
        send_error_log(f"Error applying stylesheet: {e}")

    if get_output_path():
        w = Porn_Fetch()
        w.show()

    else:
        label = QLabel("Porn Fetch can't write to your Download directory.")
        label.show()

    app.exec()