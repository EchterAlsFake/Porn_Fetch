"""Event-driven adapter for the outline published by the Android activity."""
import json
from pathlib import Path

from PySide6.QtCore import QObject, Property, Signal, QFileSystemWatcher


class AndroidDisplay(QObject):
    outlineChanged = Signal()

    def __init__(self, private_directory: str = "", parent=None):
        super().__init__(parent)
        self._outline = {}
        self._path = Path(private_directory) / "display-outline.json" if private_directory else None
        self._watcher = QFileSystemWatcher(self)
        if self._path is not None:
            self._watcher.addPath(str(self._path.parent))
            self._watcher.directoryChanged.connect(self.refresh)
            self.refresh()

    @Property("QVariantMap", notify=outlineChanged)
    def outline(self):
        return self._outline

    def refresh(self, *_):
        if self._path is None:
            return
        try:
            geometry = json.loads(self._path.read_text(encoding="utf-8"))
            if geometry["width"] <= 0 or geometry["height"] <= 0 or len(geometry["corners"]) != 4:
                return
            for corner in geometry["corners"]:
                if corner["radius"] < 0:
                    return
                float(corner["x"]), float(corner["y"])
        except (OSError, ValueError, KeyError, TypeError):
            return
        if geometry != self._outline:
            self._outline = geometry
            self.outlineChanged.emit()
