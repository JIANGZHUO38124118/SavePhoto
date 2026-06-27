# boundary/ImagePreviewDialog.py
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QKeyEvent
from PyQt5.QtCore import Qt
from control.ShowService import ShowService

class ImagePreviewDialog(QDialog):

    def __init__(self, photos, index, user, mode="community", parent=None):
        super().__init__(parent)
        self.photos = photos
        self.index = index
        self.user = user
        self.mode = mode 
        self.service = ShowService()

        self.setWindowTitle("Image Detailed View")
        self.resize(950, 650)
        self.setFocusPolicy(Qt.StrongFocus)

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.publisherLabel = QLabel("Publisher: -")
        self.likesLabel = QLabel("Likes:  0")
        
        self.likeBtn = QPushButton("Like")
        self.likeBtn.setFixedWidth(80)
        
        self.titleLabel = QLabel("<b>[ Photo Name ]</b>") 
        self.titleLabel.setWordWrap(True)
        self.titleLabel.setStyleSheet("font-size: 14px; color: #333333;")
        
        self.paramTitle = QLabel("<b>[ Technical Parameters ]</b>")
        self.paramText = QTextEdit()
        self.paramText.setReadOnly(True) 
        self.paramText.setFixedWidth(240) 
        self.paramText.setFocusPolicy(Qt.NoFocus)

        self.editParamBtn = QPushButton("Edit Parameters")
        self.statusBtn = QPushButton("Make Public")
        self.statusBtn.setStyleSheet("font-weight: bold;")

        mainLayout = QHBoxLayout()
        
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.imageLabel, 1) 
        
        socialLayout = QHBoxLayout()
        socialLayout.addWidget(self.publisherLabel)
        socialLayout.addSpacing(30)
        socialLayout.addWidget(self.likesLabel)
        socialLayout.addSpacing(15)
        socialLayout.addWidget(self.likeBtn) 
        socialLayout.addStretch() 
        leftLayout.addLayout(socialLayout)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.titleLabel) 
        rightLayout.addSpacing(15)
        rightLayout.addWidget(self.paramTitle)
        rightLayout.addWidget(self.paramText, 1) 
        rightLayout.addWidget(self.editParamBtn) 
        rightLayout.addWidget(self.statusBtn)
        
        mainLayout.addLayout(leftLayout, 1) 
        mainLayout.addLayout(rightLayout)
        self.setLayout(mainLayout)

        self.updateContent()

        self.likeBtn.clicked.connect(self.doLike)
        self.editParamBtn.clicked.connect(self.doEditParam)
        self.statusBtn.clicked.connect(self.doToggleStatus)

    def updateContent(self):
        photo = self.photos[self.index]

        if self.mode == "community":
            self.likeBtn.show()
            self.editParamBtn.hide()
            self.statusBtn.hide()
            
            import sqlite3
            conn = sqlite3.connect("database/photo.db")
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM likes WHERE userid = ? AND photoid = ?", (self.user.userid, photo.photoid))
            is_user_liked = cursor.fetchone() is not None
            cursor.close()
            conn.close()

            if is_user_liked:
                self.likeBtn.setText("Liked")
            else:
                self.likeBtn.setText("Like")
        else:
            self.likeBtn.hide()
            self.editParamBtn.show()
            self.statusBtn.show()

            if photo.isPublic():
                self.statusBtn.setText("Set to Private")
            else:
                self.statusBtn.setText("Set to Public")

        self.titleLabel.setText(f"<b>File Name:</b><br>{photo.filename}")
        
        pixmap = QPixmap(photo.filepath)
        if not pixmap.isNull():
            self.imageLabel.setPixmap(pixmap.scaled(920, 820, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.imageLabel.setText("Failed to load image.")

        if hasattr(photo, 'owner_account') and photo.owner_account:
            self.publisherLabel.setText(f"<b>Publisher:</b> {photo.owner_account}")
        else:
            self.publisherLabel.setText("<b>Publisher:</b> My Storage")

        likes = getattr(photo, 'likes_count', 0)
        self.likesLabel.setText(f"<b>Likes:</b> {likes}")

        self.refreshParamText(photo)
        self.setFocus()

    def refreshParamText(self, photo):
        param_info = ""
        if photo.parameter:
            for p in photo.parameter:
                param_info += f"• {p.key}:\n  {p.value}\n\n"
        else:
            param_info = "No technical parameters found for this photo."
        self.paramText.setPlainText(param_info)

    def doToggleStatus(self):
        photo = self.photos[self.index]
        from entity.PhotoVisibility import PhotoVisibility
        
        if photo.isPublic():
            success = self.service.unpublishPhoto(photo.photoid)
            if success:
                photo.visibility = PhotoVisibility.PRIVATE
                QMessageBox.information(self, "Success", "Photo is now Private.")
        else:
            success = self.service.publishPhoto(photo.photoid)
            if success:
                photo.visibility = PhotoVisibility.PUBLIC
                QMessageBox.information(self, "Success", "Photo is now Public.")
        
        self.updateContent()

    def doLike(self):
        photo = self.photos[self.index]
        is_liked, message = self.service.toggleLikePhoto(self.user.userid, photo.photoid)
        if hasattr(photo, 'likes_count'):
            photo.likes_count = photo.likes_count + 1 if is_liked else photo.likes_count - 1
        QMessageBox.information(self, "Notice", message)
        self.updateContent()

    def doEditParam(self):
        photo = self.photos[self.index]
        if not photo.parameter:
            QMessageBox.information(self, "Notice", "This photo has no parameters to edit.")
            return

        keys = [p.key for p in photo.parameter]
        key, ok1 = QInputDialog.getItem(self, "Select Parameter", "Which parameter do you want to change?", keys, 0, False)
        
        if ok1 and key:
            old_value = next((p.value for p in photo.parameter if p.key == key), "")
            new_value, ok2 = QInputDialog.getText(self, f"Edit {key}", f"Enter new value for {key}:", text=old_value)
            
            if ok2 and new_value.strip():
                success = self.service.updatePhotoParameter(photo.photoid, key, new_value.strip())
                if success:
                    QMessageBox.information(self, "Success", f"{key} updated successfully!")
                    for p in photo.parameter:
                        if p.key == key:
                            p.value = new_value.strip()
                            break
                    self.refreshParamText(photo)
                else:
                    QMessageBox.critical(self, "Error", "Failed to update parameter.")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Left and self.index > 0:
            self.index -= 1
            self.updateContent()
        elif event.key() == Qt.Key_Right and self.index < len(self.photos) - 1:
            self.index += 1
            self.updateContent()
        elif event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)