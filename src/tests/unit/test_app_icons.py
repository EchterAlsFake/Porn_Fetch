"""Check shipped icon artwork and native containers without platform build tools."""

import json
import math
import struct
import unittest

from PySide6.QtGui import QImage, QImageReader

from scripts.generate_app_icons import GRAPHICS, alpha_bounds


class AppIconTests(unittest.TestCase):
    def test_square_artwork_fills_canvas_and_native_frames_decode(self):
        for name in ("logo.png", "logo_square.png", "logo_transparent.png"):
            image = QImage(str(GRAPHICS / name))
            self.assertEqual(image.width(), image.height())
            x, y, width, height = alpha_bounds(image)
            self.assertGreaterEqual(max(width, height) / image.width(), 0.9)
            self.assertLessEqual(max(width, height) / image.width(), 0.94)
            self.assertLessEqual(abs(y - (image.height() - height) / 2), 1)
            self.assertLessEqual(abs(x - (image.width() - width) / 2), 1)

        for suffix, sizes in (
            ("ico", {16, 20, 24, 32, 40, 48, 64, 96, 128, 256}),
            ("icns", {16, 32, 64, 128, 256, 512, 1024}),
        ):
            reader = QImageReader(str(GRAPHICS / f"logo_transparent.{suffix}"))
            self.assertTrue(reader.canRead())
            decoded = set()
            for index in range(reader.imageCount()):
                self.assertTrue(reader.jumpToImage(index))
                image = reader.read()
                self.assertFalse(image.isNull(), reader.errorString())
                self.assertEqual(image.width(), image.height())
                decoded.add(image.width())
            self.assertEqual(decoded, sizes)

        # A directory claiming 256px with a 512px PNG is not a valid ICO frame.
        ico = (GRAPHICS / "logo_transparent.ico").read_bytes()
        count = struct.unpack_from("<H", ico, 4)[0]
        for index in range(count):
            width, height, _, _, _, _, length, offset = struct.unpack_from("<BBBBHHII", ico, 6 + 16 * index)
            frame = QImage.fromData(ico[offset:offset + length])
            self.assertEqual(frame.size().toTuple(), (width or 256, height or 256))

    def test_android_foreground_fits_launcher_safe_circle(self):
        image = QImage(str(GRAPHICS / "icon_foreground.png")).convertToFormat(QImage.Format.Format_RGBA8888)
        alpha = bytes(image.constBits())[3::4]
        radius = max(math.hypot(x + 0.5 - image.width() / 2, y + 0.5 - image.height() / 2)
                     for y in range(image.height()) for x in range(image.width()) if alpha[y * image.width() + x])
        self.assertLessEqual(radius, image.width() * 33 / 108)
        self.assertGreater(radius, image.width() * 30 / 108)

    def test_ios_catalog_references_an_opaque_high_resolution_icon(self):
        icons = GRAPHICS / "ios/Assets.xcassets/AppIcon.appiconset"
        catalog = json.loads((icons / "Contents.json").read_text())
        image = QImage(str(icons / catalog["images"][0]["filename"]))
        self.assertEqual(image.size().toTuple(), (1024, 1024))
        self.assertFalse(image.hasAlphaChannel())


if __name__ == "__main__":
    unittest.main()
