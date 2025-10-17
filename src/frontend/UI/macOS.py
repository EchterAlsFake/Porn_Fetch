"""
This is the startup file for macOS. Porn Fetch will at startup check if the executable was executed in a macOS
(.dmg) container. If yes, the user will receive a Dialog asking to move the executable of Porn Fetch out of the
container into the Applications folder in Finder and then start Porn Fetch again from Launchpad.

This is the correct and clean solution for Python Apps on macOS. It's expected this way, however I moved it into
this file, to split the main code a little bit, since this is only needed once and I probably don't have
to work a lot here anymore :)
"""



import sys
from PySide6.QtWidgets import QApplication, QWidget, QTextBrowser, QVBoxLayout, QPushButton

class Notification(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 600, 600)
        self.setStyleSheet("""
QWidget: {
color: #ECECEC;  /* Brightened for better contrast */
background-color: #262626; /* Darkened for better contrast */
border: none}
""")
        self.layout = QVBoxLayout()
        self.close_button = QPushButton("Close")
        self.close_button.setMinimumHeight(30)
        self.msg_box = QTextBrowser(self)
        self.msg_box.setText("""
Please move Porn Fetch into your applications folder. You can do that by opening 'Finder' and dragging the Porn Fetch
executable you just clicked on, into the 'Applications' folder that you'll see in Finder. After that, you can open 'Launchpad'
and type 'Porn Fetch'. You'll find it there and can run it easily from Launchpad and also add it to your application bar at
the bottom.

This is an intended behaviour from macOS and all applications follow this scheme. 
Thank you for your patience :)
""")
        self.msg_box.setObjectName("reader")
        self.msg_box.setStyleSheet("""
/* Apply to a QTextBrowser with objectName "reader" */
#reader {
background: #0b1220;            /* near-black with a hint of blue */
color: #e5e7eb;                 /* gray-200 */
border: 1px solid #1f2937;      /* slate-800 */
border-radius: 12px;
padding: 12px;
selection-background-color: rgba(96, 165, 250, 0.28); /* soft blue */
selection-color: #0b1220;
font-family: Inter, Segoe UI, Roboto, "Helvetica Neue", Arial, sans-serif;
font-size: 14px;
line-height: 1.35;
}

#reader img, #reader table {
margin: 6px;
}

/* Vertical scrollbar */
#reader QScrollBar:vertical {
width: 10px;
margin: 8px 4px 8px 0;
background: transparent;
border: none;
}
#reader QScrollBar::handle:vertical {
min-height: 24px;
background: #374151;            /* gray-700 */
border-radius: 8px;
}
#reader QScrollBar::handle:vertical:hover {
background: #4b5563;            /* gray-600 */
}
#reader QScrollBar::add-line:vertical,
#reader QScrollBar::sub-line:vertical { height: 0; }
#reader QScrollBar::add-page:vertical,
#reader QScrollBar::sub-page:vertical { background: transparent; }

/* Horizontal scrollbar */
#reader QScrollBar:horizontal {
height: 10px;
margin: 0 8px 4px 8px;
background: transparent;
border: none;
}
#reader QScrollBar::handle:horizontal {
min-width: 24px;
background: #374151;
border-radius: 8px;
}
#reader QScrollBar::handle:horizontal:hover {
background: #4b5563;
}
#reader QScrollBar::add-line:horizontal,
#reader QScrollBar::sub-line:horizontal { width: 0; }
#reader QScrollBar::add-page:horizontal,
#reader QScrollBar::sub-page:horizontal { background: transparent; }

#reader:focus {
border: 1px solid #60a5fa;      /* blue-400 */
}
""")
        self.layout.addWidget(self.msg_box)
        self.layout.addWidget(self.close_button)
        self.setLayout(self.layout)
        self.close_button.setStyleSheet("""
QPushButton {
background-color: #7B1FA2; /* Purple */
color: white;
border-radius: 8px;
}

QPushButton:hover {
background-color: #9575CD; /* Lighter violet */
}

QPushButton:pressed {
background-color: #6A1B9A; /* Dark purple */
}

""")
        self.close_button.clicked.connect(self.close)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

def check_macos():
    app = QApplication(sys.argv)
    w = Notification()
    w.show()
    sys.exit(app.exec())