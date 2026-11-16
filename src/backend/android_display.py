"""Event-driven adapter for Android window geometry and keyboard navigation."""
import json
from pathlib import Path

from PySide6.QtCore import Property, QFileSystemWatcher, QObject, Signal, Slot, QUrl, QCoreApplication, QEvent, Qt
from PySide6.QtGui import QDesktopServices, QKeyEvent


class AndroidDisplay(QObject):
    outlineChanged = Signal()
    keyboardNavigationChanged = Signal()
    televisionChanged = Signal()
    carStateChanged = Signal()
    webLinkRequested = Signal(str)

    def __init__(self, private_directory: str = "", parent=None):
        super().__init__(parent)
        self._outline = {}
        self._path = Path(private_directory) / "display-outline.json" if private_directory else None
        self._keyboard_navigation = self._path is None
        self._television = False
        self._car_state = {}
        self._car_controls = False
        self._url_handlers_installed = False
        self._watcher = QFileSystemWatcher(self)
        if self._path is not None:
            self._watcher.addPath(str(self._path.parent))
            self._watcher.directoryChanged.connect(self.refresh)
            self.refresh()

    @Property("QVariantMap", notify=outlineChanged)
    def outline(self):
        return self._outline

    @Property(bool, notify=keyboardNavigationChanged)
    def keyboardNavigation(self):
        return self._keyboard_navigation or self._car_state.get("controllerNavigation", False) is True

    @Property(bool, notify=televisionChanged)
    def television(self):
        return self._television

    @Property(bool, notify=carStateChanged)
    def automotive(self):
        return self._car_state.get("automotive", False) is True

    @Property(bool, notify=carStateChanged)
    def carMode(self):
        return self.automotive or self._car_controls or self._car_state.get("carMode", False) is True

    @Property(bool, notify=carStateChanged)
    def systemNavigation(self):
        return self.automotive and self._car_state.get("systemNavigation", False) is True

    @Property(bool, notify=carStateChanged)
    def interactionBlocked(self):
        return self.automotive and self._car_state.get("restricted", False) is True

    @Property(bool, notify=carStateChanged)
    def restrictionsKnown(self):
        return self._car_state.get("restrictionsKnown", False) is True

    @Property(bool, notify=carStateChanged)
    def foreground(self):
        return self._car_state.get("foreground", True) is True

    @Property(int, notify=carStateChanged)
    def pauseGeneration(self):
        return self._car_state.get("pauseGeneration", 0)

    @Slot(bool)
    def setCarControls(self, enabled):
        if enabled != self._car_controls:
            self._car_controls = enabled
            self.carStateChanged.emit()

    @Slot(QObject, int)
    def sendNavigationKey(self, window, key):
        """Let native selectors handle a rotary detent like an ordinary arrow key."""
        for event_type in (QEvent.Type.KeyPress, QEvent.Type.KeyRelease):
            QCoreApplication.sendEvent(window, QKeyEvent(event_type, key, Qt.KeyboardModifier.NoModifier))

    def install_url_handlers(self):
        """TVs and car screens show addresses without requiring a browser app."""
        for scheme in ("http", "https"):
            QDesktopServices.setUrlHandler(scheme, self, "open_web_link")
        self._url_handlers_installed = True

    @Slot(QUrl)
    def open_web_link(self, url):
        if self.interactionBlocked:
            return
        if self._television or self.carMode:
            self.webLinkRequested.emit(url.toString())
        else:
            # Qt bypasses this handler when openUrl is called from inside it.
            QDesktopServices.openUrl(url)

    def close(self):
        if self._url_handlers_installed:
            for scheme in ("http", "https"):
                QDesktopServices.unsetUrlHandler(scheme)
            self._url_handlers_installed = False

    def refresh(self, *_):
        if self._path is None:
            return
        previous_keyboard = self.keyboardNavigation
        try:
            state = json.loads((self._path.parent / "automotive-state.json").read_text(encoding="utf-8"))
            if isinstance(state, dict) and state != self._car_state:
                self._car_state = state
                self.carStateChanged.emit()
        except (OSError, ValueError):
            pass
        try:
            geometry = json.loads(self._path.read_text(encoding="utf-8"))
            if geometry["width"] <= 0 or geometry["height"] <= 0 or len(geometry["corners"]) != 4:
                raise ValueError("Invalid window outline")
            for corner in geometry["corners"]:
                if corner["radius"] < 0:
                    raise ValueError("Invalid corner radius")
                float(corner["x"]), float(corner["y"])
        except (OSError, ValueError, KeyError, TypeError):
            if self.keyboardNavigation != previous_keyboard:
                self.keyboardNavigationChanged.emit()
            return
        keyboard_navigation = geometry.get("keyboardNavigation", False) is True
        television = geometry.get("television", False) is True
        if television != self._television:
            self._television = television
            self.televisionChanged.emit()
        self._keyboard_navigation = keyboard_navigation
        if self.keyboardNavigation != previous_keyboard:
            self.keyboardNavigationChanged.emit()
        if geometry != self._outline:
            self._outline = geometry
            self.outlineChanged.emit()
