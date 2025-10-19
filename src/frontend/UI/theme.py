"""
Contains the theme for Porn Fetch's main UI. This is a massive rewrite starting from v3.7+
100% written by ChatGPT. I may not be a good designer, nor a good programmer, but I know how
to use ChatGPT to build a working app, and that's all that counts.

:)
"""
import random
import colorsys

from PySide6.QtCore import Qt, QObject, QEvent
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (QApplication, QComboBox, QListView, QFrame, QWidget, QLineEdit, QTextEdit, QSpinBox,
                               QDoubleSpinBox, QAbstractButton, QPlainTextEdit)

"""This is the main stylesheet"""
QSS = """
/* --- Base --- */
QWidget { color:#EAEAEA; background:#1f1f21; }
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
QPushButton[size="lg"] { padding:10px 16px; }

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
QHeaderView::section { background:#2a2b2e; padding:6px 8px}

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

/* Standout QCheckBox with transparent unchecked background + SVG checkmark */
QCheckBox {
  spacing: 8px;            /* gap between box and label */
}

/* Indicator (the box) */
QCheckBox::indicator {
  width: 22px;
  height: 22px;
  border: 2px solid #2563eb;    /* vibrant, clearly visible even when unchecked */
  border-radius: 6px;
  background: transparent;      /* no fill as requested */
  margin-top: 1px;              /* aligns with text baseline a bit better */
}

/* Explicitly no image when unchecked */
QCheckBox::indicator:unchecked {
  image: none;
}

/* Hover / pressed cues without adding fill */
QCheckBox::indicator:hover {
  border-color: #1d4ed8;        /* slightly darker blue */
}
QCheckBox::indicator:pressed {
  border-color: #1e40af;
}

/* (Some styles honor :focus on indicator; harmless if ignored) */
QCheckBox::indicator:focus {
  border-color: #1d4ed8;
}

/* Checked — keep border visible and draw your SVG */
QCheckBox::indicator:checked {
  background: transparent;      /* still no fill */
  border-color: #16a34a;        /* green border to differentiate state */
  image: url(:/images/graphics/done.svg);
}

/* Indeterminate (optional) — still transparent, distinct border */
QCheckBox::indicator:indeterminate {
  background: transparent;
  border-color: #f59e0b;        /* amber border */
  image: none;
}

/* Disabled */
QCheckBox:disabled { color: #9ca3af; }
QCheckBox::indicator:disabled {
  border-color: #cbd5e1;
  background: transparent;
  image: none;
}

/* --- Tree item checkbox indicator --- */
QTreeView::indicator, QTreeWidget::indicator {
  width: 20px;
  height: 20px;
  border: 2px solid #2563eb;   /* vibrant so it's clearly visible */
  border-radius: 5px;
  background: transparent;      /* no fill for unchecked */
}

/* No icon when unchecked */
QTreeView::indicator:unchecked, QTreeWidget::indicator:unchecked {
  image: none;
}

/* Hover / focus cues */
QTreeView::indicator:hover, QTreeWidget::indicator:hover {
  border-color: #1d4ed8;
}
QTreeView::indicator:focus, QTreeWidget::indicator:focus {
  border-color: #1d4ed8;
}

/* Checked — draw your SVG, keep border visible */
QTreeView::indicator:checked, QTreeWidget::indicator:checked {
  image: url(:/images/graphics/done.svg);
  background: transparent;
  border-color: #16a34a;        /* green border to differentiate state */
}

/* Indeterminate (optional) */
QTreeView::indicator:indeterminate, QTreeWidget::indicator:indeterminate {
  image: none;                   /* or point to an indeterminate icon */
  background: transparent;
  border-color: #f59e0b;         /* amber */
}

/* Disabled */
QTreeView::indicator:disabled, QTreeWidget::indicator:disabled {
  border-color: #cbd5e1;
  image: none;
}

"""

