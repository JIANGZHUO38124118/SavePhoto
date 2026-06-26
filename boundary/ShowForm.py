from PyQt5.QtWidgets import *

from control.ShowService import ShowService
from control.DeleteService import DeleteService


class ShowForm(QWidget):

    def __init__(self, parent, user):
        super().__init__()

        self.parent = parent
        self.user = user

        self.service = ShowService()
        self.deleteService = DeleteService()

        self.setWindowTitle("My Photos")
        self.resize(500, 400)

        self.listWidget = QListWidget()

        self.publicBtn = QPushButton("Make Public")
        self.deleteBtn = QPushButton("Delete")
        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.publicBtn)
        layout.addWidget(self.deleteBtn)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.loadData()

        self.publicBtn.clicked.connect(self.makePublic)
        self.deleteBtn.clicked.connect(self.deletePhoto)
        self.backBtn.clicked.connect(self.goBack)

    def loadData(self):

        self.photos = self.service.getMyPhotos(self.user.userid)

        self.listWidget.clear()

        for p in self.photos:
            self.listWidget.addItem(f"{p.photoid} - {p.filename}")

    def makePublic(self):

        row = self.listWidget.currentRow()

        if row < 0:
            return

        photo = self.photos[row]

        self.service.setPublic(photo.photoid)

        QMessageBox.information(self, "OK", "Now Public")

    def deletePhoto(self):

        row = self.listWidget.currentRow()

        if row < 0:
            return

        photo = self.photos[row]

        self.deleteService.delete(photo.photoid)

        self.loadData()

    def goBack(self):

        self.parent.show()
        self.close()