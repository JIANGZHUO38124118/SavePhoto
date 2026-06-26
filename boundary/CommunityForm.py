from PyQt5.QtWidgets import *

from control.ShowService import ShowService


class CommunityForm(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.service = ShowService()

        self.setWindowTitle("Community")
        self.resize(500, 400)

        self.listWidget = QListWidget()
        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.loadData()

        self.backBtn.clicked.connect(self.goBack)

    def loadData(self):

        photos = self.service.getPublicPhotos()

        self.listWidget.clear()

        for p in photos:
            self.listWidget.addItem(p.filename)

    def goBack(self):

        self.parent.show()
        self.close()