LIGHT_QSS = """
/* --- Base --- */
QWidget { color:#111827; background:#F8FAFC;}
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
  background:#FFFFFF; color:#111827; border:1px solid #E5E7EB; border-radius:8px; padding:6px 8px;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus { border:2px solid #2563EB; }

/* --- Buttons --- */
QPushButton {
  border:1px solid #D1D5DB; background:#FFFFFF; color:#111827; border-radius:8px; padding:6px 12px;
}
QPushButton:hover { background:#F3F4F6; }
QPushButton[intent="primary"] { background:#2563EB; border-color:#2563EB; color:white; }
QPushButton[intent="success"] { background:#16A34A; border-color:#16A34A; color:#062b12; }
QPushButton[intent="danger"]  { background:#DC2626; border-color:#DC2626; color:white; }
QPushButton[appearance="flat"] { background:transparent; border-color:transparent; color:#374151; }
QPushButton[size="lg"] { padding:10px 16px }

/* --- Segmented top nav --- */
QAbstractButton[seg="1"] {
  background:#FFFFFF; border:1px solid #E5E7EB; color:#1F2937; padding:6px 12px; border-radius:10px;
}
QAbstractButton[seg="1"]:checked { background:#2563EB; border-color:#2563EB; color:white; }

/* --- Tree / headers --- */
QTreeWidget { background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; alternate-background-color:#F3F4F6; }
QTreeWidget::item:selected { background:#2563EB; color:white; }
QHeaderView::section { background:#F3F4F6; color:#374151; border:none; border-right:1px solid #E5E7EB; padding:6px 8px;}
QTreeView::item { height: 28px; }

/* --- Scrollbars --- */
QScrollBar:vertical { width:10px; background:transparent; margin:4px; }
QScrollBar::handle:vertical { min-height:24px; background:#CBD5E1; border-radius:5px; }
QScrollBar:horizontal { height:10px; background:transparent; margin:4px; }
QScrollBar::handle:horizontal { min-width:24px; background:#CBD5E1; border-radius:5px; }

/* --- Progress --- */
QProgressBar { background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; color:#1F2937; text-align:center; padding:3px; }
QProgressBar::chunk { background:#2563EB; border-radius:7px; }
QProgressBar[role="convert"]::chunk { background:#16A34A; }
QProgressBar[role="total"]::chunk { background:#2563EB; }

/* --- TextBrowser --- */
QTextBrowser { background:#F5F7FB; color:#111827; border:1px solid #D1D5DB; border-radius:12px; padding:12px; }
QTextBrowser:focus { border:1px solid #60A5FA; }

/* Popup (QComboBox list) */
QComboBox QAbstractItemView {
  background:#FFFFFF; border:1px solid #E5E7EB; border-radius:8px; padding:6px; outline:0;
  selection-background-color: transparent;
}
QComboBox QAbstractItemView::item {
  padding:6px 8px; border:1px solid #E5E7EB; border-radius:8px; margin:2px 0;
}
QComboBox QAbstractItemView::item:hover {
  border-color:#60A5FA; background:rgba(37,99,235,0.06);
}
QComboBox QAbstractItemView::item:selected {
  border:2px solid #2563EB; background:rgba(37,99,235,0.12); color:#0B1220;
}

/* Cards and highlight helpers */
*[variant="card"] { background:#FFFFFF; border:1px solid #E5E7EB; border-radius:12px; }
*[highlight="accent"]  { border:2px solid #2563EB; border-radius:12px; }
*[highlight="success"] { border:2px solid #16A34A; border-radius:12px; }
*[highlight="warning"] { border:2px solid #D97706; border-radius:12px; }

/* Rings */
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit,
QSpinBox, QDoubleSpinBox, QAbstractButton {
  border: 2px solid #D1D5DB;
  border-radius: 8px;
}
QLineEdit:hover, QComboBox:hover, QTextEdit:hover, QPlainTextEdit:hover,
QSpinBox:hover, QDoubleSpinBox:hover, QAbstractButton:hover {
  border-color: #93C5FD;
}
*[kbd="1"],
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QAbstractButton:focus {
  border-color: #2563EB;
}
*:disabled { border-color:#E5E7EB; color:#9CA3AF; }
"""

