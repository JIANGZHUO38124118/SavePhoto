from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

from control.ShowService import ShowService
from boundary.ImagePreviewDialog import ImagePreviewDialog


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

        # 双击查看大图
        self.listWidget.itemDoubleClicked.connect(
            self.showImage
        )

    def loadData(self):

        self.photos = self.service.getPublicPhotos()

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

        # ⭐ 传入完整的照片列表和当前点击的索引位置
        dialog = ImagePreviewDialog(self.photos, row, self)
        dialog.exec_()

    def goBack(self):
        self.parent.show()  # 显示主菜单 MainForm
        self.close()