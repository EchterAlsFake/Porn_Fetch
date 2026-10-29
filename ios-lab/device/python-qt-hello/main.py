"""Embedded Python + static PySide Core/Gui test on the physical phone."""
import json
import os
from pathlib import Path
import sys

documents = Path.home() / "Documents"
documents.mkdir(parents=True, exist_ok=True)
sys.stdout = (documents / "python-qt-runtime.log").open("w", buffering=1)
sys.stderr = sys.stdout
os.environ["QT_LOGGING_RULES"] = "qt.rhi.*=true;qt.qpa.backingstore=true"

import PySide6
from PySide6.QtCore import QRect, Qt, QTimer, qInstallMessageHandler, qVersion
from PySide6.QtGui import QBackingStore, QColor, QFont, QGuiApplication, QPainter, QRegion, QWindow

qInstallMessageHandler(lambda kind, context, message: print(message, flush=True))
app = QGuiApplication(sys.argv)

class HelloWindow(QWindow):
    def __init__(self):
        super().__init__()
        self.backing = QBackingStore(self)
        self.frames = 0
        self.resize(375, 667)
        self.setTitle("Python and Qt on iPhone 7")

    def exposeEvent(self, event):
        if self.isExposed():
            self.render()

    def render(self):
        if not self.isExposed():
            return
        rectangle = QRect(0, 0, self.width(), self.height())
        self.backing.resize(self.size())
        self.backing.beginPaint(QRegion(rectangle))
        painter = QPainter(self.backing.paintDevice())
        painter.fillRect(rectangle, QColor("#172234"))
        painter.setPen(QColor("#eaf2ff"))
        font = QFont()
        font.setPixelSize(22)
        painter.setFont(font)
        painter.drawText(rectangle, Qt.AlignmentFlag.AlignCenter,
            "Hello Python + Qt!\n\nPython 3.15 / Qt " + qVersion() + "\nOn your real iPhone 7.")
        painter.end()
        self.backing.endPaint()
        self.backing.flush(QRegion(rectangle))
        self.frames += 1
        result = {"python": sys.version, "pyside": PySide6.__version__, "qt": qVersion(),
                  "platform": sys.platform, "frames": self.frames,
                  "exposed": self.isExposed(), "active": app.applicationState() == Qt.ApplicationState.ApplicationActive}
        (documents / "python-qt-result.json").write_text(json.dumps(result, indent=2))

window = HelloWindow()
window.show()
timer = QTimer()
timer.timeout.connect(window.render)
timer.start(2000)
sys.exit(app.exec())
