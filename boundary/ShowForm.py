from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt

from control.ShowService import ShowService
from control.DeleteService import DeleteService
from boundary.ImagePreviewDialog import ImagePreviewDialog


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

        self.parameterLabel = QLabel("Select a photo to view parameters.")
        self.parameterLabel.setWordWrap(True)

        # ⭐ 修改：初始按钮文本设为通用文本
        self.publicBtn = QPushButton("Public Status") 
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

        # 信号绑定
        self.listWidget.itemClicked.connect(self.showParameter)
        self.listWidget.itemDoubleClicked.connect(self.showImage)
        
        # ⭐ 绑定新的切换方法
        self.publicBtn.clicked.connect(self.togglePublic) 
        self.deleteBtn.clicked.connect(self.deletePhoto)
        self.backBtn.clicked.connect(self.goBack)

    def loadData(self):
        self.photos = self.service.getMyPhotos(self.user.userid)
        self.listWidget.clear()

        for p in self.photos:
            item = QListWidgetItem()
            # 可以在名字后面加上状态提示（可选）
            status = " [Public]" if p.visibility == 1 else " [Private]"
            item.setText(p.filename + status)
            item.setIcon(QIcon(p.filepath))
            self.listWidget.addItem(item)
            
        self.publicBtn.setText("Public Status") # 刷新后重置按钮字样

    def showImage(self):
        row = self.listWidget.currentRow()
        if row < 0:
            return
        dialog = ImagePreviewDialog(self.photos, row, self)
        dialog.exec_()

    def showParameter(self):
        row = self.listWidget.currentRow()
        if row < 0:
            return

        photo = self.photos[row]

        # ⭐ 新增：根据当前照片的可见性，动态改变按钮文字
        if photo.visibility == 1:
            self.publicBtn.setText("Unpublish (Make Private)")
        else:
            self.publicBtn.setText("Publish (Make Public)")

        if not photo.parameter:
            self.parameterLabel.setText("No parameters.")
            return

        text = ""
        for p in photo.parameter:
            text += f"{p.name}: {p.value}\n"
        self.parameterLabel.setText(text)

    # ⭐ 新增：双态切换核心方法
    def togglePublic(self):
        row = self.listWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a photo first.")
            return

        photo = self.photos[row]

        # 如果当前是公开的(1)，就转为私有(0)
        if photo.visibility == 1:
            self.service.setPrivate(photo.photoid)
            QMessageBox.information(self, "OK", "Photo is now Private.")
        else:
            # 如果当前是私有的(0)，就转为公开(1)
            self.service.setPublic(photo.photoid)
            QMessageBox.information(self, "OK", "Photo is now Public.")

        # 重新加载数据以刷新界面状态和按钮文字
        self.loadData()
        self.parameterLabel.setText("Select a photo to view parameters.")

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