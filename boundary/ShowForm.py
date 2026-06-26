from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

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
        self.resize(600, 500)

        self.listWidget = QListWidget()
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(120, 120))
        self.listWidget.setGridSize(QSize(150, 160))
        self.listWidget.setResizeMode(QListView.Adjust)

        # 参数显示区域
        self.parameterLabel = QLabel("Select a photo to view parameters.")
        self.parameterLabel.setWordWrap(True)

        self.publicBtn = QPushButton("Make Public")
        self.deleteBtn = QPushButton("Delete")
        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.parameterLabel)
        layout.addWidget(self.publicBtn)
        layout.addWidget(self.deleteBtn)
        layout.addWidget(self.backBtn)

        self.setLayout(layout)

        self.loadData()

        # 点击图片显示参数
        self.listWidget.itemClicked.connect(self.showParameter)

        self.publicBtn.clicked.connect(self.makePublic)
        self.deleteBtn.clicked.connect(self.deletePhoto)
        self.backBtn.clicked.connect(self.goBack)

    def loadData(self):

        self.photos = self.service.getMyPhotos(self.user.userid)

        self.listWidget.clear()

        for p in self.photos:
            item = QListWidgetItem()
            item.setText(p.filename)
            item.setIcon(QIcon(p.filepath))
            self.listWidget.addItem(item)

    # 新增：显示参数
    def showParameter(self):

        row = self.listWidget.currentRow()

        if row < 0:
            return

        photo = self.photos[row]

        if not photo.parameter:
            self.parameterLabel.setText("No parameters.")
            return

        text = ""

        for p in photo.parameter:
            text += f"{p.name}: {p.value}\n"

        self.parameterLabel.setText(text)

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
        self.parameterLabel.setText("Select a photo to view parameters.")

    def goBack(self):

        self.parent.show()
        self.close()