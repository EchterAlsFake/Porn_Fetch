import sys
import os
from src.frontend.UI import resources
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

def main():
    # Enable the modern Material Design style built into Qt Quick Controls.
    # This automatically gives us nice hover effects, ripples, and clean dark colors
    # without needing to write custom CSS-like styling in QML.
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Dark"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_ACCENT"] = "Blue"

    # Initialize the GUI application
    app = QGuiApplication(sys.argv)
    
    # Initialize the QML engine which parses and runs the .qml files
    engine = QQmlApplicationEngine()
    
    # Resolve the absolute path to Settings.qml
    qml_file = Path(__file__).parent / "Home.qml"
    
    # Load the QML file
    engine.load(qml_file)

    # If the engine failed to load the root objects (e.g., due to syntax error), exit.
    if not engine.rootObjects():
        print("Failed to load Settings.qml. Check for syntax errors.")
        sys.exit(-1)

    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
