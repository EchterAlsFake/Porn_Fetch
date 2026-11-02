"""Print a static GUI inventory for manual localization/accessibility review.

Counts are navigation aids, never evidence of screen-reader conformance.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inventory():
    print("| Page/component | Controls | Accessible annotations | Raw text candidates |")
    print("| --- | ---: | ---: | ---: |")
    for path in sorted((ROOT / "src/frontend/UI").glob("*.qml")):
        text = path.read_text(encoding="utf-8")
        controls = len(re.findall(r"\b(?:Button|ToolButton|CheckBox|RadioButton|TextField|ComboBox|SpinBox|Slider|Switch|ItemDelegate)\s*\{", text))
        accessible = len(re.findall(r"Accessible\.", text))
        raw = len(re.findall(r'\b(?:text|title|placeholderText|label|heading|content):\s*"[A-Za-z]', text))
        print(f"| {path.name} | {controls} | {accessible} | {raw} |")


if __name__ == "__main__":
    inventory()
