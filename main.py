import ctypes
import os
import sys
from PySide6.QtCore import QObject, Slot

class SparkleUpdater(QObject):
    def __init__(self, feed_url: str | None = None):
        super().__init__()

        # In a macOS .app:
        # sys.executable -> .../MyApp.app/Contents/MacOS/MyApp
        macos_dir = os.path.dirname(os.path.realpath(sys.executable))
        frameworks_dir = os.path.realpath(os.path.join(macos_dir, "..", "Frameworks"))
        dylib_path = os.path.join(frameworks_dir, "sparkle_bridge.dylib")

        self._lib = ctypes.CDLL(dylib_path)

        # Define signatures
        self._lib.sparkle_start_updater.argtypes = [ctypes.c_char_p]
        self._lib.sparkle_start_updater.restype = None

        self._lib.sparkle_check_for_updates.argtypes = []
        self._lib.sparkle_check_for_updates.restype = None

        self._lib.sparkle_check_for_updates_in_background.argtypes = []
        self._lib.sparkle_check_for_updates_in_background.restype = None

        self._lib.sparkle_can_check_for_updates.argtypes = []
        self._lib.sparkle_can_check_for_updates.restype = ctypes.c_int

        # Start Sparkle once (use Info.plist SUFeedURL if feed_url is None)
        if feed_url:
            self._lib.sparkle_start_updater(feed_url.encode("utf-8"))
        else:
            self._lib.sparkle_start_updater(None)

    @Slot()
    def check_for_updates(self):
        # Must be called from Qt main thread (your UI thread)
        self._lib.sparkle_check_for_updates()

    @Slot()
    def check_for_updates_in_background(self):
        self._lib.sparkle_check_for_updates_in_background()

    def can_check_for_updates(self) -> bool:
        return bool(self._lib.sparkle_can_check_for_updates())


from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sparkle = SparkleUpdater(
            feed_url=None  # use SUFeedURL from Info.plist
        )

        menubar = QMenuBar(self)
        self.setMenuBar(menubar)

        app_menu = menubar.addMenu("App")
        check_action = app_menu.addAction("Check for Updates…")
        check_action.triggered.connect(self.sparkle.check_for_updates)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()