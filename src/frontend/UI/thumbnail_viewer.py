import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPainter, QFont
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame, QApplication


class ImageViewer(QGraphicsView):
    def __init__(self, image_data=None):
        super().__init__()

        # 1. Setup Scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 2. Setup Item
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # 3. Configure View
        # Start with a default size, but it will change instantly when image loads
        self.resize(800, 600)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWindowTitle("Image Viewer")
        self.setStyleSheet("background-color: #121212;")

        # 4. Load Initial Image
        if image_data:
            self.set_image(image_data)

    def set_image(self, image_data):
        """
        Updates the view and dynamically resizes the window.
        """
        pixmap = QPixmap()
        loaded = False

        # --- 1. Load Data ---
        if isinstance(image_data, str) and os.path.exists(image_data):
            loaded = pixmap.load(image_data)
        elif isinstance(image_data, bytes):
            loaded = pixmap.loadFromData(image_data)

        # --- 2. Handle Fallback ---
        if not loaded:
            # Default fallback size
            pixmap = QPixmap(600, 400)
            pixmap.fill(QColor("#1A1A1A"))
            painter = QPainter(pixmap)
            painter.setPen(QColor("#00DAC6"))
            painter.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "NO DATA")
            painter.end()

        # --- 3. Update Scene ---
        self.pixmap_item.setPixmap(pixmap)
        self.setSceneRect(self.pixmap_item.boundingRect())

        # --- 4. Dynamic Resizing Logic ---
        # Get image dimensions
        img_w = pixmap.width()
        img_h = pixmap.height()

        # Define your maximum limits
        MAX_W = 1280
        MAX_H = 720

        # We add a tiny padding (e.g., 2px) to prevent scrollbars
        # from appearing if the image fits exactly.
        padding = 2

        # Calculate target size: Smallest between (Image Size) and (Max Limit)
        target_w = min(img_w + padding, MAX_W)
        target_h = min(img_h + padding, MAX_H)

        # Apply the new size to the window
        self.resize(target_w, target_h)

        # Optional: Center the window on screen (if you want it to pop up in the middle)
        # self._center_on_screen()

    def _center_on_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)