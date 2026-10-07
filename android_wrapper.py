"""Android debug wrapper script.

Imports the entire backend wrapped in try/except.
- If everything succeeds: displays "Hello World".
- If an exception occurs: displays the full traceback on screen and logs to stderr.
"""
from __future__ import annotations

import importlib
import os
import pkgutil
import sys
import traceback

# Ensure --android flag is set so backend modules know this is Android/mobile mode
if "--android" not in sys.argv:
    sys.argv.append("--android")


def import_entire_backend() -> None:
    """Import all modules in src.backend, src.database, src.licensing, and src.shared."""
    import src.backend
    import src.backend.application  # noqa: F401
    import src.database
    import src.licensing
    import src.shared

    for pkg in (src.backend, src.database, src.licensing, src.shared):
        if hasattr(pkg, "__path__"):
            for _, module_name, _ in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
                importlib.import_module(module_name)


QML_SOURCE = b"""
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: window
    visible: true
    width: 480
    height: 800
    title: hasError ? "Backend Error" : "Hello World"

    background: Rectangle {
        color: hasError ? "#1e1e1e" : "#121212"
    }

    Item {
        anchors.fill: parent
        anchors.margins: 16

        // Normal Hello World view
        Column {
            anchors.centerIn: parent
            spacing: 16
            visible: !hasError

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Hello World"
                font.pixelSize: 32
                font.bold: true
                color: "#4CAF50"
            }

            Label {
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Backend imported successfully!"
                font.pixelSize: 16
                color: "#B0BEC5"
            }
        }

        // Traceback view
        Column {
            anchors.fill: parent
            spacing: 12
            visible: hasError

            Label {
                text: "Backend Import Error"
                font.pixelSize: 20
                font.bold: true
                color: "#FF5252"
            }

            ScrollView {
                width: parent.width
                height: parent.height - 40
                clip: true

                TextArea {
                    width: parent.width
                    text: displayText
                    readOnly: true
                    wrapMode: TextEdit.Wrap
                    selectByMouse: true
                    font.family: "monospace"
                    font.pixelSize: 12
                    color: "#ECEFF1"
                    background: Rectangle {
                        color: "#263238"
                        radius: 6
                    }
                }
            }
        }
    }
}
"""


def main() -> int:
    # Initialize Qt Application
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication(sys.argv)
    except ImportError:
        from PySide6.QtGui import QGuiApplication
        app = QGuiApplication.instance() or QGuiApplication(sys.argv)

    # Attempt to style application
    try:
        from PySide6.QtQuickControls2 import QQuickStyle
        QQuickStyle.setStyle("Material")
    except Exception as err:
        print(f"Could not set Material style: {err}", file=sys.stderr, flush=True)

    # Attempt importing the entire backend
    backend_error: str | None = None
    try:
        import_entire_backend()
    except BaseException:
        backend_error = traceback.format_exc()

    has_error = backend_error is not None
    display_text = backend_error if has_error else "Hello World"

    if has_error:
        print("=" * 60, file=sys.stderr, flush=True)
        print("BACKEND IMPORT FAILED! Traceback:", file=sys.stderr, flush=True)
        print(backend_error, file=sys.stderr, flush=True)
        print("=" * 60, file=sys.stderr, flush=True)
    else:
        print("=" * 60, flush=True)
        print("Hello World: Backend imported successfully!", flush=True)
        print("=" * 60, flush=True)

    # Attempt loading QML UI
    qml_loaded = False
    try:
        from PySide6.QtQml import QQmlApplicationEngine
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("hasError", has_error)
        engine.rootContext().setContextProperty("displayText", display_text)
        engine.loadData(QML_SOURCE)
        if engine.rootObjects():
            qml_loaded = True
    except Exception as qml_err:
        print(f"QML initialization failed: {qml_err}", file=sys.stderr, flush=True)

    # Fallback to QtWidgets if QML could not be loaded
    if not qml_loaded:
        try:
            from PySide6.QtCore import Qt
            from PySide6.QtWidgets import QLabel, QMainWindow, QTextEdit, QVBoxLayout, QWidget

            window = QMainWindow()
            window.resize(480, 800)
            central = QWidget()
            layout = QVBoxLayout(central)
            if has_error:
                window.setWindowTitle("Backend Import Error")
                edit = QTextEdit()
                edit.setReadOnly(True)
                edit.setPlainText(display_text)
                layout.addWidget(edit)
            else:
                window.setWindowTitle("Hello World")
                label = QLabel("Hello World\n\nBackend imported successfully!")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(label)
            window.setCentralWidget(central)
            window.show()
        except Exception as widget_err:
            print(f"QtWidgets fallback failed: {widget_err}", file=sys.stderr, flush=True)

    if "--test" in sys.argv or os.environ.get("PORN_FETCH_TEST_ENV"):
        from PySide6.QtCore import QTimer
        QTimer.singleShot(100, app.quit)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
