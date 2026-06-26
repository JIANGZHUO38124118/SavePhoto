from PyQt5.QtWidgets import *

from boundary.UploadForm import UploadForm
from boundary.ShowForm import ShowForm


class PersonalForm(QWidget):

    def __init__(self, parent, user):
        super().__init__()

        self.parent = parent
        self.user = user

        self.setWindowTitle("Personal")
        self.resize(400, 300)

        self.uploadBtn = QPushButton("Upload Photo")
        self.showBtn = QPushButton("My Photos")
        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.uploadBtn)
        layout.addWidget(self.showBtn)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.uploadBtn.clicked.connect(self.openUpload)
        self.showBtn.clicked.connect(self.openShow)
        self.backBtn.clicked.connect(self.goBack)

    def openUpload(self):

        self.uploadForm = UploadForm(self, self.user)
        self.uploadForm.show()
        self.hide()

    def openShow(self):

        self.showForm = ShowForm(self, self.user)
        self.showForm.show()
        self.hide()

    def goBack(self):

        self.parent.show()
        self.close()