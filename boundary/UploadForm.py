import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt

from control.UploadService import UploadService
from entity.Photo import Photo
from entity.Parameter import Parameter
from entity.PhotoVisibility import PhotoVisibility


class UploadForm(QWidget):

    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user
        self.uploadService = UploadService()

        self.setWindowTitle("Upload Photo")
        self.resize(550, 600)

        self.param_rows = []

        self.btnSelect = QPushButton("Select Photo")
        self.lblPath = QLabel("No file selected")
        self.lblPath.setWordWrap(True)

        self.txtFileName = QLineEdit()
        self.txtFileName.setPlaceholderText("Enter photo name (Required)")

        self.txtDate = QLineEdit()
        self.txtDate.setPlaceholderText("例如：2026年06月27日 (Required)")

        self.paramContainer = QWidget()
        self.paramLayout = QVBoxLayout(self.paramContainer)
        self.paramLayout.setContentsMargins(0, 0, 0, 0)

        self.btnAddParam = QPushButton("+ Add Parameter")
        self.btnAddParam.setStyleSheet("QPushButton { background-color: #28a745; color: white; font-weight: bold; }")

        self.btnUpload = QPushButton("Upload")
        self.btnBack = QPushButton("Back")

        formLayout = QFormLayout()
        formLayout.addRow("Selected File:", self.lblPath)
        formLayout.addRow("Photo Name *:", self.txtFileName)
        formLayout.addRow("Upload Date *:", self.txtDate)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scrollContent = QWidget()
        scrollLayout = QVBoxLayout(scrollContent)
        
        scrollLayout.addLayout(formLayout)
        scrollLayout.addWidget(QLabel("<b>Custom Parameters (Optional):</b>"))
        scrollLayout.addWidget(self.paramContainer)
        scrollLayout.addWidget(self.btnAddParam)
        scrollLayout.addSpacing(10)
        scrollLayout.addWidget(self.btnUpload)
        scrollLayout.addWidget(self.btnBack)
        
        scroll.setWidget(scrollContent)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.btnSelect)
        mainLayout.addWidget(scroll)
        self.setLayout(mainLayout)

        self.btnSelect.clicked.connect(self.selectPhoto)
        self.btnAddParam.clicked.connect(self.addParameterRow)
        self.btnUpload.clicked.connect(self.uploadPhoto)
        self.btnBack.clicked.connect(self.goBack)

        self.selected_filepath = ""

        self.addParameterRow()

    def addParameterRow(self):
        rowWidget = QWidget()
        hLayout = QHBoxLayout(rowWidget)
        hLayout.setContentsMargins(0, 2, 0, 2)

        txtKey = QLineEdit()
        txtKey.setPlaceholderText("Key (e.g., ISO)")
        txtValue = QLineEdit()
        txtValue.setPlaceholderText("Value (e.g., 400)")

        btnDeleteRow = QPushButton("X")
        btnDeleteRow.setFixedWidth(30)
        btnDeleteRow.setStyleSheet("color: red; font-weight: bold;")

        hLayout.addWidget(txtKey)
        hLayout.addWidget(txtValue)
        hLayout.addWidget(btnDeleteRow)

        self.paramLayout.addWidget(rowWidget)

        row_data = (txtKey, txtValue, rowWidget)
        self.param_rows.append(row_data)

        btnDeleteRow.clicked.connect(lambda: self.removeParameterRow(row_data))

    def removeParameterRow(self, row_data):
        txtKey, txtValue, rowWidget = row_data
        if row_data in self.param_rows:
            self.param_rows.remove(row_data)
            self.paramLayout.removeWidget(rowWidget)
            rowWidget.deleteLater()

    def selectPhoto(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.selected_filepath = file_path
            self.lblPath.setText(file_path)
            filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
            self.txtFileName.setText(filename_without_ext)

    def uploadPhoto(self):
        if not self.selected_filepath:
            QMessageBox.warning(self, "Warning", "Please select a photo first!")
            return

        filename = self.txtFileName.text().strip()
        if not filename:
            QMessageBox.warning(self, "Warning", "Photo Name is required!")
            return

        upload_date_str = self.txtDate.text().strip()
        if not upload_date_str:
            QMessageBox.warning(self, "Warning", "Upload Date is required!")
            return

        parameter_list = []
        for txtKey, txtValue, _ in self.param_rows:
            key = txtKey.text().strip()
            value = txtValue.text().strip()
            if key:
                parameter_list.append(Parameter(key=key, value=value))

        parameter_list.append(Parameter(key="Upload Date", value=upload_date_str))

        photo_entity = Photo(
            photoid=0,
            filename=filename,
            filepath=self.selected_filepath,
            visibility=PhotoVisibility.PRIVATE,
            owner=self.user.userid,
            parameter=parameter_list
        )

        success = self.uploadService.uploadPhoto(photo_entity, parameter_list)

        if success:
            QMessageBox.information(self, "Success", "Photo uploaded successfully with parameters!")
            self.clearForm()
        else:
            QMessageBox.critical(self, "Error", "Upload failed.")

    def clearForm(self):
        self.selected_filepath = ""
        self.lblPath.setText("No file selected")
        self.txtFileName.clear()
        self.txtDate.clear()

        for _, _, rowWidget in self.param_rows:
            self.paramLayout.removeWidget(rowWidget)
            rowWidget.deleteLater()
        self.param_rows.clear()
        self.addParameterRow()

    def goBack(self):
        self.parent.show()
        self.close()