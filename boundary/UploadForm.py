from PyQt5.QtWidgets import *
import shutil
import os

from dao.PhotoDAO import PhotoDAO
from dao.ParameterDAO import ParameterDAO
from entity.Photo import Photo
from entity.Parameter import Parameter


class UploadForm(QWidget):

    def __init__(self, parent, user):
        super().__init__()

        self.parent = parent
        self.user = user

        self.photoDao = PhotoDAO()
        self.parameterDao = ParameterDAO()

        self.file = ""
        self.parameters = []

        self.setWindowTitle("Upload")
        self.resize(400, 500)

        self.chooseBtn = QPushButton("Choose Image")

        self.nameEdit = QLineEdit()
        self.nameEdit.setPlaceholderText("Parameter Name")

        self.valueEdit = QLineEdit()
        self.valueEdit.setPlaceholderText("Parameter Value")

        self.addBtn = QPushButton("Add Parameter")

        self.parameterList = QListWidget()

        self.uploadBtn = QPushButton("Upload")

        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()

        layout.addWidget(self.chooseBtn)
        layout.addWidget(self.nameEdit)
        layout.addWidget(self.valueEdit)
        layout.addWidget(self.addBtn)
        layout.addWidget(self.parameterList)
        layout.addWidget(self.uploadBtn)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.chooseBtn.clicked.connect(self.chooseImage)
        self.addBtn.clicked.connect(self.addParameter)
        self.uploadBtn.clicked.connect(self.upload)
        self.backBtn.clicked.connect(self.goBack)

    def chooseImage(self):

        self.file, _ = QFileDialog.getOpenFileName(
            self,
            "Choose",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

    def addParameter(self):

        name = self.nameEdit.text().strip()
        value = self.valueEdit.text().strip()

        if name == "" or value == "":
            return

        self.parameters.append((name, value))

        self.parameterList.addItem(f"{name} : {value}")

        self.nameEdit.clear()
        self.valueEdit.clear()

    def upload(self):

        if self.file == "":
            QMessageBox.warning(self, "Error", "Please choose an image.")
            return

        os.makedirs("photos/uploads", exist_ok=True)

        filename = os.path.basename(self.file)

        target = f"photos/uploads/{filename}"

        shutil.copy(self.file, target)

        photo = Photo(
            None,
            filename,
            target,
            0,
            self.user.userid,
            None
        )

        photoid = self.photoDao.insertPhoto(photo)

        for name, value in self.parameters:

            parameter = Parameter(
                None,
                photoid,
                name,
                value
            )

            self.parameterDao.insertParameter(parameter)

        QMessageBox.information(self, "OK", "Upload Success")

        self.parameters.clear()
        self.parameterList.clear()

    def goBack(self):

        self.parent.show()
        self.close()