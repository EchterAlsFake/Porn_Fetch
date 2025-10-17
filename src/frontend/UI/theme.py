"""
Contains the theme for Porn Fetch's main UI. This is a massive rewrite starting from v3.7+
100% written by ChatGPT. I may not be a good designer, nor a good programmer, but I know how
to use ChatGPT to build a working app, and that's all that counts.

:)
"""

from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QApplication, QComboBox, QListView, QFrame, QWidget, QLineEdit, QTextEdit, QPlainTextEdit,
                               QSpinBox, QDoubleSpinBox, QAbstractButton)


"""This is the main stylesheet"""
QSS = """
/* --- Base --- */
QWidget { color:#EAEAEA; background:#1f1f21; font-size:13px; }
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
  background:#2a2b2e; color:#EAEAEA; border:1px solid #3a3b3f; border-radius:8px; padding:6px 8px;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus { border:2px solid #2f80ed; }

/* --- Buttons --- */
QPushButton {
  border:1px solid #3a3b3f; background:#2a2b2e; color:#EAEAEA; border-radius:8px; padding:6px 12px;
}
QPushButton:hover { background:#323338; }
QPushButton[intent="primary"] { background:#3b82f6; border-color:#3b82f6; color:white; }
QPushButton[intent="success"] { background:#22c55e; border-color:#22c55e; color:#071a0e; }
QPushButton[intent="danger"]  { background:#ef4444; border-color:#ef4444; color:white; }
QPushButton[appearance="flat"] { background:transparent; border-color:transparent; color:#D0D1D6; }
QPushButton[size="lg"] { padding:10px 16px; font-weight:600; }

/* --- Segmented top nav (works on QPushButton or QToolButton) --- */
QAbstractButton[seg="1"] {
  background:#262628; border:1px solid #333437; color:#D7D8DD; padding:6px 12px; border-radius:10px;
}
QAbstractButton[seg="1"]:checked { background:#3b82f6; border-color:#3b82f6; color:white; }

/* --- Tree / headers --- */
QTreeWidget { background:#262628; border:1px solid #333437; border-radius:12px; alternate-background-color:#232427; }
QTreeWidget::item:selected { background:#2f80ed; color:white; }
QHeaderView::section { background:#2a2b2e; color:#C8C9CD; border:none; border-right:1px solid #333437; padding:6px 8px; }

/* --- Scrollbars --- */
QScrollBar:vertical { width:10px; background:transparent; margin:4px; }
QScrollBar::handle:vertical { min-height:24px; background:#44464b; border-radius:5px; }
QScrollBar:horizontal { height:10px; background:transparent; margin:4px; }
QScrollBar::handle:horizontal { min-width:24px; background:#44464b; border-radius:5px; }

/* --- Progress --- */
QProgressBar { background:#2a2b2e; border:1px solid #3a3b3f; border-radius:8px; color:#D7D8DD; text-align:center; padding:3px; }
QProgressBar::chunk { background:#3b82f6; border-radius:7px; }
QProgressBar[role="convert"]::chunk { background:#22c55e; }   /* converting */
QProgressBar[role="total"]::chunk { background:#3b82f6; }     /* total */

/* --- TextBrowser (your “reader”) --- */
QTextBrowser { background:#0b1220; color:#e5e7eb; border:1px solid #1f2937; border-radius:12px; padding:12px; }
QTextBrowser:focus { border:1px solid #60a5fa; }

QAbstractButton[seg="1"]:checked {
  background:#3b82f6; border-color:#3b82f6; color:white;
}

/* Tree selection + header alignment */
QTreeWidget::item:selected { background:#2f80ed; color:white; }
QHeaderView::section { background:#2a2b2e; padding:6px 8px; font-weight:500; }

/* Popup container */
QComboBox QAbstractItemView {
  background: #2a2b2e;
  border: 1px solid #3a3b3f;
  border-radius: 8px;
  padding: 6px;                 /* inset around the list */
  outline: 0;
  selection-background-color: transparent;  /* we'll style items ourselves */
}

/* Each entry “card” */
QComboBox QAbstractItemView::item {
  padding: 6px 8px;
  border: 1px solid #3a3b3f;    /* the outline */
  border-radius: 8px;
  margin: 2px 0;                /* may be ignored on some platforms – see code below */
}

/* Hover / selected states */
QComboBox QAbstractItemView::item:hover {
  border-color: #4b8dff;
  background: rgba(59,130,246,0.08);
}
QComboBox QAbstractItemView::item:selected {
  border: 2px solid #3b82f6;
  background: rgba(59,130,246,0.16);
  color: white;
}

/* subtle card you already have */
*[variant="card"] {
  background:#26292f; border:1px solid #3d4148; border-radius:12px;
}

/* on-demand highlight borders */
*[highlight="accent"]  { border:2px solid #3b82f6; border-radius:12px; }
*[highlight="success"] { border:2px solid #22c55e; border-radius:12px; }
*[highlight="warning"] { border:2px solid #f59e0b; border-radius:12px; }

QTreeView::item { height: 28px; }             /* bigger row targets */
QHeaderView::section { font-weight: 500; }     /* clearer hierarchy */

QComboBox QAbstractItemView { padding:6px; border-radius:8px; }
QComboBox QAbstractItemView::item { padding:6px 8px; border:1px solid #3a3b3f; border-radius:8px; margin:2px 0; }
QComboBox QAbstractItemView::item:hover    { border-color:#4b8dff; background:rgba(59,130,246,.08); }
QComboBox QAbstractItemView::item:selected { border:2px solid #3b82f6; background:rgba(59,130,246,.16); color:white; }

/* Base: neutral 2px ring on interactive widgets */
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit,
QSpinBox, QDoubleSpinBox, QAbstractButton {
  border: 2px solid #3a3b3f;          /* neutral ring */
  border-radius: 8px;
}

/* Mouse hover ring (subtle) */
QLineEdit:hover, QComboBox:hover, QTextEdit:hover, QPlainTextEdit:hover,
QSpinBox:hover, QDoubleSpinBox:hover, QAbstractButton:hover {
  border-color: #4b8dff;               /* hover ring */
}

/* Keyboard focus ring (strong) */
*[kbd="1"],                            /* set by our event filter below */
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QAbstractButton:focus {
  border-color: #3b82f6;               /* focus ring */
}

/* Don’t show hover/focus ring for disabled */
*:disabled { border-color: #2c2d31; }

"""

