# boundary/ShowForm.py
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
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
        self.resize(600, 480)

        self.listWidget = QListWidget()
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(120, 120))
        self.listWidget.setGridSize(QSize(150, 150))
        self.listWidget.setResizeMode(QListView.Adjust)

        self.deleteBtn = QPushButton("Delete Selected Photo")
        self.backBtn = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.deleteBtn)
        layout.addWidget(self.backBtn)
        self.setLayout(layout)

        self.loadData()
        self.listWidget.itemDoubleClicked.connect(self.showImage)
        self.deleteBtn.clicked.connect(self.deletePhoto)
        self.backBtn.clicked.connect(self.goBack)

    def loadData(self):
        personal_data = self.service.getMyPhotos(self.user.userid)
        self.photos = personal_data.getPhotos()
        
        self.listWidget.clear()
        for p in self.photos:
            item = QListWidgetItem()
            status = " [Public]" if p.isPublic() else " [Private]"
            item.setText(p.filename + status) 
            item.setIcon(QIcon(p.filepath))
            self.listWidget.addItem(item)

    def showImage(self):
        row = self.listWidget.currentRow()
        if row < 0: return
        
        dialog = ImagePreviewDialog(self.photos, row, self.user, mode="personal", parent=self)
        dialog.exec_()
        
        self.loadData() 

    def deletePhoto(self):
        row = self.listWidget.currentRow()
        if row < 0: 
            QMessageBox.warning(self, "Warning", "Please select a photo to delete.")
            return
        
        reply = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this photo?", 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            photo = self.photos[row]
            self.deleteService.delete(photo.photoid)
            self.loadData()

    def goBack(self):
        self.parent.show()
        self.close()