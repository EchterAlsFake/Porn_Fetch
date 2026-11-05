"""Generate platform icons from the original artwork using the GUI's Qt dependency.

Run with the GUI environment, then rebuild Qt resources. No display is required.
"""

from __future__ import annotations

import json
import math
import struct
from pathlib import Path

from PySide6.QtCore import QBuffer, QIODevice, Qt
from PySide6.QtGui import QImage, QPainter

GRAPHICS = Path(__file__).resolve().parents[1] / "src/frontend/graphics"
WINDOWS_SIZES = (16, 20, 24, 32, 40, 48, 64, 96, 128, 256)
MAC_SIZES = {
    b"icp4": 16, b"icp5": 32, b"icp6": 64, b"ic07": 128,
    b"ic08": 256, b"ic09": 512, b"ic10": 1024,
    b"ic11": 32, b"ic12": 64, b"ic13": 256, b"ic14": 512,
}


def alpha_bounds(image: QImage) -> tuple[int, int, int, int]:
    """Return the nontransparent bounds without depending on an imaging package."""
    rgba = image.convertToFormat(QImage.Format.Format_RGBA8888)
    alpha = bytes(rgba.constBits())[3::4]
    width = rgba.width()
    left, top, right, bottom = width, rgba.height(), -1, -1
    for y in range(rgba.height()):
        row = alpha[y * width:(y + 1) * width]
        if row.strip(b"\0"):
            left = min(left, width - len(row.lstrip(b"\0")))
            right = max(right, len(row.rstrip(b"\0")) - 1)
            top, bottom = min(top, y), y
    if right < left:
        raise ValueError("Icon artwork is empty")
    return left, top, right - left + 1, bottom - top + 1


def render(artwork: QImage, size: int, extent: float = 0.92, background=Qt.GlobalColor.transparent) -> QImage:
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(background)
    side = round(size * extent)
    scaled = artwork.scaled(side, side, Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation)
    painter = QPainter(image)
    painter.drawImage((size - scaled.width()) // 2, (size - scaled.height()) // 2, scaled)
    painter.end()
    return image


def png(image: QImage) -> bytes:
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    if not image.save(buffer, "PNG"):
        raise RuntimeError("Qt could not encode the icon")
    return bytes(buffer.data())


def generate(graphics: Path = GRAPHICS) -> None:
    source = QImage(str(graphics / "logo_artwork.png"))
    if source.isNull():
        raise ValueError("Cannot read logo_artwork.png")
    artwork = source.copy(*alpha_bounds(source))
    for name, size in (("logo.png", 1024), ("logo_transparent.png", 1024), ("logo_square.png", 512)):
        (graphics / name).write_bytes(png(render(artwork, size)))

    # ICO directory dimensions are limited to 256; zero represents 256, not 512.
    frames = [png(render(artwork, size)) for size in WINDOWS_SIZES]
    offset = 6 + 16 * len(frames)
    entries = []
    for size, frame in zip(WINDOWS_SIZES, frames):
        entries.append(struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(frame), offset))
        offset += len(frame)
    (graphics / "logo_transparent.ico").write_bytes(
        struct.pack("<HHH", 0, 1, len(frames)) + b"".join(entries) + b"".join(frames))

    chunks = []
    for kind, size in MAC_SIZES.items():
        frame = png(render(artwork, size))
        chunks.append(kind + struct.pack(">I", len(frame) + 8) + frame)
    payload = b"".join(chunks)
    (graphics / "logo_transparent.icns").write_bytes(b"icns" + struct.pack(">I", len(payload) + 8) + payload)

    # Android's 108dp layers have a central 66dp safe circle. Fit the actual
    # artwork inside that circle; desktop padding must not be used here.
    rgba = artwork.convertToFormat(QImage.Format.Format_RGBA8888)
    alpha = bytes(rgba.constBits())[3::4]
    radius = max(math.hypot(x + 0.5 - artwork.width() / 2, y + 0.5 - artwork.height() / 2)
                 for y in range(artwork.height()) for x in range(artwork.width())
                 if alpha[y * artwork.width() + x])
    extent = (64 / 108) * max(artwork.width(), artwork.height()) / (2 * radius)
    (graphics / "icon_foreground.png").write_bytes(png(render(artwork, 512, extent)))

    # iOS masks its own corners and requires opaque artwork.
    catalog = graphics / "ios/Assets.xcassets"
    icons = catalog / "AppIcon.appiconset"
    icons.mkdir(parents=True, exist_ok=True)
    info = {"author": "xcode", "version": 1}
    (catalog / "Contents.json").write_text(json.dumps({"info": info}, indent=2) + "\n")
    (icons / "Contents.json").write_text(json.dumps({"images": [{
        "filename": "AppIcon.png", "idiom": "universal", "platform": "ios", "size": "1024x1024",
    }], "info": info}, indent=2) + "\n")
    (icons / "AppIcon.png").write_bytes(png(render(artwork, 1024, background=Qt.GlobalColor.black).convertToFormat(
        QImage.Format.Format_RGB32)))


if __name__ == "__main__":
    generate()
    print("Generated desktop, Android and iOS app icons.")
