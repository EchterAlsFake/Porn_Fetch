from pathlib import Path
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl


class LicenseBridge(QObject):
    importFinished = Signal(bool, str)
    statusChanged = Signal()

    def __init__(self, manager: LicenseManager):
        super().__init__()
        self._manager = manager
        self._refresh_state()

    def _refresh_state(self):
        """Reads the current license state and updates properties."""
        res = self._manager.load_installed()
        self._is_valid = res.valid
        self._reason = res.reason
        self._data = res.data if res.data else {}
        self.statusChanged.emit()

    # noinspection PyPropertyDefinition
    @Property(bool, notify=statusChanged)
    def isValid(self):
        return self._is_valid

    # noinspection PyPropertyDefinition
    @Property(str, notify=statusChanged)
    def reason(self):
        return self._reason

    # noinspection PyPropertyDefinition
    @Property(str, notify=statusChanged)
    def licenseKey(self):
        return self._data.get("license_key", "")

    # noinspection PyPropertyDefinition
    @Property(list, notify=statusChanged)
    def features(self):
        return self._data.get("features", [])

    # noinspection PyPropertyDefinition
    @Property(bool, notify=statusChanged)
    def isPremium(self):
        # Checks if they have the specific feature unlocked
        return self.isValid and "full_unlock" in self.features

    @Slot(str)
    def installFromPath(self, file_url: str):
        """Called by QML when the user selects a license file."""
        # QML FileDialog returns a URL like 'file:///C:/...', convert it to a local Path
        local_path = Path(QUrl(file_url).toLocalFile())

        res = self._manager.install_from_file(local_path)
        self._refresh_state()
        self.importFinished.emit(res.valid, res.reason)
