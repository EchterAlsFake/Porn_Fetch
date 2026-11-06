"""Live highlighting for the filename template editor."""

from string import Template

from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat

from src.shared.download_options import PLACEHOLDERS


class TitleFormatHighlighter(QSyntaxHighlighter):
    def set_theme(self, dark: bool, high_contrast: bool) -> None:
        self.placeholder = QTextCharFormat()
        self.placeholder.setForeground(QColor(
            ("#ffff00" if dark else "#000080") if high_contrast else ("#7dd3fc" if dark else "#075985")))
        self.placeholder.setFontWeight(QFont.Weight.Bold)
        self.escaped = QTextCharFormat(self.placeholder)
        if not high_contrast:
            self.escaped.setForeground(QColor("#86efac" if dark else "#166534"))
        self.invalid = QTextCharFormat()
        self.invalid.setForeground(QColor(
            ("#ffffff" if dark else "#000000") if high_contrast else ("#fda4af" if dark else "#b91c1c")))
        self.invalid.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
        self.rehighlight()

    def highlightBlock(self, text: str) -> None:
        for match in Template.pattern.finditer(text):
            name = match.group("named") or match.group("braced")
            style = (self.escaped if match.group("escaped") else
                     self.placeholder if name in PLACEHOLDERS else self.invalid)
            # Qt indexes text in UTF-16 units, including any emoji before a token.
            start = len(text[:match.start()].encode("utf-16-le")) // 2
            length = len(match.group().encode("utf-16-le")) // 2
            self.setFormat(start, length, style)