def apply_theme(app: QApplication):
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor("#1f1f21"))
    pal.setColor(QPalette.ColorRole.Base, QColor("#262628"))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor("#232427"))
    pal.setColor(QPalette.ColorRole.Text, QColor("#EAEAEA"))
    pal.setColor(QPalette.ColorRole.Button, QColor("#2a2b2e"))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor("#EAEAEA"))
    pal.setColor(QPalette.ColorRole.Highlight, QColor("#3b82f6"))
    pal.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    pal.setColor(QPalette.ColorRole.PlaceholderText, QColor("#8b8f97"))
    app.setPalette(pal)
    app.setStyleSheet(QSS)

def apply_theme_light(app: QApplication):
    app.setStyle("Fusion")
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor("#F8FAFC"))
    pal.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor("#F3F4F6"))
    pal.setColor(QPalette.ColorRole.Text, QColor("#111827"))
    pal.setColor(QPalette.ColorRole.Button, QColor("#FFFFFF"))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor("#111827"))
    pal.setColor(QPalette.ColorRole.Highlight, QColor("#2563EB"))
    pal.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    pal.setColor(QPalette.ColorRole.PlaceholderText, QColor("#9CA3AF"))
    app.setPalette(pal)
    app.setStyleSheet(LIGHT_QSS)

def _hsl(h, s, l):
    return QColor.fromHsl(h % 360, int(max(0, min(1, s)) * 255), int(max(0, min(1, l)) * 255))

def _hex(q: QColor) -> str:
    return q.name(QColor.NameFormat.HexRgb)

def _lg(c1, c2, x2=1, y2=1):
    return f"qlineargradient(x1:0, y1:0, x2:{x2}, y2:{y2}, stop:0 {c1}, stop:1 {c2})"

