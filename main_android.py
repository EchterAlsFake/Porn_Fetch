try:
    import sys
    import threading
    from PySide6.QtCore import QObject, Slot, Signal, QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine, QQmlContext
    from PySide6.QtQuickControls2 import QQuickStyle

# Import the pre-existing check_video function
    from src.backend.shared_functions import check_video
except Exception as e:
    import traceback
    import sys
    error = traceback.format_exc()
    from PySide6.QtWidgets import QWidget, QApplication, QLabel
    class Fortnite(QWidget):
        def __init__(self):
            super().__init__()
            self.msg_box = QLabel(self)
            self.msg_box.setText(error)
    
    app = QApplication(sys.argv)
    w = Fortnite()
    w.show()
    app.exec()


class VideoDownloader(QObject):
    titleChanged = Signal(str)
    progressChanged = Signal(int, int)

    @Slot(str, str)
    def downloadVideo(self, url, quality):
        if not url:
            return
        # Run download in a separate thread to avoid UI blocking
        def _worker():
            try:
                video = check_video(url)
                # Emit title once retrieved
                self.titleChanged.emit(video.title)
                # Start download with progress callback
                try:
                    video.download(
                    quality=quality,
                    downloader="default",
                    callback=self._on_progress,
                    remux=False,
                    path="/storage/emulated/0/Download/"
                    )

                except TypeError:
                    video.download(
                        quality=quality,
                        downloader="threaded",
                        display=self._on_progress,
                        remux=False,
                        path="/storage/emulated/0/Download/"
                    )

            except Exception as e:
                print(f"Error checking or downloading video: {e}")

        threading.Thread(target=_worker, daemon=True).start()

    def _on_progress(self, current, total):
        # Emit progress updates to QML
        self.progressChanged.emit(current, total)

if __name__ == "__main__":
    # Set Material dark style
    QQuickStyle.setStyle("Material")

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # Expose our downloader to QML
    downloader = VideoDownloader()
    ctx = engine.rootContext()
    ctx.setContextProperty("backend", downloader)

    engine.load(QUrl.fromLocalFile("main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())

