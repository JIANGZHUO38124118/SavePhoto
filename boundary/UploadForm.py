from PyQt5.QtWidgets import *
import shutil
import os

from dao.PhotoDAO import PhotoDAO
from entity.Photo import Photo


class UploadForm(QWidget):

    def __init__(self, parent, user):
        super().__init__()

        self.parent = parent
        self.user = user
        self.dao = PhotoDAO()

        self.setWindowTitle("Upload")
        self.resize(400, 200)

        self.btn = QPushButton("Choose Image")
        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.btn.clicked.connect(self.upload)
        self.backBtn.clicked.connect(self.goBack)

    def upload(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Choose",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file:

            filename = os.path.basename(file)
            target = f"photos/uploads/{filename}"

            shutil.copy(file, target)

            photo = Photo(
                None,
                filename,
                target,
                0,
                self.user.userid
            )

            self.dao.insertPhoto(photo)

            QMessageBox.information(self, "OK", "Upload Success")

    def goBack(self):

        self.parent.show()
        self.close()