def build_lsd_qss(seed=None) -> tuple[str, dict]:
    rnd = random.Random(seed)
    h = rnd.randrange(0, 360)
    # Neon triad
    cA = _hsl(h,     1.0, 0.55)
    cB = _hsl(h+120, 1.0, 0.55)
    cC = _hsl(h+240, 1.0, 0.55)
    # Pastel surface so text stays readable
    base_bg   = _hsl(h+30,  0.20, 0.97)
    panel_bg  = _hsl(h+200, 0.18, 0.95)
    alt_bg    = _hsl(h+160, 0.22, 0.92)
    ink       = QColor("#0b0c0f")

    # Role mapping (still playful but consistent)
    primary  = cA
    success  = _hsl(h+90, 0.95, 0.52)
    danger   = _hsl(h-90, 0.95, 0.54)
    warning  = _hsl(h+45, 0.95, 0.55)

    g_win   = _lg(_hex(base_bg), _hex(panel_bg))
    g_btn   = _lg(_hex(cA), _hex(cB))
    g_btn_h = _lg(_hex(cB), _hex(cC))
    g_seg   = _lg(_hex(cC), _hex(cA))
    g_prog  = _lg(_hex(cA), _hex(cC), x2=1, y2=0)
    g_sel   = _lg(_hex(cB), _hex(cA))
    g_scroll= _lg(_hex(cC), _hex(cB))

    qss = f"""
/* --- Base (pastel canvas with neon accents) --- */
QWidget {{
  color:{_hex(ink)}; background:{g_win}; 
}}
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {{
  background:#ffffff; color:{_hex(ink)}; border:2px solid {_hex(cB)}; border-radius:10px; padding:6px 10px;
}}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus {{ border:3px solid {_hex(primary)}; }}

/* --- Buttons (neon gradient pills) --- */
QPushButton {{
  border:0; background:{g_btn}; color:white; border-radius:999px; padding:8px 14px;
}}
QPushButton:hover {{ background:{g_btn_h}}}
QPushButton[intent="primary"] {{ background:{g_btn}; color:white; }}
QPushButton[intent="success"] {{ background:{_lg(_hex(success), _hex(cA))}; color:#06170b; }}
QPushButton[intent="danger"]  {{ background:{_lg(_hex(danger), _hex(cC))}; color:white; }}
QPushButton[appearance="flat"] {{ background:transparent; border:2px dashed {_hex(cC)}; color:{_hex(cC)}; }}
QPushButton[size="lg"] {{ padding:12px 18px; }}

/* --- Segmented nav (candy bar) --- */
QAbstractButton[seg="1"] {{
  background:{g_seg}; border:2px solid transparent; color:white; padding:6px 12px; border-radius:12px;
}}
QAbstractButton[seg="1"]:checked {{ border-color:#ffffff; color:#0b0c0f; background:#ffffff; }}

/* --- Tree / headers --- */
QTreeWidget {{
  background:{_hex(alt_bg)}; border:2px solid {_hex(cB)}; border-radius:14px; alternate-background-color:{_hex(panel_bg)};
}}
QTreeWidget::item:selected {{ background:{g_sel}; color:white; }}
QHeaderView::section {{
  background:{_hex(panel_bg)}; color:{_hex(ink)}; border:none; border-right:2px dashed {_hex(cC)}; padding:6px 8px
}}

/* --- Scrollbars (neon sticks) --- */
QScrollBar:vertical {{ width:12px; background:transparent; margin:4px; }}
QScrollBar::handle:vertical {{ min-height:24px; background:{g_scroll}; border-radius:6px; }}
QScrollBar:horizontal {{ height:12px; background:transparent; margin:4px; }}
QScrollBar::handle:horizontal {{ min-width:24px; background:{g_scroll}; border-radius:6px; }}

/* --- Progress (liquid rainbow) --- */
QProgressBar {{
  background:#ffffff; border:2px solid {_hex(cB)}; border-radius:10px; color:{_hex(ink)}; text-align:center; padding:3px;
}}
QProgressBar::chunk {{ background:{g_prog}; border-radius:8px; }}
QProgressBar[role="convert"]::chunk {{ background:{_lg(_hex(success), _hex(cB))}; }}
QProgressBar[role="total"]::chunk {{ background:{_lg(_hex(primary), _hex(cC))}; }}

/* --- Reader --- */
QTextBrowser {{
  background:{_hex(panel_bg)}; color:{_hex(ink)}; border:2px solid {_hex(cA)}; border-radius:14px; padding:12px;
}}
QTextBrowser:focus {{ border-color:{_hex(cC)}; }}

/* --- Popup list --- */
QComboBox QAbstractItemView {{
  background:#ffffff; border:2px solid {_hex(cB)}; border-radius:10px; padding:6px; outline:0;
  selection-background-color: transparent;
}}
QComboBox QAbstractItemView::item {{
  padding:6px 8px; border:2px solid transparent; border-radius:8px; margin:3px 0;
}}
QComboBox QAbstractItemView::item:hover {{
  border-color:{_hex(cA)}; background:rgba(0,0,0,0.03);
}}
QComboBox QAbstractItemView::item:selected {{
  border:2px solid {_hex(cC)}; background:{g_sel}; color:white;
}}

/* --- Cards & highlights --- */
*[variant="card"] {{
  background:{_hex(panel_bg)}; border:2px solid {_hex(cB)}; border-radius:14px;
}}
*[highlight="accent"]  {{ border:3px solid {_hex(primary)}; border-radius:14px; }}
*[highlight="success"] {{ border:3px solid {_hex(success)};  border-radius:14px; }}
*[highlight="warning"] {{ border:3px solid {_hex(warning)};  border-radius:14px; }}

/* Input rings on hover/focus for everything clickable */
QLineEdit:hover, QComboBox:hover, QTextEdit:hover, QPlainTextEdit:hover,
QSpinBox:hover, QDoubleSpinBox:hover, QAbstractButton:hover {{
  border-color: {_hex(cA)};
}}
*[kbd="1"],
QLineEdit:focus, QComboBox:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus, QAbstractButton:focus {{
  border-color: {_hex(cC)};
}}

/* ToolTip for extra spice */
QToolTip {{
  background:{_lg(_hex(cA), _hex(cC))}; color:white; border:0; padding:6px 8px; border-radius:8px;
}}
"""
    roles = dict(
        window=_hex(base_bg), base="#ffffff", alt=_hex(alt_bg),
        text=_hex(ink), primary=_hex(primary), success=_hex(success),
        danger=_hex(danger), highlight=_hex(primary)
    )
    return qss, roles

