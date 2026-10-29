"""Minimal PySide/QML probe, independent of Porn Fetch's dependencies."""
import os
import sys
from pathlib import Path

# This probe targets the Intel simulator. Qt's raster backend still presents via
# Metal on iOS; OpenGL reaches Apple's CPU renderer on this VM instead.
if sys.platform == "ios":
    os.environ.setdefault("QT_QUICK_BACKEND", "rhi")
    os.environ.setdefault("QSG_RHI_BACKEND", "opengl")
    os.environ.setdefault("QSG_RENDER_LOOP", "basic")
else:
    os.environ.setdefault("QT_QUICK_BACKEND", "software")

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load(str(Path(__file__).parent / "qml" / "Main.qml"))
if not engine.rootObjects():
    raise SystemExit("QML failed to load")
print("HELLO_WORLD_PYSIDE_STARTED", sys.version, sys.platform, flush=True)
if "--smoke-test" in sys.argv:
    QTimer.singleShot(300, app.quit)
raise SystemExit(app.exec())
