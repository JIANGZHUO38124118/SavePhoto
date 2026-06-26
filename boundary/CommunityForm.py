from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from control.ShowService import ShowService


class CommunityForm(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.service = ShowService()

        self.setWindowTitle("Community")
        self.resize(500, 400)

        self.listWidget = QListWidget()
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(120, 120))
        self.listWidget.setGridSize(QSize(150, 160))
        self.listWidget.setResizeMode(QListView.Adjust)

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
            item = QListWidgetItem()
            item.setText(p.filename)
            item.setIcon(QIcon(p.path))
            self.listWidget.addItem(item)

    def goBack(self):

        self.parent.show()
        self.close()