def apply_theme_lsd(app: QApplication, seed=None):
    app.setStyle("Fusion")
    qss, r = build_lsd_qss(seed=seed)
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(r["window"]))
    pal.setColor(QPalette.ColorRole.Base,   QColor(r["base"]))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor(r["alt"]))
    pal.setColor(QPalette.ColorRole.Text, QColor(r["text"]))
    pal.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor(r["text"]))
    pal.setColor(QPalette.ColorRole.Highlight, QColor(r["highlight"]))
    pal.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    pal.setColor(QPalette.ColorRole.PlaceholderText, QColor("#6b7280"))
    app.setPalette(pal)
    app.setStyleSheet(qss)

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
    view.setFrameShape(QFrame.Shape.NoFrame)  # we draw the border in QSS
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
                reason = Qt.FocusReason.OtherFocusReason
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


def generate_random_progressbar_qss(seed=None):
    """
    Generate a random, dimension-consistent QSS stylesheet for a QProgressBar.

    Usage:
        bar.setStyleSheet(generate_random_progressbar_qss())
        # (Optionally) reproducible:
        bar.setStyleSheet(generate_random_progressbar_qss(seed=42))

    Notes:
      - Dimensions (height, padding, border thickness, radius) are fixed for consistency.
      - Colors and visual effects (flat, gradient, glossy, striped, glass) vary randomly.
      - Works for horizontal and vertical QProgressBar (Qt applies the same rules).
      - For "busy/indeterminate" mode, setRange(0, 0) as usual; the style remains compatible.
    """
    if seed is not None:
        rnd = random.Random(seed)
    else:
        rnd = random

    # ===== Consistent metrics across all variants =====
    HEIGHT_PX        = 20
    BORDER_RADIUS_PX = 10
    BORDER_PX        = 1
    PADDING_PX       = 2
    TEXT_WEIGHT      = 600  # semi-bold for readability

    # ===== Color helpers =====
    def clamp01(x): return max(0.0, min(1.0, x))
    def hsl(h, s, l):
        r, g, b = colorsys.hls_to_rgb(h, l, s)  # note: colorsys uses HLS, not HSL
        return int(r*255), int(g*255), int(b*255)

    def to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def lighten(rgb, amount=0.15):
        # Convert to HLS, tweak L, convert back
        r, g, b = [c/255 for c in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = clamp01(l + amount)
        rr, gg, bb = colorsys.hls_to_rgb(h, l, s)
        return int(rr*255), int(gg*255), int(bb*255)

    def darken(rgb, amount=0.15):
        r, g, b = [c/255 for c in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = clamp01(l - amount)
        rr, gg, bb = colorsys.hls_to_rgb(h, l, s)
        return int(rr*255), int(gg*255), int(bb*255)

    def readable_text_on(bg_rgb):
        # Simple luma-based contrast: choose dark or light text
        r, g, b = bg_rgb
        luma = 0.2126*(r/255) + 0.7152*(g/255) + 0.0722*(b/255)
        return (30, 30, 30) if luma > 0.6 else (245, 245, 245)

    # ===== Random base palette =====
    base_h = rnd.random()            # 0..1
    base_s = rnd.uniform(0.55, 0.85) # colorful but not neon
    base_l = rnd.uniform(0.40, 0.60) # mid lightness for good gradients

    base_rgb   = hsl(base_h, base_s, base_l)
    base_hex   = to_hex(base_rgb)
    light_hex  = to_hex(lighten(base_rgb, 0.18))
    dark_hex   = to_hex(darken(base_rgb, 0.22))
    dim_bg_rgb = darken(base_rgb, 0.35)              # track background
    dim_bg_hex = to_hex(dim_bg_rgb)
    border_hex = to_hex(darken(base_rgb, 0.45))
    text_hex   = to_hex(readable_text_on(dim_bg_rgb))
    chunk_text_hex = to_hex(readable_text_on(base_rgb))

    # A few subtle neutral tweaks for disabled state
    disabled_track_hex = "#cfcfcf"
    disabled_chunk_hex = "#9f9f9f"
    disabled_text_hex  = "#5f5f5f"

    # ===== Visual variants =====
    variant = rnd.choice([
        "flat", "soft-gradient", "glossy", "striped", "glass"
    ])

    # Shared header: consistent dimensions & text
    header = f"""
    QProgressBar {{
        min-height: {HEIGHT_PX}px;
        max-height: {HEIGHT_PX}px;
        padding: {PADDING_PX}px;
        border: {BORDER_PX}px solid {border_hex};
        border-radius: {BORDER_RADIUS_PX}px;
        background-color: {dim_bg_hex};
        color: {text_hex};
        text-align: center;
    }}
    QProgressBar:disabled {{
        background-color: {disabled_track_hex};
        color: {disabled_text_hex};
        border-color: #b5b5b5;
    }}
    """

    # Chunk templates per variant
    if variant == "flat":
        chunk = f"""
        QProgressBar::chunk {{
            background-color: {base_hex};
            border-radius: {BORDER_RADIUS_PX - max(0, BORDER_PX)}px;
        }}
        QProgressBar::chunk:disabled {{
            background-color: {disabled_chunk_hex};
        }}
        """

    elif variant == "soft-gradient":
        # Horizontal gradient along progress direction
        chunk = f"""
        QProgressBar::chunk {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {light_hex}, stop:1 {dark_hex});
            border-radius: {BORDER_RADIUS_PX - max(0, BORDER_PX)}px;
        }}
        QProgressBar::chunk:disabled {{
            background-color: {disabled_chunk_hex};
        }}
        """

    elif variant == "glossy":
        # Vertical gloss overlay inside the chunk
        top_gloss   = to_hex(lighten(base_rgb, 0.28))
        mid_gloss   = to_hex(lighten(base_rgb, 0.10))
        bottom_deep = to_hex(darken(base_rgb, 0.25))
        chunk = f"""
        QProgressBar::chunk {{
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 {top_gloss}, stop:0.49 {mid_gloss},
                stop:0.5 {base_hex}, stop:1 {bottom_deep});
            border-radius: {BORDER_RADIUS_PX - max(0, BORDER_PX)}px;
        }}
        QProgressBar::chunk:disabled {{
            background-color: {disabled_chunk_hex};
        }}
        """

    elif variant == "striped":
        # Diagonal "barber pole" stripes built with multi-stop gradient
        c1 = light_hex
        c2 = to_hex(darken(base_rgb, 0.10))
        # Slightly stronger border to emphasize stripes
        header = header.replace(f"border: {BORDER_PX}px", f"border: {BORDER_PX}px")
        # Diagonal stripes via 45° linear gradient approximation
        chunk = f"""
        QProgressBar::chunk {{
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0   {c1},
                stop:0.125 {c1},
                stop:0.126 {c2},
                stop:0.25  {c2},
                stop:0.251 {c1},
                stop:0.375 {c1},
                stop:0.376 {c2},
                stop:0.5   {c2},
                stop:0.501 {c1},
                stop:0.625 {c1},
                stop:0.626 {c2},
                stop:0.75  {c2},
                stop:0.751 {c1},
                stop:0.875 {c1},
                stop:0.876 {c2},
                stop:1     {c2});
            border-radius: {BORDER_RADIUS_PX - max(0, BORDER_PX)}px;
        }}
        QProgressBar::chunk:disabled {{
            background-color: {disabled_chunk_hex};
        }}
        """

    else:  # "glass"
        # Semi-transparent glassy chunk over a tinted track
        glass_bg = f"rgba(255,255,255,40%)"
        tint_hex = to_hex(lighten(base_rgb, 0.35))
        header = header.replace(f"background-color: {dim_bg_hex};",
                                f"background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {tint_hex}, stop:1 {dim_bg_hex});")
        chunk = f"""
        QProgressBar::chunk {{
            background: {glass_bg};
            border: 1px solid {light_hex};
            border-radius: {BORDER_RADIUS_PX - max(0, BORDER_PX)}px;
        }}
        QProgressBar::chunk:disabled {{
            background-color: {disabled_chunk_hex};
            border-color: #c8c8c8;
        }}
        """

    # Optional: stronger contrast for the text over the filled area
    # (Qt draws the same text once; this helps when chunk is bright)
    overlay_text = f"""
    QProgressBar[format^="%"] {{
        /* No-op selector to keep compatibility; users can change format externally */
    }}
    """

    return header + chunk + overlay_text
