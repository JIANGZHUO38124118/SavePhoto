# boundary/ImagePreviewDialog.py
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImagePreviewDialog(QDialog):
    def __init__(self, photos, current_index, parent=None):
        super().__init__(parent)
        self.photos = photos
        self.current_index = current_index

        self.resize(800, 600)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.updateImage()

    def updateImage(self):
        if not (0 <= self.current_index < len(self.photos)):
            return
        
        photo = self.photos[self.current_index]
        self.setWindowTitle(photo.filename)

        pixmap = QPixmap(photo.filepath)
        if pixmap.isNull():
            self.label.setText("Image not found")
        else:
            scaled_pixmap = pixmap.scaled(
                750, 
                550, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Left:
            self.current_index = (self.current_index - 1) % len(self.photos)
            self.updateImage()
        elif event.key() == Qt.Key_Right:
            self.current_index = (self.current_index + 1) % len(self.photos)
            self.updateImage()
        else:
            super().keyPressEvent(event)