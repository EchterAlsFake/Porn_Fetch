"""Open the session-only creator UI without starting application services.

Run: .venv/bin/python scripts/preview_creators.py
Use --width 390 --height 844 for a phone-sized preview, or --light/--contrast.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=900)
    parser.add_argument("--light", action="store_true")
    parser.add_argument("--contrast", action="store_true")
    parser.add_argument("--capture", type=Path, help="Save a preview screenshot and exit")
    args = parser.parse_args()
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Material")
    os.environ.setdefault("QT_QUICK_BACKEND", "software")
    from PySide6.QtCore import QObject, Property, QTimer, QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlApplicationEngine
    from PySide6.QtQuick import QQuickWindow  # Register the concrete window wrapper before loading QML.

    app = QGuiApplication(sys.argv[:1])
    class PreviewSettings(QObject):
        dark_mode = Property(bool, lambda self: not args.light, constant=True)
        high_contrast = Property(bool, lambda self: args.contrast, constant=True)
        accent_color = Property(str, lambda self: "#6550bd" if args.light else "#a69bff", constant=True)
        font_size = Property(int, lambda self: 12, constant=True)
        anonymous_mode = Property(bool, lambda self: False, constant=True)
        reduced_motion = Property(bool, lambda self: True, constant=True)

    settings = PreviewSettings()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("appSettings", settings)
    engine.load(QUrl.fromLocalFile(str(Path(__file__).resolve().parents[1] / "src/frontend/UI/CreatorsPreview.qml")))
    if not engine.rootObjects():
        return 1
    window = engine.rootObjects()[0]
    window.setWidth(args.width)
    window.setHeight(args.height)
    if args.capture:
        def capture():
            args.capture.parent.mkdir(parents=True, exist_ok=True)
            app.exit(0 if window.grabWindow().save(str(args.capture)) else 1)
        QTimer.singleShot(800, capture)
    result = app.exec()
    import shiboken6
    shiboken6.delete(engine)
    return result


if __name__ == "__main__":
    raise SystemExit(main())
