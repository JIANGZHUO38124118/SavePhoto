from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from control.ShowService import ShowService
from boundary.ImagePreviewDialog import ImagePreviewDialog
from entity import Community


class CommunityForm(QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.service = ShowService()

        self.setWindowTitle("Community")
        self.resize(700, 500)

        self.listWidget = QListWidget()

        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(150, 150))
        self.listWidget.setGridSize(QSize(180, 180))
        self.listWidget.setResizeMode(QListView.Adjust)

        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()

        layout.addWidget(self.listWidget)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.loadData()

        self.backBtn.clicked.connect(self.goBack)

        self.listWidget.itemDoubleClicked.connect(
            self.showImage
        )

    def loadData(self):
        community_data = self.service.getPublicPhotos()
        
        self.photos = community_data.getPublicPhotos()
        
        self.listWidget.clear()
        for p in self.photos:
            item = QListWidgetItem()
            item.setText(p.filename)
            item.setIcon(QIcon(p.filepath))
            self.listWidget.addItem(item)

    def showImage(self):
        row = self.listWidget.currentRow()
        if row < 0:
            return

        dialog = ImagePreviewDialog(self.photos, row, self)
        dialog.exec_()

    def getPublicPhotos(self) -> Community:
        raw_public_photos = self.dao.findPublic()
        
        from dao.ParameterDAO import ParameterDAO
        param_dao = ParameterDAO()
        for photo in raw_public_photos:
            photo.parameter = param_dao.findByPhoto(photo.photoid)
            
        return Community(communityId=1, publicPhotos=raw_public_photos)

    def goBack(self):
        self.parent.show()
        self.close()