def apply_theme(app: QApplication):
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor("#1f1f21"))
    pal.setColor(QPalette.Base, QColor("#262628"))
    pal.setColor(QPalette.AlternateBase, QColor("#232427"))
    pal.setColor(QPalette.Text, QColor("#EAEAEA"))
    pal.setColor(QPalette.Button, QColor("#2a2b2e"))
    pal.setColor(QPalette.ButtonText, QColor("#EAEAEA"))
    pal.setColor(QPalette.Highlight, QColor("#3b82f6"))
    pal.setColor(QPalette.HighlightedText, Qt.white)
    pal.setColor(QPalette.PlaceholderText, QColor("#8b8f97"))
    app.setPalette(pal)
    app.setStyleSheet(QSS)

def mark(w, *, intent=None, size=None, flat=False, seg=False, role=None):
    if intent: w.setProperty("intent", intent)
    if size: w.setProperty("size", size)
    if flat: w.setProperty("appearance", "flat")
    if seg: w.setProperty("seg", "1")
    if role: w.setProperty("role", role)    # for progress bars etc.
    w.style().unpolish(w); w.style().polish(w)

def pretty_combo(combo: QComboBox):
    view = QListView()
    view.setSpacing(6)  # space between outlined items
    view.setFrameShape(QFrame.NoFrame)  # we draw the border in QSS
    combo.setView(view)

def outline(widget, mode="accent"):
    widget.setProperty("highlight", mode)
    widget.style().unpolish(widget); widget.style().polish(widget)


class FocusOutlineFilter(QObject):
    def eventFilter(self, obj: QObject, ev: QEvent) -> bool:
        et = ev.type()
        keyboard_reasons = {Qt.FocusReason.TabFocusReason, Qt.FocusReason.BacktabFocusReason,
                            Qt.FocusReason.ShortcutFocusReason}
        if et == QEvent.Type.FocusIn:
            # keyboard-driven focus? (chatgpt why do you put a question mark there? LMAO)
            try:
                reason = ev.reason()  # QFocusEvent

            except Exception:
                reason = Qt.OtherFocusReason
            obj.setProperty("kbd", "1" if reason in keyboard_reasons else "0")
            _repolish(obj)
        elif et == QEvent.Type.FocusOut:
            obj.setProperty("kbd", "0")
            _repolish(obj)
        # we rely on native :hover, so no Enter/Leave handling needed
        return False

def _repolish(w: QObject):
    if isinstance(w, QWidget):
        w.setStyleSheet(w.styleSheet())   # re-evaluate inline (even if empty)
        w.style().unpolish(w)
        w.style().polish(w)
        w.update()

def install_focus_outline(root: QWidget):
    """Attach to all interactive widgets now (call again after dynamic UI changes)."""
    filter = FocusOutlineFilter(root)
    root._focus_outline_filter = filter  # keep a reference
    classes = [QLineEdit, QComboBox, QTextEdit, QPlainTextEdit,
               QSpinBox, QDoubleSpinBox, QAbstractButton]
    for cls in classes:
        for w in root.findChildren(cls):
            w.installEventFilter(filter)
