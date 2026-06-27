# boundary/ImagePreviewDialog.py
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class ImagePreviewDialog(QDialog):

    def __init__(self, photos, current_index, parent=None):
        super().__init__(parent)
        self.photos = photos
        self.current_index = current_index

        self.resize(1000, 650)

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.imageLabel, stretch=3) 

        self.sidePanel = QWidget()
        self.sidePanel.setFixedWidth(250)
        panelLayout = QVBoxLayout(self.sidePanel)
        panelLayout.setAlignment(Qt.AlignTop)
        panelLayout.setContentsMargins(10, 20, 10, 20)


        self.lblTitle = QLabel()
        font_title = QFont()
        font_title.setBold(True)
        font_title.setPointSize(14)
        self.lblTitle.setFont(font_title)
        self.lblTitle.setWordWrap(True)

        self.lblDate = QLabel()
        self.lblDate.setStyleSheet("color: #666666; font-size: 12px;")


        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #cccccc;")

        self.lblParams = QLabel()
        self.lblParams.setWordWrap(True)
        self.lblParams.setAlignment(Qt.AlignTop)

        panelLayout.addWidget(self.lblTitle)
        panelLayout.addWidget(self.lblDate)
        panelLayout.addSpacing(10)
        panelLayout.addWidget(line)
        panelLayout.addSpacing(10)
        panelLayout.addWidget(QLabel("<b>Technical Specs:</b>"))
        panelLayout.addWidget(self.lblParams)

        mainLayout.addWidget(self.sidePanel, stretch=1)

        self.updateImage()

    def updateImage(self):
        if not (0 <= self.current_index < len(self.photos)):
            return
        
        photo = self.photos[self.current_index]

        self.setWindowTitle(f"Preview - {photo.filename}")
        self.lblTitle.setText(photo.filename)

        upload_date = "Unknown Date"
        if photo.parameter:
            for p in photo.parameter:
                if p.key == "Upload Date":
                    upload_date = p.value
                    break

        self.lblDate.setText(f"Uploaded: {upload_date}")


        if not photo.parameter:
            self.lblParams.setText("<i style='color:gray;'>No extra parameters.</i>")
        else:
            param_text = ""
            for p in photo.parameter:
                if p.key == "Upload Date":
                    continue
                param_text += f"<p><b>{p.key}:</b> {p.value}</p>"
            
            if not param_text.strip():
                param_text = "<i style='color:gray;'>No extra parameters.</i>"
                
            self.lblParams.setText(param_text)

        pixmap = QPixmap(photo.filepath)
        if pixmap.isNull():
            self.imageLabel.setText("Image not found")
        else:
            scaled_pixmap = pixmap.scaled(
                700, 
                600, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.imageLabel.setPixmap(scaled_pixmap)

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