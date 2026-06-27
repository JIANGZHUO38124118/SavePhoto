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

        self.listWidget.itemClicked.connect(self.showParameter)
        self.listWidget.itemDoubleClicked.connect(self.showImage)
        

        self.publicBtn.clicked.connect(self.togglePublic) 
        self.deleteBtn.clicked.connect(self.deletePhoto)
        self.backBtn.clicked.connect(self.goBack)


    def showImage(self):
        row = self.listWidget.currentRow()
        if row < 0:
            return
        dialog = ImagePreviewDialog(self.photos, row, self)
        dialog.exec_()

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
            
        self.publicBtn.setText("Toggle Status")

    def showParameter(self):
        row = self.listWidget.currentRow()
        if row < 0:
            return

        photo = self.photos[row]

        if photo.isPublic():
            self.publicBtn.setText("Make Private")
        else:
            self.publicBtn.setText("Make Public")

        if not photo.parameter:
            self.parameterLabel.setText("No parameters.")
            return

        text = ""
        for p in photo.parameter:
            text += f"{p.key}: {p.value}\n"
        self.parameterLabel.setText(text)

    def togglePublic(self):
        row = self.listWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select a photo first.")
            return

        photo = self.photos[row]

        if photo.isPublic():
            self.service.unpublishPhoto(photo.photoid) 
            QMessageBox.information(self, "OK", "Photo is now Private.")
        else:
            self.service.publishPhoto(photo.photoid)
            QMessageBox.information(self, "OK", "Photo is now Public.")


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